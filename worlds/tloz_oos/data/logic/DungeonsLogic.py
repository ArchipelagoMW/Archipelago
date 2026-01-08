from worlds.tloz_oos.data.logic.LogicPredicates import *


def make_d0_logic(player: int):
    return [
        # 0 keys
        ["enter d0", "d0 key chest", False, None],
        ["enter d0", "d0 rupee chest", False, lambda state:
            # If hole is removed, stairs are added inside dungeon to make the chest reachable
            oos_option_no_d0_alt_entrance(state, player)
         ],
        ["d0 rupee chest", "enter d0", False, None],
        ["enter d0", "d0 hidden 2d section", False, lambda state: any([
            oos_can_kill_normal_enemy(state, player),
            oos_has_boomerang(state, player),
            oos_has_switch_hook(state, player)
        ])],

        # 1 key
        ["enter d0", "d0 sword chest", False, lambda state: any([
            oos_has_small_keys(state, player, 0, 1),
            oos_self_locking_small_key(state, player, "d0 sword chest", 0),
            oos_self_locking_item(state, player, "d0 sword chest", "Master Key (Hero's Cave)")
        ])],
    ]


def make_d1_logic(player: int):
    return [
        # 0 keys
        ["enter d1", "d1 stalfos drop", False, lambda state: any([
            oos_can_kill_stalfos(state, player),
            all([
                # Medium logic expects the player to be able to use bushes
                oos_option_medium_logic(state, player),
                oos_has_bracelet(state, player)
            ])
        ])],

        ["enter d1", "d1 floormaster room", False, lambda state: oos_can_use_ember_seeds(state, player, True)],

        ["d1 floormaster room", "d1 boss", False, lambda state: all([
            oos_has_boss_key(state, player, 1),
            oos_can_kill_armored_enemy(state, player, False, False)
        ])],

        # 1 key
        ["enter d1", "d1 stalfos chest", False, lambda state: all([
            oos_has_small_keys(state, player, 1, 1),
            oos_can_kill_stalfos(state, player)
        ])],

        ["d1 stalfos chest", "d1 goriya chest", False, lambda state: all([
            oos_can_use_ember_seeds(state, player, True),
            oos_can_kill_normal_enemy(state, player, True)
        ])],

        ["d1 stalfos chest", "d1 lever room", False, None],

        ["d1 stalfos chest", "d1 block-pushing room", False, lambda state: any([
            oos_can_kill_normal_enemy(state, player),
            all([
                oos_option_hard_logic(state, player),
                oos_has_bracelet(state, player)
            ])
        ])],

        ["d1 stalfos chest", "d1 railway chest", False, lambda state: any([
            oos_can_trigger_lever(state, player),
            all([
                oos_option_hard_logic(state, player),
                oos_has_bracelet(state, player)
            ])
        ])],

        ["d1 railway chest", "d1 button chest", False, None],

        # 2 keys
        ["d1 railway chest", "d1 basement", False, lambda state: any([
            oos_self_locking_small_key(state, player, "d1 basement", 1),
            all([
                oos_can_remove_rockslide(state, player, False),
                oos_has_small_keys(state, player, 1, 2),
                oos_can_kill_armored_enemy(state, player, False, True)
            ])
        ])],
    ]


def make_d2_logic(player: int):
    return [
        # 0 keys
        ["enter d2", "d2 torch room", True, None],
        ["d2 torch room", "d2 left from entrance", False, None],
        ["d2 torch room", "d2 rope drop", False, lambda state: any([
            oos_can_kill_normal_enemy(state, player),
            oos_has_switch_hook(state, player)
        ])],
        ["d2 torch room", "d2 arrow room", False, lambda state: oos_can_use_ember_seeds(state, player, True)],

        ["d2 arrow room", "d2 torch room", False, lambda state: oos_can_kill_normal_enemy(state, player)],
        ["d2 arrow room", "d2 rupee room", False, lambda state: oos_can_remove_rockslide(state, player, False)],
        ["d2 arrow room", "d2 rope chest", False, lambda state: any([
            oos_can_kill_normal_enemy(state, player),
            oos_has_switch_hook(state, player)
        ])],
        ["d2 arrow room", "d2 blade chest", False, lambda state: oos_can_kill_normal_enemy(state, player)],

        ["d2 blade chest", "d2 arrow room", False, None],  # Backwards path
        ["d2 blade chest", "d2 alt entrances", True, lambda state: oos_has_bracelet(state, player)],
        ["d2 blade chest", "d2 roller chest", False, lambda state: all([
            oos_can_remove_rockslide(state, player, False),
            oos_has_bracelet(state, player),
        ])],
        ["d2 alt entrances", "d2 spiral chest", False, lambda state: all([
            oos_can_break_bush(state, player, False, True),
            any([
                oos_has_bombs(state, player),
                all([
                    # It's tight but doable
                    oos_option_medium_logic(state, player),
                    oos_can_use_pegasus_seeds(state, player),
                    oos_has_bombchus(state, player, 5)
                ])
            ])
        ])],
        ["d2 alt entrances", "d2 scrub", False, lambda state: oos_has_rupees_for_shop(state, player, "d2Scrub")],

        # 2 keys
        ["d2 roller chest", "d2 spinner", False, lambda state: all([
            oos_has_small_keys(state, player, 2, 2),
            oos_can_kill_facade(state, player)
        ])],
        # terrace self-locking rules
        ["d2 arrow room", "d2 terrace chest", False, lambda state: all([
            oos_has_small_keys(state, player, 2, 2),
            oos_self_locking_small_key(state, player, "d2 terrace chest", 2)
        ])],
        # You can take the Facade miniboss teleporter to reach dungeon entrance, even if you entered the dungeon
        # through the alt-entrance
        ["d2 spinner", "d2 torch room", False, None],
        ["d2 spinner", "dodongo owl", False, lambda state: oos_can_use_mystery_seeds(state, player)],
        ["d2 spinner", "d2 boss", False, lambda state: all([
            oos_has_boss_key(state, player, 2),
            oos_has_bombs(state, player),
            oos_has_bracelet(state, player)
        ])],

        # 3 keys
        ["d2 arrow room", "d2 hardhat room", False, lambda state: oos_has_small_keys(state, player, 2, 3)],
        ["d2 hardhat room", "d2 pot chest", False, lambda state: oos_can_break_pot(state, player)],
        ["d2 hardhat room", "d2 moblin chest", False, lambda state: any([
            all([
                oos_can_kill_d2_hardhat(state, player),
                oos_can_kill_d2_far_moblin(state, player)
            ])
        ])],
        ["d2 spinner", "d2 terrace chest", False, lambda state: oos_has_small_keys(state, player, 2, 3)],
    ]


def make_d3_logic(player: int):
    return [
        # 0 keys
        ["enter d3", "spiked beetles owl", False, lambda state: oos_can_use_mystery_seeds(state, player)],
        ["enter d3", "d3 center", False, lambda state: any([
            oos_can_kill_spiked_beetle(state, player),
            all([
                oos_option_medium_logic(state, player),
                oos_can_flip_spiked_beetle(state, player),
                oos_has_bracelet(state, player)
            ])
        ])],

        ["d3 center", "d3 water room", False, lambda state: oos_has_feather(state, player)],
        ["d3 center", "d3 mimic stairs", False, lambda state: any([
            oos_has_bracelet(state, player),
            all([
                oos_can_break_pot(state, player),
                oos_has_cane(state, player)
            ])
        ])],
        ["d3 center", "trampoline owl", False, lambda state: all([
            oos_has_feather(state, player),
            oos_can_use_mystery_seeds(state, player)
        ])],
        ["d3 center", "d3 trampoline chest", False, lambda state: oos_has_feather(state, player)],
        ["d3 center", "d3 zol chest", False, lambda state: oos_has_feather(state, player)],

        ["d3 mimic stairs", "d3 water room", True, None],
        ["d3 mimic stairs", "d3 roller chest", False, lambda state: oos_has_bracelet(state, player)],
        ["d3 mimic stairs", "d3 quicksand terrace", False, lambda state: oos_has_feather(state, player)],
        ["d3 quicksand terrace", "omuai owl", False, lambda state: all([
            oos_can_use_mystery_seeds(state, player)
        ])],
        ["d3 mimic stairs", "d3 moldorm chest", False, lambda state: oos_can_kill_moldorm(state, player)],
        ["d3 mimic stairs", "d3 bombed wall chest", False, lambda state: oos_can_remove_rockslide(state, player, False)],

        # 2 keys
        ["d3 water room", "d3 mimic chest", False, lambda state: all([
            any([
                oos_has_small_keys(state, player, 3, 2),
                oos_self_locking_small_key(state, player, "d3 mimic chest", 3)
            ]),
            oos_can_kill_normal_enemy(state, player)
        ])],
        ["d3 mimic stairs", "d3 omuai stairs", False, lambda state: all([
            any([
                oos_has_feather(state, player),

                # With switch hook, even with pegasus, you can barely see the pots, so it's not casual friendly
                all([
                    oos_option_medium_logic(state, player),
                    oos_has_switch_hook(state, player, 2)
                ]),
                all([
                    oos_option_medium_logic(state, player),
                    oos_can_use_pegasus_seeds(state, player),
                    oos_has_switch_hook(state, player)
                ])
            ]),
            oos_has_small_keys(state, player, 3, 2),
            oos_has_bracelet(state, player),
            oos_can_kill_armored_enemy(state, player, False, False)
        ])],
        ["d3 omuai stairs", "d3 quicksand terrace", False, None],
        ["d3 omuai stairs", "d3 giant blade room", False, lambda state: any([
            oos_has_feather(state, player),
            oos_option_hard_logic(state, player)
        ])],
        ["d3 omuai stairs", "d3 boss", False, lambda state: oos_has_boss_key(state, player, 3)],
    ]


def make_d4_logic(player: int):
    return [
        # 0 keys
        ["enter d4", "d4 north of entrance", False, lambda state: any([
            oos_has_flippers(state, player),
            oos_has_cape(state, player)
        ])],
        ["d4 north of entrance", "d4 pot puzzle", False, lambda state: all([
            oos_can_remove_rockslide(state, player, False),
            oos_has_bracelet(state, player)
        ])],
        ["d4 north of entrance", "d4 maze chest", False, lambda state: any([
            oos_can_trigger_lever_from_minecart(state, player),
            all([
                oos_option_hard_logic(state, player),
                oos_has_bracelet(state, player)
            ])
        ])],
        ["d4 maze chest", "d4 dark room", False, lambda state: oos_has_feather(state, player)],

        # 1 key
        ["enter d4", "d4 water ring room", False, lambda state: all([
            oos_has_small_keys(state, player, 4, 1),
            any([
                oos_has_cape(state, player),
                all([
                    # Feather is required to jump above spike lines
                    oos_has_feather(state, player),
                    oos_has_flippers(state, player)
                ])
            ]),
            oos_can_remove_rockslide(state, player, False),
            any([
                oos_can_kill_normal_enemy(state, player),
                all([  # killing enemies with pots
                    oos_option_medium_logic(state, player),
                    oos_has_bracelet(state, player),
                ]),
                all([  # pushing enemies in the water
                    oos_has_rod(state, player),
                    any([
                        oos_has_boomerang(state, player),
                        oos_has_switch_hook(state, player)
                    ])
                ])
            ])
        ])],

        ["enter d4", "d4 roller minecart", False, lambda state: all([
            oos_has_small_keys(state, player, 4, 1),
            oos_has_feather(state, player),
            any([
                oos_has_flippers(state, player),
                all([
                    oos_option_hell_logic(state, player),
                    oos_has_cape(state, player),
                    oos_can_use_pegasus_seeds(state, player),
                    oos_has_bombs(state, player)
                ])
            ])
        ])],

        ["d4 roller minecart", "d4 pool", False, lambda state: all([
            any([
                oos_has_flippers(state, player),
                oos_option_medium_logic(state, player)
            ]),
            any([
                oos_can_kill_normal_enemy(state, player),
                all([
                    oos_option_medium_logic(state, player),
                    oos_has_bracelet(state, player)
                ])
            ]),
            any([
                oos_can_trigger_lever_from_minecart(state, player),
                all([
                    oos_option_hard_logic(state, player),
                    oos_has_bracelet(state, player)
                ])
            ])
        ])],

        # 2 keys
        ["d4 roller minecart", "greater distance owl", False, lambda state: all([
            oos_has_small_keys(state, player, 4, 2),
            oos_can_use_mystery_seeds(state, player)
        ])],

        ["d4 roller minecart", "d4 stalfos stairs", False, lambda state: all([
            oos_has_small_keys(state, player, 4, 2),
            any([
                oos_can_kill_stalfos(state, player),
                all([
                    # Kill Stalfos by using pots in the room
                    oos_option_medium_logic(state, player),
                    oos_has_bracelet(state, player)
                ])
            ]),
            oos_can_jump_2_wide_pit(state, player)
        ])],

        ["d4 stalfos stairs", "d4 terrace", False, None],
        ["d4 terrace", "d4 scrub", False, lambda state: oos_has_rupees_for_shop(state, player, "d4Scrub")],

        ["d4 stalfos stairs", "d4 torch chest", False, lambda state: all([
            oos_has_seed_thrower(state, player),
            oos_has_ember_seeds(state, player)
        ])],

        ["d4 stalfos stairs", "d4 miniboss room", False, None],
        ["d4 miniboss room", "d4 miniboss room wild embers", False, lambda state: \
            oos_can_harvest_regrowing_bush(state, player)],

        ["d4 miniboss room", "d4 final minecart", False, lambda state: all([
            oos_can_use_ember_seeds(state, player, False),
            oos_can_kill_armored_enemy(state, player, False, False)
        ])],

        # 5 keys
        ["d4 final minecart", "d4 cracked floor room", False, lambda state: any([
            oos_has_small_keys(state, player, 4, 5),
            oos_self_locking_small_key(state, player, "d4 cracked floor room", 4)
        ])],
        ["d4 final minecart", "d4 dive spot", False, lambda state: all([
            any([
                all([
                    any([  # hit distant levers
                        oos_has_magic_boomerang(state, player),
                        oos_has_seed_thrower(state, player)
                    ]),
                    # In medium, switch is also valid, but a feather is required to get there anyway
                    oos_can_jump_2_wide_pit(state, player),
                    oos_has_small_keys(state, player, 4, 5),
                ]),
                # For self-locking, we don't need to check if the player is able to
                # waste the key first to then get it back, only to get it back if they waste it
                oos_self_locking_small_key(state, player, "d4 dive spot", 4)
            ]),
            oos_has_flippers(state, player)
        ])],

        ["d4 final minecart", "d4 basement stairs", False, lambda state: all([
            oos_has_small_keys(state, player, 4, 5),
            any([
                oos_has_boomerang(state, player),
                oos_has_seed_thrower(state, player),
                oos_has_switch_hook(state, player),
                oos_option_hard_logic(state, player)
            ])
        ])],

        ["d4 basement stairs", "gohma owl", False, lambda state: oos_can_use_mystery_seeds(state, player)],

        ["d4 basement stairs", "enter gohma", False, lambda state: all([
            oos_has_boss_key(state, player, 4),
            any([
                all([
                    oos_has_seed_thrower(state, player),
                    oos_can_use_ember_seeds(state, player, True)
                ]),
                oos_can_jump_3_wide_pit(state, player),
                all([  # throw seeds using satchel during a jump
                    oos_option_hard_logic(state, player),
                    oos_has_feather(state, player),
                    oos_can_use_ember_seeds(state, player, False)
                ])
            ])
        ])],

        ["enter gohma", "d4 boss", False, lambda state: any([
            all([
                # Kill Gohma without breaking its pincer
                oos_option_medium_logic(state, player),
                any([
                    oos_has_seed_thrower(state, player),
                    oos_option_hard_logic(state, player)  # You can kill Gohma with the satchel. Yup...
                ]),
                any([
                    oos_has_scent_seeds(state, player),
                    oos_has_ember_seeds(state, player)
                ])
            ]),
            all([
                # Kill Gohma with sword beams (Gohma's minions give enough hearts to justify it)
                oos_option_medium_logic(state, player),
                any([
                    oos_has_noble_sword(state, player),
                    oos_shoot_beams(state, player)
                ])
            ]),
            all([
                # Kill Gohma traditionally (break pincer, then spam seeds)
                any([
                    oos_has_sword(state, player),
                    oos_has_fools_ore(state, player)
                ]),
                any([
                    oos_can_use_ember_seeds(state, player, False),
                    oos_can_use_scent_seeds(state, player),
                    all([
                        oos_option_medium_logic(state, player),
                        oos_has_satchel(state, player, 2),  # It may require quite a bunch of mystery seeds...
                        oos_can_use_mystery_seeds(state, player)
                    ])
                ])
            ])
        ])],
    ]


def make_d5_logic(player: int):
    return [
        # 0 keys
        ["enter d5", "d5 left chest", False, lambda state: any([
            oos_has_magnet_gloves(state, player),
            oos_has_cape(state, player),
            all([
                # Tight bomb jump to reach the chest
                oos_option_hell_logic(state, player),
                oos_can_jump_3_wide_liquid(state, player),
            ])
        ])],

        ["enter d5", "d5 spiral chest", False, lambda state: all([
            oos_can_kill_moldorm(state, player, True),
            oos_can_kill_normal_enemy(state, player, True)
        ])],

        ["enter d5", "d5 terrace chest", False, lambda state: oos_has_magnet_gloves(state, player)],

        ["d5 terrace chest", "armos knights owl", False, lambda state: oos_can_use_mystery_seeds(state, player)],
        ["d5 terrace chest", "d5 armos chest", False, lambda state: all([
            oos_can_kill_moldorm(state, player),
            oos_can_kill_normal_enemy(state, player)
        ])],

        ["enter d5", "d5 cart bay", False, lambda state: any([
            oos_has_flippers(state, player),
            oos_can_jump_2_wide_liquid(state, player)
        ])],

        ["d5 cart bay", "d5 terrace chest", False, lambda state: all([
            oos_has_feather(state, player),
            oos_can_remove_rockslide(state, player, False)  # Bombchus can be thrown from the middle platform
        ])],

        ["d5 cart bay", "d5 cart chest", False, lambda state: oos_can_trigger_lever_from_minecart(state, player)],

        ["d5 cart bay", "d5 spinner chest", False, lambda state: any([
            oos_has_magnet_gloves(state, player),
            oos_can_jump_5_wide_pit(state, player),
            all([
                # Switch with the pots on the bottom left
                oos_option_medium_logic(state, player),
                oos_has_switch_hook(state, player, 2)
            ]),
            all([
                # Wait for le helmasaur to be on the left side of the hole.
                # By being on the right border, you can see pixels of it and switch hook 1 with it
                oos_option_hell_logic(state, player),
                oos_has_switch_hook(state, player)
            ])
        ])],

        ["d5 cart bay", "d5 drop ball", False, lambda state: all([
            oos_can_trigger_lever_from_minecart(state, player),
            any([
                oos_can_kill_armored_enemy(state, player, True, True),
                oos_has_shield(state, player),
                all([
                    oos_option_medium_logic(state, player),
                    oos_has_shovel(state, player)
                ]),
                all([
                    oos_option_medium_logic(state, player),
                    # Pull the darknut in the water
                    oos_has_magnet_gloves(state, player)
                ])
            ])
        ])],

        ["enter d5", "d5 pot room", False, lambda state: all([
            oos_has_magnet_gloves(state, player),
            oos_can_remove_rockslide(state, player, False),
            oos_has_feather(state, player)
        ])],

        ["d5 cart bay", "d5 pot room", False, lambda state: any([
            oos_has_feather(state, player),
            all([
                oos_option_hard_logic(state, player),
                oos_can_use_pegasus_seeds(state, player)
            ])
        ])],

        ["d5 pot room", "d5 gibdo/zol chest", False, lambda state: oos_can_kill_normal_enemy(state, player)],

        ["d5 cart bay", "d5 syger lobby", False, lambda state: any([
            oos_has_magnet_gloves(state, player),
            oos_has_cape(state, player),
        ])],
        ["d5 pot room", "d5 syger lobby", False, lambda state: any([
            oos_has_magnet_gloves(state, player),
            oos_has_cape(state, player),
        ])],

        ["d5 syger lobby", "d5 stalfos room", False, None],

        # 5 keys
        ["d5 syger lobby", "d5 post syger", False, lambda state: all([
            oos_has_small_keys(state, player, 5, 3),
            oos_can_kill_armored_enemy(state, player, False, False)
        ])],

        ["enter d5", "d5 magnet ball chest", False, lambda state: \
            oos_self_locking_small_key(state, player, "d5 magnet ball chest", 5)],
        ["enter d5", "d5 basement", False, lambda state: all([
            oos_self_locking_small_key(state, player, "d5 basement", 5),
            state.has("_dropped_d5_magnet_ball", player),
            oos_has_small_keys(state, player, 5, 3),
            oos_has_magnet_gloves(state, player),
            any([
                oos_can_kill_magunesu(state, player),
                all([
                    oos_option_medium_logic(state, player),
                    oos_has_feather(state, player)
                ])
            ])
        ])],

        ["d5 pot room", "d5 magnet ball chest", False, lambda state: all([
            any([
                oos_has_flippers(state, player),
                all([
                    # Lower route pushing secret blocks requires knowledge, therefore is medium+.
                    # Going there requires jumping a 3.2 wide liquid gap which corresponds the best to a "4 wide pit"
                    # in terms of logic requirements.
                    oos_can_jump_4_wide_pit(state, player),
                    oos_option_medium_logic(state, player),
                    # Upper route would require 6 wide liquid that can only be jumped above with a bomb jump,
                    # which makes the lower route always better when in medium+.
                ])
            ]),
            oos_has_small_keys(state, player, 5, 5),
        ])],

        ["d5 post syger", "d5 basement", False, lambda state: all([
            any([
                oos_has_small_keys(state, player, 5, 5),
                oos_self_locking_small_key(state, player, "d5 basement", 5)
            ]),

            # Magnet ball button
            any([
                all([
                    state.has("_dropped_d5_magnet_ball", player),
                    oos_has_magnet_gloves(state, player),
                ]),
                oos_has_cane(state, player)
            ]),

            # Flamme wall
            any([
                all([
                    oos_has_magnet_gloves(state, player),
                    oos_can_kill_magunesu(state, player),
                ]),
                all([
                    oos_option_medium_logic(state, player),
                    oos_has_feather(state, player)
                ])
            ]),

            # Basement
            any([
                oos_has_magnet_gloves(state, player),
                all([
                    oos_has_cane(state, player),
                    oos_can_jump_3_wide_pit(state, player)
                ])
            ])
        ])],

        ["d5 post syger", "d5 boss", False, lambda state: all([
            oos_has_small_keys(state, player, 5, 5),
            oos_has_magnet_gloves(state, player),
            oos_has_boss_key(state, player, 5),
            any([
                oos_option_medium_logic(state, player),
                oos_has_feather(state, player)
            ]),
        ])],
    ]


def make_d6_logic(player: int):
    return [
        # 0 keys
        ["enter d6", "d6 1F east", False, lambda state: any([
            oos_has_feather(state, player),
            oos_has_sword(state, player),
            oos_has_bombs(state, player),
            oos_option_hard_logic(state, player)
        ])],

        ["d6 1F east", "d6 rupee room", False, lambda state: oos_can_remove_rockslide(state, player, False)],

        ["d6 1F east", "d6 1F terrace", False, None],
        ["enter d6", "d6 1F terrace", False, lambda state: all([
            oos_has_small_keys(state, player, 6, 2),
            any([
                oos_has_magnet_gloves(state, player),
                oos_has_cane(state, player)
            ])
        ])],

        ["d6 1F terrace", "d6 magnet ball drop", False, lambda state: any([
            all([
                oos_has_feather(state, player),
                oos_has_magnet_gloves(state, player)
            ]),
            oos_can_jump_4_wide_pit(state, player),
            all([
                # Cane through the block
                oos_option_medium_logic(state, player),
                oos_has_cane(state, player)
            ])
        ])],
        ["d6 1F terrace", "d6 crystal trap room", False, None],
        ["d6 1F terrace", "d6 U-room", False, lambda state: all([
            oos_can_break_crystal(state, player),
            any([
                oos_has_magic_boomerang(state, player),
                all([
                    # Clip into the right statues for the first orb,
                    # then manipulate the position to clip into the bottom right of the opening for the second one
                    oos_option_hell_logic(state, player),
                    oos_has_shooter(state, player),
                ]),
                all([
                    # Just do the first one in hard, then use bombchus to kill the keese then hit the orb
                    oos_option_hard_logic(state, player),
                    oos_has_shooter(state, player),
                    oos_has_bombchus(state, player, 2),
                ])
            ])
        ])],
        ["d6 U-room", "d6 torch stairs", False, lambda state: all([
            any([
                # In easy, logic expects slingshot, but medium+ can expect satchel
                # as well since the distance between platforms & torches is a half-tile
                oos_has_seed_thrower(state, player),
                oos_option_medium_logic(state, player)
            ]),
            oos_can_use_ember_seeds(state, player, False)
        ])],

        ["d6 torch stairs", "d6 escape room", False, lambda state: oos_has_feather(state, player)],
        ["d6 escape room", "d6 vire chest", False, lambda state: oos_can_kill_stalfos(state, player)],

        # 3 keys
        ["enter d6", "d6 beamos room", False, lambda state: oos_has_small_keys(state, player, 6, 3)],
        ["d6 beamos room", "d6 2F gibdo chest", False, None],
        ["d6 beamos room", "d6 2F armos chest", False, lambda state: oos_can_remove_rockslide(state, player, False)],
        ["d6 2F armos chest", "d6 armos hall", False, lambda state: oos_has_feather(state, player)],

        ["enter d6", "d6 spinner north", False, lambda state: all([
            oos_can_break_crystal(state, player),
            any([
                oos_has_magnet_gloves(state, player),
                all([  # Clip into the blocks to place the somaria block on the button
                    oos_option_hard_logic(state, player),
                    oos_has_cane(state, player)
                ])
            ]),
            any([
                oos_option_medium_logic(state, player),  # Iframes through the spikes
                oos_has_feather(state, player)
            ]),
            any([
                all([
                    oos_has_small_keys(state, player, 6, 1),

                    # Go through beamos room
                    all([
                        oos_can_remove_rockslide(state, player, False),
                        oos_has_feather(state, player)
                    ]),

                    any([
                        # Kill Vire (the rest doesn't matter because we don't care about not being able to not spend a key somewhere)
                        oos_has_sword(state, player, False),
                        oos_has_fools_ore(state, player),
                        all([
                            oos_option_medium_logic(state, player),
                            oos_has_bombs(state, player, 4)
                        ]),
                        all([
                            # Fist Ring doesn't damage Vire
                            state.has("expert's ring", player),
                            oos_option_medium_logic(state, player)
                        ])
                    ])
                ]),
                all([
                    oos_has_small_keys(state, player, 6, 2),
                    any([
                        # Go through beamos room
                        all([
                            oos_can_remove_rockslide(state, player, False),
                            oos_has_feather(state, player)
                        ]),

                        # Kill Vire
                        oos_has_sword(state, player, False),
                        oos_has_fools_ore(state, player),
                        all([
                            oos_option_medium_logic(state, player),
                            oos_has_bombs(state, player, 4)
                        ]),
                        all([
                            # Fist Ring doesn't damage Vire
                            state.has("expert's ring", player),
                            oos_option_medium_logic(state, player)
                        ])
                    ])
                ]),
                oos_has_small_keys(state, player, 6, 3),
            ])
        ])],

        ["d6 vire chest", "d6 enter vire", False, lambda state: all([
            oos_has_small_keys(state, player, 6, 3),
            any([
                # Kill Vire
                oos_has_sword(state, player, False),
                oos_has_fools_ore(state, player),
                all([
                    oos_option_medium_logic(state, player),
                    oos_has_bombs(state, player, 4)
                ]),
                all([
                    # Fist Ring doesn't damage Vire
                    state.has("expert's ring", player),
                    oos_option_medium_logic(state, player)
                ])
            ])
        ])],
        ["d6 enter vire", "d6 pre-boss room", False, lambda state: all([
            oos_has_small_keys(state, player, 6, 3),
            any([
                # Kill hardhats
                oos_has_magnet_gloves(state, player),
                all([
                    oos_option_medium_logic(state, player),
                    oos_has_gale_seeds(state, player),
                    any([
                        oos_has_seed_thrower(state, player),
                        all([
                            oos_option_hard_logic(state, player),
                            oos_has_satchel(state, player)
                        ])
                    ])
                ])
            ]),
            oos_has_feather(state, player)  # jump on trampoline
            # Switches here are considered trivial since we'll need magic boomerang for
            # Manhandla anyway
        ])],

        ["d6 pre-boss room", "d6 boss", False, lambda state: all([
            oos_has_boss_key(state, player, 6),
            oos_has_magic_boomerang(state, player),
            any([
                oos_has_sword(state, player),
                oos_has_fools_ore(state, player),
                oos_has_seed_thrower(state, player),
                # state.has("expert's ring", player)
            ])
        ])],
    ]


def make_d7_logic(player: int):
    return [
        # 0 keys
        ["enter d7", "poe curse owl", False, lambda state: oos_can_use_mystery_seeds(state, player)],
        ["enter d7", "d7 wizzrobe chest", False, lambda state: oos_can_kill_normal_enemy_no_cane(state, player)],
        ["enter d7", "d7 bombed wall chest", False, lambda state: oos_can_break_crystal(state, player)],
        ["enter d7", "d7 entrance wild embers", False, lambda state: oos_can_harvest_regrowing_bush(state, player)],

        # 1 key
        ["enter d7", "enter poe A", False, lambda state: all([
            oos_has_small_keys(state, player, 7, 1),
            oos_has_seed_thrower(state, player),
            oos_can_use_ember_seeds(state, player, True)
        ])],

        ["enter poe A", "d7 pot room", False, lambda state: all([
            any([
                # Kill poe sister
                oos_can_kill_armored_enemy(state, player, False, False),
                all([
                    oos_option_medium_logic(state, player),
                    oos_has_rod(state, player),
                ]),
                all([
                    # Mystery isn't reasonable due to having only ~8.8% chance of not getting a gale before killing the sister
                    oos_has_ember_seeds(state, player),
                    any([
                        oos_option_medium_logic(state, player),
                        oos_has_satchel(state, player, 2)
                    ])
                ])
            ]),
            oos_has_bracelet(state, player)
        ])],
        ["enter d7", "d7 pot room", False, lambda state: all([
            # Poe skip
            oos_option_hell_logic(state, player),
            oos_can_remove_rockslide(state, player, False),
            oos_can_use_pegasus_seeds(state, player),
            oos_has_feather(state, player),
            oos_has_bracelet(state, player),
        ])],

        ["d7 pot room", "d7 zol button", False, lambda state: oos_has_feather(state, player)],
        ["d7 pot room", "d7 armos puzzle", False, lambda state: any([
            oos_can_jump_3_wide_pit(state, player),
            oos_has_magnet_gloves(state, player)
        ])],
        ["d7 pot room", "d7 magunesu chest", False, lambda state: oos_has_cane(state, player)],

        ["d7 armos puzzle", "d7 magunesu chest", False, lambda state: all([
            oos_can_kill_magunesu(state, player),
            oos_has_magnet_gloves(state, player),
            any([
                oos_can_jump_3_wide_pit(state, player),
                all([
                    # Really precise bomb jumps to cross the 3-holes
                    oos_option_hell_logic(state, player),
                    oos_can_jump_2_wide_liquid(state, player)
                ])
            ])
        ])],

        # 2 keys
        ["d7 pot room", "d7 quicksand chest", False, lambda state: all([
            oos_has_small_keys(state, player, 7, 2),
            oos_has_feather(state, player)
        ])],
        ["d7 pot room", "d7 water stairs", False, lambda state: all([
            # poe skip 2 : https://youtu.be/MIMm6q_yGyQ
            oos_option_hell_logic(state, player),
            oos_has_small_keys(state, player, 7, 2),
            oos_has_bombs(state, player),
            oos_has_cape(state, player),
            oos_can_use_pegasus_seeds(state, player),
            oos_has_flippers(state, player),
            state.has("Swimmer's Ring", player)
        ])],

        # 3 keys
        ["d7 pot room", "enter poe B", False, lambda state: all([
            oos_has_small_keys(state, player, 7, 3),
            oos_can_use_ember_seeds(state, player, False),
            any([
                oos_can_use_pegasus_seeds(state, player),
                # Hard logic can do it without pegasus, it's very tight but doable
                oos_option_hard_logic(state, player)
            ])
        ])],

        ["enter poe B", "d7 water stairs", False, lambda state: oos_has_flippers(state, player)],

        ["d7 water stairs", "d7 darknut bridge trampolines", False, lambda state: any([
            all([
                # Boomerang to activate the switch then magnet gloves to go to the trampolines
                oos_has_magnet_gloves(state, player),
                oos_has_magic_boomerang(state, player)
            ]),
            all([
                oos_option_hard_logic(state, player),
                oos_has_feather(state, player),
                oos_has_magnet_gloves(state, player)
            ]),
        ])],
        ["d7 water stairs", "d7 past darknut bridge", False, lambda state: any([
            # Just jump to the other side directly
            oos_can_jump_4_wide_pit(state, player),
            oos_has_tight_switch_hook(state, player),  # or hook to the other side

            all([
                oos_has_seed_thrower(state, player),
                oos_has_scent_seeds(state, player)
            ]),
            all([
                # Kill one darknut then pull the others
                oos_has_magnet_gloves(state, player),
                any([
                    oos_can_kill_armored_enemy(state, player, True, True),
                    oos_has_shield(state, player),  # To push the darknut, the rod not really working
                    # Pull the right darknut by just going and stalling in the hole
                    oos_option_medium_logic(state, player),
                ])
            ]),
            oos_shoot_beams(state, player)
        ])],
        ["d7 past darknut bridge", "d7 darknut bridge trampolines", False, lambda state: any([
            # Reach trampolines directly
            oos_can_jump_3_wide_pit(state, player),

            all([
                any([
                    # Trigger the spinner switch
                    oos_has_sword(state, player),
                    oos_has_fools_ore(state, player),
                    oos_has_rod(state, player),
                    oos_has_bombs(state, player),
                    oos_has_bombchus(state, player, 5)
                ]),
                # Reach trampolines using the magnet gloves
                oos_has_feather(state, player),
                oos_has_magnet_gloves(state, player)
            ])
        ])],

        ["d7 darknut bridge trampolines", "d7 spike chest", False, lambda state: oos_can_kill_stalfos(state, player)],

        # 4 keys
        ["d7 water stairs", "d7 maze chest", False, lambda state: all([
            oos_has_small_keys(state, player, 7, 4),
            any([
                oos_can_kill_armored_enemy(state, player, False, False),
                all([
                    oos_can_kill_moldorm(state, player,
                                         pit_available=oos_option_medium_logic(state, player)),
                    any([
                        # Kill poe sisters
                        oos_has_rod(state, player),
                        all([
                            # 18 embers are needed to kill the boss
                            oos_has_ember_seeds(state, player),
                            any([
                                oos_option_hard_logic(state, player),
                                oos_can_harvest_regrowing_bush(state, player),  # refill embers in the middle
                                oos_has_satchel(state, player, 2)
                            ])
                        ])
                    ]),
                ])
            ]),
            any([
                oos_can_jump_3_wide_liquid(state, player),  # Technically not a liquid but a diagonal pit
                all([
                    # Switch hook from above with the pot next to the button then jump in the hole
                    oos_option_medium_logic(state, player),
                    oos_has_switch_hook(state, player)
                ])
                # Casual could switch 2 from the left, but they'd have to jump in the hole to move out
                # which is against casual logic's spirit
            ])
        ])],

        ["d7 maze chest", "d7 B2F drop", False, lambda state: any([
            oos_has_magnet_gloves(state, player),
            all([
                # The jumps in this room being pretty intricate, precise and counterintuitive,
                # we chose to put that in hard logic only.
                oos_option_hard_logic(state, player),
                oos_can_jump_6_wide_pit(state, player)
            ])
        ])],

        # 5 keys
        ["enter d7", "d7 stalfos chest", False, lambda state: all([
            oos_has_small_keys(state, player, 7, 4),
            oos_self_locking_small_key(state, player, "d7 stalfos chest", 7),
            any([
                oos_can_jump_5_wide_pit(state, player),
                all([
                    oos_option_hard_logic(state, player),
                    oos_can_jump_1_wide_pit(state, player, False)
                ])
            ]),
            oos_can_kill_stalfos(state, player),
        ])],
        ["d7 maze chest", "d7 stalfos chest", False, lambda state: all([
            oos_has_small_keys(state, player, 7, 5),
            any([
                oos_can_jump_5_wide_pit(state, player),
                all([
                    oos_option_hard_logic(state, player),
                    oos_can_jump_1_wide_pit(state, player, False)
                ])
            ]),
            oos_can_kill_stalfos(state, player),
        ])],

        ["d7 stalfos chest", "shining blue owl", False, lambda state: oos_can_use_mystery_seeds(state, player)],

        ["enter d7", "d7 right of entrance", False, lambda state: all([
            oos_can_kill_normal_enemy(state, player),
            any([
                oos_has_small_keys(state, player, 7, 5),
                all([
                    oos_has_small_keys(state, player, 7, 1),
                    oos_self_locking_small_key(state, player, "d7 right of entrance", 7)
                ])
            ])
        ])],

        ["d7 maze chest", "d7 boss", False, lambda state: all([
            oos_has_boss_key(state, player, 7),
            any([
                oos_has_sword(state, player),
                oos_has_fools_ore(state, player),
                # oos_can_punch(state, player)
            ])
        ])]
    ]


def make_d8_logic(player: int):
    return [
        # 0 keys
        ["enter d8", "d8 eye drop", False, lambda state: all([
            oos_can_break_pot(state, player),
            any([
                oos_has_seed_thrower(state, player),
                all([
                    oos_option_medium_logic(state, player),
                    oos_has_feather(state, player),
                    any([
                        oos_can_use_ember_seeds(state, player, False),
                        oos_can_use_scent_seeds(state, player),
                        oos_can_use_mystery_seeds(state, player),
                    ])
                ])
            ])
        ])],

        ["enter d8", "d8 three eyes chest", False, lambda state: all([
            oos_has_feather(state, player),
            any([
                oos_has_hyper_slingshot(state, player),
                all([
                    oos_option_hell_logic(state, player),
                    any([
                        oos_has_satchel(state, player),
                    ]),
                    any([
                        oos_can_use_ember_seeds(state, player, False),
                        oos_can_use_scent_seeds(state, player),
                        oos_can_use_mystery_seeds(state, player),
                    ])
                ]),
                all([
                    oos_option_hell_logic(state, player),
                    oos_has_slingshot(state, player),
                    any([
                        oos_can_use_ember_seeds(state, player, False),
                        oos_can_use_scent_seeds(state, player),
                        oos_can_use_pegasus_seeds(state, player),
                        oos_can_use_mystery_seeds(state, player),
                    ])
                ]),
                all([
                    oos_option_hell_logic(state, player),
                    oos_has_shooter(state, player),
                    any([
                        oos_can_use_ember_seeds(state, player, False),
                        oos_can_use_scent_seeds(state, player),
                        oos_can_use_pegasus_seeds(state, player),
                        oos_can_use_mystery_seeds(state, player),
                    ])
                ])
            ])
        ])],

        ["enter d8", "d8 hardhat room", False, lambda state: oos_can_kill_magunesu(state, player)],

        ["d8 hardhat room", "d8 hardhat drop", False, lambda state: any([
            all([
                oos_can_remove_rockslide(state, player, False),  # For the bombchus, leave the hardhat stuck in the upper line to guide the bombchus
                oos_has_magnet_gloves(state, player)
            ]),
            oos_can_use_gale_seeds_offensively(state, player)
        ])],

        # 1 key
        ["d8 hardhat room", "d8 spike room", False, lambda state: all([
            oos_has_small_keys(state, player, 8, 1),
            any([
                oos_has_cape(state, player),
                all([  # Tight 2D section jump is hard mode without cape
                    oos_option_hard_logic(state, player),
                    oos_has_feather(state, player),
                    oos_can_use_pegasus_seeds(state, player)
                ])
            ])
        ])],

        # 2 keys
        ["d8 spike room", "d8 spinner", False, lambda state: oos_has_small_keys(state, player, 8, 2)],
        ["d8 spinner", "silent watch owl", False, lambda state: oos_can_use_mystery_seeds(state, player)],
        ["d8 spinner", "d8 magnet ball room", False, None],
        ["d8 spinner", "d8 armos chest", False, lambda state: any([
            oos_has_magnet_gloves(state, player),
            all([
                # Clip into the block right of staircase with pegasus seeds and use the cane of somaria to activate the bridge, save&exit and redo the whole dungeon to get to the other side
                oos_option_hard_logic(state, player),
                oos_can_use_pegasus_seeds(state, player),
                oos_has_cane(state, player)
            ])
        ])],
        ["d8 armos chest", "d8 spinner chest", False, None],
        ["d8 spinner chest", "frypolar entrance", False, lambda state: oos_has_magnet_gloves(state, player)],
        ["frypolar entrance", "frypolar owl", False, lambda state: oos_can_use_mystery_seeds(state, player)],
        ["frypolar entrance", "d8 darknut chest", False, lambda state: all([
            any([
                oos_has_hyper_slingshot(state, player),
                all([
                    oos_option_hell_logic(state, player),
                    any([
                        oos_has_satchel(state, player),
                    ]),
                    any([
                        oos_can_use_ember_seeds(state, player, False),
                        oos_can_use_scent_seeds(state, player),
                        oos_can_use_mystery_seeds(state, player),
                    ])
                ]),
                all([
                    oos_option_hell_logic(state, player),
                    oos_has_slingshot(state, player),
                    any([
                        oos_can_use_ember_seeds(state, player, False),
                        oos_can_use_scent_seeds(state, player),
                        oos_can_use_pegasus_seeds(state, player),
                        oos_can_use_mystery_seeds(state, player),
                    ])
                ]),
                all([
                    # This one is way easier to time by just bouncing on the left
                    # then going down as the seed spawns in the eye
                    oos_option_hard_logic(state, player),
                    oos_has_shooter(state, player),
                    any([
                        oos_can_use_ember_seeds(state, player, False),
                        oos_can_use_scent_seeds(state, player),
                        oos_can_use_pegasus_seeds(state, player),
                        oos_can_use_mystery_seeds(state, player),
                    ])
                ])
            ]),
            # oos_can_kill_armored_enemy(state, player),
            oos_can_remove_rockslide(state, player, False),
        ])],
        ["frypolar entrance", "frypolar room", False, lambda state: oos_has_small_keys(state, player, 8, 3)],
        ["frypolar room", "frypolar room wild mystery", False, lambda state: \
            oos_can_harvest_regrowing_bush(state, player)],

        # 3 keys
        ["frypolar room", "d8 ice puzzle room", False, lambda state: all([
            # Hard-require HSS since we need it in the room right after Frypolar to hit the torches anyway
            oos_has_hyper_slingshot(state, player),

            # Requirements to kill Frypolar
            any([
                all([
                    # Casual logic: mystery seeds method is considered mandatory since it's the easiest one
                    oos_has_mystery_seeds(state, player),
                    oos_has_bracelet(state, player)
                ]),
                all([
                    # Medium logic: allow killing Frypolar with ember only, but with at least a Lv2 satchel
                    # (the miniboss require 15 embers to die, so 20 max is a bit tight)
                    oos_option_medium_logic(state, player),
                    oos_can_use_ember_seeds(state, player, False),
                    oos_has_satchel(state, player, 2),
                ]),
                all([
                    # Hard logic: yolo
                    oos_option_hard_logic(state, player),
                    oos_can_use_ember_seeds(state, player, False)
                ]),
            ]),

            # Requirements to pass the room after Frypolar
            oos_can_use_ember_seeds(state, player, False),
        ])],

        ["d8 ice puzzle room", "d8 pols voice chest", False, lambda state: any([
            oos_has_magic_boomerang(state, player),
            oos_can_jump_6_wide_pit(state, player),
            oos_has_shooter(state, player),
            all([
                oos_option_medium_logic(state, player),
                oos_has_bombchus(state, player, 2)
            ])
        ])],

        # 4 keys
        ["d8 ice puzzle room", "d8 crystal room", False, lambda state: oos_has_small_keys(state, player, 8, 4)],
        ["d8 crystal room", "magical ice owl", False, lambda state: oos_can_use_mystery_seeds(state, player)],
        ["d8 crystal room", "d8 ghost armos drop", False, lambda state: oos_can_remove_rockslide(state, player, False)],
        ["d8 crystal room", "d8 NE crystal", False, lambda state: all([
            oos_has_bracelet(state, player),
            oos_can_trigger_lever(state, player)
        ])],
        ["d8 crystal room", "d8 SE crystal", False, lambda state: oos_has_bracelet(state, player)],
        ["d8 crystal room", "d8 SW lava chest", False, None],
        ["d8 SE crystal", "d8 SE lava chest", False, None],

        ["d8 SE crystal", "d8 spark chest", False, None],
        ["d8 ice puzzle room", "d8 spark chest", False, lambda state: all([
            # Switch hook from the ice puzzle, then s&q
            oos_option_medium_logic(state, player),
            oos_has_switch_hook(state, player)
        ])],

        # 6 keys
        ["d8 crystal room", "d8 NW crystal", False, lambda state: all([
            oos_has_bracelet(state, player),
            oos_has_small_keys(state, player, 8, 6)
        ])],
        ["d8 crystal room", "d8 SW crystal", False, lambda state: all([
            oos_has_bracelet(state, player),
            oos_has_small_keys(state, player, 8, 6)
        ])],

        # 7 keys
        ["d8 NW crystal", "d8 boss", False, lambda state: all([
            oos_has_small_keys(state, player, 8, 7),
            oos_has_boss_key(state, player, 8),
            any([
                oos_has_sword(state, player),
                oos_has_fools_ore(state, player)
            ])
        ])],
    ]
