import re
from datetime import datetime
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from .config import CHROME_DRIVER_PATH, CHROME_PATH, Config
from .logger import logger
from .models import Game


class MyWebDriver:
    """Custom wrapper for the selenium web driver."""

    def __init__(self, config: Config) -> None:
        logger.info("Start the Web driver")
        service = Service(executable_path=CHROME_DRIVER_PATH)
        options = Options()
        options.binary_location = CHROME_PATH
        options.add_argument("--lang=en")  # Use the english language to allow parsing

        self.driver = webdriver.Chrome(service=service, options=options)
        self.config = config

    def quit(self) -> None:
        logger.info("Quit the Web driver")
        self.driver.quit()

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
        if len(game_rows) == 0:
            logger.warning("No game row found")

        for game_row in game_rows:
            game_id_raw: str = game_row.get_attribute("id")
            if game_id_raw is None:
                logger.warning("No game ID found for this row")
                game_id = None
            else:
                # Use a regex to retrieve the ID of the game
                game_id_match = re.match(r"game_(\d+)", game_id_raw)
                if game_id_match is None:
                    logger.warning("Game ID badly formatted : %s", game_id_raw)
                    game_id = None
                else:
                    game_id = int(game_id_match.group(1))

            game_name: str = game_row.find_element(By.CSS_SELECTOR, '.gameListRowItemName').text
            game = Game(id=game_id, name=game_name)
            games.append(game)

        return games

    def get_achievements_dates(self, game_id: int) -> List[datetime]:
        """Fetch the unlocking date of each achievement of a game.

        :param game_id: The Steam ID of the game
        :rtype: List[datetime]
        :return: The unlocking date of each achievement
        """
        achievement_url = self.config.achievements_url(game_id)
        self.driver.get(achievement_url)

        all_dates: List[datetime] = []
        for date_element in self.driver.find_elements(By.CLASS_NAME, "achieveUnlockTime"):
            raw_date: str = date_element.text
            # logger.debug("Raw date : %s", raw_date)
            try:
                date = datetime.strptime(raw_date, "Unlocked %d %b, %Y @ %I:%M%p")
                # logger.debug("Parsed date : %s", date)
                all_dates.append(date)
            except ValueError:
                try:
                    date = datetime.strptime(raw_date, "Unlocked %d %b @ %I:%M%p")
                    # logger.debug("Parsed date : %s", date)
                    all_dates.append(date)
                except ValueError as err:
                    logger.error("Error when parsing : %s", raw_date, err)

        # logger.debug("All dates parsed : %s", all_dates)
        return all_dates
