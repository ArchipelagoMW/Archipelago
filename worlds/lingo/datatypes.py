from typing import List, NamedTuple, Optional


class RoomAndDoor(NamedTuple):
    room: Optional[str]
    door: str


class RoomAndPanel(NamedTuple):
    room: Optional[str]
    panel: str


class RoomEntrance(NamedTuple):
    room: str  # source room
    door: Optional[RoomAndDoor]
    painting: bool


class Room(NamedTuple):
    name: str
    entrances: List[RoomEntrance]


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
    junk_item: bool
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
