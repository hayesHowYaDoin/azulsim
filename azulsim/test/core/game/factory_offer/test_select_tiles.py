"""Contains unit tests for the azulsim.core.game.factory_offer module's select_tiles function."""

from azulsim.core.factory import (
    FactoryDisplay,
    FactoryDisplays,
    PickedTableCenter,
    UnpickedTableCenter,
)
from azulsim.core.game import factory_offer
from azulsim.core.tiles import ColoredTile, StartingPlayerMarker


def test_factory() -> None:
    """Tests that output exists when factory offer selection is valid."""
    raw_factories = [
        FactoryDisplay.new([ColoredTile.BLUE] * 2 + [ColoredTile.BLACK] * 2),
        FactoryDisplay.new([ColoredTile.BLUE] * 2 + [ColoredTile.BLACK] * 2),
    ]
    factories = FactoryDisplays.new(raw_factories)
    table_center = UnpickedTableCenter.default()
    tile_pool = raw_factories[0]

    result = factory_offer.select_tiles(
        factories, table_center, tile_pool, ColoredTile.BLACK
    )

    assert result is not None
    assert len(result.factory_displays) == 1
    assert next(iter(result.factory_displays)) == raw_factories[1]
    assert result.table_center.count(ColoredTile.BLUE) == 2
    assert result.tiles == tuple([ColoredTile.BLACK] * 2)


def test_factory_not_in_game() -> None:
    """Tests that output is None when factory does not exist in game."""
    factories = FactoryDisplays.new(
        [
            FactoryDisplay.new([ColoredTile.BLACK] * 4),
            FactoryDisplay.new([ColoredTile.BLACK] * 4),
        ]
    )
    table_center = UnpickedTableCenter.default()
    tile_pool = FactoryDisplay.new([ColoredTile.BLACK] * 4)

    result = factory_offer.select_tiles(
        factories, table_center, tile_pool, ColoredTile.BLACK
    )

    assert result is None


def test_factory_no_tiles() -> None:
    """Tests that output is None when selected tiles are not in factory display."""
    raw_factories = [
        FactoryDisplay.new([ColoredTile.BLACK] * 4),
        FactoryDisplay.new([ColoredTile.BLACK] * 4),
    ]
    factories = FactoryDisplays.new(raw_factories)
    table_center = UnpickedTableCenter.default()
    tile_pool = raw_factories[0]

    result = factory_offer.select_tiles(
        factories, table_center, tile_pool, ColoredTile.BLUE
    )

    assert result is None


def test_picked_center() -> None:
    """Tests that output exists when picked table center selection is valid."""
    raw_factories = [
        FactoryDisplay.new([ColoredTile.BLUE] * 2 + [ColoredTile.BLACK] * 2),
        FactoryDisplay.new([ColoredTile.BLUE] * 2 + [ColoredTile.BLACK] * 2),
    ]
    factories = FactoryDisplays.new(raw_factories)
    table_center = PickedTableCenter.new(
        [ColoredTile.BLUE] * 2 + [ColoredTile.BLACK] * 2
    )
    tile_pool = table_center

    result = factory_offer.select_tiles(
        factories, table_center, tile_pool, ColoredTile.BLACK
    )

    assert result is not None
    assert len(result.factory_displays) == 2
    assert isinstance(result.table_center, PickedTableCenter)
    assert result.table_center.count(ColoredTile.BLUE) == 2
    assert result.table_center.count(ColoredTile.BLACK) == 0
    assert result.tiles == tuple([ColoredTile.BLACK] * 2)


def test_picked_center_not_in_game() -> None:
    """Tests that output is None when picked table center is not in game."""
    factories = FactoryDisplays.new(
        [
            FactoryDisplay.new([ColoredTile.BLACK] * 4),
            FactoryDisplay.new([ColoredTile.BLACK] * 4),
        ]
    )
    table_center = PickedTableCenter.new([ColoredTile.BLACK] * 4)
    tile_pool = PickedTableCenter.new([ColoredTile.BLACK] * 4)
    result = factory_offer.select_tiles(
        factories, table_center, tile_pool, ColoredTile.BLACK
    )

    assert result is None


def test_picked_center_no_tiles() -> None:
    """Tests that output is None when selected tiles are not in picked table center."""
    factories = FactoryDisplays.new(
        [
            FactoryDisplay.new([ColoredTile.BLACK] * 4),
            FactoryDisplay.new([ColoredTile.BLACK] * 4),
        ]
    )
    table_center = PickedTableCenter.new([])
    tile_pool = PickedTableCenter.new([ColoredTile.BLACK] * 4)
    result = factory_offer.select_tiles(
        factories,
        table_center,
        tile_pool,
        ColoredTile.BLUE,
    )

    assert result is None


def test_unpicked_center() -> None:
    """Tests that output exists when unpicked table center selection is valid."""
    raw_factories = [
        FactoryDisplay.new([ColoredTile.BLUE] * 2 + [ColoredTile.BLACK] * 2),
        FactoryDisplay.new([ColoredTile.BLUE] * 2 + [ColoredTile.BLACK] * 2),
    ]
    factories = FactoryDisplays.new(raw_factories)
    table_center = UnpickedTableCenter.new(
        [ColoredTile.BLUE] * 2 + [ColoredTile.BLACK] * 2
    )
    tile_pool = table_center

    result = factory_offer.select_tiles(
        factories, table_center, tile_pool, ColoredTile.BLACK
    )

    assert result is not None

    assert len(result.factory_displays) == 2

    assert isinstance(result.table_center, PickedTableCenter)
    assert result.table_center.count(ColoredTile.BLUE) == 2
    assert result.table_center.count(ColoredTile.BLACK) == 0

    assert len(result.tiles) == 3
    black_count = len(
        [tile for tile in result.tiles if tile == ColoredTile.BLACK]
    )
    assert black_count == 2
    starting_count = len(
        [
            tile
            for tile in result.tiles
            if isinstance(tile, StartingPlayerMarker)
        ]
    )
    assert starting_count == 1


def test_unpicked_center_not_in_game() -> None:
    """Tests that output is None when unpicked table center is not in game."""
    factories = FactoryDisplays.new(
        [
            FactoryDisplay.new([ColoredTile.BLACK] * 4),
            FactoryDisplay.new([ColoredTile.BLACK] * 4),
        ]
    )
    table_center = UnpickedTableCenter.new([ColoredTile.BLACK] * 4)
    tile_pool = UnpickedTableCenter.new([ColoredTile.BLACK] * 4)
    result = factory_offer.select_tiles(
        factories,
        table_center,
        tile_pool,
        ColoredTile.BLACK,
    )

    assert result is None


def test_unpicked_center_no_tiles() -> None:
    """Tests that output is None when selected tiles are not in unpicked table center."""
    factories = FactoryDisplays.new(
        [
            FactoryDisplay.new([ColoredTile.BLACK] * 4),
            FactoryDisplay.new([ColoredTile.BLACK] * 4),
        ]
    )
    table_center = UnpickedTableCenter.new([ColoredTile.BLACK] * 4)
    tile_pool = table_center
    result = factory_offer.select_tiles(
        factories,
        table_center,
        tile_pool,
        ColoredTile.BLUE,
    )

    assert result is None
