from enum import Enum
from typing import TYPE_CHECKING, TypedDict, List, Dict, TypeVar

from typing_extensions import Unpack, NotRequired

from BaseClasses import ItemClassification
from worlds.gstla.GameData import ElementType, ItemType
from .InternalItemData import ItemData, DjinnItemData, EventItemData
import worlds.gstla.gen.InternalItemData as ItemLists

if TYPE_CHECKING:
    base_item = ItemData
    base_djinn = DjinnItemData
    base_event = EventItemData
else:
    base_item = object
    base_djinn = object
    base_event = object

class TrapType(str, Enum):
    Mimic = "Mimic"

class FillerType(str, Enum):
    ForgeMaterials = "Forge Materials"
    RustyMaterials = "Rusty Materials"
    StatBoosts = "Stat Boosts"
    UsefulConsumables = "Useful Consumables"
    ForgedEquipment = "Forged Equipment"
    LuckyEquipment = "Lucky Equipment"
    ShopEquipment = "Shop Equipment"
    Coins = "Coins"
    CommonConsumables = "Common Consumables"

class ItemDataDict(TypedDict):
    id: NotRequired[int]
    name: NotRequired[str]
    progression: NotRequired[ItemClassification]
    addr: NotRequired[int]
    type: NotRequired[ItemType]
    is_mimic: NotRequired[bool]
    is_rare: NotRequired[bool]

class DjinnDataDict(ItemDataDict):
    element: NotRequired[ElementType]
    vanilla_id: NotRequired[int]
    stats_addr: NotRequired[int]
    stats: NotRequired[List[int]]

class EventDataDict(ItemDataDict):
    flag: NotRequired[int]
    location: NotRequired[str]

class TestItemData(base_item):

    def __init__(self, item: ItemData, **kwargs: Unpack[ItemDataDict]):
        self._item = item
        self._kwargs = kwargs

    def __getattribute__(self, name):
        if name in self._kwargs:
            return self._kwargs[name] # type: ignore
        return getattr(self.item, name)

class TestDjinnItemData(TestItemData, base_djinn):

    def __init__(self, item: DjinnItemData, **kwargs: Unpack[DjinnDataDict]):
        super().__init__(item, **kwargs)

class EventItemData(TestItemData, base_event):
    def __init__(self, item: ItemData, **kwargs: Unpack[EventDataDict]):
        super().__init__(item, **kwargs)

_overrides: Dict[str, ItemDataDict] = {
}

def _wrap_datum(item: ItemData) -> ItemData:
    if item.name in _overrides:
        return TestItemData(item, **_overrides[item.name])
    else:
        return item

def _wrap_djinn(djinn: DjinnItemData) -> DjinnItemData:
    if djinn.name in _overrides:
        return TestDjinnItemData(djinn, **_overrides[djinn.name])
    else:
        return djinn

def _wrap_event(event: EventItemData) -> EventItemData:
    if event.name in _overrides:
        return EventItemData(event, **_overrides[event.name])
    else:
        return event


def _convert_data(data: List[ItemData]) -> List[ItemData]:
    return [_wrap_datum(x) for x in data]

def _convert_djinn(data: List[DjinnItemData]) -> List[DjinnItemData]:
    return [_wrap_djinn(x) for x in data]

def _convert_events(data: List[EventItemData]) -> List[EventItemData]:
    return [_wrap_event(x) for x in data]


summon_list: List[ItemData] = _convert_data(ItemLists.summon_list)

psyenergy_list: List[ItemData] = _convert_data(ItemLists.psyenergy_list)
psyenergy_as_item_list: List[ItemData] = _convert_data(ItemLists.psyenergy_as_item_list)

djinn_items: List[DjinnItemData] = _convert_djinn(ItemLists.djinn_items)
events: List[EventItemData] = _convert_events(ItemLists.events)

characters: List[ItemData] = _convert_data(ItemLists.characters)

mimics: List[ItemData] = _convert_data(ItemLists.mimics)

other_progression: List[ItemData] = _convert_data(ItemLists.other_progression)

useful_consumables: List[ItemData] = _convert_data(ItemLists.useful_consumables)
forge_materials: List[ItemData] = _convert_data(ItemLists.forge_materials)
class_change_items: List[ItemData] = _convert_data(ItemLists.class_change_items)
rusty_items: List[ItemData] = _convert_data(ItemLists.rusty_items)
stat_boosters: List[ItemData] = _convert_data(ItemLists.stat_boosters)
useful_remainder = _convert_data(ItemLists.useful_remainder)

other_useful: List[ItemData] = useful_remainder  + useful_consumables  + forge_materials  + class_change_items

shop_only: List[ItemData] = _convert_data(ItemLists.shop_only)
forge_only: List[ItemData] = _convert_data(ItemLists.forge_only)
lucky_only: List[ItemData] = _convert_data(ItemLists.lucky_only)

non_vanilla: List[ItemData] = _convert_data(ItemLists.non_vanilla)

vanilla_coins: List[ItemData] = _convert_data(ItemLists.vanilla_coins)
misc: List[ItemData] = _convert_data(ItemLists.misc)
remainder: List[ItemData] = _convert_data(ItemLists.remainder)

all_items: List[ItemData] = djinn_items + psyenergy_as_item_list + psyenergy_list + summon_list + events + characters + \
                            mimics + other_progression + other_useful + shop_only + forge_only + lucky_only + non_vanilla + vanilla_coins + \
                            misc  + rusty_items  + stat_boosters  + remainder
assert len(all_items) == len({x.id for x in all_items})
item_table: Dict[str, ItemData] = {item.name: item for item in all_items}
items_by_id: Dict[int, ItemData] = {item.id: item for item in all_items}
