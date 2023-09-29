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
    weight: Optional[int] = None


def get_items_by_category(category: str) -> Dict[str, RiskOfRainItemData]:
    item_dict: Dict[str, RiskOfRainItemData] = {}
    for name, data in item_table.items():
        if data.category == category:
            item_dict.setdefault(name, data)

    return item_dict


offset: int = 37000
filler_offset: int = offset + 300
trap_offset: int = offset + 400
# 37000 - 37499, 38000
upgrade_table: Dict[str, RiskOfRainItemData] = {
    "Common Item":          RiskOfRainItemData("Upgrade", 2 + offset, ItemClassification.filler, 64),
    "Uncommon Item":        RiskOfRainItemData("Upgrade", 3 + offset, ItemClassification.filler, 32),
    "Legendary Item":       RiskOfRainItemData("Upgrade", 4 + offset, ItemClassification.useful, 8),
    "Boss Item":            RiskOfRainItemData("Upgrade", 5 + offset, ItemClassification.useful, 4),
    "Equipment":            RiskOfRainItemData("Upgrade", 7 + offset, ItemClassification.filler, 32),
    "Item Scrap, White":    RiskOfRainItemData("Upgrade", 8 + offset, ItemClassification.filler, 32),
    "Item Scrap, Green":    RiskOfRainItemData("Upgrade", 9 + offset, ItemClassification.filler, 16),
    "Item Scrap, Red":      RiskOfRainItemData("Upgrade", 10 + offset, ItemClassification.filler, 4),
    "Item Scrap, Yellow":   RiskOfRainItemData("Upgrade", 11 + offset, ItemClassification.filler, 1),
    "Void Item":            RiskOfRainItemData("Upgrade", 12 + offset, ItemClassification.filler, 16),
}
other_table: Dict[str, RiskOfRainItemData] = {
    "Dio's Best Friend":    RiskOfRainItemData("ExtraLife", 1 + offset, ItemClassification.filler),
    "Beads of Fealty":      RiskOfRainItemData("Beads", 13 + offset, ItemClassification.progression),
    "Radar Scanner":        RiskOfRainItemData("Radar", 14 + offset, ItemClassification.progression)
}
filler_table: Dict[str, RiskOfRainItemData] = {
    "Money":                RiskOfRainItemData("Filler", 1 + filler_offset, ItemClassification.filler, 50),
    "Lunar Coin":           RiskOfRainItemData("Filler", 2 + filler_offset, ItemClassification.filler, 30),
    "1000 Exp":             RiskOfRainItemData("Filler", 3 + filler_offset, ItemClassification.filler, 50)
}
trap_table: Dict[str, RiskOfRainItemData] = {
    "Lunar Item": RiskOfRainItemData("Trap", 6 + offset, ItemClassification.trap, 16),
    "Mountain Trap":        RiskOfRainItemData("Trap", 1 + trap_offset, ItemClassification.trap, 20),
    "Time Warp Trap":       RiskOfRainItemData("Trap", 2 + trap_offset, ItemClassification.trap, 20),
    "Combat Trap":          RiskOfRainItemData("Trap", 3 + trap_offset, ItemClassification.trap, 40),
    "Teleport Trap":        RiskOfRainItemData("Trap", 4 + trap_offset, ItemClassification.trap, 30)
}

item_table = {**upgrade_table, **other_table, **filler_table, **trap_table}
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
    "Void Item":            16,
    "Equipment":            20
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
    "Void Item":            100,
    "Equipment":            0
}

item_pool_weights: Dict[int, Dict[str, int]] = {
    ItemWeights.option_default:     default_weights,
    ItemWeights.option_new:         new_weights,
    ItemWeights.option_uncommon:    uncommon_weights,
    ItemWeights.option_legendary:   legendary_weights,
    ItemWeights.option_chaos:       chaos_weights,
    ItemWeights.option_no_scraps:   no_scraps_weights,
    ItemWeights.option_even:        even_weights,
    ItemWeights.option_scraps_only: scraps_only,
    ItemWeights.option_void:        void_weights,
}

lookup_id_to_name: Dict[int, str] = {id: name for name, id in item_table.items()}
