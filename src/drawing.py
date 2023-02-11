"""Define the functions to prepare the calendar data and render it to a file."""

import calendar
import contextlib
import itertools
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Generator, List, Optional, Tuple

import jinja2

from .config import DrawConfig
from .logger import logger
from .models import Event, Game

cal = calendar.Calendar()

YearMonth = Tuple[int, int]


@dataclass
class PrepDay:
    day: int
    event_count: int
    events: List[Event]


@dataclass
class PrepLine:
    game_name: str
    days: List[PrepDay]


@dataclass
class PrepMonth:
    year: int
    month: int
    days: List[int]
    lines: List[PrepLine]


def get_days_in_month(year: int, month: int, padding=True) -> List[int]:
    """Return the days numbers in a month.
    :param year: The year of the month
    :param month: The number of the month
    :param padding: Whether to keep the 0 at the start to match the other
        month's alignment (the first 0 is a monday)
    :return: The list of days numbers
    """
    generator = cal.itermonthdays(year, month)
    if padding is False:
        generator = filter(lambda d: d != 0, generator)
    return list(generator)


def range_year_month(start: datetime, end: datetime) -> Generator[YearMonth, None, None]:
    """Return all the couples (year, month) between two dates."""
    # Build all the couples (year, months)
    i1 = itertools.product(range(start.year, end.year + 1), range(1, 12 + 1))
    # Skip the start of the first year
    i2 = itertools.dropwhile(lambda a: a[1] != start.month, i1)
    # Skip the end of the last year
    i3 = itertools.takewhile(lambda a: a[0] != end.year or a[1] <= end.month, i2)
    yield from i3


def prepare_data_for_display(games: List[Game]) -> Optional[List[PrepMonth]]:
    """Return a structure of months, lines, days and events suitable for
    display.
    :param games: The list of games and events to prepare
    :return: The convenient data structure, or None if no events have been found
    """
    earliest_date: Optional[datetime] = None
    latest_date: Optional[datetime] = None

    # The aim is not to spend useless time processing the data.
    # Thus, we are doing two loops :
    # - One over all events, to group them by month, game and day.
    # - One over all months, to constitute the final data structure.

    # 1. Group the events

    # The following definition is a bit strange. The aim is to use
    # grouped_events[(year, month)][game_name][day] to get a list of events.
    # The defaultdict structure create itself as we use the object.
    grouped_events: Dict[YearMonth, Dict[str, Dict[int, List[Event]]]]
    grouped_events = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for game in games:
        for event in game.events:
            # Use the local timezone
            date: datetime = event.date.astimezone(tz=None)
            event.date = date
            year_month: YearMonth = (date.year, date.month)
            # Insert the event at the right place in grouped_events
            grouped_events[year_month][game.name][date.day].append(event)
            # Update the min/max dates in order to know which months to display
            if earliest_date is None or date < earliest_date:
                earliest_date = date
            if latest_date is None or date > latest_date:
                latest_date = date

    if earliest_date is None:  # latest_date will be None too
        return None

    # 2. Create a structure with all the months

    rv: List[PrepMonth] = []
    for ym in range_year_month(earliest_date, latest_date):
        days_in_months: List[int] = get_days_in_month(ym[0], ym[1])
        lines_data: List[PrepLine] = []
        # If there's an event this month, that means there's a game, so we have
        # to add a line to the month data.
        if ym in grouped_events:
            for game_name, days in grouped_events[ym].items():
                # The line must be filled with a PrepDay for every day of the
                # current month. Those PrepDay must also be filled with a list
                # of events that occurred this day and belong to this line.
                days_data: List[PrepDay] = []
                for day in days_in_months:
                    event_list: List[Event] = grouped_events[ym][game_name][day]
                    day_data = PrepDay(
                        day=day,
                        event_count=len(event_list),
                        events=event_list,
                    )
                    days_data.append(day_data)
                line_data = PrepLine(game_name=game_name, days=days_data)
                lines_data.append(line_data)
        month_data = PrepMonth(
            year=ym[0],
            month=ym[1],
            days=days_in_months,
            lines=lines_data,
        )
        rv.append(month_data)

    return rv


# TEXT CALENDAR


def draw_text_line(line_data: PrepLine) -> None:
    """Draw a game line."""
    output = []
    for day_data in line_data.days:
        if day_data.day == 0:
            output.append(" ")
        elif day_data.event_count > 0:
            output.append("X")
        else:
            output.append(".")
    formatted_name = line_data.game_name[0:16]
    print(f"{formatted_name:19}\t" + "\t".join(output))


def draw_text_month(month_data: PrepMonth) -> None:
    """Draw a month line and its games lines."""
    year, month = month_data.year, month_data.month
    month_label = f"----- {str(month).zfill(2)}/{year} -----"
    days_numbers = "\t".join(str(day) if day != 0 else " " for day in month_data.days)
    print(month_label + "\t" + days_numbers)
    for line_data in month_data.lines:
        draw_text_line(line_data)


def draw_text_calendar(games: List[Game], config: DrawConfig) -> None:
    """Draw the whole calendar as text."""
    data = prepare_data_for_display(games)
    if data is None:
        raise ValueError("There's no data to display")
    destination_file = config.export_file
    with destination_file.open("w", encoding="utf8") as file:
        logger.info("Export the calendar as text to %s", destination_file)
        with contextlib.redirect_stdout(file):
            for month_data in data:
                draw_text_month(month_data)


# HTMl CALENDAR

def make_day_description(events: List[Event]) -> str:
    """Return the description to display beneath a day."""
    length: int = len(events)
    if length == 0:
        return "No events"

    titles = [ev.extras.get("title", "...") for ev in events]
    summary = "\n".join("- " + title for title in titles if title != "")
    if length == 1:
        return f"1 event :\n{summary}"
    else:
        return f"{length} events :\n{summary}"


def draw_html_calendar(games: List[Game], config: DrawConfig) -> None:
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
    data = prepare_data_for_display(games)
    if data is None:
        raise ValueError("There's no data to display")
    # Render the template to a file
    destination_file = config.export_file
    with destination_file.open("w", encoding="utf8") as file:
        logger.info("Export the calendar as HTML to %s", destination_file)
        rendered = template.render(
            data=data,
            make_day_description=make_day_description,
        )
        file.write(rendered)
