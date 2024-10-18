import typing

from BaseClasses import Item, ItemClassification
from .utils import Constants
from .dice import all_dice
from .duelists import all_duelists

item_id_to_item_name: typing.Dict[int, str] = {}
# Duelist unlock items as their Duelist ID's + Duelist unlock offset
for duelist in all_duelists:
    item_id_to_item_name[Constants.DUELIST_UNLOCK_OFFSET + duelist.id] = duelist.name
# Dice items as their Dice ID + Dice offset (eventually)

item_name_to_item_id: typing.Dict[str, int] = {value: key for key, value in item_id_to_item_name.items()}


class YGODDMItem(Item):
    game: str = Constants.GAME_NAME

def create_item(name: str, player_id: int) -> YGODDMItem:
    return YGODDMItem(name, ItemClassification.progression, item_name_to_item_id[name], player_id)

def create_victory_event(player_id: int) -> YGODDMItem:
    return YGODDMItem(Constants.VICTORY_ITEM_NAME, ItemClassification.progression, Constants.VICTORY_ITEM_ID, player_id)