"""Defines the score section of a game board."""

from __future__ import annotations

from pydantic.dataclasses import dataclass
from pydantic.types import NonNegativeInt


@dataclass(frozen=True, kw_only=True)
class GameScore:
    """The score for a board in a game."""

    score: NonNegativeInt

    @staticmethod
    def default() -> GameScore:
        """Returns a game score object representing a score of 0."""
        return GameScore(score=0)

    @staticmethod
    def new(score: NonNegativeInt) -> GameScore:
        """Returns a game score object representing the provided score."""
        return GameScore(score=score)

    def __add__(self, other: int) -> GameScore:
        """Adds an integer to a game score objects."""
        return GameScore.new(score=self.score + other)

    def __sub__(self, other: int) -> GameScore:
        """Subtracts an integer from a game score object."""
        return GameScore.new(score=max(self.score - other, 0))
