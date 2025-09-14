from typing import Callable, TYPE_CHECKING

from BaseClasses import CollectionState

if TYPE_CHECKING:
    from . import SohWorld


def get_soh_rule(world: "SohWorld") -> Callable[[CollectionState], bool]:

    return lambda state: True


def has_explosives(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link has access to explosives (bombs or bombchus)."""
    return can_use("Bomb Bag", state, world) or can_use("Bombchus", state, world)


def blast_or_smash(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can blast or smash obstacles."""
    return has_explosives(state, world) or can_use("Megaton Hammer", state, world)


def blue_fire(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link has access to blue fire."""
    return can_use("Bottle with Blue Fire", state, world)  # or blue fire arrows


def has_bottle(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link has any bottle."""
    from .Logic import HasBottle
    return HasBottle(state, world)


def has_projectile(state: CollectionState, world: "SohWorld", age: str = "either") -> bool:
    """Check if Link has access to projectiles."""
    child_projectiles = (can_use("Fairy Slingshot", state, world) or 
                        can_use("Boomerang", state, world))
    adult_projectiles = (can_use("Hookshot", state, world) or 
                        can_use("Fairy Bow", state, world))
    
    if age == "child":
        return child_projectiles or has_explosives(state, world)
    elif age == "adult":
        return adult_projectiles or has_explosives(state, world)
    elif age == "both":
        return (child_projectiles and adult_projectiles) or has_explosives(state, world)
    else:  # "either"
        return child_projectiles or adult_projectiles or has_explosives(state, world)


def can_break_mud_walls(state: CollectionState, world: "SohWorld") -> bool:
    # todo: logic goes here
    return blast_or_smash(state, world) or (can_do_trick("Blue Fire Mud Walls", state, world) and blue_fire(state, world))


def is_adult(state: CollectionState, world: "SohWorld") -> bool:
    """
    Check if Link is an adult. In OoT, this typically means having access to adult-only items
    or having pulled the Master Sword from the Temple of Time.
    This is a simplified check - for more complex logic, use the can_be_adult parameter in CanUse.
    """
    # For now, return True as a placeholder since age logic is complex and context-dependent
    # The real age checking should be done through the CanUse function's can_be_adult parameter
    # TODO: Implement proper age checking based on world settings and progression
    return True


def can_damage(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can deal damage to enemies."""
    return (can_use("Fairy Slingshot", state, world) or 
            can_jump_slash(state, world) or 
            has_explosives(state, world) or 
            can_use("Din's Fire", state, world) or
            can_use("Fairy Bow", state, world))


def can_attack(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can attack enemies (damage or stun)."""
    return (can_damage(state, world) or 
            can_use("Boomerang", state, world) or
            can_use("Hookshot", state, world))


def can_shield(state: CollectionState, world: "SohWorld") -> bool:
    # todo: logic goes here
    return True


def take_damage(state: CollectionState, world: "SohWorld") -> bool:
    # todo: logic goes here
    return True


def can_kill_enemy(state: CollectionState, world: "SohWorld", enemy: str, combat_range: int, wall_or_floor: bool = True,
                   quantity: int = 1, timer: bool = False, in_water: bool = False) -> bool:
    # todo: logic goes here
    # also combat_range will probably be an enum or something
    return True


def has_fire_source_with_torch(state: CollectionState, world: "SohWorld") -> bool:
    # todo: logic goes here
    return True


def can_use(item_name: str, state: CollectionState, world: "SohWorld") -> bool:
    """
    Check if an item can be used based on the C++ Logic::CanUse implementation.
    This checks both if the item is possessed and if it can actually be used.
    """
    # Import here to avoid circular imports
    from .Logic import HasItem, CanUse
    
    # Use the existing CanUse function from Logic.py which already implements
    # the full C++ logic with proper age restrictions, magic requirements, etc.
    return CanUse(state, world, item_name)


def can_do_trick(trick: str, state: CollectionState, world: "SohWorld") -> bool:
    # todo: logic goes here
    return True


def can_jump_slash(state: CollectionState, world: "SohWorld") -> bool:
    """Check if Link can perform a jump slash with any sword."""
    return (can_use("Kokiri Sword", state, world) or 
            can_use("Master Sword", state, world) or 
            can_use("Biggoron's Sword", state, world) or
            can_use("Megaton Hammer", state, world))  # Hammer can substitute for sword in some cases
