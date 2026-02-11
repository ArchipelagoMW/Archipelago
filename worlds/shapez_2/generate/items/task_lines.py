from typing import TYPE_CHECKING, Iterator
from ...items import Shapez2Item

if TYPE_CHECKING:
    from ... import Shapez2World


def generate_default(world: "Shapez2World") -> Iterator[Shapez2Item]:
    from ...data.items.misc import task_lines

    if "Lock task lines" in world.options.location_modifiers:
        for i in range(3, world.options.location_adjustments["Task lines"]):
            name = f"Task line #{i+1}"
            data = task_lines[name]
            yield Shapez2Item(name, data.classification(world), world.item_name_to_id[name], world.player)


def generate_starting(world: "Shapez2World") -> Iterator[str]:
    if "Lock task lines" in world.options.location_modifiers:
        yield from ("Task line #1", "Task line #2", "Task line #3")
