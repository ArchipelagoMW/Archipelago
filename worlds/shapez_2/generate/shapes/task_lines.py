from typing import TYPE_CHECKING

from . import Processor

if TYPE_CHECKING:
    from ... import Shapez2World


def get_processors_list(world: "Shapez2World") -> list[list[Processor]]:
    task_processors: list[list[Processor]] = []
    line_count = world.options.location_adjustments["Task lines"]
    min_per_line = world.options.location_adjustments["Minimum checks per task line"]
    max_per_line = world.options.location_adjustments["Maximum checks per task line"]
    for i in range(line_count):
        task_count = world.random.randint(min_per_line, max_per_line)
        if i < 3 and task_count == 5:  # Ensures that the first three lines **can** always have a sphere 1 shape
            task_count = 4
        task: list[Processor] = []
        for __ in range(task_count):
            Processor.add_random_next(world.random, task, None)
        task_processors.append(task)
    return task_processors


def get_shapes_list(
    world: "Shapez2World",
    task_processors: list[list[Processor]]
) -> list[list[str]]:
    from .generator import generate_shape
    from .downgrader import downgrade_shape, distinct_downgrades

    task_shapes: list[list[str]] = []
    i = -1
    for task in task_processors:
        i += 1
        complexity = world.random.randint(len(task) + 2 + (i // 3), len(task) + 3 + i)
        builder = generate_shape(world, task, complexity)
        shapes = distinct_downgrades(world, builder, task.copy(), len(task)-1, complexity, builder.build())[0]
        if i < 3 or (len(task) < 5 and world.random.choice((True, False, False))):
            # Assumes the first three lines always have less than 5 processors
            builder = downgrade_shape(world, builder, [], task[0], complexity)
            shapes.insert(0, builder.build())
        task_shapes.append(shapes)

    return task_shapes
