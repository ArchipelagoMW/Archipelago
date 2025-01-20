import typing
import math
import logging

from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from worlds.AutoWorld import WebWorld, World

from .items import Ty1Item, ty1_item_table, create_items
from .locations import ty1_location_table
from .options import Ty1Options, ty1_option_groups
from .regions import create_regions, connect_regions, ty1_levels, Ty1LevelCode
#from .Rules import set_rules


class Ty1Web(WebWorld):
    theme = "jungle"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Ty the Tasmanian Tiger 1 randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["xMcacutt"]
    )

    tutorials = [setup_en]
    option_groups = ty1_option_groups

class Ty1World(World):
    """
    Ty the Tasmanian Tiger is a 3D platformer collectathon created by Australian developers Krome Studios. Play as Ty and travel the Australian outback to snowy mountains to defeat Boss Cass and rescue your family from The Dreaming.
    """
    game: str = "Ty the Tasmanian Tiger"
    options_dataclass = Ty1Options
    options: Ty1Options
    topology_present = True
    item_name_to_id = {name: id for id, name in enumerate(ty1_item_table)}
    location_name_to_id = {name: id for id, name in enumerate(ty1_location_table)}

    portal_map: typing.Dict[int, int]
    region_thegg_map: typing.Dict[int, int]
    boss_map: typing.Dict[int, int]

    web = Ty1Web()

    def fill_slot_data(self) -> dict:
        return {
            "ModVersion": 100,
            "Goal": self.options.goal.value,
            "LogicDifficulty": self.options.logic_difficulty,
            "ProgressiveElementals": self.options.progressive_elementals,
            "StartWithBoom": self.options.start_with_boom,
            "LevelShuffle": self.options.level_shuffle,
            "PortalMap": self.portal_map,
            "BossShuffle": self.options.boss_shuffle,
            "BossMap": self.boss_map,
            "LevelUnlockStyle": self.options.level_unlock_style,
            "ProgressiveLevel": self.options.progressive_level,
            "HubTheggCounts": self.options.hub_te_counts,
            "RegionTheggMap": self.region_thegg_map,
            "Cogsanity": self.options.cogsanity.value,
            "Bilbysanity": self.options.bilbysanity.value,
            "Attributesanity": self.options.attributesanity.value,
            "Framesanity": self.options.framesanity.value,
            "DeathLink": self.options.death_link.value,
            "PlayerNum": self.player,
        }

    def create_item(self, name: str) -> Item:
        item_info = ty1_item_table[name]
        return Ty1Item(name, item_info[0], item_info[1], self.player)

    def create_items(self):
        create_items(self.multiworld, self.options, self.player)

    def create_regions(self):
        create_regions(self.multiworld, self.options, self.player)

