from random import Random
from typing import TYPE_CHECKING

from . import Processor, ShapeBuilder, downgrade_hexagonal, downgrade_tetragonal

if TYPE_CHECKING:
    from ... import Shapez2World


def downgrade_shape(world: "Shapez2World", builder: ShapeBuilder, remaining_processors: list[Processor],
                    missing_processor: Processor, original_complexity: int) -> ShapeBuilder:
    # IMPORTANT: Modifies the builder itself
    if world.options.shape_configuration == "tetragonal":
        return downgrade_tetragonal.downgrade_4(world.random, builder, remaining_processors, missing_processor,
                                                original_complexity)
    else:
        return downgrade_hexagonal.downgrade_6(world.random, builder, remaining_processors, missing_processor,
                                               original_complexity)


def distinct_downgrades(world: "Shapez2World", builder: ShapeBuilder, processors: list[Processor], count: int,
                        original_complexity: int, original_shape: str) -> tuple[list[str], ShapeBuilder]:
    return _distinct_downgrades(world.random, builder, processors, count,
                                world.options.shape_configuration == "tetragonal", original_complexity, original_shape)


def _distinct_downgrades(rand: Random, builder: ShapeBuilder, processors: list[Processor], count: int, tetragonal: bool,
                         original_complexity: int, original_shape: str) -> tuple[list[str], ShapeBuilder]:
    # IMPORTANT: Modifies the builder and processors list themselves
    # output is reversed, i.e. least to most remaining processors
    # original shape is also put into output
    out = [original_shape]
    downgrade = downgrade_tetragonal.downgrade_4 if tetragonal else downgrade_hexagonal.downgrade_6
    for _ in range(count):
        missing = processors.pop()
        builder = downgrade(rand, builder, processors, missing, original_complexity)
        down_shape = builder.build()
        tries = 0
        while out[0] == down_shape:
            to_put = 0
            if not processors or tries > 2:
                break
            if missing in Processor.restrictions():
                needed = Processor.restrictions()[missing]
                if processors[-1] in needed:
                    break
                else:
                    to_put = -1
            processors.insert(to_put, missing)
            missing = processors.pop()
            builder = downgrade(rand, builder, processors, missing, original_complexity)
            down_shape = builder.build()
            tries += 1
        out.insert(0, down_shape)
    return out, builder
