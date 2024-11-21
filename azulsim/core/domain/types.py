from dataclasses import dataclass
from enum import auto, Enum
from typing import Optional, TypeAlias


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


@dataclass(frozen=True)
class FactoryDisplay:
    """A single factory display."""

    tiles: Optional[tuple[ColoredTile, ColoredTile, ColoredTile, ColoredTile]]


@dataclass(frozen=True)
class UnpickedTableCenter:
    """The tile pot in the center of the table before the first player marker has been taken."""

    tiles: tuple[ColoredTile, ...]


@dataclass(frozen=True)
class PickedTableCenter:
    """The tile pot in the center of the table after the first player marker has been taken."""

    tiles: tuple[ColoredTile, ...]


"""The pot of tiles in the center of the table."""
TableCenter: TypeAlias = UnpickedTableCenter | PickedTableCenter
