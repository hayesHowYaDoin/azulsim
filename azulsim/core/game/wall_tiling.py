"""Defines the wall tiling (scoring) phase."""

from __future__ import annotations

from pydantic import NonNegativeInt

from ..board import EmptyWallSpace, PopulatedWallSpace

from ..board import (
    Board,
    PopulatedPatternLine,
    Wall,
    WallLine,
    calculate_floor_penalty,
)


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

    total_score = current.score_track + earned_score - deduction

    return Board.new(
        total_score,
        current.pattern_lines,
        current.floor_line,
        current.wall,
    )


def _discard_tiles(board: Board) -> Board:
    return Board.new(
        board.score_track,
        board.pattern_lines,
        board.floor_line,
        board.wall,
    )


def wall_tiling(boards: list[Board]) -> list[Board]:
    """Returns the boards tiled and scored."""
    updated_boards: list[Board] = []
    for board in boards:
        updated_board = _tile_wall(board)
        updated_board = _score_board(board, updated_board)
        updated_board = _discard_tiles(updated_board)

        updated_boards.append(updated_board)

    return boards
