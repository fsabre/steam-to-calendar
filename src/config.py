"""Define the models containing launch configuration."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Final, Literal, Tuple

ExportMode = Literal["text", "html"]

HOME_PAGE: Final = "https://store.steampowered.com/"
LOGIN_PAGE: Final = "https://store.steampowered.com/login"
LOGIN_WAIT_TIMEOUT: Final[int] = 60 * 60  # Time spent waiting for the user to log in, in seconds

ROOT_PATH = Path(__file__).parent.parent
DEFAULT_DATA_FILE = ROOT_PATH / "dump.json"
DEFAULT_EXPORT_FILE = ROOT_PATH / "cal.html"


@dataclass
class FetchConfig:
    # Public Steam profile URL
    profile_url: str
    # Whether to prompt the user for login
    login_user: bool = False
    # File where the data will be saved
    destination_file: Path = DEFAULT_DATA_FILE
    # Whether to fetch the achievements dates
    no_achievements: bool = False
    # List of game ID. Only parse the achievements of those games.
    only_achievements_for: Tuple[str, ...] = field(default_factory=tuple)

    def games_url(self) -> str:
        """URL used to fetch the game list"""
        stripped_profile_url = self.profile_url.rstrip('/')
        return f"{stripped_profile_url}/games/?tab=all&sort=name"

    def achievements_url(self, game_id: str) -> str:
        """URL used to fetch the game list"""
        # Team Fortress 2 acts differently.
        if game_id == "440":
            game_id = "TF2"
        stripped_profile_url = self.profile_url.rstrip('/')
        return f"{stripped_profile_url}/stats/{game_id}/?tab=achievements"


@dataclass
class DrawConfig:
    # Export mode (text, html, ...)
    mode: ExportMode
    # File where the data will be read
    data_file: Path = DEFAULT_DATA_FILE
    # File where the calendar will be exported
    export_file: Path = DEFAULT_EXPORT_FILE

    def __post_init__(self) -> None:
        # Ensure the extension fit the export mode, but only if it wasn't
        # manually changed
        if self.export_file == DEFAULT_EXPORT_FILE:
            self.export_file = self.export_file.with_suffix(
                ".txt" if self.mode == "text" else ".html"
            )
