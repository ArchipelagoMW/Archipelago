from typing import ClassVar, Dict, Any, Type, List

from BaseClasses import Tutorial, ItemClassification as ItemClass
from Options import PerGameCommonOptions, StartInventory
from ..AutoWorld import World, WebWorld

from . import Options, Items, Locations
from .Constants import *


class SavingPrincessWeb(WebWorld):
    theme = "partyTime"
    bug_report_page = "https://github.com/LeonarthCG/saving-princess-archipelago/issues"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Saving Princess for Archipelago multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["LeonarthCG"]
    )
    tutorials = [setup_en]


class SavingPrincessWorld(World):
    """ 
    Explore a space station crawling with rogue machines and even rival bounty hunters
    with the same objective as you - but with far, far different intentions!

    Expand your arsenal as you collect upgrades to your trusty arm cannon and armor!
    """  # Excerpt from itch
    game = GAME_NAME
    web = SavingPrincessWeb()

    topology_present = False

    item_name_to_id = {key: value.code for key, value in Items.item_dict.items()}
    location_name_to_id = {key: value.code for key, value in Locations.location_dict.items()}

    item_name_groups = {
        "Weapons": {key for key in Items.item_dict_weapons.keys()},
        "Upgrades": {key for key in Items.item_dict_upgrades.keys()},
        "Keys": {key for key in Items.item_dict_keys.keys()},
        "Filler": {key for key in Items.item_dict_filler.keys()},
        "Traps": {key for key in Items.item_dict_traps.keys()},
    }

    options_dataclass: ClassVar[Type[PerGameCommonOptions]] = Options.SavingPrincessOptions
    options: Options.SavingPrincessOptions

    is_pool_expanded: bool = False
    music_table: List[int] = [i for i in range(16)]

    def generate_early(self) -> None:
        self.is_pool_expanded = self.options.expanded_pool > 0
        if self.options.music_shuffle:
            self.random.shuffle(self.music_table)
            # find zzz and purple and swap them back to their original positions
            for song_id in [9, 13]:
                song_index = self.music_table.index(song_id)
                t = self.music_table[song_id]
                self.music_table[song_id] = song_id
                self.music_table[song_index] = t

    def create_regions(self) -> None:
        from .Regions import create_regions
        create_regions(self.multiworld, self.player, self.is_pool_expanded)

    def create_items(self) -> None:
        items_made: int = 0

        # now, for each item
        item_dict = Items.item_dict_expanded if self.is_pool_expanded else Items.item_dict_base
        for item_name, item_data in item_dict.items():
            # create count copies of the item
            for i in range(item_data.count):
                self.multiworld.itempool.extend([self.create_item(item_name)])
            items_made += item_data.count
            # and create count_extra useful copies of the item
            original_item_class: ItemClass = item_data.item_class
            item_data.item_class = ItemClass.useful
            for i in range(item_data.count_extra):
                self.multiworld.itempool.extend([self.create_item(item_name)])
            item_data.item_class = original_item_class
            items_made += item_data.count_extra

        # get the number of unfilled locations, that is, locations for items - items generated
        location_count = len(Locations.location_dict_base)
        if self.is_pool_expanded:
            location_count = len(Locations.location_dict_expanded)
        junk_count: int = location_count - items_made

        # and generate as many junk items as unfilled locations
        for i in range(junk_count):
            self.multiworld.itempool.extend([self.create_item(self.get_filler_item_name())])

    def create_item(self, name: str) -> Items.SavingPrincessItem:
        return Items.item_dict[name].create_item(self.player)

    def get_filler_item_name(self) -> str:
        filler_list = list(Items.item_dict_filler.keys())
        # check if this is going to be a trap
        if self.random.randint(0, 99) < self.options.trap_chance:
            filler_list = list(Items.item_dict_traps.keys())
        # and return one of the names at random
        return self.random.choice(filler_list)

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "death_link": self.options.death_link.value,
            "expanded_pool": self.options.expanded_pool.value,
            "instant_saving": self.options.instant_saving.value,
            "sprint_availability": self.options.sprint_availability.value,
            "cliff_weapon_upgrade": self.options.cliff_weapon_upgrade.value,
            "ace_weapon_upgrade": self.options.ace_weapon_upgrade.value,
            "shake_intensity": self.options.shake_intensity.value,
            "iframes_duration": self.options.iframes_duration.value,
            "music_table": self.music_table,
        }

    def set_rules(self):
        from .Rules import set_rules
        set_rules(self)
