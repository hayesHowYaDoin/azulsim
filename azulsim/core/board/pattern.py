from typing import TypeAlias

from pydantic import BaseModel, Field, field_validator
from pydantic.types import NonNegativeInt
from pydantic.dataclasses import dataclass

from ..tiles import ColoredTile


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
