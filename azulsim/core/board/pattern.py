"""Defines the pattern line section of a game board."""

from __future__ import annotations
from annotated_types import Ge, Le
from typing import Annotated, Generator, Optional, Sequence, TypeAlias

from pydantic import ConfigDict, field_validator
from pydantic.types import NonNegativeInt, PositiveInt
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
    def new(lines: Sequence[PatternLine]) -> PatternLines:
        """Returns a pattern lines object with the provided pattern lines."""
        lines_tuple = tuple(lines)
        assert len(lines_tuple) == 5
        return PatternLines(lines=lines_tuple)

    @staticmethod
    def line_count() -> PositiveInt:
        """Returns the number of pattern lines in the pattern lines section of a board."""
        return 5

    def try_add(
        self,
        index: Annotated[int, Ge(0), Le(line_count())],
        count: PositiveInt,
        color: ColoredTile,
    ) -> Optional[tuple[PatternLines, NonNegativeInt]]:
        """Returns the pattern lines updated to contain the added tile count with the number of remaining tiles if possible."""
        prev_line = self.lines[index]
        max_tiles = index + 1
        match prev_line:
            case PopulatedPatternLine():
                if prev_line.color != color:
                    return None
                remainder = max(count - (max_tiles - prev_line.tile_count), 0)
                next_line_count = min(prev_line.tile_count + count, max_tiles)
            case EmptyPatternLine():
                remainder = max(count - max_tiles, 0)
                next_line_count = min(count, max_tiles)

        next_line = PopulatedPatternLine.new(next_line_count, color)
        updated_lines = tuple(
            next_line if i == index else line
            for i, line in enumerate(self.lines)
        )
        assert (
            len(updated_lines) == 5
        ), "Number of lines in the pattern section must be 5."

        return PatternLines(lines=updated_lines), remainder

    def __iter__(self) -> Generator[PatternLine, None, None]:
        """Returns a generator for iterating through the pattern lines."""
        return (line for line in self.lines)

    def __getitem__(self, key: NonNegativeInt) -> PatternLine:
        """Returns the pattern line at the provided index key."""
        return self.lines[key]

    @field_validator("lines")
    @classmethod
    def _validate_lines(
        cls,
        lines: _PatternLinesType,
    ) -> _PatternLinesType:
        return (
            cls._validate_line(lines[0], 1),
            cls._validate_line(lines[1], 2),
            cls._validate_line(lines[2], 3),
            cls._validate_line(lines[3], 4),
            cls._validate_line(lines[4], 5),
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
