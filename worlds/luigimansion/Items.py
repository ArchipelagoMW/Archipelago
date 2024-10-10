from typing import NamedTuple, Dict, Set, Optional

from BaseClasses import Item
from BaseClasses import ItemClassification as IC


class LMItemData(NamedTuple):
    type: str
    code: Optional[int]
    classification: IC
    quantity: int = 1
    item_id: Optional[int] = None  # potentially use when we figure out how to receive items in game


class LMItem(Item):
    game: str = "Luigi's Mansion"

    def __init__(self, name: str, player: int, data: LMItemData, force_nonprogress: bool):
        adjusted_classification = IC.filler if force_nonprogress else data.classification
        super(LMItem, self).__init__(name, adjusted_classification, LMItem.get_apid(data.code), player)

        self.type = data.type
        self.item_id = data.item_id

    @staticmethod
    def get_apid(code: int):
        base_id: int = 8500
        return base_id + code if code is not None else None


item_table: dict[str, LMItemData] = {
    "Heart Key":           LMItemData('Suite Key',  0, IC.progression),
    "Club Key":            LMItemData('Suite Key',  1, IC.progression),
    "Diamond Key":         LMItemData('Suite Key',  2, IC.progression),
    "Spade Key":           LMItemData('Suite Key',  3, IC.progression),
    # 'Parlor Key':          LMItemData('Door Key',   04,), Left here in case I can play with starting location
    "Anteroom Key":        LMItemData('Door Key',   5, IC.progression),
    # 'Wardrobe Key':        LMItemData('Door Key',   06), does not actually exist
    "Front Hallway Key":   LMItemData('Door Key',   7, IC.progression),
    "Master Bedroom Key":  LMItemData('Door Key',   8, IC.progression),
    "Nursery Key":         LMItemData('Door Key',   9, IC.progression),
    "Twins Bedroom Key":   LMItemData('Door Key',   10, IC.progression),
    "Ballroom Key":        LMItemData('Door Key',   11, IC.progression),
    "Storage Room Key":    LMItemData('Door Key',   12, IC.progression),
    "Fortune Teller Key":  LMItemData('Door Key',   13, IC.progression),
    "Laundry Key":         LMItemData('Door Key',   14, IC.progression),
    "2F Stairwell Key":    LMItemData('Door Key',   15, IC.progression),
    "Conservatory Key":    LMItemData('Door Key',   16, IC.progression),
    "Dining Room Key":     LMItemData('Door Key',   17, IC.progression),
    "Rec Room Key":        LMItemData('Door Key',   18, IC.progression),
    "Billiards Key":       LMItemData('Door Key',   19, IC.progression),
    "Safari Key":          LMItemData('Door Key',   20, IC.progression),
    "Balcony Key":         LMItemData('Door Key',   21, IC.progression),
    "Breaker Key":         LMItemData('Door Key',   22, IC.progression),
    "Cellar Key":          LMItemData('Door Key',   23, IC.progression),
    "Clockwork Key":       LMItemData('Door Key',   24, IC.progression),
    "Armory Key":          LMItemData('Door Key',   25, IC.progression),
    "Sitting Room Key":    LMItemData('Door Key',   26, IC.progression),
    "Pipe Room Key":       LMItemData('Door Key',   27, IC.progression),
    "Cold Storage Key":    LMItemData('Door Key',   28, IC.progression),
    "Art Studio Key":      LMItemData('Door Key',   29, IC.progression),
    "Fire Element Medal":  LMItemData('Medal',      30, IC.progression),
    "Water Element Medal": LMItemData('Medal',      31, IC.progression),
    "Ice Element Medal":   LMItemData('Medal',      32, IC.progression),
    "Mario's Glove":       LMItemData('Mario Item', 33, IC.progression),
    "Mario's Hat":         LMItemData('Mario Item', 34, IC.progression),
    "Mario's Letter":      LMItemData('Mario Item', 35, IC.progression),
    "Mario's Star":        LMItemData('Mario Item', 36, IC.progression),
    "Mario's Shoe":        LMItemData('Mario Item', 37, IC.progression),
    "Boo":                 LMItemData('Boo Item',   38, IC.progression, 35),
    "Boo Radar":           LMItemData('Upgrade',    39, IC.progression),
    # does the Boo release cutscene trigger the butler, or is it acquiring the boo radar?
    "Poltergust 4000":     LMItemData('Upgrade',    40, IC.useful),
    "Treasure Bundle":     LMItemData('Filler',     41, IC.filler),
    "Poison Mushroom":     LMItemData('Trap',       42, IC.trap),
    "Ghost":               LMItemData('Trap',       43, IC.trap),
    "Nothing":             LMItemData('Filler',     44, IC.filler),
    "Small Heart":         LMItemData('Filler',     46, IC.filler),
    "Medium Heart":        LMItemData('Filler',     47, IC.filler),
    "Large Heart":         LMItemData('Filler',     48, IC.filler)
}

filler_items: Dict[str, LMItemData] = {
    "Treasure Bundle": LMItemData('Filler', 49, IC.filler),
    "Poison Mushroom": LMItemData('Trap', 50, IC.trap),
    "Ghost": LMItemData('Trap', 51, IC.trap),
    "Nothing": LMItemData('Filler', 52, IC.filler),
    "Small Heart": LMItemData('Filler', 53, IC.filler),
    "Medium Heart": LMItemData('Filler', 54, IC.filler),
    "Large Heart": LMItemData('Filler', 55, IC.filler)
}

LOOKUP_ID_TO_NAME: dict[int, str] = {
    LMItem.get_apid(data.code): item for item, data in item_table.items() if data.code is not None
}


def get_item_names_per_category() -> Dict[str, Set[str]]:
    categories: Dict[str, Set[str]] = {}

    for name, data in item_table.items():
        categories.setdefault(data.type, set()).add(name)

    return categories
