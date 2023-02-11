"""Define the games data storage functions."""

import json
from pathlib import Path
from typing import List

from .config import FetchConfig
from .logger import logger
from .models import Game


def save_to_file(games: List[Game], config: FetchConfig) -> None:
    """Save the game data to a file."""
    logger.info("Dump output to %s", config.destination_file)
    with config.destination_file.open("w") as destination_file:
        output_json = [game.to_json() for game in games]
        json.dump(output_json, destination_file, indent=4)


def load_from_file(path: Path) -> List[Game]:
    """Load the data from a file."""
    logger.info("Load data from %s", path)
    with path.open() as source_file:
        loaded_data = json.load(source_file)

    output: List[Game] = []
    for game_data in loaded_data:
        game = Game.from_json(game_data)
        output.append(game)

    return output
