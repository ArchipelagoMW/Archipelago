from . import dexsanity, regions, region_connections
from .encounters import regions as encounter_regions, slots, static, region_connections as encounter_region_connections
from .ingame_items import overworld_items, hidden_items, other, special
from typing import TYPE_CHECKING
from collections import ChainMap

if TYPE_CHECKING:
    from .. import AnyLocationData, TMLocationData

all_tm_locations: ChainMap[str, "TMLocationData"] = ChainMap[str, "TMLocationData"](
    special.gym_tms,
    special.tm_hm_ncps,
)

all_item_locations: ChainMap[str, "AnyLocationData"] = ChainMap[str, "AnyLocationData"](
    overworld_items.table,
    overworld_items.abyssal_ruins,
    hidden_items.table,
    other.table,
    special.gym_badges,
    special.gym_tms,
    special.tm_hm_ncps,
)
