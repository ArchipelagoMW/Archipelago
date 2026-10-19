import json
import math
from importlib.resources import files
from logging import warning
from typing import ClassVar, Union, Set, Any, Dict, Optional

import settings
from Options import OptionError
from Utils import visualize_regions
from worlds.AutoWorld import WebWorld, World
from BaseClasses import Tutorial, MultiWorld
from .constants import TCG_CARD_SHOP_SIM_NAME, STARTING_LICENSES_COUNT
from .data.items import all_items, BoosterPackItems, AccessoriesItems, FigurineItems, TableTopItems, Events, Workers
from .data.items.shop_licenses import get_total_licenses, ITEM_BY_ID
from .data.locations import all_Enum_locations, all_Generated_locations
from .options import *
from .locations import *
from .items import *
from .rules import *
from .world_base import TCGSimulatorBase


class TCGSimulatorWeb(WebWorld):
    theme = "partyTime"
    #85957132542149874884
    setup_en = Tutorial(
        tutorial_name="Multiworld Setup Guide",
        description="A guide to setting up the TCG Card Shop Simulator randomizer connected to an Archipelago Multiworld.",
        language="English",
        file_name="setup_en.md",
        link="setup/en",
        authors=["FyreDay"]
    )
    option_groups = tcg_cardshop_simulator_option_groups
    tutorials = [setup_en]

class TCGSimulatorSettings(settings.Group):
    class LimitChecksDifficultyToHard(settings.Bool):
        """This removes the Impossible level checks from your multiworlds."""
    class AllowCardSanity(settings.Bool):
        """Card Sanity adds thousands of pure randomness checks. This option disables this sanity in your multiworlds"""
    class ImposeGoalLimits(settings.Bool):
        """This limits the max level to 60, and how many cards they need to collect to 60% of the cards in the game"""

    limit_impossible_checks: Union[LimitChecksDifficultyToHard, bool] = False
    allow_card_sanity: Union[AllowCardSanity, bool] = True
    impose_goal_limits: Union[ImposeGoalLimits, bool] = False



def load_manifest():
    return json.loads(
        files(__package__).joinpath("archipelago.json").read_text("utf-8")
    )

class TCGSimulatorWorld(TCGSimulatorBase):
    manifest = load_manifest()

    game = TCG_CARD_SHOP_SIM_NAME
    web = TCGSimulatorWeb()
    options_dataclass = TCGSimulatorOptions
    settings: ClassVar[TCGSimulatorSettings]

    item_name_to_id: ClassVar[dict[str, int]] = {
        item.value: item.item_id for item in all_items
    }

    item_lookup = {item.value: item for item in all_items}


    location_name_to_id: ClassVar[dict[str, int]] = {
        **{
            loc.value: loc.location_id
            for loc in all_Enum_locations
        },
        **{
            gen_loc.name: gen_loc.location_id
            for gen_loc in all_Generated_locations
        },
    }
    item_name_groups = {
        "Booster License": {license.value for license in BoosterPackItems},
        "Accessories License": {license.value for license in AccessoriesItems},
        "Figurine License": {license.value for license in FigurineItems},
        "TableTop License": {license.value for license in TableTopItems},
        "Event": {event.value for event in Events},
        "Worker": {worker.value for worker in Workers},
    }

    # UT Stuff Here
    ut_can_gen_without_yaml = True

    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        return slot_data

    def __init__(self, multiworld, player):
        self.itempool = []
        self.sanity_fill_locations: list[Location] = []
        self.backup_sanity_fill_locations: list[Location] = []
        self.filler_items = []
        self.created_region_types: set[RegionTypeEnum] = set()

        self.starting_items: list[Item] = []

        self.ghost_item_counts = 0
        self.total_licenses = 0
        self.license_items = []
        self.starting_license_items = []

        self.is_ut = False

        super().__init__(multiworld, player)

    def generate_early(self) -> None:

        if self.settings.impose_goal_limits and self.options.max_level.value > 60:
            self.options.max_level.value = 60

        if self.options.goal.value == self.options.goal.option_collection_builder and self.settings.impose_goal_limits and self.options.collection_goal_percentage.value > 60:
            self.options.collection_goal_percentage.value = 60

        if self.settings.limit_impossible_checks:
            if self.options.checks_opening_difficulty.value > 3:
                self.options.checks_opening_difficulty.value = CardOpeningCheckDifficulty.option_hard
            if self.options.checks_selling_difficulty.value > 3:
                self.options.checks_selling_difficulty.value = CardSellingCheckDifficulty.option_hard
            if self.options.checks_grading_difficulty.value > 3:
                self.options.checks_grading_difficulty.value = CardGradingCheckDifficulty.option_hard

        if self.options.card_sanity.value > 0 and not self.settings.allow_card_sanity:
            self.options.card_sanity.value = 0

        if 0 == sum(self.options.filler_weights.value.values()):
            raise OptionError("All Filler Weights are Zero")

        if self.options.trap_fill.value != 0 and 0 == sum(self.options.trap_weights.value.values()):
            raise OptionError("Trap Fill is ON and All Trap Weights are Zero")

        self.options.max_level.value = math.ceil(self.options.max_level.value / 5) * 5

        available_licenses = min(
            get_total_licenses(),
            self.options.product_licenses.value
        )

        self.total_licenses = available_licenses

        self.is_ut = (hasattr(self.multiworld, "re_gen_passthrough")
                      and isinstance(self.multiworld.re_gen_passthrough, dict)
                      and self.game in self.multiworld.re_gen_passthrough)
        self.handle_ut_yamless(None)

    def pre_fill(self) -> None:
        if not self.filler_items or self.multiworld.players <= 1:
            return

        primary = [
            loc
            for loc in self.sanity_fill_locations
            if loc.item is None
        ]

        backup = [
            loc
            for loc in self.backup_sanity_fill_locations
            if loc.item is None
        ]

        self.random.shuffle(primary)
        self.random.shuffle(backup)

        if len(primary) + len(backup) < len(self.filler_items):
            raise OptionError(
                f"Insufficient card-sanity locations: "
                f"{len(self.filler_items)} reserved items, "
                f"{len(primary) + len(backup)} eligible locations."
            )

        self.fill_locations = primary
        self.backup_locations = backup

    @classmethod
    def stage_pre_fill(cls, multiworld: MultiWorld) -> None:
        for world in multiworld.get_game_worlds(TCG_CARD_SHOP_SIM_NAME):
            if not world.filler_items or multiworld.players <= 1:
                continue

            for item in world.filler_items:
                location = next(
                    (
                        loc
                        for loc in world.fill_locations
                                   + world.backup_locations
                        if loc.item is None
                    ),
                    None,
                )

                if location is None:
                    raise OptionError(
                        f"No available card-sanity location "
                        f"for {world.player_name}."
                    )

                location.place_locked_item(item)

    def create_regions(self):
        licenses, starting_licenses = locations.create_regions(self)
        self.license_items = licenses
        self.starting_license_items = starting_licenses
        items.create_events(self)
        locations.create_entrances(self)

    def connect_entrances(self) -> None:
        pass

    def create_item(self, item: str) -> Item:
        item_enum = self.item_lookup[item]

        return Item(
            item,
            item_enum.classification,
            item_enum.item_id,
            self.player,
        )

    def create_items(self):
        starting_items, ghost_counts = create_items(self)
        for item in starting_items:
            #print(item.name)
            self.push_precollected(item)

        self.ghost_item_counts = ghost_counts


    def set_rules(self):
        set_goal(self)

    def generate_output(self, output_directory: str):
        print("Generating Output")
        visualize_regions(self.multiworld.get_region("Menu", self.player), f"Player{self.player}_output.puml",
                          show_entrance_names=True,
                          regions_to_highlight=self.multiworld.get_all_state(self.player).reachable_regions[
                              self.player])


    def fill_slot_data(self) -> id:
        #print("Filling Slot Data")
        return {
            "ModVersion": self.manifest["mod_version"],

            "license_checks": [item.item_id for item in self.license_items],
            "starting_checks": [item.item_id for item in self.starting_license_items],
            "GhostCounts": self.ghost_item_counts,

            "total_licenses": self.total_licenses,
            "MaxLevel": self.options.max_level.value,
            "TotalProductLicenses": self.options.product_licenses.value,
            "Goal": self.options.goal.value,
            "CollectionGoalPercent": self.options.collection_goal_percentage.value,
            "GhostGoalAmount": self.options.ghost_goal_amount.value,

            "AutoRenovate": self.options.auto_renovate.value,
            "SellCheckAmount": self.options.sell_check_amount.value,
            "CardOpeningCheckDifficulty": self.options.checks_opening_difficulty.value,
            "CardSellingCheckDifficulty": self.options.checks_selling_difficulty.value,
            "CardGradingCheckDifficulty": self.options.checks_grading_difficulty.value,
            "PlayTableChecks": self.options.play_table_checks.value,
            "StartingEmployeeIndex": self.options.start_with_worker.value - 1,

            "CardSanity": self.options.card_sanity.value,
            "CardSanityPercentage": self.options.card_sanity_percentage.value,
            "BulkBoxChecks": self.options.bulk_box.value,
            "StartingWorker": self.options.start_with_worker.value,

            "TrapFill": self.options.trap_fill.value,
            "Deathlink": self.options.deathlink.value,
            "NoFormat": self.options.no_formats.value,
        }

    def handle_ut_yamless(
            self, slot_data: dict[str, Any] | None
    ) -> dict[str, Any] | None:
        if self.is_ut and not slot_data:
            slot_data = self.multiworld.re_gen_passthrough[self.game]
        if not slot_data:
            return None

        self.license_items = [ITEM_BY_ID[item_id] for item_id in slot_data["license_checks"]]
        self.starting_license_items = [ITEM_BY_ID[item_id] for item_id in slot_data["starting_checks"]]
        self.ghost_item_counts = slot_data["GhostCounts"]

        self.total_licenses = slot_data["total_licenses"]

        self.options.max_level.value = slot_data["MaxLevel"]
        self.options.product_licenses.value = slot_data["TotalProductLicenses"]
        self.options.goal.value = slot_data["Goal"]
        self.options.collection_goal_percentage.value = slot_data["CollectionGoalPercent"]
        self.options.ghost_goal_amount.value = slot_data["GhostGoalAmount"]

        self.options.auto_renovate.value = slot_data["AutoRenovate"]
        self.options.sell_check_amount.value = slot_data["SellCheckAmount"]
        self.options.checks_opening_difficulty.value = slot_data["CardOpeningCheckDifficulty"]
        self.options.checks_selling_difficulty.value = slot_data["CardSellingCheckDifficulty"]
        self.options.checks_grading_difficulty.value = slot_data["CardGradingCheckDifficulty"]
        self.options.play_table_checks.value = slot_data["PlayTableChecks"]

        self.options.card_sanity.value = slot_data["CardSanity"]
        self.options.no_formats.value = slot_data["NoFormat"]

        self.options.trap_fill.value = slot_data["TrapFill"]

        self.options.card_sanity_percentage.value = slot_data["CardSanityPercentage"]

        self.options.bulk_box.value = slot_data["BulkBoxChecks"]

        self.options.start_with_worker.value = slot_data["StartingWorker"]

        return slot_data