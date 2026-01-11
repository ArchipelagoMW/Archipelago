from typing import TYPE_CHECKING

from ...locations import PokemonBWLocation

if TYPE_CHECKING:
    from ... import PokemonBWWorld
    from BaseClasses import Region
    from ...data import AccessRule, FlagLocationData


def lookup(domain: int) -> dict[str, int]:
    from ...data.locations.ingame_items.hidden_items import table

    return {name: data.flag_id + domain for name, data in table.items()}


def create(world: "PokemonBWWorld") -> None:
    from ...data.locations.ingame_items.hidden_items import table

    dowsing_machine_rule: "AccessRule" = lambda state: state.has("Dowsing Machine", world.player)

    def f(loc_data: "FlagLocationData") -> "AccessRule":
        return lambda state: loc_data.rule(state, world) and dowsing_machine_rule(state)

    for name, data in table.items():
        if data.inclusion_rule is None or data.inclusion_rule(world):
            r: "Region" = world.regions[data.region]
            l: PokemonBWLocation = PokemonBWLocation(world.player, name, world.location_name_to_id[name], r)
            l.progress_type = data.progress_type(world)
            if "Require Dowsing Machine" in world.options.modify_logic:
                if data.rule is not None:
                    l.access_rule = f(data)
                else:
                    l.access_rule = dowsing_machine_rule
            else:
                if data.rule is not None:
                    l.access_rule = world.rules_dict[data.rule]
            r.locations.append(l)
