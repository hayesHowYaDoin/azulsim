"""Defines the factory offer phase."""

from annotated_types import Ge, Le
from typing import Annotated, Iterable, Optional

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


@dataclass(frozen=True, kw_only=True)
class FactoryOfferSelection:
    """A valid move for a player to take during the factory offer phase."""

    factory_display: FactoryDisplay
    color: ColoredTile


def select_tiles(
    factories: FactoryDisplays,
    table_center: TableCenter,
    tile_pool: PickableTilePool,
    color: ColoredTile,
) -> Optional[tuple[list[Tile], FactoryDisplays, TableCenter]]:
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
            if count == 0:
                return None
            table_center = table_center.pick(color)

    tiles: list[Tile] = [color] * count
    if isinstance(tile_pool, UnpickedTableCenter):
        tiles.append(StartingPlayerMarker())

    return tiles, factories, table_center


def place_tiles(
    board: Board,
    line_index: Annotated[int, Ge(0), Le(PatternLines.line_count())],
    tiles: Iterable[Tile],
) -> Optional[Board]:
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
        board.score_track,
        pattern_lines,
        floor_line,
        board.wall,
    )


def phase_end(
    factory_displays: FactoryDisplays,
    table_center: TableCenter,
) -> bool:
    return factory_displays.empty() and table_center.empty()
