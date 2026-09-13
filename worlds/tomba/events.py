from __future__ import annotations

from dataclasses import dataclass
from rule_builder.rules import Has, Rule, CanReachRegion

from .helpers import HasStarted, HasCleared, Rules
from .constants import Regions, Events, Items, Locations
from .sections import Sections


@dataclass
class EventData:
    id: int
    name: str
    region: str
    started_rule: Rule  # Check to start the event
    cleared_rule: Rule  # Check to clear the event

    def __init__(self, id, name: str, region: str, started_rule: Rule | None = None, cleared_rule: Rule | None = None):
        self.id = id
        self.name = name
        self.region = region

        if started_rule is None:
            started_rule = CanReachRegion(self.region)

        if cleared_rule is None:
            cleared_rule = CanReachRegion(self.region)

        self.started_rule = started_rule
        self.cleared_rule = HasStarted(name) & cleared_rule

    def __repr__(self) -> str:
        return self.name


class EventHandler:
    event_table: list[EventData] = [
        # EventData(
        #     0x00,
        #     Events.GRANDPAS_BRACELET,
        #     Regions.VILLAGE_OF_ALL_BEGINNINGS,
        #     cleared_rule=CanReachRegion(Regions.THE_STRANGE_SMALL_ROOM) & HasCleared(Events.SEVEN_FRIENDS),
        # ),
        EventData(
            0x01,
            Events.THE_100_YEAR_OLD_WISE_MAN,
            Regions.VILLAGE_OF_ALL_BEGINNINGS,
            cleared_rule=CanReachRegion(Regions.FOREST_OF_ALL_BEGINNINGS),
        ),
        EventData(
            0x02, Events.CLEAR_THE_FOG, Regions.VILLAGE_OF_ALL_BEGINNINGS, cleared_rule=Has(Items.FURIOUS_TORNADO)
        ),
        EventData(0x03, Events.TAKE_ME_HOME, Regions.OL_POND, started_rule=Rules.CAN_BREAK_STUFF),
        EventData(
            0x04,
            Events.MOTOCROSS_COURSE,
            Regions.GARAGE,
        ),
        EventData(
            0x05,
            Events.WHO_ARE_YOU,
            Regions.FOREST_OF_ALL_BEGINNINGS,
            cleared_rule=HasCleared(Events.THE_100_YEAR_OLD_WISE_MAN),
        ),
        # EventData(0x06, Events., Regions.), # Unused
        EventData(
            0x07,
            Events.HIDE_AND_GO_SEEK,
            Regions.FOREST_OF_ALL_BEGINNINGS,
            started_rule=HasCleared(Events.WHO_ARE_YOU),
            cleared_rule=CanReachRegion(Regions.HIDDEN_VILLAGE) & Has(Items.JEWEL_OF_FIRE),
        ),
        EventData(
            0x08,
            Events.I_CANT_SWIM,
            Regions.OL_POND,
            cleared_rule=CanReachRegion(Regions.MASAKARI_JUNGLE) & HasCleared(Events.A_REFRESHING_DRINK),
        ),
        EventData(
            0x09, Events.INSIDE_THE_KOKKA_EGGS, Regions.FOREST_OF_ALL_BEGINNINGS, cleared_rule=Has(Items.CHICK, 4)
        ),
        EventData(
            0x0A,
            Events.TALE_OF_THE_EVIL_PIGS,
            Regions.FOREST_OF_ALL_BEGINNINGS,
            started_rule=HasCleared(Events.INSIDE_THE_KOKKA_EGGS),
        ),
        EventData(
            0x0B,
            Events.THE_1000_YEAR_OLD_MAN,
            Regions.BACCUS_VILLAGE,
            started_rule=HasCleared(Events.A_DRINK_FOR_GROWNUPS),
        ),
        EventData(
            0x0C,
            Events.DWARF_ELDER,
            Regions.DWARF_VILLAGE,
            started_rule=CanReachRegion(Regions.FOREST_OF_ALL_BEGINNINGS),
        ),
        EventData(0x0D, Events.BEGINNERS_DWARF_LANGUAGE, Regions.DWARF_VILLAGE),
        EventData(0x0E, Events.A_LOST_CHILD, Regions.DWARF_VILLAGE),
        EventData(
            0x0F,
            Events.FLOWER_SEEDS,
            Regions.DWARF_VILLAGE,
            started_rule=HasCleared(Events.A_LOST_CHILD) & HasCleared(Events.DEATH_FRUIT_JUICE),
            cleared_rule=Has(Items.FLOWER_SEEDS) & CanReachRegion(Regions.DWARF_VILLAGE),
        ),
        EventData(0x10, Events.THE_AP_BOX, Regions.FOREST_OF_ALL_BEGINNINGS),
        EventData(
            0x11,
            Events.SAVE_THE_DWARVES,
            Regions.DWARF_VILLAGE,
            started_rule=HasCleared(Events.BEGINNERS_DWARF_LANGUAGE),
        ),
        # EventData(0x12, Events., Regions.), # Unused
        EventData(
            0x13,
            Events.LOST_AND_FOUND,
            Regions.FOREST_OF_100_FLOWERS,
            started_rule=HasStarted(Events.SAVE_THE_DWARVES),
            cleared_rule=CanReachRegion(Regions.CHARITY_SQUARE),
        ),
        EventData(
            0x14,
            Events.STOP_THE_FIGHT,
            Regions.DWARF_VILLAGE,
            started_rule=HasCleared(Events.WHERED_THE_LIGHTS_GO),
        ),
        EventData(0x15, Events.THE_GREAT_ESCAPE, Regions.DWARF_VILLAGE, started_rule=HasCleared(Events.STOP_THE_FIGHT)),
        EventData(0x16, Events.LOOK_AND_SEE, Regions.WATCH_TOWER, cleared_rule=Has(Items.TELESCOPE)),
        EventData(
            0x17,
            Events.A_MANS_BEST_FRIEND,
            Regions.DWARF_VILLAGE,
            started_rule=HasStarted(Events.SAVE_THE_DWARVES),
            cleared_rule=HasCleared(Events.DELICIOUS_KNOWLEDGE_FRUIT) & HasCleared(Events.HEALING_HERBS_FOR_BARON),
        ),
        EventData(0x18, Events.WHAT_IS_THIS, Regions.WATCH_TOWER, cleared_rule=HasCleared(Events.WE_NEED_POWER)),
        EventData(
            0x19, Events.TREASURES_FROM_THE_MANSION, Regions.MANSION, started_rule=HasStarted(Events.THE_GREAT_ESCAPE)
        ),
        EventData(
            0x1A,
            Events.TO_PHOENIX_MOUNTAIN,
            Regions.DWARF_VILLAGE,
            started_rule=HasCleared(Events.SAVE_THE_DWARVES),
            cleared_rule=HasCleared(Events.THE_WORLDS_GREATEST_POUT),
        ),
        EventData(
            0x1B,
            Events.THE_BROKEN_FOUNTAIN,
            Regions.CHARITY_SQUARE,
            cleared_rule=HasCleared(Events.THE_100_FLOWER_FOREST) & Has(Items.FLOWER_TEARS),
        ),
        EventData(0x1C, Events.A_FAMILIAR_LOOKING_MANSION, Regions.MANSION),
        EventData(
            0x1D,
            Events.A_STORMY_PIG_BAG,
            Regions.STORMY_MOUNTAIN,
            cleared_rule=Has(Items.BIG_KEY) & CanReachRegion(Regions.STORMY_MOUNTAIN),
        ),
        EventData(
            0x1E,
            Events.PHOENIX_MOUNTAIN,
            Regions.STORMY_MOUNTAIN,
            started_rule=Has(Items.RED_EVIL_PIG_BAG),
            cleared_rule=CanReachRegion(Regions.CHARITY_SQUARE) & Rules.CAN_BIG_JUMP,
        ),
        EventData(0x1F, Events.WHERE_DID_I_COME_FROM, Regions.STORMY_MOUNTAIN),
        # EventData(0x20, Events., Regions.), # Unused
        EventData(
            0x21, Events.THE_FAMOUS_DIGGER, Regions.STORMY_MOUNTAIN, cleared_rule=HasCleared(Events.PHOENIX_MOUNTAIN)
        ),
        EventData(
            0x22,
            Events.LAVA_CAVES,
            Regions.LAVA_CAVES,
            cleared_rule=Has(Items.GREEN_EVIL_PIG_BAG) & CanReachRegion(Sections.LAUGHING_ROOM.name),
        ),
        EventData(
            0x23,
            Events.THE_MASTER_OF_THE_SKIES,
            Regions.STORMY_MOUNTAIN,
            cleared_rule=Has(Items.BUNK_FLOWER, 5) & CanReachRegion(Regions.PHOENIXS_NEST),
        ),
        EventData(
            0x24,
            Events.WHATS_A_FUNGA,
            Regions.STORMY_MOUNTAIN,
            started_rule=HasCleared(Events.PHOENIX_MOUNTAIN),
            cleared_rule=Has(Items.FUNGA_DRUM) & CanReachRegion(Regions.STORMY_MOUNTAIN),
        ),
        EventData(0x25, Events.MONSTER_HUNT, Regions.MUSHROOM_FOREST),
        EventData(0x26, Events.DEATH_FRUIT_JUICE, Regions.BACCUS_VILLAGE, cleared_rule=Has(Items.WEED_KILLER)),
        EventData(
            0x27,
            Events.PLANT_A_FLOWER_GARDEN,
            Regions.DWARF_VILLAGE,
            started_rule=Has(Items.FLOWER_SEEDS),
            cleared_rule=HasCleared(Events.THE_100_FLOWER_FOREST),
        ),  # TODO: Check this one, only 97.000 AP required or evil pig dead too ?
        EventData(
            0x28,
            Events.TEARS_FROM_A_FLOWER,
            Regions.MUSHROOM_FOREST,
            cleared_rule=Has(Items.RISE_AND_SHINE_POWDER) & Has(Items.TEAR_JAR),
        ),
        EventData(
            0x29,
            Events.SMILE,
            Regions.STORMY_MOUNTAIN,
            started_rule=CanReachRegion(Sections.MUSHROOM_FOREST.name)
            & (
                CanReachRegion(Sections.STORMY_MOUNTAINS_PART_1.name)
                | CanReachRegion(Sections.HAUNTED_MANSION_NORTH.name)
            ),
        ),
        EventData(0x2A, Events.CRY_BABY, Sections.HAUNTED_MANSION_WEST.name),
        EventData(
            0x2B,
            Events.CANT_STOP_CRYING,
            Regions.BACCUS_VILLAGE,
            started_rule=HasCleared(Events.WHERES_THE_BABY_MOUSE),
            cleared_rule=CanReachRegion(Regions.MUSHROOM_FOREST),
        ),
        EventData(
            0x2C,
            Events.THE_RED_FORTUNE_TELLER,
            Regions.BACCUS_VILLAGE,
            cleared_rule=HasCleared(Events.A_DRINK_FOR_GROWNUPS),
        ),
        # EventData(0x2D, Events., Regions.), # Unused
        EventData(0x2E, Events.WHERES_THE_BABY_MOUSE, Regions.CENTRAL_PARK),
        EventData(0x2F, Events.SOME_CHEESE_PLEASE, Regions.BACCUS_VILLAGE, cleared_rule=Has(Items.CHEESE, 10)),
        # EventData(0x30, Events., Regions.), # Unused
        EventData(
            0x31,
            Events.A_DRINK_FOR_GROWNUPS,
            Regions.CENTRAL_PARK,
            started_rule=HasCleared(Events.WHERES_THE_BABY_MOUSE),
            cleared_rule=HasCleared(Events.ROAD_TO_BACCUS_LAKE),  # Event can be completed without the Pipe
        ),
        EventData(
            0x32,
            Events.ROAD_TO_BACCUS_LAKE,
            Regions.BACCUS_VILLAGE,
            cleared_rule=HasStarted(Events.A_DRINK_FOR_GROWNUPS) & HasCleared(Events.WHERES_THE_BABY_MOUSE),
        ),
        EventData(
            0x33, Events.A_SMALL_KEY_HOLE, Sections.HAUNTED_MANSION_NORTH.name, cleared_rule=Has(Items.SMALL_KEY)
        ),
        # EventData(0x34, Events., Regions.), # Unused
        EventData(
            0x35, Events.THE_MOUSE_PIG_BAG, Regions.BACCUS_VILLAGE, cleared_rule=Has(Items.THOUSAND_YEAR_OLD_KEY)
        ),
        EventData(
            0x36,
            Events.THE_HAUNTED_MANSION,
            Sections.HAUNTED_MANSION_SOUTH.name,
            cleared_rule=Has(Items.PINK_EVIL_PIG_BAG) & HasCleared(Events.LAVA_CAVES),
        ),
        EventData(0x37, Events.A_LARGE_KEY_HOLE, Regions.STORMY_MOUNTAIN, cleared_rule=Has(Items.BIG_KEY)),
        EventData(
            0x38,
            Events.PAINTING_OF_A_BIG_KEY,
            Sections.THIEFS_ROOM_THREE.name,
            cleared_rule=Has(Items.LARGE_KEY_PANEL_1)
            & Has(Items.LARGE_KEY_PANEL_2)
            & Has(Items.LARGE_KEY_PANEL_3)
            & Has(Items.LARGE_KEY_PANEL_4)
            & Has(Items.LARGE_KEY_PANEL_5),
        ),
        EventData(
            0x39,
            Events.BREAK_THE_MAGIC_EGG,
            Sections.THOUSAND_YEAR_OLD_MANS_ROOM.name,
            cleared_rule=Has(Items.SMALL_KEY),
        ),
        EventData(0x3A, Events.RED_HIDDEN_POWERS, Sections.SUN_TORCH_STAND.name),
        # EventData(0x3B, Events., Regions.), # Unused
        # EventData(0x3C, Events., Regions.), # Unused
        # EventData(0x3D, Events., Regions.), # Unused
        EventData(
            0x3E,
            Events.TREE_OF_KNOWLEDGE_KNOWS,
            Regions.OLD_TREE_HILL,
            cleared_rule=HasStarted(Events.THE_5_GOLDEN_ITEMS),
        ),
        EventData(0x3F, Events.THE_PUMPS_ROCK, Regions.OLD_TREE_HILL),
        EventData(0x40, Events.A_REFRESHING_DRINK, Regions.MASAKARI_JUNGLE, cleared_rule=Has(Items.BANANA_JUICE)),
        EventData(
            0x41,
            Events.I_NEED_A_TEAR_BOTTLE,
            Regions.LUMBERJACK_FACTORY,
            started_rule=CanReachRegion(Regions.LUMBERJACK_FACTORY),
            cleared_rule=HasCleared(Events.THE_100_FLOWER_FOREST),
        ),
        # EventData(0x42, Events., Regions.), # Unused
        # EventData(0x43, Events., Regions.), # Unused
        # EventData(0x44, Events., Regions.), # Unused
        # EventData(0x45, Events., Regions.), # Unused
        # EventData(0x46, Events., Regions.), # Unused
        # EventData(0x47, Events., Regions.), # Unused
        # EventData(0x48, Events., Regions.), # Unused
        EventData(
            0x49,
            Events.WE_NEED_POWER,
            Regions.CLOCK_TOWER_ENGINE_ROOM,
            started_rule=CanReachRegion(Regions.CLOCK_TOWER_ENGINE_ROOM) & HasCleared(Events.A_REFRESHING_DRINK),
            cleared_rule=Has(Items.BOMB) & CanReachRegion(Regions.IRON_CASTLE_ENTRANCE),
        ),
        # EventData(0x4A, Events., Regions.), # Unused
        # EventData(0x4B, Events., Regions.), # Unused
        # EventData(0x4C, Events., Regions.), # Unused
        EventData(
            0x4D,
            Events.THE_CIVILIZATION_MACHINE,
            Regions.IRON_CASTLE_ENTRANCE,
            started_rule=HasCleared(Events.WE_NEED_POWER),
        ),
        EventData(0x4E, Events.FIND_CHARLES, Regions.MASAKARI_JUNGLE, cleared_rule=Has(Items.MINERS_HAT)),
        EventData(
            0x4F,
            Events.WHATS_UNDER_THE_FOREST,
            Regions.LUMBERJACK_FACTORY,
            started_rule=HasCleared(Events.WE_NEED_POWER),
        ),
        EventData(
            0x50,
            Events.THE_100_FLOWER_FOREST,
            Regions.FOREST_OF_100_FLOWERS,
            started_rule=HasCleared(Events.SAVE_THE_DWARVES),
            cleared_rule=CanReachRegion(Regions.MILLION_YEAR_OLD_MANS_ROOM) & Has(Items.BLUE_EVIL_PIG_BAG),
        ),
        EventData(
            0x51,
            Events.THE_BOSS_TREASURE,
            Sections.THIEFS_ROOM_ONE.name,
            started_rule=HasCleared(Events.THE_HAUNTED_MANSION) & HasCleared(Events.WHAT_THE_THIEF_FORGOT),
            cleared_rule=Has(Items.SMALL_KEY) & Has(Items.THOUSAND_YEAR_OLD_KEY),
        ),
        EventData(
            0x52,
            Events.IM_SO_HUNGRY,
            Regions.HIDDEN_VILLAGE,
            cleared_rule=Has(Items.LUNCH_BOX) | Has(Items.LARGE_LUNCH_BOX),
        ),
        # EventData(0x53, Events., Regions.), # Unused
        # EventData(0x54, Events., Regions.), # Unused
        EventData(
            0x55,
            Events.THE_DEEP_JUNGLE_PIG,
            Regions.OLD_TREE_HILL,
            started_rule=HasCleared(Events.THE_JUNGLE_PIG_BAG),
            cleared_rule=CanReachRegion(Regions.MANSION) & Has(Items.NAVY_EVIL_PIG_BAG),
        ),
        EventData(
            0x56,
            Events.HEALING_HERBS_FOR_BARON,
            Regions.WOBBLY_WHARF,
            started_rule=HasStarted(Events.SAVE_THE_DWARVES),
            cleared_rule=Has(Items.HEALING_HERBS) & CanReachRegion(Regions.DWARF_VILLAGE),
        ),
        EventData(
            0x57,
            Events.DELICIOUS_KNOWLEDGE_FRUIT,
            Regions.DWARF_VILLAGE,
            started_rule=Has(Items.HEALING_HERBS) & HasStarted(Events.A_MANS_BEST_FRIEND),
            cleared_rule=Has(Items.KNOWLEDGE_FRUIT),
        ),
        EventData(
            0x58,
            Events.SEAWEED_FOR_YOUR_HEALTH,
            Regions.DWARF_VILLAGE,
            started_rule=HasCleared(Events.A_MANS_BEST_FRIEND),
            cleared_rule=Has(Items.SEAWEED) & CanReachRegion(Regions.DWARF_VILLAGE),
        ),
        # EventData(0x59, Events., Regions.), # Unused
        EventData(
            0x5A, Events.BLUE_HIDDEN_POWERS, Regions.TRICK_VILLAGE, started_rule=HasCleared(Events.WHATS_UNDERWATER)
        ),
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
        EventData(
            0x66,
            Events.BREAK_THE_RUSTY_DOOR,
            Regions.IRON_CASTLE_ENTRANCE,
            started_rule=HasStarted(Events.WE_NEED_POWER),
            cleared_rule=Has(Items.BOMB),
        ),
        EventData(
            0x67,
            Events.THE_CUTE_WITCH,
            Regions.VILLAGE_OF_ALL_BEGINNINGS,
            started_rule=HasCleared(Events.WE_NEED_POWER),
        ),
        EventData(
            0x68,
            Events.FOOD_FOR_FUEL,
            Regions.LUMBERJACK_FACTORY,
            started_rule=HasCleared(Events.WE_NEED_POWER),
            cleared_rule=HasCleared(Events.THE_CIVILIZATION_MACHINE)
            & Has(Items.WINE)
            & CanReachRegion(Regions.LUMBERJACK_FACTORY),
        ),
        EventData(
            0x69,
            Events.I_NEED_A_BOMB,
            Regions.LUMBERJACK_FACTORY,
            started_rule=HasStarted(Events.WE_NEED_POWER),
            cleared_rule=Has(Items.BOMB) & CanReachRegion(Regions.LUMBERJACK_FACTORY),
        ),
        # EventData(0x6A, Events., Regions.), # Unused
        # EventData(0x6B, Events., Regions.), # Unused
        # EventData(0x6C, Events., Regions.), # Unused
        # EventData(0x6D, Events., Regions.), # Unused
        # EventData(0x6E, Events., Regions.), # Unused
        EventData(
            0x6F,
            Events.BACCUS_VILLAGE,
            Regions.BACCUS_VILLAGE,
            cleared_rule=Has(Items.ORANGE_EVIL_PIG_BAG) & CanReachRegion(Regions.CLOCK_TOWER_ENTRANCE),
        ),
        EventData(
            0x70,
            Events.THE_MERMAIDS_NECKLACE,
            Regions.TRICK_VILLAGE,
            started_rule=Has(Items.THOUSAND_YEAR_OLD_KEY),
            cleared_rule=Has(Items.SEASHELL_NECKLACE) & CanReachRegion(Sections.HIDING_ROOM.name),
        ),
        EventData(
            0x71,
            Events.BARONS_STRENGTH,
            Regions.DWARF_VILLAGE,
            started_rule=HasCleared(Events.A_MANS_BEST_FRIEND),
            cleared_rule=HasCleared(Events.SEAWEED_FOR_YOUR_HEALTH),
        ),
        EventData(
            0x72,
            Events.WHAT_THE_WITCH_LOST,
            Regions.WITCHS_HUT,
            cleared_rule=Has(Items.THREE_CRYSTAL_BALLS) & Has(Items.DIRTY_MIRROR),
        ),
        EventData(
            0x73,
            Events.A_SAFE_MUSHROOM,
            Regions.BACCUS_VILLAGE,
            started_rule=HasCleared(Events.BREAK_THE_MAGIC_EGG),
            cleared_rule=Has(Locations.AP_150_000),
        ),
        EventData(
            0x74,
            Events.POWER_UP_FOR_TOOLS,
            Regions.WITCHS_HUT,
            cleared_rule=Has(Items.GRAPPLE)
            & Has(Items.BLACKJACK)
            & Has(Items.THREE_CRYSTAL_BALLS)
            & Has(Items.DIRTY_MIRROR),
        ),
        # EventData(0x75, Events., Regions.), # Unused
        EventData(
            0x76,
            Events.THE_10000_YEAR_OLD_MAN,
            Regions.TRICK_VILLAGE,
            started_rule=HasCleared(Events.WE_NEED_POWER),
            cleared_rule=CanReachRegion(Regions.TRICK_VILLAGE),
        ),
        EventData(
            0x77,
            Events.MIGHTY_FISH_FOOD,
            Sections.HIDING_ROOM.name,
            started_rule=Has(Items.SEASHELL_NECKLACE) & HasCleared(Events.THE_10000_YEAR_OLD_MAN),
            cleared_rule=Has(Items.MIGHTY_FISH_FOOD)
            & (
                CanReachRegion(Regions.OL_POND)
                | CanReachRegion(Regions.MASAKARI_JUNGLE)
                | CanReachRegion(Regions.HIDING_ROOM)
            ),
        ),
        EventData(
            0x78,
            Events.LETS_MAKE_CANDY,
            Regions.WITCHS_HUT,
            cleared_rule=Has(Items.BITING_PLANT_FLOWER)
            & Has(Items.BUTAMUSHI_THORN)
            & Has(Items.KOKKA_CLAW)
            & Has(Items.MOLASSES)
            & Has(Items.NEEDLEGATOR_TEETH)
            & Has(Items.SILVER_POWDER),
        ),
        EventData(0x79, Events.THE_MERMAIDS_SINGING_ROCK, Regions.THE_MERMAIDS_SINGING_ROCK),
        # EventData(0x7A, Events., Regions.), # Unused
        EventData(
            0x7B,
            Events.THE_UNDERWATER_PIG_BAG,
            Regions.TRICK_VILLAGE,
            cleared_rule=Has(Items.TEN_THOUSAND_YEAR_OLD_KEY) & HasCleared(Events.WHATS_UNDERWATER),
        ),
        EventData(
            0x7C,
            Events.TRICK_VILLAGE,
            Regions.TRICK_VILLAGE,
            started_rule=HasCleared(Events.WHATS_UNDERWATER) & Has(Items.TEN_THOUSAND_YEAR_OLD_KEY),
            cleared_rule=Has(Items.YELLOW_EVIL_PIG_BAG) & CanReachRegion(Regions.CLOCK_TOWER_ENTRANCE),
        ),
        EventData(0x7D, Events.THE_THIEFS_DOOR, Sections.UNDERGROUND_MAZE.name, cleared_rule=Has(Items.THIEFS_WIRE)),
        EventData(
            0x7E,
            Events.THE_10_MATH_BEADS,
            Regions.TRICK_VILLAGE,
            cleared_rule=Has(Items.MATH_BEAD_1)
            & Has(Items.MATH_BEAD_2)
            & Has(Items.MATH_BEAD_3)
            & Has(Items.MATH_BEAD_4)
            & Has(Items.MATH_BEAD_5)
            & Has(Items.MATH_BEAD_6)
            & Has(Items.MATH_BEAD_7)
            & Has(Items.MATH_BEAD_8)
            & Has(Items.MATH_BEAD_9)
            & Has(Items.MATH_BEAD_10),
        ),
        EventData(
            0x7F,
            Events.THE_5_GOLDEN_ITEMS,
            Regions.TRICK_VILLAGE,
            started_rule=CanReachRegion(Regions.TRICK_VILLAGE)
            & Has(Items.MATH_BEAD_1)
            & Has(Items.MATH_BEAD_2)
            & Has(Items.MATH_BEAD_3)
            & Has(Items.MATH_BEAD_4)
            & Has(Items.MATH_BEAD_5)
            & Has(Items.MATH_BEAD_6)
            & Has(Items.MATH_BEAD_7)
            & Has(Items.MATH_BEAD_8)
            & Has(Items.MATH_BEAD_9)
            & Has(Items.MATH_BEAD_10),
            cleared_rule=Has(Items.GOLD_CANDY)
            & Has(Items.GOLD_FLOWER)
            & Has(Items.GOLD_MEDAL)
            & Has(Items.GOLDEN_LEAF_BUTTERFLY)
            & Has(Items.GOLDEN_FRUIT),
        ),
        EventData(
            0x80,
            Events.UNBREAKABLE_WIRE,
            Regions.UNDERGROUND_MAZE_INNER,
            cleared_rule=CanReachRegion(Sections.TRIBULATION_ROOM.name),
        ),
        EventData(
            0x81,
            Events.GREEN_HIDDEN_POWERS,
            Regions.PHOENIXS_NEST,
            started_rule=HasCleared(Events.THE_PHOENIXS_FAVORITE),
        ),
        # EventData(0x82, Events., Regions.), # Unused
        # EventData(0x83, Events., Regions.), # Unused
        EventData(
            0x84,
            Events.TAKE_TWO_OF_THESE,
            Regions.VILLAGE_OF_ALL_BEGINNINGS,
            started_rule=HasCleared(Events.POWER_UP_FOR_TOOLS),
            cleared_rule=Has(Items.COLD_MEDICINE),
        ),
        EventData(0x85, Events.I_WANT_A_BRONZE_MEDAL, Regions.THE_MERMAIDS_SINGING_ROCK),
        EventData(0x86, Events.I_WANT_A_SILVER_MEDAL, Regions.THE_MERMAIDS_SINGING_ROCK),
        EventData(0x87, Events.I_WANT_A_GOLD_MEDAL, Regions.THE_MERMAIDS_SINGING_ROCK),
        # EventData(0x88, Events., Regions.), # Unused
        # EventData(0x89, Events., Regions.), # Unused
        # EventData(0x8A, Events., Regions.), # Unused
        # EventData(0x8B, Events., Regions.), # Unused
        # EventData(0x8C, Events., Regions.), # Unused
        # EventData(0x8D, Events., Regions.), # Unused
        # EventData(0x8E, Events., Regions.), # Unused
        # EventData(0x8F, Events., Regions.), # Unused
        EventData(
            0x90,
            Events.MILLION_YEAR_OLD_WISH,
            Sections.MILLION_YEAR_OLD_MANS_ROOM.name,
            started_rule=CanReachRegion(Sections.MILLION_YEAR_OLD_MANS_ROOM.name),
            cleared_rule=Has(Items.RED_EVIL_PIG_BAG)
            & Has(Items.BLUE_EVIL_PIG_BAG)
            & Has(Items.NAVY_EVIL_PIG_BAG)
            & Has(Items.PINK_EVIL_PIG_BAG)
            & Has(Items.GREEN_EVIL_PIG_BAG)
            & Has(Items.ORANGE_EVIL_PIG_BAG)
            & Has(Items.YELLOW_EVIL_PIG_BAG),
        ),
        EventData(
            0x91,
            Events.DIG_LIKE_A_MOLE,
            Sections.UNDERGROUND_MAZE.name,
            started_rule=HasCleared(Events.WE_NEED_POWER),
            cleared_rule=HasCleared(Events.SOURCE_OF_EVIL_MAGIC),
        ),
        EventData(0x92, Events.THE_BLUE_FORTUNE_TELLER, Regions.UNDERGROUND_MAZE_INNER),
        # EventData(0x93, Events., Regions.), # Unused
        # EventData(0x94, Events., Regions.), # Unused
        # EventData(0x95, Events., Regions.), # Unused
        EventData(
            0x96,
            Events.LETS_RIDE_THE_RAFT,
            Regions.IRON_CASTLE_ENTRANCE,
            started_rule=HasCleared(Events.WE_NEED_POWER),
            cleared_rule=Has(Items.RAFT) & CanReachRegion(Regions.OLD_TREE_HILL),
        ),
        EventData(
            0x97, Events.TAKE_OUT, Regions.HIDDEN_VILLAGE, cleared_rule=Has(Items.YANS_LUNCH_BOX)
        ),  # TODO: Fix this event
        # EventData(0x98, Events., Regions.), # Unused
        EventData(
            0x99,
            Events.WHATS_UNDERWATER,
            Sections.HIDING_ROOM.name,
            started_rule=Has(Items.SEASHELL_NECKLACE) & HasCleared(Events.THE_10000_YEAR_OLD_MAN),
        ),
        # EventData(0x9A, Events., Regions.), # Unused
        # EventData(0x9B, Events., Regions.), # Unused
        EventData(
            0x9C,
            Events.SOURCE_OF_EVIL_MAGIC,
            Regions.TRICK_VILLAGE,
            started_rule=Has(Items.MATH_BEAD_1)
            & Has(Items.MATH_BEAD_2)
            & Has(Items.MATH_BEAD_3)
            & Has(Items.MATH_BEAD_4)
            & Has(Items.MATH_BEAD_5)
            & Has(Items.MATH_BEAD_6)
            & Has(Items.MATH_BEAD_7)
            & Has(Items.MATH_BEAD_8)
            & Has(Items.MATH_BEAD_9)
            & Has(Items.MATH_BEAD_10),
            cleared_rule=CanReachRegion(Regions.MILLION_YEAR_OLD_MANS_ROOM),
        ),
        EventData(
            0x9D,
            Events.SEVEN_FRIENDS,
            Regions.THE_STRANGE_SMALL_ROOM,
            started_rule=HasCleared(Events.MILLION_YEAR_OLD_WISH),
            cleared_rule=CanReachRegion(Regions.DWARF_VILLAGE)
            & CanReachRegion(Regions.BACCUS_VILLAGE)
            & CanReachRegion(Sections.KEYHOLE_ROOM.name)
            & CanReachRegion(Regions.Y_CROSSING)
            & CanReachRegion(Regions.LUMBERJACK_FACTORY)
            & CanReachRegion(Regions.IRON_CASTLE_ENTRANCE),
        ),
        # EventData(0x9E, Events., Regions.), # Unused
        EventData(
            0x9F,
            Events.THE_8TH_EVIL_PIG_BAG,
            Regions.THE_STRANGE_SMALL_ROOM,
            started_rule=HasCleared(Events.MILLION_YEAR_OLD_WISH),
        ),
        EventData(
            0xA0,
            Events.A_REAL_EVIL_PIG,
            Regions.THE_STRANGE_SMALL_ROOM,
            started_rule=HasCleared(Events.MILLION_YEAR_OLD_WISH),
            cleared_rule=HasCleared(Events.SEVEN_FRIENDS),
        ),
        EventData(
            0xA1,
            Events.UNDERGROUND_TREASURE,
            Regions.MILLION_YEAR_OLD_MANS_ROOM,
            started_rule=CanReachRegion(Regions.MILLION_YEAR_OLD_MANS_ROOM),
            cleared_rule=Has(Items.MILLION_YEAR_OLD_KEY),
        ),
        # EventData(0xA2, Events., Regions.), # Unused
        # EventData(0xA3, Events., Regions.), # Unused
        EventData(
            0xA4,
            Events.THE_FLOWER_TOWER,
            Regions.CHARITY_SQUARE,
            started_rule=HasCleared(Events.THE_BROKEN_FOUNTAIN),
        ),
        # EventData(0xA5, Events., Regions.), # Unused
        EventData(0xA6, Events.A_HUNGRY_MONKEY, Regions.VILLAGE_OF_ALL_BEGINNINGS, cleared_rule=Has(Items.BANANAS)),
        EventData(
            0xA7,
            Events.PEACH_FLOWER_GAS,
            Regions.VILLAGE_OF_ALL_BEGINNINGS,
            cleared_rule=HasCleared(Events.CANT_STOP_CRYING) & Has(Items.BABY_PIG),
        ),
        EventData(
            0xA8,
            Events.THE_EVIL_PIG_BAG,
            Regions.DWARF_VILLAGE,
            started_rule=HasCleared(Events.SAVE_THE_DWARVES),
            cleared_rule=HasCleared(Events.SAVE_THE_DWARVES),
        ),
        EventData(
            0xA9,
            Events.BITING_PLANT_FLOWER,
            Regions.FOREST_OF_ALL_BEGINNINGS,
            cleared_rule=HasStarted(Events.LETS_MAKE_CANDY) & Has(Items.BITING_PLANT_FLOWER),
        ),
        EventData(
            0xAA,
            Events.WHEN_THE_WIND_DIES_DOWN,
            Regions.STORMY_MOUNTAIN,
            cleared_rule=HasCleared(Events.PHOENIX_MOUNTAIN),
        ),
        EventData(
            0xAB,
            Events.THE_PHOENIXS_FAVORITE,
            Regions.LAVA_CAVES,
            started_rule=HasCleared(Events.DEATH_FRUIT_JUICE),
            cleared_rule=HasCleared(Events.LAVA_CAVES) & Has(Items.BUNK_FLOWER, 5),
        ),
        EventData(0xAC, Events.THE_FIRE_PIG_BAG, Regions.LAVA_CAVES, cleared_rule=Has(Items.THOUSAND_YEAR_OLD_KEY)),
        EventData(0xAD, Events.CHARLES_PANTS, Regions.STORMY_MOUNTAIN, cleared_rule=Has(Items.CHARLES_PANTS)),
        EventData(
            0xAE,
            Events.THE_HAUNTED_PIG_BAG,
            Sections.HAUNTED_MANSION_SOUTH.name,
            cleared_rule=Has(Items.THOUSAND_YEAR_OLD_KEY) & Has(Items.BIG_KEY),
        ),
        EventData(0xAF, Events.THE_WORLDS_GREATEST_SMILE, Regions.MUSHROOM_FOREST),
        EventData(0xB0, Events.THE_WORLDS_GREATEST_POUT, Regions.MUSHROOM_FOREST),
        EventData(0xB1, Events.SOMETHINGS_COOKIN, Regions.FOREST_OF_100_FLOWERS, cleared_rule=Has(Items.BAKED_YAM)),
        EventData(
            0xB2,
            Events.LEAF_BUTTERFLIES,
            Regions.CHARITY_SQUARE,
            started_rule=CanReachRegion(Regions.FOREST_OF_100_FLOWERS),
            cleared_rule=Has(Items.LEAF_BUTTERFLY, 29),
        ),
        EventData(
            0xB3,
            Events.WHERED_THE_LIGHTS_GO,
            Sections.UNDERGROUND_PRISON.name,
            started_rule=HasStarted(Events.TO_PHOENIX_MOUNTAIN),
            cleared_rule=Has(Items.TORCH),
        ),
        EventData(
            0xB4,
            Events.WHERE_THE_BARREL_ROLLS,
            Regions.WOBBLY_WHARF,
            started_rule=CanReachRegion(Regions.WOBBLY_WHARF) & Rules.CAN_LIGHT_BREAK_STUFF,
            cleared_rule=HasCleared(Events.WHATS_UNDERWATER),
        ),
        EventData(
            0xB5,
            Events.READY_SET_GO,
            Regions.STORMY_MOUNTAIN,
            started_rule=HasCleared(Events.THE_GREAT_ESCAPE) & HasCleared(Events.LOOK_AND_SEE),
        ),
        EventData(
            0xB6,
            Events.A_MAGIC_MIRROR,
            Regions.WATCH_TOWER,
            started_rule=Has(Items.DIRTY_MIRROR),
            cleared_rule=Has(Items.THREE_CRYSTAL_BALLS) & CanReachRegion(Regions.WITCHS_HUT),
        ),
        EventData(
            0xB7,
            Events.THE_JUNGLE_PIG_BAG,
            Regions.MASAKARI_JUNGLE,
            cleared_rule=Has(Items.TEN_THOUSAND_YEAR_OLD_KEY) & CanReachRegion(Regions.OLD_TREE_HILL),
        ),
        # EventData(0xB8, Events., Regions.), # Unused
        EventData(
            0xB9,
            Events.A_PRECIOUS_TREASURE_CHEST,
            Regions.STORMY_MOUNTAIN,
            cleared_rule=Has(Items.THOUSAND_YEAR_OLD_KEY),
        ),
        # EventData(0xBA, Events., Regions.), # Unused
        EventData(
            0xBB, Events.THE_MYSTERIOUS_MUSHROOM, Regions.CHARITY_SQUARE, cleared_rule=Has(Items.THOUSAND_YEAR_OLD_KEY)
        ),
        EventData(
            0xBC, Events.LEAF_SLIDER, Regions.CHARITY_SQUARE, cleared_rule=CanReachRegion(Regions.MUSHROOM_FOREST)
        ),
        EventData(
            0xBD,
            Events.RED_BLUE,
            Regions.CHARITY_SQUARE,
            cleared_rule=CanReachRegion(Regions.CHARITY_SQUARE) & CanReachRegion(Regions.MUSHROOM_FOREST),
        ),
        EventData(
            0xBE,
            Events.THE_TROUBLED_THIEF,
            Regions.LAVA_CAVES,
            started_rule=HasCleared(Events.LAVA_CAVES),
            cleared_rule=Has(Items.WHAT_THE_THIEF_LOST),
        ),
        EventData(
            0xBF,
            Events.WHAT_THE_THIEF_FORGOT,
            Regions.LAVA_CAVES,
            started_rule=HasCleared(Events.THE_TROUBLED_THIEF),
            cleared_rule=HasCleared(Events.THE_HAUNTED_MANSION) & Has(Items.WHAT_THE_THIEF_FORGOT),
        ),
    ]

    by_name: dict[str, EventData] = {}
    by_id: dict[int, EventData] = {}
    for index, event in enumerate(event_table):
        by_name[event.name] = event
        by_id[event.id] = event

    @staticmethod
    def get_event_region(event_name: str) -> str:
        return EventHandler.by_name[event_name].region
