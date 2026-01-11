from typing import TYPE_CHECKING
from ...items import PokemonBWItem

if TYPE_CHECKING:
    from ... import PokemonBWWorld


def generate_default(world: "PokemonBWWorld") -> list[PokemonBWItem]:
    from ...data.items.key_items import progression, vanilla, useless, special
    from ...data.items.medicine import important as med_important

    items = [
        PokemonBWItem(name, data.classification(world), data.item_id, world.player)
        for name, data in progression.items()
    ] + [
        PokemonBWItem(name, data.classification(world), data.item_id, world.player)
        for name, data in vanilla.items()
    ] + [
        PokemonBWItem(name, data.classification(world), data.item_id, world.player)
        for name, data in med_important.items()
    ]

    if "Useless key items" in world.options.modify_item_pool:
        items += [
            PokemonBWItem(name, data.classification(world), data.item_id, world.player)
            for name, data in useless.items()
        ]

    data = special["Xtransceiver (Blue)"]
    items.append(PokemonBWItem("Xtransceiver (Blue)", data.classification(world), data.item_id, world.player))
    if world.options.version == "black":
        data = special["Light Stone"]
        items.append(PokemonBWItem("Light Stone", data.classification(world), data.item_id, world.player))
    else:
        data = special["Dark Stone"]
        items.append(PokemonBWItem("Dark Stone", data.classification(world), data.item_id, world.player))

    return items
