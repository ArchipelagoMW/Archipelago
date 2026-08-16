from enum import IntEnum

# Shop cost types.
shop_cost_types: dict[str, tuple[str, ...]] = {
    "Egg_Shop": ("RANCIDEGGS",),
    "Grubfather": ("GRUBS",),
    "Seer": ("ESSENCE",),
    "Salubra_(Requires_Charms)": ("CHARMS", "GEO"),
    "Sly": ("GEO",),
    "Sly_(Key)": ("GEO",),
    "Iselda": ("GEO",),
    "Salubra": ("GEO",),
    "Leg_Eater": ("GEO",),
}

randomizable_starting_items: dict[str, tuple[str, ...]] = {
    "RandomizeFocus": ("Focus",),
    "RandomizeSwim": ("Swim",),
    "RandomizeNail": ("Upslash", "Leftslash", "Rightslash")
}

gamename = "Hollow Knight"
base_id = 0x1000000

BASE_SOUL = 12
BASE_NOTCHES = 3
BASE_HEALTH = 5


class NearbySoul(IntEnum):
    NONE = 1
    ITEMSOUL = 2
    MAPAREASOUL = 3
    AREASOUL = 4
    ROOMSOUL = 5
