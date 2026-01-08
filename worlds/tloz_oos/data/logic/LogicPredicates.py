from BaseClasses import CollectionState
from Options import Accessibility
from ..Constants import *
from ...Options import OracleOfSeasonsLogicDifficulty


# Items predicates ############################################################

def oos_has_sword(state: CollectionState, player: int, accept_biggoron: bool = True):
    return any([
        state.has("Progressive Sword", player),
        all([
            accept_biggoron,
            state.has("Biggoron's Sword", player)
        ])
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


# Cross items
def oos_has_cane(state: CollectionState, player: int):
    return state.has("Cane of Somaria", player)


def oos_has_switch_hook(state: CollectionState, player: int, level: int = 1):
    return state.has("Switch Hook", player, level)


def oos_has_tight_switch_hook(state: CollectionState, player: int):
    return any([
        oos_has_switch_hook(state, player, 2),
        all([
            oos_option_medium_logic(state, player),
            oos_has_switch_hook(state, player)
        ])
    ])


def oos_has_shooter(state: CollectionState, player: int):
    return state.has("Seed Shooter", player)


def oos_has_seed_thrower(state: CollectionState, player: int):
    return any([
        oos_has_slingshot(state, player),
        oos_has_shooter(state, player),
    ])


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
        all([
            state.has("_wild_ember_seeds", player),
            oos_option_medium_logic(state, player)
        ])
    ])


def oos_has_scent_seeds(state: CollectionState, player: int):
    return any([
        state.has("Scent Seeds", player),
        state.multiworld.worlds[player].options.default_seed == "scent"
    ])


def oos_has_pegasus_seeds(state: CollectionState, player: int):
    return any([
        state.has("Pegasus Seeds", player),
        state.multiworld.worlds[player].options.default_seed == "pegasus"
    ])


def oos_has_mystery_seeds(state: CollectionState, player: int):
    return any([
        state.has("Mystery Seeds", player),
        state.multiworld.worlds[player].options.default_seed == "mystery",
        all([
            state.has("_wild_mystery_seeds", player),
            oos_option_medium_logic(state, player)
        ])
    ])


def oos_has_gale_seeds(state: CollectionState, player: int):
    return any([
        state.has("Gale Seeds", player),
        state.multiworld.worlds[player].options.default_seed == "gale"
    ])


def oos_has_small_keys(state: CollectionState, player: int, dungeon_id: int, amount: int = 1):
    return any([
        state.has(f"Small Key ({DUNGEON_NAMES[dungeon_id]})", player, amount),
        state.has(f"Master Key ({DUNGEON_NAMES[dungeon_id]})", player)
    ])


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
    return state.multiworld.worlds[player].options.logic_difficulty >= OracleOfSeasonsLogicDifficulty.option_medium


def oos_option_hard_logic(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.logic_difficulty >= OracleOfSeasonsLogicDifficulty.option_hard


def oos_option_hell_logic(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.logic_difficulty >= OracleOfSeasonsLogicDifficulty.option_hell


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


def oos_is_default_season(state: CollectionState, player: int, area_name: str, season):
    return state.multiworld.worlds[player].default_seasons[area_name] == season


def oos_can_remove_season(state: CollectionState, player: int, season: int):
    # Test if player has any other season than the one we want to remove
    return any(
        [state.has(item_name, player) for season_name, item_name in SEASON_ITEMS.items() if season_name != season]
    )


def oos_has_essences(state: CollectionState, player: int, target_count: int):
    essence_count = [state.has(essence, player) for essence in ITEM_GROUPS["Essences"]].count(True)
    return essence_count >= target_count


def oos_has_essences_for_maku_seed(state: CollectionState, player: int):
    return oos_has_essences(state, player, state.multiworld.worlds[player].options.required_essences.value)


def oos_has_essences_for_treehouse(state: CollectionState, player: int):
    return oos_has_essences(state, player, state.multiworld.worlds[player].options.treehouse_old_man_requirement.value)


def oos_has_required_jewels(state: CollectionState, player: int):
    target_count = state.multiworld.worlds[player].options.tarm_gate_required_jewels.value
    count = [state.has(jewel, player) for jewel in ITEM_GROUPS["Jewels"]].count(True)
    return count >= target_count


def oos_can_reach_lost_woods_pedestal(state: CollectionState, player: int, allow_default: bool = False, force_deku=False):
    world = state.multiworld.worlds[player]
    seasons_in_pedestal_sequence = [season for [_, season] in world.lost_woods_item_sequence]

    return all([
        oos_can_complete_season_sequence(state, player, seasons_in_pedestal_sequence, allow_default),
        any([
            force_deku,
            state.can_reach_region("lost woods phonograph", player),
            all([
                # if sequence is vanilla, medium+ players are expected to know it
                oos_option_medium_logic(state, player),
                not state.multiworld.worlds[player].options.randomize_lost_woods_item_sequence
            ])
        ])
    ])


def oos_can_complete_lost_woods_main_sequence(state: CollectionState, player: int, allow_default: bool = False, force_deku=False):
    world = state.multiworld.worlds[player]
    seasons_in_main_sequence = [season for [_, season] in world.lost_woods_main_sequence]

    return all([
        oos_can_complete_season_sequence(state, player, seasons_in_main_sequence, allow_default),
        any([
            force_deku,
            state.can_reach_region("lost woods deku", player),
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
        first_season = season_sequence[0]
        if oos_is_default_season(state, player, "LOST_WOODS", first_season):
            while len(season_sequence) > 0 and season_sequence[0] == first_season:
                del season_sequence[0]

    return all([
        any([SEASON_WINTER not in season_sequence, oos_has_winter(state, player)]),
        any([SEASON_SPRING not in season_sequence, oos_has_spring(state, player)]),
        any([SEASON_SUMMER not in season_sequence, oos_has_summer(state, player)]),
        any([SEASON_AUTUMN not in season_sequence, oos_has_autumn(state, player)])
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
    # Having a weapon to get  or a shovel is enough to guarantee that we can reach a significant amount of rupees
    return any([
        oos_can_kill_normal_enemy(state, player, False, False),
        oos_has_shovel(state, player)
    ])


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
                oos_has_sword(state, player)
            ])
        ]),
        all([
            oos_option_hard_logic(state, player),
            any([
                state.has("_reached_subrosian_dance_hall", player),
                oos_has_bracelet(state, player),
                oos_has_switch_hook(state, player)
            ])
        ])
    ])


def oos_can_date_rosa(state: CollectionState, player: int):
    return all([
        state.has("_reached_rosa", player),
        state.has("Ribbon", player)
    ])


def oos_can_trigger_far_switch(state: CollectionState, player: int):
    return any([
        oos_has_boomerang(state, player),
        oos_has_bombs(state, player),
        oos_has_seed_thrower(state, player),
        oos_shoot_beams(state, player),
        oos_has_switch_hook(state, player)
    ])


def oos_shoot_beams(state: CollectionState, player: int):
    return any([
        all([
            oos_option_medium_logic(state, player),
            oos_has_sword(state, player, False),
            state.has("Energy Ring", player),
        ]),
        all([
            oos_option_medium_logic(state, player),
            oos_has_noble_sword(state, player),
            any([
                state.has("Heart Ring L-2", player),
                all([
                    oos_option_hard_logic(state, player),
                    state.has("Heart Ring L-1", player),
                ])
            ])
        ])
    ])


def oos_has_rod(state: CollectionState, player: int):
    return any([
        oos_has_winter(state, player),
        oos_has_summer(state, player),
        oos_has_spring(state, player),
        oos_has_autumn(state, player)
    ])


def oos_has_bombs(state: CollectionState, player: int, amount: int = 1):
    return any([
        state.has("Bombs", player, amount),
        all([
            # With medium logic, player is expected to know they can get free bombs
            # from D2 moblin room even if they never had bombs before
            amount == 1,
            oos_option_medium_logic(state, player),
            state.has("_reached_d2_bracelet_room", player),
            oos_can_harvest_regrowing_bush(state, player, False)
        ])
    ])


def oos_has_bombchus(state: CollectionState, player: int, amount: int = 1):
    return state.has("Bombchus", player, amount)


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
    return any([
        oos_has_slingshot(state, player),
        oos_has_shooter(state, player),
        oos_has_satchel(state, player)
    ])


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
    return all([
        oos_has_satchel(state, player, 2),
        oos_option_medium_logic(state, player),
        any([
            oos_has_gale_seeds(state, player),
            oos_has_mystery_seeds(state, player)
        ]),
        any([
            oos_has_seed_thrower(state, player),
            all([
                oos_has_satchel(state, player),
                any([
                    oos_option_hard_logic(state, player),
                    oos_has_feather(state, player)
                ]),
            ])
        ])
    ])


def oos_can_use_mystery_seeds(state: CollectionState, player: int):
    return all([
        oos_can_use_seeds(state, player),
        oos_has_mystery_seeds(state, player)
    ])


# Break / kill predicates ###########################################

def oos_can_break_bush(state: CollectionState, player: int, can_summon_companion: bool = False, allow_bombchus: bool = False):
    return any([
        oos_can_break_flowers(state, player, can_summon_companion, allow_bombchus),
        oos_has_bracelet(state, player)
    ])


def oos_can_harvest_regrowing_bush(state: CollectionState, player: int, allow_bombs: bool = True):
    return any([
        oos_has_sword(state, player),
        oos_has_fools_ore(state, player),
        allow_bombs and oos_has_bombs(state, player)
    ])


def oos_can_break_mushroom(state: CollectionState, player: int, can_use_companion: bool):
    return any([
        oos_has_bracelet(state, player),
        all([
            oos_option_medium_logic(state, player),
            any([
                oos_has_magic_boomerang(state, player),
                all([
                    can_use_companion,
                    oos_can_summon_dimitri(state, player)
                ])
            ])
        ]),
    ])


def oos_can_break_pot(state: CollectionState, player: int):
    return any([
        oos_has_bracelet(state, player),
        oos_has_noble_sword(state, player),
        state.has("Biggoron's Sword", player),
        oos_has_switch_hook(state, player)
    ])


def oos_can_break_flowers(state: CollectionState, player: int, can_summon_companion: bool = False, allow_bombchus: bool = False):
    return any([
        oos_has_sword(state, player),
        oos_has_magic_boomerang(state, player),
        oos_has_switch_hook(state, player),
        all([
            can_summon_companion,
            oos_has_flute(state, player)
        ]),
        all([
            # Consumables need at least medium logic, since they need a good knowledge of the game
            # not to be frustrating
            oos_option_medium_logic(state, player),
            any([
                oos_has_bombs(state, player, 2),
                oos_can_use_ember_seeds(state, player, False),
                all([
                    oos_has_seed_thrower(state, player),
                    oos_has_gale_seeds(state, player)
                ]),
                all([
                    allow_bombchus,
                    oos_has_bombchus(state, player, 5)
                ])
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
        ]),
        all([
            oos_option_medium_logic(state, player),
            oos_has_bombchus(state, player, 5)
        ]),
    ])


def oos_can_break_sign(state: CollectionState, player: int):
    return any([
        oos_has_noble_sword(state, player),
        state.has("Biggoron's Sword", player),
        oos_has_bracelet(state, player),
        oos_can_use_ember_seeds(state, player, False),
        oos_has_magic_boomerang(state, player),
        oos_has_switch_hook(state, player)
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
        any([
            # Can actually harvest the nut, and get kills
            oos_has_sword(state, player),
            oos_has_fools_ore(state, player)
        ])
    ])


def oos_can_push_enemy(state: CollectionState, player: int):
    return any([
        oos_has_rod(state, player),
        oos_has_shield(state, player),
        all([
            oos_option_medium_logic(state, player),
            oos_has_shovel(state, player)
        ])
    ])


def oos_can_kill_normal_enemy(state: CollectionState, player: int, pit_available: bool = False,
                              allow_gale_seeds: bool = True):
    return any([
        oos_can_kill_normal_enemy_no_cane(state, player, pit_available, allow_gale_seeds),
        (oos_option_medium_logic(state, player) and oos_has_cane(state, player))
    ])


def oos_can_kill_normal_enemy_no_cane(state: CollectionState, player: int, pit_available: bool = False,
                                      allow_gale_seeds: bool = True):
    return any([
        all([
            # If a pit is avaiable nearby, it can be used to put the enemies inside using
            # items that are usually non-lethal
            pit_available,
            oos_can_push_enemy(state, player)
        ]),
        oos_has_sword(state, player),
        oos_has_fools_ore(state, player),
        oos_can_kill_normal_using_satchel(state, player, allow_gale_seeds),
        oos_can_kill_normal_using_slingshot(state, player, allow_gale_seeds),
        all([
            oos_option_medium_logic(state, player),
            oos_has_bombs(state, player, 4)
        ]),
        oos_has_bombchus(state, player, 2),
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
        oos_has_seed_thrower(state, player),
        any([
            oos_has_ember_seeds(state, player),
            oos_has_scent_seeds(state, player),
            all([
                oos_option_medium_logic(state, player),
                any([
                    all([
                        allow_gale_seeds,
                        oos_has_gale_seeds(state, player),
                    ]),
                    oos_has_mystery_seeds(state, player),
                ])
            ])
        ])
    ])


def oos_can_kill_armored_enemy(state: CollectionState, player: int, allow_cane: bool, allow_bombchus: bool):
    return any([
        oos_has_sword(state, player),
        oos_has_fools_ore(state, player),
        all([
            oos_option_medium_logic(state, player),
            oos_has_bombs(state, player, 4)
        ]),
        all([
            allow_bombchus,
            oos_has_bombchus(state, player, 2)
        ]),
        all([
            oos_has_satchel(state, player, 2),  # Expect a 50+ seeds satchel to be able to chain rooms in dungeons
            oos_has_scent_seeds(state, player),
            any([
                oos_has_seed_thrower(state, player),
                oos_option_medium_logic(state, player)
            ])
        ]),
        all([
            allow_cane,
            oos_option_medium_logic(state, player),
            oos_has_cane(state, player)
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


def oos_can_kill_moldorm(state: CollectionState, player: int, pit_available: bool = False):
    return any([
        oos_can_kill_armored_enemy(state, player, True, True),
        oos_has_switch_hook(state, player),
        all([
            pit_available,
            any([
                oos_has_shield(state, player),
                all([
                    oos_option_medium_logic(state, player),
                    oos_has_shovel(state, player)
                ])
            ])
        ])
    ])


def oos_can_kill_facade(state: CollectionState, player: int):
    return any([
        oos_has_bombs(state, player),
        oos_has_bombchus(state, player, 2)
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
        oos_has_switch_hook(state, player),
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
        oos_has_seed_thrower(state, player),  # any seed works using slingshot
    ])


def oos_can_kill_d2_hardhat(state: CollectionState, player: int):
    return any([
        oos_has_sword(state, player),
        oos_has_fools_ore(state, player),
        oos_has_boomerang(state, player),
        oos_can_push_enemy(state, player),
        oos_has_switch_hook(state, player),  # Also push the hardhat
        all([
            oos_option_medium_logic(state, player),
            oos_has_satchel(state, player, 2),
            any([
                oos_has_seed_thrower(state, player),
                all([
                    oos_option_hard_logic(state, player),
                    oos_has_satchel(state, player),
                ])
            ]),
            any([
                oos_has_scent_seeds(state, player),
                oos_has_gale_seeds(state, player),
                oos_has_mystery_seeds(state, player)
            ])
        ]),
        all([
            oos_option_hard_logic(state, player),
            oos_has_shovel(state, player)
        ])
    ])


def oos_can_kill_d2_far_moblin(state: CollectionState, player: int):
    return any([
        # Use the regrowable bombs that are there
        oos_has_sword(state, player),
        oos_has_fools_ore(state, player),
        oos_has_bombs(state, player),

        oos_can_kill_normal_using_slingshot(state, player),
        all([
            any([
                oos_has_feather(state, player),
                all([
                    # Switch with a moblin, kill the other, jump in the pit, kill the first
                    oos_option_medium_logic(state, player),
                    oos_has_switch_hook(state, player)
                ])
            ]),
            oos_can_kill_normal_enemy(state, player, True),
        ]),
        all([
            oos_option_hard_logic(state, player),
            any([
                oos_can_use_ember_seeds(state, player, False),
                oos_can_punch(state, player),
                oos_has_cane(state, player)
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
                oos_can_kill_normal_using_slingshot(state, player),
                oos_has_switch_hook(state, player)
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
    return any([
        oos_has_shovel(state, player),
        all([
            can_summon_companion,
            oos_has_flute(state, player)
        ])
    ])


def oos_can_swim(state: CollectionState, player: int, can_summon_companion: bool):
    return any([
        oos_has_flippers(state, player),
        all([
            can_summon_companion,
            oos_can_summon_dimitri(state, player)
        ])
    ])


def oos_can_remove_rockslide(state: CollectionState, player: int, can_summon_companion: bool):
    return any([
        oos_has_bombs(state, player),
        all([
            oos_option_medium_logic(state, player),
            oos_has_bombchus(state, player, 5)
        ]),
        all([
            can_summon_companion,
            oos_can_summon_ricky(state, player)
        ])
    ])


def oos_can_meet_maple(state: CollectionState, player: int):
    return oos_can_kill_normal_enemy(state, player, False, False)


def oos_can_dimitri_clip(state: CollectionState, player: int):
    return all([
        oos_option_hell_logic(state, player),
        oos_can_summon_dimitri(state, player),
        oos_has_bracelet(state, player),
        oos_has_gale_seeds(state, player),
        oos_has_satchel(state, player)
    ])


# Season in region predicates ##########################################

def oos_season_in_spool_swamp(state: CollectionState, player: int, season: int):
    return any([
        oos_is_default_season(state, player, "SPOOL_SWAMP", season),
        all([
            oos_has_season(state, player, season),
            state.has("_reached_spool_stump", player)
        ])
    ])


def oos_season_in_eyeglass_lake(state: CollectionState, player: int, season: int):
    return any([
        oos_is_default_season(state, player, "EYEGLASS_LAKE", season),
        all([
            oos_has_season(state, player, season),
            state.has("_reached_eyeglass_stump", player)
        ])
    ])


def oos_season_in_temple_remains(state: CollectionState, player: int, season: int):
    return any([
        oos_is_default_season(state, player, "TEMPLE_REMAINS", season),
        all([
            oos_has_season(state, player, season),
            state.has("_reached_remains_stump", player)
        ])
    ])


def oos_season_in_holodrum_plain(state: CollectionState, player: int, season: int):
    return any([
        oos_is_default_season(state, player, "HOLODRUM_PLAIN", season),
        all([
            oos_has_season(state, player, season),
            state.has("_reached_ghastly_stump", player)
        ])
    ])


def oos_season_in_western_coast(state: CollectionState, player: int, season: int):
    return any([
        oos_is_default_season(state, player, "WESTERN_COAST", season),
        all([
            oos_has_season(state, player, season),
            state.has("_reached_coast_stump", player)
        ])
    ])


def oos_season_in_eastern_suburbs(state: CollectionState, player: int, season: int):
    return any([
        oos_is_default_season(state, player, "EASTERN_SUBURBS", season),
        oos_has_season(state, player, season)
    ])


def oos_not_season_in_eastern_suburbs(state: CollectionState, player: int, season: int):
    return any([
        not oos_is_default_season(state, player, "EASTERN_SUBURBS", season),
        oos_can_remove_season(state, player, season)
    ])


def oos_season_in_sunken_city(state: CollectionState, player: int, season: int):
    return any([
        oos_is_default_season(state, player, "SUNKEN_CITY", season),
        all([
            oos_has_season(state, player, season),
            any([
                oos_is_default_season(state, player, "SUNKEN_CITY", SEASON_WINTER),
                oos_can_swim(state, player, True),
                state.has("_saved_dimitri_in_sunken_city", player)
            ])
        ])
    ])


def oos_season_in_woods_of_winter(state: CollectionState, player: int, season: int):
    return any([
        oos_is_default_season(state, player, "WOODS_OF_WINTER", season),
        oos_has_season(state, player, season)
    ])


def oos_season_in_central_woods_of_winter(state: CollectionState, player: int, season: int):
    return any([
        oos_is_default_season(state, player, "WOODS_OF_WINTER", season),
        all([
            oos_has_season(state, player, season),
            state.has("_reached_d2_stump", player)
        ])
    ])


def oos_season_in_mt_cucco(state: CollectionState, player: int, season: int):
    return any([
        oos_is_default_season(state, player, "SUNKEN_CITY", season),
        oos_has_season(state, player, season)
    ])


def oos_season_in_lost_woods(state: CollectionState, player: int, season: int):
    return any([
        oos_is_default_season(state, player, "LOST_WOODS", season),
        oos_has_season(state, player, season)
    ])


def oos_season_in_tarm_ruins(state: CollectionState, player: int, season: int):
    return any([
        oos_is_default_season(state, player, "TARM_RUINS", season),
        oos_has_season(state, player, season)
    ])


def oos_season_in_horon_village(state: CollectionState, player: int, season: int):
    # With vanilla behavior, you can randomly have any season inside Horon, making any season virtually accessible
    return any([
        not state.multiworld.worlds[player].options.normalize_horon_village_season,
        oos_is_default_season(state, player, "HORON_VILLAGE", season),
        oos_has_season(state, player, season)
    ])


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


# Rooster adventure logic  ######################################################
def oos_roosters(state: CollectionState, player: int):
    if state.tloz_oos_available_cuccos[player] is None:
        # This computes cuccos for the whole game then caches it (total, top, bottom)
        available_cuccos = {
            "cucco mountain": (-1, -1, -1),
            "horon": (-1, -1, -1),
            "suburbs": (-1, -1, -1),
            "moblin road": (-1, -1, -1),
            "sunken": (-1, -1, -1),
            "swamp": (-1, -1, -1),
            "d6": (-1, -1, -1),
        }

        def register_cucco(region: str, new_cuccos: tuple[int, int, int]):
            old_cuccos = available_cuccos[region]
            available_cuccos[region] = tuple([max(old_cuccos[i], new_cuccos[i]) for i in range(3)])

        def use_any_cucco(cuccos: tuple[int, int, int]) -> tuple[int, int, int]:
            return cuccos[0] - 1, cuccos[1], cuccos[2]

        def use_top_cucco(cuccos: tuple[int, int, int]) -> tuple[int, int, int]:
            return cuccos[0] - 1, cuccos[1] - 1, cuccos[2]

        def use_bottom_cucco(cuccos: tuple[int, int, int]) -> tuple[int, int, int]:
            return cuccos[0] - 1, cuccos[1], cuccos[2] - 1

        # These tops count the 2 tops that have to be sacrificed to exit mt cucco
        if state.has("Shovel", player):
            if state.has("Progressive Boomerang", player):
                top = 3
            else:
                top = 2
        elif state.has("Progressive Boomerang", player) and oos_can_use_pegasus_seeds(state, player):
            top = 2
        else:
            top = 1  # Sign + season indicator

        if oos_season_in_mt_cucco(state, player, SEASON_SPRING) \
                and (oos_can_break_flowers(state, player) or state.has("Spring Banana", player)):
            bottom = 2  # Sign
            # No more than 2 bottoms can be used in logic currently
        else:
            bottom = 0

        available_cuccos["cucco mountain"] = (top + bottom, top, bottom)

        if oos_can_jump_3_wide_pit(state, player) or oos_can_swim(state, player, True):
            # Either go to holdrum plains through natzu's water or through temple remains
            available_cuccos["horon"] = available_cuccos["cucco mountain"]

        if oos_has_flute(state, player):
            # go from holodrum to sunken
            available_cuccos["sunken"] = available_cuccos["horon"]
        elif oos_is_companion_moosh(state, player):
            if oos_can_jump_4_wide_liquid(state, player) or oos_has_flute(state, player):
                # go from holodrum to sunken
                available_cuccos["sunken"] = available_cuccos["horon"]
            elif oos_can_jump_3_wide_pit(state, player):
                # go from holodrum to sunken, through moblin fortress
                available_cuccos["sunken"] = use_top_cucco(available_cuccos["horon"])
        elif oos_is_companion_ricky(state, player):
            # go from natzu north to sunken
            if oos_can_break_flowers(state, player) and oos_can_swim(state, player, False):  # distance bush break
                available_cuccos["sunken"] = use_any_cucco(available_cuccos["cucco mountain"])
        elif oos_can_swim(state, player, False):
            # go from natzu north to sunken
            available_cuccos["sunken"] = available_cuccos["cucco mountain"]
        # Jump from sunken to suburbs
        available_cuccos["suburbs"] = available_cuccos["sunken"]

        if oos_can_use_ember_seeds(state, player, False):
            # Go through horon village
            available_cuccos["suburbs"] = available_cuccos["horon"]
        elif oos_season_in_eyeglass_lake(state, player, SEASON_WINTER) \
                or ((not oos_is_default_season(state, player, "EYEGLASS_LAKE", SEASON_SUMMER) or
                     oos_can_remove_season(state, player, SEASON_SUMMER)) and oos_can_swim(state, player, True)):
            # Go through the suburbs portal screen
            available_cuccos["suburbs"] = use_any_cucco(available_cuccos["horon"])

        if oos_season_in_eastern_suburbs(state, player, SEASON_SPRING):
            # Use the flower to go from suburbs to sunken
            register_cucco("sunken", available_cuccos["suburbs"])

        if oos_season_in_eastern_suburbs(state, player, SEASON_WINTER):
            # Walk
            available_cuccos["moblin road"] = available_cuccos["suburbs"]
        else:
            # Use a top cucco from the top of the spring flower to go past the tree
            available_cuccos["moblin road"] = use_top_cucco(available_cuccos["sunken"])

        if any([
            oos_season_in_holodrum_plain(state, player, SEASON_SUMMER),
            oos_can_jump_4_wide_pit(state, player),
            oos_can_summon_ricky(state, player),
            oos_can_summon_moosh(state, player)
        ]):
            # Move up the swamp vines regularly
            available_cuccos["swamp"] = available_cuccos["horon"]
        else:
            # Or use a bottom cucco
            available_cuccos["swamp"] = use_bottom_cucco(available_cuccos["horon"])

        if all([  # Reach tarm ruins, could probably be optimized
            oos_has_required_jewels(state, player),
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
        ]):
            can_reach_deku = all([
                oos_has_shield(state, player),
                any([
                    available_cuccos["swamp"][1],
                    oos_can_jump_2_wide_liquid(state, player),
                    oos_can_swim(state, player, False)
                ])
            ])
            if all([
                oos_has_autumn(state, player),
                oos_can_break_mushroom(state, player, False),
                any([
                    oos_can_complete_lost_woods_main_sequence(state, player, False, can_reach_deku),
                    all([
                        oos_can_complete_lost_woods_main_sequence(state, player, True, can_reach_deku),
                        oos_can_reach_lost_woods_pedestal(state, player, False, all([
                            oos_can_use_ember_seeds(state, player, False),
                            state.has("Phonograph", player)
                        ])),
                    ])
                ])
            ]):
                available_cuccos["d6"] = available_cuccos["swamp"]

        for region in available_cuccos:
            if any([available_cuccos[region][i] < 0 for i in range(3)]):
                available_cuccos[region] = (-1, -1, -1)
        state.tloz_oos_available_cuccos[player] = available_cuccos

    return state.tloz_oos_available_cuccos[player]


def oos_can_reach_rooster_adventure(state: CollectionState, player: int):
    # This is only safe if an indirect condition is set
    return oos_option_hell_logic(state, player) and state.can_reach_region("rooster adventure", player)
