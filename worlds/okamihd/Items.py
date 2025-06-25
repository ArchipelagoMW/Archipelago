from BaseClasses import Item, ItemClassification
from MultiServer import console
from .Types import OkamiItem, ItemData, BrushTechniques, BrushTechniqueData, DivineInstrumentData, DivineInstruments
from typing import List, Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from . import OkamiWorld


def create_item(world: "OkamiWorld", name: str) -> Item:
    data = item_table[name]
    return OkamiItem(name, data.classification, data.code, world.player)


def create_brush_techniques_items(world: "OkamiWorld")-> List[Item]:
    items = []
    for b in BrushTechniques.list():
        for i in range(b.item_count):
            items.append(create_brush_technique_item(world, b))

    return items

def create_brush_technique_item(world: "OkamiWorld", data: BrushTechniqueData) -> Item:
    return OkamiItem(data.item_name, data.item_classification, data.code, world.player)

def create_divine_instrument_items(world: "OkamiWorld",precollected_instrument:str|None)-> List[Item]:
    items = []
    for d in DivineInstruments.list():
        if precollected_instrument and d.item_name!=precollected_instrument:
            items.append(create_divine_instrument_item(world, d))
    return items

def create_divine_instrument_item(world:"OkamiWorld", data:DivineInstrumentData) -> Item:
    return OkamiItem(data.item_name, ItemClassification.progression,data.code,world.player)


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


okami_items = {
    # Equips
    #"Water Tablet": ItemData(0x9c, ItemClassification.progression),

    #Quest Items

    ## "Biteable" Items
    ### As these disappear and respanw each time you transition, the best way to handle those would be to set the flag
    ### making them appear/respawn active, instead of giving them to the player
    ### at a potential place where they can't use them.
    ### Edit: So this Sake only resets if you go outside Kamiki village or on of its interiors;
    ### I'm not sure how that's going to work with ER.
    ### TODO: Update their ids
    "Tsuta Ruins Key": ItemData(0x40,ItemClassification.progression),
    "Vista of the Gods" : ItemData(0x5C, ItemClassification.progression),

    # Other
    #"Astral Pouch": ItemData(0x06, ItemClassification.useful),
    #"Stray Bead": ItemData(0xCC, ItemClassification.skip_balancing),

    # Filler
    "Holy Bone S": ItemData(0x8F, ItemClassification.filler),
    "Demon Fang": ItemData(0x1F, ItemClassification.filler),
    "White porcelain pot":ItemData(0xA0, ItemClassification.filler)
}

junk_weights = {
    "Holy Bone S": 1,
    "Demon Fang":2,
    "White porcelain pot":1
}
# For items that need to appear more than once
item_frequencies = {
    #"Holy Bone S": 1,
}

item_table = {
    **okami_items,
}
