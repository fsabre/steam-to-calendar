import calendar
import contextlib
import itertools
from collections import defaultdict
from datetime import datetime
from typing import Dict, Generator, List, Optional, Tuple

from .config import ROOT_PATH
from .models import Game

YearMonth = Tuple[int, int]
TotalData = Dict[YearMonth, Dict[str, List[datetime]]]

cal = calendar.Calendar()


def prepare_data(games: List[Game]) -> Tuple[TotalData, datetime, datetime]:
    """Convert the game list to a structure of datetimes to be displayed.
    Also provide the earliest and latest datetimes.
    """
    output: TotalData = defaultdict(lambda: defaultdict(list))
    earliest_date: Optional[datetime] = None
    latest_date: Optional[datetime] = None

    for game in games:
        for date in (game.min_achievement_date, game.max_achievement_date):
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


def draw_line(year: int, month: int, game: str, dates: List[datetime]) -> None:
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
    formatted_name = game[0:9]
    print(f"{formatted_name:10}\t" + "\t".join(output))


def draw_month(year: int, month: int, games: Dict[str, List[datetime]]) -> None:
    """Draw a month line and its games lines."""
    print(f"--- {str(month).zfill(2)}/{year} ---")
    print(" " * 10 + "\t" + "\t".join(str(day) if day != 0 else " " for day in cal.itermonthdays(year, month)))
    for game, dates in games.items():
        draw_line(year, month, game, dates)


def draw_calendar(games: List[Game]) -> None:
    """Draw the whole calendar as text."""
    data, start, end = prepare_data(games)
    with (ROOT_PATH / "cal.txt").open("w") as file:
        with contextlib.redirect_stdout(file):
            for year_month in range_year_month(start, end):
                year, month = year_month
                draw_month(year, month, data[year_month])
