from azulsim.core import game


def main() -> None:
    state = game.GameState.new(player_count=3, seed=42)

    while len(state.factory_displays) != 0:
        print("Select a factory display:")
        factories = state.factory_displays.factories
        for num, display in enumerate(factories):
            print(f"\t{num}: {display}")

        selected_number = int(input("Selection: "))
        if 0 <= selected_number < len(state.factory_displays):
            print(f"You selected: {factories[selected_number]}")
        else:
            print("Invalid display number.")
        selected_display = factories[selected_number]

        print("Select tile color:")
        unique_colors = list(set(selected_display.tiles))
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
            selected_display,
            selected_color,
        )
        if result is not None:
            state = game.GameState(
                boards=state.boards,
                factory_displays=result[0],
                table_center=result[1],
                bag=state.bag,
                discard=state.discard,
            )


if __name__ == "__main__":
    main()
