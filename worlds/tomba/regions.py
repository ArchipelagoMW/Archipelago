from __future__ import annotations

from typing import TYPE_CHECKING, Any
from rule_builder.rules import Has, Rule
from dataclasses import dataclass, field

from BaseClasses import Region, CollectionRule, Entrance
from entrance_rando import EntranceType

from .constants import Regions, Items, Events
from .helpers import Started, Cleared, Rules
from .sections import Section, Sections
from .events import EventHandler

if TYPE_CHECKING:
    from .world import TombaWorld


@dataclass
class Door:
    raw_name: str
    name: str

    source: Section
    target: Section

    # Entrance ID to update
    start_id: int

    # Entrance ID to go to
    end_id: int

    # Same for the return trip
    back_name: str
    back_start_id: int | None = None
    back_end_id: int | None = None

    randomization_type: EntranceType = EntranceType.TWO_WAY

    rule: CollectionRule | Rule[Any] | None = None

    related_events: list[str] = field(default_factory=list)

    def __init__(
        self,
        name: str,
        source: Section,
        target: Section,
        start_id: int,
        end_id: int,
        back_start_id: int | None = None,
        back_end_id: int | None = None,
        rule: CollectionRule | Rule[Any] | None = None,
        related_events: list[str] = [],
        related_regions: list[str] = [],
    ):
        self.raw_name = name
        self.name = f"{source.name}: {name}"
        self.back_name = f"{target.name}: {name}"
        self.source = source
        self.target = target
        self.start_id = start_id
        self.end_id = end_id
        self.back_start_id = back_start_id
        self.back_end_id = back_end_id
        self.rule = rule
        self.related_events = related_events
        self.related_regions = related_regions

        if self.back_end_id is None or self.back_start_id is None:
            self.randomization_type = EntranceType.ONE_WAY

    def is_forward(self, name: str) -> bool:
        """Indicate if the given name is the forward or backward direction"""
        assert name == self.name or name == self.back_name
        return name == self.name


region_names = [value for key, value in Regions.__dict__.items() if not key.startswith("_") and isinstance(value, str)]


def create_and_connect_regions(world: TombaWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: TombaWorld) -> None:
    regions = []

    regions.append(Region("Menu", world.player, world.multiworld))

    for region_name in region_names:
        regions.append(Region(region_name, world.player, world.multiworld))

    world.multiworld.regions += regions


def get_randomizable_doors(player: int) -> list[Door]:
    return [
        Door(
            "Garage Door",
            source=Sections.VILLAGE_OF_ALL_BEGINNING,
            target=Sections.GARAGE,
            start_id=0x00,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x01,
            rule=Rules.CAN_BREAK_STUFF,
        ),
        Door(
            "Witch Door",
            source=Sections.VILLAGE_OF_ALL_BEGINNING,
            target=Sections.WITCH_HUT,
            start_id=0x02,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x03,
            rule=lambda state: state.can_reach_location(Started(Events.THE_CUTE_WITCH), player),
            related_events=[Events.THE_CUTE_WITCH, Events.WE_NEED_POWER, Events.A_REFRESHING_DRINK],
        ),
        Door(
            "Mansion Door",
            source=Sections.MANSION,
            target=Sections.VILLAGE_OF_ALL_BEGINNING,
            start_id=0x00,
            end_id=0x02,
        ),
        Door(
            "Ol' Pond Door",
            source=Sections.FOREST_OF_ALL_BEGINNING_PART_1,
            target=Sections.OL_POND,
            start_id=0x00,
            end_id=0x02,
            back_start_id=0x00,
            back_end_id=0x01,
        ),
        Door(
            "Underground Maze Door",
            source=Sections.FOREST_OF_ALL_BEGINNING_PART_1,
            target=Sections.UNDERGROUND_MAZE,
            start_id=0x01,
            end_id=0x05,
            back_start_id=0x02,
            back_end_id=0x02,
            rule=lambda state: state.can_reach_location(Cleared(Events.THE_THIEFS_DOOR), player),
            related_events=[Events.THE_THIEFS_DOOR],
        ),
        Door(
            "Trick Village Door",
            source=Sections.OL_POND,
            target=Sections.TRICK_VILLAGE,
            start_id=0x01,
            end_id=0x01,
            back_start_id=0x00,
            back_end_id=0x01,
            rule=lambda state: (
                state.can_reach_location(Cleared(Events.I_CANT_SWIM), player)
                and state.has(Items.KEY_TO_OL_POND, player)
            )
            or state.has(Items.SACRED_FISH, player),
            related_events=[Events.I_CANT_SWIM, Events.A_REFRESHING_DRINK],
        ),
        Door(
            "100 YOAM Door",
            source=Sections.FOREST_OF_ALL_BEGINNING_PART_2,
            target=Sections.HUNDREDS_YEAR_OLD_MANS_HUT,
            start_id=0x01,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x02,
        ),
        Door(
            "Chimney",
            source=Sections.HUNDREDS_YEAR_OLD_MANS_HUT,
            target=Sections.FOREST_OF_100_FLOWERS_PART_1,
            start_id=0x01,
            end_id=0x01,
            back_start_id=0x00,
            back_end_id=0x01,
            rule=lambda state: state.can_reach_location(Cleared(Events.INSIDE_THE_KOKKA_EGGS), player),
            related_events=[Events.INSIDE_THE_KOKKA_EGGS],
        ),
        Door(
            "Big House",
            source=Sections.FOREST_OF_100_FLOWERS_PART_1,
            target=Sections.WOBBLY_WHARF,
            start_id=0x01,
            end_id=0x02,
            back_start_id=0x00,
            back_end_id=0x02,
            rule=lambda state: state.can_reach_location(Started(Events.SAVE_THE_DWARVES), player),
            related_events=[
                Events.SAVE_THE_DWARVES,
                Events.BEGINNERS_DWARF_LANGUAGE,
            ],
        ),
        Door(
            "Stone Slab",
            source=Sections.FOREST_OF_100_FLOWERS_PART_2,
            target=Sections.WATCH_TOWER,
            start_id=0x01,
            end_id=0x03,
            back_start_id=0x00,
            back_end_id=0x01,
            rule=lambda state: state.can_reach_location(Started(Events.SAVE_THE_DWARVES), player),
            related_events=[Events.SAVE_THE_DWARVES],
        ),
        Door(
            "Big Red Arrow",
            source=Sections.FOREST_OF_100_FLOWERS_PART_2,
            target=Sections.DWARF_VILLAGE,
            start_id=0x02,
            end_id=0x02,
            back_start_id=0x00,
            back_end_id=0x02,
        ),
        Door(
            "Wobbly Stairs",
            source=Sections.WOBBLY_WHARF,
            target=Sections.CHARITY_SQUARE,
            start_id=0x01,
            end_id=0x01,
            back_start_id=0x01,
            back_end_id=0x01,
            rule=lambda state: state.can_reach_location(Started(Events.TO_PHOENIX_MOUNTAIN), player),
            related_events=[Events.TO_PHOENIX_MOUNTAIN],
        ),
        Door(
            "Elevator",
            source=Sections.WATCH_TOWER,
            target=Sections.UNDERGROUND_MAZE,
            start_id=0x03,
            end_id=0x01,
            back_start_id=0x03,
            back_end_id=0x04,
            rule=lambda state: state.can_reach_location(Cleared(Events.WE_NEED_POWER), player),
            related_events=[Events.WE_NEED_POWER],
        ),
        Door(
            "Middle Door",
            source=Sections.WATCH_TOWER,
            target=Sections.CHARITY_SQUARE,
            start_id=0x01,
            end_id=0x03,
            back_start_id=0x00,
            back_end_id=0x01,
            rule=lambda state: state.can_reach_location(Started(Events.TO_PHOENIX_MOUNTAIN), player),
            related_events=[Events.TO_PHOENIX_MOUNTAIN],
        ),
        Door(
            "Rightmost Door",
            source=Sections.WATCH_TOWER,
            target=Sections.MUSHROOM_FOREST,
            start_id=0x02,
            end_id=0x01,
            back_start_id=0x01,
            back_end_id=0x02,
            rule=lambda state: state.can_reach_location(Started(Events.TO_PHOENIX_MOUNTAIN), player),
            related_events=[Events.TO_PHOENIX_MOUNTAIN],
        ),
        # Door("Leaf Slider", source=Sections.CHARITY_SQUARE, target=Sections.LEAF_SLIDER,
        #     start_id=0x02, end_id=0x00,
        #     rule=lambda state: state.can_reach_location(Cleared(Events.LEAF_SLIDER), player)
        # ),
        Door(
            "Flower Tower",
            source=Sections.CHARITY_SQUARE,
            target=Sections.FLOWER_TOWER,
            start_id=0x03,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x04,
            rule=lambda state: state.can_reach_location(Cleared(Events.THE_FLOWER_TOWER), player),
            related_events=[Events.THE_FLOWER_TOWER],
        ),
        Door(
            "Right Door",
            source=Sections.DWARF_VILLAGE,
            target=Sections.DWARF_ELDER_HUT,
            start_id=0x01,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x01,
        ),
        Door(
            "Hole",
            source=Sections.DWARF_ELDER_HUT,
            target=Sections.UNDERGROUND_PRISON,
            start_id=0x01,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x01,
            rule=lambda state: state.can_reach_location(Started(Events.TO_PHOENIX_MOUNTAIN), player),
            related_events=[Events.TO_PHOENIX_MOUNTAIN],
        ),
        Door(
            "Million Year Old Man Door",
            source=Sections.UNDERGROUND_MAZE,
            target=Sections.MILLION_YEAR_OLD_MANS_ROOM,
            start_id=0x00,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x03,
            rule=lambda state: state.has(Items.MILLION_YEAR_OLD_BELL, player)
            or state.can_reach_location(Cleared(Events.UNBREAKABLE_WIRE), player),
            related_events=[Events.UNBREAKABLE_WIRE],
        ),
        Door(
            "Upper Right Door",
            source=Sections.UNDERGROUND_MAZE,
            target=Sections.CIVILIZATION_ROOM,
            start_id=0x04,
            end_id=0x01,
            back_start_id=0x01,
            back_end_id=0x02,
            rule=lambda state: state.can_reach_location(Started(Events.THE_CIVILIZATION_MACHINE), player),
            related_events=[Events.THE_CIVILIZATION_MACHINE],
        ),
        Door(
            "Upper Left Door",
            source=Sections.UNDERGROUND_MAZE,
            target=Sections.THE_STRANGE_SMALL_ROOM,
            start_id=0x01,
            end_id=0x02,
            back_start_id=0x00,
            back_end_id=0x04,
        ),
        Door(
            "Out of Leaf Slider",
            source=Sections.LEAF_SLIDER,
            target=Sections.MUSHROOM_FOREST,
            start_id=0x01,
            end_id=0x02,
        ),
        Door(
            "Right Door",
            source=Sections.MUSHROOM_FOREST,
            target=Sections.STORMY_MOUNTAINS_PART_1,
            start_id=0x02,
            end_id=0x02,
            back_start_id=0x01,
            back_end_id=0x03,
            rule=lambda state: state.can_reach_location(Cleared(Events.THE_WORLDS_GREATEST_POUT), player),
            related_events=[Events.THE_WORLDS_GREATEST_POUT],
        ),
        Door(
            "Background Door",
            source=Sections.MUSHROOM_FOREST,
            target=Sections.HAUNTED_MANSION_WEST,
            start_id=0x03,
            end_id=0x05,
            back_start_id=0x05,
            back_end_id=0x05,
            rule=lambda state: state.can_reach_location(Cleared(Events.A_DRINK_FOR_GROWNUPS), player),
            related_events=[Events.A_DRINK_FOR_GROWNUPS],
        ),
        Door(
            "Left Door",
            source=Sections.MUSHROOM_FOREST,
            target=Sections.LAKE,
            start_id=0x00,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x04,
        ),
        Door(
            "Left Mansion Door",
            source=Sections.LAKE_LEFT_BANK,
            target=Sections.MANSION_STAIRS_DOWN,
            start_id=0x01,
            end_id=0x00,
            back_start_id=0x01,
            back_end_id=0x02,
            rule=Has(Items.NAVY_EVIL_PIG_BAG),
        ),
        Door(
            "Right Mansion Door",
            source=Sections.LAKE_LEFT_BANK,
            target=Sections.MANSION_STAIRS_UP,
            start_id=0x02,
            end_id=0x00,
            back_start_id=0x01,
            back_end_id=0x01,
        ),
        Door(
            "Upstair Door",
            source=Sections.MANSION_STAIRS_UP,
            target=Sections.MANSION,
            start_id=0x00,
            end_id=0x01,
            back_start_id=0x01,
            back_end_id=0x01,
        ),
        Door(
            "Downstair Door",
            source=Sections.MANSION_STAIRS_DOWN,
            target=Sections.MANSION_JUNGLE_PIG_ROOM,
            start_id=0x00,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x01,
        ),
        Door(
            "Right Exit",
            source=Sections.STORMY_MOUNTAINS_PART_1,
            target=Sections.STORMY_MOUNTAINS_PART_2,
            start_id=0x02,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x03,
        ),
        Door(
            "Left Door",
            source=Sections.STORMY_MOUNTAINS_PART_1,
            target=Sections.BACCUS_VILLAGE,
            start_id=0x00,
            end_id=0x01,
            back_start_id=0x00,
            back_end_id=0x01,
        ),
        Door(
            "Pipe",
            source=Sections.STORMY_MOUNTAINS_PART_2,
            target=Sections.STORMY_MOUNTAINS_PART_1,
            start_id=0x02,
            end_id=0x04,
        ),
        Door(
            "Lava Caves Door",
            source=Sections.STORMY_MOUNTAINS_PART_2,
            target=Sections.LAVA_CAVES,
            start_id=0x01,
            end_id=0x01,
            back_start_id=0x00,
            back_end_id=0x01,
        ),
        Door(
            "Right Door",
            source=Sections.LAVA_CAVES,
            target=Sections.PHOENIXS_NEST,
            start_id=0x01,
            end_id=0x01,
            back_start_id=0x00,
            back_end_id=0x02,
            rule=lambda state: state.can_reach_location(Cleared(Events.LAVA_CAVES), player),
            related_events=[Events.LAVA_CAVES],
        ),
        Door(
            "Ladder",
            source=Sections.LAVA_CAVES,
            target=Sections.HIDDEN_VILLAGE,
            start_id=0x02,
            end_id=0x02,
            back_start_id=0x00,
            back_end_id=0x03,
            rule=lambda state: state.can_reach_location(Cleared(Events.LAVA_CAVES), player)
            and (state.has(Items.GRAPPLE, player) or state.has(Items.GRAPPLEJACK, player)),
            related_events=[Events.LAVA_CAVES],
        ),
        Door(
            "Shadow Room Door",
            source=Sections.HAUNTED_MANSION_NORTH,
            target=Sections.SHADOW_ROOM,
            start_id=0x01,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x01,
        ),
        Door(
            "Civilization Room Door",
            source=Sections.HAUNTED_MANSION_NORTH,
            target=Sections.CIVILIZATION_ROOM,
            start_id=0x02,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x02,
        ),
        Door(
            "Trick Room Door",
            source=Sections.HAUNTED_MANSION_NORTH,
            target=Sections.TRICK_ROOM,
            start_id=0x03,
            end_id=0x01,
            back_start_id=0x01,
            back_end_id=0x03,
        ),
        Door(
            "Thief Room Three Door",
            source=Sections.HAUNTED_MANSION_NORTH,
            target=Sections.THIEFS_ROOM_THREE,
            start_id=0x04,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x04,
        ),
        Door(
            "Keyhole Room Door",
            source=Sections.HAUNTED_MANSION_NORTH,
            target=Sections.KEYHOLE_ROOM,
            start_id=0x05,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x05,
            rule=lambda state: state.has(Items.BIG_KEY, player),
        ),
        Door(
            "Laughing Room Door",
            source=Sections.HAUNTED_MANSION_NORTH,
            target=Sections.LAUGHING_ROOM,
            start_id=0x06,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x06,
            rule=lambda state: state.can_reach_location(Cleared(Events.SMILE), player),
            related_events=[Events.SMILE],
        ),
        Door(
            "Thief Room One Door",
            source=Sections.HAUNTED_MANSION_NORTH,
            target=Sections.THIEFS_ROOM_ONE,
            start_id=0x07,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x07,
        ),
        Door(
            "Baccus Lake Exit",
            source=Sections.HAUNTED_MANSION_WEST,
            target=Sections.BACCUS_LAKE,
            start_id=0x00,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x00,
            rule=lambda state: state.can_reach_region(Sections.BACCUS_LAKE_PIER.name, player),
            related_regions=[Sections.BACCUS_LAKE_PIER.name],
        ),
        Door(
            "Crying Door",
            source=Sections.HAUNTED_MANSION_WEST,
            target=Sections.CRY_ROOM,
            start_id=0x01,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x01,
            rule=lambda state: state.can_reach_location(Cleared(Events.A_DRINK_FOR_GROWNUPS), player),
            related_events=[Events.A_DRINK_FOR_GROWNUPS],
        ),
        Door(
            "Haunted Mansion",
            source=Sections.BACCUS_VILLAGE,
            target=Sections.HAUNTED_MANSION_SOUTH,
            start_id=0x01,
            end_id=0x07,
            back_start_id=0x00,
            back_end_id=0x02,
            rule=lambda state: state.can_reach_location(Started(Events.A_DRINK_FOR_GROWNUPS), player),
            related_events=[Events.A_DRINK_FOR_GROWNUPS],
        ),
        Door(
            "Swimming Room",
            source=Sections.HAUNTED_MANSION_SOUTH,
            target=Sections.SWIMMING_ROOM,
            start_id=0x01,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x01,
            rule=lambda state: state.can_reach_location(Cleared(Events.A_DRINK_FOR_GROWNUPS), player),
            related_events=[Events.A_DRINK_FOR_GROWNUPS],
        ),
        Door(
            "Thief's Room Two",
            source=Sections.HAUNTED_MANSION_SOUTH,
            target=Sections.THIEFS_ROOM_TWO,
            start_id=0x02,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x02,
            rule=lambda state: state.can_reach_location(Cleared(Events.A_DRINK_FOR_GROWNUPS), player),
            related_events=[Events.A_DRINK_FOR_GROWNUPS],
        ),
        Door(
            "Tribulation Room",
            source=Sections.HAUNTED_MANSION_SOUTH,
            target=Sections.TRIBULATION_ROOM,
            start_id=0x03,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x03,
        ),
        Door(
            "1,000 Year Old Man Room",
            source=Sections.HAUNTED_MANSION_SOUTH,
            target=Sections.THOUSAND_YEAR_OLD_MANS_ROOM,
            start_id=0x04,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x04,
            rule=lambda state: state.can_reach_location(Cleared(Events.A_DRINK_FOR_GROWNUPS), player),
            related_events=[Events.A_DRINK_FOR_GROWNUPS],
        ),
        Door(
            "Trick Room",
            source=Sections.HAUNTED_MANSION_SOUTH,
            target=Sections.TRICK_ROOM,
            start_id=0x05,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x05,
            rule=lambda state: state.can_reach_location(Cleared(Events.A_DRINK_FOR_GROWNUPS), player),
            related_events=[Events.A_DRINK_FOR_GROWNUPS],
        ),
        Door(
            "Hidding Room",
            source=Sections.HAUNTED_MANSION_SOUTH,
            target=Sections.HIDING_ROOM,
            start_id=0x06,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x06,
            rule=lambda state: state.can_reach_location(Cleared(Events.A_DRINK_FOR_GROWNUPS), player),
            related_events=[Events.A_DRINK_FOR_GROWNUPS],
        ),
        Door(
            "Sunny Room",
            source=Sections.HAUNTED_MANSION_EAST,
            target=Sections.SUNNY_ROOM,
            start_id=0x01,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x01,
            rule=lambda state: state.can_reach_location(Cleared(Events.A_DRINK_FOR_GROWNUPS), player),
            related_events=[Events.A_DRINK_FOR_GROWNUPS],
        ),
        Door(
            "Trap Room",
            source=Sections.HAUNTED_MANSION_EAST,
            target=Sections.TRAP_ROOM,
            start_id=0x02,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x02,
            rule=lambda state: state.can_reach_location(Cleared(Events.A_DRINK_FOR_GROWNUPS), player),
            related_events=[Events.A_DRINK_FOR_GROWNUPS],
        ),
        Door(
            "Parc Door",
            source=Sections.BACCUS_VILLAGE,
            target=Sections.CENTRAL_PARK,
            start_id=0x02,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x03,
        ),
        Door(
            "River Door",
            source=Sections.THE_MERMAIDS_SINGING_BEACH,
            target=Sections.MASAKARI_RIVER,
            start_id=0x01,
            end_id=0x03,
        ),
        # Door(
        #     "Pier Door",
        #     source=Sections.BACCUS_LAKE,
        #     target=Sections.BACCUS_LAKE_PIER,
        #     start_id=0x01,
        #     end_id=0x00,
        #     back_start_id=0x00,
        #     back_end_id=0x01,
        # ),
        Door(
            "Background Door",
            source=Sections.MASAKARI_JUNGLE,
            target=Sections.Y_CROSSING,
            start_id=0x00,
            end_id=0x04,
            back_start_id=0x03,
            back_end_id=0x02,
            rule=Has(Items.MINERS_HAT),
        ),
        Door(
            "Right Jump",
            source=Sections.MASAKARI_JUNGLE,
            target=Sections.MASAKARI_RIVER,
            start_id=0x01,
            end_id=0x01,
            back_start_id=0x00,
            back_end_id=0x03,
            rule=lambda state: state.can_reach_location(Cleared(Events.I_CANT_SWIM), player),
            related_events=[Events.I_CANT_SWIM],
        ),
        Door(
            "Middle Ladder",
            source=Sections.MASAKARI_RIVER,
            target=Sections.OLD_TREE_HILL,
            start_id=0x01,
            end_id=0x01,
            back_start_id=0x00,
            back_end_id=0x02,
            rule=lambda state: state.can_reach_location(Cleared(Events.I_CANT_SWIM), player),
            related_events=[Events.I_CANT_SWIM],
        ),
        Door(
            "Right Tunnel",
            source=Sections.MASAKARI_RIVER,
            target=Sections.TRICK_VILLAGE,
            start_id=0x02,
            end_id=0x04,
            rule=lambda state: state.can_reach_location(Cleared(Events.TRICK_VILLAGE), player)
            & state.can_reach_location(Cleared(Events.I_CANT_SWIM), player),
            related_events=[Events.TRICK_VILLAGE, Events.I_CANT_SWIM],
        ),
        Door(
            "Right Chute",
            source=Sections.TRICK_VILLAGE,
            target=Sections.MASAKARI_RIVER,
            start_id=0x02,
            end_id=0x03,
            rule=lambda state: state.can_reach_location(Cleared(Events.I_CANT_SWIM), player),
            related_events=[Events.I_CANT_SWIM],
        ),
        Door(
            "Chimney",
            source=Sections.TRICK_VILLAGE,
            target=Sections.TEN_THOUSAND_YEAR_OLD_MANS_ROOM,
            start_id=0x01,
            end_id=0x01,
            back_start_id=0x00,
            back_end_id=0x02,
            rule=lambda state: state.can_reach_location(Cleared(Events.I_CANT_SWIM), player),
            related_events=[Events.I_CANT_SWIM],
        ),
        Door(
            "Factory Door",
            source=Sections.Y_CROSSING,
            target=Sections.LUMBERJACK_FACTORY,
            start_id=0x00,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x01,
            rule=lambda state: state.can_reach_location(Started(Events.WE_NEED_POWER), player),
            related_events=[Events.WE_NEED_POWER],
        ),
        Door(
            "Castle Door",
            source=Sections.Y_CROSSING,
            target=Sections.IRON_CASTLE_ENTRANCE,
            start_id=0x01,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x02,
            rule=lambda state: state.can_reach_location(Started(Events.WE_NEED_POWER), player),
            related_events=[Events.WE_NEED_POWER],
        ),
        Door(
            "Clock Door",
            source=Sections.Y_CROSSING,
            target=Sections.CLOCK_TOWER_ENTRANCE,
            start_id=0x02,
            end_id=0x00,
            back_start_id=0x01,
            back_end_id=0x03,
        ),
        Door(
            "Broken Door",
            source=Sections.LUMBERJACK_FACTORY,
            target=Sections.DRIED_WISHING_WELL,
            start_id=0x01,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x01,
        ),
        Door(
            "Top Door",
            source=Sections.CLOCK_TOWER_ENTRANCE,
            target=Sections.CLOCK_TOWER_HALFWAY_UP,
            start_id=0x00,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x01,
        ),
        # Door(
        #     "Top Door",
        #     source=Sections.IRON_CASTLE_ENTRANCE,
        #     target=Sections.IRON_CASTLE_MAIN_ROOM,
        #     start_id=0x01,
        #     end_id=0x00,
        #     back_start_id=0x00,
        #     back_end_id=0x01,
        # ),
        Door(
            "Left Door",
            source=Sections.IRON_CASTLE_MAIN_ROOM,
            target=Sections.IRON_CASTLE_LEFT_ROOM,
            start_id=0x01,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x01,
        ),
        # Door(
        #     "Middle Door",
        #     source=Sections.IRON_CASTLE_MAIN_ROOM,
        #     target=Sections.IRON_CASTLE_ENGINE_ROOM,
        #     start_id=0x02,
        #     end_id=0x00,
        #     back_start_id=0x00,
        #     back_end_id=0x02,
        #     rule=lambda state: state.can_reach_location(Cleared(Events.BREAK_THE_RUSTY_DOOR), player),
        # ),
        Door(
            "Right Door",
            source=Sections.IRON_CASTLE_MAIN_ROOM,
            target=Sections.IRON_CASTLE_RIGHT_ROOM,
            start_id=0x03,
            end_id=0x00,
            back_start_id=0x00,
            back_end_id=0x03,
        ),
    ]


def connect_regions(world: TombaWorld) -> None:
    def register_related_events(entrance: Entrance, related_events: list[str]):
        for event_name in related_events:
            event = EventHandler.by_name[event_name]
            register_related_regions(entrance, event.related_regions)

    def register_related_regions(entrance: Entrance, related_regions: list[str]):
        for region_name in related_regions:
            region = world.get_region(region_name)
            world.multiworld.register_indirect_condition(region, entrance)

    def connect(
        source_name: str,
        target_name: str,
        entrance_type: EntranceType,
        rule: CollectionRule | Rule[Any] | None = None,
        suffix: str = "",
        related_events: list[str] = [],
        related_regions: list[str] = [],
        name: str | None = None,
        back_name: str | None = None,
    ):
        if name is None:
            name = f"{source_name} to {target_name}{suffix}"
        if back_name is None:
            back_name = f"{target_name} to {source_name}{suffix}"

        source = world.get_region(source_name)
        target = world.get_region(target_name)

        entrance = source.connect(target, name, rule)
        entrance.randomization_type = entrance_type

        register_related_events(entrance, related_events)
        register_related_regions(entrance, related_regions)

        # Add the return direction
        if entrance_type is EntranceType.TWO_WAY:
            entrance = target.connect(source, back_name, rule)
            entrance.randomization_type = entrance_type

            register_related_events(entrance, related_events)
            register_related_regions(entrance, related_regions)

    # Connect all randomizable doors
    for door in get_randomizable_doors(world.player):
        connect(
            source_name=door.source.name,
            target_name=door.target.name,
            entrance_type=door.randomization_type,
            rule=door.rule,
            suffix="",
            name=door.name,
            back_name=door.back_name,
            related_events=door.related_events,
            related_regions=door.related_regions,
        )

    connect(
        "Menu",
        Sections.VILLAGE_OF_ALL_BEGINNING.name,
        entrance_type=EntranceType.TWO_WAY,
    )
    connect(
        Sections.VILLAGE_OF_ALL_BEGINNING.name,
        Sections.FOREST_OF_ALL_BEGINNING_PART_1.name,
        rule=lambda state: state.can_reach_location(Cleared(Events.CLEAR_THE_FOG), world.player),
        entrance_type=EntranceType.TWO_WAY,
        related_events=[Events.CLEAR_THE_FOG],
    )
    connect(
        Sections.FOREST_OF_ALL_BEGINNING_PART_1.name,
        Sections.FOREST_OF_ALL_BEGINNING_PART_2.name,
        entrance_type=EntranceType.TWO_WAY,
    )
    connect(
        Sections.GARAGE.name,
        Sections.MOTOCROSS_COURSE.name,
        rule=Has(Items.FUEL_BAR),
        entrance_type=EntranceType.ONE_WAY,
    )
    connect(
        Sections.MOTOCROSS_COURSE.name, Sections.THE_MERMAIDS_SINGING_BEACH.name, entrance_type=EntranceType.ONE_WAY
    )
    connect(
        Sections.THE_MERMAIDS_SINGING_BEACH.name,
        Sections.THE_MERMAIDS_SINGING_ROCK.name,
        entrance_type=EntranceType.TWO_WAY,
    )
    connect(
        Sections.FOREST_OF_100_FLOWERS_PART_1.name,
        Sections.FOREST_OF_100_FLOWERS_PART_2.name,
        entrance_type=EntranceType.TWO_WAY,
    )
    connect(
        Sections.CHARITY_SQUARE.name,
        Sections.HIDDEN_VILLAGE.name,
        rule=Has(Items.LEAF_BUTTERFLY, 29),
        entrance_type=EntranceType.ONE_WAY,
    )
    connect(
        Sections.CHARITY_SQUARE.name,
        Sections.LEAF_SLIDER.name,
        rule=lambda state: state.can_reach_location(Cleared(Events.LEAF_SLIDER), world.player),
        entrance_type=EntranceType.ONE_WAY,
        related_events=[Events.LEAF_SLIDER],
    )
    connect(
        Sections.LAVA_CAVES.name,
        Regions.LAVA_CAVES_PURIFIED,
        rule=lambda state: state.can_reach_location(Cleared(Events.LAVA_CAVES), world.player),
        entrance_type=EntranceType.TWO_WAY,
        related_events=[Events.LAVA_CAVES],
    )
    connect(Sections.HAUNTED_MANSION_SOUTH.name, Sections.HAUNTED_MANSION_WEST.name, entrance_type=EntranceType.TWO_WAY)
    connect(
        Sections.HAUNTED_MANSION_SOUTH.name,
        Sections.HAUNTED_MANSION_EAST.name,
        rule=lambda state: state.can_reach_location(Cleared(Events.A_DRINK_FOR_GROWNUPS), world.player),
        entrance_type=EntranceType.TWO_WAY,
        related_events=[Events.A_DRINK_FOR_GROWNUPS],
    )
    connect(Sections.HAUNTED_MANSION_EAST.name, Sections.HAUNTED_MANSION_NORTH.name, entrance_type=EntranceType.TWO_WAY)
    connect(
        Sections.HAUNTED_MANSION_WEST.name,
        Sections.HAUNTED_MANSION_NORTH.name,
        rule=lambda state: state.can_reach_location(Cleared(Events.A_DRINK_FOR_GROWNUPS), world.player),
        entrance_type=EntranceType.TWO_WAY,
        related_events=[Events.A_DRINK_FOR_GROWNUPS],
    )
    connect(
        Sections.LAKE.name,
        Sections.LAKE_LEFT_BANK.name,
        rule=lambda state: state.can_reach_location(Started(Events.I_CANT_SWIM), world.player),
        entrance_type=EntranceType.TWO_WAY,
        related_events=[Events.I_CANT_SWIM],
    )
    connect(Sections.HAUNTED_MANSION_NORTH.name, Sections.SUN_TORCH_STAND.name, entrance_type=EntranceType.TWO_WAY)
    connect(
        Sections.HAUNTED_MANSION_SOUTH.name,
        Sections.SUN_TORCH_STAND.name,
        rule=lambda state: state.can_reach_location(Cleared(Events.A_DRINK_FOR_GROWNUPS), world.player),
        entrance_type=EntranceType.TWO_WAY,
        related_events=[Events.A_DRINK_FOR_GROWNUPS],
    )
    connect(
        Sections.STORMY_MOUNTAINS_PART_2.name,
        Sections.BACCUS_VILLAGE.name,
        entrance_type=EntranceType.ONE_WAY,
    )
    connect(
        Sections.BACCUS_LAKE.name,
        Sections.BACCUS_LAKE_PIER.name,
        entrance_type=EntranceType.TWO_WAY,
    )
    connect(
        Sections.PHOENIXS_NEST.name,
        Sections.MASAKARI_JUNGLE.name,
        rule=lambda state: state.can_reach_location(Cleared(Events.THE_MASTER_OF_THE_SKIES), world.player),
        entrance_type=EntranceType.ONE_WAY,
        related_events=[Events.THE_MASTER_OF_THE_SKIES],
    )
    connect(
        Sections.UNDERGROUND_MAZE.name,
        Regions.UNDERGROUND_MAZE_INNER,
        rule=lambda state: state.can_reach_location(Cleared(Events.THE_THIEFS_DOOR), world.player),
        entrance_type=EntranceType.TWO_WAY,
        related_events=[Events.THE_THIEFS_DOOR],
    )
    connect(
        Sections.CLOCK_TOWER_HALFWAY_UP.name, Sections.CLOCK_TOWER_ENGINE_ROOM.name, entrance_type=EntranceType.TWO_WAY
    )
    connect(Sections.IRON_CASTLE_ENTRANCE.name, Sections.IRON_CASTLE_MAIN_ROOM.name, entrance_type=EntranceType.TWO_WAY)
    connect(
        Sections.IRON_CASTLE_MAIN_ROOM.name,
        Sections.IRON_CASTLE_ENGINE_ROOM.name,
        entrance_type=EntranceType.TWO_WAY,
        rule=lambda state: state.can_reach_location(Cleared(Events.BREAK_THE_RUSTY_DOOR), world.player),
        related_events=[Events.BREAK_THE_RUSTY_DOOR],
    )

    connect(
        Sections.VILLAGE_OF_ALL_BEGINNING.name,
        Sections.HUNDREDS_YEAR_OLD_MANS_HUT.name,
        rule=Has(Items.HUNDRED_YEAR_OLD_BELL),
        suffix=" with Bell",
        entrance_type=EntranceType.ONE_WAY,
    )
    connect(
        Sections.VILLAGE_OF_ALL_BEGINNING.name,
        Sections.THOUSAND_YEAR_OLD_MANS_ROOM.name,
        rule=Has(Items.THOUSAND_YEAR_OLD_BELL),
        suffix=" with Bell",
        entrance_type=EntranceType.ONE_WAY,
    )
    connect(
        Sections.VILLAGE_OF_ALL_BEGINNING.name,
        Sections.TEN_THOUSAND_YEAR_OLD_MANS_ROOM.name,
        rule=Has(Items.TEN_THOUSAND_YEAR_OLD_BELL),
        suffix=" with Bell",
        entrance_type=EntranceType.ONE_WAY,
    )
    connect(
        Sections.VILLAGE_OF_ALL_BEGINNING.name,
        Sections.MILLION_YEAR_OLD_MANS_ROOM.name,
        rule=Has(Items.MILLION_YEAR_OLD_BELL),
        suffix=" with Bell",
        entrance_type=EntranceType.ONE_WAY,
    )
