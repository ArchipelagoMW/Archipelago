from enum import Enum, Flag, auto
from typing import List, NamedTuple, Optional


class RoomAndDoor(NamedTuple):
    room: Optional[str]
    door: str


class RoomAndPanel(NamedTuple):
    room: Optional[str]
    panel: str


class RoomAndPanelDoor(NamedTuple):
    room: Optional[str]
    panel_door: str


class EntranceType(Flag):
    NORMAL = auto()
    PAINTING = auto()
    SUNWARP = auto()
    WARP = auto()
    CROSSROADS_ROOF_ACCESS = auto()


class RoomEntrance(NamedTuple):
    room: str  # source room
    door: Optional[RoomAndDoor]
    type: EntranceType


class Room(NamedTuple):
    name: str
    entrances: List[RoomEntrance]


class DoorType(Enum):
    NORMAL = 1
    SUNWARP = 2
    SUN_PAINTING = 3


class Door(NamedTuple):
    name: str
    item_name: str
    location_name: Optional[str]
    panels: Optional[List[RoomAndPanel]]
    skip_location: bool
    skip_item: bool
    has_doors: bool
    painting_ids: List[str]
    event: bool
    door_group: Optional[str]
    include_reduce: bool
    type: DoorType
    item_group: Optional[str]


class Panel(NamedTuple):
    required_rooms: List[str]
    required_doors: List[RoomAndDoor]
    required_panels: List[RoomAndPanel]
    colors: List[str]
    check: bool
    event: bool
    exclude_reduce: bool
    achievement: bool
    non_counting: bool
    panel_door: Optional[RoomAndPanelDoor]  # This will always be fully specified.
    location_name: Optional[str]


class PanelDoor(NamedTuple):
    item_name: str
    panel_group: Optional[str]


class Painting(NamedTuple):
    id: str
    room: str
    enter_only: bool
    exit_only: bool
    required: bool
    required_when_no_doors: bool
    required_door: Optional[RoomAndDoor]
    disable: bool
    req_blocked: bool
    req_blocked_when_no_doors: bool


class Progression(NamedTuple):
    item_name: str
    index: int
