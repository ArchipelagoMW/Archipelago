import dataclasses
import typing
from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification, Region, Location
from Options import OptionError, PerGameCommonOptions
from worlds.AutoWorld import WebWorld, World

from .items import Ty1Item, ty1_item_table, create_items, ItemData, place_locked_items
from .locations import ty1_location_table, Ty1Location
from .options import Ty1Options, ty1_option_groups
from .regions import create_regions, connect_regions, ty1_levels, Ty1LevelCode, connect_all_regions, ty1_core_levels, \
    ty1_levels_short
from .rules import set_rules


class Ty1Web(WebWorld):
    theme = "jungle"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Ty the Tasmanian Tiger 1 randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["xMcacutt", "Dashieswag92"]
    )

    tutorials = [setup_en]
    option_groups = ty1_option_groups


class Ty1World(World):
    """
    Ty the Tasmanian Tiger is a 3D platformer collectathon created by Australian developers Krome Studios.
    Play as Ty and travel the Australian outback to snowy mountains to defeat Boss Cass and rescue your family from The Dreaming.
    """
    game: str = "Ty the Tasmanian Tiger"
    options_dataclass = Ty1Options
    options: Ty1Options
    topology_present = True
    item_name_to_id = {name: item.code for name, item in ty1_item_table.items()}
    location_name_to_id = {name: item.code for name, item in ty1_location_table.items()}
    region_name_to_code = {name: code for code, name in ty1_levels.items()}
    portal_map: typing.List[int] = [Ty1LevelCode.A1.value, Ty1LevelCode.A2.value, Ty1LevelCode.A3.value,
                                    Ty1LevelCode.B1.value, Ty1LevelCode.B2.value, Ty1LevelCode.B3.value,
                                    Ty1LevelCode.C1.value, Ty1LevelCode.C2.value, Ty1LevelCode.C3.value]
    trap_weights = {}

    web = Ty1Web()

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.itempool = []
        self.portal_map = [Ty1LevelCode.A1.value, Ty1LevelCode.A2.value, Ty1LevelCode.A3.value,
                           Ty1LevelCode.B1.value, Ty1LevelCode.B2.value, Ty1LevelCode.B3.value,
                           Ty1LevelCode.C1.value, Ty1LevelCode.C2.value, Ty1LevelCode.C3.value]

    def fill_slot_data(self) -> id:
        return {
            "ModVersion": "1.3.0",
            "Goal": self.options.goal.value,
            "ProgressiveElementals": self.options.progressive_elementals.value,
            "ProgressiveLevel": self.options.progressive_level.value,
            "LevelUnlockStyle": self.options.level_unlock_style.value,
            "TheggGating": self.options.thegg_gating.value,
            "CogGating": self.options.cog_gating.value,
            "ReqBosses": self.options.req_bosses.value,
            "GateTimeAttacks": self.options.gate_time_attacks.value,
            "PortalMap": self.portal_map,
            "FramesRequireInfra": self.options.frames_require_infra.value,
            "Scalesanity": self.options.scalesanity.value,
            "Signsanity": self.options.signsanity.value,
            "Lifesanity": self.options.lifesanity.value,
            "Framesanity": self.options.framesanity.value,
            "Opalsanity": self.options.opalsanity.value,
            "AdvancedLogic": self.options.logic_difficulty.value,
            "DeathLink": self.options.death_link.value,
            "MulTyLink": self.options.mul_ty_link.value
        }

    def generate_early(self) -> None:
        extra_thegg_count = self.options.extra_theggs * 3
        extra_cog_count = self.options.extra_cogs
        empty_cog_checks = 90 - (self.options.cog_gating * 6)
        empty_thegg_checks = 72 - (self.options.thegg_gating * 3)
        frame_count = 127 if self.options.framesanity == 0 else 9 if self.options.framesanity == 1 else 0
        scale_count = 25 if self.options.scalesanity else 0
        portal_items = 0 if self.options.level_unlock_style == 0 else 12 if self.options.level_unlock_style == 1 else 9
        excess_checks = 18 - portal_items
        excess_checks += frame_count + scale_count + empty_cog_checks + empty_thegg_checks
        total_unbalanced = extra_thegg_count + extra_cog_count
        if extra_thegg_count + extra_cog_count > excess_checks:
            print("[WARN] Ty1 - Thegg and Cog count in item pool is larger than remaining checks.")
            overflow = total_unbalanced - excess_checks
            cog_contribution_ratio = extra_cog_count / total_unbalanced
            thegg_contribution_ratio = extra_thegg_count / total_unbalanced

            reduce_cogs = int(round(overflow * cog_contribution_ratio, 0))
            reduce_theggs = int(round(overflow * thegg_contribution_ratio, 0))

            reduce_cogs = min(self.options.extra_cogs.value, reduce_cogs)
            reduce_theggs = min(self.options.extra_theggs.value, int(reduce_theggs / 3))
            rounding_error = overflow - (reduce_cogs + (reduce_theggs * 3))
            if 0 < rounding_error < 3 and self.options.extra_cogs - reduce_cogs > 0:
                reduce_cogs += rounding_error

            self.options.extra_cogs.value = extra_cog_count - int(reduce_cogs)
            self.options.extra_theggs.value = int(extra_thegg_count / 3) - int(reduce_theggs)

            thegg_count = self.options.extra_theggs * 3
            cog_count = self.options.extra_cogs

            if thegg_count + cog_count > excess_checks:
                print("[ERROR] Ty1 - Could not automatically reduce counts. Something is very wrong.")
                raise OptionError()
            else:
                print("[INFO] Ty1 - Extra Theggs and Cogs have been reduced to avoid unplaced items.")
        self.trap_weights = {
            "Knocked Down Trap": self.options.knocked_down_trap_weight.value,
            "Slow Trap": self.options.slow_trap_weight.value,
            "Gravity Trap": self.options.gravity_trap_weight.value,
            "Acid Trap": self.options.acid_trap_weight.value,
            "Exit Trap": self.options.exit_trap_weight.value,
        }

    def create_item(self, name: str) -> Item:
        item_info = ty1_item_table[name]
        return Ty1Item(name, item_info.classification, item_info.code, self.player)

    def create_items(self):
        create_items(self.multiworld, self.options, self.player)

    def create_event(self, region_name: str, event_name: str) -> None:
        region: Region = self.multiworld.get_region(region_name, self.player)
        loc: Ty1Location = Ty1Location(self.player, event_name, None, region)
        loc.place_locked_item(Ty1Item(event_name, ItemClassification.progression, None, self.player))
        region.locations.append(loc)

    def create_regions(self):
        create_regions(self.multiworld, self.options, self.player)
        place_locked_items(self.multiworld, self.player)
        self.create_event("Bull's Pen", "Beat Bull")
        self.create_event("Crikey's Cove", "Beat Crikey")
        self.create_event("Fluffy's Fjord", "Beat Fluffy")
        self.create_event("Cass' Crest", "Beat Shadow")
        self.create_event("Final Battle", "Beat Cass")
        connect_all_regions(self.multiworld, self.player, self.options, self.portal_map)

    def set_rules(self):
        set_rules(self)

    def extend_hint_information(self, hint_data: typing.Dict[int, typing.Dict[int, str]]):
        new_hint_data = {}

        for key, data in ty1_location_table.items():
            try:
                location: Location = self.multiworld.get_location(key, self.player)
            except KeyError:
                continue
            region_name: str = data.region
            containing_level_code: Ty1LevelCode = self.region_name_to_code.get(region_name)
            if containing_level_code is None or containing_level_code not in ty1_core_levels:
                continue

            try:
                level_index: int = self.portal_map.index(containing_level_code.value)
            except ValueError:
                continue

            portal_code: int = level_index + 4
            if level_index > 5:
                portal_code = portal_code + 2
            elif level_index > 2:
                portal_code = portal_code + 1

            try:
                portal_name: str = ty1_levels_short[Ty1LevelCode(portal_code)]
            except ValueError:
                continue

            new_hint_data[location.address] = f"{portal_name} Portal"
            hint_data[self.player] = new_hint_data
