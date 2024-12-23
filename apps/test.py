from typing import Generator

from azulsim.core import Game, new_game, FactoryOffer, RoundSetup, WallTiling
from azulsim.shell import terminal


def _run_round_setup(game: Game) -> FactoryOffer:
    assert isinstance(game, RoundSetup)

    print(" ROUND SETUP ".center(40, "═"))

    game = game.round_setup()

    print(terminal.format_table_center(game.state.table_center))
    for factory in game.state.factory_displays:
        print(terminal.format_factory_display(factory))

    return game


def _run_factory_offer(game: Game) -> WallTiling:
    print(" FACTORY OFFER ".center(40, "═"))

    def board_order() -> Generator[int, None, None]:
        board_index = 0
        while True:
            yield board_index % len(game.state.boards)
            board_index += 1

    board_gen = board_order()

    while isinstance(game, FactoryOffer):
        print(" POOL SELECTION ".center(40, "─"))

        print("Select a tile pool:")
        print(f"0:\n{terminal.format_table_center(game.state.table_center)}")
        for num, factory in enumerate(game.state.factory_displays):
            print(f"\n{num+1}:\n{terminal.format_factory_display(factory)}")

        selected_number = int(input("Selection: "))
        if (
            selected_number < 0
            or len(game.state.factory_displays) + 1 < selected_number
        ):
            print("Invalid selection.")
            continue

        if selected_number == 0:
            selected_pool = game.state.table_center
        elif selected_number <= len(game.state.factory_displays.factories):
            selected_pool = game.state.factory_displays.factories[
                selected_number - 1
            ]
        else:
            print("Invalid selection.")
            continue

        print(" TILE SELECTION ".center(40, "─"))

        print("Select tile color:")
        unique_colors = list(set(selected_pool.tiles))
        for num, tile_color in enumerate(unique_colors):
            print(f"\t{num}: {terminal.format_tile(tile_color)}")

        selected_number = int(input("Selection: "))
        if selected_number < 0 or len(unique_colors) <= selected_number:
            print("Invalid display number.")
            continue

        selected_color = unique_colors[selected_number]

        print(" PATTERN LINE SELECTION ".center(40, "─"))

        print("Select pattern line:")
        board_index: int = next(board_gen)
        board = game.state.boards[board_index]
        pattern_line_strs = terminal.format_pattern_lines(
            board.pattern_lines
        ).split("\n")
        for num, line in enumerate(pattern_line_strs):
            print(f"{num}: {line}")

        selected_line_index = int(input("Selection: "))
        if (
            selected_line_index < 0
            or len(board.pattern_lines.lines) + 1 < selected_line_index
        ):
            print("Invalid selection.")
            continue

        next_game = game.factory_offer(
            selected_pool, selected_color, selected_line_index
        )
        if next_game is None:
            print("Factory offer provided invalid selection.")
            continue
        game = next_game

        print(terminal.format_board(board))

    assert isinstance(game, WallTiling)
    return game


def _run_wall_tiling(game: Game) -> RoundSetup:
    assert isinstance(game, WallTiling)

    print(" WALL TILING ".center(40, "═"))
    game = game.tile_boards()

    for board in game.state.boards:
        print(terminal.format_board(board))

    return game


def main() -> None:
    game = new_game(player_count=1, seed=42)

    # TODO: Include end condition for game loop
    while True:
        game = _run_factory_offer(game)
        game = _run_wall_tiling(game)
        game = _run_round_setup(game)


if __name__ == "__main__":
    main()
