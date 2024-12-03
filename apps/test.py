from azulsim.core import game


def main() -> None:
    state = game.GameState.new(player_count=3, seed=42)
    print(state)


if __name__ == "__main__":
    main()
