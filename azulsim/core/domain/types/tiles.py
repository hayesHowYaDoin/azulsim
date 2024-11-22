from enum import auto, Enum
from typing import TypeAlias


class ColoredTile(Enum):
    """A single colored tile."""

    BLACK = auto()
    WHITE = auto()
    BLUE = auto()
    YELLOW = auto()
    RED = auto()


class StartingPlayerMarker:
    """The starting player marker which is used to determine the player that starts a round."""

    pass


"""A single game tile."""
Tile: TypeAlias = ColoredTile | StartingPlayerMarker
