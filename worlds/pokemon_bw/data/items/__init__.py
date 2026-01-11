from typing import TYPE_CHECKING
from collections import ChainMap

from . import main_items, key_items, medicine, tm_hm, berries, badges, seasons

if TYPE_CHECKING:
    from .. import ItemData, AnyItemData

all_berries: ChainMap[str, "ItemData"] = ChainMap(
    berries.standard,
    berries.niche,
)

all_key_items: ChainMap[str, "ItemData"] = ChainMap(
    key_items.progression,
    key_items.vanilla,
    key_items.useless,
    key_items.special
)

all_main_items: ChainMap[str, "ItemData"] = ChainMap(
    main_items.min_once,
    main_items.fossils,
    main_items.filler,
    main_items.mail,
    main_items.unused,
)

all_medicine: ChainMap[str, "ItemData"] = ChainMap(
    medicine.important,
    medicine.table,
)

all_tm_hm: ChainMap[str, "ItemData"] = ChainMap(
    tm_hm.tm,
    tm_hm.hm,
)

all_items_dict_view: ChainMap[str, "AnyItemData"] = ChainMap[str, "AnyItemData"](
    badges.table,
    berries.standard,
    berries.niche,
    key_items.progression,
    key_items.vanilla,
    key_items.useless,
    key_items.special,
    main_items.min_once,
    main_items.fossils,
    main_items.filler,
    main_items.mail,
    main_items.unused,
    medicine.important,
    medicine.table,
    seasons.table,
    tm_hm.tm,
    tm_hm.hm,
)
