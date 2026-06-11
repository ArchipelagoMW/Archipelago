from __future__ import annotations

from ..._pydantic_compat import BaseModel, parse_obj_as, validator
from .._csv_resources import open_csv
from ..parse_int import parse_hex

__all__ = [
    "RoomInfo",
    "room_info_collection",
]

class RoomInfo(BaseModel):
    class Config:
        extra = "allow"
        frozen = True

    room_number: int
    room_identifier: str
    room_address: int
    room_index: int

    _parse_hex_addresses = validator("room_address", pre=True, allow_reuse=True)(parse_hex)

    def _as_tuple(self) -> tuple[int, str, int, int]:
        return (self.room_number, self.room_identifier, self.room_address, self.room_index)

    def __iter__(self):
        return iter(self._as_tuple())

    def __getitem__(self, index: int):
        return self._as_tuple()[index]

    @property
    def key(self) -> str:
        return self.room_identifier

    @property
    def address_hex(self) -> str:
        return hex(self.room_address)

    @classmethod
    def lookup(cls, key: int | str) -> "RoomInfo":
        return lookup(key)


def _load_identifiers() -> dict[str, dict]:
    reader = open_csv(__name__, "room_identifiers.csv")
    ident_rows = [row for row in reader if any((v or "").strip() for v in row.values())]
    by_identifier = {row["room_identifier"]: row for row in ident_rows}
    by_address = {parse_hex(row["room_address"]): row for row in ident_rows}
    by_number = {int(row["room_number"]): row for row in ident_rows}
    return {
        "by_identifier": by_identifier,
        "by_address": by_address,
        "by_number": by_number,
    }


def _load_room_info(ident_index: dict[str, dict]) -> list[RoomInfo]:
    reader = open_csv(__name__, "room_info.csv")
    # Normalize the first field name (blank in the CSV) to room_index
    if reader.fieldnames and reader.fieldnames[0] == "":
        reader.fieldnames[0] = "room_index"

    merged_rows: list[dict] = []
    for raw in reader:
        if not any((v or "").strip() for v in raw.values()):
            continue

        # pull identifiers using room_address (primary) then index
        room_address = parse_hex(raw.get("room_address"))
        ident = ident_index["by_address"].get(room_address)
        if ident is None and "room_index" in raw:
            try:
                idx = int(raw["room_index"])
            except Exception:
                idx = None
            if idx is not None:
                ident = ident_index["by_number"].get(idx + 1)  # room_number appears 1-based

        if ident is None:
            raise ValueError(f"room_info row at address {raw.get('room_address')} has no matching identifier")

        merged = {
            **raw,
            "room_index": int(raw.get("room_index") or 0),
            "room_address": room_address,
            "room_number": int(ident["room_number"]),
            "room_identifier": ident["room_identifier"],
        }
        merged_rows.append(merged)

    return parse_obj_as(list[RoomInfo], merged_rows)


_ident_index = _load_identifiers()
rows: tuple[RoomInfo, ...] = tuple(_load_room_info(_ident_index))
by_identifier: dict[str, RoomInfo] = {row.room_identifier: row for row in rows}
by_address: dict[int, RoomInfo] = {row.room_address: row for row in rows}
by_number: dict[int, RoomInfo] = {row.room_number: row for row in rows}
room_info_collection = list(rows)


def lookup(key: int | str) -> RoomInfo:
    if isinstance(key, int):
        return by_number.get(key) or by_address[key]
    if isinstance(key, str) and key.startswith("0x"):
        return by_address[int(key, 16)]
    if key.isdigit():
        num = int(key)
        return by_number.get(num) or by_address[num]
    return by_identifier[key]
