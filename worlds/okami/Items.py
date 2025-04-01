from BaseClasses import Item, ItemClassification
from .Types import OkamiItem, ItemData
from .Locations import get_total_locations
from .Rules import get_difficulty
from .Options import get_total_time_pieces, CTRLogic
from typing import List, Dict, TYPE_CHECKING


if TYPE_CHECKING:
    from . import OkamiWorld


def create_itempool(world: "OkamiWorld") -> List[Item]:
    itempool: List[Item] = []

    for name in item_table.keys():
        item_type: ItemClassification = item_table.get(name).classification
        itempool += create_multiple_items(world, name, item_frequencies.get(name, 1), item_type)
    itempool += create_junk_items(world, get_total_locations(world) - len(itempool))
    return itempool



def create_item(world: "OkamiWorld", name: str) -> Item:
    data = item_table[name]
    return OkamiItem(name, data.classification, data.code, world.player)


def create_multiple_items(world: "OkamiWorld", name: str, count: int = 1,item_type: ItemClassification = ItemClassification.progression) -> List[Item]:
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
            junk_pool.append(world.create_item(world.random.choices(list(junk_list.keys()), weights=list(junk_list.values()), k=1)[0]))
    return junk_pool


okami_items = {
    # Brush Techniques
    "Sunrise": ItemData(0x100, ItemClassification.progression),
    "Rejuvenation": ItemData(0x101, ItemClassification.progression),
    #TODO: Probably needs to be progressive at some point.
    "Power Slash" : ItemData(0x102, ItemClassification.progression),

    # Quest Items
    "Thunder Brew": ItemData(0x47, ItemClassification.progression),

    # Other
    "Astral Pouch": ItemData(0x06, ItemClassification.useful),
    "Stray Bead": ItemData(0xCC, ItemClassification.skip_balancing),

    # Filler
    "Holy Bone S": ItemData(0x8F, ItemClassification.filler),
}

junk_weights ={
    "Holy Bone S":1
}
# For items that need to appear more than once
item_frequencies ={
}

item_table = {
    **okami_items,
}
