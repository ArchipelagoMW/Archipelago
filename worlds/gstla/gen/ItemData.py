from enum import Enum
from typing import TYPE_CHECKING, TypedDict, List, Dict, TypeVar

from typing_extensions import Unpack, NotRequired

from BaseClasses import ItemClassification
from worlds.gstla.GameData import ElementType, ItemType
from .ItemNames import ItemName
from .InternalItemData import InternalItemData, InternalDjinnItemData, InternalEventItemData
import worlds.gstla.gen.InternalItemData as ItemLists

if TYPE_CHECKING:
    # TODO: Swap name
    base_item = InternalItemData
    base_djinn = InternalDjinnItemData
    base_event = InternalEventItemData
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

class ItemData(base_item):

    def __init__(self, item: InternalItemData, **kwargs: Unpack[ItemDataDict]):
        self._item = item
        self._kwargs = kwargs

    def __getattr__(self, name):
        if name in self._kwargs:
            return self._kwargs[name] # type: ignore
        return getattr(self._item, name)

class DjinnItemData(ItemData, base_djinn):

    def __init__(self, item: InternalDjinnItemData, **kwargs: Unpack[DjinnDataDict]):
        super().__init__(item, **kwargs)

class EventItemData(ItemData, base_event):
    def __init__(self, item: InternalItemData, **kwargs: Unpack[EventDataDict]):
        super().__init__(item, **kwargs)

_overrides: dict[str, ItemDataDict] = {
    ItemName.Catch_Beads: {"progression": ItemClassification.filler},
    # TODO: Can't use deprioritized, yet
    # ItemName.Shamans_Rod: {"progression": ItemClassification.progression_deprioritized},
    # ItemName.Sea_Gods_Tear: {"progression": ItemClassification.progression_deprioritized},
    # ItemName.Right_Prong: {"progression": ItemClassification.progression_deprioritized},
    # ItemName.Left_Prong: {"progression": ItemClassification.progression_deprioritized},
    # ItemName.Center_Prong: {"progression": ItemClassification.progression_deprioritized},
    # ItemName.Healing_Fungus: {"progression": ItemClassification.progression_deprioritized},
    # ItemName.Red_Cloth: {"progression": ItemClassification.progression_deprioritized},
    # ItemName.Milk: {"progression": ItemClassification.progression_deprioritized},
    # ItemName.Aquarius_Stone: {"progression": ItemClassification.progression_deprioritized},
    # ItemName.Ruin_Key: {"progression": ItemClassification.progression_deprioritized},
}


def _wrap_datum(item: InternalItemData) -> ItemData:
    if item.name in _overrides:
        return ItemData(item, **_overrides[item.name])
    else:
        return ItemData(item)

def _wrap_djinn(djinn: InternalDjinnItemData) -> DjinnItemData:
    if djinn.name in _overrides:
        return DjinnItemData(djinn, **_overrides[djinn.name])
    else:
        return DjinnItemData(djinn)

def _wrap_event(event: InternalEventItemData) -> EventItemData:
    if event.name in _overrides:
        return EventItemData(event, **_overrides[event.name])
    else:
        return EventItemData(event)


def _convert_data(data: List[InternalItemData]) -> List[ItemData]:
    return [_wrap_datum(x) for x in data]

def _convert_djinn(data: List[InternalDjinnItemData]) -> List[DjinnItemData]:
    return [_wrap_djinn(x) for x in data]

def _convert_events(data: List[InternalEventItemData]) -> List[EventItemData]:
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

other_useful: List[ItemData] = useful_remainder + useful_consumables + forge_materials + class_change_items

shop_only: List[ItemData] = _convert_data(ItemLists.shop_only)
forge_only: List[ItemData] = _convert_data(ItemLists.forge_only)
lucky_only: List[ItemData] = _convert_data(ItemLists.lucky_only)

non_vanilla: List[ItemData] = _convert_data(ItemLists.non_vanilla)

vanilla_coins: List[ItemData] = _convert_data(ItemLists.vanilla_coins)
misc: List[ItemData] = _convert_data(ItemLists.misc)
remainder: List[ItemData] = _convert_data(ItemLists.remainder)

all_items: List[ItemData] = djinn_items + psyenergy_as_item_list + psyenergy_list + summon_list + events + characters + \
                            mimics + other_progression + other_useful + shop_only + forge_only + lucky_only + non_vanilla + vanilla_coins + \
                            misc + rusty_items + stat_boosters + remainder
assert len(all_items) == len({x.id for x in all_items})
item_table: Dict[str, ItemData] = {item.name: item for item in all_items}
items_by_id: Dict[int, ItemData] = {item.id: item for item in all_items}
