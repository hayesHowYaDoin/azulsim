"""Defines the end of game phase."""

from typing import Iterable

from azulsim.core.tiles import ColoredTile

from ..board import Board, PopulatedWallSpace, WallLine


def _score_board_bonuses(board: Board) -> Board:
    # Horizontal rows
    horizontal_count = 0
    for line in board.wall:
        if all(isinstance(space, PopulatedWallSpace) for space in line):
            horizontal_count += 1

    # Vertical rows
    vertical_count = 0
    for space_index in range(WallLine.tile_count()):
        if all(
            isinstance(line[space_index], PopulatedWallSpace)
            for line in board.wall
        ):
            vertical_count += 1

    # All of color
    color_counts = {color: 0 for color in ColoredTile}
    for line in board.wall:
        for space in line:
            if isinstance(space, PopulatedWallSpace):
                color_counts[space.color] += 1
    color_count = sum(count == 5 for count in color_counts.values())

    final_score = (
        board.score_track
        + horizontal_count * 2
        + vertical_count * 7
        + color_count * 10
    )

    return Board.new(
        final_score,
        board.pattern_lines,
        board.floor_line,
        board.wall,
    )


def score_bonuses(boards: Iterable[Board]) -> tuple[Board, ...]:
    """Adds end-of-game bonuses to each board and returns the updated boards.

    Args:
        boards: Boards in the current game to which bonuses should be applied.

    Returns:
        List of updated boards in the same order as they were passed in.
    """

    return tuple(_score_board_bonuses(board) for board in boards)
