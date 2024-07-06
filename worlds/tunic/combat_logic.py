from typing import Dict, List, NamedTuple
from BaseClasses import CollectionState
from .rules import has_sword, has_melee

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
    # pink and blue slimes really only need a stick
    "Slimes": EncounterData(0),
    "Rudelings": EncounterData(4),
    "Shield Rudelings": EncounterData(6),
    # just gets stunlocked with a stick
    "Spyrites": EncounterData(4),
    "Sappharachs": EncounterData(12),
    # can deal with single big crabs and any amount of small crabs with just stick
    "Crabs": EncounterData(0),
    "Slorms": EncounterData(8, [[sword], [fire_wand], [gun], [stick, shield]], False),
    # the birds that swoop down at you
    "Hushers": EncounterData(12),
    # can't damage with stick
    "Autobolts": EncounterData(8, [[sword], [fire_wand], [gun]], False),
    "Chompignoms": EncounterData(8),
    "Fairies": EncounterData(0, [[fire_wand], [gun], [grapple]]),
    # just fortress in general
    "Wizards": EncounterData(12),
    # just frog's domain in general
    "Frogues": EncounterData(12),
    # includes shield fleemers
    "Fleemers": EncounterData(8),
    "Big Fleemer": EncounterData(12),
    "Lost Echoes": EncounterData(8),
    "Birds with Guns": EncounterData(12),
    "Tentacles": EncounterData(12),
    # you're meant to fight them with sword, wand, shield, and some flasks
    "Foxes": EncounterData(10),
    "Scavengers": EncounterData(16),
    "Scav Snipers": EncounterData(16, [[fire_wand], [grapple]]),

    # can't damage with stick
    "Garden Knight": EncounterData(12, [[sword]], False),
    "Siege Engine": EncounterData(16),
    "Librarian": EncounterData(16, [[fire_wand], [gun]]),
    "Boss Scavenger": EncounterData(24),
    "Gauntlet": EncounterData(10, [[sword, fire_wand], [sword, gun]]),
    # the other heir requirements are included in the entrance rule for the heir fight
    "The Heir": EncounterData(28),
}


def has_combat_logic(encounters: List[str], state: CollectionState, player: int) -> bool:
    encounter_data: List[EncounterData] = [enemy_encounters[name] for name in encounters]
    # if you do not meet the item requirements for any of the encounters, you cannot proceed
    for data in encounter_data:
        if not has_required_items(data.items_required, data.stick_required, state, player):
            return False
    # if you met the item requirements, and you have enough power, then you may proceed
    level_req: int = max(data.power_required for data in encounter_data)
    # the not level_req is to short circuit early for spots with combat level 0
    if not level_req or sum_power(state, player) >= level_req:
        return True


def has_required_items(required_items: List[List[str]], stick_req: bool, state: CollectionState, player: int) -> bool:
    # stick required for power unless excepted
    if stick_req and not has_melee(state, player):
        return False
    if not required_items:
        return True

    for reqs in required_items:
        # stick and sword have special handling because of the progressive sword option
        if sword in reqs:
            # state.has_all returns true for an empty list
            if has_sword(state, player) and state.has_all([item for item in reqs if item != sword], player):
                return True
        elif stick in reqs:
            if has_melee(state, player) and state.has_all([item for item in reqs if item != stick], player):
                return True
        else:
            if state.has_all(reqs, player):
                return True
    return False


def sum_power(state: CollectionState, player: int) -> int:
    return (get_att_power(state, player) + get_def_power(state, player) + get_potion_power(state, player)
            + get_hp_power(state, player) + get_mp_power(state, player) + get_other_power(state, player))


def get_att_power(state: CollectionState, player: int) -> int:
    # no stick, no power
    if not has_melee(state, player):
        return False
    power = state.count_from_list({"ATT Offering", "Hero Relic - ATT"}, player)
    sword_upgrades = state.count("Sword Upgrade", player)
    # +4 power from sword, +2 power for the next two sword (includes the attack buff from getting it)
    if sword_upgrades >= 2:
        power += max(8, sword_upgrades * 2)
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
