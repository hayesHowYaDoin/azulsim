"""Contains unit tests for the azulsim.core.game.round_setup module's reset_tile_pools function."""

from azulsim.core.phases import round_setup
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
    assert round_setup.game_end(walls)


def test_no_full_horizontal() -> None:
    """Tests that function returns False when no wall has a fully-completed horizontal row."""
    walls = (
        Wall.default(),
        Wall.default(),
    )
    assert not round_setup.game_end(walls)
