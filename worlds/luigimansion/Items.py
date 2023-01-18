from typing import Dict, Set, Tuple, NamedTuple

class ItemData(NamedTuple):
    category: str
    code: int
    count: int = 1
    progression: bool = False
    useful: bool = False



# Treasures are a form of junk item for the purposes of the randomizer
item_table: Dict[str, ItemData] = {
    'Heart Key':            ItemData('Suite Key',  8500, progression=True),
    'Club Key':             ItemData('Suite Key',  8501, progression=True),
    'Diamond Key':          ItemData('Suite Key',  8502, progression=True),
    'Spade Key':            ItemData('Suite Key',  8503, progression=True),
    'Parlor Key':           ItemData('Door Key',   8504, progression=True),
    'Anteroom Key':         ItemData('Door Key',   8505, progression=True),
    'Wardrobe Key':         ItemData('Door Key',   8506, progression=True),
    'Front Hallway Key':    ItemData('Door Key',   8507, progression=True),
    'Master Bedroom Key':   ItemData('Door Key',   8508, progression=True),
    'Nursery Key':          ItemData('Door Key',   8509, progression=True),
    'Twins Bedroom Key':    ItemData('Door Key',   8510, progression=True),
    'Ballroom Key':         ItemData('Door Key',   8511, progression=True),
    'Storage Room Key':     ItemData('Door Key',   8512, progression=True),
    'Fortune Teller Key':   ItemData('Door Key',   8513, progression=True),
    'Laundry Key':          ItemData('Door Key',   8514, progression=True),
    #'Butler Key':              ItemData('Door Key',   8515, progression=True),
    'Conservatory Key':     ItemData('Door Key',   8516, progression=True),
    'Dining Room Key':      ItemData('Door Key',   8517, progression=True),
    'Rec Room Key':         ItemData('Door Key',   8518, progression=True),
    'Billiards Key':        ItemData('Door Key',   8519, progression=True),
    'Safari Key':           ItemData('Door Key',   8520, progression=True),
    'Balcony Key':          ItemData('Door Key',   8521, progression=True),
    #'Breaker Key':              ItemData('Door Key',   8522, progression=True),
    'Cellar Key':           ItemData('Door Key',   8523, progression=True),
    'Clockwork Key':        ItemData('Door Key',   8524, progression=True),
    'Armory Key':           ItemData('Door Key',   8525, progression=True),
    'Sitting Room Key':     ItemData('Door Key',   8526, progression=True),
    'Pipe Room Key':        ItemData('Door Key',   8527, progression=True),
    'Cold Storage Key':     ItemData('Door Key',   8528, progression=True),
    'Art Studio Key':       ItemData('Door Key',   8529, progression=True),
    'Fire Element Medal':   ItemData('Medal',      8530, progression=True),
    'Water Element Medal':  ItemData('Medal',      8531, progression=True),
    'Ice Element Medal':    ItemData('Medal',      8532, progression=True),
    'Mario\'s Glove':       ItemData('Mario Item', 8533, progression=True),
    'Mario\'s Hat':         ItemData('Mario Item', 8534, progression=True),
    'Mario\'s Letter':      ItemData('Mario Item', 8535, progression=True),
    'Mario\'s Star':        ItemData('Mario Item', 8536, progression=True),
    'Mario\'s Shoe':        ItemData('Mario Item', 8537, progression=True),
    'Boo Radar':            ItemData('Boo Radar',  8538, progression=True),
    'Poltergust 4000':      ItemData('Upgrade',    8539, useful=True),
    'Treasure Bundle':      ItemData('Treasure',   8540)
}

