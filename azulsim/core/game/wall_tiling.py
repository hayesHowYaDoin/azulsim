"""Defines the wall tiling (scoring) phase."""

from __future__ import annotations
from collections import deque
from typing import Optional, Sequence

from pydantic import NonNegativeInt

from ..board import (
    Board,
    EmptyWallSpace,
    PopulatedWallSpace,
    PopulatedPatternLine,
    Wall,
    WallLine,
    calculate_floor_penalty,
)
from ..tiles import StartingPlayerMarker


def _tile_wall(board: Board) -> Board:
    for line_number, pattern_line in enumerate(board.pattern_lines):
        if (
            isinstance(pattern_line, PopulatedPatternLine)
            and pattern_line.tile_count == line_number
        ):
            wall_line = board.wall[line_number]
            wall_line.populate_tile(color=pattern_line.color)

    return board


def _score_tile(
    wall: Wall, line_index: NonNegativeInt, tile_index: NonNegativeInt
) -> NonNegativeInt:
    # TODO: Implement tile-scoring algorithm
    return 0


def _score_board(previous: Board, current: Board) -> Board:
    earned_score = 0
    for line_index in range(Wall.line_count()):
        for tile_index in range(WallLine.tile_count()):
            previous_tile = previous.wall[line_index].tiles[tile_index]
            current_tile = current.wall[line_index].tiles[tile_index]
            if isinstance(current_tile, PopulatedWallSpace) and isinstance(
                previous_tile, EmptyWallSpace
            ):
                earned_score += _score_tile(
                    current.wall, line_index, tile_index
                )

    deduction = calculate_floor_penalty(current.floor_line)

    total_score = current.score_track + earned_score + deduction

    return Board.new(
        total_score,
        current.pattern_lines,
        current.floor_line,
        current.wall,
    )


def _rotate_turn_order(players: deque[Board], first: Board) -> deque[Board]:  # type: ignore
    if len(players) == 0:
        raise ValueError("Players object contains no players.")
    if first not in players:
        raise ValueError("Player does not exist.")

    while players[0] != first:
        players.rotate()

    return players


def _discard_tiles(board: Board) -> Board:
    return Board.new(
        board.score_track,
        board.pattern_lines,
        board.floor_line,
        board.wall,
    )


def wall_tiling(boards: Sequence[Board]) -> deque[Board]:
    """Returns the boards tiled and scored."""
    updated_boards: deque[Board] = deque([])
    starting_player: Optional[Board] = None
    for board in boards:
        updated_board = _tile_wall(board)
        updated_board = _score_board(board, updated_board)

        floor_line = updated_board.floor_line
        if any(isinstance(t, StartingPlayerMarker) for t in floor_line.tiles):
            starting_player = updated_board
        updated_board = _discard_tiles(updated_board)

        updated_boards.append(updated_board)

    assert (
        starting_player is not None
    ), "No board contains starting player token, gameplay loop likely incomplete."
    updated_boards = _rotate_turn_order(updated_boards, starting_player)

    return updated_boards
