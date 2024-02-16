from __future__ import annotations

from typing import Any, Iterable, NamedTuple, Optional, Tuple

from BaseClasses import Item
from BaseClasses import ItemClassification as IC

from .data import ap_id_offset
from .types import Box, ItemFlag, ItemType, Passage


# Items are encoded as 8-bit numbers as follows:
#                   | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
# Jewel pieces:     | 0   0   0 |  passage  | qdrnt |
# CD:               | 0   0   1 |  passage  | level |
# Wario abilities:  | 0   1   0   0   0 |  ability  |
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
#  - 5 = Enemy Jump
#
# Type for junk items:
#  - 0 = Full health item
#  - 1 = Wario form trap
#  - 2 = Single heart recovery
#  - 3 = Single heart damage
#  - 4 = Minigame coin
#
# For AP item, classifications are as reported by ItemClassification.as_flag()


def ap_id_from_wl4_data(data: ItemData) -> int:
    cat, itemid, _ = data
    if cat == ItemType.EVENT or itemid == None:
        return None
    if cat == ItemType.JEWEL:
        passage, quad = itemid
        return ap_id_offset + (passage << 2) | quad
    elif cat == ItemType.CD:
        passage, level = itemid
        return ap_id_offset + (1 << 5) | (passage << 2) | level
    elif cat == ItemType.ABILITY:
        return ap_id_offset + (1 << 6) | itemid
    elif cat == ItemType.ITEM:
        return ap_id_offset + (1 << 7) | itemid
    else:
        raise ValueError(f'Unexpected WL4 item type: {data[0]}')


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
        elif val >> 5 == 1:
            level = val & 3
            candidates = tuple(filter(lambda d: d[1][0] == ItemType.CD and
                                                d[1][1] == (passage, level),
                                      item_table.items()))
    elif val >> 4 == 4:
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
    type: ItemType
    passage: Optional[Passage]
    level: Optional[int]
    flag: Optional[ItemFlag]

    def __init__(self, name, player, data, force_non_progression):
        type, id, prog = data
        if force_non_progression:
            prog = IC.filler
        super(WL4Item, self).__init__(name, prog, ap_id_from_wl4_data(data), player)
        self.type = type
        if type == ItemType.JEWEL:
            self.passage = id[0]
            self.level = None
            self.flag = 1 << id[1]
        elif type == ItemType.CD:
            self.passage, self.level = id
            self.flag = ItemFlag.CD
        else:
            self.passage = self.level = self.flag = None

    @classmethod
    def from_name(cls, name: str, player: int, force_non_progression: bool = False):
        data = item_table[name]
        created_item = cls(name, player, data, force_non_progression)
        return created_item


class ItemData(NamedTuple):
    type: ItemType
    id: Any
    prog: IC

    def passage(self):
        if not isinstance(self.id, tuple):
            return None
        return self.id[0]

    def box(self):
        if self.type == ItemType.JEWEL:
            return self.id[1]
        elif self.type == ItemType.CD:
            return Box.CD
        else:
            return None


item_table = {
    # Item name                                  Item type          ID                                 Progression
    'Top Right Entry Jewel Piece':      ItemData(ItemType.JEWEL,   (Passage.ENTRY,    Box.JEWEL_NE),  IC.progression_skip_balancing),
    'Top Right Emerald Piece':          ItemData(ItemType.JEWEL,   (Passage.EMERALD,  Box.JEWEL_NE),  IC.progression_skip_balancing),
    'Top Right Ruby Piece':             ItemData(ItemType.JEWEL,   (Passage.RUBY,     Box.JEWEL_NE),  IC.progression_skip_balancing),
    'Top Right Topaz Piece':            ItemData(ItemType.JEWEL,   (Passage.TOPAZ,    Box.JEWEL_NE),  IC.progression_skip_balancing),
    'Top Right Sapphire Piece':         ItemData(ItemType.JEWEL,   (Passage.SAPPHIRE, Box.JEWEL_NE),  IC.progression_skip_balancing),
    'Top Right Golden Jewel Piece':     ItemData(ItemType.JEWEL,   (Passage.GOLDEN,   Box.JEWEL_NE),  IC.progression_skip_balancing),
    'Bottom Right Entry Jewel Piece':   ItemData(ItemType.JEWEL,   (Passage.ENTRY,    Box.JEWEL_SE),  IC.progression_skip_balancing),
    'Bottom Right Emerald Piece':       ItemData(ItemType.JEWEL,   (Passage.EMERALD,  Box.JEWEL_SE),  IC.progression_skip_balancing),
    'Bottom Right Ruby Piece':          ItemData(ItemType.JEWEL,   (Passage.RUBY,     Box.JEWEL_SE),  IC.progression_skip_balancing),
    'Bottom Right Topaz Piece':         ItemData(ItemType.JEWEL,   (Passage.TOPAZ,    Box.JEWEL_SE),  IC.progression_skip_balancing),
    'Bottom Right Sapphire Piece':      ItemData(ItemType.JEWEL,   (Passage.SAPPHIRE, Box.JEWEL_SE),  IC.progression_skip_balancing),
    'Bottom Right Golden Jewel Piece':  ItemData(ItemType.JEWEL,   (Passage.GOLDEN,   Box.JEWEL_SE),  IC.progression_skip_balancing),
    'Bottom Left Entry Jewel Piece':    ItemData(ItemType.JEWEL,   (Passage.ENTRY,    Box.JEWEL_SW),  IC.progression_skip_balancing),
    'Bottom Left Emerald Piece':        ItemData(ItemType.JEWEL,   (Passage.EMERALD,  Box.JEWEL_SW),  IC.progression_skip_balancing),
    'Bottom Left Ruby Piece':           ItemData(ItemType.JEWEL,   (Passage.RUBY,     Box.JEWEL_SW),  IC.progression_skip_balancing),
    'Bottom Left Topaz Piece':          ItemData(ItemType.JEWEL,   (Passage.TOPAZ,    Box.JEWEL_SW),  IC.progression_skip_balancing),
    'Bottom Left Sapphire Piece':       ItemData(ItemType.JEWEL,   (Passage.SAPPHIRE, Box.JEWEL_SW),  IC.progression_skip_balancing),
    'Bottom Left Golden Jewel Piece':   ItemData(ItemType.JEWEL,   (Passage.GOLDEN,   Box.JEWEL_SW),  IC.progression_skip_balancing),
    'Top Left Entry Jewel Piece':       ItemData(ItemType.JEWEL,   (Passage.ENTRY,    Box.JEWEL_NW),  IC.progression_skip_balancing),
    'Top Left Emerald Piece':           ItemData(ItemType.JEWEL,   (Passage.EMERALD,  Box.JEWEL_NW),  IC.progression_skip_balancing),
    'Top Left Ruby Piece':              ItemData(ItemType.JEWEL,   (Passage.RUBY,     Box.JEWEL_NW),  IC.progression_skip_balancing),
    'Top Left Topaz Piece':             ItemData(ItemType.JEWEL,   (Passage.TOPAZ,    Box.JEWEL_NW),  IC.progression_skip_balancing),
    'Top Left Sapphire Piece':          ItemData(ItemType.JEWEL,   (Passage.SAPPHIRE, Box.JEWEL_NW),  IC.progression_skip_balancing),
    'Top Left Golden Jewel Piece':      ItemData(ItemType.JEWEL,   (Passage.GOLDEN,   Box.JEWEL_NW),  IC.progression_skip_balancing),
    'About that Shepherd CD':           ItemData(ItemType.CD,      (Passage.EMERALD,  0),             IC.filler),
    'Things that Never Change CD':      ItemData(ItemType.CD,      (Passage.EMERALD,  1),             IC.filler),
    "Tomorrow's Blood Pressure CD":     ItemData(ItemType.CD,      (Passage.EMERALD,  2),             IC.filler),
    'Beyond the Headrush CD':           ItemData(ItemType.CD,      (Passage.EMERALD,  3),             IC.filler),
    'Driftwood & the Island Dog CD':    ItemData(ItemType.CD,      (Passage.RUBY,     0),             IC.filler),
    "The Judge's Feet CD":              ItemData(ItemType.CD,      (Passage.RUBY,     1),             IC.filler),
    "The Moon's Lamppost CD":           ItemData(ItemType.CD,      (Passage.RUBY,     2),             IC.filler),
    'Soft Shell CD':                    ItemData(ItemType.CD,      (Passage.RUBY,     3),             IC.filler),
    'So Sleepy CD':                     ItemData(ItemType.CD,      (Passage.TOPAZ,    0),             IC.filler),
    'The Short Futon CD':               ItemData(ItemType.CD,      (Passage.TOPAZ,    1),             IC.filler),
    'Avocado Song CD':                  ItemData(ItemType.CD,      (Passage.TOPAZ,    2),             IC.filler),
    'Mr. Fly CD':                       ItemData(ItemType.CD,      (Passage.TOPAZ,    3),             IC.filler),
    "Yesterday's Words CD":             ItemData(ItemType.CD,      (Passage.SAPPHIRE, 0),             IC.filler),
    'The Errand CD':                    ItemData(ItemType.CD,      (Passage.SAPPHIRE, 1),             IC.filler),
    'You and Your Shoes CD':            ItemData(ItemType.CD,      (Passage.SAPPHIRE, 2),             IC.filler),
    'Mr. Ether & Planaria CD':          ItemData(ItemType.CD,      (Passage.SAPPHIRE, 3),             IC.filler),
    'Progressive Ground Pound':         ItemData(ItemType.ABILITY, 0x40,                              IC.progression),
    'Swim':                             ItemData(ItemType.ABILITY, 0x41,                              IC.progression),
    'Head Smash':                       ItemData(ItemType.ABILITY, 0x42,                              IC.progression),
    'Progressive Grab':                 ItemData(ItemType.ABILITY, 0x43,                              IC.progression),
    'Dash Attack':                      ItemData(ItemType.ABILITY, 0x44,                              IC.progression),
    'Enemy Jump':                       ItemData(ItemType.ABILITY, 0x45,                              IC.progression),
    'Full Health Item':                 ItemData(ItemType.ITEM,    0x80,                              IC.useful),
    'Wario Form Trap':                  ItemData(ItemType.ITEM,    0x81,                              IC.trap),
    'Heart':                            ItemData(ItemType.ITEM,    0x82,                              IC.filler),
    'Lightning Trap':                   ItemData(ItemType.ITEM,    0x83,                              IC.trap),
    'Minigame Coin':                    ItemData(ItemType.ITEM,    0x84,                              IC.filler),
    'Entry Passage Clear':              ItemData(ItemType.EVENT,   None,                              IC.filler),
    'Emerald Passage Clear':            ItemData(ItemType.EVENT,   None,                              IC.progression),
    'Ruby Passage Clear':               ItemData(ItemType.EVENT,   None,                              IC.progression),
    'Topaz Passage Clear':              ItemData(ItemType.EVENT,   None,                              IC.progression),
    'Sapphire Passage Clear':           ItemData(ItemType.EVENT,   None,                              IC.progression),
    'Escape the Pyramid':               ItemData(ItemType.EVENT,   None,                              IC.progression),
}


def filter_items(*, type: ItemType = None, passage: Passage = None) -> Iterable[Tuple[str, ItemData]]:
    items = item_table.items()
    if type != None:
        items = filter(lambda i: i[1].type == type, items)
    if passage != None:
        items = filter(lambda i: i[1].passage() == passage, items)
    return items


def filter_item_names(*, type: ItemType = None, passage: Passage = None) -> Iterable[str]:
    return map(lambda entry: entry[0], filter_items(type=type, passage=passage))
