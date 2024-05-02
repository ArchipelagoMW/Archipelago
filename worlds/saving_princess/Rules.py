from BaseClasses import CollectionState, Location, Entrance
from worlds.generic.Rules import set_rule

from .Constants import *


def set_rules(world: "SavingPrincessWorld"):
    def get_location(name: str) -> Location:
        return world.get_location(name)

    def get_region_entrance(name: str) -> Entrance:
        return world.get_entrance(f"{name} entrance")

    def can_hover(state: CollectionState) -> bool:
        # portia can hover if she has a weapon other than the powered blaster and 4 reload speed upgrades
        return (
                state.has(ITEM_RELOAD_SPEED, world.player, 4)
                and state.has_any({ITEM_WEAPON_FIRE, ITEM_WEAPON_ICE, ITEM_WEAPON_VOLT}, world.player)
        )

    # guarantees that the player will have some upgrades before having to face the area bosses, except for cave
    def nice_check(state: CollectionState) -> bool:
        return (
                state.has(ITEM_MAX_HEALTH, world.player, 1)
                and state.has(ITEM_MAX_AMMO, world.player, 1)
                and state.has(ITEM_RELOAD_SPEED, world.player, 2)
        )

    # same as above, but for the final area
    def super_nice_check(state: CollectionState) -> bool:
        return (
                state.has(ITEM_MAX_HEALTH, world.player, 2)
                and state.has(ITEM_MAX_AMMO, world.player, 2)
                and state.has(ITEM_RELOAD_SPEED, world.player, 4)
                and state.has(ITEM_WEAPON_CHARGE, world.player)
                # at least one special weapon, other than powered blaster
                and state.has_any({ITEM_WEAPON_FIRE, ITEM_WEAPON_ICE, ITEM_WEAPON_VOLT}, world.player)
        )

    def is_gate_unlocked(state: CollectionState) -> bool:
        # the gate unlocks with all 4 boss keys, although this only applies to extended pool
        if world.is_pool_expanded:
            # in expanded, the final area requires all the boss keys
            return (
                    state.has_all(
                        {EP_ITEM_GUARD_GONE, EP_ITEM_CLIFF_GONE, EP_ITEM_ACE_GONE, EP_ITEM_SNAKE_GONE},
                        world.player
                    ) and super_nice_check(state)
            )
        else:
            # in base pool, just the powered blaster is enough to guarantee access to the final area
            return super_nice_check(state)

    def is_power_on(state: CollectionState) -> bool:
        if world.is_pool_expanded:
            # in expanded pool, the power item is what determines this
            return state.has(EP_ITEM_POWER_ON, world.player)
        else:
            # in base pool, volt laser plus the gate condition is enough
            return state.has(ITEM_WEAPON_VOLT, world.player)

    # set the location rules
    # this is behind the blast door to arctic
    set_rule(get_location(LOCATION_HUB_AMMO), lambda state: state.has(ITEM_WEAPON_CHARGE, world.player))
    # these are behind frozen doors
    for location_name in [LOCATION_ARCTIC_HEALTH, LOCATION_JACKET]:
        set_rule(get_location(location_name), lambda state: state.has(ITEM_WEAPON_FIRE, world.player))
    # these would require damage boosting otherwise
    set_rule(get_location(LOCATION_VOLCANIC_RELOAD),
             lambda state: state.has(ITEM_WEAPON_ICE, world.player) or can_hover(state))
    set_rule(get_location(LOCATION_SWAMP_AMMO), lambda state: can_hover(state))
    if world.is_pool_expanded:
        # does not spawn until the guard has been defeated
        set_rule(get_location(EP_LOCATION_HUB_NINJA_SCARE), lambda state: state.has(EP_ITEM_GUARD_GONE, world.player))
        # cannot be turned on without the volt laser
        set_rule(get_location(EP_LOCATION_ELECTRICAL_EXTRA), lambda state: state.has(ITEM_WEAPON_VOLT, world.player))

    # the roller is not very intuitive to get past without 4 ammo
    set_rule(get_location(LOCATION_CAVE_WEAPON), lambda state: state.has(ITEM_MAX_AMMO, world.player))
    if world.is_pool_expanded:
        set_rule(get_location(EP_LOCATION_CAVE_BOSS), lambda state: state.has(ITEM_MAX_AMMO, world.player))

    # guarantee some upgrades to be found before bosses
    boss_locations = [LOCATION_VOLCANIC_WEAPON, LOCATION_ARCTIC_WEAPON, LOCATION_SWAMP_SPECIAL]
    if world.is_pool_expanded:
        boss_locations += [EP_LOCATION_VOLCANIC_BOSS, EP_LOCATION_ARCTIC_BOSS, EP_LOCATION_SWAMP_BOSS]
    for location_name in boss_locations:
        set_rule(get_location(location_name), lambda state: nice_check(state))

    # set the basic access rules for the regions, these are all behind blast doors
    for region_name in [REGION_VOLCANIC, REGION_ARCTIC, REGION_SWAMP]:
        set_rule(get_region_entrance(region_name), lambda state: state.has(ITEM_WEAPON_CHARGE, world.player))

    # now for the final area regions, which have different rules based on if ep is on
    set_rule(get_region_entrance(REGION_ELECTRICAL), lambda state: is_gate_unlocked(state))
    set_rule(get_region_entrance(REGION_ELECTRICAL_POWERED), lambda state: is_power_on(state))

    # and, finally, set the victory event
    victory_item = world.create_item(EVENT_ITEM_VICTORY)
    get_location(EVENT_LOCATION_VICTORY).place_locked_item(victory_item)
    world.multiworld.completion_condition[world.player] = lambda state: state.has(EVENT_ITEM_VICTORY, world.player)
