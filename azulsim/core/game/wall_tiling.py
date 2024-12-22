"""Defines the wall tiling (scoring) phase."""

from __future__ import annotations
from collections import deque
from typing import Sequence

from pydantic.types import NonNegativeInt

from azulsim.core.board.pattern import EmptyPatternLine

from ..board import (
    Board,
    EmptyWallSpace,
    PopulatedWallSpace,
    PopulatedPatternLine,
    Wall,
    WallLine,
    WallSpace,
    PatternLine,
    PatternLines,
    FloorLine,
    calculate_floor_penalty,
)
from ..tiles import ColoredTile, TileDiscard


def _tile_wall(board: Board, discard: TileDiscard) -> tuple[Board, TileDiscard]:
    pattern_lines: list[PatternLine] = []
    wall_lines: list[WallLine] = []
    for line_index, (pattern_line, wall_line) in enumerate(
        zip(board.pattern_lines, board.wall)
    ):
        if (
            isinstance(pattern_line, PopulatedPatternLine)
            and pattern_line.tile_count == line_index + 1
        ):
            color = pattern_line.color
            discard = discard.add([color] * (pattern_line.tile_count - 1))
            pattern_line = EmptyPatternLine()

            wall_line = wall_line.populate_tile(color=color)

        pattern_lines.append(pattern_line)
        wall_lines.append(wall_line)

    board = Board.new(
        board.score_track,
        PatternLines.new(pattern_lines),
        board.floor_line,
        Wall.new(wall_lines),
    )
    return board, discard


def _score_sequence(
    spaces: Sequence[WallSpace],
    start_index: NonNegativeInt,
) -> NonNegativeInt:
    score = 1

    # Score left
    for space in reversed(spaces[:start_index]):
        if isinstance(space, EmptyWallSpace):
            break
        score = score + 1

    # Score right
    for space in spaces[start_index + 1 :]:
        if isinstance(space, EmptyWallSpace):
            break
        score = score + 1

    return score


def _score_tile(
    wall: Wall,
    line_index: NonNegativeInt,
    tile_index: NonNegativeInt,
) -> NonNegativeInt:
    if isinstance(wall[line_index][tile_index], EmptyWallSpace):
        raise ValueError("Cannot score empty tile space in wall.")

    horizontal = tuple(space for space in wall[line_index])
    horizontal_score = _score_sequence(horizontal, tile_index)

    vertical = tuple(line[tile_index] for line in wall)
    vertical_score = _score_sequence(vertical, line_index)

    score = (horizontal_score if horizontal_score > 1 else 0) + (
        vertical_score if vertical_score > 1 else 0
    )
    return max(score, 1)


def _clear_floor_line(
    floor: FloorLine, discard: TileDiscard
) -> tuple[FloorLine, TileDiscard]:
    colored_tiles = tuple(
        tile for tile in floor.tiles if isinstance(tile, ColoredTile)
    )
    discard = discard.add(colored_tiles)

    return FloorLine.default(), discard


def _score_board(
    previous: Board, current: Board, discard: TileDiscard
) -> tuple[Board, TileDiscard]:
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
    floor_line, discard = _clear_floor_line(current.floor_line, discard)

    total_score = current.score_track + earned_score + deduction

    board = Board.new(
        total_score,
        current.pattern_lines,
        floor_line,
        current.wall,
    )

    return board, discard


def wall_tiling(
    boards: Sequence[Board], discard: TileDiscard
) -> tuple[deque[Board], TileDiscard]:
    """Returns the boards tiled and scored."""
    updated_boards: deque[Board] = deque([])
    for board in boards:
        updated_board, discard = _tile_wall(board, discard)
        updated_board, discard = _score_board(board, updated_board, discard)

        updated_boards.append(updated_board)

    return updated_boards, discard
