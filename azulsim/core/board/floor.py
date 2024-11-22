from pydantic.dataclasses import dataclass
from pydantic.types import NonNegativeInt


@dataclass(frozen=True)
class FloorLine:
    """A floor line on a board."""

    num_tiles: NonNegativeInt
