"""Defines the floor line section of a game board."""

from __future__ import annotations
from annotated_types import Ge, Le
from itertools import islice
from typing import Annotated

from pydantic.dataclasses import dataclass
from pydantic.types import NegativeInt, PositiveInt


@dataclass(frozen=True, kw_only=True)
class FloorLine:
    """A floor line on a board."""

    tile_count: Annotated[int, Ge(0), Le(7)]

    @staticmethod
    def default() -> FloorLine:
        """Returns a floor line object with a tile count of zero."""
        return FloorLine(tile_count=0)

    @staticmethod
    def new(tile_count: PositiveInt) -> FloorLine:
        return FloorLine(tile_count=tile_count)


def calculate_floor_penalty(floor_line: FloorLine) -> NegativeInt:
    """Returns the calculated penalty for the contents of a floor line."""
    penalties = (-1, -1, -2, -2, -2, -3, -3)
    return sum(islice(penalties, floor_line.tile_count))
