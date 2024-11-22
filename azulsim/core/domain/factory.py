from typing import Optional, TypeAlias

from pydantic.dataclasses import dataclass

from .tiles import ColoredTile


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