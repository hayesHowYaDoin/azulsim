"""Module containing functions for representing core types in the terminal."""

from annotated_types import Ge, Le
from typing import Annotated, Optional

from pydantic.types import PositiveInt
from termcolor import colored

from azulsim.core.board import (
    Board,
    PatternLine,
    PatternLines,
    PopulatedPatternLine,
    EmptyPatternLine,
    FloorLine,
    Wall,
    WallLine,
    WallSpace,
    EmptyWallSpace,
    PopulatedWallSpace,
)
from azulsim.core.tiles import ColoredTile, StartingPlayerMarker, Tile
from azulsim.core.factory import (
    FactoryDisplay,
    TableCenter,
    UnpickedTableCenter,
)


_TILE_COLORS = {
    ColoredTile.BLACK: "black",
    ColoredTile.WHITE: "white",
    ColoredTile.BLUE: "blue",
    ColoredTile.YELLOW: "yellow",
    ColoredTile.RED: "red",
}


def format_tile(tile: Tile) -> str:
    """Returns a 'pretty' representation of a tile for terminal output."""
    match tile:
        case ColoredTile():
            return colored("█", _TILE_COLORS[tile])  # type: ignore
        case StartingPlayerMarker():
            return colored("§", "blue")


def _format_pattern_line(line: PatternLine, max_tiles: PositiveInt) -> str:
    """Returns a 'pretty' representation of a pattern line for terminal output."""
    match line:
        case PopulatedPatternLine():
            line_str = (
                "_ " * (max_tiles - line.tile_count)
                + f"{format_tile(line.color)} " * line.tile_count
            )
        case EmptyPatternLine():
            line_str = "_ " * max_tiles

    return line_str


def format_pattern_lines(lines: PatternLines) -> str:
    """Returns a 'pretty' representation of the pattern lines section of a board for terminal output."""
    lines_str: list[str] = []
    for i, line in enumerate(lines):
        max_tiles = i + 1
        line_str = _format_pattern_line(line, max_tiles)

        # Adjust pad width to adjust for extra characters added by termcolor
        pad_width = 9 - max_tiles * 2 + len(line_str)
        lines_str.append(line_str.rstrip().rjust(pad_width, " "))

    return "\n".join(lines_str)


def _format_wall_space(space: WallSpace) -> str:
    match space:
        case EmptyWallSpace():
            # TODO: Change this back to something functional
            space_str = colored("░", _TILE_COLORS[space.color])  # type: ignore
        case PopulatedWallSpace():
            space_str = colored("█", _TILE_COLORS[space.color])  # type: ignore

    return space_str


def _format_wall_line(line: WallLine) -> str:
    line_str = ""
    for tile in line.tiles:
        line_str = line_str + f"{_format_wall_space(tile)} "

    return line_str


def format_wall(wall: Wall) -> str:
    """Returns a 'pretty' representation of the wall section of a board for terminal output."""
    wall_str: list[str] = []
    for line in wall:
        wall_str.append(_format_wall_line(line).rstrip())

    return "\n".join(wall_str)


def format_floor_line(floor_line: FloorLine) -> str:
    """Returns a 'pretty' representation of the floor line section of a board for terminal output."""
    spaces: list[str] = []
    for tile_index in range(FloorLine.spaces_count()):
        if tile_index < len(floor_line.tiles):
            spaces.append(f" {format_tile(floor_line.tiles[tile_index])}")
        else:
            spaces.append(" ░")

    spaces_str = " ".join(spaces)
    number_str = "-1 -1 -2 -2 -2 -3 -3"

    return "\n".join([spaces_str, number_str])


def format_board(board: Board) -> str:
    """Returns a 'pretty' representation of a board for terminal output."""
    score_str = "".join(
        [f"│ Score: {board.score_track.score}".ljust(24, " "), "│\n"]
    )

    pattern_lines_strs = format_pattern_lines(board.pattern_lines).split("\n")
    wall_strs = format_wall(board.wall).split("\n")
    pattern_wall_lines: list[str] = []
    for pattern_line, wall_line in zip(pattern_lines_strs, wall_strs):
        pattern_wall_lines.append(f"│ {pattern_line}   {wall_line} │")
    pattern_wall_str = "\n".join(pattern_wall_lines) + "\n"

    floor_line_strs = format_floor_line(board.floor_line).split("\n")
    floor_line_lines: list[str] = []
    for floor_line_str in floor_line_strs:
        floor_line_lines.append(f"│ {floor_line_str}  │")
    floor_line_str = "\n".join(floor_line_lines) + "\n"

    return (
        "┌───────────────────────┐\n"
        + score_str
        + "│                       │\n"
        + pattern_wall_str
        + "│                       │\n"
        + floor_line_str
        + "└───────────────────────┘"
    )


def format_factory_display(
    factory: FactoryDisplay,
    number: Optional[Annotated[int, Ge(0), Le(9)]] = None,
) -> str:
    center_symbol = number if number else "x"
    return (
        "      ─┬─     \n"
        + "   ────·────  \n"
        + f"  ───{format_tile(factory.tiles[0])}─┼─{format_tile(factory.tiles[1])}───\n"
        + f"├──·───{center_symbol}───·──┤\n"
        + f"  ───{format_tile(factory.tiles[2])}─┼─{format_tile(factory.tiles[3])}───\n"
        + "   ────·────  \n"
        + "      ─┴─    "
    )


def format_table_center(center: TableCenter) -> str:
    lines: list[str] = []

    starting_player_marker_count = 0
    if isinstance(center, UnpickedTableCenter):
        starting_player_marker_count = 1
    lines.append(
        f"{format_tile(StartingPlayerMarker())} x {starting_player_marker_count}"
    )

    for color in ColoredTile:
        lines.append(f"{format_tile(color)} x {center.tiles.count(color)}")

    return "\n".join(lines)
