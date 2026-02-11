from typing import TYPE_CHECKING, Iterator
from ...items import Shapez2Item

if TYPE_CHECKING:
    from ... import Shapez2World


def generate_default(world: "Shapez2World") -> Iterator[Shapez2Item]:
    from ...data.items.buildings import always, simple_processors, sandbox

    for name, data in always.items():
        yield Shapez2Item(name, data.classification(world), data.item_id, world.player)

    for name, data in simple_processors.items():
        if name != world.starting_processor:
            yield Shapez2Item(name, data.classification(world), data.item_id, world.player)

    if "Add sandbox buildings" in world.options.item_pool_modifiers:
        for name, data in sandbox.items():
            yield Shapez2Item(name, data.classification(world), data.item_id, world.player)


def generate_starting(world: "Shapez2World") -> Iterator[str]:
    from ...data.items.buildings import starting

    yield from starting.keys()

    if world.starting_processor is not None:
        yield world.starting_processor
