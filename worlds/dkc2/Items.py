import typing

from BaseClasses import Item, ItemClassification
from .Names import ItemName

class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classsification: ItemClassification
    quantity: int = 1

STARTING_ID = 0xBF0000

class DKC2Item(Item):
    game = "Donkey Kong Country 2"

# Item tables
worlds_table = {
    ItemName.gangplank_galleon:     ItemData(STARTING_ID + 0x0001, ItemClassification.progression | ItemClassification.useful),
    ItemName.crocodile_cauldron:    ItemData(STARTING_ID + 0x0002, ItemClassification.progression | ItemClassification.useful),
    ItemName.krem_quay:             ItemData(STARTING_ID + 0x0003, ItemClassification.progression | ItemClassification.useful),
    ItemName.krazy_kremland:        ItemData(STARTING_ID + 0x0004, ItemClassification.progression | ItemClassification.useful),
    ItemName.gloomy_gulch:          ItemData(STARTING_ID + 0x0005, ItemClassification.progression | ItemClassification.useful),
    ItemName.krools_keep:           ItemData(STARTING_ID + 0x0006, ItemClassification.progression | ItemClassification.useful),
    ItemName.the_flying_krock:      ItemData(STARTING_ID + 0x0007, ItemClassification.progression | ItemClassification.useful),
}

mcguffin_table = {
    ItemName.boss_token:            ItemData(STARTING_ID + 0x002F, ItemClassification.progression_skip_balancing),
    ItemName.lost_world_rock:       ItemData(STARTING_ID + 0x0008, ItemClassification.progression_skip_balancing),
}

hints_table = {
    ItemName.dk_coin:               ItemData(STARTING_ID + 0x0009, ItemClassification.useful),
    ItemName.kremkoins:             ItemData(STARTING_ID + 0x000A, ItemClassification.useful),
}

lost_world_table = {
    ItemName.lost_world_cauldron:   ItemData(STARTING_ID + 0x000B, ItemClassification.progression | ItemClassification.useful),
    ItemName.lost_world_quay:       ItemData(STARTING_ID + 0x000C, ItemClassification.progression | ItemClassification.useful),
    ItemName.lost_world_kremland:   ItemData(STARTING_ID + 0x000D, ItemClassification.progression | ItemClassification.useful),
    ItemName.lost_world_gulch:      ItemData(STARTING_ID + 0x000E, ItemClassification.progression | ItemClassification.useful),
    ItemName.lost_world_keep:       ItemData(STARTING_ID + 0x000F, ItemClassification.progression | ItemClassification.useful),
}

progression_table = {
    ItemName.diddy:                 ItemData(STARTING_ID + 0x0010, ItemClassification.progression | ItemClassification.useful),
    ItemName.dixie:                 ItemData(STARTING_ID + 0x0011, ItemClassification.progression | ItemClassification.useful),
    ItemName.carry:                 ItemData(STARTING_ID + 0x0012, ItemClassification.progression),
    ItemName.climb:                 ItemData(STARTING_ID + 0x0013, ItemClassification.progression),
    ItemName.cling:                 ItemData(STARTING_ID + 0x0014, ItemClassification.progression),
    ItemName.cartwheel:             ItemData(STARTING_ID + 0x0015, ItemClassification.progression),
    ItemName.swim:                  ItemData(STARTING_ID + 0x0016, ItemClassification.progression),
    ItemName.team_attack:           ItemData(STARTING_ID + 0x0017, ItemClassification.progression),
    ItemName.helicopter_spin:       ItemData(STARTING_ID + 0x0018, ItemClassification.progression),
    ItemName.rambi:                 ItemData(STARTING_ID + 0x0019, ItemClassification.progression),
    ItemName.squawks:               ItemData(STARTING_ID + 0x001A, ItemClassification.progression),
    ItemName.enguarde:              ItemData(STARTING_ID + 0x001B, ItemClassification.progression),
    ItemName.squitter:              ItemData(STARTING_ID + 0x001C, ItemClassification.progression),
    ItemName.rattly:                ItemData(STARTING_ID + 0x001D, ItemClassification.progression),
    ItemName.clapper:               ItemData(STARTING_ID + 0x001E, ItemClassification.progression),
    ItemName.glimmer:               ItemData(STARTING_ID + 0x001F, ItemClassification.progression_deprioritized),
    ItemName.barrel_kannons:        ItemData(STARTING_ID + 0x0020, ItemClassification.progression),
    ItemName.barrel_exclamation:    ItemData(STARTING_ID + 0x0021, ItemClassification.progression),
    ItemName.barrel_kong:           ItemData(STARTING_ID + 0x0022, ItemClassification.progression),
    ItemName.barrel_warp:           ItemData(STARTING_ID + 0x0023, ItemClassification.useful),
    ItemName.barrel_control:        ItemData(STARTING_ID + 0x0024, ItemClassification.progression),
    ItemName.skull_kart:            ItemData(STARTING_ID + 0x0025, ItemClassification.progression),
}

misc_table = {
    ItemName.banana_coin:           ItemData(STARTING_ID + 0x0030, ItemClassification.filler),
    ItemName.red_balloon:           ItemData(STARTING_ID + 0x0031, ItemClassification.filler),
    ItemName.dk_barrel:             ItemData(STARTING_ID + 0x0032, ItemClassification.filler),
    ItemName.extractinator:         ItemData(STARTING_ID + 0x0033, ItemClassification.useful),
    ItemName.glitched:              ItemData(None, ItemClassification.progression_skip_balancing),
}

trap_table = {
    ItemName.freeze_trap:           ItemData(STARTING_ID + 0x0040, ItemClassification.trap),
    ItemName.reverse_trap:          ItemData(STARTING_ID + 0x0041, ItemClassification.trap),
    ItemName.honey_trap:            ItemData(STARTING_ID + 0x0042, ItemClassification.trap),
    ItemName.ice_trap:              ItemData(STARTING_ID + 0x0043, ItemClassification.trap),
    ItemName.tnt_barrel_trap:       ItemData(STARTING_ID + 0x0044, ItemClassification.trap),
    ItemName.damage_trap:           ItemData(STARTING_ID + 0x0045, ItemClassification.trap),
    ItemName.death_trap:            ItemData(STARTING_ID + 0x0046, ItemClassification.trap),
}

trap_name_to_value: typing.Dict[str, int] = {
    # Our native Traps
    ItemName.freeze_trap:       STARTING_ID + 0x0040,
    ItemName.reverse_trap:      STARTING_ID + 0x0041,
    ItemName.honey_trap:        STARTING_ID + 0x0042,
    ItemName.ice_trap:          STARTING_ID + 0x0043,
    ItemName.tnt_barrel_trap:   STARTING_ID + 0x0044,
    ItemName.damage_trap:       STARTING_ID + 0x0045,
    ItemName.death_trap:        STARTING_ID + 0x0046,

    # Common other trap names
    "Chaos Control Trap":   STARTING_ID + 0x0040,  # Freeze Trap
    "Confuse Trap":         STARTING_ID + 0x0041,  # Reverse Trap
    "Frozen Trap":          STARTING_ID + 0x0040,  # Freeze Trap
    "Paralyze Trap":        STARTING_ID + 0x0040,  # Freeze Trap
    "Stun Trap":            STARTING_ID + 0x0040,  # Freeze Trap
    "Reversal Trap":        STARTING_ID + 0x0041,  # Reverse Trap
    "Fuzzy Trap":           STARTING_ID + 0x0041,  # Reverse Trap
    "Confusion Trap":       STARTING_ID + 0x0041,  # Reverse Trap
    "Confound Trap":        STARTING_ID + 0x0041,  # Reverse Trap
    "Poison Trap":          STARTING_ID + 0x0045,  # Damage Trap 
    "Bee Trap":             STARTING_ID + 0x0042,  # Honey Trap 
    "Input Sequence Trap":  STARTING_ID + 0x0040,  # Freeze Trap
    "Thwimp Trap":          STARTING_ID + 0x0044,  # TNT Barrel Trap
    "Sticky Floor Trap":    STARTING_ID + 0x0042,  # Honey Trap 
    "Sticky Hands Trap":    STARTING_ID + 0x0042,  # Honey Trap 
    "Bomb":                 STARTING_ID + 0x0044,  # TNT Barrel Trap
    "Banana Trap":          STARTING_ID + 0x0043,  # Ice Trap
    "Gooey Bag":            STARTING_ID + 0x0044,  # TNT Barrel Trap
    "Posession Trap":       STARTING_ID + 0x0045,  # Damage Trap 
    "Ghost":                STARTING_ID + 0x0044,  # TNT Barrel Trap
    "Fire Trap":            STARTING_ID + 0x0044,  # TNT Barrel Trap
    "Army Trap":            STARTING_ID + 0x0044,  # TNT Barrel Trap
    "Nut Trap":             STARTING_ID + 0x0044,  # TNT Barrel Trap
    "Blue Balls Curse":     STARTING_ID + 0x0046,  # Instant Death Trap 
    "Electrocution Trap":   STARTING_ID + 0x0045,  # Damage Trap 
    "Iron Boots Trap":      STARTING_ID + 0x0042,  # Honey Trap 
    "Squash Trap":          STARTING_ID + 0x0045,  # Damage Trap 
    "Slow Trap":            STARTING_ID + 0x0042,  # Honey Trap 
    "Slowness Trap":        STARTING_ID + 0x0042,  # Honey Trap 
}

trap_value_to_name: typing.Dict[int, str] = {
    STARTING_ID + 0x0040: ItemName.freeze_trap,
    STARTING_ID + 0x0041: ItemName.reverse_trap,
    STARTING_ID + 0x0042: ItemName.honey_trap,
    STARTING_ID + 0x0043: ItemName.ice_trap,
    STARTING_ID + 0x0044: ItemName.tnt_barrel_trap,
    STARTING_ID + 0x0045: ItemName.damage_trap,
    STARTING_ID + 0x0046: ItemName.death_trap,
}

item_groups = {
    "Worlds": {
        ItemName.gangplank_galleon,
        ItemName.crocodile_cauldron,
        ItemName.krem_quay,
        ItemName.krazy_kremland,
        ItemName.gloomy_gulch,
        ItemName.krools_keep,
        ItemName.the_flying_krock,
    },
    "Lost World": {
        ItemName.lost_world_cauldron,
        ItemName.lost_world_quay,
        ItemName.lost_world_kremland,
        ItemName.lost_world_gulch,
        ItemName.lost_world_keep,
    },
    "Abilities": {
        ItemName.carry,
        ItemName.climb,
        ItemName.cling,
        ItemName.cartwheel,
        ItemName.swim,
        ItemName.team_attack,
        ItemName.helicopter_spin,
    },
    "Animals": {
        ItemName.rambi,
        ItemName.squawks,
        ItemName.enguarde,
        ItemName.squitter,
        ItemName.rattly,
        ItemName.clapper,
        ItemName.glimmer,
        ItemName.skull_kart,
    },
    "Barrels": {
        ItemName.barrel_kannons,
        ItemName.barrel_exclamation,
        ItemName.barrel_kong,
        ItemName.barrel_warp,
        ItemName.barrel_control,
    }
}

item_table = {
    **mcguffin_table,
    **worlds_table,
    **lost_world_table,
    **progression_table,
    **hints_table,
    **trap_table,
    **misc_table,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}