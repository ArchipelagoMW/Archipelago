from dataclasses import dataclass
from typing import TYPE_CHECKING

from BaseClasses import ItemClassification
from .options import DHCAccess, DungeonItem, Goal, ShuffleElements
from .constants import TMCItem, TMCLocation, MinishCapItem

if TYPE_CHECKING:
    from . import MinishCapWorld


DEPRIORITIZED_FALLBACK = 0
"""backwards-compatible fallback for AP v0.6.2 and prior"""
try:
    DEPRIORITIZED_FALLBACK = ItemClassification.progression_deprioritized_skip_balancing
except AttributeError as e:
    DEPRIORITIZED_FALLBACK = ItemClassification.progression_skip_balancing


@dataclass
class ItemData:
    classification: ItemClassification
    byte_ids: tuple[int, int]

    @property
    def item_id(self):
        return (self.byte_ids[0] << 8) + self.byte_ids[1]


def pool_elements() -> list[str]:
    return [TMCItem.EARTH_ELEMENT, TMCItem.FIRE_ELEMENT, TMCItem.WATER_ELEMENT, TMCItem.WIND_ELEMENT]


def pool_random_bottle_contents() -> list[str]:
    return [
        TMCItem.EMPTY_BOTTLE,
        TMCItem.LON_LON_BUTTER,
        TMCItem.LON_LON_MILK,
        TMCItem.LON_LON_MILK_HALF,
        TMCItem.RED_POTION,
        TMCItem.BLUE_POTION,
        TMCItem.WATER,
        TMCItem.MINERAL_WATER,
        TMCItem.BOTTLED_FAIRY,
        TMCItem.RED_PICOLYTE,
        TMCItem.ORANGE_PICOLYTE,
        TMCItem.YELLOW_PICOLYTE,
        TMCItem.GREEN_PICOLYTE,
        TMCItem.BLUE_PICOLYTE,
        TMCItem.WHITE_PICOLYTE,
        TMCItem.NAYRU_CHARM,
        TMCItem.FARORE_CHARM,
        TMCItem.DINS_CHARM,
    ]


def pool_bottles() -> list[str]:
    return [TMCItem.EMPTY_BOTTLE] * 4


def pool_baseitems() -> list[str]:
    return [
        *[TMCItem.PROGRESSIVE_SWORD] * 5,
        *[TMCItem.PROGRESSIVE_SHIELD] * 2,
        *[TMCItem.PROGRESSIVE_BOW] * 2,
        *[TMCItem.PROGRESSIVE_BOOMERANG] * 2,
        *[TMCItem.BOMB_BAG] * 4,
        TMCItem.REMOTE_BOMB,
        *[TMCItem.QUIVER] * 3,
        TMCItem.BOW_BUTTERFLY,

        TMCItem.GUST_JAR,
        TMCItem.LANTERN,
        TMCItem.CANE_OF_PACCI,
        TMCItem.ROCS_CAPE,
        TMCItem.PEGASUS_BOOTS,
        TMCItem.OCARINA,

        TMCItem.FLIPPERS,
        TMCItem.SWIM_BUTTERFLY,

        TMCItem.MOLE_MITTS,
        TMCItem.DIG_BUTTERFLY,

        TMCItem.DOG_FOOD,

        *[TMCItem.HEART_PIECE] * 44,
        *[TMCItem.HEART_CONTAINER] * 6,

        TMCItem.RUPEES_1,
        TMCItem.RUPEES_5,
        TMCItem.RUPEES_20,
        TMCItem.RUPEES_50,
        TMCItem.RUPEES_100,
        TMCItem.RUPEES_200,
        TMCItem.BIG_WALLET,
        TMCItem.BIG_WALLET,
        TMCItem.BIG_WALLET,

        TMCItem.HEART_REFILL,
        TMCItem.BOMB_REFILL_5,
        TMCItem.BOMB_REFILL_10,
        TMCItem.BOMB_REFILL_30,
        TMCItem.ARROW_REFILL_5,
        TMCItem.ARROW_REFILL_10,
        TMCItem.ARROW_REFILL_30,

        TMCItem.SPIN_ATTACK,
        TMCItem.ROLL_ATTACK,
        TMCItem.DASH_ATTACK,
        TMCItem.ROCK_BREAKER,
        TMCItem.SWORD_BEAM,
        TMCItem.GREATSPIN,
        TMCItem.DOWNTHRUST,
        TMCItem.PERIL_BEAM,
        TMCItem.FAST_SPIN_SCROLL,
        TMCItem.FAST_SPLIT_SCROLL,
        TMCItem.LONG_SPIN,

        TMCItem.TINGLE_TROPHY,
        TMCItem.CARLOV_MEDAL,
        TMCItem.JABBER_NUT,
        TMCItem.WAKEUP_MUSHROOM,
        TMCItem.GRIP_RING,
        TMCItem.POWER_BRACELETS,
        TMCItem.LONLON_KEY,
        TMCItem.GRAVEYARD_KEY,
        TMCItem.RED_BOOK,
        TMCItem.GREEN_BOOK,
        TMCItem.BLUE_BOOK,

        *(pool_kinstone_gold()),
    ]


def pool_traps() -> list[str]:
    return [TMCItem.TRAP_ICE, TMCItem.TRAP_FIRE, TMCItem.TRAP_ZAP, TMCItem.TRAP_BOMB, TMCItem.TRAP_MONEY,
            TMCItem.TRAP_STINK, TMCItem.TRAP_ROPE, TMCItem.TRAP_BAT, TMCItem.TRAP_LIKE, TMCItem.TRAP_CURSE]


def pool_dungeonmaps(world: "MinishCapWorld") -> list[str]:
    maps = [TMCItem.DUNGEON_MAP_DWS, TMCItem.DUNGEON_MAP_COF, TMCItem.DUNGEON_MAP_FOW, TMCItem.DUNGEON_MAP_TOD,
            TMCItem.DUNGEON_MAP_POW]
    if world.options.dhc_access != DHCAccess.option_closed:
        maps.append(TMCItem.DUNGEON_MAP_DHC)
    return maps


def pool_compass(world: "MinishCapWorld") -> list[str]:
    compasses = [TMCItem.DUNGEON_COMPASS_DWS, TMCItem.DUNGEON_COMPASS_COF, TMCItem.DUNGEON_COMPASS_FOW,
                 TMCItem.DUNGEON_COMPASS_TOD, TMCItem.DUNGEON_COMPASS_POW]
    if world.options.dhc_access != DHCAccess.option_closed:
        compasses.append(TMCItem.DUNGEON_COMPASS_DHC)
    return compasses


def pool_bigkeys(world: "MinishCapWorld") -> list[str]:
    keys = [TMCItem.BIG_KEY_DWS, TMCItem.BIG_KEY_COF, TMCItem.BIG_KEY_FOW, TMCItem.BIG_KEY_POW]
    if world.options.dhc_access != DHCAccess.option_closed and world.options.goal == Goal.option_vaati:
        keys.append(TMCItem.BIG_KEY_DHC)
    return keys


def pool_smallkeys(world: "MinishCapWorld") -> list[str]:
    keys = [
        *[TMCItem.SMALL_KEY_DWS] * 4,
        *[TMCItem.SMALL_KEY_COF] * 2,
        *[TMCItem.SMALL_KEY_FOW] * 4,
        *[TMCItem.SMALL_KEY_TOD] * 4,
        *[TMCItem.SMALL_KEY_POW] * 6,
        *[TMCItem.SMALL_KEY_RC] * 3,
    ]
    if world.options.dhc_access != DHCAccess.option_closed:
        keys.extend([TMCItem.SMALL_KEY_DHC] * 5)
    return keys


def pool_kinstone_gold() -> list[str]:
    return [*[TMCItem.KINSTONE_GOLD_CLOUD] * 5, *[TMCItem.KINSTONE_GOLD_SWAMP] * 3, TMCItem.KINSTONE_GOLD_FALLS]


def pool_kinstone_red() -> list[str]:
    return [*[TMCItem.KINSTONE_RED_W] * 9, *[TMCItem.KINSTONE_RED_ANGLE] * 7, *[TMCItem.KINSTONE_RED_E] * 8]


def pool_kinstone_blue() -> list[str]:
    return [*[TMCItem.KINSTONE_BLUE_L] * 9, *[TMCItem.KINSTONE_BLUE_6] * 9]


def pool_kinstone_green() -> list[str]:
    return [*[TMCItem.KINSTONE_GREEN_ANGLE] * 17, *[TMCItem.KINSTONE_GREEN_SQUARE] * 16, *[TMCItem.KINSTONE_GREEN_P] * 16]


def get_item_pool(world: "MinishCapWorld") -> list[MinishCapItem]:
    player = world.player
    multiworld = world.multiworld
    item_pool = pool_baseitems()

    if world.options.early_weapon.value:
        weapon_pool = [TMCItem.PROGRESSIVE_SWORD]
        if world.options.weapon_bomb.value in {1, 2}:
            weapon_pool.extend([TMCItem.BOMB_BAG])
        if world.options.weapon_bow.value:
            weapon_pool.extend([TMCItem.PROGRESSIVE_BOW])
        weapon_choice = world.random.choice(weapon_pool)
        multiworld.local_early_items[player][weapon_choice] = 1

    if world.options.dungeon_big_keys.value == DungeonItem.option_anywhere:
        item_pool.extend(pool_bigkeys(world))
        item_pool.append(TMCItem.BIG_KEY_TOD)
    if world.options.dungeon_small_keys.value == DungeonItem.option_anywhere:
        item_pool.extend(pool_smallkeys(world))
    if world.options.dungeon_compasses.value == DungeonItem.option_anywhere:
        item_pool.extend(pool_compass(world))
    if world.options.dungeon_maps.value == DungeonItem.option_anywhere:
        item_pool.extend(pool_dungeonmaps(world))

    # ToD is stupid, need to place the big key manually
    if world.options.dungeon_big_keys.value == DungeonItem.option_own_dungeon and \
       TMCItem.BIG_KEY_TOD not in world.options.start_inventory_from_pool.value.keys():
        location = world.random.choice([TMCLocation.DROPLETS_ENTRANCE_B2_EAST_ICEBLOCK,
                                        TMCLocation.DROPLETS_ENTRANCE_B2_WEST_ICEBLOCK])
        world.get_location(location).place_locked_item(world.create_item(TMCItem.BIG_KEY_TOD))

    if not world.options.random_bottle_contents.value:
        item_pool.extend(pool_bottles())
    else:
        selected_bottles = []
        random_bottles = pool_random_bottle_contents()
        world.random.shuffle(random_bottles)

        for i in range(0, 4):
            selected_bottles.append(random_bottles[i])

        item_pool.extend(selected_bottles)

    if world.options.shuffle_elements.value is ShuffleElements.option_anywhere:
        item_pool.extend(pool_elements())

    return [world.create_item(item) for item in item_pool]


def get_pre_fill_pool(world: "MinishCapWorld") -> list[MinishCapItem]:
    start_inv = world.options.start_inventory_from_pool.value
    pre_fill_pool = []

    if not world.options.dungeon_big_keys.value == DungeonItem.option_anywhere:
        pre_fill_pool.extend(pool_bigkeys(world))
        # ToD big key never added to pre_fill pool, always placed by get_item_pool
    if not world.options.dungeon_small_keys.value == DungeonItem.option_anywhere:
        pre_fill_pool.extend(pool_smallkeys(world))
    if not world.options.dungeon_compasses.value == DungeonItem.option_anywhere:
        pre_fill_pool.extend(pool_compass(world))
    if not world.options.dungeon_maps.value == DungeonItem.option_anywhere:
        pre_fill_pool.extend(pool_dungeonmaps(world))

    # Keep track of items that need to be removed due to start_inv
    known_start_inv = {}

    def keep_item(s):
        known_start_inv[s] = known_start_inv.get(s, 0) + 1
        return s not in start_inv or known_start_inv[s] > start_inv[s]

    return [world.create_item(item) for item in pre_fill_pool if keep_item(item)]


item_table: dict[str, ItemData] = {
    # TMCItem.SMITHS_SWORD: ItemData(ItemClassification.progression, (0x01, 0x00)),
    # TMCItem.WHITE_SWORD_GREEN: ItemData(ItemClassification.progression, (0x02, 0x00)),
    # TMCItem.WHITE_SWORD_RED: ItemData(ItemClassification.progression, (0x03, 0x00)),
    # TMCItem.WHITE_SWORD_BLUE: ItemData(ItemClassification.progression, (0x04, 0x00)),
    # TMCItem.FOUR_SWORD: ItemData(ItemClassification.progression, (0x06, 0x00)),
    TMCItem.PROGRESSIVE_SWORD: ItemData(ItemClassification.progression, (0x01, 0x00)),
    TMCItem.BOMB: ItemData(ItemClassification.progression, (0x07, 0x00)),
    TMCItem.REMOTE_BOMB: ItemData(ItemClassification.useful, (0x08, 0x00)),
    # TMCItem.BOW: ItemData(ItemClassification.progression, (0x09, 0x00)),
    # TMCItem.LIGHT_ARROW: ItemData(ItemClassification.progression, (0x0A, 0x00)),
    TMCItem.PROGRESSIVE_BOW: ItemData(ItemClassification.progression, (0x09, 0x00)),
    # TMCItem.BOOMERANG: ItemData(ItemClassification.progression, (0x0B, 0x00)),
    # TMCItem.MAGIC_BOOMERANG: ItemData(ItemClassification.progression, (0x0C, 0x00)),
    TMCItem.PROGRESSIVE_BOOMERANG: ItemData(ItemClassification.progression, (0x0B, 0x00)),
    # TMCItem.SHIELD: ItemData(ItemClassification.progression, (0x0D, 0x00)),
    # TMCItem.MIRROR_SHIELD: ItemData(ItemClassification.progression, (0x0E, 0x00)),
    TMCItem.PROGRESSIVE_SHIELD: ItemData(ItemClassification.progression, (0x0D, 0x00)),
    TMCItem.LANTERN: ItemData(ItemClassification.progression, (0x0F, 0x00)),
    # TMCItem.LANTERN_OFF: ItemData(ItemClassification.progression, (0x10, 0x00)),
    TMCItem.GUST_JAR: ItemData(ItemClassification.progression, (0x11, 0x00)),
    TMCItem.CANE_OF_PACCI: ItemData(ItemClassification.progression, (0x12, 0x00)),
    TMCItem.MOLE_MITTS: ItemData(ItemClassification.progression, (0x13, 0x00)),
    TMCItem.ROCS_CAPE: ItemData(ItemClassification.progression, (0x14, 0x00)),
    TMCItem.PEGASUS_BOOTS: ItemData(ItemClassification.progression, (0x15, 0x00)),
    TMCItem.FIRE_ROD: ItemData(ItemClassification.progression, (0x16, 0x00)),
    TMCItem.OCARINA: ItemData(ItemClassification.progression, (0x17, 0x00)),
    # TMCItem.DEBUG_BOOK: ItemData(ItemClassification.progression, (0x18, 0x00)),
    # TMCItem.DEBUG_MUSHROOM: ItemData(ItemClassification.progression, (0x19, 0x00)),
    # TMCItem.DEBUG_FLIPPERS: ItemData(ItemClassification.progression, (0x1A, 0x00)),
    # TMCItem.DEBUG_LANTERN: ItemData(ItemClassification.progression, (0x1B, 0x00)),
    TMCItem.BOTTLE_1: ItemData(ItemClassification.progression, (0x1C, 0x00)),
    TMCItem.BOTTLE_2: ItemData(ItemClassification.progression, (0x1D, 0x00)),
    TMCItem.BOTTLE_3: ItemData(ItemClassification.progression, (0x1E, 0x00)),
    TMCItem.BOTTLE_4: ItemData(ItemClassification.progression, (0x1F, 0x00)),
    TMCItem.EMPTY_BOTTLE: ItemData(ItemClassification.progression, (0x1C, 0x20)),
    TMCItem.LON_LON_BUTTER: ItemData(ItemClassification.progression, (0x1C, 0x21)),
    TMCItem.LON_LON_MILK: ItemData(ItemClassification.progression, (0x1C, 0x22)),
    TMCItem.LON_LON_MILK_HALF: ItemData(ItemClassification.progression, (0x1C, 0x23)),
    TMCItem.RED_POTION: ItemData(ItemClassification.progression, (0x1C, 0x24)),
    TMCItem.BLUE_POTION: ItemData(ItemClassification.progression, (0x1C, 0x25)),
    TMCItem.WATER: ItemData(ItemClassification.progression, (0x1C, 0x26)),
    TMCItem.MINERAL_WATER: ItemData(ItemClassification.progression, (0x1C, 0x27)),
    TMCItem.BOTTLED_FAIRY: ItemData(ItemClassification.progression, (0x1C, 0x28)),
    TMCItem.RED_PICOLYTE: ItemData(ItemClassification.progression, (0x1C, 0x29)),
    TMCItem.ORANGE_PICOLYTE: ItemData(ItemClassification.progression, (0x1C, 0x2A)),
    TMCItem.YELLOW_PICOLYTE: ItemData(ItemClassification.progression, (0x1C, 0x2B)),
    TMCItem.GREEN_PICOLYTE: ItemData(ItemClassification.progression, (0x1C, 0x2C)),
    TMCItem.BLUE_PICOLYTE: ItemData(ItemClassification.progression, (0x1C, 0x2D)),
    TMCItem.WHITE_PICOLYTE: ItemData(ItemClassification.progression, (0x1C, 0x2E)),
    TMCItem.NAYRU_CHARM: ItemData(ItemClassification.progression, (0x1C, 0x2F)),
    TMCItem.FARORE_CHARM: ItemData(ItemClassification.progression, (0x1C, 0x30)),
    TMCItem.DINS_CHARM: ItemData(ItemClassification.progression, (0x1C, 0x31)),
    # TMCItem.UNUSED: ItemData(ItemClassification.progression, (0x32, 0x00)),
    # TMCItem.UNUSED: ItemData(ItemClassification.progression, (0x33, 0x00)),
    TMCItem.SMITH_SWORD_QUEST: ItemData(ItemClassification.filler, (0x34, 0x00)),
    TMCItem.BROKEN_PICORI_BLADE: ItemData(ItemClassification.filler, (0x35, 0x00)),
    TMCItem.DOG_FOOD: ItemData(ItemClassification.progression, (0x36, 0x00)),
    TMCItem.LONLON_KEY: ItemData(ItemClassification.progression, (0x37, 0x00)),
    TMCItem.WAKEUP_MUSHROOM: ItemData(ItemClassification.progression, (0x38, 0x00)),
    TMCItem.RED_BOOK: ItemData(ItemClassification.progression, (0x39, 0x00)),
    TMCItem.GREEN_BOOK: ItemData(ItemClassification.progression, (0x3A, 0x00)),
    TMCItem.BLUE_BOOK: ItemData(ItemClassification.progression, (0x3B, 0x00)),
    TMCItem.GRAVEYARD_KEY: ItemData(ItemClassification.progression, (0x3C, 0x00)),
    TMCItem.TINGLE_TROPHY: ItemData(ItemClassification.progression, (0x3D, 0x00)),
    TMCItem.CARLOV_MEDAL: ItemData(ItemClassification.progression, (0x3E, 0x00)),
    TMCItem.SHELLS: ItemData(ItemClassification.progression, (0x3F, 0x00)),
    TMCItem.EARTH_ELEMENT: ItemData(ItemClassification.progression_skip_balancing, (0x40, 0x00)),
    TMCItem.FIRE_ELEMENT: ItemData(ItemClassification.progression_skip_balancing, (0x41, 0x00)),
    TMCItem.WATER_ELEMENT: ItemData(ItemClassification.progression_skip_balancing, (0x42, 0x00)),
    TMCItem.WIND_ELEMENT: ItemData(ItemClassification.progression_skip_balancing, (0x43, 0x00)),
    TMCItem.GRIP_RING: ItemData(ItemClassification.progression, (0x44, 0x00)),
    TMCItem.POWER_BRACELETS: ItemData(ItemClassification.progression, (0x45, 0x00)),
    TMCItem.FLIPPERS: ItemData(ItemClassification.progression, (0x46, 0x00)),
    TMCItem.HYRULE_MAP: ItemData(ItemClassification.progression, (0x47, 0x00)),
    TMCItem.SPIN_ATTACK: ItemData(ItemClassification.progression, (0x48, 0x00)),
    TMCItem.ROLL_ATTACK: ItemData(ItemClassification.progression, (0x49, 0x00)),
    TMCItem.DASH_ATTACK: ItemData(ItemClassification.progression, (0x4A, 0x00)),
    TMCItem.ROCK_BREAKER: ItemData(ItemClassification.progression, (0x4B, 0x00)),
    TMCItem.SWORD_BEAM: ItemData(ItemClassification.progression, (0x4C, 0x00)),
    TMCItem.GREATSPIN: ItemData(ItemClassification.progression, (0x4D, 0x00)),
    TMCItem.DOWNTHRUST: ItemData(ItemClassification.progression, (0x4E, 0x00)),
    TMCItem.PERIL_BEAM: ItemData(ItemClassification.progression, (0x4F, 0x00)),
    TMCItem.RUPEES_1: ItemData(ItemClassification.filler, (0x54, 0x00)),
    TMCItem.RUPEES_5: ItemData(ItemClassification.filler, (0x55, 0x00)),
    TMCItem.RUPEES_20: ItemData(ItemClassification.filler, (0x56, 0x00)),
    TMCItem.RUPEES_50: ItemData(ItemClassification.filler, (0x57, 0x00)),
    TMCItem.RUPEES_100: ItemData(ItemClassification.filler, (0x58, 0x00)),
    TMCItem.RUPEES_200: ItemData(ItemClassification.filler, (0x59, 0x00)),
    # TMCItem.UNUSED: ItemData(ItemClassification.progression, (0x5A, 0x00)),
    TMCItem.JABBER_NUT: ItemData(ItemClassification.progression, (0x5B, 0x00)),
    TMCItem.KINSTONE: ItemData(ItemClassification.progression, (0x5C, 0x00)),
    TMCItem.KINSTONE_GOLD_CLOUD: ItemData(ItemClassification.progression, (0x5C, 0x65)),
    TMCItem.KINSTONE_GOLD_SWAMP: ItemData(ItemClassification.progression, (0x5C, 0x6A)),
    TMCItem.KINSTONE_GOLD_FALLS: ItemData(ItemClassification.progression, (0x5C, 0x6D)),
    TMCItem.KINSTONE_RED_W: ItemData(ItemClassification.progression, (0x5C, 0x6E)),
    TMCItem.KINSTONE_RED_ANGLE: ItemData(ItemClassification.progression, (0x5C, 0x6F)),
    TMCItem.KINSTONE_RED_E: ItemData(ItemClassification.progression, (0x5C, 0x70)),
    TMCItem.KINSTONE_BLUE_L: ItemData(ItemClassification.progression, (0x5C, 0x71)),
    TMCItem.KINSTONE_BLUE_6: ItemData(ItemClassification.progression, (0x5C, 0x72)),
    TMCItem.KINSTONE_GREEN_ANGLE: ItemData(ItemClassification.progression, (0x5C, 0x73)),
    TMCItem.KINSTONE_GREEN_SQUARE: ItemData(ItemClassification.progression, (0x5C, 0x74)),
    TMCItem.KINSTONE_GREEN_P: ItemData(ItemClassification.progression, (0x5C, 0x75)),
    TMCItem.BOMB_REFILL_5: ItemData(ItemClassification.filler, (0x5D, 0x00)),
    TMCItem.ARROW_REFILL_5: ItemData(ItemClassification.filler, (0x5E, 0x00)),
    TMCItem.HEART_REFILL: ItemData(ItemClassification.filler, (0x5F, 0x00)),
    TMCItem.FAIRY_REFILL: ItemData(ItemClassification.filler, (0x60, 0x00)),
    TMCItem.SHELLS_30: ItemData(ItemClassification.progression, (0x61, 0x00)),
    TMCItem.HEART_CONTAINER: ItemData(DEPRIORITIZED_FALLBACK, (0x62, 0x00)),
    TMCItem.HEART_PIECE: ItemData(DEPRIORITIZED_FALLBACK, (0x63, 0x00)),
    TMCItem.BIG_WALLET: ItemData(ItemClassification.progression, (0x64, 0x00)),
    TMCItem.BOMB_BAG: ItemData(ItemClassification.progression, (0x65, 0x00)),
    TMCItem.QUIVER: ItemData(ItemClassification.useful, (0x66, 0x00)),
    TMCItem.KINSTONE_BAG: ItemData(ItemClassification.progression, (0x67, 0x00)),
    TMCItem.BRIOCHE: ItemData(ItemClassification.filler, (0x68, 0x00)),
    TMCItem.CROISSANT: ItemData(ItemClassification.filler, (0x69, 0x00)),
    TMCItem.PIE: ItemData(ItemClassification.filler, (0x6A, 0x00)),
    TMCItem.CAKE: ItemData(ItemClassification.filler, (0x6B, 0x00)),
    TMCItem.BOMB_REFILL_10: ItemData(ItemClassification.filler, (0x6C, 0x00)),
    TMCItem.BOMB_REFILL_30: ItemData(ItemClassification.filler, (0x6D, 0x00)),
    TMCItem.ARROW_REFILL_10: ItemData(ItemClassification.filler, (0x6E, 0x00)),
    TMCItem.ARROW_REFILL_30: ItemData(ItemClassification.filler, (0x6F, 0x00)),
    TMCItem.BOW_BUTTERFLY: ItemData(ItemClassification.useful, (0x70, 0x00)),
    TMCItem.DIG_BUTTERFLY: ItemData(ItemClassification.useful, (0x71, 0x00)),
    TMCItem.SWIM_BUTTERFLY: ItemData(ItemClassification.useful, (0x72, 0x00)),
    TMCItem.FAST_SPIN_SCROLL: ItemData(ItemClassification.progression, (0x73, 0x00)),
    TMCItem.FAST_SPLIT_SCROLL: ItemData(ItemClassification.progression, (0x74, 0x00)),
    TMCItem.LONG_SPIN: ItemData(ItemClassification.progression, (0x75, 0x00)),

    TMCItem.TRAP_ICE: ItemData(ItemClassification.trap, (0x1B, 0x0)),
    TMCItem.TRAP_FIRE: ItemData(ItemClassification.trap, (0x1B, 0x1)),
    TMCItem.TRAP_ZAP: ItemData(ItemClassification.trap, (0x1B, 0x2)),
    TMCItem.TRAP_BOMB: ItemData(ItemClassification.trap, (0x1B, 0x3)),
    TMCItem.TRAP_MONEY: ItemData(ItemClassification.trap, (0x1B, 0x4)),
    TMCItem.TRAP_STINK: ItemData(ItemClassification.trap, (0x1B, 0x5)),
    TMCItem.TRAP_ROPE: ItemData(ItemClassification.trap, (0x1B, 0x6)),
    TMCItem.TRAP_BAT: ItemData(ItemClassification.trap, (0x1B, 0x7)),
    TMCItem.TRAP_LIKE: ItemData(ItemClassification.trap, (0x1B, 0x8)),
    TMCItem.TRAP_CURSE: ItemData(ItemClassification.trap, (0x1B, 0x9)),

    TMCItem.DUNGEON_MAP_DWS: ItemData(ItemClassification.useful, (0x50, 0x18)),
    TMCItem.DUNGEON_MAP_COF: ItemData(ItemClassification.useful, (0x50, 0x19)),
    TMCItem.DUNGEON_MAP_FOW: ItemData(ItemClassification.useful, (0x50, 0x1A)),
    TMCItem.DUNGEON_MAP_TOD: ItemData(ItemClassification.useful, (0x50, 0x1B)),
    TMCItem.DUNGEON_MAP_POW: ItemData(ItemClassification.useful, (0x50, 0x1C)),
    TMCItem.DUNGEON_MAP_DHC: ItemData(ItemClassification.useful, (0x50, 0x1D)),
    TMCItem.DUNGEON_COMPASS_DWS: ItemData(ItemClassification.useful, (0x51, 0x18)),
    TMCItem.DUNGEON_COMPASS_COF: ItemData(ItemClassification.useful, (0x51, 0x19)),
    TMCItem.DUNGEON_COMPASS_FOW: ItemData(ItemClassification.useful, (0x51, 0x1A)),
    TMCItem.DUNGEON_COMPASS_TOD: ItemData(ItemClassification.useful, (0x51, 0x1B)),
    TMCItem.DUNGEON_COMPASS_POW: ItemData(ItemClassification.useful, (0x51, 0x1C)),
    TMCItem.DUNGEON_COMPASS_DHC: ItemData(ItemClassification.useful, (0x51, 0x1D)),
    TMCItem.BIG_KEY_DWS: ItemData(ItemClassification.progression, (0x52, 0x18)),
    TMCItem.BIG_KEY_COF: ItemData(ItemClassification.progression, (0x52, 0x19)),
    TMCItem.BIG_KEY_FOW: ItemData(ItemClassification.progression, (0x52, 0x1A)),
    TMCItem.BIG_KEY_TOD: ItemData(ItemClassification.progression, (0x52, 0x1B)),
    TMCItem.BIG_KEY_POW: ItemData(ItemClassification.progression, (0x52, 0x1C)),
    TMCItem.BIG_KEY_DHC: ItemData(ItemClassification.progression, (0x52, 0x1D)),
    TMCItem.SMALL_KEY_DWS: ItemData(ItemClassification.progression, (0x53, 0x18)),
    TMCItem.SMALL_KEY_COF: ItemData(ItemClassification.progression, (0x53, 0x19)),
    TMCItem.SMALL_KEY_FOW: ItemData(ItemClassification.progression, (0x53, 0x1A)),
    TMCItem.SMALL_KEY_TOD: ItemData(ItemClassification.progression, (0x53, 0x1B)),
    TMCItem.SMALL_KEY_POW: ItemData(ItemClassification.progression, (0x53, 0x1C)),
    TMCItem.SMALL_KEY_DHC: ItemData(ItemClassification.progression, (0x53, 0x1D)),
    TMCItem.SMALL_KEY_RC: ItemData(ItemClassification.progression, (0x53, 0x1E)),
}

item_frequencies: dict[str, int] = {
    TMCItem.RUPEES_1: 36, TMCItem.RUPEES_5: 49, TMCItem.RUPEES_20: 53,
    TMCItem.RUPEES_50: 25, TMCItem.RUPEES_100: 18, TMCItem.RUPEES_200: 15,

    TMCItem.HEART_REFILL: 29,

    TMCItem.BOMB_REFILL_5: 34, TMCItem.BOMB_REFILL_10: 22,
    TMCItem.BOMB_REFILL_30: 16,

    TMCItem.ARROW_REFILL_5: 34, TMCItem.ARROW_REFILL_10: 22,
    TMCItem.ARROW_REFILL_30: 16,
}

trap_frequencies: dict[str, int] = {
    TMCItem.TRAP_ICE: 10,
    TMCItem.TRAP_FIRE: 10,
    TMCItem.TRAP_ZAP: 10,
    TMCItem.TRAP_BOMB: 10,
    TMCItem.TRAP_MONEY: 10,
    TMCItem.TRAP_STINK: 10,
    TMCItem.TRAP_ROPE: 10,
    TMCItem.TRAP_BAT: 10,
    TMCItem.TRAP_LIKE: 10,
    TMCItem.TRAP_CURSE: 10,
}


def get_filler_item_selection(world: "MinishCapWorld"):
    frequencies = item_frequencies.copy()
    if world.options.traps_enabled:
        traps = trap_frequencies.copy()
        frequencies.update(traps)
    return [name for name, count in frequencies.items() for _ in range(count)]


item_groups: dict[str, set[str]] = {
    "Spin Scrolls": {TMCItem.SPIN_ATTACK, TMCItem.GREATSPIN, TMCItem.FAST_SPIN_SCROLL, TMCItem.FAST_SPLIT_SCROLL,
                     TMCItem.LONG_SPIN},
    "Scrolls": {TMCItem.SPIN_ATTACK, TMCItem.ROLL_ATTACK, TMCItem.DASH_ATTACK, TMCItem.ROCK_BREAKER, TMCItem.SWORD_BEAM,
                TMCItem.GREATSPIN, TMCItem.DOWNTHRUST, TMCItem.PERIL_BEAM, TMCItem.FAST_SPIN_SCROLL,
                TMCItem.FAST_SPLIT_SCROLL, TMCItem.LONG_SPIN},
    "Elements": {TMCItem.EARTH_ELEMENT, TMCItem.FIRE_ELEMENT, TMCItem.WATER_ELEMENT, TMCItem.WIND_ELEMENT},
    "Health": {TMCItem.HEART_CONTAINER, TMCItem.HEART_PIECE},
    "Bottle": {TMCItem.EMPTY_BOTTLE, TMCItem.LON_LON_BUTTER, TMCItem.LON_LON_MILK, TMCItem.LON_LON_MILK_HALF,
               TMCItem.RED_POTION, TMCItem.BLUE_POTION, TMCItem.WATER, TMCItem.MINERAL_WATER, TMCItem.BOTTLED_FAIRY,
               TMCItem.RED_PICOLYTE, TMCItem.ORANGE_PICOLYTE, TMCItem.YELLOW_PICOLYTE, TMCItem.GREEN_PICOLYTE,
               TMCItem.BLUE_PICOLYTE, TMCItem.WHITE_PICOLYTE, TMCItem.NAYRU_CHARM, TMCItem.FARORE_CHARM,
               TMCItem.DINS_CHARM},
    "Sword": {TMCItem.PROGRESSIVE_SWORD},
    # "Sword": {TMCItem.PROGRESSIVE_SWORD, TMCItem.SMITHS_SWORD, TMCItem.WHITE_SWORD_GREEN, TMCItem.WHITE_SWORD_RED,
    #           TMCItem.WHITE_SWORD_BLUE, TMCItem.FOUR_SWORD},
    "Bow": {TMCItem.PROGRESSIVE_BOW},
    # "Bow": {TMCItem.PROGRESSIVE_BOW, TMCItem.BOW, TMCItem.LIGHT_ARROW},
    "Boomerang": {TMCItem.PROGRESSIVE_BOOMERANG},
    # "Boomerang": {TMCItem.PROGRESSIVE_BOOMERANG, TMCItem.BOOMERANG, TMCItem.MAGIC_BOOMERANG},
    "Shield": {TMCItem.PROGRESSIVE_SHIELD},
    # "Shield": {TMCItem.PROGRESSIVE_SHIELD, TMCItem.SHIELD, TMCItem.MIRROR_SHIELD},
    "Cape": {TMCItem.ROCS_CAPE},
    "Cane": {TMCItem.CANE_OF_PACCI},
    "Boots": {TMCItem.PEGASUS_BOOTS},
    "Rupees": {TMCItem.RUPEES_1, TMCItem.RUPEES_5, TMCItem.RUPEES_20, TMCItem.RUPEES_50, TMCItem.RUPEES_100,
               TMCItem.RUPEES_200},
    "Traps": {TMCItem.TRAP_ICE, TMCItem.TRAP_FIRE, TMCItem.TRAP_ZAP, TMCItem.TRAP_BOMB, TMCItem.TRAP_MONEY,
              TMCItem.TRAP_STINK, TMCItem.TRAP_ROPE, TMCItem.TRAP_BAT, TMCItem.TRAP_LIKE, TMCItem.TRAP_CURSE},
    "Kinstones": {TMCItem.KINSTONE_GOLD_CLOUD, TMCItem.KINSTONE_GOLD_SWAMP, TMCItem.KINSTONE_GOLD_FALLS,
                  TMCItem.KINSTONE_RED_W, TMCItem.KINSTONE_RED_ANGLE, TMCItem.KINSTONE_RED_E,
                  TMCItem.KINSTONE_BLUE_L, TMCItem.KINSTONE_BLUE_6,
                  TMCItem.KINSTONE_GREEN_ANGLE, TMCItem.KINSTONE_GREEN_SQUARE, TMCItem.KINSTONE_GREEN_P},
    "Gold Kinstones": {TMCItem.KINSTONE_GOLD_CLOUD, TMCItem.KINSTONE_GOLD_SWAMP, TMCItem.KINSTONE_GOLD_FALLS},
    "Red Kinstones": {TMCItem.KINSTONE_RED_W, TMCItem.KINSTONE_RED_ANGLE, TMCItem.KINSTONE_RED_E},
    "Blue Kinstones": {TMCItem.KINSTONE_BLUE_L, TMCItem.KINSTONE_BLUE_6},
    "Green Kinstones": {TMCItem.KINSTONE_GREEN_ANGLE, TMCItem.KINSTONE_GREEN_SQUARE, TMCItem.KINSTONE_GREEN_P},
    "Dungeon Items": {TMCItem.SMALL_KEY_DWS, TMCItem.SMALL_KEY_COF, TMCItem.SMALL_KEY_FOW, TMCItem.SMALL_KEY_TOD,
                      TMCItem.SMALL_KEY_POW, TMCItem.SMALL_KEY_DHC, TMCItem.SMALL_KEY_RC,
                      TMCItem.BIG_KEY_DWS, TMCItem.BIG_KEY_COF, TMCItem.BIG_KEY_FOW, TMCItem.BIG_KEY_TOD,
                      TMCItem.BIG_KEY_POW, TMCItem.BIG_KEY_DHC,
                      TMCItem.DUNGEON_MAP_DWS, TMCItem.DUNGEON_MAP_COF, TMCItem.DUNGEON_MAP_FOW,
                      TMCItem.DUNGEON_MAP_TOD, TMCItem.DUNGEON_MAP_POW, TMCItem.DUNGEON_MAP_DHC,
                      TMCItem.DUNGEON_COMPASS_DWS, TMCItem.DUNGEON_COMPASS_COF, TMCItem.DUNGEON_COMPASS_FOW,
                      TMCItem.DUNGEON_COMPASS_TOD, TMCItem.DUNGEON_COMPASS_POW, TMCItem.DUNGEON_COMPASS_DHC},
    "Small Keys": {TMCItem.SMALL_KEY_DWS, TMCItem.SMALL_KEY_COF, TMCItem.SMALL_KEY_FOW, TMCItem.SMALL_KEY_TOD,
                   TMCItem.SMALL_KEY_POW, TMCItem.SMALL_KEY_DHC, TMCItem.SMALL_KEY_RC},
    "Big Keys": {TMCItem.BIG_KEY_DWS, TMCItem.BIG_KEY_COF, TMCItem.BIG_KEY_FOW, TMCItem.BIG_KEY_TOD,
                 TMCItem.BIG_KEY_POW, TMCItem.BIG_KEY_DHC},
    "Keys": {TMCItem.SMALL_KEY_DWS, TMCItem.SMALL_KEY_COF, TMCItem.SMALL_KEY_FOW, TMCItem.SMALL_KEY_TOD,
             TMCItem.SMALL_KEY_POW, TMCItem.SMALL_KEY_DHC, TMCItem.SMALL_KEY_RC,
             TMCItem.BIG_KEY_DWS, TMCItem.BIG_KEY_COF, TMCItem.BIG_KEY_FOW, TMCItem.BIG_KEY_TOD,
             TMCItem.BIG_KEY_POW, TMCItem.BIG_KEY_DHC},
    "Maps": {TMCItem.DUNGEON_MAP_DWS, TMCItem.DUNGEON_MAP_COF, TMCItem.DUNGEON_MAP_FOW, TMCItem.DUNGEON_MAP_TOD,
             TMCItem.DUNGEON_MAP_POW, TMCItem.DUNGEON_MAP_DHC},
    "Compasses": {TMCItem.DUNGEON_COMPASS_DWS, TMCItem.DUNGEON_COMPASS_COF, TMCItem.DUNGEON_COMPASS_FOW,
                  TMCItem.DUNGEON_COMPASS_TOD, TMCItem.DUNGEON_COMPASS_POW, TMCItem.DUNGEON_COMPASS_DHC},
    "DWS Items": {TMCItem.DUNGEON_MAP_DWS, TMCItem.DUNGEON_COMPASS_DWS, TMCItem.BIG_KEY_DWS, TMCItem.SMALL_KEY_DWS},
    "DWS Keys": {TMCItem.BIG_KEY_DWS, TMCItem.SMALL_KEY_DWS},
    "CoF Items": {TMCItem.DUNGEON_MAP_COF, TMCItem.DUNGEON_COMPASS_COF, TMCItem.BIG_KEY_COF, TMCItem.SMALL_KEY_COF},
    "CoF Keys": {TMCItem.BIG_KEY_COF, TMCItem.SMALL_KEY_COF},
    "FoW Items": {TMCItem.DUNGEON_MAP_FOW, TMCItem.DUNGEON_COMPASS_FOW, TMCItem.BIG_KEY_FOW, TMCItem.SMALL_KEY_FOW},
    "FoW Keys": {TMCItem.BIG_KEY_FOW, TMCItem.SMALL_KEY_FOW},
    "ToD Items": {TMCItem.DUNGEON_MAP_TOD, TMCItem.DUNGEON_COMPASS_TOD, TMCItem.BIG_KEY_TOD, TMCItem.SMALL_KEY_TOD},
    "ToD Keys": {TMCItem.BIG_KEY_TOD, TMCItem.SMALL_KEY_TOD},
    "PoW Items": {TMCItem.DUNGEON_MAP_POW, TMCItem.DUNGEON_COMPASS_POW, TMCItem.BIG_KEY_POW, TMCItem.SMALL_KEY_POW},
    "PoW Keys": {TMCItem.BIG_KEY_POW, TMCItem.SMALL_KEY_POW},
    "DHC Items": {TMCItem.DUNGEON_MAP_DHC, TMCItem.DUNGEON_COMPASS_DHC, TMCItem.BIG_KEY_DHC, TMCItem.SMALL_KEY_DHC},
    "DHC Keys": {TMCItem.BIG_KEY_DHC, TMCItem.SMALL_KEY_DHC},
}
