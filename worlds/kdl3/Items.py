from BaseClasses import Item, ItemClassification
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

misc_item_table = {
    "Heart Star": ItemData(0x770020, True, True),
    "1-Up": ItemData(0x770021, False),
    "Maxim Tomato": ItemData(0x770022, False),
    "Invincible Candy": ItemData(0x770023, False),
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


item_table = {
    **copy_ability_table,
    **animal_friend_table,
    **misc_item_table,
    **trap_item_table
}

item_names = {
    "Copy Ability": {name for name in copy_ability_table.keys()},
    "Animal Friend": {name for name in animal_friend_table.keys()}
}

lookup_name_to_id: typing.Dict[str, int] = {item_name: data.code for item_name, data in item_table.items() if data.code}