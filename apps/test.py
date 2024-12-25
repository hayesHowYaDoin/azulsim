from typing import Generator

from azulsim.core import (
    Game,
    new_game,
    FactoryOffer,
    RoundSetup,
    WallTiling,
    GameEnd,
)
from azulsim.shell import terminal


def _run_round_setup(game: RoundSetup) -> FactoryOffer | GameEnd:
    print(" ROUND SETUP ".center(40, "═"))

    next_game: Game = game.round_setup()

    print(terminal.format_table_center(next_game.state.table_center))
    for factory in next_game.state.factory_displays:
        print(terminal.format_factory_display(factory))

    return next_game


def _run_factory_offer(game: FactoryOffer) -> WallTiling:
    print(" FACTORY OFFER ".center(40, "═"))

    def board_order() -> Generator[int, None, None]:
        board_index = 0
        while True:
            yield board_index % len(game.state.boards)
            board_index += 1

    board_gen = board_order()

    next_game: Game = game
    while isinstance(next_game, FactoryOffer):
        print(" POOL SELECTION ".center(40, "─"))

        print("Select a tile pool:")
        print(
            f"0:\n{terminal.format_table_center(next_game.state.table_center)}"
        )
        for num, factory in enumerate(next_game.state.factory_displays):
            print(f"\n{num+1}:\n{terminal.format_factory_display(factory)}")

        selected_number = int(input("Selection: "))
        if (
            selected_number < 0
            or len(next_game.state.factory_displays) + 1 < selected_number
        ):
            print("Invalid selection.")
            continue

        if selected_number == 0:
            selected_pool = next_game.state.table_center
        elif selected_number <= len(next_game.state.factory_displays.factories):
            selected_pool = next_game.state.factory_displays.factories[
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
        board = next_game.state.boards[board_index]
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

        maybe_next_game = next_game.factory_offer(
            selected_pool, selected_color, selected_line_index
        )
        if maybe_next_game is None:
            print("Factory offer provided invalid selection.")
            continue
        next_game = maybe_next_game

        print(terminal.format_board(next_game.state.boards[board_index]))

    assert isinstance(next_game, WallTiling)
    return next_game


def _run_wall_tiling(game: WallTiling) -> RoundSetup | GameEnd:
    print(" WALL TILING ".center(40, "═"))

    next_game = game.tile_boards()

    for board in next_game.state.boards:
        print(terminal.format_board(board))

    return next_game


def _run_game_end(game: GameEnd) -> None:
    print(" END OF GAME ".center(40, "="))
    final_state = game.score_bonuses()

    for board in final_state.boards:
        print(terminal.format_board(board))


def main() -> None:
    game = new_game(player_count=1, seed=42)

    while not isinstance(game, GameEnd):
        match game:
            case FactoryOffer():
                game = _run_factory_offer(game)
            case WallTiling():
                game = _run_wall_tiling(game)
            case RoundSetup():
                game = _run_round_setup(game)

    _run_game_end(game)


if __name__ == "__main__":
    main()
