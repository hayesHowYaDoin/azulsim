"""Defines the factory offer phase."""

from collections import deque
from typing import Optional, Sequence

from pydantic.dataclasses import dataclass
from pydantic.types import PositiveInt

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
    pattern_line_number: PositiveInt


# TODO: To be used in factory offer phase when implemented
def _rotate_turn_order(players: deque[Board], first: Board) -> deque[Board]:  # type: ignore
    if len(players) == 0:
        raise ValueError("Players object contains no players.")
    if first not in players:
        raise ValueError("Player does not exist.")

    while players[0] != first:
        players.rotate()

    return players


def select_tiles(
    factories: FactoryDisplays,
    table_center: TableCenter,
    tile_pool: PickableTilePool,
    color: ColoredTile,
) -> Optional[tuple[FactoryDisplays, TableCenter]]:
    match tile_pool:
        case FactoryDisplay():
            if tile_pool in factories and tile_pool.count(color) != 0:
                factories = factories.remove(tile_pool)
        case PickedTableCenter() | UnpickedTableCenter():
            if tile_pool.count(color) != 0:
                table_center = table_center.pick(color)

    return factories, table_center


def phase_end(
    factory_displays: Sequence[FactoryDisplay], table_center: TableCenter
) -> bool:
    return False
