from typing import Callable, Dict, NamedTuple, Optional

from BaseClasses import Location, MultiWorld


class CliqueLocation(Location):
    game = "Clique"


class CliqueLocationData(NamedTuple):
    region: str
    address: Optional[int] = None
    can_create: Callable[[MultiWorld, int], bool] = lambda multiworld, player: True
    locked_item: Optional[str] = None


location_data_table: Dict[str, CliqueLocationData] = {
    "The Big Red Button": CliqueLocationData(
        region="The Button Realm",
        address=69696969,
    ),
    "The Item on the Desk": CliqueLocationData(
        region="The Button Realm",
        address=69696968,
        can_create=lambda multiworld, player: bool(getattr(multiworld, "hard_mode")[player]),
    ),
    "In the Player's Mind": CliqueLocationData(
        region="The Button Realm",
        locked_item="The Urge to Push",
    ),
}

location_table = {name: data.address for name, data in location_data_table.items() if data.address is not None}
locked_locations = {name: data for name, data in location_data_table.items() if data.locked_item}
