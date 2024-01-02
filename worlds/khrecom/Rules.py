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

def has_x_worlds(state: CollectionState, player: int, num_of_worlds) -> bool:
    locations = 0
    if has_item(state, player,"World Card Wonderland"):
        locations = locations + 1
    if has_item(state, player,"World Card Olympus Coliseum"):
        locations = locations + 1
    if has_item(state, player,"World Card Monstro"):
        locations = locations + 1
    if has_item(state, player,"World Card Agrabah"):
        locations = locations + 1
    if has_item(state, player,"World Card Halloween Town"):
        locations = locations + 1
    if has_item(state, player,"World Card Atlantica"):
        locations = locations + 1
    if has_item(state, player,"World Card Neverland"):
        locations = locations + 1
    if has_item(state, player,"World Card Hollow Bastion"):
        locations = locations + 1
    if has_item(state, player,"World Card 100 Acre Wood"):
        locations = locations + 1
    if has_item(state, player,"World Card Twilight Town"):
        locations = locations + 1
    if has_item(state, player,"World Card Destiny Islands"):
        locations = locations + 1
    if has_item(state, player,"World Card Castle Oblivion"):
        locations = locations + 1
    if locations > num_of_worlds:
        return True
    return False

def has_item(state: CollectionState, player: int, item) -> bool:
    return state.has(item, player)

def set_rules(multiworld: MultiWorld, player: int, days: bool):
    #Location rules.
    #Keys
    multiworld.get_location("Traverse Town Room of Rewards (Attack Cards Lionheart)"             , player).access_rule = lambda state: has_item(state, player,"Key to Rewards Traverse Town")
    multiworld.get_location("Olympus Coliseum Room of Rewards (Attack Cards Metal Chocobo)"      , player).access_rule = lambda state: has_item(state, player,"Key to Rewards Olympus Coliseum")
    multiworld.get_location("Hollow Bastion Room of Rewards (Summon Cards Mushu)"                , player).access_rule = lambda state: has_item(state, player,"Key to Rewards Hollow Bastion")
    multiworld.get_location("Destiny Islands Room of Rewards (Item Cards Megalixir)"             , player).access_rule = lambda state: has_item(state, player,"Key to Rewards Destiny Islands")
    multiworld.get_location("Atlantica Post Floor (Magic Cards Aero)"                            , player).access_rule = lambda state: has_item(state, player,"World Card Halloween Town")
   #multiworld.get_location("Twilight Town Post Floor (Item Cards Mega-Potion)"                  , player).access_rule = lambda state: has_item(state, player,"World Card Halloween Town") and has_item(state, player,"World Card Atlantica") Bugged because of the post cutscene?
    multiworld.get_location("Destiny Islands Post Floor (Enemy Cards Larxene)"                   , player).access_rule = lambda state: has_item(state, player,"World Card Halloween Town") and has_item(state, player,"World Card Atlantica")
    multiworld.get_location("Destiny Islands Post Floor (Enemy Cards Riku)"                      , player).access_rule = lambda state: has_item(state, player,"World Card Halloween Town") and has_item(state, player,"World Card Atlantica")
    multiworld.get_location("Destiny Islands Post Floor (Attack Cards Oblivion)"                 , player).access_rule = lambda state: has_item(state, player,"World Card Halloween Town") and has_item(state, player,"World Card Atlantica")
    multiworld.get_location("100 Acre Wood Tigger's Playground (Attack Cards Spellbinder)"       , player).access_rule = lambda state: has_item(state, player,"World Card Neverland") and has_item(state, player,"World Card Monstro")
    
    #Days Rules
    if days:
        multiworld.get_location("Traverse Town Room of Rewards (Enemy Cards Saix)"                   , player).access_rule = lambda state: has_item(state, player,"Key to Rewards Traverse Town")
        multiworld.get_location("Wonderland Room of Rewards (Enemy Cards Xemnas)"                    , player).access_rule = lambda state: has_item(state, player,"Key to Rewards Wonderland")
        multiworld.get_location("Olympus Coliseum Room of Rewards (Attack Cards Total Eclipse)"      , player).access_rule = lambda state: has_item(state, player,"Key to Rewards Olympus Coliseum")
        multiworld.get_location("Monstro Room of Rewards (Enemy Cards Xaldin)"                       , player).access_rule = lambda state: has_item(state, player,"Key to Rewards Monstro")
        multiworld.get_location("Agrabah Room of Rewards (Enemy Cards Luxord)"                       , player).access_rule = lambda state: has_item(state, player,"Key to Rewards Agrabah")
        multiworld.get_location("Halloween Town Room of Rewards (Attack Cards Bond of Flame)"        , player).access_rule = lambda state: has_item(state, player,"Key to Rewards Halloween Town")
        multiworld.get_location("Atlantica Room of Rewards (Enemy Cards Demyx)"                      , player).access_rule = lambda state: has_item(state, player,"Key to Rewards Atlantica")
        multiworld.get_location("Neverland Room of Rewards (Attack Cards Midnight Roar)"             , player).access_rule = lambda state: has_item(state, player,"Key to Rewards Neverland")
        multiworld.get_location("Hollow Bastion Room of Rewards (Enemy Cards Xigbar)"                , player).access_rule = lambda state: has_item(state, player,"Key to Rewards Hollow Bastion")
        multiworld.get_location("Twilight Town Room of Rewards (Enemy Cards Roxas)"                  , player).access_rule = lambda state: has_item(state, player,"Key to Rewards Twilight Town")
        multiworld.get_location("Destiny Islands Room of Rewards (Attack Cards Two Become One)"      , player).access_rule = lambda state: has_item(state, player,"Key to Rewards Destiny Islands")
        multiworld.get_location("Castle Oblivion Room of Rewards (Attack Cards Star Seeker)"         , player).access_rule = lambda state: has_item(state, player,"Key to Rewards Castle Oblivion")

    
    multiworld.get_location("Heartless Air Pirate"                                               , player).access_rule = lambda state: has_item(state, player,"World Card Neverland")
    multiworld.get_location("Heartless Air Soldier"                                              , player).access_rule = lambda state: has_item(state, player,"World Card Monstro") or has_item(state, player,"World Card Agrabah") or has_item(state, player,"World Card Halloween Town") or has_item(state, player,"World Card Destiny Islands")
    multiworld.get_location("Heartless Aquatank"                                                 , player).access_rule = lambda state: has_item(state, player,"World Card Atlantica")
    multiworld.get_location("Heartless Bandit"                                                   , player).access_rule = lambda state: has_item(state, player,"World Card Agrabah")
    multiworld.get_location("Heartless Barrel Spider"                                            , player).access_rule = lambda state: has_item(state, player,"World Card Monstro") or has_item(state, player,"World Card Agrabah") or has_item(state, player,"World Card Neverland") or has_item(state, player,"World Card Destiny Islands")
    multiworld.get_location("Heartless Bouncywild"                                               , player).access_rule = lambda state: has_item(state, player,"World Card Olympus Coliseum")
    multiworld.get_location("Heartless Creeper Plant"                                            , player).access_rule = lambda state: has_item(state, player,"World Card Wonderland") or has_item(state, player,"World Card Halloween Town") or has_item(state, player,"World Card Destiny Islands")
    multiworld.get_location("Heartless Crescendo"                                                , player).access_rule = lambda state: has_item(state, player,"World Card Wonderland") or has_item(state, player,"World Card Neverland") or has_item(state, player,"World Card Destiny Islands")
    multiworld.get_location("Heartless Darkball"                                                 , player).access_rule = lambda state: has_item(state, player,"World Card Atlantica") or has_item(state, player,"World Card Neverland") or has_item(state, player,"World Card Destiny Islands") or has_item(state, player,"World Card Castle Oblivion")
    multiworld.get_location("Heartless Defender"                                                 , player).access_rule = lambda state: has_item(state, player,"World Card Hollow Bastion") or has_item(state, player,"World Card Castle Oblivion")
    multiworld.get_location("Heartless Fat Bandit"                                               , player).access_rule = lambda state: has_item(state, player,"World Card Agrabah")
    multiworld.get_location("Heartless Gargoyle"                                                 , player).access_rule = lambda state: has_item(state, player,"World Card Halloween Town")
    multiworld.get_location("Heartless Green Requiem"                                            , player).access_rule = lambda state: has_item(state, player,"World Card Monstro") or has_item(state, player,"World Card Agrabah") or has_item(state, player,"World Card Castle Oblivion")
    multiworld.get_location("Heartless Large Body"                                               , player).access_rule = lambda state: has_item(state, player,"World Card Wonderland") or has_item(state, player,"World Card Olympus Coliseum")
    multiworld.get_location("Heartless Neoshadow"                                                , player).access_rule = lambda state: has_item(state, player,"World Card Castle Oblivion")
    multiworld.get_location("Heartless Pirate"                                                   , player).access_rule = lambda state: has_item(state, player,"World Card Neverland")
    multiworld.get_location("Heartless Powerwild"                                                , player).access_rule = lambda state: has_item(state, player,"World Card Olympus Coliseum")
    multiworld.get_location("Heartless Screwdiver"                                               , player).access_rule = lambda state: has_item(state, player,"World Card Atlantica")
    multiworld.get_location("Heartless Sea Neon"                                                 , player).access_rule = lambda state: has_item(state, player,"World Card Atlantica")
    multiworld.get_location("Heartless Search Ghost"                                             , player).access_rule = lambda state: has_item(state, player,"World Card Monstro") or has_item(state, player,"World Card Atlantica")
    multiworld.get_location("Heartless Tornado Step"                                             , player).access_rule = lambda state: has_item(state, player,"World Card Monstro") or has_item(state, player,"World Card Hollow Bastion") or has_item(state, player,"World Card Destiny Islands")
    multiworld.get_location("Heartless Wight Knight"                                             , player).access_rule = lambda state: has_item(state, player,"World Card Halloween Town")
    multiworld.get_location("Heartless Wizard"                                                   , player).access_rule = lambda state: has_item(state, player,"World Card Hollow Bastion") or has_item(state, player,"World Card Castle Oblivion")
    multiworld.get_location("Heartless Wyvern"                                                   , player).access_rule = lambda state: has_item(state, player,"World Card Hollow Bastion") or has_item(state, player,"World Card Castle Oblivion")
    multiworld.get_location("Heartless Yellow Opera"                                             , player).access_rule = lambda state: has_item(state, player,"World Card Monstro") or has_item(state, player,"World Card Agrabah") or has_item(state, player,"World Card Neverland") or has_item(state, player,"World Card Castle Oblivion")
    
    # Region rules.
    multiworld.get_entrance("Floor 2"                                                            , player).access_rule = lambda state: has_item(state, player,"World Card Wonderland")
    multiworld.get_entrance("Floor 3"                                                            , player).access_rule = lambda state: has_item(state, player,"World Card Olympus Coliseum")
    multiworld.get_entrance("Floor 4"                                                            , player).access_rule = lambda state: has_item(state, player,"World Card Monstro")
    multiworld.get_entrance("Floor 5"                                                            , player).access_rule = lambda state: has_item(state, player,"World Card Agrabah")
    multiworld.get_entrance("Floor 6"                                                            , player).access_rule = lambda state: has_item(state, player,"World Card Halloween Town")
    multiworld.get_entrance("Floor 7"                                                            , player).access_rule = lambda state: has_item(state, player,"World Card Atlantica")
    multiworld.get_entrance("Floor 8"                                                            , player).access_rule = lambda state: has_item(state, player,"World Card Neverland")
    multiworld.get_entrance("Floor 9"                                                            , player).access_rule = lambda state: has_item(state, player,"World Card Hollow Bastion")
    multiworld.get_entrance("Floor 10"                                                           , player).access_rule = lambda state: has_item(state, player,"World Card 100 Acre Wood")
    multiworld.get_entrance("Floor 11"                                                           , player).access_rule = lambda state: has_item(state, player,"World Card Twilight Town") and has_x_worlds(state, player, 5)
    multiworld.get_entrance("Floor 12"                                                           , player).access_rule = lambda state: has_item(state, player,"World Card Destiny Islands") and has_x_worlds(state, player, 7)
    multiworld.get_entrance("Floor 13"                                                           , player).access_rule = lambda state: state.has_all({"Friend Card Donald", "Friend Card Goofy", "Friend Card Aladdin", "Friend Card Ariel", "Friend Card Beast", "Friend Card Jack", "Friend Card Peter Pan", "World Card Halloween Town", "World Card Atlantica", "World Card Destiny Islands"}, player) and has_x_worlds(state, player, 9)
    
    
    
    # Win condition.
    multiworld.completion_condition[player] = lambda state: has_item(state, player,"Victory")
