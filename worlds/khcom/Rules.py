from BaseClasses import CollectionState, MultiWorld, LocationProgressType
from .Locations import get_locations_by_category

def has_room_of_beginnings(state: CollectionState, player: int, floor_num) -> bool:
    return state.has("Key of Beginnings F" + floor_num, player)

def has_room_of_guidance(state: CollectionState, player: int, floor_num) -> bool:
    return state.has_all({"Key of Beginnings F" + floor_num, "Key of Guidance F" + floor_num}, player)

def has_room_of_truth(state: CollectionState, player: int, floor_num) -> bool:
    return state.has_all({"Key of Beginnings F" + floor_num, "Key of Guidance F" + floor_num, "Key to Truth F" + floor_num}, player)

def has_room_of_rewards(state: CollectionState, player: int, floor_num) -> bool:
    return state.has("Key to Rewards F" + floor_num, player)


def set_rules(multiworld: MultiWorld, player: int):
    #Location rules.
    #Keys
    multiworld.get_location("F02 Wonderland Room of Guidance"                      , player).access_rule = lambda state: has_room_of_guidance  (state, player, "02")
    multiworld.get_location("F03 Olympus Coliseum Room of Guidance"                , player).access_rule = lambda state: has_room_of_guidance  (state, player, "03")
    multiworld.get_location("F04 Monstro Room of Guidance"                         , player).access_rule = lambda state: has_room_of_guidance  (state, player, "04")
    multiworld.get_location("F05 Agrabah Room of Guidance"                         , player).access_rule = lambda state: has_room_of_guidance  (state, player, "05")
    multiworld.get_location("F06 Halloween Town Room of Guidance"                  , player).access_rule = lambda state: has_room_of_guidance  (state, player, "06")
    multiworld.get_location("F07 Atlantica Room of Guidance"                       , player).access_rule = lambda state: has_room_of_guidance  (state, player, "07")
    multiworld.get_location("F08 Neverland Room of Guidance"                       , player).access_rule = lambda state: has_room_of_guidance  (state, player, "08")
    multiworld.get_location("F09 Hollow Bastion Room of Guidance"                  , player).access_rule = lambda state: has_room_of_guidance  (state, player, "09")
    #Progression
    multiworld.get_location("F02 Wonderland Room of Beginnings (Card Soldier Red)" , player).access_rule = lambda state: has_room_of_beginnings(state, player, "02")
    multiworld.get_location("F02 Wonderland Room of Truth (Trickmaster)"           , player).access_rule = lambda state: has_room_of_truth     (state, player, "02")
    multiworld.get_location("F03 Olympus Coliseum Room of Guidance (Hi-Potion)"    , player).access_rule = lambda state: has_room_of_guidance  (state, player, "03")
    multiworld.get_location("F03 Olympus Coliseum Room of Truth (Hades)"           , player).access_rule = lambda state: has_room_of_truth     (state, player, "03")
    multiworld.get_location("F03 Olympus Coliseum Room of Truth (Cloud)"           , player).access_rule = lambda state: has_room_of_truth     (state, player, "03")
    multiworld.get_location("F04 Monstro Room of Guidance (Parasite Cage)"         , player).access_rule = lambda state: has_room_of_guidance  (state, player, "04")
    multiworld.get_location("F04 Monstro Room of Truth (Dumbo)"                    , player).access_rule = lambda state: has_room_of_truth     (state, player, "04")
    multiworld.get_location("F05 Agrabah Room of Guidance (Ether)"                 , player).access_rule = lambda state: has_room_of_guidance  (state, player, "05")
    multiworld.get_location("F05 Agrabah Room of Truth (Jafar)"                    , player).access_rule = lambda state: has_room_of_truth     (state, player, "05")
    multiworld.get_location("F05 Agrabah Room of Truth (Genie)"                    , player).access_rule = lambda state: has_room_of_truth     (state, player, "05")
    multiworld.get_location("F06 Halloween Town Room of Truth (Oogie Boogie)"      , player).access_rule = lambda state: has_room_of_truth     (state, player, "06")
    multiworld.get_location("F06 Halloween Town Post Floor (Thunder)"              , player).access_rule = lambda state: has_room_of_truth     (state, player, "06")
    multiworld.get_location("F07 Atlantica Room of Truth (Ursula)"                 , player).access_rule = lambda state: has_room_of_truth     (state, player, "07")
    multiworld.get_location("F07 Atlantica Post Floor (Aero)"                      , player).access_rule = lambda state: has_room_of_truth     (state, player, "07")
    multiworld.get_location("F08 Neverland Room of Truth (Hook)"                   , player).access_rule = lambda state: has_room_of_truth     (state, player, "08")
    multiworld.get_location("F08 Neverland Room of Truth (Tinker Bell)"            , player).access_rule = lambda state: has_room_of_truth     (state, player, "08")
    multiworld.get_location("F09 Hollow Bastion Room of Truth (Dragon Maleficent)" , player).access_rule = lambda state: has_room_of_truth     (state, player, "09")
    multiworld.get_location("F11 Twilight Town Room of Beginnings (Vexen)"         , player).access_rule = lambda state: has_room_of_beginnings(state, player, "11")
    multiworld.get_location("F11 Twilight Town Post Floor (Mega-Potion)"           , player).access_rule = lambda state: has_room_of_beginnings(state, player, "11")
    multiworld.get_location("F12 Destiny Islands Room of Guidance (Darkside)"      , player).access_rule = lambda state: has_room_of_guidance  (state, player, "12")
    multiworld.get_location("F12 Destiny Islands Post Floor (Riku)"                , player).access_rule = lambda state: has_room_of_guidance  (state, player, "12")
    #multiworld.get_location("F12 Destiny Islands Post Floor (Larxene)"             , player).access_rule = lambda state: has_room_of_guidance  (state, player, "12")
    multiworld.get_location("F13 Castle Oblivion Room of Beginnings (Axel)"        , player).access_rule = lambda state: has_room_of_beginnings(state, player, "13")
    multiworld.get_location("F13 Castle Oblivion Post Floor (Marluxia)"            , player).access_rule = lambda state: has_room_of_beginnings(state, player, "13")
    multiworld.get_location("F13 Castle Oblivion Post Marluxia (One-Winged Angel)" , player).access_rule = lambda state: has_room_of_beginnings(state, player, "13")
    multiworld.get_location("F13 Castle Oblivion Post Marluxia (Diamond Dust)"     , player).access_rule = lambda state: has_room_of_beginnings(state, player, "13")
    #Room of Rewards
    multiworld.get_location("F01 Traverse Town Room of Rewards (Lionheart)"        , player).access_rule = lambda state: has_room_of_rewards   (state, player, "01")
    multiworld.get_location("F03 Olympus Coliseum Room of Rewards (Metal Chocobo)" , player).access_rule = lambda state: has_room_of_rewards   (state, player, "03")
    multiworld.get_location("F09 Hollow Bastion Room of Rewards (Mushu)"           , player).access_rule = lambda state: has_room_of_rewards   (state, player, "09")
    multiworld.get_location("F12 Destiny Islands Room of Rewards (Megalixir)"      , player).access_rule = lambda state: has_room_of_rewards   (state, player, "12")

    # Region rules.
    multiworld.get_entrance("Floor 2"                                              , player).access_rule = lambda state: has_room_of_beginnings(state, player, "02")
    multiworld.get_entrance("Floor 3"                                              , player).access_rule = lambda state: has_room_of_beginnings(state, player, "03")
    multiworld.get_entrance("Floor 4"                                              , player).access_rule = lambda state: has_room_of_beginnings(state, player, "04")
    multiworld.get_entrance("Floor 5"                                              , player).access_rule = lambda state: has_room_of_beginnings(state, player, "05")
    multiworld.get_entrance("Floor 6"                                              , player).access_rule = lambda state: has_room_of_beginnings(state, player, "06")
    multiworld.get_entrance("Floor 7"                                              , player).access_rule = lambda state: has_room_of_beginnings(state, player, "07")
    multiworld.get_entrance("Floor 8"                                              , player).access_rule = lambda state: has_room_of_beginnings(state, player, "08")
    multiworld.get_entrance("Floor 9"                                              , player).access_rule = lambda state: has_room_of_beginnings(state, player, "09")
    multiworld.get_entrance("Floor 10"                                             , player).access_rule = lambda state: has_room_of_beginnings(state, player, "10")
    multiworld.get_entrance("Floor 11"                                             , player).access_rule = lambda state: has_room_of_beginnings(state, player, "11")
    multiworld.get_entrance("Floor 12"                                             , player).access_rule = lambda state: has_room_of_beginnings(state, player, "12")
    multiworld.get_entrance("Floor 13"                                             , player).access_rule = lambda state: has_room_of_beginnings(state, player, "13")
    
    # Options
    if not multiworld.enemy_cards[player]:
        for location in multiworld.get_locations(player):
            if location.name in get_locations_by_category("Enemy Unlock").keys():
                location.progress_type = LocationProgressType.EXCLUDED
    
    if multiworld.prioritize_bosses[player]:
        for location in multiworld.get_locations(player):
            if location.name in get_locations_by_category("Boss").keys():
                location.progress_type = LocationProgressType.PRIORITY
    
    # Win condition.
    multiworld.completion_condition[player] = lambda state: state.has_all({"Donald", "Goofy", "Aladdin", "Ariel", "Beast", "Jack", "Peter Pan"}, player)
