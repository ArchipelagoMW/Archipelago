from BaseClasses import ItemClassification
from typing import List, Optional


class ItemDef:
    def __init__(self,
                 id: Optional[int],
                 name: str,
                 classification: ItemClassification,
                 count: int,
                 progression_count: int,
                 prefill_location: Optional[str]):
        self.id = id
        self.name = name
        self.classification = classification
        self.count = count
        self.progression_count = progression_count
        self.prefill_location = prefill_location


items: List[ItemDef] = [
    ItemDef(400000, 'Progressive Sword', ItemClassification.progression, 4, 0, None),
    ItemDef(400001, 'Progressive Armor', ItemClassification.progression, 3, 0, None),
    ItemDef(400002, 'Progressive Shield', ItemClassification.useful, 4, 0, None),
    ItemDef(400003, 'Spring Elixir', ItemClassification.progression, 1, 0, None),
    ItemDef(400004, 'Mattock', ItemClassification.progression, 1, 0, None),
    ItemDef(400005, 'Unlock Wingboots', ItemClassification.progression, 1, 0, None),
    ItemDef(400006, 'Key Jack', ItemClassification.progression, 1, 0, None),
    ItemDef(400007, 'Key Queen', ItemClassification.progression, 1, 0, None),
    ItemDef(400008, 'Key King', ItemClassification.progression, 1, 0, None),
    ItemDef(400009, 'Key Joker', ItemClassification.progression, 1, 0, None),
    ItemDef(400010, 'Key Ace', ItemClassification.progression, 1, 0, None),
    ItemDef(400011, 'Ring of Ruby', ItemClassification.progression, 1, 0, None),
    ItemDef(400012, 'Ring of Dworf', ItemClassification.progression, 1, 0, None),
    ItemDef(400013, 'Demons Ring', ItemClassification.progression, 1, 0, None),
    ItemDef(400014, 'Black Onyx', ItemClassification.progression, 1, 0, None),
    ItemDef(None, 'Sky Spring Flow', ItemClassification.progression, 1, 0, 'Sky Spring'),
    ItemDef(None, 'Tower of Fortress Spring Flow', ItemClassification.progression, 1, 0, 'Tower of Fortress Spring'),
    ItemDef(None, 'Joker Spring Flow', ItemClassification.progression, 1, 0, 'Joker Spring'),
    ItemDef(400015, 'Deluge', ItemClassification.progression, 1, 0, None),
    ItemDef(400016, 'Thunder', ItemClassification.useful, 1, 0, None),
    ItemDef(400017, 'Fire', ItemClassification.useful, 1, 0, None),
    ItemDef(400018, 'Death', ItemClassification.useful, 1, 0, None),
    ItemDef(400019, 'Tilte', ItemClassification.useful, 1, 0, None),
    ItemDef(400020, 'Ring of Elf', ItemClassification.useful, 1, 0, None),
    ItemDef(400021, 'Magical Rod', ItemClassification.useful, 1, 0, None),
    ItemDef(400022, 'Pendant', ItemClassification.useful, 1, 0, None),
    ItemDef(400023, 'Hourglass', ItemClassification.filler, 6, 0, None),
    # We need at least 4 red potions for the Tower of Red Potion. Up to the player to save them up!
    ItemDef(400024, 'Red Potion', ItemClassification.filler, 15, 4, None),
    ItemDef(400025, 'Elixir', ItemClassification.filler, 4, 0, None),
    ItemDef(400026, 'Glove', ItemClassification.filler, 5, 0, None),
    ItemDef(400027, 'Ointment', ItemClassification.filler, 8, 0, None),
    ItemDef(400028, 'Poison', ItemClassification.trap, 13, 0, None),
    ItemDef(None, 'Killed Evil One', ItemClassification.progression, 1, 0, 'Evil One'),
    # Placeholder item so the game knows which shop slot to prefill wingboots
    ItemDef(400029, 'Wingboots', ItemClassification.useful, 0, 0, None),
]
