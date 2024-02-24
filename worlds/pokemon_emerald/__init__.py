"""
Archipelago World definition for Pokemon Emerald Version
"""
from collections import Counter
import copy
import logging
import os
from typing import Any, Set, List, Dict, Optional, Tuple, ClassVar, TextIO, Union

from BaseClasses import ItemClassification, MultiWorld, Tutorial, LocationProgressType
from Fill import FillError, fill_restrictive
from Options import Toggle
import settings
from worlds.AutoWorld import WebWorld, World

from .client import PokemonEmeraldClient  # Unused, but required to register with BizHawkClient
from .data import (SpeciesData, MapData, EncounterTableData, LearnsetMove, TrainerPokemonData, MiscPokemonData,
                   TrainerData, POSTGAME_MAPS, NUM_REAL_SPECIES, data as emerald_data)
from .items import (ITEM_GROUPS, PokemonEmeraldItem, create_item_label_to_code_map, get_item_classification,
                    offset_item_value)
from .locations import (LOCATION_GROUPS, PokemonEmeraldLocation, create_location_label_to_id_map,
                        create_locations_with_tags)
from .options import (Goal, ItemPoolType, RandomizeWildPokemon, RandomizeBadges, RandomizeTrainerParties, RandomizeHms,
                      RandomizeStarters, LevelUpMoves, RandomizeAbilities, RandomizeTypes, TmCompatibility,
                      HmCompatibility, RandomizeLegendaryEncounters, NormanRequirement,
                      PokemonEmeraldOptions, HmRequirements, RandomizeMiscPokemon, DarkCavesRequireFlash)
from .pokemon import (LEGENDARY_POKEMON, UNEVOLVED_POKEMON, get_random_move,
                      get_random_damaging_move, get_random_type, get_species_id_by_label)
from .rom import PokemonEmeraldDeltaPatch, generate_output, location_visited_event_to_id_map
from .util import int_to_bool_array, bool_array_to_int, get_easter_egg


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

    data_version = 2
    required_client_version = (0, 4, 3)

    badge_shuffle_info: Optional[List[Tuple[PokemonEmeraldLocation, PokemonEmeraldItem]]]
    hm_shuffle_info: Optional[List[Tuple[PokemonEmeraldLocation, PokemonEmeraldItem]]]
    free_fly_location_id: int
    blacklisted_moves: Set[int]
    blacklisted_wilds: Set[int]
    blacklisted_starters: Set[int]
    blacklisted_opponent_pokemon: Set[int]
    hm_requirements: Dict[str, Union[int, List[str]]]
    auth: bytes

    modified_species: List[Optional[SpeciesData]]
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
        from .sanity_check import validate_regions

        if not os.path.exists(cls.settings.rom_file):
            raise FileNotFoundError(cls.settings.rom_file)

        assert validate_regions()

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
            "HM08 Dive": ["Mind Badge"]
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
        if "_Legendaries" in self.options.starter_blacklist.value:
            self.blacklisted_opponent_pokemon |= LEGENDARY_POKEMON

        # In race mode we don't patch any item location information into the ROM
        if self.multiworld.is_race and not self.options.remote_items:
            logging.warning("Pokemon Emerald: Forcing Player %s (%s) to use remote items due to race mode.",
                            self.player, self.multiworld.player_name[self.player])
            self.options.remote_items.value = Toggle.option_true

        if self.options.goal == Goal.option_legendary_hunt:
            # Prevent turning off all legendary encounters
            if len(self.options.allowed_legendary_hunt_encounters.value) == 0:
                raise ValueError(f"Pokemon Emerald: Player {self.player} ({self.multiworld.player_name[self.player]}) "
                                 "needs to allow at least one legendary encounter when goal is legendary hunt.")

            # Prevent setting the number of required legendaries higher than the number of enabled legendaries
            if self.options.legendary_hunt_count.value > len(self.options.allowed_legendary_hunt_encounters.value):
                logging.warning("Pokemon Emerald: Legendary hunt count for Player %s (%s) higher than number of allowed "
                                "legendary encounters. Reducing to number of allowed encounters.", self.player,
                                self.multiworld.player_name[self.player])
                self.options.legendary_hunt_count.value = len(self.options.allowed_legendary_hunt_encounters.value)

        # Require random wild encounters if dexsanity is enabled
        if self.options.dexsanity and self.options.wild_pokemon == RandomizeWildPokemon.option_vanilla:
            raise ValueError(f"Pokemon Emerald: Player {self.player} ({self.multiworld.player_name[self.player]}) must "
                             "not leave wild encounters vanilla if enabling dexsanity.")

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
            logging.warning("Pokemon Emerald: Norman requirements for Player %s (%s) are unsafe in combination with "
                            "other settings. Reducing to 4.", self.player, self.multiworld.get_player_name(self.player))
            self.options.norman_count.value = max_norman_count

    def create_regions(self) -> None:
        from .regions import create_regions
        regions = create_regions(self)

        tags = {"Badge", "HM", "KeyItem", "Rod", "Bike"}  # Tags with progression items always included
        if self.options.overworld_items:
            tags.add("OverworldItem")
        if self.options.hidden_items:
            tags.add("HiddenItem")
        if self.options.npc_gifts:
            tags.add("NpcGift")
        if self.options.berry_trees:
            tags.add("BerryTree")
        if self.options.dexsanity:
            tags.add("Pokedex")
        if self.options.trainersanity:
            tags.add("Trainer")
        create_locations_with_tags(self, regions, tags)

        self.multiworld.regions.extend(regions.values())

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
                "Trick House Puzzle 8 - Item"
            ])

            # Construction workers don't move until champion is defeated
            if "Safari Zone Construction Workers" not in self.options.remove_roadblocks.value:
                exclude_locations([
                    "Safari Zone NE - Hidden Item North",
                    "Safari Zone NE - Hidden Item East",
                    "Safari Zone NE - Item on Ledge",
                    "Safari Zone SE - Hidden Item in South Grass 1",
                    "Safari Zone SE - Hidden Item in South Grass 2",
                    "Safari Zone SE - Item in Grass"
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
                "Petalburg Gym - Balance Badge",
                "Petalburg Gym - TM42 from Norman",
                "Petalburg City - HM03 from Wally's Uncle",
                "Dewford Town - TM36 from Sludge Bomb Man",
                "Mauville City - Basement Key from Wattson",
                "Mauville City - TM24 from Wattson"
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

        # If Badges and HMs are set to the `shuffle` option, don't add them to
        # the normal item pool, but do create their items and save them and
        # their locations for use in `pre_fill` later.
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

        # Filter down locations to actual items that will be filled and create
        # the itempool.
        item_locations = [location for location in item_locations if len(filter_tags & location.tags) == 0]
        default_itempool = [self.create_item_by_code(location.default_item_code) for location in item_locations]

        # Take the itempool as-is
        if self.options.item_pool_type == ItemPoolType.option_shuffled:
            self.multiworld.itempool += default_itempool

        # Recreate the itempool from random items
        elif self.options.item_pool_type in (ItemPoolType.option_diverse, ItemPoolType.option_diverse_balanced):
            item_categories = ["Ball", "Heal", "Candy", "Vitamin", "EvoStone", "Money", "TM", "Held", "Misc", "Berry"]

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

                self.multiworld.itempool.append(item)

    def set_rules(self) -> None:
        from .rules import set_rules
        set_rules(self)

    def generate_basic(self) -> None:
        # Create auth
        self.auth = self.random.randbytes(16)

        # Randomize types
        if self.options.types == RandomizeTypes.option_shuffle:
            type_map = list(range(18))
            self.random.shuffle(type_map)

            # We never want to map to the ??? type, so swap whatever index maps to ??? with ???
            # which forces ??? to always map to itself. There are no pokemon which have the ??? type
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
                # which forces ??? to always map to itself. There are no pokemon which have the ??? type
                mystery_type_index = type_map.index(9)
                type_map[mystery_type_index], type_map[9] = type_map[9], type_map[mystery_type_index]

                evolutions = [species]
                while len(evolutions) > 0:
                    evolution = evolutions.pop()
                    evolution.types = (type_map[evolution.types[0]], type_map[evolution.types[1]])
                    already_modified.add(evolution.species_id)
                    evolutions += [self.modified_species[evo.species_id] for evo in evolution.evolutions]

        # Randomize wild encounters
        if self.options.wild_pokemon != RandomizeWildPokemon.option_vanilla:
            from collections import defaultdict

            should_match_bst = self.options.wild_pokemon in {
                RandomizeWildPokemon.option_match_base_stats,
                RandomizeWildPokemon.option_match_base_stats_and_type
            }
            should_match_type = self.options.wild_pokemon in {
                RandomizeWildPokemon.option_match_type,
                RandomizeWildPokemon.option_match_base_stats_and_type
            }
            catch_em_all = self.options.dexsanity == Toggle.option_true

            catch_em_all_placed = set()

            priority_species = [emerald_data.constants["SPECIES_WAILORD"], emerald_data.constants["SPECIES_RELICANTH"]]

            # Loop over map data to modify their encounter slots
            map_names = list(self.modified_maps.keys())
            self.random.shuffle(map_names)
            for map_name in map_names:
                placed_priority_species = False
                map_data = self.modified_maps[map_name]

                new_encounters: List[Optional[EncounterTableData]] = [None, None, None]
                old_encounters = [map_data.land_encounters, map_data.water_encounters, map_data.fishing_encounters]

                for i, table in enumerate(old_encounters):
                    if table is not None:
                        # Create a map from the original species to new species
                        # instead of just randomizing every slot.
                        # Force area 1-to-1 mapping, in other words.
                        species_old_to_new_map: Dict[int, int] = {}
                        for species_id in table.slots:
                            if species_id not in species_old_to_new_map:
                                if not placed_priority_species and len(priority_species) > 0:
                                    new_species_id = priority_species.pop()
                                    placed_priority_species = True
                                else:
                                    original_species = emerald_data.species[species_id]

                                    # Construct progressive tiers of blacklists that can be peeled back if they
                                    # collectively cover too much of the pokedex. A lower index in `blacklists`
                                    # indicates a more important set of species to avoid. Entries at `0` will
                                    # always be blacklisted.
                                    blacklists: Dict[int, List[Set[int]]] = defaultdict(list)

                                    # Blacklist pokemon already on this table
                                    blacklists[0].append(set(species_old_to_new_map.values()))

                                    # If doing legendary hunt, blacklist Latios from wild encounters so
                                    # it can be tracked as the roamer. Otherwise it may be impossible
                                    # to tell whether a highlighted route is the roamer or a wild
                                    # encounter.
                                    if self.options.goal == Goal.option_legendary_hunt:
                                        blacklists[0].append({emerald_data.constants["SPECIES_LATIOS"]})

                                    # If dexsanity/catch 'em all mode, blacklist already placed species
                                    # until every species has been placed once
                                    if catch_em_all and len(catch_em_all_placed) < NUM_REAL_SPECIES:
                                        blacklists[1].append(catch_em_all_placed)

                                    # Blacklist from player options
                                    blacklists[2].append(self.blacklisted_wilds)

                                    # Type matching blacklist
                                    if should_match_type:
                                        blacklists[3].append({
                                            species.species_id
                                            for species in self.modified_species
                                            if species is not None and not bool(set(species.types) & set(original_species.types))
                                        })

                                    merged_blacklist: Set[int] = set()
                                    for max_priority in reversed(sorted(blacklists.keys())):
                                        merged_blacklist = set()
                                        for priority in blacklists.keys():
                                            if priority <= max_priority:
                                                for blacklist in blacklists[priority]:
                                                    merged_blacklist |= blacklist

                                        if len(merged_blacklist) < NUM_REAL_SPECIES:
                                            break
                                    else:
                                        raise RuntimeError("This should never happen")

                                    candidates = [
                                        species
                                        for species in self.modified_species
                                        if species is not None and species.species_id not in merged_blacklist
                                    ]

                                    if should_match_bst:
                                        candidates = self.filter_species_by_nearby_bst(candidates,
                                                                                       sum(original_species.base_stats))

                                    new_species_id = self.random.choice(candidates).species_id
                                species_old_to_new_map[species_id] = new_species_id

                                if catch_em_all and map_data.name not in POSTGAME_MAPS:
                                    catch_em_all_placed.add(new_species_id)

                        # Actually create the new list of slots and encounter table
                        new_slots: List[int] = []
                        for species_id in table.slots:
                            new_slots.append(species_old_to_new_map[species_id])

                        new_encounters[i] = EncounterTableData(new_slots, table.address)

                        # Rename event items for the new wild pokemon species
                        slot_category: Tuple[str, List[Tuple[Optional[str], range]]] = [
                            ("LAND", [(None, range(0, 12))]),
                            ("WATER", [(None, range(0, 5))]),
                            ("FISHING", [("OLD_ROD", range(0, 2)), ("GOOD_ROD", range(2, 5)), ("SUPER_ROD", range(5, 10))])
                        ][i]
                        for j, new_species_id in enumerate(new_slots):
                            # Get the subcategory for rods
                            subcategory = next(sc for sc in slot_category[1] if j in sc[1])
                            subcategory_species = []
                            for k in subcategory[1]:
                                if new_slots[k] not in subcategory_species:
                                    subcategory_species.append(new_slots[k])

                            # Create the name of the location that corresponds to this encounter slot
                            # Fishing locations include the rod name
                            subcategory_str = "" if subcategory[0] is None else "_" + subcategory[0]
                            encounter_location_index = subcategory_species.index(new_species_id) + 1
                            encounter_location_name = f"{map_data.name}_{slot_category[0]}_ENCOUNTERS{subcategory_str}_{encounter_location_index}"
                            try:
                                # Get the corresponding location and change the event name to reflect the new species
                                slot_location = self.multiworld.get_location(encounter_location_name, self.player)
                                slot_location.item.name = f"CATCH_{emerald_data.species[new_species_id].name}"
                            except KeyError:
                                pass  # Map probably isn't included; should be careful here about bad encounter location names

                map_data.land_encounters = new_encounters[0]
                map_data.water_encounters = new_encounters[1]
                map_data.fishing_encounters = new_encounters[2]

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

        # Set Marine Cave and Terra Cave entrances
        terra_cave_location_name = self.random.choice([
            "TERRA_CAVE_ROUTE_114_1",
            "TERRA_CAVE_ROUTE_114_2",
            "TERRA_CAVE_ROUTE_115_1",
            "TERRA_CAVE_ROUTE_115_2",
            "TERRA_CAVE_ROUTE_116_1",
            "TERRA_CAVE_ROUTE_116_2",
            "TERRA_CAVE_ROUTE_118_1",
            "TERRA_CAVE_ROUTE_118_2"
        ])

        terra_cave_location_location = self.multiworld.get_location("TERRA_CAVE_LOCATION", self.player)
        terra_cave_location_location.item = None
        terra_cave_location_location.place_locked_item(self.create_event(terra_cave_location_name))
        
        marine_cave_location_name = self.random.choice([
            "MARINE_CAVE_ROUTE_105_1",
            "MARINE_CAVE_ROUTE_105_2",
            "MARINE_CAVE_ROUTE_125_1",
            "MARINE_CAVE_ROUTE_125_2",
            "MARINE_CAVE_ROUTE_127_1",
            "MARINE_CAVE_ROUTE_127_2",
            "MARINE_CAVE_ROUTE_129_1",
            "MARINE_CAVE_ROUTE_129_2"
        ])

        marine_cave_location_location = self.multiworld.get_location("MARINE_CAVE_LOCATION", self.player)
        marine_cave_location_location.item = None
        marine_cave_location_location.place_locked_item(self.create_event(marine_cave_location_name))

        # Key items which are considered in access rules but not randomized are converted to events and placed
        # in their vanilla locations so that the player can have them in their inventory for logic.
        def convert_unrandomized_items_to_events(tag: str) -> None:
            for location in self.multiworld.get_locations(self.player):
                if location.tags is not None and tag in location.tags:
                    location.place_locked_item(self.create_event(self.item_id_to_name[location.default_item_code]))
                    location.progress_type = LocationProgressType.DEFAULT
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
        # Badges and HMs that are set to shuffle need to be placed at
        # their own subset of locations
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
                "Feather Badge": 5
            }
            # In the case of vanilla HMs, navigating Granite Cave is required to access more than 2 gyms,
            # so Knuckle Badge deserves highest priority if Flash is logically required.
            if self.options.hms == RandomizeHms.option_vanilla and \
                    self.options.require_flash in (DarkCavesRequireFlash.option_both, DarkCavesRequireFlash.option_only_granite_cave):
                badge_priority["Knuckle Badge"] = 0
            badge_items.sort(key=lambda item: badge_priority.get(item.name, 0))

            # Un-exclude badge locations, since we need to put progression items on them
            for location in badge_locations:
                location.progress_type = LocationProgressType.DEFAULT \
                    if location.progress_type == LocationProgressType.EXCLUDED \
                    else location.progress_type

            collection_state = self.multiworld.get_all_state(False)

            # If HM shuffle is on, HMs are not placed and not in the pool, so
            # `get_all_state` did not contain them. Collect them manually for
            # this fill. We know that they will be included in all state after
            # this stage.
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

        # Badges are guaranteed to be either placed or in the multiworld's itempool now
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
                "HM02 Fly": 5
            }
            # In the case of vanilla badges, navigating Granite Cave is required to access more than 2 gyms,
            # so Flash deserves highest priority if it's logically required.
            if self.options.badges == RandomizeBadges.option_vanilla and \
                    self.options.require_flash in (DarkCavesRequireFlash.option_both, DarkCavesRequireFlash.option_only_granite_cave):
                hm_priority["HM05 Flash"] = 0
            hm_items.sort(key=lambda item: hm_priority.get(item.name, 0))

            # Un-exclude HM locations, since we need to put progression items on them
            for location in hm_locations:
                location.progress_type = LocationProgressType.DEFAULT \
                    if location.progress_type == LocationProgressType.EXCLUDED \
                    else location.progress_type

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

            ability_blacklist_labels = {"cacophony"}  # Cacophony is defined and has a description, but no effect
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
                #
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
                        # 0 is the value for "no ability"; species with only 1 ability have the other set to 0
                        new_abilities = (
                            0 if old_abilities[0] == 0 else self.random.choice(ability_whitelist),
                            0 if old_abilities[1] == 0 else self.random.choice(ability_whitelist)
                        )

                        # Recursively modify the abilities of anything that evolves from this pokemon
                        # until the evolution doesn't have a matching set of abilities
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
                    # 0 is the value for "no ability"; species with only 1 ability have the other set to 0
                    new_abilities = (
                        0 if old_abilities[0] == 0 else self.random.choice(ability_whitelist),
                        0 if old_abilities[1] == 0 else self.random.choice(ability_whitelist)
                    )

                    species.abilities = new_abilities

        def randomize_learnsets() -> None:
            type_bias = self.options.move_match_type_bias.value
            normal_bias = self.options.move_normal_type_bias.value

            for species in self.modified_species:
                if species is None:
                    continue

                old_learnset = species.learnset
                new_learnset: List[LearnsetMove] = []

                # All species have 4 moves at level 0. Up to 3 of them are blank spaces reserved for the
                # start with four moves option. This either replaces those moves or leaves it blank
                # and moves the cursor.
                i = 0
                while old_learnset[i].move_id == 0:
                    if self.options.level_up_moves == LevelUpMoves.option_start_with_four_moves:
                        new_move = get_random_move(self.random,
                                                   {move.move_id for move in new_learnset} | self.blacklisted_moves,
                                                   type_bias, normal_bias, species.types)
                    else:
                        new_move = 0
                    new_learnset.append(LearnsetMove(old_learnset[i].level, new_move))
                    i += 1

                # All moves from here onward are actual moves.
                while i < len(old_learnset):
                    # Guarantees the starter has a good damaging move; i will always be <=3 when entering this loop
                    if i == 3:
                        new_move = get_random_damaging_move(self.random, {move.move_id for move in new_learnset})
                    else:
                        new_move = get_random_move(self.random,
                                                   {move.move_id for move in new_learnset} | self.blacklisted_moves,
                                                   type_bias, normal_bias, species.types)
                    new_learnset.append(LearnsetMove(old_learnset[i].level, new_move))
                    i += 1

                species.learnset = new_learnset

        def randomize_tm_hm_compatibility() -> None:
            for species in self.modified_species:
                if species is None:
                    continue

                # TM and HM compatibility is stored as a 64-bit bitfield
                combatibility_array = int_to_bool_array(species.tm_hm_compatibility)

                # TMs
                if self.options.tm_compatibility != TmCompatibility.special_range_names["vanilla"]:
                    for i in range(0, 50):
                        combatibility_array[i] = self.random.random() < self.options.tm_compatibility / 100

                # HMs
                if self.options.hm_compatibility != HmCompatibility.special_range_names["vanilla"]:
                    for i in range(50, 58):
                        combatibility_array[i] = self.random.random() < self.options.hm_compatibility / 100

                species.tm_hm_compatibility = bool_array_to_int(combatibility_array)

        def randomize_tm_moves() -> None:
            new_moves: Set[int] = set()

            for i in range(50):
                new_move = get_random_move(self.random, new_moves | self.blacklisted_moves)
                new_moves.add(new_move)
                self.modified_tmhm_moves[i] = new_move

        def randomize_legendary_encounters() -> None:
            if self.options.legendary_encounters == RandomizeLegendaryEncounters.option_shuffle:
                # Just take the existing species and shuffle them
                shuffled_species = [encounter.species_id for encounter in emerald_data.legendary_encounters]
                self.random.shuffle(shuffled_species)

                for i, encounter in enumerate(emerald_data.legendary_encounters):
                    self.modified_legendary_encounters.append(MiscPokemonData(
                        shuffled_species[i],
                        encounter.address
                    ))

            else:
                should_match_bst = self.options.legendary_encounters in {
                    RandomizeLegendaryEncounters.option_match_base_stats,
                    RandomizeLegendaryEncounters.option_match_base_stats_and_type
                }
                should_match_type = self.options.legendary_encounters in {
                    RandomizeLegendaryEncounters.option_match_type,
                    RandomizeLegendaryEncounters.option_match_base_stats_and_type
                }

                for encounter in emerald_data.legendary_encounters:
                    original_species = self.modified_species[encounter.species_id]

                    candidates = [species for species in self.modified_species if species is not None]
                    if should_match_type:
                        candidates = [
                            species
                            for species in candidates
                            if bool(set(species.types) & set(original_species.types))
                        ]
                    if should_match_bst:
                        candidates = self.filter_species_by_nearby_bst(candidates, sum(original_species.base_stats))

                    self.modified_legendary_encounters.append(MiscPokemonData(
                        self.random.choice(candidates).species_id,
                        encounter.address
                    ))

        def randomize_misc_pokemon() -> None:
            if self.options.misc_pokemon == RandomizeMiscPokemon.option_shuffle:
                # Just take the existing species and shuffle them
                shuffled_species = [encounter.species_id for encounter in emerald_data.misc_pokemon]
                self.random.shuffle(shuffled_species)

                self.modified_misc_pokemon = []
                for i, encounter in enumerate(emerald_data.misc_pokemon):
                    self.modified_misc_pokemon.append(MiscPokemonData(
                        shuffled_species[i],
                        encounter.address
                    ))
            else:
                should_match_bst = self.options.misc_pokemon in {
                    RandomizeMiscPokemon.option_match_base_stats,
                    RandomizeMiscPokemon.option_match_base_stats_and_type
                }
                should_match_type = self.options.misc_pokemon in {
                    RandomizeMiscPokemon.option_match_type,
                    RandomizeMiscPokemon.option_match_base_stats_and_type
                }

                for encounter in emerald_data.misc_pokemon:
                    original_species = self.modified_species[encounter.species_id]

                    candidates = [species for species in self.modified_species if species is not None]
                    if should_match_type:
                        candidates = [
                            species
                            for species in candidates
                            if bool(set(species.types) & set(original_species.types))
                        ]
                    if should_match_bst:
                        candidates = self.filter_species_by_nearby_bst(candidates, sum(original_species.base_stats))

                    self.modified_misc_pokemon.append(MiscPokemonData(
                        self.random.choice(candidates).species_id,
                        encounter.address
                    ))

        def randomize_opponent_parties() -> None:
            from collections import defaultdict

            should_match_bst = self.options.trainer_parties in {
                RandomizeTrainerParties.option_match_base_stats,
                RandomizeTrainerParties.option_match_base_stats_and_type
            }
            should_match_type = self.options.trainer_parties in {
                RandomizeTrainerParties.option_match_type,
                RandomizeTrainerParties.option_match_base_stats_and_type
            }

            per_species_tmhm_moves: Dict[int, List[int]] = {}

            for trainer in self.modified_trainers:
                new_party = []
                for pokemon in trainer.party.pokemon:
                    original_species = emerald_data.species[pokemon.species_id]

                    # Construct progressive tiers of blacklists that can be peeled back if they
                    # collectively cover too much of the pokedex. A lower index in `blacklists`
                    # indicates a more important set of species to avoid. Entries at `0` will
                    # always be blacklisted.
                    blacklists: Dict[int, List[Set[int]]] = defaultdict(list)

                    # Blacklist unevolved species
                    if pokemon.level >= self.options.force_fully_evolved:
                        blacklists[0].append(UNEVOLVED_POKEMON)

                    # Blacklist from player options
                    blacklists[2].append(self.blacklisted_opponent_pokemon)

                    # Type matching blacklist
                    if should_match_type:
                        blacklists[3].append({
                            species.species_id
                            for species in self.modified_species
                            if species is not None and not bool(set(species.types) & set(original_species.types))
                        })

                    merged_blacklist: Set[int] = set()
                    for max_priority in reversed(sorted(blacklists.keys())):
                        merged_blacklist = set()
                        for priority in blacklists.keys():
                            if priority <= max_priority:
                                for blacklist in blacklists[priority]:
                                    merged_blacklist |= blacklist

                        if len(merged_blacklist) < NUM_REAL_SPECIES:
                            break
                    else:
                        raise RuntimeError("This should never happen")

                    candidates = [
                        species
                        for species in self.modified_species
                        if species is not None and species.species_id not in merged_blacklist
                    ]

                    if should_match_bst:
                        candidates = self.filter_species_by_nearby_bst(candidates, sum(original_species.base_stats))

                    new_species = self.random.choice(candidates)

                    if new_species.species_id not in per_species_tmhm_moves:
                        per_species_tmhm_moves[new_species.species_id] = list({
                            self.modified_tmhm_moves[i]
                            for i, is_compatible in enumerate(int_to_bool_array(new_species.tm_hm_compatibility))
                            if is_compatible
                        })

                    # TMs and HMs compatible with the species. Could cache this per species
                    tm_hm_movepool = per_species_tmhm_moves[new_species.species_id]

                    # Moves the pokemon could have learned by now
                    level_up_movepool = list({
                        move.move_id
                        for move in new_species.learnset
                        if move.move_id != 0 and move.level <= pokemon.level
                    })

                    # 25% chance to pick a move from TMs or HMs
                    new_moves = (
                        self.random.choice(tm_hm_movepool if self.random.random() < 0.25 and len(tm_hm_movepool) > 0 else level_up_movepool),
                        self.random.choice(tm_hm_movepool if self.random.random() < 0.25 and len(tm_hm_movepool) > 0 else level_up_movepool),
                        self.random.choice(tm_hm_movepool if self.random.random() < 0.25 and len(tm_hm_movepool) > 0 else level_up_movepool),
                        self.random.choice(tm_hm_movepool if self.random.random() < 0.25 and len(tm_hm_movepool) > 0 else level_up_movepool)
                    )

                    new_party.append(TrainerPokemonData(new_species.species_id, pokemon.level, new_moves))

                trainer.party.pokemon = new_party

        def randomize_starters() -> None:
            should_match_bst = self.options.starters in {
                RandomizeStarters.option_match_base_stats,
                RandomizeStarters.option_match_base_stats_and_type
            }
            should_match_type = self.options.starters in {
                RandomizeStarters.option_match_type,
                RandomizeStarters.option_match_base_stats_and_type
            }

            new_starters: List[SpeciesData] = []

            easter_egg_type, easter_egg_value = get_easter_egg(self.options.easter_egg.value)
            if easter_egg_type == 1:
                new_starters = [
                    self.modified_species[easter_egg_value],
                    self.modified_species[easter_egg_value],
                    self.modified_species[easter_egg_value],
                ]
            else:
                for i, starter_id in enumerate(emerald_data.starters):
                    original_starter = emerald_data.species[starter_id]
                    type_blacklist = {
                        species.species_id
                        for species in self.modified_species
                        if species is not None and not bool(set(species.types) & set(original_starter.types))
                    } if should_match_type else set()

                    merged_blacklist = set(s.species_id for s in new_starters) | self.blacklisted_starters | type_blacklist
                    if len(merged_blacklist) == NUM_REAL_SPECIES:
                        merged_blacklist = set(s.species_id for s in new_starters) | self.blacklisted_starters
                    if len(merged_blacklist) == NUM_REAL_SPECIES:
                        merged_blacklist = set(s.species_id for s in new_starters)

                    candidates = [
                        species
                        for species in self.modified_species
                        if species is not None and species.species_id not in merged_blacklist
                    ]

                    if should_match_bst:
                        candidates = self.filter_species_by_nearby_bst(candidates, sum(original_starter.base_stats))

                    new_starters.append(self.random.choice(candidates))

            self.modified_starters = (
                new_starters[0].species_id,
                new_starters[1].species_id,
                new_starters[2].species_id
            )

            # Putting the unchosen starter onto the rival's team
            # (trainer name, index of starter in team, whether the starter is evolved)
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

        self.modified_trainers = copy.deepcopy(emerald_data.trainers)
        self.modified_tmhm_moves = copy.deepcopy(emerald_data.tmhm_moves)
        self.modified_legendary_encounters = copy.deepcopy(emerald_data.legendary_encounters)
        self.modified_misc_pokemon = copy.deepcopy(emerald_data.misc_pokemon)
        self.modified_starters = copy.deepcopy(emerald_data.starters)

        # Randomize species data
        if self.options.abilities != RandomizeAbilities.option_vanilla:
            randomize_abilities()

        if self.options.level_up_moves != LevelUpMoves.option_vanilla:
            randomize_learnsets()

        randomize_tm_hm_compatibility()  # Options are checked within this function

        min_catch_rate = min(self.options.min_catch_rate.value, 255)
        for species in self.modified_species:
            if species is not None:
                species.catch_rate = max(species.catch_rate, min_catch_rate)

        if self.options.tm_moves:
            randomize_tm_moves()

        # Randomize legendary encounters
        if self.options.legendary_encounters != RandomizeLegendaryEncounters.option_vanilla:
            randomize_legendary_encounters()

        # Randomize misc pokemon
        if self.options.misc_pokemon != RandomizeMiscPokemon.option_vanilla:
            randomize_misc_pokemon()

        # Randomize opponents
        if self.options.trainer_parties != RandomizeTrainerParties.option_vanilla:
            randomize_opponent_parties()

        # Randomize starters
        if self.options.starters != RandomizeStarters.option_vanilla:
            randomize_starters()

        generate_output(self, output_directory)

        del self.modified_trainers
        del self.modified_tmhm_moves
        del self.modified_legendary_encounters
        del self.modified_misc_pokemon
        del self.modified_starters
        del self.modified_species

    def write_spoiler(self, spoiler_handle: TextIO):
        if self.options.dexsanity:
            from collections import defaultdict

            spoiler_handle.write(f"\n\nWild Pokemon ({self.multiworld.player_name[self.player]}):\n\n")

            species_maps = defaultdict(set)
            for map in self.modified_maps.values():
                if map.land_encounters is not None:
                    for encounter in map.land_encounters.slots:
                        species_maps[encounter].add(map.name[4:])

                if map.water_encounters is not None:
                    for encounter in map.water_encounters.slots:
                        species_maps[encounter].add(map.name[4:])

                if map.fishing_encounters is not None:
                    for encounter in map.fishing_encounters.slots:
                        species_maps[encounter].add(map.name[4:])

            lines = [f"\t{emerald_data.species[species].label}: {', '.join(maps)}\n"
                     for species, maps in species_maps.items()]
            lines.sort()
            for line in lines:
                spoiler_handle.write(line)

        del self.modified_maps

    def extend_hint_information(self, hint_data):
        if self.options.dexsanity:
            from collections import defaultdict

            slot_to_rod = {
                0: "_OLD_ROD",
                1: "_OLD_ROD",
                2: "_GOOD_ROD",
                3: "_GOOD_ROD",
                4: "_GOOD_ROD",
                5: "_SUPER_ROD",
                6: "_SUPER_ROD",
                7: "_SUPER_ROD",
                8: "_SUPER_ROD",
                9: "_SUPER_ROD"
            }

            species_maps = defaultdict(set)
            for map in self.modified_maps.values():
                if map.land_encounters is not None:
                    for encounter in map.land_encounters.slots:
                        species_maps[encounter].add(map.name[4:] + "_GRASS")

                if map.water_encounters is not None:
                    for encounter in map.water_encounters.slots:
                        species_maps[encounter].add(map.name[4:] + "_WATER")

                if map.fishing_encounters is not None:
                    for slot, encounter in enumerate(map.fishing_encounters.slots):
                        species_maps[encounter].add(map.name[4:] + slot_to_rod[slot])

            hint_data[self.player] = {
                self.location_name_to_id[f"Pokedex - {emerald_data.species[species].label}"]: ", ".join(maps)
                for species, maps in species_maps.items()
            }

    def modify_multidata(self, multidata: Dict[str, Any]):
        import base64
        multidata["connect_names"][base64.b64encode(self.auth).decode("ascii")] = multidata["connect_names"][self.multiworld.player_name[self.player]]

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
            ItemClassification.progression_skip_balancing,
            None,
            self.player
        )

    def filter_species_by_nearby_bst(self, species: List[SpeciesData], target_bst: int) -> List[SpeciesData]:
        # Sort by difference in bst, then chop off the tail of the list that's more than
        # 10% different. If that leaves the list empty, increase threshold to 20%, then 30%, etc.
        species = sorted(species, key=lambda species: abs(sum(species.base_stats) - target_bst))
        cutoff_index = 0
        max_percent_different = 10
        while cutoff_index == 0 and max_percent_different < 10000:
            while cutoff_index < len(species) and abs(sum(species[cutoff_index].base_stats) - target_bst) < target_bst * (max_percent_different / 100):
                cutoff_index += 1
            max_percent_different += 10

        return species[:cutoff_index + 1]
