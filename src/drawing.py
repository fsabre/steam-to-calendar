import calendar
import contextlib
import itertools
from collections import defaultdict
from datetime import datetime
from typing import Dict, Generator, List, Optional, Set, Tuple, TypedDict

import jinja2

from .config import ROOT_PATH
from .logger import logger
from .models import Game

cal = calendar.Calendar()

# TEXT CALENDAR

YearMonth = Tuple[int, int]
PreparedTextData = Dict[YearMonth, Dict[str, List[datetime]]]


def prepare_data_for_text(games: List[Game]) -> Tuple[PreparedTextData, datetime, datetime]:
    """Convert the game list to a structure of datetimes to be displayed.
    Also provide the earliest and latest datetimes.
    """
    logger.info("Prepare the data for text display")
    output: PreparedTextData = defaultdict(lambda: defaultdict(list))
    earliest_date: Optional[datetime] = None
    latest_date: Optional[datetime] = None

    for game in games:
        for date in game.achievement_dates:
            if date is None:
                continue
            year_month: YearMonth = (date.year, date.month)
            output[year_month][game.name].append(date)
            if earliest_date is None or date < earliest_date:
                earliest_date = date
            if latest_date is None or date > latest_date:
                latest_date = date
    return output, earliest_date, latest_date


def range_year_month(start: datetime, end: datetime) -> Generator[YearMonth, None, None]:
    """Return all the couples (year, month) between two dates."""
    # Build all the couples (year, months)
    i1 = itertools.product(range(start.year, end.year + 1), range(1, 12 + 1))
    # Skip the start of the first year
    i2 = itertools.dropwhile(lambda a: a[1] != start.month, i1)
    # Skip the end of the last year
    i3 = itertools.takewhile(lambda a: a[0] != end.year or a[1] <= end.month, i2)
    yield from i3


def draw_text_line(year: int, month: int, game: str, dates: List[datetime]) -> None:
    """Draw a game line."""
    days_to_mark = set(date.day for date in dates)
    output = []
    for day in cal.itermonthdays(year, month):
        if day == 0:
            output.append(" ")
        elif day in days_to_mark:
            output.append("X")
        else:
            output.append(".")
    formatted_name = game[0:16]
    print(f"{formatted_name:19}\t" + "\t".join(output))


def draw_text_month(year: int, month: int, games: Dict[str, List[datetime]]) -> None:
    """Draw a month line and its games lines."""
    month_label = f"----- {str(month).zfill(2)}/{year} -----"
    days_numbers = "\t".join(str(day) if day != 0 else " " for day in cal.itermonthdays(year, month))
    print(month_label + "\t" + days_numbers)
    for game, dates in games.items():
        draw_text_line(year, month, game, dates)


def draw_text_calendar(games: List[Game]) -> None:
    """Draw the whole calendar as text."""
    data, start, end = prepare_data_for_text(games)
    destination_file = ROOT_PATH / "cal.txt"
    with destination_file.open("w") as file:
        logger.info("Export the calendar as text to %s", destination_file)
        with contextlib.redirect_stdout(file):
            for year_month in range_year_month(start, end):
                year, month = year_month
                draw_text_month(year, month, data[year_month])


# HTMl CALENDAR

class GameHTMLData(TypedDict):
    name: str
    dates: Set[int]


class MonthHTMLData(TypedDict):
    year: int
    month: int
    days: List[int]
    games: List[GameHTMLData]


PreparedHTMLData = List[MonthHTMLData]


def prepare_data_for_html(games: List[Game]) -> PreparedHTMLData:
    """Convert the game list to a structure to be displayed.
    It's easier to prepare the data in Python than in Jinja2.
    But now it must be ordered.
    """
    logger.info("Prepare the data for HTML display")
    output: PreparedHTMLData = []

    # I'm going to use the text data, it's more convenient that starting to
    # iterate on games again.
    text_data, start, end = prepare_data_for_text(games)

    for year_month in range_year_month(start, end):
        year, month = year_month
        games: List[GameHTMLData] = []
        # All YearMonth doesn't exist in text_data, so we have to check that the
        # current one is present.
        if year_month in text_data:
            for old_game_name, old_date_list in text_data[year_month].items():
                game: GameHTMLData = dict(
                    name=old_game_name,
                    dates={date.day for date in old_date_list},
                )
                games.append(game)
        month_html_data: MonthHTMLData = dict(
            year=year,
            month=month,
            days=list(cal.itermonthdays(year, month)),
            games=games,
        )
        output.append(month_html_data)
    return output


def draw_html_calendar(games: List[Game]) -> None:
    """Draw the whole calendar as HTML."""
    # Create the jinja environment
    jinja_env = jinja2.Environment(
        loader=jinja2.PackageLoader("src"),
        autoescape=jinja2.select_autoescape(),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = jinja_env.get_template("html_calendar.jinja2")
    # Prepare the data
    data = prepare_data_for_html(games)
    # Render the template to a file
    destination_file = ROOT_PATH / "cal.html"
    with destination_file.open("w", encoding="utf8") as file:
        logger.info("Export the calendar as HTML to %s", destination_file)
        rendered = template.render(
            data=data,
        )
        file.write(rendered)
