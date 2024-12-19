"""Defines the factory offer phase."""

from collections import deque
from typing import Optional

from pydantic.dataclasses import dataclass
from pydantic.types import NonNegativeInt, PositiveInt

from ..board import Board
from ..factory import (
    FactoryDisplay,
    FactoryDisplays,
    PickedTableCenter,
    UnpickedTableCenter,
    TableCenter,
    PickableTilePool,
)
from ..tiles import ColoredTile


@dataclass(frozen=True, kw_only=True)
class FactoryOfferSelection:
    """A valid move for a player to take during the factory offer phase."""

    factory_display: FactoryDisplay
    color: ColoredTile


def select_tiles(
    factories: FactoryDisplays,
    table_center: TableCenter,
    tile_pool: PickableTilePool,
    color: ColoredTile,
) -> Optional[tuple[NonNegativeInt, FactoryDisplays, TableCenter]]:
    count = tile_pool.count(color)
    match tile_pool:
        case FactoryDisplay():
            if tile_pool not in factories or count == 0:
                return None
            table_center = table_center.add(
                tuple(tile for tile in tile_pool.tiles if tile != color)
            )
            factories = factories.remove(tile_pool)
        case PickedTableCenter() | UnpickedTableCenter():
            if count == 0:
                return None
            table_center = table_center.pick(color)

    return count, factories, table_center


def place_tiles(
    board: Board,
    color: ColoredTile,
    count: PositiveInt,
) -> Optional[Board]:
    return board


def phase_end(
    factory_displays: FactoryDisplays,
    table_center: TableCenter,
) -> bool:
    return factory_displays.empty() and table_center.empty()


# TODO: To be used in factory offer phase when implemented
def _rotate_turn_order(players: deque[Board], first: Board) -> deque[Board]:  # type: ignore
    if len(players) == 0:
        raise ValueError("Players object contains no players.")
    if first not in players:
        raise ValueError("Player does not exist.")

    while players[0] != first:
        players.rotate()

    return players
