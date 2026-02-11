import typing

from BaseClasses import Item, ItemClassification
from .Names import ItemName

class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classsification: ItemClassification
    quantity: int = 1

STARTING_ID = 0xBF1000

class DKCItem(Item):
    game = "Donkey Kong Country"

# Item tables
worlds_table = {
    ItemName.kongo_jungle:          ItemData(STARTING_ID + 0x0000, ItemClassification.progression | ItemClassification.useful),
    ItemName.monkey_mines:          ItemData(STARTING_ID + 0x0001, ItemClassification.progression | ItemClassification.useful),
    ItemName.vine_valley:           ItemData(STARTING_ID + 0x0002, ItemClassification.progression | ItemClassification.useful),
    ItemName.gorilla_glacier:       ItemData(STARTING_ID + 0x0003, ItemClassification.progression | ItemClassification.useful),
    ItemName.kremkroc_industries:   ItemData(STARTING_ID + 0x0004, ItemClassification.progression | ItemClassification.useful),
    ItemName.chimp_caverns:         ItemData(STARTING_ID + 0x0005, ItemClassification.progression | ItemClassification.useful),
}

mcguffin_table = {
    ItemName.boss_token:            ItemData(STARTING_ID + 0x000F, ItemClassification.progression_skip_balancing),
}

progression_table = {
    ItemName.donkey:                ItemData(STARTING_ID + 0x0010, ItemClassification.progression | ItemClassification.useful),
    ItemName.diddy:                 ItemData(STARTING_ID + 0x0011, ItemClassification.progression | ItemClassification.useful),
    ItemName.carry:                 ItemData(STARTING_ID + 0x0012, ItemClassification.progression),
    ItemName.swim:                  ItemData(STARTING_ID + 0x0013, ItemClassification.progression),
    ItemName.roll:                  ItemData(STARTING_ID + 0x0014, ItemClassification.progression),
    ItemName.climb:                 ItemData(STARTING_ID + 0x0015, ItemClassification.progression),
    ItemName.slap:                  ItemData(STARTING_ID + 0x0016, ItemClassification.progression),
    ItemName.kannons:               ItemData(STARTING_ID + 0x0017, ItemClassification.progression),
    ItemName.switches:              ItemData(STARTING_ID + 0x0018, ItemClassification.progression),
    ItemName.minecart:              ItemData(STARTING_ID + 0x0019, ItemClassification.progression),
    ItemName.winky:                 ItemData(STARTING_ID + 0x001A, ItemClassification.progression_deprioritized),
    ItemName.expresso:              ItemData(STARTING_ID + 0x001B, ItemClassification.progression),
    ItemName.rambi:                 ItemData(STARTING_ID + 0x001C, ItemClassification.progression),
    ItemName.enguarde:              ItemData(STARTING_ID + 0x001D, ItemClassification.progression_deprioritized),
    ItemName.squawks:               ItemData(STARTING_ID + 0x001E, ItemClassification.progression_deprioritized),
    ItemName.tires:                 ItemData(STARTING_ID + 0x001F, ItemClassification.progression),
    ItemName.platforms:             ItemData(STARTING_ID + 0x0020, ItemClassification.progression),
}

misc_table = {
    ItemName.red_balloon:           ItemData(STARTING_ID + 0x0031, ItemClassification.filler),
    ItemName.dk_barrel:             ItemData(STARTING_ID + 0x0032, ItemClassification.filler),
}

extra_table = {
    ItemName.extractinator:         ItemData(STARTING_ID + 0x0033, ItemClassification.useful),
    ItemName.radar:                 ItemData(STARTING_ID + 0x0034, ItemClassification.useful),
    ItemName.glitched:              ItemData(None, ItemClassification.progression_skip_balancing),
}

trap_table = {
    ItemName.nut_trap:              ItemData(STARTING_ID + 0x0080, ItemClassification.trap),
    ItemName.army_trap:             ItemData(STARTING_ID + 0x0081, ItemClassification.trap),
    ItemName.jump_trap:             ItemData(STARTING_ID + 0x0082, ItemClassification.trap),
    ItemName.bonus_trap:            ItemData(STARTING_ID + 0x0083, ItemClassification.trap),
    ItemName.sticky_floor_trap:     ItemData(STARTING_ID + 0x0084, ItemClassification.trap),
    ItemName.stun_trap:             ItemData(STARTING_ID + 0x0085, ItemClassification.trap),
    ItemName.ice_trap:              ItemData(STARTING_ID + 0x0086, ItemClassification.trap),
}

trap_name_to_value: typing.Dict[str, int] = {
    # Our native Traps
    ItemName.nut_trap:              STARTING_ID + 0x0080,
    ItemName.army_trap:             STARTING_ID + 0x0081,
    ItemName.jump_trap:             STARTING_ID + 0x0082,
    ItemName.bonus_trap:            STARTING_ID + 0x0083,
    ItemName.sticky_floor_trap:     STARTING_ID + 0x0084,
    ItemName.stun_trap:             STARTING_ID + 0x0085,
    ItemName.ice_trap:              STARTING_ID + 0x0086,

    # Common other trap names
    "Spring Trap":          STARTING_ID + 0x0082,  # Jump Trap
    "Eject Ability":        STARTING_ID + 0x0082,  # Jump Trap
    "Hiccup Trap":          STARTING_ID + 0x0082,  # Jump Trap
    "Ghost":                STARTING_ID + 0x0081,  # Army Trap
    "Police Trap":          STARTING_ID + 0x0081,  # Army Trap
    "Gooey Trap":           STARTING_ID + 0x0081,  # Army Trap
    "Buyon Trap":           STARTING_ID + 0x0080,  # Nut Trap
    "Thwimp Trap":          STARTING_ID + 0x0080,  # Nut Trap
    "TNT Barrel Trap":      STARTING_ID + 0x0080,  # Nut Trap
    "Bomb Trap":            STARTING_ID + 0x0080,  # Nut Trap
    "Cutscene Trap":        STARTING_ID + 0x0083,  # Animal Bonus Trap
    "Pong Trap":            STARTING_ID + 0x0083,  # Animal Bonus Trap
    "Pinball Trap":         STARTING_ID + 0x0083,  # Animal Bonus Trap
    "Snake Trap":           STARTING_ID + 0x0083,  # Animal Bonus Trap
    "Honey Trap":           STARTING_ID + 0x0084,  # Sticky Floor Trap
    "Freeze Trap":          STARTING_ID + 0x0085,  # Stun Trap
    "Frozen Trap":          STARTING_ID + 0x0085,  # Stun Trap
    "Paralyze Trap":        STARTING_ID + 0x0085,  # Stun Trap
    "Chaos Control Trap":   STARTING_ID + 0x0085,  # Stun Trap
    "Bonk Trap":            STARTING_ID + 0x0085,  # Stun Trap
    "Banana Trap":          STARTING_ID + 0x0086,  # Ice Trap
}

trap_value_to_name: typing.Dict[int, str] = {
    STARTING_ID + 0x0080: ItemName.nut_trap,
    STARTING_ID + 0x0081: ItemName.army_trap,
    STARTING_ID + 0x0082: ItemName.jump_trap,
    STARTING_ID + 0x0083: ItemName.bonus_trap,
    STARTING_ID + 0x0084: ItemName.sticky_floor_trap,
    STARTING_ID + 0x0085: ItemName.stun_trap,
    STARTING_ID + 0x0086: ItemName.ice_trap,
}

item_groups = {
    "Worlds": {
        ItemName.kongo_jungle,
        ItemName.monkey_mines,
        ItemName.vine_valley,
        ItemName.gorilla_glacier,
        ItemName.kremkroc_industries,
        ItemName.chimp_caverns,
    },
    "Abilities": {
        ItemName.carry,
        ItemName.climb,
        ItemName.roll,
        ItemName.slap,
        ItemName.swim,
    },
    "Animals": {
        ItemName.rambi,
        ItemName.expresso,
        ItemName.enguarde,
        ItemName.winky,
        ItemName.squawks,
    },
    "Objects": {
        ItemName.kannons,
        ItemName.switches,
        ItemName.minecart,
        ItemName.tires,
        ItemName.platforms,
    }
}

option_name_to_world_name = {
    "Kongo Jungle": ItemName.kongo_jungle,
    "Monkey Mines": ItemName.monkey_mines,
    "Vine Valley": ItemName.vine_valley,
    "Gorilla Glacier": ItemName.gorilla_glacier,
    "Kremkroc Industries": ItemName.kremkroc_industries,
    "Chimp Caverns": ItemName.chimp_caverns,
}

items_that_open_checks = {
    ItemName.kongo_jungle: [
        ItemName.rambi,
        ItemName.swim,
    ],
    ItemName.monkey_mines: [
        ItemName.carry,
        ItemName.kannons,
        ItemName.tires,
    ],
    ItemName.vine_valley: [
        ItemName.climb,
        ItemName.kannons,
        ItemName.expresso,
    ],
    ItemName.gorilla_glacier: [
        ItemName.swim,
        ItemName.kannons,
        ItemName.expresso,
    ],
    ItemName.kremkroc_industries: [
        ItemName.climb,
        ItemName.minecart,
        ItemName.platforms,
    ],
    ItemName.chimp_caverns: [
        ItemName.platforms,
        ItemName.climb,
    ],
}

item_table = {
    **mcguffin_table,
    **worlds_table,
    **progression_table,
    **misc_table,
    **extra_table,
    **trap_table,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}