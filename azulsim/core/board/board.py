from __future__ import annotations

from pydantic import BaseModel, Field

from .scoring import GameScore
from .pattern import PatternLines
from .floor import FloorLine
from .wall import Wall


class Board(BaseModel):
    """A player board in a game."""

    score_track: GameScore = Field(default=0)
    pattern_lines: PatternLines = Field(default=PatternLines())
    floor_line: FloorLine = Field(default=FloorLine())
    wall: Wall = Field(default=Wall())
