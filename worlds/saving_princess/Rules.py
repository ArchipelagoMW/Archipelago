from typing import TYPE_CHECKING, Optional
from BaseClasses import CollectionState, Location, Entrance
from worlds.generic.Rules import set_rule
from .Constants import *

if TYPE_CHECKING:
    from . import SavingPrincessWorld


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
                state.has(ITEM_MAX_HEALTH, world.player)
                and state.has(ITEM_MAX_AMMO, world.player)
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

    # all special weapons required so that the boss' weapons can be targeted
    def all_weapons(state: CollectionState) -> bool:
        return state.has_all({ITEM_WEAPON_FIRE, ITEM_WEAPON_ICE, ITEM_WEAPON_VOLT}, world.player)

    def is_gate_unlocked(state: CollectionState) -> bool:
        # the gate unlocks with all 4 boss keys, although this only applies to extended pool
        if world.is_pool_expanded:
            # in expanded, the final area requires all the boss keys
            return (
                    state.has_from_list_unique(
                        [EP_ITEM_GUARD_GONE, EP_ITEM_CLIFF_GONE, EP_ITEM_ACE_GONE, EP_ITEM_SNAKE_GONE],
                        world.player,
                        world.final_locks
                    ) and super_nice_check(state)
            )
        else:
            # in base pool, check that the main area bosses can be defeated
            return state.has_from_list_unique(
                [EVENT_ITEM_GUARD_GONE, EVENT_ITEM_CLIFF_GONE, EVENT_ITEM_ACE_GONE, EVENT_ITEM_SNAKE_GONE],
                world.player,
                world.final_locks
            ) and super_nice_check(state)

    def is_power_on(state: CollectionState) -> bool:
        # in expanded pool, the power item is what determines this, else it happens when the generator is powered
        return state.has(EP_ITEM_POWER_ON if world.is_pool_expanded else EVENT_ITEM_POWER_ON, world.player)

    # return the required special weapon to open a door of the given type
    def door_to_weapon(door_type: DoorType) -> Optional[str]:
        match door_type:
            case DoorType.DOOR_TYPE_NONE:
                return None
            case DoorType.DOOR_TYPE_POWER:
                return ITEM_WEAPON_CHARGE
            case DoorType.DOOR_TYPE_FIRE:
                return ITEM_WEAPON_FIRE
            case DoorType.DOOR_TYPE_ICE:
                return ITEM_WEAPON_ICE
            case DoorType.DOOR_TYPE_VOLT:
                return ITEM_WEAPON_VOLT

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
    # generator cannot be turned on without the volt laser
    set_rule(
        get_location(EP_LOCATION_ELECTRICAL_EXTRA if world.is_pool_expanded else EVENT_LOCATION_POWER_ON),
        lambda state: state.has(ITEM_WEAPON_VOLT, world.player)
    )
    # the roller is not very intuitive to get past without 4 ammo
    set_rule(get_location(LOCATION_CAVE_WEAPON), lambda state: state.has(ITEM_MAX_AMMO, world.player))
    set_rule(
        get_location(EP_LOCATION_CAVE_BOSS if world.is_pool_expanded else EVENT_LOCATION_GUARD_GONE),
        lambda state: state.has(ITEM_MAX_AMMO, world.player)
    )

    # guarantee some upgrades to be found before bosses
    boss_locations = [LOCATION_VOLCANIC_WEAPON, LOCATION_ARCTIC_WEAPON, LOCATION_SWAMP_SPECIAL]
    if world.is_pool_expanded:
        boss_locations += [EP_LOCATION_VOLCANIC_BOSS, EP_LOCATION_ARCTIC_BOSS, EP_LOCATION_SWAMP_BOSS]
    else:
        boss_locations += [EVENT_LOCATION_CLIFF_GONE, EVENT_LOCATION_ACE_GONE, EVENT_LOCATION_SNAKE_GONE]
    for location_name in boss_locations:
        set_rule(get_location(location_name), lambda state: nice_check(state))

    # set the basic access rules for the regions, these are all behind blast doors
    weapon_needed: Optional[str] = door_to_weapon(world.volcanic_door)
    if weapon_needed:
        set_rule(get_region_entrance(REGION_VOLCANIC), lambda state: state.has(weapon_needed, world.player))
    weapon_needed = door_to_weapon(world.arctic_door)
    if weapon_needed:
        set_rule(get_region_entrance(REGION_ARCTIC), lambda state: state.has(weapon_needed, world.player))
    weapon_needed = door_to_weapon(world.swamp_door)
    if weapon_needed:
        set_rule(get_region_entrance(REGION_SWAMP), lambda state: state.has(weapon_needed, world.player))

    # now for the final area regions, which have different rules based on if ep is on
    set_rule(get_region_entrance(REGION_ELECTRICAL), lambda state: is_gate_unlocked(state))
    set_rule(get_region_entrance(REGION_ELECTRICAL_POWERED), lambda state: is_power_on(state))

    # brainos requires all weapons, cannot destroy the cannons otherwise
    if world.is_pool_expanded:
        set_rule(get_location(EP_LOCATION_ELECTRICAL_FINAL_BOSS), lambda state: all_weapons(state))
    # and we need to beat brainos to beat the game
    set_rule(get_location(EVENT_LOCATION_VICTORY), lambda state: all_weapons(state))

    # if not expanded pool, place the events for the boss kills and generator
    if not world.is_pool_expanded:
        # accessible with no items
        cave_item = world.create_item(EVENT_ITEM_GUARD_GONE)
        get_location(EVENT_LOCATION_GUARD_GONE).place_locked_item(cave_item)
        volcanic_item = world.create_item(EVENT_ITEM_CLIFF_GONE)
        get_location(EVENT_LOCATION_CLIFF_GONE).place_locked_item(volcanic_item)
        arctic_item = world.create_item(EVENT_ITEM_ACE_GONE)
        get_location(EVENT_LOCATION_ACE_GONE).place_locked_item(arctic_item)
        swamp_item = world.create_item(EVENT_ITEM_SNAKE_GONE)
        get_location(EVENT_LOCATION_SNAKE_GONE).place_locked_item(swamp_item)
        power_item = world.create_item(EVENT_ITEM_POWER_ON)
        get_location(EVENT_LOCATION_POWER_ON).place_locked_item(power_item)

    # set the victory event
    victory_item = world.create_item(EVENT_ITEM_VICTORY)
    get_location(EVENT_LOCATION_VICTORY).place_locked_item(victory_item)
    world.multiworld.completion_condition[world.player] = lambda state: state.has(EVENT_ITEM_VICTORY, world.player)

    # if we have battle log locations on, set their rules
    if not world.has_battle_log:
        return
    # hub
    set_rule(get_location(BL_LOCATION_GUARD),
             lambda state: state.can_reach_location(LOCATION_HUB_AMMO, world.player))
    # cave
    set_rule(get_location(BL_LOCATION_ROLLER),
             lambda state: state.can_reach_location(LOCATION_CAVE_WEAPON, world.player))
    if world.is_pool_expanded:
        set_rule(get_location(BL_LOCATION_CAVE_BOSS),
                 lambda state: state.can_reach_location(EP_LOCATION_CAVE_BOSS, world.player))
    else:
        set_rule(get_location(BL_LOCATION_CAVE_BOSS),
                 lambda state: state.has(EVENT_ITEM_GUARD_GONE, world.player))
    # volcanic
    region = world.get_region(REGION_VOLCANIC)
    set_rule(get_location(BL_LOCATION_GOLD_CRAB),
             lambda state: state.can_reach(region, world.player))
    set_rule(get_location(BL_LOCATION_FLY),
             lambda state: state.can_reach(region, world.player))
    set_rule(get_location(BL_LOCATION_HOPPER),
             lambda state: state.can_reach(region, world.player))
    set_rule(get_location(BL_LOCATION_FIRE_GUARD),  # this enemy is immune to fire
             lambda state: state.can_reach(region, world.player)
             and state.has_any({ITEM_WEAPON_CHARGE, ITEM_WEAPON_ICE, ITEM_WEAPON_VOLT}, world.player))
    set_rule(get_location(BL_LOCATION_VOLCANIC_BOSS),
             lambda state: state.can_reach_location(LOCATION_VOLCANIC_WEAPON, world.player))
    # arctic
    region = world.get_region(REGION_ARCTIC)
    set_rule(get_location(BL_LOCATION_BAT),
             lambda state: state.can_reach(region, world.player))
    set_rule(get_location(BL_LOCATION_FLEA_EGG),
             lambda state: state.can_reach(region, world.player))
    set_rule(get_location(BL_LOCATION_FLEA),
             lambda state: state.can_reach(region, world.player))
    set_rule(get_location(BL_LOCATION_ARCTIC_BOSS),
             lambda state: state.can_reach_location(LOCATION_ARCTIC_WEAPON, world.player))
    # swamp
    set_rule(get_location(BL_LOCATION_MIDGE),
             lambda state: state.can_reach_region(REGION_SWAMP, world.player))
    set_rule(get_location(BL_LOCATION_SWAMP_BOSS),
             lambda state: state.can_reach_location(LOCATION_SWAMP_SPECIAL, world.player))
    # electrical
    region = world.get_region(REGION_ELECTRICAL)
    set_rule(get_location(BL_LOCATION_NINJA_FIGHT),
             lambda state: state.can_reach(region, world.player))
    set_rule(get_location(BL_LOCATION_ELECTRICAL_MINIBOSS),
             lambda state: state.can_reach(region, world.player))
    set_rule(get_location(BL_LOCATION_ELECTRICAL_BOSS),
             lambda state: state.can_reach_region(REGION_ELECTRICAL_POWERED, world.player))
    set_rule(get_location(BL_LOCATION_ELECTRICAL_FINAL_BOSS),
             lambda state: state.has(EVENT_ITEM_VICTORY, world.player))
