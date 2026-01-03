from collections.abc import Iterable
from typing import TYPE_CHECKING, NamedTuple

from BaseClasses import Item
from BaseClasses import ItemClassification as IC
from worlds.AutoWorld import World

from .Constants import APID_BASE, GAME_NAME, GLITCHED_ITEM
from .Enums import ItemName

if TYPE_CHECKING:
    from .randomizers.Dungeons import Dungeon


def item_factory(items: str | Iterable[str], world: World) -> Item | list[Item]:
    """
    Create items based on their names.
    Depending on the input, this function can return a single item or a list of items.

    :param items: The name or names of the items to create.
    :param world: The game world.
    :raises KeyError: If an unknown item name is provided.
    :return: A single item or a list of items.
    """
    ret: list[Item] = []
    singleton = False
    if isinstance(items, str):
        items = [items]
        singleton = True
    for item in items:
        if item in ITEM_TABLE:
            ret.append(world.create_item(item))
        else:
            raise KeyError(f"Unknown item {item}")

    return ret[0] if singleton else ret


class TWWItemData(NamedTuple):
    """Data for an item in The Wind Waker."""

    type: str
    """The type of the item (e.g., "Item", "Dungeon Item")."""
    classification: IC
    """The item's classification (progression, useful, filler)."""
    code: int | None
    """The unique code identifier for the item."""
    quantity: int
    """The number of this item available."""
    item_id: int | None
    """The ID used to represent the item in-game."""


class TWWItem(Item):
    """
    This class represents an item in The Wind Waker.

    :param name: The item's name.
    :param player: The ID of the player who owns the item.
    :param data: The data associated with this item.
    :param classification: Optional classification to override the default.
    """

    game: str = GAME_NAME
    type: str | None
    dungeon: "Dungeon | None" = None

    def __init__(self, name: str, player: int, data: TWWItemData, classification: IC | None = None) -> None:
        super().__init__(
            name,
            data.classification if classification is None else classification,
            None if data.code is None else TWWItem.get_apid(data.code),
            player,
        )

        self.type = data.type
        self.item_id = data.item_id

    @staticmethod
    def get_apid(code: int) -> int:
        """
        Compute the Archipelago ID for the given item code.

        :param code: The unique code for the item.
        :return: The computed Archipelago ID.
        """
        return APID_BASE + code

    @property
    def dungeon_item(self) -> str | None:
        """
        Get the dungeon item type if this item is a dungeon item.

        :return: The dungeon item type ("Small Key", "Big Key", "Map", "Compass"), or None.
        """
        if self.type in ("Small Key", "Big Key", "Map", "Compass"):
            return self.type
        return None


ITEM_TABLE: dict[str, TWWItemData] = {
    ItemName.TELESCOPE.value:                 TWWItemData("Item",      IC.useful,                       0,  1, 0x20),
  # ItemName.BOAT_S_SAIL.value:               TWWItemData("Item",      IC.progression,                  1,  1, 0x78),  # noqa: E131
    ItemName.WIND_WAKER.value:                TWWItemData("Item",      IC.progression,                  2,  1, 0x22),
    ItemName.GRAPPLING_HOOK.value:            TWWItemData("Item",      IC.progression,                  3,  1, 0x25),
    ItemName.SPOILS_BAG.value:                TWWItemData("Item",      IC.progression,                  4,  1, 0x24),
    ItemName.BOOMERANG.value:                 TWWItemData("Item",      IC.progression,                  5,  1, 0x2D),
    ItemName.DEKU_LEAF.value:                 TWWItemData("Item",      IC.progression,                  6,  1, 0x34),
    ItemName.TINGLE_TUNER.value:              TWWItemData("Item",      IC.progression,                  7,  1, 0x21),
    ItemName.IRON_BOOTS.value:                TWWItemData("Item",      IC.progression,                  8,  1, 0x29),
    ItemName.MAGIC_ARMOR.value:               TWWItemData("Item",      IC.progression,                  9,  1, 0x2A),
    ItemName.BAIT_BAG.value:                  TWWItemData("Item",      IC.progression,                 10,  1, 0x2C),
    ItemName.BOMBS.value:                     TWWItemData("Item",      IC.progression,                 11,  1, 0x31),
    ItemName.DELIVERY_BAG.value:              TWWItemData("Item",      IC.progression,                 12,  1, 0x30),
    ItemName.HOOKSHOT.value:                  TWWItemData("Item",      IC.progression,                 13,  1, 0x2F),
    ItemName.SKULL_HAMMER.value:              TWWItemData("Item",      IC.progression,                 14,  1, 0x33),
    ItemName.POWER_BRACELETS.value:           TWWItemData("Item",      IC.progression,                 15,  1, 0x28),

    ItemName.HERO_S_CHARM.value:              TWWItemData("Item",      IC.useful,                      16,  1, 0x43),
    ItemName.HURRICANE_SPIN.value:            TWWItemData("Item",      IC.useful,                      17,  1, 0xAA),
    ItemName.DRAGON_TINGLE_STATUE.value:      TWWItemData("Item",      IC.progression,                 18,  1, 0xA3),
    ItemName.FORBIDDEN_TINGLE_STATUE.value:   TWWItemData("Item",      IC.progression,                 19,  1, 0xA4),
    ItemName.GODDESS_TINGLE_STATUE.value:     TWWItemData("Item",      IC.progression,                 20,  1, 0xA5),
    ItemName.EARTH_TINGLE_STATUE.value:       TWWItemData("Item",      IC.progression,                 21,  1, 0xA6),
    ItemName.WIND_TINGLE_STATUE.value:        TWWItemData("Item",      IC.progression,                 22,  1, 0xA7),

    ItemName.WIND_S_REQUIEM.value:            TWWItemData("Item",      IC.progression,                 23,  1, 0x6D),
    ItemName.BALLAD_OF_GALES.value:           TWWItemData("Item",      IC.progression,                 24,  1, 0x6E),
    ItemName.COMMAND_MELODY.value:            TWWItemData("Item",      IC.progression,                 25,  1, 0x6F),
    ItemName.EARTH_GOD_S_LYRIC.value:         TWWItemData("Item",      IC.progression,                 26,  1, 0x70),
    ItemName.WIND_GOD_S_ARIA.value:           TWWItemData("Item",      IC.progression,                 27,  1, 0x71),
    ItemName.SONG_OF_PASSING.value:           TWWItemData("Item",      IC.progression,                 28,  1, 0x72),

    ItemName.TRIFORCE_SHARD_1.value:          TWWItemData("Item",      IC.progression,                 29,  1, 0x61),
    ItemName.TRIFORCE_SHARD_2.value:          TWWItemData("Item",      IC.progression,                 30,  1, 0x62),
    ItemName.TRIFORCE_SHARD_3.value:          TWWItemData("Item",      IC.progression,                 31,  1, 0x63),
    ItemName.TRIFORCE_SHARD_4.value:          TWWItemData("Item",      IC.progression,                 32,  1, 0x64),
    ItemName.TRIFORCE_SHARD_5.value:          TWWItemData("Item",      IC.progression,                 33,  1, 0x65),
    ItemName.TRIFORCE_SHARD_6.value:          TWWItemData("Item",      IC.progression,                 34,  1, 0x66),
    ItemName.TRIFORCE_SHARD_7.value:          TWWItemData("Item",      IC.progression,                 35,  1, 0x67),
    ItemName.TRIFORCE_SHARD_8.value:          TWWItemData("Item",      IC.progression,                 36,  1, 0x68),

    ItemName.SKULL_NECKLACE.value:            TWWItemData("Item",      IC.filler,                      37,  9, 0x45),
    ItemName.BOKO_BABA_SEED.value:            TWWItemData("Item",      IC.filler,                      38,  1, 0x46),
    ItemName.GOLDEN_FEATHER.value:            TWWItemData("Item",      IC.filler,                      39,  9, 0x47),
    ItemName.KNIGHT_S_CREST.value:            TWWItemData("Item",      IC.filler,                      40,  3, 0x48),
    ItemName.RED_CHU_JELLY.value:             TWWItemData("Item",      IC.filler,                      41,  1, 0x49),
    ItemName.GREEN_CHU_JELLY.value:           TWWItemData("Item",      IC.filler,                      42,  1, 0x4A),
    ItemName.JOY_PENDANT.value:               TWWItemData("Item",      IC.filler,                      43, 20, 0x1F),
    ItemName.ALL_PURPOSE_BAIT.value:          TWWItemData("Item",      IC.filler,                      44,  1, 0x82),
    ItemName.HYOI_PEAR.value:                 TWWItemData("Item",      IC.filler,                      45,  4, 0x83),

    ItemName.NOTE_TO_MOM.value:               TWWItemData("Item",      IC.progression,                 46,  1, 0x99),
    ItemName.MAGGIE_S_LETTER.value:           TWWItemData("Item",      IC.progression,                 47,  1, 0x9A),
    ItemName.MOBLIN_S_LETTER.value:           TWWItemData("Item",      IC.progression,                 48,  1, 0x9B),
    ItemName.CABANA_DEED.value:               TWWItemData("Item",      IC.progression,                 49,  1, 0x9C),
    ItemName.FILL_UP_COUPON.value:            TWWItemData("Item",      IC.useful,                      50,  1, 0x9E),

    ItemName.NAYRU_S_PEARL.value:             TWWItemData("Item",      IC.progression,                 51,  1, 0x69),
    ItemName.DIN_S_PEARL.value:               TWWItemData("Item",      IC.progression,                 52,  1, 0x6A),
    ItemName.FARORE_S_PEARL.value:            TWWItemData("Item",      IC.progression,                 53,  1, 0x6B),

    ItemName.PROGRESSIVE_SWORD.value:         TWWItemData("Item",      IC.progression,                 54,  4, 0x38),
    ItemName.PROGRESSIVE_SHIELD.value:        TWWItemData("Item",      IC.progression,                 55,  2, 0x3B),
    ItemName.PROGRESSIVE_PICTO_BOX.value:     TWWItemData("Item",      IC.progression,                 56,  2, 0x23),
    ItemName.PROGRESSIVE_BOW.value:           TWWItemData("Item",      IC.progression,                 57,  3, 0x27),
    ItemName.PROGRESSIVE_MAGIC_METER.value:   TWWItemData("Item",      IC.progression,                 58,  2, 0xB1),
    ItemName.QUIVER_CAPACITY_UPGRADE.value:   TWWItemData("Item",      IC.progression,                 59,  2, 0xAF),
    ItemName.BOMB_BAG_CAPACITY_UPGRADE.value: TWWItemData("Item",      IC.useful,                      60,  2, 0xAD),
    ItemName.WALLET_CAPACITY_UPGRADE.value:   TWWItemData("Item",      IC.progression,                 61,  2, 0xAB),
    ItemName.EMPTY_BOTTLE.value:              TWWItemData("Item",      IC.progression,                 62,  4, 0x50),

    ItemName.TRIFORCE_CHART_1.value:          TWWItemData("Item",      IC.progression_skip_balancing,  63,  1, 0xFE),
    ItemName.TRIFORCE_CHART_2.value:          TWWItemData("Item",      IC.progression_skip_balancing,  64,  1, 0xFD),
    ItemName.TRIFORCE_CHART_3.value:          TWWItemData("Item",      IC.progression_skip_balancing,  65,  1, 0xFC),
    ItemName.TRIFORCE_CHART_4.value:          TWWItemData("Item",      IC.progression_skip_balancing,  66,  1, 0xFB),
    ItemName.TRIFORCE_CHART_5.value:          TWWItemData("Item",      IC.progression_skip_balancing,  67,  1, 0xFA),
    ItemName.TRIFORCE_CHART_6.value:          TWWItemData("Item",      IC.progression_skip_balancing,  68,  1, 0xF9),
    ItemName.TRIFORCE_CHART_7.value:          TWWItemData("Item",      IC.progression_skip_balancing,  69,  1, 0xF8),
    ItemName.TRIFORCE_CHART_8.value:          TWWItemData("Item",      IC.progression_skip_balancing,  70,  1, 0xF7),
    ItemName.TREASURE_CHART_1.value:          TWWItemData("Item",      IC.progression_skip_balancing,  71,  1, 0xE7),
    ItemName.TREASURE_CHART_2.value:          TWWItemData("Item",      IC.progression_skip_balancing,  72,  1, 0xEE),
    ItemName.TREASURE_CHART_3.value:          TWWItemData("Item",      IC.progression_skip_balancing,  73,  1, 0xE0),
    ItemName.TREASURE_CHART_4.value:          TWWItemData("Item",      IC.progression_skip_balancing,  74,  1, 0xE1),
    ItemName.TREASURE_CHART_5.value:          TWWItemData("Item",      IC.progression_skip_balancing,  75,  1, 0xF2),
    ItemName.TREASURE_CHART_6.value:          TWWItemData("Item",      IC.progression_skip_balancing,  76,  1, 0xEA),
    ItemName.TREASURE_CHART_7.value:          TWWItemData("Item",      IC.progression_skip_balancing,  77,  1, 0xCC),
    ItemName.TREASURE_CHART_8.value:          TWWItemData("Item",      IC.progression_skip_balancing,  78,  1, 0xD4),
    ItemName.TREASURE_CHART_9.value:          TWWItemData("Item",      IC.progression_skip_balancing,  79,  1, 0xDA),
    ItemName.TREASURE_CHART_10.value:         TWWItemData("Item",      IC.progression_skip_balancing,  80,  1, 0xDE),
    ItemName.TREASURE_CHART_11.value:         TWWItemData("Item",      IC.progression_skip_balancing,  81,  1, 0xF6),
    ItemName.TREASURE_CHART_12.value:         TWWItemData("Item",      IC.progression_skip_balancing,  82,  1, 0xE9),
    ItemName.TREASURE_CHART_13.value:         TWWItemData("Item",      IC.progression_skip_balancing,  83,  1, 0xCF),
    ItemName.TREASURE_CHART_14.value:         TWWItemData("Item",      IC.progression_skip_balancing,  84,  1, 0xDD),
    ItemName.TREASURE_CHART_15.value:         TWWItemData("Item",      IC.progression_skip_balancing,  85,  1, 0xF5),
    ItemName.TREASURE_CHART_16.value:         TWWItemData("Item",      IC.progression_skip_balancing,  86,  1, 0xE3),
    ItemName.TREASURE_CHART_17.value:         TWWItemData("Item",      IC.progression_skip_balancing,  87,  1, 0xD7),
    ItemName.TREASURE_CHART_18.value:         TWWItemData("Item",      IC.progression_skip_balancing,  88,  1, 0xE4),
    ItemName.TREASURE_CHART_19.value:         TWWItemData("Item",      IC.progression_skip_balancing,  89,  1, 0xD1),
    ItemName.TREASURE_CHART_20.value:         TWWItemData("Item",      IC.progression_skip_balancing,  90,  1, 0xF3),
    ItemName.TREASURE_CHART_21.value:         TWWItemData("Item",      IC.progression_skip_balancing,  91,  1, 0xCE),
    ItemName.TREASURE_CHART_22.value:         TWWItemData("Item",      IC.progression_skip_balancing,  92,  1, 0xD9),
    ItemName.TREASURE_CHART_23.value:         TWWItemData("Item",      IC.progression_skip_balancing,  93,  1, 0xF1),
    ItemName.TREASURE_CHART_24.value:         TWWItemData("Item",      IC.progression_skip_balancing,  94,  1, 0xEB),
    ItemName.TREASURE_CHART_25.value:         TWWItemData("Item",      IC.progression_skip_balancing,  95,  1, 0xD6),
    ItemName.TREASURE_CHART_26.value:         TWWItemData("Item",      IC.progression_skip_balancing,  96,  1, 0xD3),
    ItemName.TREASURE_CHART_27.value:         TWWItemData("Item",      IC.progression_skip_balancing,  97,  1, 0xCD),
    ItemName.TREASURE_CHART_28.value:         TWWItemData("Item",      IC.progression_skip_balancing,  98,  1, 0xE2),
    ItemName.TREASURE_CHART_29.value:         TWWItemData("Item",      IC.progression_skip_balancing,  99,  1, 0xE6),
    ItemName.TREASURE_CHART_30.value:         TWWItemData("Item",      IC.progression_skip_balancing, 100,  1, 0xF4),
    ItemName.TREASURE_CHART_31.value:         TWWItemData("Item",      IC.progression_skip_balancing, 101,  1, 0xF0),
    ItemName.TREASURE_CHART_32.value:         TWWItemData("Item",      IC.progression_skip_balancing, 102,  1, 0xD0),
    ItemName.TREASURE_CHART_33.value:         TWWItemData("Item",      IC.progression_skip_balancing, 103,  1, 0xEF),
    ItemName.TREASURE_CHART_34.value:         TWWItemData("Item",      IC.progression_skip_balancing, 104,  1, 0xE5),
    ItemName.TREASURE_CHART_35.value:         TWWItemData("Item",      IC.progression_skip_balancing, 105,  1, 0xE8),
    ItemName.TREASURE_CHART_36.value:         TWWItemData("Item",      IC.progression_skip_balancing, 106,  1, 0xD8),
    ItemName.TREASURE_CHART_37.value:         TWWItemData("Item",      IC.progression_skip_balancing, 107,  1, 0xD5),
    ItemName.TREASURE_CHART_38.value:         TWWItemData("Item",      IC.progression_skip_balancing, 108,  1, 0xED),
    ItemName.TREASURE_CHART_39.value:         TWWItemData("Item",      IC.progression_skip_balancing, 109,  1, 0xEC),
    ItemName.TREASURE_CHART_40.value:         TWWItemData("Item",      IC.progression_skip_balancing, 110,  1, 0xDF),
    ItemName.TREASURE_CHART_41.value:         TWWItemData("Item",      IC.progression_skip_balancing, 111,  1, 0xD2),

    ItemName.TINGLE_S_CHART.value:            TWWItemData("Item",      IC.filler,                     112,  1, 0xDC),
    ItemName.GHOST_SHIP_CHART.value:          TWWItemData("Item",      IC.progression,                113,  1, 0xDB),
    ItemName.OCTO_CHART.value:                TWWItemData("Item",      IC.filler,                     114,  1, 0xCA),
    ItemName.GREAT_FAIRY_CHART.value:         TWWItemData("Item",      IC.filler,                     115,  1, 0xC9),
    ItemName.SECRET_CAVE_CHART.value:         TWWItemData("Item",      IC.filler,                     116,  1, 0xC6),
    ItemName.LIGHT_RING_CHART.value:          TWWItemData("Item",      IC.filler,                     117,  1, 0xC5),
    ItemName.PLATFORM_CHART.value:            TWWItemData("Item",      IC.filler,                     118,  1, 0xC4),
    ItemName.BEEDLE_S_CHART.value:            TWWItemData("Item",      IC.filler,                     119,  1, 0xC3),
    ItemName.SUBMARINE_CHART.value:           TWWItemData("Item",      IC.filler,                     120,  1, 0xC2),

    ItemName.GREEN_RUPEE.value:               TWWItemData("Item",      IC.filler,                     121,  1, 0x01),
    ItemName.BLUE_RUPEE.value:                TWWItemData("Item",      IC.filler,                     122,  2, 0x02),
    ItemName.YELLOW_RUPEE.value:              TWWItemData("Item",      IC.filler,                     123,  3, 0x03),
    ItemName.RED_RUPEE.value:                 TWWItemData("Item",      IC.filler,                     124,  8, 0x04),
    ItemName.PURPLE_RUPEE.value:              TWWItemData("Item",      IC.filler,                     125, 10, 0x05),
    ItemName.ORANGE_RUPEE.value:              TWWItemData("Item",      IC.useful,                     126, 15, 0x06),
    ItemName.SILVER_RUPEE.value:              TWWItemData("Item",      IC.useful,                     127, 20, 0x0F),
    ItemName.RAINBOW_RUPEE.value:             TWWItemData("Item",      IC.useful,                     128,  1, 0xB8),

    ItemName.PIECE_OF_HEART.value:            TWWItemData("Item",      IC.useful,                     129, 44, 0x07),
    ItemName.HEART_CONTAINER.value:           TWWItemData("Item",      IC.useful,                     130,  6, 0x08),

    ItemName.DRC_BIG_KEY.value:               TWWItemData("Big Key",   IC.progression,                131,  1, 0x14),
    ItemName.DRC_SMALL_KEY.value:             TWWItemData("Small Key", IC.progression,                132,  4, 0x13),
    ItemName.FW_BIG_KEY.value:                TWWItemData("Big Key",   IC.progression,                133,  1, 0x40),
    ItemName.FW_SMALL_KEY.value:              TWWItemData("Small Key", IC.progression,                134,  1, 0x1D),
    ItemName.TOTG_BIG_KEY.value:              TWWItemData("Big Key",   IC.progression,                135,  1, 0x5C),
    ItemName.TOTG_SMALL_KEY.value:            TWWItemData("Small Key", IC.progression,                136,  2, 0x5B),
    ItemName.ET_BIG_KEY.value:                TWWItemData("Big Key",   IC.progression,                138,  1, 0x74),
    ItemName.ET_SMALL_KEY.value:              TWWItemData("Small Key", IC.progression,                139,  3, 0x73),
    ItemName.WT_BIG_KEY.value:                TWWItemData("Big Key",   IC.progression,                140,  1, 0x81),
    ItemName.WT_SMALL_KEY.value:              TWWItemData("Small Key", IC.progression,                141,  2, 0x77),
    ItemName.DRC_DUNGEON_MAP.value:           TWWItemData("Map",       IC.filler,                     142,  1, 0x1B),
    ItemName.DRC_COMPASS.value:               TWWItemData("Compass",   IC.filler,                     143,  1, 0x1C),
    ItemName.FW_DUNGEON_MAP.value:            TWWItemData("Map",       IC.filler,                     144,  1, 0x41),
    ItemName.FW_COMPASS.value:                TWWItemData("Compass",   IC.filler,                     145,  1, 0x5A),
    ItemName.TOTG_DUNGEON_MAP.value:          TWWItemData("Map",       IC.filler,                     146,  1, 0x5D),
    ItemName.TOTG_COMPASS.value:              TWWItemData("Compass",   IC.filler,                     147,  1, 0x5E),
    ItemName.FF_DUNGEON_MAP.value:            TWWItemData("Map",       IC.filler,                     148,  1, 0x5F),
    ItemName.FF_COMPASS.value:                TWWItemData("Compass",   IC.filler,                     149,  1, 0x60),
    ItemName.ET_DUNGEON_MAP.value:            TWWItemData("Map",       IC.filler,                     150,  1, 0x75),
    ItemName.ET_COMPASS.value:                TWWItemData("Compass",   IC.filler,                     151,  1, 0x76),
    ItemName.WT_DUNGEON_MAP.value:            TWWItemData("Map",       IC.filler,                     152,  1, 0x84),
    ItemName.WT_COMPASS.value:                TWWItemData("Compass",   IC.filler,                     153,  1, 0x85),

    ItemName.VICTORY.value:                   TWWItemData("Event",     IC.progression,               None,  1, None),

    # Intentionally place the glitched item below the rest. As it's not a traditional item, it doesn't use the enum.
    GLITCHED_ITEM:                            TWWItemData("Event",     IC.progression,               None,  1, None),
}

ISLAND_NUMBER_TO_CHART_NAME = {
    1: ItemName.TREASURE_CHART_25.value,
    2: ItemName.TREASURE_CHART_7.value,
    3: ItemName.TREASURE_CHART_24.value,
    4: ItemName.TRIFORCE_CHART_2.value,
    5: ItemName.TREASURE_CHART_11.value,
    6: ItemName.TRIFORCE_CHART_7.value,
    7: ItemName.TREASURE_CHART_13.value,
    8: ItemName.TREASURE_CHART_41.value,
    9: ItemName.TREASURE_CHART_29.value,
    10: ItemName.TREASURE_CHART_22.value,
    11: ItemName.TREASURE_CHART_18.value,
    12: ItemName.TREASURE_CHART_30.value,
    13: ItemName.TREASURE_CHART_39.value,
    14: ItemName.TREASURE_CHART_19.value,
    15: ItemName.TREASURE_CHART_8.value,
    16: ItemName.TREASURE_CHART_2.value,
    17: ItemName.TREASURE_CHART_10.value,
    18: ItemName.TREASURE_CHART_26.value,
    19: ItemName.TREASURE_CHART_3.value,
    20: ItemName.TREASURE_CHART_37.value,
    21: ItemName.TREASURE_CHART_27.value,
    22: ItemName.TREASURE_CHART_38.value,
    23: ItemName.TRIFORCE_CHART_1.value,
    24: ItemName.TREASURE_CHART_21.value,
    25: ItemName.TREASURE_CHART_6.value,
    26: ItemName.TREASURE_CHART_14.value,
    27: ItemName.TREASURE_CHART_34.value,
    28: ItemName.TREASURE_CHART_5.value,
    29: ItemName.TREASURE_CHART_28.value,
    30: ItemName.TREASURE_CHART_35.value,
    31: ItemName.TRIFORCE_CHART_3.value,
    32: ItemName.TRIFORCE_CHART_6.value,
    33: ItemName.TREASURE_CHART_1.value,
    34: ItemName.TREASURE_CHART_20.value,
    35: ItemName.TREASURE_CHART_36.value,
    36: ItemName.TREASURE_CHART_23.value,
    37: ItemName.TREASURE_CHART_12.value,
    38: ItemName.TREASURE_CHART_16.value,
    39: ItemName.TREASURE_CHART_4.value,
    40: ItemName.TREASURE_CHART_17.value,
    41: ItemName.TREASURE_CHART_31.value,
    42: ItemName.TRIFORCE_CHART_5.value,
    43: ItemName.TREASURE_CHART_9.value,
    44: ItemName.TRIFORCE_CHART_4.value,
    45: ItemName.TREASURE_CHART_40.value,
    46: ItemName.TRIFORCE_CHART_8.value,
    47: ItemName.TREASURE_CHART_15.value,
    48: ItemName.TREASURE_CHART_32.value,
    49: ItemName.TREASURE_CHART_33.value,
}


LOOKUP_ID_TO_NAME: dict[int, str] = {
    TWWItem.get_apid(data.code): item for item, data in ITEM_TABLE.items() if data.code is not None
}

item_name_groups = {
    "Songs": {
        ItemName.WIND_S_REQUIEM.value,
        ItemName.BALLAD_OF_GALES.value,
        ItemName.COMMAND_MELODY.value,
        ItemName.EARTH_GOD_S_LYRIC.value,
        ItemName.WIND_GOD_S_ARIA.value,
        ItemName.SONG_OF_PASSING.value,
    },
    "Mail": {
        ItemName.NOTE_TO_MOM.value,
        ItemName.MAGGIE_S_LETTER.value,
        ItemName.MOBLIN_S_LETTER.value,
    },
    "Special Charts": {
        ItemName.TINGLE_S_CHART.value,
        ItemName.GHOST_SHIP_CHART.value,
        ItemName.OCTO_CHART.value,
        ItemName.GREAT_FAIRY_CHART.value,
        ItemName.SECRET_CAVE_CHART.value,
        ItemName.LIGHT_RING_CHART.value,
        ItemName.PLATFORM_CHART.value,
        ItemName.BEEDLE_S_CHART.value,
        ItemName.SUBMARINE_CHART.value,
    },
}
# generic groups, (Name, substring)
_simple_groups = {
    ("Tingle Statues", "Tingle Statue"),
    ("Shards", "Shard"),
    ("Pearls", "Pearl"),
    ("Triforce Charts", "Triforce Chart"),
    ("Treasure Charts", "Treasure Chart"),
    ("Small Keys", "Small Key"),
    ("Big Keys", "Big Key"),
    ("Rupees", "Rupee"),
    ("Dungeon Items", "Compass"),
    ("Dungeon Items", "Map"),
}
for basename, substring in _simple_groups:
    if basename not in item_name_groups:
        item_name_groups[basename] = set()
    for itemname in ITEM_TABLE:
        if substring in itemname:
            item_name_groups[basename].add(itemname)
