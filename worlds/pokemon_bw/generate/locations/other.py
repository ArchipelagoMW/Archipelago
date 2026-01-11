from typing import TYPE_CHECKING

from ...locations import PokemonBWLocation

if TYPE_CHECKING:
    from ... import PokemonBWWorld
    from BaseClasses import Region


def lookup(domain: int) -> dict[str, int]:
    from ...data.locations.ingame_items.other import table

    return {
        name: data.flag_id * 100 + domain + (
            int(name[-2:].split("#")[-1]) if "#" in name[-3:] else 0
        )
        for name, data in table.items()
    }


def create(world: "PokemonBWWorld") -> None:
    from ...data.locations.ingame_items.other import table

    for name, data in table.items():
        if data.inclusion_rule is None or data.inclusion_rule(world):
            r: "Region" = world.regions[data.region]
            l: PokemonBWLocation = PokemonBWLocation(world.player, name, world.location_name_to_id[name], r)
            l.progress_type = data.progress_type(world)
            if data.rule is not None:
                l.access_rule = world.rules_dict[data.rule]
            r.locations.append(l)
