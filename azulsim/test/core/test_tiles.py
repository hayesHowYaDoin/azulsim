"""Contains unit tests for the azulsim.core.tiles module."""

from azulsim.core.tiles import (
    ColoredTile,
    TileBag,
    TileDiscard,
    reset_tile_bag,
)


def test_tile_bag_default() -> None:
    """Tests that the default constructor for a tile bag is valid."""
    bag = TileBag.default()
    assert len(bag.tiles) == 100
    assert bag.tiles.count(ColoredTile.BLACK) == 20
    assert bag.tiles.count(ColoredTile.WHITE) == 20
    assert bag.tiles.count(ColoredTile.BLUE) == 20
    assert bag.tiles.count(ColoredTile.YELLOW) == 20
    assert bag.tiles.count(ColoredTile.RED) == 20


def test_tile_bag_new() -> None:
    """Tests that the new constructor for a tile bag is valid."""
    tiles = [ColoredTile.BLACK, ColoredTile.WHITE, ColoredTile.BLUE]
    bag = TileBag.new(tiles)
    assert len(bag.tiles) == 3
    assert bag.tiles == tuple(tiles)


def test_tile_bag_add() -> None:
    """Tests that tiles can be added to a tile bag via the new method."""
    bag = TileBag.default()
    new_tiles = (ColoredTile.BLACK, ColoredTile.WHITE)
    new_bag = bag.add(new_tiles)
    assert len(new_bag.tiles) == 102
    assert new_bag.tiles.count(ColoredTile.BLACK) == 21
    assert new_bag.tiles.count(ColoredTile.WHITE) == 21


def test_tile_bag_pull() -> None:
    """Tests that tiles can be removed from the tile bag via the pull method."""
    bag = TileBag.default()
    tile, new_bag = bag.pull(lambda x: ColoredTile.BLACK)
    assert tile is ColoredTile.BLACK
    assert len(new_bag.tiles) == 99


def test_tile_bag_pull_empty() -> None:
    """Tests that the pull method returns no new tiles and the same bag when the tile bag is empty."""
    bag = TileBag.new([])
    tile, new_bag = bag.pull(lambda x: ColoredTile.BLACK)
    assert tile is None
    assert len(new_bag.tiles) == 0


def test_tile_discard_default() -> None:
    """Tests that the default constructor for tile discard is valid."""
    discard = TileDiscard.default()
    assert len(discard.tiles) == 0
    assert discard.tiles == ()


def test_tile_discard_new() -> None:
    """Tests that the new constructor for tile discard is valid"""
    tiles = [ColoredTile.BLACK, ColoredTile.WHITE, ColoredTile.BLUE]
    discard = TileDiscard.new(tiles)
    assert len(discard.tiles) == 3
    assert discard.tiles == tuple(tiles)


def test_tile_discard_add() -> None:
    """Tests that the add method of tile discard returns the object with the added tiles."""
    discard = TileDiscard.new([ColoredTile.BLACK])
    new_tiles = (ColoredTile.WHITE, ColoredTile.BLUE)
    new_discard = discard.add(new_tiles)
    assert len(new_discard.tiles) == 3
    assert new_discard.tiles.count(ColoredTile.BLACK) == 1
    assert new_discard.tiles.count(ColoredTile.WHITE) == 1
    assert new_discard.tiles.count(ColoredTile.BLUE) == 1


def test_reset_tile_bag() -> None:
    """Tests that the reset_tile_bag method moves all tiles from the tile discard to the tile bag."""
    bag = TileBag.new([ColoredTile.BLACK])
    discard = TileDiscard.new([ColoredTile.WHITE, ColoredTile.BLUE])
    new_bag, new_discard = reset_tile_bag(bag, discard)
    assert len(new_bag.tiles) == 3
    assert new_bag.tiles.count(ColoredTile.BLACK) == 1
    assert new_bag.tiles.count(ColoredTile.WHITE) == 1
    assert new_bag.tiles.count(ColoredTile.BLUE) == 1
    assert len(new_discard.tiles) == 0
