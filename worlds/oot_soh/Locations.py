from typing import Callable, Dict, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Location

if TYPE_CHECKING:
    from . import SohWorld


class SohLocation(Location):
    game = "Ship of Harkinian"

soh_base_id = int = 0xFF0000

class SohLocationData(NamedTuple):
    region: str
    address: Optional[int] = None
    can_create: Callable[["SohWorld"], bool] = lambda world: True
    locked_item: Optional[str] = None


location_data_table: Dict[str, SohLocationData] = {
    "KF Mido Top Left Chest": SohLocationData(
        region="Hyrule",
        address=soh_base_id + 0,
        # can_create=lambda world: world.options.death_link,
        # locked_item="Green Rupee",
    ),
    "KF Mido Top Right Chest": SohLocationData(
        region="Hyrule",
        address=soh_base_id + 1,
    ),
    "KF Mido Bottom Left Chest": SohLocationData(
        region="Hyrule",
        address=soh_base_id + 2,
    ),
    "KF Mido Bottom Right Chest": SohLocationData(
        region="Hyrule",
        address=soh_base_id + 3,
    ),
}

location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None}
locked_locations = {name: data for name, data in location_data_table.items() if data.locked_item}
