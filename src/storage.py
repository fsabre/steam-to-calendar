import json
from typing import List

from .config import Config
from .logger import logger
from .models import Game


def save_to_file(games: List[Game], config: Config):
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
