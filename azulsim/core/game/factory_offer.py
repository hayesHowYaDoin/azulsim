from collections import deque
from typing import Callable, Optional

from pydantic.dataclasses import dataclass
from pydantic.types import PositiveInt

from .state import GameState
from ..board import Board
from ..factory import (
    FactoryDisplay,
    PickedTableCenter,
    TableCenter,
    UnpickedTableCenter,
)
from ..tiles import ColoredTile


@dataclass(frozen=True)
class FactoryOfferSelection:
    factory_display: FactoryDisplay
    color: ColoredTile
    pattern_line_number: PositiveInt


def _rotate_turn_order(players: deque[Board], first: Board) -> deque[Board]:
    if len(players) == 0:
        raise ValueError("Players object contains no players.")
    if first not in players:
        raise ValueError("Player does not exist.")

    while players[0] != first:
        players.rotate()

    return players


def factory_offer(
    state: GameState,
    board: Board,
    pick_strategy: Callable[[GameState, Board], FactoryOfferSelection],
) -> GameState:
    next_state: Optional[GameState] = None
    while next_state is None:
        _selection = pick_strategy(state, board)
        try:
            pass
            # _update_display
            # board = _update_board(board, selection)
        except ValueError as _ex:
            pass

    if isinstance(state.table_center, UnpickedTableCenter):
        state.boards = _rotate_turn_order(state.boards, board)

    return state


def factory_offer_end(
    factory_displays: set[FactoryDisplay], table_center: TableCenter
) -> bool:
    """Returns True if the factory display phase has ended, otherwise returns False."""
    no_factory_displays = len(factory_displays) == 0
    table_center_empty = (
        isinstance(table_center, PickedTableCenter)
        and len(table_center.tiles) == 0
    )

    return no_factory_displays and table_center_empty
