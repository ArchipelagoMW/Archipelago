from BaseClasses import CollectionState
from Options import Accessibility
from ..Constants import DUNGEON_NAMES, ESSENCES


# Items predicates ############################################################

def ooa_has_sword(state: CollectionState, player: int, accept_biggoron: bool = True):
    return any([
        state.has("Progressive Sword", player),
        accept_biggoron and state.has("Biggoron's Sword", player)
    ])


def ooa_has_noble_sword(state: CollectionState, player: int):
    return state.has("Progressive Sword", player, 2)


def ooa_has_shield(state: CollectionState, player: int):
    return state.has("Progressive Shield", player)


def ooa_has_feather(state: CollectionState, player: int):
    return state.has("Feather", player)


def ooa_has_satchel(state: CollectionState, player: int, level: int = 1):
    return state.has("Seed Satchel", player, level)


def ooa_has_seedshooter(state: CollectionState, player: int):
    return state.has("Seed Shooter", player)


def ooa_has_boomerang(state: CollectionState, player: int):
    return state.has("Boomerang", player)


def ooa_has_cane(state: CollectionState, player: int):
    return state.has("Cane of Somaria", player)

def ooa_has_bracelet(state: CollectionState, player: int):
    return state.has("Progressive Bracelet", player)

def ooa_has_glove(state: CollectionState, player: int):
    return state.has("Progressive Bracelet", player, 2)

def ooa_has_shovel(state: CollectionState, player: int):
    return state.has("Shovel", player)

def ooa_has_flippers(state: CollectionState, player: int):
    return state.has("Progressive Flippers", player)

def ooa_has_siren_suit(state: CollectionState, player: int):
    return state.has("Progressive Flippers", player, 2)

def ooa_has_switch_hook(state: CollectionState, player: int):
    return state.has("Progressive Hook", player)

def ooa_has_long_hook(state: CollectionState, player: int):
    return state.has("Progressive Hook", player, 2)


def ooa_has_ember_seeds(state: CollectionState, player: int):
    return any([
        state.has("Ember Seeds", player),
        state.multiworld.worlds[player].options.default_seed == "ember",
        (state.has("_wild_ember_seeds", player) and ooa_option_medium_logic(state, player))
    ])


def ooa_has_scent_seeds(state: CollectionState, player: int):
    return state.has("Scent Seeds", player) or state.multiworld.worlds[player].options.default_seed == "scent"


def ooa_has_pegasus_seeds(state: CollectionState, player: int):
    return state.has("Pegasus Seeds", player) or state.multiworld.worlds[player].options.default_seed == "pegasus"


def ooa_has_mystery_seeds(state: CollectionState, player: int):
    return any([
        state.has("Mystery Seeds", player),
        state.multiworld.worlds[player].options.default_seed == "mystery",
        (state.has("_wild_mystery_seeds", player) and ooa_option_medium_logic(state, player))
    ])


def ooa_has_gale_seeds(state: CollectionState, player: int):
    return state.has("Gale Seeds", player) or state.multiworld.worlds[player].options.default_seed == "gale"


def ooa_has_small_keys(state: CollectionState, player: int, dungeon_id: int, amount: int = 1):
    return (state.has(f"Small Key ({DUNGEON_NAMES[dungeon_id]})", player, amount)
            or state.has(f"Master Key ({DUNGEON_NAMES[dungeon_id]})", player))

def ooa_has_boss_key(state: CollectionState, player: int, dungeon_id: int):
    # Specific case for D6 Past, because of course D6 is mess.
    if (dungeon_id == 9):
        return any([
            state.has("Boss Key (Mermaid's Cave)", player),
            all([
                state.multiworld.worlds[player].options.master_keys == "all_dungeon_keys",
                state.has(f"Master Key ({DUNGEON_NAMES[dungeon_id]})", player)
            ])
        ])

    return any([
        state.has(f"Boss Key ({DUNGEON_NAMES[dungeon_id]})", player),
        all([
            state.multiworld.worlds[player].options.master_keys == "all_dungeon_keys",
            state.has(f"Master Key ({DUNGEON_NAMES[dungeon_id]})", player)
        ])
    ])


# Options and generation predicates ###########################################

def ooa_option_medium_logic(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.logic_difficulty in ["medium", "hard"]


def ooa_option_hard_logic(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.logic_difficulty == "hard"


def ooa_is_companion_ricky(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.animal_companion == "ricky"


def ooa_is_companion_moosh(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.animal_companion == "moosh"


def ooa_is_companion_dimitri(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.animal_companion == "dimitri"


def ooa_has_essences(state: CollectionState, player: int, target_count: int):
    essence_count = [state.has(essence, player) for essence in ESSENCES].count(True)
    return essence_count >= target_count


def ooa_has_essences_for_maku_seed(state: CollectionState, player: int):
    return ooa_has_essences(state, player, state.multiworld.worlds[player].options.required_essences.value)
    
def ooa_has_slates(state: CollectionState, player: int, target_count):
    return state.has("Slate", player, target_count)
    
def ooa_has_enough_slates(state: CollectionState, player: int):
    return ooa_has_slates(state, player, state.multiworld.worlds[player].options.required_slates.value)


# Various item predicates ###########################################

def ooa_has_rupees(state: CollectionState, player: int, amount: int):
    # Rupee checks being quite approximative, being able to farm is a
    # must-have to prevent any stupid lock
    if not ooa_can_farm_rupees(state, player):
        return False

    rupees = state.count("Rupees (1)", player)
    rupees += state.count("Rupees (5)", player) * 5
    rupees += state.count("Rupees (10)", player) * 10
    rupees += state.count("Rupees (20)", player) * 20
    rupees += state.count("Rupees (50)", player) * 50
    rupees += state.count("Rupees (100)", player) * 100
    rupees += state.count("Rupees (200)", player) * 200

    # Secret rooms inside D2 and D6 containing loads of rupees, but only in medium logic
    if ooa_option_medium_logic(state, player):
        if state.has("_reached_d2_rupee_room", player):
            rupees += 150
        if state.has("_reached_d6_rupee_room", player):
            rupees += 90

    ## Old men giving and taking rupees
    #world = state.multiworld.worlds[player]
    #for region_name, value in world.old_man_rupee_values.items():
    #    event_name = "rupees from " + region_name
    #    if state.has(event_name, player):
    #        rupees += value

    return rupees >= amount


def ooa_can_farm_rupees(state: CollectionState, player: int):
    # Having Ember Seeds and a weapon or a shovel is enough to guarantee that we can reach
    # a significant amount of rupees
    return ooa_has_sword(state, player) or ooa_has_shovel(state, player)



def ooa_can_trigger_switch(state: CollectionState, player: int):
    return any([
        ooa_has_boomerang(state, player),
        ooa_has_bombs(state, player),
        ooa_has_seedshooter(state, player),
        all([
            ooa_has_satchel(state, player),
            any([
                ooa_has_ember_seeds(state, player),
                ooa_has_scent_seeds(state, player),
                ooa_has_mystery_seeds(state, player)
            ])
        ]),
        ooa_has_sword(state, player),
        ooa_has_switch_hook(state, player),
        ooa_can_punch(state, player),
    ])

def ooa_can_trigger_far_switch(state: CollectionState, player: int):
    return any([
        ooa_has_boomerang(state, player),
        ooa_has_bombs(state, player),
        ooa_has_seedshooter(state, player),
        ooa_has_switch_hook(state, player),
        all([
            ooa_option_medium_logic(state, player),
            ooa_has_sword(state, player, False),
            state.has("Energy Ring", player)
        ])
        # TODO: Regular beams?
    ])


def ooa_has_bombs(state: CollectionState, player: int, amount: int = 1):
    return state.has("Bombs (10)", player, amount)


def ooa_has_flute(state: CollectionState, player: int):
    return any([
        ooa_can_summon_ricky(state, player),
        ooa_can_summon_moosh(state, player),
        ooa_can_summon_dimitri(state, player)
    ])


def ooa_can_summon_ricky(state: CollectionState, player: int):
    return state.has("Ricky's Flute", player)


def ooa_can_summon_moosh(state: CollectionState, player: int):
    return state.has("Moosh's Flute", player)


def ooa_can_summon_dimitri(state: CollectionState, player: int):
    return state.has("Dimitri's Flute", player)

def ooa_can_open_portal(state: CollectionState, player: int):
    return state.has("Progressive Harp", player)

def ooa_can_go_back_to_present(state: CollectionState, player: int):
    return state.has("Progressive Harp", player, 2)

def ooa_can_switch_past_and_present(state: CollectionState, player: int):
    return state.has("Progressive Harp", player, 3)

# Jump-related predicates ###########################################

def ooa_can_jump_1_wide_liquid(state: CollectionState, player: int, can_summon_companion: bool):
    return any([
        ooa_has_feather(state, player),
        all([
            ooa_option_medium_logic(state, player),
            can_summon_companion,
            ooa_can_summon_ricky(state, player)
        ])
    ])


def ooa_can_jump_2_wide_liquid(state: CollectionState, player: int):
    return any([
        all([
            ooa_has_feather(state, player),
            ooa_can_use_pegasus_seeds(state, player)
        ]),
        all([
            # Hard logic expects bomb jumps over 2-wide liquids
            ooa_option_hard_logic(state, player),
            ooa_has_feather(state, player),
            ooa_has_bombs(state, player)
        ])
    ])


def ooa_can_jump_3_wide_liquid(state: CollectionState, player: int):
    return any([
        all([
            ooa_option_hard_logic(state, player),
            ooa_has_feather(state, player),
            ooa_can_use_pegasus_seeds(state, player),
            ooa_has_bombs(state, player),
        ])
    ])

def ooa_can_jump_1_wide_pit(state: CollectionState, player: int, can_summon_companion: bool):
    return any([
        ooa_has_feather(state, player),
        all([
            can_summon_companion,
            any([
                ooa_can_summon_moosh(state, player),
                ooa_can_summon_ricky(state, player)
            ])
        ])
    ])


def ooa_can_jump_2_wide_pit(state: CollectionState, player: int, can_summon_companion: bool):
    return any([
        all([
            ooa_has_feather(state, player),
            any([
                # Medium logic expects player to be able to jump above 2-wide pits without pegasus seeds
                ooa_option_medium_logic(state, player),
                ooa_can_use_pegasus_seeds(state, player)
            ])
        ]),
        all([
            can_summon_companion,
            ooa_can_summon_moosh(state, player)
        ])
    ])


def ooa_can_jump_3_wide_pit(state: CollectionState, player: int, can_summon_companion: bool):
    return any([
        all([
            ooa_option_medium_logic(state, player),
            ooa_has_feather(state, player),
            ooa_can_use_pegasus_seeds(state, player),
        ]),
        all([
            can_summon_companion,
            ooa_can_summon_moosh(state, player)
        ])
    ])

def ooa_can_jump_4_wide_pit(state: CollectionState, player: int, can_summon_companion: bool):
    return all([
        can_summon_companion,
        ooa_can_summon_moosh(state, player)
    ])

# Seed-related predicates ###########################################

def ooa_can_use_seeds(state: CollectionState, player: int):
    return ooa_has_seedshooter(state, player) or ooa_has_satchel(state, player)

def ooa_has_seed_kind_count(state: CollectionState, player: int, count: int):
    seedCount = 0
    seedCount += 1 if ooa_has_ember_seeds(state, player) else 0
    seedCount += 1 if ooa_has_mystery_seeds(state, player) else 0
    seedCount += 1 if ooa_has_scent_seeds(state, player) else 0
    seedCount += 1 if ooa_has_pegasus_seeds(state, player) else 0
    seedCount += 1 if ooa_has_gale_seeds(state, player) else 0
    return seedCount >= count

def ooa_can_use_ember_seeds(state: CollectionState, player: int, accept_mystery_seeds: bool):
    return all([
        ooa_can_use_seeds(state, player),
        any([
            ooa_has_ember_seeds(state, player),
            all([
                # Medium logic expects the player to know they can use mystery seeds
                # to randomly get the ember effect in some cases
                accept_mystery_seeds,
                ooa_option_medium_logic(state, player),
                ooa_has_mystery_seeds(state, player),
            ])
        ])
    ])


def ooa_can_use_scent_seeds_offensively(state: CollectionState, player: int):
    return all([
        any([
            ooa_has_seedshooter(state, player),
            all([
                ooa_option_hard_logic(state, player),
                ooa_has_satchel(state, player)
            ])
        ]),
        ooa_has_scent_seeds(state, player)
    ])

def ooa_can_use_scent_seeds_for_smell(state: CollectionState, player: int):
    return all([
        ooa_has_satchel(state, player),
        ooa_has_scent_seeds(state, player)
    ])

def ooa_can_use_pegasus_seeds(state: CollectionState, player: int):
    return all([
        # Unlike other seeds, pegasus only have an interesting effect with the satchel
        ooa_has_satchel(state, player),
        ooa_has_pegasus_seeds(state, player)
    ])

def ooa_can_use_pegasus_seeds_for_stun(state: CollectionState, player: int):
    return all([
        ooa_has_seedshooter(state, player),
        ooa_has_pegasus_seeds(state, player)
    ])

def ooa_can_warp_using_gale_seeds(state: CollectionState, player: int):
    return all([
        ooa_has_satchel(state, player),
        ooa_has_gale_seeds(state, player)
    ])


def ooa_can_use_gale_seeds_offensively(state: CollectionState, player: int, ranged: bool = False):
    # If we don't have gale seeds or aren't at least in medium logic, don't even try
    if not ooa_has_gale_seeds(state, player) or not ooa_option_medium_logic(state, player):
        return False

    return any([
        ooa_has_seedshooter(state, player),
        all([
            not ranged,
            ooa_has_satchel(state, player),
            any([
                ooa_option_hard_logic(state, player),
                ooa_has_feather(state, player)
            ]),
        ])
    ])


def ooa_can_use_mystery_seeds(state: CollectionState, player: int):
    return all([
        ooa_can_use_seeds(state, player),
        ooa_has_mystery_seeds(state, player)
    ])


# Break / kill predicates ###########################################

def ooa_can_break_bush(state: CollectionState, player: int, can_summon_companion: bool = False):
    return any([
        ooa_has_sword(state, player),
        ooa_has_bracelet(state, player),
        ooa_has_switch_hook(state, player),
        (can_summon_companion and ooa_has_flute(state, player)),
        all([
            # Consumables need at least medium logic, since they need a good knowledge of the game
            # not to be frustrating
            ooa_option_medium_logic(state, player),
            any([
                ooa_has_bombs(state, player, 2),
                ooa_can_use_ember_seeds(state, player, False),
                (ooa_has_seedshooter(state, player) and ooa_has_gale_seeds(state, player)),
            ])
        ]),
    ])

def ooa_can_break_tingle_balloon(state: CollectionState, player: int):
    return any([
        ooa_has_sword(state, player),
        ooa_has_boomerang(state, player),
        #ooa_can_punch(state, player), ?
    ]) and ooa_has_feather(state, player)


def ooa_can_harvest_regrowing_bush(state: CollectionState, player: int, allow_bombs: bool = True):
    return any([
        ooa_has_sword(state, player),
        (allow_bombs and ooa_has_bombs(state, player))
    ])


def ooa_can_break_pot(state: CollectionState, player: int):
    return any([
        ooa_has_bracelet(state, player),
        ooa_has_noble_sword(state, player),
        ooa_has_switch_hook(state, player),
        state.has("Biggoron's Sword", player)
    ])


def ooa_can_break_flowers(state: CollectionState, player: int, can_summon_companion: bool):
    return any([
        ooa_has_sword(state, player),
        (can_summon_companion and ooa_has_flute(state, player)),
        all([
            # Consumables need at least medium logic, since they need a good knowledge of the game
            # not to be frustrating
            ooa_option_medium_logic(state, player),
            any([
                ooa_has_bombs(state, player, 2),
                ooa_can_use_ember_seeds(state, player, False),
                (ooa_has_seedshooter(state, player) and ooa_has_gale_seeds(state, player)),
            ])
        ]),
    ])


def ooa_can_break_crystal(state: CollectionState, player: int):
    return any([
        ooa_has_sword(state, player),
        ooa_has_bombs(state, player),
        ooa_has_bracelet(state, player),
        all([
            ooa_option_medium_logic(state, player),
            state.has("Expert's Ring", player)
        ])
    ])


def ooa_can_break_sign(state: CollectionState, player: int):
    return any([
        ooa_has_noble_sword(state, player),
        state.has("Biggoron's Sword", player),
        ooa_has_bracelet(state, player),
        ooa_can_use_ember_seeds(state, player, False),
    ])


def ooa_can_harvest_tree(state: CollectionState, player: int, can_use_companion: bool):
    return all([
        ooa_can_use_seeds(state, player),
        any([
            ooa_has_sword(state, player),
            ooa_can_punch(state, player),
            all([
                can_use_companion,
                ooa_option_medium_logic(state, player),
                ooa_can_summon_dimitri(state, player)
            ])
        ])
    ])


def ooa_can_push_enemy(state: CollectionState, player: int):
    return any([
        #ooa_has_rod(state, player),
        ooa_has_shield(state, player)
    ])


def ooa_can_kill_normal_enemy(state: CollectionState, player: int, can_kill_with_hook: bool = False, pit_available: bool = False):
    # If a pit is avaiable nearby, it can be used to put the enemies inside using
    # items that are usually non-lethal
    if pit_available and ooa_can_push_enemy(state, player):
        return True

    return any([
        ooa_has_sword(state, player),
        ooa_can_kill_normal_using_satchel(state, player),
        ooa_can_kill_normal_using_seedshooter(state, player),
        (ooa_option_medium_logic(state, player) and ooa_has_bombs(state, player, 4)),
        (ooa_option_medium_logic(state, player) and ooa_has_cane(state, player)),
        ooa_can_punch(state, player),
        can_kill_with_hook and ooa_has_switch_hook(state, player),
    ])

def ooa_can_kill_moldorm(state:CollectionState, player:int, pit_available:bool=False):
    if pit_available and ooa_can_push_enemy(state, player):
        return True

    return any([
        ooa_has_sword(state, player),
        ooa_can_use_scent_seeds_offensively(state, player),
        # Not including mystery seed, because even in hard logic this is just pure torture
        (ooa_option_medium_logic(state, player) and ooa_has_bombs(state, player, 4)),
        (ooa_option_medium_logic(state, player) and ooa_has_cane(state, player)),
        ooa_can_punch(state, player),
        ooa_has_switch_hook(state, player),
    ])

def ooa_can_kill_wizzrobes(state:CollectionState, player:int, pit_available:bool=False):
    if pit_available and ooa_can_push_enemy(state, player):
        return True

    return any([
        ooa_has_sword(state, player),
        ooa_can_kill_normal_using_satchel(state, player),
        ooa_can_kill_normal_using_seedshooter(state, player),
        (ooa_option_medium_logic(state, player) and ooa_has_bombs(state, player, 4)),
        ooa_can_punch(state, player),
    ])

def ooa_generic_boss_and_miniboss_kill(state:CollectionState, player:int):
    return any([
        ooa_has_sword(state, player),
        ooa_can_use_scent_seeds_offensively(state, player),
        # TODO : Check bombs damage on bosses
        #(ooa_option_medium_logic(state, player) and ooa_has_bombs(state, player, 4)),
        ooa_can_punch(state, player),
        ooa_has_switch_hook(state, player),
    ])

def ooa_can_kill_underwater(state: CollectionState, player: int, can_kill_with_hook: bool = False):
    return any([
        ooa_has_sword(state, player),
        ooa_can_kill_normal_using_seedshooter(state, player),
        ooa_can_punch(state, player),
        can_kill_with_hook and ooa_has_switch_hook(state, player),
    ])

def ooa_can_kill_normal_using_satchel(state: CollectionState, player: int):
    # Expect a 50+ seed satchel to ensure we can chain dungeon rooms to some extent if that's our only kill option
    if not ooa_has_satchel(state, player, 2):
        return False

    return any([
        # Casual logic => only ember
        ooa_has_ember_seeds(state, player),
        all([
            # Medium logic => allow scent or gale+feather
            ooa_option_medium_logic(state, player),
            any([
                ooa_has_scent_seeds(state, player),
                ooa_has_mystery_seeds(state, player),
                all([
                    ooa_has_gale_seeds(state, player),
                    ooa_has_feather(state, player)
                ])
            ])
        ]),
        all([
            # Hard logic => allow gale without feather
            ooa_option_hard_logic(state, player),
            ooa_has_gale_seeds(state, player)
        ])
    ])


def ooa_can_kill_normal_using_seedshooter(state: CollectionState, player: int):
    # Expect a 50+ seed satchel to ensure we can chain dungeon rooms to some extent if that's our only kill option
    if not ooa_has_satchel(state, player, 2):
        return False

    return all([
        ooa_has_seedshooter(state, player),
        any([
            ooa_has_ember_seeds(state, player),
            ooa_has_scent_seeds(state, player),
            all([
                ooa_option_medium_logic(state, player),
                any([
                    ooa_has_mystery_seeds(state, player),
                    ooa_has_gale_seeds(state, player),
                ])
            ])
        ])
    ])


def ooa_can_kill_armored_enemy(state: CollectionState, player: int):
    return any([
        ooa_has_sword(state, player),
        all([
            ooa_has_satchel(state, player, 2),  # Expect a 50+ seeds satchel to be able to chain rooms in dungeons
            ooa_has_scent_seeds(state, player),
            any([
                ooa_has_seedshooter(state, player),
                ooa_option_medium_logic(state, player)
            ])
        ]),
        (ooa_option_medium_logic(state, player) and ooa_has_cane(state, player)),
        ooa_can_punch(state, player)
    ])


def ooa_can_kill_stalfos(state: CollectionState, player: int):
    return any([
        ooa_can_kill_normal_enemy(state, player)
    ])
    
def ooa_can_kill_pols_voice(state: CollectionState, player: int, ranged: bool = False):
    return any([
        ooa_can_open_portal(state, player),
        ooa_has_flute(state, player),
        ooa_has_bombs(state, player),
        ooa_can_use_gale_seeds_offensively(state, player, ranged)
    ])

def ooa_can_kill_armos(state: CollectionState, player: int, ranged: bool = False):
    return any([
        ooa_has_bombs(state, player),
        ooa_can_use_scent_seeds_offensively(state, player)
        # magic boomrang
    ])


def ooa_can_punch(state: CollectionState, player: int):
    return all([
        ooa_option_medium_logic(state, player),
        any([
            state.has("Fist Ring", player),
            state.has("Expert's Ring", player)
        ])
    ])


def ooa_can_trigger_lever(state: CollectionState, player: int):
    return any([
        ooa_can_trigger_lever_from_minecart(state, player),
        all([
            ooa_option_medium_logic(state, player),
            ooa_has_shovel(state, player)
        ])
    ])


def ooa_can_trigger_lever_from_minecart(state: CollectionState, player: int):
    return any([
        ooa_has_sword(state, player),
        ooa_has_boomerang(state, player),

        # TODO: Test that to ensure our understanding is right
        ooa_can_use_scent_seeds_offensively(state, player),
        ooa_can_use_mystery_seeds(state, player),
        ooa_has_seedshooter(state, player),  # any seed works using slingshot
    ])



def ooa_can_flip_spiked_beetle(state: CollectionState, player: int):
    return any([
        ooa_has_shield(state, player),
        all([
            ooa_option_medium_logic(state, player),
            ooa_has_shovel(state, player)
        ])
    ])


def ooa_can_kill_spiked_beetle(state: CollectionState, player: int):
    return any([
        all([  # Regular flip + kill
            ooa_can_flip_spiked_beetle(state, player),
            any([
                ooa_has_sword(state, player),
                ooa_can_kill_normal_using_satchel(state, player),
                ooa_can_kill_normal_using_seedshooter(state, player)
            ])
        ]),
        # Instant kill using Gale Seeds
        ooa_can_use_gale_seeds_offensively(state, player)
    ])

# Action predicates ###########################################

def ooa_can_swim(state: CollectionState, player: int, can_summon_companion: bool):
    return ooa_has_flippers(state, player) or (can_summon_companion and ooa_can_summon_dimitri(state, player))

def ooa_can_swim_deepwater(state: CollectionState, player: int, can_summon_companion: bool):
    return ooa_has_siren_suit(state, player) or (can_summon_companion and ooa_can_summon_dimitri(state, player))

def ooa_can_dive(state: CollectionState, player: int):
    return ooa_has_siren_suit(state, player)

def ooa_can_remove_rockslide(state: CollectionState, player: int, can_summon_companion: bool):
    return ooa_has_bombs(state, player) or (can_summon_companion and ooa_can_summon_ricky(state, player))

def ooa_can_remove_dirt(state: CollectionState, player: int, can_summon_companion: bool):
    return ooa_has_shovel(state, player) or (can_summon_companion and ooa_has_flute(state, player))

def ooa_can_meet_maple(state: CollectionState, player: int):
    return ooa_can_kill_normal_enemy(state, player)

def ooa_can_toss_ring(state: CollectionState, player: int):
    return all([
        ooa_option_medium_logic(state, player),
        ooa_has_bracelet(state, player),
        state.has("Toss Ring", player)
    ])

# Self-locking items helper predicates ##########################################

def ooa_self_locking_item(state: CollectionState, player: int, region_name: str, item_name: str):
    if state.multiworld.worlds[player].options.accessibility == Accessibility.alias_locations:
        return False

    region = state.multiworld.get_region(region_name, player)
    items_in_region = [location.item for location in region.locations if location.item is not None]
    for item in items_in_region:
        if item.name == item_name and item.player == player:
            return True
    return False


def ooa_self_locking_small_key(state: CollectionState, player: int, region_name: str, dungeon: int):
    item_name = f"Small Key ({DUNGEON_NAMES[dungeon]})"
    return ooa_self_locking_item(state, player, region_name, item_name)

