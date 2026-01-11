
from typing import TYPE_CHECKING
from .. import EncounterEntry
import logging

if TYPE_CHECKING:
    from ... import PokemonBWWorld


def generate_wild(world: "PokemonBWWorld",
                  species_checklist: tuple[list[str], set[str]],
                  slots_checklist: dict[str, str | None]) -> dict[str, EncounterEntry]:
    from ...data.pokemon.species import by_name
    from ...data.plando.encounter_maps import maps, multiple_seasons
    from .checklist import check_species

    ret: dict[str, EncounterEntry] = {}
    warned = False

    method_abbr = {
        "Grass": "G",
        "Dark grass": "DG",
        "Rustling grass": "RG",
        "Surfing": "S",
        "Surfing rippling": "SR",
        "Fishing": "F",
        "Fishing rippling": "FR",
    }
    season_index = {
        "": 0,
        "(Spring) ": 0,
        "(Summer) ": 1,
        "(Autumn) ": 2,
        "(Winter) ": 3,
    }
    method_shifting = {
        "Grass": 0,
        "Dark grass": 12,
        "Rustling grass": 24,
        "Surfing": 36,
        "Surfing rippling": 41,
        "Fishing": 46,
        "Fishing rippling": 51,
    }

    for plando in world.options.encounter_plando:
        if len(plando.species) == 1:
            species = plando.species[0]
        else:
            species = world.random.choice(plando.species)
        if species.casefold() == "none":
            continue
        species_data = by_name[species]
        species_id = (species_data.dex_number, species_data.form)
        map_abbr = maps[plando.map][0]
        file_index = maps[plando.map][1]
        if len(plando.seasons) == 0:
            if plando.map in multiple_seasons:
                seasons = ["(Spring) ", "(Summer) ", "(Autumn) ", "(Winter) "]
            else:
                seasons = [""]
        else:
            seasons = [f"({season}) " for season in plando.seasons]
        for season in seasons:
            season_id = season_index[season]
            region = f"{map_abbr} {season}- {method_abbr[plando.method]}"
            if len(plando.slots) == 0:
                slots = (
                    list(range(12))
                    if plando.method in ("Grass", "Dark grass", "Rustling grass")
                    else list(range(5))
                )
            else:
                slots = plando.slots
            for slot in slots:
                slot_in_file = method_shifting[plando.method] + slot
                slot_name = f"{region} {slot}"
                if slot_name in ret:
                    if not warned:
                        logging.warning(f"Player {world.player_name} defined multiple Encounter Plandos on the same "
                                        f"slot(s). Only the first entry/entries will be included.")
                        warned = True
                    continue
                ret[slot_name] = EncounterEntry(
                    species_id, region, (file_index, season_id, slot_in_file), True
                )
                if region in world.regions:
                    check_species(world, species_checklist, species)
                slots_checklist[slot_name] = "FILLED"

    return ret
