from typing import Dict
from BaseClasses import Item
from .Options import ItemWeights


class RiskOfRainItem(Item):
    game: str = "Risk of Rain 2"


# 37000 - 37699, 38000
item_table: Dict[str, int] = {
    "Dio's Best Friend":    37001,
    "Common Item":          37002,
    "Uncommon Item":        37003,
    "Legendary Item":       37004,
    "Boss Item":            37005,
    "Lunar Item":           37006,
    "Equipment":            37007,
    "Item Scrap, White":    37008,
    "Item Scrap, Green":    37009,
    "Item Scrap, Red":      37010,
    "Item Scrap, Yellow":   37011
}

# 37700 - 37699
##################################################
# environments

# TODO move the environments into stages so that they can be distributed in a reasonable order
environment_vanilla_table: Dict[str, int] = {
    "Void Fields":                          37704, # arena
    "Distant Roost":                        37707, # blackbeach
    "Distant Roost (2)":                    37708, # blackbeach2
    "Abyssal Depths":                       37710, # dampcavesimple
    "Wetland Aspect":                       37712, # foggyswamp
    "Rallypoint Delta":                     37713, # frozenwall
    "Titanic Plains":                       37715, # golemplains
    "Titanic Plains (2)":                   37716, # golemplains2
    "Abandoned Aqueduct":                   37717, # goolake
    "Commencement":                         37732, # moon2
    "Sundered Grove":                       37735, # rootjungle
    "Siren's Call":                         37737, # shipgraveyard
    "Sky Meadow":                           37738, # skymeadow
    "Scorched Acres":                       37747, # wispgraveyard
}

environment_sotv_table: Dict[str, int] = {
    "Aphelian Sanctuary":                   37703, # ancientloft
    "The Simulacrum (Aphelian Sanctuary)":  37720, # itancientloft
    "The Simulacrum (Abyssal Depths)":      37721, # itdampcave
    "The Simulacrum (Rallypoint Delta)":    37722, # itfrozenwall
    "The Simulacrum (Titanic Plains)":      37723, # itgolemplains
    "The Simulacrum (Abandoned Aqueduct)":  37724, # itgoolake
    "The Simulacrum (Commencement)":        37725, # itmoon
    "The Simulacrum (Sky Meadow)":          37726, # itskymeadow
    "Siphoned Forest":                      37739, # snowyforest
    "Sulfur Pools":                         37741, # sulfurpools
    "Void Locus":                           37745, # voidstage
    "The Planetarium":                      37746, # voidraid
}

environment_hidden_realm_table: Dict[str, int] = {
    "Hidden Realm: Bulwark's Ambry":        37705, # artifactworld
    "Hidden Realm: Bazaar Between Time":    37706, # bazaar
    "Hidden Realm: Gilded Coast":           37714, # goldshores
    "Hidden Realm: A Moment, Whole":        37727, # limbo
    "Hidden Realm: A Moment, Fractured":    37733, # mysteryspace
}

def get_environment_table(dlc_sotv:bool=False) -> Dict[str, int]:
    environments = {}
    environments|= environment_vanilla_table
    if (dlc_sotv): environments|= environment_sotv_table
    environments|= environment_hidden_realm_table
    return environments

# add environments into the item table
item_table|= get_environment_table(dlc_sotv=True)
# use the sotv dlc in the item table so that all names can be looked up regardless of use

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
    ItemWeights.option_scraps_only: scraps_only
}

lookup_id_to_name: Dict[int, str] = {id: name for name, id in item_table.items()} | {id: name for name, id in get_environment_table(dlc_sotv=True).items()}
# use the sotv dlc in the lookup table so that all ids can be looked up regardless of use
