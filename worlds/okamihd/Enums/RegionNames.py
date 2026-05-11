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
    SHINSHU_FIELD = "Shinshu Field"
    SHINSHU_FIELD_AGATA_CAVE = "Shinshu Field (Cave to Agata Forest)"
    TAMA_HOUSE = "Tama's house"
    SHINSHU_PLATEAU="Shinshu Field Plateau"

    ## HANA VALLEY
    CURSED_HANA_VALLEY = "Cursed Hana Valley"
    HANA_VALLEY = "Hana Valley"
    HANA_VALLEY_SAKIGAMI = " Hana Valley - Sakigami sequence"

    ## AGATA FOREST
    CURSED_AGATA_FOREST = "Cursed Agata Forest"
    AGATA_FOREST_WAKA = "Agata Forest (Pre-waka fight)"
    AGATA_FOREST = "Agata Forest"
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
    CURSED_TAKA_PASS_WAKA = "Cursed Taka Pass (Waka Fight)"
    CURSED_TAKA_PASS_CAVE = "Cursed Taka Pass (Cave)"
    CURSED_TAKA_PASS_GUARDIAN_SAPLING = "Cursed Taka Pass (Guardian Sapling)"
    TAKA_PASS = "Taka Pass"

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
    MOON_CAVE_2F = "Moon Cave (2F Main room)"
    MOON_CAVE_B1F_LAKE = "Moon Cave (B1F Underground Lake)"
    MOON_CAVE_B1F_UNDER_LIFT = "Moon Cave (B1F Under Lift)"
    MOON_CAVE_B2F_LIFT = "Moon Cave (B2F Under Lift)"
    MOON_CAVE_B2F_FROZEN_STATUE = "Moon Cave (B2F Frozen Statue Room)"
    MOON_CAVE_B2F_OTHER_LIFT = "Moon Cave (B2F Lift Back)"
    MOON_CAVE_B2F_BOMBABLE = "Moon Cave (B2F Behind Bombable wall)"
    MOON_CAVE_KITCHEN_BACK = "Moon Cave (1F Kitchen Back)"
    MOON_CAVE_2F_FIRE_EYE = "Moon Cave (2F Fire Eye Room)"
    MOON_CAVE_2F_SAND = "Moon Cave (2F Sand room)"
    MOON_CAVE_2F_3F_RAFTERS = "Moon Cave (2F-3F Rafters)"
    MOON_CAVE_4F_RAFTERS = "Moon Cave (4F Rafters)"
    MOON_CAVE_4F_CANON = "Moon Cave (4F Canon)"
    MOON_CAVE_4F_AFTER_CANON = "Moon Cave (4F after canon)"
    MOON_CAVE_OROCHI = "Moon Cave (Orochi)"

# Reference https://github.com/Axertin/okami-apclient/blob/master/include/okami/maps.hpp
class MapIds(Enum):
    CURSED_KAMIKI = 0x100
    CAVE_OF_NAGI = 0x101
    KAMIKI_VILLAGE = 0x102
    HANA_VALLEY = 0x103
    TSUTA_RUINS = 0x104
    GALE_SHRINE = 0x107
    KUSA_VILLAGE = 0x108
    SASA_SANCTUARY = 0x109
    AGATA_FOREST_MME_FAWN = 0x10A
    CALCIFIED_CAVERN=0x10E
    MOON_CAVE = 0x110
    RIVER_OF_THE_HEAVENS = 0x122
    CURSED_SHINSHU = 0xF01
    HEALED_SHINSHU = 0xF02
    CURSED_AGATA = 0xF03
    HEALED_AGATA = 0xF04
    CURSED_TAKA = 0xF07
    HEALED_TAKA = 0xF08


class MapIndexes(Enum):
    CURSED_KAMIKI = 1
    CAVE_OF_NAGI = 2
    KAMIKI_VILLAGE = 3
    HANA_VALLEY = 4
    TSUTA_RUINS = 5
    GALE_SHRINE = 8
    KUSA_VILLAGE = 9
    SASA_SANCTUARY = 10
    AGATA_FOREST_MME_FAWN = 11
    CALCIFIED_CAVERN = 15
    MOON_CAVE = 16
    RIVER_OF_THE_HEAVENS = 30
    SHINSHU_FIELD = 71
    AGATA_FOREST = 72
    TAKA_PASS = 74
