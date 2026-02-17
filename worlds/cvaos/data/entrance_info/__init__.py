from __future__ import annotations

import csv
from pathlib import Path
from typing import Annotated

from ..parse_int import parse_hex

from pydantic import BaseModel, BeforeValidator, TypeAdapter

__all__ = [
    "EntranceInfo",
    "entrance_info_collection",
]

class EntranceInfo(BaseModel):
    """
    Information about a door/entrance in Castlevania: Aria of Sorrow.

    Each entrance represents a transition point between rooms in the game.
    """

    door_number: int
    """Sequential door number in the game data.

    Example: 1, 2, 3, etc.
    """

    door_identifier: str
    """Unique identifier combining source and destination room identifiers.

    Format: "{room_identifier}:{dest_room_identifier}"
    Example: "000:003" (door from room 000 to room 003)
    """

    room_identifier: str
    """Identifier of the source room containing this door.

    Example: "000", "001", "002"
    """

    dest_room_identifier: str
    """Identifier of the destination room this door leads to.

    Example: "003", "002", "005"
    """

    door_address: Annotated[int, BeforeValidator(parse_hex)]
    """Memory address of the door data structure in the game ROM.

    Example: 0x0850EF8C, 0x0850F00C
    """

    room_index: int
    """Index of the source room in the game's room list.

    Example: 0, 1, 2, 3
    """

    room_address: Annotated[int, BeforeValidator(parse_hex)]
    """Memory address of the source room data structure in the game ROM.

    Example: 0x0850EF9C, 0x0850F01C
    """

    door_index_within_room: int
    """Index of this door within its source room's list of doors.

    A room can have multiple doors, each with a sequential index starting at 0.
    Example: 0 (first door in room), 1 (second door), 2 (third door)
    """

    dest_room_address: Annotated[int, BeforeValidator(parse_hex)]
    """Memory address of the destination room data structure in the game ROM.

    Example: 0x0850F15C, 0x0850F0B4
    """

    x_pos_door: int
    """X-coordinate of the door in the source room (in tiles or pixels).

    Example: 2, 1, 255
    """

    y_pos_door: int
    """Y-coordinate of the door in the source room (in tiles or pixels).

    Example: 2, 0, 4, 255
    """

    dest_x_door: int
    """X-coordinate where the player spawns in the destination room (in tiles or pixels).

    Example: 0, 256, 272
    """

    dest_y_door: int
    """Y-coordinate where the player spawns in the destination room (in tiles or pixels).

    Example: 0, 512, 768
    """

    dest_x_offset_door: int
    """X-coordinate offset applied to the spawn position in the destination room.
    """

    dest_y_offset_door: int
    """Y-coordinate offset applied to the spawn position in the destination room.
    """

    @property
    def key(self) -> str:
        return self.door_identifier

    @property
    def door_hex(self) -> str:
        return hex(self.door_address)

    @classmethod
    def lookup(cls, key: int | str) -> "EntranceInfo":
        return lookup(key)


def _load() -> tuple[EntranceInfo, ...]:
    csv_path = Path(__file__).with_name("entrance_info.csv")
    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        cleaned = [
            row
            for row in reader
            if any((v or "").strip() for v in row.values())
        ]
    return tuple(TypeAdapter(list[EntranceInfo]).validate_python(cleaned))


rows: tuple[EntranceInfo, ...] = _load()
by_door_number: dict[int, EntranceInfo] = {row.door_number: row for row in rows}
by_door_identifier: dict[str, EntranceInfo] = {row.door_identifier: row for row in rows}
by_door_address: dict[int, EntranceInfo] = {row.door_address: row for row in rows}
entrance_info_collection = list(rows)


def lookup(key: int | str) -> EntranceInfo:
    if isinstance(key, int):
        return by_door_number.get(key) or by_door_address[key]
    if isinstance(key, str) and key.startswith("0x"):
        return by_door_address[int(key, 16)]
    return by_door_identifier[key]
