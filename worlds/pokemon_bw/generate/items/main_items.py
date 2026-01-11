from typing import TYPE_CHECKING
from ...items import PokemonBWItem

if TYPE_CHECKING:
    from ... import PokemonBWWorld


def generate_default(world: "PokemonBWWorld") -> list[PokemonBWItem]:
    from ...data.items.main_items import min_once, fossils

    return [
        PokemonBWItem(name, data.classification(world), data.item_id, world.player)
        for name, data in min_once.items()
    ] + [
        PokemonBWItem(name, data.classification(world), data.item_id, world.player)
        for name, data in fossils.items()
    ]
