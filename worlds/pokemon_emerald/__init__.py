"""
Archipelago World definition for Pokemon Emerald Version
"""
from collections import Counter
import copy
import logging
import os
from typing import Any, Set, List, Dict, Optional, Tuple, ClassVar

from BaseClasses import ItemClassification, MultiWorld, Tutorial
from Fill import FillError, fill_restrictive
from Options import Toggle
import settings
from worlds.AutoWorld import WebWorld, World

from .client import PokemonEmeraldClient  # Unused, but required to register with BizHawkClient
from .data import (SpeciesData, MapData, EncounterTableData, LearnsetMove, TrainerPokemonData, StaticEncounterData,
                   TrainerData, data as emerald_data)
from .items import (ITEM_GROUPS, PokemonEmeraldItem, create_item_label_to_code_map, get_item_classification,
                    offset_item_value)
from .locations import (LOCATION_GROUPS, PokemonEmeraldLocation, create_location_label_to_id_map,
                        create_locations_with_tags)
from .options import (ItemPoolType, RandomizeWildPokemon, RandomizeBadges, RandomizeTrainerParties, RandomizeHms,
                      RandomizeStarters, LevelUpMoves, RandomizeAbilities, RandomizeTypes, TmCompatibility,
                      HmCompatibility, RandomizeStaticEncounters, NormanRequirement, PokemonEmeraldOptions)
from .pokemon import get_random_species, get_random_move, get_random_damaging_move, get_random_type
from .regions import create_regions
from .rom import PokemonEmeraldDeltaPatch, generate_output, location_visited_event_to_id_map
from .rules import set_rules
from .sanity_check import validate_regions
from .util import int_to_bool_array, bool_array_to_int


class PokemonEmeraldWebWorld(WebWorld):
    """
    Webhost info for Pokemon Emerald
    """
    theme = "ocean"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Pokémon Emerald with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Zunawe"]
    )

    tutorials = [setup_en]


class PokemonEmeraldSettings(settings.Group):
    class PokemonEmeraldRomFile(settings.UserFilePath):
        """File name of your English Pokemon Emerald ROM"""
        description = "Pokemon Emerald ROM File"
        copy_to = "Pokemon - Emerald Version (USA, Europe).gba"
        md5s = [PokemonEmeraldDeltaPatch.hash]

    rom_file: PokemonEmeraldRomFile = PokemonEmeraldRomFile(PokemonEmeraldRomFile.copy_to)


class PokemonEmeraldWorld(World):
    """
    Pokémon Emerald is the definitive Gen III Pokémon game and one of the most beloved in the franchise.
    Catch, train, and battle Pokémon, explore the Hoenn region, thwart the plots
    of Team Magma and Team Aqua, challenge gyms, and become the Pokémon champion!
    """
    game = "Pokemon Emerald"
    web = PokemonEmeraldWebWorld()
    topology_present = True

    settings_key = "pokemon_emerald_settings"
    settings: ClassVar[PokemonEmeraldSettings]

    options_dataclass = PokemonEmeraldOptions
    options: PokemonEmeraldOptions

    item_name_to_id = create_item_label_to_code_map()
    location_name_to_id = create_location_label_to_id_map()
    item_name_groups = ITEM_GROUPS
    location_name_groups = LOCATION_GROUPS

    data_version = 1
    required_client_version = (0, 4, 3)

    badge_shuffle_info: Optional[List[Tuple[PokemonEmeraldLocation, PokemonEmeraldItem]]] = None
    hm_shuffle_info: Optional[List[Tuple[PokemonEmeraldLocation, PokemonEmeraldItem]]] = None
    free_fly_location_id: int = 0

    modified_species: List[Optional[SpeciesData]]
    modified_maps: List[MapData]
    modified_tmhm_moves: List[int]
    modified_static_encounters: List[int]
    modified_starters: Tuple[int, int, int]
    modified_trainers: List[TrainerData]

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        if not os.path.exists(cls.settings.rom_file):
            raise FileNotFoundError(cls.settings.rom_file)

        assert validate_regions()

    def get_filler_item_name(self) -> str:
        return "Great Ball"

    def generate_early(self) -> None:
        # If badges or HMs are vanilla, Norman locks you from using Surf, which means you're not guaranteed to be
        # able to reach Fortree Gym, Mossdeep Gym, or Sootopolis Gym. So we can't require reaching those gyms to
        # challenge Norman or it creates a circular dependency.
        # This is never a problem for completely random badges/hms because the algo will not place Surf/Balance Badge
        # on Norman on its own. It's never a problem for shuffled badges/hms because there is no scenario where Cut or
        # the Stone Badge can be a lynchpin for access to any gyms, so they can always be put on Norman in a worst case
        # scenario.
        # This will also be a problem in warp rando if direct access to Norman's room requires Surf or if access
        # any gym leader in general requires Surf. We will probably have to force this to 0 in that case.
        max_norman_count = 7

        if self.options.badges == RandomizeBadges.option_vanilla:
            max_norman_count = 4

        if self.options.hms == RandomizeHms.option_vanilla:
            if self.options.norman_requirement == NormanRequirement.option_badges:
                if self.options.badges != RandomizeBadges.option_completely_random:
                    max_norman_count = 4
            if self.options.norman_requirement == NormanRequirement.option_gyms:
                max_norman_count = 4

        if self.options.norman_count.value > max_norman_count:
            logging.warning("Pokemon Emerald: Norman requirements for Player %s (%s) are unsafe in combination with "
                            "other settings. Reducing to 4.", self.player, self.multiworld.get_player_name(self.player))
            self.options.norman_count.value = max_norman_count

    def create_regions(self) -> None:
        regions = create_regions(self)

        tags = {"Badge", "HM", "KeyItem", "Rod", "Bike"}
        if self.options.overworld_items:
            tags.add("OverworldItem")
        if self.options.hidden_items:
            tags.add("HiddenItem")
        if self.options.npc_gifts:
            tags.add("NpcGift")
        if self.options.enable_ferry:
            tags.add("Ferry")
        create_locations_with_tags(self, regions, tags)

        self.multiworld.regions.extend(regions.values())

    def create_items(self) -> None:
        item_locations: List[PokemonEmeraldLocation] = [
            location
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ]

        # Filter progression items which shouldn't be shuffled into the itempool. Their locations
        # still exist, but event items will be placed and locked at their vanilla locations instead.
        filter_tags = set()

        if not self.options.key_items:
            filter_tags.add("KeyItem")
        if not self.options.rods:
            filter_tags.add("Rod")
        if not self.options.bikes:
            filter_tags.add("Bike")

        if self.options.badges in {RandomizeBadges.option_vanilla, RandomizeBadges.option_shuffle}:
            filter_tags.add("Badge")
        if self.options.hms in {RandomizeHms.option_vanilla, RandomizeHms.option_shuffle}:
            filter_tags.add("HM")

        if self.options.badges == RandomizeBadges.option_shuffle:
            self.badge_shuffle_info = [
                (location, self.create_item_by_code(location.default_item_code))
                for location in [l for l in item_locations if "Badge" in l.tags]
            ]
        if self.options.hms == RandomizeHms.option_shuffle:
            self.hm_shuffle_info = [
                (location, self.create_item_by_code(location.default_item_code))
                for location in [l for l in item_locations if "HM" in l.tags]
            ]

        item_locations = [location for location in item_locations if len(filter_tags & location.tags) == 0]
        default_itempool = [self.create_item_by_code(location.default_item_code) for location in item_locations]

        if self.options.item_pool_type == ItemPoolType.option_shuffled:
            self.multiworld.itempool += default_itempool

        elif self.options.item_pool_type in {ItemPoolType.option_diverse, ItemPoolType.option_diverse_balanced}:
            item_categories = ["Ball", "Heal", "Vitamin", "EvoStone", "Money", "TM", "Held", "Misc"]

            # Count occurrences of types of vanilla items in pool
            item_category_counter = Counter()
            for item in default_itempool:
                if not item.advancement:
                    item_category_counter.update([tag for tag in item.tags if tag in item_categories])

            item_category_weights = [item_category_counter.get(category) for category in item_categories]
            item_category_weights = [weight if weight is not None else 0 for weight in item_category_weights]

            # Create lists of item codes that can be used to fill
            fill_item_candidates = emerald_data.items.values()

            fill_item_candidates = [item for item in fill_item_candidates if "Unique" not in item.tags]

            fill_item_candidates_by_category = {category: [] for category in item_categories}
            for item_data in fill_item_candidates:
                for category in item_categories:
                    if category in item_data.tags:
                        fill_item_candidates_by_category[category].append(offset_item_value(item_data.item_id))

            for category in fill_item_candidates_by_category:
                fill_item_candidates_by_category[category].sort()

            # Ignore vanilla occurrences and pick completely randomly
            if self.options.item_pool_type == ItemPoolType.option_diverse:
                item_category_weights = [
                    len(category_list)
                    for category_list in fill_item_candidates_by_category.values()
                ]

            # TMs should not have duplicates until every TM has been used already
            all_tm_choices = fill_item_candidates_by_category["TM"].copy()

            def refresh_tm_choices() -> None:
                fill_item_candidates_by_category["TM"] = all_tm_choices.copy()
                self.random.shuffle(fill_item_candidates_by_category["TM"])

            # Create items
            for item in default_itempool:
                if not item.advancement and "Unique" not in item.tags:
                    category = self.random.choices(item_categories, item_category_weights)[0]
                    if category == "TM":
                        if len(fill_item_candidates_by_category["TM"]) == 0:
                            refresh_tm_choices()
                        item_code = fill_item_candidates_by_category["TM"].pop()
                    else:
                        item_code = self.random.choice(fill_item_candidates_by_category[category])
                    item = self.create_item_by_code(item_code)

                self.multiworld.itempool.append(item)

    def set_rules(self) -> None:
        set_rules(self)

    def generate_basic(self) -> None:
        locations: List[PokemonEmeraldLocation] = self.multiworld.get_locations(self.player)

        # Set our free fly location
        # If not enabled, set it to Littleroot Town by default
        fly_location_name = "EVENT_VISITED_LITTLEROOT_TOWN"
        if self.options.free_fly_location:
            fly_location_name = self.random.choice([
                "EVENT_VISITED_SLATEPORT_CITY",
                "EVENT_VISITED_MAUVILLE_CITY",
                "EVENT_VISITED_VERDANTURF_TOWN",
                "EVENT_VISITED_FALLARBOR_TOWN",
                "EVENT_VISITED_LAVARIDGE_TOWN",
                "EVENT_VISITED_FORTREE_CITY",
                "EVENT_VISITED_LILYCOVE_CITY",
                "EVENT_VISITED_MOSSDEEP_CITY",
                "EVENT_VISITED_SOOTOPOLIS_CITY",
                "EVENT_VISITED_EVER_GRANDE_CITY"
            ])

        self.free_fly_location_id = location_visited_event_to_id_map[fly_location_name]

        free_fly_location_location = self.multiworld.get_location("FREE_FLY_LOCATION", self.player)
        free_fly_location_location.item = None
        free_fly_location_location.place_locked_item(self.create_event(fly_location_name))

        # Key items which are considered in access rules but not randomized are converted to events and placed
        # in their vanilla locations so that the player can have them in their inventory for logic.
        def convert_unrandomized_items_to_events(tag: str) -> None:
            for location in locations:
                if location.tags is not None and tag in location.tags:
                    location.place_locked_item(self.create_event(self.item_id_to_name[location.default_item_code]))
                    location.address = None

        if self.options.badges == RandomizeBadges.option_vanilla:
            convert_unrandomized_items_to_events("Badge")
        if self.options.hms == RandomizeHms.option_vanilla:
            convert_unrandomized_items_to_events("HM")
        if not self.options.rods:
            convert_unrandomized_items_to_events("Rod")
        if not self.options.bikes:
            convert_unrandomized_items_to_events("Bike")
        if not self.options.key_items:
            convert_unrandomized_items_to_events("KeyItem")

    def pre_fill(self) -> None:
        # Items which are shuffled between their own locations
        if self.options.badges == RandomizeBadges.option_shuffle:
            badge_locations: List[PokemonEmeraldLocation]
            badge_items: List[PokemonEmeraldItem]

            # Sort order makes `fill_restrictive` try to place important badges later, which
            # makes it less likely to have to swap at all, and more likely for swaps to work.
            # In the case of vanilla HMs, navigating Granite Cave is required to access more than 2 gyms,
            # so Knuckle Badge deserves highest priority if Flash is logically required.
            badge_locations, badge_items = [list(l) for l in zip(*self.badge_shuffle_info)]
            badge_priority = {
                "Knuckle Badge": 0 if (self.options.hms == RandomizeHms.option_vanilla and self.options.require_flash) else 3,
                "Balance Badge": 1,
                "Dynamo Badge": 1,
                "Mind Badge": 2,
                "Heat Badge": 2,
                "Rain Badge": 3,
                "Stone Badge": 4,
                "Feather Badge": 5
            }
            badge_items.sort(key=lambda item: badge_priority.get(item.name, 0))

            collection_state = self.multiworld.get_all_state(False)
            if self.hm_shuffle_info is not None:
                for _, item in self.hm_shuffle_info:
                    collection_state.collect(item)

            # In specific very constrained conditions, fill_restrictive may run
            # out of swaps before it finds a valid solution if it gets unlucky.
            # This is a band-aid until fill/swap can reliably find those solutions.
            attempts_remaining = 2
            while attempts_remaining > 0:
                attempts_remaining -= 1
                self.random.shuffle(badge_locations)
                try:
                    fill_restrictive(self.multiworld, collection_state, badge_locations, badge_items,
                                     single_player_placement=True, lock=True, allow_excluded=True)
                    break
                except FillError as exc:
                    if attempts_remaining == 0:
                        raise exc

                    logging.debug(f"Failed to shuffle badges for player {self.player}. Retrying.")
                    continue

        if self.options.hms == RandomizeHms.option_shuffle:
            hm_locations: List[PokemonEmeraldLocation]
            hm_items: List[PokemonEmeraldItem]

            # Sort order makes `fill_restrictive` try to place important HMs later, which
            # makes it less likely to have to swap at all, and more likely for swaps to work.
            # In the case of vanilla badges, navigating Granite Cave is required to access more than 2 gyms,
            # so Flash deserves highest priority if it's logically required.
            hm_locations, hm_items = [list(l) for l in zip(*self.hm_shuffle_info)]
            hm_priority = {
                "HM05 Flash": 0 if (self.options.badges == RandomizeBadges.option_vanilla and self.options.require_flash) else 3,
                "HM03 Surf": 1,
                "HM06 Rock Smash": 1,
                "HM08 Dive": 2,
                "HM04 Strength": 2,
                "HM07 Waterfall": 3,
                "HM01 Cut": 4,
                "HM02 Fly": 5
            }
            hm_items.sort(key=lambda item: hm_priority.get(item.name, 0))

            collection_state = self.multiworld.get_all_state(False)

            # In specific very constrained conditions, fill_restrictive may run
            # out of swaps before it finds a valid solution if it gets unlucky.
            # This is a band-aid until fill/swap can reliably find those solutions.
            attempts_remaining = 2
            while attempts_remaining > 0:
                attempts_remaining -= 1
                self.random.shuffle(hm_locations)
                try:
                    fill_restrictive(self.multiworld, collection_state, hm_locations, hm_items,
                                     single_player_placement=True, lock=True, allow_excluded=True)
                    break
                except FillError as exc:
                    if attempts_remaining == 0:
                        raise exc

                    logging.debug(f"Failed to shuffle HMs for player {self.player}. Retrying.")
                    continue

    def generate_output(self, output_directory: str) -> None:
        def randomize_abilities() -> None:
            # Creating list of potential abilities
            ability_label_to_value = {ability.label.lower(): ability.ability_id for ability in emerald_data.abilities}

            ability_blacklist_labels = {"cacophony"}
            option_ability_blacklist = self.options.ability_blacklist.value
            if option_ability_blacklist is not None:
                ability_blacklist_labels |= {ability_label.lower() for ability_label in option_ability_blacklist}

            ability_blacklist = {ability_label_to_value[label] for label in ability_blacklist_labels}
            ability_whitelist = [a.ability_id for a in emerald_data.abilities if a.ability_id not in ability_blacklist]

            if self.options.abilities == RandomizeAbilities.option_follow_evolutions:
                already_modified: Set[int] = set()

                # Loops through species and only tries to modify abilities if the pokemon has no pre-evolution
                # or if the pre-evolution has already been modified. Then tries to modify all species that evolve
                # from this one which have the same abilities.
                # The outer while loop only runs three times for vanilla ordering: Once for a first pass, once for
                # Hitmonlee/Hitmonchan, and once to verify that there's nothing left to do.
                while True:
                    had_clean_pass = True
                    for species in self.modified_species:
                        if species is None:
                            continue
                        if species.species_id in already_modified:
                            continue
                        if species.pre_evolution is not None and species.pre_evolution not in already_modified:
                            continue

                        had_clean_pass = False

                        old_abilities = species.abilities
                        new_abilities = (
                            0 if old_abilities[0] == 0 else self.random.choice(ability_whitelist),
                            0 if old_abilities[1] == 0 else self.random.choice(ability_whitelist)
                        )

                        evolutions = [species]
                        while len(evolutions) > 0:
                            evolution = evolutions.pop()
                            if evolution.abilities == old_abilities:
                                evolution.abilities = new_abilities
                                already_modified.add(evolution.species_id)
                                evolutions += [
                                    self.modified_species[evolution.species_id]
                                    for evolution in evolution.evolutions
                                    if evolution.species_id not in already_modified
                                ]

                    if had_clean_pass:
                        break
            else:  # Not following evolutions
                for species in self.modified_species:
                    if species is None:
                        continue

                    old_abilities = species.abilities
                    new_abilities = (
                        0 if old_abilities[0] == 0 else self.random.choice(ability_whitelist),
                        0 if old_abilities[1] == 0 else self.random.choice(ability_whitelist)
                    )

                    species.abilities = new_abilities

        def randomize_types() -> None:
            if self.options.types == RandomizeTypes.option_shuffle:
                type_map = list(range(18))
                self.random.shuffle(type_map)

                # We never want to map to the ??? type, so swap whatever index maps to ??? with ???
                # So ??? will always map to itself, and there are no pokemon which have the ??? type
                mystery_type_index = type_map.index(9)
                type_map[mystery_type_index], type_map[9] = type_map[9], type_map[mystery_type_index]

                for species in self.modified_species:
                    if species is not None:
                        species.types = (type_map[species.types[0]], type_map[species.types[1]])
            elif self.options.types == RandomizeTypes.option_completely_random:
                for species in self.modified_species:
                    if species is not None:
                        new_type_1 = get_random_type(self.random)
                        new_type_2 = new_type_1
                        if species.types[0] != species.types[1]:
                            while new_type_1 == new_type_2:
                                new_type_2 = get_random_type(self.random)

                        species.types = (new_type_1, new_type_2)
            elif self.options.types == RandomizeTypes.option_follow_evolutions:
                already_modified: Set[int] = set()

                # Similar to follow evolutions for abilities, but only needs to loop through once.
                # For every pokemon without a pre-evolution, generates a random mapping from old types to new types
                # and then walks through the evolution tree applying that map. This means that evolutions that share
                # types will have those types mapped to the same new types, and evolutions with new or diverging types
                # will still have new or diverging types.
                # Consider:
                # - Charmeleon (Fire/Fire) -> Charizard (Fire/Flying)
                # - Onyx (Rock/Ground) -> Steelix (Steel/Ground)
                # - Nincada (Bug/Ground) -> Ninjask (Bug/Flying) && Shedinja (Bug/Ghost)
                # - Azurill (Normal/Normal) -> Marill (Water/Water)
                for species in self.modified_species:
                    if species is None:
                        continue
                    if species.species_id in already_modified:
                        continue
                    if species.pre_evolution is not None and species.pre_evolution not in already_modified:
                        continue

                    type_map = list(range(18))
                    self.random.shuffle(type_map)

                    # We never want to map to the ??? type, so swap whatever index maps to ??? with ???
                    # So ??? will always map to itself, and there are no pokemon which have the ??? type
                    mystery_type_index = type_map.index(9)
                    type_map[mystery_type_index], type_map[9] = type_map[9], type_map[mystery_type_index]

                    evolutions = [species]
                    while len(evolutions) > 0:
                        evolution = evolutions.pop()
                        evolution.types = (type_map[evolution.types[0]], type_map[evolution.types[1]])
                        already_modified.add(evolution.species_id)
                        evolutions += [self.modified_species[evo.species_id] for evo in evolution.evolutions]

        def randomize_learnsets() -> None:
            type_bias = self.options.move_match_type_bias.value
            normal_bias = self.options.move_normal_type_bias.value

            for species in self.modified_species:
                if species is None:
                    continue

                old_learnset = species.learnset
                new_learnset: List[LearnsetMove] = []

                i = 0
                # Replace filler MOVE_NONEs at start of list
                while old_learnset[i].move_id == 0:
                    if self.options.level_up_moves == LevelUpMoves.option_start_with_four_moves:
                        new_move = get_random_move(self.random, {move.move_id for move in new_learnset}, type_bias,
                                                   normal_bias, species.types)
                    else:
                        new_move = 0
                    new_learnset.append(LearnsetMove(old_learnset[i].level, new_move))
                    i += 1

                while i < len(old_learnset):
                    # Guarantees the starter has a good damaging move
                    if i == 3:
                        new_move = get_random_damaging_move(self.random, {move.move_id for move in new_learnset})
                    else:
                        new_move = get_random_move(self.random, {move.move_id for move in new_learnset}, type_bias,
                                                   normal_bias, species.types)
                    new_learnset.append(LearnsetMove(old_learnset[i].level, new_move))
                    i += 1

                species.learnset = new_learnset

        def randomize_tm_hm_compatibility() -> None:
            for species in self.modified_species:
                if species is None:
                    continue

                combatibility_array = int_to_bool_array(species.tm_hm_compatibility)

                # TMs
                for i in range(0, 50):
                    if self.options.tm_compatibility == TmCompatibility.option_fully_compatible:
                        combatibility_array[i] = True
                    elif self.options.tm_compatibility == TmCompatibility.option_completely_random:
                        combatibility_array[i] = self.random.choice([True, False])

                # HMs
                for i in range(50, 58):
                    if self.options.hm_compatibility == HmCompatibility.option_fully_compatible:
                        combatibility_array[i] = True
                    elif self.options.hm_compatibility == HmCompatibility.option_completely_random:
                        combatibility_array[i] = self.random.choice([True, False])

                species.tm_hm_compatibility = bool_array_to_int(combatibility_array)

        def randomize_tm_moves() -> None:
            new_moves: Set[int] = set()

            for i in range(50):
                new_move = get_random_move(self.random, new_moves)
                new_moves.add(new_move)
                self.modified_tmhm_moves[i] = new_move

        def randomize_wild_encounters() -> None:
            should_match_bst = self.options.wild_pokemon in {
                RandomizeWildPokemon.option_match_base_stats,
                RandomizeWildPokemon.option_match_base_stats_and_type
            }
            should_match_type = self.options.wild_pokemon in {
                RandomizeWildPokemon.option_match_type,
                RandomizeWildPokemon.option_match_base_stats_and_type
            }
            should_allow_legendaries = self.options.allow_wild_legendaries == Toggle.option_true

            for map_data in self.modified_maps:
                new_encounters: List[Optional[EncounterTableData]] = [None, None, None]
                old_encounters = [map_data.land_encounters, map_data.water_encounters, map_data.fishing_encounters]

                for i, table in enumerate(old_encounters):
                    if table is not None:
                        species_old_to_new_map: Dict[int, int] = {}
                        for species_id in table.slots:
                            if species_id not in species_old_to_new_map:
                                original_species = emerald_data.species[species_id]
                                target_bst = sum(original_species.base_stats) if should_match_bst else None
                                target_type = self.random.choice(original_species.types) if should_match_type else None

                                species_old_to_new_map[species_id] = get_random_species(
                                    self.random,
                                    self.modified_species,
                                    target_bst,
                                    target_type,
                                    should_allow_legendaries
                                ).species_id

                        new_slots: List[int] = []
                        for species_id in table.slots:
                            new_slots.append(species_old_to_new_map[species_id])

                        new_encounters[i] = EncounterTableData(new_slots, table.rom_address)

                map_data.land_encounters = new_encounters[0]
                map_data.water_encounters = new_encounters[1]
                map_data.fishing_encounters = new_encounters[2]

        def randomize_static_encounters() -> None:
            if self.options.static_encounters == RandomizeStaticEncounters.option_shuffle:
                shuffled_species = [encounter.species_id for encounter in emerald_data.static_encounters]
                self.random.shuffle(shuffled_species)

                self.modified_static_encounters = []
                for i, encounter in enumerate(emerald_data.static_encounters):
                    self.modified_static_encounters.append(StaticEncounterData(
                        shuffled_species[i],
                        encounter.rom_address
                    ))
            else:
                should_match_bst = self.options.static_encounters in {
                    RandomizeStaticEncounters.option_match_base_stats,
                    RandomizeStaticEncounters.option_match_base_stats_and_type
                }
                should_match_type = self.options.static_encounters in {
                    RandomizeStaticEncounters.option_match_type,
                    RandomizeStaticEncounters.option_match_base_stats_and_type
                }

                for encounter in emerald_data.static_encounters:
                    original_species = self.modified_species[encounter.species_id]
                    target_bst = sum(original_species.base_stats) if should_match_bst else None
                    target_type = self.random.choice(original_species.types) if should_match_type else None

                    self.modified_static_encounters.append(StaticEncounterData(
                        get_random_species(self.random, self.modified_species, target_bst, target_type).species_id,
                        encounter.rom_address
                    ))

        def randomize_opponent_parties() -> None:
            should_match_bst = self.options.trainer_parties in {
                RandomizeTrainerParties.option_match_base_stats,
                RandomizeTrainerParties.option_match_base_stats_and_type
            }
            should_match_type = self.options.trainer_parties in {
                RandomizeTrainerParties.option_match_type,
                RandomizeTrainerParties.option_match_base_stats_and_type
            }
            allow_legendaries = self.options.allow_trainer_legendaries == Toggle.option_true

            per_species_tmhm_moves: Dict[int, List[int]] = {}

            for trainer in self.modified_trainers:
                new_party = []
                for pokemon in trainer.party.pokemon:
                    original_species = emerald_data.species[pokemon.species_id]
                    target_bst = sum(original_species.base_stats) if should_match_bst else None
                    target_type = self.random.choice(original_species.types) if should_match_type else None

                    new_species = get_random_species(
                        self.random,
                        self.modified_species,
                        target_bst,
                        target_type,
                        allow_legendaries
                    )

                    if new_species.species_id not in per_species_tmhm_moves:
                        per_species_tmhm_moves[new_species.species_id] = list({
                            self.modified_tmhm_moves[i]
                            for i, is_compatible in enumerate(int_to_bool_array(new_species.tm_hm_compatibility))
                            if is_compatible
                        })

                    tm_hm_movepool = per_species_tmhm_moves[new_species.species_id]
                    level_up_movepool = list({
                        move.move_id
                        for move in new_species.learnset
                        if move.move_id != 0 and move.level <= pokemon.level
                    })

                    new_moves = (
                        self.random.choice(tm_hm_movepool if self.random.random() < 0.25 and len(tm_hm_movepool) > 0 else level_up_movepool),
                        self.random.choice(tm_hm_movepool if self.random.random() < 0.25 and len(tm_hm_movepool) > 0 else level_up_movepool),
                        self.random.choice(tm_hm_movepool if self.random.random() < 0.25 and len(tm_hm_movepool) > 0 else level_up_movepool),
                        self.random.choice(tm_hm_movepool if self.random.random() < 0.25 and len(tm_hm_movepool) > 0 else level_up_movepool)
                    )

                    new_party.append(TrainerPokemonData(new_species.species_id, pokemon.level, new_moves))

                trainer.party.pokemon = new_party

        def randomize_starters() -> None:
            match_bst = self.options.starters in {
                RandomizeStarters.option_match_base_stats,
                RandomizeStarters.option_match_base_stats_and_type
            }
            match_type = self.options.starters in {
                RandomizeStarters.option_match_type,
                RandomizeStarters.option_match_base_stats_and_type
            }
            allow_legendaries = self.options.allow_starter_legendaries == Toggle.option_true

            starter_bsts = (
                sum(emerald_data.species[emerald_data.starters[0]].base_stats) if match_bst else None,
                sum(emerald_data.species[emerald_data.starters[1]].base_stats) if match_bst else None,
                sum(emerald_data.species[emerald_data.starters[2]].base_stats) if match_bst else None
            )

            starter_types = (
                self.random.choice(emerald_data.species[emerald_data.starters[0]].types) if match_type else None,
                self.random.choice(emerald_data.species[emerald_data.starters[1]].types) if match_type else None,
                self.random.choice(emerald_data.species[emerald_data.starters[2]].types) if match_type else None
            )

            new_starters = (
                get_random_species(self.random, self.modified_species,
                                   starter_bsts[0], starter_types[0], allow_legendaries),
                get_random_species(self.random, self.modified_species,
                                   starter_bsts[1], starter_types[1], allow_legendaries),
                get_random_species(self.random, self.modified_species,
                                   starter_bsts[2], starter_types[2], allow_legendaries)
            )

            egg_code = self.options.easter_egg.value
            egg_check_1 = 0
            egg_check_2 = 0

            for i in egg_code:
                egg_check_1 += ord(i)
                egg_check_2 += egg_check_1 * egg_check_1

            egg = 96 + egg_check_2 - (egg_check_1 * 0x077C)
            if egg_check_2 == 0x14E03A and egg < 411 and egg > 0 and egg not in range(252, 277):
                self.modified_starters = (egg, egg, egg)
            else:
                self.modified_starters = (
                    new_starters[0].species_id,
                    new_starters[1].species_id,
                    new_starters[2].species_id
                )

            # Putting the unchosen starter onto the rival's team
            rival_teams: List[List[Tuple[str, int, bool]]] = [
                [
                    ("TRAINER_BRENDAN_ROUTE_103_TREECKO", 0, False),
                    ("TRAINER_BRENDAN_RUSTBORO_TREECKO",  1, False),
                    ("TRAINER_BRENDAN_ROUTE_110_TREECKO", 2, True ),
                    ("TRAINER_BRENDAN_ROUTE_119_TREECKO", 2, True ),
                    ("TRAINER_BRENDAN_LILYCOVE_TREECKO",  3, True ),
                    ("TRAINER_MAY_ROUTE_103_TREECKO",     0, False),
                    ("TRAINER_MAY_RUSTBORO_TREECKO",      1, False),
                    ("TRAINER_MAY_ROUTE_110_TREECKO",     2, True ),
                    ("TRAINER_MAY_ROUTE_119_TREECKO",     2, True ),
                    ("TRAINER_MAY_LILYCOVE_TREECKO",      3, True )
                ],
                [
                    ("TRAINER_BRENDAN_ROUTE_103_TORCHIC", 0, False),
                    ("TRAINER_BRENDAN_RUSTBORO_TORCHIC",  1, False),
                    ("TRAINER_BRENDAN_ROUTE_110_TORCHIC", 2, True ),
                    ("TRAINER_BRENDAN_ROUTE_119_TORCHIC", 2, True ),
                    ("TRAINER_BRENDAN_LILYCOVE_TORCHIC",  3, True ),
                    ("TRAINER_MAY_ROUTE_103_TORCHIC",     0, False),
                    ("TRAINER_MAY_RUSTBORO_TORCHIC",      1, False),
                    ("TRAINER_MAY_ROUTE_110_TORCHIC",     2, True ),
                    ("TRAINER_MAY_ROUTE_119_TORCHIC",     2, True ),
                    ("TRAINER_MAY_LILYCOVE_TORCHIC",      3, True )
                ],
                [
                    ("TRAINER_BRENDAN_ROUTE_103_MUDKIP", 0, False),
                    ("TRAINER_BRENDAN_RUSTBORO_MUDKIP",  1, False),
                    ("TRAINER_BRENDAN_ROUTE_110_MUDKIP", 2, True ),
                    ("TRAINER_BRENDAN_ROUTE_119_MUDKIP", 2, True ),
                    ("TRAINER_BRENDAN_LILYCOVE_MUDKIP",  3, True ),
                    ("TRAINER_MAY_ROUTE_103_MUDKIP",     0, False),
                    ("TRAINER_MAY_RUSTBORO_MUDKIP",      1, False),
                    ("TRAINER_MAY_ROUTE_110_MUDKIP",     2, True ),
                    ("TRAINER_MAY_ROUTE_119_MUDKIP",     2, True ),
                    ("TRAINER_MAY_LILYCOVE_MUDKIP",      3, True )
                ]
            ]

            for i, starter in enumerate([new_starters[1], new_starters[2], new_starters[0]]):
                potential_evolutions = [evolution.species_id for evolution in starter.evolutions]
                picked_evolution = starter.species_id
                if len(potential_evolutions) > 0:
                    picked_evolution = self.random.choice(potential_evolutions)

                for trainer_name, starter_position, is_evolved in rival_teams[i]:
                    trainer_data = self.modified_trainers[emerald_data.constants[trainer_name]]
                    trainer_data.party.pokemon[starter_position].species_id = picked_evolution if is_evolved else starter.species_id

        self.modified_species = copy.deepcopy(emerald_data.species)
        self.modified_trainers = copy.deepcopy(emerald_data.trainers)
        self.modified_maps = copy.deepcopy(emerald_data.maps)
        self.modified_tmhm_moves = copy.deepcopy(emerald_data.tmhm_moves)
        self.modified_static_encounters = copy.deepcopy(emerald_data.static_encounters)
        self.modified_starters = copy.deepcopy(emerald_data.starters)

        # Randomize species data
        if self.options.abilities != RandomizeAbilities.option_vanilla:
            randomize_abilities()

        if self.options.types != RandomizeTypes.option_vanilla:
            randomize_types()

        if self.options.level_up_moves != LevelUpMoves.option_vanilla:
            randomize_learnsets()

        randomize_tm_hm_compatibility()  # Options are checked within this function

        min_catch_rate = min(self.options.min_catch_rate.value, 255)
        for species in self.modified_species:
            if species is not None:
                species.catch_rate = max(species.catch_rate, min_catch_rate)

        if self.options.tm_moves:
            randomize_tm_moves()

        # Randomize wild encounters
        if self.options.wild_pokemon != RandomizeWildPokemon.option_vanilla:
            randomize_wild_encounters()

        # Randomize static encounters
        if self.options.static_encounters != RandomizeStaticEncounters.option_vanilla:
            randomize_static_encounters()

        # Randomize opponents
        if self.options.trainer_parties != RandomizeTrainerParties.option_vanilla:
            randomize_opponent_parties()

        # Randomize starters
        if self.options.starters != RandomizeStarters.option_vanilla:
            randomize_starters()

        generate_output(self, output_directory)

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = self.options.as_dict(
            "goal",
            "badges",
            "hms",
            "key_items",
            "bikes",
            "rods",
            "overworld_items",
            "hidden_items",
            "npc_gifts",
            "require_itemfinder",
            "require_flash",
            "enable_ferry",
            "elite_four_requirement",
            "elite_four_count",
            "norman_requirement",
            "norman_count",
            "extra_boulders",
            "remove_roadblocks",
            "free_fly_location",
            "fly_without_badge",
        )
        slot_data["free_fly_location_id"] = self.free_fly_location_id
        return slot_data

    def create_item(self, name: str) -> PokemonEmeraldItem:
        return self.create_item_by_code(self.item_name_to_id[name])

    def create_item_by_code(self, item_code: int) -> PokemonEmeraldItem:
        return PokemonEmeraldItem(
            self.item_id_to_name[item_code],
            get_item_classification(item_code),
            item_code,
            self.player
        )

    def create_event(self, name: str) -> PokemonEmeraldItem:
        return PokemonEmeraldItem(
            name,
            ItemClassification.progression,
            None,
            self.player
        )
