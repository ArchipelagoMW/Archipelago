from typing import Set, List, FrozenSet

from worlds.stardew_valley.game_item import MuseumItem

none = set({})
stardew = {"Stardew Valley"}
farm = {"Farm"}
town = {"Town"}
beach = {"Beach"}
mountain = {"Mountain"}
forest = {"Forest"}
bus = {"Bus Stop"}
backwoods = {"Backwoods"}
railroad = {"Railroad"}
secret_woods = {"Secret Woods"}
desert = {"The Desert"}
mines_20 = {"The Mines - Floor 20"}
mines_60 = {"The Mines - Floor 60"}
mines_100 = {"The Mines - Floor 100"}
skull_cavern = {"Skull Cavern"}
sewers = {"Sewers"}
mutant_bug_lair = {"Mutant Bug Lair"}
witch_swamp = {"Witch's Swamp"}
ginger_island = {"Ginger Island"}
perfect_skull_cavern = {"Skull Cavern Floor 100"}
bone_node = {*ginger_island}
mines_any = {*mines_20, *mines_60, *mines_100}
forest_mountain = {*forest, *mountain}
bus_forest_town = {*bus, *forest, *town}
mountain_forest_bus = {*forest_mountain, *bus}
mountain_forest_town = {*forest_mountain, *town}
beach_forest_town = {*beach, *forest, *town}
mountain_skull_cavern = {*mountain, *skull_cavern}
bone_farm = {*bone_node, *farm}
bone_bus = {*bone_node, *bus}
bone_mountain = {*bone_node, *mountain}
bone_forest = {*bone_node, *forest}
bone_beach = {*bone_node, *beach}
bone_mines = {*bone_node, *mines_20}
bone_farm_town = {*bone_farm, *town}
bone_forest_town = {*bone_forest, *town}
bone_forest_mountain = {*bone_forest, *mountain}
bone_forest_railroad = {*bone_forest, *railroad}
bone_backwoods_beach = {*bone_node, *backwoods, *beach}
bone_beach_forest_mountain = {*bone_forest, *mountain, *beach}
bone_desert_forest_beach = {*bone_forest, *desert, *beach}

geode = {"Geode"}
frozen = {"Frozen Geode"}
magma = {"Magma Geode"}
omni = {"Omni Geode"}
trove = {"Artifact Trove"}
fishing = {"Fishing Chest"}
secret_note = {"Secret Note"}
geode_omni = {*geode, *omni}
frozen_omni = {*frozen, *omni}
magma_omni = {*magma, *omni}
omni_trove = {*omni, *trove}
trove_fishing = {*trove, *fishing}
geode_omni_trove = {*geode_omni, *trove}
frozen_omni_trove = {*frozen_omni, *trove}
magma_omni_trove = {*magma_omni, *trove}
geode_omni_fishing = {*geode_omni, *fishing}
frozen_omni_fishing = {*frozen_omni, *fishing}
magma_omni_fishing = {*magma_omni, *fishing}

unlikely = set({})
duggy = {"Duggy"}
blue_slime = {"Blue Slime"}
pepper_rex = {"Pepper Rex"}
stone_golem = {"Stone Golem"}
frozen_monsters = {*blue_slime}

all_artifact_items: List[MuseumItem] = []
all_mineral_items: List[MuseumItem] = []
all_museum_items: List[MuseumItem] = []


def artifact(name: str, item_id: int, difficulty: float, locations: Set[str], geodes: Set[str],
             monsters: Set[str] = frozenset()) -> MuseumItem:
    artifact_item = museum_item(name, item_id, difficulty, frozenset(locations), frozenset(geodes), frozenset(monsters))
    all_artifact_items.append(artifact_item)
    return artifact_item


def mineral(name: str, item_id: int, locations: Set[str], geodes: Set[str],
            monsters: Set[str] = frozenset(), difficulty: float = -1) -> MuseumItem:

    if difficulty == -1:
        difficulty = 0
        if "Geode" in geodes:
            difficulty += 1.0 / 32.0
        if "Frozen Geode" in geodes:
            difficulty += 1.0 / 30.0
        if "Magma Geode" in geodes:
            difficulty += 1.0 / 26.0
        if "Omni Geode" in geodes:
            difficulty += 31.0 / 2750.0

    mineral_item = museum_item(name, item_id, difficulty, frozenset(locations), frozenset(geodes), frozenset(monsters))
    all_mineral_items.append(mineral_item)
    return mineral_item


def museum_item(name: str, item_id: int, difficulty: float, locations: FrozenSet[str], geodes: FrozenSet[str],
                monsters: FrozenSet[str]) -> MuseumItem:
    item = MuseumItem(name, item_id, frozenset(locations), frozenset(geodes), frozenset(monsters), difficulty)
    all_museum_items.append(item)
    return item


dwarf_scroll_i = artifact("Dwarf Scroll I", 96, 5.6, mines_20, none, unlikely)
dwarf_scroll_ii = artifact("Dwarf Scroll II", 97, 3, mines_20, none, unlikely)
dwarf_scroll_iii = artifact("Dwarf Scroll III", 98, 7.5, mines_60, none, blue_slime)
dwarf_scroll_iv = artifact("Dwarf Scroll IV", 99, 4, mines_100, none)
chipped_amphora = artifact("Chipped Amphora", 100, 6.7, town, trove)
arrowhead = artifact("Arrowhead", 101, 8.5, mountain_forest_bus, trove)
ancient_doll = artifact("Ancient Doll", 103, 13.1, mountain_forest_bus, trove_fishing)
elvish_jewelry = artifact("Elvish Jewelry", 104, 5.3, forest, trove_fishing)
chewing_stick = artifact("Chewing Stick", 105, 10.3, mountain_forest_town, trove_fishing)
ornamental_fan = artifact("Ornamental Fan", 106, 7.4, beach_forest_town, trove_fishing)
dinosaur_egg = artifact("Dinosaur Egg", 107, 11.4, mountain_skull_cavern, fishing, pepper_rex)
rare_disc = artifact("Rare Disc", 108, 5.6, stardew, trove_fishing, unlikely)
ancient_sword = artifact("Ancient Sword", 109, 5.8, forest_mountain, trove_fishing)
rusty_spoon = artifact("Rusty Spoon", 110, 9.6, town, trove_fishing)
rusty_spur = artifact("Rusty Spur", 111, 15.6, farm, trove_fishing)
rusty_cog = artifact("Rusty Cog", 112, 9.6, mountain, trove_fishing)
chicken_statue = artifact("Chicken Statue", 113, 13.5, farm, trove_fishing)
ancient_seed = artifact("Ancient Seed", 114, 8.4, forest_mountain, trove_fishing, unlikely)
prehistoric_tool = artifact("Prehistoric Tool", 115, 11.1, mountain_forest_bus, trove_fishing)
dried_starfish = artifact("Dried Starfish", 116, 12.5, beach, trove_fishing)
anchor = artifact("Anchor", 117, 8.5, beach, trove_fishing)
glass_shards = artifact("Glass Shards", 118, 11.5, beach, trove_fishing)
bone_flute = artifact("Bone Flute", 119, 6.3, mountain_forest_town, trove_fishing)
prehistoric_handaxe = artifact("Prehistoric Handaxe", 120, 13.7, mountain_forest_bus, trove)
dwarvish_helm = artifact("Dwarvish Helm", 121, 8.7, mines_20, geode_omni_trove)
dwarf_gadget = artifact("Dwarf Gadget", 122, 9.7, mines_60, magma_omni_trove)
ancient_drum = artifact("Ancient Drum", 123, 9.5, bus_forest_town, frozen_omni_trove)
golden_mask = artifact("Golden Mask", 124, 6.7, desert, trove)
golden_relic = artifact("Golden Relic", 125, 9.7, desert, trove)
strange_doll_green = artifact("Strange Doll (Green)", 126, 10, town, secret_note)
strange_doll = artifact("Strange Doll", 127, 10, desert, secret_note)
prehistoric_scapula = artifact("Prehistoric Scapula", 579, 6.2, bone_forest_town, none)
prehistoric_tibia = artifact("Prehistoric Tibia", 580, 16.6, bone_forest_railroad, none)
prehistoric_skull = artifact("Prehistoric Skull", 581, 3.9, bone_mountain, none)
skeletal_hand = artifact("Skeletal Hand", 582, 7.9, bone_backwoods_beach, none)
prehistoric_rib = artifact("Prehistoric Rib", 583, 15, bone_farm_town, none, pepper_rex)
prehistoric_vertebra = artifact("Prehistoric Vertebra", 584, 12.7, bone_bus, none, pepper_rex)
skeletal_tail = artifact("Skeletal Tail", 585, 5.1, bone_mines, fishing)
nautilus_fossil = artifact("Nautilus Fossil", 586, 6.9, bone_beach, fishing)
amphibian_fossil = artifact("Amphibian Fossil", 587, 6.3, bone_forest_mountain, fishing)
palm_fossil = artifact("Palm Fossil", 588, 10.2, bone_desert_forest_beach, none)
trilobite = artifact("Trilobite", 589, 7.4, bone_beach_forest_mountain, none)

quartz = mineral("Quartz", 80, mines_20, none, stone_golem)
fire_quartz = mineral("Fire Quartz", 82, mines_100, magma_omni_fishing, none, 1.0/12.0)
frozen_tear = mineral("Frozen Tear", 84, mines_60, frozen_omni_fishing, unlikely, 1.0/12.0)
earth_crystal = mineral("Earth Crystal", 86, mines_20, geode_omni_fishing, duggy, 1.0/12.0)
emerald = mineral("Emerald", 60, mines_100, fishing)
aquamarine = mineral("Aquamarine", 62, mines_60, fishing)
ruby = mineral("Ruby", 64, mines_100, fishing)
amethyst = mineral("Amethyst", 66, mines_20, fishing)
topaz = mineral("Topaz", 68, mines_20, fishing)
jade = mineral("Jade", 70, mines_60, fishing)
diamond = mineral("Diamond", 72, mines_60, fishing)
prismatic_shard = mineral("Prismatic Shard", 74, perfect_skull_cavern, unlikely, unlikely)
alamite = mineral("Alamite", 538, town, geode_omni)
bixite = mineral("Bixite", 539, town, magma_omni, unlikely)
baryte = mineral("Baryte", 540, town, magma_omni)
aerinite = mineral("Aerinite", 541, town, frozen_omni)
calcite = mineral("Calcite", 542, town, geode_omni)
dolomite = mineral("Dolomite", 543, town, magma_omni)
esperite = mineral("Esperite", 544, town, frozen_omni)
fluorapatite = mineral("Fluorapatite", 545, town, frozen_omni)
geminite = mineral("Geminite", 546, town, frozen_omni)
helvite = mineral("Helvite", 547, town, magma_omni)
jamborite = mineral("Jamborite", 548, town, geode_omni)
jagoite = mineral("Jagoite", 549, town, geode_omni)
kyanite = mineral("Kyanite", 550, town, frozen_omni)
lunarite = mineral("Lunarite", 551, town, frozen_omni)
malachite = mineral("Malachite", 552, town, geode_omni)
neptunite = mineral("Neptunite", 553, town, magma_omni)
lemon_stone = mineral("Lemon Stone", 554, town, magma_omni)
nekoite = mineral("Nekoite", 555, town, geode_omni)
orpiment = mineral("Orpiment", 556, town, geode_omni)
petrified_slime = mineral("Petrified Slime", 557, town, geode_omni)
thunder_egg = mineral("Thunder Egg", 558, town, geode_omni)
pyrite = mineral("Pyrite", 559, town, frozen_omni)
ocean_stone = mineral("Ocean Stone", 560, town, frozen_omni)
ghost_crystal = mineral("Ghost Crystal", 561, town, frozen_omni)
tigerseye = mineral("Tigerseye", 562, town, magma_omni)
jasper = mineral("Jasper", 563, town, magma_omni)
opal = mineral("Opal", 564, town, frozen_omni)
fire_opal = mineral("Fire Opal", 565, town, magma_omni)
celestine = mineral("Celestine", 566, town, geode_omni)
marble = mineral("Marble", 567, town, frozen_omni)
sandstone = mineral("Sandstone", 568, town, geode_omni)
granite = mineral("Granite", 569, town, geode_omni)
basalt = mineral("Basalt", 570, town, magma_omni)
limestone = mineral("Limestone", 571, town, geode_omni)
soapstone = mineral("Soapstone", 572, town, frozen_omni)
hematite = mineral("Hematite", 573, town, frozen_omni)
mudstone = mineral("Mudstone", 574, town, geode_omni)
obsidian = mineral("Obsidian", 575, town, magma_omni)
slate = mineral("Slate", 576, town, geode_omni)
fairy_stone = mineral("Fairy Stone", 577, town, frozen_omni)
star_shards = mineral("Star Shards", 578, town, magma_omni)

dwarf_scrolls = {dwarf_scroll_i, dwarf_scroll_ii, dwarf_scroll_iii, dwarf_scroll_iv}
skeleton_front = {prehistoric_skull, skeletal_hand, prehistoric_scapula}
skeleton_middle = {prehistoric_rib, prehistoric_vertebra}
skeleton_back = {prehistoric_tibia, skeletal_tail}

all_museum_items_by_name = {item.name: item for item in all_museum_items}
all_museum_items_by_id = {item.item_id: item for item in all_museum_items}
