import re
from datetime import datetime
from typing import List, Optional, Tuple

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from .config import Config
from .logger import logger
from .models import Game


def retrieve_game_list(driver: WebDriver, config: Config) -> List[Game]:
    """Create a list of Game filled with names and ID."""

    games: List[Game] = []

    logger.debug("Open the page %s", config.games_url)
    driver.get(config.games_url())

    logger.debug("Look for game rows")
    game_rows = driver.find_elements(By.CSS_SELECTOR, ".gameListRow")
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


def get_achievements_interval(
    driver: WebDriver, config: Config, game_id: int
) -> Tuple[Optional[datetime], Optional[datetime]]:
    """Find the first and last achievement date for a game."""
    driver.get(config.achievements_url(game_id))

    all_dates: List[datetime] = []
    for date_element in driver.find_elements(By.CLASS_NAME, "achieveUnlockTime"):
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

    # If no date has been found
    if not all_dates:
        return None, None

    logger.debug("All dates parsed : %s", all_dates)
    return min(all_dates), max(all_dates)
