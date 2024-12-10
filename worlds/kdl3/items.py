from BaseClasses import Item
import typing


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    skip_balancing: bool = False
    trap: bool = False


class KDL3Item(Item):
    game = "Kirby's Dream Land 3"


copy_ability_table = {
    "Burning": ItemData(0x770001, True),
    "Stone": ItemData(0x770002, True),
    "Ice": ItemData(0x770003, True),
    "Needle": ItemData(0x770004, True),
    "Clean": ItemData(0x770005, True),
    "Parasol": ItemData(0x770006, True),
    "Spark": ItemData(0x770007, True),
    "Cutter": ItemData(0x770008, True)
}

animal_friend_table = {
    "Rick": ItemData(0x770010, True),
    "Kine": ItemData(0x770011, True),
    "Coo": ItemData(0x770012, True),
    "Nago": ItemData(0x770013, True),
    "ChuChu": ItemData(0x770014, True),
    "Pitch": ItemData(0x770015, True)
}

animal_friend_spawn_table = {
    "Rick Spawn": ItemData(None, True),
    "Kine Spawn": ItemData(None, True),
    "Coo Spawn": ItemData(None, True),
    "Nago Spawn": ItemData(None, True),
    "ChuChu Spawn": ItemData(None, True),
    "Pitch Spawn": ItemData(None, True)
}

copy_ability_access_table = {
    "No Ability": ItemData(None, False),
    "Burning Ability": ItemData(None, True),
    "Stone Ability": ItemData(None, True),
    "Ice Ability": ItemData(None, True),
    "Needle Ability": ItemData(None, True),
    "Clean Ability": ItemData(None, True),
    "Parasol Ability": ItemData(None, True),
    "Spark Ability": ItemData(None, True),
    "Cutter Ability": ItemData(None, True),
}

misc_item_table = {
    "Heart Star": ItemData(0x770020, True, True),
    "1-Up": ItemData(0x770021, False),
    "Maxim Tomato": ItemData(0x770022, False),
    "Invincible Candy": ItemData(0x770023, False),
    "Little Star": ItemData(0x770024, False),
    "Medium Star": ItemData(0x770025, False),
    "Big Star": ItemData(0x770026, False),
}

trap_item_table = {
    "Gooey Bag": ItemData(0x770040, False, False, True),
    "Slowness": ItemData(0x770041, False, False, True),
    "Eject Ability": ItemData(0x770042, False, False, True)
}

filler_item_weights = {
    "1-Up": 4,
    "Maxim Tomato": 2,
    "Invincible Candy": 2
}

star_item_weights = {
    "Little Star": 16,
    "Medium Star": 8,
    "Big Star": 4
}

total_filler_weights = {
    **filler_item_weights,
    **star_item_weights
}


item_table = {
    **copy_ability_table,
    **copy_ability_access_table,
    **animal_friend_table,
    **animal_friend_spawn_table,
    **misc_item_table,
    **trap_item_table
}

item_names = {
    "Copy Ability": set(copy_ability_table),
    "Animal Friend": set(animal_friend_table),
}

lookup_item_to_id: typing.Dict[str, int] = {item_name: data.code for item_name, data in item_table.items() if data.code}
