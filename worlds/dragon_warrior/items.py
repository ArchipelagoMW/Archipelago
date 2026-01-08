from typing import Dict, NamedTuple, Set
from BaseClasses import Item
from . import names


class ItemData(NamedTuple):
    code: int
    progression: bool = False
    useful: bool = False
    skip_balancing: bool = False


class DWItem(Item):
    game = "Dragon Warrior"

equipment_table = {
    names.progressive_weapon: ItemData(0xE20, True),
    names.progressive_armor: ItemData(0xE04, True),
    names.progressive_shield: ItemData(0xE01, True),
    names.erdricks_armor: ItemData(0xFE, True, useful=True),
    names.erdricks_sword: ItemData(0xFF, True, useful=True),
    names.dragon_scale: ItemData(0x4, False, useful=True),
    names.fighters_ring: ItemData(0x6, False, useful=True)
}

important_table = {
    names.fairy_flute: ItemData(0x5, True),
    names.erdricks_token: ItemData(0x7, True),
    names.gwaelins_love: ItemData(0x8, True),
    names.silver_harp: ItemData(0xA, True),
    names.stones_of_sunlight: ItemData(0xC, True),
    names.staff_of_rain: ItemData(0xD, True),
    names.rainbow_drop: ItemData(0xE, True),
    names.magic_key: ItemData(0xD4, True, useful=True),
    names.ball_of_light: ItemData(0x12345, True)
}

cursed_table = {
    names.cursed_belt: ItemData(0x9),
    names.death_necklace: ItemData(0xB, False, useful=True)
}

filler_table = {
    names.herb: ItemData(0xF),
    names.gold: ItemData(0xD1),
}

useful_table = {
    names.high_gold: ItemData(0xD2, useful=True)
}

item_table = {
    **equipment_table,
    **important_table,
    **cursed_table,
    **filler_table,
    **useful_table,
}

item_names: Dict[str, Set[str]] = {
    "Equipment": set(name for name in list(equipment_table.keys()) + list(cursed_table.keys())),
    "Progression": set(name for name in important_table.keys()),
    "Consumable": set(name for name in list(filler_table.keys()) + list(useful_table.keys())),
    }

lookup_name_to_id: Dict[str, int] = {item_name: data.code for item_name, data in item_table.items()}
lookup_id_to_name: Dict[int, str] = {data.code: item_name for item_name, data in item_table.items() if data.code}