from typing import Callable, Dict, NamedTuple, Optional, TYPE_CHECKING

from BaseClasses import Location

if TYPE_CHECKING:
    from . import CliqueWorld


class CliqueLocation(Location):
    game = "Clique"


class CliqueLocationData(NamedTuple):
    region: str
    address: Optional[int] = None
    can_create: Callable[["CliqueWorld"], bool] = lambda world: True
    locked_item: Optional[str] = None


location_data_table: Dict[str, CliqueLocationData] = {
    "The Big Red Button": CliqueLocationData(
        region="The Button Realm",
        address=69696969,
    ),
    "The Item on the Desk": CliqueLocationData(
        region="The Button Realm",
        address=69696968,
        can_create=lambda world: world.options.hard_mode,
    ),
    "In the Player's Mind": CliqueLocationData(
        region="The Button Realm",
        locked_item="The Urge to Push",
    ),
}

location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None}
locked_locations = {name: data for name, data in location_data_table.items() if data.locked_item}
