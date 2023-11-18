from BaseClasses import CollectionState, MultiWorld, LocationProgressType
from .Locations import get_locations_by_category

#def has_room_of_beginnings(state: CollectionState, player: int, floor_num) -> bool:
#    return state.has("Key of Beginnings F" + floor_num, player)
#
#def has_room_of_guidance(state: CollectionState, player: int, floor_num) -> bool:
#    return state.has_all({"Key of Beginnings F" + floor_num, "Key of Guidance F" + floor_num}, player)
#
#def has_room_of_truth(state: CollectionState, player: int, floor_num) -> bool:
#    return state.has_all({"Key of Beginnings F" + floor_num, "Key of Guidance F" + floor_num, "Key to Truth F" + floor_num}, player)

def has_room_of_rewards(state: CollectionState, player: int, floor_num) -> bool:
    return state.has("Key to Rewards F" + floor_num, player)

def has_item(state: CollectionState, player: int, item) -> bool:
    return state.has(item, player)

def set_rules(multiworld: MultiWorld, player: int):
    #Location rules.
    #Keys
    multiworld.get_location("F01 Traverse Town Room of Rewards (Attack Cards Lionheart)"         , player).access_rule = lambda state: has_room_of_rewards   (state, player, "01")
    multiworld.get_location("F03 Olympus Coliseum Room of Rewards (Attack Card Metal Chocobo)"   , player).access_rule = lambda state: has_room_of_rewards   (state, player, "03")
    multiworld.get_location("F09 Hollow Bastion Room of Rewards (Characters I Mushu)"            , player).access_rule = lambda state: has_room_of_rewards   (state, player, "09")
    multiworld.get_location("F09 Hollow Bastion Room of Rewards (Magic Cards Mushu)"             , player).access_rule = lambda state: has_room_of_rewards   (state, player, "09")
    
    multiworld.get_location("Heartless Air Pirate"                                               , player).access_rule = lambda state: has_item(state, player,"Neverland")
    multiworld.get_location("Heartless Air Soldier"                                              , player).access_rule = lambda state: has_item(state, player,"Monstro") or has_item(state, player,"Agrabah") or has_item(state, player,"Halloween Town") or has_item(state, player,"Destiny Islands")
    multiworld.get_location("Heartless Aquatank"                                                 , player).access_rule = lambda state: has_item(state, player,"Atlantica")
    multiworld.get_location("Heartless Bandit"                                                   , player).access_rule = lambda state: has_item(state, player,"Agrabah")
    multiworld.get_location("Heartless Barrel Spider"                                            , player).access_rule = lambda state: has_item(state, player,"Monstro") or has_item(state, player,"Agrabah") or has_item(state, player,"Neverland") or has_item(state, player,"Destiny Islands")
    multiworld.get_location("Heartless Bouncywild"                                               , player).access_rule = lambda state: has_item(state, player,"Olympus Coliseum")
    multiworld.get_location("Heartless Creeper Plant"                                            , player).access_rule = lambda state: has_item(state, player,"Wonderland") or has_item(state, player,"Halloween Town") or has_item(state, player,"Destiny Islands")
    multiworld.get_location("Heartless Crescendo"                                                , player).access_rule = lambda state: has_item(state, player,"Wonderland") or has_item(state, player,"Neverland") or has_item(state, player,"Destiny Islands")
    multiworld.get_location("Heartless Darkball"                                                 , player).access_rule = lambda state: has_item(state, player,"Atlantica") or has_item(state, player,"Neverland") or has_item(state, player,"Destiny Islands") or has_item(state, player,"Castle Oblivion")
    multiworld.get_location("Heartless Defender"                                                 , player).access_rule = lambda state: has_item(state, player,"Hollow Bastion") or has_item(state, player,"Castle Oblivion")
    multiworld.get_location("Heartless Fat Bandit"                                               , player).access_rule = lambda state: has_item(state, player,"Agrabah")
    multiworld.get_location("Heartless Gargoyle"                                                 , player).access_rule = lambda state: has_item(state, player,"Halloween Town")
    multiworld.get_location("Heartless Green Requiem"                                            , player).access_rule = lambda state: has_item(state, player,"Monstro") or has_item(state, player,"Agrabah") or has_item(state, player,"Castle Oblivion")
    multiworld.get_location("Heartless Large Body"                                               , player).access_rule = lambda state: has_item(state, player,"Wonderland") or has_item(state, player,"Olympus Coliseum")
    multiworld.get_location("Heartless Neoshadow"                                                , player).access_rule = lambda state: has_item(state, player,"Castle Oblivion")
    multiworld.get_location("Heartless Pirate"                                                   , player).access_rule = lambda state: has_item(state, player,"Neverland")
    multiworld.get_location("Heartless Powerwild"                                                , player).access_rule = lambda state: has_item(state, player,"Olympus Coliseum")
    multiworld.get_location("Heartless Screwdiver"                                               , player).access_rule = lambda state: has_item(state, player,"Atlantica")
    multiworld.get_location("Heartless Sea Neon"                                                 , player).access_rule = lambda state: has_item(state, player,"Atlantica")
    multiworld.get_location("Heartless Search Ghost"                                             , player).access_rule = lambda state: has_item(state, player,"Monstro") or has_item(state, player,"Atlantica")
    multiworld.get_location("Heartless Tornado Step"                                             , player).access_rule = lambda state: has_item(state, player,"Monstro") or has_item(state, player,"Hollow Bastion") or has_item(state, player,"Destiny Islands")
    multiworld.get_location("Heartless Wight Knight"                                             , player).access_rule = lambda state: has_item(state, player,"Halloween Town")
    multiworld.get_location("Heartless Wizard"                                                   , player).access_rule = lambda state: has_item(state, player,"Hollow Bastion") or has_item(state, player,"Castle Oblivion")
    multiworld.get_location("Heartless Wyvern"                                                   , player).access_rule = lambda state: has_item(state, player,"Hollow Bastion") or has_item(state, player,"Castle Oblivion")
    multiworld.get_location("Heartless Yellow Opera"                                             , player).access_rule = lambda state: has_item(state, player,"Monstro") or has_item(state, player,"Agrabah") or has_item(state, player,"Neverland") or has_item(state, player,"Castle Oblivion")
    
    # Region rules.
    multiworld.get_entrance("Floor 2"                                                            , player).access_rule = lambda state: has_item(state, player,"Wonderland")
    multiworld.get_entrance("Floor 3"                                                            , player).access_rule = lambda state: has_item(state, player,"Olympus Coliseum")
    multiworld.get_entrance("Floor 4"                                                            , player).access_rule = lambda state: has_item(state, player,"Monstro")
    multiworld.get_entrance("Floor 5"                                                            , player).access_rule = lambda state: has_item(state, player,"Agrabah")
    multiworld.get_entrance("Floor 6"                                                            , player).access_rule = lambda state: has_item(state, player,"Halloween Town")
    multiworld.get_entrance("Floor 7"                                                            , player).access_rule = lambda state: has_item(state, player,"Atlantica")
    multiworld.get_entrance("Floor 8"                                                            , player).access_rule = lambda state: has_item(state, player,"Neverland")
    multiworld.get_entrance("Floor 9"                                                            , player).access_rule = lambda state: has_item(state, player,"Hollow Bastion")
    multiworld.get_entrance("Floor 10"                                                           , player).access_rule = lambda state: has_item(state, player,"100 Acre Wood")
    multiworld.get_entrance("Floor 11"                                                           , player).access_rule = lambda state: has_item(state, player,"Twilight Town")
    multiworld.get_entrance("Floor 12"                                                           , player).access_rule = lambda state: has_item(state, player,"Destiny Islands")
    multiworld.get_entrance("Floor 13"                                                           , player).access_rule = lambda state: has_item(state, player,"Castle Oblivion")
    
    # Options
    
    if multiworld.prioritize_bosses[player]:
        for location in multiworld.get_locations(player):
            if location.name in get_locations_by_category("Boss").keys():
                location.progress_type = LocationProgressType.PRIORITY
    
    
    # Win condition.
    multiworld.completion_condition[player] = lambda state: state.has_all({"Donald", "Goofy", "Aladdin", "Ariel", "Beast", "Jack", "Peter Pan"}, player)
