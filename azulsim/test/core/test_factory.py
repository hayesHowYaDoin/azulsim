"""Contains unit tests for the azulsim.core.factory module."""

import pytest

from azulsim.core.factory import (
    FactoryDisplay,
    UnpickedTableCenter,
    PickedTableCenter,
)
from azulsim.core.tiles import ColoredTile


def test_factory_display_new_valid() -> None:
    """Tests that the new method of FactoryDisplay has valid results for valid arguments."""
    tiles = [
        ColoredTile.BLUE,
        ColoredTile.RED,
        ColoredTile.YELLOW,
        ColoredTile.BLUE,
    ]
    factory_display = FactoryDisplay.new(tiles)
    assert factory_display.tiles == tuple(tiles)


def test_factory_display_new_invalid() -> None:
    """Tests that the new method of FactoryDisplay throws when provided invalid arguments."""
    tiles = [ColoredTile.BLUE, ColoredTile.RED, ColoredTile.YELLOW]
    with pytest.raises(ValueError):
        FactoryDisplay.new(tiles)


def test_unpicked_table_center_default() -> None:
    """Tests that the default constructor for UnpickedTableCenter is valid."""
    table_center = UnpickedTableCenter.default()
    assert table_center.tiles == ()


def test_unpicked_table_center_new() -> None:
    """ "Tests that the new constructor for UnpickedTableCenter is valid."""
    tiles = [ColoredTile.BLUE, ColoredTile.RED]
    table_center = UnpickedTableCenter.new(tiles)
    assert table_center.tiles == tuple(tiles)


def test_picked_table_center_default() -> None:
    """Tests that the default constructor for PickedTableCenter is valid."""
    table_center = PickedTableCenter.default()
    assert table_center.tiles == ()


def test_picked_table_center_new() -> None:
    """Tests that the new constructor for PickedTableCenter is valid."""
    tiles = [ColoredTile.BLUE, ColoredTile.RED]
    table_center = PickedTableCenter.new(tiles)
    assert table_center.tiles == tuple(tiles)
