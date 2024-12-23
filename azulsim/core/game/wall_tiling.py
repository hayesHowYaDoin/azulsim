"""Defines the wall tiling (scoring) phase."""

from __future__ import annotations
from collections import deque
from typing import Optional, Sequence

from pydantic.types import NonNegativeInt

from azulsim.core.board.pattern import EmptyPatternLine
from azulsim.core.board.wall import PopulatedWallSpace

from ..board import (
    Board,
    EmptyWallSpace,
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
    wall: Sequence[WallLine],
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


def tile_board(board: Board, discard: TileDiscard) -> tuple[Board, TileDiscard]:
    """Returns the board tiled and scored with the updated discard pile."""
    earned_score = 0
    pattern_lines: list[PatternLine] = []
    wall_lines: list[WallLine] = list(board.wall.lines)
    for line_index, (pattern_line, wall_line) in enumerate(
        zip(board.pattern_lines, board.wall)
    ):
        if (
            isinstance(pattern_line, PopulatedPatternLine)
            and pattern_line.tile_count == line_index + 1
        ):
            color = pattern_line.color
            newly_populated = isinstance(wall_lines[line_index], EmptyWallSpace)

            if newly_populated:
                wall_lines[line_index] = wall_line.populate_tile(color=color)

                tile_index: Optional[NonNegativeInt] = None
                for index, space in enumerate(wall_line):
                    if space.color == color:
                        tile_index = index
                assert (
                    tile_index is not None
                ), "Could not find tile of color in wall line."

                earned_score += _score_tile(wall_lines, line_index, tile_index)
                discarded_tile_count = pattern_line.tile_count - 1
            else:
                discarded_tile_count = pattern_line.tile_count

            discard = discard.add([color] * discarded_tile_count)
            pattern_line = EmptyPatternLine()

        pattern_lines.append(pattern_line)

    deduction = calculate_floor_penalty(board.floor_line)
    floor_line, discard = _clear_floor_line(board.floor_line, discard)

    score = board.score_track + earned_score + deduction

    board = Board.new(
        score,
        PatternLines.new(pattern_lines),
        floor_line,
        Wall.new(wall_lines),
    )
    return board, discard


def tile_boards(
    boards: Sequence[Board], discard: TileDiscard
) -> tuple[deque[Board], TileDiscard]:
    """Returns the boards tiled and scored with the updated discard pile."""
    updated_boards: deque[Board] = deque([])
    for board in boards:
        updated_board, discard = tile_board(board, discard)
        updated_boards.append(updated_board)

    return updated_boards, discard
