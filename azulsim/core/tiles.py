from enum import auto, Enum
from typing import TypeAlias

from pydantic.dataclasses import dataclass


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


@dataclass(frozen=True)
class TileBag:
    """The tile bag from which colored tiles are drawn to fill the factory displays at the start of a round."""

    tiles: tuple[ColoredTile, ...]


@dataclass(frozen=True)
class TileDiscard:
    """The collection of colored tiles that have been discarded."""

    tiles: tuple[ColoredTile, ...]
