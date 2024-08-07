from BaseClasses import CollectionState, MultiWorld, LocationProgressType
from .Locations import get_locations_by_category

def has_castle_oblivion(state: CollectionState, player: int) -> bool:
    return state.has_all({"Friend Card Donald", "Friend Card Goofy", "Friend Card Aladdin", "Friend Card Ariel"\
        , "Friend Card Beast", "Friend Card Jack", "Friend Card Peter Pan", "Friend Card Pluto"\
        , "World Card Halloween Town", "World Card Atlantica", "World Card Destiny Islands"\
        }, player) and has_x_worlds(state, player, 8)

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
    if locations > num_of_worlds:
        return True
    return False

def has_item(state: CollectionState, player: int, item) -> bool:
    return state.has(item, player)

def set_rules(multiworld: MultiWorld, player: int, options):
    #Location rules.
    multiworld.get_location("Traverse Town Room of Rewards (Attack Cards Lionheart)"                 , player).access_rule = lambda state: has_item(state, player,"Key to Rewards Traverse Town")
    multiworld.get_location("Olympus Coliseum Room of Rewards (Attack Cards Metal Chocobo)"          , player).access_rule = lambda state: has_item(state, player,"Key to Rewards Olympus Coliseum")
    multiworld.get_location("Hollow Bastion Room of Rewards (Summon Cards Mushu)"                    , player).access_rule = lambda state: has_item(state, player,"Key to Rewards Hollow Bastion")
    multiworld.get_location("Destiny Islands Room of Rewards (Item Cards Megalixir)"                 , player).access_rule = lambda state: has_item(state, player,"Key to Rewards Destiny Islands")
    multiworld.get_location("06F Exit Hall Larxene I (Magic Cards Thunder)"                          , player).access_rule = lambda state: has_x_worlds(state, player, 4)
    multiworld.get_location("07F Exit Hall Riku I (Magic Cards Aero)"                                , player).access_rule = lambda state: has_x_worlds(state, player, 5)
    multiworld.get_location("11F Exit Hall Riku III (Item Cards Mega-Potion)"                        , player).access_rule = lambda state: has_x_worlds(state, player, 6)
    multiworld.get_location("12F Exit Hall Larxene II (Attack Cards Oblivion)"                       , player).access_rule = lambda state: has_x_worlds(state, player, 7)
    multiworld.get_location("12F Exit Hall Larxene II (Enemy Cards Larxene)"                         , player).access_rule = lambda state: has_x_worlds(state, player, 7)
    multiworld.get_location("12F Exit Hall Riku IV (Enemy Cards Riku)"                               , player).access_rule = lambda state: has_x_worlds(state, player, 7)
    multiworld.get_location("100 Acre Wood Tigger's Playground (Attack Cards Spellbinder)"           , player).access_rule = lambda state: has_item(state, player,"World Card Neverland") and has_item(state, player,"World Card Monstro")
    
    #Days Rules
    if options.days_locations:
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

    
    multiworld.get_location("Defeat 1 Heartless Air Pirate"                                          , player).access_rule = lambda state: has_item(state, player,"World Card Neverland")
    multiworld.get_location("Defeat 2 Heartless Air Pirate"                                          , player).access_rule = lambda state: has_item(state, player,"World Card Neverland")
    multiworld.get_location("Defeat 3 Heartless Air Pirate"                                          , player).access_rule = lambda state: has_item(state, player,"World Card Neverland")
    multiworld.get_location("Defeat 1 Heartless Air Soldier"                                         , player).access_rule = lambda state: has_item(state, player,"World Card Monstro") or has_item(state, player,"World Card Agrabah") or has_item(state, player,"World Card Twilight Town")
    multiworld.get_location("Defeat 2 Heartless Air Soldier"                                         , player).access_rule = lambda state: has_item(state, player,"World Card Monstro") or has_item(state, player,"World Card Agrabah") or has_item(state, player,"World Card Twilight Town")
    multiworld.get_location("Defeat 3 Heartless Air Soldier"                                         , player).access_rule = lambda state: has_item(state, player,"World Card Monstro") or has_item(state, player,"World Card Agrabah") or has_item(state, player,"World Card Twilight Town")
    multiworld.get_location("Defeat 1 Heartless Aquatank"                                            , player).access_rule = lambda state: has_item(state, player,"World Card Atlantica")
    multiworld.get_location("Defeat 2 Heartless Aquatank"                                            , player).access_rule = lambda state: has_item(state, player,"World Card Atlantica")
    multiworld.get_location("Defeat 3 Heartless Aquatank"                                            , player).access_rule = lambda state: has_item(state, player,"World Card Atlantica")
    multiworld.get_location("Defeat 1 Heartless Bandit"                                              , player).access_rule = lambda state: has_item(state, player,"World Card Agrabah")
    multiworld.get_location("Defeat 2 Heartless Bandit"                                              , player).access_rule = lambda state: has_item(state, player,"World Card Agrabah")
    multiworld.get_location("Defeat 3 Heartless Bandit"                                              , player).access_rule = lambda state: has_item(state, player,"World Card Agrabah")
    multiworld.get_location("Defeat 1 Heartless Barrel Spider"                                       , player).access_rule = lambda state: has_item(state, player,"World Card Monstro") or has_item(state, player,"World Card Agrabah") or has_item(state, player,"World Card Neverland")
    multiworld.get_location("Defeat 2 Heartless Barrel Spider"                                       , player).access_rule = lambda state: has_item(state, player,"World Card Monstro") or has_item(state, player,"World Card Agrabah") or has_item(state, player,"World Card Neverland")
    multiworld.get_location("Defeat 3 Heartless Barrel Spider"                                       , player).access_rule = lambda state: has_item(state, player,"World Card Monstro") or has_item(state, player,"World Card Agrabah") or has_item(state, player,"World Card Neverland")
    multiworld.get_location("Defeat 1 Heartless Bouncywild"                                          , player).access_rule = lambda state: has_item(state, player,"World Card Olympus Coliseum")
    multiworld.get_location("Defeat 2 Heartless Bouncywild"                                          , player).access_rule = lambda state: has_item(state, player,"World Card Olympus Coliseum")
    multiworld.get_location("Defeat 3 Heartless Bouncywild"                                          , player).access_rule = lambda state: has_item(state, player,"World Card Olympus Coliseum")
    multiworld.get_location("Defeat 1 Heartless Creeper Plant"                                       , player).access_rule = lambda state: has_item(state, player,"World Card Wonderland") or has_item(state, player,"World Card Halloween Town") or has_item(state, player,"World Card Destiny Islands")
    multiworld.get_location("Defeat 2 Heartless Creeper Plant"                                       , player).access_rule = lambda state: has_item(state, player,"World Card Wonderland") or has_item(state, player,"World Card Halloween Town") or has_item(state, player,"World Card Destiny Islands")
    multiworld.get_location("Defeat 3 Heartless Creeper Plant"                                       , player).access_rule = lambda state: has_item(state, player,"World Card Wonderland") or has_item(state, player,"World Card Halloween Town") or has_item(state, player,"World Card Destiny Islands")
    multiworld.get_location("Defeat 1 Heartless Crescendo"                                           , player).access_rule = lambda state: has_item(state, player,"World Card Wonderland") or has_item(state, player,"World Card Neverland") or has_item(state, player,"World Card Destiny Islands")
    multiworld.get_location("Defeat 2 Heartless Crescendo"                                           , player).access_rule = lambda state: has_item(state, player,"World Card Wonderland") or has_item(state, player,"World Card Neverland") or has_item(state, player,"World Card Destiny Islands")
    multiworld.get_location("Defeat 3 Heartless Crescendo"                                           , player).access_rule = lambda state: has_item(state, player,"World Card Wonderland") or has_item(state, player,"World Card Neverland") or has_item(state, player,"World Card Destiny Islands")
    multiworld.get_location("Defeat 1 Heartless Darkball"                                            , player).access_rule = lambda state: has_item(state, player,"World Card Atlantica") or has_item(state, player,"World Card Neverland") or has_item(state, player,"World Card Destiny Islands") or has_castle_oblivion(state, player)
    multiworld.get_location("Defeat 2 Heartless Darkball"                                            , player).access_rule = lambda state: has_item(state, player,"World Card Atlantica") or has_item(state, player,"World Card Neverland") or has_item(state, player,"World Card Destiny Islands") or has_castle_oblivion(state, player)
    multiworld.get_location("Defeat 3 Heartless Darkball"                                            , player).access_rule = lambda state: has_item(state, player,"World Card Atlantica") or has_item(state, player,"World Card Neverland") or has_item(state, player,"World Card Destiny Islands") or has_castle_oblivion(state, player)
    multiworld.get_location("Defeat 1 Heartless Defender"                                            , player).access_rule = lambda state: has_item(state, player,"World Card Hollow Bastion") or has_castle_oblivion(state, player)
    multiworld.get_location("Defeat 2 Heartless Defender"                                            , player).access_rule = lambda state: has_item(state, player,"World Card Hollow Bastion") or has_castle_oblivion(state, player)
    multiworld.get_location("Defeat 3 Heartless Defender"                                            , player).access_rule = lambda state: has_item(state, player,"World Card Hollow Bastion") or has_castle_oblivion(state, player)
    multiworld.get_location("Defeat 1 Heartless Fat Bandit"                                          , player).access_rule = lambda state: has_item(state, player,"World Card Agrabah")
    multiworld.get_location("Defeat 2 Heartless Fat Bandit"                                          , player).access_rule = lambda state: has_item(state, player,"World Card Agrabah")
    multiworld.get_location("Defeat 3 Heartless Fat Bandit"                                          , player).access_rule = lambda state: has_item(state, player,"World Card Agrabah")
    multiworld.get_location("Defeat 1 Heartless Gargoyle"                                            , player).access_rule = lambda state: has_item(state, player,"World Card Halloween Town")
    multiworld.get_location("Defeat 2 Heartless Gargoyle"                                            , player).access_rule = lambda state: has_item(state, player,"World Card Halloween Town")
    multiworld.get_location("Defeat 3 Heartless Gargoyle"                                            , player).access_rule = lambda state: has_item(state, player,"World Card Halloween Town")
    multiworld.get_location("Defeat 1 Heartless Green Requiem"                                       , player).access_rule = lambda state: has_item(state, player,"World Card Monstro") or has_item(state, player,"World Card Agrabah") or has_castle_oblivion(state, player)
    multiworld.get_location("Defeat 2 Heartless Green Requiem"                                       , player).access_rule = lambda state: has_item(state, player,"World Card Monstro") or has_item(state, player,"World Card Agrabah") or has_castle_oblivion(state, player)
    multiworld.get_location("Defeat 3 Heartless Green Requiem"                                       , player).access_rule = lambda state: has_item(state, player,"World Card Monstro") or has_item(state, player,"World Card Agrabah") or has_castle_oblivion(state, player)
    multiworld.get_location("Defeat 1 Heartless Large Body"                                          , player).access_rule = lambda state: has_item(state, player,"World Card Wonderland") or has_item(state, player,"World Card Olympus Coliseum")
    multiworld.get_location("Defeat 2 Heartless Large Body"                                          , player).access_rule = lambda state: has_item(state, player,"World Card Wonderland") or has_item(state, player,"World Card Olympus Coliseum")
    multiworld.get_location("Defeat 3 Heartless Large Body"                                          , player).access_rule = lambda state: has_item(state, player,"World Card Wonderland") or has_item(state, player,"World Card Olympus Coliseum")
    multiworld.get_location("Defeat 1 Heartless Neoshadow"                                           , player).access_rule = lambda state: has_castle_oblivion(state, player)
    multiworld.get_location("Defeat 2 Heartless Neoshadow"                                           , player).access_rule = lambda state: has_castle_oblivion(state, player)
    multiworld.get_location("Defeat 3 Heartless Neoshadow"                                           , player).access_rule = lambda state: has_castle_oblivion(state, player)
    multiworld.get_location("Defeat 1 Heartless Pirate"                                              , player).access_rule = lambda state: has_item(state, player,"World Card Neverland")
    multiworld.get_location("Defeat 2 Heartless Pirate"                                              , player).access_rule = lambda state: has_item(state, player,"World Card Neverland")
    multiworld.get_location("Defeat 3 Heartless Pirate"                                              , player).access_rule = lambda state: has_item(state, player,"World Card Neverland")
    multiworld.get_location("Defeat 1 Heartless Powerwild"                                           , player).access_rule = lambda state: has_item(state, player,"World Card Olympus Coliseum")
    multiworld.get_location("Defeat 2 Heartless Powerwild"                                           , player).access_rule = lambda state: has_item(state, player,"World Card Olympus Coliseum")
    multiworld.get_location("Defeat 3 Heartless Powerwild"                                           , player).access_rule = lambda state: has_item(state, player,"World Card Olympus Coliseum")
    multiworld.get_location("Defeat 1 Heartless Screwdiver"                                          , player).access_rule = lambda state: has_item(state, player,"World Card Atlantica")
    multiworld.get_location("Defeat 2 Heartless Screwdiver"                                          , player).access_rule = lambda state: has_item(state, player,"World Card Atlantica")
    multiworld.get_location("Defeat 3 Heartless Screwdiver"                                          , player).access_rule = lambda state: has_item(state, player,"World Card Atlantica")
    multiworld.get_location("Defeat 1 Heartless Sea Neon"                                            , player).access_rule = lambda state: has_item(state, player,"World Card Atlantica")
    multiworld.get_location("Defeat 2 Heartless Sea Neon"                                            , player).access_rule = lambda state: has_item(state, player,"World Card Atlantica")
    multiworld.get_location("Defeat 3 Heartless Sea Neon"                                            , player).access_rule = lambda state: has_item(state, player,"World Card Atlantica")
    multiworld.get_location("Defeat 1 Heartless Search Ghost"                                        , player).access_rule = lambda state: has_item(state, player,"World Card Monstro") or has_item(state, player,"World Card Atlantica")
    multiworld.get_location("Defeat 2 Heartless Search Ghost"                                        , player).access_rule = lambda state: has_item(state, player,"World Card Monstro") or has_item(state, player,"World Card Atlantica")
    multiworld.get_location("Defeat 3 Heartless Search Ghost"                                        , player).access_rule = lambda state: has_item(state, player,"World Card Monstro") or has_item(state, player,"World Card Atlantica")
    multiworld.get_location("Defeat 1 Heartless Tornado Step"                                        , player).access_rule = lambda state: has_item(state, player,"World Card Monstro") or has_item(state, player,"World Card Hollow Bastion") or has_item(state, player,"World Card Destiny Islands")
    multiworld.get_location("Defeat 2 Heartless Tornado Step"                                        , player).access_rule = lambda state: has_item(state, player,"World Card Monstro") or has_item(state, player,"World Card Hollow Bastion") or has_item(state, player,"World Card Destiny Islands")
    multiworld.get_location("Defeat 3 Heartless Tornado Step"                                        , player).access_rule = lambda state: has_item(state, player,"World Card Monstro") or has_item(state, player,"World Card Hollow Bastion") or has_item(state, player,"World Card Destiny Islands")
    multiworld.get_location("Defeat 1 Heartless Wight Knight"                                        , player).access_rule = lambda state: has_item(state, player,"World Card Halloween Town")
    multiworld.get_location("Defeat 2 Heartless Wight Knight"                                        , player).access_rule = lambda state: has_item(state, player,"World Card Halloween Town")
    multiworld.get_location("Defeat 3 Heartless Wight Knight"                                        , player).access_rule = lambda state: has_item(state, player,"World Card Halloween Town")
    multiworld.get_location("Defeat 1 Heartless Wizard"                                              , player).access_rule = lambda state: has_item(state, player,"World Card Hollow Bastion") or has_castle_oblivion(state, player)
    multiworld.get_location("Defeat 2 Heartless Wizard"                                              , player).access_rule = lambda state: has_item(state, player,"World Card Hollow Bastion") or has_castle_oblivion(state, player)
    multiworld.get_location("Defeat 3 Heartless Wizard"                                              , player).access_rule = lambda state: has_item(state, player,"World Card Hollow Bastion") or has_castle_oblivion(state, player)
    multiworld.get_location("Defeat 1 Heartless Wyvern"                                              , player).access_rule = lambda state: has_item(state, player,"World Card Hollow Bastion") or has_castle_oblivion(state, player)
    multiworld.get_location("Defeat 2 Heartless Wyvern"                                              , player).access_rule = lambda state: has_item(state, player,"World Card Hollow Bastion") or has_castle_oblivion(state, player)
    multiworld.get_location("Defeat 3 Heartless Wyvern"                                              , player).access_rule = lambda state: has_item(state, player,"World Card Hollow Bastion") or has_castle_oblivion(state, player)
    multiworld.get_location("Defeat 1 Heartless Yellow Opera"                                        , player).access_rule = lambda state: has_item(state, player,"World Card Monstro") or has_item(state, player,"World Card Agrabah") or has_item(state, player,"World Card Neverland") or has_castle_oblivion(state, player)
    multiworld.get_location("Defeat 2 Heartless Yellow Opera"                                        , player).access_rule = lambda state: has_item(state, player,"World Card Monstro") or has_item(state, player,"World Card Agrabah") or has_item(state, player,"World Card Neverland") or has_castle_oblivion(state, player)
    multiworld.get_location("Defeat 3 Heartless Yellow Opera"                                        , player).access_rule = lambda state: has_item(state, player,"World Card Monstro") or has_item(state, player,"World Card Agrabah") or has_item(state, player,"World Card Neverland") or has_castle_oblivion(state, player)
    
    if options.levels:
        multiworld.get_location("Level 12 (Sleight Strike Raid)"                                     , player).access_rule = lambda state: has_x_worlds(state, player, 2)
        multiworld.get_location("Level 17 (Sleight Blitz)"                                           , player).access_rule = lambda state: has_x_worlds(state, player, 2)
        multiworld.get_location("Level 22 (Sleight Zantetsuken)"                                     , player).access_rule = lambda state: has_x_worlds(state, player, 3)
        multiworld.get_location("Level 27 (Sleight Sonic Blade)"                                     , player).access_rule = lambda state: has_x_worlds(state, player, 3)
        multiworld.get_location("Level 32 (Sleight Lethal Frame)"                                    , player).access_rule = lambda state: has_x_worlds(state, player, 4)
        multiworld.get_location("Level 37 (Sleight Tornado)"                                         , player).access_rule = lambda state: has_x_worlds(state, player, 4)
        multiworld.get_location("Level 42 (Sleight Ars Arcanum)"                                     , player).access_rule = lambda state: has_x_worlds(state, player, 5)
        multiworld.get_location("Level 47 (Sleight Holy)"                                            , player).access_rule = lambda state: has_x_worlds(state, player, 5)
        multiworld.get_location("Level 52 (Sleight Ragnarok)"                                        , player).access_rule = lambda state: has_x_worlds(state, player, 6)
        multiworld.get_location("Level 57 (Sleight Mega Flare)"                                      , player).access_rule = lambda state: has_x_worlds(state, player, 6)
    multiworld.get_location("Agrabah Room of Rewards (Sleight Warp)"                                 , player).access_rule = lambda state: has_item(state, player, "Key to Rewards Agrabah")
    multiworld.get_location("Atlantica Room of Rewards (Sleight Quake)"                              , player).access_rule = lambda state: has_item(state, player, "Key to Rewards Atlantica")
    multiworld.get_location("Halloween Town Room of Rewards (Sleight Bind)"                          , player).access_rule = lambda state: has_item(state, player, "Key to Rewards Halloween Town")
    multiworld.get_location("Hollow Bastion Room of Rewards (Sleight Flare Breath LV2)"              , player).access_rule = lambda state: has_item(state, player, "Key to Rewards Hollow Bastion")
    multiworld.get_location("Hollow Bastion Room of Rewards (Sleight Flare Breath LV3)"              , player).access_rule = lambda state: has_item(state, player, "Key to Rewards Hollow Bastion")
    multiworld.get_location("Monstro Room of Rewards (Sleight Aqua Splash)"                          , player).access_rule = lambda state: has_item(state, player, "Key to Rewards Monstro")
    multiworld.get_location("Neverland Room of Rewards (Sleight Thunder Raid)"                       , player).access_rule = lambda state: has_item(state, player, "Key to Rewards Neverland")
    multiworld.get_location("Twilight Town Room of Rewards (Sleight Stardust Blitz)"                 , player).access_rule = lambda state: has_item(state, player, "Key to Rewards Twilight Town")
    multiworld.get_location("Wonderland Room of Rewards (Sleight Synchro)"                           , player).access_rule = lambda state: has_item(state, player, "Key to Rewards Wonderland")
    multiworld.get_location("08F Exit Hall Riku II (Sleight Magnet Spiral)"                          , player).access_rule = lambda state: has_x_worlds(state, player, 5)
    multiworld.get_location("10F Exit Hall Vexen I (Sleight Freeze)"                                 , player).access_rule = lambda state: has_x_worlds(state, player, 6)
    multiworld.get_location("06F Exit Hall Larxene I (Sleight Thundara)"                             , player).access_rule = lambda state: has_x_worlds(state, player, 4)
    multiworld.get_location("06F Exit Hall Larxene I (Sleight Thundaga)"                             , player).access_rule = lambda state: has_x_worlds(state, player, 4)
    multiworld.get_location("07F Exit Hall Riku I (Sleight Aerora)"                                  , player).access_rule = lambda state: has_x_worlds(state, player, 5)
    multiworld.get_location("07F Exit Hall Riku I (Sleight Aeroga)"                                  , player).access_rule = lambda state: has_x_worlds(state, player, 5)
    
    # Region rules.
    multiworld.get_entrance("Wonderland"                                                             , player).access_rule = lambda state: has_item(state, player,"World Card Wonderland")
    multiworld.get_entrance("Olympus Coliseum"                                                       , player).access_rule = lambda state: has_item(state, player,"World Card Olympus Coliseum")
    multiworld.get_entrance("Monstro"                                                                , player).access_rule = lambda state: has_item(state, player,"World Card Monstro")
    multiworld.get_entrance("Agrabah"                                                                , player).access_rule = lambda state: has_item(state, player,"World Card Agrabah")
    multiworld.get_entrance("Halloween Town"                                                         , player).access_rule = lambda state: has_item(state, player,"World Card Halloween Town")
    multiworld.get_entrance("Atlantica"                                                              , player).access_rule = lambda state: has_item(state, player,"World Card Atlantica")
    multiworld.get_entrance("Neverland"                                                              , player).access_rule = lambda state: has_item(state, player,"World Card Neverland")
    multiworld.get_entrance("Hollow Bastion"                                                         , player).access_rule = lambda state: has_item(state, player,"World Card Hollow Bastion")
    multiworld.get_entrance("100 Acre Wood"                                                          , player).access_rule = lambda state: has_item(state, player,"World Card 100 Acre Wood")
    multiworld.get_entrance("Twilight Town"                                                          , player).access_rule = lambda state: has_item(state, player,"World Card Twilight Town") and has_x_worlds(state, player, 4)
    multiworld.get_entrance("Destiny Islands"                                                        , player).access_rule = lambda state: has_item(state, player,"World Card Destiny Islands") and has_x_worlds(state, player, 6)
    multiworld.get_entrance("Castle Oblivion"                                                        , player).access_rule = lambda state: has_castle_oblivion(state, player)
    
    
    
    # Win condition.
    multiworld.completion_condition[player] = lambda state: has_item(state, player,"Victory")
