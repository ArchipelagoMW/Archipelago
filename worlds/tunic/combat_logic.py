from typing import Dict, List, NamedTuple, Tuple
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
    # marked as boss because the garden knights can't get hurt by stick
    "Gauntlet": AreaStats(1, 1, 1, 1, 1, 1, 6, ["Sword", "Shield", "Magic"], is_boss=True),
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
            def_to_buy = 0
            sp_to_buy = 0

            if paid_stats <= 0:
                # if you don't have to pay for any stats, you don't need money for these upgrades
                pass
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
    att_offering_count = state.count("ATT Offering", player)
    att_upgrades = state.count("Hero Relic - ATT", player)
    sword_level = state.count("Sword Upgrade", player)
    if sword_level >= 3:
        att_upgrades += min(2, sword_level - 2)
    # attack falls off, can just cap it at 8 for simplicity
    return min(8, 1 + att_offering_count + att_upgrades), att_offering_count


# returns a tuple of your max defense level, the number of defense offerings
def get_def_level(state: CollectionState, player: int) -> Tuple[int, int]:
    def_offering_count = state.count("DEF Offering", player)
    # defense falls off, can just cap it at 8 for simplicity
    return (min(8, 1 + def_offering_count
                + state.count_from_list({"Hero Relic - DEF", "Secret Legend", "Phonomath"}, player)),
            def_offering_count)


# returns a tuple of your max potion level, the number of potion offerings
def get_potion_level(state: CollectionState, player: int) -> Tuple[int, int]:
    potion_offering_count = min(2, state.count("Potion Offering", player))
    # your third potion upgrade (from offerings) costs 1,000 money, reasonable to assume you won't do that
    return (1 + potion_offering_count
            + state.count_from_list({"Hero Relic - POTION", "Just Some Pals", "Spring Falls", "Back To Work"}, player),
            potion_offering_count)


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
