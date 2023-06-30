import typing

from BaseClasses import Item, ItemClassification


class ItemNames:
    Lumbridge = "Area: Lumbridge"
    Lumbridge_Swamp = "Area: Lumbridge Swamp"
    Lumbridge_Farms = "Area: Lumbridge Farms"
    HAM_Hideout = "Area: HAM Hideout"
    Draynor_Village = "Area: Draynor Village"
    Draynor_Manor = "Area: Draynor Manor"
    Wizards_Tower = "Area: Wizard's Tower"
    Al_Kharid = "Area: Al Kharid"
    Citharede_Abbey = "Area: Cathraede Abbey"
    South_Of_Varrock = "Area: South of Varrock"
    Central_Varrock = "Area: Central Varrock"
    Varrock_Palace = "Area: Varrock Palace"
    East_Of_Varrock = "Area: East of Varrock"
    West_Varrock = "Area: West Varrock"
    Edgeville = "Area: Edgeville"
    Barbarian_Village = "Area: Barbarian Village"
    Monastery = "Area: Monastery"
    Ice_Mountain = "Area: Ice Mountain"
    Dwarven_Mines = "Area: Dwarven Mines"
    Falador = "Area: Falador"
    Falador_Farm = "Area: Falador Farm"
    Crafting_Guild = "Area: Crafting Guild"
    Rimmington = "Area: Rimmington"
    Port_Sarim = "Area: Port Sarim"
    Mudskipper_Point = "Area: Mudskipper Point"
    Karamja = "Area: Karamja"
    Crandor = "Area: Crandor"
    Corsair_Cove = "Area: Corsair Cove"
    Wilderness = "Area: The Wilderness"
    Progressive_Armor = "Progressive Armor"
    Progressive_Weapons = "Progressive Weapons"
    Progressive_Tools = "Progressive Tools"
    Progressive_Range_Armor = "Progressive Range Armor"
    Progressive_Range_Weapon = "Progressive Range Weapon"
    Progressive_Magic = "Progressive Magic Spell"
    Lobsters = "10 Lobsters"
    Swordfish = "5 Swordfish"
    Energy_Potions = "10 Energy Potions"
    Coins = "5,000 Coins"
    Mind_Runes = "50 Mind Runes"
    Chaos_Runes = "25 Chaos Runes"
    Death_Runes = "10 Death Runes"
    Law_Runes = "10 Law Runes"
    QP_Cooks_Assistant = "1 QP (Cook's Assistant)"
    QP_Demon_Slayer = "3 QP (Demon Slayer)"
    QP_Restless_Ghost = "1 QP (The Restless Ghost)"
    QP_Romeo_Juliet = "5 QP (Romeo & Juliet)"
    QP_Sheep_Shearer = "1 QP (Sheep Shearer)"
    QP_Shield_of_Arrav = "1 QP (Shield of Arrav)"
    QP_Ernest_the_Chicken = "4 QP (Ernest the Chicken)"
    QP_Vampyre_Slayer = "3 QP (Vampyre Slayer)"
    QP_Imp_Catcher = "1 QP (Imp Catcher)"
    QP_Prince_Ali_Rescue = "3 QP (Prince Ali Rescue)"
    QP_Dorics_Quest = "1 QP (Doric's Quest)"
    QP_Black_Knights_Fortress = "3 QP (Black Knights' Fortress)"
    QP_Witchs_Potion = "1 QP (Witch's Potion)"
    QP_Knights_Sword = "1 QP (The Knight's Sword)"
    QP_Goblin_Diplomacy = "5 QP (Goblin Diplomacy)"
    QP_Pirates_Treasure = "2 QP (Pirate's Treasure)"
    QP_Rune_Mysteries = "1 QP (Rune Mysteries)"
    QP_Misthalin_Mystery = "1 QP (Misthalin Mystery)"
    QP_Corsair_Curse = "2 QP (The Corsair Curse)"
    QP_X_Marks_the_Spot = "1 QP (X Marks The Spot)"
    QP_Below_Ice_Mountain = "1 QP (Below Ice Mountain)"


class OSRSItem(Item):
    game: str = "Old School Runescape"


class ItemData(typing.NamedTuple):
    id: int
    itemName: str
    progression: ItemClassification
    count: int = 1


Location_Items: typing.List[ItemData] = [
    ItemData(0x070000, ItemNames.Lumbridge, ItemClassification.progression_skip_balancing),
    ItemData(0x070001, ItemNames.Lumbridge_Swamp, ItemClassification.progression_skip_balancing),
    ItemData(0x070002, ItemNames.Lumbridge_Farms, ItemClassification.progression_skip_balancing),
    ItemData(0x070003, ItemNames.HAM_Hideout, ItemClassification.progression_skip_balancing),
    ItemData(0x070004, ItemNames.Draynor_Village, ItemClassification.progression_skip_balancing),
    ItemData(0x070005, ItemNames.Draynor_Manor, ItemClassification.progression_skip_balancing),
    ItemData(0x070006, ItemNames.Wizards_Tower, ItemClassification.progression_skip_balancing),
    ItemData(0x070007, ItemNames.Al_Kharid, ItemClassification.progression_skip_balancing),
    ItemData(0x070008, ItemNames.Citharede_Abbey, ItemClassification.progression_skip_balancing),
    ItemData(0x070009, ItemNames.South_Of_Varrock, ItemClassification.progression_skip_balancing),
    ItemData(0x07000A, ItemNames.Central_Varrock, ItemClassification.progression_skip_balancing),
    ItemData(0x07000B, ItemNames.Varrock_Palace, ItemClassification.progression_skip_balancing),
    ItemData(0x07000C, ItemNames.East_Of_Varrock, ItemClassification.progression_skip_balancing),
    ItemData(0x07000D, ItemNames.West_Varrock, ItemClassification.progression_skip_balancing),
    ItemData(0x07000E, ItemNames.Edgeville, ItemClassification.progression_skip_balancing),
    ItemData(0x07000F, ItemNames.Barbarian_Village, ItemClassification.progression_skip_balancing),
    ItemData(0x070010, ItemNames.Monastery, ItemClassification.progression_skip_balancing),
    ItemData(0x070011, ItemNames.Ice_Mountain, ItemClassification.progression_skip_balancing),
    ItemData(0x070012, ItemNames.Dwarven_Mines, ItemClassification.progression_skip_balancing),
    ItemData(0x070013, ItemNames.Falador, ItemClassification.progression_skip_balancing),
    ItemData(0x070014, ItemNames.Falador_Farm, ItemClassification.progression_skip_balancing),
    ItemData(0x070015, ItemNames.Crafting_Guild, ItemClassification.progression_skip_balancing),
    ItemData(0x070016, ItemNames.Rimmington, ItemClassification.progression_skip_balancing),
    ItemData(0x070017, ItemNames.Port_Sarim, ItemClassification.progression_skip_balancing),
    ItemData(0x070018, ItemNames.Mudskipper_Point, ItemClassification.progression_skip_balancing),
    ItemData(0x070019, ItemNames.Karamja, ItemClassification.progression_skip_balancing),
    ItemData(0x07001A, ItemNames.Crandor, ItemClassification.progression_skip_balancing),
    ItemData(0x07001B, ItemNames.Corsair_Cove, ItemClassification.progression_skip_balancing),
    ItemData(0x07001C, ItemNames.Wilderness, ItemClassification.progression_skip_balancing)
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
