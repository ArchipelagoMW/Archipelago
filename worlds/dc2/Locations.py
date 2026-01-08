from enum import IntEnum
from typing import Optional, NamedTuple, Dict

from BaseClasses import Location, Region


class DC2LocationCategory(IntEnum):
    FLOOR = 0
    DUNGEON = 1
    RECRUIT = 2
    GEORAMA = 3
    MIRACLE_CHEST = 4
    BOSS = 5
    MISC = 6
    GEOSTONE = 7
    EVENT = 8
    SKIP = 9,
    KEY_ITEM = 10


class DC2LocationData(NamedTuple):
    id: int
    name: str
    default_item: str
    category: DC2LocationCategory


class DarkCloud2Location(Location):
    game: str = "Dark Cloud 2"
    category: DC2LocationCategory
    default_item_name: str

    def __init__(
            self,
            player: int,
            name: str,
            category: DC2LocationCategory,
            default_item_name: str,
            address: Optional[int] = None,
            parent: Optional[Region] = None):
        super().__init__(player, name, address, parent)
        self.default_item_name = default_item_name
        self.category = category

    @staticmethod
    def get_name_to_id() -> dict:
        base_id = 694200000
        table_offset = 1000

        table_order = [
            "Palm Brinks",
            "Underground Water Channel",
            "Sindain",
            "Jurak Mall",
            "Rainbow Butterfly Wood",
            "Balance Valley",
            "Starlight Temple",
            "Starlight Canyon",
            "Veniccio",
            "Lunatic Wisdom Laboratories",
            "Ocean's Roar Cave",
            "Heim Rada",
            "Gundorada Workshop",
            "Mount Gundor",
            "Moon Flower Palace"
        ]

        output = {}
        for i, region_name in enumerate(table_order):
            if len(location_tables[region_name]) > table_offset:
                raise Exception("A location table has {} entries, that is more than {} entries (table #{})".format(len(location_tables[region_name]), table_offset, i))
            output.update({location_data.name: location_data.id for location_data in location_tables[region_name]})
        return output
        
location_skip_categories = {
DC2LocationCategory.EVENT, DC2LocationCategory.SKIP
}

location_tables = {
    "Palm Brinks": [
        DC2LocationData(694201000, "PB: Miracle chest 1",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201001, "PB: Miracle chest 2",                      "Potato Pie",                       DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201002, "PB: Miracle chest 3",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
    ],
    "Underground Water Channel": [
        DC2LocationData(694202000, "UWC: Floor 1 - To the Outside World",      "Bread",                             DC2LocationCategory.FLOOR),
        DC2LocationData(694202001, "UWC: Floor 2 - Battle with Rats",          "Bread",                             DC2LocationCategory.FLOOR),
        DC2LocationData(694202002, "UWC: Floor 3 - Ghosts in the Channel",     "Bread",                             DC2LocationCategory.FLOOR),
        DC2LocationData(694202003, "UWC: Pump Room",                           "Bread",                             DC2LocationCategory.FLOOR),
        DC2LocationData(694203000, "UWC: Linda",                               "Bread",                             DC2LocationCategory.BOSS),
        DC2LocationData(694202004, "UWC: Floor 4 - Steve's Battle",            "Bread",                             DC2LocationCategory.FLOOR),
        DC2LocationData(694202005, "UWC: Floor 5 - Ghost in the Channel",      "Bread",                             DC2LocationCategory.FLOOR),
        DC2LocationData(694203001, "UWC: Halloween",                           "Bread",                             DC2LocationCategory.BOSS),
        DC2LocationData(694202006, "UWC: Chapter 1 Complete",                  "Chapter 1 Complete",                DC2LocationCategory.EVENT),
    ],
    "Sindain": [
        DC2LocationData(694204000, "S: Grape Juice",                           "Grape Juice",                      DC2LocationCategory.KEY_ITEM),
    ],
    "Jurak Mall": [
        DC2LocationData(694201003, "JM: Miracle chest 1",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201004, "JM: Miracle chest 2",                      "Potato Pie",                       DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201005, "JM: Miracle chest 3",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201006, "JM: Miracle chest 4",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201007, "JM: Miracle chest 5",                      "Potato Pie",                       DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201008, "JM: Miracle chest 6",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201009, "JM: Miracle chest 7",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201010, "JM: Miracle chest 8",                      "Potato Pie",                       DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201011, "JM: Miracle chest 9",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201012, "JM: Miracle chest 10",                      "Fruit of Eden",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201013, "JM: Miracle chest 11",                      "Potato Pie",                      DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201014, "JM: Miracle chest 12",                      "Fruit of Eden",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201015, "JM: Miracle chest 13",                      "Fruit of Eden",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201016, "JM: Miracle chest 14",                      "Fruit of Eden",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201017, "JM: Miracle chest 15",                      "Potato Pie",                      DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201018, "JM: Miracle chest 16",                      "Fruit of Eden",                   DC2LocationCategory.MIRACLE_CHEST),

        DC2LocationData(694204001, "JM: Lafrescia Seed",                        "Lafrescia Seed",                  DC2LocationCategory.KEY_ITEM),
    ],
    "Rainbow Butterfly Wood": [    
        DC2LocationData(694202007, "RBW: Floor 1 - Frightening Forest",        "Bread",                             DC2LocationCategory.FLOOR),
        DC2LocationData(694202008, "RBW: Floor 2 - Strange Tree",              "Bread",                             DC2LocationCategory.FLOOR),
        DC2LocationData(694202009, "RBW: Floor 3 - Rolling Shells",            "Bread",                             DC2LocationCategory.FLOOR),
        DC2LocationData(694202010, "RBW: Fish Monster Swamp",                  "Bread",                             DC2LocationCategory.FLOOR),
        DC2LocationData(694202011, "RBW: Floor 4 - This is a Geostone?",       "Bread",                             DC2LocationCategory.FLOOR),
        DC2LocationData(694202012, "RBW: Floor 5 - Noise in the Forest",       "Bread",                             DC2LocationCategory.FLOOR),
        DC2LocationData(694202013, "RBW: Floor 6 - I'm a Pixie",               "Bread",                             DC2LocationCategory.FLOOR),
        DC2LocationData(694202014, "RBW: Floor 7 - Legendary Killer Snake",    "Bread",                             DC2LocationCategory.FLOOR),
        DC2LocationData(694202015, "RBW: Floor 8 - Grotesque Spider Lady",     "Bread",                             DC2LocationCategory.FLOOR),
        DC2LocationData(694203002, "RBW: Rainbow Butterfly",                   "Bread",                             DC2LocationCategory.BOSS),
        DC2LocationData(694202016, "RBW: Chapter 2 Complete",                  "Chapter 2 Complete",               DC2LocationCategory.EVENT),

       # Star Floors
        DC2LocationData(694202017, "RBW: Floor 9 - Looking for the Earth Gem", "Bread",                             DC2LocationCategory.FLOOR),
        DC2LocationData(694202018, "RBW: Floor 10 - Something Rare Here!",      "Bread",                            DC2LocationCategory.FLOOR),
        DC2LocationData(694202019, "RBW: Floor 11 - Scary Tree",                "Bread",                            DC2LocationCategory.FLOOR),
        DC2LocationData(694203003, "RBW: Trentos",                              "Bread",                            DC2LocationCategory.BOSS),

        DC2LocationData(694204002, "RBW: Fishing Rod",                         "Fishing Rod",                      DC2LocationCategory.KEY_ITEM),
        DC2LocationData(694204003, "RBW: Earth Gem",                           "Earth Gem",                        DC2LocationCategory.KEY_ITEM),
    ],
    "Balance Valley": [

    ],
    "Starlight Temple": [
        DC2LocationData(694201019, "ST: Miracle chest 1",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201020, "ST: Miracle chest 2",                      "Potato Pie",                       DC2LocationCategory.MIRACLE_CHEST),

        # Missable
        DC2LocationData(694201021, "ST: Miracle chest 3",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201022, "ST: Miracle chest 4",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201023, "ST: Miracle chest 5",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201024, "ST: Miracle chest 6",                      "Witch Parfait",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201025, "ST: Miracle chest 7",                      "Potato Pie",                       DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201026, "ST: Miracle chest 8",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201027, "ST: Miracle chest 9",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201028, "ST: Miracle chest 10",                     "Emerald",                          DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201029, "ST: Miracle chest 11",                     "Pearl",                            DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201030, "ST: Miracle chest 12",                     "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201031, "ST: Miracle chest 13",                     "Witch Parfait",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201032, "ST: Miracle chest 14",                     "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201033, "ST: Miracle chest 15",                     "Potato Pie",                       DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201034, "ST: Miracle chest 16",                     "Witch Parfait",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201035, "ST: Miracle chest 17",                     "Potato Pie",                       DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201036, "ST: Miracle chest 18",                     "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201037, "ST: Miracle chest 19",                     "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201038, "ST: Miracle chest 20",                     "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201039, "ST: Miracle chest 21",                     "Potato Pie",                       DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201040, "ST: Miracle chest 22",                     "Witch Parfait",                    DC2LocationCategory.MIRACLE_CHEST),

        DC2LocationData(694204004, "ST: Starglass",                            "Starglass",                        DC2LocationCategory.KEY_ITEM),
        DC2LocationData(694204005, "ST: Miracle Dumplings",                    "Miracle Dumplings",                DC2LocationCategory.KEY_ITEM),
    ],
    "Starlight Canyon": [
        DC2LocationData(694202020, "SC: Floor 1 - Headlong Dash",               "Bread",                            DC2LocationCategory.FLOOR),
        DC2LocationData(694202021, "SC: Floor 2 - Fire and Ice Don't Mix",      "Bread",                            DC2LocationCategory.FLOOR),
        DC2LocationData(694202022, "SC: Floor 3 - Earth-Shaking Demon",         "Bread",                            DC2LocationCategory.FLOOR),
        DC2LocationData(694202023, "SC: Floor 4 - Powerful Yo-Yo Robot",        "Bread",                            DC2LocationCategory.FLOOR),
        DC2LocationData(694202024, "SC: Floor 5 - Elephant Army in the Valley", "Bread",                            DC2LocationCategory.FLOOR),
        DC2LocationData(694202025, "SC: Floor 6 - Dangerous Treasure Chest",    "Bread",                            DC2LocationCategory.FLOOR),
        DC2LocationData(694202026, "SC: Floor 7 - Little Dragon Counterattack", "Bread",                            DC2LocationCategory.FLOOR),
        DC2LocationData(694202027, "SC: Barga's Valley",                        "Bread",                            DC2LocationCategory.FLOOR),
        DC2LocationData(694202028, "SC: Floor 8 - Warrior in Starlight Canyon", "Bread",                            DC2LocationCategory.FLOOR),
        DC2LocationData(694202029, "SC: Floor 9 - Smiling Fairy Village",       "Bread",                            DC2LocationCategory.FLOOR),
        DC2LocationData(694202030, "SC: Floor 10 - Cursed Mask",                "Bread",                            DC2LocationCategory.FLOOR),
        DC2LocationData(694202031, "SC: Floor 11 - We're the Roly-Poly Brothers", "Bread",                          DC2LocationCategory.FLOOR),
        DC2LocationData(694202032, "SC: Floor 12 - Dragon Slayer",              "Bread",                            DC2LocationCategory.FLOOR),
        DC2LocationData(694203004, "SC: Memo Eater",                            "Bread",                            DC2LocationCategory.BOSS),
        DC2LocationData(694202033, "SC: Floor 13 - Rama Priests Like Cheese",   "Bread",                            DC2LocationCategory.FLOOR),
        DC2LocationData(694202034, "SC: Floor 14 - Nature's Threat",            "Bread",                            DC2LocationCategory.FLOOR),
        DC2LocationData(694202035, "SC: Floor 15 - Moon Baron",                 "Bread",                            DC2LocationCategory.FLOOR),
        DC2LocationData(694202036, "SC: Floor 16 - Lighthouse Appears",         "Bread",                            DC2LocationCategory.FLOOR),
        DC2LocationData(694202037, "SC: Evil Flame and Gaspard",                "Bread",                            DC2LocationCategory.BOSS),
        DC2LocationData(694202038, "SC: Chapter 3 Complete",                    "Chapter 3 Complete",              DC2LocationCategory.EVENT),

        # Star path floors
        DC2LocationData(694202039, "SC: Floor 17 - Looking for the Wind Gem",   "Bread",                            DC2LocationCategory.FLOOR),
        DC2LocationData(694202040, "SC: Floor 18 - Evil Spirit in the Valley",  "Bread",                            DC2LocationCategory.FLOOR),
        DC2LocationData(694202041, "SC: Floor 19 - Brave Warriors in the Valley", "Bread",                          DC2LocationCategory.FLOOR),
        DC2LocationData(694203005, "SC: Lapis Garter",                           "Bread",                           DC2LocationCategory.BOSS),

        DC2LocationData(694204006, "SC: White Windflower",                      "White Windflower",                DC2LocationCategory.KEY_ITEM),
        DC2LocationData(694204007, "SC: Wind Gem",                              "Wind Gem",                        DC2LocationCategory.KEY_ITEM),
    ],
    "Veniccio": [

    ],
    "Lunatic Wisdom Laboratories": [
        DC2LocationData(694201041, "LWL: Miracle chest 1",                      "Fruit of Eden",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201042, "LWL: Miracle chest 2",                      "Fruit of Eden",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201043, "LWL: Miracle chest 3",                      "Potato Pie",                      DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201044, "LWL: Miracle chest 4",                      "Fruit of Eden",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201045, "LWL: Miracle chest 5",                      "Witch Parfait",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201046, "LWL: Miracle chest 6",                      "Fruit of Eden",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201047, "LWL: Miracle chest 7",                      "Potato Pie",                      DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201048, "LWL: Miracle chest 8",                      "Fruit of Eden",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201049, "LWL: Miracle chest 9",                      "Witch Parfait",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201050, "LWL: Miracle chest 10",                     "Fruit of Eden",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201051, "LWL: Miracle chest 11",                     "Witch Parfait",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201052, "LWL: Miracle chest 12",                     "Fruit of Eden",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201053, "LWL: Miracle chest 13",                     "Potato Pie",                      DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201054, "LWL: Miracle chest 14",                     "Witch Parfait",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201055, "LWL: Miracle chest 15",                     "Fruit of Eden",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201056, "LWL: Miracle chest 16",                     "Fruit of Eden",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201057, "LWL: Miracle chest 17",                     "Potato Pie",                      DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201058, "LWL: Miracle chest 18",                     "Fruit of Eden",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201059, "LWL: Miracle chest 19",                     "Witch Parfait",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201060, "LWL: Miracle chest 20",                     "Potato Pie",                      DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201061, "LWL: Miracle chest 21",                     "Ruby",                            DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201062, "LWL: Miracle chest 22",                     "Peridot",                         DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201063, "LWL: Miracle chest 23",                     "Sapphire",                        DC2LocationCategory.MIRACLE_CHEST),

        DC2LocationData(694204008, "LWL: Electric Worm",                       "Electric Worm",                     DC2LocationCategory.KEY_ITEM),
        DC2LocationData(694204009, "LWL: Shell Talkie",                        "Shell Talkie",                      DC2LocationCategory.KEY_ITEM),
    ],
    "Ocean's Roar Cave": [
        DC2LocationData(694202042, "ORC: Floor 1 - Pirates!",                  "Bread",                              DC2LocationCategory.FLOOR),
        DC2LocationData(694202043, "ORC: Floor 2 - Tons of Fish",              "Bread",                              DC2LocationCategory.FLOOR),
        DC2LocationData(694202044, "ORC: Floor 3 - Tank and Boss",             "Bread",                              DC2LocationCategory.FLOOR),
        DC2LocationData(694202045, "ORC: Floor 4 - Water Monster",             "Bread",                              DC2LocationCategory.FLOOR),
        DC2LocationData(694202046, "ORC: Floor 5 - Scary Auntie Medusa",       "Bread",                              DC2LocationCategory.FLOOR),
        DC2LocationData(694202047, "ORC: Floor 6 - Sand Molers",               "Bread",                              DC2LocationCategory.FLOOR),
        DC2LocationData(694202048, "ORC: Floor 7 - Bat Den",                   "Bread",                              DC2LocationCategory.FLOOR),
        DC2LocationData(694202049, "ORC: Floor 8 - Pirates' Hideout",          "Bread",                              DC2LocationCategory.FLOOR),
        DC2LocationData(694202050, "ORC: Cave of Ancient Murals",              "Bread",                              DC2LocationCategory.FLOOR),
        DC2LocationData(694202051, "ORC: Floor 9 - Wandering Zappy",           "Bread",                              DC2LocationCategory.FLOOR),
        DC2LocationData(694202052, "ORC: Floor 10 - Banquet of the Dead",      "Bread",                              DC2LocationCategory.FLOOR),
        DC2LocationData(694202053, "ORC: Floor 11 - Improvements",             "Bread",                              DC2LocationCategory.FLOOR),
        DC2LocationData(694202054, "ORC: Floor 12 - Return of the Serpent",    "Bread",                              DC2LocationCategory.FLOOR),
        DC2LocationData(694202055, "ORC: Floor 13 - Cursed Sea",               "Bread",                              DC2LocationCategory.FLOOR),
        DC2LocationData(694202056, "ORC: Floor 14 - Sea of Atrocity",          "Bread",                              DC2LocationCategory.FLOOR),
        DC2LocationData(694203006, "ORC: Dr. Jaming",                          "Bread",                              DC2LocationCategory.BOSS),
        DC2LocationData(694202057, "ORC: Chapter 4 Complete",                  "Chapter 4 Complete",                DC2LocationCategory.EVENT),

        # Star path floors
        DC2LocationData(694202058, "ORC: Floor 15 - Looking for the Water Gem", "Bread",                             DC2LocationCategory.FLOOR),
        DC2LocationData(694202059, "ORC: Floor 16 - Pirates' Revenge",          "Bread",                             DC2LocationCategory.FLOOR),
        DC2LocationData(694202060, "ORC: Floor 17 - Death Ocean",               "Bread",                             DC2LocationCategory.FLOOR),
        DC2LocationData(694203007, "ORC: Sea Dragon",                           "Bread",                             DC2LocationCategory.BOSS),

        DC2LocationData(694204010, "ORC: Secret Dragon Remedy",                 "Secret Dragon Remedy",             DC2LocationCategory.KEY_ITEM),
        DC2LocationData(694204011, "ORC: Water Gem",                            "Water Gem",                        DC2LocationCategory.KEY_ITEM),
    ],
    "Heim Rada": [

    ],
    "Gundorada Workshop": [
        DC2LocationData(694201064, "GW: Miracle chest 1",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201065, "GW: Miracle chest 2",                      "Potato Pie",                       DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201066, "GW: Miracle chest 3",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201067, "GW: Miracle chest 4",                      "Witch Parfait",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201068, "GW: Miracle chest 5",                      "Potato Pie",                       DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201069, "GW: Miracle chest 6",                      "Witch Parfait",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201070, "GW: Miracle chest 7",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201071, "GW: Miracle chest 8",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201072, "GW: Miracle chest 9",                      "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201073, "GW: Miracle chest 10",                     "Potato Pie",                       DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201074, "GW: Miracle chest 11",                     "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201075, "GW: Miracle chest 12",                     "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201076, "GW: Miracle chest 13",                     "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201077, "GW: Miracle chest 14",                     "Potato Pie",                       DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201078, "GW: Miracle chest 15",                     "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201079, "GW: Miracle chest 16",                     "Witch Parfait",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201080, "GW: Miracle chest 17",                     "Potato Pie",                       DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201081, "GW: Miracle chest 18",                     "Witch Parfait",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201082, "GW: Miracle chest 19",                     "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201083, "GW: Miracle chest 20",                     "Fruit of Eden",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201084, "GW: Miracle chest 21",                     "Witch Parfait",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201085, "GW: Miracle chest 22",                     "Witch Parfait",                    DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201086, "GW: Miracle chest 23",                     "Diamond",                          DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201087, "GW: Miracle chest 24",                     "Turquoise",                        DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201088, "GW: Miracle chest 25",                     "Topaz",                            DC2LocationCategory.MIRACLE_CHEST),

        DC2LocationData(694204012, "GW: Time Bomb",                            "Time Bomb",                        DC2LocationCategory.KEY_ITEM),
        DC2LocationData(694204013, "GW: Fire Horn",                            "Fire Horn",                        DC2LocationCategory.KEY_ITEM)
    ],
    "Mount Gundor": [
        DC2LocationData(694202061, "MG: Floor 1 - Battle with Griffon's Army", "Bread",                             DC2LocationCategory.FLOOR),
        DC2LocationData(694202062, "MG: Floor 2 - Mt. Gundor Wind",             "Bread",                            DC2LocationCategory.FLOOR),
        DC2LocationData(694202063, "MG: Floor 3 - Little Dragons on the Mountain", "Bread",                         DC2LocationCategory.FLOOR),
        DC2LocationData(694202064, "MG: Floor 4 - Steam Goyone",                 "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202065, "MG: Floor 5 - Mountain Baddie Appears",      "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202066, "MG: Floor 6 - Magmanoff",                    "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202067, "MG: Floor 7 - Danger Zone",                  "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202068, "MG: Floor 8 - Secret of Fire Mountain",      "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202069, "MG: Floor 9 - Deathtrap",                    "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202070, "MG: Floor 10 - Desperation on the Mountain", "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202071, "MG: Floor 11 - Pains in the Neck",           "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202072, "MG: Mount Gundor Peak",                      "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202073, "MG: Floor 12 - Walking the Path of Flames",  "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202074, "MG: Floor 13 - Burning Undead",              "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202075, "MG: Floor 14 - Fire Dragon",                 "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202076, "MG: Floor 15 - Treasure Chest Danger Zone",  "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202077, "MG: Floor 16 - Road to the River of Flames", "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694203008, "MG: Gaspard",                                "Bread",                           DC2LocationCategory.BOSS),
        DC2LocationData(694202078, "MG: Chapter 5 Complete",                     "Chapter 5 Complete",             DC2LocationCategory.EVENT),

        # Star path floors
        DC2LocationData(694202079, "MG: Floor 17 - Looking for the Fire Gem",    "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202080, "MG: Floor 18 - Explosive Hot Spring",        "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202081, "MG: Floor 19 - Crazy Mountain",              "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694203009, "MG: Inferno",                                "Bread",                           DC2LocationCategory.BOSS),

        DC2LocationData(694204014, "MG: Fire Gem",                               "Fire Gem",                       DC2LocationCategory.KEY_ITEM),
    ],
    "Moon Flower Palace": [
        DC2LocationData(694201089, "MFP: Miracle chest 1",                      "Fruit of Eden",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201090, "MFP: Miracle chest 2",                      "Potato Pie",                      DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201091, "MFP: Miracle chest 3",                      "Fruit of Eden",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201092, "MFP: Miracle chest 4",                      "Witch Parfait",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201093, "MFP: Miracle chest 5",                      "Fruit of Eden",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201094, "MFP: Miracle chest 6",                      "Potato Pie",                      DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201095, "MFP: Miracle chest 7",                      "Fruit of Eden",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201096, "MFP: Miracle chest 8",                      "Witch Parfait",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201097, "MFP: Miracle chest 9",                      "Fruit of Eden",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201098, "MFP: Miracle chest 10",                     "Potato Pie",                      DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201099, "MFP: Miracle chest 11",                     "Fruit of Eden",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201100, "MFP: Miracle chest 12",                     "Witch Parfait",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201101, "MFP: Miracle chest 13",                     "Fruit of Eden",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201102, "MFP: Miracle chest 14",                     "Potato Pie",                      DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201103, "MFP: Miracle chest 15",                     "Fruit of Eden",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201104, "MFP: Miracle chest 16",                     "Witch Parfait",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201105, "MFP: Miracle chest 17",                     "Fruit of Eden",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201106, "MFP: Miracle chest 18",                     "Potato Pie",                      DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201107, "MFP: Miracle chest 19",                     "Fruit of Eden",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201108, "MFP: Miracle chest 20",                     "Witch Parfait",                   DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201109, "MFP: Miracle chest 21",                     "Potato Pie",                      DC2LocationCategory.MIRACLE_CHEST),
        DC2LocationData(694201110, "MFP: Miracle chest 22",                     "Witch Parfait",                   DC2LocationCategory.MIRACLE_CHEST),

        DC2LocationData(694202082, "MFP: Floor 1 - Ancient Wind",               "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202083, "MFP: Floor 2 - Card Warriors Gather",       "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202084, "MFP: Floor 3 - Dangerous Treasure",         "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202085, "MFP: Floor 4 - Zombie Zone",                "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202086, "MFP: Floor 5 - Feeling Out of Place",       "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202087, "MFP: Floor 6 - Living Statue",              "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202088, "MFP: Floor 7 - Danger Zone",                "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202089, "MFP: Floor 8 - Scary Women",                "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202090, "MFP: Floor 9 - Hell Elephant",              "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202091, "MFP: Floor 10 - Crush the Undead",          "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202092, "MFP: Garden",                               "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202093, "MFP: Floor 11 - Missing Gem Dealer",        "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202094, "MFP: Floor 12 - Max's Longest Day",         "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202095, "MFP: Floor 13 - Hell's Corridor",           "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202096, "MFP: Floor 14 - Monica All Alone",          "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202097, "MFP: Floor 15 - Raging Spirits",            "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202098, "MFP: Floor 16 - Lonely Machine",            "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202099, "MFP: Floor 17 - Nobility",                  "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202100, "MFP: Floor 18 - Palace Watchdog",           "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202101, "MFP: Floor 19 - Road to Memories",          "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202102, "MFP: Alexandra's Room",                     "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202103, "MFP: Floor 20 - Final Trump Card",          "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202104, "MFP: Floor 21 - Elemental Party",           "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202105, "MFP: Floor 22 - Wandering Knight's Soul",   "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202106, "MFP: Floor 23 - Beware Carelessness",       "Bread",                           DC2LocationCategory.FLOOR),
        DC2LocationData(694202107, "MFP: Floor 24 - Final Battle",              "Bread",                           DC2LocationCategory.FLOOR),

        DC2LocationData(694204015, "MFP: Flower of the Sun",                    "Flower of the Sun",              DC2LocationCategory.KEY_ITEM)
    ],
    
}

location_dictionary: Dict[str, DC2LocationData] = {}
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})
