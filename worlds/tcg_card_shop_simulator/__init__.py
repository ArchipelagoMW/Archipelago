from typing import ClassVar, Union, Set, Any

import settings
from Options import OptionError
from Utils import visualize_regions
from worlds.AutoWorld import WebWorld, World
from BaseClasses import Tutorial
from .options import *
from .regions import *
from .locations import *
from .items import *
from .rules import *
from .data.LocationData import *
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

    game = "TCG Card Shop Simulator"
    web = TCGSimulatorWeb()
    options_dataclass = TCGSimulatorOptions
    settings: ClassVar[TCGSimulatorSettings]

    item_name_to_id: ClassVar[Dict[str, int]] = {item_name: item_data.code for item_name, item_data in full_item_dict.items()}



    location_name_to_id: ClassVar[Dict[str, int]] = {item_name: item_code for item_name, item_code in locations.get_all_locations().items()}

    item_name_groups = {
        "licenses": set(item_dict.keys()),
        "workers": {
            "Worker - Zachery",
            "Worker - Terence",
            "Worker - Dennis",
            "Worker - Clark",
            "Worker - Angus",
            "Worker - Benji",
            "Worker - Lauren",
            "Worker - Axel",
            "Worker - Alexander"
        }
    }

    # UT Stuff Here
    ut_can_gen_without_yaml = True

    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        return slot_data

    def __init__(self, multiworld, player):
        self.itempool = []

        self.max_level = 10

        self.starting_item_ids = []
        self.pg1_licenses: dict[int, int] = {}
        self.pg2_licenses: dict[int, int] = {}
        self.pg3_licenses: dict[int, int] = {}
        self.tt_licenses: dict[int, int] = {}

        self.ghost_item_counts = 0
        self.required_licenses = 0

        self.hints = {}

        self.open_achievements: ClassVar[List[Dict[str, Any]]] = []
        self.sell_achievements: ClassVar[List[Dict[str, Any]]] = []
        self.grade_achievements: ClassVar[List[Dict[str, Any]]] = []

        super().__init__(multiworld, player)

    def generate_early(self) -> None:
        if self.options.required_licenses.value >  self.options.licenses_per_region:
            raise OptionError("License requirement is larger than the amount of licenses")
        self.required_licenses = self.options.required_licenses.value

        if self.options.goal.value == 1 and self.options.max_level.value < 20:
            self.options.max_level.value = 20

        if self.settings.impose_goal_limits and self.options.max_level.value > 60:
            self.options.max_level.value = 60

        if self.options.goal.value == 1 and self.settings.impose_goal_limits and self.options.collection_goal_percentage.value > 60:
            self.options.collection_goal_percentage.value = 60

        if self.options.extra_starting_item_checks.value + self.options.sell_check_amount.value > 16:
            self.options.extra_starting_item_checks.value = 16-self.options.sell_check_amount.value

        if self.settings.limit_impossible_checks:
            if self.options.checks_opening_difficulty.value > 3:
                self.options.checks_opening_difficulty = CardOpeningCheckDifficulty.option_hard
            if self.options.checks_selling_difficulty.value > 3:
                self.options.checks_selling_difficulty_difficulty = CardSellingCheckDifficulty.option_hard
            if self.options.checks_grading_difficulty.value > 3:
                self.options.checks_grading_difficulty = CardGradingCheckDifficulty.option_hard

        if self.options.card_sanity.value > 0 and not self.settings.allow_card_sanity:
            self.options.card_sanity.value = 0

        if self.options.money_filler.value == 0 and self.options.xp_filler.value == 0 and \
                self.options.wallet_filler == 0 and self.options.luck_filler == 0 and self.options.card_filler == 0:
            raise OptionError("All Filler Weights are Zero")

        if self.options.trap_fill.value != 0 and self.options.stink_trap.value == 0 and self.options.poltergeist_trap.value == 0 \
                and self.options.decrease_card_luck_trap.value == 0:
            raise OptionError("All Trap Weights are Zero")

        if self.options.max_level.value % 5 != 0:
            self.options.max_level.value += 5 - (self.options.max_level.value % 5)

        # UT Stuff Here
        self.handle_ut_yamless(None)


    def create_regions(self):
        if hasattr(self.multiworld, "generation_is_fake"):
            ut_recreate_regions(self, self.pg1_licenses, self.pg2_licenses, self.pg3_licenses, self.tt_licenses)
        else:
            level_grouped_locs = create_regions(self)

            self.pg1_licenses = level_grouped_locs[0]
            self.pg2_licenses = level_grouped_locs[1]
            self.pg3_licenses = level_grouped_locs[2]
            self.tt_licenses = level_grouped_locs[3]

        connect_entrances(self)


    def create_item(self, item: str) -> TCGSimulatorItem:
        junk_weights = {
            "Small Xp": self.options.xp_filler.value * .5,
            "Small Money": self.options.money_filler.value * .5,
            "Medium Money": self.options.money_filler.value * .3,
            "Medium Xp": self.options.xp_filler.value * .3,
            "Large Money": self.options.money_filler.value * .2,
            "Large Xp": self.options.xp_filler.value * .2,
            "Random Card": self.options.card_filler.value,
            "Progressive Customer Money": self.options.wallet_filler.value,
            "Increase Card Luck": self.options.luck_filler.value
        }
        if item in junk_weights.keys():
            return TCGSimulatorItem(item, ItemClassification.filler, self.item_name_to_id[item], self.player)
        return TCGSimulatorItem(item, ItemClassification.progression, self.item_name_to_id[item], self.player)

    def create_items(self):
        starting_items, ghost_counts = create_items(self)
        for item in starting_items:
            #print(item.name)
            self.push_precollected(item)

        self.ghost_item_counts = ghost_counts

        # source = "Tracker" if hasattr(self.multiworld, "re_gen_passthrough") \
        #                       and isinstance(self.multiworld.re_gen_passthrough, dict) else "Gen"
        # visualize_regions(self.multiworld.get_region("Menu", self.player), f"Player{self.player}_{source}.puml",
        #                   show_entrance_names=True,
        #                   regions_to_highlight=self.multiworld.get_all_state(self.player).reachable_regions[
        #                       self.player])


    def set_rules(self):
        set_rules(self)

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
            "StartingIds": self.starting_item_ids,
            "ShopPg1Mapping": self.pg1_licenses,
            "ShopPg2Mapping": self.pg2_licenses,
            "ShopPg3Mapping": self.pg3_licenses,
            "ShopTTMapping": self.tt_licenses,
            "OpenAchievements": self.open_achievements,
            "SellAchievements": self.sell_achievements,
            "GradeAchievements": self.grade_achievements,

            "MaxLevel": self.options.max_level.value,
            "LicensesPerRegion": self.options.licenses_per_region.value,
            "RequiredLicenses": self.required_licenses,
            "Goal": self.options.goal.value,
            "CollectionGoalPercent": self.options.collection_goal_percentage.value,
            "GhostGoalAmount": self.options.ghost_goal_amount.value,

            "AutoRenovate": self.options.auto_renovate.value,
            "ExtraStartingItemChecks": self.options.extra_starting_item_checks.value,
            "SellCheckAmount": self.options.sell_check_amount.value,
            "BulkBoxChecks": self.options.bulk_box.value,
            "CardOpeningCheckDifficulty": self.options.checks_opening_difficulty.value,
            "CardSellingCheckDifficulty": self.options.checks_selling_difficulty.value,
            "CardGradingCheckDifficulty": self.options.checks_grading_difficulty.value,
            "PlayTableChecks": self.options.play_table_checks.value,
            "StartingEmployeeIndex": self.options.start_with_worker.value - 1,

            "CardSanity": self.options.card_sanity.value,

            "TrapFill": self.options.trap_fill.value,
            "Deathlink": self.options.deathlink.value,
            "NoFormat": self.options.no_formats.value,
            "grading_locked": True
        }

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        hint_data[self.player] = self.hints

    def handle_ut_yamless(self, slot_data: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:

        if not slot_data \
                and hasattr(self.multiworld, "re_gen_passthrough") \
                and isinstance(self.multiworld.re_gen_passthrough, dict) \
                and self.game in self.multiworld.re_gen_passthrough:
            slot_data = self.multiworld.re_gen_passthrough[self.game]

        if not slot_data:
            return None

        # fill in options
        self.starting_item_ids = [int(x) for x in slot_data["StartingIds"]]
        self.pg1_licenses = {
            int(k): int(v)
            for k, v in slot_data["ShopPg1Mapping"].items()
        }

        self.pg2_licenses = {
            int(k): int(v)
            for k, v in slot_data["ShopPg2Mapping"].items()
        }

        self.pg3_licenses = {
            int(k): int(v)
            for k, v in slot_data["ShopPg3Mapping"].items()
        }

        self.tt_licenses = {
            int(k): int(v)
            for k, v in slot_data["ShopTTMapping"].items()
        }
        self.open_achievements = slot_data["OpenAchievements"]
        self.sell_achievements = slot_data["SellAchievements"]
        self.grade_achievements = slot_data["GradeAchievements"]

        self.options.max_level.value = slot_data["MaxLevel"]
        self.options.licenses_per_region.value = slot_data["LicensesPerRegion"]
        self.required_licenses = slot_data["RequiredLicenses"]
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