"""
Archipelago World definition for Pokémon FireRed/LeafGreen
"""
import base64
import copy
import logging
import os.path
import pkgutil
import settings
import threading

from collections import defaultdict
from typing import Any, ClassVar, Dict, List, Set, TextIO

from BaseClasses import CollectionState, ItemClassification, LocationProgressType, MultiWorld, Tutorial, Item
from Fill import fill_restrictive, FillError
from worlds.AutoWorld import WebWorld, World
from entrance_rando import ERPlacementState
from .client import PokemonFRLGClient
from .data import (data, ability_name_map, ALL_SPECIES, APWORLD_VERSION, LEGENDARY_POKEMON, NAME_TO_SPECIES_ID,
                   POPTRACKER_CHECKSUM, LocationCategory, EventData, EvolutionMethodEnum, FlyData, MapData,
                   MiscPokemonData, MoveData, move_name_map, SpeciesData, StarterData, TrainerData, TradePokemonData)
from .entrances import shuffle_entrances
from .groups import item_groups, location_groups
from .items import PokemonFRLGItem, create_item_name_to_id_map, get_random_item, get_item_classification
from .level_scaling import level_scaling
from .locations import (PokemonFRLGLocation, create_location_name_to_id_map, create_locations_from_categories,
                        fill_unrandomized_locations, set_free_fly)
from .options import (PokemonFRLGOptions, CardKey, CeruleanCaveRequirement, Dexsanity, DungeonEntranceShuffle,
                      FlashRequired, FreeFlyLocation, GameVersion, Goal, IslandPasses, RandomizeLegendaryPokemon,
                      RandomizeMiscPokemon, RandomizeWildPokemon, ShuffleFlyUnlocks, ShuffleHiddenItems, ShuffleBadges,
                      ShuffleRunningShoes, TownMapFlyLocation, Trainersanity, ViridianCityRoadblock)
from .pokemon import (add_hm_compatability, randomize_abilities, randomize_damage_categories, randomize_legendaries,
                      randomize_misc_pokemon, randomize_moves, randomize_move_types, randomize_requested_trade_pokemon,
                      randomize_starters, randomize_tm_hm_compatibility, randomize_tm_moves, randomize_trainer_parties,
                      randomize_types, randomize_wild_encounters)
from .regions import starting_town_map, create_indirect_conditions, create_regions
from .rules import PokemonFRLGLogic, set_hm_compatible_pokemon, set_logic_options, set_rules, verify_hm_accessibility
from .rom import PokemonFRLGPatchData, PokemonFireRedProcedurePatch, PokemonLeafGreenProcedurePatch, write_tokens
from .sanity_check import validate_regions
from .util import int_to_bool_array, HM_TO_COMPATIBILITY_ID

# Try adding the Pokemon Gen 3 Adjuster
try:
    from worlds._pokemon_gen3_adjuster import __init__
except:
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


class PokemonFRLGSettings(settings.Group):
    class PokemonFireRedRomFile(settings.UserFilePath):
        """File name of your English Pokémon FireRed ROM"""
        description = "Pokemon FireRed ROM File"
        copy_to = "Pokemon - FireRed Version (USA, Europe).gba"
        md5s = PokemonFireRedProcedurePatch.hash

    class PokemonLeafGreenRomFile(settings.UserFilePath):
        """File name of your English Pokémon LeafGreen ROM"""
        description = "Pokemon LeafGreen ROM File"
        copy_to = "Pokemon - LeafGreen Version (USA, Europe).gba"
        md5s = PokemonLeafGreenProcedurePatch.hash

    firered_rom_file: PokemonFireRedRomFile = PokemonFireRedRomFile(PokemonFireRedRomFile.copy_to)
    leafgreen_rom_file: PokemonLeafGreenRomFile = PokemonLeafGreenRomFile(PokemonLeafGreenRomFile.copy_to)


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

    logic: PokemonFRLGLogic
    patch_data: PokemonFRLGPatchData
    starting_town: str
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
    blacklisted_abilities: Set[int]
    blacklisted_moves: Set[int]
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
    er_spoiler_names: List[str]
    moves_by_type: Dict[int, Set[int]]
    shop_locations_by_spheres: List[Set[PokemonFRLGLocation]]
    auth: bytes

    def __init__(self, multiworld, player):
        super(PokemonFRLGWorld, self).__init__(multiworld, player)
        self.logic = PokemonFRLGLogic(player, self.item_id_to_name)
        self.patch_data = PokemonFRLGPatchData()
        self.starting_town = "SPAWN_PALLET_TOWN"
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
        self.er_spoiler_names = []
        self.moves_by_type = {}
        self.shop_locations_by_spheres = []
        self.finished_level_scaling = threading.Event()

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        assert validate_regions()

    def get_filler_item_name(self) -> str:
        return get_random_item(self, ItemClassification.filler)

    def generate_early(self) -> None:
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

        self.blacklisted_abilities = {ability_name_map[name] for name in self.options.ability_blacklist.value}
        self.blacklisted_moves = {move_name_map[name] for name in self.options.move_blacklist.value}

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

        # Remove badges from non-local items if they are shuffled among gyms
        if not self.options.shuffle_badges:
            self.options.local_items.value.update(item_groups["Badges"])

        # Add starting items from settings
        if self.options.shuffle_running_shoes == ShuffleRunningShoes.option_start_with:
            self.options.start_inventory.value["Running Shoes"] = 1

        if (self.options.viridian_city_roadblock == ViridianCityRoadblock.option_early_parcel and
                not self.options.random_starting_town):
            self.multiworld.local_early_items[self.player]["Oak's Parcel"] = 1

        set_logic_options(self)
        randomize_types(self)
        randomize_abilities(self)
        randomize_move_types(self)
        randomize_damage_categories(self)
        randomize_moves(self)
        randomize_wild_encounters(self)
        randomize_starters(self)
        randomize_legendaries(self)
        randomize_misc_pokemon(self)
        randomize_tm_hm_compatibility(self)
        set_hm_compatible_pokemon(self)

    def create_regions(self) -> None:
        regions = create_regions(self)

        categories = {
            LocationCategory.BADGE,
            LocationCategory.HM,
            LocationCategory.KEY_ITEM,
            LocationCategory.FLY_UNLOCK,
            LocationCategory.ITEM_BALL,
            LocationCategory.STARTING_ITEM,
            LocationCategory.NPC_GIFT
        }

        if self.options.shuffle_hidden == ShuffleHiddenItems.option_all:
            categories.update([LocationCategory.HIDDEN_ITEM, LocationCategory.HIDDEN_ITEM_RECURRING])
        elif self.options.shuffle_hidden == ShuffleHiddenItems.option_nonrecurring:
            categories.add(LocationCategory.HIDDEN_ITEM)
        if self.options.extra_key_items:
            categories.add(LocationCategory.EXTRA_KEY_ITEM)
        if self.options.shopsanity:
            categories.add(LocationCategory.SHOPSANITY)
        if self.options.trainersanity != Trainersanity.special_range_names["none"]:
            categories.add(LocationCategory.TRAINERSANITY)
        if self.options.dexsanity != Dexsanity.special_range_names["none"]:
            categories.add(LocationCategory.DEXSANITY)
        if self.options.famesanity:
            categories.add(LocationCategory.FAMESANITY)
            if self.options.pokemon_request_locations:
                categories.add(LocationCategory.FAMESANITY_POKEMON_REQUEST)
        if self.options.pokemon_request_locations:
            categories.add(LocationCategory.POKEMON_REQUEST)
        if self.options.card_key != CardKey.option_vanilla:
            categories.add(LocationCategory.SPLIT_CARD_KEY)
        if (self.options.island_passes == IslandPasses.option_split or
                self.options.island_passes == IslandPasses.option_progressive_split):
            categories.add(LocationCategory.SPLIT_ISLAND_PASS)
        if self.options.split_teas:
            categories.add(LocationCategory.SPLIT_TEA)
        if self.options.shuffle_running_shoes != ShuffleRunningShoes.option_vanilla:
            categories.add(LocationCategory.RUNNING_SHOES)
        if self.options.gym_keys:
            categories.add(LocationCategory.GYM_KEY)

        create_locations_from_categories(self, regions, categories)
        self.multiworld.regions.extend(regions.values())

        create_indirect_conditions(self)
        randomize_requested_trade_pokemon(self)
        fill_unrandomized_locations(self)

        def exclude_locations(locations: List[str]):
            for location in locations:
                try:
                    self.get_location(location).progress_type = LocationProgressType.EXCLUDED
                except KeyError:
                    continue

        if self.options.goal == Goal.option_champion:
            exclude_locations([
                "Lorelei's Room - Elite Four Lorelei Rematch Reward",
                "Bruno's Room - Elite Four Bruno Rematch Reward",
                "Agatha's Room - Elite Four Agatha Rematch Reward",
                "Lance's Room - Elite Four Lance Rematch Reward",
                "Champion's Room - Champion Rematch Reward",
                "Two Island Town - Beauty Info"
            ])

            if ((self.options.cerulean_cave_requirement == CeruleanCaveRequirement.option_vanilla
                    or self.options.cerulean_cave_requirement == CeruleanCaveRequirement.option_champion)
                    and self.options.dungeon_entrance_shuffle == DungeonEntranceShuffle.option_off):
                exclude_locations([
                    "Cerulean Cave 1F - Southwest Item",
                    "Cerulean Cave 1F - East Plateau Item",
                    "Cerulean Cave 1F - West Plateau Item",
                    "Cerulean Cave 2F - East Item",
                    "Cerulean Cave 2F - West Item",
                    "Cerulean Cave 2F - Center Item",
                    "Cerulean Cave B1F - Northeast Item",
                    "Cerulean Cave B1F - East Plateau Item",
                    "Cerulean Cave 1F - West Plateau Hidden Item"
                ])

            if "Early Gossipers" not in self.options.modify_world_state.value:
                exclude_locations([
                    "Professor Oak's Lab - Oak's Aide M Info (Right)",
                    "Professor Oak's Lab - Oak's Aide M Info (Left)",
                    "Cerulean Pokemon Center 1F - Bookshelf Info",
                    "Pokemon Fan Club - Worker Info",
                    "Lavender Pokemon Center 1F - Balding Man Info",
                    "Celadon Condominiums 1F - Tea Woman Info",
                    "Celadon Department Store 2F - Woman Info",
                    "Fuchsia City - Koga's Daughter Info",
                    "Pokemon Trainer Fan Club - Bookshelf Info",
                    "Saffron City - Battle Girl Info",
                    "Cinnabar Pokemon Center 1F - Bookshelf Info",
                    "Indigo Plateau Pokemon Center 1F - Black Belt Info 1",
                    "Indigo Plateau Pokemon Center 1F - Black Belt Info 2",
                    "Indigo Plateau Pokemon Center 1F - Bookshelf Info",
                    "Indigo Plateau Pokemon Center 1F - Cooltrainer Info",
                    "Ember Spa - Black Belt Info",
                    "Five Island Pokemon Center 1F - Bookshelf Info",
                    "Seven Island Pokemon Center 1F - Bookshelf Info"
                ])

        set_rules(self)

    def create_items(self) -> None:
        item_locations: List[PokemonFRLGLocation] = [
            location for location in self.get_locations() if location.address is not None
        ]

        self.itempool = [self.create_item_by_id(location.default_item_id) for location in item_locations]

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

        # Remove duplicates of unique items from the itempool
        unique_items = set()
        for item in self.itempool.copy():
            if item.name in item_groups["Unique Items"]:
                if item in unique_items:
                    self.itempool.remove(item)
                    self.itempool.append(self.create_item(get_random_item(self, ItemClassification.filler)))
                else:
                    unique_items.add(item)

        filler_items = [item for item in self.itempool if item.classification == ItemClassification.filler and
                        item.name not in item_groups["Unique Items"]]
        self.random.shuffle(filler_items)

        # Add key items that are relevant in Kanto Only to the itempool
        if self.options.kanto_only:
            items_to_add = ["HM06 Rock Smash", "HM07 Waterfall", "Sun Stone"]
            for item_name in items_to_add:
                self.itempool.append(self.create_item(item_name))
                self.itempool.remove(filler_items.pop())

        # Remove copies of unique and progressive items based on how many are in the start inventory
        for item_name, quantity in self.options.start_inventory.value.items():
            if item_name in item_groups["Unique Items"] or item_name in item_groups["Progressive Items"]:
                removed_items_count = 0
                for _ in range(quantity):
                    try:
                        item_to_remove = next(i for i in self.itempool if i.name == item_name)
                        self.itempool.remove(item_to_remove)
                        removed_items_count += 1
                    except StopIteration:
                        break
                while removed_items_count > 0:
                    self.itempool.append(self.create_item(get_random_item(self, ItemClassification.filler)))
                    removed_items_count -= 1

        verify_hm_accessibility(self)
        state = self.get_world_collection_state()

        # Delete evolutions that are not in logic in an all state so that the accessibility check doesn't fail
        evolution_region = self.multiworld.get_region("Evolutions", self.player)
        for location in evolution_region.locations.copy():
            if not location.can_reach(state):
                evolution_region.locations.remove(location)

        # Delete trainersanity locations if there are more than the amount specified in the settings
        if self.options.trainersanity != Trainersanity.special_range_names["none"]:
            locations: List[PokemonFRLGLocation] = self.get_locations()
            trainer_locations = [loc for loc in locations if loc.category == LocationCategory.TRAINERSANITY]
            locs_to_remove = len(trainer_locations) - self.options.trainersanity.value
            if locs_to_remove > 0:
                priority_trainer_locations = [loc for loc in trainer_locations
                                              if loc.name in self.options.priority_locations.value]
                non_priority_trainer_locations = [loc for loc in trainer_locations
                                                  if loc.name not in self.options.priority_locations.value]
                self.random.shuffle(priority_trainer_locations)
                self.random.shuffle(non_priority_trainer_locations)
                trainer_locations = non_priority_trainer_locations + priority_trainer_locations
                for location in trainer_locations:
                    region = location.parent_region
                    region.locations.remove(location)
                    self.itempool.remove(filler_items.pop())
                    locs_to_remove -= 1
                    if locs_to_remove <= 0:
                        break

        if self.options.dexsanity != Dexsanity.special_range_names["none"]:
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
            self.shuffle_badges()
        if self.options.dungeon_entrance_shuffle != DungeonEntranceShuffle.option_off:
            shuffle_entrances(self)
            verify_hm_accessibility(self)

    def shuffle_badges(self) -> None:
        badge_items = []
        badge_items.extend(self.get_pre_fill_items())
        self.pre_fill_items.clear()
        locations: List[PokemonFRLGLocation] = self.get_locations()
        for attempt in range(5):
            badge_locations: List[PokemonFRLGLocation] = [
                loc for loc in locations if loc.category == LocationCategory.BADGE and loc.item is None
            ]
            state = self.get_world_collection_state()
            # Try to place badges with current Pokemon and HM access
            # If it can't, try with guaranteed HM access and fix it later
            if attempt > 1:
                for hm in ["Cut", "Fly", "Surf", "Strength", "Flash", "Rock Smash", "Waterfall"]:
                    state.collect(f"Teach {hm}")
            state.sweep_for_advancements()
            self.random.shuffle(badge_items)
            self.random.shuffle(badge_locations)
            fill_restrictive(self.multiworld, state, badge_locations.copy(), badge_items,
                             single_player_placement=True, lock=True, allow_partial=True, allow_excluded=True)
            if len(badge_items) > 8 - len(badge_locations):
                for location in badge_locations:
                    if location.item:
                        badge_items.append(location.item)
                        location.item = None
                continue
            else:
                break
        else:
            raise FillError(f"Failed to place badges for player {self.player}")
        self.logic.guaranteed_hm_access = False
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
        shop_locations: Dict[int, List[Set[PokemonFRLGLocation]]] = defaultdict(list)
        for sphere in multiworld.get_spheres():
            mon_locations_in_sphere = defaultdict(list)
            shop_locations_in_sphere = defaultdict(set)
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
                    if location.category == LocationCategory.SHOPSANITY:
                        shop_locations_in_sphere[location.player].add(location)
            for key, mon_locations in mon_locations_in_sphere.items():
                found_mons.add(key)
                if len(mon_locations) > 1:
                    mon_locations.sort()
                    for location in mon_locations[1:]:
                        location.item.classification = ItemClassification.useful
            for player, locations in shop_locations_in_sphere.items():
                shop_locations[player].append(locations)
        for world in multiworld.get_game_worlds("Pokemon FireRed and LeafGreen"):
            if world.options.shopsanity:
                world.shop_locations_by_spheres = shop_locations[world.player]
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

        del self.modified_species
        del self.modified_maps
        del self.modified_starters
        del self.modified_events
        del self.modified_legendary_pokemon
        del self.modified_misc_pokemon
        del self.modified_trade_pokemon
        del self.modified_trainers
        del self.modified_tmhm_moves
        del self.modified_moves
        del self.modified_type_damage_categories

    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        if self.options.random_starting_town:
            starting_town = starting_town_map[self.starting_town]
            if starting_town == "Viridian City South" or starting_town == "Three Island Town South":
                starting_town = starting_town[:-6]
            spoiler_handle.write(f"Starting Town:                   {starting_town}\n")
        if self.options.free_fly_location:
            free_fly_location = self.multiworld.get_location("Free Fly Location", self.player)
            spoiler_handle.write(f"Free Fly Location:               {free_fly_location.item.name}\n")
        if self.options.town_map_fly_location:
            town_map_fly_location = self.multiworld.get_location("Town Map Fly Location", self.player)
            spoiler_handle.write(f"Town Map Fly Location:           {town_map_fly_location.item.name}\n")

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        # Add dungeon entrances to the spoiler log if they are shuffled
        if self.options.dungeon_entrance_shuffle != DungeonEntranceShuffle.option_off:
            spoiler_handle.write(f"\n\nDungeon Entrances ({self.multiworld.player_name[self.player]}):\n\n")
            for entrance, exit in self.er_placement_state.pairings:
                if entrance in self.er_spoiler_names:
                    spoiler_handle.write(f"{entrance} <=> {exit}\n")

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
                    if location.item.name.startswith("Missable"):
                        continue
                    pokemon_name = location.item.name.replace("Static ", "")
                    species_locations[pokemon_name].add(location.spoiler_name)

            lines = [f"{species}: {', '.join(sorted(locations))}\n"
                     for species, locations in species_locations.items()]
            lines.sort()
            for line in lines:
                spoiler_handle.write(line)

    def extend_hint_information(self, hint_data):
        if self.options.dexsanity != Dexsanity.special_range_names["none"]:
            species_locations = defaultdict(set)

            for location in self.get_locations():
                assert isinstance(location, PokemonFRLGLocation)
                if location.category in [LocationCategory.EVENT_WILD_POKEMON,
                                         LocationCategory.EVENT_STATIC_POKEMON,
                                         LocationCategory.EVENT_LEGENDARY_POKEMON]:
                    if location.item.name.startswith("Missable"):
                        continue
                    pokemon_name = location.item.name.replace("Static ", "")
                    species_locations[pokemon_name].add(location.spoiler_name)

            hint_data[self.player] = {
                self.location_name_to_id[f"Pokedex - {species}"]: ", ".join(sorted(maps))
                for species, maps in species_locations.items()
            }

    def modify_multidata(self, multidata: Dict[str, Any]):
        multidata["connect_names"][base64.b64encode(self.auth).decode("ascii")] = \
            multidata["connect_names"][self.player_name]

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = self.options.as_dict(
            "game_version",
            "goal",
            "skip_elite_four",
            "kanto_only",
            "shuffle_badges",
            "shuffle_hidden",
            "extra_key_items",
            "shopsanity",
            "famesanity",
            "shuffle_fly_unlocks",
            "pokemon_request_locations",
            "shuffle_running_shoes",
            "shuffle_berry_pouch",
            "shuffle_tm_case",
            "card_key",
            "island_passes",
            "split_teas",
            "gym_keys",
            "itemfinder_required",
            "flash_required",
            "fame_checker_required",
            "remove_badge_requirement",
            "oaks_aide_route_2",
            "oaks_aide_route_10",
            "oaks_aide_route_11",
            "oaks_aide_route_16",
            "oaks_aide_route_15",
            "viridian_city_roadblock",
            "pewter_city_roadblock",
            "modify_world_state",
            "additional_dark_caves",
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
            "provide_hints",
            "death_link"
        )
        slot_data["trainersanity"] = 1 if self.options.trainersanity != Trainersanity.special_range_names["none"] else 0
        slot_data["elite_four_rematch_requirement"] = self.options.elite_four_requirement.value
        slot_data["starting_town"] = data.constants[self.starting_town]
        slot_data["free_fly_location_id"] = self.free_fly_location_id
        slot_data["town_map_fly_location_id"] = self.town_map_fly_location_id
        if self.options.randomize_fly_destinations:
            slot_data["randomize_fly_destinations"] = {}
            for exit in self.get_region("Sky").exits:
                slot_data["randomize_fly_destinations"][exit.name] = exit.connected_region.name
        if self.options.dungeon_entrance_shuffle != DungeonEntranceShuffle.option_off:
            slot_data["dungeon_entrance_shuffle"] = {}
            for source, dest in self.er_placement_state.pairings:
                slot_data["dungeon_entrance_shuffle"][source] = dest
        slot_data["wild_encounters"] = {}
        for location in self.get_locations():
            assert isinstance(location, PokemonFRLGLocation)
            if location.category == LocationCategory.EVENT_WILD_POKEMON:
                national_dex_id = data.species[NAME_TO_SPECIES_ID[location.item.name]].national_dex_number
                if national_dex_id not in slot_data["wild_encounters"]:
                    slot_data["wild_encounters"][national_dex_id] = []
                slot_data["wild_encounters"][national_dex_id].append(location.name)
        slot_data["apworld_version"] = APWORLD_VERSION
        slot_data["poptracker_checksum"] = POPTRACKER_CHECKSUM
        return slot_data

    def create_item(self, name: str) -> "PokemonFRLGItem":
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
        return self.pre_fill_items

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
