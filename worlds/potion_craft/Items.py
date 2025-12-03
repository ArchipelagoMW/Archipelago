from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional, List

from BaseClasses import Item, ItemClassification


class PotionCraftItem(Item):
    game: str = "Potion Craft"
class Direction(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3

@dataclass
class ItemData:
    code: int
    classification: ItemClassification
    chapter: int = 0
    direction: list[Direction] | None = None
    amount: Optional[int] = 1

@dataclass
class TalentData:
    code: int
    classification: ItemClassification
    amount: Optional[int] = 1

def get_junk_item_names(rand, k: int) -> str:
    junk = rand.choices(
        list(junk_weights.keys()),
        weights=list(junk_weights.values()),
        k=k)
    return junk

def create_item(world, name: str, classification: ItemClassification, amount: Optional[int] = 1):
    for i in range(amount):
        world.itempool.append(Item(name, classification, world.item_name_to_id[name], world.player))


def create_potion_craft_items(world):
    total_location_count = len(world.multiworld.get_unfilled_locations(world.player)) #adds items to world.item pool

    print(len(world.itempool))

    remaining_locations: int = total_location_count - len(world.itempool)
    junk_count: int = remaining_locations - 1  # Minus 1 because we placed victory at the goal check in Rules.py
    junk = get_junk_item_names(world.random, junk_count)
    for name in junk:
        create_item(world, name, ItemClassification.filler)
    world.multiworld.itempool += world.itempool

def get_ingredients_by_direction(direction: Direction) -> List[str]:

    return [
        key
        for key, value in ingredients.items()
        if value.direction is not None and direction in value.direction
    ]

ingredients: Dict[str, ItemData] = {
    "Windbloom" : ItemData(1, ItemClassification.progression, 1,[Direction.NORTH]), #Herb start
    "Waterbloom" : ItemData(2, ItemClassification.progression, 1, [Direction.EAST]),
    "Terraria" : ItemData(3, ItemClassification.progression, 1, [Direction.SOUTH]),
    "Tangleweed" : ItemData(4, ItemClassification.progression, 1, [Direction.EAST]),
    "Lifeleaf" : ItemData(5, ItemClassification.progression, 1, [Direction.EAST, Direction.SOUTH]),
    "Firebell" : ItemData(6, ItemClassification.progression, 1, [Direction.WEST]),
    "Thunder Thistle" : ItemData(7, ItemClassification.progression, 2, [Direction.WEST, Direction.SOUTH]),
    "Icefruit" : ItemData(8, ItemClassification.useful, 2, [Direction.NORTH, Direction.SOUTH, Direction.EAST]),
    "Hairy Banana" : ItemData(9, ItemClassification.progression, 2, [Direction.SOUTH, Direction.WEST]),
    "Goodberry" : ItemData(10, ItemClassification.progression, 2, [Direction.EAST, Direction.SOUTH]),
    "Goldthorn" : ItemData(11, ItemClassification.progression, 2, [Direction.SOUTH, Direction.EAST]),
    "Lava Root" : ItemData(12, ItemClassification.progression, 3, [Direction.WEST]),
    "Featherbloom" : ItemData(13, ItemClassification.progression, 3, [Direction.NORTH]),
    "Druid's Rosemary" : ItemData(14, ItemClassification.progression, 3, [Direction.SOUTH, Direction.EAST]),
    "Dream Beet" : ItemData(15, ItemClassification.progression, 3, [Direction.EAST, Direction.NORTH]),
    "Bloodthorn" : ItemData(16, ItemClassification.progression, 3, [Direction.NORTH, Direction.WEST]),
    "Whirlweed" : ItemData(17, ItemClassification.progression, 4, [Direction.NORTH]),
    "Thornstick" : ItemData(18, ItemClassification.progression, 4, [Direction.SOUTH, Direction.WEST]),
    "Grasping Root" : ItemData(19, ItemClassification.progression, 4, [Direction.NORTH, Direction.WEST]),
    "Flameweed" : ItemData(20, ItemClassification.progression, 4, [Direction.WEST]),
    "Coldleaf" : ItemData(21, ItemClassification.progression, 4, [Direction.EAST]),
    "Spellbloom" : ItemData(22, ItemClassification.progression, 5, [Direction.NORTH, Direction.EAST]),
    "Healer's Heather" : ItemData(23, ItemClassification.progression, 5, [Direction.SOUTH, Direction.EAST]),
    "Fluffbloom" : ItemData(24, ItemClassification.progression, 5, [Direction.NORTH, Direction.EAST]),
    "Dragon Pepper" : ItemData(25, ItemClassification.useful, 5, [Direction.SOUTH, Direction.WEST, Direction.NORTH]),
    "Boombloom" : ItemData(26, ItemClassification.progression, 5, [Direction.NORTH, Direction.WEST]),
    "Terror Bud" : ItemData(27, ItemClassification.useful, 6, [Direction.SOUTH, Direction.WEST, Direction.NORTH]),
    "Mageberry" : ItemData(28, ItemClassification.progression, 6, [Direction.EAST, Direction.NORTH]),
    "Evergreen Fern" : ItemData(29, ItemClassification.progression, 6, [Direction.EAST, Direction.SOUTH]), #Herb End
    "Dryad's Saddle" : ItemData(30, ItemClassification.progression, 1, [Direction.SOUTH]), #Mushroom Start
    "Mad Mushroom" : ItemData(31, ItemClassification.progression, 1, [Direction.NORTH, Direction.WEST]),
    "Marshroom" : ItemData(32, ItemClassification.progression, 1, [Direction.SOUTH, Direction.EAST]),
    "Mudshroom" : ItemData(33, ItemClassification.progression, 1, [Direction.SOUTH]),
    "Stink Mushroom" : ItemData(34, ItemClassification.progression, 1, [Direction.NORTH, Direction.EAST]),
    "Sulphur Shelf" : ItemData(35, ItemClassification.progression, 1, [Direction.WEST]),
    "Witch Mushroom" : ItemData(36, ItemClassification.progression, 1, [Direction.SOUTH, Direction.WEST]),
    "Shadow Chanterelle" : ItemData(37, ItemClassification.progression, 2, [Direction.NORTH, Direction.EAST]),
    "Weirdshroom" : ItemData(38, ItemClassification.progression, 2, [Direction.SOUTH, Direction.EAST]),
    "Foggy Parasol" : ItemData(39, ItemClassification.progression, 3, [Direction.NORTH]),
    "Goblin Shroom" : ItemData(40, ItemClassification.progression, 3, [Direction.SOUTH, Direction.WEST]),
    "Moss Shroom" : ItemData(41, ItemClassification.progression, 3, [Direction.SOUTH, Direction.EAST]),
    "Phantom Skirt" : ItemData(42, ItemClassification.useful, 4, [Direction.NORTH, Direction.EAST, Direction.WEST]), #TODO might edit later
    "Poopshroom" : ItemData(43, ItemClassification.progression, 4, [Direction.SOUTH]),
    "Watercap" : ItemData(44, ItemClassification.progression, 4, [Direction.EAST]),
    "Kraken Mushroom" : ItemData(45, ItemClassification.progression, 5, [Direction.EAST]),
    "Lust Mushroom" : ItemData(46, ItemClassification.progression, 5, [Direction.SOUTH]),
    "Magma Morel" : ItemData(47, ItemClassification.progression, 5, [Direction.EAST]),
    "Grave Truffle" : ItemData(48, ItemClassification.useful, 6, [Direction.SOUTH, Direction.WEST]), #TODO might edit later
    "Rainbow Cap" : ItemData(49, ItemClassification.useful, 6, [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]),  #Mushroom END #TODO might remove west
    "Cloud Crystal" : ItemData(50, ItemClassification.progression, 2, [Direction.NORTH]), #Mineral Start
    "Earth Pyrite" : ItemData(51, ItemClassification.progression, 2, [Direction.SOUTH]),
    "Frost Sapphire" : ItemData(52, ItemClassification.progression, 2, [Direction.EAST]),
    "Fire Citrine" : ItemData(53, ItemClassification.progression, 2, [Direction.WEST]),
    "Blood Ruby" : ItemData(54, ItemClassification.progression, 3, [Direction.NORTH, Direction.WEST]),
    "Arcane Crystal" : ItemData(55, ItemClassification.progression, 4, [Direction.NORTH, Direction.EAST]),
    "Life Crystal" : ItemData(56, ItemClassification.progression, 5, [Direction.SOUTH, Direction.EAST]),
    "Plague Stibnite" : ItemData(57, ItemClassification.progression, 6, [Direction.SOUTH, Direction.WEST]),
    "Fable Bismuth" : ItemData(58, ItemClassification.useful, 7, [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]), #Mineral END
    #TODO maybe add salts?

}

potion_effects: Dict[str, ItemData] = {
    #Chapters are the chapters the potions are needed to beat, not how early you can get them <------
    "Healing" : ItemData(59, ItemClassification.progression, 1, None), #Needs South East
    "Frost" : ItemData(60, ItemClassification.progression, 1, None), #Needs East
    "Poison" : ItemData(61, ItemClassification.progression, 1, None), #Needs South West
    "Fire" : ItemData(62, ItemClassification.progression, 1, None), #Needs West (You don't need north to beat chapter 1)
    "Explosion" : ItemData(63, ItemClassification.progression, 2, None), #Needs North West
    "Wild Growth" : ItemData(64, ItemClassification.progression, 2, None), #Needs South East
    "Strength" : ItemData(65, ItemClassification.progression, 2, None), # Needs South
    "Dexterity" : ItemData(66, ItemClassification.progression, 2, None), #Needs East and South
    "Swiftness" : ItemData(67, ItemClassification.progression, 2, None), #Needs North
    "Lightning" : ItemData(68, ItemClassification.progression, 3, None), #Mainly South, slightly east
    "Mana" : ItemData(69, ItemClassification.progression, 3, None), #South East
    "Stone Skin": ItemData(70, ItemClassification.progression, 3, None), #South West and East OR a south crystal
    "Sleep" : ItemData(71, ItemClassification.progression, 3, None), #Needs East, can take a South or a North
    "Light" : ItemData(72, ItemClassification.progression, 3, None), #West
    "Charm" : ItemData(73, ItemClassification.progression, 4, None), #Mainly North, need someway west
    "Slowness" : ItemData(74, ItemClassification.progression, 4, None), #South and West, No need for east because water
    "Rage" : ItemData(75, ItemClassification.progression, 4, None), #North and East
    "Magical Vision" : ItemData(76, ItemClassification.progression, 4, None), #North and East
    "Acid" : ItemData(77, ItemClassification.progression, 5, None), #Mainly West, Still needs South
    "Libido" : ItemData(78, ItemClassification.progression, 5, None), #Needs North West,
    "Invisibility" : ItemData(79, ItemClassification.progression, 5, None), #Needs North and East
    "Levitation" : ItemData(80,ItemClassification.progression, 5, None), #Needs North, can use West and East OR a North Crystal
    "Necromancy" : ItemData(81, ItemClassification.progression, 5, None), #South West, Recommend crystal Or East
    "Poison Protection": ItemData(82, ItemClassification.progression, 6, None), #Needs All directions (should have by chapter 6 anyway)
    "Lightning Protection" : ItemData(83, ItemClassification.progression, 6, None), #All Directions OR South with Crystal
    "Fire Protection" : ItemData(84,ItemClassification.progression, 6, None), #All Directions OR east wth crystals
    "Frost Protection": ItemData(85, ItemClassification.progression, 6, None), #All Directions Mainly West
    "Gluing" : ItemData(86, ItemClassification.progression, 6, None), #All Directions
    "Slipperiness": ItemData(87, ItemClassification.progression, 6, None),
    "Stench": ItemData(88, ItemClassification.progression, 6, None),
    "Acid Protection" : ItemData(89, ItemClassification.progression, 7, None),
    "Anti Magic" : ItemData(90, ItemClassification.progression, 7, None),
    "Shrinking" : ItemData(91, ItemClassification.progression, 7, None),
    "Enlargement" : ItemData(92, ItemClassification.progression, 7, None),
    "Rejuvenation" : ItemData(93, ItemClassification.progression, 7, None),
    "Inspiration" : ItemData(94, ItemClassification.progression, 8, None),
    "Fragrance" : ItemData(95, ItemClassification.progression, 8, None),
    "Fear" : ItemData(96, ItemClassification.progression, 8, None),
    "Hallucinations" : ItemData(97, ItemClassification.progression, 9, None),
    "Luck" : ItemData(98, ItemClassification.progression, 9, None),
    "Curse" : ItemData(99, ItemClassification.progression, 9, None),
}

talents: Dict[str, TalentData] = {
    "Trading" : TalentData(100, ItemClassification.useful), #trading start
    "Irrepressible Seller" : TalentData(101, ItemClassification.useful),
    "Charisma" : TalentData(102, ItemClassification.useful),
    "Great Potion Demand" : TalentData(103, ItemClassification.useful),
    "Advertising Master" : TalentData(104, ItemClassification.useful),
    "Perfect Haggling" : TalentData(105, ItemClassification.useful),
    "Haggling over complex topics" : TalentData(106, ItemClassification.useful),
    "Haggling over extremely complex topics" : TalentData(107, ItemClassification.useful),
    "Unhurried Haggling" : TalentData(108, ItemClassification.useful),
    "Accommodating Haggling" : TalentData(109, ItemClassification.useful),
    "Calming Haggling Manner" : TalentData(110, ItemClassification.useful),
    "Good Potion Seller" : TalentData(111, ItemClassification.useful),
    "Best Simple Potion Seller": TalentData(112, ItemClassification.useful),
    "Selling Potions to Merchants" : TalentData(113, ItemClassification.useful),
    "Friendship with Merchants" : TalentData(114, ItemClassification.useful),
    "Increased Discount Chance" : TalentData(115, ItemClassification.useful),
    "Reduced Markup Chance" : TalentData(116, ItemClassification.useful),
    "Skilled Manipulator" : TalentData(117, ItemClassification.useful),
    "Talented Potion Seller" : TalentData(118, ItemClassification.useful), #Trading end
    "Fertilizing Herbs and Mushrooms with Potions": TalentData(119, ItemClassification.useful), #Gardening Start
    "Careful Herb Care": TalentData(120, ItemClassification.useful),
    "Careful Mushroom Care": TalentData(121, ItemClassification.useful),
    "Careful Crystal Care": TalentData(122, ItemClassification.useful),
    "Herbalism": TalentData(123, ItemClassification.useful),
    "Wildly Overgrown Herb Harvesting": TalentData(124, ItemClassification.useful),
    "Mushroom Harvesting": TalentData(125, ItemClassification.useful),
    "Wildly Overgrown Mushroom Harvesting": TalentData(126, ItemClassification.useful),
    "Crystal Harvesting": TalentData(127, ItemClassification.useful),
    "Wildly Overgrown Crystal Harvesting": TalentData(128, ItemClassification.useful),
    "Gold Digger": TalentData(129, ItemClassification.useful),
    "Gold Fever": TalentData(130, ItemClassification.useful),
    "Herb Planting": TalentData(131, ItemClassification.useful),
    "Herb Replanting": TalentData(132, ItemClassification.useful),
    "Herb Seed Harvesting": TalentData(133, ItemClassification.useful),
    "Quick Herb Growth": TalentData(134, ItemClassification.useful),
    "Underwater Growing": TalentData(135, ItemClassification.useful),
    "Cave Herbs": TalentData(136, ItemClassification.useful),
    "Mushroom Planting": TalentData(137, ItemClassification.useful),
    "Mushroom Replanting": TalentData(138, ItemClassification.useful),
    "Mycelium Harvesting": TalentData(139, ItemClassification.useful),
    "Quick Mushroom Growth": TalentData(140, ItemClassification.useful),
    "Truffle Growing": TalentData(141, ItemClassification.useful),
    "Crystal Planting": TalentData(142, ItemClassification.useful),
    "Crystal Replanting": TalentData(143, ItemClassification.useful),
    "Crystal Seed Harvesting": TalentData(144, ItemClassification.useful),
    "Quick Crystal Growth": TalentData(145, ItemClassification.useful),
    "Fertilizing Crystals with Potions": TalentData(146, ItemClassification.useful), #Gardening End
    "Bulk Brewing": TalentData(147, ItemClassification.useful), #Alchemy Start
    "Alchemical Practice": TalentData(148, ItemClassification.useful),
    "Precious Residue": TalentData(149, ItemClassification.useful),
    "Alchemy Map: Visibility Radius": TalentData(150, ItemClassification.useful),
    "The key is to pull it out just in time": TalentData(151, ItemClassification.useful),
    "Better Restore Salt": TalentData(152, ItemClassification.useful),
    "Salt Specialist": TalentData(153, ItemClassification.useful),#Alchemy End, talents End
}

key_items: Dict[str, ItemData] = {
    "Progressive Alchemy Machine" : ItemData(500, ItemClassification.useful),
    "Progressive Garden" : ItemData(501, ItemClassification.useful),
    "Recipe Page" : ItemData(502, ItemClassification.useful),
    "Progressive Salt" : ItemData(503, ItemClassification.progression),
    "Progressive Crystal Recipe" : ItemData(504, ItemClassification.progression),

}


junk_items: Dict[str, ItemData] = {
    "Xp": ItemData(1000, ItemClassification.filler),
    "Money": ItemData(1001, ItemClassification.filler),
    "Bulk North Ingredient Bundle" : ItemData(1002, ItemClassification.filler),
    "Bulk East Ingredient Bundle" : ItemData(1003, ItemClassification.filler),
    "Bulk South Ingredient Bundle" : ItemData(1004, ItemClassification.filler),
    "Bulk West Ingredient Bundle" : ItemData(1005, ItemClassification.filler),
}

junk_weights = {
    "Xp": 50,
    "Money": 50,
    "Bulk North Ingredient Bundle": 20
}

full_item_dict: Dict[str, any] = {**ingredients, **talents, **key_items, **junk_items, **potion_effects} #full item dictionary