"""Defines a game board."""

from __future__ import annotations
from typing import Generator, Sequence

from pydantic import NonNegativeInt
from pydantic.types import PositiveInt
from pydantic.dataclasses import dataclass

from .scoring import GameScore
from .pattern import PatternLines
from .floor import FloorLine
from .wall import Wall


@dataclass(frozen=True, kw_only=True)
class Board:
    """A player board in a game."""

    score_track: GameScore
    pattern_lines: PatternLines
    floor_line: FloorLine
    wall: Wall

    @staticmethod
    def default() -> Board:
        """Returns a board with defaulted sections."""
        return Board(
            score_track=GameScore.default(),
            pattern_lines=PatternLines.default(),
            floor_line=FloorLine.default(),
            wall=Wall.default(),
        )

    @staticmethod
    def new(
        score_track: GameScore,
        pattern_lines: PatternLines,
        floor_line: FloorLine,
        wall: Wall,
    ) -> Board:
        """Returns a board with the argument sections."""
        return Board(
            score_track=score_track,
            pattern_lines=pattern_lines,
            floor_line=floor_line,
            wall=wall,
        )


@dataclass(frozen=True, kw_only=True)
class Boards:
    boards: list[Board]
    starting_board_index: NonNegativeInt

    @staticmethod
    def with_defaulted(board_count: PositiveInt) -> Boards:
        """Returns a Boards object with the given number of defaulted Boards."""
        boards = (Board.default() for _ in range(board_count))
        return Boards(boards=list(boards), starting_board_index=0)

    @staticmethod
    def new(
        boards: Sequence[Board], starting_board_index: NonNegativeInt
    ) -> Boards:
        """Returns a Boards object with the given Board objects in turn-order."""
        if starting_board_index < 0 or len(boards) >= len(boards):
            raise ValueError(
                f"Starting board index out of bounds (starting_board_index={starting_board_index})."
            )

        return Boards(
            boards=list(boards), starting_board_index=starting_board_index
        )

    def count(self) -> PositiveInt:
        """Returns the number of Board objects."""
        return len(self.boards)

    def set_starting_board(self, index: NonNegativeInt) -> Boards:
        """Returns the object updated to set the Board with the associated index as the first in the turn order."""
        if index < 0 or len(self.boards) <= index:
            raise ValueError(
                f"Starting board index out of bounds (index={index})."
            )

        return Boards(boards=self.boards, starting_board_index=index)

    def turn_order(self) -> Generator[NonNegativeInt, None, None]:
        """Yields the index of the next board in the underlying turn order."""
        index = self.starting_board_index
        while True:
            yield index
            index = (index + 1) % len(self.boards)

    def set_board(self, index: NonNegativeInt, board: Board) -> Boards:
        """Returns the object updated to associate the given Board with the given key."""
        if index < 0 or len(self.boards) <= index:
            raise ValueError(f"Index does not exist (index={index}).")

        boards = self.boards
        boards[index] = board

        return Boards(
            boards=boards, starting_board_index=self.starting_board_index
        )

    def __getitem__(self, index: NonNegativeInt) -> Board:
        """Returns the board associated with the given index."""
        return self.boards[index]
