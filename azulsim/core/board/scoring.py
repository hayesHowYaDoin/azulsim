"""Defines the score section of a game board."""

from typing import TypeAlias

from pydantic.types import PositiveInt


"""The score for a board in a game."""
GameScore: TypeAlias = PositiveInt
