"""Defines the round setup phase."""

from collections import deque
from typing import Callable, Sequence

from .state import GameState
from ..board import Board
from ..factory import FactoryDisplay, FactoryDisplays, UnpickedTableCenter
from ..tiles import ColoredTile, TileBag, TileDiscard, reset_tile_bag


def round_setup(
    boards: Sequence[Board],
    bag: TileBag,
    discard: TileDiscard,
    random_strategy: Callable[[Sequence[ColoredTile]], ColoredTile],
) -> GameState:
    """Initializes necessary components to start a round of the game.

    Args:
        boards: Sequence of all boards in the game.
        bag: The tile bag to pull from.
        discard: The discard pile to reset the bag.

    Returns:
        The modified tile bag and tile discard with the initialized set of factory displays.
    """
    player_count = len(boards)

    factory_displays: list[FactoryDisplay] = list()
    for _ in range(player_count + 1):
        pulled_tiles: list[ColoredTile] = []
        while len(pulled_tiles) < 4:
            new_tile, bag = bag.pull(random_strategy)
            if new_tile is not None:
                pulled_tiles.append(new_tile)
            else:
                bag, discard = reset_tile_bag(bag, discard)

        tiles = tuple(pulled_tiles)
        assert (
            len(tiles) == 4
        ), "Number of tiles in a factory display must be 4."

        factory_displays.append(FactoryDisplay(tiles=tiles))

    return GameState(
        boards=deque(boards),
        factory_displays=FactoryDisplays.new(factory_displays),
        table_center=UnpickedTableCenter.default(),
        bag=bag,
        discard=discard,
    )
