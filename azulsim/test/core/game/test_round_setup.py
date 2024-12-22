"""Contains unit tests for the azulsim.core.game.round_setup module."""

from azulsim.core.game import round_setup
from azulsim.core.tiles import ColoredTile, TileBag, TileDiscard


def test_full_bag() -> None:
    """Tests that output for a full tile bag."""
    for player_count in range(1, 5):
        bag = TileBag.default()
        discard = TileDiscard.default()

        result = round_setup.reset_tile_pools(
            player_count,
            bag,
            discard,
            lambda _x: ColoredTile.BLACK,
        )

        assert len(result.bag.tiles) == len(bag.tiles) - 4 * (player_count + 1)
        assert len(result.discard.tiles) == len(discard.tiles)

        assert len(result.factory_displays) == player_count + 1
        for factory in result.factory_displays:
            assert len(factory.tiles) == 4


def test_bag_exact_needed() -> None:
    """Tests that output when the tile bag has the exact number of tiles needed to fill the factories."""
    for player_count in range(1, 5):
        num_tiles = 4 * (player_count + 1)
        bag = TileBag.new([ColoredTile.BLACK] * num_tiles)
        discard = TileDiscard.default()

        result = round_setup.reset_tile_pools(
            player_count,
            bag,
            discard,
            lambda _x: ColoredTile.BLACK,
        )

        assert len(result.bag.tiles) == 0
        assert len(result.discard.tiles) == len(discard.tiles)

        assert len(result.factory_displays) == player_count + 1
        for factory in result.factory_displays:
            assert len(factory.tiles) == 4


def test_bag_less_than_needed() -> None:
    """Tests output when the tile bag has less than the number of tiles needed to fill the factories."""
    for player_count in range(1, 5):
        num_tiles = 4 * (player_count + 1) - (player_count)
        bag = TileBag.new([ColoredTile.BLACK] * num_tiles)
        discard = TileDiscard.new([ColoredTile.BLACK] * 50)

        result = round_setup.reset_tile_pools(
            player_count,
            bag,
            discard,
            lambda _x: ColoredTile.BLACK,
        )

        assert len(result.bag.tiles) == 50 - player_count
        assert len(result.discard.tiles) == 0

        assert len(result.factory_displays) == player_count + 1
        for factory in result.factory_displays:
            assert len(factory.tiles) == 4


def test_bag_empty() -> None:
    """Tests output when the tile bag is completely empty."""
    for player_count in range(1, 5):
        bag = TileBag.new([])
        discard = TileDiscard.new([ColoredTile.BLACK] * 50)

        result = round_setup.reset_tile_pools(
            player_count,
            bag,
            discard,
            lambda _x: ColoredTile.BLACK,
        )

        assert len(result.bag.tiles) == 50 - (4 * (player_count + 1))
        assert len(result.discard.tiles) == 0

        assert len(result.factory_displays) == player_count + 1
        for factory in result.factory_displays:
            assert len(factory.tiles) == 4
