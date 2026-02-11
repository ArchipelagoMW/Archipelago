from BaseClasses import CollectionState
from ..Items import GoldenBugs, TPItem
from ..RoomFunctions import RoomFunctions
from ..options import FaronWoodsLogic


def can_use(state: CollectionState, player: int, item: str):
    if isinstance(item, str):
        return state.has(item, player)
    elif isinstance(item, TPItem):
        return state.has(item.name, player)
    else:
        return False


def can_change_time(state: CollectionState, player: int):
    if state.has("Shadow Crystal", player):
        return True
    else:
        for room in RoomFunctions.time_flow_rooms:
            if state.can_reach_region(room, player):
                return True
    return False


def can_warp(state: CollectionState, player: int):
    if not state.has("Shadow Crystal", player):
        return False
    return any(
        state.can_reach_region(room, player) for room in RoomFunctions.warp_rooms
    )


def can_get_hot_spring_water(state: CollectionState, player: int):
    return (
        state.can_reach_region("Lower Kakariko Village", player)
        or (
            state.can_reach_region("Death Mountain Elevator Lower", player)
            and can_defeat_Goron(state, player)
        )
    ) and has_bottle(state, player)


def has_damaging_item(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            state.has("Progressive Hero's Bow", player)
            and can_get_arrows(state, player)
        )
        or has_bombs(state, player)
        or state.has("Iron Boots", player)
        or state.has("Shadow Crystal", player)
        or state.has("Spinner", player)
    )


def has_sword(state: CollectionState, player: int, count=1):
    return state.has("Progressive Master Sword", player, count)


def can_defeat_Aeralfos(state: CollectionState, player: int):
    return (state.has("Progressive Clawshot", player)) and (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or state.has("Shadow Crystal", player)
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
    )


def can_defeat_Armos(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Shadow Crystal", player)
        or (state.has("Progressive Clawshot", player))
        or has_bombs(state, player)
        or state.has("Spinner", player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_BabaSerpent(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_HangingBabaSerpent(state: CollectionState, player: int):
    return (
        state.has("Gale Boomerang", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
    ) and can_defeat_BabaSerpent(state, player)


def can_defeat_BabyGohma(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Slingshot", player)
        or (state.has("Progressive Clawshot", player))
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Bari(state: CollectionState, player: int):
    return can_use_water_bombs(state, player) or (
        state.has("Progressive Clawshot", player)
    )


def can_defeat_Beamos(state: CollectionState, player: int):
    return (
        state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or has_bombs(state, player)
    )


def can_defeat_BigBaba(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Shadow Crystal", player)
        or state.has("Spinner", player)
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Chu(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
        or (state.has("Progressive Clawshot", player))
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Bokoblin(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Slingshot", player)
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Bokoblin_Red(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
        or (
            can_do_difficult_combat(state, player)
            and (state.has("Iron Boots", player) or state.has("Spinner", player))
        )
    )


def can_defeat_Bombfish(state: CollectionState, player: int):
    return (
        state.has("Iron Boots", player)
        or state._tp_glitched(player)
        and state.has("Magic Armor", player)
    ) and (
        has_sword(state, player)
        or (state.has("Progressive Clawshot", player))
        or (
            state.has("Progressive Hidden Skill", player)
            and state.has("Progressive Hidden Skill", player, 2)
        )
    )


def can_defeat_Bombling(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
        or (state.has("Progressive Clawshot", player))
    )


def can_defeat_Bomskit(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
    )


def can_defeat_Bubble(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Bulblin(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Chilfos(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Shadow Crystal", player)
        or state.has("Spinner", player)
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_ChuWorm(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
        or can_use_backslice_as_sword(state, player)
    ) and (has_bombs(state, player) or (state.has("Progressive Clawshot", player)))


def can_defeat_Darknut(state: CollectionState, player: int):
    return has_sword(state, player) or (
        can_do_difficult_combat(state, player)
        and (has_bombs(state, player) or state.has("Ball and Chain", player))
    )


def can_defeat_DekuBaba(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or (
            has_shield(state, player)
            and state.has("Progressive Hidden Skill", player, 2)
        )
        or state.has("Slingshot", player)
        or (state.has("Progressive Clawshot", player))
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_DekuLike(state: CollectionState, player: int):
    return has_bombs(state, player)


def can_defeat_Dodongo(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Dinalfos(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or state.has("Shadow Crystal", player)
    )


def can_defeat_FireBubble(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_FireKeese(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Slingshot", player)
        or state.has("Shadow Crystal", player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_FireToadpoli(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (
            state.has("Hylian Shield", player)
            and state.has("Progressive Hidden Skill", player, 2)
        )
        or (
            can_do_difficult_combat(state, player)
            and state.has("Shadow Crystal", player)
        )
    )


def can_defeat_Freezard(state: CollectionState, player: int):
    return state.has("Ball and Chain", player)


def can_defeat_Goron(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Shadow Crystal", player)
        or (
            has_shield(state, player)
            and state.has("Progressive Hidden Skill", player, 2)
        )
        or state.has("Slingshot", player)
        or (can_do_difficult_combat(state, player) and state.has("Lantern", player))
        or (state.has("Progressive Clawshot", player))
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_GhoulRat(state: CollectionState, player: int):
    return state.has("Shadow Crystal", player)


def can_defeat_Guay(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or (can_do_difficult_combat(state, player) and state.has("Spinner", player))
        or state.has("Shadow Crystal", player)
        or state.has("Slingshot", player)
    )


def can_defeat_Helmasaur(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Helmasaurus(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_IceBubble(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_IceKeese(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Slingshot", player)
        or state.has("Shadow Crystal", player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Poe(state: CollectionState, player: int):
    return state.has("Shadow Crystal", player)


def can_defeat_Kargarok(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Keese(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Slingshot", player)
        or state.has("Shadow Crystal", player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Leever(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
    )


def can_defeat_Lizalfos(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_MiniFreezard(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Moldorm(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
    )


def can_defeat_PoisonMite(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or state.has("Lantern", player)
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
    )


def can_defeat_Puppet(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Rat(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Slingshot", player)
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_RedeadKnight(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_ShadowBeast(state: CollectionState, player: int):
    return has_sword(state, player) or (
        state.has("Shadow Crystal", player)  # and can_complete_MDH(state, player)
    )


def can_defeat_ShadowBulblin(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_ShadowDekuBaba(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Shadow Crystal", player)
        or (
            has_shield(state, player)
            and state.has("Progressive Hidden Skill", player, 2)
        )
        or state.has("Slingshot", player)
        or (state.has("Progressive Clawshot", player))
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_ShadowInsect(state: CollectionState, player: int):
    return state.has("Shadow Crystal", player)


def can_defeat_ShadowKargarok(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_ShadowKeese(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Slingshot", player)
        or state.has("Shadow Crystal", player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_ShadowVermin(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_ShellBlade(state: CollectionState, player: int):
    return can_use_water_bombs(state, player) or (
        has_sword(state, player)
        and (
            state.has("Iron Boots", player)
            or (state._tp_glitched(player) and state.has("Magic Armor", player))
        )
    )


def can_defeat_Skullfish(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
    )


def can_defeat_Skulltula(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Stalfos(state: CollectionState, player: int):
    return can_smash(state, player)


def can_defeat_Stalhound(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Stalchild(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Tektite(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_TileWorm(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    ) and state.has("Gale Boomerang", player)


def can_defeat_Toado(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
    )


def can_defeat_WaterToadpoli(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (
            has_shield(state, player)
            and state.has("Progressive Hidden Skill", player, 2)
        )
        or can_do_difficult_combat(state, player)
        and (state.has("Shadow Crystal", player))
    )


def can_defeat_TorchSlug(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
    )


def can_defeat_Walltula(state: CollectionState, player: int):
    return (
        state.has("Ball and Chain", player)
        or state.has("Slingshot", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or state.has("Gale Boomerang", player)
        or (state.has("Progressive Clawshot", player))
    )


def can_defeat_WhiteWolfos(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
    )


def can_defeat_YoungGohma(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Spinner", player)
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
    )


def can_defeat_ZantHead(state: CollectionState, player: int):
    return (
        state.has("Shadow Crystal", player) or has_sword(state, player)
    ) or can_use_backslice_as_sword(state, player)


def can_defeat_Ook(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_Dangoro(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Shadow Crystal", player)
        or (
            state._tp_glitched(player)
            and state.has("Ball and Chain", player)
            or (
                (state.has("Progressive Hero's Bow", player))
                and has_bombs(state, player)
            )
        )
    ) and state.has("Iron Boots", player)


def can_defeat_CarrierKargarok(state: CollectionState, player: int):
    return state.has("Shadow Crystal", player)


def can_defeat_TwilitBloat(state: CollectionState, player: int):
    return state.has("Shadow Crystal", player)


def can_defeat_DekuToad(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def can_defeat_SkullKid(state: CollectionState, player: int):
    return state.has("Progressive Hero's Bow", player)


def can_defeat_KingBulblinBridge(state: CollectionState, player: int):
    return state.has("Progressive Hero's Bow", player)


def can_defeat_KingBulblinDesert(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or state.has("Shadow Crystal", player)
        or state.has("Progressive Hero's Bow", player, 3)
        or can_use_backslice_as_sword(state, player)
        or (
            can_do_difficult_combat(state, player)
            and (
                state.has("Shadow Crystal", player)
                or state.has("Iron Boots", player)
                or has_bombs(state, player)
                or state.has("Progressive Hero's Bow", player, 2)
            )
        )
    )


def can_defeat_KingBulblinCastle(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or state.has("Shadow Crystal", player)
        or state.has("Progressive Hero's Bow", player, 3)
        or (
            can_do_difficult_combat(state, player)
            and (
                state.has("Shadow Crystal", player)
                or state.has("Iron Boots", player)
                or has_bombs(state, player)
                or can_use_backslice_as_sword(state, player)
            )
        )
    )


def can_defeat_DeathSword(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        and (
            state.has("Gale Boomerang", player)
            or (
                (state.has("Progressive Hero's Bow", player))
                and can_get_arrows(state, player)
            )
            or (state.has("Progressive Clawshot", player))
        )
        and state.has("Shadow Crystal", player)
    )


def can_defeat_Darkhammer(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Ball and Chain", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state._tp_glitched(player) and state.has("Iron Boots", player))
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
        or (
            can_do_difficult_combat(state, player)
            and can_use_backslice_as_sword(state, player)
        )
    )


def can_defeat_PhantomZant(state: CollectionState, player: int):
    return state.has("Shadow Crystal", player) or has_sword(state, player)


def can_defeat_Diababa(state: CollectionState, player: int):
    return can_launch_bombs(state, player) or (
        state.has("Gale Boomerang", player)
        and (
            has_sword(state, player)
            or state.has("Ball and Chain", player)
            or (state._tp_glitched(player) and state.has("Iron Boots", player))
            or state.has("Shadow Crystal", player)
            or has_bombs(state, player)
            or (
                can_do_difficult_combat(state, player)
                and can_use_backslice_as_sword(state, player)
            )
        )
    )


def can_defeat_Fyrus(state: CollectionState, player: int):
    return (
        state.has("Progressive Hero's Bow", player)
        and state.has("Iron Boots", player)
        and (
            has_sword(state, player)
            or (
                can_do_difficult_combat(state, player)
                and can_use_backslice_as_sword(state, player)
            )
        )
    )


def can_defeat_Morpheel(state: CollectionState, player: int):
    return (
        state.has("Zora Armor", player)
        and state.has("Iron Boots", player)
        and has_sword(state, player)
        and (state.has("Progressive Clawshot", player))
    ) or (
        state._tp_glitched(player)
        and (
            (state.has("Progressive Clawshot", player))
            and can_do_air_refill(state, player)
            and has_sword(state, player)
        )
    )


def can_defeat_Stallord(state: CollectionState, player: int):
    return (state.has("Spinner", player) and has_sword(state, player)) or (
        can_do_difficult_combat(state, player) and state.has("Shadow Crystal", player)
    )


def can_defeat_Blizzeta(state: CollectionState, player: int):
    return state.has("Ball and Chain", player)


def can_defeat_Armogohma(state: CollectionState, player: int):
    return (state.has("Progressive Hero's Bow", player)) and (
        state.has("Progressive Dominion Rod", player)
    )


def can_defeat_Argorok(state: CollectionState, player: int):
    return (
        state.has("Progressive Clawshot", player, 2)
        and has_sword(state, player, 2)
        and (
            state.has("Iron Boots", player)
            or (state._tp_glitched(player) and state.has("Magic Armor", player))
        )
    )


def can_defeat_Zant(state: CollectionState, player: int):
    return (has_sword(state, player, 3)) and (
        state.has("Gale Boomerang", player)
        and (state.has("Progressive Clawshot", player))
        and state.has("Ball and Chain", player)
        and (
            state.has("Iron Boots", player)
            or (state._tp_glitched(player) and state.has("Magic Armor", player))
        )
        and (
            state.has("Zora Armor", player)
            or (state._tp_glitched(player) and can_do_air_refill(state, player))
        )
    )


def can_defeat_Ganondorf(state: CollectionState, player: int):
    return (
        state.has("Shadow Crystal", player)
        and (has_sword(state, player, 3))
        and (state.has("Progressive Hidden Skill", player))
    )


def can_smash(state: CollectionState, player: int):
    return state.has("Ball and Chain", player) or has_bombs(state, player)


def can_burn_webs(state: CollectionState, player: int):
    return (
        state.has("Lantern", player)
        or has_bombs(state, player)
        or state.has("Ball and Chain", player)
    )


def has_ranged_item(state: CollectionState, player: int):
    return (
        state.has("Ball and Chain", player)
        or state.has("Slingshot", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state.has("Progressive Clawshot", player))
        or state.has("Gale Boomerang", player)
    )


def has_shield(state: CollectionState, player: int):
    return (
        state.has("Hylian Shield", player)
        or (
            state.can_reach_region("Kakariko Malo Mart", player)
            and not state._tp_shops_shuffled(player)
        )
        or (
            state.can_reach_region("Castle Town Goron House", player)
            and not state._tp_shops_shuffled(player)
        )
        # or state.can_reach_region("Death Mountain Hot Spring", player)
    )


def can_use_bottled_fairy(state: CollectionState, player: int):
    return has_bottle(state, player) and state.can_reach_region("Lake Hylia", player)


def can_use_bottled_fairies(state: CollectionState, player: int):
    return has_bottles(state, player) and state.can_reach_region("Lake Hylia", player)


def can_use_oil_bottle(state: CollectionState, player: int):
    return state.has("Lantern", player) and state.has(
        "Lantern Oil (Coro Bottle)", player
    )


def can_launch_bombs(state: CollectionState, player: int):
    return (
        state.has("Gale Boomerang", player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
    ) and has_bombs(state, player)


def can_cut_hanging_web(state: CollectionState, player: int):
    return (
        (state.has("Progressive Clawshot", player))
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or state.has("Gale Boomerang", player)
        or state.has("Ball and Chain", player)
    )


# def get_player_health(state: CollectionState, player: int):
#     playerHealth = 3.0  # start at 3 since we have 3 hearts.

#     playerHealth = playerHealth + (
#         state.world_state.get_item_count("Piece of Heart") * 0.2
#     )  # Pieces of heart are 1/5 of a heart.
#     playerHealth = playerHealth + state.world_state.get_item_count(
#         "Heart Container"
#     )

#     return playerHealth


def can_knock_down_hc_painting(state: CollectionState, player: int):
    return state.has("Progressive Hero's Bow", player) or (
        state._tp_glitched(player)
        and (
            (
                has_bombs(state, player)
                or (
                    has_sword(state, player)
                    and state.has("Progressive Hidden Skill", player, 6)
                )
            )
            or (
                (has_sword(state, player) and can_do_moon_boots(state, player))
                or can_do_bs_moon_boots(state, player)
            )
        )
    )


def can_break_monkey_cage(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or state.has("Iron Boots", player)
        or state.has("Spinner", player)
        or state.has("Ball and Chain", player)
        or state.has("Shadow Crystal", player)
        or has_bombs(state, player)
        or (
            (state.has("Progressive Hero's Bow", player))
            and can_get_arrows(state, player)
        )
        or (state.has("Progressive Clawshot", player))
        or (
            state._tp_glitched(player)
            and has_shield(state, player)
            and state.has("Progressive Hidden Skill", player, 2)
        )
    )


def can_press_mines_switch(state: CollectionState, player: int):
    return state.has("Iron Boots", player) or (
        state._tp_glitched(player) and state.has("Ball and Chain", player)
    )


def can_free_all_monkeys(state: CollectionState, player: int):
    return (
        can_break_monkey_cage(state, player)
        and (
            state.has("Lantern", player)
            # Holdover from Keysy
            # or (
            #     state._tp_is_small_keysy(player)
            #     and (has_bombs(state, player) or state.has("Iron Boots", player))
            # )
        )
        and can_burn_webs(state, player)
        and state.has("Gale Boomerang", player)
        and can_defeat_Bokoblin(state, player)
        and (
            (state.has("Forest Temple Small Key", player, 4))
            # Holdover from Keysy
            # or (state._tp_is_small_keysy(player))
        )
    )


def can_knock_down_HangingBaba(state: CollectionState, player: int):
    return (
        (state.has("Progressive Hero's Bow", player))
        or (state.has("Progressive Clawshot", player))
        or state.has("Gale Boomerang", player)
        or state.has("Slingshot", player)
    )


def can_break_wooden_door(state: CollectionState, player: int):
    return (
        state.has("Shadow Crystal", player)
        or has_sword(state, player)
        or can_smash(state, player)
        or can_use_backslice_as_sword(state, player)
    )


def has_bombs(state: CollectionState, player: int):
    return has_bomb_bag(state, player) and (
        state.can_reach_region("Kakariko Barnes Bomb Shop Lower", player)
        or (
            state.can_reach_region("Eldin Field Water Bomb Fish Grotto", player)
            and state.has("Progressive Fishing Rod", player)
        )
        or state.can_reach_region("City in The Sky Entrance", player)
    )


def has_bomb_bag(state: CollectionState, player: int):
    return state.has("Bomb Bag", player)


def can_use_water_bombs(state: CollectionState, player: int):
    return has_bomb_bag(state, player) and (
        state.can_reach_region("Kakariko Barnes Bomb Shop Lower", player)
        or (
            state.can_reach_region("Eldin Field Water Bomb Fish Grotto", player)
            and (state.has("Progressive Fishing Rod", player))
        )
        or (
            state.can_reach_region("Kakariko Barnes Bomb Shop Lower", player)
            and state.can_reach_region("Castle Town Malo Mart", player)
        )
    )


def can_get_arrows(state: CollectionState, player: int):
    return (
        state.can_reach_region("Lost Woods", player)
        or (
            can_complete_goron_mines(state, player)
            and state.can_reach_region("Kakariko Malo Mart", player)
        )
        # or ( # TODO: renable this logic
        #     state.can_reach_region("Castle Town Goron House Balcony", player)
        #     and not state._tp_shops_shuffled(player)
        # )
    )


# def can_complete_prologue(state: CollectionState, player: int):
#     assert False, "This is no longer used"
#     # return (
#     #     state.can_reach_region("North Faron Woods", player)
#     #     and can_defeat_Bokoblin(state, player)
#     # ) or state._tp_skip_prologue(player)


def can_complete_goats1(state: CollectionState, player: int):
    return state.can_reach_region("Ordon Ranch", player)
    # or can_complete_prologue(
    #     state, player
    # )


# def can_complete_MDH(state: CollectionState, player: int):
#     assert False, "This is no longer used"
#     # return state._tp_skip_mdh(player) or (
#     #     can_complete_lakebed_temple(state, player)
#     #     and state.can_reach_region("Castle Town South", player)
#     # )
#     # return (canCompleteLakebedTemple() or (state.world.options.skip_mdh.value == True))


# TODO: Figure this out
def can_strike_pedestal(state: CollectionState, player: int):
    return has_sword(state, player, 3)


def can_clear_forest(state: CollectionState, player: int):
    return (
        can_complete_forest_temple(state, player)
        or (state._tp_faron_woods_logic(player) == FaronWoodsLogic.option_open)
        # and can_complete_prologue(state, player)
        # and can_complete_faron_twilight(state, player)
    )


def can_complete_faron_twilight(state: CollectionState, player: int):
    assert False, "This is no longer used"
    # return ( # state._tp_faron_twilight_cleared(player) or
    #     can_complete_prologue(state, player)
    #     and state.can_reach_region("South Faron Woods", player)
    #     and state.can_reach_region("Faron Woods Coros House Lower", player)
    #     and state.can_reach_region("Mist Area Near Faron Woods Cave", player)
    #     and state.can_reach_region("North Faron Woods", player)
    #     and state.can_reach_region("Ordon Spring", player)
    #     and (
    #         not state._tp_bonks_do_damage(player)
    #         or (
    #             state._tp_bonks_do_damage(player)
    #             and (
    #                 (
    #                     state._tp_damage_magnification(player)
    #                     is not DamageMagnification.option_ohko
    #                 )
    #                 or can_use_bottled_fairies(state, player)
    #             )
    #         )
    #     )
    # )


# def can_complete_eldin_twilight(state: CollectionState, player: int):
#     assert False, "This is no longer used"
#     return state._tp_eldin_twilight_cleared(player) or (
#         state.can_reach_region("Faron Field", player)
#         and state.can_reach_region("Lower Kakariko Village", player)
#         and state.can_reach_region("Kakariko Graveyard", player)
#         and state.can_reach_region("Kakariko Malo Mart", player)
#         and state.can_reach_region("Kakariko Barnes Bomb Shop Upper", player)
#         and state.can_reach_region("Kakariko Renados Sanctuary Basement", player)
#         and state.can_reach_region("Kakariko Elde Inn", player)
#         and state.can_reach_region("Kakariko Bug House", player)
#         and state.can_reach_region("Upper Kakariko Village", player)
#         and state.can_reach_region("Kakariko Watchtower", player)
#         and state.can_reach_region("Death Mountain Volcano", player)
#         and (
#             not state._tp_bonks_do_damage(player)
#             or (
#                 state._tp_bonks_do_damage(player)
#                 and (
#                     (
#                         state._tp_damage_magnification(player)
#                         is not DamageMagnification.option_ohko
#                     )
#                     or can_use_bottled_fairies(state, player)
#                 )
#             )
#         )
#     )


# def can_complete_lanayru_twilight(state: CollectionState, player: int):
#     assert False, "This is no longer used"
#     # return state._tp_lanayru_twilight_cleared(player) or (
#     #     (
#     #         state.can_reach_region("North Eldin Field", player)
#     #         or state.has("Shadow Crystal", player)
#     #     )
#     #     and state.can_reach_region("Zoras Domain", player)
#     #     and state.can_reach_region("Zoras Domain Throne Room", player)
#     #     and state.can_reach_region("Upper Zoras River", player)
#     #     and state.can_reach_region("Lake Hylia", player)
#     #     and state.can_reach_region("Lake Hylia Lanayru Spring", player)
#     #     and state.can_reach_region("Castle Town South", player)
#     #     and (
#     #         not state._tp_bonks_do_damage(player)
#     #         or (
#     #             state._tp_bonks_do_damage(player)
#     #             and (
#     #                 (
#     #                     state._tp_damage_magnification(player)
#     #                     is not DamageMagnification.option_ohko
#     #                 )
#     #                 or can_use_bottled_fairies(state, player)
#     #             )
#     #         )
#     #     )
#     # )


# def can_complete_all_twilight(state: CollectionState, player: int):
# assert False, "This is no longer used"
# return (
#     can_complete_faron_twilight(state, player)
#     and can_complete_eldin_twilight(state, player)
#     and can_complete_lanayru_twilight(state, player)
# )


def can_complete_forest_temple(state: CollectionState, player: int):
    return state.has("Diababa Defeated", player)


def can_complete_goron_mines(state: CollectionState, player: int):
    return state.has("Fyrus Defeated", player)


def can_complete_lakebed_temple(state: CollectionState, player: int):
    return state.has("Morpheel Defeated", player)


def can_complete_arbiters_grounds(state: CollectionState, player: int):
    return state.has("Stallord Defeated", player)


def can_complete_snowpeak_ruins(state: CollectionState, player: int):
    return state.has("Blizzeta Defeated", player)


def can_complete_temple_of_time(state: CollectionState, player: int):
    return state.has("Armogohma Defeated", player)


def can_complete_city_in_the_sky(state: CollectionState, player: int):
    return state.has("Argorok Defeated", player)


def can_complete_palace_of_twilight(state: CollectionState, player: int):
    return state.has("Zant Defeated", player)


def can_complete_all_dungeons(state: CollectionState, player: int):
    return (
        can_complete_forest_temple(state, player)
        and can_complete_goron_mines(state, player)
        and can_complete_lakebed_temple(state, player)
        and can_complete_arbiters_grounds(state, player)
        and can_complete_snowpeak_ruins(state, player)
        and can_complete_temple_of_time(state, player)
        and can_complete_city_in_the_sky(state, player)
        and can_complete_palace_of_twilight(state, player)
    )


def has_bug(state: CollectionState, player: int):
    for bug in GoldenBugs:
        if state.has(bug, player):
            return True
    return False


def has_bugs(state: CollectionState, player: int, count: int):
    n = 0
    for bug in GoldenBugs:
        if state.has(bug, player):
            n += 1
    return n >= count


def can_unlock_ordona_map(state: CollectionState, player: int):
    if state._tp_open_map(player):
        return True
    for mapRoom in RoomFunctions.OrdonaMapRooms:
        if state.can_reach_region(mapRoom):
            return True
    return False


def can_unlock_faron_map(state: CollectionState, player: int):
    if state._tp_open_map(player):
        return True
    for mapRoom in RoomFunctions.FaronMapRooms:
        if state.can_reach_region(mapRoom):
            return True
    return False


def can_unlock_eldin_map(state: CollectionState, player: int):
    if state._tp_open_map(player):
        return True
    for mapRoom in RoomFunctions.EldinMapRooms:
        if state.can_reach_region(mapRoom):
            return True
    return False


def can_unlock_lanayru_map(state: CollectionState, player: int):
    if state._tp_open_map(player):
        return True
    for mapRoom in RoomFunctions.LanayruMapRooms:
        if state.can_reach_region(mapRoom):
            return True
    return False


def can_unlock_snowpeak_map(state: CollectionState, player: int):
    if state._tp_open_map(player) or state._tp_skip_snowpeak_entrance(player):
        return True
    for mapRoom in RoomFunctions.SnowpeakMapRooms:
        if state.can_reach_region(mapRoom):
            return True
    return False


def can_unlock_gerudo_map(state: CollectionState, player: int):
    if state._tp_open_map(player):
        return True
    for mapRoom in RoomFunctions.GerudoMapRooms:
        if state.can_reach_region(mapRoom):
            return True
    return False


def can_do_difficult_combat(state: CollectionState, player: int):
    # TODO: Change to use setting once it's made
    return False


def can_do_niche_stuff(state: CollectionState, player: int):
    # TODO: Change to use setting once it's made
    return state._tp_glitched(player)


def can_use_backslice_as_sword(state: CollectionState, player: int):
    return state._tp_glitched(player) and state.has(
        "Progressive Hidden Skill", player, 3
    )


def can_get_bug_with_lantern(state: CollectionState, player: int):
    # TODO: If option to not have bug models replaced becomes a thing, this function can be useful
    return False


# START OF GLITCHED LOGIC


def has_sword_or_BS(state: CollectionState, player: int):
    return has_sword(state, player) or state.has("Progressive Hidden Skill", player, 3)


def has_bottle(state: CollectionState, player: int):
    return (
        state.has("Empty Bottle (Fishing Hole)", player)
        or state.has("Milk (half) (Sera Bottle)", player)
        or state.has("Great Fairy Tears (Jovani)", player)
        or state.has("Lantern Oil (Coro Bottle)", player)
    ) and state.has(
        "Lantern", player
    )  # NOTE: Is this true?


def has_bottles(state: CollectionState, player: int):
    n = 0
    if state.has("Lantern", player):
        if state.has("Empty Bottle (Fishing Hole)", player):
            n += 1
        if state.has("Milk (half) (Sera Bottle)", player):
            n += 1
        if state.has("Great Fairy Tears (Jovani)", player):
            n += 1
        if state.has("Lantern Oil (Coro Bottle)", player):
            n += 1

    if n > 1:
        return True
    return False


def has_heavy_mod(state: CollectionState, player: int):
    return state.has("Iron Boots", player) or state.has("Magic Armor", player)


def has_cutscene_item(state: CollectionState, player: int):
    return (
        state.has("Progressive Sky Book", player)
        or has_bottle(state, player)
        or state.has("Horse Call", player)
    )


def can_do_lja(state: CollectionState, player: int):
    return has_sword(state, player) and state.has("Gale Boomerang", player)


def can_do_js_lja(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        and state.has("Gale Boomerang", player)
        and state.has("Progressive Hidden Skill", player, 6)
    )


def can_do_map_glitch(state: CollectionState, player: int):
    return state.has("Shadow Crystal", player) and state.can_reach_region(
        "Kakariko Gorge", player
    )


def can_do_storage(state: CollectionState, player: int):
    return can_do_map_glitch(state, player) and has_one_handed_item(state, player)


def has_one_handed_item(state: CollectionState, player: int):
    return (
        has_sword(state, player)
        or has_bottle(state, player)
        or state.has("Gale Boomerang", player)
        or state.has("Progressive Clawshot", player)
        or state.has("Lantern", player)
        or state.has("Progressive Hero's Bow", player)
        or state.has("Slingshot", player)
        or state.has("Progressive Dominion Rod", player)
    )


def can_do_moon_boots(state: CollectionState, player: int):
    return has_sword(state, player) and (
        state.has("Magic Armor", player)
        or (
            state.has("Iron Boots", player)
            and state.has("Progressive Hidden Skill", player, 3)
        )
    )  # Ensure you can equip something over boots


def can_do_js_moon_boots(state: CollectionState, player: int):
    return can_do_moon_boots(state, player) and state.has(
        "Progressive Hidden Skill", player, 6
    )


def can_do_bs_moon_boots(state: CollectionState, player: int):
    return state.has("Progressive Hidden Skill", player, 3) and state.has(
        "Magic Armor", player
    )


def can_do_eb_moon_boots(state: CollectionState, player: int):
    return (
        can_do_moon_boots(state, player)
        and state.has("Progressive Hidden Skill", player)
        and has_sword(state, player, 2)
    )


def can_do_hs_moon_boots(state: CollectionState, player: int):
    return (
        can_do_moon_boots(state, player)
        and state.has("Progressive Hidden Skill", player, 4)
        and has_sword(state, player)
        and has_shield(state, player)
    )


def can_do_fly_glitch(state: CollectionState, player: int):
    return state.has("Progressive Fishing Rod", player) and has_heavy_mod(state, player)


def can_do_air_refill(state: CollectionState, player: int):
    return can_use_water_bombs(state, player) and (
        state.has("Magic Armor", player)
        or (
            state.has("Iron Boots", player)
            and state.has("Progressive Hidden Skill", player, 3)
        )
    )  # Ensure you can equip something over boots


def can_do_hidden_village_glitched(state: CollectionState, player: int):
    return (
        state.has("Progressive Hero's Bow", player)
        or state.has("Ball and Chain", player)
        or (
            state.has("Slingshot", player)
            and (
                state.has("Shadow Crystal", player)
                or has_sword(state, player)
                or has_bombs(state, player)
                or state.has("Iron Boots", player)
                or state.has("Shadow Crystal", player)
            )
        )
    )


def can_do_ft_windless_bridge_room(state: CollectionState, player: int):
    return (
        has_bombs(state, player)
        or can_do_bs_moon_boots(state, player)
        or can_do_js_moon_boots(state, player)
    )


def can_clear_forest_glitched(state: CollectionState, player: int):
    return (  # can_complete_prologue(state, player) and
        state._tp_faron_woods_logic(player) == FaronWoodsLogic.option_open
    ) or (
        can_complete_forest_temple(state, player)
        or can_do_lja(state, player)
        or can_do_map_glitch(state, player)
    )


def can_complete_eldin_twilight_glitched(state: CollectionState, player: int):
    return state._tp_eldin_twilight_cleared(player) or can_clear_forest_glitched(
        state, player
    )


def can_skip_key_to_deku_toad(state: CollectionState, player: int):
    return (
        # Holdover from Keysy
        # state._tp_is_small_keysy(player)
        state.has("Progressive Hidden Skill", player, 3)
        or can_do_bs_moon_boots(state, player)
        or can_do_js_moon_boots(state, player)
        or can_do_lja(state, player)
        or (
            has_bombs(state, player)
            and (
                has_heavy_mod(state, player)
                or state.has("Progressive Hidden Skill", player, 6)
            )
        )
    )
