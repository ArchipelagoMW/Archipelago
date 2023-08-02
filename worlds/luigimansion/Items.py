from typing import Dict, NamedTuple, Set

from BaseClasses import ItemClassification, Item


class LMItem(Item):
    game = "Luigi's Mansion"


class ItemData(NamedTuple):
    group: str
    code: int
    classification: ItemClassification
    count: int = 1


item_table: Dict[str, ItemData] = {
    "Heart Key": ItemData('Suite Key', 8500, ItemClassification.progression),
    "Club Key": ItemData('Suite Key', 8501, ItemClassification.progression),
    "Diamond Key": ItemData('Suite Key', 8502, ItemClassification.progression),
    "Spade Key": ItemData('Suite Key', 8503, ItemClassification.progression),
    # 'Parlor Key':          ItemData('Door Key',   8504,), Left here in case I can play with starting location
    "Anteroom Key": ItemData('Door Key', 8505, ItemClassification.progression),
    # 'Wardrobe Key':        ItemData('Door Key',   8506), does not actually exist
    "Front Hallway Key": ItemData('Door Key', 8507, ItemClassification.progression),
    "Master Bedroom Key": ItemData('Door Key', 8508, ItemClassification.progression),
    "Nursery Key": ItemData('Door Key', 8509, ItemClassification.progression),
    "Twins Bedroom Key": ItemData('Door Key', 8510, ItemClassification.progression),
    "Ballroom Key": ItemData('Door Key', 8511, ItemClassification.progression),
    "Storage Room Key": ItemData('Door Key', 8512, ItemClassification.progression),
    "Fortune Teller Key": ItemData('Door Key', 8513, ItemClassification.progression),
    "Laundry Key": ItemData('Door Key', 8514, ItemClassification.progression),
    "2F Stairwell Key": ItemData('Door Key', 8515, ItemClassification.progression),
    "Conservatory Key": ItemData('Door Key', 8516, ItemClassification.progression),
    "Dining Room Key": ItemData('Door Key', 8517, ItemClassification.progression),
    "Rec Room Key": ItemData('Door Key', 8518, ItemClassification.progression),
    "Billiards Key": ItemData('Door Key', 8519, ItemClassification.progression),
    "Safari Key": ItemData('Door Key', 8520, ItemClassification.progression),
    "Balcony Key": ItemData('Door Key', 8521, ItemClassification.progression),
    "Breaker Key": ItemData('Door Key', 8522, ItemClassification.progression),
    "Cellar Key": ItemData('Door Key', 8523, ItemClassification.progression),
    "Clockwork Key": ItemData('Door Key', 8524, ItemClassification.progression),
    "Armory Key": ItemData('Door Key', 8525, ItemClassification.progression),
    "Sitting Room Key": ItemData('Door Key', 8526, ItemClassification.progression),
    "Pipe Room Key": ItemData('Door Key', 8527, ItemClassification.progression),
    "Cold Storage Key": ItemData('Door Key', 8528, ItemClassification.progression),
    "Art Studio Key": ItemData('Door Key', 8529, ItemClassification.progression),
    "Fire Element Medal": ItemData('Medal', 8530, ItemClassification.progression),
    "Water Element Medal": ItemData('Medal', 8531, ItemClassification.progression),
    "Ice Element Medal": ItemData('Medal', 8532, ItemClassification.progression),
    "Mario's Glove": ItemData('Mario Item', 8533, ItemClassification.progression),
    "Mario's Hat": ItemData('Mario Item', 8534, ItemClassification.progression),
    "Mario's Letter": ItemData('Mario Item', 8535, ItemClassification.progression),
    "Mario's Star": ItemData('Mario Item', 8536, ItemClassification.progression),
    "Mario's Shoe": ItemData('Mario Item', 8537, ItemClassification.progression),
    "Boo": ItemData('Boo', 8538, ItemClassification.progression, count=50),
    "Boo Radar": ItemData('Upgrade', 8539, ItemClassification.progression),
    # does the Boo release cutscene trigger the butler, or is it acquiring the boo radar?
    "Poltergust 4000": ItemData('Upgrade', 8540, ItemClassification.useful),
    "Treasure Bundle": ItemData('Filler', 8541, ItemClassification.filler),
    "Poison Mushroom": ItemData('Trap', 8542, ItemClassification.trap),
    "Ghost": ItemData('Trap', 8543, ItemClassification.trap),
    "Nothing": ItemData('Filler', 8544, ItemClassification.filler),
    "Small Heart": ItemData('Filler', 8546, ItemClassification.filler),
    "Medium Heart": ItemData('Filler', 8547, ItemClassification.filler),
    "Large Heart": ItemData('Filler', 8548, ItemClassification.filler)
}

filler_items: Dict[str, ItemData] = {
    "Treasure Bundle": ItemData('Filler', 8549, ItemClassification.filler),
    "Poison Mushroom": ItemData('Trap', 8550, ItemClassification.trap),
    "Ghost": ItemData('Trap', 8551, ItemClassification.trap),
    "Nothing": ItemData('Filler', 8552, ItemClassification.filler),
    "Small Heart": ItemData('Filler', 8553, ItemClassification.filler),
    "Medium Heart": ItemData('Filler', 8554, ItemClassification.filler),
    "Large Heart": ItemData('Filler', 8555, ItemClassification.filler)
}


def get_item_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in item_table.items():
        categories.setdefault(data.group, set()).add(name)

    return categories
