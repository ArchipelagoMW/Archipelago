from BaseClasses import Item, ItemClassification
from MultiServer import console
from .Types import OkamiItem, ItemData
from .Enums.BrushTechniques import BrushTechniques, BrushTechniqueData
from .Enums.DivineInstruments import DivineInstrumentData, DivineInstruments
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from . import OkamiWorld


def create_item(world: "OkamiWorld", name: str) -> Item:
    data = item_table[name]
    return OkamiItem(name, data.classification, data.code, world.player)


def create_brush_techniques_items(world: "OkamiWorld") -> List[Item]:
    items = []
    for b in BrushTechniques.list():
        for i in range(b.item_count):
            items.append(create_brush_technique_item(world, b))

    return items


def create_brush_technique_item(world: "OkamiWorld", data: BrushTechniqueData) -> Item:
    return OkamiItem(data.item_name, data.item_classification, data.code, world.player)


def create_divine_instrument_items(world: "OkamiWorld", precollected_instrument: str | None) -> List[Item]:
    items = []
    for d in DivineInstruments.list():
        if precollected_instrument and d.item_name != precollected_instrument:
            items.append(create_divine_instrument_item(world, d))
    return items


def create_divine_instrument_item(world: "OkamiWorld", data: DivineInstrumentData) -> Item:
    return OkamiItem(data.item_name, ItemClassification.progression, data.code, world.player)


def create_multiple_items(world: "OkamiWorld", name: str, count: int = 1,
                          item_type: ItemClassification = ItemClassification.progression) -> List[Item]:
    data = item_table[name]
    itemlist: List[Item] = []

    for i in range(count):
        itemlist += [OkamiItem(name, item_type, data.code, world.player)]

    return itemlist


def create_junk_items(world: "OkamiWorld", count: int) -> List[Item]:
    junk_pool: List[Item] = []
    junk_list: Dict[str, int] = {}
    ic: ItemClassification

    for name in item_table.keys():
        ic = item_table[name].classification
        if ic == ItemClassification.filler:
            junk_list[name] = junk_weights.get(name)

    for i in range(count):
        junk_pool.append(
            world.create_item(world.random.choices(list(junk_list.keys()), weights=list(junk_list.values()), k=1)[0]))
    return junk_pool


def get_item_name_to_id_dict() -> dict:
    item_dict = {name: data.code for name, data in item_table.items()}
    for b in BrushTechniques.list():
        item_dict[b.item_name] = b.code
    for d in DivineInstruments.list():
        item_dict[d.item_name] = d.code
    return item_dict

progressive_weapons={
    "Progressive Mirror":ItemData(0x300,ItemClassification.progression),
    "Progressive Rosary":ItemData(0x301,ItemClassification.progression),
    "Progressive Sword":ItemData(0x302,ItemClassification.progression),
}

karmic_transformers = {
    "Karmic Returner": ItemData(0xc8, ItemClassification.filler),
    "Karmic Transformer 1": ItemData(0x5b, ItemClassification.filler),
    "Karmic Transformer 2": ItemData(0xc9, ItemClassification.filler),
    "Karmic Transformer 3": ItemData(0x79, ItemClassification.filler),
    "Karmic Transformer 4": ItemData(0xcf, ItemClassification.filler),
    "Karmic Transformer 5": ItemData(0xcb, ItemClassification.filler),
    "Karmic Transformer 6": ItemData(0xca, ItemClassification.filler),
    "Karmic Transformer 7": ItemData(0x7b, ItemClassification.filler),
    "Karmic Transformer 8": ItemData(0x7a, ItemClassification.filler),
    "Karmic Transformer 9": ItemData(0x7c, ItemClassification.filler),
}

okami_items = {

    # Equips
    # "Water Tablet": ItemData(0x9c, ItemClassification.progression),
    "Peace Bell": ItemData(0x0b, ItemClassification.useful),
    "Golden Lucky Cat": ItemData(0x95, ItemClassification.useful),
    "Thief's Glove": ItemData(0x96, ItemClassification.useful),
    "Wood Mat": ItemData(0x97, ItemClassification.useful),
    "Golden Ink Pot": ItemData(0x98, ItemClassification.useful),
    "Fire Tablet": ItemData(0x9d, ItemClassification.progression),

    # Quest Items

    "Canine Tracker": ItemData(0x42, ItemClassification.progression),
    "Lucky Mallet": ItemData(0x43, ItemClassification.progression),
    "Border Key": ItemData(0x44, ItemClassification.progression),
    "Dragon Orb": ItemData(0x45, ItemClassification.progression),
    "Fox Rods": ItemData(0x46, ItemClassification.progression),
    "Thunder Brew": ItemData(0x47, ItemClassification.progression),
    "Shell Amulet": ItemData(0x48, ItemClassification.progression),
    "Mask": ItemData(0x49, ItemClassification.progression),
    "Ogre Liver": ItemData(0x4a, ItemClassification.progression),
    "Lips of Ice": ItemData(0x4b, ItemClassification.progression),
    "Eyeball of Fire": ItemData(0x4c, ItemClassification.progression),
    "Black Demon Horn": ItemData(0x4d, ItemClassification.progression),
    "Loyalty Orb": ItemData(0x4e, ItemClassification.progression),
    "Justice Orb": ItemData(0x4f, ItemClassification.progression),
    "Duty Orb": ItemData(0x50, ItemClassification.progression),
    "Golden Mushroom": ItemData(0x5f, ItemClassification.progression),
    "Gimmick Gear": ItemData(0x60, ItemClassification.progression),
    "8 Purification Sake": ItemData(0x62, ItemClassification.progression),
    "Sewaprolo": ItemData(0x63, ItemClassification.progression),
    "Charcoal": ItemData(0x71, ItemClassification.progression),
    "Blinding Snow": ItemData(0x72, ItemClassification.progression),
    "Treasure Box": ItemData(0x73, ItemClassification.progression),
    "Herbal Medicine": ItemData(0x75, ItemClassification.progression),
    "Pinwheel": ItemData(0x76, ItemClassification.progression),
    "Marlin Rod": ItemData(0x77, ItemClassification.progression),
    # Not sure if this should be an item as we already have the power in the item pool...
    # "Fog Pot":ItemData(0x9f,ItemClassification.progression),

    ## "Biteable" Items
    ### As these disappear and respanw each time you transition, the best way to handle those would be to set the flag
    ### making them appear/respawn active, instead of giving them to the player
    ### at a potential place where they can't use them.
    ### Edit: So this Sake only resets if you go outside Kamiki village or on of its interiors;
    ### I'm not sure how that's going to work with ER.
    "Vista of the Gods": ItemData(0x5C, ItemClassification.progression),
    "Tsuta Ruins Key": ItemData(0x40, ItemClassification.progression),
    # "Oddly Shaped Turnip": ItemData(0x41, ItemClassification.progression),

    # Useful items
    "Sun Fragment": ItemData(0x05, ItemClassification.useful),
    "Astral Pouch": ItemData(0x06, ItemClassification.useful),
    "Stray Bead": ItemData(0xCC, ItemClassification.useful),
    # probably will have to be changed to progession_skip balancing once DF shops get randomized
    "Demon Fang": ItemData(0x1F, ItemClassification.useful),
    # Technically a filler item, but useful feels more appropriate. Warping with those without Fountain will probably be out of logic.
    "Mermaid Coin": ItemData(0x0e, ItemClassification.useful),
    "Golden Peach": ItemData(0x0f, ItemClassification.useful),
    "Gold Dust": ItemData(0x9e, ItemClassification.useful),

    # Filler
    "Exorcism Slip L": ItemData(0x08, ItemClassification.filler),
    "Exorcism Slip M": ItemData(0x09, ItemClassification.filler),
    "Exorcism Slip S": ItemData(0x0a, ItemClassification.filler),
    "Vengeance Slip": ItemData(0x0c, ItemClassification.filler),
    "Inkfinity Stone": ItemData(0x0d, ItemClassification.filler),
    "Holy Bone L": ItemData(0x04, ItemClassification.filler),
    "Holy Bone S": ItemData(0x8F, ItemClassification.filler),
    "White porcelain pot": ItemData(0xA0, ItemClassification.filler),
    "Traveler's Charm": ItemData(0x70, ItemClassification.filler),
    "Holy Bone M": ItemData(0x8e, ItemClassification.filler),
    "Feedbag (Meat)": ItemData(0x90, ItemClassification.filler),
    "Feedbag (Herbs)": ItemData(0x91, ItemClassification.filler),
    "Feedbag (Seeds)": ItemData(0x92, ItemClassification.filler),
    "Feedbag (Fish)": ItemData(0x93, ItemClassification.filler),
    "Steel Fist Sake": ItemData(0x99, ItemClassification.filler),
    "Steel Soul Sake": ItemData(0x9a, ItemClassification.filler),
    "Godly Charm": ItemData(0x9b, ItemClassification.filler),
    "Kutani Pottery": ItemData(0xa1, ItemClassification.filler),
    "Incense Burner": ItemData(0xa3, ItemClassification.filler),
    "Vase": ItemData(0xa4, ItemClassification.filler),
    "Silver Pocket Watch": ItemData(0xa5, ItemClassification.filler),
    "Rat Statue": ItemData(0xa6, ItemClassification.filler),
    "Bull Horn": ItemData(0xa7, ItemClassification.filler),
    "Etched Glass": ItemData(0xa9, ItemClassification.filler),
    "Lacquerware Set": ItemData(0xaa, ItemClassification.filler),
    "Wooden Bear": ItemData(0xab, ItemClassification.filler),
    "Glass Beads": ItemData(0xad, ItemClassification.filler),
    "Dragonfly Bead": ItemData(0xae, ItemClassification.filler),
    "Coral Fragment": ItemData(0xb0, ItemClassification.filler),
    "Crystal": ItemData(0xb1, ItemClassification.filler),
    "Pearl": ItemData(0xb2, ItemClassification.filler),
    "Ruby Tassels": ItemData(0xb3, ItemClassification.filler),
    "Bull Statue": ItemData(0xb4, ItemClassification.filler),
    "Tiger Statue": ItemData(0xb5, ItemClassification.filler),
    "Rabbit Statue": ItemData(0xb6, ItemClassification.filler),
    "Dragon Statue": ItemData(0xb7, ItemClassification.filler),
    "Snake Statue": ItemData(0xb8, ItemClassification.filler),
    "Horse Statue": ItemData(0xb9, ItemClassification.filler),
    "Sheep Statue": ItemData(0xba, ItemClassification.filler),
    "Monkey Statue": ItemData(0xbb, ItemClassification.filler),
    "Rooster Statue": ItemData(0xbc, ItemClassification.filler),
    "Dog Statue": ItemData(0xbd, ItemClassification.filler),
    "Boar Statue": ItemData(0xbe, ItemClassification.filler),
    "Cat Statue": ItemData(0xbf, ItemClassification.filler),
    "Sapphire Tassels": ItemData(0xc0, ItemClassification.filler),
    "Emerald Tassels": ItemData(0xc1, ItemClassification.filler),
    "Turquoise Tassels": ItemData(0xc2, ItemClassification.filler),
    "Agate Tassels": ItemData(0xc3, ItemClassification.filler),
    "Amber Tassels": ItemData(0xc4, ItemClassification.filler),
    "Cat's Eye Tassels": ItemData(0xc5, ItemClassification.filler),
    "Amethyst Tassels": ItemData(0xc6, ItemClassification.filler),
    "Jade Tassels": ItemData(0xc7, ItemClassification.filler),
}

junk_weights = {
    "Holy Bone S": 1,
    "Demon Fang": 2,
    "White porcelain pot": 1,

    # Set junk_weight to 0 so additional copies won't be placed if there's space for them
    "Karmic Returner": 0,
    "Karmic Transformer 2":0,
    "Karmic Transformer 6":0,
    "Karmic Transformer 5":0,
    "Karmic Transformer 4":0,
    "Karmic Transformer 3":0,
    "Karmic Transformer 8":0,
    "Karmic Transformer 7":0,
    "Karmic Transformer 9":0,
    "Karmic Transformer 1":0,
}
# For items that need to appear more than once, I'll put the right numbers, but keep them commented to not flood
# the item pool while there aren't enough locations to place them
item_frequencies = {
    # "Sun Fragment": 15
    # "Stray Bead": 100
    # "Mermaid Coin" : 5
    # "Gold Dust": 15
}

item_table = {
    **okami_items,
}
