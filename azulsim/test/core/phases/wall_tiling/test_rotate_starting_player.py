"""Contains unit tests for the azulsim.core.game.wall_tiling module's rotate_starting_player function."""

import pytest

from azulsim.core.board import Board, GameScore, PatternLines, FloorLine, Wall
from azulsim.core.phases import wall_tiling
from azulsim.core.tiles import StartingPlayerMarker


def test_single_player() -> None:
    """Tests that the function returns the one board in a single-player game."""
    boards = [
        Board.new(
            GameScore.new(0),
            PatternLines.default(),
            FloorLine.new([StartingPlayerMarker()]),
            Wall.default(),
        )
    ]
    starting_player_index = wall_tiling.next_starting_board(boards)

    assert starting_player_index == 0


def test_multiplayer() -> None:
    """Tests that the function returns the board in rotated order in a multiplayer game."""
    boards = [
        Board.default(),
        Board.new(
            GameScore.new(0),
            PatternLines.default(),
            FloorLine.new([StartingPlayerMarker()]),
            Wall.default(),
        ),
        Board.default(),
    ]
    starting_player_index = wall_tiling.next_starting_board(boards)

    assert starting_player_index == 1


def test_no_single_player_marker() -> None:
    """Tests that the function raises a ValueError if no boards have the starting player marker."""
    boards = [
        Board.default(),
        Board.default(),
        Board.default(),
    ]
    with pytest.raises(ValueError):
        _rotated_boards = wall_tiling.next_starting_board(boards)
