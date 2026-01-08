from typing import ClassVar, Union, Set

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


class TCGSimulatorWeb(WebWorld):
    theme = "partyTime"

    setup_en = Tutorial(
        tutorial_name="Multiworld Setup Guide",
        description="A guide to setting up the TCG Card Shop Simulator randomizer connected to an Archipelago Multiworld.",
        language="English",
        file_name="setup_en.md",
        link="setup/en",
        authors=["FyreDay"]
    )

    tutorials = [setup_en]

class TCGSimulatorSettings(settings.Group):
    class LimitChecksForSyncs(settings.Bool):
        """This limits goals to a reasonable number and sets all excessive settings to local_fill or Excluded for better sync experiences."""
    class AllowCardSanity(settings.Bool):
        """Card Sanity adds pure randomness to card checks. This option disables this sanity in your multiworlds"""

    limit_checks_for_syncs: Union[LimitChecksForSyncs, bool] = False
    allow_card_sanity: Union[AllowCardSanity, bool] = True





class TCGSimulatorWorld(World):

    game = "TCG Card Shop Simulator"
    web = TCGSimulatorWeb()
    options_dataclass = TCGSimulatorOptions
    options: TCGSimulatorOptions

    option_groups = tcg_cardshop_simulator_option_groups

    settings: ClassVar[TCGSimulatorSettings]

    item_name_to_id: ClassVar[Dict[str, int]] = {item_name: item_data.code for item_name, item_data in full_item_dict.items()}



    location_name_to_id: ClassVar[Dict[str, int]] = {item_name: item_code for item_name, item_code in locations.get_all_locations().items()}

    item_name_groups = {
        "licenses": set(item_dict.keys()),
    }

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

        super().__init__(multiworld, player)

    def generate_early(self) -> None:
        self.required_licenses = int(
            self.options.licenses_per_region.value * (self.options.required_licenses.value/100)
        )
        if self.required_licenses < 3:
            self.required_licenses = 3
        if self.required_licenses > 10:
            self.required_licenses = 10

        if self.options.extra_starting_item_checks.value + self.options.sell_check_amount.value > 16:
            self.options.extra_starting_item_checks.value = 16-self.options.sell_check_amount.value
        if self.settings.limit_checks_for_syncs:
            if self.options.max_level.value > 50:
                print(f"The Max Level {self.options.max_level.value} is too high for sync mode. Lowering to 50.")
                self.options.max_level.value = 50

        if self.options.money_bags.value == 0 and self.options.xp_boosts.value == 0 and self.options.random_card.value == 0 and self.options.random_new_card.value == 0:
            raise OptionError("All Junk Weights are Zero")
        if self.options.trap_fill.value != 0 and self.options.stink_trap.value == 0 and self.options.poltergeist_trap.value == 0 and self.options.decrease_card_luck_trap == 0 and self.options.market_change_trap == 0 and self.options.currency_trap == 0:
            raise OptionError("All Trap Weights are Zero")

        if self.options.max_level.value % 5 != 0:
            self.options.max_level.value += 5 - (self.options.max_level.value % 5)


    def create_regions(self):
        level_grouped_locs = create_regions(self)

        self.pg1_licenses = level_grouped_locs[0]
        self.pg2_licenses = level_grouped_locs[1]
        self.pg3_licenses = level_grouped_locs[2]
        self.tt_licenses = level_grouped_locs[3]

        connect_entrances(self)


    def create_item(self, item: str) -> TCGSimulatorItem:
        if item in junk_weights.keys():
            return TCGSimulatorItem(item, ItemClassification.filler, self.item_name_to_id[item], self.player)
        return TCGSimulatorItem(item, ItemClassification.progression, self.item_name_to_id[item], self.player)

    def create_items(self):
        starting_items, ghost_counts = create_items(self)
        for item in starting_items:
            self.push_precollected(item)

        self.ghost_item_counts = ghost_counts

    def set_rules(self):
        set_rules(self)

    def generate_output(self, output_directory: str):
        visualize_regions(self.multiworld.get_region("Menu", self.player), f"Player{self.player}.puml",
                          show_entrance_names=True,
                          regions_to_highlight=self.multiworld.get_all_state(self.player).reachable_regions[
                              self.player])

    def fill_slot_data(self) -> id:
        return {
            "ModVersion": "0.5.12",
            "StartingIds": self.starting_item_ids,
            "ShopPg1Mapping": self.pg1_licenses,
            "ShopPg2Mapping": self.pg2_licenses,
            "ShopPg3Mapping": self.pg3_licenses,
            "ShopTTMapping": self.tt_licenses,

            "MaxLevel": self.options.max_level.value,
            "LicensesPerRegion": self.options.licenses_per_region.value,
            "RequiredLicenses": self.required_licenses,
            "Goal": self.options.goal.value,
            # "CollectionGoalPercent": self.options.collection_goal_percentage.value,
            "GhostGoalAmount": self.options.ghost_goal_amount.value,

            "AutoRenovate": self.options.auto_renovate.value,
            "BetterTrades": self.options.better_trades.value,
            "ExtraStartingItemChecks": self.options.extra_starting_item_checks.value,
            "SellCheckAmount": self.options.sell_check_amount.value,
            "ChecksPerPack": self.options.checks_per_pack.value,
            "CardCollectPercentage": self.options.card_collect_percent.value,
            "PlayTableChecks": self.options.play_table_checks.value,
            "GamesPerCheck": self.options.games_per_check.value,
            "NumberOfSellCardChecks": self.options.sell_card_check_count.value,
            "SellCardsPerCheck": self.options.sell_cards_per_check.value,

            "CardSanity": self.options.card_sanity.value,
            "FoilInSanity": self.options.foil_sanity.value,
            "BorderInSanity": self.options.border_sanity.value,

            "TrapFill": self.options.trap_fill.value,
            "Deathlink": self.options.deathlink.value,
        }

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        hint_data[self.player] = self.hints
