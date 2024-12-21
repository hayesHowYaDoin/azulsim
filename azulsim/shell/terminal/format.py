"""Module containing functions for representing core types in the terminal."""

from typing import Optional

from termcolor import colored

from azulsim.core.board import (
    Board,
    PatternLines,
    PopulatedPatternLine,
    EmptyPatternLine,
    FloorLine,
    Wall,
    EmptyWallSpace,
    PopulatedWallSpace,
)
from azulsim.core.tiles import ColoredTile, StartingPlayerMarker, Tile


def format_tile(tile: Optional[Tile]) -> str:
    """Returns a 'pretty' representation of a tile for terminal output."""
    match tile:
        case ColoredTile():
            colors = {
                ColoredTile.BLACK: "black",
                ColoredTile.WHITE: "white",
                ColoredTile.BLUE: "blue",
                ColoredTile.YELLOW: "yellow",
                ColoredTile.RED: "red",
            }
            return colored("█", colors[tile])  # type: ignore
        case StartingPlayerMarker():
            return colored("§", "blue")
        case None:
            return "░"


def format_pattern_lines(pattern_lines: PatternLines) -> str:
    """Returns a 'pretty' representation of the pattern lines section of a board for terminal output."""
    lines_str: list[str] = []
    for i, line in enumerate(pattern_lines):
        max_tiles = i + 1
        pad_width = 9
        match line:
            case PopulatedPatternLine():
                line_str = (
                    "_ " * (max_tiles - line.tile_count)
                    + f"{format_tile(line.color)} " * line.tile_count
                )
                # Adjust pad width to adjust for extra characters added by termcolor
                pad_width = 9 - max_tiles * 2 + len(line_str)
            case EmptyPatternLine():
                line_str = "_ " * max_tiles

        lines_str.append(line_str.rstrip().rjust(pad_width, " "))

    return "\n".join(lines_str)


def format_wall(wall: Wall) -> str:
    wall_str: list[str] = []
    for line in wall:
        line_str = ""
        for tile in line.tiles:
            match tile:
                case EmptyWallSpace():
                    line_str = line_str + "░ "
                case PopulatedWallSpace():
                    line_str = line_str + "█ "
        wall_str.append(line_str.rstrip())

    return "\n".join(wall_str)


def format_floor_line(floor_line: FloorLine) -> str:
    spaces: list[str] = []
    for tile_index in range(FloorLine.spaces_count()):
        if tile_index < len(floor_line.tiles):
            spaces.append(f" {format_tile(floor_line.tiles[tile_index])}")
        else:
            spaces.append(f" {format_tile(None)}")

    spaces_str = " ".join(spaces)
    number_str = "-1 -1 -2 -2 -2 -3 -3"

    return "\n".join([spaces_str, number_str])


def format_board(board: Board) -> str:
    """Returns a 'pretty' representation of a board for terminal output."""
    score_str = "".join(
        [f"| Score: {board.score_track.score}".ljust(24, " "), "|\n"]
    )

    pattern_lines_strs = format_pattern_lines(board.pattern_lines).split("\n")
    wall_strs = format_wall(board.wall).split("\n")
    pattern_wall_lines: list[str] = []
    for pattern_line, wall_line in zip(pattern_lines_strs, wall_strs):
        pattern_wall_lines.append(f"| {pattern_line}   {wall_line} |")
    pattern_wall_str = "\n".join(pattern_wall_lines) + "\n"

    floor_line_strs = format_floor_line(board.floor_line).split("\n")
    floor_line_lines: list[str] = []
    for floor_line_str in floor_line_strs:
        floor_line_lines.append(f"| {floor_line_str}  |")
    floor_line_str = "\n".join(floor_line_lines) + "\n"

    return (
        " _ _ _ _ _ _ _ _ _ _ _ _\n"
        + score_str
        + "|                       |\n"
        + pattern_wall_str
        + "|                       |\n"
        + floor_line_str
        + "|_ _ _ _ _ _ _ _ _ _ _ _|"
    )


#  _ _ _ _ _ _ _ _ _ _ _ _ _
# | Score:                  |
# |                         |
# |         _    ░ ░ ░ ░ █  |
# |       _ _    ░ ░ ░ ░ ░  |
# |     _ _ █ B  ░ ░ █ ░ ░  |
# |   _ █ █ █ Y  ░ ░ █ ░ ░  |
# | _ _ _ _ _    ░ ░ ░ ░ ░  |
# |                         |
# |   ░  ░  ░  ░  ░  ░  ░   |
# |  -1 -1 -2 -2 -2 -3 -3   |
# |_ _ _ _ _ _ _ _ _ _ _ _ _|
