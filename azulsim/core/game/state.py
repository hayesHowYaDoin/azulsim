"""Defines the encapsulation of game state."""

from __future__ import annotations
from collections import deque
import random

from pydantic import PositiveInt
from pydantic.dataclasses import dataclass

from .round_setup import round_setup
from ..board import Board
from ..factory import FactoryDisplays, TableCenter
from ..tiles import TileBag, TileDiscard


@dataclass(kw_only=True)
class GameState:
    """Aggregation of game state."""

    boards: deque[Board]
    factory_displays: FactoryDisplays
    table_center: TableCenter
    bag: TileBag
    discard: TileDiscard

    @staticmethod
    def new(player_count: PositiveInt, seed: int) -> GameState:
        """Returns a state object for a new game.

        Args:
            player_count: Number of players in the game.
            seed: Seed used for random number generation.

        Returns:
            A constructed game state object.
        """
        random.seed(seed)

        boards = deque([Board.default()] * player_count)
        boards, factory_displays, table_center, bag, discard = round_setup(
            boards,
            TileBag.default(),
            TileDiscard.default(),
            selection_strategy=lambda x: random.sample(x, 1)[0],
        )

        return GameState(
            boards=boards,
            factory_displays=factory_displays,
            table_center=table_center,
            bag=bag,
            discard=discard,
        )
