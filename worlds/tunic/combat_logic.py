from typing import Dict, List, NamedTuple, TYPE_CHECKING
from BaseClasses import CollectionState
from .rules import has_sword, has_stick
if TYPE_CHECKING:
    from . import TunicWorld

stick = "Stick"
sword = "Sword"
shield = "Shield"
laurels = "Hero's Laurels"
fire_wand = "Magic Wand"
gun = "Gun"
grapple = "Magic Orb"


class EncounterData(NamedTuple):
    power_required: int  # how strong you need to be to do the encounter
    items_required: List[List[str]] = []  # any(all(requirements))
    stick_required: bool = True  # by default, you need a stick. but for some, you may not need one if you have alts


# general requirements for enemy encounters in the game, for use in determining whether you can access a chest
enemy_encounters: Dict[str, EncounterData] = {
    # pink slimes are basically free
    "Blue Slimes": EncounterData(0),
    "Rudelings": EncounterData(4),
    "Shield Rudelings": EncounterData(6),
    # just gets stunlocked with a stick
    "Spyrites": EncounterData(4),
    "Sappharachs": EncounterData(12),
    # can deal with single big crabs and any amount of small crabs with just stick
    "Crabs": EncounterData(0),
    "Slorms": EncounterData(8, [[sword], [fire_wand], [gun], [stick, shield]], False),
    # includes shield fleemers
    "Fleemers": EncounterData(8),
    "Big Fleemer": EncounterData(12),
    "Lost Echo": EncounterData(0, [[sword]]),
    "Autobolts": EncounterData(8, [[sword], [fire_wand], [gun]], False),
    "Chompignoms": EncounterData(8),
    "Fairies": EncounterData(0, [[fire_wand], [gun], [grapple]]),
    # and custodians
    "Wizards": EncounterData(12),
    # just frog's domain in general, basically
    "Frogues": EncounterData(12),
    "Birds with Guns": EncounterData(12),
    # you're meant to fight them with sword, wand, shield, no stats
    "Foxes": EncounterData(8),

    "Garden Knight": EncounterData(12, [[sword]], False),
    "Siege Engine": EncounterData(16),
    "Librarian": EncounterData(16, [[fire_wand], [gun]]),
    "Boss Scavenger": EncounterData(20),
    # the other heir requirements are included in the entrance rule for the heir fight
    "The Heir": EncounterData(24),
}


def has_combat_logic(level: int, required_items: List[str], state: CollectionState, player: int) -> bool:
    # no stick, no power
    if not has_stick(state, player):
        return False
    # if level required is 0, just return true, you already have stick
    if level == 0:
        return True
    # use the helper for sword
    if "Sword" in required_items and not has_sword(state, player):
        return False
    else:
        required_items.remove("Sword")

    if required_items and not state.has_all(required_items, player):
        return False
    power = (get_att_power(state, player) + get_def_power(state, player) + get_potion_power(state, player)
             + get_hp_power(state, player) + get_mp_power(state, player) + get_other_power(state, player))
    return True if power >= level else False


def get_att_power(state: CollectionState, player: int) -> int:
    # not relevant if you don't have a weapon that benefits from attack
    if not has_stick(state, player):
        return 0
    power = state.count_from_list({"ATT Offering", "Hero Relic - ATT"}, player)
    sword_upgrades = state.count("Sword Upgrade", player)
    # +4 power from sword, +2 power for the next two sword (includes the attack buff from getting it)
    if sword_upgrades >= 2:
        power += sword_upgrades * 2
    return power


# defense helps a lot when you're trying not to die, as it turns out
def get_def_power(state: CollectionState, player: int) -> int:
    return min(4, state.count_from_list({"DEF Offering", "Hero Relic - DEF", "Secret Legend", "Phonomath"}, player))


# healing is kinda power, right?
def get_potion_power(state: CollectionState, player: int) -> int:
    potion_count = state.count("Potion Flask", player) + state.count("Flask Shard", player) // 3
    if potion_count == 0:
        return 0
    power = min(3, potion_count // 2)
    # get potion upgrades
    power += min(3, state.count_from_list({"Potion Offering", "Hero Relic - POTION",
                                           "Just Some Pals", "Spring Falls", "Back To Work"}, player))
    return power


def get_hp_power(state: CollectionState, player: int) -> int:
    return min(3, state.count_from_list({"HP Offering", "Hero Relic - HP"}, player) // 2)


def get_mp_power(state: CollectionState, player: int) -> int:
    if not state.has_any({"Gun", "Magic Wand"}, player):
        return 0
    # default 2 power for having a wand or gun. Having both doesn't increase it since they do basically the same thing
    power = 2
    # max of 3 power from mp gains
    power += min(3, state.count_from_list({"MP Offering", "Hero Relic - MP",
                                           "Sacred Geometry", "Vintage", "Dusty"}, player))
    return power


def get_other_power(state: CollectionState, player: int) -> int:
    power = 0
    if state.has("Shield", player):
        power += 2
    if state.has("Hero's Laurels", player):
        power += 4
    return power
