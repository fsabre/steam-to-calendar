import click

from .config import Config, DEFAULT_DATA_FILE
from .drawing import draw_html_calendar, draw_text_calendar
from .logger import logger
from .parsing import MyWebDriver
from .storage import load_from_file, save_to_file


def fetch(config: Config) -> None:
    """Fetch data by scraping Steam with Selenium."""

    driver = MyWebDriver(config=config)

    try:
        games = driver.get_game_list()

        if config.no_achievements:
            logger.info("Skipping the achievements fetch")
        else:
            for game in games:
                logger.info("Fetching achievements dates of '%s'", game.name)
                dates = driver.get_achievements_dates(game.id)

                game.achievement_dates = dates
                if dates:
                    game.min_achievement_date = min(dates)
                    game.max_achievement_date = max(dates)

        save_to_file(games, config=config)

    finally:
        driver.quit()


def draw(mode: str) -> None:
    games = load_from_file(DEFAULT_DATA_FILE)
    if mode == "text":
        draw_text_calendar(games)
    else:
        draw_html_calendar(games)


@click.group()
def main_cli():
    """View your Steam history on a calendar."""


@main_cli.command("fetch")
@click.argument("steam_id")
@click.option("-na", "--no-achievements", is_flag=True, help="Don't fetch the achievements dates")
def fetch_command(steam_id: str, no_achievements: bool) -> None:
    """Fetch the Steam data and save it to a file.

    You can find your STEAM_ID by looking at your profile URL."""
    config = Config(username=steam_id, no_achievements=no_achievements)
    fetch(config)


@main_cli.command("draw")
@click.option(
    "-m", "--mode",
    type=click.Choice(["text", "html"], case_sensitive=False),
    default="html",
    show_default=True,
    help="Change the output mode",
)
def draw_command(mode: str) -> None:
    """Draw the dates of a data file as a calendar."""
    draw(mode)
