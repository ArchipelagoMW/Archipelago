from .LogicPredicates import *


def make_d0_logic(player: int):
    return [
        ["enter d0", "d0 key chest", False, lambda state: ooa_can_kill_normal_enemy(state, player)],
        ["enter d0", "d0 behind the door", True, lambda state: ooa_has_small_keys(state, player, 0, 1)],
        ["d0 behind the door", "d0 basement", False, None],
        ["d0 behind the door", "maku path heartpiece", False, lambda state: ooa_can_kill_normal_enemy(state, player)],
        #["d0 behind the door", "d0 heart piece", False, None],
        ["d0 behind the door", "d0 exit", False, lambda state: ooa_can_kill_normal_enemy(state, player)],
        ["d0 exit", "d0 behind the door", False, None],
    ]

def make_d1_logic(player: int):
    return [
        # 0 keys
        ["enter d1", "d1 east terrace", False, lambda state: ooa_can_kill_normal_enemy(state, player, True)],
        ["d1 east terrace", "d1 ghini drop", False, None],
        ["d1 east terrace", "d1 crossroad", False, None],
        ["d1 east terrace", "d1 crystal room", False, lambda state: all([
            ooa_can_use_ember_seeds(state, player, False),
            ooa_can_break_crystal(state, player)
        ])],
        ["enter d1", "d1 west terrace", False, lambda state: ooa_can_break_pot(state, player)],
        ["enter d1", "d1 pot chest", False, lambda state: ooa_can_break_pot(state, player)],

        # 2 keys => Risk of softlock if we require only one key. 
        ["d1 ghini drop", "d1 wide room", False, lambda state: ooa_has_small_keys(state, player, 1, 2)],
        ["d1 wide room", "d1 two-button chest", False, None],
        ["d1 wide room", "d1 one-button chest", False, None],
        ["d1 wide room", "d1 boss", False, lambda state: all([
            ooa_has_boss_key(state, player, 1),
            ooa_has_bracelet(state, player),
            ooa_generic_boss_and_miniboss_kill(state, player),
        ])],

        # potentially 3 keys w/ vanilla route
        ["d1 wide room", "d1 U-room", False, lambda state: all([
            ooa_can_break_bush(state, player),
            ooa_generic_boss_and_miniboss_kill(state, player),
            ooa_has_small_keys(state, player, 1, 3)
        ])],
        ["d1 west terrace", "d1 U-room", False, None],
        ["d1 U-room", "d1 basement", False, lambda state: ooa_can_use_ember_seeds(state, player, True)],
    ]


def make_d2_logic(player: int):
    return [
        # 0 keys
        ["enter d2", "d2 bombed terrace", False, lambda state: all([
            ooa_can_kill_spiked_beetle(state, player),
            ooa_has_bombs(state, player)
        ])],
        ["enter d2", "d2 moblin drop", False, lambda state: all([
            ooa_can_kill_spiked_beetle(state, player),
            ooa_can_kill_normal_enemy(state, player)
        ])],

        # potentially 2 keys w/ vanilla route 
        ["enter d2", "d2 miniboss arena", False, lambda state: any([
                all([
                    ooa_has_small_keys(state, player, 2, 2),
                    ooa_can_kill_normal_enemy(state, player, True, True)
                ]),
                all([
                    ooa_can_jump_2_wide_pit(state, player, False),
                    ooa_can_kill_spiked_beetle(state, player)
                ])
            ])
        ],
        # The key door doesn't need you to kill the beetles to go past it
        # So come in with keys, and do the 2-wide pit jump from the other side
        # To get to these items without being able to kill the spiked beetles.
        # You also don't need to kill swoop for these, as you can just fall down one of the holes they make.
        # (only relevant in keysanity)
        ["d2 miniboss arena", "d2 bombed terrace", False, lambda state: all([
            ooa_can_jump_2_wide_pit(state, player, False),
            ooa_has_bombs(state, player)
        ])],
        ["d2 miniboss arena", "d2 moblin drop", False, lambda state: all([
            ooa_can_jump_2_wide_pit(state, player, False),
            ooa_can_kill_normal_enemy(state, player)
        ])],
        ["d2 miniboss arena", "d2 basement", False, lambda state: ooa_generic_boss_and_miniboss_kill(state, player)],
        ["d2 basement", "d2 thwomp tunnel", False, None],
        ["d2 basement", "d2 thwomp shelf", False, lambda state: any([
            ooa_can_jump_1_wide_pit(state, player, False),
            all([
                ooa_option_hard_logic(state, player),
                ooa_has_cane(state, player),
                any([
                    ooa_has_bombs(state, player),
                    ooa_can_use_pegasus_seeds(state, player)
                ])
            ])
        ])],
        ["d2 basement", "d2 basement drop", False, lambda state: ooa_has_feather(state, player)],
        ["d2 basement", "d2 basement chest", False, lambda state: all([
            ooa_has_feather(state, player),
            ooa_can_trigger_lever_from_minecart(state,player),
            ooa_has_bombs(state, player),
            ooa_can_kill_normal_enemy(state, player)
        ])],

        # 3 keys
        ["d2 basement", "d2 moblin platform", False, lambda state: all([
            ooa_has_feather(state, player),
            ooa_has_small_keys(state, player, 2, 3),
        ])],
        ["d2 moblin platform", "d2 statue puzzle", False, lambda state: any([
            ooa_has_bracelet(state, player),
            ooa_has_cane(state, player),
            all([
                # push moblin into doorway, stand on button, use switch hook
                ooa_option_hard_logic(state, player),
                ooa_can_push_enemy(state, player),
                ooa_has_switch_hook(state, player)
            ])
        ])],

        # 4 keys
        ["enter d2", "d2 rope room", False, lambda state: all([
            ooa_can_kill_normal_enemy(state, player, True, True),
            ooa_has_small_keys(state, player, 2, 4),
        ])],
        ["enter d2", "d2 ladder chest", False, lambda state: all([
            ooa_can_kill_normal_enemy(state, player, True),
            ooa_has_small_keys(state, player, 2, 4),
            ooa_has_bombs(state, player)
        ])],

        # 5 keys
        ["d2 statue puzzle", "d2 color room", False, lambda state: ooa_has_small_keys(state, player, 2, 5)],
        ["d2 color room", "d2 boss", False, lambda state: all([
            ooa_has_boss_key(state, player, 2),
            any([
                ooa_has_bombs(state, player),
                ooa_option_hard_logic(state, player)
            ])
        ])],
    ]


def make_d3_logic(player: int):
    return [
        
        # 0 keys
        ["enter d3", "d3 pols voice chest", False, lambda state: ooa_has_bombs(state, player)],
        ["d3 six-blocs drop", "d3 pols voice chest", False, lambda state: all([
            ooa_can_break_bush(state, player),
            ooa_can_kill_pols_voice(state, player)
        ])],

        ["enter d3", "d3 1F spinner", False, lambda state: any([
            ooa_can_kill_moldorm(state, player, True),
            ooa_has_bracelet(state, player)
        ])],
        ["d3 1F spinner", "d3 S crystal", False, None],
        ["d3 1F spinner", "d3 E crystal", False, lambda state: ooa_has_bombs(state, player)],
        ["d3 E crystal", "d3 statue drop", False, lambda state: ooa_has_bombs(state, player)],

        # 1 key
        ["enter d3", "d3 pitfall", False, lambda state: ooa_has_small_keys(state, player, 3, 1)],
        # TODO : d3 seeds from bridge room: [enter d3, d3 small key, seed item, or: [sword, fool's ore, bombs]]
        ["d3 pitfall", "d3 W crystal", False, lambda state: ooa_can_kill_pols_voice(state, player, True)],
        # you can clip into the blocks enough to hit this crystal with switch hook
        ["d3 pitfall", "d3 N crystal", False, lambda state: any([
            ooa_has_seedshooter(state, player),
            ooa_has_boomerang(state, player),
            all([
                ooa_option_hard_logic(state, player),
                ooa_has_switch_hook(state, player)
            ])
        ])],
        ["d3 pitfall", "d3 armos drop", False, lambda state: ooa_can_kill_armos(state, player)],
        ["d3 W crystal", "d3 six-blocs drop", False, lambda state: all([
            any([ # kill moldorm
                ooa_has_bombs(state, player),
                all([
                    ooa_has_scent_seeds(state, player),
                    ooa_has_seedshooter(state, player),
                ]),
                ooa_has_switch_hook(state, player),
                all([
                    ooa_has_cane(state, player),
                    ooa_has_bracelet(state, player),
                    ooa_option_medium_logic(state, player),
                ])
            ]),
            any([ # hit orb
                ooa_has_bombs(state, player),
                ooa_has_seedshooter(state, player),
                all([
                    ooa_option_hard_logic(state, player),
                    any([
                        ooa_has_switch_hook(state, player),
                        ooa_has_boomerang(state, player),
                    ])
                ])
            ])
        ])],
        ["d3 six-blocs drop", "d3 conveyor belt room", False, lambda state: ooa_can_kill_armos(state, player)],
        ["d3 pitfall", "d3 B1F spinner", False, lambda state: all([
            state.has("_d3_S_crystal", player),
            state.has("_d3_E_crystal", player),
            state.has("_d3_N_crystal", player),
            state.has("_d3_W_crystal", player),
        ])],
        ["d3 B1F spinner", "d3 crossroad", False, None],
        ["d3 B1F spinner", "d3 torch chest", False, lambda state: all([
            ooa_can_use_ember_seeds(state, player, True),
            ooa_has_seedshooter(state, player),
        ])],
        # Have the ability to traverse the first switch room from the bottom to the
        # door. TODO: HSS + seeds + feather?
        ["d3 pitfall", "d3 crossing bridge room 1", True, lambda state: any([
            ooa_has_seedshooter(state, player),
            ooa_can_jump_3_wide_pit(state, player, False),
            ooa_can_toss_ring(state, player),
            all([
                ooa_option_hard_logic(state, player),
                ooa_has_boomerang(state, player)
            ])
        ])],
        ["d3 crossing bridge room 1", "d3 between two bridge room", True, lambda state: ooa_has_small_keys(state, player, 3, 4)],
        # Have the ability to traverse the second switch room from the bottom to the
        # boss door area (TODO: boomerang logic should be hard?)
        ["d3 between two bridge room", "d3 crossing bridge room 2", True, lambda state: any([
            ooa_has_seedshooter(state, player),
            ooa_can_jump_4_wide_pit(state, player, False),
            all([
                ooa_option_hard_logic(state, player),
                ooa_has_feather(state, player),
                any([
                    ooa_has_sword(state, player),
                    all([
                        ooa_has_bombs(state, player),
                        any([
                            ooa_can_use_ember_seeds(state, player, True),
                            ooa_can_use_scent_seeds_offensively(state, player)
                        ]),
                    ]),
                ]),
                any([
                    ooa_can_jump_3_wide_pit(state, player, False),
                    ooa_has_switch_hook(state, player),
                    all([
                        ooa_has_bracelet(state, player),
                        ooa_has_small_keys(state, player, 3, 4)
                    ])
                ])
            ])
        ])],
        ["d3 crossing bridge room 1", "d3 bridge chest", False, None],
        # TODO ["d3 crossing bridge room 1", "d3 scent seed bush", False, lambda state: ooa_can_harvest_regrowing_bush(state, player)],
        ["d3 post-subterror", "d3 between two bridge room", True, lambda state: all([
            ooa_can_jump_2_wide_pit(state, player, False)
        ])],
        ["d3 B1F spinner", "d3 B1F east", False, lambda state: all([
            # No need to go through the key door, you can use the warp, which should always be accessible since the spinner in down
            ooa_generic_boss_and_miniboss_kill(state, player), 
            ooa_has_shovel(state, player),
            any([
                ooa_has_seedshooter(state, player),
                all([
                    ooa_option_hard_logic(state, player), # Make it medium ?
                    ooa_has_sword(state, player), # spin slash through corner
                ])
            ])
        ])],
        ["d3 crossing bridge room 2", "d3 post-subterror", False, None],
        ["d3 B1F spinner", "d3 post-subterror", False, lambda state: all([
            ooa_generic_boss_and_miniboss_kill(state, player), 
            ooa_has_shovel(state, player),
        ])],

        ["d3 post-subterror", "d3 moldorm drop", False, lambda state: ooa_can_kill_moldorm(state, player, True)],
        ["d3 crossing bridge room 2", "d3 boss", False, lambda state: all([
            ooa_has_boss_key(state, player, 3),
            any([
                ooa_has_seedshooter(state, player),
                all([
                    ooa_option_hard_logic(state, player),
                    ooa_can_use_seeds(state, player)
                ])
            ]),
            any([
                ooa_has_ember_seeds(state, player),
                ooa_has_scent_seeds(state, player),
            ])
        ])],

        # 3 keys
        ["enter d3", "d3 bush beetle room", False, lambda state: all([
            ooa_can_kill_normal_enemy(state, player, True),
            ooa_has_small_keys(state, player, 3, 3),
        ])],

        # 4 keys
        ["d3 bush beetle room", "d3 mimic room", False, lambda state: all([
            ooa_can_kill_normal_enemy(state, player, False),
            ooa_has_small_keys(state, player, 3, 4),
        ])],
    ]

def make_d4_logic(player: int):
    return [
        ["enter d4", "d4 first chest", False, lambda state: all([
            any([
                ooa_can_kill_stalfos(state, player),
                ooa_can_push_enemy(state, player)
            ]),
            any([
                ooa_has_switch_hook(state, player),
                ooa_can_jump_1_wide_liquid(state, player, False)
            ]),
        ])],
         ["d4 first chest", "d4 cube chest", False, lambda state: ooa_has_feather(state, player)],

        # No checks require 1 key since cape was introduced (can now open last keydoor
        # before the others, effectively adding +1 key requirement to most checks)

        # 1 keys
        ["enter d4", "d4 minecart A", False, lambda state: all([
            ooa_has_small_keys(state, player, 4, 1),
            ooa_can_jump_1_wide_liquid(state, player, False)
        ])],
        ["d4 minecart A", "d4 first crystal switch", False, lambda state: any([
            ooa_has_seedshooter(state, player),
            all([
                ooa_option_hard_logic(state, player),
                ooa_has_boomerang(state, player)
            ])
        ])],
        ["d4 minecart A", "d4 minecart chest", False, lambda state: ooa_can_trigger_lever(state, player)],

        # 2 keys
        ["d4 minecart A", "d4 minecart B", False, lambda state: all([
            ooa_can_trigger_lever_from_minecart(state, player),
            ooa_has_bracelet(state, player),
            ooa_can_kill_stalfos(state, player),
            ooa_has_small_keys(state, player, 4, 2)
        ])],
        ["d4 minecart B", "d4 second crystal switch", False, lambda state: any([
            ooa_has_seedshooter(state, player),
            all([
                ooa_option_hard_logic(state, player),
                ooa_has_boomerang(state, player)
            ])
        ])],

        # 3 keys
        ["d4 minecart B", "d4 minecart C", False, lambda state: ooa_has_small_keys(state, player, 4, 3)],
        ["d4 minecart C", "d4 color tile drop", False, lambda state: any([
            ooa_can_kill_normal_using_seedshooter(state, player),
            all([
                ooa_option_medium_logic(state, player),
                ooa_has_sword(state, player),
            ]),
        ])],

        # 4 keys
        ["d4 color tile drop", "d4 minecart D", False, lambda state: ooa_has_small_keys(state, player, 4, 4)],

        ["d4 minecart D", "d4 small floor puzzle", False, lambda state: all([
            ooa_generic_boss_and_miniboss_kill(state, player),
            ooa_has_bombs(state, player)
        ])],
        ["d4 minecart D", "d4 large floor puzzle", False, lambda state: any([
            all([
                ooa_can_jump_1_wide_liquid(state, player, False),
                ooa_has_switch_hook(state, player),
            ]),
            all([
                # We can jump the gap between minecart A and the bridge above,
                # But it needs that the cariot is not there anymore, 
                # so you need to kill the miniboss first
                # Of course it's hard logic.
                ooa_option_hard_logic(state, player),
                ooa_generic_boss_and_miniboss_kill(state, player),
                ooa_can_jump_3_wide_liquid(state, player),
                ooa_has_cane(state, player),
                ooa_has_noble_sword(state, player),
            ])
        ])],
        
        ["d4 large floor puzzle", "d4 boss", False, lambda state: all([
            ooa_has_boss_key(state, player, 4),
            ooa_has_switch_hook(state, player),
            any([
                ooa_has_sword(state, player),
                #(ooa_option_medium_logic(state, player) and ooa_has_bombs(state, player, 4)),
                ooa_can_punch(state, player),
                ooa_has_boomerang(state, player)
            ])
        ])],
        
        # 5 keys 
        ["d4 large floor puzzle", "d4 lava pot chest", False, lambda state: all([
            ooa_has_small_keys(state, player, 4, 5),
            ooa_has_bracelet(state, player),
            ooa_has_switch_hook(state, player),
        ])],
    ]

def make_d5_logic(player: int):
    return [


        # 0 keys
        ["enter d5", "d5 switch A", False, lambda state: all([
            ooa_can_kill_normal_enemy(state, player),
            any([
                ooa_can_trigger_switch(state, player),
                all([
                    ooa_option_hard_logic(state, player), # Not hard to reproduce but clearly not instinctive to find.
                    ooa_has_bracelet(state, player),
                ])
            ])
        ])],
        ["d5 switch A", "d5 blue peg chest", False, None],
        ["d5 switch A", "d5 dark room", False, lambda state: all([
            ooa_can_trigger_switch(state, player),
            any([
                # Finding the road in the dark room
                ooa_has_cane(state, player),
                ooa_has_switch_hook(state, player),
                all([
                    ooa_option_medium_logic(state, player),
                    any([
                        ooa_can_kill_normal_enemy(state, player, False),
                        ooa_can_push_enemy(state, player),
                        ooa_has_boomerang(state, player),
                        ooa_can_use_pegasus_seeds_for_stun(state, player),
                    ])
                ])
            ])
        ])],
        ["d5 switch A", "d5 like-like chest", False, lambda state: any([
            ooa_can_trigger_far_switch(state, player),
            all([
                ooa_option_hard_logic(state, player), # Not hard to reproduce but clearly not instinctive to find.
                ooa_has_bracelet(state, player),
            ]),
            all([
                ooa_option_hard_logic(state, player),
                ooa_has_feather(state, player),
                any([
                    ooa_can_use_ember_seeds(state, player, False),
                    ooa_can_use_scent_seeds_for_smell(state, player),
                    ooa_can_use_mystery_seeds(state, player),
                ])
            ])
        ])],
        ["d5 switch A", "d5 eyes chest", False, lambda state: any([
            ooa_has_seedshooter(state, player),
            all([
                ooa_can_use_pegasus_seeds(state, player),
                ooa_has_feather(state, player),
                ooa_can_use_mystery_seeds(state, player),
                ooa_can_toss_ring(state, player)
            ])
        ])],
        ["d5 switch A", "d5 two-statue puzzle", False, lambda state: all([
            ooa_can_break_pot(state, player),
            any([
                ooa_has_cane(state, player),
                ooa_option_medium_logic(state, player),
            ]),
            ooa_has_feather(state, player),
            any([
                ooa_has_seedshooter(state, player),
                ooa_has_boomerang(state, player),
                all([
                    ooa_option_hard_logic(state, player),
                    ooa_can_jump_2_wide_pit(state, player, False),
                    any([
                        ooa_can_use_ember_seeds(state, player, False),
                        ooa_can_use_scent_seeds_for_smell(state, player),
                        ooa_can_use_mystery_seeds(state, player),
                    ])
                ])
            ])
        ])],
        ["d5 switch A", "d5 boss", False, lambda state: all([
            ooa_has_boss_key(state, player, 5),
            ooa_has_cane(state, player),
            ooa_has_sword(state, player),
        ])],

        # 2 keys
        ["d5 switch A", "d5 crossroads", False, lambda state: all([
            ooa_can_kill_normal_enemy(state, player, False),
            ooa_can_jump_2_wide_pit(state, player, False),
            ooa_has_bracelet(state, player),
            ooa_has_small_keys(state, player, 5, 2),
            any([
                ooa_has_cane(state, player),
                all([
                    ooa_option_hard_logic(state, player),
                    ooa_can_jump_3_wide_pit(state, player, False), # May need a proper check. Bomb jump ?
                ]),
                all([
                    ooa_option_hard_logic(state, player),
                    ooa_has_sword(state, player),
                    ooa_has_switch_hook(state, player),
                ])
            ])
        ])],
        ["d5 crossroads", "d5 diamond chest", False, lambda state: ooa_has_switch_hook(state, player)],

        # 5 keys
        ["d5 switch A", "d5 three-statue puzzle", False, lambda state: all([
            ooa_has_cane(state, player),
            ooa_has_small_keys(state, player, 5, 5),
        ])],
        ["d5 switch A", "d5 six-statue puzzle", False, lambda state: all([
            ooa_has_ember_seeds(state, player),
            ooa_has_seedshooter(state, player),
            ooa_has_small_keys(state, player, 5, 5),
            ooa_can_jump_1_wide_pit(state, player, False),
        ])],
        ["d5 crossroads", "d5 red peg chest", False, lambda state: all([
            ooa_can_trigger_far_switch(state, player),
            ooa_has_small_keys(state, player, 5, 5),
        ])],
        ["d5 red peg chest", "d5 owl puzzle", False, lambda state: any([
            ooa_option_medium_logic(state, player),
            ooa_has_cane(state, player)
        ])],
    ]

def make_d6past_logic(player: int):
    return [
        ["enter d6 past", "d6 wall A bombed", False, lambda state: ooa_has_bombs(state, player)],
        ["d6 wall A bombed", "d6 past wizzrobe", False, lambda state: ooa_can_kill_wizzrobes(state, player)],
        ["d6 wall A bombed", "d6 past pool chest", False, lambda state: all([
            ooa_can_use_ember_seeds(state, player, True),
            ooa_can_swim(state, player, False),
        ])],
        ["d6 wall A bombed", "d6 canal expanded", False, lambda state: all([
            ooa_can_use_ember_seeds(state, player, False),
            ooa_has_seedshooter(state, player),
        ])],
        ["d6 canal expanded", "d6 past rope chest", False, lambda state: all([
            ooa_can_dive(state, player),
            ooa_can_kill_underwater(state, player, True),
        ])],
        ["enter d6 past", "d6 past color room", False, lambda state: all([
            ooa_can_kill_normal_enemy(state, player, True),
            any([
                ooa_has_feather(state, player),
                all([
                    ooa_option_medium_logic(state, player),
                    ooa_can_use_mystery_seeds(state, player),
                ])
            ])
        ])],
        ["enter d6 past", "d6 past stalfos chest", False, lambda state: all([
            ooa_can_use_ember_seeds(state, player, False),
            any([
                ooa_option_hard_logic(state, player),
                ooa_can_use_scent_seeds_for_smell(state, player),
                #ooa_can_kill_ranged
                all([
                    ooa_can_jump_1_wide_pit(state, player, False),
                    ooa_can_kill_stalfos(state, player),
                ])
            ])
        ])],

        # past, 1 key
        ["enter d6 past", "d6 wall B bombed", False, lambda state: all([
            ooa_has_cane(state, player),
            ooa_has_bracelet(state, player),
            ooa_can_jump_1_wide_pit(state, player, False),
            ooa_has_small_keys(state, player, 9, 1),
            ooa_has_bombs(state, player)
        ])],
        ["d6 wall B bombed", "d6 past spear chest", False, lambda state: ooa_can_dive(state, player)],
        ["d6 wall B bombed", "d6 past diamond chest", False, lambda state: all([
            ooa_can_dive(state, player),
            ooa_has_switch_hook(state, player)
        ])],
        # past, 3 keys
        ["d6 wall B bombed", "d6 boss", False, lambda state: all([
            ooa_has_boss_key(state, player, 9),
            ooa_can_dive(state, player),
            ooa_has_small_keys(state, player, 9, 3),
            ooa_has_seedshooter(state, player),
            any([
                ooa_has_sword(state, player),
                all([
                    ooa_has_seedshooter(state, player),
                    any ([
                        ooa_has_scent_seeds(state, player),
                        ooa_has_ember_seeds(state, player),
                    ]),
                ]),
                ooa_can_punch(state, player),
            ])
        ])],
    ]

def make_d6present_logic(player: int):
    return [
        ["enter d6 present", "d6 present diamond chest", False, lambda state: ooa_has_switch_hook(state, player)],
        ["enter d6 present", "d6 present orb room", False, lambda state: any([
            ooa_can_swim(state, player, False),
            ooa_can_jump_3_wide_liquid(state, player),
            ooa_has_switch_hook(state, player),
        ])],
        ["d6 present orb room", "d6 present rope chest", False, lambda state: all([
            any([
                ooa_has_seedshooter(state, player),
                all([
                    ooa_option_hard_logic(state, player),
                    ooa_can_jump_2_wide_pit(state, player, False),
                    ooa_has_sword(state, player),
                ]),
                ooa_can_jump_3_wide_pit(state, player, False)
            ]),
            ooa_can_use_scent_seeds_for_smell(state, player)
        ])],
        ["d6 present orb room", "d6 present handmaster room", False, lambda state: any([
            ooa_has_seedshooter(state, player),
            all([
                ooa_option_hard_logic(state, player),
                ooa_can_jump_2_wide_pit(state, player, False),
                ooa_has_sword(state, player),
            ]),
            ooa_can_jump_4_wide_pit(state, player, False)
        ])],
        
        ["d6 present handmaster room", "d6 present cube chest", False, lambda state: all([
            ooa_has_switch_hook(state, player),
            ooa_has_bombs(state, player),
            any([
                ooa_option_hard_logic(state, player),
                ooa_can_jump_1_wide_pit(state, player, False)
            ])
        ])],
        ["d6 present handmaster room", "d6 present spinner chest", False, lambda state: all([
            state.has("_d6_wall_B_bombed", player),
            any([
                # To go past the pit in handmaster room
                ooa_has_switch_hook(state, player),
                ooa_can_jump_1_wide_pit(state, player, False),
            ])
        ])],
        
        ["enter d6 present", "d6 present beamos chest", False, lambda state: all([
            state.has("_d6_canal_expanded", player),
            ooa_has_feather(state, player),
            any([
                ooa_can_swim(state, player, False),
                all([
                    ooa_has_small_keys(state, player, 6, 3),
                    ooa_has_switch_hook(state, player),
                ])
            ])
        ])],

        # present, 3 keys
        # only sustainable weapons count for killing the ropes
        
        ["d6 present beamos chest", "d6 present rng chest", False, lambda state: all([
            ooa_has_bracelet(state, player),
            ooa_can_kill_normal_enemy(state, player, True),
            ooa_has_small_keys(state, player, 6, 3),
        ])],

        ["enter d6 present", "d6 present channel chest", False, lambda state: all([
            state.has("_d6_canal_expanded", player),
            ooa_has_switch_hook(state, player),
            ooa_has_small_keys(state, player, 6, 3),
        ])],

        ["d6 present spinner chest", "d6 present vire chest", False, lambda state: all([
            any([
                ooa_has_sword(state, player),
                state.has("Expert's Ring", player),
                ooa_option_medium_logic(state, player) # for switch hook kill (?)
            ]),
            ooa_has_small_keys(state, player, 6, 3),
            ooa_has_switch_hook(state, player)
        ])],
    ]

def make_d7_logic(player: int):
    return [
        
        # leaving/entering the dungeon (but not loading a file) resets the water level.
        # this is necessary to make keys work out, since otherwise you can drain the
        # water level without getting enough keys to refill it! there just aren't
        # enough chests otherwise.
        # Now that dungeon entrances are randomized, mermaid suit can't be assumed
        # anymore. The OG randomizer would allow you to enter jabu without the mermaid
        # suit but would prevent you from surfacing a level up, since you would
        # instantly drown then. This was changed in NG; now you're prevented from
        # entering the dungeon without the mermaid suit.
        # Be careful never to use the "enter d7" node for the purpose of logic, always
        # use "enter d7 with suit".
        ["enter d7", "enter d7 with suit", False, lambda state: ooa_can_dive(state, player)],

        # 0 keys
        ["enter d7 with suit", "d7 spike chest", False, None],
        ["enter d7 with suit", "d7 crab chest", False, lambda state: any([
            ooa_can_kill_underwater(state, player),
            all([
                state.has("_d7_drain", player),
                ooa_can_kill_normal_enemy(state, player)
            ])
        ])],
        ["enter d7 with suit", "d7 diamond puzzle", False, lambda state: ooa_has_switch_hook(state, player)],
        ["enter d7 with suit", "d7 flower room", False, lambda state: all([
            ooa_has_long_hook(state, player),
            ooa_has_feather(state, player)
        ])],
        ["enter d7 with suit", "d7 stairway chest", False, lambda state: any([
            ooa_has_long_hook(state, player),
            all([
                state.has("_d7_drain", player),
                ooa_has_cane(state, player),
                ooa_has_switch_hook(state, player),
            ])
        ])],
        ["d7 stairway chest", "d7 right wing", False, lambda state: ooa_can_kill_moldorm(state, player)],

        # 3 keys - enough to drain dungeon
        ["enter d7 with suit", "d7 drain", False, lambda state: any([
            ooa_has_small_keys(state, player, 7, 3),
        ])],
        ["d7 drain", "d7 boxed chest", False, None],
        ["d7 drain", "d7 cane/diamond puzzle", False, lambda state: all([
            ooa_has_long_hook(state, player),
            ooa_has_cane(state, player),
        ])],

        # 4 keys - enough to choose any water level (middle water level keydoor doesn't
        # necessarily need to be unlocked since water level resets upon reentry)
        ["enter d7 with suit", "d7 flood", False, lambda state: all([
            ooa_has_long_hook(state, player),
            ooa_has_small_keys(state, player, 7, 4),
        ])],
        ["d7 flood", "d7 terrace", False, None],
        ["d7 flood", "d7 left wing", False, None],
        ["d7 flood", "d7 boss", False, lambda state: ooa_has_boss_key(state, player, 7)],

        # 5 keys
        ["d7 flood", "d7 hallway chest", False, lambda state: ooa_has_small_keys(state, player, 7, 5)],

        # 7 keys
        ["d7 stairway chest", "d7 miniboss chest", False, lambda state: all([
            ooa_has_feather(state, player),
            ooa_has_small_keys(state, player, 7, 7),
            any([
                ooa_has_sword(state, player),
                ooa_has_boomerang(state, player),
                all([
                    ooa_has_seedshooter(state, player),
                    ooa_has_scent_seeds(state, player)
                ])
            ])
        ])],
        ["d7 flood", "d7 post-hallway chest", False, lambda state: ooa_has_small_keys(state, player, 7, 7)],
        ["d7 drain", "d7 island chest", False, lambda state: all([
            ooa_has_small_keys(state, player, 7, 7),
            ooa_has_switch_hook(state, player),
        ])],
    ]

def make_d8_logic(player: int):
    return [
        
        ["enter d8", "d8 1f single chest", False, lambda state: all([
            ooa_has_bombs(state, player),
            any([
                ooa_can_kill_normal_enemy(state, player, True),
                ooa_has_boomerang(state, player),
                ooa_can_use_pegasus_seeds_for_stun(state, player),
            ])
        ])],

        # 1 key - access B1F
        ["d8 1f single chest", "d8 nw chest", False, lambda state: all([
            ooa_has_small_keys(state, player, 8, 1),
            ooa_has_switch_hook(state, player),
            ooa_has_cane(state, player),
            ooa_can_use_ember_seeds(state, player, True),
            ooa_has_seedshooter(state, player),
        ])],
        ["d8 nw chest", "d8 ghini chest", False, lambda state: ooa_can_kill_normal_enemy(state, player)],

        # 2 keys - access SE spinner
        ["d8 ghini chest", "d8 blue peg chest", False, lambda state: ooa_has_small_keys(state, player, 8, 2)],
        ["d8 blue peg chest", "d8 blade trap", False, None],
        ["d8 blue peg chest", "d8 sarcophagus chest", False, lambda state: ooa_has_glove(state, player)],
        ["d8 blue peg chest", "d8 stalfos", False, lambda state: ooa_can_kill_stalfos(state, player)],

        # 4 keys - reach miniboss
        ["d8 blue peg chest", "d8 maze chest", False, lambda state: all([
            ooa_has_feather(state, player),
            ooa_has_sword(state, player),
            ooa_has_small_keys(state, player, 8, 4)
        ])],
        ["d8 maze chest", "d8 nw slate chest", False, None],
        ["d8 maze chest", "d8 ne slate chest", False, lambda state: all([
            ooa_has_feather(state, player),
            ooa_can_swim(state, player, False),
            ooa_can_use_ember_seeds(state, player, False),
        ])],

        
        ["d8 maze chest", "d8 b3f single chest", False, lambda state: ooa_has_glove(state, player)],
        ["d8 b3f single chest", "d8 tile room", False, lambda state: ooa_has_feather(state, player)],
        ["d8 tile room", "d8 se slate chest", False, None],
        ["d8 tile room", "d8 boss", False, lambda state: all([
            ooa_has_enough_slates(state, player),
            ooa_has_boss_key(state, player, 8),
            ooa_has_glove(state, player),
            ooa_has_sword(state, player),
        ])],

        # 5 keys
        ["d8 blue peg chest", "d8 floor puzzle", False, lambda state: ooa_has_small_keys(state, player, 8, 5)],
        ["d8 maze chest", "d8 sw slate chest", False, lambda state: all([
            ooa_has_bracelet(state, player),
            ooa_has_small_keys(state, player, 8, 5)
        ])],
    ] 
