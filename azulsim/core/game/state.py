"""Defines the encapsulation of game state."""

from __future__ import annotations
from collections import deque

from pydantic.dataclasses import dataclass

from azulsim.core.tiles import TileBag, TileDiscard

from ..board import Board
from ..factory import FactoryDisplay, TableCenter


@dataclass
class GameState:
    """Aggregation of game state."""

    boards: deque[Board]
    factory_displays: set[FactoryDisplay]
    table_center: TableCenter
    tile_bag: TileBag
    tile_discard: TileDiscard
