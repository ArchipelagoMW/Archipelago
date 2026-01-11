import itertools
from typing import TYPE_CHECKING, Callable
from .. import EncounterEntry

if TYPE_CHECKING:
    from ... import PokemonBWWorld
    from ...data import SpeciesData
    from .. import EncounterEntry


def organize_by_method(world: "PokemonBWWorld") -> dict[str, tuple[list[str], list[int]]]:
    from ...data.pokemon.species import by_id
    # {method: ([species names], [dex numbers])}
    ret: dict[str, tuple[list[str], list[int]]] = {}
    for slot, data in world.wild_encounter.items():
        if data.encounter_region not in ret:
            ret[data.encounter_region] = ([], [])
        spec = by_id[data.species_id]
        if spec not in ret[data.encounter_region][0]:
            ret[data.encounter_region][0].append(spec)
        if data.species_id[0] not in ret[data.encounter_region][1]:
            ret[data.encounter_region][1].append(data.species_id[0])
    return ret


def generate_wild_encounters(world: "PokemonBWWorld",
                             species_checklist: tuple[list[str], set[str]],
                             slots_checklist: dict[str, str | None]) -> dict[str, EncounterEntry]:
    from ...data.pokemon.species import by_name, by_id
    from ...data.locations.encounters.slots import table
    from .checklist import check_species

    versioned_species = (
        (lambda d: d.species_white)
        if world.options.version == "white"
        else (lambda d: d.species_black)
    )

    if "Randomize" not in world.options.randomize_wild_pokemon:
        return {
            name: EncounterEntry(
                versioned_species(table[name]), table[name].encounter_region, table[name].file_index, False
            )
            for name, to_copy in slots_checklist.items() if to_copy != "FILLED"
        }

    encounter_entries: dict[str, EncounterEntry] = {}
    logic_slots: list[str] = []
    other_slots: list[str] = []
    copy_slots: list[str] = []
    for name, to_copy in slots_checklist.items():
        if to_copy == "FILLED":
            continue
        elif to_copy is not None:
            copy_slots.append(name)
        elif table[name].encounter_region in world.regions:
            logic_slots.append(name)
        else:
            other_slots.append(name)
    world.random.shuffle(logic_slots)
    world.random.shuffle(other_slots)
    world.random.shuffle(copy_slots)

    if len(species_checklist[0]) > len(logic_slots):
        for species in species_checklist[0][:]:
            species_data = by_name[species]
            for evolution in species_data.evolutions:
                if evolution[0] != "Level up with party member":
                    check_species(world, species_checklist, evolution[2])
        if len(species_checklist[0]) > len(logic_slots):
            raise Exception(
                f"More required species for randomized wild encounter than slots they could be placed in "
                f"for player {world.player_name}: {len(species_checklist[0])} > {len(logic_slots)}"
            )

    similar_base_stats = "Similar base stats" in world.options.randomize_wild_pokemon
    type_themed = "Type themed areas" in world.options.randomize_wild_pokemon
    area_types: dict[str, str] = {}
    stats_total: Callable[["SpeciesData"], int] = lambda data: (
        data.base_hp + data.base_attack + data.base_defense +
        data.base_sp_attack + data.base_sp_defense + data.base_speed
    )

    while len(species_checklist[0]) > 0:
        random_species = world.random.choice(species_checklist[0])
        species_data = by_name[random_species]
        stat_tolerance = world.options.pokemon_randomization_adjustments["Stats leniency"]
        skip_strict = False
        while True:
            skipped_stat = False
            for slot in logic_slots:
                if type_themed and not skip_strict:
                    region = table[slot].encounter_region
                    area = region[:region.index(" - ")]
                    if area not in area_types:
                        area_types[area] = world.random.choice((species_data.type_1, species_data.type_2))
                    elif area_types[area] not in (species_data.type_1, species_data.type_2):
                        continue
                if similar_base_stats:  # stats last because it's more lenient than tape themed
                    random_stats = stats_total(species_data)
                    vanilla_stats = stats_total(by_name[by_id[versioned_species(table[slot])]])
                    if random_stats not in range(vanilla_stats - stat_tolerance, vanilla_stats + stat_tolerance + 1):
                        skipped_stat = True
                        continue
                encounter_entries[slot] = EncounterEntry(
                    (species_data.dex_number, species_data.form),
                    table[slot].encounter_region, table[slot].file_index, True
                )
                check_species(world, species_checklist, random_species)
                logic_slots.remove(slot)
                break
            else:
                if skipped_stat:
                    stat_tolerance += 10
                else:
                    # Force place into any slot that still kinda fits
                    skip_strict = True
                continue
            break

    any_species = [name for name in by_name]
    any_species_by_type: dict[str, list[str]] = {}
    for s in any_species:
        for t in (by_name[s].type_1, by_name[s].type_2):
            if t not in any_species_by_type:
                any_species_by_type[t] = [s]
            else:
                any_species_by_type[t].append(s)
    for slot in itertools.chain(logic_slots, other_slots):
        stat_tolerance = world.options.pokemon_randomization_adjustments["Stats leniency"]
        region = table[slot].encounter_region
        area = region[:region.index(" - ")]
        while True:
            species_name = world.random.choice(any_species)
            species_data = by_name[species_name]
            if type_themed:
                if area not in area_types:
                    area_types[area] = world.random.choice((species_data.type_1, species_data.type_2))
                elif area_types[area] not in (species_data.type_1, species_data.type_2):
                    species_name = world.random.choice(any_species_by_type[area_types[area]])
                    species_data = by_name[species_name]
            if similar_base_stats:
                random_stats = stats_total(species_data)
                vanilla_stats = stats_total(by_name[by_id[versioned_species(table[slot])]])
                if random_stats not in range(vanilla_stats - stat_tolerance, vanilla_stats + stat_tolerance + 1):
                    stat_tolerance += 10
                    continue
            encounter_entries[slot] = EncounterEntry(
                (species_data.dex_number, species_data.form), table[slot].encounter_region, table[slot].file_index, True
            )
            break
    for slot in copy_slots:
        to_copy = slots_checklist[slot]
        while slots_checklist[to_copy] is not None:
            to_copy = slots_checklist[to_copy]
        encounter_entries[slot] = EncounterEntry(
            encounter_entries[to_copy].species_id, table[slot].encounter_region, table[slot].file_index, True
        )

    if len(encounter_entries) + len(world.wild_encounter) != len(table):
        raise Exception(f"Player {world.player_name}: Number of generated encounters does not match data "
                        f"({len(encounter_entries) + len(world.wild_encounter)} entries, {len(table)} data rows)")

    return encounter_entries
