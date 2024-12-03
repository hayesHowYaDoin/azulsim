"""Contains unit tests for the azulsim.core.board.wall module."""

import pytest

from azulsim.core.board.wall import (
    EmptyWallSpace,
    PopulatedWallSpace,
    WallRow,
    Wall,
)
from azulsim.core.tiles import ColoredTile


def test_empty_wall_space_new():
    color = ColoredTile.BLUE
    empty_space = EmptyWallSpace.new(color)
    assert empty_space.color == color


def test_populated_wall_space_new():
    color = ColoredTile.RED
    populated_space = PopulatedWallSpace.new(color)
    assert populated_space.color == color


def test_wall_row_new():
    wall_row = WallRow.new(leftmost_color=ColoredTile.YELLOW)
    assert len(wall_row.tiles) == 5
    assert wall_row.tiles[0].color == ColoredTile.YELLOW
    assert wall_row.tiles[1].color == ColoredTile.RED
    assert wall_row.tiles[2].color == ColoredTile.BLACK
    assert wall_row.tiles[3].color == ColoredTile.WHITE
    assert wall_row.tiles[4].color == ColoredTile.BLUE


def test_wall_default():
    wall = Wall.default()
    assert len(wall.rows) == 5
    assert wall.rows[0].tiles[0].color == ColoredTile.BLUE
    assert wall.rows[1].tiles[0].color == ColoredTile.YELLOW
    assert wall.rows[2].tiles[0].color == ColoredTile.RED
    assert wall.rows[3].tiles[0].color == ColoredTile.BLACK
    assert wall.rows[4].tiles[0].color == ColoredTile.WHITE


def test_wall_new() -> None:
    wall = Wall.new(
        (
            WallRow.new(ColoredTile.BLACK),
            WallRow.new(ColoredTile.WHITE),
            WallRow.new(ColoredTile.BLUE),
            WallRow.new(ColoredTile.YELLOW),
            WallRow.new(ColoredTile.RED),
        )
    )
    assert len(wall.rows) == 5
    assert wall.rows[0].tiles[0].color == ColoredTile.BLACK
    assert wall.rows[1].tiles[0].color == ColoredTile.WHITE
    assert wall.rows[2].tiles[0].color == ColoredTile.BLUE
    assert wall.rows[3].tiles[0].color == ColoredTile.YELLOW
    assert wall.rows[4].tiles[0].color == ColoredTile.RED


def test_wall_invalid_row_sequence():
    with pytest.raises(ValueError):
        Wall(
            rows=(
                WallRow.new(ColoredTile.BLUE),
                WallRow.new(ColoredTile.RED),
                WallRow.new(ColoredTile.YELLOW),
                WallRow.new(ColoredTile.BLACK),
                WallRow.new(ColoredTile.WHITE),
            )
        )
