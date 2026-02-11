
from random import Random
from typing import Iterable

from . import Processor, ShapeBuilder


def downgrade_6(rand: Random, builder: ShapeBuilder, remaining_processors: list[Processor],
                missing_processor: Processor, original_complexity: int) -> ShapeBuilder:
    ...
