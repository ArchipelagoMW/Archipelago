import typing

from BaseClasses import Location, Region, LocationProgressType, Item
from .dice import Dice, all_dice
from .utils import Constants
from .duelists import Duelist, get_duelist_defeat_location_name, ids_to_duelists

def get_location_name_for_dice(dice: Dice) -> str:
    return f"{dice.name}"

def get_location_id_for_dice_id(dice_id: int) -> int:
    return Constants.DICE_COLLECTION_OFFSET + dice_id

def get_location_id_for_dice(dice: Dice) -> int:
    return get_location_id_for_dice_id(dice.id)

def get_location_name_for_duelist(duelist: Duelist) -> str:
    return get_duelist_defeat_location_name(duelist)

def get_location_id_for_duelist(duelist: Duelist) -> int:
    return Constants.DUELIST_UNLOCK_OFFSET + duelist.id

def duelist_from_location_id(location_id: int) -> Duelist:
    print ("duelist from location id")
    print (ids_to_duelists[location_id - Constants.DUELIST_UNLOCK_OFFSET])
    return ids_to_duelists[location_id - Constants.DUELIST_UNLOCK_OFFSET]

class YGODDMLocation(Location):
    game: str

    def __init__(self, region: Region, player: int, name: str, id: int):
        super().__init__(player, name, parent=region)
        self.game = Constants.GAME_NAME
        self.address = id

    def exclude(self) -> None:
        self.progress_type = LocationProgressType.EXCLUDED

    def place(self, item: Item) -> None:
        self.item = item
        item.location = self

class DuelistLocation(YGODDMLocation):
    # Check for a duelist being defeated for the first time
    duelist: Duelist

    def __init__(self, region: Region, player: int, duelist: Duelist):
        super().__init__(region, player, get_location_name_for_duelist(duelist), get_location_id_for_duelist(duelist))
        self.duelist = duelist

dice_location_name_to_id: typing.Dict[str, int] = {}
for dice in all_dice:
    dice_location_name_to_id[get_location_name_for_dice(dice)] = get_location_id_for_dice(dice)

duelist_location_name_to_id: typing.Dict[str, int] = {}
for duelist in Duelist:
    duelist_location_name_to_id[get_location_name_for_duelist(duelist)] = get_location_id_for_duelist(duelist)

# Not until we have dice locations as checks
#location_name_to_id: typing.Dict[str, int] = {**dice_location_name_to_id, **duelist_location_name_to_id}
location_name_to_id: typing.Dict[str, int] = {**duelist_location_name_to_id}