from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Union, Optional

from . import common_data as common
from .game_item import GameItem
from .monster_data import Monster
from .region_data import SVRegion


@dataclass(frozen=True)
class MuseumItem(GameItem):
    locations: Tuple[str, ...]
    geodes: Tuple[str, ...]
    monsters: Tuple[str, ...]
    difficulty: float

    @staticmethod
    def of(name: str,
           item_id: int,
           difficulty: float,
           locations: Union[str, Tuple[str, ...]],
           geodes: Union[str, Tuple[str, ...]],
           monsters: Union[str, Tuple[str, ...]]) -> MuseumItem:
        if isinstance(locations, str):
            locations = (locations,)

        if isinstance(geodes, str):
            geodes = (geodes,)

        if isinstance(monsters, str):
            monsters = (monsters,)

        return MuseumItem(name, item_id, locations, geodes, monsters, difficulty)

    def __repr__(self):
        return f"{self.name} [{self.item_id}] (Locations: {self.locations} |" \
               f" Geodes: {self.geodes} |" \
               f" Monsters: {self.monsters}) "


class Geode:
    geode = "Geode"
    frozen_geode = "Frozen Geode"
    magma_geode = "Magma Geode"
    omni_geode = "Omni Geode"
    artifact_trove = "Artifact Trove"


unlikely = ()

all_artifact_items: List[MuseumItem] = []
all_mineral_items: List[MuseumItem] = []

all_museum_items: List[MuseumItem] = []


def create_artifact(name: str,
                    item_id: int,
                    difficulty: float,
                    locations: Union[str, Tuple[str, ...]] = (),
                    geodes: Union[str, Tuple[str, ...]] = (),
                    monsters: Union[str, Tuple[str, ...]] = ()) -> MuseumItem:
    artifact_item = MuseumItem.of(name, item_id, difficulty, locations, geodes, monsters)
    all_artifact_items.append(artifact_item)
    all_museum_items.append(artifact_item)
    return artifact_item


def create_mineral(name: str,
                   item_id: int,
                   locations: Union[str, Tuple[str, ...]],
                   geodes: Union[str, Tuple[str, ...]] = (),
                   monsters: Union[str, Tuple[str, ...]] = (),
                   difficulty: Optional[float] = None) -> MuseumItem:
    if difficulty is None:
        difficulty = 0
        if "Geode" in geodes:
            difficulty += 1.0 / 32.0 * 100
        if "Frozen Geode" in geodes:
            difficulty += 1.0 / 30.0 * 100
        if "Magma Geode" in geodes:
            difficulty += 1.0 / 26.0 * 100
        if "Omni Geode" in geodes:
            difficulty += 31.0 / 2750.0 * 100

    mineral_item = MuseumItem.of(name, item_id, difficulty, locations, geodes, monsters)
    all_mineral_items.append(mineral_item)
    all_museum_items.append(mineral_item)
    return mineral_item


class Artifact:
    dwarf_scroll_i = create_artifact("Dwarf Scroll I", 96, 5.6, SVRegion.mines_floor_20,
                                     monsters=unlikely)
    dwarf_scroll_ii = create_artifact("Dwarf Scroll II", 97, 3, SVRegion.mines_floor_20,
                                      monsters=unlikely)
    dwarf_scroll_iii = create_artifact("Dwarf Scroll III", 98, 7.5, SVRegion.mines_floor_60,
                                       monsters=Monster.blue_slime)
    dwarf_scroll_iv = create_artifact("Dwarf Scroll IV", 99, 4, SVRegion.mines_floor_100)
    chipped_amphora = create_artifact("Chipped Amphora", 100, 6.7, SVRegion.town,
                                      geodes=Geode.artifact_trove)
    arrowhead = create_artifact("Arrowhead", 101, 8.5, (SVRegion.mountain, SVRegion.forest, SVRegion.bus_stop),
                                geodes=Geode.artifact_trove)
    ancient_doll = create_artifact("Ancient Doll", 103, 13.1, (SVRegion.mountain, SVRegion.forest, SVRegion.bus_stop),
                                   geodes=(Geode.artifact_trove, common.fishing_chest))
    elvish_jewelry = create_artifact("Elvish Jewelry", 104, 5.3, SVRegion.forest,
                                     geodes=(Geode.artifact_trove, common.fishing_chest))
    chewing_stick = create_artifact("Chewing Stick", 105, 10.3, (SVRegion.mountain, SVRegion.forest, SVRegion.town),
                                    geodes=(Geode.artifact_trove, common.fishing_chest))
    ornamental_fan = create_artifact("Ornamental Fan", 106, 7.4, (SVRegion.beach, SVRegion.forest, SVRegion.town),
                                     geodes=(Geode.artifact_trove, common.fishing_chest))
    dinosaur_egg = create_artifact("Dinosaur Egg", 107, 11.4, (SVRegion.mountain, SVRegion.skull_cavern),
                                   geodes=common.fishing_chest,
                                   monsters=Monster.pepper_rex)
    rare_disc = create_artifact("Rare Disc", 108, 5.6, SVRegion.stardew_valley,
                                geodes=(Geode.artifact_trove, common.fishing_chest),
                                monsters=unlikely)
    ancient_sword = create_artifact("Ancient Sword", 109, 5.8, (SVRegion.forest, SVRegion.mountain),
                                    geodes=(Geode.artifact_trove, common.fishing_chest))
    rusty_spoon = create_artifact("Rusty Spoon", 110, 9.6, SVRegion.town,
                                  geodes=(Geode.artifact_trove, common.fishing_chest))
    rusty_spur = create_artifact("Rusty Spur", 111, 15.6, SVRegion.farm,
                                 geodes=(Geode.artifact_trove, common.fishing_chest))
    rusty_cog = create_artifact("Rusty Cog", 112, 9.6, SVRegion.mountain,
                                geodes=(Geode.artifact_trove, common.fishing_chest))
    chicken_statue = create_artifact("Chicken Statue", 113, 13.5, SVRegion.farm,
                                     geodes=(Geode.artifact_trove, common.fishing_chest))
    ancient_seed = create_artifact("Ancient Seed", 114, 8.4, (SVRegion.forest, SVRegion.mountain),
                                   geodes=(Geode.artifact_trove, common.fishing_chest),
                                   monsters=unlikely)
    prehistoric_tool = create_artifact("Prehistoric Tool", 115, 11.1, (SVRegion.mountain, SVRegion.forest, SVRegion.bus_stop),
                                       geodes=(Geode.artifact_trove, common.fishing_chest))
    dried_starfish = create_artifact("Dried Starfish", 116, 12.5, SVRegion.beach,
                                     geodes=(Geode.artifact_trove, common.fishing_chest))
    anchor = create_artifact("Anchor", 117, 8.5, SVRegion.beach, geodes=(Geode.artifact_trove, common.fishing_chest))
    glass_shards = create_artifact("Glass Shards", 118, 11.5, SVRegion.beach,
                                   geodes=(Geode.artifact_trove, common.fishing_chest))
    bone_flute = create_artifact("Bone Flute", 119, 6.3, (SVRegion.mountain, SVRegion.forest, SVRegion.town),
                                 geodes=(Geode.artifact_trove, common.fishing_chest))
    prehistoric_handaxe = create_artifact("Prehistoric Handaxe", 120, 13.7,
                                          (SVRegion.mountain, SVRegion.forest, SVRegion.bus_stop),
                                          geodes=Geode.artifact_trove)
    dwarvish_helm = create_artifact("Dwarvish Helm", 121, 8.7, SVRegion.mines_floor_20,
                                    geodes=(Geode.geode, Geode.omni_geode, Geode.artifact_trove))
    dwarf_gadget = create_artifact("Dwarf Gadget", 122, 9.7, SVRegion.mines_floor_60,
                                   geodes=(Geode.magma_geode, Geode.omni_geode, Geode.artifact_trove))
    ancient_drum = create_artifact("Ancient Drum", 123, 9.5, (SVRegion.bus_stop, SVRegion.forest, SVRegion.town),
                                   geodes=(Geode.frozen_geode, Geode.omni_geode, Geode.artifact_trove))
    golden_mask = create_artifact("Golden Mask", 124, 6.7, SVRegion.desert,
                                  geodes=Geode.artifact_trove)
    golden_relic = create_artifact("Golden Relic", 125, 9.7, SVRegion.desert,
                                   geodes=Geode.artifact_trove)
    strange_doll_green = create_artifact("Strange Doll (Green)", 126, 10, SVRegion.town,
                                         geodes=common.secret_note)
    strange_doll = create_artifact("Strange Doll", 127, 10, SVRegion.desert,
                                   geodes=common.secret_note)
    prehistoric_scapula = create_artifact("Prehistoric Scapula", 579, 6.2,
                                          (SVRegion.dig_site, SVRegion.forest, SVRegion.town))
    prehistoric_tibia = create_artifact("Prehistoric Tibia", 580, 16.6,
                                        (SVRegion.dig_site, SVRegion.forest, SVRegion.railroad))
    prehistoric_skull = create_artifact("Prehistoric Skull", 581, 3.9, (SVRegion.dig_site, SVRegion.mountain))
    skeletal_hand = create_artifact("Skeletal Hand", 582, 7.9, (SVRegion.dig_site, SVRegion.backwoods, SVRegion.beach))
    prehistoric_rib = create_artifact("Prehistoric Rib", 583, 15, (SVRegion.dig_site, SVRegion.farm, SVRegion.town),
                                      monsters=Monster.pepper_rex)
    prehistoric_vertebra = create_artifact("Prehistoric Vertebra", 584, 12.7, (SVRegion.dig_site, SVRegion.bus_stop),
                                           monsters=Monster.pepper_rex)
    skeletal_tail = create_artifact("Skeletal Tail", 585, 5.1, (SVRegion.dig_site, SVRegion.mines_floor_20),
                                    geodes=common.fishing_chest)
    nautilus_fossil = create_artifact("Nautilus Fossil", 586, 6.9, (SVRegion.dig_site, SVRegion.beach),
                                      geodes=common.fishing_chest)
    amphibian_fossil = create_artifact("Amphibian Fossil", 587, 6.3, (SVRegion.dig_site, SVRegion.forest, SVRegion.mountain),
                                       geodes=common.fishing_chest)
    palm_fossil = create_artifact("Palm Fossil", 588, 10.2,
                                  (SVRegion.dig_site, SVRegion.desert, SVRegion.forest, SVRegion.beach))
    trilobite = create_artifact("Trilobite", 589, 7.4, (SVRegion.dig_site, SVRegion.desert, SVRegion.forest, SVRegion.beach))


class Mineral:
    quartz = create_mineral("Quartz", 80, SVRegion.mines_floor_20,
                            monsters=Monster.stone_golem)
    fire_quartz = create_mineral("Fire Quartz", 82, SVRegion.mines_floor_100,
                                 geodes=(Geode.magma_geode, Geode.omni_geode, common.fishing_chest),
                                 difficulty=1.0 / 12.0)
    frozen_tear = create_mineral("Frozen Tear", 84, SVRegion.mines_floor_60,
                                 geodes=(Geode.frozen_geode, Geode.omni_geode, common.fishing_chest),
                                 monsters=unlikely,
                                 difficulty=1.0 / 12.0)
    earth_crystal = create_mineral("Earth Crystal", 86, SVRegion.mines_floor_20,
                                   geodes=(Geode.geode, Geode.omni_geode, common.fishing_chest),
                                   monsters=Monster.duggy,
                                   difficulty=1.0 / 12.0)
    emerald = create_mineral("Emerald", 60, SVRegion.mines_floor_100,
                             geodes=common.fishing_chest)
    aquamarine = create_mineral("Aquamarine", 62, SVRegion.mines_floor_60,
                                geodes=common.fishing_chest)
    ruby = create_mineral("Ruby", 64, SVRegion.mines_floor_100,
                          geodes=common.fishing_chest)
    amethyst = create_mineral("Amethyst", 66, SVRegion.mines_floor_20,
                              geodes=common.fishing_chest)
    topaz = create_mineral("Topaz", 68, SVRegion.mines_floor_20,
                           geodes=common.fishing_chest)
    jade = create_mineral("Jade", 70, SVRegion.mines_floor_60,
                          geodes=common.fishing_chest)
    diamond = create_mineral("Diamond", 72, SVRegion.mines_floor_60,
                             geodes=common.fishing_chest)
    prismatic_shard = create_mineral("Prismatic Shard", 74, SVRegion.perfect_skull_cavern,
                                     geodes=unlikely,
                                     monsters=unlikely)
    alamite = create_mineral("Alamite", 538, SVRegion.town,
                             geodes=(Geode.geode, Geode.omni_geode))
    bixite = create_mineral("Bixite", 539, SVRegion.town,
                            geodes=(Geode.magma_geode, Geode.omni_geode),
                            monsters=unlikely)
    baryte = create_mineral("Baryte", 540, SVRegion.town,
                            geodes=(Geode.magma_geode, Geode.omni_geode))
    aerinite = create_mineral("Aerinite", 541, SVRegion.town,
                              geodes=(Geode.frozen_geode, Geode.omni_geode))
    calcite = create_mineral("Calcite", 542, SVRegion.town,
                             geodes=(Geode.geode, Geode.omni_geode))
    dolomite = create_mineral("Dolomite", 543, SVRegion.town,
                              geodes=(Geode.magma_geode, Geode.omni_geode))
    esperite = create_mineral("Esperite", 544, SVRegion.town,
                              geodes=(Geode.frozen_geode, Geode.omni_geode))
    fluorapatite = create_mineral("Fluorapatite", 545, SVRegion.town,
                                  geodes=(Geode.frozen_geode, Geode.omni_geode))
    geminite = create_mineral("Geminite", 546, SVRegion.town,
                              geodes=(Geode.frozen_geode, Geode.omni_geode))
    helvite = create_mineral("Helvite", 547, SVRegion.town,
                             geodes=(Geode.magma_geode, Geode.omni_geode))
    jamborite = create_mineral("Jamborite", 548, SVRegion.town,
                               geodes=(Geode.geode, Geode.omni_geode))
    jagoite = create_mineral("Jagoite", 549, SVRegion.town,
                             geodes=(Geode.geode, Geode.omni_geode))
    kyanite = create_mineral("Kyanite", 550, SVRegion.town,
                             geodes=(Geode.frozen_geode, Geode.omni_geode))
    lunarite = create_mineral("Lunarite", 551, SVRegion.town,
                              geodes=(Geode.frozen_geode, Geode.omni_geode))
    malachite = create_mineral("Malachite", 552, SVRegion.town,
                               geodes=(Geode.geode, Geode.omni_geode))
    neptunite = create_mineral("Neptunite", 553, SVRegion.town,
                               geodes=(Geode.magma_geode, Geode.omni_geode))
    lemon_stone = create_mineral("Lemon Stone", 554, SVRegion.town,
                                 geodes=(Geode.magma_geode, Geode.omni_geode))
    nekoite = create_mineral("Nekoite", 555, SVRegion.town,
                             geodes=(Geode.geode, Geode.omni_geode))
    orpiment = create_mineral("Orpiment", 556, SVRegion.town,
                              geodes=(Geode.geode, Geode.omni_geode))
    petrified_slime = create_mineral("Petrified Slime", 557, SVRegion.town,
                                     geodes=(Geode.geode, Geode.omni_geode))
    thunder_egg = create_mineral("Thunder Egg", 558, SVRegion.town,
                                 geodes=(Geode.geode, Geode.omni_geode))
    pyrite = create_mineral("Pyrite", 559, SVRegion.town,
                            geodes=(Geode.frozen_geode, Geode.omni_geode))
    ocean_stone = create_mineral("Ocean Stone", 560, SVRegion.town,
                                 geodes=(Geode.frozen_geode, Geode.omni_geode))
    ghost_crystal = create_mineral("Ghost Crystal", 561, SVRegion.town,
                                   geodes=(Geode.frozen_geode, Geode.omni_geode))
    tigerseye = create_mineral("Tigerseye", 562, SVRegion.town,
                               geodes=(Geode.magma_geode, Geode.omni_geode))
    jasper = create_mineral("Jasper", 563, SVRegion.town,
                            geodes=(Geode.magma_geode, Geode.omni_geode))
    opal = create_mineral("Opal", 564, SVRegion.town,
                          geodes=(Geode.frozen_geode, Geode.omni_geode))
    fire_opal = create_mineral("Fire Opal", 565, SVRegion.town,
                               geodes=(Geode.magma_geode, Geode.omni_geode))
    celestine = create_mineral("Celestine", 566, SVRegion.town,
                               geodes=(Geode.geode, Geode.omni_geode))
    marble = create_mineral("Marble", 567, SVRegion.town,
                            geodes=(Geode.frozen_geode, Geode.omni_geode))
    sandstone = create_mineral("Sandstone", 568, SVRegion.town,
                               geodes=(Geode.geode, Geode.omni_geode))
    granite = create_mineral("Granite", 569, SVRegion.town,
                             geodes=(Geode.geode, Geode.omni_geode))
    basalt = create_mineral("Basalt", 570, SVRegion.town,
                            geodes=(Geode.magma_geode, Geode.omni_geode))
    limestone = create_mineral("Limestone", 571, SVRegion.town,
                               geodes=(Geode.geode, Geode.omni_geode))
    soapstone = create_mineral("Soapstone", 572, SVRegion.town,
                               geodes=(Geode.frozen_geode, Geode.omni_geode))
    hematite = create_mineral("Hematite", 573, SVRegion.town,
                              geodes=(Geode.frozen_geode, Geode.omni_geode))
    mudstone = create_mineral("Mudstone", 574, SVRegion.town,
                              geodes=(Geode.geode, Geode.omni_geode))
    obsidian = create_mineral("Obsidian", 575, SVRegion.town,
                              geodes=(Geode.magma_geode, Geode.omni_geode))
    slate = create_mineral("Slate", 576, SVRegion.town,
                           geodes=(Geode.geode, Geode.omni_geode))
    fairy_stone = create_mineral("Fairy Stone", 577, SVRegion.town,
                                 geodes=(Geode.frozen_geode, Geode.omni_geode))
    star_shards = create_mineral("Star Shards", 578, SVRegion.town,
                                 geodes=(Geode.magma_geode, Geode.omni_geode))


dwarf_scrolls = (Artifact.dwarf_scroll_i, Artifact.dwarf_scroll_ii, Artifact.dwarf_scroll_iii, Artifact.dwarf_scroll_iv)
skeleton_front = (Artifact.prehistoric_skull, Artifact.skeletal_hand, Artifact.prehistoric_scapula)
skeleton_middle = (Artifact.prehistoric_rib, Artifact.prehistoric_vertebra)
skeleton_back = (Artifact.prehistoric_tibia, Artifact.skeletal_tail)

all_museum_items_by_name = {item.name: item for item in all_museum_items}
