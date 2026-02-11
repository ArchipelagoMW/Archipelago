from typing import TYPE_CHECKING

from . import Processor

if TYPE_CHECKING:
    from ... import Shapez2World


def get_processors_list(world: "Shapez2World", milestone_processors: list[list[Processor]]) -> list[list[Processor]]:
    operator_processors: list[list[Processor]] = []
    line_count = world.options.location_adjustments["Operator lines"]
    random_lines_count = world.options.location_adjustments["Random operator lines"]
    use_milestones = "Milestone operator lines" in world.options.shape_generation_modifiers
    for line_index in range(line_count-random_lines_count):
        if use_milestones and line_index + 2 < len(milestone_processors):
            operator_processors.append(milestone_processors[line_index + 2].copy())
        else:
            proc_count = world.random.randint(3, 8)
            proc = []
            for _ in range(proc_count):
                Processor.add_random_next(world.random, proc, None)
            operator_processors.append(proc)
    for line_index in range(random_lines_count):
        if line_index != 0 and line_index == random_lines_count - 1:
            operator_processors.append([
                Processor.CUTTER, Processor.ROTATOR, Processor.STACKER, Processor.PAINTER,
                Processor.MIXER, Processor.PIN_PUSHER, Processor.CRYSTALLIZER, Processor.SWAPPER,
            ])
        else:
            operator_processors.append([
                Processor.CUTTER, Processor.ROTATOR, Processor.STACKER, Processor.PAINTER,
                Processor.MIXER, Processor.PIN_PUSHER, Processor.SWAPPER,
            ])
    return operator_processors


def get_shapes_list(
    world: "Shapez2World",
    operator_processors: list[list[Processor]]
) -> list[str | None | int]:
    from .generator import generate_shape

    operator_shapes: list[str | None | int] = []  # str is shape, None is random, int is milestone
    line_count = world.options.location_adjustments["Operator lines"]
    random_lines_count = world.options.location_adjustments["Random operator lines"]
    milestone_count = world.options.location_adjustments["Milestones"]
    use_milestones = "Milestone operator lines" in world.options.shape_generation_modifiers

    for line_index in range(line_count-random_lines_count):
        if use_milestones and line_index + 2 < milestone_count:
            operator_shapes.append(line_index + 2)
        else:
            operator_shapes.append(generate_shape(world, operator_processors[line_index],
                                                  world.random.randint(15, 30)).build())
    operator_shapes.extend([None] * random_lines_count)

    return operator_shapes
