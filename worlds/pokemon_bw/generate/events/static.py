from typing import TYPE_CHECKING, Callable

from ...locations import PokemonBWLocation
from BaseClasses import ItemClassification, CollectionState
from ...items import PokemonBWItem

if TYPE_CHECKING:
    from ... import PokemonBWWorld
    from BaseClasses import Region
    from ...data import SpeciesData


def create(world: "PokemonBWWorld") -> dict[str, "SpeciesData"]:
    from ...data.pokemon.species import by_id as species_by_id, by_name as species_by_name
    from ...generate import TradeEncounterEntry, StaticEncounterEntry

    catchable_species_data: dict[str, "SpeciesData"] = {}

    def get_trade_rule(x: str) -> Callable[[CollectionState], bool]:
        return lambda state: state.has(x, world.player)

    def f(table: dict[str, TradeEncounterEntry | StaticEncounterEntry]):
        for name, data in table.items():
            if type(data) is TradeEncounterEntry or ((data.inclusion_rule is None) or data.inclusion_rule(world)):
                r: "Region" = world.regions[data.encounter_region]
                l: PokemonBWLocation = PokemonBWLocation(world.player, name, None, r)
                species_id: tuple[int, int] = data.species_id
                species_name: str = species_by_id[species_id]
                item: PokemonBWItem = PokemonBWItem(species_name, ItemClassification.progression, None, world.player)
                l.place_locked_item(item)
                if type(data) is StaticEncounterEntry:
                    if data.access_rule is not None:
                        l.access_rule = world.rules_dict[data.access_rule]
                else:
                    l.access_rule = get_trade_rule(species_by_id[(data.wanted_dex_number, 0)])
                r.locations.append(l)

                species_data: "SpeciesData" = species_by_name[species_name]
                catchable_species_data[species_name] = species_data

    f(world.static_encounter)
    f(world.trade_encounter)

    return catchable_species_data
