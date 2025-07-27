from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Union, Optional

from ..strings.animal_product_names import AnimalProduct
from ..strings.fish_names import WaterChest
from ..strings.forageable_names import Forageable
from ..strings.geode_names import Geode
from ..strings.metal_names import Mineral, Artifact, Fossil
from ..strings.monster_names import Monster
from ..strings.region_names import Region


@dataclass(frozen=True)
class MuseumItem:
    item_name: str
    locations: Tuple[str, ...]
    geodes: Tuple[str, ...]
    monsters: Tuple[str, ...]
    difficulty: float

    @staticmethod
    def of(item_name: str,
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

        return MuseumItem(item_name, locations, geodes, monsters, difficulty)

    def __repr__(self):
        return f"{self.item_name} (Locations: {self.locations} |" \
               f" Geodes: {self.geodes} |" \
               f" Monsters: {self.monsters}) "


unlikely = ()

all_museum_artifacts: List[MuseumItem] = []
all_museum_minerals: List[MuseumItem] = []

all_museum_items: List[MuseumItem] = []


def create_artifact(name: str,
                    difficulty: float,
                    locations: Union[str, Tuple[str, ...]] = (),
                    geodes: Union[str, Tuple[str, ...]] = (),
                    monsters: Union[str, Tuple[str, ...]] = ()) -> MuseumItem:
    artifact_item = MuseumItem.of(name, difficulty, locations, geodes, monsters)
    all_museum_artifacts.append(artifact_item)
    all_museum_items.append(artifact_item)
    return artifact_item


def create_mineral(name: str,
                   locations: Union[str, Tuple[str, ...]] = (),
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
        if "Fishing Chest" in geodes:
            difficulty += 4.3

    mineral_item = MuseumItem.of(name, difficulty, locations, geodes, monsters)
    all_museum_minerals.append(mineral_item)
    all_museum_items.append(mineral_item)
    return mineral_item


class Artifact:
    dwarf_scroll_i = create_artifact("Dwarf Scroll I", 5.6, Region.mines_floor_20,
                                     monsters=unlikely)
    dwarf_scroll_ii = create_artifact("Dwarf Scroll II", 3, Region.mines_floor_20,
                                      monsters=unlikely)
    dwarf_scroll_iii = create_artifact("Dwarf Scroll III", 7.5, Region.mines_floor_60,
                                       monsters=Monster.blue_slime)
    dwarf_scroll_iv = create_artifact("Dwarf Scroll IV", 4, Region.mines_floor_100)
    chipped_amphora = create_artifact("Chipped Amphora", 6.7, Region.town,
                                      geodes=Geode.artifact_trove)
    arrowhead = create_artifact("Arrowhead", 8.5, (Region.mountain, Region.forest, Region.bus_stop),
                                geodes=Geode.artifact_trove)
    ancient_doll = create_artifact(Artifact.ancient_doll, 13.1, (Region.mountain, Region.forest, Region.bus_stop),
                                   geodes=(Geode.artifact_trove, WaterChest.fishing_chest))
    elvish_jewelry = create_artifact("Elvish Jewelry", 5.3, Region.forest,
                                     geodes=(Geode.artifact_trove, WaterChest.fishing_chest))
    chewing_stick = create_artifact("Chewing Stick", 10.3, (Region.mountain, Region.forest, Region.town),
                                    geodes=(Geode.artifact_trove, WaterChest.fishing_chest))
    ornamental_fan = create_artifact("Ornamental Fan", 7.4, (Region.beach, Region.forest, Region.town),
                                     geodes=(Geode.artifact_trove, WaterChest.fishing_chest))
    dinosaur_egg = create_artifact(AnimalProduct.dinosaur_egg, 11.4, (Region.skull_cavern),
                                   monsters=Monster.pepper_rex)
    rare_disc = create_artifact("Rare Disc", 5.6, Region.stardew_valley,
                                geodes=(Geode.artifact_trove, WaterChest.fishing_chest),
                                monsters=unlikely)
    ancient_sword = create_artifact("Ancient Sword", 5.8, (Region.forest, Region.mountain),
                                    geodes=(Geode.artifact_trove, WaterChest.fishing_chest))
    rusty_spoon = create_artifact("Rusty Spoon", 9.6, Region.town,
                                  geodes=(Geode.artifact_trove, WaterChest.fishing_chest))
    rusty_spur = create_artifact("Rusty Spur", 15.6, Region.farm,
                                 geodes=(Geode.artifact_trove, WaterChest.fishing_chest))
    rusty_cog = create_artifact("Rusty Cog", 9.6, Region.mountain,
                                geodes=(Geode.artifact_trove, WaterChest.fishing_chest))
    chicken_statue = create_artifact("Chicken Statue", 13.5, Region.farm,
                                     geodes=(Geode.artifact_trove, WaterChest.fishing_chest))
    ancient_seed = create_artifact("Ancient Seed", 8.4, (Region.forest, Region.mountain),
                                   geodes=(Geode.artifact_trove, WaterChest.fishing_chest),
                                   monsters=unlikely)
    prehistoric_tool = create_artifact("Prehistoric Tool", 11.1, (Region.mountain, Region.forest, Region.bus_stop),
                                       geodes=(Geode.artifact_trove, WaterChest.fishing_chest))
    dried_starfish = create_artifact("Dried Starfish", 12.5, Region.beach,
                                     geodes=(Geode.artifact_trove, WaterChest.fishing_chest))
    anchor = create_artifact("Anchor", 8.5, Region.beach, geodes=(Geode.artifact_trove, WaterChest.fishing_chest))
    glass_shards = create_artifact("Glass Shards", 11.5, Region.beach,
                                   geodes=(Geode.artifact_trove, WaterChest.fishing_chest))
    bone_flute = create_artifact("Bone Flute", 6.3, (Region.mountain, Region.forest, Region.town),
                                 geodes=(Geode.artifact_trove, WaterChest.fishing_chest))
    prehistoric_handaxe = create_artifact(Artifact.prehistoric_handaxe, 13.7,
                                          (Region.mountain, Region.forest, Region.bus_stop),
                                          geodes=Geode.artifact_trove)
    dwarvish_helm = create_artifact("Dwarvish Helm", 8.7, Region.mines_floor_20,
                                    geodes=(Geode.geode, Geode.omni, Geode.artifact_trove))
    dwarf_gadget = create_artifact("Dwarf Gadget", 9.7, Region.mines_floor_60,
                                   geodes=(Geode.magma, Geode.omni, Geode.artifact_trove))
    ancient_drum = create_artifact("Ancient Drum", 9.5, (Region.bus_stop, Region.forest, Region.town),
                                   geodes=(Geode.frozen, Geode.omni, Geode.artifact_trove))
    golden_mask = create_artifact("Golden Mask", 6.7, Region.desert,
                                  geodes=Geode.artifact_trove)
    golden_relic = create_artifact("Golden Relic", 9.7, Region.desert,
                                   geodes=Geode.artifact_trove)
    strange_doll_green = create_artifact("Strange Doll (Green)", 10, Region.town,
                                         geodes=Forageable.secret_note)
    strange_doll = create_artifact("Strange Doll", 10, Region.desert,
                                   geodes=Forageable.secret_note)
    prehistoric_scapula = create_artifact("Prehistoric Scapula", 6.2,
                                          (Region.dig_site, Region.forest, Region.town))
    prehistoric_tibia = create_artifact("Prehistoric Tibia", 16.6,
                                        (Region.dig_site, Region.forest, Region.railroad))
    prehistoric_skull = create_artifact("Prehistoric Skull", 3.9, (Region.dig_site, Region.mountain))
    skeletal_hand = create_artifact(Fossil.skeletal_hand, 7.9, (Region.dig_site, Region.backwoods, Region.beach))
    prehistoric_rib = create_artifact("Prehistoric Rib", 15, (Region.dig_site, Region.farm, Region.town),
                                      monsters=Monster.pepper_rex)
    prehistoric_vertebra = create_artifact("Prehistoric Vertebra", 12.7, (Region.dig_site, Region.bus_stop),
                                           monsters=Monster.pepper_rex)
    skeletal_tail = create_artifact("Skeletal Tail", 5.1, (Region.dig_site, Region.mines_floor_20),
                                    geodes=WaterChest.fishing_chest)
    nautilus_fossil = create_artifact("Nautilus Fossil", 6.9, (Region.dig_site, Region.beach),
                                      geodes=WaterChest.fishing_chest)
    amphibian_fossil = create_artifact("Amphibian Fossil", 6.3, (Region.dig_site, Region.forest, Region.mountain),
                                       geodes=WaterChest.fishing_chest)
    palm_fossil = create_artifact("Palm Fossil", 10.2,
                                  (Region.dig_site, Region.desert, Region.forest, Region.beach))
    trilobite = create_artifact("Trilobite", 7.4, (Region.dig_site, Region.desert, Region.forest, Region.beach))


class Mineral:
    quartz = create_mineral(Mineral.quartz, Region.mines_floor_20, difficulty=100.0 / 5.0)
    fire_quartz = create_mineral("Fire Quartz", Region.mines_floor_100,
                                 geodes=(Geode.magma, Geode.omni, WaterChest.fishing_chest),
                                 difficulty=100.0 / 5.0)
    frozen_tear = create_mineral("Frozen Tear", Region.mines_floor_60,
                                 geodes=(Geode.frozen, Geode.omni, WaterChest.fishing_chest),
                                 monsters=unlikely,
                                 difficulty=100.0 / 5.0)
    earth_crystal = create_mineral("Earth Crystal", Region.mines_floor_20,
                                   geodes=(Geode.geode, Geode.omni, WaterChest.fishing_chest),
                                   monsters=Monster.duggy,
                                   difficulty=100.0 / 5.0)
    emerald = create_mineral("Emerald", Region.mines_floor_100,
                             geodes=WaterChest.fishing_chest)
    aquamarine = create_mineral("Aquamarine", Region.mines_floor_60,
                                geodes=WaterChest.fishing_chest)
    ruby = create_mineral("Ruby", Region.mines_floor_100,
                          geodes=WaterChest.fishing_chest)
    amethyst = create_mineral("Amethyst", Region.mines_floor_20,
                              geodes=WaterChest.fishing_chest)
    topaz = create_mineral("Topaz", Region.mines_floor_20,
                           geodes=WaterChest.fishing_chest)
    jade = create_mineral("Jade", Region.mines_floor_60,
                          geodes=WaterChest.fishing_chest)
    diamond = create_mineral("Diamond", Region.mines_floor_60,
                             geodes=WaterChest.fishing_chest)
    prismatic_shard = create_mineral("Prismatic Shard", Region.skull_cavern_100,
                                     geodes=unlikely,
                                     monsters=unlikely)
    alamite = create_mineral("Alamite",
                             geodes=(Geode.geode, Geode.omni))
    bixite = create_mineral("Bixite",
                            geodes=(Geode.magma, Geode.omni),
                            monsters=unlikely)
    baryte = create_mineral("Baryte",
                            geodes=(Geode.magma, Geode.omni))
    aerinite = create_mineral("Aerinite",
                              geodes=(Geode.frozen, Geode.omni))
    calcite = create_mineral("Calcite",
                             geodes=(Geode.geode, Geode.omni))
    dolomite = create_mineral("Dolomite",
                              geodes=(Geode.magma, Geode.omni))
    esperite = create_mineral("Esperite",
                              geodes=(Geode.frozen, Geode.omni))
    fluorapatite = create_mineral("Fluorapatite",
                                  geodes=(Geode.frozen, Geode.omni))
    geminite = create_mineral("Geminite",
                              geodes=(Geode.frozen, Geode.omni))
    helvite = create_mineral("Helvite",
                             geodes=(Geode.magma, Geode.omni))
    jamborite = create_mineral("Jamborite",
                               geodes=(Geode.geode, Geode.omni))
    jagoite = create_mineral("Jagoite",
                             geodes=(Geode.geode, Geode.omni))
    kyanite = create_mineral("Kyanite",
                             geodes=(Geode.frozen, Geode.omni))
    lunarite = create_mineral("Lunarite",
                              geodes=(Geode.frozen, Geode.omni))
    malachite = create_mineral("Malachite",
                               geodes=(Geode.geode, Geode.omni))
    neptunite = create_mineral("Neptunite",
                               geodes=(Geode.magma, Geode.omni))
    lemon_stone = create_mineral("Lemon Stone",
                                 geodes=(Geode.magma, Geode.omni))
    nekoite = create_mineral("Nekoite",
                             geodes=(Geode.geode, Geode.omni))
    orpiment = create_mineral("Orpiment",
                              geodes=(Geode.geode, Geode.omni))
    petrified_slime = create_mineral(Mineral.petrified_slime, Region.slime_hutch)
    thunder_egg = create_mineral("Thunder Egg",
                                 geodes=(Geode.geode, Geode.omni))
    pyrite = create_mineral("Pyrite",
                            geodes=(Geode.frozen, Geode.omni))
    ocean_stone = create_mineral("Ocean Stone",
                                 geodes=(Geode.frozen, Geode.omni))
    ghost_crystal = create_mineral("Ghost Crystal",
                                   geodes=(Geode.frozen, Geode.omni))
    tigerseye = create_mineral("Tigerseye",
                               geodes=(Geode.magma, Geode.omni))
    jasper = create_mineral("Jasper",
                            geodes=(Geode.magma, Geode.omni))
    opal = create_mineral("Opal",
                          geodes=(Geode.frozen, Geode.omni))
    fire_opal = create_mineral("Fire Opal",
                               geodes=(Geode.magma, Geode.omni))
    celestine = create_mineral("Celestine",
                               geodes=(Geode.geode, Geode.omni))
    marble = create_mineral("Marble",
                            geodes=(Geode.frozen, Geode.omni))
    sandstone = create_mineral("Sandstone",
                               geodes=(Geode.geode, Geode.omni))
    granite = create_mineral("Granite",
                             geodes=(Geode.geode, Geode.omni))
    basalt = create_mineral("Basalt",
                            geodes=(Geode.magma, Geode.omni))
    limestone = create_mineral("Limestone",
                               geodes=(Geode.geode, Geode.omni))
    soapstone = create_mineral("Soapstone",
                               geodes=(Geode.frozen, Geode.omni))
    hematite = create_mineral("Hematite",
                              geodes=(Geode.frozen, Geode.omni))
    mudstone = create_mineral("Mudstone",
                              geodes=(Geode.geode, Geode.omni))
    obsidian = create_mineral("Obsidian",
                              geodes=(Geode.magma, Geode.omni))
    slate = create_mineral("Slate", geodes=(Geode.geode, Geode.omni))
    fairy_stone = create_mineral("Fairy Stone", geodes=(Geode.frozen, Geode.omni))
    star_shards = create_mineral("Star Shards", geodes=(Geode.magma, Geode.omni))


dwarf_scrolls = (Artifact.dwarf_scroll_i, Artifact.dwarf_scroll_ii, Artifact.dwarf_scroll_iii, Artifact.dwarf_scroll_iv)
skeleton_front = (Artifact.prehistoric_skull, Artifact.skeletal_hand, Artifact.prehistoric_scapula)
skeleton_middle = (Artifact.prehistoric_rib, Artifact.prehistoric_vertebra)
skeleton_back = (Artifact.prehistoric_tibia, Artifact.skeletal_tail)

all_museum_items_by_name = {item.item_name: item for item in all_museum_items}
