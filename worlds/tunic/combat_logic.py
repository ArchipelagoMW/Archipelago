from typing import Dict, List, NamedTuple
from BaseClasses import CollectionState
from .rules import has_sword, has_melee


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
    is_boss: bool = False


area_data: Dict[str, AreaStats] = {
    # The upgrade page is right by the Well entrance. Upper Overworld by the chest in the top right might need something
    "Overworld": AreaStats(1, 1, 1, 1, 1, 1, 0, ["Stick"]),
    "East Forest": AreaStats(1, 1, 1, 1, 1, 1, 0, ["Sword"]),
    "Before Well": AreaStats(1, 1, 1, 1, 1, 1, 3, ["Sword", "Shield"]),
    # learn how to upgrade
    "Beneath the Well": AreaStats(2, 1, 3, 3, 1, 1, 3, ["Sword", "Shield"]),
    "Dark Tomb": AreaStats(2, 2, 3, 3, 1, 1, 3, ["Sword", "Shield"]),
    "West Garden": AreaStats(2, 3, 3, 3, 1, 1, 4, ["Sword", "Shield"]),
    "Garden Knight": AreaStats(3, 3, 3, 3, 2, 1, 4, ["Sword", "Shield"], is_boss=True),
    # get the wand here
    "Beneath the Vault": AreaStats(3, 3, 3, 3, 2, 1, 4, ["Sword", "Shield", "Magic"]),
    "Eastern Vault Fortress": AreaStats(3, 3, 3, 4, 3, 2, 4, ["Sword", "Shield", "Magic"]),
    "Siege Engine": AreaStats(3, 3, 3, 4, 3, 2, 4, ["Sword", "Shield", "Magic"], is_boss=True),
    "Frog's Domain": AreaStats(3, 4, 3, 5, 3, 3, 4, ["Sword", "Shield", "Magic"]),
    # the second half of Atoll is the part you need the stats for, so putting it after frogs
    "Ruined Atoll": AreaStats(4, 4, 3, 5, 3, 3, 5, ["Sword", "Shield", "Magic"]),
    "The Librarian": AreaStats(4, 4, 3, 5, 3, 3, 5, ["Sword", "Shield", "Magic"], is_boss=True),
    "Quarry": AreaStats(5, 4, 3, 5, 3, 3, 5, ["Sword", "Shield", "Magic"]),
    "Rooted Ziggurat": AreaStats(5, 5, 3, 5, 3, 3, 6, ["Sword", "Shield", "Magic"]),
    "Boss Scavenger": AreaStats(5, 5, 3, 5, 3, 3, 6, ["Sword", "Shield", "Magic"], is_boss=True),
    "Swamp": AreaStats(1, 1, 1, 1, 1, 1, 6, ["Sword", "Shield", "Magic"]),
    "Cathedral": AreaStats(1, 1, 1, 1, 1, 1, 6, ["Sword", "Shield", "Magic"]),
    "Gauntlet": AreaStats(1, 1, 1, 1, 1, 1, 6, ["Sword", "Shield", "Magic"]),
    "The Heir": AreaStats(5, 5, 3, 5, 3, 3, 6, ["Sword", "Shield", "Magic", "Laurels"], is_boss=True),
}


def has_combat_reqs(area_name: str, state: CollectionState, player: int) -> bool:
    data = area_data[area_name]
    extra_att_needed = 0
    extra_def_needed = 0
    extra_mp_needed = 0
    has_magic = state.has_any({"Magic Wand", "Gun"}, player)
    for item in data.equipment:
        if item == "Stick":
            if not has_melee(state, player):
                if has_magic:
                    # magic can make up for the lack of stick
                    extra_mp_needed += 2
                    extra_att_needed -= 16
                else:
                    return False

        elif item == "Sword":
            if not has_sword(state, player):
                # need sword for bosses
                if data.is_boss:
                    return False
                if has_magic:
                    # +4 mp pretty much makes up for the lack of sword, at least in Quarry
                    extra_mp_needed += 4
                    # stick is a backup plan, and doesn't scale well, so let's require a little less
                    extra_att_needed -= 2
                elif has_melee(state, player):
                    # may revise this later based on feedback
                    extra_att_needed += 3
                    extra_def_needed += 2
                else:
                    return False
        elif item == "Shield":
            if not state.has("Shield", player):
                extra_def_needed += 2
        elif item == "Laurels":
            if not state.has("Hero's Laurels", player):
                # these are entirely based on vibes
                extra_att_needed += 2
                extra_def_needed += 3
        elif item == "Magic":
            if not has_magic:
                extra_att_needed += 2
                extra_def_needed += 2
                extra_mp_needed -= 16
    modified_stats = AreaStats(data.att_level + extra_att_needed, data.def_level + extra_def_needed, data.potion_level,
                               data.hp_level, data.sp_level, data.mp_level + extra_mp_needed, data.potion_count)
    if not has_required_stats(modified_stats, state, player):
        return False
    return True


def has_required_stats(data: AreaStats, state: CollectionState, player: int) -> bool:
    # for now, just check if you have the vanilla stat requirements, can get more advanced later
    player_att = get_att_level(state, player)
    if player_att < data.att_level:
        return False
    # adding defense and sp together since they accomplish similar things: making you take less damage
    if (data.def_level + data.sp_level > 2
            and get_def_level(state, player) + get_sp_level(state, player) < data.def_level + data.sp_level):
        return False
    # if you have 2 more attack than needed, we can forego needing mp
    if not player_att > data.att_level + 2:
        if data.mp_level > 1 and get_mp_level(state, player) < data.mp_level:
            return False

    req_hp = 60 + data.hp_level * 20
    # required hp if you include your potions at 75% healing effectiveness
    req_effective_hp = req_hp + .75 * min(20 + data.potion_level * 10, req_hp) * data.potion_count
    if get_effective_hp(state, player) < req_effective_hp:
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
    # your third potion upgrade (from offerings) costs 1,000 money, reasonable to assume you won't do that
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
