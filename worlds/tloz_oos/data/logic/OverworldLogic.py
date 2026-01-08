from worlds.tloz_oos.Options import OracleOfSeasonsOptions
from .LogicPredicates import *


def make_holodrum_logic(player: int, origin_name: str, options: OracleOfSeasonsOptions):
    gasha_connections = [
        [origin_name, "gasha tree 1", False, lambda state: oos_can_harvest_gasha(state, player, 1)],
        ["gasha tree 1", "gasha tree 2", False, lambda state: oos_can_harvest_gasha(state, player, 2)],
        ["gasha tree 2", "gasha tree 3", False, lambda state: oos_can_harvest_gasha(state, player, 3)],
        ["gasha tree 3", "gasha tree 4", False, lambda state: oos_can_harvest_gasha(state, player, 4)],
        ["gasha tree 4", "gasha tree 5", False, lambda state: oos_can_harvest_gasha(state, player, 5)],
        ["gasha tree 5", "gasha tree 6", False, lambda state: oos_can_harvest_gasha(state, player, 6)],
        ["gasha tree 6", "gasha tree 7", False, lambda state: oos_can_harvest_gasha(state, player, 7)],
        ["gasha tree 7", "gasha tree 8", False, lambda state: oos_can_harvest_gasha(state, player, 8)],
        ["gasha tree 8", "gasha tree 9", False, lambda state: oos_can_harvest_gasha(state, player, 9)],
        ["gasha tree 9", "gasha tree 10", False, lambda state: oos_can_harvest_gasha(state, player, 10)],
        ["gasha tree 10", "gasha tree 11", False, lambda state: oos_can_harvest_gasha(state, player, 11)],
        ["gasha tree 11", "gasha tree 12", False, lambda state: oos_can_harvest_gasha(state, player, 12)],
        ["gasha tree 12", "gasha tree 13", False, lambda state: oos_can_harvest_gasha(state, player, 13)],
        ["gasha tree 13", "gasha tree 14", False, lambda state: oos_can_harvest_gasha(state, player, 14)],
        ["gasha tree 14", "gasha tree 15", False, lambda state: oos_can_harvest_gasha(state, player, 15)],
        ["gasha tree 15", "gasha tree 16", False, lambda state: oos_can_harvest_gasha(state, player, 16)],
    ]

    holodrum_logic = [
        ["maple encounter", "maple trade", False, lambda state: any([
            state.has("Lon Lon Egg", player),
            oos_self_locking_item(state, player, "maple trade", "Lon Lon Egg")
        ])],

        ["horon village", "mayor's gift", False, None],
        ["horon village", "vasu's gift", False, None],
        ["horon village", "mayor's house secret room", False, lambda state: oos_can_remove_rockslide(state, player, False)],
        ["horon village", "horon heart piece", False, lambda state: any([
            oos_can_use_ember_seeds(state, player, False),
            oos_can_dimitri_clip(state, player)
        ])],
        ["horon village", "dr. left reward", False, lambda state: oos_can_use_ember_seeds(state, player, True)],
        ["horon village", "old man in horon", False, lambda state: oos_can_use_ember_seeds(state, player, False)],
        ["horon village", "old man trade", False, lambda state: any([
            state.has("Fish", player),
            oos_self_locking_item(state, player, "old man trade", "Fish")
        ])],
        ["horon village", "tick tock trade", False, lambda state: any([
            state.has("Wooden Bird", player),
            oos_self_locking_item(state, player, "tick tock trade", "Wooden Bird")
        ])],
        ["horon village", "maku tree", False, lambda state: oos_has_sword(state, player, False)],
        ["horon village", "horon village SE chest", False, lambda state: all([
            oos_can_remove_rockslide(state, player, False),
            any([
                oos_can_swim(state, player, False),
                oos_season_in_horon_village(state, player, SEASON_WINTER),
                oos_can_jump_2_wide_liquid(state, player)
            ])
        ])],
        ["horon village", "horon village SW chest", False, lambda state: any([
            all([
                oos_season_in_horon_village(state, player, SEASON_AUTUMN),
                oos_can_break_mushroom(state, player, True)
            ]),
            oos_can_dimitri_clip(state, player)
        ])],

        ["horon village", "horon village portal", False, lambda state: any([
            oos_has_magic_boomerang(state, player),
            oos_can_jump_6_wide_pit(state, player)
        ])],
        ["horon village portal", "horon village", False, lambda state: any([
            oos_can_trigger_lever(state, player),
            oos_can_jump_6_wide_pit(state, player)
        ])],

        ["horon village", "horon village tree", False, lambda state: oos_can_harvest_tree(state, player, True)],

        ["horon village", "horon shop", False, lambda state:
            oos_has_rupees_for_shop(state, player, "horonShop")],
        ["horon village", "advance shop", False, lambda state:
            oos_has_rupees_for_shop(state, player, "advanceShop")],
        ["horon village", "member's shop", False, lambda state: all([
            state.has("Member's Card", player),
            oos_has_rupees_for_shop(state, player, "memberShop")
        ])],
        ["horon village", "clock shop secret", False, lambda state: all([
            oos_has_shovel(state, player),
            any([
                oos_has_noble_sword(state, player),
                state.has("Biggoron's Sword", player),
                oos_has_fools_ore(state, player),
                all([
                    oos_option_medium_logic(state, player),
                    any([
                        oos_has_sword(state, player),
                        oos_has_bombchus(state, player, 3)
                    ])
                ])
            ])
        ])],

        # WESTERN COAST ##############################################################################################

        ["horon village", "western coast", True, None],
        ["western coast", "maple encounter", False, lambda state: oos_can_meet_maple(state, player)],
        ["western coast", "black beast's chest", False, lambda state: all([
            all([
                oos_has_seed_thrower(state, player),
                oos_can_use_ember_seeds(state, player, True),
            ]),
            oos_can_use_mystery_seeds(state, player),
            oos_can_kill_moldorm(state, player)
        ])],

        ["western coast", "d0 entrance", True, None],
        ["western coast", "d0 rupee chest", False, lambda state: all([
            not oos_option_no_d0_alt_entrance(state, player),
            oos_can_break_bush(state, player, True)
        ])],

        ["western coast after ship", "western coast", False, lambda state: all([
            state.has("_met_pirates", player),
            state.has("Pirate's Bell", player)
        ])],

        ["western coast after ship", "coast stump", False, lambda state: all([
            oos_can_remove_rockslide(state, player, False),
            any([
                oos_has_feather(state, player),
                oos_option_hard_logic(state, player)
            ])
        ])],

        ["western coast after ship", "old man near western coast house", False, lambda state: \
            oos_can_use_ember_seeds(state, player, False)],

        ["western coast after ship", "graveyard (winter)", False, lambda state: all([
            oos_can_jump_3_wide_pit(state, player),
            oos_season_in_western_coast(state, player, SEASON_WINTER)
        ])],
        ["graveyard (winter)", "western coast after ship", False, None],

        ["western coast after ship", "graveyard (autumn)", False, lambda state: all([
            oos_can_jump_3_wide_pit(state, player),
            oos_season_in_western_coast(state, player, SEASON_AUTUMN)
        ])],
        ["graveyard (autumn)", "western coast after ship", False, None],

        ["western coast after ship", "graveyard (summer or spring)", False, lambda state: any([
            oos_can_jump_3_wide_pit(state, player),
            oos_season_in_western_coast(state, player, SEASON_SUMMER)
        ])],
        ["graveyard (summer or spring)", "western coast after ship", False, None],

        ["graveyard (winter)", "d7 entrance", False, lambda state: oos_can_remove_snow(state, player, False)],
        ["graveyard (autumn)", "d7 entrance", False, None],
        ["graveyard (summer or spring)", "d7 entrance", False, None],

        ["d7 entrance", "graveyard (winter)", False, lambda state: \
            oos_is_default_season(state, player, "WESTERN_COAST", SEASON_WINTER)],
        ["d7 entrance", "graveyard (autumn)", False, lambda state: \
            oos_is_default_season(state, player, "WESTERN_COAST", SEASON_AUTUMN)],
        ["d7 entrance", "graveyard (summer or spring)", False, lambda state: any([
            oos_is_default_season(state, player, "WESTERN_COAST", SEASON_SUMMER),
            oos_is_default_season(state, player, "WESTERN_COAST", SEASON_SPRING)
        ])],

        ["graveyard (autumn)", "graveyard heart piece", False, lambda state: oos_can_break_mushroom(state, player, False)],

        ["d7 entrance", "graveyard secret", False, lambda state: oos_has_shovel(state, player)],

        # EASTERN SUBURBS #############################################################################################

        ["horon village", "suburbs", True, lambda state: oos_can_use_ember_seeds(state, player, False)],

        ["suburbs", "maple encounter", False, lambda state: oos_can_meet_maple(state, player)],
        ["suburbs", "windmill heart piece", False, lambda state: any([
            oos_season_in_eastern_suburbs(state, player, SEASON_WINTER),
            oos_can_dimitri_clip(state, player)
        ])],
        ["suburbs", "guru-guru trade", False, lambda state: any([
            state.has("Engine Grease", player),
            oos_self_locking_item(state, player, "guru-guru trade", "Engine Grease")
        ])],

        ["suburbs", "eastern suburbs spring cave", False, lambda state: all([
            oos_has_bracelet(state, player),
            oos_season_in_eastern_suburbs(state, player, SEASON_SPRING),
            any([
                oos_has_magnet_gloves(state, player),
                oos_can_jump_3_wide_pit(state, player)
            ])
        ])],

        ["eastern suburbs portal", "suburbs", False, lambda state: oos_can_break_bush(state, player, False)],
        ["suburbs", "eastern suburbs portal", False, lambda state: oos_can_break_bush(state, player, True)],

        ["suburbs", "suburbs fairy fountain", True, lambda state: all([
            any([
                oos_can_swim(state, player, True),
                oos_can_jump_1_wide_liquid(state, player, True),
                oos_has_switch_hook(state, player)
            ]),
            oos_not_season_in_eastern_suburbs(state, player, SEASON_WINTER)
        ])],
        ["suburbs fairy fountain", "maple encounter", False, lambda state: oos_can_meet_maple(state, player)],
        ["suburbs fairy fountain", "suburbs fairy fountain (winter)", False, lambda state: \
            oos_has_winter(state, player)],  # Should be a useless transition, but it might be useful someday
        ["suburbs", "suburbs fairy fountain (winter)", True, lambda state: oos_season_in_eastern_suburbs(state, player, SEASON_WINTER)],
        ["suburbs fairy fountain (winter)", "maple encounter", False, lambda state: oos_can_meet_maple(state, player)],
        ["suburbs fairy fountain (winter)", "suburbs fairy fountain", False, lambda state: \
            oos_can_remove_season(state, player, SEASON_WINTER)],

        ["suburbs fairy fountain", "sunken city", False, lambda state: \
            oos_season_in_eastern_suburbs(state, player, SEASON_SPRING)],
        ["sunken city", "suburbs fairy fountain", False, lambda state: oos_not_season_in_eastern_suburbs(state, player, SEASON_WINTER)],
        ["sunken city", "suburbs fairy fountain (winter)", False, lambda state: oos_season_in_eastern_suburbs(state, player, SEASON_WINTER)],

        # WOODS OF WINTER / 2D SECTOR ################################################################################

        ["suburbs fairy fountain (winter)", "moblin road", False, None],
        ["moblin road", "suburbs fairy fountain (winter)", False, lambda state: \
            oos_season_in_eastern_suburbs(state, player, SEASON_WINTER)],

        ["moblin road", "maple encounter", False, lambda state: oos_can_meet_maple(state, player)],

        ["sunken city", "moblin road", False, lambda state: all([
            oos_has_flippers(state, player),
            any([
                not oos_is_default_season(state, player, "SUNKEN_CITY", SEASON_WINTER),
                oos_can_remove_season(state, player, SEASON_WINTER)
            ])
        ])],

        ["moblin road", "woods of winter, 1st cave", False, lambda state: all([
            oos_can_remove_rockslide(state, player, True),
            oos_can_break_bush(state, player, False, True),
            any([
                not oos_is_default_season(state, player, "WOODS_OF_WINTER", SEASON_WINTER),
                oos_can_remove_season(state, player, SEASON_WINTER)
            ])
        ])],

        ["moblin road", "woods of winter, 2nd cave", False, lambda state: any([
            oos_can_swim(state, player, False),
            oos_can_jump_3_wide_liquid(state, player)
        ])],

        ["moblin road", "holly's house", False, lambda state: \
            oos_season_in_woods_of_winter(state, player, SEASON_WINTER)],

        ["moblin road", "old man near holly's house", False, lambda state: oos_can_use_ember_seeds(state, player, False)],

        ["moblin road", "woods of winter heart piece", False, lambda state: any([
            oos_can_swim(state, player, True),
            oos_has_bracelet(state, player),
            oos_can_jump_1_wide_liquid(state, player, True)
        ])],

        ["suburbs fairy fountain", "central woods of winter", False, None],
        ["suburbs fairy fountain (winter)", "central woods of winter", False, lambda state: any([
            oos_can_jump_1_wide_pit(state, player, True),
            all([
                oos_option_medium_logic(state, player),
                oos_has_switch_hook(state, player)
            ]),
            oos_can_remove_snow(state, player, True)
        ])],

        ["central woods of winter", "woods of winter tree", False, lambda state: oos_can_harvest_tree(state, player, True)],
        ["central woods of winter", "d2 entrance", True, lambda state: oos_can_break_bush(state, player, True, True)],
        ["central woods of winter", "cave outside D2", False, lambda state: all([
            any([
                all([
                    oos_season_in_central_woods_of_winter(state, player, SEASON_AUTUMN),
                    oos_can_break_mushroom(state, player, True),
                ]),
                oos_can_dimitri_clip(state, player)
            ]),
            any([
                oos_can_jump_4_wide_pit(state, player),
                oos_has_magnet_gloves(state, player)
            ])
        ])],

        ["central woods of winter", "d2 stump", True, None],

        ["d2 stump", "d2 roof", True, lambda state: oos_has_bracelet(state, player)],
        ["d2 roof", "d2 alt entrances", True, lambda state: not oos_option_no_d2_alt_entrance(state, player)],

        # EYEGLASS LAKE SECTOR #########################################################################################

        ["impa's house", "horon village", True, None],
        ["impa's house", "maple encounter", False, lambda state: oos_can_meet_maple(state, player)],
        ["impa's house", "eyeglass lake, across bridge", False, lambda state: any([
            oos_can_jump_4_wide_pit(state, player),
            all([
                oos_has_feather(state, player),
                any([
                    oos_is_default_season(state, player, "EYEGLASS_LAKE", SEASON_AUTUMN),
                    all([
                        oos_has_autumn(state, player),
                        oos_can_break_bush(state, player, True)
                    ])
                ])
            ])
        ])],

        ["impa's house", "d1 stump", True, lambda state: oos_can_break_bush(state, player, True, True)],
        ["d1 stump", "north horon", True, lambda state: oos_has_bracelet(state, player)],
        ["d1 stump", "malon trade", False, lambda state: any([
            state.has("Cuccodex", player),
            oos_self_locking_item(state, player, "malon trade", "Cuccodex")
        ])],
        ["d1 stump", "d1 island", True, lambda state: oos_can_break_bush(state, player, True, True)],
        ["d1 stump", "old man near d1", False, lambda state: oos_can_use_ember_seeds(state, player, False)],

        ["d1 island", "d1 entrance", True, lambda state: state.has("Gnarled Key", player)],
        ["d1 island", "golden beasts old man", False, lambda state: all([
            any([
                oos_is_default_season(state, player, "EYEGLASS_LAKE", SEASON_SUMMER),
                all([
                    oos_has_summer(state, player),
                    oos_can_break_bush(state, player, True)
                ])
            ]),
            oos_can_beat_required_golden_beasts(state, player)
        ])],

        ["d1 stump", "eyeglass lake (default)", True, lambda state: all([
            any([
                oos_season_in_eyeglass_lake(state, player, SEASON_SPRING),
                oos_season_in_eyeglass_lake(state, player, SEASON_AUTUMN),
            ]),
            oos_can_jump_1_wide_pit(state, player, True),
            any([
                oos_can_swim(state, player, False),
                all([
                    # To be able to use Dimitri, we need the bracelet to throw him above the pit
                    oos_option_medium_logic(state, player),
                    oos_can_summon_dimitri(state, player),
                    oos_has_bracelet(state, player)
                ])
            ])
        ])],
        ["d1 stump", "eyeglass lake (dry)", True, lambda state: all([
            oos_season_in_eyeglass_lake(state, player, SEASON_SUMMER),
            oos_can_jump_1_wide_pit(state, player, True)
        ])],
        ["d1 stump", "eyeglass lake (frozen)", True, lambda state: all([
            oos_season_in_eyeglass_lake(state, player, SEASON_WINTER),
            oos_can_jump_1_wide_pit(state, player, True)
        ])],

        ["d5 stump", "maple encounter", False, lambda state: oos_can_meet_maple(state, player)],

        ["d5 stump", "eyeglass lake (default)", True, lambda state: all([
            any([
                oos_season_in_eyeglass_lake(state, player, SEASON_SPRING),
                oos_season_in_eyeglass_lake(state, player, SEASON_AUTUMN),
            ]),
            oos_can_swim(state, player, True)
        ])],
        ["d5 stump", "eyeglass lake (dry)", False, lambda state: all([
            oos_season_in_eyeglass_lake(state, player, SEASON_SUMMER),
            oos_can_swim(state, player, False)
        ])],
        ["d5 stump", "eyeglass lake (frozen)", True, lambda state: \
            oos_season_in_eyeglass_lake(state, player, SEASON_WINTER)],

        ["eyeglass lake portal", "eyeglass lake (default)", False, lambda state: all([
            any([
                oos_is_default_season(state, player, "EYEGLASS_LAKE", SEASON_AUTUMN),
                oos_is_default_season(state, player, "EYEGLASS_LAKE", SEASON_SPRING)
            ]),
            oos_can_swim(state, player, False)
        ])],
        ["eyeglass lake (default)", "eyeglass lake portal", False, None],
        ["eyeglass lake portal", "eyeglass lake (frozen)", False, lambda state: all([
            oos_is_default_season(state, player, "EYEGLASS_LAKE", SEASON_WINTER),
            any([
                oos_can_swim(state, player, False),
                oos_can_jump_5_wide_liquid(state, player)
            ])
        ])],
        ["eyeglass lake (frozen)", "eyeglass lake portal", False, lambda state: any([
            oos_can_swim(state, player, True),
            oos_can_jump_5_wide_liquid(state, player)
        ])],
        # This transition has been removed since the anti-softlock has been removed
        # ["eyeglass lake portal", "eyeglass lake (dry)", False, lambda state: \
        #     oos_is_default_season(state, player, "EYEGLASS_LAKE", SEASON_SUMMER)],
        # Instead, jump straight from the portal to lost woods in summer
        ["eyeglass lake portal", "lost woods", False, lambda state: all([
            oos_option_hard_logic(state, player),
            oos_is_default_season(state, player, "EYEGLASS_LAKE", SEASON_SUMMER)
        ])],

        ["eyeglass lake (dry)", "dry eyeglass lake, west cave", False, lambda state: all([
            oos_can_remove_rockslide(state, player, True),
            oos_can_swim(state, player, False)  # chest is surrounded by water
        ])],

        ["d5 stump", "d5 entrance", False, lambda state: all([
            # If we don't have autumn, we need to ensure we were able to reach that node with autumn as default
            # season without changing to another season which we wouldn't be able to revert back.
            # For this reason, "default season is autumn" case is handled through direct routes from the lake portal
            # and from D1 stump.
            oos_has_autumn(state, player),
            oos_can_break_mushroom(state, player, True)
        ])],
        # Direct route #1 to reach D5 entrance taking advantage of autumn as default season
        ["d1 stump", "d5 entrance", False, lambda state: all([
            oos_is_default_season(state, player, "EYEGLASS_LAKE", SEASON_AUTUMN),
            oos_can_jump_1_wide_pit(state, player, True),
            oos_can_break_mushroom(state, player, True),
            any([
                oos_can_swim(state, player, False),
                all([
                    # To be able to use Dimitri, we need the bracelet to throw him above the pit
                    oos_option_medium_logic(state, player),
                    oos_can_summon_dimitri(state, player),
                    oos_has_bracelet(state, player)
                ]),
                all([
                    # Alternatively, we can use winter to summon Dimitri then reset the season with the portal
                    oos_can_summon_dimitri(state, player),
                    oos_has_winter(state, player)
                ])
            ]),
        ])],
        # Direct route #2 to reach D5 entrance taking advantage of autumn as default season
        ["eyeglass lake portal", "d5 entrance", False, lambda state: all([
            oos_is_default_season(state, player, "EYEGLASS_LAKE", SEASON_AUTUMN),
            oos_can_swim(state, player, False),
            oos_can_break_mushroom(state, player, True)
        ])],

        ["d5 entrance", "d5 stump", False, lambda state: any([
            oos_can_jump_1_wide_pit(state, player, True),
            all([
                oos_is_default_season(state, player, "EYEGLASS_LAKE", SEASON_AUTUMN),
                oos_can_break_mushroom(state, player, False)
                # TODO: Maybe change that by removing the anti-softlock mechanism that also adds an anti-ricky protection
                # Alternatively, move the rock up to prevent ricky from jumping while preserving the anti-softlock
            ])
        ])],

        ["d5 stump", "dry eyeglass lake, east cave", False, lambda state: all([
            oos_has_summer(state, player),
            oos_has_bracelet(state, player),
        ])],

        ["d5 entrance", "dry eyeglass lake, east cave", False, lambda state: all([
            oos_can_jump_1_wide_pit(state, player, True),
            oos_is_default_season(state, player, "EYEGLASS_LAKE", SEASON_SUMMER),
            oos_has_bracelet(state, player),
        ])],

        # NORTH HORON / HOLODRUM PLAIN ###############################################################################

        ["north horon", "maple encounter", False, lambda state: oos_can_meet_maple(state, player)],
        ["north horon", "north horon tree", False, lambda state: oos_can_harvest_tree(state, player, True)],
        ["north horon", "blaino prize", False, lambda state: oos_can_farm_rupees(state, player)],
        ["north horon", "cave north of D1", False, lambda state: all([
            any([
                all([
                    oos_season_in_holodrum_plain(state, player, SEASON_AUTUMN),
                    oos_can_break_mushroom(state, player, True),
                ]),
                oos_can_dimitri_clip(state, player)
            ]),
            oos_has_flippers(state, player)
        ])],
        ["north horon", "old man near blaino", False, lambda state: all([
            oos_can_use_ember_seeds(state, player, False),
            any([
                oos_is_default_season(state, player, "HOLODRUM_PLAIN", SEASON_SUMMER),
                oos_can_summon_ricky(state, player),
                all([
                    # can get from the stump to old man in summer
                    oos_has_summer(state, player),
                    any([
                        oos_can_jump_1_wide_pit(state, player, True),
                        all([
                            oos_can_break_bush(state, player, True),
                            oos_can_swim(state, player, True)
                        ])
                    ])
                ])
            ])
        ])],
        ["north horon", "underwater item below natzu bridge", False, lambda state: oos_can_swim(state, player, False)],

        ["north horon", "temple remains lower stump", False, lambda state: oos_can_jump_3_wide_pit(state, player)],
        ["temple remains lower stump", "north horon", False, lambda state: any([
            oos_can_jump_3_wide_pit(state, player),
            oos_has_switch_hook(state, player)
        ])],

        ["ghastly stump", "maple encounter", False, lambda state: oos_can_meet_maple(state, player)],

        ["ghastly stump", "mrs. ruul trade", False, lambda state: any([
            state.has("Ghastly Doll", player),
            oos_self_locking_item(state, player, "mrs. ruul trade", "Ghastly Doll")
        ])],
        ["ghastly stump", "old man near mrs. ruul", False, lambda state: oos_can_use_ember_seeds(state, player, False)],

        ["north horon", "ghastly stump", True, lambda state: any([
            oos_can_jump_1_wide_pit(state, player, True),
            oos_season_in_holodrum_plain(state, player, SEASON_WINTER)
        ])],

        ["spool swamp north", "ghastly stump", False, None],
        ["ghastly stump", "spool swamp north", False, lambda state: any([
            oos_season_in_holodrum_plain(state, player, SEASON_SUMMER),
            oos_can_jump_4_wide_pit(state, player),
            oos_can_summon_ricky(state, player),
            oos_can_summon_moosh(state, player)
        ])],

        ["ghastly stump", "spool swamp south", True, lambda state: all([
            oos_can_swim(state, player, True),
            oos_can_break_bush(state, player, True),
        ])],

        # Goron Mountain <-> North Horon <-> D1 island <-> Spool swamp waterway
        ["spool swamp south", "d1 island", True, lambda state: oos_can_swim(state, player, True)],
        ["d1 island", "north horon", True, lambda state: oos_can_swim(state, player, True)],
        ["north horon", "goron mountain entrance", True, lambda state: oos_can_swim(state, player, True)],
        ["goron mountain entrance", "natzu region, across water", True, lambda state: oos_can_swim(state, player, True)],
        ["ghastly stump", "d1 island", True, lambda state: all([
            # Technically, Ricky and Moosh don't work to go from the ghastly stump bank to the stump,
            # but both can go through north horon and jump the holes
            oos_can_break_bush(state, player, True),
            oos_can_swim(state, player, True)
        ])],

        ["d1 island", "old man in treehouse", False, lambda state: all([
            oos_can_swim(state, player, True),
            oos_has_essences_for_treehouse(state, player)
        ])],
        ["d1 island", "cave south of mrs. ruul", False, lambda state: oos_can_swim(state, player, False)],

        # SPOOL SWAMP #############################################################################################

        ["spool swamp north", "maple encounter", False, lambda state: oos_can_meet_maple(state, player)],

        ["spool swamp north", "spool swamp tree", False, lambda state: oos_can_harvest_tree(state, player, True)],

        ["spool swamp north", "floodgate keeper's house", False, lambda state: any([
            oos_can_trigger_lever(state, player),
            all([
                oos_option_hard_logic(state, player),
                oos_has_bracelet(state, player)
            ])
        ])],

        ["spool swamp north", "spool swamp digging spot", False, lambda state: all([
            oos_season_in_spool_swamp(state, player, SEASON_SUMMER),
            oos_has_shovel(state, player)
        ])],

        ["floodgate keeper's house", "floodgate keyhole", False, lambda state: all([
            any([
                oos_can_use_pegasus_seeds(state, player),
                oos_has_flippers(state, player),
                oos_has_feather(state, player),
                oos_has_cane(state, player)
            ]),
            oos_has_bracelet(state, player)
        ])],
        ["floodgate keyhole", "spool swamp scrub", False, lambda state: \
            oos_has_rupees_for_shop(state, player, "spoolSwampScrub")],
        ["floodgate keyhole", "spool stump", False, lambda state: state.has("Floodgate Key", player)],

        ["spool stump", "d3 entrance", False, lambda state: oos_season_in_spool_swamp(state, player, SEASON_SUMMER)],

        ["spool stump", "spool swamp middle", False, lambda state: any([
            not oos_is_default_season(state, player, "SPOOL_SWAMP", SEASON_SPRING),
            oos_can_remove_season(state, player, SEASON_SPRING),
            oos_can_swim(state, player, True)
        ])],

        ["spool swamp middle", "spool swamp south near gasha spot", False, lambda state: oos_can_summon_ricky(state, player)],
        ["spool swamp south near gasha spot", "spool swamp middle", False, lambda state: any([
            oos_can_summon_ricky(state, player),
            all([
                oos_has_feather(state, player),
                any([
                    oos_has_magic_boomerang(state, player),
                    all([
                        oos_option_medium_logic(state, player),
                        any([
                            oos_has_sword(state, player),
                            all([
                                oos_has_seed_thrower(state, player),
                                oos_can_use_ember_seeds(state, player, False),
                            ]),
                            all([
                                oos_has_bombs(state, player, 2),
                                oos_option_hard_logic(state, player)
                            ])
                        ])
                    ])
                ])
            ])
        ])],

        ["spool swamp south near gasha spot", "maple encounter", False, lambda state: oos_can_meet_maple(state, player)],

        ["spool swamp south near gasha spot", "spool swamp portal", True, lambda state: oos_has_bracelet(state, player)],

        ["spool swamp middle", "spool swamp south", True, lambda state: any([
            oos_can_jump_2_wide_pit(state, player),
            oos_can_summon_moosh(state, player),
            oos_can_swim(state, player, True)
        ])],

        ["spool swamp south", "maple encounter", False, lambda state: oos_can_meet_maple(state, player)],

        # make sure you can go directly from the stump to south, or default season
        # just because you can reach the stump doesn't mean you can also get there
        # ex. only access to gasha section is through subrosia
        ["spool swamp south", "spool swamp south (spring)", False, lambda state: \
            oos_is_default_season(state, player, "SPOOL_SWAMP", SEASON_SPRING)],
        ["spool stump", "spool swamp south (spring)", False, lambda state: all([
            oos_has_spring(state, player),
            oos_can_swim(state, player, True),
            any([
                oos_can_summon_ricky(state, player),
                oos_can_summon_moosh(state, player),
                oos_can_jump_2_wide_pit(state, player)
            ])
        ])],
        ["spool swamp south", "spool swamp south (summer)", False, lambda state: \
            oos_is_default_season(state, player, "SPOOL_SWAMP", SEASON_SUMMER)],
        ["spool stump", "spool swamp south (summer)", False, lambda state: all([
            oos_has_summer(state, player),
            any([
                oos_can_swim(state, player, True),
                oos_can_summon_ricky(state, player),
                oos_can_summon_moosh(state, player),
                oos_can_jump_2_wide_pit(state, player)
            ])
        ])],
        ["spool swamp south", "spool swamp south (autumn)", False, lambda state: \
            oos_is_default_season(state, player, "SPOOL_SWAMP", SEASON_AUTUMN)],
        ["spool stump", "spool swamp south (autumn)", False, lambda state: all([
            oos_has_autumn(state, player),
            any([
                oos_can_swim(state, player, True),
                oos_can_summon_ricky(state, player),
                oos_can_summon_moosh(state, player),
                oos_can_jump_2_wide_pit(state, player)
            ])
        ])],
        ["spool swamp south", "spool swamp south (winter)", False, lambda state: \
            oos_is_default_season(state, player, "SPOOL_SWAMP", SEASON_WINTER)],
        ["spool stump", "spool swamp south (winter)", False, lambda state: all([
            oos_has_winter(state, player),
            any([
                oos_can_swim(state, player, True),
                oos_can_summon_ricky(state, player),
                oos_can_summon_moosh(state, player),
                oos_can_jump_2_wide_pit(state, player)
            ])
        ])],
        ["spool swamp south (winter)", "spool swamp south", False, None],
        ["spool swamp south (spring)", "spool swamp south", False, None],
        ["spool swamp south (summer)", "spool swamp south", False, None],
        ["spool swamp south (autumn)", "spool swamp south", False, None],

        ["spool swamp south (spring)", "spool swamp south near gasha spot", False, lambda state: \
            oos_can_break_flowers(state, player, True)],
        ["spool swamp south (winter)", "spool swamp south near gasha spot", False, lambda state: \
            oos_can_remove_snow(state, player, True)],
        ["spool swamp south (summer)", "spool swamp south near gasha spot", False, None],
        ["spool swamp south (autumn)", "spool swamp south near gasha spot", False, None],

        # default season only because of the portal
        ["spool swamp south near gasha spot", "spool swamp south (spring)", False, lambda state: all([
            oos_is_default_season(state, player, "SPOOL_SWAMP", SEASON_SPRING),
            oos_can_break_flowers(state, player, True)
        ])],
        ["spool swamp south near gasha spot", "spool swamp south (summer)", False, lambda state: \
            oos_is_default_season(state, player, "SPOOL_SWAMP", SEASON_SUMMER)],
        ["spool swamp south near gasha spot", "spool swamp south (autumn)", False, lambda state: \
            oos_is_default_season(state, player, "SPOOL_SWAMP", SEASON_AUTUMN)],
        ["spool swamp south near gasha spot", "spool swamp south (winter)", False, lambda state: all([
            oos_is_default_season(state, player, "SPOOL_SWAMP", SEASON_WINTER),
            oos_can_remove_snow(state, player, True)
        ])],

        ["spool swamp south (winter)", "spool swamp cave", False, lambda state: all([
            oos_can_remove_snow(state, player, True),
            oos_can_remove_rockslide(state, player, True)
        ])],

        ["spool swamp south (spring)", "spool swamp heart piece", False, lambda state: \
            oos_can_swim(state, player, True)],

        # NATZU REGION #############################################################################################

        ["north horon", "natzu west", True, None],

        ["moblin keep bridge", "moblin keep", True, lambda state: any([
            oos_has_flippers(state, player),
            oos_can_jump_4_wide_liquid(state, player)
        ])],
        ["moblin keep", "moblin keep chest", False, lambda state: oos_has_bracelet(state, player)],
        ["moblin keep", "sunken city", False, None],

        ["natzu river bank", "goron mountain entrance", True, lambda state: oos_can_swim(state, player, True)],

        # Access to natzu deku is companion specific
        ["natzu deku", "deku secret", False, lambda state: all([
            oos_can_use_seeds(state, player),
            oos_has_ember_seeds(state, player),
            oos_has_scent_seeds(state, player),
            oos_has_pegasus_seeds(state, player),
            oos_has_gale_seeds(state, player),
            oos_has_mystery_seeds(state, player)
        ])],

        # SUNKEN CITY ############################################################################################

        ["sunken city", "sunken city tree", False, lambda state: all([
            any([
                oos_has_feather(state, player),
                oos_has_flippers(state, player),
                oos_can_summon_dimitri(state, player),
                oos_is_default_season(state, player, "SUNKEN_CITY", SEASON_WINTER)
            ]),
            oos_can_harvest_tree(state, player, True)
        ])],

        ["sunken city", "sunken city dimitri", False, lambda state: any([
            oos_can_summon_dimitri(state, player),
            all([
                oos_has_bombs(state, player),
                any([
                    oos_has_feather(state, player),
                    oos_has_flippers(state, player),
                    oos_is_default_season(state, player, "SUNKEN_CITY", SEASON_WINTER)
                ])
            ])
        ])],

        ["sunken city", "ingo trade", False, lambda state: all([
            any([
                oos_has_feather(state, player),
                oos_has_flippers(state, player),
                oos_can_summon_dimitri(state, player),
                oos_is_default_season(state, player, "SUNKEN_CITY", SEASON_WINTER)
            ]),
            any([
                state.has("Goron Vase", player),
                oos_self_locking_item(state, player, "ingo trade", "Goron Vase")
            ])
        ])],

        ["sunken city", "syrup trade", False, lambda state: all([
            oos_season_in_sunken_city(state, player, SEASON_WINTER),
            state.has("Mushroom", player)
        ])],
        ["syrup trade", "syrup shop", False, lambda state: oos_has_rupees_for_shop(state, player, "syrupShop")],

        # Use Dimitri to get the tree seeds, using dimitri to get seeds being medium difficulty
        ["sunken city dimitri", "sunken city tree", False, lambda state: all([
            oos_option_medium_logic(state, player),
            oos_can_use_seeds(state, player)
        ])],

        ["sunken city dimitri", "master diver's challenge", False, lambda state: all([
            oos_has_sword(state, player, False),
            any([
                oos_has_feather(state, player),
                oos_has_flippers(state, player)
            ])
        ])],

        ["sunken city dimitri", "master diver's reward", False, lambda state: any([
            state.has("Master's Plaque", player),
            oos_self_locking_item(state, player, "master diver's reward", "Master's Plaque")
        ])],
        ["sunken city dimitri", "chest in master diver's cave", False, None],

        ["sunken city", "sunken city, summer cave", False, lambda state: all([
            oos_season_in_sunken_city(state, player, SEASON_SUMMER),
            oos_has_flippers(state, player),
            oos_can_break_bush(state, player, False, True)
        ])],

        ["sunken city", "diver secret", False, lambda state: all([
            oos_has_flippers(state, player),
            any([
                oos_option_medium_logic(state, player),
                oos_has_sword(state, player),
                oos_has_fools_ore(state, player),
            ])
        ])],

        ["mount cucco", "sunken city", False, lambda state: oos_has_flippers(state, player)],
        ["sunken city", "mount cucco", False, lambda state: all([
            oos_has_flippers(state, player),
            oos_season_in_sunken_city(state, player, SEASON_SUMMER)
        ])],

        # MT. CUCCO / GORON MOUNTAINS ##############################################################################

        ["mount cucco", "mt. cucco portal", True, None],

        ["mount cucco", "rightmost rooster ledge", False, lambda state: all([
            any([  # to reach the rooster
                all([
                    oos_season_in_mt_cucco(state, player, SEASON_SPRING),
                    any([
                        oos_can_break_flowers(state, player),
                        state.has("Spring Banana", player),
                    ])
                ]),
                oos_option_hard_logic(state, player)
            ]),
            oos_has_bracelet(state, player),  # to grab the rooster
        ])],

        ["rightmost rooster ledge", "mt. cucco, platform cave", False, None],
        ["rightmost rooster ledge", "spring banana tree", False, lambda state: all([
            oos_has_feather(state, player),
            oos_season_in_mt_cucco(state, player, SEASON_SPRING),
            any([  # can harvest tree
                oos_has_sword(state, player),
                oos_has_fools_ore(state, player)
            ])
        ])],

        ["mount cucco", "mt. cucco, talon's cave entrance", False, lambda state: \
            oos_season_in_mt_cucco(state, player, SEASON_SPRING)],
        ["mt. cucco, talon's cave entrance", "mount cucco", False, None],

        ["mt. cucco, talon's cave entrance", "talon trade", False, lambda state: all([
            state.has("Megaphone", player),
            any([
                not oos_is_default_season(state, player, "SUNKEN_CITY", SEASON_WINTER),
                oos_can_remove_season(state, player, SEASON_WINTER)
            ])
        ])],

        ["mt. cucco, talon's cave entrance", "mt. cucco heart piece", False, None],

        ["mt. cucco, talon's cave entrance", "diving spot outside D4", False, lambda state: all([
            oos_has_flippers(state, player),
            any([
                not oos_is_default_season(state, player, "SUNKEN_CITY", SEASON_WINTER),
                oos_can_remove_season(state, player, SEASON_WINTER)
            ])
        ])],

        ["mt. cucco, talon's cave entrance", "dragon keyhole", False, lambda state: all([
            oos_has_winter(state, player),  # to reach cave
            oos_has_feather(state, player),  # to jump in cave
            oos_has_bracelet(state, player)  # to grab the rooster
        ])],

        ["dragon keyhole", "d4 entrance", False, lambda state: all([
            state.has("Dragon Key", player),
            oos_has_summer(state, player)
        ])],
        ["d4 entrance", "mt. cucco, talon's cave entrance", False, None],

        ["mount cucco", "goron mountain, across pits", False, lambda state: any([
            state.has("Spring Banana", player),
            oos_can_jump_4_wide_pit(state, player),
        ])],

        ["mount cucco", "goron blocked cave entrance", False, lambda state: any([
            oos_can_remove_snow(state, player, False),
            state.has("Spring Banana", player)
        ])],
        ["goron blocked cave entrance", "mount cucco", False, lambda state: \
            oos_can_remove_snow(state, player, False)],

        ["goron blocked cave entrance", "maple encounter", False, lambda state: oos_can_meet_maple(state, player)],

        ["goron blocked cave entrance", "goron mountain", True, lambda state: oos_has_bracelet(state, player)],

        ["goron mountain", "maple encounter", False, lambda state: oos_can_meet_maple(state, player)],

        ["goron blocked cave entrance", "goron's gift", False, lambda state: oos_can_remove_rockslide(state, player, False)],

        ["goron mountain", "biggoron trade", False, lambda state: all([
            oos_can_jump_1_wide_liquid(state, player, False),
            any([
                state.has("Lava Soup", player),
                all([
                    oos_self_locking_item(state, player, "biggoron trade", "Lava Soup"),
                    not state.multiworld.worlds[player].options.secret_locations
                ])
            ])
        ])],

        ["goron mountain", "chest in goron mountain", False, lambda state: all([
            oos_can_jump_3_wide_liquid(state, player),
            any([
                oos_has_bombs(state, player),
                all([  # Bombchu can only destroy the second block, so we need to use cape to jump around the first
                    oos_option_medium_logic(state, player),
                    oos_has_bombchus(state, player, 5),
                    oos_can_use_pegasus_seeds(state, player)
                ]),
            ])
        ])],
        ["goron mountain", "old man in goron mountain", False, lambda state: \
            oos_can_use_ember_seeds(state, player, False)],

        ["goron mountain entrance", "goron mountain", False, lambda state: any([
            oos_has_flippers(state, player),
            oos_can_jump_4_wide_liquid(state, player),
            oos_has_tight_switch_hook(state, player)
        ])],

        ["goron mountain", "goron mountain entrance", False, lambda state: any([
            oos_has_flippers(state, player),
            oos_can_jump_4_wide_liquid(state, player),
            all([
                # You can't see the other side from this point
                oos_option_medium_logic(state, player),
                oos_has_switch_hook(state, player)
            ])
        ])],

        ["goron mountain entrance", "temple remains lower stump", True, lambda state: \
            oos_can_jump_3_wide_pit(state, player)],

        # TARM RUINS ###############################################################################################

        ["spool swamp north", "tarm ruins", False, lambda state: oos_has_required_jewels(state, player)],
        ["tarm ruins", "spool swamp north", False, None],

        ["tarm ruins", "lost woods top statue", False, lambda state: all([
            any([
                oos_season_in_lost_woods(state, player, SEASON_SUMMER),
                all([
                    oos_season_in_lost_woods(state, player, SEASON_AUTUMN),
                    oos_option_medium_logic(state, player),
                    oos_has_magic_boomerang(state, player),
                    any([
                        oos_can_jump_1_wide_pit(state, player, False),
                        oos_option_hard_logic(state, player)
                    ])
                ])
            ]),
            oos_season_in_lost_woods(state, player, SEASON_WINTER),
            oos_can_remove_season(state, player, SEASON_WINTER)
        ])],
        ["lost woods top statue", "lost woods stump", False, lambda state: all([
            # Winter has to be in inventory to be here, it allows crossing the water
            oos_has_autumn(state, player),
            oos_can_break_mushroom(state, player, False)
        ])],
        ["lost woods top statue", "lost woods deku", False, lambda state: all([
            oos_has_autumn(state, player),
            any([
                oos_can_jump_2_wide_liquid(state, player),
                oos_can_swim(state, player, False)
            ]),
            oos_can_break_mushroom(state, player, False),
            oos_has_shield(state, player)
        ])],

        ["lost woods stump", "maple encounter", False, lambda state: oos_can_meet_maple(state, player)],
        ["lost woods stump", "tarm ruins", False, lambda state: all([
            oos_season_in_lost_woods(state, player, SEASON_AUTUMN),
            oos_can_break_mushroom(state, player, False),
            oos_has_winter(state, player),
            state.multiworld.worlds[player].options.tarm_gate_required_jewels.value == 0
        ])],
        ["lost woods stump", "lost woods top statue", False, lambda state: all([
            oos_season_in_lost_woods(state, player, SEASON_AUTUMN),
            oos_has_season(state, player, SEASON_WINTER),
            any([
                oos_has_season(state, player, SEASON_SUMMER),
                all([
                    oos_has_season(state, player, SEASON_AUTUMN),
                    oos_option_medium_logic(state, player),
                    oos_has_magic_boomerang(state, player),
                    any([
                        oos_can_jump_1_wide_pit(state, player, False),
                        oos_option_hard_logic(state, player)
                    ])
                ])
            ])
        ])],
        ["lost woods stump", "lost woods phonograph", False, lambda state: all([
            any([
                oos_can_remove_snow(state, player, False),
                oos_can_remove_season(state, player, SEASON_WINTER),
            ]),
            oos_can_use_ember_seeds(state, player, False),
            state.has("Phonograph", player)
        ])],

        ["lost woods stump", "lost woods", False, lambda state: oos_can_reach_lost_woods_pedestal(state, player)],
        # When coming back from the eyeglass lake
        ["lost woods", "lost woods stump", False, None],
        # To allow reaching the deku if base season is autumn
        ["lost woods", "lost woods deku", False, lambda state: all([
            oos_season_in_tarm_ruins(state, player, SEASON_AUTUMN),
            state.can_reach_region("lost woods top statue", player),
            any([
                # A bit tight and diagonal, above water
                oos_can_jump_3_wide_pit(state, player),
                oos_can_swim(state, player, False)
            ]),
            oos_can_break_mushroom(state, player, False),
            oos_has_shield(state, player)
        ])],
        # special case for getting to d6 using default season
        ["lost woods", "d6 sector", False, lambda state: all([
            oos_can_complete_lost_woods_main_sequence(state, player, True),
            oos_option_medium_logic(state, player)
        ])],
        ["lost woods stump", "d6 sector", False, lambda state: oos_can_complete_lost_woods_main_sequence(state, player)],
        ["d6 sector", "lost woods stump", False, None],
        # special case for getting to pedestal using default season
        ["d6 sector", "lost woods", False, lambda state: all([
            oos_can_reach_lost_woods_pedestal(state, player, True),
            oos_option_medium_logic(state, player)
        ])],

        ["d6 sector", "maple encounter", False, lambda state: oos_can_meet_maple(state, player)],

        ["d6 sector", "tarm ruins tree", False, lambda state: oos_can_harvest_tree(state, player, False)],
        ["d6 sector", "tarm ruins, under tree", False, lambda state: all([
            oos_season_in_tarm_ruins(state, player, SEASON_AUTUMN),
            oos_can_break_mushroom(state, player, False),
            oos_can_use_ember_seeds(state, player, False)
        ])],

        ["d6 sector", "d6 entrance", False, lambda state: all([
            oos_season_in_tarm_ruins(state, player, SEASON_WINTER),
            any([
                oos_has_shovel(state, player),
                oos_can_use_ember_seeds(state, player, False),
                all([
                    oos_can_reach_rooster_adventure(state, player),
                    oos_roosters(state, player)["d6"][0] > 0
                ])
            ]),
            oos_season_in_tarm_ruins(state, player, SEASON_SPRING),
            oos_can_break_flowers(state, player)
        ])],
        ["d6 sector", "old man near d6", False, lambda state: all([
            oos_season_in_tarm_ruins(state, player, SEASON_WINTER),
            oos_can_use_ember_seeds(state, player, False),
            any([
                all([
                    oos_season_in_tarm_ruins(state, player, SEASON_SPRING),
                    oos_can_break_flowers(state, player)
                ]),
                all([
                    oos_can_reach_rooster_adventure(state, player),
                    oos_roosters(state, player)["d6"][1] > 0
                ])
            ])
        ])],
        # When coming from D6 entrance, the pillar needs to be broken during spring to be able to go backwards
        ["d6 entrance", "d6 sector", False, lambda state: all([
            oos_is_default_season(state, player, "TARM_RUINS", SEASON_SPRING),
            oos_can_break_flowers(state, player)
        ])],

        # SAMASA DESERT ######################################################################################

        ["suburbs", "samasa desert", False, lambda state: state.has("_met_pirates", player)],
        ["samasa desert", "samasa desert pit", False, lambda state: oos_has_bracelet(state, player)],
        ["samasa desert", "samasa desert chest", False, lambda state: oos_has_flippers(state, player)],
        ["samasa desert", "samasa desert scrub", False, lambda state: \
            oos_has_rupees_for_shop(state, player, "samasaCaveScrub")],

        # TEMPLE REMAINS ####################################################################################

        ["temple remains lower stump", "maple encounter", False, lambda state: oos_can_meet_maple(state, player)],

        ["temple remains lower stump", "temple remains upper stump", False, lambda state: all([
            oos_has_feather(state, player),  # Require feather in case volcano has erupted
            oos_can_break_bush(state, player, False, False),
            any([
                state.has("_triggered_volcano", player),  # Volcano rule
                all([  # Winter rule
                    oos_season_in_temple_remains(state, player, SEASON_WINTER),
                    oos_can_remove_snow(state, player, False),
                    oos_can_jump_6_wide_pit(state, player)
                ]),
                all([  # Summer rule
                    oos_season_in_temple_remains(state, player, SEASON_SUMMER),
                    oos_can_jump_6_wide_pit(state, player)
                ]),
                all([  # Spring rule
                    oos_season_in_temple_remains(state, player, SEASON_SPRING),
                    oos_can_break_flowers(state, player),
                    oos_can_jump_6_wide_pit(state, player)
                ]),
                oos_season_in_temple_remains(state, player, SEASON_AUTUMN)  # Autumn rule
            ])
        ])],
        ["temple remains upper stump", "temple remains lower stump", False, lambda state: all([
            oos_has_feather(state, player),  # Require feather in case volcano has erupted
            any([
                state.has("_triggered_volcano", player),  # Volcano rule
                oos_season_in_temple_remains(state, player, SEASON_WINTER),  # Winter rule
                all([  # Summer rule
                    oos_season_in_temple_remains(state, player, SEASON_SUMMER),
                    oos_can_break_bush(state, player, False, False),
                    oos_can_jump_6_wide_pit(state, player)
                ]),
                all([  # Spring rule
                    oos_season_in_temple_remains(state, player, SEASON_SPRING),
                    oos_can_break_flowers(state, player),
                    oos_can_break_bush(state, player, False, False),
                    oos_can_jump_6_wide_pit(state, player)
                ]),
                all([  # Autumn rule
                    oos_season_in_temple_remains(state, player, SEASON_AUTUMN),
                    oos_can_break_bush(state, player)
                ])
            ])
        ])],

        ["temple remains lower stump", "temple remains lower portal access", False, lambda state: all([
            state.has("_triggered_volcano", player),
            oos_has_feather(state, player)
        ])],

        ["temple remains upper stump", "temple remains lower portal access", False, lambda state: all([
            oos_has_feather(state, player),
            any([
                oos_has_winter(state, player),
                state.has("_triggered_volcano", player),
                all([
                    # You can only reach the portal from here with the default Winter if you made the zipper jump first
                    # Otherwise you would have turned it Autumn first
                    oos_season_in_temple_remains(state, player, SEASON_WINTER),
                    oos_can_remove_snow(state, player, False),
                    oos_can_break_bush(state, player, False),
                    oos_can_jump_6_wide_pit(state, player)
                ])
            ])
        ])],

        ["temple remains lower portal access", "temple remains lower portal", True, None],

        # There is an added ledge in rando that enables jumping from the portal down to the stump, whatever the season is
        ["temple remains lower portal", "temple remains lower stump", False, None],

        ["temple remains lower stump", "temple remains heart piece", False, lambda state: all([
            state.has("_triggered_volcano", player),
            oos_can_jump_2_wide_liquid(state, player),
            oos_can_remove_rockslide(state, player, False),
        ])],

        ["temple remains lower stump", "temple remains upper portal", False, lambda state: all([
            state.has("_triggered_volcano", player),
            oos_season_in_temple_remains(state, player, SEASON_SUMMER),
            oos_can_jump_2_wide_liquid(state, player),
            any([
                oos_has_magnet_gloves(state, player),
                oos_can_jump_6_wide_pit(state, player)
            ])
        ])],
        ["temple remains upper portal", "temple remains lower stump", False, lambda state: all([
            state.has("_triggered_volcano", player),
            oos_can_jump_1_wide_liquid(state, player, False)
        ])],

        ["temple remains upper portal", "temple remains upper stump", False, lambda state: \
            oos_can_jump_1_wide_pit(state, player, False)],

        ["temple remains upper portal", "temple remains lower portal access", False, lambda state: all([
            oos_has_feather(state, player),  # Require feather in case volcano has erupted
            any([
                state.has("_triggered_volcano", player),
                oos_is_default_season(state, player, "TEMPLE_REMAINS", SEASON_WINTER)
            ])
        ])],

        # ONOX CASTLE #############################################################################################

        ["maku tree", "maku seed", False, lambda state: oos_has_essences_for_maku_seed(state, player)],
        ["maku tree", "maku tree, 3 essences", False, lambda state: oos_has_essences(state, player, 3)],
        ["maku tree", "maku tree, 5 essences", False, lambda state: oos_has_essences(state, player, 5)],
        ["maku tree", "maku tree, 7 essences", False, lambda state: oos_has_essences(state, player, 7)],

        ["north horon", "d9 entrance", False, lambda state: state.has("Maku Seed", player)],
        ["d9 entrance", "onox beaten", False, lambda state: all([
            oos_can_kill_armored_enemy(state, player, True, True),
            oos_can_kill_facade(state, player),
            oos_has_sword(state, player, False),
            oos_has_feather(state, player),
            any([
                oos_option_hard_logic(state, player),
                oos_has_rod(state, player)
            ])
        ])],

        ["onox beaten", "ganon beaten", False, lambda state: any([
            all([
                # casual rules
                oos_has_noble_sword(state, player),
                oos_has_seed_thrower(state, player),
                oos_can_use_ember_seeds(state, player, False),
                oos_can_use_mystery_seeds(state, player)
            ]),
            all([
                oos_option_medium_logic(state, player),
                oos_has_sword(state, player, False),
                any([
                    # all seeds damage Twinrova phase 2
                    oos_has_seed_thrower(state, player),
                    all([
                        oos_option_hard_logic(state, player),
                        oos_can_use_seeds(state, player),
                        # satchel can't use pegasus to damage, but all others work
                        any([
                            oos_has_ember_seeds(state, player),
                            oos_has_mystery_seeds(state, player),
                            oos_has_scent_seeds(state, player),
                            oos_has_gale_seeds(state, player)
                        ])
                    ])
                ])
            ])
        ])],

        # GOLDEN BEASTS #############################################################################################

        ["d0 entrance", "golden darknut", False, lambda state: all([
            any([
                oos_is_default_season(state, player, "WESTERN_COAST", SEASON_SPRING),
                all([
                    oos_season_in_western_coast(state, player, SEASON_SPRING),
                    state.has("Pirate's Bell", player),
                    state.has("_met_pirates", player),
                ])
            ]),
            any([
                oos_has_sword(state, player),
                oos_has_fools_ore(state, player),
                oos_can_summon_dimitri(state, player)
            ])
        ])],
        ["lost woods top statue", "golden lynel", False, lambda state: any([
            oos_has_sword(state, player),
            oos_has_fools_ore(state, player)
        ])],
        ["lost woods stump", "golden lynel", False, lambda state: all([
            # We can assume coming from d6 or pedestal otherwise rule above applies
            oos_season_in_lost_woods(state, player, SEASON_AUTUMN),
            oos_can_break_mushroom(state, player, False),
            oos_has_winter(state, player),
            any([
                oos_has_sword(state, player),
                oos_has_fools_ore(state, player)
            ])
        ])],
        ["d2 entrance", "golden moblin", False, lambda state: all([
            oos_season_in_central_woods_of_winter(state, player, SEASON_AUTUMN),
            any([
                oos_has_sword(state, player),
                oos_has_fools_ore(state, player),
                # Moblin has the interesting property of being one-shottable using an ember seed
                all([
                    oos_option_medium_logic(state, player),
                    oos_can_use_ember_seeds(state, player, True)
                ]),
                oos_can_summon_dimitri(state, player)
            ])
        ])],
        ["spool swamp south (summer)", "golden octorok", False, lambda state: any([
            oos_has_sword(state, player),
            oos_has_fools_ore(state, player),
            oos_can_summon_dimitri(state, player)
        ])],

        # GASHA TREES #############################################################################################

        ["horon village", "horon gasha spot", False, None],
        ["impa's house", "impa gasha spot", False, lambda state: oos_can_break_bush(state, player, True, True)],
        ["suburbs", "suburbs gasha spot", False, lambda state: oos_can_break_bush(state, player, True, True)],
        ["ghastly stump", "holodrum plain gasha spot", False, lambda state: all([
            oos_can_break_bush(state, player, True, False),  # Zoras make the bombchus not viable
            oos_has_shovel(state, player),
        ])],
        ["d1 island", "holodrum plain island gasha spot", False, lambda state: all([
            oos_can_swim(state, player, True),
            any([
                oos_can_break_bush(state, player, False, False),
                oos_can_summon_dimitri(state, player),  # Only Dimitri can be brought here
            ]),
        ])],
        ["floodgate keyhole", "spool swamp north gasha spot", False, lambda state: oos_has_bracelet(state, player)],
        ["spool swamp south near gasha spot", "spool swamp south gasha spot", False, lambda state: oos_has_bracelet(state, player)],
        ["sunken city", "sunken city gasha spot", False, lambda state: all([
            oos_season_in_sunken_city(state, player, SEASON_SUMMER),
            oos_can_swim(state, player, False),
            oos_can_break_bush(state, player, False, False),  # Technically doable by positioning link with a sword
        ])],
        ["sunken city dimitri", "sunken city gasha spot", False, None],
        ["goron mountain entrance", "goron mountain left gasha spot", False, lambda state: oos_has_shovel(state, player)],
        ["goron mountain entrance", "goron mountain right gasha spot", False, lambda state: oos_has_bracelet(state, player)],
        ["d5 stump", "eyeglass lake gasha spot", False, lambda state: all([
            oos_has_shovel(state, player),
            oos_can_break_bush(state, player, True, True),
        ])],
        ["mount cucco", "mt cucco gasha spot", False, lambda state: all([
            oos_season_in_mt_cucco(state, player, SEASON_AUTUMN),
            oos_can_break_mushroom(state, player, False),
        ])],
        ["d6 sector", "tarm ruins gasha spot", False, lambda state: oos_has_shovel(state, player)],
        ["samasa desert", "samasa desert gasha spot", False, None],
        ["western coast after ship", "western coast gasha spot", False, None],
        ["north horon", "onox gasha spot", False, lambda state: oos_has_shovel(state, player)],
    ]
    if options.animal_companion == "ricky":
        holodrum_logic.extend([
            ["natzu west", "natzu west (ricky)", True, None],
            ["natzu west (ricky)", "natzu east (ricky)", True, lambda state: oos_can_summon_ricky(state, player)],
            ["natzu east (ricky)", "sunken city", True, None],
            ["natzu east (ricky)", "moblin keep bridge", False, None],
            ["natzu east (ricky)", "natzu river bank", True, lambda state: oos_can_summon_ricky(state, player)],
            ["natzu east (ricky)", "natzu deku", False, lambda state: oos_can_break_bush(state, player, True)],
        ])
    elif options.animal_companion == "dimitri":
        holodrum_logic.extend([
            ["natzu west", "natzu west (dimitri)", True, None],
            ["natzu west (dimitri)", "natzu east (dimitri)", True, lambda state: oos_can_swim(state, player, True)],
            ["natzu east (dimitri)", "sunken city", True, lambda state: oos_can_jump_1_wide_pit(state, player, False)],
            ["natzu east (dimitri)", "natzu region, across water", False, lambda state: oos_can_jump_5_wide_liquid(state, player)],
            ["natzu east (dimitri)", "moblin keep bridge", False, lambda state: any([
                oos_can_summon_dimitri(state, player),
                all([
                    oos_option_medium_logic(state, player),
                    oos_has_flippers(state, player),
                    state.has("Swimmer's Ring", player)
                ])
            ])],
            ["natzu east (dimitri)", "natzu river bank", True, None],
            ["natzu west (dimitri)", "natzu deku", False, lambda state: oos_can_summon_dimitri(state, player)],
            ["sunken city", "moblin keep", False, lambda state: oos_can_dimitri_clip(state, player)],
            ["moblin keep bridge", "natzu east (dimitri)", False, lambda state: oos_can_swim(state, player, True)],
        ])
    elif options.animal_companion == "moosh":
        holodrum_logic.extend([
            ["natzu west", "natzu west (moosh)", True, lambda state: oos_is_companion_moosh(state, player)],
            ["natzu west (moosh)", "natzu east (moosh)", True, lambda state: any([
                oos_can_summon_moosh(state, player),
                all([
                    oos_option_medium_logic(state, player),
                    oos_can_break_bush(state, player, True),
                    oos_can_jump_3_wide_pit(state, player)
                ])
            ])],
            ["natzu east (moosh)", "sunken city", True, lambda state: any([
                oos_can_summon_moosh(state, player),
                oos_can_jump_3_wide_liquid(state, player)  # Not a liquid, but it's a diagonal jump so that's the same
            ])],
            ["natzu east (moosh)", "moblin keep bridge", False, lambda state: any([
                oos_can_summon_moosh(state, player),
                all([
                    oos_can_break_bush(state, player),
                    oos_can_jump_3_wide_pit(state, player)
                ])
            ])],
            ["natzu east (moosh)", "natzu river bank", True, lambda state: oos_is_companion_moosh(state, player)],
            ["natzu west (moosh)", "natzu deku", False, lambda state: any([
                oos_can_summon_moosh(state, player),
                oos_can_jump_4_wide_liquid(state, player),
                all([
                    oos_can_jump_4_wide_pit(state, player),
                    oos_can_break_bush(state, player)
                ])
            ])],
        ])

    if options.logic_difficulty == OracleOfSeasonsLogicDifficulty.option_hell:
        # Rooster adventure
        holodrum_logic.extend([
            ["d4 entrance", "dragon keyhole", False, lambda state: all([
                # Rule specifically to get to the dragon keyhole from a side entrance, only useful for rooster's adventure
                oos_is_default_season(state, player, "SUNKEN_CITY", SEASON_WINTER),  # to reach cave
                oos_has_feather(state, player),  # to jump in cave
                oos_has_bracelet(state, player)  # to grab the rooster
            ])],

            # Item assumptions for the rest of that logic :
            # Bracelet
            # Feather
            ["dragon keyhole", "rooster adventure", False, lambda state: all([
                oos_has_gale_seeds(state, player),
                oos_has_satchel(state, player),
                any([
                    oos_has_shovel(state, player),
                    state.has("Spring Banana", player)
                ])
            ])],

            ["rooster adventure", "goron mountain entrance", False, lambda state: oos_roosters(state, player)["cucco mountain"][0] != -1],
            ["rooster adventure", "moblin keep", False, lambda state: any([
                all([
                    oos_roosters(state, player)["sunken"][1] > 0,
                    oos_is_companion_ricky(state, player)
                ]),
                all([
                    oos_roosters(state, player)["horon"][1] > 0,
                    any([
                        oos_has_flute(state, player),
                        all([
                            oos_is_companion_moosh(state, player),
                            oos_can_jump_3_wide_pit(state, player)
                        ])
                    ])
                ])
            ])],

            ["rooster adventure", "sunken city", False, lambda state: oos_roosters(state, player)["sunken"][0] >= 0],
            ["rooster adventure", "sunken city gasha spot", False, lambda state: all([
                oos_roosters(state, player)["sunken"][2] > 0,
                oos_season_in_sunken_city(state, player, SEASON_WINTER)
            ])],
            ["rooster adventure", "syrup trade", False, lambda state: all([
                oos_roosters(state, player)["sunken"][2] > 0,
                state.has("Mushroom", player)
            ])],

            ["rooster adventure", "suburbs", False, lambda state: oos_roosters(state, player)["suburbs"][0] >= 0],
            ["rooster adventure", "eastern suburbs spring cave", False, lambda state: all([
                oos_roosters(state, player)["suburbs"][2] > 0,
                oos_season_in_eastern_suburbs(state, player, SEASON_SPRING),
                any([
                    oos_has_magnet_gloves(state, player),
                    oos_can_jump_3_wide_pit(state, player)
                ])
            ])],
            ["rooster adventure", "windmill heart piece", False, lambda state: oos_roosters(state, player)["suburbs"][1] > 0],
            ["rooster adventure", "samasa desert chest", False, lambda state: all([
                oos_roosters(state, player)["suburbs"][1] > 0,
                state.has("_met_pirates", player),
            ])],

            ["rooster adventure", "moblin road", False, lambda state: oos_roosters(state, player)["moblin road"][0] >= 0],
            ["rooster adventure", "holly's house", False, lambda state: oos_roosters(state, player)["moblin road"][1] > 0],

            ["rooster adventure", "horon heart piece", False, lambda state: oos_roosters(state, player)["horon"][1] > 0],
            ["rooster adventure", "graveyard heart piece", False, lambda state: all([
                oos_roosters(state, player)["horon"][1] > 0,
                state.has("_met_pirates", player),
                state.has("Pirate's Bell", player),
                oos_is_default_season(state, player, "WESTERN_COAST", SEASON_SUMMER)
            ])],

            ["rooster adventure", "spool swamp north", False, lambda state: oos_roosters(state, player)["swamp"][0] >= 0],
            ["rooster adventure", "lost woods deku", False, lambda state: all([
                oos_roosters(state, player)["swamp"][1] > 0,
                oos_has_required_jewels(state, player),
                any([
                    oos_season_in_lost_woods(state, player, SEASON_SUMMER),
                    state.can_reach_region("lost woods top statue", player)
                ])
            ])],
            ["rooster adventure", "spool swamp cave", False, lambda state: any([
                all([
                    oos_can_swim(state, player, True),
                    oos_roosters(state, player)["horon"][0] > 0
                ]),
                all([
                    # We can assume jump 3 holes here, coming from the north
                    state.has("Floodgate Key", player),
                    any([
                        not oos_is_default_season(state, player, "SPOOL_SWAMP", SEASON_SPRING),
                        oos_can_remove_season(state, player, SEASON_SPRING)
                    ]),
                    oos_roosters(state, player)["swamp"][0] > 0
                ])
            ])],

            ["rooster adventure", "temple remains upper stump", False, lambda state: all([
                oos_can_jump_3_wide_pit(state, player),
                oos_roosters(state, player)["cucco mountain"][0] > 0,
                any([
                    # autumn doesn't matter since regular logic already covers that case
                    oos_season_in_temple_remains(state, player, SEASON_SUMMER),
                    all([
                        oos_season_in_temple_remains(state, player, SEASON_WINTER),
                        oos_has_shovel(state, player)
                    ]),
                    all([
                        oos_season_in_temple_remains(state, player, SEASON_SPRING),
                        oos_can_break_flowers(state, player)
                    ])
                ])
            ])],
            ["rooster adventure", "temple remains upper portal", False, lambda state: all([
                state.has("_triggered_volcano", player),
                oos_can_jump_3_wide_pit(state, player),
                oos_roosters(state, player)["cucco mountain"][1] > 0,
                any([
                    oos_has_magnet_gloves(state, player),
                    oos_can_jump_6_wide_pit(state, player)
                ])
            ])],
        ])

    for i in range(options.deterministic_gasha_locations):
        holodrum_logic.append(gasha_connections[i])

    return holodrum_logic
