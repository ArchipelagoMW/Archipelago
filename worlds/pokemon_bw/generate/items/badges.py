from typing import TYPE_CHECKING
from ...items import PokemonBWItem

if TYPE_CHECKING:
    from ... import PokemonBWWorld


def generate_default(world: "PokemonBWWorld") -> list[PokemonBWItem]:
    from ...data.items.badges import table

    return [
        PokemonBWItem(name, data.classification(world), data.item_id, world.player)
        for name, data in table.items()
    ]
