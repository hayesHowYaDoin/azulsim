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

    @staticmethod
    def new(state: State) -> RoundSetup:
        return RoundSetup(_state=state)

    @property
    def state(self) -> State:
        return self._state

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

        return FactoryOffer.new(self._state)


@dataclass(kw_only=True)
class FactoryOffer:
    _state: State
    _next_board_index: NonNegativeInt

    @staticmethod
    def new(state: State) -> FactoryOffer:
        return FactoryOffer(_state=state, _next_board_index=0)

    @property
    def state(self) -> State:
        return self._state

    @property
    def next_board(self) -> Board:
        return self.state.boards[self._next_board_index]

    def factory_offer(
        self,
        tile_pool: PickableTilePool,
        color: ColoredTile,
        line_index: Annotated[int, Ge(0), Le(PatternLines.line_count())],
    ) -> Optional[Self | WallTiling]:
        board = self.next_board

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
        self._state.boards[self._next_board_index] = updated_board

        self._next_board_index = (self._next_board_index + 1) % len(
            self._state.boards
        )

        next_state = self
        if factory_offer.phase_end(
            self._state.factory_displays, self._state.table_center
        ):
            next_state = WallTiling.new(self._state)

        return next_state


@dataclass(kw_only=True)
class WallTiling:
    _state: State

    @staticmethod
    def new(state: State) -> WallTiling:
        return WallTiling(_state=state)

    @property
    def state(self) -> State:
        return self._state

    def tile_boards(self) -> RoundSetup:
        self._state.boards, self._state.discard = wall_tiling.tile_boards(
            self._state.boards, self._state.discard
        )

        return RoundSetup.new(self._state)


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

    return FactoryOffer.new(state)
