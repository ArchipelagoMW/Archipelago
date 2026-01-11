from BaseClasses import Item
from BaseClasses import ItemClassification as IC
from typing import NamedTuple, Optional


class SSItemData(NamedTuple):
    """
    Data for an item in SS.
    """

    type: str
    classification: IC
    code: Optional[int]
    quantity: int
    item_id: Optional[int]


class SSItem(Item):
    """
    Class represents a Skyward Sword item.
    """

    game: str = "Skyward Sword"
    type: Optional[str]

    def __init__(
        self,
        name: str,
        player: int,
        data: SSItemData,
        classification: Optional[IC] = None,
    ) -> None:
        super().__init__(
            name,
            data.classification if classification is None else classification,
            None if data.code is None else SSItem.get_apid(data.code),
            player,
        )

        self.type = data.type
        self.item_id = data.item_id

    @staticmethod
    def get_apid(code: int) -> int:
        """
        Compute the Archipelago ID for the given item index.

        :param code: The index of the item.
        :return: The computed Archipelago ID.
        """
        base_id: int = 99000
        return base_id + code


ITEM_TABLE: dict[str, SSItemData] = {
    "Small Key":            SSItemData("Item",         IC.progression,         1,      0,  0x01), # unused
    "Green Rupee":          SSItemData("Consumable",   IC.filler,              2,      4,  0x02),
    "Blue Rupee":           SSItemData("Consumable",   IC.filler,              3,      12, 0x03),
    "Red Rupee":            SSItemData("Consumable",   IC.filler,              4,      44, 0x04),
    "Heart":                SSItemData("Item",         IC.filler,              6,      0,  0x06), # not in item pool
    "Progressive Sword":    SSItemData("Item",         IC.progression,         10,     6,  0x0A),
    "Sailcloth":            SSItemData("Item",         IC.progression,         15,     0,  0x0F), # not in item pool
    "Goddess's Harp":       SSItemData("Item",         IC.progression,         16,     1,  0x10),
    "Progressive Bow":      SSItemData("Item",         IC.progression,         19,     3,  0x13),
    "Clawshots":            SSItemData("Item",         IC.progression,         20,     1,  0x14),
    "Spiral Charge":        SSItemData("Item",         IC.progression,         21,     1,  0x15),

    "Ancient Cistern Boss Key":         SSItemData("Boss Key",     IC.progression_skip_balancing,         25,  1,  0x19),
    "Fire Sanctuary Boss Key":          SSItemData("Boss Key",     IC.progression_skip_balancing,         26,  1,  0x1A),
    "Sandship Boss Key":                SSItemData("Boss Key",     IC.progression_skip_balancing,         27,  1,  0x1B),
    "Key Piece":                        SSItemData("Item",         IC.progression,                        28,  5,  0x1C),
    "Skyview Boss Key":                 SSItemData("Boss Key",     IC.progression_skip_balancing,         29,  1,  0x1D),
    "Earth Temple Boss Key":            SSItemData("Boss Key",     IC.progression_skip_balancing,         30,  1,  0x1E),
    "Lanayru Mining Facility Boss Key": SSItemData("Boss Key",     IC.progression_skip_balancing,         31,  1,  0x1F),

    "Silver Rupee":         SSItemData("Consumable",   IC.filler,              32,     24, 0x20),
    "Gold Rupee":           SSItemData("Consumable",   IC.filler,              33,     11, 0x21),
    "Rupoor":               SSItemData("Consumable",   IC.trap,                34,     0,  0x22),

    "Gratitude Crystal Pack":       SSItemData("Item",         IC.progression,         35,     13, 0x23),
    "5 Bombs":                      SSItemData("Item",         IC.filler,              40,     1,  0x28),
    "10 Bombs":                     SSItemData("Item",         IC.filler,              41,     0,  0x29), # Rupin
    "Gratitude Crystal":            SSItemData("Item",         IC.progression,         48,     15, 0x30), # Locked
    "Gust Bellows":                 SSItemData("Item",         IC.progression,         49,     1,  0x31),
    "Map":                          SSItemData("Item",         IC.filler,              50,     0,  0x32), # unused
    "Progressive Slingshot":        SSItemData("Item",         IC.progression,         52,     2,  0x34),
    "Progressive Beetle":           SSItemData("Item",         IC.progression,         53,     4,  0x35),
    "Progressive Mitts":            SSItemData("Item",         IC.progression,         56,     2,  0x38),
    "10 Deku Seeds":                SSItemData("Item",         IC.filler,              60,     0,  0x3C), # Rupin
    "Semi Rare Treasure":           SSItemData("Consumable",   IC.filler,              63,     10, 0x3F),
    "Rare Treasure":                SSItemData("Consumable",   IC.filler,              64,     4,  0x40),
    "Water Dragon's Scale":         SSItemData("Item",         IC.progression,         68,     1,  0x44),
    "Bug Medal":                    SSItemData("Item",         IC.filler,              70,     1,  0x46),
    "Progressive Bug Net":          SSItemData("Item",         IC.progression,         71,     2,  0x47),

    "Bomb Bag":                     SSItemData("Item",         IC.progression,         92,     1,  0x5C),
    "Heart Container":              SSItemData("Item",         IC.filler,              93,     6,  0x5D),
    "Heart Piece":                  SSItemData("Item",         IC.filler,              94,     24, 0x5E),

    "Triforce of Courage":          SSItemData("Item",         IC.progression_skip_balancing,         95,     1,  0x5F),
    "Triforce of Power":            SSItemData("Item",         IC.progression_skip_balancing,         96,     1,  0x60),
    "Triforce of Wisdom":           SSItemData("Item",         IC.progression_skip_balancing,         97,     1,  0x61),

    "Sea Chart":                    SSItemData("Item",         IC.progression,         98,     1,  0x62),

    "Heart Medal":                  SSItemData("Item",         IC.filler,              100,    2,  0x64),
    "Rupee Medal":                  SSItemData("Item",         IC.filler,              101,    2,  0x65),
    "Treasure Medal":               SSItemData("Item",         IC.filler,              102,    1,  0x66),
    "Potion Medal":                 SSItemData("Item",         IC.filler,              103,    1,  0x67),
    "Cursed Medal":                 SSItemData("Item",         IC.trap,                104,    1,  0x68),
    "Progressive Wallet":           SSItemData("Item",         IC.progression,         108,    4,  0x6C),
    "Progressive Pouch":            SSItemData("Item",         IC.progression,         112,    5,  0x70),
    "Life Medal":                   SSItemData("Item",         IC.filler,              114,    2,  0x72),
    "Wooden Shield":                SSItemData("Item",         IC.filler,              116,    1,  0x74),
    "Hylian Shield":                SSItemData("Item",         IC.useful,              125,    1,  0x7D),
    "Revitalizing Potion":          SSItemData("Item",         IC.filler,              126,    0,  0x7E), # not in pool
    "Small Seed Satchel":           SSItemData("Item",         IC.filler,              128,    1,  0x80),
    "Small Quiver":                 SSItemData("Item",         IC.filler,              131,    1,  0x83),
    "Small Bomb Bag":               SSItemData("Item",         IC.filler,              134,    1,  0x86),

    "Whip":                         SSItemData("Item",         IC.progression,         137,    1,  0x89),
    "Fireshield Earrings":          SSItemData("Item",         IC.progression,         138,    1,  0x8A),
    "Empty Bottle":                 SSItemData("Item",         IC.progression,         153,    5,  0x99),
    "Cawlin's Letter":              SSItemData("Item",         IC.progression,         158,    1,  0x9E),
    "Horned Colossus Beetle":       SSItemData("Item",         IC.progression,         159,    1,  0x9F),
    "Baby Rattle":                  SSItemData("Item",         IC.progression,         160,    1,  0xA0),

    "Tumbleweed":                   SSItemData("Item",         IC.filler,              163,    1,  0xA3),
    "Eldin Ore":                    SSItemData("Item",         IC.filler,              165,    2,  0xA5),
    "Dusk Relic":                   SSItemData("Item",         IC.filler,              168,    41, 0xA8),
    "Monster Horn":                 SSItemData("Item",         IC.filler,              171,    0,  0xAB),
    "Evil Crystal":                 SSItemData("Item",         IC.filler,              173,    2,  0xAD),
    "Golden Skull":                 SSItemData("Item",         IC.filler,              175,    9,  0xAF),
    "Goddess Plume":                SSItemData("Item",         IC.filler,              176,    1,  0xB0),

    "Emerald Tablet":               SSItemData("Item",         IC.progression,         177,    1,  0xB1),
    "Ruby Tablet":                  SSItemData("Item",         IC.progression,         178,    1,  0xB2),
    "Amber Tablet":                 SSItemData("Item",         IC.progression,         179,    1,  0xB3),
    "Stone of Trials":              SSItemData("Item",         IC.progression,         180,    1,  0xB4),
    "Ballad of the Goddess":        SSItemData("Item",         IC.progression,         186,    1,  0xBA),
    "Farore's Courage":             SSItemData("Item",         IC.progression,         187,    1,  0xBB),
    "Nayru's Wisdom":               SSItemData("Item",         IC.progression,         188,    1,  0xBC),
    "Din's Power":                  SSItemData("Item",         IC.progression,         189,    1,  0xBD),

    "Faron Song of the Hero Part":      SSItemData("Item",         IC.progression,         190,    1,  0xBE),
    "Eldin Song of the Hero Part":      SSItemData("Item",         IC.progression,         191,    1,  0xBF),
    "Lanayru Song of the Hero Part":    SSItemData("Item",         IC.progression,         192,    1,  0xC0),

    "Life Tree Seedling":           SSItemData("Item",         IC.progression,         197,    0,  0xC5),
    "Life Tree Fruit":              SSItemData("Item",         IC.progression,         198,    1,  0xC6),
    "Extra Wallet":                 SSItemData("Item",         IC.progression,         199,    3,  0xC7),

    #Rando custom items
    "Skyview Small Key":                    SSItemData("Small Key",    IC.progression,         200,    2,  0xC8),
    "Lanayru Mining Facility Small Key":    SSItemData("Small Key",    IC.progression,         201,    1,  0xC9),
    "Ancient Cistern Small Key":            SSItemData("Small Key",    IC.progression,         202,    2,  0xCA),
    "Fire Sanctuary Small Key":             SSItemData("Small Key",    IC.progression,         203,    3,  0xCB),
    "Sandship Small Key":                   SSItemData("Small Key",    IC.progression,         204,    2,  0xCC),
    "Sky Keep Small Key":                   SSItemData("Small Key",    IC.progression,         205,    1,  0xCD),
    "Lanayru Caves Small Key":              SSItemData("Small Key",    IC.progression,         206,    1,  0xCE),

    "Skyview Map":                          SSItemData("Map",          IC.useful,              207,    1,  0xCF),
    "Earth Temple Map":                     SSItemData("Map",          IC.useful,              208,    1,  0xD0),
    "Lanayru Mining Facility Map":          SSItemData("Map",          IC.useful,              209,    1,  0xD1),
    "Ancient Cistern Map":                  SSItemData("Map",          IC.useful,              210,    1,  0xD2),
    "Fire Sanctuary Map":                   SSItemData("Map",          IC.useful,              211,    1,  0xD3),
    "Sandship Map":                         SSItemData("Map",          IC.useful,              212,    1,  0xD4),
    "Sky Keep Map":                         SSItemData("Map",          IC.useful,              213,    1,  0xD5),

    "Group of Tadtones":                    SSItemData("Item",         IC.progression,         214,    17, 0xD6),
    "Scrapper":                             SSItemData("Item",         IC.progression,         215,    1,  0xD7),

    # AP Victory item
    "Victory":                              SSItemData("Event",        IC.progression,         None,   1,  None),
}

CONSUMABLE_ITEMS: dict[str, int] = {
    "Green Rupee": 4,
    "Blue Rupee": 12,
    "Red Rupee": 44,
    "Silver Rupee": 24,
    "Gold Rupee": 11,
    "Semi Rare Treasure": 10,
    "Rare Treasure": 4,
}

LOOKUP_ID_TO_NAME: dict[int, str] = {
    SSItem.get_apid(data.code): item for item, data in ITEM_TABLE.items() if data.code is not None
}
