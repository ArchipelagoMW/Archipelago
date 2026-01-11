from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ... import PokemonBWWorld


def get_species_checklist(world: "PokemonBWWorld") -> tuple[list[str], set[str]]:
    # Returns ({to be checked species}, {already checked species})
    # Species needed for trade are added in generate_trade_encounters()
    from ...data.pokemon.species import by_name, by_id
    from ...data.pokemon.pokedex import unovan_pokemon

    if "Randomize" not in world.options.randomize_wild_pokemon:
        return [], set()
    elif "Ensure all obtainable" in world.options.randomize_wild_pokemon:
        return [species for species in by_name], set()
    else:  # Just "Randomize"
        always_required = [
            "Celebi",
            "Raikou",
            "Entei",
            "Suicune",
        ]

        unova = [num for num in unovan_pokemon]
        world.random.shuffle(unova)
        for num in unova:
            spec = by_id[(num, 0)]
            if "Fighting" in (by_name[spec].type_1, by_name[spec].type_2):
                always_required.append(spec)
                unova.remove(num)
                break
        always_required += [by_id[(num, 0)] for num in unova[:114]]

        unova_guaranteed = [
            "Tornadus",
            "Thundurus",
            "Deerling (Spring)",
            "Deerling (Summer)",
            "Deerling (Autumn)",
            "Deerling (Winter)",
        ]
        for species in unova_guaranteed:
            if species not in always_required:
                always_required.append(species)

        return always_required, set()


def check_species(world: "PokemonBWWorld", checklist: tuple[list[str], set[str]], species: str, loop=0) -> None:
    from ...data.pokemon.species import by_name, by_id

    if species in checklist[0]:
        checklist[0].remove(species)
    checklist[1].add(species)

    # Looping evolutions are not planned to be prevented
    if loop >= 5:
        return

    data = by_name[species]
    for evolution in data.evolutions:
        if evolution[0] == "Level up with party member":
            add_species_to_check(checklist, by_id[(evolution[1], 0)])
        check_species(world, checklist, evolution[2], loop+1)


def add_species_to_check(checklist: tuple[list[str], set[str]], species: str) -> None:
    if species not in checklist[1]:
        checklist[0].append(species)


def random_percentage_distribution(world: "PokemonBWWorld", length: int) -> list[int]:
    ret = []
    remaining = 100
    for i in reversed(range(2, length+1)):
        rand = world.random.random() ** (i//2)
        if int(rand * 100) % 2:
            value = (remaining//i) + int((remaining-(remaining//i))*rand)
        else:
            value = (remaining//i) + int(-(remaining//i)*rand)
        value = max(1, min(value, remaining-i+1))
        ret.append(value)
        remaining -= value
    ret.append(remaining)
    return ret


def track_down_copy_from(copy_from: dict[str, str | None], slot: str) -> str:
    current = slot
    while copy_from[current] is not None:
        current = copy_from[current]
    return current


def get_slots_checklist(world: "PokemonBWWorld") -> dict[str, str | None]:
    from ...data.locations.encounters.slots import table
    from ...data.locations.encounters import rates

    # {slot: to copy from}
    copy_from: dict[str, str | None] = {slot: None for slot in table}
    # Important: make copies of lists afterwards
    if world.options.modify_encounter_rates.current_key == "plando":
        plando = world.options.modify_encounter_rates.value
        encounter_rates = (
            plando["grass"] if "grass" in plando else rates.tables["vanilla"][0],
            plando["surfing"] if "surfing" in plando else rates.tables["vanilla"][1],
            plando["fishing"] if "fishing" in plando else rates.tables["vanilla"][2],
        )
        world.options.modify_encounter_rates.custom_rates = encounter_rates
    elif world.options.modify_encounter_rates.current_key == "randomized_12":
        encounter_rates = (
            random_percentage_distribution(world, 12),
            random_percentage_distribution(world, 5),
            random_percentage_distribution(world, 5),
        )
        world.options.modify_encounter_rates.custom_rates = encounter_rates
    else:
        encounter_rates = rates.tables[world.options.modify_encounter_rates.current_key]

    if "Randomize" not in world.options.randomize_wild_pokemon:
        return copy_from

    merge_phenomenons = "Merge phenomenons" in world.options.randomize_wild_pokemon
    area_1_to_1 = "Area 1-to-1" in world.options.randomize_wild_pokemon
    prevent_rare_encounters = "Prevent rare encounters" in world.options.randomize_wild_pokemon
    versioned_species = (
        (lambda d: d.species_white)
        if world.options.version == "white"
        else (lambda d: d.species_black)
    )

    if merge_phenomenons:
        # Assumes a fresh copy_from dict without any modifier applied
        for slot in copy_from:
            file_index = table[slot].file_index
            if 24 < file_index[2] < 34 or 41 < file_index[2] < 46 or 51 < file_index[2]:
                copy_from[slot] = slot[:-1] + "0"
            elif file_index[2] in (34, 35):
                copy_from[slot] = slot[:-2] + "0"

    if area_1_to_1:
        # {area: {(dex_num, form): slot}}
        first_slot: dict[int, dict[tuple[int, int], str]] = {}
        for slot in copy_from:
            if copy_from[slot] is None:
                area = table[slot].file_index[0]
                species: tuple[int, int] = versioned_species(table[slot])
                if area not in first_slot:
                    first_slot[area] = {}
                if species not in first_slot[area]:
                    first_slot[area][species] = slot
                else:
                    copy_from[slot] = first_slot[area][species]

    if prevent_rare_encounters:
        # {region: [slot1 rate, slot2 rate, ...]}
        region_added_rates: dict[str, list[int]] = {}
        for slot in copy_from:
            region = table[slot].encounter_region
            method_index = int(slot[-2:])
            if region not in region_added_rates:
                if "G" in region[-2:]:
                    region_added_rates[region] = list(encounter_rates[0])
                elif "S" in region[-2:]:
                    region_added_rates[region] = list(encounter_rates[1])
                elif "F" in region[-2:]:
                    region_added_rates[region] = list(encounter_rates[2])
            if copy_from[slot] is not None:
                to_copy = track_down_copy_from(copy_from, slot)
                region_added_rates[region][int(to_copy[-2:])] += region_added_rates[region][method_index]
                region_added_rates[region][method_index] = 0
        for slot in copy_from:  # StrCity - FR 0, 1, ...11
            region = table[slot].encounter_region  # StrCity - FR
            method_index = int(slot[-2:])  # 0, 1, ..., 11
            is_grass = region[-2:] in (" G", "DG", "RG")
            if copy_from[slot] is None and region_added_rates[region][method_index] < 10:
                for next_index_down in range(12 if is_grass else 5):
                    if next_index_down == method_index:
                        continue
                    next_slot = table[slot].encounter_region + f" {next_index_down}"
                    tracked_slot = track_down_copy_from(copy_from, next_slot)
                    tracked_index = int(tracked_slot[-2:])
                    # if < 15 to distribute them more evenly
                    if (
                        tracked_slot != slot and
                        region_added_rates[region][tracked_index] + region_added_rates[region][method_index] < 15
                    ):
                        copy_from[slot] = next_slot
                        region_added_rates[region][tracked_index] += region_added_rates[region][method_index]
                        region_added_rates[region][method_index] = 0
                        break
                else:
                    for next_index_down in range(12 if is_grass else 5):
                        if next_index_down == method_index:
                            continue
                        next_slot = table[slot].encounter_region + f" {next_index_down}"
                        # If all slots in region were to copy this, then this wouldn't have < 10 added rate
                        if track_down_copy_from(copy_from, next_slot) != slot:
                            copy_from[slot] = next_slot
                            region_added_rates[region][next_index_down] += region_added_rates[region][method_index]
                            region_added_rates[region][method_index] = 0
                            break

    return copy_from
