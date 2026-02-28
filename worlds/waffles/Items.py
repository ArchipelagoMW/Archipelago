import typing

from BaseClasses import Item, ItemClassification
from .Names import ItemName


class ItemData(typing.NamedTuple):
    code: typing.Optional[int] = None
    type: ItemClassification = ItemClassification.filler


class WaffleItem(Item):
    game: str = "SMW: Spicy Mycena Waffles"


# Separate tables for each type of item.
junk_table = {
    ItemName.one_coin:                  ItemData(0xBC0017),
    ItemName.five_coins:                ItemData(0xBC0018),
    ItemName.ten_coins:                 ItemData(0xBC0019),
    ItemName.fifty_coins:               ItemData(0xBC001A),
    ItemName.heart_inventory:           ItemData(0xBC0001),
    ItemName.mushroom_inventory:        ItemData(0xBC0040),
    ItemName.fire_flower_inventory:     ItemData(0xBC0041),
    ItemName.feather_inventory:         ItemData(0xBC0042),
    ItemName.star_inventory:            ItemData(0xBC0043),
    ItemName.green_yoshi_inventory:     ItemData(0xBC0044),
    ItemName.red_yoshi_inventory:       ItemData(0xBC0045),
    ItemName.blue_yoshi_inventory:      ItemData(0xBC0046),
    ItemName.yellow_yoshi_inventory:    ItemData(0xBC0047),
    ItemName.trap_repellent:            ItemData(0xBC0048, ItemClassification.useful),
}

collectable_table = {
    ItemName.yoshi_egg:       ItemData(0xBC0002, ItemClassification.progression_deprioritized_skip_balancing | ItemClassification.useful),
}

upgrade_table = {
    ItemName.run:                   ItemData(0xBC0003, ItemClassification.progression),
    ItemName.carry:                 ItemData(0xBC0004, ItemClassification.progression | ItemClassification.useful),
    ItemName.swim:                  ItemData(0xBC0005, ItemClassification.progression),
    ItemName.spin_jump:             ItemData(0xBC0006, ItemClassification.progression),
    ItemName.climb:                 ItemData(0xBC0007, ItemClassification.progression),
    ItemName.yoshi:                 ItemData(0xBC0008, ItemClassification.progression | ItemClassification.useful),
    ItemName.p_switch:              ItemData(0xBC0009, ItemClassification.progression),
    ItemName.progressive_powerup:   ItemData(0xBC000A, ItemClassification.progression | ItemClassification.useful),
    ItemName.p_balloon:             ItemData(0xBC000B, ItemClassification.progression),
    ItemName.super_star_active:     ItemData(0xBC000D, ItemClassification.progression_deprioritized),
    ItemName.special_world_clear:   ItemData(0xBC001B, ItemClassification.progression),
    ItemName.extra_defense:         ItemData(0xBC0020, ItemClassification.useful),
    ItemName.midway_point:          ItemData(0xBC0021, ItemClassification.progression),
    ItemName.better_timer:          ItemData(0xBC0022, ItemClassification.useful),
    ItemName.item_box:              ItemData(0xBC0023, ItemClassification.useful),
    ItemName.progressive_yoshi:     ItemData(0xBC0024, ItemClassification.progression),
    ItemName.progressive_run:       ItemData(0xBC0025, ItemClassification.progression),
    ItemName.progressive_swim:      ItemData(0xBC0026, ItemClassification.progression),
}

switch_palace_table = {
    ItemName.yellow_switch_palace: ItemData(0xBC000E, ItemClassification.progression | ItemClassification.useful),
    ItemName.green_switch_palace:  ItemData(0xBC000F, ItemClassification.progression | ItemClassification.useful),
    ItemName.red_switch_palace:    ItemData(0xBC0010, ItemClassification.progression_deprioritized),
    ItemName.blue_switch_palace:   ItemData(0xBC0011, ItemClassification.progression_deprioritized),
}

trap_table = {
    ItemName.ice_trap:              ItemData(0xBC0080, ItemClassification.trap),
    ItemName.stun_trap:             ItemData(0xBC0081, ItemClassification.trap),
    ItemName.literature_trap:       ItemData(0xBC0082, ItemClassification.trap),
    ItemName.timer_trap:            ItemData(0xBC0083, ItemClassification.trap),
    ItemName.reverse_controls_trap: ItemData(0xBC0084, ItemClassification.trap),
    ItemName.thwimp_trap:           ItemData(0xBC0085, ItemClassification.trap),
    ItemName.fishin_trap:           ItemData(0xBC0086, ItemClassification.trap),
    ItemName.screen_flip_trap:      ItemData(0xBC0087, ItemClassification.trap),
    ItemName.sticky_floor_trap:     ItemData(0xBC0088, ItemClassification.trap),
    ItemName.sticky_hands_trap:     ItemData(0xBC0089, ItemClassification.trap),
    ItemName.pixelate_trap:         ItemData(0xBC008A, ItemClassification.trap),
    ItemName.spotlight_trap:        ItemData(0xBC008B, ItemClassification.trap),
    ItemName.bullet_time_trap:      ItemData(0xBC008C, ItemClassification.trap),
    ItemName.invisibility_trap:     ItemData(0xBC008D, ItemClassification.trap),
    ItemName.empty_item_box_trap:   ItemData(0xBC008E, ItemClassification.trap),
}

event_table = {
    ItemName.victory:   ItemData(0xBC0000, ItemClassification.progression_skip_balancing | ItemClassification.useful),
    ItemName.koopaling: ItemData(0xBC0012, ItemClassification.progression_skip_balancing),
    ItemName.glitched:  ItemData(None, ItemClassification.progression_skip_balancing),
}

# Complete item table.
item_table = {
    **junk_table,
    **collectable_table,
    **upgrade_table,
    **switch_palace_table,
    **trap_table,
    **event_table,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}

option_name_to_item_unlock = {
    "Run": ItemName.run,
    "Carry": ItemName.carry,
    "Swim": ItemName.swim,
    "Spin Jump": ItemName.spin_jump,
    "Climb": ItemName.spin_jump,
    "P-Balloon": ItemName.p_balloon,
    "Yoshi": ItemName.yoshi,
    "Powerups": ItemName.progressive_powerup,
    "Super Star": ItemName.super_star_active,
    "P-Switch": ItemName.p_switch,
    "Item Box": ItemName.item_box,
    "Midway Points": ItemName.midway_point,
    "Yellow Switch Palace": ItemName.yellow_switch_palace,
    "Green Switch Palace": ItemName.green_switch_palace,
    "Red Switch Palace": ItemName.red_switch_palace,
    "Blue Switch Palace": ItemName.blue_switch_palace,
    "Special Zone": ItemName.special_world_clear,
}

trap_value_to_name: typing.Dict[int, str] = {
    0xBC0080: ItemName.ice_trap,
    0xBC0081: ItemName.stun_trap,
    0xBC0082: ItemName.literature_trap,
    0xBC0083: ItemName.timer_trap,
    0xBC0084: ItemName.reverse_controls_trap,
    0xBC0085: ItemName.thwimp_trap,
    0xBC0086: ItemName.fishin_trap,
    0xBC0087: ItemName.screen_flip_trap,
    0xBC0088: ItemName.sticky_floor_trap,
    0xBC0089: ItemName.sticky_hands_trap,
    0xBC008A: ItemName.pixelate_trap,
    0xBC008B: ItemName.spotlight_trap,
    0xBC008C: ItemName.bullet_time_trap,
    0xBC008D: ItemName.invisibility_trap,
    0xBC008E: ItemName.empty_item_box_trap,
}

trap_name_to_value: typing.Dict[str, int] = {
    # Our native Traps
    ItemName.ice_trap:              0xBC0080,
    ItemName.stun_trap:             0xBC0081,
    ItemName.literature_trap:       0xBC0082,
    ItemName.timer_trap:            0xBC0083,
    ItemName.reverse_controls_trap: 0xBC0084,
    ItemName.thwimp_trap:           0xBC0085,
    ItemName.fishin_trap:           0xBC0086,
    ItemName.screen_flip_trap:      0xBC0087,
    ItemName.sticky_floor_trap:     0xBC0088,
    ItemName.sticky_hands_trap:     0xBC0089,
    ItemName.pixelate_trap:         0xBC008A,
    ItemName.spotlight_trap:        0xBC008B,
    ItemName.bullet_time_trap:      0xBC008C,
    ItemName.invisibility_trap:     0xBC008D,
    ItemName.empty_item_box_trap:   0xBC008E,

    # Common other trap names
    "Exposition Trap":      0xBC0082,  # Literature Trap
    "Cutscene Trap":        0xBC0082,  # Literature Trap
    "Phone Trap":           0xBC0082,  # Literature Trap

    "Freeze Trap":          0xBC0081,  # Stun Trap
    "Frozen Trap":          0xBC0081,  # Stun Trap
    "Paralyze Trap":        0xBC0081,  # Stun Trap
    "Chaos Control Trap":   0xBC0081,  # Stun Trap

    "Reversal Trap":        0xBC0084,  # Reverse Trap
    "Fuzzy Trap":           0xBC0084,  # Reverse Trap
    "Confound Trap":        0xBC0084,  # Reverse Trap
    "Confuse Trap":         0xBC0084,  # Reverse Trap
    "Confusion Trap":       0xBC0084,  # Reverse Trap

    "Police Trap":          0xBC0085,  # Thwimp Trap
    "Buyon Trap":           0xBC0085,  # Thwimp Trap
    "Gooey Bag":            0xBC0085,  # Thwimp Trap
    "TNT Barrel Trap":      0xBC0085,  # Thwimp Trap
    "Rockfall Trap":        0xBC0085,  # Thwimp Trap
    "Bomb":                 0xBC0085,  # Thwimp Trap

    "Honey Trap":           0xBC0088,  # Sticky Floor Trap
    "Slowness Trap":        0xBC0088,  # Sticky Floor Trap

    "Ice Floor Trap":       0xBC0080,  # Ice Trap
    "Banana Peel Trap":     0xBC0080,  # Ice Trap
    "Banana Trap":          0xBC0080,  # Ice Trap
    
    "Spooky Time":          0xBC008B,  # Spotlight Trap
    "Darkness Trap":        0xBC008B,  # Spotlight Trap

    "Mirror Trap":          0xBC0087,  # Screen Flip Trap

    "144p Trap":            0xBC008A,  # Pixelate Trap
    "Fuzzy Trap":           0xBC008A,  # Pixelate Trap
    "Pixellation Trap":     0xBC008A,  # Pixelate Trap
    "Zoom Trap":            0xBC008A,  # Pixelate Trap

    "Slow Trap":            0xBC008C,  # Bullet Time Trap
    "PowerPoint Trap":      0xBC008C,  # Bullet Time Trap

    "Invisible Trap":       0xBC008D,  # Invisibility Trap

    "Dry Trap":             0xBC008E,  # Empty Item Box Trap 
    "Depletion Trap":       0xBC008E,  # Empty Item Box Trap 
    "No Stocks":            0xBC008E,  # Empty Item Box Trap 
    "No Vac Trap":          0xBC008E,  # Empty Item Box Trap 
}
