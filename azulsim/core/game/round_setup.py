"""Defines the round setup phase."""

from typing import Callable, Sequence

from pydantic.types import PositiveInt
from pydantic.dataclasses import dataclass

from ..factory import FactoryDisplay, FactoryDisplays, UnpickedTableCenter
from ..tiles import (
    ColoredTile,
    TileBag,
    TileDiscard,
    reset_tile_bag,
)


@dataclass(frozen=True, kw_only=True)
class ResetTilePoolsResult:
    """Updated state from resetting the tile pools.

    Attributes:
        factory_displays: Updated factory displays.
        table_center: Table center reset to unpicked state.
        bag: Updated bag of game tiles.
        discard: Updated collection of discarded game tiles.
    """

    factory_displays: FactoryDisplays
    table_center: UnpickedTableCenter
    bag: TileBag
    discard: TileDiscard


def reset_tile_pools(
    player_count: PositiveInt,
    bag: TileBag,
    discard: TileDiscard,
    selection_strategy: Callable[[Sequence[ColoredTile]], ColoredTile],
) -> ResetTilePoolsResult:
    """Returns updated game components from refilling the factory displays and clearing the table center.

    Args:
        player_count: Number of players in the current game.
        bag: Tile bag state for the current game.
        discard: Tile discard state for the current game.
        selection_strategy: Invocable strategy for selecting a tile from the tile bag.

    Returns:
        Aggregation of updated state objects.
    """
    factory_displays: list[FactoryDisplay] = list()
    for _ in range(player_count + 1):
        pulled_tiles: list[ColoredTile] = []
        while len(pulled_tiles) < 4:
            new_tile, bag = bag.pull(selection_strategy)
            if new_tile is not None:
                pulled_tiles.append(new_tile)
            else:
                bag, discard = reset_tile_bag(bag, discard)

        tiles = tuple(pulled_tiles)
        assert (
            len(tiles) == 4
        ), "Number of tiles in a factory display must be 4."

        factory_displays.append(FactoryDisplay(tiles=tiles))

    updated_factory_displays = FactoryDisplays.new(factory_displays)
    updated_table_center = UnpickedTableCenter.default()

    return ResetTilePoolsResult(
        factory_displays=updated_factory_displays,
        table_center=updated_table_center,
        bag=bag,
        discard=discard,
    )
