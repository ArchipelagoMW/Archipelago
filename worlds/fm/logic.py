import typing
from typing import NamedTuple

from .cards import all_cards, Card
from .duelists import Duelist
from .drop_pools import Drop, DuelRank
from .utils import Constants, flatten
# from .proxy import ValueProxy, OptionsProxy

# I tried this way but WebHost.py thew a NameError and refuse to load the WebWorld
# Why would it care about typing?

# if typing.TYPE_CHECKING:
#     from .options import FMOptions

# The `options` module can't be imported here, because the tracker loads this file and doesn't load any of the
# Baseclasses. The solution above didn't work, so I reluctantly settled on typing.Any


class LogicCard(NamedTuple):
    card: Card
    accessible_drops: typing.Tuple[Drop, ...]


def determine_accessible_drops(
    card: Card,
    allowed_atecs: typing.List[Duelist],
    # options: typing.Union[FMOptions, OptionsProxy]) -> typing.List[Drop]:
    options: typing.Any
) -> typing.Tuple[Drop, ...]:
    """Determines all drops that are in logic for a given card and set of options."""
    legal_atecs: typing.List[Drop] = [drop for drop in card.drop_pool if drop.duel_rank is not DuelRank.SATEC
                                      or drop.duelist in allowed_atecs]
    legal_ultra_rares: typing.List[Drop] = [drop for drop in legal_atecs
                                            if drop.probability > options.drop_rate_logic.value]
    return tuple(legal_ultra_rares)


def get_all_cards_that_have_locations(options: typing.Any) -> typing.List[Card]:
    # These cards are not obtainable by any means besides hacking
    unobtainable_ids: typing.Tuple[int, ...] = (
        7, 17, 18, 28, 51, 52, 56, 57, 60, 62, 63, 67, 235, 252, 284, 288, 299, 369, 428, 429, 499, 541, 554,
        555, 562, 603, 628, 640, 709, 711, 717, 721, 722
    )
    # Remove the cards that don't drop. FM-TODO: fusion-only and ritual-only card logic
    return [card for card in all_cards if card.id not in unobtainable_ids and card.drop_pool]


def filter_to_in_logic_cards(
    obtainable_cards: typing.List[Card],
    # options: typing.Union[FMOptions, OptionsProxy]) -> typing.List[Card]:
    options: typing.Any
) -> typing.List[LogicCard]:
    logical_atec_duelists: typing.List[Duelist] = []
    if options.atec_logic.value == Constants.ATecLogicOptionValues.all:
        logical_atec_duelists.extend([duelist for duelist in Duelist if duelist is not Duelist.HEISHIN])
    else:
        if options.atec_logic.value >= Constants.ATecLogicOptionValues.pegasus_only:
            logical_atec_duelists.append(Duelist.PEGASUS)
        if options.atec_logic.value >= Constants.ATecLogicOptionValues.hundo_atecs:
            logical_atec_duelists.extend((
                Duelist.KAIBA, Duelist.MAGE_SOLDIER, Duelist.MEADOW_MAGE, Duelist.NITEMARE
            ))
    logic_cards: typing.List[LogicCard] = []
    for card in obtainable_cards:
        in_logic: typing.Tuple[Drop, ...] = determine_accessible_drops(card, logical_atec_duelists, options)
        if in_logic:
            logic_cards.append(LogicCard(card, in_logic))
    return logic_cards


def get_unlocked_duelists(
        progressive_duelist_item_count: int,
        duelist_unlock_order: typing.Sequence[typing.Tuple[Duelist, ...]],
        final_6_order: typing.Sequence[Duelist]
) -> typing.List[Duelist]:
    duelists_available: typing.List[Duelist] = []
    # the first element is unlocked at the start
    progressive_duelist_item_count += 1
    if progressive_duelist_item_count >= len(duelist_unlock_order):
        duelists_available.extend(flatten(duelist_unlock_order))
        final_6_unlocks: int = progressive_duelist_item_count - len(duelist_unlock_order)
        if final_6_unlocks > 0:
            duelists_available.extend(final_6_order[:final_6_unlocks])
    else:
        for i in range(progressive_duelist_item_count):
            duelists_available.extend(duelist_unlock_order[i])
    return duelists_available
