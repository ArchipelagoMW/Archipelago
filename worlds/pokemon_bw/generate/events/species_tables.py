from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ... import PokemonBWWorld
    from ...data import SpeciesData


def populate(world: "PokemonBWWorld", catchable_species_data: dict[str, "SpeciesData"]) -> None:
    from ...data.pokemon import movesets

    for species_name, data in catchable_species_data.items():
        moveset = movesets.table[species_name].tm_hm_moves
        if "HM04" in moveset:
            world.strength_species.add(species_name)
        if "HM01" in moveset:
            world.cut_species.add(species_name)
        if "HM03" in moveset:
            world.surf_species.add(species_name)
        if "HM06" in moveset:
            world.dive_species.add(species_name)
        if "HM05" in moveset:
            world.waterfall_species.add(species_name)
        if "TM70" in moveset:
            world.flash_species.add(species_name)
        if "Fighting" in (data.type_1, data.type_2):
            world.fighting_type_species.add(species_name)
