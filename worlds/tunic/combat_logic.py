from typing import Dict, List, NamedTuple, Tuple, Optional
from enum import IntEnum
from collections import defaultdict
from BaseClasses import CollectionState
from .rules import has_sword, has_melee
from worlds.AutoWorld import LogicMixin


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


# the vanilla upgrades/equipment you would have
area_data: Dict[str, AreaStats] = {
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
    # marked as boss because the garden knights can't get hurt by stick
    "Gauntlet": AreaStats(1, 1, 1, 1, 1, 1, 6, ["Sword", "Shield", "Magic"], is_boss=True),
    "The Heir": AreaStats(5, 5, 3, 5, 3, 3, 6, ["Sword", "Shield", "Magic", "Laurels"], is_boss=True),
}


# these are used for caching which areas can currently be reached in state
boss_areas: List[str] = [name for name, data in area_data.items() if data.is_boss and name != "Gauntlet"]
non_boss_areas: List[str] = [name for name, data in area_data.items() if not data.is_boss]


class CombatState(IntEnum):
    unchecked = 0
    failed = 1
    succeeded = 2


def has_combat_reqs(area_name: str, state: CollectionState, player: int) -> bool:
    # we're caching whether you've met the combat reqs before if the state didn't change first
    # if the combat state is stale, mark each area's combat state as stale
    if state.tunic_need_to_reset_combat_from_collect[player]:
        state.tunic_need_to_reset_combat_from_collect[player] = False
        for name in area_data.keys():
            if state.tunic_area_combat_state[player][name] == CombatState.failed:
                state.tunic_area_combat_state[player][name] = CombatState.unchecked

    if state.tunic_need_to_reset_combat_from_remove[player]:
        state.tunic_need_to_reset_combat_from_remove[player] = False
        for name in area_data.keys():
            if state.tunic_area_combat_state[player][name] == CombatState.succeeded:
                state.tunic_area_combat_state[player][name] = CombatState.unchecked

    if state.tunic_area_combat_state[player][area_name] > CombatState.unchecked:
        return state.tunic_area_combat_state[player][area_name] == CombatState.succeeded

    met_combat_reqs = check_combat_reqs(area_name, state, player)

    # we want to skip the "none area" since we don't record its results
    if area_name not in area_data.keys():
        return met_combat_reqs

    # loop through the lists and set the easier/harder area states accordingly
    if area_name in boss_areas:
        area_list = boss_areas
    elif area_name in non_boss_areas:
        area_list = non_boss_areas
    else:
        area_list = [area_name]

    if met_combat_reqs:
        # set the state as true for each area until you get to the area we're looking at
        for name in area_list:
            state.tunic_area_combat_state[player][name] = CombatState.succeeded
            if name == area_name:
                break
    else:
        # set the state as false for the area we're looking at and each area after that
        reached_name = False
        for name in area_list:
            if name == area_name:
                reached_name = True
            if reached_name:
                state.tunic_area_combat_state[player][name] = CombatState.failed

    return met_combat_reqs


def check_combat_reqs(area_name: str, state: CollectionState, player: int, alt_data: Optional[AreaStats] = None) -> bool:
    data = alt_data or area_data[area_name]
    extra_att_needed = 0
    extra_def_needed = 0
    extra_mp_needed = 0
    has_magic = state.has_any({"Magic Wand", "Gun"}, player)
    stick_bool = False
    sword_bool = False
    for item in data.equipment:
        if item == "Stick":
            if not has_melee(state, player):
                if has_magic:
                    # magic can make up for the lack of stick
                    extra_mp_needed += 2
                    extra_att_needed -= 16
                else:
                    return False
            else:
                stick_bool = True

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
            else:
                sword_bool = True

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
        # we may need to check if you would have the required stats if you were missing a weapon
        # it's kinda janky, but these only get hit in less than once per 100 generations, so whatever
        if sword_bool and "Sword" in data.equipment and "Magic" in data.equipment:
            # we need to check if you would have the required stats if you didn't have melee
            equip_list = [item for item in data.equipment if item != "Sword"]
            more_modified_stats = AreaStats(data.att_level - 16, data.def_level, data.potion_level,
                                            data.hp_level, data.sp_level, data.mp_level + 4, data.potion_count,
                                            equip_list)
            if check_combat_reqs("none", state, player, more_modified_stats):
                return True

            # and we need to check if you would have the required stats if you didn't have magic
            equip_list = [item for item in data.equipment if item != "Magic"]
            more_modified_stats = AreaStats(data.att_level + 2, data.def_level + 2, data.potion_level,
                                            data.hp_level, data.sp_level, data.mp_level - 16, data.potion_count,
                                            equip_list)
            if check_combat_reqs("none", state, player, more_modified_stats):
                return True
            return False

        elif stick_bool and "Stick" in data.equipment and "Magic" in data.equipment:
            # we need to check if you would have the required stats if you didn't have the stick
            equip_list = [item for item in data.equipment if item != "Stick"]
            more_modified_stats = AreaStats(data.att_level - 16, data.def_level, data.potion_level,
                                            data.hp_level, data.sp_level, data.mp_level + 4, data.potion_count,
                                            equip_list)
            if check_combat_reqs("none", state, player, more_modified_stats):
                return True
            return False
        else:
            return False
    return True


# check if you have the required stats, and the money to afford them
# it may be innaccurate due to poor spending, and it may even require you to "spend poorly"
# but that's fine -- it's already pretty generous to begin with
def has_required_stats(data: AreaStats, state: CollectionState, player: int) -> bool:
    money_required = 0
    player_att = 0

    # check if we actually need the stat before checking state
    if data.att_level > 1:
        player_att, att_offerings = get_att_level(state, player)
        if player_att < data.att_level:
            return False
        else:
            extra_att = player_att - data.att_level
            paid_att = max(0, att_offerings - extra_att)
            # attack upgrades cost 100 for the first, +50 for each additional
            money_per_att = 100
            for _ in range(paid_att):
                money_required += money_per_att
                money_per_att += 50

    # adding defense and sp together since they accomplish similar things: making you take less damage
    if data.def_level + data.sp_level > 2:
        player_def, def_offerings = get_def_level(state, player)
        player_sp, sp_offerings = get_sp_level(state, player)
        if player_def + player_sp < data.def_level + data.sp_level:
            return False
        else:
            free_def = player_def - def_offerings
            free_sp = player_sp - sp_offerings
            paid_stats = data.def_level + data.sp_level - free_def - free_sp
            sp_to_buy = 0

            if paid_stats <= 0:
                # if you don't have to pay for any stats, you don't need money for these upgrades
                def_to_buy = 0
            elif paid_stats <= def_offerings:
                # get the amount needed to buy these def offerings
                def_to_buy = paid_stats
            else:
                def_to_buy = def_offerings
                sp_to_buy = max(0, paid_stats - def_offerings)

            # if you have to buy more than 3 def, it's cheaper to buy 1 extra sp
            if def_to_buy > 3 and sp_offerings > 0:
                def_to_buy -= 1
                sp_to_buy += 1
            # def costs 100 for the first, +50 for each additional
            money_per_def = 100
            for _ in range(def_to_buy):
                money_required += money_per_def
                money_per_def += 50
            # sp costs 200 for the first, +200 for each additional
            money_per_sp = 200
            for _ in range(sp_to_buy):
                money_required += money_per_sp
                money_per_sp += 200

    # if you have 2 more attack than needed, we can forego needing mp
    if data.mp_level > 1 and player_att < data.att_level + 2:
        player_mp, mp_offerings = get_mp_level(state, player)
        if player_mp < data.mp_level:
            return False
        else:
            extra_mp = player_mp - data.mp_level
            paid_mp = max(0, mp_offerings - extra_mp)
            # mp costs 300 for the first, +50 for each additional
            money_per_mp = 300
            for _ in range(paid_mp):
                money_required += money_per_mp
                money_per_mp += 50

    req_effective_hp = calc_effective_hp(data.hp_level, data.potion_level, data.potion_count)
    player_potion, potion_offerings = get_potion_level(state, player)
    player_hp, hp_offerings = get_hp_level(state, player)
    player_potion_count = get_potion_count(state, player)
    player_effective_hp = calc_effective_hp(player_hp, player_potion, player_potion_count)
    if player_effective_hp < req_effective_hp:
        return False
    else:
        # need a way to determine which of potion offerings or hp offerings you can reduce
        # your level if you didn't pay for offerings
        free_potion = player_potion - potion_offerings
        free_hp = player_hp - hp_offerings
        paid_hp_count = 0
        paid_potion_count = 0
        if calc_effective_hp(free_hp, free_potion, player_potion_count) >= req_effective_hp:
            # you don't need to buy upgrades
            pass
        # if you have no potions, or no potion upgrades, you only need to check your hp upgrades
        elif player_potion_count == 0 or potion_offerings == 0:
            # check if you have enough hp at each paid hp offering
            for i in range(hp_offerings):
                paid_hp_count = i + 1
                if calc_effective_hp(paid_hp_count, 0, player_potion_count) > req_effective_hp:
                    break
        else:
            for i in range(potion_offerings):
                paid_potion_count = i + 1
                if calc_effective_hp(free_hp, free_potion + paid_potion_count, player_potion_count) > req_effective_hp:
                    break
                for j in range(hp_offerings):
                    paid_hp_count = j + 1
                    if (calc_effective_hp(free_hp + paid_hp_count, free_potion + paid_potion_count, player_potion_count)
                            > req_effective_hp):
                        break
        # hp costs 200 for the first, +50 for each additional
        money_per_hp = 200
        for _ in range(paid_hp_count):
            money_required += money_per_hp
            money_per_hp += 50

        # potion costs 100 for the first, 300 for the second, 1,000 for the third, and +200 for each additional
        # currently we assume you will not buy past the second potion upgrade, but we might change our minds later
        money_per_potion = 100
        for _ in range(paid_potion_count):
            money_required += money_per_potion
            if money_per_potion == 100:
                money_per_potion = 300
            elif money_per_potion == 300:
                money_per_potion = 1000
            else:
                money_per_potion += 200

    if money_required > get_money_count(state, player):
        return False

    return True


# returns a tuple of your max attack level, the number of attack offerings
def get_att_level(state: CollectionState, player: int) -> Tuple[int, int]:
    att_offerings = state.count("ATT Offering", player)
    att_upgrades = state.count("Hero Relic - ATT", player)
    sword_level = state.count("Sword Upgrade", player)
    if sword_level >= 3:
        att_upgrades += min(2, sword_level - 2)
    # attack falls off, can just cap it at 8 for simplicity
    return min(8, 1 + att_offerings + att_upgrades), att_offerings


# returns a tuple of your max defense level, the number of defense offerings
def get_def_level(state: CollectionState, player: int) -> Tuple[int, int]:
    def_offerings = state.count("DEF Offering", player)
    # defense falls off, can just cap it at 8 for simplicity
    return (min(8, 1 + def_offerings
                + state.count_from_list({"Hero Relic - DEF", "Secret Legend", "Phonomath"}, player)),
            def_offerings)


# returns a tuple of your max potion level, the number of potion offerings
def get_potion_level(state: CollectionState, player: int) -> Tuple[int, int]:
    potion_offerings = min(2, state.count("Potion Offering", player))
    # your third potion upgrade (from offerings) costs 1,000 money, reasonable to assume you won't do that
    return (1 + potion_offerings
            + state.count_from_list({"Hero Relic - POTION", "Just Some Pals", "Spring Falls", "Back To Work"}, player),
            potion_offerings)


# returns a tuple of your max hp level, the number of hp offerings
def get_hp_level(state: CollectionState, player: int) -> Tuple[int, int]:
    hp_offerings = state.count("HP Offering", player)
    return 1 + hp_offerings + state.count("Hero Relic - HP", player), hp_offerings


# returns a tuple of your max sp level, the number of sp offerings
def get_sp_level(state: CollectionState, player: int) -> Tuple[int, int]:
    sp_offerings = state.count("SP Offering", player)
    return (1 + sp_offerings
            + state.count_from_list({"Hero Relic - SP", "Mr Mayor", "Power Up",
                                     "Regal Weasel", "Forever Friend"}, player),
            sp_offerings)


def get_mp_level(state: CollectionState, player: int) -> Tuple[int, int]:
    mp_offerings = state.count("MP Offering", player)
    return (1 + mp_offerings
            + state.count_from_list({"Hero Relic - MP", "Sacred Geometry", "Vintage", "Dusty"}, player),
            mp_offerings)


def get_potion_count(state: CollectionState, player: int) -> int:
    return state.count("Potion Flask", player) + state.count("Flask Shard", player) // 3


def calc_effective_hp(hp_level: int, potion_level: int, potion_count: int) -> int:
    player_hp = 60 + hp_level * 20
    # since you don't tend to use potions efficiently all the time, scale healing by .75
    total_healing = int(.75 * potion_count * min(player_hp, 20 + 10 * potion_level))
    return player_hp + total_healing


# returns the total amount of progression money the player has
def get_money_count(state: CollectionState, player: int) -> int:
    money: int = 0
    # this could be done with something to parse the money count at the end of the string, but I don't wanna
    money += state.count("Money x255", player) * 255  # 1 in pool
    money += state.count("Money x200", player) * 200  # 1 in pool
    money += state.count("Money x128", player) * 128  # 3 in pool
    # total from regular money: 839
    # first effigy is 8, doubles until it reaches 512 at number 7, after effigy 28 they stop dropping money
    # with the vanilla count of 12, you get 3,576 money from effigies
    effigy_count = min(28, state.count("Effigy", player))  # 12 in pool
    money_per_break = 8
    for _ in range(effigy_count):
        money += money_per_break
        money_per_break = min(512, money_per_break * 2)
    return money


class TunicState(LogicMixin):
    tunic_need_to_reset_combat_from_collect: Dict[int, bool]
    tunic_need_to_reset_combat_from_remove: Dict[int, bool]
    tunic_area_combat_state: Dict[int, Dict[str, int]]

    def init_mixin(self, _):
        # the per-player need to reset the combat state when collecting a combat item
        self.tunic_need_to_reset_combat_from_collect = defaultdict(lambda: False)
        # the per-player need to reset the combat state when removing a combat item
        self.tunic_need_to_reset_combat_from_remove = defaultdict(lambda: False)
        # the per-player, per-area state of combat checking -- unchecked, failed, or succeeded
        self.tunic_area_combat_state = defaultdict(lambda: defaultdict(lambda: CombatState.unchecked))
