from BaseClasses import MultiWorld
from .Names import LocationName, ItemName
from ..generic.Rules import add_rule, CollectionRule


def add_rule_safe(multiworld: MultiWorld, spot_name: str, player: int, rule: CollectionRule):
    try:
        location = multiworld.get_location(spot_name, player)
    except KeyError:
        # Do nothing for episode end locations that do not exist
        pass
    else:
        add_rule(location, rule)


def set_rules(world: MultiWorld, player: int, total_required_episodes: int):
    # S1E1
    add_rule(world.get_location(LocationName.s1e1_well, player),
             lambda state: state.has(ItemName.s1e1_hook, player))
    add_rule(world.get_location(LocationName.s1e1_shed_wall, player),
             lambda state: state.has(ItemName.s1e1_matches, player))

    # S1E3
    add_rule(world.get_location(LocationName.s1e3_seth_cover, player),
             lambda state: state.has(ItemName.seth, player))
    add_rule(world.get_location(LocationName.s1e3_chandelier, player),
             lambda state: state.has(ItemName.s1e3_platter, player))
    add_rule(world.get_location(LocationName.s1e3_lever, player),
             lambda state: state.has(ItemName.s1e3_crowbar, player))
    add_rule_safe(world, LocationName.s1e3_end, player,
                  lambda state: state.has(ItemName.s1e3_crowbar, player))

    # S1E4
    add_rule(world.get_location(LocationName.s1e4_bottle, player),
             lambda state: state.has(ItemName.s1e4_gun, player))

    # S2E1
    add_rule(world.get_location(LocationName.s2e1_message, player),
             lambda state: state.has(ItemName.s2e1_cylinder, player))
    add_rule_safe(world, LocationName.s2e1_end, player,
                  lambda state: state.has(ItemName.s2e1_cylinder, player))

    # S2E2
    add_rule(world.get_location(LocationName.s2e2_closet, player),
             lambda state: state.has(ItemName.s2e2_key, player))

    # S2E4
    add_rule(world.get_location(LocationName.s2e4_in_statue_r, player),
             lambda state: state.has(ItemName.s2e4_ruby, player) and state.has(ItemName.s2e4_alazif, player))
    add_rule(world.get_location(LocationName.s2e4_in_statue_l, player),
             lambda state: state.has(ItemName.s2e4_bucket, player) and state.has(ItemName.s2e4_matches, player))
    add_rule(world.get_location(LocationName.s2e4_chair, player),
             lambda state: state.has(ItemName.ibinoculars, player))

    # S2E6
    add_rule(world.get_location(LocationName.s2e6_ashes, player),
             lambda state: state.has(ItemName.s2e6_urn, player))

    # S2E8
    add_rule(world.get_location(LocationName.s2e8_pu_r, player),
             lambda state: state.has(ItemName.ibinoculars, player))
    add_rule(world.get_location(LocationName.s2e8_pu_l, player),
             lambda state: state.has(ItemName.ibinoculars, player))

    world.completion_condition[player] = lambda state: state.has(ItemName.clear, player, total_required_episodes)
