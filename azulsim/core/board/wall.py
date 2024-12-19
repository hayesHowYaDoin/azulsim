"""Defines the wall section of a game board."""

from __future__ import annotations
from collections import deque
from itertools import cycle, islice
from typing import Generator, Iterable, TypeAlias

from pydantic import field_validator, PositiveInt
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


_WallLineTilesType: TypeAlias = tuple[
    WallSpace, WallSpace, WallSpace, WallSpace, WallSpace
]


@dataclass(frozen=True, kw_only=True)
class WallLine:
    """A line in the wall section of a board."""

    tiles: _WallLineTilesType

    @staticmethod
    def default(leftmost_color: ColoredTile) -> WallLine:
        """Returns a wall line starting from the provided leftmost color."""
        row_sequence = (
            EmptyWallSpace.new(tile)
            for tile in _wall_tile_sequence(leftmost_color)
        )

        tiles = tuple(islice(row_sequence, WallLine.tile_count()))
        assert len(tiles) == 5, "Number of tiles in a wall row must be 5."
        return WallLine(tiles=tiles)

    @staticmethod
    def new(tiles: Iterable[WallSpace]) -> WallLine:
        return WallLine(tiles=_WallLineTilesType(tiles))

    @staticmethod
    def tile_count() -> PositiveInt:
        return 5

    def populate_tile(self, color: ColoredTile) -> WallLine:
        """Returns a wall line with the space of the argument color added."""
        tiles: list[WallSpace] = []
        for tile in self.tiles:
            if tile.color != color:
                tiles.append(tile)
            else:
                tiles.append(PopulatedWallSpace(color=color))

        return WallLine.new(tiles)

    @field_validator("tiles")
    @classmethod
    def _validate_tiles(cls, tiles: _WallLineTilesType) -> _WallLineTilesType:
        row_colors = [tile.color for tile in tiles]
        valid_colors = _wall_tile_sequence(row_colors[0])
        for color, valid_color in zip(row_colors, valid_colors):
            if color != valid_color:
                raise ValueError("Colors must follow wall sequence.")

        return tiles


def _build_default_wall_rows() -> (
    tuple[WallLine, WallLine, WallLine, WallLine, WallLine]
):
    left_tile_sequence = _wall_tile_sequence(ColoredTile.BLUE)
    rows = tuple((WallLine.default(next(left_tile_sequence)) for _ in range(5)))

    assert len(rows) == 5, "Number of rows in a wall must be 5."
    return rows


_WallLinesType: TypeAlias = tuple[
    WallLine, WallLine, WallLine, WallLine, WallLine
]


@dataclass(frozen=True, kw_only=True)
class Wall:
    """The wall section of a board."""

    lines: _WallLinesType

    @staticmethod
    def default() -> Wall:
        """Returns a wall with empty wall rows in the required pattern."""
        return Wall(lines=_build_default_wall_rows())

    @staticmethod
    def new(rows: _WallLinesType) -> Wall:
        """Returns a wall with the provided rows."""
        return Wall(lines=rows)

    @staticmethod
    def line_count() -> PositiveInt:
        return 5

    @field_validator("rows")
    @classmethod
    def _validate_rows(cls, rows: _WallLinesType) -> _WallLinesType:
        row_start_colors = [row.tiles[0].color for row in rows]
        valid_colors = _wall_tile_sequence(row_start_colors[0])
        for color, valid_color in zip(row_start_colors, valid_colors):
            if color != valid_color:
                raise ValueError("Colors for rows must follow wall sequence.")

        return rows
