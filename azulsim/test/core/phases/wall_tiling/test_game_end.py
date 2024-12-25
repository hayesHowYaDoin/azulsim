"""Contains unit tests for the azulsim.core.game.wall_tiling module's game_end function."""

from azulsim.core.phases import wall_tiling
from azulsim.core.board import Wall
from azulsim.core.tiles import ColoredTile


def test_wall_with_full_horizontal() -> None:
    """Tests that function returns True when a wall has a fully-completed horizontal row."""
    walls = (
        Wall.default(),
        Wall.with_populated(((0, color) for color in ColoredTile)),
        Wall.default(),
        Wall.default(),
    )
    assert wall_tiling.game_end(walls)


def test_no_full_horizontal() -> None:
    """Tests that function returns False when no wall has a fully-completed horizontal row."""
    walls = (
        Wall.default(),
        Wall.default(),
    )
    assert not wall_tiling.game_end(walls)
