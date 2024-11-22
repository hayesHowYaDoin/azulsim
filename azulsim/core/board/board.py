from __future__ import annotations

from pydantic import BaseModel

from .scoring import GameScore
from .pattern import PatternLines
from .floor import FloorLine
from .wall import Wall


class Board(BaseModel):
    """A player board in a game."""

    score_track: GameScore
    pattern_lines: PatternLines
    floor_line: FloorLine
    wall: Wall
