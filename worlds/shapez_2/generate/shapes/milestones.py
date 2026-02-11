from typing import TYPE_CHECKING

from . import Processor

if TYPE_CHECKING:
    from ... import Shapez2World


def get_processors_list(world: "Shapez2World") -> list[list[Processor]]:
    milestone_processors: list[list[Processor]] = []
    milestone_order: list[Processor] = []
    milestone_count = world.options.location_adjustments["Milestones"]
    max_processors = world.options.shape_generation_adjustments["Maximum processors per milestone"]
    for _ in range(min(milestone_count, 8)):
        Processor.add_random_next(world.random, milestone_order, None)
    for i in range(milestone_count):
        order_index = (i * 8) // milestone_count if milestone_count > 8 else i
        proc = [milestone_order[order_index]]
        for _ in range(min(max_processors - 1, i)):
            if not Processor.add_restricted_previous(world.random, proc, milestone_order[:order_index]):
                Processor.add_random_next(world.random, proc, milestone_order[:order_index])
        milestone_processors.append(proc)
    return milestone_processors


def get_shapes_list(
    world: "Shapez2World",
    milestone_processors: list[list[Processor]]
) -> list[tuple[list[str], list[str]]]:
    from .generator import generate_shape
    from .downgrader import distinct_downgrades

    milestone_shapes: list[tuple[list[str], list[str]]] = []

    i = 0
    for milestone in milestone_processors:
        i += 3
        # Assumes all milestones have at least 1 processor
        builder1 = generate_shape(world, milestone, i)
        builder2 = generate_shape(world, milestone, i, [builder1.build()])
        milestone_shapes.append((
            distinct_downgrades(world, builder1, milestone.copy(), min(2, len(milestone)), i, builder1.build())[0],
            distinct_downgrades(world, builder2, milestone.copy(), min(2, len(milestone)), i, builder2.build())[0],
        ))

    return milestone_shapes
