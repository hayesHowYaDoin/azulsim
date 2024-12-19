"""Contains unit tests for the azulsim.core.tiles module."""

from azulsim.core.tiles import (
    ColoredTile,
    TileBag,
    TileDiscard,
    reset_tile_bag,
)


def test_tile_bag_default() -> None:
    bag = TileBag.default()
    assert len(bag.tiles) == 100
    assert bag.tiles.count(ColoredTile.BLACK) == 20
    assert bag.tiles.count(ColoredTile.WHITE) == 20
    assert bag.tiles.count(ColoredTile.BLUE) == 20
    assert bag.tiles.count(ColoredTile.YELLOW) == 20
    assert bag.tiles.count(ColoredTile.RED) == 20


def test_tile_bag_new() -> None:
    tiles = [ColoredTile.BLACK, ColoredTile.WHITE, ColoredTile.BLUE]
    bag = TileBag.new(tiles)
    assert len(bag.tiles) == 3
    assert bag.tiles == tuple(tiles)


def test_tile_bag_add() -> None:
    bag = TileBag.default()
    new_tiles = (ColoredTile.BLACK, ColoredTile.WHITE)
    new_bag = bag.add(new_tiles)
    assert len(new_bag.tiles) == 102
    assert new_bag.tiles.count(ColoredTile.BLACK) == 21
    assert new_bag.tiles.count(ColoredTile.WHITE) == 21


def test_tile_bag_pull() -> None:
    bag = TileBag.default()
    tile, new_bag = bag.pull(lambda x: ColoredTile.BLACK)
    assert tile is ColoredTile.BLACK
    assert len(new_bag.tiles) == 99


def test_tile_bag_pull_empty() -> None:
    bag = TileBag.new([])
    tile, new_bag = bag.pull(lambda x: ColoredTile.BLACK)
    assert tile is None
    assert len(new_bag.tiles) == 0


def test_tile_discard_new() -> None:
    tiles = [ColoredTile.BLACK, ColoredTile.WHITE, ColoredTile.BLUE]
    discard = TileDiscard.new(tiles)
    assert len(discard.tiles) == 3
    assert discard.tiles == tuple(tiles)


def test_tile_discard_add() -> None:
    discard = TileDiscard.new([ColoredTile.BLACK])
    new_tiles = (ColoredTile.WHITE, ColoredTile.BLUE)
    new_discard = discard.add(new_tiles)
    assert len(new_discard.tiles) == 3
    assert new_discard.tiles.count(ColoredTile.BLACK) == 1
    assert new_discard.tiles.count(ColoredTile.WHITE) == 1
    assert new_discard.tiles.count(ColoredTile.BLUE) == 1


def test_reset_tile_bag() -> None:
    bag = TileBag.new([ColoredTile.BLACK])
    discard = TileDiscard.new([ColoredTile.WHITE, ColoredTile.BLUE])
    new_bag, new_discard = reset_tile_bag(bag, discard)
    assert len(new_bag.tiles) == 3
    assert new_bag.tiles.count(ColoredTile.BLACK) == 1
    assert new_bag.tiles.count(ColoredTile.WHITE) == 1
    assert new_bag.tiles.count(ColoredTile.BLUE) == 1
    assert len(new_discard.tiles) == 0
