from typing import Dict, Set, Tuple, NamedTuple
from BaseClasses import ItemClassification

class ItemData(NamedTuple):
    group: str
    code: int
    classification: ItemClassification = 0b0001
    count: int = 1

item_table: Dict[str, ItemData] = {
    'Heart Key':            ItemData('Suite Key',  8500),
    'Club Key':             ItemData('Suite Key',  8501),
    'Diamond Key':          ItemData('Suite Key',  8502),
    'Spade Key':            ItemData('Suite Key',  8503),
    #'Parlor Key':           ItemData('Door Key',   8504,), Left here in case I can play with starting location
    'Anteroom Key':         ItemData('Door Key',   8505),
    #'Wardrobe Key':         ItemData('Door Key',   8506), does not actually exist
    'Front Hallway Key':    ItemData('Door Key',   8507),
    'Master Bedroom Key':   ItemData('Door Key',   8508),
    'Nursery Key':          ItemData('Door Key',   8509),
    'Twins Bedroom Key':    ItemData('Door Key',   8510),
    'Ballroom Key':         ItemData('Door Key',   8511),
    'Storage Room Key':     ItemData('Door Key',   8512),
    'Fortune Teller Key':   ItemData('Door Key',   8513),
    'Laundry Key':          ItemData('Door Key',   8514),
    '2F Stairwell Key':     ItemData('Door Key',   8515),
    'Conservatory Key':     ItemData('Door Key',   8516),
    'Dining Room Key':      ItemData('Door Key',   8517),
    'Rec Room Key':         ItemData('Door Key',   8518),
    'Billiards Key':        ItemData('Door Key',   8519),
    'Safari Key':           ItemData('Door Key',   8520),
    'Balcony Key':          ItemData('Door Key',   8521),
    #'Breaker Key':              ItemData('Door Key',   8522,), Special logic needed
    'Cellar Key':           ItemData('Door Key',   8523),
    'Clockwork Key':        ItemData('Door Key',   8524),
    'Armory Key':           ItemData('Door Key',   8525),
    'Sitting Room Key':     ItemData('Door Key',   8526),
    'Pipe Room Key':        ItemData('Door Key',   8527),
    'Cold Storage Key':     ItemData('Door Key',   8528),
    'Art Studio Key':       ItemData('Door Key',   8529),
    'Fire Element Medal':   ItemData('Medal',      8530),
    'Water Element Medal':  ItemData('Medal',      8531),
    'Ice Element Medal':    ItemData('Medal',      8532),
    'Mario\'s Glove':       ItemData('Mario Item', 8533),
    'Mario\'s Hat':         ItemData('Mario Item', 8534),
    'Mario\'s Letter':      ItemData('Mario Item', 8535),
    'Mario\'s Star':        ItemData('Mario Item', 8536),
    'Mario\'s Shoe':        ItemData('Mario Item', 8537),
    'Boo':                  ItemData('Boo',        8538, Count=50),
    'Boo Radar':            ItemData('Upgrade',    8539),
    'Poltergust 4000':      ItemData('Upgrade',    8540, 0b0010),
    'Treasure Bundle':      ItemData('Filler',     8541, 0b0000),
    'Poison Mushroom':      ItemData('Trap',       8542, 0b0100),
    'Ghost':                ItemData('Trap',       8543, 0b0100),
    'Nothing':              ItemData('FIller',     8544, 0b0000)
}

