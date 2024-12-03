"""Defines the pattern line section of a game board."""

from __future__ import annotations
from typing import TypeAlias

from pydantic import ConfigDict, field_validator
from pydantic.types import NonNegativeInt
from pydantic.dataclasses import dataclass

from ..tiles import ColoredTile


class EmptyPatternLine:
    """A pattern line with no tiles."""

    pass


@dataclass(frozen=True, kw_only=True)
class PopulatedPatternLine:
    """A pattern line with tiles."""

    tile_count: NonNegativeInt
    color: ColoredTile

    @staticmethod
    def new(
        tile_count: NonNegativeInt, color: ColoredTile
    ) -> PopulatedPatternLine:
        """Returns a populated pattern line with the provided tile count and color."""
        return PopulatedPatternLine(tile_count=tile_count, color=color)


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

    assert (
        len(lines) == 5
    ), "A board's pattern lines section must have five pattern lines."
    return lines


@dataclass(
    frozen=True, kw_only=True, config=ConfigDict(arbitrary_types_allowed=True)
)
class PatternLines:
    """The pattern lines section of a board."""

    lines: _PatternLinesType

    @staticmethod
    def default() -> PatternLines:
        """Returns a pattern lines object with empty pattern lines."""
        return PatternLines(lines=_build_default_pattern_lines())

    @staticmethod
    def new(lines: _PatternLinesType) -> PatternLines:
        """Returns a pattern lines object with the provided pattern lines."""
        return PatternLines(lines=lines)

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
                if line.tile_count > max_tiles:
                    raise ValueError(
                        f"Number of tiles exceeded maximum for line: {line.tile_count} > {max_tiles}"
                    )
            case EmptyPatternLine():
                pass

        return line
