from typing import Callable, TYPE_CHECKING

from BaseClasses import CollectionState

if TYPE_CHECKING:
    from . import SohWorld


def get_soh_rule(world: "SohWorld") -> Callable[[CollectionState], bool]:

    return lambda state: True


def has_explosives(state: CollectionState, world: "SohWorld") -> bool:
    return can_use("Bomb Bag", state, world) or can_use("Bombchus", state, world)


def blast_or_smash(state: CollectionState, world: "SohWorld") -> bool:
    return has_explosives(state, world) or can_use("Megaton Hammer", state, world)


def blue_fire(state: CollectionState, world: "SohWorld") -> bool:
    return can_use("Bottle with Blue Fire", state, world)  # or blue fire arrows


def can_break_mud_walls(state: CollectionState, world: "SohWorld") -> bool:
    # todo: logic goes here
    return blast_or_smash(state, world) or (can_do_trick("Blue Fire Mud Walls", state, world) and blue_fire(state, world))


def is_adult(state: CollectionState, world: "SohWorld") -> bool:
    # todo: logic goes here
    # also maybe this will be handled differently, idk yet, this is just a placeholder
    return True


def has_explosives(state: CollectionState, world: "SohWorld") -> bool:
    # todo: logic goes here
    return True


def can_attack(state: CollectionState, world: "SohWorld") -> bool:
    # todo: logic goes here
    return True


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
    # todo: logic goes here
    # this one might end up having some complicated backend
    return True


def can_do_trick(trick: str, state: CollectionState, world: "SohWorld") -> bool:
    # todo: logic goes here
    return True


def can_jump_slash(state: CollectionState, world: "SohWorld") -> bool:
    # todo: logic goes here
    return True
