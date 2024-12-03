# Python Project Template

This project serves to model and simulate the board game [Azul][5], the rulebook for which can be found [here][6]. The 
original intent is for this simulation to be used to train bots to play the 
game, but it could just as easily be used as a standalone game for 1-4 players. 
All dependencies are managed through the [Poetry package manager][1], unit 
tests utilize the [pytest][4] framework, and the static analysis tools 
[ruff][2] and [mypy][3] installed by default.

## Playing the Game

As of now, an interactive GUI has yet to be developed. However, an interactive 
installation script is planned.

## Development

### Prerequisites

The following instructions assume that Docker, VSCode and Git are installed on 
the host computer. The VSCode extension Remote Development 
(ms-vscode-remote.vscode-remote-extensionpack) is required to open the project 
in a Dev Container. 

### Setting Up The Development Environment

1) Clone the repository onto the host computer with the following command:
   ```
    git clone https://github.com/hayesHowYaDoin/physics_backend.git
   ```
2) Open the folder in VSCode. In the Command Palette (Ctrl+Shift+P), execute 
the command "Dev Containers: Open Folder In Container..."

And... that's it!

### Commands

- ```make install```: Installs package dependencies.
- ```make analyze```: Runs static analysis.
- ```make test```: Runs unit tests.
- ```make run```: Executes the script.

[1]: https://python-poetry.org/
[2]: https://docs.astral.sh/ruff/
[3]: https://mypy-lang.org/
[4]: https://docs.pytest.org/en/7.4.x/
[5]: https://boardgamegeek.com/boardgame/230802/azul
[6]: https://cdn.1j1ju.com/medias/03/14/fd-azul-rulebook.pdf
