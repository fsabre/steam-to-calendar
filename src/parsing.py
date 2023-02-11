"""Define the webscraping functions."""

import contextlib
import re
from datetime import datetime, timezone, timedelta
from typing import List, Optional

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from . import exceptions
from .config import CHROME_DRIVER_PATH, CHROME_PATH, FetchConfig, LOGIN_PAGE
from .logger import logger
from .models import Event, Game


class MyWebDriver:
    """Custom wrapper for the selenium web driver."""

    def __init__(self, config: FetchConfig) -> None:
        logger.info("Start the Web driver")
        service = Service(executable_path=CHROME_DRIVER_PATH)
        options = Options()
        options.binary_location = CHROME_PATH
        options.add_argument("--lang=en")  # Use the english language to allow parsing
        options.add_experimental_option(
            'excludeSwitches', ['enable-logging']  # Disable selenium logging
        )

        self.driver = webdriver.Chrome(service=service, options=options)
        # Load one page from the hostname to prepare cookies
        self.driver.get("https://steamcommunity.com")  # TODO Too heavy, find a lighter page
        self.config = config

    def quit(self) -> None:
        """Quit the webdriver."""
        logger.info("Quit the Web driver")
        self.driver.quit()

    def get_page_timezone_offset(self) -> int:
        """Return the timezone offset in seconds provided by the Steam cookie."""
        offset_cookie = self.driver.get_cookie("timezoneOffset")
        if offset_cookie is not None:
            raw_offset: str = offset_cookie["value"]
            # Convert the part before "," or "." to an integer
            return int(raw_offset.replace(",", ".").partition(".")[0])
        return 0

    def is_user_connected(self) -> bool:
        """Return True if a user is connected."""
        # The user is connected if their avatar is found.
        avatar_element = self.driver.find_element(By.CSS_SELECTOR, ".user_avatar")
        # user_profile_url = avatar_element.get_attribute("href")
        return avatar_element is not None

    def log_in_user(self) -> None:
        """Redirect to the login page and wait for the user to login."""
        logger.info("Go to login page")
        self.driver.get(LOGIN_PAGE)

        logger.debug("Wait for the user to login")
        try:
            WebDriverWait(self.driver, timeout=3600) \
                .until(lambda d: self.is_user_connected())
        except TimeoutException:
            raise exceptions.TimeoutException("Waited too long (1h) for user login")
        logger.info("Logged in user detected")

    def get_game_list(self) -> List[Game]:
        """Fetch the user Steam game page.

        :rtype: List[Game]
        :return: A list of Game filled with names and ID
        """

        games: List[Game] = []
        games_url = self.config.games_url()

        logger.debug("Open the page %s", games_url)
        self.driver.get(games_url)

        logger.debug("Look for game rows")
        game_rows = self.driver.find_elements(By.CSS_SELECTOR, ".gameListRow")
        game_rows_count: int = len(game_rows)
        if game_rows_count <= 0:
            logger.warning(
                "No game row found. "
                "Maybe this profile is private ? Try with the --login option."
            )
        else:
            logger.info("%d game rows found", game_rows_count)

        for game_row in game_rows:
            # Parse the ID of the game
            game_id_raw: str = game_row.get_attribute("id")
            if game_id_raw is None:
                logger.warning("No game ID found for this row")
                continue
            # Use a regex to retrieve the ID of the game
            game_id_match = re.match(r"game_(\d+)", game_id_raw)
            if game_id_match is None:
                logger.warning("Game ID badly formatted : %s", game_id_raw)
                continue
            game_id = game_id_match.group(1)

            # Parse the name of the game
            game_name: str = game_row.find_element(By.CSS_SELECTOR, '.gameListRowItemName').text

            # Append the game to game list
            game = Game(id=game_id, name=game_name)
            games.append(game)

        return games

    def get_achievements_events(self, game_id: str) -> List[Event]:
        """Fetch the event of each achievement of a game.

        :param game_id: The Steam ID of the game
        :return: A list of achievement events
        """
        url = self.config.achievements_url(game_id)
        # The page must be in english to be parsed.
        # So I set a cookie to force it in english.
        # But if there's a redirection, the cookie is changed by the connected
        # user language. In that case, I set again the cookie, then refresh.
        for try_no in range(1, 6):
            logger.debug("Open the page %s (try %s)", url, try_no)
            self.driver.add_cookie({"name": "Steam_Language", "value": "english"})
            self.driver.get(url)
            lang = self.driver.find_element(By.CSS_SELECTOR, "html").get_attribute("lang")
            if lang == "en":
                break
            url = self.driver.current_url
        else:
            logger.warning("Couldn't load %s in english", url)

        text: str = self.driver.page_source
        soup = BeautifulSoup(text, "html.parser")

        timezone_offset: int = self.get_page_timezone_offset()
        new_tzinfo = timezone(timedelta(seconds=timezone_offset))

        all_events: List[Event] = []

        for web_element in soup.find_all(class_="achieveTxtHolder"):
            title: str = web_element.find("h3").text
            desc: str = web_element.find("h5").text
            date_element = web_element.find(class_="achieveUnlockTime")
            # The unlocking date may not be there, because the achievement may
            # not be unlocked. In that case, we skip it.
            if date_element is None:
                continue
            raw_date: str = date_element.text.strip()
            date: Optional[datetime] = understand_date(raw_date)
            if date is not None:
                # Add the timezone info
                date = date.replace(tzinfo=new_tzinfo)

                # logger.debug("'%s' -> %s", raw_date, date)
                event = Event.create_achievement_event(
                    # Store an UTC datetime
                    event_date=date.astimezone(timezone.utc),
                    title=title,
                    desc=desc,
                )
                all_events.append(event)
            else:
                logger.error("Couldn't parse '%s'", raw_date)

        logger.debug("Found {%s} achievements", len(all_events))
        return all_events


def understand_date(raw: str) -> Optional[datetime]:
    """Convert a formatted date into a datetime object.

    :param raw: The formatted date
    :return: The datetime object or None
    """
    with contextlib.suppress(ValueError):
        return datetime.strptime(raw, "Unlocked %d %b, %Y @ %I:%M%p")
    with contextlib.suppress(ValueError):
        parsed = datetime.strptime(raw, "Unlocked %d %b @ %I:%M%p")
        filled = parsed.replace(year=datetime.now().year)
        return filled
    return None
