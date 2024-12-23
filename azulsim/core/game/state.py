"""Defines the encapsulation of game state."""

from __future__ import annotations
from collections import deque
from typing import Callable, Sequence

from pydantic import PositiveInt
from pydantic.dataclasses import dataclass

from .round_setup import reset_tile_pools
from ..board import Board
from ..factory import FactoryDisplays, TableCenter
from ..tiles import ColoredTile, TileBag, TileDiscard


@dataclass(kw_only=True)
class GameState:
    """Aggregation of game state."""

    boards: deque[Board]
    factory_displays: FactoryDisplays
    table_center: TableCenter
    bag: TileBag
    discard: TileDiscard

    @staticmethod
    def new(
        player_count: PositiveInt,
        selection_strategy: Callable[[Sequence[ColoredTile]], ColoredTile],
    ) -> GameState:
        """Returns a state object for a new game.

        Args:
            player_count: Number of players in the game.
            seed: Seed used for random number generation.

        Returns:
            A constructed game state object.
        """
        boards = deque([Board.default()] * player_count)
        result = reset_tile_pools(
            len(boards),
            TileBag.default(),
            TileDiscard.default(),
            selection_strategy=selection_strategy,
        )

        return GameState(
            boards=boards,
            factory_displays=result.factory_displays,
            table_center=result.table_center,
            bag=result.bag,
            discard=result.discard,
        )
