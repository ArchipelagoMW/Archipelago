"""
Archipelago World definition for Pokemon Emerald Version
"""
from collections import Counter
import copy
import logging
import os
import pkgutil
from typing import Any, Set, List, Dict, Optional, Tuple, ClassVar, TextIO, Union

from BaseClasses import CollectionState, ItemClassification, MultiWorld, Tutorial, LocationProgressType
from Fill import FillError, fill_restrictive
from Options import OptionError, Toggle
import settings
from worlds.AutoWorld import WebWorld, World

from .client import PokemonEmeraldClient  # Unused, but required to register with BizHawkClient
from .data import LEGENDARY_POKEMON, MapData, SpeciesData, TrainerData, LocationCategory, data as emerald_data
from .groups import ITEM_GROUPS, LOCATION_GROUPS
from .items import PokemonEmeraldItem, create_item_label_to_code_map, get_item_classification, offset_item_value
from .locations import (PokemonEmeraldLocation, create_location_label_to_id_map, create_locations_by_category,
                        set_free_fly, set_legendary_cave_entrances)
from .opponents import randomize_opponent_parties
from .options import (Goal, DarkCavesRequireFlash, HmRequirements, ItemPoolType, PokemonEmeraldOptions,
                      RandomizeWildPokemon, RandomizeBadges, RandomizeHms, NormanRequirement, OPTION_GROUPS)
from .pokemon import (get_random_move, get_species_id_by_label, randomize_abilities, randomize_learnsets,
                      randomize_legendary_encounters, randomize_misc_pokemon, randomize_starters,
                      randomize_tm_hm_compatibility,randomize_types, randomize_wild_encounters)
from .rom import PokemonEmeraldProcedurePatch, write_tokens 
from .util import get_encounter_type_label


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

    setup_es = Tutorial(
        "Guía de configuración para Multiworld",
        "Una guía para jugar Pokémon Emerald en Archipelago",
        "Español",
        "setup_es.md",
        "setup/es",
        ["nachocua"]
    )
    
    setup_sv = Tutorial(
        "Multivärld Installations Guide",
        "En guide för att kunna spela Pokémon Emerald med Archipelago.",
        "Svenska",
        "setup_sv.md",
        "setup/sv",
        ["Tsukino"]
    )

    tutorials = [setup_en, setup_es, setup_sv]
    option_groups = OPTION_GROUPS


class PokemonEmeraldSettings(settings.Group):
    class PokemonEmeraldRomFile(settings.UserFilePath):
        """File name of your English Pokemon Emerald ROM"""
        description = "Pokemon Emerald ROM File"
        copy_to = "Pokemon - Emerald Version (USA, Europe).gba"
        md5s = [PokemonEmeraldProcedurePatch.hash]

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

    required_client_version = (0, 4, 6)

    item_pool: List[PokemonEmeraldItem]
    badge_shuffle_info: Optional[List[Tuple[PokemonEmeraldLocation, PokemonEmeraldItem]]]
    hm_shuffle_info: Optional[List[Tuple[PokemonEmeraldLocation, PokemonEmeraldItem]]]
    free_fly_location_id: int
    blacklisted_moves: Set[int]
    blacklisted_wilds: Set[int]
    blacklisted_starters: Set[int]
    blacklisted_opponent_pokemon: Set[int]
    hm_requirements: Dict[str, Union[int, List[str]]]
    auth: bytes

    modified_species: Dict[int, SpeciesData]
    modified_maps: Dict[str, MapData]
    modified_tmhm_moves: List[int]
    modified_legendary_encounters: List[int]
    modified_starters: Tuple[int, int, int]
    modified_trainers: List[TrainerData]

    def __init__(self, multiworld, player):
        super(PokemonEmeraldWorld, self).__init__(multiworld, player)
        self.badge_shuffle_info = None
        self.hm_shuffle_info = None
        self.free_fly_location_id = 0
        self.blacklisted_moves = set()
        self.blacklisted_wilds = set()
        self.blacklisted_starters = set()
        self.blacklisted_opponent_pokemon = set()
        self.modified_maps = copy.deepcopy(emerald_data.maps)
        self.modified_species = copy.deepcopy(emerald_data.species)
        self.modified_tmhm_moves = []
        self.modified_starters = emerald_data.starters
        self.modified_trainers = []
        self.modified_legendary_encounters = []

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        from .sanity_check import validate_regions, validate_group_maps

        assert validate_regions()
        assert validate_group_maps()

    def get_filler_item_name(self) -> str:
        return "Great Ball"

    def generate_early(self) -> None:
        self.hm_requirements = {
            "HM01 Cut": ["Stone Badge"],
            "HM02 Fly": ["Feather Badge"],
            "HM03 Surf": ["Balance Badge"],
            "HM04 Strength": ["Heat Badge"],
            "HM05 Flash": ["Knuckle Badge"],
            "HM06 Rock Smash": ["Dynamo Badge"],
            "HM07 Waterfall": ["Rain Badge"],
            "HM08 Dive": ["Mind Badge"],
        }
        if self.options.hm_requirements == HmRequirements.option_fly_without_badge:
            self.hm_requirements["HM02 Fly"] = 0

        self.blacklisted_moves = {emerald_data.move_labels[label] for label in self.options.move_blacklist.value}

        self.blacklisted_wilds = {
            get_species_id_by_label(species_name)
            for species_name in self.options.wild_encounter_blacklist.value
            if species_name != "_Legendaries"
        }
        if "_Legendaries" in self.options.wild_encounter_blacklist.value:
            self.blacklisted_wilds |= LEGENDARY_POKEMON

        self.blacklisted_starters = {
            get_species_id_by_label(species_name)
            for species_name in self.options.starter_blacklist.value
            if species_name != "_Legendaries"
        }
        if "_Legendaries" in self.options.starter_blacklist.value:
            self.blacklisted_starters |= LEGENDARY_POKEMON

        self.blacklisted_opponent_pokemon = {
            get_species_id_by_label(species_name)
            for species_name in self.options.trainer_party_blacklist.value
            if species_name != "_Legendaries"
        }
        if "_Legendaries" in self.options.trainer_party_blacklist.value:
            self.blacklisted_opponent_pokemon |= LEGENDARY_POKEMON

        # In race mode we don't patch any item location information into the ROM
        if self.multiworld.is_race and not self.options.remote_items:
            logging.warning("Pokemon Emerald: Forcing player %s (%s) to use remote items due to race mode.",
                            self.player, self.player_name)
            self.options.remote_items.value = Toggle.option_true

        if self.options.goal == Goal.option_legendary_hunt:
            # Prevent turning off all legendary encounters
            if len(self.options.allowed_legendary_hunt_encounters.value) == 0:
                raise OptionError(f"Pokemon Emerald: Player {self.player} ({self.player_name}) needs to allow at "
                                   "least one legendary encounter when goal is legendary hunt.")

            # Prevent setting the number of required legendaries higher than the number of enabled legendaries
            if self.options.legendary_hunt_count.value > len(self.options.allowed_legendary_hunt_encounters.value):
                logging.warning("Pokemon Emerald: Legendary hunt count for player %s (%s) higher than number of allowed "
                                "legendary encounters. Reducing to number of allowed encounters.", self.player,
                                self.player_name)
                self.options.legendary_hunt_count.value = len(self.options.allowed_legendary_hunt_encounters.value)

        # Require random wild encounters if dexsanity is enabled
        if self.options.dexsanity and self.options.wild_pokemon == RandomizeWildPokemon.option_vanilla:
            raise OptionError(f"Pokemon Emerald: Player {self.player} ({self.player_name}) must not leave wild "
                               "encounters vanilla if enabling dexsanity.")

        # If badges or HMs are vanilla, Norman locks you from using Surf,
        # which means you're not guaranteed to be able to reach Fortree Gym,
        # Mossdeep Gym, or Sootopolis Gym. So we can't require reaching those
        # gyms to challenge Norman or it creates a circular dependency.
        #
        # This is never a problem for completely random badges/hms because the
        # algo will not place Surf/Balance Badge on Norman on its own. It's
        # never a problem for shuffled badges/hms because there is no scenario
        # where Cut or the Stone Badge can be a lynchpin for access to any gyms,
        # so they can always be put on Norman in a worst case scenario.
        #
        # This will also be a problem in warp rando if direct access to Norman's
        # room requires Surf or if access any gym leader in general requires
        # Surf. We will probably have to force this to 0 in that case.
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
            logging.warning("Pokemon Emerald: Norman requirements for player %s (%s) are unsafe in combination with "
                            "other settings. Reducing to 4.", self.player, self.player_name)
            self.options.norman_count.value = max_norman_count

        # Shuffled badges/hms will always be placed locally, so add them to local_items
        if self.options.badges == RandomizeBadges.option_shuffle:
            self.options.local_items.value.update(self.item_name_groups["Badge"])

        if self.options.hms == RandomizeHms.option_shuffle:
            self.options.local_items.value.update(self.item_name_groups["HM"])

    def create_regions(self) -> None:
        from .regions import create_regions
        all_regions = create_regions(self)

        # Categories with progression items always included
        categories = {
            LocationCategory.BADGE,
            LocationCategory.HM,
            LocationCategory.KEY,
            LocationCategory.ROD,
            LocationCategory.BIKE,
            LocationCategory.TICKET
        }
        if self.options.overworld_items:
            categories.add(LocationCategory.OVERWORLD_ITEM)
        if self.options.hidden_items:
            categories.add(LocationCategory.HIDDEN_ITEM)
        if self.options.npc_gifts:
            categories.add(LocationCategory.GIFT)
        if self.options.berry_trees:
            categories.add(LocationCategory.BERRY_TREE)
        if self.options.dexsanity:
            categories.add(LocationCategory.POKEDEX)
        if self.options.trainersanity:
            categories.add(LocationCategory.TRAINER)
        create_locations_by_category(self, all_regions, categories)

        self.multiworld.regions.extend(all_regions.values())

        # Exclude locations which are always locked behind the player's goal
        def exclude_locations(location_names: List[str]):
            for location_name in location_names:
                try:
                    self.multiworld.get_location(location_name,
                                                 self.player).progress_type = LocationProgressType.EXCLUDED
                except KeyError:
                    continue  # Location not in multiworld

        if self.options.goal == Goal.option_champion:
            # Always required to beat champion before receiving these
            exclude_locations([
                "Littleroot Town - S.S. Ticket from Norman",
                "Littleroot Town - Aurora Ticket from Norman",
                "Littleroot Town - Eon Ticket from Norman",
                "Littleroot Town - Mystic Ticket from Norman",
                "Littleroot Town - Old Sea Map from Norman",
                "Ever Grande City - Champion Wallace",
                "Meteor Falls 1F - Rival Steven",
                "Trick House Puzzle 8 - Item",
            ])

            # Construction workers don't move until champion is defeated
            if "Safari Zone Construction Workers" not in self.options.remove_roadblocks.value:
                exclude_locations([
                    "Safari Zone NE - Hidden Item North",
                    "Safari Zone NE - Hidden Item East",
                    "Safari Zone NE - Item on Ledge",
                    "Safari Zone SE - Hidden Item in South Grass 1",
                    "Safari Zone SE - Hidden Item in South Grass 2",
                    "Safari Zone SE - Item in Grass",
                ])

            # Sacred ash is on Navel Rock, which is locked behind the event tickets
            if not self.options.event_tickets:
                exclude_locations([
                    "Navel Rock Top - Hidden Item Sacred Ash",
                ])
        elif self.options.goal == Goal.option_steven:
            exclude_locations([
                "Meteor Falls 1F - Rival Steven",
            ])
        elif self.options.goal == Goal.option_norman:
            # If the player sets their options such that Surf or the Balance
            # Badge is vanilla, a very large number of locations become
            # "post-Norman". Similarly, access to the E4 may require you to
            # defeat Norman as an event or to get his badge, making postgame
            # locations inaccessible. Detecting these situations isn't trivial
            # and excluding all locations requiring Surf would be a bad idea.
            # So for now we just won't touch it and blame the user for
            # constructing their options in this way. Players usually expect
            # to only partially complete their world when playing this goal
            # anyway.

            # Locations which are directly unlocked by defeating Norman.
            exclude_locations([
                "Petalburg Gym - Leader Norman",
                "Petalburg Gym - Balance Badge",
                "Petalburg Gym - TM42 from Norman",
                "Petalburg City - HM03 from Wally's Uncle",
                "Dewford Town - TM36 from Sludge Bomb Man",
                "Mauville City - Basement Key from Wattson",
                "Mauville City - TM24 from Wattson",
            ])

    def create_items(self) -> None:
        item_locations: List[PokemonEmeraldLocation] = [
            location
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ]

        # Filter progression items which shouldn't be shuffled into the itempool.
        # Their locations will still exist, but event items will be placed and
        # locked at their vanilla locations instead.
        filter_categories = set()

        if not self.options.key_items:
            filter_categories.add(LocationCategory.KEY)
        if not self.options.rods:
            filter_categories.add(LocationCategory.ROD)
        if not self.options.bikes:
            filter_categories.add(LocationCategory.BIKE)
        if not self.options.event_tickets:
            filter_categories.add(LocationCategory.TICKET)

        if self.options.badges in {RandomizeBadges.option_vanilla, RandomizeBadges.option_shuffle}:
            filter_categories.add(LocationCategory.BADGE)
        if self.options.hms in {RandomizeHms.option_vanilla, RandomizeHms.option_shuffle}:
            filter_categories.add(LocationCategory.HM)

        # If Badges and HMs are set to the `shuffle` option, don't add them to
        # the normal item pool, but do create their items and save them and
        # their locations for use in `pre_fill` later.
        if self.options.badges == RandomizeBadges.option_shuffle:
            self.badge_shuffle_info = [
                (location, self.create_item_by_code(location.default_item_code))
                for location in [l for l in item_locations if emerald_data.locations[l.key].category == LocationCategory.BADGE]
            ]
        if self.options.hms == RandomizeHms.option_shuffle:
            self.hm_shuffle_info = [
                (location, self.create_item_by_code(location.default_item_code))
                for location in [l for l in item_locations if emerald_data.locations[l.key].category == LocationCategory.HM]
            ]

        # Filter down locations to actual items that will be filled and create
        # the itempool.
        item_locations = [location for location in item_locations if emerald_data.locations[location.key].category not in filter_categories]
        default_itempool = [self.create_item_by_code(location.default_item_code) for location in item_locations]

        if self.options.item_pool_type == ItemPoolType.option_shuffled:
            # Take the itempool as-is
            self.item_pool = default_itempool
        elif self.options.item_pool_type in (ItemPoolType.option_diverse, ItemPoolType.option_diverse_balanced):
            # Recreate the itempool from random items
            item_categories = ["Ball", "Healing", "Rare Candy", "Vitamin", "Evolution Stone",
                               "Money", "TM", "Held", "Misc", "Berry"]

            # Count occurrences of types of vanilla items in pool
            item_category_counter = Counter()
            for item in default_itempool:
                if not item.advancement:
                    item_category_counter.update([tag for tag in item.tags if tag in item_categories])

            self.item_pool = []
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
            refresh_tm_choices()

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

                self.item_pool.append(item)

        self.multiworld.itempool += self.item_pool

        set_free_fly(self)
        set_legendary_cave_entrances(self)

        # Key items which are considered in access rules but not randomized are converted to events and placed
        # in their vanilla locations so that the player can have them in their inventory for logic.
        def convert_unrandomized_items_to_events(category: LocationCategory) -> None:
            for location in self.multiworld.get_locations(self.player):
                assert isinstance(location, PokemonEmeraldLocation)
                if location.key is not None and emerald_data.locations[location.key].category == category:
                    location.place_locked_item(self.create_event(self.item_id_to_name[location.default_item_code]))
                    location.progress_type = LocationProgressType.DEFAULT
                    location.address = None

        if self.options.badges == RandomizeBadges.option_vanilla:
            convert_unrandomized_items_to_events(LocationCategory.BADGE)
        if self.options.hms == RandomizeHms.option_vanilla:
            convert_unrandomized_items_to_events(LocationCategory.HM)
        if not self.options.rods:
            convert_unrandomized_items_to_events(LocationCategory.ROD)
        if not self.options.bikes:
            convert_unrandomized_items_to_events(LocationCategory.BIKE)
        if not self.options.event_tickets:
            convert_unrandomized_items_to_events(LocationCategory.TICKET)
        if not self.options.key_items:
            convert_unrandomized_items_to_events(LocationCategory.KEY)

    def set_rules(self):
        from .rules import set_rules
        set_rules(self)

    def connect_entrances(self):
        randomize_wild_encounters(self)
        self.shuffle_badges_hms()
        # For entrance randomization, disconnect entrances here, randomize map, then
        # undo badge/HM placement and re-shuffle them in the new map.

    def shuffle_badges_hms(self) -> None:
        my_progression_items = [item for item in self.item_pool if item.advancement]
        my_locations = list(self.get_locations())

        if self.options.badges == RandomizeBadges.option_shuffle:
            badge_locations: List[PokemonEmeraldLocation]
            badge_items: List[PokemonEmeraldItem]

            # Sort order makes `fill_restrictive` try to place important badges later, which
            # makes it less likely to have to swap at all, and more likely for swaps to work.
            badge_locations, badge_items = [list(l) for l in zip(*self.badge_shuffle_info)]
            badge_priority = {
                "Knuckle Badge": 3,
                "Balance Badge": 1,
                "Dynamo Badge": 1,
                "Mind Badge": 2,
                "Heat Badge": 2,
                "Rain Badge": 3,
                "Stone Badge": 4,
                "Feather Badge": 5,
            }
            # In the case of vanilla HMs, navigating Granite Cave is required to access more than 2 gyms,
            # so Knuckle Badge deserves highest priority if Flash is logically required.
            if self.options.hms == RandomizeHms.option_vanilla and \
                    self.options.require_flash in (DarkCavesRequireFlash.option_both, DarkCavesRequireFlash.option_only_granite_cave):
                badge_priority["Knuckle Badge"] = 0
            badge_items.sort(key=lambda item: badge_priority.get(item.name, 0))

            # Build state
            state = CollectionState(self.multiworld)
            for item in my_progression_items:
                state.collect(item, True)
            # If HM shuffle is on, HMs are neither placed in locations nor in
            # the item pool, so we also need to collect them.
            if self.hm_shuffle_info is not None:
                for _, item in self.hm_shuffle_info:
                    state.collect(item, True)
            state.sweep_for_advancements(my_locations)

            # Shuffle badges
            self.fill_subset_with_retries(badge_items, badge_locations, state)

        if self.options.hms == RandomizeHms.option_shuffle:
            hm_locations: List[PokemonEmeraldLocation]
            hm_items: List[PokemonEmeraldItem]

            # Sort order makes `fill_restrictive` try to place important HMs later, which
            # makes it less likely to have to swap at all, and more likely for swaps to work.
            hm_locations, hm_items = [list(l) for l in zip(*self.hm_shuffle_info)]
            hm_priority = {
                "HM05 Flash": 3,
                "HM03 Surf": 1,
                "HM06 Rock Smash": 1,
                "HM08 Dive": 2,
                "HM04 Strength": 2,
                "HM07 Waterfall": 3,
                "HM01 Cut": 4,
                "HM02 Fly": 5,
            }
            # In the case of vanilla badges, navigating Granite Cave is required to access more than 2 gyms,
            # so Flash deserves highest priority if it's logically required.
            if self.options.badges == RandomizeBadges.option_vanilla and \
                    self.options.require_flash in (DarkCavesRequireFlash.option_both, DarkCavesRequireFlash.option_only_granite_cave):
                hm_priority["HM05 Flash"] = 0
            hm_items.sort(key=lambda item: hm_priority.get(item.name, 0), reverse=True)

            # Build state
            # Badges are either in the item pool, or already placed and collected during sweep
            state = CollectionState(self.multiworld)
            for item in my_progression_items:
                state.collect(item, True)
            state.sweep_for_advancements(my_locations)

            # Shuffle HMs
            self.fill_subset_with_retries(hm_items, hm_locations, state)

    def fill_subset_with_retries(self, items: list[PokemonEmeraldItem], locations: list[PokemonEmeraldLocation], state: CollectionState):
        # Un-exclude locations, since we need to put progression items on them
        for location in locations:
            location.progress_type = LocationProgressType.DEFAULT \
                if location.progress_type == LocationProgressType.EXCLUDED \
                else location.progress_type

        # In specific very constrained conditions, `fill_restrictive` may run
        # out of swaps before it finds a valid solution if it gets unlucky.
        attempts_remaining = 2
        while attempts_remaining > 0:
            attempts_remaining -= 1
            locations_copy = locations.copy()
            items_copy = items.copy()
            self.random.shuffle(locations_copy)
            try:
                fill_restrictive(self.multiworld, state, locations_copy, items_copy, single_player_placement=True,
                                 lock=True)
                break
            except FillError as exc:
                if attempts_remaining <= 0:
                    raise exc

                # Undo partial item placement
                for location in locations:
                    location.locked = False
                    if location.item is not None:
                        location.item.location = None
                        location.item = None

                logging.debug(f"Failed to shuffle items for player {self.player} ({self.player_name}). Retrying.")
                continue

    def generate_basic(self) -> None:
        # Create auth
        self.auth = self.random.randbytes(16)

        randomize_types(self)

    def generate_output(self, output_directory: str) -> None:
        self.modified_trainers = copy.deepcopy(emerald_data.trainers)
        self.modified_tmhm_moves = copy.deepcopy(emerald_data.tmhm_moves)
        self.modified_legendary_encounters = copy.deepcopy(emerald_data.legendary_encounters)
        self.modified_misc_pokemon = copy.deepcopy(emerald_data.misc_pokemon)
        self.modified_starters = copy.deepcopy(emerald_data.starters)

        # Modify catch rate
        min_catch_rate = min(self.options.min_catch_rate.value, 255)
        for species in self.modified_species.values():
            species.catch_rate = max(species.catch_rate, min_catch_rate)

        # Modify TM moves
        if self.options.tm_tutor_moves:
            new_moves: Set[int] = set()

            for i in range(50):
                new_move = get_random_move(self.random, new_moves | self.blacklisted_moves)
                new_moves.add(new_move)
                self.modified_tmhm_moves[i] = new_move

        randomize_abilities(self)
        randomize_learnsets(self)
        randomize_tm_hm_compatibility(self)
        randomize_legendary_encounters(self)
        randomize_misc_pokemon(self)
        randomize_opponent_parties(self)
        randomize_starters(self)

        patch = PokemonEmeraldProcedurePatch(player=self.player, player_name=self.player_name)
        patch.write_file("base_patch.bsdiff4", pkgutil.get_data(__name__, "data/base_patch.bsdiff4"))
        write_tokens(self, patch)

        del self.modified_trainers
        del self.modified_tmhm_moves
        del self.modified_legendary_encounters
        del self.modified_misc_pokemon
        del self.modified_starters
        del self.modified_species

        # Write Output
        out_file_name = self.multiworld.get_out_file_name_base(self.player)
        patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))

    def write_spoiler(self, spoiler_handle: TextIO):
        if self.options.dexsanity:
            from collections import defaultdict

            spoiler_handle.write(f"\n\nWild Pokemon ({self.player_name}):\n\n")

            species_maps = defaultdict(set)
            for map_data in self.modified_maps.values():
                for encounter_type, encounter_data in map_data.encounters.items():
                    for i, encounter in enumerate(encounter_data.slots):
                        species_maps[encounter].add(f"{map_data.label} ({get_encounter_type_label(encounter_type, i)})")

            lines = [f"{emerald_data.species[species].label}: {', '.join(sorted(maps))}\n"
                     for species, maps in species_maps.items()]
            lines.sort()
            for line in lines:
                spoiler_handle.write(line)

        del self.modified_maps

    def extend_hint_information(self, hint_data):
        if self.options.dexsanity:
            from collections import defaultdict

            species_maps = defaultdict(set)
            for map_data in self.modified_maps.values():
                for encounter_type, encounter_data in map_data.encounters.items():
                    for i, encounter in enumerate(encounter_data.slots):
                        species_maps[encounter].add(f"{map_data.label} ({get_encounter_type_label(encounter_type, i)})")

            hint_data[self.player] = {
                self.location_name_to_id[f"Pokedex - {emerald_data.species[species].label}"]: ", ".join(sorted(maps))
                for species, maps in species_maps.items()
            }

    def modify_multidata(self, multidata: Dict[str, Any]):
        import base64
        multidata["connect_names"][base64.b64encode(self.auth).decode("ascii")] = multidata["connect_names"][self.player_name]

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = self.options.as_dict(
            "goal",
            "badges",
            "hms",
            "key_items",
            "bikes",
            "event_tickets",
            "rods",
            "overworld_items",
            "hidden_items",
            "npc_gifts",
            "berry_trees",
            "require_itemfinder",
            "require_flash",
            "elite_four_requirement",
            "elite_four_count",
            "norman_requirement",
            "norman_count",
            "legendary_hunt_catch",
            "legendary_hunt_count",
            "extra_boulders",
            "remove_roadblocks",
            "allowed_legendary_hunt_encounters",
            "extra_bumpy_slope",
            "free_fly_location",
            "remote_items",
            "dexsanity",
            "trainersanity",
            "modify_118",
            "death_link",
            "normalize_encounter_rates",
        )
        slot_data["free_fly_location_id"] = self.free_fly_location_id
        slot_data["hm_requirements"] = self.hm_requirements
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
