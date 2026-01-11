from typing import TYPE_CHECKING
from ...items import PokemonBWItem

if TYPE_CHECKING:
    from ... import PokemonBWWorld


def generate_default(world: "PokemonBWWorld") -> list[PokemonBWItem]:
    from ...data.items.seasons import table

    if world.options.season_control == "randomized":
        return [
            PokemonBWItem(name, data.classification(world), data.item_id, world.player)
            for name, data in table.items()
        ]
    else:
        return []
