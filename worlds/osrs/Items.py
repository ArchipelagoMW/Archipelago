import typing

from BaseClasses import Item, ItemClassification
from .Names import ItemNames


class ItemRow(typing.NamedTuple):
    name: str
    amount: int
    progression: ItemClassification


class OSRSItem(Item):
    game: str = "Old School Runescape"


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

starting_area_dict: typing.Dict[int, str] = {
    0: ItemNames.Lumbridge,
    1: ItemNames.Al_Kharid,
    2: ItemNames.Central_Varrock,
    3: ItemNames.West_Varrock,
    4: ItemNames.Edgeville,
    5: ItemNames.Falador,
    6: ItemNames.Draynor_Village,
    7: ItemNames.Wilderness,
}

chunksanity_starting_chunks: typing.List[str] = [
    ItemNames.Lumbridge,
    ItemNames.Lumbridge_Swamp,
    ItemNames.Lumbridge_Farms,
    ItemNames.HAM_Hideout,
    ItemNames.Draynor_Village,
    ItemNames.Draynor_Manor,
    ItemNames.Wizards_Tower,
    ItemNames.Al_Kharid,
    ItemNames.Citharede_Abbey,
    ItemNames.South_Of_Varrock,
    ItemNames.Central_Varrock,
    ItemNames.Varrock_Palace,
    ItemNames.East_Of_Varrock,
    ItemNames.West_Varrock,
    ItemNames.Edgeville,
    ItemNames.Barbarian_Village,
    ItemNames.Monastery,
    ItemNames.Ice_Mountain,
    ItemNames.Dwarven_Mines,
    ItemNames.Falador,
    ItemNames.Falador_Farm,
    ItemNames.Crafting_Guild,
    ItemNames.Rimmington,
    ItemNames.Port_Sarim,
    ItemNames.Mudskipper_Point,
    ItemNames.Wilderness
]

# Some starting areas contain multiple regions, so if that area is rolled for Chunksanity, we need to map it to one
chunksanity_special_region_names: typing.Dict[str, str] = {
    ItemNames.Lumbridge_Farms: 'Lumbridge Farms East',
    ItemNames.Crafting_Guild: 'Crafting Guild Outskirts',
}
