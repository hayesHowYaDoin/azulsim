"""Contains unit tests for the azulsim.core.board.scoring module."""

import pytest
from pydantic import ValidationError

from azulsim.core.board.scoring import GameScore


def test_default_score() -> None:
    score = GameScore.default()
    assert score.score == 0


def test_new_score() -> None:
    score = GameScore.new(10)
    assert score.score == 10


def test_add_scores() -> None:
    score1 = GameScore.new(10)
    result = score1 + 5
    assert result.score == 15


def test_subtract_scores() -> None:
    score1 = GameScore.new(10)
    result = score1 - 5
    assert result.score == 5


def test_subtract_scores_below_zero() -> None:
    score1 = GameScore.new(5)
    result = score1 - 10
    assert result.score == 0


def test_invalid_score() -> None:
    with pytest.raises(ValidationError):
        GameScore.new(-1)
