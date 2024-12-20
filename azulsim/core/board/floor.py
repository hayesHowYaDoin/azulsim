"""Defines the floor line section of a game board."""

from __future__ import annotations
from itertools import islice
from typing import Sequence

from pydantic import ConfigDict
from pydantic.dataclasses import dataclass
from pydantic.types import NegativeInt, PositiveInt

from ..tiles import ColoredTile, StartingPlayerMarker, Tile


@dataclass(
    frozen=True, kw_only=True, config=ConfigDict(arbitrary_types_allowed=True)
)
class FloorLine:
    """A floor line on a board."""

    tiles: tuple[Tile, ...]

    @staticmethod
    def default() -> FloorLine:
        """Returns a floor line object with a tile count of zero."""
        return FloorLine(tiles=())

    @staticmethod
    def new(tiles: Sequence[Tile]) -> FloorLine:
        return FloorLine(tiles=tuple(tiles))

    @staticmethod
    def spaces_count() -> PositiveInt:
        return 7

    def add(self, tiles: Sequence[Tile]) -> FloorLine:
        remaining_spaces = FloorLine.spaces_count() - len(self.tiles)
        if remaining_spaces <= 0:
            return self

        tiles = self.tiles + tuple(tiles[:remaining_spaces])
        return FloorLine(tiles=tiles)


def calculate_floor_penalty(floor_line: FloorLine) -> NegativeInt:
    """Returns the calculated penalty for the contents of a floor line."""
    penalties = (-1, -1, -2, -2, -2, -3, -3)
    return sum(islice(penalties, len(floor_line.tiles)))
