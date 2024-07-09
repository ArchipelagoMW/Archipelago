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


# the vanilla stats you are expected to have to get through an area, based on where they are in vanilla
class AreaStats(NamedTuple):
    att_level: int
    def_level: int
    potion_level: int  # all 3 are before your first bonfire after getting the upgrade page, third costs 1k
    hp_level: int
    sp_level: int
    mp_level: int
    potion_count: int


area_data: Dict[str, AreaStats] = {
    # The upgrade page is right by the Well entrance. Upper Overworld by the chest in the top right might need something
    "Overworld": AreaStats(1, 1, 1, 1, 1, 1, 0),
    "East Forest": AreaStats(1, 1, 1, 1, 1, 1, 0),
    # learn how to upgrade
    "Beneath the Well": AreaStats(2, 1, 3, 3, 1, 1, 3),
    "Dark Tomb": AreaStats(2, 2, 3, 3, 1, 1, 3),
    "West Garden": AreaStats(2, 3, 3, 3, 1, 1, 4),
    "Garden Knight": AreaStats(3, 3, 3, 3, 2, 1, 4),
    # get the wand here
    "Beneath the Vault": AreaStats(3, 3, 3, 3, 2, 1, 4),
    "Eastern Vault Fortress": AreaStats(3, 3, 3, 4, 3, 2, 4),
    "Frog's Domain": AreaStats(3, 4, 3, 5, 3, 3, 4),
    # the second half of Atoll is the part you need the stats for, so putting it after frogs
    "Ruined Atoll": AreaStats(4, 4, 3, 5, 3, 3, 5),
    "Library": AreaStats(4, 4, 3, 5, 3, 3, 5),
    "Quarry": AreaStats(5, 4, 3, 5, 3, 3, 5),
    "Rooted Ziggurat": AreaStats(5, 5, 3, 5, 3, 3, 6),
    "Swamp": AreaStats(1, 1, 1, 1, 1, 1, 6),
    "Cathedral": AreaStats(1, 1, 1, 1, 1, 1, 6),
}


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


def get_effective_hp(state: CollectionState, player: int) -> int:
    # starting hp is 80, you get 20 per upgrade
    player_hp = 60 + get_hp_level(state, player) * 20
    potion_count = state.count("Potion Flask", player) + state.count("Flask Shard", player) // 3
    potion_upgrade_level = 1 + state.count_from_list({"Potion Offering", "Hero Relic - POTION",
                                                      "Just Some Pals", "Spring Falls", "Back To Work"}, player)
    # total health you get from potions
    total_healing = potion_count * (min(20 + 10 * potion_upgrade_level, player_hp))
    effective_hp = player_hp + total_healing * .75  # since you don't tend to use potions efficiently all the time

    # scale your extra mitigation based on your max stamina over your starting stamina
    return int(effective_hp)


def get_att_level(state: CollectionState, player: int) -> int:
    att_upgrades = state.count_from_list({"ATT Offering", "Hero Relic - ATT"}, player)
    sword_level = state.count("Sword Upgrade", player)
    if sword_level >= 3:
        att_upgrades += min(2, sword_level - 2)
    # attack falls off, can just cap it at 8 for simplicity
    return min(8, 1 + att_upgrades)


def get_def_level(state: CollectionState, player: int) -> int:
    # defense falls off, can just cap it at 8 for simplicity
    return min(8, 1 + state.count_from_list({"DEF Offering", "Hero Relic - DEF", "Secret Legend", "Phonomath"}, player))


def get_potion_level(state: CollectionState, player: int) -> int:
    potion_offering_count = state.count("Potion Offering", player)
    # getting from 3 to 4 potion costs 1,000 money, can assume most players will not do that
    return (1 + state.count_from_list({"Hero Relic - POTION", "Just Some Pals", "Spring Falls", "Back To Work"}, player)
            + min(2, potion_offering_count))


def get_hp_level(state: CollectionState, player: int) -> int:
    return 1 + state.count_from_list({"HP Offering", "Hero Relic - HP"}, player)


def get_sp_level(state: CollectionState, player: int) -> int:
    return 1 + state.count_from_list({"SP Offering", "Hero Relic - SP",
                                      "Mr Mayor", "Power Up", "Regal Weasel", "Forever Friend"}, player)


def get_mp_level(state: CollectionState, player: int) -> int:
    return 1 + state.count_from_list({"MP Offering", "Hero Relic - MP",
                                      "Sacred Geometry", "Vintage", "Dusty"}, player)
