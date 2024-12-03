"""Defines the factory offer phase."""

from collections import deque
from typing import Callable

from pydantic.dataclasses import dataclass
from pydantic.types import PositiveInt

from .state import GameState
from ..board import Board
from ..factory import (
    FactoryDisplay,
    TableCenter,
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


def factory_offer(
    state: GameState,
    _board: Board,
    _pick_strategy: Callable[[GameState, Board], FactoryOfferSelection],
) -> GameState:
    return state


def factory_offer_end(
    factory_displays: set[FactoryDisplay], table_center: TableCenter
) -> bool:
    return False
