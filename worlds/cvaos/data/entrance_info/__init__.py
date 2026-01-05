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
    door_number: int
    door_identifier: str
    room_identifier: str
    dest_room_identifier: str
    door_address: Annotated[int, BeforeValidator(parse_hex)]
    room_index: int
    room_address: Annotated[int, BeforeValidator(parse_hex)]
    door_index_within_room: int
    dest_room_address: Annotated[int, BeforeValidator(parse_hex)]
    x_pos_door: int
    y_pos_door: int
    dest_x_door: int
    dest_y_door: int
    dest_x_offset_door: int
    dest_y_offset_door: int

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
