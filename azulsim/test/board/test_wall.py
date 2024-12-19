"""Contains unit tests for the azulsim.core.board.wall module."""

import pytest

from azulsim.core.board.wall import (
    EmptyWallSpace,
    PopulatedWallSpace,
    WallLine,
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
    wall_row = WallLine.default(leftmost_color=ColoredTile.YELLOW)
    assert len(wall_row.tiles) == 5
    assert wall_row.tiles[0].color == ColoredTile.YELLOW
    assert wall_row.tiles[1].color == ColoredTile.RED
    assert wall_row.tiles[2].color == ColoredTile.BLACK
    assert wall_row.tiles[3].color == ColoredTile.WHITE
    assert wall_row.tiles[4].color == ColoredTile.BLUE


def test_wall_default():
    wall = Wall.default()
    assert len(wall.lines) == 5
    assert wall.lines[0].tiles[0].color == ColoredTile.BLUE
    assert wall.lines[1].tiles[0].color == ColoredTile.YELLOW
    assert wall.lines[2].tiles[0].color == ColoredTile.RED
    assert wall.lines[3].tiles[0].color == ColoredTile.BLACK
    assert wall.lines[4].tiles[0].color == ColoredTile.WHITE


def test_wall_new() -> None:
    wall = Wall.new(
        (
            WallLine.default(ColoredTile.BLACK),
            WallLine.default(ColoredTile.WHITE),
            WallLine.default(ColoredTile.BLUE),
            WallLine.default(ColoredTile.YELLOW),
            WallLine.default(ColoredTile.RED),
        )
    )
    assert len(wall.lines) == 5
    assert wall.lines[0].tiles[0].color == ColoredTile.BLACK
    assert wall.lines[1].tiles[0].color == ColoredTile.WHITE
    assert wall.lines[2].tiles[0].color == ColoredTile.BLUE
    assert wall.lines[3].tiles[0].color == ColoredTile.YELLOW
    assert wall.lines[4].tiles[0].color == ColoredTile.RED


def test_wall_invalid_row_sequence():
    with pytest.raises(ValueError):
        Wall(
            lines=(
                WallLine.default(ColoredTile.BLUE),
                WallLine.default(ColoredTile.RED),
                WallLine.default(ColoredTile.YELLOW),
                WallLine.default(ColoredTile.BLACK),
                WallLine.default(ColoredTile.WHITE),
            )
        )
