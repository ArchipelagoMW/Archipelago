from BaseClasses import CollectionState, MultiWorld

def has_room_of_beginnings(state: CollectionState, player: int, floor_num: str) -> bool:
    return state.has("Key of Beginnings F" + floor_num, player)

def has_room_of_guidance(state: CollectionState, player: int, floor_num: str) -> bool:
    return state.has_all({"Key of Beginnings F" + floor_num, "Key of Guidance F" + floor_num}, player)

def has_room_of_truth(state: CollectionState, player: int, floor_num: str) -> bool:
    return state.has_all({"Key of Beginnings F" + floor_num, "Key of Guidance F" + floor_num, "Key to Truth F" + floor_num}, player)

def has_room_of_rewards(state: CollectionState, player: int, floor_num: str) -> bool:
    return state.has("Key to Rewards F" + floor_num, player)


def set_rules(multiworld: MultiWorld, player: int):
    #Location rules.
    #Keys
    multiworld.get_location("Key of Guidance F02" + str, player).access_rule = lambda state: has_room_of_beginnings(state, player, "02")
    multiworld.get_location("Key of Guidance F03" + str, player).access_rule = lambda state: has_room_of_beginnings(state, player, "03")
    multiworld.get_location("Key of Guidance F04" + str, player).access_rule = lambda state: has_room_of_beginnings(state, player, "04")
    multiworld.get_location("Key of Guidance F05" + str, player).access_rule = lambda state: has_room_of_beginnings(state, player, "05")
    multiworld.get_location("Key of Guidance F06" + str, player).access_rule = lambda state: has_room_of_beginnings(state, player, "06")
    multiworld.get_location("Key of Guidance F07" + str, player).access_rule = lambda state: has_room_of_beginnings(state, player, "07")
    multiworld.get_location("Key of Guidance F08" + str, player).access_rule = lambda state: has_room_of_beginnings(state, player, "08")
    multiworld.get_location("Key of Guidance F09" + str, player).access_rule = lambda state: has_room_of_beginnings(state, player, "09")
    multiworld.get_location("Key of Guidance F12" + str, player).access_rule = lambda state: has_room_of_beginnings(state, player, "12")
    multiworld.get_location("Key to Truth F02"    + str, player).access_rule = lambda state: has_room_of_guidance  (state, player, "02")
    multiworld.get_location("Key to Truth F03"    + str, player).access_rule = lambda state: has_room_of_guidance  (state, player, "03")
    multiworld.get_location("Key to Truth F04"    + str, player).access_rule = lambda state: has_room_of_guidance  (state, player, "04")
    multiworld.get_location("Key to Truth F05"    + str, player).access_rule = lambda state: has_room_of_guidance  (state, player, "05")
    multiworld.get_location("Key to Truth F06"    + str, player).access_rule = lambda state: has_room_of_guidance  (state, player, "06")
    multiworld.get_location("Key to Truth F07"    + str, player).access_rule = lambda state: has_room_of_guidance  (state, player, "07")
    multiworld.get_location("Key to Truth F08"    + str, player).access_rule = lambda state: has_room_of_guidance  (state, player, "08")
    multiworld.get_location("Key to Truth F09"    + str, player).access_rule = lambda state: has_room_of_guidance  (state, player, "09")
    #Progression
    multiworld.get_location("Card Soldier (Red)"  + str, player).access_rule = lambda state: has_room_of_beginnings(state, player, "02")
    multiworld.get_location("Trickmaster"         + str, player).access_rule = lambda state: has_room_of_truth     (state, player, "02")
    multiworld.get_location("Hi-Potion"           + str, player).access_rule = lambda state: has_room_of_guidance  (state, player, "03")
    multiworld.get_location("Hades"               + str, player).access_rule = lambda state: has_room_of_truth     (state, player, "03")
    multiworld.get_location("Cloud"               + str, player).access_rule = lambda state: has_room_of_truth     (state, player, "03")
    multiworld.get_location("Parasite Cage"       + str, player).access_rule = lambda state: has_room_of_guidance  (state, player, "04")
    multiworld.get_location("Dumbo"               + str, player).access_rule = lambda state: has_room_of_truth     (state, player, "04")
    multiworld.get_location("Ether"               + str, player).access_rule = lambda state: has_room_of_guidance  (state, player, "05")
    multiworld.get_location("Jafar"               + str, player).access_rule = lambda state: has_room_of_truth     (state, player, "05")
    multiworld.get_location("Genie"               + str, player).access_rule = lambda state: has_room_of_truth     (state, player, "05")
    multiworld.get_location("Oogie Boogie"        + str, player).access_rule = lambda state: has_room_of_truth     (state, player, "06")
    multiworld.get_location("Thunder"             + str, player).access_rule = lambda state: has_room_of_truth     (state, player, "06")
    multiworld.get_location("Ursula"              + str, player).access_rule = lambda state: has_room_of_truth     (state, player, "07")
    multiworld.get_location("Aero"                + str, player).access_rule = lambda state: has_room_of_truth     (state, player, "07")
    multiworld.get_location("Hook"                + str, player).access_rule = lambda state: has_room_of_truth     (state, player, "08")
    multiworld.get_location("Tinker Bell"         + str, player).access_rule = lambda state: has_room_of_truth     (state, player, "08")
    multiworld.get_location("Dragon Malificent"   + str, player).access_rule = lambda state: has_room_of_truth     (state, player, "09")
    multiworld.get_location("Vexen"               + str, player).access_rule = lambda state: has_room_of_beginnings(state, player, "11")
    multiworld.get_location("Mega-Potion"         + str, player).access_rule = lambda state: has_room_of_beginnings(state, player, "11")
    multiworld.get_location("Darkside"            + str, player).access_rule = lambda state: has_room_of_guidance  (state, player, "12")
    multiworld.get_location("Riku"                + str, player).access_rule = lambda state: has_room_of_guidance  (state, player, "12")
    multiworld.get_location("Larxene"             + str, player).access_rule = lambda state: has_room_of_guidance  (state, player, "12")
    multiworld.get_location("Axel"                + str, player).access_rule = lambda state: has_room_of_beginnings(state, player, "13")
    multiworld.get_location("Marluxia"            + str, player).access_rule = lambda state: has_room_of_beginnings(state, player, "13")
    #Room of Rewards
    multiworld.get_location("Lionheart"           + str, player).access_rule = lambda state: has_room_of_rewards   (state, player, "01")
    multiworld.get_location("Metal Chocobo"       + str, player).access_rule = lambda state: has_room_of_rewards   (state, player, "03")
    multiworld.get_location("Mushu"               + str, player).access_rule = lambda state: has_room_of_rewards   (state, player, "09")
    multiworld.get_location("Megalixir"           + str, player).access_rule = lambda state: has_room_of_rewards   (state, player, "12")

    # Region rules.
    multiworld.get_entrance("Floor 2" , player).access_rule = lambda state: state.has("Wonderland"      , player)
    multiworld.get_entrance("Floor 3" , player).access_rule = lambda state: state.has("Olympus Coliseum", player)
    multiworld.get_entrance("Floor 4" , player).access_rule = lambda state: state.has("Monstro"         , player)
    multiworld.get_entrance("Floor 5" , player).access_rule = lambda state: state.has("Agrabah"         , player)
    multiworld.get_entrance("Floor 6" , player).access_rule = lambda state: state.has("Halloween Town"  , player)
    multiworld.get_entrance("Floor 7" , player).access_rule = lambda state: state.has("Atlantica"       , player)
    multiworld.get_entrance("Floor 8" , player).access_rule = lambda state: state.has("Never Land"      , player)
    multiworld.get_entrance("Floor 9" , player).access_rule = lambda state: state.has("Hollow Bastion"  , player)
    multiworld.get_entrance("Floor 10", player).access_rule = lambda state: state.has("100 Acre Wood"   , player)
    multiworld.get_entrance("Floor 11", player).access_rule = lambda state: state.has("Twilight Town"   , player)
    multiworld.get_entrance("Floor 12", player).access_rule = lambda state: state.has("Destiny Islands" , player)
    multiworld.get_entrance("Floor 13", player).access_rule = lambda state: state.has("Castle Oblivion" , player)
    # Win condition.
    multiworld.completion_condition[player] = lambda state: state.has("Marluxia", player)
