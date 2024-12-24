"""Defines a game board."""

from __future__ import annotations
import uuid

from pydantic.dataclasses import dataclass

from .scoring import GameScore
from .pattern import PatternLines
from .floor import FloorLine
from .wall import Wall


@dataclass(frozen=True, kw_only=True)
class Board:
    """A player board in a game."""

    uid: uuid.UUID
    score_track: GameScore
    pattern_lines: PatternLines
    floor_line: FloorLine
    wall: Wall

    @staticmethod
    def default() -> Board:
        """Returns a board with defaulted sections."""
        return Board(
            uid=uuid.uuid4(),
            score_track=GameScore.default(),
            pattern_lines=PatternLines.default(),
            floor_line=FloorLine.default(),
            wall=Wall.default(),
        )

    @staticmethod
    def new(
        uid: uuid.UUID,
        score_track: GameScore,
        pattern_lines: PatternLines,
        floor_line: FloorLine,
        wall: Wall,
    ) -> Board:
        """Returns a board with the argument sections."""
        return Board(
            uid=uid,
            score_track=score_track,
            pattern_lines=pattern_lines,
            floor_line=floor_line,
            wall=wall,
        )
