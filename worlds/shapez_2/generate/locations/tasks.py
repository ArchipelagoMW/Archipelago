from typing import TYPE_CHECKING

from BaseClasses import Region

if TYPE_CHECKING:
    from ... import Shapez2World
    from ...data import AccessRule
    from ..shapes import Processor


def create_locations(world: "Shapez2World",
                     regions: dict[str, Region],
                     processor_rules_dict: dict[tuple[str, ...], "AccessRule"]) -> None:
    from ..rules import extended_has_all
    from ..shapes import event_by_processor
    from ...locations import Shapez2Location
    from ...data.locations import all_locations

    def get_rule(proc_: tuple[str, ...]) -> "AccessRule":
        if proc_ not in processor_rules_dict:
            processor_rules_dict[proc_] = lambda state: extended_has_all(world, state, *proc_)
        return processor_rules_dict[proc_]

    task_processors: list[list[Processor]] = world.task_processors
    task_shapes: list[list[str]] = world.task_shapes

    for task_line in range(len(task_shapes)):
        region = regions[f"Task line {task_line + 1}"]
        proc_names = tuple(event_by_processor[p] for p in task_processors[task_line])
        num_tasks = len(task_shapes[task_line])
        for task_num in range(num_tasks):
            name = f"Task #{task_line + 1}-{num_tasks - task_num}"
            rule = get_rule(proc_names[:len(proc_names)-task_num])
            region.locations.append(Shapez2Location(world.player, name, world.location_name_to_id[name], region,
                                                    all_locations[name].progress_type(world), rule))
