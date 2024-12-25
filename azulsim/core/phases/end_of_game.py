"""Defines the end of game phase."""

from azulsim.core.tiles import ColoredTile

from ..board import Wall, PopulatedWallSpace, WallLine, GameScore


def score_bonuses(wall: Wall, current_score: GameScore) -> GameScore:
    """Adds end-of-game bonuses to the given board and returns final score.

    Args:
        board: Board in the current game to which bonuses should be applied.

    Returns:
        Final score for the board, including end-of-game bonuses.
    """
    # Horizontal rows
    horizontal_count = 0
    for line in wall:
        if all(isinstance(space, PopulatedWallSpace) for space in line):
            horizontal_count += 1

    # Vertical rows
    vertical_count = 0
    for space_index in range(WallLine.tile_count()):
        if all(
            isinstance(line[space_index], PopulatedWallSpace) for line in wall
        ):
            vertical_count += 1

    # All of color
    color_counts = {color: 0 for color in ColoredTile}
    for line in wall:
        for space in line:
            if isinstance(space, PopulatedWallSpace):
                color_counts[space.color] += 1
    color_count = sum(count == 5 for count in color_counts.values())

    return (
        current_score
        + horizontal_count * 2
        + vertical_count * 7
        + color_count * 10
    )
