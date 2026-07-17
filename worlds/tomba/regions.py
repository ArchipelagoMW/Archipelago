from __future__ import annotations

from typing import TYPE_CHECKING, Any
from dataclasses import dataclass

from BaseClasses import Region, CollectionRule

from .constants import Areas, Regions, Items, Events
from .events import Started

if TYPE_CHECKING:
    from .world import TombaWorld
    from rule_builder.rules import Rule


@dataclass
class SectionData:
    game_id: int
    name: str


@dataclass
class AreaData:
    game_id: int
    name: str
    sections: list[SectionData]


@dataclass
class RegionData:
    area: AreaData
    section: SectionData

    def __init__(self, area: AreaData, section: SectionData):
        self.area = area
        self.section = section

    def __repr__(self) -> str:
        return f"{self.section} ({self.area})"


class RegionHandler:
    # Unused right now
    area_table: list[AreaData] = [
        AreaData(
            0x00,
            Areas.VILLAGE_OF_ALL_BEGINNINGS,
            [
                SectionData(0x00, "Village Of All Beginnings"),
                SectionData(0x01, "Forest Of All Beginnings"),
                SectionData(0x02, "Hut Entrance"),
                SectionData(0x03, "100 Year Old Man's Hut"),
                SectionData(0x04, "Behind The Hut"),
                SectionData(0x05, "Ol' Pond"),
            ],
        ),
        AreaData(
            0x01,
            Areas.DWARF_FOREST,
            [
                SectionData(0x00, "Forest Of 100 Flowers"),
                SectionData(0x01, "Right Entrance"),
                SectionData(0x02, "Wobbly Wharf"),
                SectionData(0x03, "Watch Tower"),
                SectionData(0x04, "Charity Square"),
            ],
        ),
        AreaData(
            0x02,
            Areas.DWARF_VILLAGE,
            [
                SectionData(0x00, "Dwarf Village"),
                SectionData(0x01, "Dwarf Elder's Hut"),
                SectionData(0x02, "Underground Prison"),
                SectionData(0x03, "Underground Maze"),
                SectionData(0x04, "Million Year Old Man's Room"),
                SectionData(0x05, "The Small Strange Room"),
            ],
        ),
        AreaData(
            0x03,
            Areas.PHOENIX_MOUNTAIN,
            [
                SectionData(0x00, "Stormy Mountain"),
                SectionData(0x01, "Stormy Mountain Second"),
                SectionData(0x02, "Lava Caves"),
                SectionData(0x03, "Phoenix Nest"),
                SectionData(0x04, "Stormy Mountain Purified"),
                SectionData(0x05, "Stormy Mountain Purified Second"),
            ],
        ),
        AreaData(
            0x04,
            Areas.HAUNTED_MANSION,
            [
                SectionData(0x00, "North Side Of Mansion"),
                SectionData(0x01, "West Side Of Mansion"),
                SectionData(0x02, "South Side Of Mansion"),
                SectionData(0x03, "East Side Of Mansion"),
                SectionData(0x04, "Sunny Room"),
                SectionData(0x05, "Thief's Room One"),
                SectionData(0x06, "Swimming Room"),
                SectionData(0x07, "Keyhole Room"),
                SectionData(0x08, "Hiding Room"),
                SectionData(0x09, "Room Of Tribulation"),
                SectionData(0x0A, "Laughing Room"),
                SectionData(0x0B, "Civilization Room"),
                SectionData(0x0C, "Trap Room"),
                SectionData(0x0D, "Trick Room"),
                SectionData(0x0E, "Sun Torch Stand"),
                SectionData(0x0F, "1000 Year Old Man's Room"),
                SectionData(0x10, "Shadow Room"),
                SectionData(0x11, "Thief's Room Two"),
                SectionData(0x12, "Thief's Room Three"),
                SectionData(0x13, "Crying Room"),
            ],
        ),
        AreaData(
            0x05,
            Areas.BACCUS_VILLAGE,
            [
                SectionData(0x00, "Baccus Village"),
                SectionData(0x01, "Central Park"),
                SectionData(0x02, "Baccus Village"),
                SectionData(0x03, "Central Park"),
            ],
        ),
        AreaData(
            0x06,
            Areas.DIRT_MOTOCROSS,
            [
                SectionData(0x00, "The Mermaid Singing Rock Beach"),
                SectionData(0x01, "The Mermaid Singing Rock Mermaid"),
            ],
        ),
        AreaData(
            0x07,
            Areas.DWARF_FOREST_PURIFIED,
            [
                SectionData(0x00, "Forest Of 100 Flowers"),
                SectionData(0x01, "Right Entrance"),
                SectionData(0x02, "Wobbly Wharf"),
                SectionData(0x03, "Watch Tower"),
                SectionData(0x04, "Charity Square"),
            ],
        ),
        AreaData(
            0x08,
            Areas.BACCUS_LAKE,
            [
                SectionData(0x00, "Baccus Lake"),
                SectionData(0x01, "Baccus Pier"),
                SectionData(0x02, "Baccus Lake"),
                SectionData(0x03, "Baccus Pier"),
            ],
        ),
        AreaData(
            0x09,
            Areas.MUSHROOM_VILLAGE,
            [
                SectionData(0x00, "Mushroom Forest"),
                SectionData(0x01, "Lake"),
                SectionData(0x02, "Mansion Grandfather Clock Room"),
                SectionData(0x03, "Mansion Chandelier Room"),
                SectionData(0x04, "Mansion Descending Stairs"),
                SectionData(0x05, "Mansion Ascending Stairs"),
                SectionData(0x06, "Leaf Slider"),
            ],
        ),
        AreaData(
            0x0A,
            Areas.DEEP_JUNGLE,
            [
                SectionData(0x00, "Masakari Jungle"),
                SectionData(0x01, "Masakari River"),
                SectionData(0x02, "Old Tree Hill"),
                SectionData(0x03, "Trick Village"),
                SectionData(0x04, "Masakari Jungle Purified"),
                SectionData(0x05, "Masakari River Purified"),
                SectionData(0x06, "Old Tree Hill Purified"),
                SectionData(0x07, "Trick Village Purified"),
                SectionData(0x08, "10000 Year Old Man's Room"),
            ],
        ),
        AreaData(
            0x0B,
            Areas.VILLAGE_OF_CIVILIZATION,
            [
                SectionData(0x00, "Lumberjack Town"),
                SectionData(0x01, "Lumberjack Factory"),
                SectionData(0x02, "Dried Wishing Well"),
            ],
        ),
        AreaData(
            0x0C,
            Areas.HAUNTED_MANSION_PURIFIED,
            [
                SectionData(0x00, "North Side Of Mansion"),
                SectionData(0x01, "West Side Of Mansion"),
                SectionData(0x02, "South Side Of Mansion"),
                SectionData(0x03, "East Side Of Mansion"),
                SectionData(0x04, "Sunny Room"),
                SectionData(0x05, "Thief's Room One"),
                SectionData(0x06, "Swimming Room"),
                SectionData(0x07, "Keyhole Room"),
                SectionData(0x08, "Hiding Room"),
                SectionData(0x09, "Room Of Tribulation"),
                SectionData(0x0A, "Laughing Room"),
                SectionData(0x0B, "Civilization Room"),
                SectionData(0x0C, "Trap Room"),
                SectionData(0x0D, "Trick Room"),
                SectionData(0x0E, "Sun Torch Stand"),
                SectionData(0x0F, "1000 Year Old Man's Room"),
                SectionData(0x10, "Shadow Room"),
                SectionData(0x11, "Thief's Room Two"),
                SectionData(0x12, "Thief's Room Three"),
                SectionData(0x13, "Crying Room"),
            ],
        ),
        AreaData(
            0x0D,
            Areas.PIG_ISLAND,
            [
                SectionData(0x00, "Pig Island"),
                SectionData(0x01, "Pig Island Cave"),
                SectionData(0x02, "Pig Island Cave End"),
            ],
        ),
        AreaData(
            0x0E,
            Areas.EVIL_PIGS,
            [
                SectionData(0x00, "Evil Pig Area One"),
                SectionData(0x01, "Evil Pig Area Two"),
                SectionData(0x02, "Evil Pig Area Three"),
                SectionData(0x03, "Evil Pig Area Four"),
                SectionData(0x04, "Evil Pig Area Five"),
                SectionData(0x05, "Evil Pig Area Six"),
                SectionData(0x06, "Evil Pig Area Seven"),
                SectionData(0x07, "Evil Pig Area Eight"),
            ],
        ),
        AreaData(
            0x0F,
            Areas.UNKNOWN,
            [
                SectionData(0x00, "Softlock 1"),
                SectionData(0x01, "Softlock 2"),
                SectionData(0x02, "Blackscreen 1"),
                SectionData(0x03, "Blackscreen 2"),
            ],
        ),
        AreaData(
            0x10,
            Areas.CLOCK_TOWER,
            [
                SectionData(0x00, "Stones Town"),
                SectionData(0x01, "Clock Tower Softlock"),
                SectionData(0x02, "Clock Tower Crash"),
                SectionData(0x03, "Clock Tower Engines Room"),
                SectionData(0x04, "Clock Tower Entrance"),
                SectionData(0x05, "Clock Tower Halfway Up"),
                SectionData(0x06, "Clock Tower Engines Room No Exit"),
            ],
        ),
        AreaData(
            0x11,
            Areas.IRON_TOWER,
            [
                SectionData(0x00, "Iron Town Crash"),
                SectionData(0x01, "Iron Castle Entrance"),
                SectionData(0x02, "Iron Castle Main Room"),
                SectionData(0x03, "Iron Castle Left Room"),
                SectionData(0x04, "Iron Castle Right Room"),
                SectionData(0x05, "Iron Castle Engine Room"),
                SectionData(0x06, "Iron Castle Softlock 1"),
                SectionData(0x07, "Iron Castle Softlock 2"),
                SectionData(0x08, "Iron Castle Softlock 3"),
                SectionData(0x09, "Iron Castle Crash"),
                SectionData(0x0A, "Iron Castle Softlock 4"),
                SectionData(0x0B, "Iron Castle Softlock 5"),
            ],
        ),
        AreaData(
            0x12,
            Areas.Y_CROSSING,
            [
                SectionData(0x00, "Village Of Civilization"),
                SectionData(0x01, "Y Crossing"),
                SectionData(0x02, "Witch's Hut"),
            ],
        ),
        AreaData(
            0x13,
            Areas.VILLAGE_OF_CIVILIZATION_PURIFIED,
            [
                SectionData(0x00, "Dwarf Elder's Hut"),
                SectionData(0x01, "Dwarf Elder's Hut"),
                SectionData(0x02, "Hidden Village"),
            ],
        ),
    ]

    region_names = [
        value for key, value in Regions.__dict__.items() if not key.startswith("_") and isinstance(value, str)
    ]


def create_and_connect_regions(world: TombaWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: TombaWorld) -> None:
    regions = []

    for region_name in RegionHandler.region_names:
        regions.append(Region(region_name, world.player, world.multiworld))

    world.multiworld.regions += regions


def connect(world: TombaWorld, source_name: str, target_name: str, rule: CollectionRule | Rule[Any] | None = None):
    source = world.get_region(source_name)
    target = world.get_region(target_name)
    source.connect(target, f"{source} to {target}", rule)


def connect_regions(world: TombaWorld) -> None:
    connect(
        world,
        Regions.VILLAGE_OF_ALL_BEGINNINGS,
        Regions.FOREST_OF_ALL_BEGINNINGS,
        lambda state: state.has(Items.FURIOUS_TORNADO, world.player),
    )

    connect(
        world,
        Regions.FOREST_OF_ALL_BEGINNINGS,
        Regions.FOREST_OF_100_FLOWERS,
        lambda state: state.has(Items.CHICK, world.player, 4),
    )
    connect(world, Regions.FOREST_OF_ALL_BEGINNINGS, Regions.OL_POND)

    connect(world, Regions.FOREST_OF_100_FLOWERS, Regions.DWARF_VILLAGE)
    connect(
        world,
        Regions.FOREST_OF_100_FLOWERS,
        Regions.WOBBLY_WHARF,
        lambda state: state.has(Started(Events.SAVE_THE_DWARVES), world.player),
    )
    connect(
        world,
        Regions.FOREST_OF_100_FLOWERS,
        Regions.WATCH_TOWER,
        lambda state: state.has(Started(Events.SAVE_THE_DWARVES), world.player),
    )

    connect(
        world,
        Regions.CHARITY_SQUARE,
        Regions.HIDDEN_VILLAGE,
        lambda state: state.has(Items.LEAF_BUTTERFLY, world.player, 29),
    )

    connect(
        world,
        Regions.DWARF_VILLAGE,
        Regions.DWARF_JAIL,
        lambda state: state.has(Started(Events.TO_PHOENIX_MOUNTAIN), world.player),
    )

    connect(
        world,
        Regions.WATCH_TOWER,
        Regions.MUSHROOM_FOREST,
        lambda state: state.has(Started(Events.TO_PHOENIX_MOUNTAIN), world.player),
    )
    connect(
        world,
        Regions.WATCH_TOWER,
        Regions.CHARITY_SQUARE,
        lambda state: state.has(Started(Events.TO_PHOENIX_MOUNTAIN), world.player),
    )

    connect(
        world,
        Regions.WOBBLY_WHARF,
        Regions.CHARITY_SQUARE,
        lambda state: state.has(Started(Events.TO_PHOENIX_MOUNTAIN), world.player),
    )
