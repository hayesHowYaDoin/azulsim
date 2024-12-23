"""Contains unit tests for the azulsim.core.game.factory_offer module's phase_end function."""

import pytest

from azulsim.core.factory import (
    FactoryDisplay,
    FactoryDisplays,
    PickedTableCenter,
    UnpickedTableCenter,
    TableCenter,
)
from azulsim.core.game import factory_offer
from azulsim.core.tiles import ColoredTile


_EMPTY_FACTORY_DISPLAYS = FactoryDisplays.new([])
_POPULATED_FACTORY_DISPLAYS = FactoryDisplays.new(
    [FactoryDisplay.new([ColoredTile.BLACK] * 4)]
)

_EMPTY_PICKED_TABLE_CENTER = PickedTableCenter.new([])
_POPULATED_PICKED_TABLE_CENTER = PickedTableCenter.new([ColoredTile.BLUE])
_EMPTY_UNPICKED_TABLE_CENTER = UnpickedTableCenter.new([])
_POPULATED_UNPICKED_TABLE_CENTER = UnpickedTableCenter.new([ColoredTile.BLUE])


@pytest.mark.parametrize(
    "factories, table_center, expected",
    [
        (_EMPTY_FACTORY_DISPLAYS, _EMPTY_PICKED_TABLE_CENTER, True),
        (_EMPTY_FACTORY_DISPLAYS, _POPULATED_PICKED_TABLE_CENTER, False),
        (_EMPTY_FACTORY_DISPLAYS, _EMPTY_UNPICKED_TABLE_CENTER, False),
        (_EMPTY_FACTORY_DISPLAYS, _POPULATED_UNPICKED_TABLE_CENTER, False),
        (_POPULATED_FACTORY_DISPLAYS, _EMPTY_PICKED_TABLE_CENTER, False),
        (_POPULATED_FACTORY_DISPLAYS, _POPULATED_PICKED_TABLE_CENTER, False),
        (_POPULATED_FACTORY_DISPLAYS, _EMPTY_UNPICKED_TABLE_CENTER, False),
        (_POPULATED_FACTORY_DISPLAYS, _POPULATED_UNPICKED_TABLE_CENTER, False),
    ],
)
def test_phase_end(
    factories: FactoryDisplays, table_center: TableCenter, expected: bool
) -> None:
    assert factory_offer.phase_end(factories, table_center) == expected
