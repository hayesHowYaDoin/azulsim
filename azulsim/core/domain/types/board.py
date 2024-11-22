from typing import Optional, TypeAlias

from pydantic import BaseModel, Field, field_validator
from pydantic.dataclasses import dataclass
from pydantic.types import PositiveInt

from .tiles import ColoredTile


GameScore: TypeAlias = PositiveInt


@dataclass(frozen=True)
class PatternLine:
    num_tiles: int
    color: Optional[ColoredTile]


class PatternLines(BaseModel):
    """A collection of pattern lines."""

    first: PatternLine = Field(default=PatternLine(0, None))
    second: PatternLine = Field(default=PatternLine(0, None))
    third: PatternLine = Field(default=PatternLine(0, None))
    fourth: PatternLine = Field(default=PatternLine(0, None))
    fifth: PatternLine = Field(default=PatternLine(0, None))

    @field_validator("first")
    @classmethod
    def _validate_first(cls, line: PatternLine) -> PatternLine:
        return cls._validate_pattern_line(line, 1)

    @field_validator("second")
    @classmethod
    def _validate_second(cls, line: PatternLine) -> PatternLine:
        return cls._validate_pattern_line(line, 2)

    @field_validator("third")
    @classmethod
    def _validate_third(cls, line: PatternLine) -> PatternLine:
        return cls._validate_pattern_line(line, 2)

    @field_validator("fourth")
    @classmethod
    def _validate_fourth(cls, line: PatternLine) -> PatternLine:
        return cls._validate_pattern_line(line, 2)

    @field_validator("fifth")
    @classmethod
    def _validate_fifth(cls, line: PatternLine) -> PatternLine:
        return cls._validate_pattern_line(line, 2)

    @staticmethod
    def _validate_pattern_line(
        line: PatternLine, max_tiles: int
    ) -> PatternLine:
        if line.num_tiles > max_tiles:
            raise ValueError(
                f"Number of tiles exceeded maximum for line: {line.num_tiles} > {max_tiles}"
            )

        return line


class Board(BaseModel):
    score_track: GameScore
    pattern_lines: PatternLines
