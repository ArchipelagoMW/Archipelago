from .LogicPredicates import *


def make_overworld_logic(player: int):
    return [
        
        # FOREST OF TIME
        #######################################
        ["Menu", "forest of time", False, None],
        ["Menu", "maple trade", False, lambda state: all([
            ooa_can_kill_normal_enemy(state, player, True),
            state.has("Touching Book", player)
        ])],
        ["forest of time", "starting item", False, None],
        ["forest of time", "nayru's house", False, None],

        # LYNNA CITY
        #######################################
        ["forest of time", "lynna city", True, lambda state: ooa_can_break_bush(state, player)],
        ["lynna city", "south lynna tree", False, lambda state: ooa_can_harvest_tree(state, player, True)],
        ["lynna city", "lynna city chest", False, lambda state: ooa_can_use_ember_seeds(state, player, False)],
        ["lynna village", "lynna city chest", False, lambda state: ooa_can_go_back_to_present(state, player)],
        ["lynna city", "lynna shop", False, lambda state: ooa_has_rupees(state, player, 400)],
        ["lynna village", "hidden shop", False, lambda state: all([
            ooa_can_go_back_to_present(state, player),
            ooa_has_rupees(state, player, 400)
        ])],
        
        ["lynna city", "mayor plen's house", False, lambda state: ooa_has_long_hook(state, player)],
        ["lynna city", "lynna city comedian trade", False, lambda state: state.has("Cheesy Mustache", player)],
        ["lynna city", "mamamu yan trade", False, lambda state: state.has("Doggie Mask", player)],
        ["lynna city", "vasu's gift", False, None],

        # LYNNA VILLAGE
        #######################################
        ["lynna city", "lynna village", True, None],
        ["forest of time", "lynna village", False, lambda state: ooa_can_open_portal(state, player)],
        ["lynna village", "gasha farmer", False, None],
        ["lynna village", "black tower worker", False, None],
        ["lynna village", "black tower heartpiece", False, lambda state: ooa_can_remove_dirt(state, player, False)],
        ["lynna village", "advance shop", False, lambda state: ooa_has_rupees(state, player, 400)],
        ["lynna village", "lynna shooting gallery", False, lambda state: ooa_has_sword(state, player)],
        ["lynna village", "ambi's palace tree", False, lambda state: ooa_can_harvest_tree(state, player, False)],
        ["lynna village", "ambi's palace chest", False, lambda state: any([
            all([
                ooa_option_hard_logic(state, player),
                ooa_can_use_scent_seeds_for_smell(state, player),
                ooa_can_use_pegasus_seeds(state, player)
            ]),
            all([
                ooa_can_break_bush(state, player),
                ooa_can_dive(state, player)
            ]),
            ooa_can_switch_past_and_present(state, player)
        ])],
        ["ambi's palace chest", "rescue nayru", False, lambda state: all([
            ooa_has_switch_hook(state, player),
            ooa_can_use_mystery_seeds(state, player),
            any([
                ooa_has_sword(state, player),
                ooa_can_punch(state, player)
            ])
        ])],
        ["lynna village", "postman trade", False, lambda state: state.has("Poe Clock", player)],
        ["lynna village", "toilet hand trade", False, lambda state: state.has("Stationary", player)],
        ["lynna village", "sad boi trade", False, lambda state: state.has("Funny Joke", player)],
        ["lynna village", "rafton's raft", False, lambda state: all([
            state.has("Cheval Rope", player),
            state.has("Island Chart", player)
        ])],
        ["rafton's raft", "rafton trade", False, lambda state: state.has("Magic Oar", player)],
        ["lynna village", "d0 entrance", True, lambda state: ooa_can_remove_dirt(state, player, False)],

        # MAKU TREE
        #######################################
        ["d0 exit", "maku tree", True, lambda state: ooa_can_kill_normal_enemy(state, player)],
        ["rescue nayru", "maku tree", False, None],
        ["maku tree", "maku seed", False, lambda state: ooa_has_essences_for_maku_seed(state, player)],
        ["maku seed", "veran beaten", False, lambda state: all([
            ooa_can_use_mystery_seeds(state, player),
            ooa_has_switch_hook(state, player),
            ooa_has_bombs(state, player),
            any([
                ooa_has_sword(state, player),
                ooa_can_punch(state, player)
            ])
        ])],
        ["veran beaten", "ganon beaten", False, lambda state: any([
            all([
                # casual rules
                ooa_has_noble_sword(state, player),
                ooa_has_seedshooter(state, player),
                ooa_can_use_ember_seeds(state, player, False),
                ooa_can_use_mystery_seeds(state, player)
            ]),
            all([
                ooa_option_medium_logic(state, player),
                ooa_has_sword(state, player, False),
                any([
                    # all seeds damage Twinrova phase 2
                    ooa_has_seedshooter(state, player),
                    all([
                        ooa_option_hard_logic(state, player),
                        ooa_can_use_seeds(state, player),
                        # satchel can't use pegasus to damage, but all others work
                        any([
                            ooa_has_ember_seeds(state, player),
                            ooa_has_mystery_seeds(state, player),
                            ooa_has_scent_seeds(state, player),
                            ooa_has_gale_seeds(state, player)
                        ])
                    ])
                ])
            ])
        ])],
        # TODO : Check Essence 3, 5, 7

        # SHORE PRESENT
        #######################################
        ["forest of time", "shore present", True,  lambda state: state.has("Ricky's Gloves", player)],
        ["lynna city", "shore present", True, lambda state: any([
            ooa_can_swim_deepwater(state, player, True),
            ooa_has_bracelet(state, player),
            ooa_can_go_back_to_present(state, player),
            all([
                ooa_can_break_bush(state, player, True),
                ooa_can_jump_1_wide_pit(state, player, True)
            ]),
        ])],
        ["shore present", "south shore dirt", False, lambda state: ooa_can_remove_dirt(state, player, True)],
        ["shore present", "balloon guy's gift", False,  lambda state: all([
            any([
                ooa_has_seedshooter(state, player),
                ooa_can_summon_ricky(state, player),
                state.has("Ricky's Gloves", player),
                ooa_can_go_back_to_present(state, player), #lynna city and lynna village are connected, so no need to create a different logic                    
            ]),
            ooa_can_break_tingle_balloon(state, player)
        ])],
        ["balloon guy's gift", "balloon guy's upgrade", False, lambda state: ooa_has_seed_kind_count(state, player, 3)],
        
        # YOLL GRAVEYARD
        #######################################
        ["forest of time", "yoll graveyard", True, lambda state: ooa_can_use_ember_seeds(state, player, False)],
        ["yoll graveyard", "cheval's grave", False, lambda state: any([
            ooa_can_kill_normal_enemy(state, player, True),
            ooa_can_jump_3_wide_pit(state, player, True)
        ])],
        ["cheval's grave", "cheval's test", False, lambda state: all([
            any([
                ooa_has_feather(state, player),
                ooa_can_swim(state, player, False),                    
            ]),
            ooa_has_bracelet(state, player)
        ])],
        ["cheval's grave", "cheval's invention", False, lambda state: ooa_can_swim(state, player, False)],
        ["yoll graveyard", "grave under tree", False, lambda state: ooa_can_use_ember_seeds(state, player, False)],
        ["yoll graveyard", "yoll graveyard heartpiece", False, lambda state: ooa_has_bracelet(state, player)],
        ["yoll graveyard", "graveyard door", False, lambda state: state.has("Graveyard Key", player)],
        ["graveyard door", "syrup shop", False, lambda state: all([
            any([
                ooa_can_jump_2_wide_liquid(state, player),
                ooa_can_swim(state, player, True),
                ooa_has_long_hook(state, player)                    
            ]),
            ooa_has_rupees(state, player, 400)
        ])],
        ["graveyard door", "graveyard poe trade", False, lambda state: ooa_has_bracelet(state, player)],
        ["graveyard door", "d1 entrance", False, None],

        # FAIRIES' WOODS
        #######################################
        ["lynna city", "fairies' woods", True, lambda state: any([
            ooa_can_swim(state, player, True),
            ooa_has_bracelet(state, player),
            ooa_can_switch_past_and_present(state, player),
            all([ # it's possible to switch hook the octorok through the boulder to enter fairies' woods. 
                ooa_option_hard_logic(state, player),
                ooa_has_switch_hook(state, player)
            ])
        ])],
        ["fairies' woods", "fairies' woods chest", False, lambda state: any([
            ooa_can_jump_1_wide_pit(state, player, True),
            ooa_has_switch_hook(state, player)
        ])],
        ["deku forest", "fairies' woods chest", False, lambda state: ooa_can_go_back_to_present(state, player)],
        ["fairies' woods", "happy mask salesman trade", False, lambda state: state.has("Tasty Meat", player)],
        ["deku forest", "d2 present entrance", False, lambda state: ooa_can_go_back_to_present(state, player)],

        # DEKU FOREST
        #######################################
        ["lynna village", "deku forest", True, lambda state: any([
            ooa_has_bracelet(state, player),
            ooa_can_switch_past_and_present(state, player),
        ])],
        ["deku forest", "deku forest cave east", False, None], # You need the bracelet or the ages song to access deku forest. Either way, you can access that easily.
        ["deku forest", "deku forest heartpiece", False, lambda state: ooa_can_use_ember_seeds(state, player, False)],
        ["deku forest", "restoration wall heartpiece", False, lambda state: ooa_can_jump_1_wide_pit(state, player, False)], # Still need feather inside the cave
        ["deku forest", "deku forest cave west", False, lambda state: all([
            ooa_has_bracelet(state, player),                    
            any([
                ooa_can_jump_1_wide_pit(state, player, False),
                ooa_has_switch_hook(state, player),
                ooa_can_use_ember_seeds(state, player, False),        
                ooa_can_warp_using_gale_seeds(state, player),   
                ooa_can_switch_past_and_present(state, player),          
            ])
        ])],
        ["deku forest", "deku forest tree", False, lambda state: all([
            ooa_can_harvest_tree(state, player, False),
            any([
                ooa_can_jump_1_wide_pit(state, player, False),
                ooa_has_switch_hook(state, player),
                ooa_can_use_ember_seeds(state, player, False),        
                ooa_can_warp_using_gale_seeds(state, player),   
                ooa_can_switch_past_and_present(state, player),          
            ])
        ])],
        ["deku forest", "deku forest soldier", False, lambda state: all([
            ooa_can_use_mystery_seeds(state, player)
        ])],
        ["deku forest", "d2 past entrance", False, lambda state: ooa_has_bombs(state, player)],

        # CRESCENT PAST
        #######################################
        ["lynna village", "crescent past west", True, lambda state: ooa_can_swim_deepwater(state, player, False)],
        ["rafton's raft", "crescent past west", False, None],
        ["crescent present west", "crescent past west", False, lambda state: ooa_can_go_back_to_present(state, player)],
        ["crescent past west", "tokay crystal cave", False, lambda state: all([
            any([
                ooa_has_shovel(state, player),
                ooa_can_break_crystal(state, player),                    
            ]),
            ooa_can_jump_1_wide_pit(state, player, False)
        ])],
        ["lynna village", "hidden tokay cave", True, lambda state: ooa_can_dive(state, player)],
        ["crescent past west", "crescent past east", False, lambda state: ooa_can_break_bush(state, player)],
        ["crescent present west", "crescent past east", False, lambda state: ooa_can_go_back_to_present(state, player)],
        ["crescent past east", "tokay bomb cave", False, lambda state: all([
            ooa_has_bracelet(state, player),
            ooa_has_bombs(state, player),
        ])],
        ["crescent past east", "wild tokay game", False, lambda state: all([
            ooa_has_bracelet(state, player),
            ooa_has_bombs(state, player),
        ])],
        ["crescent past east", "tokay pot cave", False, lambda state: ooa_has_long_hook(state, player)],
        ["crescent past east", "tokay market 1", False, lambda state: ooa_has_mystery_seeds(state, player)],
        ["crescent past east", "tokay market 2", False, lambda state: ooa_has_scent_seeds(state, player)],

        # CRESCENT PRESENT
        #######################################
        ["lynna city", "crescent present west", True, lambda state: ooa_can_swim_deepwater(state, player, True)],
        ["crescent past west", "crescent present west", False, lambda state: any([
            ooa_can_go_back_to_present(state, player),
            all([
                ooa_has_shovel(state, player),
                ooa_can_open_portal(state, player)
            ])
        ])],
        ["crescent present west", "d3 entrance", False, None],
        ["lynna city", "under crescent island", True, lambda state: ooa_can_dive(state, player)],
        ["crescent present east", "tokay chef trade", False, lambda state: state.has("Stink Bag", player)],
        ["crescent past west", "crescent island tree", False, lambda state: all([
            any([
                ooa_has_bracelet(state, player),
                ooa_can_switch_past_and_present(state, player),
            ]),
            state.has("Scent Seedling", player),
            ooa_can_harvest_tree(state, player, False),
            any([
                ooa_can_open_portal(state, player),
                all([
                    # Can get the warp point by swimming under crescent island, but that's pretty unintuitive, so it's hard logic only. (medium maybe ?)
                    ooa_option_hard_logic(state, player),
                    ooa_can_dive(state, player),
                    ooa_can_warp_using_gale_seeds(state, player),
                ])
            ]),
        ])],
        ["crescent past east", "crescent present east", True, lambda state: ooa_can_open_portal(state, player)],
        ["crescent past west", "crescent present east", False, lambda state: ooa_can_go_back_to_present(state, player)],

        # NUUN
        #######################################
        ["fairies' woods", "nuun", True, lambda state: all([
            ooa_can_use_ember_seeds(state, player, False),
            ooa_has_seedshooter(state, player),
        ])],
        ["lynna village", "nuun", True, lambda state: ooa_can_go_back_to_present(state, player)],
        ["nuun", "nuun (ricky)", True, lambda state: ooa_is_companion_ricky(state, player)],
        ["nuun", "nuun (moosh)", True, lambda state: ooa_is_companion_moosh(state, player)],
        ["nuun", "nuun (dimitri)", True, lambda state: ooa_is_companion_dimitri(state, player)],

        ["nuun (ricky)", "nuun highlands cave", False, lambda state: any([
            ooa_can_summon_ricky(state, player),
            ooa_can_go_back_to_present(state, player),
        ])],
        ["nuun (moosh)", "nuun highlands cave", False, lambda state: any([
            ooa_can_summon_moosh(state, player),
            ooa_can_go_back_to_present(state, player),
            all([
                ooa_can_break_bush(state, player),
                ooa_can_jump_3_wide_pit(state, player, False),
            ])
        ])],
        ["nuun (dimitri)", "nuun highlands cave", False, lambda state: ooa_can_summon_dimitri(state, player)],


        # SYMMETRY CITY PRESENT
        #######################################
        ["nuun", "symmetry present", True, lambda state: any([
            ooa_can_go_back_to_present(state, player),
            ooa_has_flute(state, player),
            all([
                ooa_is_companion_moosh(state, player),
                ooa_can_break_bush(state, player),
                ooa_can_jump_3_wide_pit(state, player, False),
                ooa_option_hard_logic(state, player),
            ])
        ])],
        ["symmetry present", "symmetry city tree", False, lambda state: ooa_can_harvest_tree(state, player, False)],
        ["symmetry present", "d4 entrance", False, lambda state: all([
            state.has("Tuni Nut", player),
            any([
                ooa_can_go_back_to_present(state, player),
                ooa_can_open_portal(state, player)
            ])
        ])],

        # SYMMETRY CITY PAST
        #######################################
        ["symmetry present", "symmetry past", False,  lambda state: any([
            ooa_can_switch_past_and_present(state, player),
            all([
                ooa_can_open_portal(state, player),
                ooa_can_break_bush(state, player, False)
            ])
        ])],

        ["symmetry past", "symmetry city brother", False, None],
        ["symmetry past", "symmetry middle man trade", False, lambda state: state.has("Dumbbell", player)],
        ["symmetry past", "symmetry city heartpiece", False, lambda state: ooa_can_go_back_to_present(state, player)],
        ["symmetry past", "tokkey's composition", False, lambda state: ooa_can_swim(state, player, False)],

        ["symmetry past", "talus peaks", False, lambda state: all([
            ooa_can_go_back_to_present(state, player),
            ooa_has_bracelet(state, player)
        ])],

        
        # TALUS PEAK & RESTORATION WALL
        #######################################
        ["talus peaks", "bomb fairy", False, lambda state: ooa_has_bombs(state, player)],

        ["talus peaks", "restoration wall", True, lambda state: any([
            ooa_can_swim(state, player, False),
            ooa_can_jump_3_wide_liquid(state, player)
        ])],
        ["restoration wall", "talus peaks chest", False, None],
        ["fairies' woods", "restoration wall", True, lambda state: ooa_can_switch_past_and_present(state, player)],
        ["restoration wall", "patch", True, lambda state: any([
            ooa_has_sword(state, player),
            all([
                ooa_option_medium_logic(state, player),
                any([
                    ooa_has_shield(state, player),
                    ooa_has_boomerang(state, player),
                    ooa_has_switch_hook(state, player),
                ])
            ]),
            all([
                ooa_option_hard_logic(state, player),
                any([
                    ooa_has_scent_seeds(state, player),
                    ooa_has_shovel(state, player),
                ])
            ])
        ])],
        ["patch", "patch tuni nut ceremony", False, lambda state: state.has("Cracked Tuni Nut", player)],
        ["patch", "patch broken sword ceremony", False, lambda state: state.has("Broken Sword", player)],

        # ROLLING RIDGE WEST
        #######################################
        ["lynna village", "old zora trade", False, lambda state: all([
            any([
                ooa_can_switch_past_and_present(state, player),
                all([
                    ooa_can_jump_1_wide_pit(state, player, False),
                    any([
                        ooa_can_jump_4_wide_pit(state, player, False),
                        ooa_has_switch_hook(state, player),
                        ooa_can_swim_deepwater(state, player, False),
                    ]),
                ]),
            ]),
            state.has("Sea Ukulele", player),
        ])],
        ["lynna village", "ridge west past base", True, lambda state: all([
            any([
                ooa_can_switch_past_and_present(state, player),
                ooa_can_jump_1_wide_pit(state, player, False),
            ]),
            any([
                ooa_can_jump_4_wide_pit(state, player, False),
                ooa_has_switch_hook(state, player),
            ]),
        ])],
        ["ridge west past base", "goron elder", False, lambda state: state.has("Bomb Flower", player)],
        ["ridge west present", "ridge west past", False, lambda state: all([
            ooa_can_open_portal(state, player),
            ooa_has_bracelet(state, player)
        ])],
        ["ridge west present", "ridge west heartpiece", False, lambda state: ooa_has_bombs(state, player)],
        ["goron elder", "ridge west past", False, None],
        ["ridge west past", "ridge west past base", False, None],
        ["ridge west past", "ridge west tree", False, lambda state: ooa_can_harvest_tree(state, player, False)],
        #########
        ["ridge west past", "ridge west present", False, lambda state: ooa_can_go_back_to_present(state, player)],
        ["ridge upper present", "ridge west present", False, None],
        ["ridge west present", "goron's hiding place", False, lambda state: ooa_has_bombs(state, player)],
        ["ridge west present", "ridge base chest", False, None],
        ["ridge west present", "ridge west cave", False, None],
        ["ridge west present", "under moblin keep", False, lambda state: all([
            ooa_can_jump_1_wide_pit(state,player, False),
            ooa_can_swim(state, player, False),
        ])],
        ["ridge west present", "defeat great moblin", False, lambda state: all([
            ooa_can_use_pegasus_seeds(state,player),
            ooa_has_bracelet(state, player),
        ])],
        
        # ROLLING UPPER
        #######################################
        ["defeat great moblin", "ridge upper present", False, lambda state: ooa_can_jump_2_wide_pit(state, player, False)],
        ["ridge upper past", "ridge upper present", False, lambda state: ooa_can_go_back_to_present(state, player)],
        ["ridge upper present", "d5 entrance", False, lambda state: state.has("Crown Key", player)],
        ["ridge mid present", "ridge NE cave present", True, None],
        ["ridge base present", "ridge upper present", False, lambda state: ooa_can_jump_3_wide_pit(state, player, False)],
        ["ridge base past west", "ridge upper past", True, lambda state: all([
            ooa_has_switch_hook(state, player),
        ])],
        #####
        ["ridge upper present", "ridge upper past", False, lambda state: ooa_can_switch_past_and_present(state, player)],
        ["ridge upper present", "treasure hunting goron", False, lambda state: all([
            ooa_has_bombs(state, player),
            ooa_has_ember_seeds(state, player),
            ooa_can_open_portal(state, player),
            ooa_has_bracelet(state, player)
        ])],
        ["ridge upper past", "bomb goron head", False, lambda state: ooa_has_bombs(state, player)],
        ["ridge upper past", "ridge upper heartpiece", False, lambda state: all([
            ooa_can_go_back_to_present(state, player),
            ooa_can_break_bush(state, player)
        ])],
        
        # ROLLING BASE
        #######################################
        ["ridge upper present", "ridge base present", False, None],
        ["ridge base past east", "ridge base present", False, lambda state: ooa_can_go_back_to_present(state, player)],
        ["ridge base past west", "ridge base present", False, lambda state: ooa_can_go_back_to_present(state, player)],
        ["ridge base present", "d6 present entrance", False, lambda state: state.has("Old Mermaid Key", player)],
        ["ridge base present", "pool in d6 entrance", False, lambda state: ooa_can_dive(state, player)],
        ["ridge base present", "trade rock brisket", False, lambda state: state.has("Rock Brisket", player) and state.has("Brother Emblem", player)],
        ["ridge base present", "first goron dance", False, lambda state: ooa_has_rupees(state, player, 10)],
        #########
        ["ridge base present", "ridge base past west", False, lambda state: any([
            ooa_can_switch_past_and_present(state, player),
            all([
                ooa_can_open_portal(state, player),
                ooa_can_break_bush(state, player)
            ])
        ])],
        ["lynna village", "ridge base past west", True, lambda state: all([
            ooa_can_swim_deepwater(state, player, False),
            any([
                ooa_can_jump_1_wide_pit(state, player, False),
                ooa_can_switch_past_and_present(state, player)
            ])
        ])],
        ["ridge base past west", "ridge base bomb past", False, lambda state: ooa_has_bombs(state, player)],
        ["ridge base past west", "ridge diamonds past", False, lambda state: ooa_has_switch_hook(state, player)],
        ["ridge base past west", "d6 past entrance", False, lambda state: all([
            ooa_can_swim(state, player, False),
            state.has("Mermaid Key", player)
        ])],
        #########
        ["ridge base past west", "ridge base past east", True, lambda state: ooa_can_swim(state, player, False)],
        ["ridge base past east", "first goron dance", False, lambda state: ooa_has_rupees(state, player, 10)],
        ["ridge base past east", "goron dance, with letter", False, lambda state: ooa_has_rupees(state, player, 10) and state.has("Letter of Introduction", player)],
        ["ridge base past east", "trade goron vase", False, lambda state: state.has("Goron Vase", player) and state.has("Brother Emblem", player)],
        #["ridge base past east", "rolling ridge past old man", False, lambda state: ooa_can_use_ember_seeds(state, player, False)],
        
        # ROLLING MID
        #######################################
        ["ridge base present", "ridge mid present", True, lambda state: all([
            state.has("Brother Emblem", player),
            any([
                ooa_has_switch_hook(state, player),
                ooa_can_jump_3_wide_pit(state, player, False),
            ])
        ])],
        ["ridge mid past", "ridge mid present", False, lambda state: ooa_can_go_back_to_present(state, player)],
        ["ridge mid present", "target carts", True, lambda state: all([
            ooa_has_switch_hook(state, player),
            state.has("_access_cart", player),
        ])],
        ["goron shooting gallery", "target carts", False, lambda state: ooa_can_go_back_to_present(state, player)],
        ["target carts", "target carts 1", True, lambda state: all([
            ooa_has_seedshooter(state, player),
            any([
                ooa_has_ember_seeds(state, player),
                ooa_has_mystery_seeds(state, player),
                ooa_has_pegasus_seeds(state, player),
                ooa_has_scent_seeds(state, player),
            ])
        ])],
        ["target carts 1", "target carts 2", True, None],
        ["ridge mid present", "big bang game", True, lambda state: state.has("Goronade", player)],
        ["ridge mid present", "goron diamond cave", True, lambda state: any([
            ooa_has_switch_hook(state, player),
            ooa_can_jump_3_wide_pit(state, player, False),
        ])],
        #########
        ["ridge mid present", "ridge mid past", False, lambda state: ooa_can_switch_past_and_present(state, player)],
        ["ridge base past east", "ridge mid past", False, lambda state: all([
            state.has("Brother Emblem", player),
            ooa_can_jump_2_wide_pit(state, player, False),
        ])],
        ["ridge mid past", "ridge move vine seed", False, lambda state: ooa_has_switch_hook(state, player)],
        ["target carts", "goron shooting gallery", False, lambda state: all([
            ooa_can_open_portal(state, player),
            ooa_has_bracelet(state, player),
        ])],
        ["ridge mid present", "goron shooting gallery", False, lambda state: ooa_can_switch_past_and_present(state, player)],
        ["goron shooting gallery", "goron shooting gallery price", False, lambda state: ooa_has_sword(state, player)],
        ["ridge mid past", "ridge east tree", False, lambda state: all([
            ooa_can_harvest_tree(state, player, False),
            ooa_can_warp_using_gale_seeds(state, player),
        ])],
        ["goron shooting gallery", "ridge east tree", False, lambda state: ooa_can_harvest_tree(state, player, False)],
        ["ridge mid past", "trade lava juice", False, lambda state: state.has("Lava Juice", player)],
        ["ridge mid past", "ridge bush cave", False, lambda state: ooa_has_switch_hook(state, player)],
        


        # ZORA VILLAGE
        #######################################
        ["lynna city", "zora village", True, lambda state: all([
            ooa_can_dive(state, player),
            ooa_has_switch_hook(state, player),
            ooa_can_switch_past_and_present(state, player),
        ])],
        ["zora village", "zora village tree", False, lambda state: ooa_can_harvest_tree(state, player, False)],
        ["zora village", "zora village present", False, None],
        ["zora village", "zora palace chest", False, None],
        ["zora village", "zora NW cave", False, lambda state: all([
            ooa_has_bombs(state, player),
            ooa_has_glove(state, player),
        ])],
        ["zora village", "fairies' coast chest", False, None],
        ["zora village", "library present", False, lambda state: state.has("Library Key", player)],
        ["library present", "library past", False, lambda state: state.has("Book of Seals", player)],
        ["zora village", "zora seas chest", False, lambda state: state.has("Fairy Powder", player)],
        ["zora village", "zora king gift", False, lambda state: all([
            state.has("King Zora's Potion", player)
        ])],
        ["zora king gift", "d7 entrance", False, lambda state: all([
            state.has("Fairy Powder", player),
        ])],
        ["zora village", "fisher's island cave", False, lambda state: ooa_has_long_hook(state, player)],
        ["zora village", "zora's reward", False, lambda state:  state.has("_finished_d7", player),],
        
        # SEA OF NO RETURN
        #######################################
        ["lynna city", "piratian captain", False, lambda state: all([
            ooa_can_dive(state, player),
            state.has("Zora Scale", player),
        ])],
        ["piratian captain", "sea of storms past", False, None],
        ["crescent past west", "d8 entrance", False, lambda state: all([
            state.has("Tokay Eyeball", player),
            ooa_can_break_pot(state, player),
            ooa_can_dive(state, player),
            ooa_has_bombs(state, player),
            ooa_can_jump_1_wide_pit(state, player, False),
            ooa_can_kill_normal_enemy(state, player),
            any([
                # Finding the road in the dark room
                ooa_has_cane(state, player),
                all([
                    ooa_option_medium_logic(state, player),
                    any([
                        ooa_can_kill_normal_enemy(state, player, False),
                        ooa_can_push_enemy(state, player),
                        ooa_has_boomerang(state, player),
                        ooa_has_switch_hook(state, player),
                        ooa_can_use_pegasus_seeds_for_stun(state, player),
                    ])
                ])
            ]),
        ])],
        ["d8 entrance", "sea of no return", False, lambda state: ooa_has_glove(state, player)],

    ]
