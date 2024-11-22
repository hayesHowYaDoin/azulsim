from __future__ import annotations
from collections import deque
from itertools import cycle, islice
from typing import Generator, TypeAlias

from pydantic import BaseModel, Field, field_validator
from pydantic.dataclasses import dataclass
from pydantic.types import PositiveInt, NonNegativeInt

from .tiles import ColoredTile


"""The score for a board in a game."""
GameScore: TypeAlias = PositiveInt


class EmptyPatternLine:
    """A pattern line with no tiles."""

    pass


@dataclass(frozen=True)
class PopulatedPatternLine:
    """A pattern line with tiles."""

    num_tiles: NonNegativeInt
    color: ColoredTile


"""A pattern line in the pattern lines section of a board."""
PatternLine: TypeAlias = EmptyPatternLine | PopulatedPatternLine


_PatternLinesType: TypeAlias = tuple[
    PatternLine, PatternLine, PatternLine, PatternLine, PatternLine
]


def _build_default_pattern_lines() -> _PatternLinesType:
    lines = tuple(
        (
            EmptyPatternLine(),
            EmptyPatternLine(),
            EmptyPatternLine(),
            EmptyPatternLine(),
            EmptyPatternLine(),
        )
    )

    assert len(lines) == 5, "Pattern lines must"
    return lines


class PatternLines(BaseModel):
    """The pattern lines section of a board."""

    lines: _PatternLinesType = Field(default=_build_default_pattern_lines())

    @field_validator("lines")
    @classmethod
    def _validate_lines(
        cls,
        lines: _PatternLinesType,
    ) -> _PatternLinesType:
        return (
            cls._validate_line(lines[0], 1),
            cls._validate_line(lines[1], 2),
            cls._validate_line(lines[1], 3),
            cls._validate_line(lines[1], 4),
            cls._validate_line(lines[1], 5),
        )

    @staticmethod
    def _validate_line(line: PatternLine, max_tiles: int) -> PatternLine:
        match line:
            case PopulatedPatternLine():
                if line.num_tiles > max_tiles:
                    raise ValueError(
                        f"Number of tiles exceeded maximum for line: {line.num_tiles} > {max_tiles}"
                    )
            case EmptyPatternLine():
                pass

        return line


@dataclass(frozen=True)
class FloorLine:
    """A floor line on a board."""

    num_tiles: NonNegativeInt


@dataclass(frozen=True)
class EmptyWallSpace:
    """A space in the wall section of a board which unoccupied."""

    tile: ColoredTile


@dataclass(frozen=True)
class PopulatedWallSpace:
    """A space in the wall section of a board which occupied."""

    tile: ColoredTile


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


@dataclass(frozen=True)
class WallRow:
    """A row in the wall section of a board."""

    tiles: _WallRowTilesType

    @staticmethod
    def default_from_leftmost(leftmost_color: ColoredTile) -> WallRow:
        row_sequence = (
            EmptyWallSpace(tile) for tile in _wall_tile_sequence(leftmost_color)
        )

        tiles = tuple(islice(row_sequence, 5))
        assert len(tiles) == 5, "Number of tiles in a wall row must be 5."
        return WallRow(tiles)


def _build_default_wall_rows() -> (
    tuple[WallRow, WallRow, WallRow, WallRow, WallRow]
):
    left_tile_sequence = _wall_tile_sequence(ColoredTile.BLUE)
    rows = tuple(
        (
            WallRow.default_from_leftmost(next(left_tile_sequence))
            for _ in range(5)
        )
    )

    assert len(rows) == 5, "Number of rows in a wall must be 5."
    return rows


class Wall(BaseModel):
    """The wall section of a board."""

    rows: tuple[WallRow, WallRow, WallRow, WallRow, WallRow] = Field(
        default=_build_default_wall_rows()
    )


class Board(BaseModel):
    """A player board in a game."""

    score_track: GameScore
    pattern_lines: PatternLines
    floor_line: FloorLine
    wall: Wall
