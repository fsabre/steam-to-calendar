from dataclasses import dataclass
from pathlib import Path
from typing import Final

CHROME_PATH: Final = r"C:\Program Files\Vivaldi\Application\Vivaldi.exe"
CHROME_DRIVER_PATH: Final = "chromedriver.exe"

ROOT_PATH = Path(__file__).parent.parent


@dataclass
class Config:
    # Steam account ID (in profile URL)
    username: str
    # File where the data will be saved
    destination_file: Path = ROOT_PATH / "dump.json"

    def games_url(self) -> str:
        """URL used to fetch the game list"""
        return f"https://steamcommunity.com/id/{self.username}/games/?tab=all&sort=name"

    def achievements_url(self, game_id: int) -> str:
        """URL used to fetch the game list"""
        return f"https://steamcommunity.com/id/{self.username}/stats/{game_id}/?tab=achievements"
