from __future__ import annotations

from enum import IntEnum
from typing import Any, Iterable, NamedTuple, Optional, Tuple, Union

from BaseClasses import Item, ItemClassification as IC

from .data import ap_id_offset, ItemFlag, Passage


# Items are encoded as 8-bit numbers as follows:
#                   | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
# Jewel pieces:     | 0   0   0 |  passage  | qdrnt |
# CD:               | 0   0   1 |  passage  | level |
# Wario abilities:  | 0   1   0   0   0 |  ability  |
# Golden treasures: | 0   1   1   1 |   treasure    |
#
# Junk items:       | 1   0   0   0 |     type      |
# AP item:          | 1   1   1   1   0 |   class   |
#
# For jewel pieces:
#  - passage = 0-5 for entry/emerald/ruby/topaz/sapphire/golden
#  - qdrnt = quadrant, increasing counterclockwise from top left
#
# For CDs:
#  - passage = 0-5 same as jewel pieces, but only 1-4 has a CD
#  - level = increasing as the level goes deeper
#
# For Wario abilities:
#  - 0 = Progressive Ground Pound
#  - 1 = Swimming
#  - 2 = Head Smash
#  - 3 = Progressive Grab
#  - 4 = Dash Attack
#  - 5 = Stomp Jump
#
# Type for junk items:
#  - 0 = Full health item
#  - 1 = Wario form trap
#  - 2 = Single heart recovery
#  - 3 = Single heart damage
#  - 4 = Minigame Medal
#
# Classification for AP items:
#  - 0 = Filler
#  - 1 = Progression
#  - 2 = Useful
#  - 3 = Trap


class Box(IntEnum):
    JEWEL_NE = 0
    JEWEL_SE = 1
    JEWEL_SW = 2
    JEWEL_NW = 3
    CD = 4
    FULL_HEALTH = 5


class ItemType(IntEnum):
    JEWEL = 0
    CD = 1
    ITEM = 2
    ABILITY = 4
    TREASURE = 5


def ap_id_from_wl4_data(data: ItemData) -> int:
    cat, itemid, _ = data
    if cat == ItemType.JEWEL:
        passage, quad = itemid
        item = (passage << 2) | quad
    elif cat == ItemType.CD:
        passage, level = itemid
        item = (1 << 5) | (passage << 2) | level
    elif cat == ItemType.ABILITY:
        item = (1 << 6) | itemid
    elif cat == ItemType.ITEM:
        item = (1 << 7) | itemid
    elif cat == ItemType.TREASURE:
        item = 0x70 | itemid
    else:
        raise ValueError(f'Unexpected WL4 item type: {cat}')
    return ap_id_offset + item


def wl4_data_from_ap_id(ap_id: int) -> Tuple[str, ItemData]:
    val = ap_id - ap_id_offset
    if val >> 6 == 0:
        passage = (val & 0x1C) >> 2
        if val >> 5 == 0:
            quad = val & 3
            candidates = tuple(filter(lambda d: d[1][0] == ItemType.JEWEL and
                                                d[1][1][0] == passage and
                                                d[1][1][1] == quad,
                                      item_table.items()))
        else:
            level = val & 3
            candidates = tuple(filter(lambda d: d[1][0] == ItemType.CD and
                                                d[1][1] == (passage, level),
                                      item_table.items()))
    elif val >> 3 == 8:
        candidates = tuple(filter(lambda d: d[1][0] == ItemType.ABILITY and
                                            d[1][1] == val,
                                  item_table.items()))
    elif val >> 4 == 7:
        candidates = tuple(filter(lambda d: d[1][0] == ItemType.TREASURE and
                                            d[1][1] == val,
                                  item_table.items()))
    elif val >> 4 == 8:
        candidates = tuple(filter(lambda d: d[1][0] == ItemType.ITEM and
                                            d[1][1] == val,
                                  item_table.items()))
    else:
        candidates = ()

    if not candidates:
        raise ValueError(f'Could not find WL4 item ID: {ap_id}')
    return candidates[0]


class WL4Item(Item):
    game: str = 'Wario Land 4'
    type: Optional[ItemType]
    passage: Optional[Passage]
    level: Optional[int]
    flag: Optional[ItemFlag]

    def __init__(self, name: str, player: int, force_non_progression: bool = False):
        if name in item_table:
            data = item_table[name]
            self.type, id, prog = data
            code = ap_id_from_wl4_data(data)
        else:
            self.type = code = None
            prog = IC.progression
        super(WL4Item, self).__init__(name, IC.filler if force_non_progression else prog, code, player)
        if self.type == ItemType.JEWEL:
            self.passage = id[0]
            self.level = None
            self.flag = 1 << id[1]
        elif self.type == ItemType.CD:
            self.passage, self.level = id
            self.flag = ItemFlag.CD
        else:
            self.passage = self.level = self.flag = None


class ItemData(NamedTuple):
    type: ItemType
    id: Union[Tuple[Passage, Box], Tuple[Passage, int], int]
    prog: IC

    def passage(self):
        if not isinstance(self.id, tuple):
            return None
        return self.id[0]

    def box(self) -> Optional[Box]:
        if self.type == ItemType.JEWEL:
            return self.id[1]
        if self.type == ItemType.CD:
            return Box.CD
        return None


item_table = {
    # Item name                                  Item type          ID                                 Progression
    'Top Right Entry Jewel Piece':      ItemData(ItemType.JEWEL,    (Passage.ENTRY,    Box.JEWEL_NE),  IC.filler),
    'Top Right Emerald Piece':          ItemData(ItemType.JEWEL,    (Passage.EMERALD,  Box.JEWEL_NE),  IC.progression_skip_balancing),
    'Top Right Ruby Piece':             ItemData(ItemType.JEWEL,    (Passage.RUBY,     Box.JEWEL_NE),  IC.progression_skip_balancing),
    'Top Right Topaz Piece':            ItemData(ItemType.JEWEL,    (Passage.TOPAZ,    Box.JEWEL_NE),  IC.progression_skip_balancing),
    'Top Right Sapphire Piece':         ItemData(ItemType.JEWEL,    (Passage.SAPPHIRE, Box.JEWEL_NE),  IC.progression_skip_balancing),
    'Top Right Golden Jewel Piece':     ItemData(ItemType.JEWEL,    (Passage.GOLDEN,   Box.JEWEL_NE),  IC.progression_skip_balancing),
    'Bottom Right Entry Jewel Piece':   ItemData(ItemType.JEWEL,    (Passage.ENTRY,    Box.JEWEL_SE),  IC.filler),
    'Bottom Right Emerald Piece':       ItemData(ItemType.JEWEL,    (Passage.EMERALD,  Box.JEWEL_SE),  IC.progression_skip_balancing),
    'Bottom Right Ruby Piece':          ItemData(ItemType.JEWEL,    (Passage.RUBY,     Box.JEWEL_SE),  IC.progression_skip_balancing),
    'Bottom Right Topaz Piece':         ItemData(ItemType.JEWEL,    (Passage.TOPAZ,    Box.JEWEL_SE),  IC.progression_skip_balancing),
    'Bottom Right Sapphire Piece':      ItemData(ItemType.JEWEL,    (Passage.SAPPHIRE, Box.JEWEL_SE),  IC.progression_skip_balancing),
    'Bottom Right Golden Jewel Piece':  ItemData(ItemType.JEWEL,    (Passage.GOLDEN,   Box.JEWEL_SE),  IC.progression_skip_balancing),
    'Bottom Left Entry Jewel Piece':    ItemData(ItemType.JEWEL,    (Passage.ENTRY,    Box.JEWEL_SW),  IC.filler),
    'Bottom Left Emerald Piece':        ItemData(ItemType.JEWEL,    (Passage.EMERALD,  Box.JEWEL_SW),  IC.progression_skip_balancing),
    'Bottom Left Ruby Piece':           ItemData(ItemType.JEWEL,    (Passage.RUBY,     Box.JEWEL_SW),  IC.progression_skip_balancing),
    'Bottom Left Topaz Piece':          ItemData(ItemType.JEWEL,    (Passage.TOPAZ,    Box.JEWEL_SW),  IC.progression_skip_balancing),
    'Bottom Left Sapphire Piece':       ItemData(ItemType.JEWEL,    (Passage.SAPPHIRE, Box.JEWEL_SW),  IC.progression_skip_balancing),
    'Bottom Left Golden Jewel Piece':   ItemData(ItemType.JEWEL,    (Passage.GOLDEN,   Box.JEWEL_SW),  IC.progression_skip_balancing),
    'Top Left Entry Jewel Piece':       ItemData(ItemType.JEWEL,    (Passage.ENTRY,    Box.JEWEL_NW),  IC.filler),
    'Top Left Emerald Piece':           ItemData(ItemType.JEWEL,    (Passage.EMERALD,  Box.JEWEL_NW),  IC.progression_skip_balancing),
    'Top Left Ruby Piece':              ItemData(ItemType.JEWEL,    (Passage.RUBY,     Box.JEWEL_NW),  IC.progression_skip_balancing),
    'Top Left Topaz Piece':             ItemData(ItemType.JEWEL,    (Passage.TOPAZ,    Box.JEWEL_NW),  IC.progression_skip_balancing),
    'Top Left Sapphire Piece':          ItemData(ItemType.JEWEL,    (Passage.SAPPHIRE, Box.JEWEL_NW),  IC.progression_skip_balancing),
    'Top Left Golden Jewel Piece':      ItemData(ItemType.JEWEL,    (Passage.GOLDEN,   Box.JEWEL_NW),  IC.progression_skip_balancing),
    'About that Shepherd CD':           ItemData(ItemType.CD,       (Passage.EMERALD,  0),             IC.filler),
    'Things that Never Change CD':      ItemData(ItemType.CD,       (Passage.EMERALD,  1),             IC.filler),
    "Tomorrow's Blood Pressure CD":     ItemData(ItemType.CD,       (Passage.EMERALD,  2),             IC.filler),
    'Beyond the Headrush CD':           ItemData(ItemType.CD,       (Passage.EMERALD,  3),             IC.filler),
    'Driftwood & the Island Dog CD':    ItemData(ItemType.CD,       (Passage.RUBY,     0),             IC.filler),
    "The Judge's Feet CD":              ItemData(ItemType.CD,       (Passage.RUBY,     1),             IC.filler),
    "The Moon's Lamppost CD":           ItemData(ItemType.CD,       (Passage.RUBY,     2),             IC.filler),
    'Soft Shell CD':                    ItemData(ItemType.CD,       (Passage.RUBY,     3),             IC.filler),
    'So Sleepy CD':                     ItemData(ItemType.CD,       (Passage.TOPAZ,    0),             IC.filler),
    'The Short Futon CD':               ItemData(ItemType.CD,       (Passage.TOPAZ,    1),             IC.filler),
    'Avocado Song CD':                  ItemData(ItemType.CD,       (Passage.TOPAZ,    2),             IC.filler),
    'Mr. Fly CD':                       ItemData(ItemType.CD,       (Passage.TOPAZ,    3),             IC.filler),
    "Yesterday's Words CD":             ItemData(ItemType.CD,       (Passage.SAPPHIRE, 0),             IC.filler),
    'The Errand CD':                    ItemData(ItemType.CD,       (Passage.SAPPHIRE, 1),             IC.filler),
    'You and Your Shoes CD':            ItemData(ItemType.CD,       (Passage.SAPPHIRE, 2),             IC.filler),
    'Mr. Ether & Planaria CD':          ItemData(ItemType.CD,       (Passage.SAPPHIRE, 3),             IC.filler),
    'Progressive Ground Pound':         ItemData(ItemType.ABILITY,  0x40,                              IC.progression),
    'Swim':                             ItemData(ItemType.ABILITY,  0x41,                              IC.progression),
    'Head Smash':                       ItemData(ItemType.ABILITY,  0x42,                              IC.progression),
    'Progressive Grab':                 ItemData(ItemType.ABILITY,  0x43,                              IC.progression),
    'Dash Attack':                      ItemData(ItemType.ABILITY,  0x44,                              IC.progression),
    'Stomp Jump':                       ItemData(ItemType.ABILITY,  0x45,                              IC.progression),
    'Golden Tree Pot':                  ItemData(ItemType.TREASURE, 0x70,                              IC.progression_skip_balancing),
    'Golden Apple':                     ItemData(ItemType.TREASURE, 0x71,                              IC.progression_skip_balancing),
    'Golden Fish':                      ItemData(ItemType.TREASURE, 0x72,                              IC.progression_skip_balancing),
    'Golden Candle Holder':             ItemData(ItemType.TREASURE, 0x73,                              IC.progression_skip_balancing),
    'Golden Lamp':                      ItemData(ItemType.TREASURE, 0x74,                              IC.progression_skip_balancing),
    'Golden Crescent Moon Bed':         ItemData(ItemType.TREASURE, 0x75,                              IC.progression_skip_balancing),
    'Golden Teddy Bear':                ItemData(ItemType.TREASURE, 0x76,                              IC.progression_skip_balancing),
    'Golden Lollipop':                  ItemData(ItemType.TREASURE, 0x77,                              IC.progression_skip_balancing),
    'Golden Game Boy Advance':          ItemData(ItemType.TREASURE, 0x78,                              IC.progression_skip_balancing),
    'Golden Robot':                     ItemData(ItemType.TREASURE, 0x79,                              IC.progression_skip_balancing),
    'Golden Rocket':                    ItemData(ItemType.TREASURE, 0x7A,                              IC.progression_skip_balancing),
    'Golden Rocking Horse':             ItemData(ItemType.TREASURE, 0x7B,                              IC.progression_skip_balancing),
    'Full Health Item':                 ItemData(ItemType.ITEM,     0x80,                              IC.useful),
    'Wario Form Trap':                  ItemData(ItemType.ITEM,     0x81,                              IC.trap),
    'Heart':                            ItemData(ItemType.ITEM,     0x82,                              IC.filler),
    'Lightning Trap':                   ItemData(ItemType.ITEM,     0x83,                              IC.trap),
    'Minigame Medal':                   ItemData(ItemType.ITEM,     0x84,                              IC.filler),
    'Diamond':                          ItemData(ItemType.ITEM,     0x85,                              IC.filler),
}


def filter_items(*, type: Optional[ItemType] = None, passage: Optional[Passage] = None) -> Iterable[Tuple[str, ItemData]]:
    items: Iterable[Tuple[str, ItemData]] = item_table.items()
    if type is not None:
        items = filter(lambda i: i[1].type == type, items)
    if passage is not None:
        items = filter(lambda i: i[1].passage() == passage, items)
    return items


def filter_item_names(*, type: Optional[ItemType] = None, passage: Optional[Passage] = None) -> Iterable[str]:
    return map(lambda entry: entry[0], filter_items(type=type, passage=passage))
