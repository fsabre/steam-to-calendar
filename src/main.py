from pathlib import Path
from typing import List, Tuple

import click

from .config import DEFAULT_DATA_FILE, DEFAULT_EXPORT_FILE, DrawConfig, ExportMode, FetchConfig
from .drawing import draw_html_calendar, draw_text_calendar
from .logger import logger
from .models import Game
from .parsing import MyWebDriver
from .storage import load_from_file, save_to_file


def fetch(config: FetchConfig) -> None:
    """Fetch data by scraping Steam with Selenium."""

    driver = MyWebDriver(config=config)

    try:
        games = driver.get_game_list()

        # List of games whose achievements will be fetched
        games_to_parse_achiev: List[Game] = games

        if config.no_achievements:
            logger.info("Skipping the achievements fetch")
            games_to_parse_achiev = []
        elif config.only_achievements_for:
            logger.info("Fetching achievements of those games : %s", config.only_achievements_for)
            games_to_parse_achiev = [g for g in games_to_parse_achiev if g.id in config.only_achievements_for]
        else:
            logger.info("Fetching achievements of all games")

        for game in games_to_parse_achiev:
            logger.info("Fetching achievements of '%s'", game.name)
            game.events = driver.get_achievements_events(game.id)

        save_to_file(games, config=config)

    finally:
        driver.quit()


def draw(config: DrawConfig) -> None:
    games = load_from_file(config.data_file)
    if config.mode == "text":
        draw_text_calendar(games, config=config)
    else:
        draw_html_calendar(games, config=config)


@click.group()
def main_cli():
    """View your Steam history on a calendar."""


@main_cli.command("fetch")
@click.argument("steam_profile_url")
@click.option("-na", "--no-achievements", is_flag=True, help="Don't fetch the achievements dates")
@click.option(
    "-oa",
    "--only-achievements-for",
    multiple=True,
    help="Only fetch the achievements dates of games with those ID"
)
@click.option(
    "-o", "--output",
    type=click.Path(dir_okay=False, writable=True, path_type=Path),
    default=DEFAULT_DATA_FILE,
    show_default=True,
    help="Path of the data file to write",
)
def fetch_command(
    steam_profile_url: str,
    no_achievements: bool,
    only_achievements_for: Tuple[str, ...],
    output: Path
) -> None:
    """Fetch the Steam data and save it to a file.

    You can find your STEAM_PROFILE_URL by looking at your profile URL."""
    config = FetchConfig(
        profile_url=steam_profile_url,
        no_achievements=no_achievements,
        only_achievements_for=only_achievements_for,
        destination_file=output,
    )
    fetch(config)


@main_cli.command("draw")
@click.option(
    "-m", "--mode",
    type=click.Choice(["text", "html"], case_sensitive=False),
    default="html",
    show_default=True,
    help="Change the output mode",
)
@click.option(
    "-f", "--file",
    type=click.Path(exists=True, dir_okay=False, readable=True, path_type=Path),
    default=DEFAULT_DATA_FILE,
    show_default=True,
    help="Path of the data file to parse",
)
@click.option(
    "-o", "--output",
    type=click.Path(dir_okay=False, writable=True, path_type=Path),
    default=DEFAULT_EXPORT_FILE,
    show_default=True,
    help="Path of the calendar export",
)
def draw_command(mode: ExportMode, file: Path, output: Path) -> None:
    """Draw the dates of a data file as a calendar."""
    config = DrawConfig(mode=mode, data_file=file, export_file=output)
    draw(config)
