from collections import deque

from azulsim.core import game
from azulsim.shell import terminal


def factory_offer(state: game.GameState) -> game.GameState:
    while not game.factory_offer.phase_end(
        state.factory_displays, state.table_center
    ):
        print(" POOL SELECTION ".center(40, "─"))

        factories = state.factory_displays.factories
        table_center = state.table_center
        print("Select a tile pool:")
        print(f"0:\n{terminal.format_table_center(table_center)}")
        for num, factory in enumerate(factories):
            print(f"\n{num+1}:\n{terminal.format_factory_display(factory)}")

        selected_number = int(input("Selection: "))
        if (
            selected_number < 0
            or len(state.factory_displays) + 1 < selected_number
        ):
            print("Invalid selection.")
            continue

        if selected_number == 0:
            selected_pool = table_center
        else:
            selected_pool = factories[selected_number - 1]

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

        result = game.factory_offer.select_tiles(
            state.factory_displays,
            state.table_center,
            selected_pool,
            selected_color,
        )
        if result is None:
            print("Invalid selection.")
            continue

        tiles, factories, table_center = result

        print(" PATTERN LINE SELECTION ".center(40, "─"))

        print("Select pattern line:")
        board = state.boards[0]
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

        board = game.factory_offer.place_tiles(
            board,
            selected_line_index,
            tiles,
        )
        if board is None:
            print("Weird error encountered...")
            continue

        print(terminal.format_board(board))

        state = game.GameState(
            boards=deque([board]),
            factory_displays=factories,
            table_center=table_center,
            bag=state.bag,
            discard=state.discard,
        )

    return state


def main() -> None:
    state = game.GameState.new(player_count=1, seed=42)

    print(" ROUND SETUP ".center(40, "═"))
    print(terminal.format_board(state.boards[0]))

    print(" FACTORY OFFER ".center(40, "═"))
    state = factory_offer(state)

    print(" WALL TILING ".center(40, "═"))
    boards = game.wall_tiling.wall_tiling(state.boards)
    print(terminal.format_board(boards[0]))


if __name__ == "__main__":
    main()
