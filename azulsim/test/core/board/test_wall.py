"""Contains unit tests for the azulsim.core.board.wall module."""

import pytest

from azulsim.core.board.wall import (
    EmptyWallSpace,
    PopulatedWallSpace,
    WallLine,
    Wall,
)
from azulsim.core.tiles import ColoredTile


def test_empty_wall_space_new() -> None:
    """Tests that the new constructor for EmptyWallSpace is valid."""
    color = ColoredTile.BLUE
    empty_space = EmptyWallSpace.new(color)
    assert empty_space.color == color


def test_populated_wall_space_new() -> None:
    """Tests that the new constructor for PopulatedWallSpace is valid."""
    color = ColoredTile.RED
    populated_space = PopulatedWallSpace.new(color)
    assert populated_space.color == color


def test_wall_line_new() -> None:
    """Tests that the new constructor for WallLine is valid."""
    wall_row = WallLine.from_leftmost(leftmost_color=ColoredTile.YELLOW)
    assert len(wall_row.spaces) == 5
    assert wall_row.spaces[0].color == ColoredTile.YELLOW
    assert wall_row.spaces[1].color == ColoredTile.RED
    assert wall_row.spaces[2].color == ColoredTile.BLACK
    assert wall_row.spaces[3].color == ColoredTile.WHITE
    assert wall_row.spaces[4].color == ColoredTile.BLUE


def test_wall_line_invalid_sequence() -> None:
    """Tests that the new constructor for WallLine throws when given an invalid color sequence."""
    with pytest.raises(ValueError):
        WallLine.new(
            (
                PopulatedWallSpace.new(ColoredTile.BLUE),
                PopulatedWallSpace.new(ColoredTile.RED),
                PopulatedWallSpace.new(ColoredTile.YELLOW),
                PopulatedWallSpace.new(ColoredTile.BLACK),
                PopulatedWallSpace.new(ColoredTile.WHITE),
            )
        )


def test_wall_default() -> None:
    """Tests that the default constructor for Wall is valid."""
    wall = Wall.default()
    assert len(wall.lines) == 5
    assert wall.lines[0].spaces[0].color == ColoredTile.BLUE
    assert wall.lines[1].spaces[0].color == ColoredTile.YELLOW
    assert wall.lines[2].spaces[0].color == ColoredTile.RED
    assert wall.lines[3].spaces[0].color == ColoredTile.BLACK
    assert wall.lines[4].spaces[0].color == ColoredTile.WHITE


def test_wall_with_populated() -> None:
    """Tests that the with_populated constructor for Wall is valid."""
    populated_indices = (
        (0, ColoredTile.BLUE),
        (1, ColoredTile.RED),
        (4, ColoredTile.RED),
        (3, ColoredTile.RED),
    )
    wall = Wall.with_populated(populated_indices)
    assert len(wall.lines) == 5
    assert wall.lines[0].spaces[0].color == ColoredTile.BLUE
    assert wall.lines[1].spaces[0].color == ColoredTile.YELLOW
    assert wall.lines[2].spaces[0].color == ColoredTile.RED
    assert wall.lines[3].spaces[0].color == ColoredTile.BLACK
    assert wall.lines[4].spaces[0].color == ColoredTile.WHITE

    for line_index, line in enumerate(wall):
        for space in line:
            if (line_index, space.color) in populated_indices:
                assert isinstance(space, PopulatedWallSpace)
            else:
                assert isinstance(space, EmptyWallSpace)


def test_wall_new() -> None:
    """Tests that the new constructor for Wall is valid."""
    wall = Wall.new(
        (
            WallLine.from_leftmost(ColoredTile.BLACK),
            WallLine.from_leftmost(ColoredTile.WHITE),
            WallLine.from_leftmost(ColoredTile.BLUE),
            WallLine.from_leftmost(ColoredTile.YELLOW),
            WallLine.from_leftmost(ColoredTile.RED),
        )
    )
    assert len(wall.lines) == 5
    assert wall.lines[0].spaces[0].color == ColoredTile.BLACK
    assert wall.lines[1].spaces[0].color == ColoredTile.WHITE
    assert wall.lines[2].spaces[0].color == ColoredTile.BLUE
    assert wall.lines[3].spaces[0].color == ColoredTile.YELLOW
    assert wall.lines[4].spaces[0].color == ColoredTile.RED


def test_wall_invalid_line_sequence() -> None:
    """Tests that the new constructor for Wall raises an exception on an invalid color sequence."""
    with pytest.raises(ValueError):
        Wall.new(
            (
                WallLine.from_leftmost(ColoredTile.BLUE),
                WallLine.from_leftmost(ColoredTile.RED),
                WallLine.from_leftmost(ColoredTile.YELLOW),
                WallLine.from_leftmost(ColoredTile.BLACK),
                WallLine.from_leftmost(ColoredTile.WHITE),
            )
        )
