"""Contains unit tests for the azulsim.core.game.wall_tiling module."""

import pytest

from azulsim.core.board import (
    Board,
    GameScore,
    FloorLine,
    PatternLines,
    EmptyPatternLine,
    PopulatedPatternLine,
    Wall,
    wall_tile_sequence,
)
from azulsim.core.game import wall_tiling
from azulsim.core.tiles import ColoredTile, StartingPlayerMarker, TileDiscard


@pytest.mark.parametrize(
    "input_board, expected_board, expected_discard",
    [
        # No tiles in board
        (
            Board.new(
                GameScore.new(0),
                PatternLines.new([EmptyPatternLine()] * 5),
                FloorLine.default(),
                Wall.default(),
            ),
            Board.new(
                GameScore.new(0),
                PatternLines.new([EmptyPatternLine()] * 5),
                FloorLine.default(),
                Wall.default(),
            ),
            TileDiscard.default(),
        ),
        # No tiles in pattern line, tiles in wall
        (
            Board.new(
                GameScore.new(0),
                PatternLines.new([EmptyPatternLine()] * 5),
                FloorLine.new([]),
                Wall.with_populated(
                    (
                        (0, ColoredTile.BLUE),
                        (1, ColoredTile.RED),
                        (2, ColoredTile.WHITE),
                        (3, ColoredTile.YELLOW),
                        (4, ColoredTile.BLACK),
                    )
                ),
            ),
            Board.new(
                GameScore.new(0),
                PatternLines.new([EmptyPatternLine()] * 5),
                FloorLine.default(),
                Wall.with_populated(
                    (
                        (0, ColoredTile.BLUE),
                        (1, ColoredTile.RED),
                        (2, ColoredTile.WHITE),
                        (3, ColoredTile.YELLOW),
                        (4, ColoredTile.BLACK),
                    )
                ),
            ),
            TileDiscard.default(),
        ),
        # No tiles in pattern line, 2 tiles in floor line (with starting player marker), score is 0
        (
            Board.new(
                GameScore.new(0),
                PatternLines.new([EmptyPatternLine()] * 5),
                FloorLine.new([ColoredTile.BLUE, StartingPlayerMarker()]),
                Wall.default(),
            ),
            Board.new(
                GameScore.new(0),
                PatternLines.new([EmptyPatternLine()] * 5),
                FloorLine.default(),
                Wall.default(),
            ),
            TileDiscard.new([ColoredTile.BLUE]),
        ),
        # No tiles in pattern line, 2 tiles in floor line, score > deduction
        (
            Board.new(
                GameScore.new(5),
                PatternLines.new([EmptyPatternLine()] * 5),
                FloorLine.new([ColoredTile.BLUE, ColoredTile.RED]),
                Wall.default(),
            ),
            Board.new(
                GameScore.new(3),
                PatternLines.new([EmptyPatternLine()] * 5),
                FloorLine.default(),
                Wall.default(),
            ),
            TileDiscard.new([ColoredTile.BLUE, ColoredTile.RED]),
        ),
        # No tiles in pattern line, full floor line, score > deduction
        (
            Board.new(
                GameScore.new(14),
                PatternLines.new([EmptyPatternLine()] * 5),
                FloorLine.new([ColoredTile.RED] * 7),
                Wall.default(),
            ),
            Board.new(
                GameScore.new(0),
                PatternLines.new([EmptyPatternLine()] * 5),
                FloorLine.default(),
                Wall.default(),
            ),
            TileDiscard.new([ColoredTile.RED] * 7),
        ),
        # Unfilled pattern lines with unique colors, wall empty, floor empty
        (
            Board.new(
                GameScore.new(20),
                PatternLines.new(
                    [EmptyPatternLine()]
                    + [
                        PopulatedPatternLine.new(count, color)
                        for count, color in zip(range(1, 5), ColoredTile)
                    ]
                ),
                FloorLine.default(),
                Wall.default(),
            ),
            Board.new(
                GameScore.new(20),
                PatternLines.new(
                    [EmptyPatternLine()]
                    + [
                        PopulatedPatternLine.new(count, color)
                        for count, color in zip(range(1, 5), ColoredTile)
                    ]
                ),
                FloorLine.default(),
                Wall.default(),
            ),
            TileDiscard.default(),
        ),
        # Filled pattern lines with same colors, wall empty, floor empty
        (
            Board.new(
                GameScore.new(10),
                PatternLines.new(
                    [
                        PopulatedPatternLine.new(count, ColoredTile.BLUE)
                        for count in range(1, 6)
                    ]
                ),
                FloorLine.default(),
                Wall.default(),
            ),
            Board.new(
                GameScore.new(15),
                PatternLines.default(),
                FloorLine.default(),
                Wall.with_populated(
                    [(index, ColoredTile.BLUE) for index in range(5)]
                ),
            ),
            TileDiscard.new([ColoredTile.BLUE] * sum(range(5))),
        ),
        # Filled pattern lines -> new full vertical run
        (
            Board.new(
                GameScore.new(0),
                PatternLines.new(
                    [
                        PopulatedPatternLine.new(count, color)
                        for count, color in zip(range(1, 6), ColoredTile)
                    ]
                ),
                FloorLine.default(),
                Wall.default(),
            ),
            Board.new(
                GameScore.new(15),
                PatternLines.default(),
                FloorLine.default(),
                Wall.with_populated(
                    [
                        (index, color)
                        for index, color in zip(range(5), ColoredTile)
                    ]
                ),
            ),
            TileDiscard.new([ColoredTile.BLUE] * sum(range(5))),
        ),
        # Filled pattern line -> completes full vertical run
        (
            Board.new(
                GameScore.new(0),
                PatternLines.new(
                    [
                        PopulatedPatternLine.new(count, color)
                        for count, color in zip(range(1, 6), ColoredTile)
                    ]
                ),
                FloorLine.default(),
                Wall.default(),
            ),
            Board.new(
                GameScore.new(15),
                PatternLines.default(),
                FloorLine.default(),
                Wall.with_populated(
                    [
                        (index, color)
                        for index, color in zip(range(5), ColoredTile)
                    ]
                ),
            ),
            TileDiscard.new([ColoredTile.BLUE] * sum(range(5))),
        ),
        # Filled pattern line -> completes full horizontal run
        (
            Board.new(
                GameScore.new(0),
                PatternLines.new(
                    [EmptyPatternLine()] * 4
                    + [PopulatedPatternLine.new(5, ColoredTile.BLUE)]
                ),
                FloorLine.default(),
                Wall.with_populated(
                    (4, color)
                    for color in ColoredTile
                    if color != ColoredTile.BLUE
                ),
            ),
            Board.new(
                GameScore.new(5),
                PatternLines.default(),
                FloorLine.default(),
                Wall.with_populated([(4, color) for color in ColoredTile]),
            ),
            TileDiscard.new([ColoredTile.BLUE] * 4),
        ),
        # Filled pattern line -> completes full horizontal and vertical runs
        (
            Board.new(
                GameScore.new(0),
                PatternLines.new(
                    [EmptyPatternLine()] * 3
                    + [PopulatedPatternLine.new(4, ColoredTile.YELLOW)]
                    + [EmptyPatternLine()]
                ),
                FloorLine.default(),
                Wall.with_populated(
                    [
                        (index, color)
                        for index, color in zip(range(5), ColoredTile)
                        if index != 3
                    ]
                    + [
                        (3, color)
                        for color in ColoredTile
                        if color != ColoredTile.YELLOW
                    ]
                ),
            ),
            Board.new(
                GameScore.new(10),
                PatternLines.default(),
                FloorLine.default(),
                Wall.with_populated(
                    [
                        (index, color)
                        for index, color in zip(range(5), ColoredTile)
                    ]
                    + [(3, color) for color in ColoredTile]
                ),
            ),
            TileDiscard.new([ColoredTile.YELLOW] * 3),
        ),
        # Filled pattern line -> creates incomplete horizontal and vertical runs
        (
            Board.new(
                GameScore.new(0),
                PatternLines.new(
                    [EmptyPatternLine()] * 2
                    + [PopulatedPatternLine.new(3, ColoredTile.WHITE)]
                    + [EmptyPatternLine()] * 2
                ),
                FloorLine.default(),
                Wall.with_populated(
                    [
                        (index, color)
                        for index, color in zip(
                            range(5), wall_tile_sequence(ColoredTile.RED)
                        )
                        if index not in (1, 2, 4)
                    ]
                    + [
                        (2, color)
                        for color in wall_tile_sequence(ColoredTile.RED)
                        if color
                        not in (
                            ColoredTile.RED,
                            ColoredTile.WHITE,
                            ColoredTile.YELLOW,
                        )
                    ]
                ),
            ),
            Board.new(
                GameScore.new(10),
                PatternLines.default(),
                FloorLine.default(),
                Wall.with_populated(
                    [
                        (index, color)
                        for index, color in zip(
                            range(5), wall_tile_sequence(ColoredTile.RED)
                        )
                    ]
                    + [(2, color) for color in wall_tile_sequence(ColoredTile.RED)]
                ),
            ),
            TileDiscard.new([ColoredTile.WHITE] * 2),
        ),
        # Filled pattern line of same color as placed wall space
    ],
)
def test_pattern_lines_board(
    input_board: Board,
    expected_board: Board,
    expected_discard: TileDiscard,
) -> None:
    discard = TileDiscard.default()
    board, discard = wall_tiling.tile_board(input_board, discard)

    assert board.score_track == expected_board.score_track
    assert board.wall == expected_board.wall
    assert board.floor_line == expected_board.floor_line
    for pattern_line, expected_pattern_line in zip(
        board.pattern_lines, expected_board.pattern_lines
    ):
        assert type(pattern_line) == type(expected_pattern_line)
        if isinstance(pattern_line, PopulatedPatternLine):
            assert pattern_line == expected_pattern_line

    assert len(discard.tiles) == len(expected_discard.tiles)
