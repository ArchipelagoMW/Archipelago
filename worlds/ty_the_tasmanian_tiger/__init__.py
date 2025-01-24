import typing
from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from worlds.AutoWorld import WebWorld, World

from .items import Ty1Item, ty1_item_table, create_items, ItemData
from .locations import ty1_location_table
from .options import Ty1Options, ty1_option_groups
from .regions import create_regions, connect_regions, ty1_levels, Ty1LevelCode, connect_all_regions

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
    item_name_to_id = {name: item.id for name, item in ty1_item_table.items()}
    location_name_to_id = {name: item.id for name, item in ty1_location_table.items()}
    id_to_item_name = {item.id: name for name, item in ty1_item_table.items()}

    portal_map: typing.List[Ty1LevelCode] = [Ty1LevelCode.A1, Ty1LevelCode.A2, Ty1LevelCode.A3,
                                            Ty1LevelCode.B1, Ty1LevelCode.B2, Ty1LevelCode.B3,
                                            Ty1LevelCode.C1, Ty1LevelCode.C2, Ty1LevelCode.C3]
    boss_map: typing.List[Ty1LevelCode] = [Ty1LevelCode.A4, Ty1LevelCode.D4, Ty1LevelCode.C4]

    web = Ty1Web()

    def fill_slot_data(self) -> id:
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
        return Ty1Item(name, item_info.classification, item_info.id, self.player)

    def create_items(self):
        create_items(self.multiworld, self.options, self.player)

    def create_regions(self):
        create_regions(self.multiworld, self.options, self.player)
        connect_all_regions(self.multiworld, self.player, self.options, self.portal_map, self.boss_map)
        from Utils import visualize_regions
        state = self.multiworld.get_all_state(False)
        print("HELLO WORLD")
        state.update_reachable_regions(self.player)
        visualize_regions(self.get_region("Menu"), "ty_the_tasmanian_tiger.puml", show_entrance_names=True)




