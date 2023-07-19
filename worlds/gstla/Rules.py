from worlds.generic.Rules import add_rule, add_item_rule
from typing import Set
from .Items import ItemType, all_items
from .Names.LocationName import LocationName
from .Names.ItemName import ItemName


def set_access_rules(multiworld, player):
    add_rule(multiworld.get_location(LocationName.Kandorean_Temple_Lash_Pebble, player),
             lambda state: state.has(ItemName.DefeatChestbeaters, player) or (state.has(ItemName.Lash_Pebble, player)))

    add_rule(multiworld.get_location(LocationName.DefeatChestBeaters, player),
            lambda state: (state.count_group(ItemType.Djinn, player) > 1))


    add_rule(multiworld.get_location(LocationName.Dehkan_Plateau_Nut, player),
             lambda state: state.has(ItemName.Lash_Pebble, player))

    add_rule(multiworld.get_location(LocationName.DoomDragonDefeated, player),
             lambda state: state.has(ItemName.Cyclone_Chip, player))


def set_item_rules(multiworld, player):
    djinn: Set[str] = {item.itemName for item in all_items if item.type == ItemType.Djinn}

    add_item_rule(multiworld.get_location("Echo", player),
                  lambda item: item.player == player and item.name in djinn)
    add_item_rule(multiworld.get_location("Fog", player),
                  lambda item: item.player == player and item.name in djinn)
    add_item_rule(multiworld.get_location("Breath", player),
                  lambda item: item.player == player and item.name in djinn)
    add_item_rule(multiworld.get_location("Iron", player),
                  lambda item: item.player == player and item.name in djinn)
    add_item_rule(multiworld.get_location("Cannon", player),
                  lambda item: item.player == player and item.name in djinn)

    add_item_rule(multiworld.get_location(LocationName.Kandorean_Temple_Lash_Pebble, player),
                  lambda item: item.player == player and item.name == ItemName.Cyclone_Chip)