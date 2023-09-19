from datetime import datetime, timezone, timedelta
from typing import Optional

import pytest

from src.config import FetchConfig
from src.models import Event, Game
from src.parsing import MyWebDriver


@pytest.fixture
def webdriver() -> MyWebDriver:
    config = FetchConfig(profile_url="https://steamcommunity.com/id/Lial_Slasher/", login_user=True)
    wd = MyWebDriver(config=config)
    yield wd
    wd.quit()


def test_get_game_list(webdriver: MyWebDriver) -> None:
    games = webdriver.get_game_list()
    a_hat_in_time_game = Game(id="253230", name="A Hat in Time", events=[])
    deathloop_game = Game(id="1252330", name="DEATHLOOP", events=[])
    tf2_game = Game(id="440", name="Team Fortress 2", events=[])
    assert a_hat_in_time_game in games
    assert deathloop_game in games
    assert tf2_game in games


def test_get_achievements_events(webdriver: MyWebDriver) -> None:
    events = webdriver.get_achievements_events(game_id="253230")
    assert len(events) == 45, "Number of unlocked achievements is wrong"
    no_time_to_explain_event = Event(
        type="achievement",
        date=datetime(2018, 5, 27, 19, 33, tzinfo=timezone(timedelta(hours=1))),
        extras=dict(
            title="No Time To Explain",
            desc="Complete Train Rush without dying or time bonuses!",
        ),
    )
    found_event: Optional[Event] = next((ev for ev in events if ev.extras["title"] == "No Time To Explain"), None)
    assert found_event is not None, "Missing an unlocked achievement"
    assert found_event.type == no_time_to_explain_event.type, "Event type is wrong"
    assert found_event.extras == no_time_to_explain_event.extras, "Achievement title or description are wrong"


def test_get_achievements_events_dates() -> None:
    # TODO
    pass
