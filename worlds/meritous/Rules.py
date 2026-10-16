# Copyright (c) 2022 FelicitusNeko
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from ..generic.Rules import forbid_item, exclusion_rules, add_rule


def set_rules(world, player, include_evolution_traps):
    # Prevent PSI keys from showing up in any boss' room
    # This is to prevent softlock from ending up having to fight a boss in the wrong boss room
    for boss in ["Meridian", "Ataraxia", "Merodach"]:
        for key in range(1, 4):
            forbid_item(world.get_location(boss, player), f"PSI Key {key}", player)

    # Prevent progression from showing up in last six checks per store
    # This is to prevent softlock from high prices or low chest drop
    default_exclude_locations = set()
    for store in ["Alpha Cache", "Beta Cache", "Gamma Cache"]:
        for check_number in range(22, 25):
            default_exclude_locations.add(f"{store} {check_number}")
    for check_number in range(19,25):
        default_exclude_locations.add(f"Reward Chest {check_number}")
    exclusion_rules(world, player, default_exclude_locations)

    # Make sure late caches only become in logic after obtaining the cursed seal
    
    for store in ["Alpha Cache", "Beta Cache", "Gamma Cache"]:
        for check_number in range(17, 25):
            add_rule(world.get_location(f"{store} {check_number}",player), 
                     lambda state: state.has("Cursed Seal", player))

    # Storage key minimum strength logic
    for i in range(1,4):
        if i == 1 and not include_evolution_traps:
            add_rule(world.get_location(f"PSI Key Storage {i}",player), 
                    lambda state: state.has_from_list(["Circuit Charge upgrade", "Circuit Refill upgrade"], player, 
                                                    15))
        else:
            add_rule(world.get_location(f"PSI Key Storage {i}",player), 
                lambda state: state.has_from_list(["Circuit Charge upgrade", "Circuit Refill upgrade"], player, 
                                                  20))