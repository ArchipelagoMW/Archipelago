from __future__ import annotations

from dataclasses import dataclass

from .constants import Regions, Events


@dataclass
class EventData:
    id: int
    name: str
    started_region: str  # Region that needs to be accessible to start this
    cleared_region: str  # Region that needs to be accessible to complete this

    def __init__(self, id, name: str, started_region: str, cleared_region: str | None = None):
        self.id = id
        self.name = name
        self.started_region = started_region
        self.cleared_region = cleared_region if cleared_region is not None else started_region

    def __repr__(self) -> str:
        return self.name


class EventHandler:
    event_table: list[EventData] = [
        # EventData(0x00, Events.GRANDPAS_BRACELET, Regions.VILLAGE_OF_ALL_BEGINNINGS, Regions.THE_STRANGE_SMALL_ROOM),
        EventData(0x01, Events.THE_100_YEAR_OLD_WISE_MAN, Regions.FOREST_OF_ALL_BEGINNINGS),
        EventData(0x02, Events.CLEAR_THE_FOG, Regions.VILLAGE_OF_ALL_BEGINNINGS),
        EventData(0x03, Events.TAKE_ME_HOME, Regions.VILLAGE_OF_ALL_BEGINNINGS, Regions.OL_POND),
        # EventData(0x04, Events.MOTOCROSS_COURSE, Regions.),
        EventData(0x05, Events.WHO_ARE_YOU, Regions.FOREST_OF_ALL_BEGINNINGS),
        # EventData(0x06, Events., Regions.), # Unused
        EventData(0x07, Events.HIDE_AND_GO_SEEK, Regions.FOREST_OF_ALL_BEGINNINGS),
        EventData(0x08, Events.I_CANT_SWIM, Regions.OL_POND),
        EventData(
            0x09, Events.INSIDE_THE_KOKKA_EGGS, Regions.VILLAGE_OF_ALL_BEGINNINGS, Regions.FOREST_OF_ALL_BEGINNINGS
        ),
        # EventData(0x0A, Events.TALE_OF_THE_EVIL_PIGS, Regions.),
        # EventData(0x0B, Events.THE_1000_YEAR_OLD_MAN, Regions.),
        EventData(0x0C, Events.DWARF_ELDER, Regions.FOREST_OF_ALL_BEGINNINGS, Regions.WOBBLY_WHARF),
        EventData(0x0D, Events.BEGINNERS_DWARF_LANGUAGE, Regions.FOREST_OF_100_FLOWERS, Regions.DWARF_VILLAGE),
        EventData(0x0E, Events.A_LOST_CHILD, Regions.DWARF_VILLAGE, Regions.WATCH_TOWER),
        # EventData(0x0F, Events.FLOWER_SEEDS, Regions.),
        EventData(0x10, Events.THE_AP_BOX, Regions.FOREST_OF_ALL_BEGINNINGS),
        EventData(0x11, Events.SAVE_THE_DWARVES, Regions.DWARF_VILLAGE),
        # EventData(0x12, Events., Regions.), # Unused
        EventData(0x13, Events.LOST_AND_FOUND, Regions.WATCH_TOWER),
        # EventData(0x14, Events.STOP_THE_FIGHT, Regions.),
        # EventData(0x15, Events.THE_GREAT_ESCAPE, Regions.),
        EventData(0x16, Events.LOOK_AND_SEE, Regions.WATCH_TOWER),
        EventData(0x17, Events.A_MANS_BEST_FRIEND, Regions.WOBBLY_WHARF),
        EventData(0x18, Events.WHAT_IS_THIS, Regions.WATCH_TOWER),
        # EventData(0x19, Events.TREASURES_FROM_THE_MANSION, Regions.),
        EventData(0x1A, Events.TO_PHOENIX_MOUNTAIN, Regions.WOBBLY_WHARF),
        # EventData(0x1B, Events.THE_BROKEN_FOUNTAIN, Regions.),
        # EventData(0x1C, Events.A_FAMILIAR_LOOKING_MANSION, Regions.),
        # EventData(0x1D, Events.A_STORMY_PIG_BAG, Regions.),
        # EventData(0x1E, Events.PHOENIX_MOUNTAIN, Regions.),
        # EventData(0x1F, Events.WHERE_DID_I_COME_FROM, Regions.),
        # EventData(0x20, Events., Regions.), # Unused
        # EventData(0x21, Events.THE_FAMOUS_DIGGER, Regions.),
        # EventData(0x22, Events.LAVA_CAVES, Regions.),
        # EventData(0x23, Events.THE_MASTER_OF_THE_SKIES, Regions.),
        # EventData(0x24, Events.WHATS_A_FUNGA, Regions.),
        EventData(0x25, Events.MONSTER_HUNT, Regions.MUSHROOM_FOREST),
        # EventData(0x26, Events.DEATH_FRUIT_JUICE, Regions.),
        # EventData(0x27, Events.PLANT_A_FLOWER_GARDEN, Regions.),
        # EventData(0x28, Events.TEARS_FROM_A_FLOWER, Regions.),
        # EventData(0x29, Events.SMILE, Regions.),
        # EventData(0x2A, Events.CRY_BABY, Regions.),
        # EventData(0x2B, Events.CANT_STOP_CRYING, Regions.),
        # EventData(0x2C, Events.THE_RED_FORTUNE_TELLER, Regions.),
        # EventData(0x2D, Events., Regions.), # Unused
        # EventData(0x2E, Events.WHERES_THE_BABY_MOUSE, Regions.),
        # EventData(0x2F, Events.SOME_CHEESE_PLEASE, Regions.),
        # EventData(0x30, Events., Regions.), # Unused
        # EventData(0x31, Events.A_DRINK_FOR_GROWNUPS, Regions.),
        # EventData(0x32, Events.ROAD_TO_BACCUS_LAKE, Regions.),
        # EventData(0x33, Events.A_SMALL_KEY_HOLE, Regions.),
        # EventData(0x34, Events., Regions.), # Unused
        # EventData(0x35, Events.THE_MOUSE_PIG_BAG, Regions.),
        # EventData(0x36, Events.THE_HAUNTED_MANSION, Regions.),
        # EventData(0x37, Events.A_LARGE_KEY_HOLE, Regions.),
        # EventData(0x38, Events.PAINTING_OF_A_BIG_KEY, Regions.),
        # EventData(0x39, Events.BREAK_THE_MAGIC_EGG, Regions.),
        # EventData(0x3A, Events.RED_HIDDEN_POWERS, Regions.),
        # EventData(0x3B, Events., Regions.), # Unused
        # EventData(0x3C, Events., Regions.), # Unused
        # EventData(0x3D, Events., Regions.), # Unused
        # EventData(0x3E, Events.TREE_OF_KNOWLEDGE_KNOWS, Regions.),
        # EventData(0x3F, Events.THE_PUMPS_ROCKS, Regions.),
        # EventData(0x40, Events.A_REFRESHING_DRING, Regions.),
        # EventData(0x41, Events.I_NEED_A_TEAR_BOTTLE, Regions.),
        # EventData(0x42, Events., Regions.), # Unused
        # EventData(0x43, Events., Regions.), # Unused
        # EventData(0x44, Events., Regions.), # Unused
        # EventData(0x45, Events., Regions.), # Unused
        # EventData(0x46, Events., Regions.), # Unused
        # EventData(0x47, Events., Regions.), # Unused
        # EventData(0x48, Events., Regions.), # Unused
        # EventData(0x49, Events.WE_NEED_POWER, Regions.),
        # EventData(0x4A, Events., Regions.), # Unused
        # EventData(0x4B, Events., Regions.), # Unused
        # EventData(0x4C, Events., Regions.), # Unused
        # EventData(0x4D, Events.THE_CIVILIZATION_MACHINE, Regions.),
        # EventData(0x4E, Events.FIND_CHARLES, Regions.),
        # EventData(0x4F, Events.WHATS_UNDER_THE_FOREST, Regions.),
        EventData(0x50, Events.THE_100_FLOWER_FOREST, Regions.WOBBLY_WHARF),
        # EventData(0x51, Events.THE_BOSS_TREASURE, Regions.),
        # EventData(0x52, Events.IM_SO_HUNGRY, Regions.),
        # EventData(0x53, Events., Regions.), # Unused
        # EventData(0x54, Events., Regions.), # Unused
        # EventData(0x55, Events.THE_DEEP_JUNGLE_PIG, Regions.),
        EventData(0x56, Events.HEALING_HERBS_FOR_BARON, Regions.WOBBLY_WHARF),
        # EventData(0x57, Events.DELICIOUS_KNOWLEDGE_FRUIT, Regions.),
        # EventData(0x58, Events.SEAWEED_FOR_YOUR_HEALTH, Regions.),
        # EventData(0x59, Events.BLUE_HIDDEN_POWERS, Regions.),
        # EventData(0x5A, Events., Regions.), # Unused
        # EventData(0x5B, Events., Regions.), # Unused
        # EventData(0x5C, Events., Regions.), # Unused
        # EventData(0x5D, Events., Regions.), # Unused
        # EventData(0x5E, Events., Regions.), # Unused
        # EventData(0x5F, Events., Regions.), # Unused
        # EventData(0x60, Events., Regions.), # Unused
        # EventData(0x61, Events., Regions.), # Unused
        # EventData(0x62, Events., Regions.), # Unused
        # EventData(0x63, Events., Regions.), # Unused
        # EventData(0x64, Events., Regions.), # Unused
        # EventData(0x65, Events., Regions.), # Unused
        # EventData(0x66, Events.BREAK_THE_RUSTY_DOOR, Regions.),
        # EventData(0x67, Events.THE_CUTE_WITCH, Regions.),
        # EventData(0x68, Events.FOOD_FOR_FUEL, Regions.),
        # EventData(0x69, Events.I_NEED_A_BOMB, Regions.),
        # EventData(0x6A, Events., Regions.), # Unused
        # EventData(0x6B, Events., Regions.), # Unused
        # EventData(0x6C, Events., Regions.), # Unused
        # EventData(0x6D, Events., Regions.), # Unused
        # EventData(0x6E, Events., Regions.), # Unused
        # EventData(0x6F, Events.BACCUS_VILLAGE, Regions.),
        # EventData(0x70, Events.THE_MERMAIDS_NECKLACE, Regions.),
        # EventData(0x71, Events.BARONS_STRENGTH, Regions.),
        # EventData(0x72, Events.WHAT_THE_WITCH_LOST, Regions.),
        # EventData(0x73, Events.A_SAFE_MUSHROOM, Regions.),
        # EventData(0x74, Events.POWER_UP_FOR_TOOLS, Regions.),
        # EventData(0x75, Events., Regions.), # Unused
        # EventData(0x76, Events.THE_10000_YEAR_OLD_MAN, Regions.),
        # EventData(0x77, Events.MIGHTY_FISH_FOOD, Regions.),
        # EventData(0x78, Events.LETS_MAKE_CANDY, Regions.),
        # EventData(0x79, Events.THE_MERMAIDS_SINGING_ROCK, Regions.),
        # EventData(0x7A, Events., Regions.), # Unused
        # EventData(0x7B, Events.THE_UNDERWATER_PIG_BAG, Regions.),
        # EventData(0x7C, Events.TRICK_VILLAGE, Regions.),
        # EventData(0x7D, Events.THE_THIEFS_DOOR, Regions.),
        # EventData(0x7E, Events.THE_10_MATH_BEADS, Regions.),
        # EventData(0x7F, Events.THE_5_GOLDEN_ITEMS, Regions.),
        # EventData(0x80, Events.UNBREAKABLE_WIRE, Regions.),
        # EventData(0x81, Events.GREEN_HIDDEN_POWERS, Regions.),
        # EventData(0x82, Events., Regions.), # Unused
        # EventData(0x83, Events., Regions.), # Unused
        # EventData(0x84, Events.TAKE_TWO_OF_THESE, Regions.),
        # EventData(0x85, Events.I_WANT_A_BRONZE_MEDAL, Regions.),
        # EventData(0x86, Events.I_WANT_A_SILVER_MEDAL, Regions.),
        # EventData(0x87, Events.I_WANT_A_GOLD_MEDAL, Regions.),
        # EventData(0x88, Events., Regions.), # Unused
        # EventData(0x89, Events., Regions.), # Unused
        # EventData(0x8A, Events., Regions.), # Unused
        # EventData(0x8B, Events., Regions.), # Unused
        # EventData(0x8C, Events., Regions.), # Unused
        # EventData(0x8D, Events., Regions.), # Unused
        # EventData(0x8E, Events., Regions.), # Unused
        # EventData(0x8F, Events., Regions.), # Unused
        # EventData(0x90, Events.MILLION_YEAR_OLD_WISH, Regions.),
        # EventData(0x91, Events.DIG_LIKE_A_MOLE, Regions.),
        # EventData(0x92, Events.THE_BLUE_FORTUNE_TELLER, Regions.),
        # EventData(0x93, Events., Regions.), # Unused
        # EventData(0x94, Events., Regions.), # Unused
        # EventData(0x95, Events., Regions.), # Unused
        # EventData(0x96, Events.LETS_RIDE_THE_RAFT, Regions.),
        # EventData(0x97, Events.TAKE_OUT, Regions.),
        # EventData(0x98, Events., Regions.), # Unused
        # EventData(0x99, Events.WHATS_UNDERWATER, Regions.),
        # EventData(0x9A, Events., Regions.), # Unused
        # EventData(0x9B, Events., Regions.), # Unused
        # EventData(0x9C, Events.SOURCE_OF_EVIL_MAGIC, Regions.),
        # EventData(0x9D, Events.SEVEN_FRIENDS, Regions.),
        # EventData(0x9E, Events., Regions.), # Unused
        # EventData(0x9F, Events.THE_8TH_EVIL_PIG_BAG, Regions.),
        # EventData(0xA0, Events.A_REAL_EVIL_PIG, Regions.),
        # EventData(0xA1, Events.UNDERGROUND_TREASURE, Regions.),
        # EventData(0xA2, Events., Regions.), # Unused
        # EventData(0xA3, Events., Regions.), # Unused
        # EventData(0xA4, Events.THE_FLOWER_TOWER, Regions.),
        # EventData(0xA5, Events., Regions.), # Unused
        EventData(0xA6, Events.A_HUNGRY_MONKEY, Regions.VILLAGE_OF_ALL_BEGINNINGS),
        EventData(0xA7, Events.PEACH_FLOWER_GAS, Regions.VILLAGE_OF_ALL_BEGINNINGS),
        EventData(0xA8, Events.THE_EVIL_PIG_BAG, Regions.WOBBLY_WHARF),
        EventData(0xA9, Events.BITTING_PLANT_FLOWER, Regions.FOREST_OF_ALL_BEGINNINGS),
        # EventData(0xAA, Events.WHEN_THE_WIND_DIES_DOWN, Regions.),
        # EventData(0xAB, Events.THE_PHOENIXS_FAVORITE, Regions.),
        # EventData(0xAC, Events.THE_FIRE_PIG_BAG, Regions.),
        # EventData(0xAD, Events.CHARLES_PANTS, Regions.),
        # EventData(0xAE, Events.THE_HAUNTED_PIG_BAG, Regions.),
        EventData(0xAF, Events.THE_WORLDS_GREATEST_SMILE, Regions.MUSHROOM_FOREST),
        EventData(0xB0, Events.THE_WORLDS_GREATEST_POUT, Regions.MUSHROOM_FOREST),
        EventData(0xB1, Events.SOMETHINGS_COOKIN, Regions.WOBBLY_WHARF),
        # EventData(0xB2, Events.LEAF_BUTTERFLIES, Regions.),
        EventData(0xB3, Events.WHERED_THE_LIGHTS_GO, Regions.DWARF_JAIL),
        EventData(0xB4, Events.WHERE_THE_BARREL_ROLLS, Regions.WOBBLY_WHARF),
        # EventData(0xB5, Events.READY_SET_GO, Regions.),
        EventData(0xB6, Events.A_MAGIC_MIRROR, Regions.WATCH_TOWER),
        # EventData(0xB7, Events.THE_JUNGLE_PIG_BAG, Regions.),
        # EventData(0xB8, Events., Regions.), # Unused
        # EventData(0xB9, Events.A_PRECIOUS_TREASURE_CHEST, Regions.),
        # EventData(0xBA, Events., Regions.), # Unused
        # EventData(0xBB, Events.THE_MYSTERIOUS_MUSHROOM, Regions.),
        # EventData(0xBC, Events.LEAF_SLIDER, Regions.),
        # EventData(0xBD, Events.RED_BLUE, Regions.),
        # EventData(0xBE, Events.THE_TROUBLED_THIEF, Regions.),
        # EventData(0xBF, Events.WHAT_THE_THIEF_FORGOT, Regions.),
    ]

    by_name = {}

    for index, event in enumerate(event_table):
        by_name[event.name] = event


def Started(event_name: str):
    return f"{event_name} Started"


def Cleared(event_name: str):
    return f"{event_name} Cleared"
