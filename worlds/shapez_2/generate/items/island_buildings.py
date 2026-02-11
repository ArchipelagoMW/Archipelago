from typing import TYPE_CHECKING, Iterator
from ...items import Shapez2Item

if TYPE_CHECKING:
    from ... import Shapez2World


def generate_default(world: "Shapez2World") -> Iterator[Shapez2Item]:
    from ...data.items.island_buildings import always, miners

    for name, data in always.items():
        yield Shapez2Item(name, data.classification(world), world.item_name_to_id[name], world.player)

    if "Unlock extensions with miners" not in world.options.item_pool_modifiers:
        for name in ("Shape Miner Extension", "Fluid Miner Extension", "Fluid Miner"):
            data = miners[name]
            yield Shapez2Item(name, data.classification(world), world.item_name_to_id[name], world.player)
    else:
        name = "Fluid Miner + Extension"
        data = miners[name]
        yield Shapez2Item(name, data.classification(world), world.item_name_to_id[name], world.player)


def generate_starting(world: "Shapez2World") -> Iterator[str]:
    from ...data.items.island_buildings import starting

    yield from starting

    if "Unlock extensions with miners" in world.options.item_pool_modifiers:
        yield "Shape Miner + Extension"
    else:
        yield "Shape Miner"
