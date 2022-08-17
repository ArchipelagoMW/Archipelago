from typing import Dict, Tuple, NamedTuple


class ItemData(NamedTuple):
    code: int
    count: int = 1
    progression: bool = False
    useful: bool = False


item_table: Dict[str, ItemData] = {
    # "White jewel": ItemData(0xC64001, 0),
    "Red jewel(S)": ItemData(0xC64002),
    "Red jewel(L)": ItemData(0xC64003),
    "Special1": ItemData(0xC64004, progression=True),
    # "Special2": ItemData(0xC64005, progression=True),
    # "Roast chicken": ItemData(0xC64006, 0),  # 35
    "Roast beef": ItemData(0xC64007, 4),  # 31
    # "Healing kit": ItemData(0xC64008, 0),  # 4
    # "Purifying": ItemData(0xC64009, 0),  # 21
    # "Cure ampoule": ItemData(0xC6400A, 0),  # 12
    # "pot-pourri": ItemData(0xC6400B, 0),
    "PowerUp": ItemData(0xC6400C),  # 12
    # "Holy water": ItemData(0xC6400D, 10),
    # "Cross": ItemData(0xC6400E, 9),
    # "Axe": ItemData(0xC6400F, 8),
    # "Knife": ItemData(0xC64010, 8),
    # "Wooden stake": ItemData(0xC64011, 0),
    # "Rose": ItemData(0xC64012, 0),
    # "The contract": ItemData(0xC64013, 0),
    # "engagement ring": ItemData(0xC64014, 0),
    # "Magical Nitro": ItemData(0xC64015, 2, progression=True),
    # "Mandragora": ItemData(0xC64016, 2, progression=True),
    "Sun card": ItemData(0xC64017, 3),  # 10
    "Moon card": ItemData(0xC64018, 3),  # 9
    # "Incandescent gaze": ItemData(0xC64019, 0),
    "500 GOLD": ItemData(0xC6401A),  # 50
    "300 GOLD": ItemData(0xC6401B),  # 5
    "100 GOLD": ItemData(0xC6401C),  # 7
    # "Archives key": ItemData(0xC6401D, progression=True),
    "Left Tower Key": ItemData(0xC6401E, progression=True),
    # "Storeroom Key": ItemData(0xC6401F, progression=True),
    # "Garden Key": ItemData(0xC64020, progression=True),
    # "Copper Key": ItemData(0xC64021, progression=True),
    # "Chamber Key": ItemData(0xC64022, progression=True),
    # "Execution Key": ItemData(0xC64023, progression=True),
    # "Science Key1": ItemData(0xC64024, progression=True),
    # "Science Key2": ItemData(0xC64025, progression=True),
    # "Science Key3": ItemData(0xC64026, progression=True),
    # "Clocktower Key1": ItemData(0xC64027, progression=True),
    # "Clocktower Key2": ItemData(0xC64028, progression=True),
    # "Clocktower Key3": ItemData(0xC64029, progression=True)
    # pot-pourri, Wooden stake, Rose, engagement ring, and Incandescent gaze are all unused items.
    # They're included because I plan to overwrite them with custom items later, in which case they'll be renamed.
    # White jewel and The contract are included in the event I decide to shuffle them locally later.
}


filler_items: Tuple[str, ...] = (
    'Red jewel(S)',
    'Red jewel(L)',
    '500 GOLD',
    '300 GOLD',
    '100 GOLD'
)
