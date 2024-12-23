from collections import deque
import random

from azulsim.core import phases
from azulsim.shell import terminal


def _run_round_setup(state: phases.Game) -> phases.Game:
    print(" ROUND SETUP ".center(40, "═"))
    boards = state.boards
    factory_displays = state.factory_displays
    table_center = state.table_center
    bag = state.bag
    discard = state.discard

    tile_pools_result = phases.round_setup.reset_tile_pools(
        len(boards),
        bag,
        discard,
        lambda x: random.sample(x, 1)[0],
    )
    factory_displays = tile_pools_result.factory_displays
    table_center = tile_pools_result.table_center
    bag = tile_pools_result.bag
    discard = tile_pools_result.discard

    print(terminal.format_table_center(table_center))
    for factory in factory_displays:
        print(terminal.format_factory_display(factory))

    return phases.Game(
        boards=boards,
        factory_displays=factory_displays,
        table_center=table_center,
        bag=bag,
        discard=discard,
    )


def _run_factory_offer(state: phases.Game) -> phases.Game:
    print(" FACTORY OFFER ".center(40, "═"))

    while not phases.factory_offer.phase_end(
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

        result = phases.factory_offer.select_tiles(
            state.factory_displays,
            state.table_center,
            selected_pool,
            selected_color,
        )
        if result is None:
            print("Invalid selection.")
            continue

        tiles = result.tiles
        factories = result.factory_displays
        table_center = result.table_center

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

        board = phases.factory_offer.place_tiles(
            board,
            selected_line_index,
            tiles,
        )
        if board is None:
            print("Weird error encountered...")
            continue

        print(terminal.format_board(board))

        state = phases.Game(
            boards=deque([board]),
            factory_displays=factories,
            table_center=table_center,
            bag=state.bag,
            discard=state.discard,
        )

    return state


def _run_wall_tiling(state: phases.Game) -> phases.Game:
    print(" WALL TILING ".center(40, "═"))
    boards, discard = phases.wall_tiling.tile_boards(
        state.boards, state.discard
    )

    for board in boards:
        print(terminal.format_board(board))

    return phases.Game(
        boards=boards,
        factory_displays=state.factory_displays,
        table_center=state.table_center,
        bag=state.bag,
        discard=discard,
    )


def main() -> None:
    state = phases.Game.new(player_count=1, seed=42)

    # TODO: Include end condition for game loop
    while True:
        state = _run_factory_offer(state)
        state = _run_wall_tiling(state)
        state = _run_round_setup(state)


if __name__ == "__main__":
    main()
