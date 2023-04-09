from datetime import datetime, timezone, timedelta

import pytest
from selenium.webdriver.support.wait import WebDriverWait

from src import exceptions
from src.config import FetchConfig, LOGIN_PAGE
from src.models import Event, Game
from src.parsing import MyWebDriver


@pytest.fixture
def webdriver() -> MyWebDriver:
    config = FetchConfig(profile_url="https://steamcommunity.com/id/Lial_Slasher/")
    wd = MyWebDriver(config=config)
    yield wd
    wd.quit()


def test_get_game_list(webdriver: MyWebDriver) -> None:
    games = webdriver.get_game_list()
    a_hat_in_time_game = Game(id="253230", name="A Hat in Time")
    deathloop_game = Game(id="1252330", name="DEATHLOOP")
    tf2_game = Game(id="440", name="Team Fortress 2")
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
    assert no_time_to_explain_event in events, "Missing an unlocked achievement"


def test_login_redirect(webdriver: MyWebDriver) -> None:
    """Test that the login page is opened if needed."""

    # Patch the WaitDriver wait to have an immediate timeout and check the
    # according exception is raised
    TIMEOUT_SECONDS = 1

    old = WebDriverWait
    def fake_init(self, *args, **kwargs) -> None:
        kwargs["timeout"] = TIMEOUT_SECONDS
        old.__init__(self, *args, **kwargs)

    WebDriverWait.__init__ = fake_init

    print(webdriver.driver.current_url)

    assert (
        webdriver.driver.current_url == LOGIN_PAGE,
        "The current page is not the login page",
    )
    with pytest.raises(exceptions.TimeoutException):
        webdriver.log_in_user()
