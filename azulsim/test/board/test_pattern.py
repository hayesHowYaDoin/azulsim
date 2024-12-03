"""Contains unit tests for the azulsim.core.board.pattern module."""

import pytest
from pydantic import ValidationError

from azulsim.core.board.pattern import (
    EmptyPatternLine,
    PopulatedPatternLine,
    PatternLine,
    PatternLines,
)
from azulsim.core.tiles import ColoredTile


def test_empty_pattern_line():
    line = EmptyPatternLine()
    assert isinstance(line, EmptyPatternLine)


def test_populated_pattern_line():
    line = PopulatedPatternLine.new(tile_count=3, color=ColoredTile.BLUE)
    assert line.tile_count == 3
    assert line.color == ColoredTile.BLUE


def test_pattern_lines_default():
    pattern_lines = PatternLines.default()
    assert len(pattern_lines.lines) == 5
    assert all(
        isinstance(line, EmptyPatternLine) for line in pattern_lines.lines
    )


def test_pattern_lines_new_valid():
    lines = (
        PopulatedPatternLine.new(tile_count=1, color=ColoredTile.BLUE),
        EmptyPatternLine(),
        EmptyPatternLine(),
        EmptyPatternLine(),
        EmptyPatternLine(),
    )
    pattern_lines = PatternLines.new(lines=lines)

    assert isinstance(pattern_lines.lines[0], PopulatedPatternLine)
    assert pattern_lines.lines[0].tile_count == 1
    assert pattern_lines.lines[0].color == ColoredTile.BLUE

    assert isinstance(pattern_lines.lines[1], EmptyPatternLine)
    assert isinstance(pattern_lines.lines[1], EmptyPatternLine)
    assert isinstance(pattern_lines.lines[1], EmptyPatternLine)
    assert isinstance(pattern_lines.lines[1], EmptyPatternLine)


_INVALID_LINES = (
    (
        PopulatedPatternLine.new(tile_count=2, color=ColoredTile.BLUE),
        EmptyPatternLine(),
        EmptyPatternLine(),
        EmptyPatternLine(),
        EmptyPatternLine(),
    ),
    (
        EmptyPatternLine(),
        PopulatedPatternLine.new(tile_count=3, color=ColoredTile.WHITE),
        EmptyPatternLine(),
        EmptyPatternLine(),
        EmptyPatternLine(),
    ),
    (
        EmptyPatternLine(),
        EmptyPatternLine(),
        PopulatedPatternLine.new(tile_count=4, color=ColoredTile.RED),
        EmptyPatternLine(),
        EmptyPatternLine(),
    ),
    (
        EmptyPatternLine(),
        EmptyPatternLine(),
        EmptyPatternLine(),
        PopulatedPatternLine.new(tile_count=5, color=ColoredTile.BLACK),
        EmptyPatternLine(),
    ),
    (
        EmptyPatternLine(),
        EmptyPatternLine(),
        EmptyPatternLine(),
        EmptyPatternLine(),
        PopulatedPatternLine.new(tile_count=6, color=ColoredTile.YELLOW),
    ),
)


@pytest.mark.parametrize("invalid_lines", _INVALID_LINES)
def test_pattern_lines_new_invalid(
    invalid_lines: tuple[
        PatternLine, PatternLine, PatternLine, PatternLine, PatternLine
    ],
) -> None:
    with pytest.raises(ValidationError):
        PatternLines.new(lines=invalid_lines)
