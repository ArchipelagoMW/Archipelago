from dataclasses import replace
from typing import TYPE_CHECKING

from .data import data as crystal_data, EncounterKey, EncounterType, EncounterMon, StaticPokemon, EvolutionType, \
    EvolutionData
from .moves import LOGIC_MOVES
from .pokemon import get_pokemon_id_by_rom_id

if TYPE_CHECKING:
    from .world import PokemonCrystalWorld


def load_ut_slot_data(world: "PokemonCrystalWorld"):
    if not world.is_universal_tracker: return

    for key, value in world.ut_slot_data.items():
        try:
            getattr(world.options, key).value = value
        except AttributeError:
            pass

    world.generated_dexcountsanity = world.ut_slot_data["dexcountsanity_counts"]
    world.generated_dexsanity = {get_pokemon_id_by_rom_id(id) for id in world.ut_slot_data["dexsanity_pokemon"]}

    starting_town_id = world.ut_slot_data["starting_town"]
    if starting_town_id:
        world.starting_town = next(
            town for town in crystal_data.starting_towns if town.id == starting_town_id)

    world.options.free_fly_location.value = world.ut_slot_data["free_fly_location_option"]
    free_fly_location_id = world.ut_slot_data["free_fly_location"]
    if free_fly_location_id:
        world.free_fly_location = next(
            region for region in crystal_data.fly_regions if region.id == free_fly_location_id)

    map_card_fly_location_id = world.ut_slot_data["map_card_fly_location"]
    if map_card_fly_location_id:
        world.map_card_fly_location = next(
            region for region in crystal_data.fly_regions if region.id == map_card_fly_location_id)

    request_pokemon = world.ut_slot_data["request_pokemon"]
    world.generated_request_pokemon = [get_pokemon_id_by_rom_id(id) for id in request_pokemon]

    if world.options.trades_required:
        for trade_id, trade_data in world.ut_slot_data["trades"].items():
            world.generated_trades[trade_id] = replace(world.generated_trades[trade_id],
                                                       requested_pokemon=get_pokemon_id_by_rom_id(
                                                           int(trade_data["requested"])),
                                                       received_pokemon=get_pokemon_id_by_rom_id(
                                                           int(trade_data["received"])))

    world.generated_wild = dict()
    world.generated_static = dict()
    for keystring, encounter_ids in world.ut_slot_data["region_encounters"].items():
        key = EncounterKey.from_string(keystring)
        encounters = [get_pokemon_id_by_rom_id(id) for id in encounter_ids]

        if key.encounter_type is EncounterType.Static:
            static = StaticPokemon(name=key.region_id, pokemon=encounters[0], addresses=[], level=1, level_type="",
                                   level_address=None)
            world.generated_static[key] = static
        else:
            wild_encounters = [EncounterMon(1, poke) for poke in encounters]
            world.generated_wild[key] = wild_encounters

    for i, encounter in enumerate(world.ut_slot_data["contest_encounters"]):
        world.generated_contest[i] = replace(world.generated_contest[i], pokemon=get_pokemon_id_by_rom_id(encounter))

    for breeder_str, child in world.ut_slot_data["breeding_info"].items():
        breeder = int(breeder_str)
        world.generated_pokemon[get_pokemon_id_by_rom_id(breeder)] = replace(
            world.generated_pokemon[get_pokemon_id_by_rom_id(breeder)], produces_egg=get_pokemon_id_by_rom_id(child))

    for base_str, evos in world.ut_slot_data["evolution_info"].items():
        base = get_pokemon_id_by_rom_id(int(base_str))
        evolutions = list[EvolutionData]()
        for evo in evos:
            into = get_pokemon_id_by_rom_id(evo["into"])
            evo_type = EvolutionType.from_string(evo["method"])
            level = evo["level"]
            condition = evo["condition"]

            evolutions.append(EvolutionData(
                evo_type=evo_type,
                level=level,
                condition=condition if condition is str else None,
                pokemon=into
            ))

        world.generated_pokemon[base] = replace(world.generated_pokemon[base], evolutions=evolutions)

    for poke_str, hms in world.ut_slot_data["hm_compat"].items():
        poke = get_pokemon_id_by_rom_id(int(poke_str))

        world.generated_pokemon[poke] = replace(world.generated_pokemon[poke],
                                                tm_hm=[LOGIC_MOVES[hm_index] for hm_index in hms])

    world.grass_location_mapping = world.ut_slot_data["grass_location_mapping"]
    world.generated_unown_signs = world.ut_slot_data["unown_signs"]
