"""Defines the highest-level representation of a game of Azul."""

from __future__ import annotations
from annotated_types import Ge, Le
import random
from typing import Annotated, Optional, Self, TypeAlias

from pydantic import NonNegativeInt, PositiveInt
from pydantic.dataclasses import dataclass

from .board import Board, PatternLines
from .factory import FactoryDisplays, TableCenter, PickableTilePool
from .phases import factory_offer, round_setup, wall_tiling, end_of_game
from .tiles import TileBag, TileDiscard, ColoredTile


@dataclass(kw_only=True)
class State:
    """Representation of the current state of a game of Azul."""

    boards: list[Board]
    factory_displays: FactoryDisplays
    table_center: TableCenter
    bag: TileBag
    discard: TileDiscard


@dataclass(kw_only=True)
class RoundSetup:
    """Round setup gameplay phase."""

    _state: State

    @staticmethod
    def new(state: State) -> RoundSetup:
        """Returns an initialized RoundSetup object with the given state."""
        return RoundSetup(_state=state)

    @property
    def state(self) -> State:
        """Returns the internal game state."""
        return self._state

    def round_setup(self) -> FactoryOffer:
        """Executes the round setup phase and returns the next state.

        Returns:
            A FactoryOffer object constructed with the updated state.
        """
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

        return FactoryOffer.new(self._state)


@dataclass(kw_only=True)
class FactoryOffer:
    """Factory offer gameplay phase."""

    _state: State
    _next_board_index: NonNegativeInt

    @staticmethod
    def new(state: State) -> FactoryOffer:
        """Returns an initialized FactoryOffer object with the given state."""
        return FactoryOffer(_state=state, _next_board_index=0)

    @property
    def state(self) -> State:
        """Returns the internal game state."""
        return self._state

    @property
    def next_board(self) -> Board:
        """Returns the next board in the turn order."""
        return self.state.boards[self._next_board_index]

    def factory_offer(
        self,
        tile_pool: PickableTilePool,
        color: ColoredTile,
        line_index: Annotated[int, Ge(0), Le(PatternLines.line_count())],
    ) -> Optional[Self | WallTiling]:
        """Executes the factory offer phase for the next board and returns the
        next state.

        Note: The turn-order is tracked internally by the FactoryOffer object.
        To indicate to an external player that it is their turn, invoke the
        next_board method first, then associate that Board with a player.

        Args:
            tile_pool: The selected tile pool from which to pick from.
            color: The tile color selected from the tile pool.
            line_index: The pattern line in which to place the colord tiles.

        Returns:
            The updated FactoryOffer object or a WallTiling object constructed
            with the current state. If the argument selection is invalid,
            returns None.
        """
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
    """Wall-tiling gameplay phase."""

    _state: State

    @staticmethod
    def new(state: State) -> WallTiling:
        """Returns an initialized WallTiling object with the given state."""
        return WallTiling(_state=state)

    @property
    def state(self) -> State:
        """Returns the internal game state."""
        return self._state

    def tile_boards(self) -> RoundSetup | GameEnd:
        """
        Executes the wall tiling phase and returns the next state.

        Returns:
            A RoundSetup object constructed with the updated state.
        """
        self._state.boards = wall_tiling.rotate_starting_player(
            self._state.boards
        )
        self._state.boards, self._state.discard = wall_tiling.tile_boards(
            self._state.boards, self._state.discard
        )

        if wall_tiling.game_end((board.wall for board in self._state.boards)):
            return GameEnd.new(self._state)

        return RoundSetup.new(self._state)


@dataclass(kw_only=True)
class GameEnd:
    _state: State

    @staticmethod
    def new(state: State) -> GameEnd:
        """Returns an initialized GameEnd object with the given state."""
        return GameEnd(_state=state)

    @property
    def state(self) -> State:
        """Returns the internal game state."""
        return self._state

    def score_bonuses(self) -> State:
        """Adds end-of-game bonuses to each board and returns the updated
        boards in descending order of their scores.

        Returns:
            List of updated boards in the same order as they were passed in.
        """
        scores = (
            end_of_game.score_bonuses(board.wall, board.score_track)
            for board in self._state.boards
        )

        scored_boards: list[Board] = []
        for board, score in zip(self._state.boards, scores):
            scored_boards.append(
                Board.new(
                    score,
                    board.pattern_lines,
                    board.floor_line,
                    board.wall,
                )
            )

        self._state.boards = scored_boards
        return self._state


"""Game state machine object encapsulating internal state and possible operations at each phase."""
Game: TypeAlias = RoundSetup | FactoryOffer | WallTiling | GameEnd


def new_game(player_count: PositiveInt, seed: NonNegativeInt) -> FactoryOffer:
    """Returns a new game.

    Args:
        player_count: Number of players in the game.
        seed: Seed used for random number generation.

    Returns:
        A constructed game object.
    """
    random.seed(seed)

    boards = [Board.default()] * player_count
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
