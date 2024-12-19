"""Defines representations of tile pools from which a player can pick from."""

from __future__ import annotations
from typing import Sequence, TypeAlias

from pydantic.dataclasses import dataclass

from .tiles import ColoredTile


@dataclass(frozen=True, kw_only=True)
class FactoryDisplay:
    """A factory display which contains a pot of tiles."""

    tiles: tuple[ColoredTile, ColoredTile, ColoredTile, ColoredTile]

    @staticmethod
    def new(tiles: Sequence[ColoredTile]) -> FactoryDisplay:
        """Returns a factory display with the provided tiles."""
        if len(tiles) != 4:
            raise ValueError("FactoryDisplay must contain 4 tiles.")

        tiles_tuple = tuple(tiles)
        assert len(tiles_tuple) == 4

        return FactoryDisplay(tiles=tiles_tuple)


@dataclass(frozen=True, kw_only=True)
class UnpickedTableCenter:
    """The tile pot in the center of the table before the first player marker has been taken."""

    tiles: tuple[ColoredTile, ...]

    @staticmethod
    def default() -> UnpickedTableCenter:
        """Returns an unpicked table center in its default state with no tiles."""
        return UnpickedTableCenter(tiles=())

    @staticmethod
    def new(tiles: Sequence[ColoredTile]) -> UnpickedTableCenter:
        """Returns an unpicked table center with the provided tiles."""
        return UnpickedTableCenter(tiles=tuple(tiles))


@dataclass(frozen=True, kw_only=True)
class PickedTableCenter:
    """The tile pot in the center of the table after the first player marker has been taken."""

    tiles: tuple[ColoredTile, ...]

    @staticmethod
    def default() -> PickedTableCenter:
        """Returns a picked table center in its default state with no tiles."""
        return PickedTableCenter(tiles=())

    @staticmethod
    def new(tiles: Sequence[ColoredTile]) -> PickedTableCenter:
        """Returns a picked table center with the provided tiles."""
        return PickedTableCenter(tiles=tuple(tiles))


"""The pot of tiles in the center of the table."""
TableCenter: TypeAlias = UnpickedTableCenter | PickedTableCenter
