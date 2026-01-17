from collections import defaultdict
from dataclasses import replace
from typing import TYPE_CHECKING

from .data import EncounterMon, LogicalAccess, EncounterKey
from .options import RandomizeWilds, EncounterGrouping, BreedingMethodsRequired, RandomizePokemonRequests, \
    RandomizeTrades, EncounterSlotDistribution, Goal
from .pokemon import get_random_pokemon, get_priority_dexsanity
from .utils import pokemon_convert_friendly_to_ids

if TYPE_CHECKING:
    from .world import PokemonCrystalWorld


def randomize_wild_pokemon(world: "PokemonCrystalWorld"):
    if world.options.randomize_wilds and not world.is_universal_tracker:

        exclude_unown = world.options.goal == Goal.option_unown_hunt

        world.generated_wooper = get_random_pokemon(world, exclude_unown=True)

        required_logical_pokemon = 0
        required_accessible_pokemon = 0
        required_inaccessible_pokemon = 0

        for region_key, wilds in world.generated_wild.items():
            logical_access = world.logic.wild_regions[region_key]

            if world.options.encounter_grouping == EncounterGrouping.option_all_split:
                count = len(wilds)
            elif world.options.encounter_grouping == EncounterGrouping.option_one_per_method:
                count = 1
            else:
                count = len({encounter.pokemon for encounter in wilds})

            if logical_access is LogicalAccess.InLogic:
                required_logical_pokemon += count
            elif logical_access is LogicalAccess.OutOfLogic:
                required_accessible_pokemon += count
            else:
                required_inaccessible_pokemon += count

        logical_pokemon_pool = list[str]()
        accessible_pokemon_pool = list[str]()

        if world.options.randomize_wilds.value == RandomizeWilds.option_base_forms:
            logical_pokemon_pool.extend(
                pokemon_id for pokemon_id, pokemon_data in world.generated_pokemon.items() if pokemon_data.is_base)
        elif world.options.randomize_wilds.value == RandomizeWilds.option_evolution_lines:
            base_pokemon = [pokemon_id for pokemon_id, pokemon_data in world.generated_pokemon.items() if
                            pokemon_data.is_base]
            evo_lines = list[list[str]]()
            for base in base_pokemon:
                line = [base]
                for evo in world.generated_pokemon[base].evolutions:
                    line.append(evo.pokemon)
                    for evo2 in world.generated_pokemon[evo.pokemon].evolutions:
                        line.append(evo2.pokemon)
                evo_lines.append(line)

            logical_pokemon_pool.extend(world.random.choice(evo_line) for evo_line in evo_lines)
        elif world.options.randomize_wilds.option_catch_em_all:
            logical_pokemon_pool.extend(world.generated_pokemon.keys())
            if world.options.goal == Goal.option_unown_hunt:
                logical_pokemon_pool = [poke for poke in logical_pokemon_pool if poke != "UNOWN"]

        if world.options.randomize_pokemon_requests == RandomizePokemonRequests.option_items:
            logical_pokemon_pool.extend(world.generated_request_pokemon)

        if world.options.randomize_pokemon_requests:
            logical_pokemon_pool.append("MAGIKARP")

        if world.options.randomize_trades.value in (RandomizeTrades.option_received,
                                                    RandomizeTrades.option_vanilla) and world.options.trades_required:
            logical_pokemon_pool.extend(trade.requested_pokemon for trade in world.generated_trades.values())

        logical_pokemon_pool.extend(get_priority_dexsanity(world))

        global_blocklist = pokemon_convert_friendly_to_ids(world, world.options.wild_encounter_blocklist)

        if global_blocklist:
            logical_pokemon_pool = [pokemon_id for pokemon_id in logical_pokemon_pool if
                                    pokemon_id not in global_blocklist]

        if world.options.randomize_pokemon_requests == RandomizePokemonRequests.option_items:
            logical_pokemon_pool.extend(world.generated_request_pokemon)

        if len(logical_pokemon_pool) > required_logical_pokemon:
            world.random.shuffle(logical_pokemon_pool)
            accessible_pokemon_pool = logical_pokemon_pool[(len(accessible_pokemon_pool) - required_logical_pokemon):]
            logical_pokemon_pool = logical_pokemon_pool[:required_logical_pokemon]

        if len(logical_pokemon_pool) < required_logical_pokemon:
            logical_pokemon_pool.extend(
                get_random_pokemon(world, blocklist=global_blocklist, exclude_unown=exclude_unown) for _ in
                range(required_logical_pokemon - len(logical_pokemon_pool)))

        if (world.options.breeding_methods_required.value == BreedingMethodsRequired.option_with_ditto
                and "DITTO" not in logical_pokemon_pool):
            accessible_pokemon_pool.append(logical_pokemon_pool.pop())
            logical_pokemon_pool.append("DITTO")

        world.random.shuffle(logical_pokemon_pool)

        if len(accessible_pokemon_pool) > required_accessible_pokemon:
            accessible_pokemon_pool = accessible_pokemon_pool[:required_accessible_pokemon]

        if len(accessible_pokemon_pool) < required_accessible_pokemon:
            accessible_pokemon_pool.extend(
                get_random_pokemon(world, blocklist=global_blocklist, exclude_unown=exclude_unown) for _ in
                range(required_accessible_pokemon - len(accessible_pokemon_pool)))

        world.random.shuffle(accessible_pokemon_pool)

        inaccessible_pokemon_pool = [get_random_pokemon(world, blocklist=global_blocklist, exclude_unown=exclude_unown)
                                     for _ in
                                     range(required_inaccessible_pokemon)]

        world.random.shuffle(inaccessible_pokemon_pool)

        def get_pokemon_from_pool(pool: list[str], blocklist: set[str] | None = None) -> str:
            pokemon = pool.pop()

            if blocklist and pokemon in blocklist:
                pokemon = get_random_pokemon(world, blocklist=blocklist | global_blocklist, exclude_unown=exclude_unown)
            return pokemon

        def randomize_encounter_list(region_key: EncounterKey, encounter_list: list[EncounterMon]) -> list[
            EncounterMon]:

            region_type = world.logic.wild_regions[region_key]
            if region_type is LogicalAccess.InLogic:
                pokemon_pool = logical_pokemon_pool
            elif region_type is LogicalAccess.OutOfLogic:
                pokemon_pool = accessible_pokemon_pool
            else:
                pokemon_pool = inaccessible_pokemon_pool

            new_encounters = list[EncounterMon]()
            if world.options.encounter_grouping.value == EncounterGrouping.option_one_per_method:
                pokemon = get_pokemon_from_pool(pokemon_pool)
                for encounter in encounter_list:
                    new_encounters.append(replace(encounter, pokemon=pokemon))

            elif world.options.encounter_grouping.value == EncounterGrouping.option_one_to_one:
                distribution = defaultdict[str, list[int]](list)
                new_encounters = [encounter for encounter in encounter_list]
                encounter_blocklist = set()
                for i, encounter in enumerate(encounter_list):
                    distribution[encounter.pokemon].append(i)
                for pokemon, slots in distribution.items():
                    pokemon = get_pokemon_from_pool(pokemon_pool, encounter_blocklist)
                    encounter_blocklist.add(pokemon)
                    for slot in slots:
                        new_encounters[slot] = replace(new_encounters[slot], pokemon=pokemon)
            else:
                encounter_blocklist = set()
                for encounter in encounter_list:
                    pokemon = get_pokemon_from_pool(pokemon_pool, encounter_blocklist)
                    encounter_blocklist.add(pokemon)
                    new_encounters.append(replace(encounter, pokemon=pokemon))

            return new_encounters

        region_keys = list(world.generated_wild)
        world.random.shuffle(region_keys)
        for region_key in region_keys:
            encounters = world.generated_wild[region_key]
            world.generated_wild[region_key] = randomize_encounter_list(region_key, encounters)

        if logical_pokemon_pool: raise AssertionError(
            "Logical Pokemon pool is not empty, something went horribly wrong.")
        if accessible_pokemon_pool: raise AssertionError(
            "Accessible Pokemon pool is not empty, something went horribly wrong.")
        if inaccessible_pokemon_pool: raise AssertionError(
            "Inaccessible Pokemon pool is not empty, something went horribly wrong.")

        for i, slot in enumerate(world.generated_contest):
            pokemon = get_random_pokemon(world, exclude_unown=True) if world.options.randomize_wilds else slot.pokemon
            world.generated_contest[i] = replace(
                slot,
                pokemon=pokemon,
                percentage=10 if world.options.encounter_slot_distribution == EncounterSlotDistribution.option_equal
                else slot.percentage)
    else:
        for region_key, wilds in world.generated_wild.items():
            if not world.is_universal_tracker and world.options.goal.value == Goal.option_unown_hunt and any(
                    wild.pokemon == "UNOWN" for wild in wilds):
                wilds = [replace(wild, pokemon="RATTATA") for wild in wilds]
                world.generated_wild[region_key] = wilds

    ensure_placed = []

    if world.options.randomize_pokemon_requests:
        ensure_placed.append("MAGIKARP")

    if world.options.randomize_pokemon_requests == RandomizePokemonRequests.option_items:
        ensure_placed.extend(world.generated_request_pokemon)

    if world.options.breeding_methods_required == BreedingMethodsRequired.option_with_ditto:
        ensure_placed.append("DITTO")

    if world.options.trades_required and world.options.randomize_trades.value in (RandomizeTrades.option_received,
                                                                                  RandomizeTrades.option_vanilla):
        ensure_placed.extend(trade.requested_pokemon for trade in world.generated_trades.values())

    for ensure_placed_pokemon in ensure_placed:

        if ensure_placed_pokemon in get_logically_available_wilds(world): continue

        wilds = [(key, wilds) for key, wilds in world.generated_wild.items() if
                 world.logic.wild_regions[key] is LogicalAccess.InLogic and key.region_id is not None]

        wilds.sort(key=lambda x: x[0].region_id)
        world.random.shuffle(wilds)

        seen_pokemon = set()

        to_replace = None
        encounter_key = None
        encounters = None

        while (not to_replace or (to_replace in ensure_placed)) and (to_replace not in seen_pokemon):
            if to_replace:
                seen_pokemon.add(to_replace)
            if not wilds:
                raise RuntimeError(f"{ensure_placed_pokemon} could not be placed anywhere. Aborting.")
            encounter_key, encounters = wilds.pop()
            to_replace = world.random.choice(encounters).pokemon

        encounters = [
            replace(encounter, pokemon=ensure_placed_pokemon if encounter.pokemon == to_replace else encounter.pokemon)
            for
            encounter in encounters]

        world.generated_wild[encounter_key] = encounters


def randomize_static_pokemon(world: "PokemonCrystalWorld"):
    if not world.is_universal_tracker:
        if world.options.randomize_static_pokemon:
            logically_available_wilds = get_logically_available_wilds(world)
            priority_pokemon = get_priority_dexsanity(world) - logically_available_wilds
            blocklist = pokemon_convert_friendly_to_ids(world, world.options.static_blocklist)
            for static_name, pkmn_data in world.generated_static.items():
                pokemon = get_random_pokemon(world,
                                             exclude_unown=True,
                                             base_only=pkmn_data.level_type == "giveegg",
                                             priority_pokemon=priority_pokemon,
                                             blocklist=blocklist)
                world.generated_static[static_name] = replace(
                    world.generated_static[static_name],
                    pokemon=pokemon,
                )
                priority_pokemon.discard(pokemon)

        else:  # Still randomize the Odd Egg
            pokemon = world.random.choice(["PICHU", "CLEFFA", "IGGLYBUFF", "SMOOCHUM", "MAGBY", "ELEKID", "TYROGUE"])
            encounter_key = EncounterKey.static("OddEgg")
            world.generated_static[encounter_key] = replace(world.generated_static[encounter_key], pokemon=pokemon)


def get_logically_available_wilds(world: "PokemonCrystalWorld") -> set[str]:
    logical_pokemon = set[str]()

    for region_key, wilds in world.generated_wild.items():
        access = world.logic.wild_regions[region_key]
        if access is LogicalAccess.InLogic:
            logical_pokemon.update(wild.pokemon for wild in wilds)

    if "Bug Catching Contest" in world.options.wild_encounter_methods_required:
        logical_pokemon.update(slot.pokemon for slot in world.generated_contest)

    if world.options.goal == Goal.option_unown_hunt:
        logical_pokemon.add("UNOWN")

    return logical_pokemon


def get_logically_available_statics(world: "PokemonCrystalWorld") -> set[str]:
    return {static.pokemon for region_key, static in world.generated_static.items() if world.logic.wild_regions[
        region_key] is LogicalAccess.InLogic}
