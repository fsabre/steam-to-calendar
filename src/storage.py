import json
from datetime import datetime
from pathlib import Path
from typing import List

from .config import Config
from .logger import logger
from .models import Game


def save_to_file(games: List[Game], config: Config) -> None:
    """Save the game data to a file."""
    logger.info("Dump output to %s", config.destination_file)
    with config.destination_file.open("w") as destination_file:
        output_json = [
            {
                "id": game.id,
                "name": game.name,
                "min_achievement_date": game.min_achievement_date.isoformat() if game.min_achievement_date is not None else None,
                "max_achievement_date": game.max_achievement_date.isoformat() if game.max_achievement_date is not None else None,
            } for game in games
        ]
        json.dump(output_json, destination_file, indent=4)


def load_from_file(path: Path) -> List[Game]:
    """Load the data from a file."""
    logger.info("Load data from %s", path)
    with path.open() as source_file:
        loaded_data = json.load(source_file)

    output: List[Game] = []
    for game_data in loaded_data:
        game = Game(id=game_data["id"], name=game_data["name"])
        if (min_date := game_data["min_achievement_date"]) is not None:
            game.min_achievement_date = datetime.fromisoformat(min_date)
        if (max_date := game_data["max_achievement_date"]) is not None:
            game.max_achievement_date = datetime.fromisoformat(max_date)
        output.append(game)

    return output
