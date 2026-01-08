import logging
import pkgutil
from collections import defaultdict
from dataclasses import replace
from threading import Event
from typing import ClassVar, Any

import settings
from BaseClasses import Tutorial, ItemClassification, MultiWorld, CollectionState, Item
from Fill import fill_restrictive, FillError
from worlds.AutoWorld import World, WebWorld
from .breeding import randomize_breeding, can_breed, breeding_is_randomized, get_logically_available_breeding
from .data import PokemonData, TrainerData, MiscData, TMHMData, data as crystal_data, StaticPokemon, \
    MusicData, MoveData, FlyRegion, TradeData, MiscOption, StartingTown, LogicalAccess, EncounterType, EncounterKey, \
    EncounterMon, EvolutionType, TypeData, BugContestEncounter
from .evolution import randomize_evolution, evolution_in_logic, get_logically_available_evolutions
from .item_data import POKEDEX_OFFSET
from .items import PokemonCrystalItem, create_item_label_to_code_map, get_item_classification, ITEM_GROUPS, \
    item_const_name_to_id, item_const_name_to_label, adjust_item_classifications, get_random_filler_item, \
    get_random_ball, place_x_items, PokemonCrystalGlitchedToken
from .level_scaling import perform_level_scaling
from .locations import create_locations, PokemonCrystalLocation, create_location_label_to_id_map, LOCATION_GROUPS
from .misc import randomize_mischief, get_misc_spoiler_log
from .moves import randomize_tms, randomize_move_values, randomize_move_types, cap_hm_move_power, randomize_type_chart, \
    LOGIC_MOVES
from .music import randomize_music
from .options import PokemonCrystalOptions, JohtoOnly, RandomizeBadges, HMBadgeRequirements, FreeFlyLocation, \
    EliteFourRequirement, MtSilverRequirement, RedRequirement, \
    Route44AccessRequirement, RadioTowerRequirement, RequireItemfinder, \
    OPTION_GROUPS, RandomizeFlyUnlocks, Shopsanity, Grasssanity, Goal
from .phone import generate_phone_traps
from .phone_data import PhoneScript
from .pokemon import randomize_pokemon_data, randomize_starters, fill_wild_encounter_locations, fill_trade_locations, \
    randomize_unown_signs, randomize_trade_received_pokemon, randomize_trade_requested_pokemon, \
    get_logically_available_trade_pokemon, randomize_request_pokemon
from .regions import create_regions, setup_free_fly_regions
from .rom import generate_output, PokemonCrystalProcedurePatch
from .rules import set_rules, PokemonCrystalLogic, verify_hm_accessibility
from .sign_data import FRIENDLY_SIGN_NAMES
from .trainers import randomize_trainers
from .universal_tracker import load_ut_slot_data
from .utils import get_free_fly_locations, randomize_starting_town, adjust_options
from .wild import randomize_wild_pokemon, randomize_static_pokemon, get_logically_available_wilds, \
    get_logically_available_statics


class PokemonCrystalSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        description = "Pokemon Crystal (UE) (V1.0 or V1.1) ROM File"
        copy_to = "Pokemon - Crystal Version (UE) [C][!].gbc"
        md5s = PokemonCrystalProcedurePatch.hash

    class OptionOverrides(dict):
        """
        Provided options will be used as overrides when patching.
        Pass the options as you would in an options yaml. (Option weights and triggers are not supported)
        Always available option overrides: trainer_name, game_options, field_move_menu_order, default_pokedex_mode
        Option overrides available when race mode is off: shopsanity_restrict_rare_candies, encounter_slot_distribution, reusable_tms, minimum_catch_rate, skip_elite_four, better_marts, build_a_mart, experience_modifier, starting_money, all_pokemon_seen

        example:
        option_overrides:
          experience_modifier: triple
          trainer_name: CHRIS
          game_options:
            turbo_button: a
            low_hp_beep: off
        """

    rom_file: RomFile = RomFile(RomFile.copy_to)
    option_overrides = {}

    class MaximumFillerTrapPercentage(int):
        """
        The maximum allowed filler_trap_percentage
        """

    maximum_filler_trap_percentage = MaximumFillerTrapPercentage(20)


class PokemonCrystalWebWorld(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Pokemon Crystal with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["AliceMousie", "gerbiljames"]
    )]

    option_groups = OPTION_GROUPS


class PokemonCrystalWorld(World):
    """Pokémon Crystal is the culmination of the Generation I and II Pokémon games.
    Explore the Johto and Kanto regions, become the Pokémon League Champion, and
    defeat the elusive Red at the peak of Mt. Silver!"""
    game = crystal_data.manifest.game
    apworld_version = crystal_data.manifest.pokemon_crystal_version

    topology_present = True
    web = PokemonCrystalWebWorld()

    ut_can_gen_without_yaml = True
    glitches_item_name = PokemonCrystalGlitchedToken.TOKEN_NAME
    is_universal_tracker: bool

    settings_key = "pokemon_crystal_settings"
    settings: ClassVar[PokemonCrystalSettings]

    options_dataclass = PokemonCrystalOptions
    options: PokemonCrystalOptions

    required_client_version = (0, 6, 0)

    item_name_to_id = create_item_label_to_code_map()
    location_name_to_id = create_location_label_to_id_map()
    item_name_groups = ITEM_GROUPS  # item_groups
    location_name_groups = LOCATION_GROUPS  # location groups

    auth: bytes

    free_fly_location: FlyRegion
    map_card_fly_location: FlyRegion

    starting_town: StartingTown

    generated_moves: dict[str, MoveData]
    generated_types: dict[str, TypeData]
    generated_pokemon: dict[str, PokemonData]

    generated_trainers: dict[str, TrainerData]

    generated_tms: dict[str, TMHMData]
    generated_wild: dict[EncounterKey, list[EncounterMon]]
    generated_static: dict[EncounterKey, StaticPokemon]
    generated_trades: dict[str, TradeData]
    generated_contest: list[BugContestEncounter]

    generated_dexsanity: set[str]
    generated_dexcountsanity: list[int]
    generated_wooper: str
    generated_starters: tuple[list[str], list[str], list[str]]
    generated_starter_helditems: tuple[str, str, str]
    generated_palettes: dict[str, list[int]]
    generated_request_pokemon: list[str]
    generated_unown_signs: dict[str, str]

    generated_music: MusicData
    generated_misc: MiscData

    generated_phone_traps: list[PhoneScript]
    generated_phone_indices: list[int]

    trainer_name_list: list[str]
    trainer_level_list: list[int]
    trainer_name_level_dict: dict[str, int]
    static_name_list: list[str]
    static_level_list: list[int]
    encounter_region_name_list: list[str]
    encounter_region_levels_list = list[int]

    shop_locations_by_spheres: list[set[PokemonCrystalLocation]]

    itempool: list[PokemonCrystalItem]
    pre_fill_items: list[PokemonCrystalItem]
    logic: PokemonCrystalLogic

    filler_pool: list[list[str]]
    grass_location_mapping: dict[str, int]

    finished_level_scaling: Event

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.generated_moves = dict(crystal_data.moves)
        self.generated_types = dict(crystal_data.types)
        self.generated_pokemon = dict(crystal_data.pokemon)
        self.generated_trainers = dict(crystal_data.trainers)
        self.generated_tms = dict(crystal_data.tmhm)
        self.generated_wild = {key: list(encounters) for key, encounters in crystal_data.wild.items()}
        self.generated_static = dict(crystal_data.static)
        self.generated_trades = dict(crystal_data.trades)
        self.generated_contest = list(crystal_data.bug_contest_encounters)
        self.generated_dexsanity = set()
        self.generated_dexcountsanity = []
        self.generated_wooper = "WOOPER"
        self.generated_starters = (["CYNDAQUIL", "QUILAVA", "TYPHLOSION"],
                                   ["TOTODILE", "CROCONAW", "FERALIGATR"],
                                   ["CHIKORITA", "BAYLEEF", "MEGANIUM"])
        self.generated_starter_helditems = ("BERRY", "BERRY", "BERRY")
        self.generated_palettes = {}
        self.generated_request_pokemon = list(crystal_data.request_pokemon)
        self.generated_music = replace(crystal_data.music)
        self.generated_misc = replace(crystal_data.misc)
        self.generated_phone_traps = []
        self.generated_phone_indices = []
        self.generated_unown_signs = {}

        self.trainer_name_list = []
        self.trainer_level_list = []
        self.trainer_name_level_dict = {}
        self.static_name_list = []
        self.static_level_list = []
        self.encounter_region_name_list = []
        self.encounter_region_levels_list = []

        self.shop_locations_by_spheres = []

        self.itempool = []
        self.pre_fill_items = []
        self.filler_pool = []
        self.grass_location_mapping = {}

        self.finished_level_scaling = Event()

        self.is_universal_tracker = hasattr(self.multiworld, "generation_is_fake")

    def generate_early(self) -> None:
        adjust_options(self)
        load_ut_slot_data(self)
        randomize_mischief(self)
        self.logic = PokemonCrystalLogic(self)

        if not self.is_universal_tracker:
            if self.options.early_fly:
                self.multiworld.local_early_items[self.player]["HM02 Fly"] = 1
                if (self.options.hm_badge_requirements.value != HMBadgeRequirements.option_no_badges
                        and "Fly" not in self.options.remove_badge_requirement.value
                        and self.options.randomize_badges == RandomizeBadges.option_completely_random):
                    self.multiworld.local_early_items[self.player]["Storm Badge"] = 1

            randomize_move_types(self)
            randomize_pokemon_data(self)
            randomize_unown_signs(self)

        self.logic.set_hm_compatible_pokemon(self)

    def create_regions(self) -> None:

        randomize_starting_town(self)
        regions = create_regions(self)

        preevolutions = randomize_evolution(self)
        randomize_breeding(self, preevolutions)

        randomize_starters(self)
        randomize_wild_pokemon(self)
        randomize_static_pokemon(self)

        self.logic.available_pokemon.update(get_logically_available_wilds(self))
        self.logic.available_pokemon.update(get_logically_available_statics(self))

        previous_logically_available_pokemon_count = 0
        while previous_logically_available_pokemon_count != len(self.logic.available_pokemon):
            previous_logically_available_pokemon_count = len(self.logic.available_pokemon)
            self.logic.available_pokemon.update(get_logically_available_evolutions(self))
            self.logic.available_pokemon.update(get_logically_available_breeding(self))

        randomize_trade_requested_pokemon(self)
        randomize_trade_received_pokemon(self)

        self.logic.available_pokemon.update(get_logically_available_trade_pokemon(self))

        randomize_request_pokemon(self)

        create_locations(self, regions)
        self.multiworld.regions.extend(regions.values())

        if self.options.free_fly_location:
            if not self.is_universal_tracker:
                get_free_fly_locations(self)
            setup_free_fly_regions(self)

    def create_items(self) -> None:

        item_locations = [
            location
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None and location.address < POKEDEX_OFFSET
        ]

        if self.options.randomize_badges == RandomizeBadges.option_shuffle:
            self.pre_fill_items.extend(
                self.create_item_by_code(loc.default_item_code) for loc in item_locations if "Badge" in loc.tags)
            item_locations = [location for location in item_locations if "Badge" not in location.tags]

        if (self.options.randomize_fly_unlocks == RandomizeFlyUnlocks.option_exclude_silver_cave
                and self.options.johto_only.value != JohtoOnly.option_on):
            item_locations = [location for location in item_locations if location.name != "Visit Silver Cave"]

        badge_option_counts = [8]
        if self.options.radio_tower_requirement == RadioTowerRequirement.option_badges:
            badge_option_counts.append(self.options.radio_tower_count.value)
        if self.options.elite_four_requirement == EliteFourRequirement.option_badges:
            badge_option_counts.append(self.options.elite_four_count.value)
        if self.options.route_44_access_requirement == Route44AccessRequirement.option_badges:
            badge_option_counts.append(self.options.route_44_access_count.value)

        if self.options.johto_only == JohtoOnly.option_include_silver_cave:
            if self.options.mt_silver_requirement == MtSilverRequirement.option_badges:
                badge_option_counts.append(self.options.mt_silver_count.value)
            if self.options.red_requirement == RedRequirement.option_badges:
                badge_option_counts.append(self.options.red_count.value)

        required_badges = max(badge_option_counts)

        add_items = []
        # Extra badges to add to the pool in johto only
        if self.options.johto_only and required_badges > 8:
            kanto_badges = [item_data.item_const for item_data in crystal_data.items.values() if
                            "KantoBadge" in item_data.tags]
            self.random.shuffle(kanto_badges)
            add_items.extend(kanto_badges[:required_badges - 8])

        if self.options.johto_only:
            if self.options.progressive_rods:
                add_items.append("PROG_ROD")
            else:
                add_items.append("SUPER_ROD")

        if Shopsanity.blue_card in self.options.shopsanity.value:
            add_items.extend(["BLUE_CARD_PT"] * 5)

        if Shopsanity.apricorns in self.options.shopsanity.value and not self.options.randomize_berry_trees:
            add_items.extend(
                ["RED_APRICORN", "GRN_APRICORN", "BLU_APRICORN", "YLW_APRICORN", "PNK_APRICORN", "BLK_APRICORN",
                 "WHT_APRICORN"])

        if self.options.goal == Goal.option_unown_hunt:
            add_items.extend(["KABUTO_TILE"] * 16)
            add_items.extend(["OMANYTE_TILE"] * 16)
            add_items.extend(["AERO_TILE"] * 16)
            add_items.extend(["HO_OH_TILE"] * 16)

        if self.options.add_missing_useful_items:
            add_items.extend(["TM_9", "TWISTEDSPOON", "THICK_CLUB", "BRIGHTPOWDER", "STICK", "LUCKY_PUNCH",
                              "LIGHT_BALL", "METAL_POWDER"])

            if Shopsanity.game_corners not in self.options.shopsanity.value:
                add_items.extend(["TM_14", "TM_15", "TM_25", "TM_32", "TM_38"])

            if self.options.johto_only != JohtoOnly.option_off:
                add_items.extend(["TM_3", "TM_6", "TM_7", "TM_17", "TM_19", "TM_29", "TM_42", "TM_47"])

        for location in item_locations:
            item_code = location.default_item_code
            if item_code > 0:
                self.itempool.append(self.create_item_by_code(item_code))
            else:  # item is NO_ITEM, trainersanity checks
                self.itempool.append(self.create_item_by_const_name(get_random_filler_item(self)))

        if self.options.dexsanity:
            self.itempool.extend(
                self.create_item_by_const_name(get_random_ball(self.random))
                for _ in self.generated_dexsanity)

        if self.generated_dexcountsanity:
            self.itempool.extend(
                self.create_item_by_const_name(get_random_ball(self.random))
                for _ in self.generated_dexcountsanity)

        if self.options.grasssanity:
            self.itempool.extend(
                self.create_item_by_const_name("GRASS_ITEM")
                for _ in [loc for loc in self.multiworld.get_locations(self.player) if "grass" in loc.tags])

        if self.options.johto_only.value != JohtoOnly.option_off:
            # Replace the S.S. Ticket with the Silver Wing for Johto only seeds
            self.itempool = [item if item.name != "S.S. Ticket" else self.create_item_by_const_name("SILVER_WING")
                             for item in self.itempool]

        if self.options.progressive_rods:
            self.itempool = [
                item if item.name not in ("Old Rod", "Good Rod", "Super Rod") else self.create_item_by_const_name(
                    "PROG_ROD") for item in self.itempool]

        x_items_to_remove = place_x_items(self)
        if x_items_to_remove:
            filtered_itempool = []
            for item in self.itempool:
                if item.name in x_items_to_remove:
                    x_items_to_remove.remove(item.name)
                    continue
                filtered_itempool.append(item)
            self.itempool = filtered_itempool

        adjust_item_classifications(self)

        trap_names, trap_weights = zip(
            ("Phone Trap", self.options.phone_trap_weight.value),
            ("Sleep Trap", self.options.sleep_trap_weight.value),
            ("Poison Trap", self.options.poison_trap_weight.value),
            ("Burn Trap", self.options.burn_trap_weight.value),
            ("Freeze Trap", self.options.freeze_trap_weight.value),
            ("Paralysis Trap", self.options.paralysis_trap_weight.value),
        )
        total_trap_weight = self.options.filler_trap_percentage.value if any(trap_weights) else 0

        for i in range(len(self.itempool)):
            if self.itempool[i].classification == ItemClassification.filler:
                if add_items:
                    self.itempool[i] = self.create_item_by_const_name(add_items.pop())
                elif total_trap_weight and self.random.randint(0, 100) <= total_trap_weight:
                    self.itempool[i] = self.create_item(self.random.choices(trap_names, trap_weights)[0])

        adjust_item_classifications(self)

        self.multiworld.itempool.extend(self.itempool)

    def set_rules(self) -> None:
        set_rules(self)

    def generate_basic(self) -> None:
        fill_wild_encounter_locations(self)
        fill_trade_locations(self)

        if self.is_universal_tracker: return

        if not self.options.field_moves_always_usable:
            verify_hm_accessibility(self)
        randomize_move_values(self)
        cap_hm_move_power(self)
        randomize_music(self)
        randomize_tms(self)
        randomize_type_chart(self)

        self.auth = self.random.randbytes(16)

    def pre_fill(self) -> None:

        if self.is_universal_tracker: return

        if (self.options.randomize_fly_unlocks == RandomizeFlyUnlocks.option_exclude_silver_cave
                and self.options.johto_only != JohtoOnly.option_on):
            self.get_location("Visit Silver Cave").place_locked_item(self.create_item_by_const_name("FLY_SILVER_CAVE"))
        if self.options.randomize_badges == RandomizeBadges.option_shuffle:
            badge_items = []
            badge_items.extend(self.pre_fill_items)
            self.pre_fill_items.clear()

            if self.options.early_fly and "Fly" not in self.options.remove_badge_requirement.value:
                early_badge_locs = [loc for loc in
                                    self.multiworld.get_reachable_locations(self.multiworld.state, self.player) if
                                    "Badge" in loc.tags]
                # take one of the early badge locations, set it to storm badge
                if early_badge_locs:
                    storm_loc = self.random.choice(early_badge_locs)
                    storm_badge = next(item for item in badge_items if item.name == "Storm Badge")
                    storm_loc.place_locked_item(storm_badge)
                    badge_items.remove(storm_badge)

            # If we can't do this in 5 attempts then just accept our fate
            for attempt in range(5):
                if attempt >= 1:
                    self.logic.guaranteed_hm_access = True
                state = self.get_world_collection_state()

                attempt_locs = [loc for loc in self.multiworld.get_locations(self.player) if
                                "Badge" in loc.tags and not loc.item]
                attempt_items = badge_items.copy()
                self.random.shuffle(attempt_locs)
                self.random.shuffle(attempt_items)
                fill_restrictive(self.multiworld, state, attempt_locs.copy(), attempt_items,
                                 single_player_placement=True, lock=True, allow_excluded=True, allow_partial=True)
                if not attempt_items:
                    break

                if attempt >= 4:
                    raise FillError(
                        f"Failed to shuffle badges for player {self.player} ({self.player_name}). Aborting.")

                for location in attempt_locs:
                    location.locked = False
                    if location.item is not None:
                        location.item.location = None
                        location.item = None

                logging.debug(f"Failed to shuffle badges for player {self.player} ({self.player_name}). Retrying.")

            self.logic.guaranteed_hm_access = False
            if not self.options.field_moves_always_usable:
                verify_hm_accessibility(self)

    @classmethod
    def stage_generate_output(cls, multiworld: MultiWorld, output_directory: str):
        shop_locations: dict[int, list[set[PokemonCrystalLocation]]] = defaultdict(list)

        exclude_shops = ("REGION_MART_BLUE_CARD", "REGION_MART_GOLDENROD_GAME_CORNER",
                         "REGION_MART_CELADON_GAME_CORNER_PRIZE_ROOM", "REGION_MART_KURTS_BALLS")
        for sphere in multiworld.get_spheres():
            shop_locations_in_sphere = defaultdict(set)
            for location in sphere:
                if location.game == cls.game:
                    assert isinstance(location, PokemonCrystalLocation)
                    if "shopsanity" in location.tags and location.parent_region.name not in exclude_shops:
                        shop_locations_in_sphere[location.player].add(location)

            for player, locations in shop_locations_in_sphere.items():
                shop_locations[player].append(locations)

        for world in multiworld.get_game_worlds(cls.game):
            if world.options.shopsanity:
                world.shop_locations_by_spheres = shop_locations[world.player]

        perform_level_scaling(multiworld)

    def generate_output(self, output_directory: str) -> None:
        generate_phone_traps(self)
        self.finished_level_scaling.wait()

        randomize_trainers(self)

        patch = PokemonCrystalProcedurePatch(player=self.player, player_name=self.player_name)
        patch.write_file("basepatch.bsdiff4", pkgutil.get_data(__name__, "data/basepatch.bsdiff4"))
        patch.write_file("basepatch11.bsdiff4", pkgutil.get_data(__name__, "data/basepatch11.bsdiff4"))
        generate_output(self, output_directory, patch)

    def fill_slot_data(self) -> dict[str, Any]:
        slot_data = self.options.as_dict(
            "goal",
            "johto_only",
            "elite_four_requirement",
            "elite_four_count",
            "red_requirement",
            "red_count",
            "randomize_badges",
            "dexsanity",
            "randomize_pokegear",
            "hm_badge_requirements",
            "randomize_berry_trees",
            "remove_ilex_cut_tree",
            "radio_tower_requirement",
            "radio_tower_count",
            "route_44_access_requirement",
            "route_44_access_count",
            "route_32_condition",
            "mt_silver_requirement",
            "mt_silver_count",
            "east_west_underground",
            "undergrounds_require_power",
            "red_gyarados_access",
            "route_2_access",
            "blackthorn_dark_cave_access",
            "national_park_access",
            "kanto_access_requirement",
            "kanto_access_count",
            "route_3_access",
            "vanilla_clair",
            "static_pokemon_required",
            "breeding_methods_required",
            "evolution_gym_levels",
            "rematchsanity",
            "all_pokemon_seen",
            "dexcountsanity_leniency",
            "dexcountsanity_step",
            "provide_shop_hints",
            "randomize_fly_unlocks",
            "fly_cheese",
            "route_42_access",
            "mount_mortar_access",
            "randomize_pokemon_requests",
            "randomize_evolution",
            "randomize_breeding",
            "dark_areas",
            "require_flash",
            "victory_road_access",
            "lock_kanto_gyms",
            "randomize_starting_town",
            "saffron_gatehouse_tea",
            "shopsanity",
            "wild_encounter_methods_required",
            "evolution_methods_required",
            "remove_badge_requirement",
            "johto_trainersanity",
            "kanto_trainersanity",
            "randomize_hidden_items",
            "require_itemfinder",
            "skip_elite_four",
            "field_moves_always_usable",
            "grasssanity",
            "enforce_wild_encounter_methods_logic",
            "randomize_trades",
            "trades_required",
            "trap_link",
            "randomize_bug_catching_contest",
            "randomize_phone_call_items",
            "progressive_rods",
            "add_missing_useful_items",
            "ss_aqua_access",
            "magnet_train_access",
            "route_12_access",
            "route_30_battle",
            "require_pokegear_for_phone_numbers",
        )
        slot_data["apworld_version"] = self.apworld_version
        slot_data["tea_north"] = 1 if "North" in self.options.saffron_gatehouse_tea.value else 0
        slot_data["tea_east"] = 1 if "East" in self.options.saffron_gatehouse_tea.value else 0
        slot_data["tea_south"] = 1 if "South" in self.options.saffron_gatehouse_tea.value else 0
        slot_data["tea_west"] = 1 if "West" in self.options.saffron_gatehouse_tea.value else 0
        slot_data["dexsanity_count"] = len(self.generated_dexsanity)
        slot_data["dexsanity_pokemon"] = [self.generated_pokemon[poke].id for poke in self.generated_dexsanity]
        slot_data["logically_available_pokemon_count"] = len(self.logic.available_pokemon)

        region_encounters = dict[str, set[int]]()
        for encounter_key, encounters in self.generated_wild.items():
            region_encounters[encounter_key.region_name()] = {self.generated_pokemon[enc.pokemon].id for enc in
                                                              encounters}

        for encounter_key, encounter in self.generated_static.items():
            region_encounters[encounter_key.region_name()] = {self.generated_pokemon[encounter.pokemon].id}

        slot_data["region_encounters"] = region_encounters

        slot_data["contest_encounters"] = [self.generated_pokemon[slot.pokemon].id for slot in self.generated_contest]

        for hm in [key for key in self.options.remove_badge_requirement.valid_keys if key not in ("_All", "_Random")]:
            slot_data["free_" + hm.lower()] = 1 if hm in self.options.remove_badge_requirement.value else 0

        slot_data["free_fly_location_option"] = self.options.free_fly_location.value
        slot_data["free_fly_location"] = 0
        slot_data["map_card_fly_location"] = 0

        if self.options.free_fly_location.value in (FreeFlyLocation.option_free_fly,
                                                    FreeFlyLocation.option_free_fly_and_map_card):
            slot_data["free_fly_location"] = self.free_fly_location.id

        if self.options.free_fly_location.value in (FreeFlyLocation.option_free_fly_and_map_card,
                                                    FreeFlyLocation.option_map_card):
            slot_data["map_card_fly_location"] = self.map_card_fly_location.id

        slot_data["enable_mischief"] = 1 if (self.options.enable_mischief
                                             and MiscOption.SecretSwitch.value in self.generated_misc.selected) else 0

        slot_data["starting_town"] = 0
        if self.options.randomize_starting_town:
            slot_data["starting_town"] = self.starting_town.id

        slot_data["dexcountsanity"] = self.generated_dexcountsanity[-1] if self.generated_dexcountsanity else 0
        slot_data["dexcountsanity_checks"] = len(self.generated_dexcountsanity)
        slot_data["dexcountsanity_counts"] = self.generated_dexcountsanity

        ool_encounter_method = 1 if self.options.enforce_wild_encounter_methods_logic else 0

        slot_data["encmethod_land"] = 2 if "Land" in self.options.wild_encounter_methods_required \
            else ool_encounter_method
        slot_data["encmethod_water"] = 2 if "Surfing" in self.options.wild_encounter_methods_required \
            else ool_encounter_method
        slot_data["encmethod_fishing"] = 2 if "Fishing" in self.options.wild_encounter_methods_required \
            else ool_encounter_method
        slot_data["encmethod_headbutt"] = 2 if "Headbutt" in self.options.wild_encounter_methods_required \
            else ool_encounter_method
        slot_data["encmethod_rocksmash"] = 2 if "Rock Smash" in self.options.wild_encounter_methods_required \
            else ool_encounter_method
        slot_data["encmethod_contest"] = 2 if "Bug Catching Contest" in self.options.wild_encounter_methods_required \
            else 0

        slot_data["evomethod_happiness"] = 1 if "Happiness" in self.options.evolution_methods_required else 0
        slot_data["evomethod_level"] = 1 if "Level" in self.options.evolution_methods_required else 0
        slot_data["evomethod_tyrogue"] = 1 if "Level Tyrogue" in self.options.evolution_methods_required else 0
        slot_data["evomethod_useitem"] = 1 if "Use Item" in self.options.evolution_methods_required else 0

        if not self.options.randomize_hidden_items:
            if not self.options.require_itemfinder:
                hidden_items_setting = 0
            elif self.options.require_itemfinder.value == RequireItemfinder.option_logically_required:
                hidden_items_setting = 1
            else:
                hidden_items_setting = 2
        else:
            if not self.options.require_itemfinder:
                hidden_items_setting = 3
            elif self.options.require_itemfinder.value == RequireItemfinder.option_logically_required:
                hidden_items_setting = 4
            else:
                hidden_items_setting = 5

        slot_data["hiddenitem_logic"] = hidden_items_setting
        slot_data["trainersanity"] = [loc.address for loc in self.get_locations() if "Trainersanity" in loc.tags]

        slot_data["shopsanity_apricorn"] = 1 if Shopsanity.apricorns in self.options.shopsanity.value else 0
        slot_data["shopsanity_bluecard"] = 1 if Shopsanity.blue_card in self.options.shopsanity.value else 0
        slot_data["shopsanity_gamecorners"] = 1 if Shopsanity.game_corners in self.options.shopsanity.value else 0
        slot_data["shopsanity_johtomarts"] = 1 if Shopsanity.johto_marts in self.options.shopsanity.value else 0
        slot_data["shopsanity_kantomarts"] = 1 if Shopsanity.kanto_marts in self.options.shopsanity.value else 0

        evolution_data = dict[int, list[dict]]()
        for pokemon_id, pokemon_data in self.generated_pokemon.items():
            evo_data = list()
            for evo in pokemon_data.evolutions:
                evo_data.append({
                    "into": self.generated_pokemon[evo.pokemon].id,
                    "method": str(evo.evo_type),
                    "level": evo.level,
                    "condition": evo.level if evo.evo_type is EvolutionType.Level else evo.condition
                })
            if evo_data: evolution_data[self.generated_pokemon[pokemon_id].id] = evo_data
        slot_data["evolution_info"] = evolution_data

        breeding_data = dict()
        for pokemon_id, pokemon_data in self.generated_pokemon.items():
            if not can_breed(self, pokemon_id): continue
            breeding_data[pokemon_data.id] = self.generated_pokemon[pokemon_data.produces_egg].id
        slot_data["breeding_info"] = breeding_data

        slot_data["request_pokemon"] = [self.generated_pokemon[poke].id for poke in self.generated_request_pokemon]

        hm_compat = dict[int, set[int]]()
        for pokemon_data in self.generated_pokemon.values():
            hm_compat[pokemon_data.id] = {
                index for index, move in enumerate(LOGIC_MOVES) if move in pokemon_data.tm_hm
            }
        slot_data["hm_compat"] = hm_compat

        slot_data["grass_location_mapping"] = self.grass_location_mapping

        slot_data["trades"] = {
            trade_id: {"requested": str(self.generated_pokemon[trade.requested_pokemon].id), "received": str(
                self.generated_pokemon[trade.received_pokemon].id)} for trade_id, trade in
            self.generated_trades.items()}

        slot_data["trap_weights"] = {
            "Phone Trap": self.options.phone_trap_weight.value,
            "Sleep Trap": self.options.sleep_trap_weight.value,
            "Burn Trap": self.options.burn_trap_weight.value,
            "Freeze Trap": self.options.freeze_trap_weight.value,
            "Poison Trap": self.options.poison_trap_weight.value,
            "Paralysis Trap": self.options.paralysis_trap_weight.value,
        }

        if not self.options.remote_items and self.options.filler_trap_percentage:
            slot_data["trap_locations"] = {str(location.address): location.item.code for location in
                                           self.get_locations() if
                                           location.item.player == self.player and ("Trap" in location.item.tags)}

        slot_data["unown_signs"] = self.generated_unown_signs

        return slot_data

    def modify_multidata(self, multidata: dict[str, Any]):
        import base64
        multidata["connect_names"][base64.b64encode(self.auth).decode("ascii")] \
            = multidata["connect_names"][self.player_name]

    def write_spoiler(self, spoiler_handle) -> None:
        spoiler_handle.write(f"\nPokemon Crystal ({self.player_name}):\n")

        if self.options.goal == Goal.option_diploma:
            available_pokemon = len(self.logic.available_pokemon)
            spoiler_handle.write(f"Diploma requirement: {available_pokemon}\n species")

        if self.options.goal == Goal.option_unown_hunt:
            spoiler_handle.write("Unown locations:\n")
            for sign, unown in self.generated_unown_signs.items():
                sign_friendly_name = FRIENDLY_SIGN_NAMES[sign]
                spoiler_handle.write(f"{sign_friendly_name}: {unown.replace('_', ' ')}\n")
            spoiler_handle.write("\n")

        if self.options.randomize_starters:
            spoiler_handle.write("Starters: ")
            spoiler_handle.write(
                ", ".join([self.generated_pokemon[line[0]].friendly_name for line in self.generated_starters]))
            spoiler_handle.write("\n")

        if self.options.free_fly_location.value in (FreeFlyLocation.option_free_fly,
                                                    FreeFlyLocation.option_free_fly_and_map_card):
            spoiler_handle.write(f"Free Fly Location: {self.free_fly_location.name}\n")

        if self.options.free_fly_location.value in (FreeFlyLocation.option_free_fly_and_map_card,
                                                    FreeFlyLocation.option_map_card):
            spoiler_handle.write(f"Map Card Fly Location: {self.map_card_fly_location.name}\n")

        if self.options.randomize_starting_town:
            spoiler_handle.write(f"Starting Town: {self.starting_town.name}\n")

        encounters_per_pokemon = defaultdict(list)
        if self.options.randomize_wilds:
            for key, encounters in self.generated_wild.items():
                if key.encounter_type == EncounterType.Fish and key.region_id.startswith("Remoraid"):
                    # The Remoraid table is only for GS, not Crystal
                    continue
                friendly_region_name = key.friendly_region_name()
                for encounter in encounters:
                    if friendly_region_name not in encounters_per_pokemon[encounter.pokemon]:
                        encounters_per_pokemon[encounter.pokemon].append(friendly_region_name)
            for slot in self.generated_contest:
                encounters_per_pokemon[slot.pokemon].append("Bug Catching Contest")
        if self.options.randomize_static_pokemon:
            for key, static in self.generated_static.items():
                if static.level_type == "ignore" or \
                        key.friendly_region_name() in encounters_per_pokemon[static.pokemon]:
                    continue
                encounters_per_pokemon[static.pokemon].append(key.friendly_region_name())
        else:
            key = EncounterKey.static("OddEgg")
            odd_egg = self.generated_static[key]
            encounters_per_pokemon[odd_egg.pokemon].append(key.friendly_region_name())

        if encounters_per_pokemon:
            spoiler_handle.write(f"\nRandomized Pokemon ({self.player_name}):\n")
            lines = [f"{self.generated_pokemon[pokemon_id].friendly_name}: {', '.join(locations)}\n"
                     for pokemon_id, locations in encounters_per_pokemon.items()]
            lines.sort()
            for line in lines:
                spoiler_handle.write(line)

        if self.options.randomize_evolution:
            spoiler_handle.write(f"\nEvolutions ({self.player_name}):\n")

            for pokemon_id, pokemon_data in self.generated_pokemon.items():
                for evo in pokemon_data.evolutions:
                    pokemon_name = self.generated_pokemon[pokemon_id].friendly_name
                    evo_name = self.generated_pokemon[evo.pokemon].friendly_name
                    spoiler_handle.write(f"{pokemon_name} -> {evo.method} -> {evo_name}\n")

        if breeding_is_randomized(self):
            spoiler_handle.write(f"\nBreeding ({self.player_name}):\n")
            for pokemon, data in self.generated_pokemon.items():
                if not can_breed(self, pokemon): continue
                parent_name = self.generated_pokemon[pokemon].friendly_name
                child_name = self.generated_pokemon[data.produces_egg].friendly_name
                if child_name == "Nidoran F": child_name = "Nidoran F/Nidoran M"
                spoiler_handle.write(f"{parent_name} -> {child_name}\n")

        if self.options.randomize_pokemon_requests:
            request_pokemon = ", ".join(
                self.generated_pokemon[pokemon].friendly_name for pokemon in self.generated_request_pokemon)
            spoiler_handle.write(f"\nBill's Grandpa Pokemon ({self.player_name}): {request_pokemon}\n")

        if self.options.randomize_trades:
            spoiler_handle.write(f"\nTrades ({self.player_name}):\n")
            for trade in self.generated_trades.values():
                requested = self.generated_pokemon[trade.requested_pokemon].friendly_name
                received = self.generated_pokemon[trade.received_pokemon].friendly_name
                spoiler_handle.write(f"{trade.friendly_name}: {requested} -> {received}\n")

        if self.options.grasssanity == Grasssanity.option_one_per_area:
            spoiler_handle.write(f"\nGrass locations ({self.player_name}):\n")
            for loc_id in self.grass_location_mapping.keys():
                spoiler_handle.write(f"{self.location_id_to_name[int(loc_id)]}\n")

        if self.options.enable_mischief:
            spoiler_handle.write(f"\nMischief ({self.player_name}):\n")
            get_misc_spoiler_log(self, spoiler_handle.write)

    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]):

        def get_dexsanity_wild_hint_data(dexsanity_hint_data: dict[str, set[str]]):
            for key, encounters in self.generated_wild.items():
                if (self.logic.wild_regions[key] is not LogicalAccess.InLogic) or \
                        (key.encounter_type == EncounterType.Fish and
                         (key.region_id.startswith("Remoraid") or key.region_id.endswith("_Swarm"))):
                    continue
                friendly_region_name = key.friendly_region_name()
                if MiscOption.WhirlDexLocations in self.generated_misc.selected and friendly_region_name.startswith(
                        "Whirl"):
                    friendly_region_name = friendly_region_name.replace(" N" if " N" in friendly_region_name else " S",
                                                                        " S" if " N" in friendly_region_name else " N") \
                        .replace("W " if "W " in friendly_region_name else "E ",
                                 "E " if "W " in friendly_region_name else "W ")
                for encounter in encounters:
                    if encounter.pokemon not in self.generated_dexsanity:
                        continue
                    dexsanity_hint_data[encounter.pokemon].add(friendly_region_name)

        def get_dexsanity_static_hint_data(dexsanity_hint_data: dict[str, set[str]]):
            for key, static in self.generated_static.items():
                if static.pokemon not in self.generated_dexsanity or static.level_type == "ignore" or \
                        key.region_id in ["Entei", "Raikou"]:
                    continue
                dexsanity_hint_data[static.pokemon].add(key.friendly_region_name())

        def get_dexsanity_evolution_hint_data(dexsanity_hint_data: dict[str, set[str]]):
            for pokemon_id, pokemon_data in self.generated_pokemon.items():
                for evo in pokemon_data.evolutions:
                    if not (evo.pokemon in self.generated_dexsanity and evolution_in_logic(self, evo)):
                        continue
                    hint_text = f"Evolve {self.generated_pokemon[pokemon_id].friendly_name}"
                    divergent_evolutions = ("EEVEE", "GLOOM", "POLIWHIRL", "SLOWPOKE", "TYROGUE")
                    if pokemon_id in divergent_evolutions:
                        hint_text += f" ({evo.method})"
                    dexsanity_hint_data[evo.pokemon].add(hint_text)

        def get_dexsanity_breeding_hint_data(dexsanity_hint_data: dict[str, set[str]]):
            for parent, data in self.generated_pokemon.items():
                if not can_breed(self, parent): continue
                child = data.produces_egg
                parent_name = self.generated_pokemon[parent].friendly_name
                if child == "NIDORAN_F" and parent != "NIDORAN_M" and "NIDORAN_M" in self.generated_dexsanity:
                    dexsanity_hint_data["NIDORAN_M"].add(f"Breed {parent_name}")
                if parent == child: continue
                if child in self.generated_dexsanity:
                    dexsanity_hint_data[child].add(f"Breed {parent_name}")

        def get_dexsanity_trade_hint_data(dexsanity_hint_data: dict[str, set[str]]):
            for trade in self.generated_trades.values():
                requested = self.generated_pokemon[trade.requested_pokemon].friendly_name
                dexsanity_hint_data[trade.received_pokemon].add(f"{trade.friendly_name} - Trade for {requested}")

        player_hint_data = dict()
        if self.options.dexsanity:
            dexsanity_hint_data = defaultdict(set)
            get_dexsanity_wild_hint_data(dexsanity_hint_data)
            if self.options.static_pokemon_required:
                get_dexsanity_static_hint_data(dexsanity_hint_data)
            if self.options.randomize_evolution:
                get_dexsanity_evolution_hint_data(dexsanity_hint_data)
            if self.options.breeding_methods_required and breeding_is_randomized(self):
                get_dexsanity_breeding_hint_data(dexsanity_hint_data)
            get_dexsanity_trade_hint_data(dexsanity_hint_data)
            player_hint_data |= {
                self.location_name_to_id[f"Pokedex - {self.generated_pokemon[pokemon_id].friendly_name}"]: ", ".join(
                    methods)
                for pokemon_id, methods in dexsanity_hint_data.items()}

        hint_data[self.player] = player_hint_data

    def create_item(self, name: str) -> Item:
        if name == self.glitches_item_name: return PokemonCrystalGlitchedToken(self.player)
        return self.create_item_by_code(self.item_name_to_id[name])

    def get_filler_item_name(self) -> str:
        item = get_random_filler_item(self)
        return item_const_name_to_label(item)

    def create_item_by_const_name(self, item_const: str) -> PokemonCrystalItem:
        item_code = item_const_name_to_id(item_const)
        return self.create_item_by_code(item_code)

    def create_item_by_code(self, item_code: int) -> PokemonCrystalItem:
        return PokemonCrystalItem(
            self.item_id_to_name[item_code],
            get_item_classification(item_code),
            item_code,
            self.player
        )

    def create_event(self, name: str) -> PokemonCrystalItem:
        return PokemonCrystalItem(
            name,
            ItemClassification.progression,
            None,
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
            for hm in ("CUT", "FLY", "SURF", "STRENGTH", "FLASH", "WHIRLPOOL", "WATERFALL", "HEADBUTT", "ROCK_SMASH"):
                pre_fill_items.append(self.create_event(f"Teach {hm}"))
        return pre_fill_items

    def collect(self, state: CollectionState, item: Item) -> bool:
        changed = super().collect(state, item)
        if changed:
            item_name = item.name
            if item_name in self.logic.pokemon_hm_use:
                state.prog_items[self.player].update(self.logic.pokemon_hm_use[item_name])
            return True
        else:
            return False

    def remove(self, state: CollectionState, item: Item) -> bool:
        changed = super().remove(state, item)
        if changed:
            item_name = item.name
            if item_name in self.logic.pokemon_hm_use:
                state.prog_items[self.player].subtract(self.logic.pokemon_hm_use[item_name])
            return True
        else:
            return False

    # UT Stuff

    @property
    def ut_slot_data(self) -> dict[str, Any]:
        if hasattr(self.multiworld, "re_gen_passthrough"):
            return self.multiworld.re_gen_passthrough[self.game]
        else:
            return {}

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]):
        return slot_data
