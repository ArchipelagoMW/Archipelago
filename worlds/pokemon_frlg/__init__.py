"""
Archipelago World definition for Pokémon FireRed/LeafGreen
"""
import base64
import copy
import logging
import os.path
import pkgutil
import threading

from collections import defaultdict
from settings import FilePath, Group, UserFilePath
from typing import Any, ClassVar, Dict, List, Set, TextIO, Tuple

from BaseClasses import CollectionState, Entrance, Item, ItemClassification, MultiWorld, Region, Tutorial
from worlds.AutoWorld import WebWorld, World
from entrance_rando import ERPlacementState
from .client import PokemonFRLGClient
from .data import (data, ability_name_map, ALL_SPECIES, APWORLD_VERSION, LEGENDARY_POKEMON, NAME_TO_SPECIES_ID,
                   POPTRACKER_CHECKSUM, LocationCategory, EventData, EvolutionMethodEnum, FlyData, MapData,
                   MiscPokemonData, MoveData, move_name_map, SpeciesData, StarterData, TrainerData, TradePokemonData)
from .entrances import set_hint_entrances, shuffle_entrances
from .groups import item_groups, location_groups
from .items import (PokemonFRLGItem, PokemonFRLGGlitchedToken, add_starting_items, create_item_name_to_id_map,
                    get_random_item, get_item_classification)
from .level_scaling import level_scaling
from .locations import (PokemonFRLGLocation, create_location_name_to_id_map, create_locations,
                        place_unrandomized_items, place_shop_items, set_free_fly, shuffle_badges)
from .options import (PokemonFRLGOptions, CardKey, CeruleanCaveRequirement, Dexsanity, FishingRods, FlashRequired,
                      FreeFlyLocation, GameVersion, Goal, IslandPasses, MixEntranceWarpPools, RandomizeLegendaryPokemon,
                      RandomizeMiscPokemon, RandomizeWildPokemon, ShuffleBadges, ShuffleBuildingEntrances,
                      ShuffleDungeonEntrances, ShuffleFlyUnlocks, ShuffleHiddenItems, ShufflePokedex,
                      ShuffleRunningShoes, TownMapFlyLocation, Trainersanity, ViridianCityRoadblock)
from .pokemon import (add_hm_compatability, randomize_abilities, randomize_base_stats, randomize_damage_categories,
                      randomize_legendaries, randomize_misc_pokemon, randomize_moves, randomize_move_types,
                      randomize_requested_trade_pokemon, randomize_starters, randomize_tm_hm_compatibility,
                      randomize_tm_moves, randomize_trainer_parties, randomize_types, randomize_wild_encounters)
from .regions import starting_town_map, create_indirect_conditions, create_regions, PokemonFRLGRegion
from .rules import PokemonFRLGLogic, set_hm_compatible_pokemon, set_logic_options, set_rules, verify_hm_accessibility
from .rom import PokemonFRLGPatchData, PokemonFireRedProcedurePatch, PokemonLeafGreenProcedurePatch, write_tokens
from .sanity_check import validate_regions
from .universal_tracker import (POPTRACKER_LOCATIONS, map_page_index, ut_reconnect_found_entrances, ut_set_locations,
                                ut_set_maps, ut_set_options)
from .util import int_to_bool_array, HM_TO_COMPATIBILITY_ID

# Try adding the Pokémon Gen 3 Adjuster
try:
    from worlds._pokemon_gen3_adjuster import __init__
except ImportError:
    pass

class PokemonFRLGWebWorld(WebWorld):
    """
    Webhost info for Pokémon FireRed and LeafGreen
    """
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Pokémon FireRed and LeafGreen with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Vyneras"]
    )

    adjuster_en = Tutorial(
        "Usage Guide",
        "A guide to use the Pokemon Gen 3 Adjuster with Pokemon Firered/Leafgreen.",
        "English",
        "adjuster_en.md",
        "adjuster/en",
        ["RhenaudTheLukark"]
    )

    tutorials = [setup_en, adjuster_en]


class PokemonFRLGSettings(Group):
    class PokemonFireRedRomFile(UserFilePath):
        """File name of your English Pokémon FireRed ROM"""
        description = "Pokemon FireRed ROM File"
        copy_to = "Pokemon - FireRed Version (USA, Europe).gba"
        md5s = PokemonFireRedProcedurePatch.hash

    class PokemonLeafGreenRomFile(UserFilePath):
        """File name of your English Pokémon LeafGreen ROM"""
        description = "Pokemon LeafGreen ROM File"
        copy_to = "Pokemon - LeafGreen Version (USA, Europe).gba"
        md5s = PokemonLeafGreenProcedurePatch.hash

    class UTPoptrackerPath(FilePath):
        description = "Pokemon FRLG Poptracker Pack Zip File"
        required = False

    firered_rom_file: PokemonFireRedRomFile = PokemonFireRedRomFile(PokemonFireRedRomFile.copy_to)
    leafgreen_rom_file: PokemonLeafGreenRomFile = PokemonLeafGreenRomFile(PokemonLeafGreenRomFile.copy_to)
    ut_poptracker_path: UTPoptrackerPath | str = UTPoptrackerPath()


class PokemonFRLGWorld(World):
    """
    Pokémon FireRed and LeafGreen are remakes of the very first Pokémon games.
    Experience the Kanto region with several updated features from Gen III.
    Catch, train, and battle Pokémon, face off against the evil organization Team Rocket, challenge Gyms in order to
    earn Badges, help resolve the many crises on the Sevii Islands, and become the Pokémon Champion!
    """
    game = "Pokemon FireRed and LeafGreen"
    web = PokemonFRLGWebWorld()
    topology_present = True

    settings_key = "pokemon_frlg_settings"
    settings: ClassVar[PokemonFRLGSettings]

    options_dataclass = PokemonFRLGOptions
    options: PokemonFRLGOptions

    item_name_to_id = create_item_name_to_id_map()
    location_name_to_id = create_location_name_to_id_map()
    item_name_groups = item_groups
    location_name_groups = location_groups

    required_client_version = (0, 6, 0)
    origin_region_name = "Title Screen"

    ut_can_gen_without_yaml = True
    glitches_item_name = PokemonFRLGGlitchedToken.TOKEN_NAME
    is_universal_tracker: bool
    found_entrances_datastorage_key: List[str] = []
    tracker_world = {
        "external_pack_key": "ut_poptracker_path",
        "poptracker_name_mapping": {k: data.locations[v].flag for k, v in POPTRACKER_LOCATIONS.items()},
        "map_page_index": map_page_index,
        "map_page_setting_key": "pokemon_frlg_map_{team}_{player}",
    }

    logic: PokemonFRLGLogic
    patch_data: PokemonFRLGPatchData
    starting_town: str
    starting_respawn: str
    free_fly_location_id: int
    town_map_fly_location_id: int
    modified_species: Dict[int, SpeciesData]
    modified_maps: Dict[str, MapData]
    modified_starters: Dict[str, StarterData]
    modified_events: Dict[str, EventData]
    modified_legendary_pokemon: Dict[str, MiscPokemonData]
    modified_misc_pokemon: Dict[str, MiscPokemonData]
    modified_trade_pokemon: Dict[str, TradePokemonData]
    modified_trainers: Dict[str, TrainerData]
    modified_tmhm_moves: List[int]
    modified_moves: Dict[str, MoveData]
    modified_type_damage_categories: List[int]
    per_species_tmhm_moves: Dict[int, List[int]]
    blacklisted_wild_pokemon: Set[int]
    blacklisted_starters: Set[int]
    blacklisted_trainer_pokemon: Set[int]
    blacklisted_legendary_pokemon: Set[int]
    blacklisted_misc_pokemon: Set[int]
    blacklisted_abilities: Set[int]
    blacklisted_moves: Set[int]
    blacklisted_tm_tutor_moves: Set[int]
    trainer_name_level_dict: Dict[str, int]
    trainer_name_list: List[str]
    trainer_level_list: List[int]
    encounter_name_level_dict: Dict[str, int]
    encounter_name_list: List[str]
    encounter_level_list: List[int]
    itempool: List[PokemonFRLGItem]
    pre_fill_items: List[PokemonFRLGItem]
    fly_destination_data: Dict[str, FlyData]
    er_placement_state: ERPlacementState | None
    er_entrances: List[Tuple[Entrance, Region]]
    moves_by_type: Dict[int, Set[int]]
    cerulean_cave_included: bool
    auth: bytes

    def __init__(self, multiworld, player):
        super(PokemonFRLGWorld, self).__init__(multiworld, player)
        self.is_universal_tracker = hasattr(self.multiworld, "generation_is_fake")
        self.logic = PokemonFRLGLogic(player, self.item_id_to_name)
        self.patch_data = PokemonFRLGPatchData()
        self.starting_town = "SPAWN_PALLET_TOWN"
        self.starting_respawn = "SPAWN_PALLET_TOWN"
        self.free_fly_location_id = 0
        self.town_map_fly_location_id = 0
        self.modified_species = copy.deepcopy(data.species)
        self.modified_maps = copy.deepcopy(data.maps)
        self.modified_starters = copy.deepcopy(data.starters)
        self.modified_events = copy.deepcopy(data.events)
        self.modified_legendary_pokemon = copy.deepcopy(data.legendary_pokemon)
        self.modified_misc_pokemon = copy.deepcopy(data.misc_pokemon)
        self.modified_trade_pokemon = copy.deepcopy(data.trade_pokemon)
        self.modified_trainers = copy.deepcopy(data.trainers)
        self.modified_tmhm_moves = copy.deepcopy(data.tmhm_moves)
        self.modified_moves = copy.deepcopy(data.moves)
        self.modified_type_damage_categories = copy.deepcopy(data.type_damage_categories)
        self.per_species_tmhm_moves = {}
        self.trainer_name_level_dict = {}
        self.trainer_name_list = []
        self.trainer_level_list = []
        self.encounter_name_level_dict = {}
        self.encounter_name_list = []
        self.encounter_level_list = []
        self.itempool = []
        self.pre_fill_items = []
        self.fly_destination_data = {}
        self.er_placement_state = None
        self.er_entrances = []
        self.moves_by_type = {}
        self.cerulean_cave_included = True
        self.finished_level_scaling = threading.Event()

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        assert validate_regions()

    def get_filler_item_name(self) -> str:
        return get_random_item(self, ItemClassification.filler)

    def generate_early(self) -> None:
        if self.is_universal_tracker:
            ut_set_options(self)
            ut_set_maps(self)
            ut_set_locations(self)

        self.blacklisted_wild_pokemon = {
            species.species_id for species in self.modified_species.values()
            if species.name in self.options.wild_pokemon_blacklist.value
        }
        if "Legendaries" in self.options.wild_pokemon_blacklist.value:
            self.blacklisted_wild_pokemon |= LEGENDARY_POKEMON

        self.blacklisted_starters = {
            species.species_id for species in self.modified_species.values()
            if species.name in self.options.starter_blacklist.value
        }
        if "Legendaries" in self.options.starter_blacklist.value:
            self.blacklisted_starters |= LEGENDARY_POKEMON

        self.blacklisted_trainer_pokemon = {
            species.species_id for species in self.modified_species.values()
            if species.name in self.options.trainer_blacklist.value
        }
        if "Legendaries" in self.options.trainer_blacklist.value:
            self.blacklisted_trainer_pokemon |= LEGENDARY_POKEMON

        self.blacklisted_legendary_pokemon = {
            species.species_id for species in self.modified_species.values()
            if species.name in self.options.legendary_pokemon_blacklist.value
        }
        if "Legendaries" in self.options.legendary_pokemon_blacklist.value:
            self.blacklisted_legendary_pokemon |= LEGENDARY_POKEMON

        self.blacklisted_misc_pokemon = {
            species.species_id for species in self.modified_species.values()
            if species.name in self.options.misc_pokemon_blacklist.value
        }
        if "Legendaries" in self.options.misc_pokemon_blacklist.value:
            self.blacklisted_misc_pokemon |= LEGENDARY_POKEMON

        self.blacklisted_abilities = {ability_name_map[name] for name in self.options.ability_blacklist.value}
        self.blacklisted_moves = {move_name_map[name] for name in self.options.move_blacklist.value}
        self.blacklisted_tm_tutor_moves = {move_name_map[name] for name in self.options.tm_tutor_moves_blacklist.value}

        if "All" in self.options.mix_entrance_warp_pools.value:
            for key in MixEntranceWarpPools.valid_keys:
                self.options.mix_entrance_warp_pools.value.add(key)

        # Modify options that are incompatible with each other
        if self.options.kanto_only:
            if self.options.goal == Goal.option_champion_rematch:
                logging.warning("Pokemon FRLG: Goal for player %s (%s) incompatible with Kanto Only. "
                                "Setting goal to Champion.", self.player, self.player_name)
                self.options.goal.value = Goal.option_champion
            if (self.options.cerulean_cave_requirement == CeruleanCaveRequirement.option_vanilla or
                    self.options.cerulean_cave_requirement == CeruleanCaveRequirement.option_restore_network):
                logging.warning("Pokemon FRLG: Cerulean Cave Requirement for player %s (%s) "
                                "incompatible with Kanto Only. Setting requirement to Defeat Champion.",
                                self.player, self.player_name)
                self.options.cerulean_cave_requirement.value = CeruleanCaveRequirement.option_champion

        if self.options.decouple_entrances_warps:
            if self.options.shuffle_buildings == ShuffleBuildingEntrances.option_simple:
                logging.warning("Pokemon FRLG: Simple Building Shuffle for player %s (%s) is "
                                "incompatible with Decoupled Entrances. Setting shuffle to Restricted.",
                                self.player, self.player_name)
                self.options.shuffle_buildings.value = ShuffleBuildingEntrances.option_restricted
            if self.options.shuffle_dungeons == ShuffleDungeonEntrances.option_simple:
                logging.warning("Pokemon FRLG: Simple Dungeon Shuffle for player %s (%s) is "
                                "incompatible with Decoupled Entrances. Setting shuffle to Restricted.",
                                self.player, self.player_name)
                self.options.shuffle_dungeons.value = ShuffleDungeonEntrances.option_restricted

        # Check if Ceruelan Cave should be included in this world
        if (not self.options.post_goal_locations and
                self.options.goal == Goal.option_champion and
                self.options.cerulean_cave_requirement in (CeruleanCaveRequirement.option_vanilla,
                                                           CeruleanCaveRequirement.option_champion)):
            self.cerulean_cave_included = False

        # Remove badges from non-local items if they are shuffled among gyms
        if not self.options.shuffle_badges:
            self.options.local_items.value.update(item_groups["Badges"])

        if (self.options.viridian_city_roadblock == ViridianCityRoadblock.option_early_parcel and
                not self.options.random_starting_town):
            self.multiworld.local_early_items[self.player]["Oak's Parcel"] = 1

        set_logic_options(self)
        randomize_types(self)
        randomize_abilities(self)
        randomize_move_types(self)
        randomize_damage_categories(self)
        randomize_moves(self)
        randomize_base_stats(self)
        randomize_wild_encounters(self)
        randomize_starters(self)
        randomize_legendaries(self)
        randomize_misc_pokemon(self)
        randomize_tm_hm_compatibility(self)
        set_hm_compatible_pokemon(self)

    def create_regions(self) -> None:
        regions = create_regions(self)
        create_locations(self, regions)
        self.multiworld.regions.extend(regions.values())
        create_indirect_conditions(self)
        randomize_requested_trade_pokemon(self)
        set_rules(self)

    def create_items(self) -> None:
        item_locations = [location for location in self.get_locations() if location.item is None]
        self.itempool = [self.create_item_by_id(location.default_item_id) for location in item_locations]

        add_starting_items(self)
        place_unrandomized_items(self)
        place_shop_items(self)

        items_to_remove: List[PokemonFRLGItem] = []
        items_to_add: List[PokemonFRLGItem] = []

        if not self.options.shuffle_badges:
            badge_items = [self.create_item(badge) for badge in sorted(item_groups["Badges"])]
            items_to_remove.extend(badge_items)
            self.pre_fill_items.extend(badge_items)

        if self.options.card_key == CardKey.option_split:
            items_to_remove.append(self.create_item("Card Key"))
            items_to_add.append(self.create_item("Card Key 3F"))
        elif self.options.card_key == CardKey.option_progressive:
            for item in ["Card Key", "Card Key 2F", "Card Key 4F", "Card Key 5F", "Card Key 6F", "Card Key 7F",
                         "Card Key 8F", "Card Key 9F", "Card Key 10F", "Card Key 11F"]:
                items_to_remove.append(self.create_item(item))
            for _ in range(10):
                items_to_add.append(self.create_item("Progressive Card Key"))

        if not self.options.kanto_only:
            if self.options.island_passes == IslandPasses.option_progressive:
                for item in ["Tri Pass", "Rainbow Pass"]:
                    items_to_remove.append(self.create_item(item))
                for _ in range(2):
                    items_to_add.append(self.create_item("Progressive Pass"))
            elif self.options.island_passes == IslandPasses.option_split:
                for item in ["Tri Pass", "Rainbow Pass"]:
                    items_to_remove.append(self.create_item(item))
                for item in ["Three Pass", "Four Pass"]:
                    items_to_add.append(self.create_item(item))
            elif self.options.island_passes == IslandPasses.option_progressive_split:
                for item in ["Tri Pass", "One Pass", "Two Pass", "Rainbow Pass", "Five Pass", "Six Pass", "Seven Pass"]:
                    items_to_remove.append(self.create_item(item))
                for _ in range(7):
                    items_to_add.append(self.create_item("Progressive Pass"))

        if self.options.fishing_rods == FishingRods.option_progressive:
            for item in ["Old Rod", "Good Rod", "Super Rod"]:
                items_to_remove.append(self.create_item(item))
            for _ in range(3):
                items_to_add.append(self.create_item("Progressive Rod"))

        if self.options.split_teas:
            items_to_remove.append(self.create_item("Tea"))
            items_to_add.append(self.create_item("Green Tea"))

        if self.options.gym_keys:
            items_to_remove.append(self.create_item("Secret Key"))
            items_to_add.append(self.create_item("Cinnabar Key"))

        for item in items_to_remove:
            self.itempool.remove(item)
        for item in items_to_add:
            self.itempool.append(item)

        filler_items = [item for item in self.itempool if item.classification == ItemClassification.filler and
                        item.name not in item_groups["Unique Items"]]
        self.random.shuffle(filler_items)

        # Add progression items that should replace filler items
        if self.options.shuffle_berry_pouch:
            self.itempool.append(self.create_item("Berry Pouch"))
            self.itempool.remove(filler_items.pop())
        if self.options.shuffle_tm_case:
            self.itempool.append(self.create_item("TM Case"))
            self.itempool.remove(filler_items.pop())
        if self.options.shuffle_jumping_shoes:
            self.itempool.append(self.create_item("Jumping Shoes"))
            self.itempool.remove(filler_items.pop())

        # Add key items that are relevant in Kanto Only to the itempool
        if self.options.kanto_only:
            item_names = ["HM06 Rock Smash", "HM07 Waterfall", "Sun Stone"]
            for item_name in item_names:
                self.itempool.append(self.create_item(item_name))
                self.itempool.remove(filler_items.pop())

        # Remove copies unique items based on how many are in the start inventory
        unique_items: Set[str] = set(item_groups["Unique Items"] |
                                     item_groups["Progressive Items"])
        for item in self.multiworld.precollected_items[self.player]:
            assert isinstance(item, PokemonFRLGItem)
            if item.name in unique_items:
                try:
                    self.itempool.remove(item)
                    self.itempool.append(self.create_item(get_random_item(self, ItemClassification.filler)))
                except ValueError:
                    continue

        verify_hm_accessibility(self)
        state = self.get_world_collection_state()

        # Delete evolutions that are not in logic in an all state so that the accessibility check doesn't fail
        evolution_region = self.multiworld.get_region("Evolutions", self.player)
        for location in evolution_region.locations.copy():
            if not location.can_reach(state):
                evolution_region.locations.remove(location)

        if self.options.dexsanity != Dexsanity.special_range_names["none"] and not self.is_universal_tracker:
            # Delete dexsanity locations that are not in logic in an all state since they aren't accessible
            pokedex_region = self.multiworld.get_region("Pokedex", self.player)
            for location in pokedex_region.locations.copy():
                if not location.can_reach(state):
                    pokedex_region.locations.remove(location)
                    self.itempool.remove(filler_items.pop())

            # Delete dexsanity locations if there are more than the amount specified in the settings
            if len(pokedex_region.locations) > self.options.dexsanity.value:
                pokedex_locations = pokedex_region.locations.copy()
                priority_pokedex_locations = [loc for loc in pokedex_locations
                                              if loc.name in self.options.priority_locations.value]
                non_priority_pokedex_locations = [loc for loc in pokedex_locations
                                                  if loc.name not in self.options.priority_locations.value]
                self.random.shuffle(priority_pokedex_locations)
                self.random.shuffle(non_priority_pokedex_locations)
                pokedex_locations = non_priority_pokedex_locations + priority_pokedex_locations
                for location in pokedex_locations:
                    pokedex_region.locations.remove(location)
                    self.itempool.remove(filler_items.pop())
                    if len(pokedex_region.locations) <= self.options.dexsanity.value:
                        break

        self.multiworld.itempool += self.itempool
        # Any unreachable evolutions have been removed, so update the species items oak's aides and dexsanity check for.
        self.logic.update_species(self)

    def connect_entrances(self) -> None:
        set_free_fly(self)
        if not self.options.shuffle_badges:
            shuffle_badges(self)
            verify_hm_accessibility(self)
        if shuffle_entrances(self):
            verify_hm_accessibility(self)

    def generate_basic(self) -> None:
        # Create auth
        self.auth = self.random.getrandbits(16 * 8).to_bytes(16, "little")

    @classmethod
    def stage_generate_output(cls, multiworld, output_directory):
        # Change all but one instance of a Pokémon in each sphere to useful classification
        # This cuts down on time calculating the playthrough
        found_mons = set()
        pokemon = {species.name for species in data.species.values()}
        for sphere in multiworld.get_spheres():
            mon_locations_in_sphere = defaultdict(list)
            for location in sphere:
                if location.game == "Pokemon FireRed and LeafGreen":
                    assert isinstance(location, PokemonFRLGLocation)
                    if (location.item.game == "Pokemon FireRed and LeafGreen" and
                            (location.item.name in pokemon or
                             "Static " in location.item.name or
                             "Evolved " in location.item.name)
                            and location.item.advancement):
                        key = (location.player, location.item.name)
                        if key in found_mons:
                            location.item.classification = ItemClassification.useful
                        else:
                            mon_locations_in_sphere[key].append(location)
            for key, mon_locations in mon_locations_in_sphere.items():
                found_mons.add(key)
                if len(mon_locations) > 1:
                    mon_locations.sort()
                    for location in mon_locations[1:]:
                        location.item.classification = ItemClassification.useful
        level_scaling(multiworld)

    def generate_output(self, output_directory: str) -> None:
        # Modify catch rate
        min_catch_rate = min(self.options.min_catch_rate.value, 255)
        for species in self.modified_species.values():
            species.catch_rate = max(species.catch_rate, min_catch_rate)

        self.finished_level_scaling.wait()

        randomize_tm_moves(self)
        randomize_trainer_parties(self)

        if self.options.game_version == GameVersion.option_firered:
            patch = PokemonFireRedProcedurePatch(player=self.player, player_name=self.player_name)
            patch.write_file("base_patch_rev0.bsdiff4",
                             pkgutil.get_data(__name__, "data/base_patch_firered.bsdiff4"))
            patch.write_file("base_patch_rev1.bsdiff4",
                             pkgutil.get_data(__name__, "data/base_patch_firered_rev1.bsdiff4"))
        else:
            patch = PokemonLeafGreenProcedurePatch(player=self.player, player_name=self.player_name)
            patch.write_file("base_patch_rev0.bsdiff4",
                             pkgutil.get_data(__name__, "data/base_patch_leafgreen.bsdiff4"))
            patch.write_file("base_patch_rev1.bsdiff4",
                             pkgutil.get_data(__name__, "data/base_patch_leafgreen_rev1.bsdiff4"))

        game_version = self.options.game_version.current_key
        self.patch_data.set_game_version(game_version)
        write_tokens(self)
        patch.write_file("token_data_rev0.bin", self.patch_data.get_rev_token_bytes(game_version))
        patch.write_file("token_data_rev1.bin", self.patch_data.get_rev_token_bytes(f"{game_version}_rev1"))

        # Write output
        out_file_name = self.multiworld.get_out_file_name_base(self.player)
        patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))

    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        if self.options.random_starting_town:
            starting_town = starting_town_map[self.starting_town]
            if starting_town == "Viridian City (South)" or starting_town == "Three Island Town (South)":
                starting_town = starting_town[:-8]
            spoiler_handle.write(f"Starting Town:                   {starting_town}\n")
        if self.options.free_fly_location:
            free_fly_location = self.multiworld.get_location("Free Fly Location", self.player)
            spoiler_handle.write(f"Free Fly Location:               {free_fly_location.item.name}\n")
        if self.options.town_map_fly_location:
            town_map_fly_location = self.multiworld.get_location("Town Map Fly Location", self.player)
            spoiler_handle.write(f"Town Map Fly Location:           {town_map_fly_location.item.name}\n")

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        # Add entrances to the spoiler log if they are shuffled
        if self.er_placement_state:
            spoiler_handle.write(f"\n\nEntrances ({self.multiworld.player_name[self.player]}):\n\n")
            for entrance_name, exit_name in sorted(self.er_placement_state.pairings):
                entrance = self.get_entrance(entrance_name)
                spoiler_handle.write(f"{entrance_name} => {entrance.connected_region}\n")

        # Add fly destinations to the spoiler log if they are randomized
        if self.options.randomize_fly_destinations:
            spoiler_handle.write(f"\n\nFly Destinations ({self.multiworld.player_name[self.player]}):\n\n")
            for exit in self.get_region("Sky").exits:
                spoiler_handle.write(f"{exit.name}: {exit.connected_region.name}\n")

        wild_pokemon_randomized = self.options.wild_pokemon != RandomizeWildPokemon.option_vanilla
        static_pokemon_randomized = self.options.misc_pokemon != RandomizeMiscPokemon.option_vanilla
        legendary_pokemon_randomized = self.options.legendary_pokemon != RandomizeLegendaryPokemon.option_vanilla

        # Add Pokémon locations to the spoiler log if they are not vanilla
        if wild_pokemon_randomized or static_pokemon_randomized or legendary_pokemon_randomized:
            spoiler_handle.write(f"\n\nPokemon Locations ({self.multiworld.player_name[self.player]}):\n\n")

            species_locations = defaultdict(set)

            for location in self.get_locations():
                assert isinstance(location, PokemonFRLGLocation)
                if ((wild_pokemon_randomized and
                     location.category == LocationCategory.EVENT_WILD_POKEMON) or
                        (static_pokemon_randomized and
                         location.category == LocationCategory.EVENT_STATIC_POKEMON) or
                        (legendary_pokemon_randomized and
                         location.category == LocationCategory.EVENT_LEGENDARY_POKEMON)):
                    pokemon_name = location.item.name.replace("Static ", "")
                    species_locations[pokemon_name].add(location.spoiler_name)

            lines = [f"{species}: {', '.join(sorted(locations))}\n"
                     for species, locations in species_locations.items()]
            lines.sort()
            for line in lines:
                spoiler_handle.write(line)

    def extend_hint_information(self, hint_data):
        hint_data[self.player] = {}
        if self.options.dexsanity != Dexsanity.special_range_names["none"]:
            species_locations = defaultdict(set)

            for location in self.get_locations():
                assert isinstance(location, PokemonFRLGLocation)
                if location.category in [LocationCategory.EVENT_WILD_POKEMON,
                                         LocationCategory.EVENT_STATIC_POKEMON,
                                         LocationCategory.EVENT_LEGENDARY_POKEMON]:
                    pokemon_name = location.item.name.replace("Static ", "")
                    species_locations[pokemon_name].add(location.spoiler_name)

            for species, maps in species_locations.items():
                hint_data[self.player][self.location_name_to_id[f"Pokedex - {species}"]] = ", ".join(sorted(maps))

        if self.er_placement_state is not None:
            set_hint_entrances(self)
            for region in self.get_regions():
                assert isinstance(region, PokemonFRLGRegion)
                if region.entrance_hints:
                    for location in region.locations:
                        if not location.is_event:
                            hint_data[self.player][location.address] = ", ".join(sorted(region.entrance_hints))

    def modify_multidata(self, multidata: Dict[str, Any]):
        multidata["connect_names"][base64.b64encode(self.auth).decode("ascii")] = \
            multidata["connect_names"][self.player_name]

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = self.options.as_dict(
            "game_version",
            "goal",
            "skip_elite_four",
            "kanto_only",
            "random_starting_town",
            "shuffle_pokemon_centers",
            "shuffle_gyms",
            "shuffle_marts",
            "shuffle_harbors",
            "shuffle_buildings",
            "shuffle_dungeons",
            "shuffle_interiors",
            "shuffle_warp_tiles",
            "shuffle_dropdowns",
            "decouple_entrances_warps",
            "randomize_fly_destinations",
            "shuffle_badges",
            "shuffle_hidden",
            "extra_key_items",
            "shopsanity",
            "vending_machines",
            "prizesanity",
            "shop_slots",
            "rematchsanity",
            "rematch_requirements",
            "famesanity",
            "shuffle_fly_unlocks",
            "pokemon_request_locations",
            "shuffle_pokedex",
            "shuffle_running_shoes",
            "shuffle_berry_pouch",
            "shuffle_tm_case",
            "shuffle_jumping_shoes",
            "post_goal_locations",
            "card_key",
            "island_passes",
            "fishing_rods",
            "split_teas",
            "gym_keys",
            "itemfinder_required",
            "flash_required",
            "fame_checker_required",
            "bicycle_requires_jumping_shoes",
            "acrobatic_bicycle",
            "evolutions_required",
            "evolution_methods_required",
            "viridian_city_roadblock",
            "pewter_city_roadblock",
            "modify_world_state",
            "additional_dark_caves",
            "remove_badge_requirement",
            "oaks_aide_route_2",
            "oaks_aide_route_10",
            "oaks_aide_route_11",
            "oaks_aide_route_16",
            "oaks_aide_route_15",
            "fossil_count",
            "viridian_gym_requirement",
            "viridian_gym_count",
            "route22_gate_requirement",
            "route22_gate_count",
            "route23_guard_requirement",
            "route23_guard_count",
            "elite_four_requirement",
            "elite_four_count",
            "elite_four_rematch_count",
            "cerulean_cave_requirement",
            "cerulean_cave_count",
            "free_fly_location",
            "town_map_fly_location",
            "provide_hints",
            "death_link"
        )

        game_version = self.options.game_version.current_key

        slot_data["trainersanity"] = 1 if self.options.trainersanity != Trainersanity.special_range_names["none"] else 0
        slot_data["trainersanity_locations"] = [loc.address for loc in self.get_locations()
                                                if loc.category == LocationCategory.TRAINER
                                                or loc.category == LocationCategory.TRAINER_REMATCH]
        slot_data["dexsanity"] = 1 if self.options.dexsanity != Dexsanity.special_range_names["none"] else 0
        slot_data["dexsanity_locations"] = [loc.address for loc in self.get_locations()
                                            if loc.category == LocationCategory.POKEDEX]
        slot_data["elite_four_rematch_requirement"] = self.options.elite_four_requirement.value
        slot_data["starting_town"] = data.constants[self.starting_town]
        slot_data["free_fly_location_id"] = self.free_fly_location_id
        slot_data["town_map_fly_location_id"] = self.town_map_fly_location_id

        if self.options.randomize_fly_destinations:
            slot_data["fly_destinations"] = {}
            for exit in self.get_region("Sky").exits:
                slot_data["fly_destinations"][exit.name] = exit.connected_region.name

        if self.er_placement_state is not None:
            slot_data["entrances"] = {}
            for source, dest in self.er_placement_state.pairings:
                slot_data["entrances"][source] = self.get_entrance(source).connected_region.name

        slot_data["wild_encounters"] = {}
        slot_data["static_encounters"] = {}
        wild_locations = [loc for loc in self.get_locations() if loc.category == LocationCategory.EVENT_WILD_POKEMON]
        static_locations = [loc for loc in self.get_locations()
                            if loc.category == LocationCategory.EVENT_STATIC_POKEMON
                            or loc.category == LocationCategory.EVENT_LEGENDARY_POKEMON]
        for location in wild_locations:
            national_dex_id = data.species[NAME_TO_SPECIES_ID[location.item.name]].national_dex_number
            if location.encounter_key not in slot_data["wild_encounters"]:
                slot_data["wild_encounters"][location.encounter_key] = set()
            slot_data["wild_encounters"][location.encounter_key].add(national_dex_id)
        for location in static_locations:
            pokemon_name = location.item.name.replace("Static ", "")
            national_dex_id = data.species[NAME_TO_SPECIES_ID[pokemon_name]].national_dex_number
            slot_data["static_encounters"][location.encounter_key] = national_dex_id

        slot_data["tm_hm_compatibility"] = {v.name: v.tm_hm_compatibility for v in self.modified_species.values()}
        slot_data["requested_trade_pokemon"] = {k: v.requested_species_id[game_version]
                                                for k, v in self.modified_trade_pokemon.items()}
        slot_data["resort_gorgeous_pokemon"] = self.logic.resort_gorgeous_pokemon
        slot_data["poptracker_checksum"] = POPTRACKER_CHECKSUM
        return slot_data

    def create_item(self, name: str) -> "PokemonFRLGItem":
        if name == self.glitches_item_name:
            return PokemonFRLGGlitchedToken(self.player)
        return self.create_item_by_id(self.item_name_to_id[name])

    def create_item_by_id(self, item_id: int):
        return PokemonFRLGItem(
            self.item_id_to_name[item_id],
            get_item_classification(item_id),
            item_id,
            self.player
        )

    def get_world_collection_state(self) -> CollectionState:
        state = CollectionState(self.multiworld, True)
        progression_items = [item for item in self.itempool if item.advancement]
        locations = self.get_locations()
        for item in progression_items:
            state.collect(item, True)
        for item in self.get_pre_fill_items():
            state.collect(item, True)
        state.sweep_for_advancements(locations)
        return state

    def get_pre_fill_items(self):
        pre_fill_items = self.pre_fill_items.copy()
        if self.logic.guaranteed_hm_access:
            for hm in ["Cut", "Fly", "Surf", "Strength", "Flash", "Rock Smash", "Waterfall"]:
                pre_fill_items.append(PokemonFRLGItem(f"Teach {hm}",
                                                      ItemClassification.progression,
                                                      None,
                                                      self.player))
        return pre_fill_items

    def collect(self, state: "CollectionState", item: "Item") -> bool:
        changed = super().collect(state, item)
        if changed:
            item_name = item.name
            if item_name in self.logic.pokemon_hm_use:
                state.prog_items[self.player].update(self.logic.pokemon_hm_use[item_name])
            return True
        else:
            return False

    def remove(self, state: "CollectionState", item: "Item") -> bool:
        changed = super().remove(state, item)
        if changed:
            item_name = item.name
            if item_name in self.logic.pokemon_hm_use:
                state.prog_items[self.player].subtract(self.logic.pokemon_hm_use[item_name])
            return True
        else:
            return False

    # Universal Tracker
    @property
    def ut_slot_data(self) -> dict[str, Any]:
        if hasattr(self.multiworld, "re_gen_passthrough"):
            return self.multiworld.re_gen_passthrough[self.game]
        else:
            return {}

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]):
        return slot_data

    def reconnect_found_entrances(self, found_key: str, data_storage_value: Any) -> None:
        if data_storage_value:
            ut_reconnect_found_entrances(self, found_key)
