from typing import TYPE_CHECKING, Iterator
from ...items import Shapez2Item

if TYPE_CHECKING:
    from ... import Shapez2World


def generate_default(world: "Shapez2World") -> Iterator[Shapez2Item]:
    from ...data.items.misc import operator_lines

    if "Lock operator lines" in world.options.location_modifiers:
        for i in range(world.options.location_adjustments["Operator lines"]):
            name = f"Operator line #{i + 1}"
            data = operator_lines[name]
            yield Shapez2Item(name, data.classification(world), world.item_name_to_id[name], world.player)
