"""Contains unit tests for the azulsim.core.board.floor module."""

import pytest
from azulsim.core.board.floor import FloorLine, calculate_floor_penalty
from pydantic import ValidationError


def test_floor_line_default() -> None:
    floor_line = FloorLine.default()
    assert floor_line.tile_count == 0


def test_floor_line_valid_tile_count() -> None:
    for count in range(8):
        floor_line = FloorLine.new(tile_count=count)
        assert floor_line.tile_count == count


def test_floor_line_invalid_tile_count() -> None:
    with pytest.raises(ValidationError):
        FloorLine.new(tile_count=-1)
    with pytest.raises(ValidationError):
        FloorLine.new(tile_count=8)


def test_calculate_floor_penalty() -> None:
    penalties = [0, -1, -2, -4, -6, -8, -11, -14]
    for count in range(8):
        floor_line = FloorLine.new(tile_count=count)
        assert calculate_floor_penalty(floor_line) == penalties[count]
