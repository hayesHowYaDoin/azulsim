from azulsim.core import game


def main() -> None:
    state = game.GameState.new(3)
    print(state)


if __name__ == "__main__":
    main()
