"""Contains unit tests for the azulsim.core.game.factory_offer module's phase_end function."""

import pytest

from azulsim.core.phases import end_of_game
from azulsim.core.board import GameScore, Wall


@pytest.mark.parametrize(
    "wall, score, score_with_bonus",
    [
        (
            Wall.default(),
            GameScore.new(0),
            GameScore.new(0),
        ),
    ],
)
def test_phase_end(
    wall: Wall,
    score: GameScore,
    score_with_bonus: GameScore,
) -> None:
    """Tests that phase_end calculates the correct final score in a variety of conditions."""
    final_score = end_of_game.score_bonuses(wall, score)
    assert final_score == score_with_bonus
