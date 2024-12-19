from azulsim.core import game


def main() -> None:
    state = game.GameState.new(player_count=3, seed=42)

    while not game.factory_offer.phase_end(
        state.factory_displays, state.table_center
    ):
        factories = state.factory_displays.factories
        table_center = state.table_center
        print("Select a tile pool:")
        print(f"\t0: {table_center}")
        for num, factory in enumerate(factories):
            print(f"\t{num+1}: {factory}")

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
        print(f"You selected: {table_center}")

        print("Select tile color:")
        unique_colors = list(set(selected_pool.tiles))
        for num, tile_color in enumerate(unique_colors):
            print(f"\t{num}: {tile_color}")

        selected_number = int(input("Selection: "))
        if 0 <= selected_number < len(unique_colors):
            print(f"You selected: {unique_colors[selected_number]}")
        else:
            print("Invalid display number.")
        selected_color = unique_colors[selected_number]

        result = game.factory_offer.select_tiles(
            state.factory_displays,
            state.table_center,
            selected_pool,
            selected_color,
        )
        if result is not None:
            state = game.GameState(
                boards=state.boards,
                factory_displays=result[1],
                table_center=result[2],
                bag=state.bag,
                discard=state.discard,
            )


if __name__ == "__main__":
    main()
