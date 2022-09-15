from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class Game:
    id: Optional[int]
    name: str
    purchase_date: str = ""
    achievement_dates: List[datetime] = field(default_factory=list)
    min_achievement_date: Optional[datetime] = None
    max_achievement_date: Optional[datetime] = None
