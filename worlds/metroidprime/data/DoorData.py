from dataclasses import dataclass, field
from typing import Callable, List, Optional, Tuple, TYPE_CHECKING
from .Tricks import TrickInfo
from BaseClasses import CollectionState
from .AreaNames import MetroidPrimeArea
from .RoomNames import RoomName
from ..DoorRando import DoorLockType

if TYPE_CHECKING:
    from .. import MetroidPrimeWorld
    from ..BlastShieldRando import BlastShieldType


@dataclass
class DoorData:
    default_destination: Optional[RoomName]
    defaultLock: DoorLockType = DoorLockType.Blue
    blast_shield: Optional["BlastShieldType"] = None
    lock: Optional[DoorLockType] = None
    destination_area: Optional[MetroidPrimeArea] = (
        None  # Used for rooms that have the same name in different areas like Transport Tunnel A
    )
    rule_func: Optional[Callable[["MetroidPrimeWorld", CollectionState], bool]] = None
    tricks: List[TrickInfo] = field(default_factory=list)
    exclude_from_rando: bool = (
        False  # Used primarily for door rando when a door doesn't actually exist
    )
    sub_region_door_index: Optional[int] = (
        None  # Used when this door also provides access to another door in the target room
    )
    sub_region_access_override: Optional[
        Callable[["MetroidPrimeWorld", CollectionState], bool]
    ] = None  # Used to override the access check for reaching this door, if necessary when connecting it to a sub region
    indirect_condition_rooms: Optional[List[RoomName]] = None

    def get_destination_region_name(self) -> str:
        assert self.default_destination is not None
        if self.destination_area is not None:
            return f"{self.destination_area.value}: {self.default_destination.value}"
        return self.default_destination.value


def get_door_data_by_room_names(
    source_room: RoomName,
    target_room: RoomName,
    area: MetroidPrimeArea,
    world: "MetroidPrimeWorld",
) -> Optional[Tuple[DoorData, int]]:
    region_data = world.game_region_data.get(area)

    assert region_data

    source_room_data = region_data.rooms.get(source_room)
    if not source_room_data:
        return None

    # Retrieve the target room data
    target_room_data = region_data.rooms.get(target_room)
    if not target_room_data:
        return None

    # Iterate through the doors in the source room to find a matching door
    for door_id, door_data in source_room_data.doors.items():
        if door_data.default_destination == target_room:
            return door_data, door_id

    return None
