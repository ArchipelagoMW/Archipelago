import typing
from random import Random  # for typing only; instance obtained from multiworld

from BaseClasses import Item, ItemClassification
from .utils import Constants
from .cards import all_cards

starchip_values: typing.Tuple[int, int, int] = (1, 5, 25)
starchip_distribution_weights: typing.Tuple[float, float, float] = (0.88, 0.10, 0.02)
starchip_values_to_strings: typing.Dict[int, str] = {
    value: f"Starchip{'' if value == 1 else f's x{value}'}"
    for value in starchip_values
}

# ids are Progressive Duelist's id, then each index in starchip_values
item_id_to_item_name: typing.Dict[int, str] = {}
item_id_to_item_name[Constants.PROGRESSIVE_DUELIST_ITEM_ID] = Constants.PROGRESSIVE_DUELIST_ITEM_NAME
starchip_item_ids_to_starchip_values: typing.Dict[int, int] = {}
for i in range(len(starchip_values)):
    id: int = Constants.STARCHIP_ITEM_ID_OFFSET + i
    item_id_to_item_name[id] = starchip_values_to_strings[starchip_values[i]]
    starchip_item_ids_to_starchip_values[id] = starchip_values[i]
item_id_to_item_name[Constants.VICTORY_ITEM_ID] = Constants.VICTORY_ITEM_NAME
# add cards as items, reusing the location ids as item ids
for card in all_cards:
    item_id_to_item_name[Constants.CARD_ID_OFFSET + card.id] = card.name

item_name_to_item_id: typing.Dict[str, int] = {value: key for key, value in item_id_to_item_name.items()}


class FMItem(Item):
    game: str = Constants.GAME_NAME


def create_item(name: str, player_id: int) -> FMItem:
    return FMItem(name, ItemClassification.progression if name == Constants.PROGRESSIVE_DUELIST_ITEM_NAME
                  else ItemClassification.filler, item_name_to_item_id[name], player_id)


def create_victory_event(player_id: int) -> FMItem:
    return FMItem(Constants.VICTORY_ITEM_NAME, ItemClassification.progression, Constants.VICTORY_ITEM_ID, player_id)


def create_starchip_items(player_id: int, count: int, rand: Random) -> typing.List[FMItem]:
    dist: typing.List[int] = rand.choices(starchip_values, weights=starchip_distribution_weights, k=count)
    return [create_item(starchip_values_to_strings[e], player_id) for e in dist]


def is_card_item(item_id: int) -> bool:
    return item_id >= Constants.CARD_ID_OFFSET and item_id <= Constants.CARD_ID_OFFSET + 722


def convert_item_id_to_card_id(item_id: int) -> int:
    return item_id - Constants.CARD_ID_OFFSET
