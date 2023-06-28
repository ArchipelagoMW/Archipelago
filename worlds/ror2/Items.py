from BaseClasses import Item, ItemClassification
from .Options import ItemWeights
from .RoR2Environments import *
from typing import NamedTuple, Optional


class RiskOfRainItem(Item):
    game: str = "Risk of Rain 2"


class RiskOfRainItemData(NamedTuple):
    category: str
    code: Optional[int] = None
    item_type: ItemClassification = ItemClassification.filler


offset: int = 37000
# 37000 - 37499, 38000
item_table: Dict[str, RiskOfRainItemData] = {
    "Dio's Best Friend":    RiskOfRainItemData("Upgrade", 1 + offset, ItemClassification.filler),
    "Common Item":          RiskOfRainItemData("Upgrade", 2 + offset, ItemClassification.filler),
    "Uncommon Item":        RiskOfRainItemData("Upgrade", 3 + offset, ItemClassification.filler),
    "Legendary Item":       RiskOfRainItemData("Upgrade", 4 + offset, ItemClassification.useful),
    "Boss Item":            RiskOfRainItemData("Upgrade", 5 + offset, ItemClassification.useful),
    "Lunar Item":           RiskOfRainItemData("Upgrade", 6 + offset, ItemClassification.trap),
    "Equipment":            RiskOfRainItemData("Upgrade", 7 + offset, ItemClassification.filler),
    "Item Scrap, White":    RiskOfRainItemData("Upgrade", 8 + offset, ItemClassification.filler),
    "Item Scrap, Green":    RiskOfRainItemData("Upgrade", 9 + offset, ItemClassification.filler),
    "Item Scrap, Red":      RiskOfRainItemData("Upgrade", 10 + offset, ItemClassification.filler),
    "Item Scrap, Yellow":   RiskOfRainItemData("Upgrade", 11 + offset, ItemClassification.filler),
    "Void Item":            RiskOfRainItemData("Upgrade", 12 + offset, ItemClassification.filler),
    "Beads of Fealty":      RiskOfRainItemData("Beads", 13 + offset, ItemClassification.progression)
}

# 37700 - 37699
##################################################
# environments


# add ALL environments into the item table
def create_environment_table(name: str, environment_id: int, environment_classification: ItemClassification) \
        -> Dict[str, RiskOfRainItemData]:
    return {name: RiskOfRainItemData("Stage", 700 + offset + environment_id, environment_classification)}


environment_table: Dict[str, RiskOfRainItemData] = {}
# use the sotv dlc in the item table so that all names can be looked up regardless of use
for data, key in environment_ALL_table.items():
    classification = ItemClassification.progression
    if data in {"Hidden Realm: Bulwark's Ambry", "Hidden Realm: Gilded Coast,"}:
        classification = ItemClassification.useful

    environment_table.update(create_environment_table(data, key, classification))

item_table.update(environment_table)

# end of environments
##################################################

default_weights: Dict[str, int] = {
    "Item Scrap, Green":    16,
    "Item Scrap, Red":      4,
    "Item Scrap, Yellow":   1,
    "Item Scrap, White":    32,
    "Common Item":          64,
    "Uncommon Item":        32,
    "Legendary Item":       8,
    "Boss Item":            4,
    "Lunar Item":           16,
    "Void Item":            16,
    "Equipment":            32
}

new_weights: Dict[str, int] = {
    "Item Scrap, Green":    15,
    "Item Scrap, Red":      5,
    "Item Scrap, Yellow":   1,
    "Item Scrap, White":    30,
    "Common Item":          75,
    "Uncommon Item":        40,
    "Legendary Item":       10,
    "Boss Item":            5,
    "Lunar Item":           10,
    "Void Item":            16,
    "Equipment":            20
}

uncommon_weights: Dict[str, int] = {
    "Item Scrap, Green":    45,
    "Item Scrap, Red":      5,
    "Item Scrap, Yellow":   1,
    "Item Scrap, White":    30,
    "Common Item":          45,
    "Uncommon Item":        100,
    "Legendary Item":       10,
    "Boss Item":            5,
    "Lunar Item":           15,
    "Void Item":            16,
    "Equipment":            20
}

legendary_weights: Dict[str, int] = {
    "Item Scrap, Green":    15,
    "Item Scrap, Red":      5,
    "Item Scrap, Yellow":   1,
    "Item Scrap, White":    30,
    "Common Item":          50,
    "Uncommon Item":        25,
    "Legendary Item":       100,
    "Boss Item":            5,
    "Lunar Item":           15,
    "Void Item":            16,
    "Equipment":            20
}

lunartic_weights: Dict[str, int] = {
    "Item Scrap, Green":    0,
    "Item Scrap, Red":      0,
    "Item Scrap, Yellow":   0,
    "Item Scrap, White":    0,
    "Common Item":          0,
    "Uncommon Item":        0,
    "Legendary Item":       0,
    "Boss Item":            0,
    "Lunar Item":           100,
    "Void Item":            0,
    "Equipment":            0
}

chaos_weights: Dict[str, int] = {
    "Item Scrap, Green":    80,
    "Item Scrap, Red":      45,
    "Item Scrap, Yellow":   30,
    "Item Scrap, White":    100,
    "Common Item":          100,
    "Uncommon Item":        70,
    "Legendary Item":       30,
    "Boss Item":            20,
    "Lunar Item":           60,
    "Void Item":            60,
    "Equipment":            40
}

no_scraps_weights: Dict[str, int] = {
    "Item Scrap, Green":    0,
    "Item Scrap, Red":      0,
    "Item Scrap, Yellow":   0,
    "Item Scrap, White":    0,
    "Common Item":          100,
    "Uncommon Item":        40,
    "Legendary Item":       15,
    "Boss Item":            5,
    "Lunar Item":           10,
    "Void Item":            16,
    "Equipment":            25
}

even_weights: Dict[str, int] = {
    "Item Scrap, Green":    1,
    "Item Scrap, Red":      1,
    "Item Scrap, Yellow":   1,
    "Item Scrap, White":    1,
    "Common Item":          1,
    "Uncommon Item":        1,
    "Legendary Item":       1,
    "Boss Item":            1,
    "Lunar Item":           1,
    "Void Item":            1,
    "Equipment":            1
}

scraps_only: Dict[str, int] = {
    "Item Scrap, Green":    70,
    "Item Scrap, White":    100,
    "Item Scrap, Red":      30,
    "Item Scrap, Yellow":   5,
    "Common Item":          0,
    "Uncommon Item":        0,
    "Legendary Item":       0,
    "Boss Item":            0,
    "Lunar Item":           0,
    "Void Item":            0,
    "Equipment":            0
}

void_weights: Dict[str, int] = {
    "Item Scrap, Green":    0,
    "Item Scrap, Red":      0,
    "Item Scrap, Yellow":   0,
    "Item Scrap, White":    0,
    "Common Item":          0,
    "Uncommon Item":        0,
    "Legendary Item":       0,
    "Boss Item":            0,
    "Lunar Item":           0,
    "Void Item":            100,
    "Equipment":            0
}

item_pool_weights: Dict[int, Dict[str, int]] = {
    ItemWeights.option_default:     default_weights,
    ItemWeights.option_new:         new_weights,
    ItemWeights.option_uncommon:    uncommon_weights,
    ItemWeights.option_legendary:   legendary_weights,
    ItemWeights.option_lunartic:    lunartic_weights,
    ItemWeights.option_chaos:       chaos_weights,
    ItemWeights.option_no_scraps:   no_scraps_weights,
    ItemWeights.option_even:        even_weights,
    ItemWeights.option_scraps_only: scraps_only,
    ItemWeights.option_void:        void_weights,
}

lookup_id_to_name: Dict[int, str] = {id: name for name, id in item_table.items()}
