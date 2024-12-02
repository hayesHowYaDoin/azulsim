from azulsim.core import game


def main() -> None:
    state = game.GameState.default()
    print(state)


if __name__ == "__main__":
    main()
