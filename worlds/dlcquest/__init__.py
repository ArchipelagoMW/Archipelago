from typing import Union

from BaseClasses import Tutorial, CollectionState
from worlds.AutoWorld import WebWorld, World
from . import Options
from .Items import DLCQuestItem, ItemData, create_items, item_table, items_by_group, Group
from .Locations import DLCQuestLocation, location_table
from .Options import DLCQuestOptions
from .Regions import create_regions
from .Rules import set_rules

client_version = 0


class DLCqwebworld(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up the Archipelago DLCQuest game on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["axe_y"]
    )]


class DLCqworld(World):
    """
    DLCQuest is a metroid ish game where everything is an in-game dlc.
    """
    game = "DLCQuest"
    topology_present = False
    web = DLCqwebworld()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = location_table

    data_version = 1

    options_dataclass = DLCQuestOptions
    options: DLCQuestOptions

    def create_regions(self):
        create_regions(self.multiworld, self.player, self.options)

    def set_rules(self):
        set_rules(self.multiworld, self.player, self.options)

    def create_event(self, event: str):
        return DLCQuestItem(event, True, None, self.player)

    def create_items(self):
        self.precollect_coinsanity()
        locations_count = len([location
                               for location in self.multiworld.get_locations(self.player)
                               if not location.event])

        items_to_exclude = [excluded_items
                            for excluded_items in self.multiworld.precollected_items[self.player]]

        created_items = create_items(self, self.options, locations_count + len(items_to_exclude), self.multiworld.random)

        self.multiworld.itempool += created_items

        if self.options.campaign == Options.Campaign.option_basic or self.options.campaign == Options.Campaign.option_both:
            self.multiworld.early_items[self.player]["Movement Pack"] = 1

        for item in items_to_exclude:
            if item in self.multiworld.itempool:
                self.multiworld.itempool.remove(item)

    def precollect_coinsanity(self):
        if self.options.campaign == Options.Campaign.option_basic:
            if self.options.coinsanity == Options.CoinSanity.option_coin and self.options.coinbundlequantity >= 5:
                self.multiworld.push_precollected(self.create_item("Movement Pack"))

    def create_item(self, item: Union[str, ItemData]) -> DLCQuestItem:
        if isinstance(item, str):
            item = item_table[item]

        return DLCQuestItem(item.name, item.classification, item.code, self.player)

    def get_filler_item_name(self) -> str:
        trap = self.multiworld.random.choice(items_by_group[Group.Trap])
        return trap.name

    def fill_slot_data(self):
        options_dict = self.options.as_dict(
            "death_link", "ending_choice", "campaign", "coinsanity", "item_shuffle"
        )
        options_dict.update({
            "coinbundlerange": self.options.coinbundlequantity.value,
            "seed": self.random.randrange(99999999)
        })
        return options_dict

    def collect(self, state: CollectionState, item: DLCQuestItem) -> bool:
        change = super().collect(state, item)
        if change:
            suffix = item.coin_suffix
            if suffix:
                state.prog_items[self.player][suffix] += item.coins
        return change

    def remove(self, state: CollectionState, item: DLCQuestItem) -> bool:
        change = super().remove(state, item)
        if change:
            suffix = item.coin_suffix
            if suffix:
                state.prog_items[self.player][suffix] -= item.coins
        return change
