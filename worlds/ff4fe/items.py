import pkgutil

from BaseClasses import Item, ItemClassification
from .FreeEnterpriseForAP.FreeEnt import csvdb

class FF4FEItem(Item):
    game = 'Final Fantasy IV Free Enterprise'

class ItemData:
    name: str
    classification: ItemClassification
    tier: int
    fe_id: int

    def __init__(self, name: str, classification: ItemClassification, tier: int, fe_id: int, price: int = 0):
        self.name = name
        self.classification = classification
        self.tier = tier
        self.fe_id = fe_id
        self.price = price

    def to_json(self):
        return {
            "name": self.name,
            "fe_id": self.fe_id
        }

    @classmethod
    def create_ap_item(cls):
        return ItemData("Archipelago Item", ItemClassification.filler, 100, 0x500)


all_items: list[ItemData] = []
filler_items: list[ItemData] = []
useful_items: list[ItemData] = []

itemscsv = csvdb.CsvDb(pkgutil.get_data(__name__, "FreeEnterpriseForAP/FreeEnt/assets/db/items.csvdb").decode().splitlines())

for item in itemscsv.create_view():
    item_tier = int(item.tier) if item.tier.isdecimal() else -1
    item_classification = ItemClassification.filler
    if item.spoilername == "" or item.spoilername == "Medusa Sword":
        continue
    if item.subtype == "key" or item.spoilername == "Legend Sword":
        item_classification = ItemClassification.progression if item.spoilername != "DkMatter" \
            else ItemClassification.progression_skip_balancing
    elif item.spoilername == "Spoon" or ((int(item.tier) > 4) if item.tier.isdecimal() else False):
        item_classification = ItemClassification.useful
    item_price = int(item.price, 10) if item.price != '' else 0
    new_item = ItemData(item.spoilername, item_classification, item_tier, int(item.code, 16), item_price)
    all_items.append(new_item)


useful_items = [item for item in all_items if item.classification == ItemClassification.useful and item.name != "Spoon"]
filler_items = [item for item in all_items if item.classification == ItemClassification.filler and item.name != "Spoon"]
# 0x46,#item.fe_CustomWeapon,,,,,,D,,,,,yes,,yes,
all_items.append(ItemData("Advance Weapon", ItemClassification.useful, 8, 0x46, 100000))

useful_item_names = [item.name for item in [*useful_items]]
filler_item_names = [item.name for item in [*filler_items]]
sellable_item_names = [item for item in [*useful_item_names, *filler_item_names]]

character_data = [
    ("Cecil", 0x01),
    ("Kain", 0x02),
    ("Rydia", 0x03),
    ("Tellah", 0x04),
    ("Edward", 0x05),
    ("Rosa", 0x06),
    ("Yang", 0x07),
    ("Palom", 0x08),
    ("Porom", 0x09),
    ("Cid", 0x0E),
    ("Edge", 0x12),
    ("Fusoya", 0x13),
    ("None", 0xFF)
]

characters = [
    "Cecil",
    "Kain",
    "Rydia",
    "Tellah",
    "Edward",
    "Rosa",
    "Yang",
    "Palom",
    "Porom",
    "Cid",
    "Edge",
    "Fusoya",
    "None",
]

for character in character_data:
    new_item = ItemData(character[0], ItemClassification.progression, -1, character[1] + 0x300)
    all_items.append(new_item)

key_items = [item for item in all_items if
             (item.classification == ItemClassification.progression or item.name == "Spoon")
             and item.name not in characters]

key_item_names = [item.name for item in all_items if
                  (item.classification == ItemClassification.progression or item.name == "Spoon")
                  and item.name not in characters]

key_items_tracker_order = [
    "Package",
    "SandRuby",
    "Legend Sword",
    "Baron Key",
    "TwinHarp",
    "Earth Crystal",
    "Magma Key",
    "Tower Key",
    "Hook",
    "Luca Key",
    "Darkness Crystal",
    "Rat Tail",
    "Adamant",
    "Pan",
    "Spoon",
    "Pink Tail",
    "Crystal"
]

key_items_tracker_ids = {k: i for i, k in enumerate(key_items_tracker_order)}

item_name_groups = {
    "characters": [*characters],
    "key_items": [*key_items_tracker_order],
    "non_key_items": [*sellable_item_names],
    "filler_items": [*filler_item_names],
    "useful_items": [*useful_item_names]
}


for i in range(32):
    all_items.append(ItemData(f"Objective {i + 1} Cleared", ItemClassification.progression, 8, 0))