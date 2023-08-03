from worlds.generic.Rules import add_rule, add_item_rule
from typing import Set
from .Items import ItemType, all_items
from .Names.LocationName import LocationName
from .Names.ItemName import ItemName
from .Locations import location_type_to_data, LocationType


def set_access_rules(multiworld, player):
    add_rule(multiworld.get_location(LocationName.Kandorean_Temple_Lash_Pebble, player),
             lambda state: state.has(ItemName.Chestbeaters_defeated, player) or (state.has(ItemName.Lash_Pebble, player)))

    add_rule(multiworld.get_location(LocationName.Kandorean_Temple_Chestbeaters, player),
            lambda state: (state.count_group(ItemType.Djinn, player) > 1))


    add_rule(multiworld.get_location(LocationName.Dehkan_Plateau_Nut, player),
             lambda state: state.has(ItemName.Lash_Pebble, player))

    add_rule(multiworld.get_location(LocationName.Mars_Lighthouse_Doom_Dragon, player),
             lambda state: state.has(ItemName.Cyclone_Chip, player))

    for loc in location_type_to_data[LocationType.Hidden]:
        add_rule(multiworld.get_location(loc.name, player),
                 lambda state: state.has(ItemName.Reveal, player))


def set_item_rules(multiworld, player):
    djinn: Set[str] = {item.itemName for item in all_items if item.type == ItemType.Djinn}

    for loc in location_type_to_data[LocationType.Djinn]:
        add_item_rule(multiworld.get_location(loc.name, player), lambda item: item.player == player and item.name in djinn)

    add_item_rule(multiworld.get_location(LocationName.Daila_Smoke_Bomb, player),
                  lambda item: item.player == player and item.name == ItemName.Cyclone_Chip)