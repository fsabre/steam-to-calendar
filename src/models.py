from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Literal, Type, TypeVar

T = TypeVar("T")

EVENT_TYPE = Literal["purchase", "achievement"]


@dataclass
class Event:
    """A date with a event type and additional data if needed."""
    type: EVENT_TYPE
    date: datetime
    extras: Dict[str, Any]

    @classmethod
    def create_achievement_event(cls: Type[T], event_date: datetime, title: str, desc: str) -> T:
        """Create a new Event with the achievement type.
        :param event_date: The date of the achievement unlock
        :param title: The title of the achievement
        :param desc: The description of the achievement
        :return: The Event object
        """
        return cls(
            type="achievement",
            date=event_date,
            extras=dict(title=title, desc=desc),
        )

    @classmethod
    def from_json(cls: Type[T], raw: Dict) -> T:
        """Create a new Event object based on raw dump data.
        :param raw: The raw data dict
        :return: The Event object
        """
        return Event(
            type=raw["type"],
            date=datetime.fromisoformat(raw["date"]),
            extras=raw["extras"],
        )

    def to_json(self) -> Dict:
        """Dump the Event to a raw data dict.
        :return: The raw data dict
        """
        return dict(
            type=self.type,
            date=self.date.isoformat(),
            extras=self.extras,
        )


@dataclass
class Game:
    """A game with a list of events."""
    id: str
    name: str
    events: List[Event] = field(default_factory=list)

    @classmethod
    def from_json(cls: Type[T], raw: Dict) -> T:
        """Create a new Game object based on raw dump data.
        :param raw: The raw data dict
        :return: The Game object
        """
        return Game(
            id=raw["id"],
            name=raw["name"],
            events=[Event.from_json(raw_event) for raw_event in raw["events"]],
        )

    def to_json(self) -> Dict:
        """Dump the Game to a raw data dict.
        :return: The raw data dict
        """
        return dict(
            id=self.id,
            name=self.name,
            events=[event.to_json() for event in self.events],
        )
