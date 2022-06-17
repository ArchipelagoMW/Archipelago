import typing

from BaseClasses import Item, ItemClassification
from .Names import ItemName


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    quantity: int = 1
    event: bool = False


class SA2BItem(Item):
    game: str = "Sonic Adventure 2: Battle"

    def __init__(self, name, classification: ItemClassification, code: int = None, player: int = None):
        super(SA2BItem, self).__init__(name, classification, code, player)

        if self.name == ItemName.sonic_light_shoes or self.name == ItemName.shadow_air_shoes:
            self.pedestal_credit_text = "and the Soap Shoes"


# Separate tables for each type of item.
emblems_table = {
    ItemName.emblem:  ItemData(0xFF0000, True),
}

upgrades_table = {
    ItemName.sonic_gloves:          ItemData(0xFF0001, False),
    ItemName.sonic_light_shoes:     ItemData(0xFF0002, True),
    ItemName.sonic_ancient_light:   ItemData(0xFF0003, False),
    ItemName.sonic_bounce_bracelet: ItemData(0xFF0004, True),
    ItemName.sonic_flame_ring:      ItemData(0xFF0005, True),
    ItemName.sonic_mystic_melody:   ItemData(0xFF0006, True),
    
    ItemName.tails_laser_blaster: ItemData(0xFF0007, False),
    ItemName.tails_booster:       ItemData(0xFF0008, True),
    ItemName.tails_mystic_melody: ItemData(0xFF0009, True),
    ItemName.tails_bazooka:       ItemData(0xFF000A, True),

    ItemName.knuckles_mystic_melody: ItemData(0xFF000B, True),
    ItemName.knuckles_shovel_claws:  ItemData(0xFF000C, True),
    ItemName.knuckles_air_necklace:  ItemData(0xFF000D, True),
    ItemName.knuckles_hammer_gloves: ItemData(0xFF000E, True),
    ItemName.knuckles_sunglasses:    ItemData(0xFF000F, True),
    
    ItemName.shadow_flame_ring:    ItemData(0xFF0010, True),
    ItemName.shadow_air_shoes:     ItemData(0xFF0011, True),
    ItemName.shadow_ancient_light: ItemData(0xFF0012, False),
    ItemName.shadow_mystic_melody: ItemData(0xFF0013, True),
    
    ItemName.eggman_laser_blaster:    ItemData(0xFF0014, False),
    ItemName.eggman_mystic_melody:    ItemData(0xFF0015, True),
    ItemName.eggman_jet_engine:       ItemData(0xFF0016, True),
    ItemName.eggman_large_cannon:     ItemData(0xFF0017, True),
    ItemName.eggman_protective_armor: ItemData(0xFF0018, False),

    ItemName.rouge_mystic_melody:  ItemData(0xFF0019, True),
    ItemName.rouge_pick_nails:     ItemData(0xFF001A, True),
    ItemName.rouge_treasure_scope: ItemData(0xFF001B, True),
    ItemName.rouge_iron_boots:     ItemData(0xFF001C, True),
}

event_table = {
    ItemName.maria: ItemData(0xFF001D, True),
}

# Complete item table.
item_table = {
    **emblems_table,
    **upgrades_table,
    **event_table,
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}
