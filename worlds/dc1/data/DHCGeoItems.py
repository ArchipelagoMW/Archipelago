from typing import List

from BaseClasses import ItemClassification
from worlds.dc1.Items import DarkCloudItem
from worlds.dc1.Options import DarkCloudOptions

ids = {
    "Progressive Crowning Day": 971110600,
    "Progressive Ceremony": 971110601,
    "Progressive Reunion": 971110602,
    "Progressive Campaign": 971110603,
    "Progressive Menace": 971110604,
    "Progressive The Deal": 971110605,
    "Progressive Dark Power": 971110606,
    "Progressive Assassin": 971110607,
    "Progressive Protected": 971110608,
    "Progressive Demon": 971110609,
    "Progressive Things Lost": 971110610,
    "Progressive Departure": 971110611,
  }

cday_ids = ["Progressive Crowning Day", "Progressive Crowning Day",
            "Progressive Crowning Day", "Progressive Crowning Day"]
ceremony_ids = ["Progressive Ceremony", "Progressive Ceremony", "Progressive Ceremony",
                "Progressive Ceremony", "Progressive Ceremony", "Progressive Ceremony"]
reunion_ids = ["Progressive Reunion", "Progressive Reunion", "Progressive Reunion",
               "Progressive Reunion", "Progressive Reunion"]
campaign_ids = ["Progressive Campaign", "Progressive Campaign", "Progressive Campaign",
                "Progressive Campaign", "Progressive Campaign", "Progressive Campaign",]
menace_ids = ["Progressive Menace", "Progressive Menace", "Progressive Menace",
              "Progressive Menace", "Progressive Menace", "Progressive Menace",]
deal_ids = ["Progressive The Deal", "Progressive The Deal", "Progressive The Deal",
            "Progressive The Deal", "Progressive The Deal"]
power_ids = ["Progressive Dark Power", "Progressive Dark Power", "Progressive Dark Power",
             "Progressive Dark Power", "Progressive Dark Power", "Progressive Dark Power"]
assassin_ids = ["Progressive Assassin", "Progressive Assassin", "Progressive Assassin", "Progressive Assassin",
                "Progressive Assassin", "Progressive Assassin", "Progressive Assassin"]
prot_ids = ["Progressive Protected", "Progressive Protected", "Progressive Protected", "Progressive Protected"]
demon_ids = ["Progressive Demon", "Progressive Demon", "Progressive Demon", "Progressive Demon"]
things_ids = ["Progressive Things Lost", "Progressive Things Lost",
              "Progressive Things Lost", "Progressive Things Lost"]
departure_ids = ["Progressive Departure", "Progressive Departure", "Progressive Departure",
                 "Progressive Departure", "Progressive Departure"]

def create_castle_atla(options: DarkCloudOptions, player: int) -> List["DarkCloudItem"]:
    """Create atla items for Dark Heaven Castle."""
    items = []
    required = (cday_ids + ceremony_ids + reunion_ids + campaign_ids + menace_ids + deal_ids + power_ids +
                assassin_ids + prot_ids + demon_ids + things_ids + departure_ids)

    # All castle atla are required for the genie fight
    for i in required:
        items.append(DarkCloudItem(i, ItemClassification.progression, ids[i], player))

    return items
