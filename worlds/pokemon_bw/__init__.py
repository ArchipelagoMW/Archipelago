import datetime
import logging
import os
from typing import ClassVar, Mapping, Any, List

import settings
from BaseClasses import MultiWorld, Tutorial, Item, Location, Region
from Options import Option, OptionError
from worlds.AutoWorld import World, WebWorld
from . import items, locations, options, bizhawk_client, rom, groups, tracker
from .generate import EncounterEntry, StaticEncounterEntry, TradeEncounterEntry, TrainerPokemonEntry
from .data import RulesDict

bizhawk_client.register_client()


class PokemonBWSettings(settings.Group):

    class PokemonBlackRomFile(settings.UserFilePath):
        """File name of your Pokémon Black Version ROM"""
        description = "Pokemon Black Version ROM"
        copy_to = "PokemonBlack.nds"

    class PokemonWhiteRomFile(settings.UserFilePath):
        """File name of your Pokémon White Version ROM"""
        description = "Pokemon White Version ROM"
        copy_to = "PokemonWhite.nds"

    class RemoveCollectedFieldItems(settings.Bool):
        """Toggles whether overworld and hidden items should be automatically removed
        if collected by another player."""

    class EnableEncounterPlando(settings.Bool):
        """Toggles whether Encounter Plando is enabled for players in generation.
        If disabled, yamls that use Encounter Plando do not raise OptionErrors, but display a warning."""

    class DumpPatchedFiles(settings.Bool):
        """If enabled, files inside the rom that are changed as part of the patching process (except for base patches)
        will be dumped into a zip file next to the patched rom (for debug purposes)."""

    black_rom: PokemonBlackRomFile = PokemonBlackRomFile(PokemonBlackRomFile.copy_to)
    white_rom: PokemonWhiteRomFile = PokemonWhiteRomFile(PokemonWhiteRomFile.copy_to)
    # remove_collected_field_items: RemoveCollectedFieldItems | bool = False
    enable_encounter_plando: EnableEncounterPlando | bool = True
    dump_patched_files: DumpPatchedFiles | bool = False


class PokemonBWWeb(WebWorld):
    rich_text_options_doc = True
    theme = ("grassFlowers", "ocean", "dirt", "ice")[(datetime.datetime.now().month - 1) % 4]
    game_info_languages = ["en"]
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Pokémon Black and White with Archipelago:",
        "English",
        "setup_en.md",
        "setup/en",
        ["BlastSlimey"]
    )
    tutorials = [setup_en]


class PokemonBWWorld(World):
    """
    Pokémon Black and White are the introduction to the fifth generation of the Pokémon franchise.
    Travel through the Unova region, catch a variety of brand-new Pokémon you have never seen before,
    collect the eight gym badges, fight Team Plasma, who claim to be the saviors of all the Pokémon,
    and become the champion of the region.
    These games present themselves in 2.5D graphics,
    while still using the well-known grid-based movement mechanics and battle UI.
    """
    game = "Pokemon Black and White"
    options_dataclass = options.PokemonBWOptions
    options: options.PokemonBWOptions
    topology_present = True
    web = PokemonBWWeb()
    item_name_to_id = items.get_item_lookup_table()
    location_name_to_id = locations.get_location_lookup_table()
    settings_key = "pokemon_bw_settings"
    settings: ClassVar[PokemonBWSettings]
    item_name_groups = groups.get_item_groups()
    location_name_groups = groups.get_location_groups()

    ut_can_gen_without_yaml = True
    tracker_world = {
        "map_page_folder": "tracker",
        "map_page_maps": "maps/maps.json",
        "map_page_locations": {
            "locations/locations.json",
            "locations/submaps_cities.json",
            "locations/submaps_dungeons.json",
            "locations/submaps_routes.json",
            "locations/old_compat.json",
        },
        "map_page_index": tracker.map_page_index,
        "map_page_setting_key": "pokemon_bw_map_{team}_{player}",
    }

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)

        from .data.version import ap_minimum
        from Utils import version_tuple
        if version_tuple < ap_minimum():
            raise Exception(f"Archipelago version too old for Pokémon BW "
                            f"(requires minimum {ap_minimum()}, found {version_tuple}")

        self.strength_species: set[str] = set()
        self.cut_species: set[str] = set()
        self.surf_species: set[str] = set()
        self.dive_species: set[str] = set()
        self.waterfall_species: set[str] = set()
        self.flash_species: set[str] = set()
        self.fighting_type_species: set[str] = set()  # Needed for challenge rock outside of pinwheel forest
        self.to_be_filled_locations: int = 0
        self.seed: int = 0
        self.to_be_locked_items: dict[str, list[items.PokemonBWItem] | dict[str, items.PokemonBWItem]] = {}
        self.wild_encounter: dict[str, EncounterEntry] = {}
        self.static_encounter: dict[str, StaticEncounterEntry] | None = None
        self.trade_encounter: dict[str, TradeEncounterEntry] | None = None
        self.trainer_teams: list[TrainerPokemonEntry] | None = None
        self.encounter_by_method: dict[str, tuple[list[str], list[int]]] = {}
        self.dexsanity_numbers: list[int] = []
        self.regions: dict[str, Region] | None = None
        self.rules_dict: RulesDict | None = None
        self.master_ball_seller_cost: int = 0

        self.ut_active: bool = False
        self.location_id_to_alias: dict[int, str] = {}

    def generate_early(self) -> None:
        from .generate.encounter import wild, checklist, static, plando
        from .generate import trainers

        # Load values from UT if this is a regenerated world
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if self.game in self.multiworld.re_gen_passthrough:
                from .data import version

                self.ut_active = True
                re_ge_slot_data: dict[str, Any] = self.multiworld.re_gen_passthrough[self.game]
                re_gen_options: dict[str, Any] = re_ge_slot_data["options"]
                # Populate options from UT
                for key, value in re_gen_options.items():
                    opt: Option | None = getattr(self.options, key, None)
                    if opt is not None:
                        setattr(self.options, key, opt.from_any(value))
                self.seed = re_ge_slot_data["seed"]
                loaded_ut_version = re_ge_slot_data.get("ut_compatibility", (0, 3, 2))
                if version.ut() != loaded_ut_version:
                    logging.warning("UT compatibility mismatch detected. You can continue tracking with this "
                                    "apworld version, but tracking might not be entirely accurate.")

        if not self.ut_active:
            self.seed = self.random.getrandbits(64)

        self.random.seed(self.seed)

        # TODO quick bandaid fix, need to fix it in another way later
        if (
            # False and
            self.options.modify_encounter_rates.current_key in ("invasive", "randomized_12") and
            "Prevent rare encounters" in self.options.randomize_wild_pokemon
        ):
            raise OptionError(f"Player {self.player_name}: Modify Encounter Rates choice "
                              f"\"{self.options.modify_encounter_rates.current_key}\" (currently) not allowed "
                              f"in combination with \"Prevent rare encounters\" in wild randomization.")

        cost_start, cost_end = 999999, -1
        for modifier in self.options.master_ball_seller.value:
            if modifier.casefold().startswith("cost"):
                if modifier.casefold().endswith("free"):
                    cost = 0
                else:
                    cost = int(modifier[modifier.index(" ")+1:])
                cost_start = min(cost_start, cost)
                cost_end = max(cost_end, cost)
        self.master_ball_seller_cost = self.random.randrange(cost_start, cost_end+1, 500) if cost_end != -1 else 3000

        self.regions = locations.get_regions(self)
        self.rules_dict = locations.create_rule_dict(self)
        locations.connect_regions(self)
        locations.cleanup_regions(self.regions)
        species_checklist = checklist.get_species_checklist(self)
        slots_checklist = checklist.get_slots_checklist(self)
        # Static and trade encounter generation also remove and add species from/to checklist
        self.wild_encounter |= plando.generate_wild(self, species_checklist, slots_checklist)  # only removes species and slots
        self.trade_encounter = static.generate_trade_encounters(self, species_checklist)  # removes and adds species
        self.static_encounter = static.generate_static_encounters(self, species_checklist)  # only removes species
        self.wild_encounter |= wild.generate_wild_encounters(  # only removes species
            self, species_checklist, slots_checklist
        )
        self.encounter_by_method = wild.organize_by_method(self)
        self.trainer_teams = trainers.generate_trainer_teams(self)

    def create_item(self, name: str) -> items.PokemonBWItem:
        return items.generate_item(name, self)

    def get_filler_item_name(self) -> str:
        return items.generate_filler(self)

    def create_regions(self) -> None:
        catchable_species_data = locations.create_and_place_event_locations(self)
        locations.create_and_place_locations(self, catchable_species_data)
        self.to_be_filled_locations = locations.count_to_be_filled_locations(self.regions)
        self.multiworld.regions.extend(self.regions.values())

    def create_items(self) -> None:
        item_pool = items.get_main_item_pool(self)
        items.populate_starting_inventory(self, item_pool)
        if len(item_pool) > self.to_be_filled_locations:
            raise Exception(f"Player {self.player_name} has more guaranteed items ({len(item_pool)}) "
                            f"than to-be-filled locations ({self.to_be_filled_locations})."
                            f"Please report this to the devs and provide the yaml used for generating.")
        for _ in range(self.to_be_filled_locations-len(item_pool)):
            item_pool.append(self.create_item(self.get_filler_item_name()))
        items.place_locked_items(self, item_pool)
        self.multiworld.itempool.extend(item_pool)

    def fill_hook(self,
                  progitempool: List[Item],
                  usefulitempool: List[Item],
                  filleritempool: List[Item],
                  fill_locations: List[Location]) -> None:
        from .generate.locked_placement import place_tm_hm_fill, place_badges_fill

        place_badges_fill(self, progitempool, usefulitempool, filleritempool, fill_locations)
        place_tm_hm_fill(self, progitempool, usefulitempool, filleritempool, fill_locations)

    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]):
        hint_data[self.player] = {}
        locations.extend_dexsanity_hints(self, hint_data)

    def generate_output(self, output_directory: str) -> None:
        if self.options.version == "black":
            rom.PokemonBlackPatch(
                path=os.path.join(
                    output_directory,
                    self.multiworld.get_out_file_name_base(self.player) + rom.PokemonBlackPatch.patch_file_ending
                ), world=self, player=self.player, player_name=self.player_name
            ).write()
        else:
            rom.PokemonWhitePatch(
                path=os.path.join(
                    output_directory,
                    self.multiworld.get_out_file_name_base(self.player) + rom.PokemonWhitePatch.patch_file_ending
                ), world=self, player=self.player, player_name=self.player_name
            ).write()

    def fill_slot_data(self) -> Mapping[str, Any]:
        from .data import version

        # Some options and data are included for UT
        return {
            "options": {
                "version": self.options.version.current_key,
                "goal": self.options.goal.current_key,
                "randomize_wild_pokemon": self.options.randomize_wild_pokemon.value,
                "randomize_trainer_pokemon": self.options.randomize_trainer_pokemon.value,
                "pokemon_randomization_adjustments": self.options.pokemon_randomization_adjustments.value,
                "encounter_plando": self.options.encounter_plando.to_slot_data(),
                "shuffle_badges": self.options.shuffle_badges.current_key,
                "shuffle_tm_hm": self.options.shuffle_tm_hm.current_key,
                "dexsanity": self.options.dexsanity.value,
                "season_control": self.options.season_control.current_key,
                "adjust_levels": self.options.adjust_levels.value,
                "modify_encounter_rates": self.options.modify_encounter_rates.value,  # value property because of plando
                "master_ball_seller": self.options.master_ball_seller.value,
                "modify_item_pool": self.options.modify_item_pool.value,
                "modify_logic": self.options.modify_logic.value,
            },
            # Needed for UT
            "seed": self.seed,
            "ut_compatibility": version.ut(),
            # NOT needed for UT
            "master_ball_seller_cost": self.master_ball_seller_cost,
            "reusable_tms": self.options.reusable_tms.current_key,
            # Needed for PopTracker
            "encounter_by_method": {method: lists[1] for method, lists in self.encounter_by_method.items()},
            "dexsanity_pokemon": self.dexsanity_numbers,
        }

    def interpret_slot_data(self, slot_data: dict[str, Any]) -> dict[str, Any]:
        """Helper function for Universal Tracker"""
        _ = self  # Damn PyCharm screaming "meThoD mAy bE stAtiC"
        return slot_data
