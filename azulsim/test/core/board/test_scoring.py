"""Contains unit tests for the azulsim.core.board.scoring module."""

import pytest
from pydantic import ValidationError

from azulsim.core.board.scoring import GameScore


def test_default_score() -> None:
    """Tests that the default constructor for GameScore is valid."""
    score = GameScore.default()
    assert score.score == 0


def test_new_score() -> None:
    """Tests that the new constructor for GameScore is valid."""
    score = GameScore.new(10)
    assert score.score == 10


def test_add_scores() -> None:
    """Tests the __add__ dunder method for GameScore is valid."""
    score1 = GameScore.new(10)
    result = score1 + 5
    assert result.score == 15


def test_add_scores_below_zero() -> None:
    """Tests that invoking the __add__ dunder method for GameScore with a negative number caps at 0."""
    score1 = GameScore.new(5)
    result = score1 + (-10)
    assert result.score == 0


def test_subtract_scores() -> None:
    """Tests the __sub__ dunder method for GameScore is valid."""
    score1 = GameScore.new(10)
    result = score1 - 5
    assert result.score == 5


def test_subtract_scores_below_zero() -> None:
    """Tests that invoking the __sub__ dunder method for GameScore with a positive number caps at 0."""
    score1 = GameScore.new(5)
    result = score1 - 10
    assert result.score == 0


def test_invalid_score() -> None:
    """Tests GameScore throws when created with a negative number."""
    with pytest.raises(ValidationError):
        GameScore.new(-1)
