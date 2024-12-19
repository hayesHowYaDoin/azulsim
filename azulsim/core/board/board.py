"""Defines a game board."""

from __future__ import annotations

from pydantic.dataclasses import dataclass

from .scoring import GameScore
from .pattern import PatternLines
from .floor import FloorLine
from .wall import Wall


@dataclass(frozen=True, kw_only=True)
class Board:
    """A player board in a game."""

    score_track: GameScore
    pattern_lines: PatternLines
    floor_line: FloorLine
    wall: Wall

    @staticmethod
    def default() -> Board:
        """Returns a board with defaulted sections."""
        return Board(
            score_track=GameScore.default(),
            pattern_lines=PatternLines.default(),
            floor_line=FloorLine.default(),
            wall=Wall.default(),
        )

    @staticmethod
    def new(
        score_track: GameScore,
        pattern_lines: PatternLines,
        floor_line: FloorLine,
        wall: Wall,
    ) -> Board:
        """Returns a board with the argument sections."""
        return Board(
            score_track=score_track,
            pattern_lines=pattern_lines,
            floor_line=floor_line,
            wall=wall,
        )
