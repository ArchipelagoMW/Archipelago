from worlds.generic.Rules import add_rule, add_item_rule
from typing import Set
from .Items import ItemType, all_items
from .Names.LocationName import LocationName
from .Names.ItemName import ItemName
from .Locations import location_type_to_data, LocationType


def set_access_rules(multiworld, player):
    #Daila
    add_rule(multiworld.get_location(LocationName.Daila_Sea_Gods_Tear, player),
             lambda state: state.has(ItemName.Lash_Pebble, player))

    add_rule(multiworld.get_location(LocationName.Daila_Psy_Crystal, player),
             lambda state: state.has(ItemName.Scoop_Gem, player))

    #Kandorean Temple
    add_rule(multiworld.get_location(LocationName.Fog, player),
             lambda state: state.has(ItemName.Lash_Pebble, player))

    add_rule(multiworld.get_location(LocationName.Kandorean_Temple_Lash_Pebble, player),
             lambda state: state.has(ItemName.Chestbeaters_defeated, player) or (state.has(ItemName.Lash_Pebble, player)))

    #Dehkan Platea
    add_rule(multiworld.get_location(LocationName.Cannon, player),
             lambda state: state.has(ItemName.Pound_Cube, player))

    add_rule(multiworld.get_location(LocationName.Dehkan_Plateau_Nut, player),
             lambda state: state.has(ItemName.Lash_Pebble, player))

    #Shrine of the Sea God
    add_rule(multiworld.get_location(LocationName.Shrine_of_the_Sea_God_Rusty_Staff, player),
             lambda state: state.has(ItemName.Frost_Jewel, player))

    add_rule(multiworld.get_location(LocationName.Shrine_of_the_Sea_God_Right_Prong, player),
             lambda state: state.has(ItemName.Frost_Jewel, player) and state.has(ItemName.Reveal, player))


    #Indra Cavern
    add_rule(multiworld.get_location(LocationName.Indra_Cavern_Zagan, player),
             lambda state: state.has(ItemName.Lash_Pebble, player))

    #Madra
    add_rule(multiworld.get_location(LocationName.Madra_Cyclone_Chip, player),
             lambda state: state.has(ItemName.Gabombo_Statue_Completed, player))

    #Madra Catacombs
    add_rule(multiworld.get_location(LocationName.Madra_Catacombs_Ruin_Key, player),
             lambda state: state.has(ItemName.Tremor_Bit, player) and state.has(ItemName.Lash_Pebble, player) and state.has(ItemName.Frost_Jewel, player))

    add_rule(multiworld.get_location(LocationName.Madra_Catacombs_Mist_Potion, player),
             lambda state: state.has(ItemName.Lash_Pebble, player) and state.has(ItemName.Frost_Jewel, player))

    add_rule(multiworld.get_location(LocationName.Madra_Catacombs_Moloch, player),
             lambda state: state.has(ItemName.Ruin_Key, player))

    #Yampi Desert
    add_rule(multiworld.get_location(LocationName.Blitz, player),
             lambda state: state.has(ItemName.Pound_Cube, player))

    add_rule(multiworld.get_location(LocationName.Yampi_Desert_Guardian_Ring, player),
             lambda state: state.has(ItemName.Pound_Cube, player) or state.has(ItemName.Sand, player))

    add_rule(multiworld.get_location(LocationName.Yampi_Desert_Antidote, player),
             lambda state: state.has(ItemName.Pound_Cube, player) or state.has(ItemName.Sand, player))


    add_rule(multiworld.get_location(LocationName.Yampi_Desert_King_Scorpion, player),
             lambda state: state.has(ItemName.Pound_Cube, player) and state.count_group(ItemType.Djinn, player) >= 3)

    add_rule(multiworld.get_location(LocationName.Yampi_Desert_Scoop_Gem, player),
             lambda state: state.has(ItemName.King_Scorpion_defeated, player))

    #Yamp Desert Backside
    add_rule(multiworld.get_location(LocationName.Yampi_Desert_Lucky_Medal, player),
             lambda state: state.has(ItemName.Reveal, player))

    add_rule(multiworld.get_location(LocationName.Yampi_Desert_Trainers_Whip, player),
             lambda state: state.has(ItemName.Lash_Pebble, player) or state.has(ItemName.Sand, player))

    add_rule(multiworld.get_location(LocationName.Yampi_Desert_Trainers_Whip, player),
             lambda state: state.has(ItemName.Pound_Cube, player))

    add_rule(multiworld.get_location(LocationName.Yampi_Desert_315_coins, player),
             lambda state: state.has(ItemName.Scoop_Gem, player))


    #Alhafra
    add_rule(multiworld.get_location(LocationName.Alhafra_Psy_Crystal, player),
             lambda state: state.has(ItemName.Reveal, player))


    add_rule(multiworld.get_location(LocationName.Alhafra_Lucky_Medal, player),
             lambda state: state.has(ItemName.Briggs_defeated, player))

    add_rule(multiworld.get_location(LocationName.Alhafra_Briggs, player),
             lambda state: state.count_group(ItemType.Djinn, player) >= 6)

    add_rule(multiworld.get_location(LocationName.Alhafra_Prison_Briggs, player),
             lambda state: state.has(ItemName.Briggs_defeated, player) and state.has(ItemName.Lash_Pebble, player) and state.has(ItemName.Burst_Brooch, player) and state.has(ItemName.Pound_Cube, player))

    #Alhafra Cave
    add_rule(multiworld.get_location(LocationName.Alhafran_Cave_123_coins, player),
             lambda state: state.has(ItemName.Lash_Pebble, player) and state.has(ItemName.Pound_Cube, player))

    add_rule(multiworld.get_location(LocationName.Alhafran_Cave_Ixion_Mail, player),
             lambda state: state.has(ItemName.Lash_Pebble, player) and state.has(ItemName.Pound_Cube, player))

    add_rule(multiworld.get_location(LocationName.Alhafran_Cave_Lucky_Medal, player),
             lambda state: state.has(ItemName.Lash_Pebble, player) and state.has(ItemName.Pound_Cube, player))

    add_rule(multiworld.get_location(LocationName.Alhafran_Cave_Power_Bread, player),
             lambda state: state.has(ItemName.Briggs_escaped, player))

    add_rule(multiworld.get_location(LocationName.Alhafran_Cave_777_coins, player),
             lambda state: state.has(ItemName.Briggs_escaped, player) and state.has(ItemName.Frost_Jewel, player))

    add_rule(multiworld.get_location(LocationName.Alhafran_Cave_Potion, player),
             lambda state: state.has(ItemName.Briggs_escaped, player) and state.has(ItemName.Frost_Jewel, player))

    add_rule(multiworld.get_location(LocationName.Alhafran_Cave_Psy_Crystal, player),
             lambda state: state.has(ItemName.Briggs_escaped, player) and state.has(ItemName.Frost_Jewel, player))



    add_rule(multiworld.get_location(LocationName.Mars_Lighthouse_Doom_Dragon, player),
             lambda state: state.count_group(ItemType.Djinn, player) >= 56)

    for loc in location_type_to_data[LocationType.Hidden]:
        add_rule(multiworld.get_location(loc.name, player),
                 lambda state: state.has(ItemName.Reveal, player))


def set_item_rules(multiworld, player):
    djinn: Set[str] = {item.itemName for item in all_items if item.type == ItemType.Djinn}

    for loc in location_type_to_data[LocationType.Djinn]:
        add_item_rule(multiworld.get_location(loc.name, player), lambda item: item.player == player and item.name in djinn)