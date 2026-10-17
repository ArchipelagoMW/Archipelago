import math
from typing import ClassVar, Union, Set, Any, Dict, Optional

import settings
from Options import OptionError
from Utils import visualize_regions
from worlds.AutoWorld import WebWorld, World
from BaseClasses import Tutorial
from .constants import TCG_CARD_SHOP_SIM_NAME, STARTING_LICENSES_COUNT
from .data.items import all_items, BoosterPackItems, AccessoriesItems, FigurineItems, TableTopItems, Events, Workers
from .data.items.shop_licenses import get_total_licenses
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





class TCGSimulatorWorld(TCGSimulatorBase):

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
        self.starting_items: list[Item] = []

        self.total_licenses = 0
        self.license_items = []
        self.starting_license_items = []

        self.is_ut = False

        super().__init__(multiworld, player)

    def generate_early(self) -> None:



        if self.options.goal.value == 1 and self.options.max_level.value < 20:
            self.options.max_level.value = 20

        if self.settings.impose_goal_limits and self.options.max_level.value > 60:
            self.options.max_level.value = 60

        if self.options.goal.value == 1 and self.settings.impose_goal_limits and self.options.collection_goal_percentage.value > 60:
            self.options.collection_goal_percentage.value = 60

        if self.settings.limit_impossible_checks:
            if self.options.checks_opening_difficulty.value > 3:
                self.options.checks_opening_difficulty = CardOpeningCheckDifficulty.option_hard
            if self.options.checks_selling_difficulty.value > 3:
                self.options.checks_selling_difficulty_difficulty = CardSellingCheckDifficulty.option_hard
            if self.options.checks_grading_difficulty.value > 3:
                self.options.checks_grading_difficulty = CardGradingCheckDifficulty.option_hard

        if self.options.card_sanity.value > 0 and not self.settings.allow_card_sanity:
            self.options.card_sanity.value = 0

        if False:
            raise OptionError("All Filler Weights are Zero")

        if self.options.trap_fill.value != 0 and False:
            raise OptionError("All Trap Weights are Zero")

        self.options.max_level.value = math.ceil(self.options.max_level.value / 5) * 5

        total_steps = self.options.max_level.value // 5

        available_licenses = min(
            get_total_licenses(),
            STARTING_LICENSES_COUNT + total_steps * self.licenses_per
        )

        self.total_licenses = available_licenses

        self.is_ut = (hasattr(self.multiworld, "re_gen_passthrough")
                      and isinstance(self.multiworld.re_gen_passthrough, dict)
                      and self.game in self.multiworld.re_gen_passthrough)
        self.handle_ut_yamless(None)

    def create_regions(self):
        licenses, starting_licenses = locations.create_regions(self)
        self.license_items = licenses
        self.starting_license_items = starting_licenses
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

    #def connect_entrances(self):
       # print("connecting entrances")

    def generate_output(self, output_directory: str):
        print("Generating Output")
        visualize_regions(self.multiworld.get_region("Menu", self.player), f"Player{self.player}_output.puml",
                          show_entrance_names=True,
                          regions_to_highlight=self.multiworld.get_all_state(self.player).reachable_regions[
                              self.player])


    def fill_slot_data(self) -> id:
        #print("Filling Slot Data")
        return {
            "ModVersion": "1.1.0",

            "license_checks": [
                {
                    "type": type(item).__name__,
                    "name": item.name,
                }
                for item in self.license_items
            ],

            "MaxLevel": self.options.max_level.value,
            "LicensesPerCap": self.options.licenses_per_cap.value,
            "RequiredLicenses": self.required_licenses,
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

            "TrapFill": self.options.trap_fill.value,
            "Deathlink": self.options.deathlink.value,
            "NoFormat": self.options.no_formats.value,
        }

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        hint_data[self.player] = self.hints

    def handle_ut_yamless(
            self, slot_data: dict[str, Any] | None
    ) -> dict[str, Any] | None:
        if self.is_ut and not slot_data:
            slot_data = self.multiworld.re_gen_passthrough[self.game]
        if not slot_data:
            return None

        ITEM_ENUMS = {
            enum.__name__: enum
            for enum in (
                BoosterPackItems,
                AccessoriesItems,
                FigurineItems,
                TableTopItems,
            )
        }

        # fill in options
        self.starting_item_ids = [int(x) for x in slot_data["StartingIds"]]

        self.license_items = [
            ITEM_ENUMS[item["type"]][item["name"]]
            for item in slot_data["license_checks"]
        ]

        self.options.max_level.value = slot_data["MaxLevel"]
        self.options.licenses_per_region.value = slot_data["LicensesPerRegion"]
        self.options.goal.value = slot_data["Goal"]
        self.options.collection_goal_percentage.value = slot_data["CollectionGoalPercent"]
        self.options.ghost_goal_amount.value = slot_data["GhostGoalAmount"]

        self.options.auto_renovate.value = slot_data["AutoRenovate"]
        self.options.extra_starting_item_checks.value = slot_data["ExtraStartingItemChecks"]
        self.options.sell_check_amount.value = slot_data["SellCheckAmount"]
        self.options.bulk_box.value = slot_data["BulkBoxChecks"]
        self.options.checks_opening_difficulty.value = slot_data["CardOpeningCheckDifficulty"]
        self.options.checks_selling_difficulty.value = slot_data["CardSellingCheckDifficulty"]
        self.options.checks_grading_difficulty.value = slot_data["CardGradingCheckDifficulty"]
        self.options.play_table_checks.value = slot_data["PlayTableChecks"]

        self.options.card_sanity.value = slot_data["CardSanity"]
        self.options.no_formats.value = slot_data["NoFormat"]

        self.options.trap_fill.value = slot_data["TrapFill"]

        return slot_data