"""Defines the factory offer phase."""

from annotated_types import Ge, Le
from typing import Annotated, Iterable, Optional

from pydantic import ConfigDict
from pydantic.dataclasses import dataclass

from ..board import Board, PatternLines
from ..factory import (
    FactoryDisplay,
    FactoryDisplays,
    PickedTableCenter,
    UnpickedTableCenter,
    TableCenter,
    PickableTilePool,
)
from ..tiles import ColoredTile, StartingPlayerMarker, Tile


@dataclass(
    frozen=True,
    kw_only=True,
    config=ConfigDict(arbitrary_types_allowed=True),
)
class SelectTilesResult:
    """Result aggregate from the select_tiles method.

    Attributes:
        tiles: Tiles selected from the factory display
        factory_displays: Updated factory displays.
        table_center: Updated table center.
    """

    tiles: tuple[Tile, ...]
    factory_displays: FactoryDisplays
    table_center: TableCenter


def select_tiles(
    factories: FactoryDisplays,
    table_center: TableCenter,
    tile_pool: PickableTilePool,
    color: ColoredTile,
) -> Optional[SelectTilesResult]:
    """Select all tiles of a color from a tile pool, updating the game state to
    reflect these tiles being taken.

    Args:
        factories: Collection of factory displays in the current game.
        table_center: Tile pool in the center of the table.
        tile_pool: Selected tile pool from which to draw tiles from.
        color: Tile color selected from the selected tile pool.

    Returns:
        Aggregation of selected tiles and updated state objects or None if
        selection is not possible.
    """
    count = tile_pool.count(color)
    match tile_pool:
        case FactoryDisplay():
            if tile_pool not in factories or count == 0:
                return None
            table_center = table_center.add(
                tuple(tile for tile in tile_pool.tiles if tile != color)
            )
            factories = factories.remove(tile_pool)
        case PickedTableCenter() | UnpickedTableCenter():
            if tile_pool != table_center or count == 0:
                return None
            table_center = table_center.pick(color)

    tiles: list[Tile] = [color] * count
    if isinstance(tile_pool, UnpickedTableCenter):
        tiles.append(StartingPlayerMarker())

    return SelectTilesResult(
        tiles=tuple(tiles),
        factory_displays=factories,
        table_center=table_center,
    )


def place_tiles(
    board: Board,
    line_index: Annotated[int, Ge(0), Le(PatternLines.line_count())],
    tiles: Iterable[Tile],
) -> Optional[Board]:
    """Place a collection of tiles in the pattern line section of the board
    at a given line index. Pattern line must be either empty or have tiles of
    the same color as the new tiles. Any tiles that cannot be placed on the
    pattern line are moved to the floor line and will count as a deduction for
    end-of-round scoring.

    Args:
        board: Board owning the destination pattern line.
        line_index: Zero-based index of the pattern line. Must be in range
            [0, # pattern lines]
        tiles: Tiles to place. All colored tiles must be the same color.

    Returns:
        Updated board with tiles placed in pattern line or None if move is
        impossible.
    """
    colored_tiles = [tile for tile in tiles if isinstance(tile, ColoredTile)]
    if len(colored_tiles) == 0:
        return None

    color = colored_tiles[0]
    if not all(tile == color for tile in colored_tiles):
        return None

    result = board.pattern_lines.try_add(line_index, len(colored_tiles), color)
    if result is None:
        return None
    pattern_lines, remainder = result

    new_tiles: list[Tile] = [color] * remainder
    if any((isinstance(tile, StartingPlayerMarker) for tile in tiles)):
        new_tiles.append(StartingPlayerMarker())

    floor_line = board.floor_line.add(new_tiles)

    return Board.new(
        board.uid,
        board.score_track,
        pattern_lines,
        floor_line,
        board.wall,
    )


def phase_end(
    factory_displays: FactoryDisplays,
    table_center: TableCenter,
) -> bool:
    """Returns boolean indicating if factory offer phase has ended."""
    return (
        factory_displays.empty()
        and isinstance(table_center, PickedTableCenter)
        and table_center.empty()
    )
