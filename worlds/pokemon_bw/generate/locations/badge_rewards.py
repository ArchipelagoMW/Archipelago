from typing import TYPE_CHECKING

from ...locations import PokemonBWLocation

if TYPE_CHECKING:
    from ... import PokemonBWWorld
    from BaseClasses import Region


def lookup(domain: int) -> dict[str, int]:
    from ...data.locations.ingame_items.special import gym_badges

    return {name: data.flag_id + domain for name, data in gym_badges.items()}


def create(world: "PokemonBWWorld") -> None:
    from ...data.locations.ingame_items.special import gym_badges

    for name, data in gym_badges.items():
        if data.inclusion_rule is None or data.inclusion_rule(world):
            r: "Region" = world.regions[data.region]
            l: PokemonBWLocation = PokemonBWLocation(world.player, name, world.location_name_to_id[name], r)
            l.progress_type = data.progress_type(world)
            if data.rule is not None:
                l.access_rule = world.rules_dict[data.rule]
            r.locations.append(l)
