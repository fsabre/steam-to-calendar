from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Game:
    id: Optional[int]
    name: str
    purchase_date: str = ""
    min_achievement_date: Optional[datetime] = None
    max_achievement_date: Optional[datetime] = None
