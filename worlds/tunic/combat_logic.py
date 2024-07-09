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
    equipment: List[str] = []


area_data: Dict[str, AreaStats] = {
    # The upgrade page is right by the Well entrance. Upper Overworld by the chest in the top right might need something
    "Overworld": AreaStats(1, 1, 1, 1, 1, 1, 0, ["Stick"]),
    "East Forest": AreaStats(1, 1, 1, 1, 1, 1, 0, ["Stick"]),
    # learn how to upgrade
    "Beneath the Well": AreaStats(2, 1, 3, 3, 1, 1, 3, ["Sword", "Shield"]),
    "Dark Tomb": AreaStats(2, 2, 3, 3, 1, 1, 3, ["Sword", "Shield"]),
    "West Garden": AreaStats(2, 3, 3, 3, 1, 1, 4, ["Sword", "Shield"]),
    "Garden Knight": AreaStats(3, 3, 3, 3, 2, 1, 4, ["Sword", "Shield"]),
    # get the wand here
    "Beneath the Vault": AreaStats(3, 3, 3, 3, 2, 1, 4, ["Sword", "Shield", "Magic Wand"]),
    "Eastern Vault Fortress": AreaStats(3, 3, 3, 4, 3, 2, 4, ["Sword", "Shield", "Magic Wand"]),
    "Frog's Domain": AreaStats(3, 4, 3, 5, 3, 3, 4, ["Sword", "Shield", "Magic Wand"]),
    # the second half of Atoll is the part you need the stats for, so putting it after frogs
    "Ruined Atoll": AreaStats(4, 4, 3, 5, 3, 3, 5, ["Sword", "Shield", "Magic Wand"]),
    "The Librarian": AreaStats(4, 4, 3, 5, 3, 3, 5, ["Sword", "Shield", "Magic Wand"]),
    "Quarry": AreaStats(5, 4, 3, 5, 3, 3, 5, ["Sword", "Shield", "Magic Wand"]),
    "Rooted Ziggurat": AreaStats(5, 5, 3, 5, 3, 3, 6, ["Sword", "Shield", "Magic Wand"]),
    "Swamp": AreaStats(1, 1, 1, 1, 1, 1, 6, ["Sword", "Shield", "Magic Wand"]),
    "Cathedral": AreaStats(1, 1, 1, 1, 1, 1, 6, ["Sword", "Shield", "Magic Wand"]),
    "The Heir": AreaStats(5, 5, 3, 5, 3, 3, 6, ["Sword", "Shield", "Magic Wand"]),
}


def has_combat_reqs(area_name: str, state: CollectionState, player: int) -> bool:
    data = area_data[area_name]
    for item in data.equipment:
        if item == "Stick" and not has_melee(state, player):
            return False
        elif item == "Sword" and not has_sword(state, player):
            return False
        else:
            if not state.has(item, player):
                return False
    if not has_required_stats(data, state, player):
        return False
    return True


def has_required_stats(data: AreaStats, state: CollectionState, player: int) -> bool:
    # for now, just check if you have the vanilla stat requirements, can get more advanced later
    if data.att_level > 1 and get_att_level(state, player) < data.att_level:
        return False
    if data.def_level > 1 and get_def_level(state, player) < data.def_level:
        return False
    if data.potion_level > 1 and get_potion_level(state, player) < data.potion_level:
        return False
    if data.hp_level > 1 and get_hp_level(state, player) < data.hp_level:
        return False
    if data.sp_level > 1 and get_sp_level(state, player) < data.sp_level:
        return False
    if data.mp_level > 1 and get_mp_level(state, player) < data.mp_level:
        return False
    if data.potion_count > 0 and get_potion_count(state, player) < data.potion_count:
        return False
    return True


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


def get_potion_count(state: CollectionState, player: int) -> int:
    return state.count("Potion Flask", player) + state.count("Flask Shard", player) // 3
