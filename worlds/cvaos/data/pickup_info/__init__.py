from __future__ import annotations

import csv
from pathlib import Path
from typing import Annotated

from ..parse_int import parse_hex

from pydantic import BaseModel, BeforeValidator, TypeAdapter

__all__ = [
    "PickupInfo",
    "pickup_info_collection",
]

class PickupInfo(BaseModel):
    pickup_number: int
    ptr_address: Annotated[int, BeforeValidator(parse_hex)]
    simple_name: str
    specifier: str | None = None
    flag_offset: int
    item_offset: int
    type_num: int
    type_name: str
    subtype_num: int
    room_identifier: str
    room_address: Annotated[int, BeforeValidator(parse_hex)]
    pickup_number_within_room: int
    x: int
    y: int

    def _as_tuple(
        self,
    ) -> tuple[
        int,
        int,
        str,
        str | None,
        int,
        int,
        int,
        str,
        int,
        str,
        int,
        int,
        int,
        int,
    ]:
        return (
            self.pickup_number,
            self.ptr_address,
            self.simple_name,
            self.specifier,
            self.flag_offset,
            self.item_offset,
            self.type_num,
            self.type_name,
            self.subtype_num,
            self.room_identifier,
            self.room_address,
            self.pickup_number_within_room,
            self.x,
            self.y,
        )

    def __iter__(self):
        return iter(self._as_tuple())

    def __getitem__(self, index: int):
        return self._as_tuple()[index]

    @property
    def key(self) -> int:
        return self.ptr_address

    @property
    def ptr_hex(self) -> str:
        return hex(self.ptr_address)

    @property
    def room_hex(self) -> str:
        return hex(self.room_address)

    @property
    def identifier_key(self) -> str:
        return f"{self.simple_name}{self.specifier or ''}"

    @property
    def display_name(self) -> str:
        """
        Human-readable AP item/location name. Money (subtype 1) renders its gold value
        (``500 Gold``) instead of the bare number; a duplicate-suffix like ``_a`` becomes `` (A)``.
        ``identifier_key`` stays the internal key; this is display-only (codes/ids are unaffected).\
        """
        spec = (self.specifier or "").lstrip("_")
        if not spec:
            suffix = ""
        elif len(spec) == 1 and spec.isalpha():
            suffix = f" ({spec.upper()})"
        else:
            suffix = f" ({spec})"
        if self.subtype_num == 1:  # money: simple_name is the gold value
            return f"{int(self.simple_name)} Gold{suffix}"
        return f"{self.simple_name}{suffix}"

    @classmethod
    def find(cls, key: int | str) -> "PickupInfo":
        return find(key)


def _load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = []
        for row in reader:
            # Skip completely empty lines
            if not any((v or "").strip() for v in row.values()):
                continue
            rows.append(row)
        return rows


def _merge_rows() -> list[PickupInfo]:
    ident_rows = _load_csv(Path(__file__).with_name("pickup_identifiers.csv"))
    room_rows = _load_csv(Path(__file__).with_name("pickup_rooms.csv"))

    by_pickup_number_ident = {int(r["pickup_number"]): r for r in ident_rows}
    by_pickup_number_room = {int(r["pickup_number"]): r for r in room_rows}

    merged: list[dict] = []
    for pickup_number, ident in sorted(by_pickup_number_ident.items()):
        room = by_pickup_number_room.get(pickup_number)
        if room is None:
            raise ValueError(f"pickup_rooms.csv missing entry for pickup_number {pickup_number}")

        ptr_ident = parse_hex(ident["ptr_address"])
        ptr_room = parse_hex(room.get("ptr_address"))
        ptr_address = ptr_ident if ptr_room is None else ptr_room

        if ptr_address is None:
            raise ValueError(f"pickup_number {pickup_number} missing ptr_address in both CSVs")
        if ptr_room is not None and ptr_ident is not None and ptr_room != ptr_ident:
            raise ValueError(
                f"ptr_address mismatch for pickup_number {pickup_number}: "
                f"{ptr_ident} (identifiers) vs {ptr_room} (rooms)"
            )

        merged.append(
            {
                "pickup_number": pickup_number,
                "ptr_address": ptr_address,
                "simple_name": ident["simple_name"],
                "specifier": ident.get("specifier") or None,
                "flag_offset": int(ident["flag_offset (varA)"]),
                "item_offset": int(ident["item_offset (varB)"]),
                "type_num": int(ident["type_num"]),
                "type_name": ident["type_name"],
                "subtype_num": int(ident["subtype_num"]),
                "room_identifier": room["room_identifier"],
                "room_address": room["room_address"],
                "pickup_number_within_room": int(room["pickup_number_within_room"]),
                "x": int(room["x"]),
                "y": int(room["y"]),
            }
        )

    return TypeAdapter(list[PickupInfo]).validate_python(merged)


rows: tuple[PickupInfo, ...] = tuple(_merge_rows())
by_ptr_address: dict[int, PickupInfo] = {row.ptr_address: row for row in rows}
by_pickup_number: dict[int, PickupInfo] = {row.pickup_number: row for row in rows}
by_identifier_key: dict[str, PickupInfo] = {row.identifier_key: row for row in rows}
by_simple_name: dict[str, list[PickupInfo]] = {}
for row in rows:
    by_simple_name.setdefault(row.simple_name, []).append(row)

pickup_info_collection = list(rows)

def find(key: int | str) -> PickupInfo:
    if isinstance(key, int):
        return by_ptr_address.get(key) or by_pickup_number[key]
    if isinstance(key, str) and key.startswith("0x"):
        return by_ptr_address[int(key, 16)]
    if key.isdigit():
        num = int(key)
        return by_ptr_address.get(num) or by_pickup_number[num]
    if key in by_identifier_key:
        return by_identifier_key[key]
    # Fallback: if only one entry shares the simple_name, return it
    matches = by_simple_name.get(key)
    if matches and len(matches) == 1:
        return matches[0]
    raise KeyError(f"No pickup matches key '{key}'")
