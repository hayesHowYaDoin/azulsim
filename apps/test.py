from azulsim.core import game


def main() -> None:
    state = game.GameState.new(player_count=3, seed=42)
    print("Select a display:")
    for num, display in enumerate(state.factory_displays):
        print(f"\t{num}: {display}")


if __name__ == "__main__":
    main()
