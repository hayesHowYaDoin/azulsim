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
        return Board(
            score_track=0,
            pattern_lines=PatternLines.default(),
            floor_line=FloorLine.default(),
            wall=Wall.default(),
        )
