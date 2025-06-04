from BaseClasses import CollectionState
from Options import Accessibility
from ..Constants import *


# Items predicates ############################################################

def oos_has_sword(state: CollectionState, player: int, accept_biggoron: bool = True):
    return any([
        state.has("Progressive Sword", player),
        accept_biggoron and state.has("Biggoron's Sword", player)
    ])


def oos_has_noble_sword(state: CollectionState, player: int):
    return state.has("Progressive Sword", player, 2)


def oos_has_shield(state: CollectionState, player: int):
    return state.has("Progressive Shield", player)


def oos_has_fools_ore(state: CollectionState, player: int):
    return state.has("Fool's Ore", player)


def oos_has_feather(state: CollectionState, player: int):
    return state.has("Progressive Feather", player)


def oos_has_cape(state: CollectionState, player: int):
    return state.has("Progressive Feather", player, 2)


def oos_has_satchel(state: CollectionState, player: int, level: int = 1):
    return state.has("Seed Satchel", player, level)


def oos_has_slingshot(state: CollectionState, player: int):
    return state.has("Progressive Slingshot", player)


def oos_has_hyper_slingshot(state: CollectionState, player: int):
    return state.has("Progressive Slingshot", player, 2)


def oos_has_boomerang(state: CollectionState, player: int):
    return state.has("Progressive Boomerang", player)


def oos_has_magic_boomerang(state: CollectionState, player: int):
    return state.has("Progressive Boomerang", player, 2)


def oos_has_bracelet(state: CollectionState, player: int):
    return state.has("Power Bracelet", player)


def oos_has_shovel(state: CollectionState, player: int):
    return state.has("Shovel", player)


def oos_has_flippers(state: CollectionState, player: int):
    return state.has("Flippers", player)


def oos_has_season(state: CollectionState, player: int, season: int):
    return state.has(SEASON_ITEMS[season], player)


def oos_has_summer(state: CollectionState, player: int):
    return state.has(SEASON_ITEMS[SEASON_SUMMER], player)


def oos_has_spring(state: CollectionState, player: int):
    return state.has(SEASON_ITEMS[SEASON_SPRING], player)


def oos_has_winter(state: CollectionState, player: int):
    return state.has(SEASON_ITEMS[SEASON_WINTER], player)


def oos_has_autumn(state: CollectionState, player: int):
    return state.has(SEASON_ITEMS[SEASON_AUTUMN], player)


def oos_has_magnet_gloves(state: CollectionState, player: int):
    return state.has("Magnetic Gloves", player)


def oos_has_ember_seeds(state: CollectionState, player: int):
    return any([
        state.has("Ember Seeds", player),
        state.multiworld.worlds[player].options.default_seed == "ember",
        (state.has("_wild_ember_seeds", player) and oos_option_medium_logic(state, player))
    ])


def oos_has_scent_seeds(state: CollectionState, player: int):
    return state.has("Scent Seeds", player) or state.multiworld.worlds[player].options.default_seed == "scent"


def oos_has_pegasus_seeds(state: CollectionState, player: int):
    return state.has("Pegasus Seeds", player) or state.multiworld.worlds[player].options.default_seed == "pegasus"


def oos_has_mystery_seeds(state: CollectionState, player: int):
    return any([
        state.has("Mystery Seeds", player),
        state.multiworld.worlds[player].options.default_seed == "mystery",
        (state.has("_wild_mystery_seeds", player) and oos_option_medium_logic(state, player))
    ])


def oos_has_gale_seeds(state: CollectionState, player: int):
    return state.has("Gale Seeds", player) or state.multiworld.worlds[player].options.default_seed == "gale"


def oos_has_small_keys(state: CollectionState, player: int, dungeon_id: int, amount: int = 1):
    return (state.has(f"Small Key ({DUNGEON_NAMES[dungeon_id]})", player, amount)
            or state.has(f"Master Key ({DUNGEON_NAMES[dungeon_id]})", player))


def oos_has_boss_key(state: CollectionState, player: int, dungeon_id: int):
    return any([
        state.has(f"Boss Key ({DUNGEON_NAMES[dungeon_id]})", player),
        all([
            state.multiworld.worlds[player].options.master_keys == "all_dungeon_keys",
            state.has(f"Master Key ({DUNGEON_NAMES[dungeon_id]})", player)
        ])
    ])


# Options and generation predicates ###########################################

def oos_option_medium_logic(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.logic_difficulty in ["medium", "hard"]


def oos_option_hard_logic(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.logic_difficulty == "hard"


def oos_option_shuffled_dungeons(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.shuffle_dungeons


def oos_option_no_d0_alt_entrance(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.remove_d0_alt_entrance.value


def oos_option_no_d2_alt_entrance(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.remove_d2_alt_entrance.value


def oos_is_companion_ricky(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.animal_companion == "ricky"


def oos_is_companion_moosh(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.animal_companion == "moosh"


def oos_is_companion_dimitri(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.animal_companion == "dimitri"


def oos_get_default_season(state: CollectionState, player: int, area_name: str):
    return state.multiworld.worlds[player].default_seasons[area_name]


def oos_can_remove_season(state: CollectionState, player: int, season: int):
    # Test if player has any other season than the one we want to remove
    return any(
        [state.has(item_name, player) for season_name, item_name in SEASON_ITEMS.items() if season_name != season])


def oos_has_essences(state: CollectionState, player: int, target_count: int):
    essence_count = [state.has(essence, player) for essence in ESSENCES].count(True)
    return essence_count >= target_count


def oos_has_essences_for_maku_seed(state: CollectionState, player: int):
    return oos_has_essences(state, player, state.multiworld.worlds[player].options.required_essences.value)


def oos_has_essences_for_treehouse(state: CollectionState, player: int):
    return oos_has_essences(state, player, state.multiworld.worlds[player].options.treehouse_old_man_requirement.value)


def oos_has_required_jewels(state: CollectionState, player: int):
    target_count = state.multiworld.worlds[player].options.tarm_gate_required_jewels.value
    count = [state.has(jewel, player) for jewel in JEWELS].count(True)
    return count >= target_count


def oos_can_reach_lost_woods_pedestal(state: CollectionState, player: int, allow_default: bool = False):
    world = state.multiworld.worlds[player]
    seasons_in_pedestal_sequence = [season for [_, season] in world.lost_woods_item_sequence]

    return all([
        oos_can_complete_season_sequence(state, player, seasons_in_pedestal_sequence, allow_default),
        any([
            all([
                oos_can_use_ember_seeds(state, player, False),
                state.has("Phonograph", player)
            ]),
            all([
                # if sequence is vanilla, medium+ players are expected to know it
                oos_option_medium_logic(state, player),
                not state.multiworld.worlds[player].options.randomize_lost_woods_item_sequence
            ])
        ])
    ])


def oos_can_complete_lost_woods_main_sequence(state: CollectionState, player: int, allow_default: bool = False):
    world = state.multiworld.worlds[player]
    seasons_in_main_sequence = [season for [_, season] in world.lost_woods_main_sequence]

    return all([
        oos_can_complete_season_sequence(state, player, seasons_in_main_sequence, allow_default),
        any([
            all([
                oos_can_break_mushroom(state, player, False),
                oos_has_shield(state, player)
            ]),
            all([
                # if sequence is vanilla, medium+ players are expected to know it
                oos_option_medium_logic(state, player),
                not state.multiworld.worlds[player].options.randomize_lost_woods_main_sequence
            ])
        ])
    ])


def oos_can_complete_season_sequence(state: CollectionState, player: int, season_sequence: list[int], allow_default: bool = False):
    # In medium logic and above, it is assumed the player can exploit the default season from Lost Woods to cheese
    # the first few seasons of the sequence even if they don't own the matching rod.
    if allow_default and oos_option_medium_logic(state, player):
        default_season = oos_get_default_season(state, player, "LOST_WOODS")
        while len(season_sequence) > 0 and season_sequence[0] == default_season:
            del season_sequence[0]

    return all([
        (SEASON_WINTER not in season_sequence) or oos_has_winter(state, player),
        (SEASON_SPRING not in season_sequence) or oos_has_spring(state, player),
        (SEASON_SUMMER not in season_sequence) or oos_has_summer(state, player),
        (SEASON_AUTUMN not in season_sequence) or oos_has_autumn(state, player)
    ])


def oos_can_beat_required_golden_beasts(state: CollectionState, player: int):
    GOLDEN_BEAST_EVENTS = ["_beat_golden_darknut", "_beat_golden_lynel", "_beat_golden_moblin", "_beat_golden_octorok"]
    beast_count = [state.has(beast, player) for beast in GOLDEN_BEAST_EVENTS].count(True)
    return beast_count >= state.multiworld.worlds[player].options.golden_beasts_requirement.value


# Various item predicates ###########################################

def oos_has_rupees(state: CollectionState, player: int, amount: int):
    # Make free shops sphere 1 as players will get them at the start of the game anyway
    if amount == 0:
        return True
    # Rupee checks being quite approximative, being able to farm is a must-have to prevent any stupid lock
    if not oos_can_farm_rupees(state, player):
        return False
    # In hard logic, having the shovel is equivalent to having an infinite amount of Rupees thanks to RNG manips
    if oos_option_hard_logic(state, player) and oos_has_shovel(state, player):
        return True

    rupees = state.count("Rupees (1)", player)
    rupees += state.count("Rupees (5)", player) * 5
    rupees += state.count("Rupees (10)", player) * 10
    rupees += state.count("Rupees (20)", player) * 20
    rupees += state.count("Rupees (30)", player) * 30
    rupees += state.count("Rupees (50)", player) * 50
    rupees += state.count("Rupees (100)", player) * 100
    rupees += state.count("Rupees (200)", player) * 200

    # Secret rooms inside D2 and D6 containing loads of rupees, but only in medium logic
    if oos_option_medium_logic(state, player):
        if state.has("_reached_d2_rupee_room", player):
            rupees += 150
        if state.has("_reached_d6_rupee_room", player):
            rupees += 90

    # Old men giving and taking rupees
    world = state.multiworld.worlds[player]
    for region_name, value in world.old_man_rupee_values.items():
        event_name = "rupees from " + region_name
        # Always assume bad rupees are obtained, otherwise getting an item could make a shop no longer available and break AP
        if state.has(event_name, player) or value < 0:
            rupees += value

    return rupees >= amount


def oos_has_rupees_for_shop(state: CollectionState, player: int, shop_name: str):
    world = state.multiworld.worlds[player]
    required_rupees = world.shop_rupee_requirements.get(shop_name, 0)
    # In shops, players are expected to buy at most 50% of items (in the vast majority of seeds).
    # For edge cases, the logic ensures player is able to farm to compensate for the missing rupees.
    return oos_has_rupees(state, player, int(required_rupees * 0.50))


def oos_can_farm_rupees(state: CollectionState, player: int):
    # Having a sword or a shovel is enough to guarantee that we can reach a significant amount of rupees
    return oos_has_sword(state, player) or oos_has_shovel(state, player)


def oos_has_ore_chunks(state: CollectionState, player: int, amount: int):
    world = state.multiworld.worlds[player]
    if not world.options.shuffle_golden_ore_spots:
        return oos_can_farm_ore_chunks(state, player)

    if not oos_can_farm_ore_chunks(state, player):
        return False

    ore_chunks = 0
    ore_chunks += state.count("Ore Chunks (10)", player) * 10
    ore_chunks += state.count("Ore Chunks (25)", player) * 25
    ore_chunks += state.count("Ore Chunks (50)", player) * 50
    return ore_chunks >= amount


def oos_can_buy_market(state: CollectionState, player: int):
    world = state.multiworld.worlds[player]
    total_market_price = sum([world.shop_prices[loc] for loc in MARKET_LOCATIONS])
    # In shops, players are expected to buy at most 50% of items (in the vast majority of seeds).
    # For edge cases, the logic ensures player is able to farm to compensate for the missing ore.
    return oos_has_ore_chunks(state, player, int(total_market_price * 0.50))


def oos_can_farm_ore_chunks(state: CollectionState, player: int):
    return any([
        oos_has_shovel(state, player),
        all([
            oos_option_medium_logic(state, player),
            any([
                oos_has_magic_boomerang(state, player),
                oos_has_sword(state, player),
                oos_has_bracelet(state, player)
            ])
        ]),
        all([
            oos_option_hard_logic(state, player),
            state.has("_reached_subrosian_dance_hall", player)
        ])
    ])


def oos_can_date_rosa(state: CollectionState, player: int):
    return state.has("_reached_rosa", player) and state.has("Ribbon", player)


def oos_can_trigger_far_switch(state: CollectionState, player: int):
    return any([
        oos_has_boomerang(state, player),
        oos_has_bombs(state, player),
        oos_has_slingshot(state, player),
        oos_use_energy_ring(state, player)
    ])


def oos_use_energy_ring(state: CollectionState, player: int):
    return all([
        oos_option_medium_logic(state, player),
        oos_has_sword(state, player, False),
        state.has("Energy Ring", player)
    ])


def oos_has_rod(state: CollectionState, player: int):
    return any([
        oos_has_winter(state, player),
        oos_has_summer(state, player),
        oos_has_spring(state, player),
        oos_has_autumn(state, player)
    ])


def oos_has_bombs(state: CollectionState, player: int, amount: int = 1):
    if state.has("Bombs (10)", player, amount):
        return True

    return all([
        # With hard logic, player is expected to know they can get free bombs
        # from D2 moblin room even if they never had bombs before
        (amount == 1),
        oos_option_medium_logic(state, player),
        state.has("_reached_d2_bracelet_room", player),
        oos_can_harvest_regrowing_bush(state, player, False)
    ])


def oos_has_flute(state: CollectionState, player: int):
    return any([
        oos_can_summon_ricky(state, player),
        oos_can_summon_moosh(state, player),
        oos_can_summon_dimitri(state, player)
    ])


def oos_can_summon_ricky(state: CollectionState, player: int):
    return state.has("Ricky's Flute", player)


def oos_can_summon_moosh(state: CollectionState, player: int):
    return state.has("Moosh's Flute", player)


def oos_can_summon_dimitri(state: CollectionState, player: int):
    return state.has("Dimitri's Flute", player)


# Jump-related predicates ###########################################

def oos_can_jump_1_wide_liquid(state: CollectionState, player: int, can_summon_companion: bool):
    return any([
        oos_has_feather(state, player),
        all([
            oos_option_medium_logic(state, player),
            can_summon_companion,
            oos_can_summon_ricky(state, player)
        ])
    ])


def oos_can_jump_2_wide_liquid(state: CollectionState, player: int):
    return any([
        oos_has_cape(state, player),
        all([
            oos_has_feather(state, player),
            oos_can_use_pegasus_seeds(state, player)
        ]),
        all([
            # Hard logic expects bomb jumps over 2-wide liquids
            oos_option_hard_logic(state, player),
            oos_has_feather(state, player),
            oos_has_bombs(state, player)
        ])
    ])


def oos_can_jump_3_wide_liquid(state: CollectionState, player: int):
    return any([
        oos_has_cape(state, player),
        all([
            oos_option_hard_logic(state, player),
            oos_has_feather(state, player),
            oos_can_use_pegasus_seeds(state, player),
            oos_has_bombs(state, player),
        ])
    ])


def oos_can_jump_4_wide_liquid(state: CollectionState, player: int):
    return all([
        oos_has_cape(state, player),
        any([
            oos_can_use_pegasus_seeds(state, player),
            all([
                # Hard logic expects player to be able to cape bomb-jump above 4-wide liquids
                oos_option_hard_logic(state, player),
                oos_has_bombs(state, player)
            ])
        ])
    ])


def oos_can_jump_5_wide_liquid(state: CollectionState, player: int):
    return all([
        oos_has_cape(state, player),
        oos_can_use_pegasus_seeds(state, player),
    ])


def oos_can_jump_1_wide_pit(state: CollectionState, player: int, can_summon_companion: bool):
    return any([
        oos_has_feather(state, player),
        all([
            can_summon_companion,
            any([
                oos_can_summon_moosh(state, player),
                oos_can_summon_ricky(state, player)
            ])
        ])
    ])


def oos_can_jump_2_wide_pit(state: CollectionState, player: int):
    return any([
        oos_has_cape(state, player),
        all([
            oos_has_feather(state, player),
            any([
                # Medium logic expects player to be able to jump above 2-wide pits without pegasus seeds
                oos_option_medium_logic(state, player),
                oos_can_use_pegasus_seeds(state, player)
            ])
        ])
    ])


def oos_can_jump_3_wide_pit(state: CollectionState, player: int):
    return any([
        oos_has_cape(state, player),
        all([
            oos_option_medium_logic(state, player),
            oos_has_feather(state, player),
            oos_can_use_pegasus_seeds(state, player),
        ])
    ])


def oos_can_jump_4_wide_pit(state: CollectionState, player: int):
    return all([
        oos_has_cape(state, player),
        any([
            oos_option_medium_logic(state, player),
            oos_can_use_pegasus_seeds(state, player),
        ])
    ])


def oos_can_jump_5_wide_pit(state: CollectionState, player: int):
    return all([
        oos_has_cape(state, player),
        oos_can_use_pegasus_seeds(state, player),
    ])


def oos_can_jump_6_wide_pit(state: CollectionState, player: int):
    return all([
        oos_option_medium_logic(state, player),
        oos_has_cape(state, player),
        oos_can_use_pegasus_seeds(state, player),
    ])


# Seed-related predicates ###########################################

def oos_can_use_seeds(state: CollectionState, player: int):
    return oos_has_slingshot(state, player) or oos_has_satchel(state, player)


def oos_can_use_ember_seeds(state: CollectionState, player: int, accept_mystery_seeds: bool):
    return all([
        oos_can_use_seeds(state, player),
        any([
            oos_has_ember_seeds(state, player),
            all([
                # Medium logic expects the player to know they can use mystery seeds
                # to randomly get the ember effect in some cases
                accept_mystery_seeds,
                oos_option_medium_logic(state, player),
                oos_has_mystery_seeds(state, player),
            ])
        ])
    ])


def oos_can_use_scent_seeds(state: CollectionState, player: int):
    return all([
        oos_can_use_seeds(state, player),
        oos_has_scent_seeds(state, player)
    ])


def oos_can_use_pegasus_seeds(state: CollectionState, player: int):
    return all([
        # Unlike other seeds, pegasus only have an interesting effect with the satchel
        oos_has_satchel(state, player),
        oos_has_pegasus_seeds(state, player)
    ])


def oos_can_use_gale_seeds_offensively(state: CollectionState, player: int):
    # If we don't have gale seeds or aren't at least in medium logic, don't even try
    if not oos_has_gale_seeds(state, player) or not oos_option_medium_logic(state, player):
        return False

    return any([
        oos_has_slingshot(state, player),
        all([
            oos_has_satchel(state, player),
            any([
                oos_option_hard_logic(state, player),
                oos_has_feather(state, player)
            ]),
        ])
    ])


def oos_can_use_mystery_seeds(state: CollectionState, player: int):
    return all([
        oos_can_use_seeds(state, player),
        oos_has_mystery_seeds(state, player)
    ])


# Break / kill predicates ###########################################

def oos_can_break_bush(state: CollectionState, player: int, can_summon_companion: bool = False):
    return any([
        oos_can_break_flowers(state, player, can_summon_companion),
        oos_has_bracelet(state, player)
    ])


def oos_can_harvest_regrowing_bush(state: CollectionState, player: int, allow_bombs: bool = True):
    return any([
        oos_has_sword(state, player),
        oos_has_fools_ore(state, player),
        (allow_bombs and oos_has_bombs(state, player))
    ])


def oos_can_break_mushroom(state: CollectionState, player: int, can_use_companion: bool):
    return any([
        oos_has_bracelet(state, player),
        all([
            oos_option_medium_logic(state, player),
            any([
                oos_has_magic_boomerang(state, player),
                can_use_companion and oos_can_summon_dimitri(state, player)
            ])
        ]),
    ])


def oos_can_break_pot(state: CollectionState, player: int):
    return any([
        oos_has_bracelet(state, player),
        oos_has_noble_sword(state, player),
        state.has("Biggoron's Sword", player)
    ])


def oos_can_break_flowers(state: CollectionState, player: int, can_summon_companion: bool = False):
    return any([
        oos_has_sword(state, player),
        oos_has_magic_boomerang(state, player),
        (can_summon_companion and oos_has_flute(state, player)),
        all([
            # Consumables need at least medium logic, since they need a good knowledge of the game
            # not to be frustrating
            oos_option_medium_logic(state, player),
            any([
                oos_has_bombs(state, player, 2),
                oos_can_use_ember_seeds(state, player, False),
                (oos_has_slingshot(state, player) and oos_has_gale_seeds(state, player)),
            ])
        ]),
    ])


def oos_can_break_crystal(state: CollectionState, player: int):
    return any([
        oos_has_sword(state, player),
        oos_has_bombs(state, player),
        oos_has_bracelet(state, player),
        all([
            oos_option_medium_logic(state, player),
            state.has("Expert's Ring", player)
        ])
    ])


def oos_can_break_sign(state: CollectionState, player: int):
    return any([
        oos_has_noble_sword(state, player),
        state.has("Biggoron's Sword", player),
        oos_has_bracelet(state, player),
        oos_can_use_ember_seeds(state, player, False),
        oos_has_magic_boomerang(state, player)
    ])


def oos_can_harvest_tree(state: CollectionState, player: int, can_use_companion: bool):
    return all([
        oos_can_use_seeds(state, player),
        any([
            oos_has_sword(state, player),
            oos_has_fools_ore(state, player),
            oos_has_rod(state, player),
            oos_can_punch(state, player),
            all([
                can_use_companion,
                oos_option_medium_logic(state, player),
                oos_can_summon_dimitri(state, player)
            ])
        ])
    ])


def oos_can_harvest_gasha(state: CollectionState, player: int, count: int):
    reachable_soils = [state.has(f"_reached_{region_name}", player) for region_name in GASHA_SPOT_REGIONS]
    return all([
        reachable_soils.count(True) >= count,  # Enough soils are reachable
        state.has("Gasha Seed", player, count),  # Enough seeds to plant
        oos_has_sword(state, player) or oos_has_fools_ore(state, player)  # Can actually harvest the nut, and get kills
    ])


def oos_can_push_enemy(state: CollectionState, player: int):
    return any([
        oos_has_rod(state, player),
        oos_has_shield(state, player)
    ])


def oos_can_kill_normal_enemy(state: CollectionState, player: int, pit_available: bool = False,
                              allow_gale_seeds: bool = True):
    # If a pit is avaiable nearby, it can be used to put the enemies inside using
    # items that are usually non-lethal
    if pit_available and oos_can_push_enemy(state, player):
        return True

    return any([
        oos_has_sword(state, player),
        oos_has_fools_ore(state, player),
        oos_can_kill_normal_using_satchel(state, player, allow_gale_seeds),
        oos_can_kill_normal_using_slingshot(state, player, allow_gale_seeds),
        (oos_option_medium_logic(state, player) and oos_has_bombs(state, player, 4)),
        oos_can_punch(state, player)
    ])


def oos_can_kill_normal_using_satchel(state: CollectionState, player: int, allow_gale_seeds: bool = True):
    # Expect a 50+ seed satchel to ensure we can chain dungeon rooms to some extent if that's our only kill option
    if not oos_has_satchel(state, player, 2):
        return False

    return any([
        # Casual logic => only ember
        oos_has_ember_seeds(state, player),
        all([
            # Medium logic => allow scent or gale+feather
            oos_option_medium_logic(state, player),
            any([
                oos_has_scent_seeds(state, player),
                oos_has_mystery_seeds(state, player),
                all([
                    allow_gale_seeds,
                    oos_has_gale_seeds(state, player),
                    oos_has_feather(state, player)
                ])
            ])
        ]),
        all([
            # Hard logic => allow gale without feather
            allow_gale_seeds,
            oos_option_hard_logic(state, player),
            oos_has_gale_seeds(state, player)
        ])
    ])


def oos_can_kill_normal_using_slingshot(state: CollectionState, player: int, allow_gale_seeds: bool = True):
    # Expect a 50+ seed satchel to ensure we can chain dungeon rooms to some extent if that's our only kill option
    if not oos_has_satchel(state, player, 2):
        return False

    return all([
        oos_has_slingshot(state, player),
        any([
            oos_has_ember_seeds(state, player),
            oos_has_scent_seeds(state, player),
            all([
                oos_option_medium_logic(state, player),
                any([
                    allow_gale_seeds,
                    oos_has_mystery_seeds(state, player),
                    oos_has_gale_seeds(state, player),
                ])
            ])
        ])
    ])


def oos_can_kill_armored_enemy(state: CollectionState, player: int):
    return any([
        oos_has_sword(state, player),
        oos_has_fools_ore(state, player),
        all([
            oos_has_satchel(state, player, 2),  # Expect a 50+ seeds satchel to be able to chain rooms in dungeons
            oos_has_scent_seeds(state, player),
            any([
                oos_has_slingshot(state, player),
                oos_option_medium_logic(state, player)
            ])
        ]),
        oos_can_punch(state, player)
    ])


def oos_can_kill_stalfos(state: CollectionState, player: int):
    return any([
        oos_can_kill_normal_enemy(state, player),
        all([
            oos_option_medium_logic(state, player),
            oos_has_rod(state, player)
        ])
    ])


def oos_can_punch(state: CollectionState, player: int):
    return all([
        oos_option_medium_logic(state, player),
        any([
            state.has("Fist Ring", player),
            state.has("Expert's Ring", player)
        ])
    ])


def oos_can_trigger_lever(state: CollectionState, player: int):
    return any([
        oos_can_trigger_lever_from_minecart(state, player),
        all([
            oos_option_medium_logic(state, player),
            oos_has_shovel(state, player)
        ])
    ])


def oos_can_trigger_lever_from_minecart(state: CollectionState, player: int):
    return any([
        oos_can_punch(state, player),
        oos_has_sword(state, player),
        oos_has_fools_ore(state, player),
        oos_has_boomerang(state, player),
        oos_has_rod(state, player),

        oos_can_use_scent_seeds(state, player),
        oos_can_use_mystery_seeds(state, player),
        oos_can_use_ember_seeds(state, player, False),
        oos_has_slingshot(state, player),  # any seed works using slingshot
    ])


def oos_can_kill_d2_hardhat(state: CollectionState, player: int):
    return any([
        oos_has_sword(state, player),
        oos_has_fools_ore(state, player),
        oos_has_boomerang(state, player),
        oos_can_push_enemy(state, player),
        all([
            oos_option_medium_logic(state, player),
            any([
                oos_has_slingshot(state, player),
                all([
                    oos_option_hard_logic(state, player),
                    oos_has_satchel(state, player),
                ])
            ]),
            any([
                oos_has_scent_seeds(state, player),
                oos_has_gale_seeds(state, player),
            ])
        ]),
        all([
            oos_option_hard_logic(state, player),
            oos_has_shovel(state, player)
        ])
    ])


def oos_can_kill_d2_far_moblin(state: CollectionState, player: int):
    return any([
        oos_has_sword(state, player),
        oos_has_fools_ore(state, player),
        oos_can_kill_normal_using_slingshot(state, player),
        all([
            oos_has_feather(state, player),
            oos_can_push_enemy(state, player),
        ]),
        all([
            oos_option_hard_logic(state, player),
            any([
                oos_can_use_ember_seeds(state, player, False),
                oos_can_punch(state, player)
            ])
        ])
    ])


def oos_can_flip_spiked_beetle(state: CollectionState, player: int):
    return any([
        oos_has_shield(state, player),
        all([
            oos_option_medium_logic(state, player),
            oos_has_shovel(state, player)
        ])
    ])


def oos_can_kill_spiked_beetle(state: CollectionState, player: int):
    return any([
        all([  # Regular flip + kill
            oos_can_flip_spiked_beetle(state, player),
            any([
                oos_has_sword(state, player),
                oos_has_fools_ore(state, player),
                oos_can_kill_normal_using_satchel(state, player),
                oos_can_kill_normal_using_slingshot(state, player)
            ])
        ]),
        # Instant kill using Gale Seeds
        oos_can_use_gale_seeds_offensively(state, player)
    ])


def oos_can_kill_magunesu(state: CollectionState, player: int):
    return any([
        oos_has_sword(state, player),
        oos_has_fools_ore(state, player),
        # state.has("expert's ring", player)
    ])


# Action predicates ###########################################

def oos_can_remove_snow(state: CollectionState, player: int, can_summon_companion: bool):
    return oos_has_shovel(state, player) or (can_summon_companion and oos_has_flute(state, player))


def oos_can_swim(state: CollectionState, player: int, can_summon_companion: bool):
    return oos_has_flippers(state, player) or (can_summon_companion and oos_can_summon_dimitri(state, player))


def oos_can_remove_rockslide(state: CollectionState, player: int, can_summon_companion: bool):
    return oos_has_bombs(state, player) or (can_summon_companion and oos_can_summon_ricky(state, player))


def oos_can_meet_maple(state: CollectionState, player: int):
    return oos_can_kill_normal_enemy(state, player, False, False)


# Season in region predicates ##########################################

def oos_season_in_spool_swamp(state: CollectionState, player: int, season: int):
    if oos_get_default_season(state, player, "SPOOL_SWAMP") == season:
        return True
    return oos_has_season(state, player, season) and state.has("_reached_spool_stump", player)


def oos_season_in_eyeglass_lake(state: CollectionState, player: int, season: int):
    if oos_get_default_season(state, player, "EYEGLASS_LAKE") == season:
        return True
    return oos_has_season(state, player, season) and state.has("_reached_eyeglass_stump", player)


def oos_season_in_temple_remains(state: CollectionState, player: int, season: int):
    if oos_get_default_season(state, player, "TEMPLE_REMAINS") == season:
        return True
    return oos_has_season(state, player, season) and state.has("_reached_remains_stump", player)


def oos_season_in_holodrum_plain(state: CollectionState, player: int, season: int):
    if oos_get_default_season(state, player, "HOLODRUM_PLAIN") == season:
        return True
    return oos_has_season(state, player, season) and state.has("_reached_ghastly_stump", player)


def oos_season_in_western_coast(state: CollectionState, player: int, season: int):
    if oos_get_default_season(state, player, "WESTERN_COAST") == season:
        return True
    return oos_has_season(state, player, season) and state.has("_reached_coast_stump", player)


def oos_season_in_eastern_suburbs(state: CollectionState, player: int, season: int):
    return (oos_get_default_season(state, player, "EASTERN_SUBURBS") == season
            or oos_has_season(state, player, season))


def oos_season_in_sunken_city(state: CollectionState, player: int, season: int):
    return (oos_get_default_season(state, player, "SUNKEN_CITY") == season
            or oos_has_season(state, player, season))


def oos_season_in_woods_of_winter(state: CollectionState, player: int, season: int):
    return (oos_get_default_season(state, player, "WOODS_OF_WINTER") == season
            or oos_has_season(state, player, season))


def oos_season_in_central_woods_of_winter(state: CollectionState, player: int, season: int):
    if oos_get_default_season(state, player, "WOODS_OF_WINTER") == season:
        return True
    return oos_has_season(state, player, season) and state.has("_reached_d2_stump", player)


def oos_season_in_mt_cucco(state: CollectionState, player: int, season: int):
    if oos_get_default_season(state, player, "SUNKEN_CITY") == season:
        return True
    return oos_has_season(state, player, season)


def oos_season_in_lost_woods(state: CollectionState, player: int, season: int):
    if oos_get_default_season(state, player, "LOST_WOODS") == season:
        return True
    return oos_has_season(state, player, season)


def oos_season_in_tarm_ruins(state: CollectionState, player: int, season: int):
    if oos_get_default_season(state, player, "TARM_RUINS") == season:
        return True
    return oos_has_season(state, player, season)


def oos_season_in_horon_village(state: CollectionState, player: int, season: int):
    # With vanilla behavior, you can randomly have any season inside Horon, making any season virtually accessible
    if not state.multiworld.worlds[player].options.normalize_horon_village_season:
        return True
    if oos_get_default_season(state, player, "HORON_VILLAGE") == season:
        return True
    return oos_has_season(state, player, season)


# Self-locking items helper predicates ##########################################

def oos_self_locking_item(state: CollectionState, player: int, region_name: str, item_name: str):
    if state.multiworld.worlds[player].options.accessibility == Accessibility.option_full:
        return False

    region = state.multiworld.get_region(region_name, player)
    items_in_region = [location.item for location in region.locations if location.item is not None]
    for item in items_in_region:
        if item.name == item_name and item.player == player:
            return True
    return False


def oos_self_locking_small_key(state: CollectionState, player: int, region_name: str, dungeon: int):
    item_name = f"Small Key ({DUNGEON_NAMES[dungeon]})"
    return oos_self_locking_item(state, player, region_name, item_name)
