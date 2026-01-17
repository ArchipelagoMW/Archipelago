from collections import Counter

from BaseClasses import CollectionState
from .Options import FF6WCOptions


def has_dragons(prog_items_player: Counter[str], number: int) -> bool:
    from . import FF6WCWorld
    found: int = 0
    for dragon_event_name in FF6WCWorld.all_dragon_clears:
        found += prog_items_player[dragon_event_name]
        if found >= number:
            return True
    return False


def can_beat_final_kefka(options: FF6WCOptions, player: int, cs: CollectionState) -> bool:
    # Even if the character objective is less than 3, 3 characters are required to enter the final dungeon.
    # TODO: maybe this should be has_group_unique
    # I don't know what happens if you get more than 1 of a character/esper
    return (cs.has_group("characters", player, max(3, options.CharacterCount.value))
            and cs.has_group("espers", player, options.EsperCount.value)
            and has_dragons(cs.prog_items[player], options.DragonCount.value)
            and cs.has("Busted!", player, options.BossCount.value))
