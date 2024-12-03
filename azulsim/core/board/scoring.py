"""Defines the score section of a game board."""

from typing import TypeAlias

from pydantic.types import NonNegativeInt


"""The score for a board in a game."""
GameScore: TypeAlias = NonNegativeInt
