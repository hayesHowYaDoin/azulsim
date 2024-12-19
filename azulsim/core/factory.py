"""Defines representations of tile pools from which a player can pick from."""

from __future__ import annotations
from typing import Iterable, Sequence, TypeAlias

from pydantic import NonNegativeInt
from pydantic.dataclasses import dataclass

from .tiles import ColoredTile


@dataclass(frozen=True, kw_only=True)
class FactoryDisplay:
    """A factory display which contains a pot of tiles."""

    tiles: tuple[ColoredTile, ColoredTile, ColoredTile, ColoredTile]

    @staticmethod
    def new(tiles: Sequence[ColoredTile]) -> FactoryDisplay:
        """Returns a collection of factory displays with the provided tiles."""
        if len(tiles) != 4:
            raise ValueError("FactoryDisplay must contain 4 tiles.")

        tiles_tuple = tuple(tiles)
        assert len(tiles_tuple) == 4

        return FactoryDisplay(tiles=tiles_tuple)

    def count(self, color: ColoredTile) -> NonNegativeInt:
        """Returns the number of tiles of a given color are in the factory display."""
        return self.tiles.count(color)

    def __contains__(self, item: ColoredTile) -> bool:
        """Returns a boolean indicating whether or not the collection contains an item."""
        return item in self.tiles


@dataclass(frozen=True, kw_only=True)
class FactoryDisplays:
    """Aggregation of all available factory displays."""

    factories: tuple[FactoryDisplay, ...]

    @staticmethod
    def new(factory_displays: Iterable[FactoryDisplay]):
        return FactoryDisplays(factories=tuple(factory_displays))

    def empty(self) -> bool:
        """Returns a boolean indicating whether or not the collection is empty."""
        return len(self.factories) == 0

    def remove(self, factory: FactoryDisplay) -> FactoryDisplays:
        """Returns the factory displays with the argument removed if present."""
        return FactoryDisplays(
            factories=tuple(f for f in self.factories if f != factory)
        )

    def __contains__(self, item: FactoryDisplay) -> bool:
        """Returns a boolean indicating whether or not the collection contains an item."""
        return item in self.factories

    def __len__(self) -> NonNegativeInt:
        """Returns the number of factory displays in the collection."""
        return len(self.factories)


@dataclass(frozen=True, kw_only=True)
class PickedTableCenter:
    """The tile pot in the center of the table after the first player marker has been taken."""

    tiles: tuple[ColoredTile, ...]

    @staticmethod
    def default() -> PickedTableCenter:
        """Returns a picked table center in its default state with no tiles."""
        return PickedTableCenter(tiles=())

    @staticmethod
    def new(tiles: Sequence[ColoredTile]) -> PickedTableCenter:
        """Returns a picked table center with the provided tiles."""
        return PickedTableCenter(tiles=tuple(tiles))

    def count(self, color: ColoredTile) -> NonNegativeInt:
        """Returns the number of tiles of a given color are in the factory display."""
        return self.tiles.count(color)

    def pick(self, color: ColoredTile) -> PickedTableCenter:
        """Returns a picked table center with all tiles of the given color removed."""
        return PickedTableCenter(
            tiles=tuple(tile for tile in self.tiles if tile != color)
        )

    def add(self, tiles: Iterable[ColoredTile]) -> PickedTableCenter:
        """Returns a picked table center with the given tiles added to the pool."""
        return PickedTableCenter(tiles=self.tiles + tuple(tiles))

    def empty(self) -> bool:
        """Returns a boolean representing if the collection is empty."""
        return len(self.tiles) == 0


@dataclass(frozen=True, kw_only=True)
class UnpickedTableCenter:
    """The tile pot in the center of the table before the first player marker has been taken."""

    tiles: tuple[ColoredTile, ...]

    @staticmethod
    def default() -> UnpickedTableCenter:
        """Returns an unpicked table center in its default state with no tiles."""
        return UnpickedTableCenter(tiles=())

    @staticmethod
    def new(tiles: Sequence[ColoredTile]) -> UnpickedTableCenter:
        """Returns an unpicked table center with the provided tiles."""
        return UnpickedTableCenter(tiles=tuple(tiles))

    def count(self, color: ColoredTile) -> NonNegativeInt:
        """Returns the number of tiles of a given color are in the factory display."""
        return self.tiles.count(color)

    def pick(self, color: ColoredTile) -> PickedTableCenter:
        """Returns a picked table center with all tiles of the given color removed."""
        return PickedTableCenter(
            tiles=tuple(tile for tile in self.tiles if tile != color)
        )

    def add(self, tiles: Iterable[ColoredTile]) -> UnpickedTableCenter:
        """Returns a picked table center with the given tiles added to the pool."""
        return UnpickedTableCenter(tiles=self.tiles + tuple(tiles))

    def empty(self) -> bool:
        """Returns a boolean representing if the collection is empty."""
        return len(self.tiles) == 0


"""The pot of tiles in the center of the table."""
TableCenter: TypeAlias = UnpickedTableCenter | PickedTableCenter


"""A pool of tiles from which the player can pick from."""
PickableTilePool: TypeAlias = FactoryDisplay | TableCenter
