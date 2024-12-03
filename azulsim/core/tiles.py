"""Defines representations of game tiles."""

from __future__ import annotations
from enum import auto, Enum
import random
from typing import Iterable, Optional, TypeAlias

from pydantic.dataclasses import dataclass


class ColoredTile(Enum):
    """A single colored tile."""

    BLACK = auto()
    WHITE = auto()
    BLUE = auto()
    YELLOW = auto()
    RED = auto()


class StartingPlayerMarker:
    """The starting player marker which is used to determine the player that starts a round."""

    pass


"""A single game tile."""
Tile: TypeAlias = ColoredTile | StartingPlayerMarker


_ALL_COLORED_TILES = (
    (ColoredTile.BLACK,) * 20
    + (ColoredTile.WHITE,) * 20
    + (ColoredTile.BLUE,) * 20
    + (ColoredTile.YELLOW,) * 20
    + (ColoredTile.RED,) * 20
)


@dataclass(frozen=True)
class TileBag:
    """The tile bag from which colored tiles are drawn to fill the factory displays at the start of a round."""

    tiles: tuple[ColoredTile, ...]

    @staticmethod
    def default() -> TileBag:
        """Returns a tile bag in its default state with all colored tiles in the game."""
        return TileBag(tiles=_ALL_COLORED_TILES)

    @staticmethod
    def new(tiles: Iterable[ColoredTile]) -> TileBag:
        """Returns a tile bag containing the privided tiles."""
        return TileBag(tiles=tuple(tiles))

    def add(self, tiles: tuple[ColoredTile, ...]) -> TileBag:
        """Returns a discarded tile collection with the argument tiles appended."""
        return TileBag(tiles=self.tiles + tiles)

    def pull_random(self, seed: int) -> tuple[Optional[ColoredTile], TileBag]:
        """Returns a randomly selected tile from the tile bag with the modified tile bag.

        Args:
            seed: A seed for the random number generator.

        Returns:
            A randomly selected tile (if one exists) and the tile bag with the selected tile removed.
        """

        if len(self.tiles) == 0:
            return None, self

        random.seed(seed)

        selected_tile = random.sample(self.tiles, 1)[0]
        remaining_tiles = list(self.tiles)
        remaining_tiles.remove(selected_tile)

        return selected_tile, TileBag(tiles=tuple(remaining_tiles))


@dataclass(frozen=True, kw_only=True)
class TileDiscard:
    """The collection of colored tiles that have been discarded."""

    tiles: tuple[ColoredTile, ...]

    @staticmethod
    def default() -> TileDiscard:
        """Returns a discarded tile collection with no tiles."""
        return TileDiscard(tiles=())

    @staticmethod
    def new(tiles: Iterable[ColoredTile]) -> TileDiscard:
        """Returns a discarded tile collection with the argument tiles."""
        return TileDiscard(tiles=tuple(tiles))

    def add(self, tiles: tuple[ColoredTile, ...]) -> TileDiscard:
        """Returns a discarded tile collection with the argument tiles appended."""
        return TileDiscard(tiles=self.tiles + tiles)


def reset_tile_bag(
    bag: TileBag, discard: TileDiscard
) -> tuple[TileBag, TileDiscard]:
    """Returns tile bag and discard with the discarded tiles moved back into the bag."""
    return bag.add(discard.tiles), TileDiscard.default()
