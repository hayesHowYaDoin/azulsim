"""Defines the wall section of a game board."""

from __future__ import annotations
from collections import deque
from itertools import cycle, islice
from typing import Generator, TypeAlias

from pydantic import field_validator
from pydantic.dataclasses import dataclass

from ..tiles import ColoredTile


@dataclass(frozen=True, kw_only=True)
class EmptyWallSpace:
    """A space in the wall section of a board which unoccupied."""

    color: ColoredTile

    @staticmethod
    def new(color: ColoredTile) -> EmptyWallSpace:
        """Returns an empty wall space object with the provided tile color."""
        return EmptyWallSpace(color=color)


@dataclass(frozen=True, kw_only=True)
class PopulatedWallSpace:
    """A space in the wall section of a board which occupied."""

    color: ColoredTile

    @staticmethod
    def new(color: ColoredTile) -> PopulatedWallSpace:
        """Returns a populated wall space object with the provided tile color."""
        return PopulatedWallSpace(color=color)


"""A space in the wall section of a board."""
WallSpace: TypeAlias = EmptyWallSpace | PopulatedWallSpace


def _wall_tile_sequence(
    start: ColoredTile,
) -> Generator[ColoredTile, None, None]:
    color_sequence = deque(
        (
            ColoredTile.BLUE,
            ColoredTile.YELLOW,
            ColoredTile.RED,
            ColoredTile.BLACK,
            ColoredTile.WHITE,
        )
    )
    while color_sequence[0] != start:
        color_sequence.rotate()

    color_cycle = cycle(color_sequence)
    for color in color_cycle:
        yield color


_WallRowTilesType: TypeAlias = tuple[
    WallSpace, WallSpace, WallSpace, WallSpace, WallSpace
]


@dataclass(frozen=True, kw_only=True)
class WallRow:
    """A row in the wall section of a board."""

    tiles: _WallRowTilesType

    @staticmethod
    def new(leftmost_color: ColoredTile) -> WallRow:
        """Returns a wall row starting from the provided leftmost color."""
        row_sequence = (
            EmptyWallSpace.new(tile)
            for tile in _wall_tile_sequence(leftmost_color)
        )

        tiles = tuple(islice(row_sequence, 5))
        assert len(tiles) == 5, "Number of tiles in a wall row must be 5."
        return WallRow.new(tiles)

    @field_validator("tiles")
    @classmethod
    def _validate_tiles(cls, tiles: _WallRowTilesType) -> _WallRowTilesType:
        row_colors = [tile.color for tile in tiles]
        valid_colors = _wall_tile_sequence(row_colors[0])
        for color, valid_color in zip(row_colors, valid_colors):
            if color != valid_color:
                raise ValueError("Colors must follow wall sequence.")

        return tiles


def _build_default_wall_rows() -> (
    tuple[WallRow, WallRow, WallRow, WallRow, WallRow]
):
    left_tile_sequence = _wall_tile_sequence(ColoredTile.BLUE)
    rows = tuple((WallRow.new(next(left_tile_sequence)) for _ in range(5)))

    assert len(rows) == 5, "Number of rows in a wall must be 5."
    return rows


_WallRowsType: TypeAlias = tuple[WallRow, WallRow, WallRow, WallRow, WallRow]


@dataclass(frozen=True, kw_only=True)
class Wall:
    """The wall section of a board."""

    rows: _WallRowsType

    @staticmethod
    def default() -> Wall:
        """Returns a wall with empty wall rows in the required pattern."""
        return Wall(rows=_build_default_wall_rows())

    @staticmethod
    def new(rows: _WallRowsType) -> Wall:
        """Returns a wall with the provided rows."""
        return Wall(rows=rows)

    @field_validator("rows")
    @classmethod
    def _validate_rows(cls, rows: _WallRowsType) -> _WallRowsType:
        row_start_colors = [row.tiles[0].color for row in rows]
        valid_colors = _wall_tile_sequence(row_start_colors[0])
        for color, valid_color in zip(row_start_colors, valid_colors):
            if color != valid_color:
                raise ValueError("Colors for rows must follow wall sequence.")

        return rows
