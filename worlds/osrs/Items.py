import typing

from BaseClasses import Item, ItemClassification
from .Names import ItemNames, RegionNames


class OSRSItem(Item):
    game: str = "Old School Runescape"


class ItemData(typing.NamedTuple):
    id: int
    itemName: str
    progression: ItemClassification
    count: int = 1
    unlocksRegion: typing.Optional[str] = None


Location_Items: typing.List[ItemData] = [
    ItemData(0x070000, ItemNames.Lumbridge, ItemClassification.progression,
             unlocksRegion=RegionNames.Lumbridge),
    ItemData(0x070001, ItemNames.Lumbridge_Swamp, ItemClassification.progression,
             unlocksRegion=RegionNames.Lumbridge_Swamp),
    ItemData(0x070002, ItemNames.Lumbridge_Farms, ItemClassification.progression,
             unlocksRegion=RegionNames.Lumbridge_Farms),
    ItemData(0x070003, ItemNames.HAM_Hideout, ItemClassification.progression,
             unlocksRegion=RegionNames.HAM_Hideout),
    ItemData(0x070004, ItemNames.Draynor_Village, ItemClassification.progression,
             unlocksRegion=RegionNames.Draynor_Village),
    ItemData(0x070005, ItemNames.Draynor_Manor, ItemClassification.progression,
             unlocksRegion=RegionNames.Draynor_Manor),
    ItemData(0x070006, ItemNames.Wizards_Tower, ItemClassification.progression,
             unlocksRegion=RegionNames.Wizards_Tower),
    ItemData(0x070007, ItemNames.Al_Kharid, ItemClassification.progression,
             unlocksRegion=RegionNames.Al_Kharid),
    ItemData(0x070008, ItemNames.Citharede_Abbey, ItemClassification.progression,
             unlocksRegion=RegionNames.Citharede_Abbey),
    ItemData(0x070009, ItemNames.South_Of_Varrock, ItemClassification.progression,
             unlocksRegion=RegionNames.South_Of_Varrock),
    ItemData(0x07000A, ItemNames.Central_Varrock, ItemClassification.progression,
             unlocksRegion=RegionNames.Central_Varrock),
    ItemData(0x07000B, ItemNames.Varrock_Palace, ItemClassification.progression,
             unlocksRegion=RegionNames.Varrock_Palace),
    ItemData(0x07000C, ItemNames.East_Of_Varrock, ItemClassification.progression,
             unlocksRegion=RegionNames.East_Of_Varrock),
    ItemData(0x07000D, ItemNames.West_Varrock, ItemClassification.progression,
             unlocksRegion=RegionNames.West_Varrock),
    ItemData(0x07000E, ItemNames.Edgeville, ItemClassification.progression,
             unlocksRegion=RegionNames.Edgeville),
    ItemData(0x07000F, ItemNames.Barbarian_Village, ItemClassification.progression,
             unlocksRegion=RegionNames.Barbarian_Village),
    ItemData(0x070010, ItemNames.Monastery, ItemClassification.progression,
             unlocksRegion=RegionNames.Monastery),
    ItemData(0x070011, ItemNames.Ice_Mountain, ItemClassification.progression,
             unlocksRegion=RegionNames.Ice_Mountain),
    ItemData(0x070012, ItemNames.Dwarven_Mines, ItemClassification.progression,
             unlocksRegion=RegionNames.Dwarven_Mines),
    ItemData(0x070013, ItemNames.Falador, ItemClassification.progression,
             unlocksRegion=RegionNames.Falador),
    ItemData(0x070014, ItemNames.Falador_Farm, ItemClassification.progression,
             unlocksRegion=RegionNames.Falador_Farm),
    ItemData(0x070015, ItemNames.Crafting_Guild, ItemClassification.progression,
             unlocksRegion=RegionNames.Crafting_Guild),
    ItemData(0x070016, ItemNames.Rimmington, ItemClassification.progression,
             unlocksRegion=RegionNames.Rimmington),
    ItemData(0x070017, ItemNames.Port_Sarim, ItemClassification.progression,
             unlocksRegion=RegionNames.Port_Sarim),
    ItemData(0x070018, ItemNames.Mudskipper_Point, ItemClassification.progression,
             unlocksRegion=RegionNames.Mudskipper_Point),
    ItemData(0x070019, ItemNames.Karamja, ItemClassification.progression,
             unlocksRegion=RegionNames.Karamja),
    ItemData(0x07001A, ItemNames.Crandor, ItemClassification.progression,
             unlocksRegion=RegionNames.Crandor),
    ItemData(0x07001B, ItemNames.Corsair_Cove, ItemClassification.progression,
             unlocksRegion=RegionNames.Corsair_Cove),
    ItemData(0x07001C, ItemNames.Wilderness, ItemClassification.progression,
             unlocksRegion=RegionNames.Wilderness)
]

Gear_Items: typing.List[ItemData] = [
    ItemData(0x07001D, ItemNames.Progressive_Armor, ItemClassification.progression, 6),
    ItemData(0x07001E, ItemNames.Progressive_Weapons, ItemClassification.progression, 6),
    ItemData(0x07001F, ItemNames.Progressive_Tools, ItemClassification.useful, 6),
    ItemData(0x070020, ItemNames.Progressive_Range_Armor, ItemClassification.useful, 3),
    ItemData(0x070021, ItemNames.Progressive_Range_Weapon, ItemClassification.useful, 3),
    ItemData(0x070022, ItemNames.Progressive_Magic, ItemClassification.useful, 2)
]

QP_Items: typing.List[str] = [
    ItemNames.QP_Cooks_Assistant,
    ItemNames.QP_Demon_Slayer,
    ItemNames.QP_Restless_Ghost,
    ItemNames.QP_Romeo_Juliet,
    ItemNames.QP_Sheep_Shearer,
    ItemNames.QP_Shield_of_Arrav,
    ItemNames.QP_Ernest_the_Chicken,
    ItemNames.QP_Vampyre_Slayer,
    ItemNames.QP_Imp_Catcher,
    ItemNames.QP_Prince_Ali_Rescue,
    ItemNames.QP_Dorics_Quest,
    ItemNames.QP_Black_Knights_Fortress,
    ItemNames.QP_Witchs_Potion,
    ItemNames.QP_Knights_Sword,
    ItemNames.QP_Goblin_Diplomacy,
    ItemNames.QP_Pirates_Treasure,
    ItemNames.QP_Rune_Mysteries,
    ItemNames.QP_Misthalin_Mystery,
    ItemNames.QP_Corsair_Curse,
    ItemNames.QP_X_Marks_the_Spot,
    ItemNames.QP_Below_Ice_Mountain
]

all_items: typing.List[ItemData] = Location_Items + Gear_Items
item_table: typing.Dict[str, ItemData] = {item.itemName: item for item in all_items}
items_by_id: typing.Dict[int, ItemData] = {item.id: item for item in all_items}

starting_area_dict: typing.Dict[int, ItemData] = {
    0: item_table[ItemNames.Lumbridge],
    1: item_table[ItemNames.Al_Kharid],
    2: item_table[ItemNames.East_Of_Varrock],
    3: item_table[ItemNames.West_Varrock],
    4: item_table[ItemNames.Edgeville],
    5: item_table[ItemNames.Falador],
    6: item_table[ItemNames.Draynor_Village],
    7: item_table[ItemNames.Wilderness],
}

chunksanity_starting_chunks: typing.List[ItemData] = [
    item_table[ItemNames.Lumbridge],
    item_table[ItemNames.Lumbridge_Swamp],
    item_table[ItemNames.Lumbridge_Farms],
    item_table[ItemNames.HAM_Hideout],
    item_table[ItemNames.Draynor_Village],
    item_table[ItemNames.Draynor_Manor],
    item_table[ItemNames.Wizards_Tower],
    item_table[ItemNames.Al_Kharid],
    item_table[ItemNames.Citharede_Abbey],
    item_table[ItemNames.South_Of_Varrock],
    item_table[ItemNames.Central_Varrock],
    item_table[ItemNames.Varrock_Palace],
    item_table[ItemNames.East_Of_Varrock],
    item_table[ItemNames.West_Varrock],
    item_table[ItemNames.Edgeville],
    item_table[ItemNames.Barbarian_Village],
    item_table[ItemNames.Monastery],
    item_table[ItemNames.Ice_Mountain],
    item_table[ItemNames.Dwarven_Mines],
    item_table[ItemNames.Falador],
    item_table[ItemNames.Falador_Farm],
    item_table[ItemNames.Crafting_Guild],
    item_table[ItemNames.Rimmington],
    item_table[ItemNames.Port_Sarim],
    item_table[ItemNames.Mudskipper_Point],
    item_table[ItemNames.Wilderness]
]
