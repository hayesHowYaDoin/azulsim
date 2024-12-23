"""Contains unit tests for the azulsim.core.game.factory_offer module's place_tiles function."""

from pydantic.types import NonNegativeInt, PositiveInt

from azulsim.core.game import factory_offer
from azulsim.core.board import (
    Board,
    GameScore,
    PatternLine,
    PatternLines,
    FloorLine,
    EmptyPatternLine,
    PopulatedPatternLine,
    Wall,
)
from azulsim.core.tiles import ColoredTile


def _build_populated_board(
    index: NonNegativeInt, color: ColoredTile, count: PositiveInt
) -> Board:
    raw_pattern_lines: list[PatternLine] = []
    for line_index in range(5):
        if line_index == index:
            raw_pattern_lines.append(PopulatedPatternLine.new(count, color))
        else:
            raw_pattern_lines.append(EmptyPatternLine())

    pattern_lines = PatternLines.new(raw_pattern_lines)
    return Board.new(
        GameScore.new(0),
        pattern_lines,
        FloorLine.default(),
        Wall.default(),
    )


def test_no_tiles() -> None:
    """Tests that output is None when placing no tiles."""
    board = Board.default()
    result = factory_offer.place_tiles(board, 0, [])
    assert result is None


def test_tiles_color_mismatch() -> None:
    """Tests that output is None when placed tiles collection is not all the same color."""
    board = Board.default()
    tiles = [ColoredTile.BLACK, ColoredTile.BLUE]
    result = factory_offer.place_tiles(board, 0, tiles)
    assert result is None


def test_unpopulated_pattern_line_underfilled() -> None:
    """Tests that output is valid when placing tiles in an unpopulated pattern line leaves spaces unfilled."""
    board = Board.default()
    tiles = [ColoredTile.BLACK] * 2
    result = factory_offer.place_tiles(board, 2, tiles)

    assert result is not None

    assert result.score_track == board.score_track
    assert result.floor_line == FloorLine.default()
    assert result.wall == Wall.default()

    placed_line = result.pattern_lines[2]
    assert isinstance(placed_line, PopulatedPatternLine)
    assert placed_line.color == ColoredTile.BLACK
    assert placed_line.tile_count == 2
    for line_index in (0, 1, 3, 4):
        assert isinstance(result.pattern_lines[line_index], EmptyPatternLine)


def test_unpopulated_pattern_line_filled() -> None:
    """Tests that output is valid when placing tiles in an unpopulated pattern line leaves no unfilled spaces."""
    board = Board.default()
    tiles = [ColoredTile.BLACK] * 3
    result = factory_offer.place_tiles(board, 2, tiles)

    assert result is not None

    assert result.score_track == board.score_track
    assert result.floor_line == FloorLine.default()
    assert result.wall == Wall.default()

    placed_line = result.pattern_lines[2]
    assert isinstance(placed_line, PopulatedPatternLine)
    assert placed_line.color == ColoredTile.BLACK
    assert placed_line.tile_count == 3
    for line_index in (0, 1, 3, 4):
        assert isinstance(result.pattern_lines[line_index], EmptyPatternLine)


def test_unpopulated_pattern_line_overflow() -> None:
    """Tests that output is valid when placing tiles in an unpopulated pattern line overflows into the floor line."""
    board = Board.default()
    tiles = [ColoredTile.BLACK] * 4
    result = factory_offer.place_tiles(board, 2, tiles)

    assert result is not None

    assert result.score_track == board.score_track
    assert result.wall == Wall.default()

    placed_line = result.pattern_lines[2]
    assert isinstance(placed_line, PopulatedPatternLine)
    assert placed_line.color == ColoredTile.BLACK
    assert placed_line.tile_count == 3
    for line_index in (0, 1, 3, 4):
        assert isinstance(result.pattern_lines[line_index], EmptyPatternLine)

    assert result.floor_line.tiles == (ColoredTile.BLACK,)


def test_populated_pattern_line_color_mismatch() -> None:
    """Tests that output is None when placing tiles in a populated pattern of a different color."""
    board = _build_populated_board(2, ColoredTile.RED, 1)
    tiles = [ColoredTile.BLACK] * 2
    result = factory_offer.place_tiles(board, 2, tiles)

    assert result is None


def test_populated_pattern_line_underfilled() -> None:
    """Tests that output is valid when placing tiles in a populated pattern line leaves spaces unfilled."""
    board = _build_populated_board(2, ColoredTile.BLACK, 1)
    tiles = [ColoredTile.BLACK] * 1
    result = factory_offer.place_tiles(board, 2, tiles)

    assert result is not None

    assert result.score_track == board.score_track
    assert result.floor_line == FloorLine.default()
    assert result.wall == Wall.default()

    placed_line = result.pattern_lines[2]
    assert isinstance(placed_line, PopulatedPatternLine)
    assert placed_line.color == ColoredTile.BLACK
    assert placed_line.tile_count == 2
    for line_index in (0, 1, 3, 4):
        assert isinstance(result.pattern_lines[line_index], EmptyPatternLine)


def test_populated_pattern_line_filled() -> None:
    """Tests that output is valid when placing tiles in a populated pattern line leaves no unfilled spaces."""
    board = _build_populated_board(2, ColoredTile.BLACK, 1)
    tiles = [ColoredTile.BLACK] * 2
    result = factory_offer.place_tiles(board, 2, tiles)

    assert result is not None

    assert result.score_track == board.score_track
    assert result.floor_line == FloorLine.default()
    assert result.wall == Wall.default()

    placed_line = result.pattern_lines[2]
    assert isinstance(placed_line, PopulatedPatternLine)
    assert placed_line.color == ColoredTile.BLACK
    assert placed_line.tile_count == 3
    for line_index in (0, 1, 3, 4):
        assert isinstance(result.pattern_lines[line_index], EmptyPatternLine)


def test_populated_pattern_line_overflow() -> None:
    """Tests that output is valid when placing tiles in a populated pattern line overflows into the floor line."""
    board = _build_populated_board(2, ColoredTile.BLACK, 1)
    tiles = [ColoredTile.BLACK] * 3
    result = factory_offer.place_tiles(board, 2, tiles)

    assert result is not None

    assert result.score_track == board.score_track
    assert result.wall == Wall.default()

    placed_line = result.pattern_lines[2]
    assert isinstance(placed_line, PopulatedPatternLine)
    assert placed_line.color == ColoredTile.BLACK
    assert placed_line.tile_count == 3
    for line_index in (0, 1, 3, 4):
        assert isinstance(result.pattern_lines[line_index], EmptyPatternLine)

    assert result.floor_line.tiles == (ColoredTile.BLACK,)
