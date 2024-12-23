"""Defines the encapsulation of game state."""

from __future__ import annotations
from annotated_types import Ge, Le
from collections import deque
import random
from typing import Annotated, Optional, Self, TypeAlias

from pydantic import NonNegativeInt, PositiveInt
from pydantic.dataclasses import dataclass

from .board import Board, PatternLines
from .factory import FactoryDisplays, TableCenter, PickableTilePool
from .phases import factory_offer, round_setup, wall_tiling
from .tiles import TileBag, TileDiscard, ColoredTile


@dataclass(kw_only=True)
class State:
    """Representation of the current state of a game of Azul."""

    boards: deque[Board]
    factory_displays: FactoryDisplays
    table_center: TableCenter
    bag: TileBag
    discard: TileDiscard


@dataclass(kw_only=True)
class RoundSetup:
    _state: State

    def round_setup(self) -> FactoryOffer:
        tile_pools_result = round_setup.reset_tile_pools(
            len(self._state.boards),
            self._state.bag,
            self._state.discard,
            lambda x: random.sample(x, 1)[0],
        )
        self._state.factory_displays = tile_pools_result.factory_displays
        self._state.table_center = tile_pools_result.table_center
        self._state.bag = tile_pools_result.bag
        self._state.discard = tile_pools_result.discard

        if round_setup.game_end((board.wall for board in self._state.boards)):
            # TODO: Move to end-of-game scoring
            pass

        return FactoryOffer(_state=self._state)


@dataclass(kw_only=True)
class FactoryOffer:
    _state: State

    def factory_offer(
        self,
        tile_pool: PickableTilePool,
        color: ColoredTile,
        board: Board,
        line_index: Annotated[int, Ge(0), Le(PatternLines.line_count())],
    ) -> Optional[Self | WallTiling]:
        if board not in self._state.boards:
            return None
        board_index = self._state.boards.index(board)

        result = factory_offer.select_tiles(
            self._state.factory_displays,
            self._state.table_center,
            tile_pool,
            color,
        )
        if not result:
            return None

        tiles = result.tiles
        updated_factory_displays = result.factory_displays
        updated_table_center = result.table_center

        updated_board = factory_offer.place_tiles(board, line_index, tiles)
        if not updated_board:
            return None

        self._state.factory_displays = updated_factory_displays
        self._state.table_center = updated_table_center
        self._state.boards[board_index] = updated_board

        next_state = self
        if factory_offer.phase_end(
            self._state.factory_displays, self._state.table_center
        ):
            next_state = WallTiling(_state=self._state)

        return next_state


@dataclass(kw_only=True)
class WallTiling:
    _state: State

    def tile_boards(self) -> RoundSetup:
        self._state.boards, self._state.discard = wall_tiling.tile_boards(
            self._state.boards, self._state.discard
        )

        return RoundSetup(_state=self._state)


Game: TypeAlias = RoundSetup | FactoryOffer | WallTiling


def new_game(player_count: PositiveInt, seed: NonNegativeInt) -> FactoryOffer:
    """Returns a new game.

    Args:
        player_count: Number of players in the game.
        seed: Seed used for random number generation.

    Returns:
        A constructed game object.
    """
    random.seed(seed)

    boards = deque([Board.default()] * player_count)
    result = round_setup.reset_tile_pools(
        len(boards),
        TileBag.default(),
        TileDiscard.default(),
        selection_strategy=lambda x: random.sample(x, 1)[0],
    )

    state = State(
        boards=boards,
        factory_displays=result.factory_displays,
        table_center=result.table_center,
        bag=result.bag,
        discard=result.discard,
    )

    return FactoryOffer(_state=state)
