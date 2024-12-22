"""Defines the round setup phase."""

from collections import deque
from typing import Callable, Optional, Sequence

from pydantic.types import PositiveInt
from pydantic.dataclasses import dataclass

from ..board import (
    Board,
    FloorLine,
    PatternLine,
    PatternLines,
    EmptyPatternLine,
    PopulatedPatternLine,
)
from ..factory import FactoryDisplay, FactoryDisplays, UnpickedTableCenter
from ..tiles import (
    ColoredTile,
    StartingPlayerMarker,
    TileBag,
    TileDiscard,
    reset_tile_bag,
)


def _rotate_turn_order(boards: deque[Board], first: Board) -> deque[Board]:  # type: ignore
    if len(boards) == 0:
        raise ValueError("Players object contains no players.")
    if first not in boards:
        raise ValueError("Player does not exist.")

    while boards[0] != first:
        boards.rotate()

    return boards


def _clear_full_pattern_lines(
    lines: PatternLines,
    discard: TileDiscard,
) -> tuple[PatternLines, TileDiscard]:
    updated_lines: list[PatternLine] = []
    for index, line in enumerate(lines):
        if (
            isinstance(line, PopulatedPatternLine)
            and line.tile_count == index + 1
        ):
            discard = discard.add([line.color] * line.tile_count)
            updated_lines.append(EmptyPatternLine())
        else:
            updated_lines.append(line)

    pattern_lines = tuple(updated_lines)
    assert len(pattern_lines) == PatternLines.line_count()
    return PatternLines.new(pattern_lines), discard


def _clear_floor_line(
    floor: FloorLine, discard: TileDiscard
) -> tuple[FloorLine, TileDiscard]:
    colored_tiles = tuple(
        tile for tile in floor.tiles if isinstance(tile, ColoredTile)
    )
    discard = discard.add(colored_tiles)

    return FloorLine.default(), discard


@dataclass(frozen=True, kw_only=True)
class ResetBoardsResult:
    boards: deque[Board]
    discard: TileDiscard


def reset_boards(
    boards: Sequence[Board], discard: TileDiscard
) -> ResetBoardsResult:
    if len(boards) == 0:
        raise ValueError("No boards in argument sequence.")

    first_player: Optional[Board] = None
    updated_boards: deque[Board] = deque([])
    for board in boards:
        pattern_lines, discard = _clear_full_pattern_lines(
            board.pattern_lines, discard
        )
        floor_line, discard = _clear_floor_line(board.floor_line, discard)

        updated_board = Board.new(
            board.score_track,
            pattern_lines,
            floor_line,
            board.wall,
        )

        floor_tiles = board.floor_line.tiles
        if any(isinstance(tile, StartingPlayerMarker) for tile in floor_tiles):
            first_player = updated_board

        updated_boards.append(updated_board)

    if first_player is None:
        raise ValueError(
            "No board in the provided list has the starting player marker."
        )

    updated_boards = _rotate_turn_order(updated_boards, first_player)
    return ResetBoardsResult(boards=updated_boards, discard=discard)


@dataclass(frozen=True, kw_only=True)
class ResetTilePoolsResult:
    factory_displays: FactoryDisplays
    table_center: UnpickedTableCenter
    bag: TileBag
    discard: TileDiscard


def reset_tile_pools(
    player_count: PositiveInt,
    bag: TileBag,
    discard: TileDiscard,
    selection_strategy: Callable[[Sequence[ColoredTile]], ColoredTile],
) -> ResetTilePoolsResult:
    factory_displays: list[FactoryDisplay] = list()
    for _ in range(player_count + 1):
        pulled_tiles: list[ColoredTile] = []
        while len(pulled_tiles) < 4:
            new_tile, bag = bag.pull(selection_strategy)
            if new_tile is not None:
                pulled_tiles.append(new_tile)
            else:
                bag, discard = reset_tile_bag(bag, discard)

        tiles = tuple(pulled_tiles)
        assert (
            len(tiles) == 4
        ), "Number of tiles in a factory display must be 4."

        factory_displays.append(FactoryDisplay(tiles=tiles))

    updated_factory_displays = FactoryDisplays.new(factory_displays)
    updated_table_center = UnpickedTableCenter.default()

    return ResetTilePoolsResult(
        factory_displays=updated_factory_displays,
        table_center=updated_table_center,
        bag=bag,
        discard=discard,
    )
