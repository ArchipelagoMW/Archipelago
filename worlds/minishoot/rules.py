import re
from BaseClasses import CollectionState
from worlds.minishoot.options import MinishootOptions

bard = 'Bard'
blacksmith = 'Blacksmith'
boost = 'Boost'
d1_boss_key = 'Boss Key (Dungeon 1)'
d1_reward = 'Dungeon 1 Reward'
d1_small_key = 'Small Key (Dungeon 1)'
d2_boss_key = 'Boss Key (Dungeon 2)'
d2_reward = 'Dungeon 2 Reward'
d2_small_key = 'Small Key (Dungeon 2)'
d3_boss_key = 'Boss Key (Dungeon 3)'
d3_reward = 'Dungeon 3 Reward'
d3_small_key = 'Small Key (Dungeon 3)'
d4_reward = 'Dungeon 4 Reward'
dark_heart = 'Dark Heart'
dark_key = 'Dark Key'
dash = 'Dash'
family_child = 'Family Child'
family_parent_1 = 'Family Parent 1'
family_parent_2 = 'Family Parent 2'
mercant = 'Merchant'
power_of_protection = "Power of protection"
primordial_crystal = "Primordial Crystal"
progressive_cannon = 'Progressive Cannon'
progressive_dash = 'Progressive Dash'
scarab = "Scarab"
scarab_collector = 'Scarab Collector'
scarab_key = 'Scarab Key'
spirit = "Spirit"
spirit_dash = 'Spirit Dash'
supershot = 'Supershot'
surf = 'Surf'

d5_boss = 'Dungeon 5 - Boss'
d5_central_wing = 'Dungeon 5 - Central wing'
d5_east_wing = 'Dungeon 5 - East wing'
d5_west_wing = 'Dungeon 5 - West wing'
desert_grotto_east_drop = 'Desert Grotto - East Drop'
desert_grotto_west_drop = 'Desert Grotto - West Drop'
scarab_temple_bottom_left_torch = 'Scarab Temple - Bottom Left Torch'
scarab_temple_bottom_right_torch = 'Scarab Temple - Bottom Right Torch'
scarab_temple_top_left_torch = 'Scarab Temple - Top Left Torch'
scarab_temple_top_right_torch = 'Scarab Temple - Top Right Torch'
sunken_city_city = 'Sunken City - City'
sunken_city_east = 'Sunken City - East'
sunken_city_east_torch = 'Sunken City - East torch'
sunken_city_fountain = 'Sunken City - Fountain'
sunken_city_west_island = 'Sunken City - West Island'
sunken_city_west_torch = 'Sunken City - West torch'
swamp_south_west_island = 'Swamp - South West Island'

# This is a rudimentary implementation of a rule parser for Minishoot logic.
# Basically, it allows for predicates to be defined in the form of strings, and then evaluated in the context of a given state.
# Those predicates can be combined using "and" and "or" operators, with "and" having higher precedence.
# For example, the expression "can_fight and can_surf or can_dash" would be parsed as "(can_fight and can_surf) or can_dash".
# Some predicates can take arguments, which are passed in parentheses after the predicate name (e.g. "have_d1_keys(2)").
def simple_parse(expression: str, state: CollectionState, world) -> bool:
    player = world.player
    options = world.options

    def can_fight(state: CollectionState, options: MinishootOptions, level: int = 1) -> bool:
        if not options.ignore_cannon_level_requirements:
            return state.has(progressive_cannon, player, level - 1)
        return True
    
    def can_dash(state: CollectionState, options: MinishootOptions) -> bool:
        if options.progressive_dash:
            return state.has(progressive_dash, player)
        return state.has(dash, player)
    
    def can_spirit_dash(state: CollectionState, options: MinishootOptions) -> bool:
        if options.progressive_dash:
            return state.has(progressive_dash, player, 2)
        return state.has(spirit_dash, player)
    
    def can_surf(state: CollectionState) -> bool:
        return state.has(surf, player)
    
    def can_destroy_walls(state: CollectionState, options: MinishootOptions) -> bool:
        if options.enable_primordial_crystal_logic:
            return state.has(supershot, player) or state.has(primordial_crystal, player)
        return state.has(supershot, player)
    
    def can_use_springboards(state: CollectionState, options: MinishootOptions) -> bool:
        if options.boostless_springboards:
            return can_dash(state, options) or state.has(boost, player)
        return state.has(boost, player)
    
    def can_race_spirits(state: CollectionState, options: MinishootOptions) -> bool:
        if options.boostless_spirit_races:
            return can_dash(state, options) or state.has(boost, player)
        return state.has(boost, player)
    
    def can_race_torches(state: CollectionState, options: MinishootOptions) -> bool:
        if options.boostless_torch_races:
            return True
        return state.has(boost, player)
    
    def can_cross_gaps(state: CollectionState, options: MinishootOptions, size: str = "normal") -> bool:
        if can_dash(state, options):
            return True
        
        if (size == "tight" or size == "very_tight") and options.dashless_gaps > 0 and state.has(boost, player):
            return True
        
        if size == "very_tight" and options.dashless_gaps == 2:
            return True
        
        return False
    
    def have_all_spirits(state: CollectionState, options: MinishootOptions) -> bool:
        return state.has(spirit, player, options.spirit_tower_requirement.value)
    
    def can_buy_from_scarab_collector(state: CollectionState, options: MinishootOptions, index1: int) -> bool:
        if options.scarab_items_cost == 0:
            return True
        return state.has(scarab, player, index1 * options.scarab_items_cost.value)

    conditions = {
        'true': lambda state: True,
        'can_free_blacksmith': lambda state: state.has(blacksmith, player),
        'can_free_mercant': lambda state: state.has(mercant, player),
        'can_obtain_super_crystals': lambda state, arg: can_dash(state, options) and state.has(supershot, player) and can_surf(state), # TODO: Implement this
        'can_fight': lambda state: can_fight(state, options, 1),
        'can_fight_lvl2': lambda state: can_fight(state, options, 2),
        'can_fight_lvl3': lambda state: can_fight(state, options, 3),
        'can_fight_lvl4': lambda state: can_fight(state, options, 4),
        'can_fight_lvl5': lambda state: can_fight(state, options, 5),
        'can_cross_gaps': lambda state: can_cross_gaps(state, options, "normal"),
        'can_cross_tight_gaps': lambda state: can_cross_gaps(state, options, "tight"),
        'can_cross_very_tight_gaps': lambda state: can_cross_gaps(state, options, "very_tight"),
        'can_surf': lambda state: can_surf(state),
        'can_boost': lambda state: state.has(boost, player),
        'can_destroy_bushes': lambda state: True,
        'can_destroy_ruins': lambda state: True,
        'have_d1_keys': lambda state, arg: state.has(d1_small_key, player, arg),
        'have_d1_boss_key': lambda state: state.has(d1_boss_key, player),
        'can_destroy_rocks': lambda state: can_destroy_walls(state, options),
        'can_destroy_pots': lambda state: True,
        'can_destroy_crystals': lambda state: True,
        'have_d2_keys': lambda state, arg: state.has(d2_small_key, player, arg),
        'have_d2_boss_key': lambda state: state.has(d2_boss_key, player),
        'can_destroy_walls': lambda state: can_destroy_walls(state, options),
        'can_buy_from_scarab_collector_1': lambda state: can_buy_from_scarab_collector(state, options, 1),
        'can_buy_from_scarab_collector_2': lambda state: can_buy_from_scarab_collector(state, options, 2),
        'can_buy_from_scarab_collector_3': lambda state: can_buy_from_scarab_collector(state, options, 3),
        'can_buy_from_scarab_collector_4': lambda state: can_buy_from_scarab_collector(state, options, 4),
        'can_buy_from_scarab_collector_5': lambda state: can_buy_from_scarab_collector(state, options, 5),
        'can_buy_from_scarab_collector_6': lambda state: can_buy_from_scarab_collector(state, options, 6),
        'can_free_scarab_collector': lambda state: state.has(scarab_collector, player),
        'can_light_torches': lambda state: state.has(supershot, player),
        'can_destroy_plants': lambda state: True,
        'can_destroy_coconuts': lambda state: True,
        'can_destroy_shells': lambda state: True,
        'have_d3_keys': lambda state, arg: state.has(d3_small_key, player, arg),
        'have_d3_boss_key': lambda state: state.has(d3_boss_key, player),
        'can_light_all_scarab_temple_torches': lambda state: can_surf(state) and state.has(supershot, player) and can_fight(state, options, 4),
        'can_dodge_purple_bullets': lambda state: can_dash(state, options) and can_spirit_dash(state, options),
        'can_unlock_final_boss_door': lambda state: state.has(dark_heart, player),
        'can_open_north_city_bridge': lambda state: can_dash(state, options) and can_fight(state, options, 4) and can_surf(state) and can_destroy_walls(state, options),
        'can_free_bard': lambda state: state.has(bard, player),
        'have_all_spirits': lambda state: have_all_spirits(state, options),
        'can_open_dungeon_5': lambda state: state.has(d1_reward, player) and state.has(d2_reward, player) and state.has(d3_reward, player) and state.has(d4_reward, player) and state.has(dark_key, player),
        'can_unlock_primordial_cave_door': lambda state: state.has(scarab_key, player),
        'can_light_city_torches': lambda state: state.has(supershot, player) and can_surf(state) and can_fight(state, options, 4) and can_use_springboards(state, options),
        'can_open_sunken_temple': lambda state: can_surf(state) and can_fight(state, options, 4) and can_dash(state, options) and can_destroy_walls(state, options),
        'can_light_desert_grotto_torches': lambda state: state.has(supershot, player) and (can_surf(state) or can_cross_gaps(state, options, "normal")) and can_fight(state, options, 3),
        'can_clear_both_d5_arenas': lambda state: can_fight(state, options, 5) and can_dash(state, options) and can_surf(state),
        'can_free_family': lambda state: state.has(family_child, player) and state.has(family_parent_1, player) and state.has(family_parent_2, player),
        'forest_is_blocked': lambda state: options.blocked_forest,
        'forest_is_open': lambda state: not options.blocked_forest,
        'can_blast_crystals': lambda state: state.has(power_of_protection, player),
        'can_destroy_trees': lambda state: state.has(supershot, player),
        'can_use_springboards': lambda state: can_use_springboards(state, options),
        'can_race_spirits': lambda state: can_race_spirits(state, options),
        'can_race_torches': lambda state: can_race_torches(state, options),
        'can_open_swamp_tower': lambda state: can_surf(state) or can_use_springboards(state, options)
    }

    # Split the expression by "or" and "and" using regular expressions
    try:
        or_parts = re.split(r'\s+or\s+', expression)
        for or_part in or_parts:
            and_parts = re.split(r'\s+and\s+', or_part)
            if all(
                conditions[cond.split('(')[0].strip()](state, int(cond.strip().split('(')[1].rstrip(')'))) if '(' in cond else conditions[cond.strip()](state)
                for cond in and_parts
            ):
                return True
        return False
    except KeyError:
        raise ValueError(f"Invalid condition: {expression}")
