from typing import TYPE_CHECKING

from . import Processor

if TYPE_CHECKING:
    from ... import Shapez2World


def get_shapes_list(world: "Shapez2World") -> list[str]:
    from .generator import generate_shape
    from .downgrader import distinct_downgrades
    from ...data import blueprint_shapes

    if world.options.blueprint_shapes.is_plando():
        return world.options.blueprint_shapes.plando
    elif world.options.blueprint_shapes == "randomized":
        proc: list[Processor] = []
        for _ in range(5):
            Processor.add_random_next(world.random, proc, None)
        builder = generate_shape(world, proc, 25)
        return distinct_downgrades(world, builder, proc, 4, 25, builder.build())[0]
    elif world.options.shape_configuration == "tetragonal":
        return blueprint_shapes.shapes[world.options.blueprint_shapes.current_key]
    else:
        return blueprint_shapes.shapes["hexagonal"]


def get_points(world: "Shapez2World", blueprint_shapes: list[str]) -> list[int]:
    from ...data.blueprint_shapes import points

    return points[world.options.shape_configuration.current_key][:len(blueprint_shapes)]
