from typing import TYPE_CHECKING

from ...locations import PokemonBWLocation
from BaseClasses import ItemClassification
from ...items import PokemonBWItem

if TYPE_CHECKING:
    from ... import PokemonBWWorld
    from BaseClasses import Region
    from ...data import SpeciesData


def create(world: "PokemonBWWorld") -> dict[str, "SpeciesData"]:
    from ...data.pokemon.species import by_id as species_by_id, by_name as species_by_name

    catchable_species_data: dict[str, "SpeciesData"] = {}
    # To remove duplicates
    available_in_region: dict[str, set[str]] = {}

    for name, data in world.wild_encounter.items():
        if data.encounter_region in world.regions:
            if data.encounter_region not in available_in_region:
                available_in_region[data.encounter_region] = set()
            r: "Region" = world.regions[data.encounter_region]
            species_id: tuple[int, int] = data.species_id
            species_name: str = species_by_id[species_id]
            if species_name in available_in_region[data.encounter_region]:
                continue
            l: PokemonBWLocation = PokemonBWLocation(world.player, name, None, r)
            item: PokemonBWItem = PokemonBWItem(species_name, ItemClassification.progression, None, world.player)
            l.place_locked_item(item)
            r.locations.append(l)

            species_data: "SpeciesData" = species_by_name[species_name]
            catchable_species_data[species_name] = species_data
            available_in_region[data.encounter_region].add(species_name)

    return catchable_species_data
