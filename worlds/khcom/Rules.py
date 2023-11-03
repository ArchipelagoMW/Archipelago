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
    multiworld.get_location("Key of Guidance F02", player).access_rule = lambda state: has_room_of_beginnings(state, player, "02")
    multiworld.get_location("Key of Guidance F03", player).access_rule = lambda state: has_room_of_beginnings(state, player, "03")
    multiworld.get_location("Key of Guidance F04", player).access_rule = lambda state: has_room_of_beginnings(state, player, "04")
    multiworld.get_location("Key of Guidance F05", player).access_rule = lambda state: has_room_of_beginnings(state, player, "05")
    multiworld.get_location("Key of Guidance F06", player).access_rule = lambda state: has_room_of_beginnings(state, player, "06")
    multiworld.get_location("Key of Guidance F07", player).access_rule = lambda state: has_room_of_beginnings(state, player, "07")
    multiworld.get_location("Key of Guidance F08", player).access_rule = lambda state: has_room_of_beginnings(state, player, "08")
    multiworld.get_location("Key of Guidance F09", player).access_rule = lambda state: has_room_of_beginnings(state, player, "09")
    multiworld.get_location("Key of Guidance F12", player).access_rule = lambda state: has_room_of_beginnings(state, player, "12")
    multiworld.get_location("Key to Truth F02"   , player).access_rule = lambda state: has_room_of_guidance  (state, player, "02")
    multiworld.get_location("Key to Truth F03"   , player).access_rule = lambda state: has_room_of_guidance  (state, player, "03")
    multiworld.get_location("Key to Truth F04"   , player).access_rule = lambda state: has_room_of_guidance  (state, player, "04")
    multiworld.get_location("Key to Truth F05"   , player).access_rule = lambda state: has_room_of_guidance  (state, player, "05")
    multiworld.get_location("Key to Truth F06"   , player).access_rule = lambda state: has_room_of_guidance  (state, player, "06")
    multiworld.get_location("Key to Truth F07"   , player).access_rule = lambda state: has_room_of_guidance  (state, player, "07")
    multiworld.get_location("Key to Truth F08"   , player).access_rule = lambda state: has_room_of_guidance  (state, player, "08")
    multiworld.get_location("Key to Truth F09"   , player).access_rule = lambda state: has_room_of_guidance  (state, player, "09")
    #Progression
    multiworld.get_location("Card Soldier (Red)" , player).access_rule = lambda state: has_room_of_beginnings(state, player, "02")
    multiworld.get_location("Trickmaster"        , player).access_rule = lambda state: has_room_of_truth     (state, player, "02")
    multiworld.get_location("Hi-Potion"          , player).access_rule = lambda state: has_room_of_guidance  (state, player, "03")
    multiworld.get_location("Hades"              , player).access_rule = lambda state: has_room_of_truth     (state, player, "03")
    multiworld.get_location("Cloud"              , player).access_rule = lambda state: has_room_of_truth     (state, player, "03")
    multiworld.get_location("Parasite Cage"      , player).access_rule = lambda state: has_room_of_guidance  (state, player, "04")
    multiworld.get_location("Dumbo"              , player).access_rule = lambda state: has_room_of_truth     (state, player, "04")
    multiworld.get_location("Ether"              , player).access_rule = lambda state: has_room_of_guidance  (state, player, "05")
    multiworld.get_location("Jafar"              , player).access_rule = lambda state: has_room_of_truth     (state, player, "05")
    multiworld.get_location("Genie"              , player).access_rule = lambda state: has_room_of_truth     (state, player, "05")
    multiworld.get_location("Oogie Boogie"       , player).access_rule = lambda state: has_room_of_truth     (state, player, "06")
    multiworld.get_location("Thunder"            , player).access_rule = lambda state: has_room_of_truth     (state, player, "06")
    multiworld.get_location("Ursula"             , player).access_rule = lambda state: has_room_of_truth     (state, player, "07")
    multiworld.get_location("Aero"               , player).access_rule = lambda state: has_room_of_truth     (state, player, "07")
    multiworld.get_location("Hook"               , player).access_rule = lambda state: has_room_of_truth     (state, player, "08")
    multiworld.get_location("Tinker Bell"        , player).access_rule = lambda state: has_room_of_truth     (state, player, "08")
    multiworld.get_location("Dragon Maleficent"  , player).access_rule = lambda state: has_room_of_truth     (state, player, "09")
    multiworld.get_location("Vexen"              , player).access_rule = lambda state: has_room_of_beginnings(state, player, "11")
    multiworld.get_location("Mega-Potion"        , player).access_rule = lambda state: has_room_of_beginnings(state, player, "11")
    multiworld.get_location("Darkside"           , player).access_rule = lambda state: has_room_of_guidance  (state, player, "12")
    multiworld.get_location("Riku"               , player).access_rule = lambda state: has_room_of_guidance  (state, player, "12")
    #multiworld.get_location("Larxene"            , player).access_rule = lambda state: has_room_of_guidance  (state, player, "12") missable
    multiworld.get_location("Axel"               , player).access_rule = lambda state: has_room_of_beginnings(state, player, "13")
    multiworld.get_location("Marluxia"           , player).access_rule = lambda state: has_room_of_beginnings(state, player, "13")
    #Room of Rewards
    multiworld.get_location("Lionheart"          , player).access_rule = lambda state: has_room_of_rewards   (state, player, "01")
    multiworld.get_location("Metal Chocobo"      , player).access_rule = lambda state: has_room_of_rewards   (state, player, "03")
    multiworld.get_location("Mushu"              , player).access_rule = lambda state: has_room_of_rewards   (state, player, "09")
    multiworld.get_location("Megalixir"          , player).access_rule = lambda state: has_room_of_rewards   (state, player, "12")

    # Region rules.
    multiworld.get_entrance("Floor 2" , player).access_rule = lambda state: has_room_of_beginnings(state, player, "02")
    multiworld.get_entrance("Floor 3" , player).access_rule = lambda state: has_room_of_beginnings(state, player, "03")
    multiworld.get_entrance("Floor 4" , player).access_rule = lambda state: has_room_of_beginnings(state, player, "04")
    multiworld.get_entrance("Floor 5" , player).access_rule = lambda state: has_room_of_beginnings(state, player, "05")
    multiworld.get_entrance("Floor 6" , player).access_rule = lambda state: has_room_of_beginnings(state, player, "06")
    multiworld.get_entrance("Floor 7" , player).access_rule = lambda state: has_room_of_beginnings(state, player, "07")
    multiworld.get_entrance("Floor 8" , player).access_rule = lambda state: has_room_of_beginnings(state, player, "08")
    multiworld.get_entrance("Floor 9" , player).access_rule = lambda state: has_room_of_beginnings(state, player, "09")
    multiworld.get_entrance("Floor 10" , player).access_rule = lambda state: has_room_of_beginnings(state, player, "10")
    multiworld.get_entrance("Floor 11" , player).access_rule = lambda state: has_room_of_beginnings(state, player, "11")
    multiworld.get_entrance("Floor 12" , player).access_rule = lambda state: has_room_of_beginnings(state, player, "12")
    multiworld.get_entrance("Floor 13", player).access_rule = lambda state: has_room_of_guidance(state, player, "12")
    
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
