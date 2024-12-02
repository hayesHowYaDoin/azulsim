from annotated_types import Ge, Le
from itertools import islice
from typing import Annotated

from pydantic import BaseModel, Field
from pydantic.types import NegativeInt


class FloorLine(BaseModel):
    """A floor line on a board."""

    num_tiles: Annotated[int, Ge(0), Le(7)] = Field(default=0)


def calculate_penalty(floor_line: FloorLine) -> NegativeInt:
    """Returns the calculated penalty for the contents of a floor line."""
    penalties = (-1, -1, -2, -2, -2, -3, -3)
    return sum(islice(penalties, floor_line.num_tiles))
