"""Contains unit tests for the azulsim.core.board.floor module."""

from azulsim.core.board import FloorLine, calculate_floor_penalty
from azulsim.core.tiles import ColoredTile


def test_floor_line_default() -> None:
    floor_line = FloorLine.default()
    assert len(floor_line.tiles) == 0


def test_floor_line_valid_tile_count() -> None:
    for count in range(8):
        floor_line = FloorLine.new([ColoredTile.BLACK] * count)
        assert len(floor_line.tiles) == count


def test_calculate_floor_penalty() -> None:
    penalties = [0, -1, -2, -4, -6, -8, -11, -14]
    for count in range(8):
        floor_line = FloorLine.new([ColoredTile.RED] * count)
        assert calculate_floor_penalty(floor_line) == penalties[count]
