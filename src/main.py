import click
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from .config import CHROME_DRIVER_PATH, CHROME_PATH, Config
from .logger import logger
from .parsing import get_achievements_interval, retrieve_game_list
from .storage import save_to_file


def fetch(config: Config) -> None:
    """Fetch data by scraping Steam with Selenium."""
    logger.info("Start the Web driver")
    service = Service(executable_path=CHROME_DRIVER_PATH)
    options = Options()
    options.binary_location = CHROME_PATH
    options.add_argument("--lang=en")  # Use the english language to allow parsing
    driver = webdriver.Chrome(service=service, options=options)

    try:
        games = retrieve_game_list(driver, config)

        for game in games:
            logger.info("Fetching achievements dates of '%s'", game.name)
            dates_interval = get_achievements_interval(driver, game.id)
            (game.min_achievement_date, game.max_achievement_date) = dates_interval

        save_to_file(games, config)

    finally:
        logger.info("Quit the Web driver")
        driver.quit()


@click.group()
def main_cli():
    """View your Steam history on a calendar."""


@main_cli.command("fetch")
@click.argument("steam_id")
def fetch_command(steam_id: str) -> None:
    """Fetch the Steam data and save it to a file.

    You can find your STEAM_ID by looking at your profile URL."""
    fetch(Config(username=steam_id))
