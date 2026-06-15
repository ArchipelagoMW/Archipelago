from typing import TYPE_CHECKING, NamedTuple
from enum import StrEnum, Enum

from BaseClasses import ItemClassification

if TYPE_CHECKING:
    from .. import OkamiWorld


class RegionNames(StrEnum):
    MENU = "Menu"

    # Eastern Nippon

    ## Cursed Kamiki
    CURSED_KAMIKI = "Cursed Kamiki"

    ## River of the Heavens
    RIVER_OF_THE_HEAVENS_KAMIKI = "River of the Heavens (Kamiki side)"
    RIVER_OF_THE_HEAVENS_NAGI = "River of the Heavens (Nagi side)"

    ## Cave of Nagi
    CAVE_OF_NAGI = "Cave of Nagi"

    ## Kamiki Village
    ### Exteriors
    STONE_KAMIKI = "Kamiki Village (Stone state)"
    KAMIKI_VILLAGE = "Kamiki Village"
    KAMIKI_ISLANDS = "Kamiki Village Islands"
    ### Interiors
    KUSHIS_HOUSE = "Kushi's house"
    SUSANOS_HOUSE = "Susano's house"
    SUSANOS_UNDERGROUD = "Susano's Secret Underground Meditation Chamber"
    ORANGES_HOUSE = "Mr and Mrs Orange's house"
    # Special Region te check for merchant avilability for its random items
    KAMIKI_MERCHANT = "Kamiki Village Merchant"

    ## Shinshu Field
    CURSED_SHINSHU_FIELD = "Cursed Shinshu Field"
    # Exits, locations, events etc... Common to both states of Shinshu
    SHINSHU_LOGIC_COMMON = "Shinshu Field (Common)"
    SHINSHU_FIELD = "Shinshu Field"
    SHINSHU_FIELD_AGATA_CAVE = "Shinshu Field (Cave to Agata Forest)"
    TAMA_HOUSE = "Tama's house"
    SHINSHU_PLATEAU = "Shinshu Field Plateau"
    SHINSHU_AGATA_SHORTCUT_LEDGE = "Ledge Shortcut From Agata Forest"

    ## HANA VALLEY
    CURSED_HANA_VALLEY = "Cursed Hana Valley"
    HANA_VALLEY = "Hana Valley"
    HANA_VALLEY_SAKIGAMI = " Hana Valley - Sakigami sequence"

    ## AGATA FOREST
    CURSED_AGATA_FOREST = "Cursed Agata Forest"
    AGATA_COMMON_LOGIC = "Agata Forest (Common)"
    AGATA_FOREST_WAKA = "Agata Forest (Pre-waka fight)"
    AGATA_FOREST = "Agata Forest"
    AGATA_FOREST_TAKA = "Agata Forest (Behind Bridge to Taka Pass)"
    ### INTERIORS
    FAWNS_HOUSE = "Madame Fawn's House"

    ## TSUTA RUINS
    TSUTA_RUINS_1F_MAIN_PART = "Tsuta Ruins (1F - Main Part)"
    TSUTA_RUINS_MUSHROOMS = "Tsuta Ruins (Mushrooms)"
    TSUTA_RUINS_LEFT_SIDE = "Tsuta Ruins (Left Side)"
    TSUTA_RUINS_DEVIL_GATES = "Tsuta Ruins (Devil Gates)"
    TSUTA_RUINS_CENTRAL_STATUE = "Tsuta Ruins (Inside central Statue)"
    TSUTA_RUINS_SPIDER = "Tsuta Ruins (Spider Queen's lair)"

    ## TAKA PASS
    CURSED_TAKA_PASS = "Curesd Taka Pass"
    TAKA_COMMON_LOGIC = "Taka Pass (Common)"
    CURSED_TAKA_PASS_WAKA = "Cursed Taka Pass (Waka Fight)"
    CURSED_TAKA_PASS_CAVE = "Cursed Taka Pass (Cave)"
    CURSED_TAKA_PASS_GUARDIAN_SAPLING = "Cursed Taka Pass (Guardian Sapling)"
    TAKA_PASS = "Taka Pass"
    TAKA_PASS_CAVE = "Taka Pass Cave"

    ## KUSA VILLAGE
    KUSA_VILLAGE = "Kusa Village"
    KUSA_VILLAGE_BLOCKHEAD = "Kusa Village (Blockhead cave)"

    ### INTERIORS
    BAMBOO_HOUSE = "Mr Bamboo's house"
    KUSA_INN = "Kusa Village Inn"

    ## SASA SANCTUARY
    SASA_SANCTUARY_ENTRANCE = "Sasa Sanctuary (Entrance)"
    SASA_SANCTUARY = "Sasa Sanctuary"
    SASA_SANCTUARY_BAMBOO = "Sasa Sanctuary (Bamboo Grove)"

    ## GALE SHRINE
    GALE_SHRINE_ENTRANCE = "Gale Shrine (1F Entrance)"
    GALE_SHRINE = "Gale Shrine (1F Main room)"
    GALE_SHRINE_LIFT = "Gale Shrine (Lift)"
    GALE_SHRINE_2F = "Gale Shrine (2F)"
    GALE_SHRINE_3F = "Gale Shrine (3F)"
    GALE_SHRINE_BACK = "Gale Shrine (After Windmill Bridges)"
    GALE_SHRINE_BOSS = "Gale Shrine (Crimson Helm Arena)"

    ## MOON CAVE
    MOON_CAVE_OUTSIDE = "Moon Cave (Entrance outside)"
    MOON_CAVE_BROKEN_STAIRS = "Moon Cave (Broken stairs)"
    MOON_CAVE_UNDERGROUND_ENTRANCE = "Moon Cave (Underground Entrance)"
    CALCIFIED_CAVERN = "Calcified Cavern"
    MOON_CAVE = "Moon Cave (1F Main Room)"
    MOON_CAVE_1F_LOCKED_CAVE = "Moon Cave (1F locked cave)"
    MOON_CAVE_1F_LOCKED_CAVE_BACK = "Moon Cave (1F locked cave back)"
    MOON_CAVE_2F_GEYSER_RAFTER = "Moon Cave (2F Geyser rafter)"
    MOON_CAVE_3F = "Moon Cave (3F Main room)"
    MOON_CAVE_B1F_LAKE = "Moon Cave (B1F Underground Lake)"
    MOON_CAVE_B1F_UNDER_LIFT = "Moon Cave (B1F Under Lift)"
    MOON_CAVE_B2F_LIFT = "Moon Cave (B2F Under Lift)"
    MOON_CAVE_B2F_FROZEN_STATUE = "Moon Cave (B2F Frozen Statue Room)"
    MOON_CAVE_B2F_OTHER_LIFT = "Moon Cave (B2F Lift Back)"
    MOON_CAVE_B2F_BOMBABLE = "Moon Cave (B2F Behind Bombable wall)"
    MOON_CAVE_KITCHEN_BACK = "Moon Cave (1F Kitchen Back)"
    MOON_CAVE_3F_FIRE_EYE = "Moon Cave (3F Fire Eye Room)"
    MOON_CAVE_3F_SAND = "Moon Cave (3F Sand room)"
    MOON_CAVE_2F_SAND_PIT = "Moon Cave (2F Sand pit)"
    MOON_CAVE_3F_RAFTERS_AFTER_SAND = "Moon Cave (3F Rafters after sand room)"
    MOON_CAVE_2F_RAFTERS_CHEST = "Moon Cave (2F Chest Rafter)"
    MOON_CAVE_4F_RAFTERS = "Moon Cave (4F Rafters)"
    MOON_CAVE_4F_CANON = "Moon Cave (4F Canon)"
    MOON_CAVE_4F_AFTER_CANON = "Moon Cave (4F after canon)"
    MOON_CAVE_OROCHI = "Moon Cave (Orochi)"

    ## CITY CHECKPOINT
    CITY_CHECKPOINT_TAKA = "City Checkpoint (Taka side)"
    CITY_CHECKPOINT_DRAWBRIDGE = "City Checkpoint Drawbridge"
    CITY_CHECKPOINT_RYOSHIMA = "City Checkpoint (Ryoshima side)"
    CITY_CHECKPOINT_RIVER = "City Checkpoint (River)"

    # Western Nippon

    ## RYOSHIMA COAST
    CURSED_RYOSHIMA_COAST = "Cursed Ryoshima Coast"
    CURSED_RYOSHIMA_COAST_GUARDIAN_SAPLING_CAVE = "Cursed Ryoshima Coast"
    RYOSHIMA_COAST = "Ryoshima Coast"
    RYOSHIMA_COAST_SEA = "Ryoshima Coast (Sea)"
    RYOSHIMA_COAST_SEA_FAR = "Ryoshima Coast (Sea, far away)"
    RYOSHIMA_COAST_DOJO = "Ryoshima Coast (Dojo)"
    RYOSHIMA_COAST_SHIP_TOP = "Ryoshima Coast (Top of Sunken Ship)"
    RYOSHIMA_COAST_CATWALK_TOWER = "Ryoshima Coast (Catwalk Tower)"
    RYOSHIMA_COAST_SEIAN = "Ryoshima Coast (Near Seian City Entrance)"
    RYOSHIMA_COAST_SEIAN_ENCOUNTER = "Ryoshima Coast (Near Seian City Entrance Encounter)"
    RYOSHIMA_COAST_LUNAR_LAGOON = "Ryoshima Coast (Lunar Lagoon)"
    RYOSHIMA_COAST_WEST_PIER = "Ryoshima Coast (West of Pier)"
    ANKOKU_TEMPLE = "Ankoku Temple"
    RYOSHIMA_COAST_BANDIT_SPIDER = "Ryoshima Coast (Bandit spider cave)"

    ## SEIAN CITY
    ### COMMONERS QUARTER
    SEIAN_CITY_COMMONERS = "Sei-an City Commoners' Quarter"
    SEIAN_CITY_COMMONERS_DRY = "Sei-an City Commoners' Quarter (No water)"
    SEIAN_CITY_YAMA = "Sei-an City (Yama's restaurant)"
    SEIAN_CITY_FLOWERS = "Sei-an City (Mr. Flower's house)"
    SEIAN_CITY_SOUTHWEST = "Sei-an City (Southwest building)"
    SEIAN_CITY_TAO = "Sei-an City (Tao Troopers Headquarters)"
    SEIAN_CITY_TOOL_SHOP = "Sei-an City (Tool Shop)"
    SEIAN_CITY_WEAPON_SHOP = "Sei-an City (Weapon Shop)"
    SEIAN_CITY_BLOSSOM = "Sei-an City (Blossom's house)"

    ### ARISTOCRATIC QUARTERS
    SEIAN_CITY_BRIDGE_COMMONERS = "Sei-an City Lake Beewa Bridge (Commoner's Side)"
    SEIAN_CITY_BRIDGE_ARISTOCRATIC = "Sei-an City Lake Beewa Bridge(Aristocratic Side)"
    SEIAN_CITY_LECTURE_HALL = "Sei-an City (Lecture Hall)"
    SEIAN_CITY_ARISTOCRATIC_SICK = "Sei-an City Aristocratic Quarter (Sick)"
    # Since she's the only one in here to have a name, it's her house now.
    SEIAN_CITY_OKUNI = "Sei-an City (Okuni's house)"
    SEIAN_CITY_ARISTOCRATIC_NORTH_EAST = "Sei-an City Aristocratic Quarter (Northeast house)"
    SEIAN_CITY_CLOCK_TOWER = "Sei-an City (Clock tower)"
    SEIAN_CITY_ARISTOCRATIC = "Sei-an City Aristocratic Quarter"
    SEIAN_CITY_HIMIKO = "Sei-an City (Himiko's palace entrance)"
    SEIAN_CITY_TREASURE_WEST = "Sei-an City (Himiko's palace West Treasure Room)"
    SEIAN_CITY_TREASURE_EAST = "Sei-an City (Himiko's palace East Treasure Room)"
    SEIAN_CITY_GUARDS = "Sei-an City (Guards house)"
    SEIAN_CITY_LAKE = "Sei-an City (Lake Beewa)"

    ## HIMIKO'S PALACE
    HIMIKO_PALACE = "Himiko's Palace"
    HIMIKO_CHAMBERS = "Himiko's Palace (Himiko's Chambers)"

    ## SUNKEN SHIP
    SUNKEN_SHIP_ENTRANCE = "Sunken Ship (Entrance)"
    SUNKEN_SHIP_SW_LOW = "Sunken Ship (Southwest Room, Low water)"
    SUNKEN_SHIP_BONES_LOW = "Sunken Ship (Bone Pile Room, Low water)"
    SUNKEN_SHIP_NW_LOW = "Sunken Ship (Northwest Room, Low water)"
    SUNKEN_SHIP_SW_HIGH = "Sunken Ship (Southwest Room, High water)"
    SUNKEN_SHIP_BONES_HIGH = "Sunken Ship (Bone Pile Room, High water)"
    SUNKEN_SHIP_NW_HIGH = "Sunken Ship (Northwest Room, High water)"
    SUNKEN_SHIP_SE_HIGH = "Sunken Ship (Southeast Room, High water)"
    SUNKEN_SHIP_E_HALLWAY_HIGH = "Sunken Ship (East Hallway High water)"
    SUNKEN_SHIP_HANDS_HIGH = "Sunken Ship (Hands room High water)"
    SUNKEN_SHIP_SE_LOW = "Sunken Ship (Southeast Room, Low water)"
    SUNKEN_SHIP_E_HALLWAY_LOW = "Sunken Ship (East Hallway Low water)"
    SUNKEN_SHIP_HANDS_LOW = "Sunken Ship (Hands room Low water)"
    SUNKEN_SHIP_SE_CHESTS = "Sunken Ship (Southeast Room Chests)"
    SUNKEN_SHIP_TREASURE = "Sunken Ship (Treasure Room)"
    SUNKEN_SHIP_S_LEDGE = "Sunken Ship (Southern room ledge)"

    ## IMPERIAL PALACE
    ### Regular Size
    IMPERIAL_PALACE_ENTRANCE = "Imperial Palace (Entrance)"
    IMPERIAL_PALACE = "Imperial Palace"

    ### Small Size
    IMPERIAL_PALACE_SMALL_ENTRANCE = "Imperial Palace (Small Size - Entrance)"
    IMPERIAL_PALACE_FEET_HELL = "Imperial Palace (Small Size - Feet Hell)"
    IMPERIAL_PALACE_WEST_CAVE = "Imperial Palace (Small Size - West cave after lockjaw)"
    IMPERIAL_PALACE_SPIDER_CAVE = "Imperial Palace (Small Size - Spider Cave)"
    IMPERIAL_PALACE_SPIDER_CAVE_TOP = "Imperial Palace (Small Size - Spider Cave Top Ledges)"
    IMPERIAL_PALACE_FLASK_ROOM = "Imperial Palace (Small Size - Mist Flask Room)"
    IMPERIAL_PALACE_POISON_SOZU = "Imperial Palace (Small Size - Poison Sōzu Room)"
    IMPERIAL_PALACE_EMPERORS_ROOM = "Imperial Palace (Small Size - Emperor's Bedroom)"
    IMPERIAL_PALACE_WEST_BEAM = "Imperial Palace (Small Size - West Beam)"
    IMPERIAL_PALACE_INSIDE_EMPEROR = "Imperial Palace (Small Size - Inside the Emperor's Body)"

    ## Northern Ryoshima Coast
    NORTHERN_RYOSHIMA_COAST_MANDATORY_FIGHT = "Nothern Rysohima Coast (Mandatory Fight)"
    NORTHERN_RYOSHIMA_COAST = "Nothern Rysohima Coast"
    NORTHERN_RYOSHIMA_COAST_MIST_WARP = "Northern Ryoshima Coast (Secret Mist Warp Area)"
    NORTHERN_RYOSHIMA_COAST_WATCHERS_ENCOUNTER = "Northern Ryoshima Coast (Watcher's cape mandatory Encounter)"
    NORTHERN_RYOSHIMA_COAST_WATCHERS = "Northern Ryoshima Coast (Watcher's cape)"
    NORTHERN_RYOSHIMA_COAST_SAPLING = "Northern Ryoshima Coast (Guardian Sapling Island)"
    NORTHERN_RYOSHIMA_COAST_TOMB = "Northern Ryoshima Coast (Tomb Cave)"
    NORTHERN_RYOSHIMA_COAST_WESTERN_ISLAND = "Northern Ryoshima Coast (Westernmost Island)"
    NORTHERN_RYOSHIMA_COAST_UMI = "Northern Ryoshima Coast (Umi's Restaurant)"
    NORTHERN_RYOSHIMA_COAST_CATCALL_NORTH = "Northern Ryoshima Coast (Island North of Catcall Tower)"
    NORTHERN_RYOSHIMA_COAST_CB2_ISLAND = "Northern Ryoshima Coast (Cherry Bomb 2 Island)"
    NORTHERN_RYOSHIMA_COAST_PS2_ISLAND = "Northern Ryoshima Coast (Power Slash 2 Island)"
    NORTHERN_RYOSHIMA_COAST_BANDIT_SPIDER_ISLAND = "Northern Ryoshima Coast (Bandit Spider Island)"
    NORTHERN_RYOSHIMA_COAST_SEA = "Northern Ryoshima Coast (Sea)"
    NORTHERN_RYOSHIMA_COAST_PS2_CAVE = "Northern Ryoshima Coast (Power Slash 2 Cave)"
    NORTHERN_RYOSHIMA_COAST_CB2_CAVE = "Northern Ryoshima Coast (Cherry Bomb 2 Cave)"
    NORTHERN_RYOSHIMA_COAST_BANDIT_SPIDER_CAVE = "Northern Ryoshima Coast (Bandit spider cave)"
    NORTHERN_RYOSHIMA_COAST_TREASURE_CAVE = "Northern Ryoshima Coast (Treasure cave)"
    NORTHERN_RYOSHIMA_COAST_CATCALL_ISLAND = "Northern Ryoshima Coast (Catcall Tower Island)"

    ## Catcall Tower
    CATCALL_TOWER_BOTTOM = "Catcall Tower (Bottom)"
    CATCALL_TOWER = "Catcall Tower"
    CATCALL_TOWER_TOP = "Catcall Tower(Top)"

    ## DRAGON PALACE
    DRAGON_PALACE = "Dragon Palace"
    DRAGON_PALACE_SPRING = "Dragon Palace (Soothing Spring)"
    DRAGON_PALACE_CAVE = "Dragon Palace (Treasure Cave)"
    DRAGON_PALACE_GARDEN = "Dragon Palace (Water Dragon's Garden)"

    ## INSIDE THE DRAGON
    INSIDE_THE_DRAGON = "Inside the dragon"
    INSIDE_THE_DRAGON_DEEP = "Inside the dragon (Deeper part)"
    INSIDE_THE_DRAGON_ORB = "Inside the dragon (Orb area)"

    ## ONI ISLAND
    ONI_ISLAND_ENTRANCE = "Oni Island (Entrance)"
    ONI_ISLAND_ENTRANCE_BRIDGE = "Oni Island (Entrance Bridge)"
    ONI_ISLAND_ENTRANCE_SEA_OF_FIRE = "Oni Island (Sea of Fire)"
    ONI_ISLAND_ENTRANCE_UPPER = "Oni Island (Sea of Fire Upper Part)"

    # SPECIAL REGIONS
    # Special Hub regions to handle warps
    MIST_WARP_HUB = "Mist Warp Hub"
    MERMAID_SPRING_HUB = "Mermaid Spring Warp Hub"



# Reference https://github.com/Axertin/okami-apclient/blob/master/include/okami/maps.hpp
class MapIds(Enum):
    CURSED_KAMIKI = 0x100
    CAVE_OF_NAGI = 0x101
    KAMIKI_VILLAGE = 0x102
    HANA_VALLEY = 0x103
    TSUTA_RUINS = 0x104
    CITY_CHECKPOINT = 0x105
    GALE_SHRINE = 0x107
    KUSA_VILLAGE = 0x108
    SASA_SANCTUARY = 0x109
    AGATA_FOREST_MME_FAWN = 0x10A
    CALCIFIED_CAVERN = 0x10E
    MOON_CAVE = 0x110
    RYOSHIMA_BANDIT_SPIDER = 0x113
    TAKA_PASS_CAVE = 0x114
    POWER_SLASH_2_CAVE = 0x116
    CHERRY_BOMB_2_CAVE = 0x117
    NORTHERN_RYOSHIMA_BANDIT_SPIDER = 0x11A
    DRAGON_PALACE_TREASURE = 0x11C
    NORTHERN_RYOSHIMA_TREASURE = 0x11D
    RIVER_OF_THE_HEAVENS = 0x122
    SEIAN_ARISTORATIC = 0x200
    SEIAN_COMMONERS = 0x201
    HIMIKO_PALACE = 0x202
    DRAGON_PALACE = 0x203
    INSIDE_THE_DRAGON = 0x204
    SUNKEN_SHIP = 0x205
    IMPERIAL_PALACE = 0x206
    IMPERIAL_PALACE_SMALL = 0x207
    CATCALL_TOWER = 0x20A
    ONI_ISLAND_EXT= 0x20D
    CURSED_SHINSHU = 0xF01
    HEALED_SHINSHU = 0xF02
    CURSED_AGATA = 0xF03
    HEALED_AGATA = 0xF04
    CURSED_TAKA = 0xF07
    HEALED_TAKA = 0xF08
    CURSED_RYOSHIMA = 0xF09
    HEALED_RYOSHIMA = 0xF0A
    NORTHERN_RYOSHIMA = 0xF0C


class MapIndexes(Enum):
    CURSED_KAMIKI = 1
    CAVE_OF_NAGI = 2
    KAMIKI_VILLAGE = 3
    HANA_VALLEY = 4
    TSUTA_RUINS = 5
    CITY_CHECKPOINT = 6
    GALE_SHRINE = 8
    KUSA_VILLAGE = 9
    SASA_SANCTUARY = 10
    AGATA_FOREST_MME_FAWN = 11
    CALCIFIED_CAVERN = 15
    MOON_CAVE = 16
    RIVER_OF_THE_HEAVENS = 30
    SEIAN_CITY_COMMONERS = 32
    SHINSHU_FIELD = 71
    AGATA_FOREST = 72
    TAKA_PASS = 74
    RYOSHIMA_COAST = 75
