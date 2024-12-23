"""Contains unit tests for the azulsim.core.board.floor module."""

from azulsim.core.board import FloorLine, calculate_floor_penalty
from azulsim.core.tiles import ColoredTile


def test_floor_line_default() -> None:
    """Tests that the default constructor for FloorLine is valid."""
    floor_line = FloorLine.default()
    assert len(floor_line.tiles) == 0


def test_floor_line_new() -> None:
    """Tests that the new constructor for FloorLine is valid."""
    for count in range(8):
        floor_line = FloorLine.new([ColoredTile.BLACK] * count)
        assert len(floor_line.tiles) == count


def test_calculate_floor_penalty() -> None:
    """Tests that the calculate_floor_penalty function is valid for all possible outcomes."""
    penalties = [0, -1, -2, -4, -6, -8, -11, -14]
    for count in range(8):
        floor_line = FloorLine.new([ColoredTile.RED] * count)
        assert calculate_floor_penalty(floor_line) == penalties[count]
