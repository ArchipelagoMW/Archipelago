from dataclasses import dataclass


@dataclass
class RAC3WEAPONVENDORSLOTDATA:
    item_id: int = 0
    ammo_text: int = 0
    item_class: int = 0x0CDB
    is_free: int = 0
    item_mega: int = 0
    item_all_ammo: int = 0
    item_memcard: int = 0

    def __init__(self,
                item_id: int = 0,
                ammo_text: int = 0,
                item_class: int = 0x0CDB,
                is_free: int = 0,
                item_mega: int = 0,
                item_all_ammo: int = 0,
                item_memcard: int = 0):
        self.item_id = item_id
        self.ammo_text = ammo_text
        self.item_class = item_class
        self.is_free = is_free
        self.item_mega = item_mega
        self.item_all_ammo = item_all_ammo
        self.item_memcard = item_memcard

@dataclass
class RAC3ARMORVENDORSLOTDATA:
    item_icon: int = 0
    item_cost: int = 0
    item_level: int = 0

    def __init__(self,
                item_icon: int = 0,
                item_cost: int = 0,
                item_level: int = 0):
        self.item_icon = item_icon
        self.item_cost = item_cost
        self.item_level = item_level