from __future__ import annotations

from dataclasses import dataclass
import json
import pkgutil
from typing import TYPE_CHECKING

from Utils import snes_to_pc

if TYPE_CHECKING:
    from . import ALTTPWorld
    from .Rom import LocalRom


POT_ITEM_POINTER_TABLE = 0xDB67
POT_KEY = 0x08
POT_ARROW = 0x09
POT_BLUE_RUPEE = 0x07
POT_SWITCH = 0x88
POT_HOLE = 0x80


@dataclass(frozen=True)
class PotData:
    x: int
    y: int
    reserved: int


@dataclass(frozen=True)
class PotRoomData:
    room_id: int
    pots: tuple[PotData, ...]
    items: tuple[int, ...]


@dataclass(frozen=True)
class FilledPot:
    x: int
    y: int
    item: int


def generate_pot_shuffle(world: "ALTTPWorld") -> dict[int, tuple[FilledPot, ...]]:
    room_data = _load_pot_room_data()
    shuffled_pots: dict[int, tuple[FilledPot, ...]] = {}

    for room in room_data:
        room_items = list(room.items)
        if world.options.retro_bow:
            room_items = [POT_BLUE_RUPEE if item == POT_ARROW else item for item in room_items]

        empty_pots: list[PotData] = []
        filled_pots: list[FilledPot] = []
        reserved_keys = 0
        reserved_switches = 0

        for pot in room.pots:
            if pot.reserved == 3:
                filled_pots.append(FilledPot(pot.x, pot.y, POT_HOLE))
            else:
                empty_pots.append(pot)
            if pot.reserved == 1:
                reserved_keys += 1
            elif pot.reserved == 2:
                reserved_switches += 1

        while reserved_keys > 0:
            candidate_indices = [index for index, pot in enumerate(empty_pots) if pot.reserved == 1]
            if not candidate_indices:
                break
            pot_index = world.random.choice(candidate_indices)
            pot = empty_pots.pop(pot_index)
            if POT_KEY in room_items:
                room_items.remove(POT_KEY)
                reserved_keys -= 1
            else:
                reserved_keys = 0
            filled_pots.append(FilledPot(pot.x, pot.y, POT_KEY))

        while reserved_switches > 0:
            candidate_indices = [index for index, pot in enumerate(empty_pots) if pot.reserved == 2]
            if not candidate_indices:
                break
            pot_index = world.random.choice(candidate_indices)
            pot = empty_pots.pop(pot_index)
            if POT_SWITCH in room_items:
                room_items.remove(POT_SWITCH)
                reserved_switches -= 1
            else:
                reserved_switches = 0
            filled_pots.append(FilledPot(pot.x, pot.y, POT_SWITCH))

        while room_items and empty_pots:
            pot_index = world.random.randrange(len(empty_pots))
            item_index = world.random.randrange(len(room_items))
            pot = empty_pots.pop(pot_index)
            item = room_items.pop(item_index)
            filled_pots.append(FilledPot(pot.x, pot.y, item))

        shuffled_pots[room.room_id] = tuple(filled_pots)

    return shuffled_pots


def apply_pot_shuffle(rom: "LocalRom", shuffled_pots: dict[int, tuple[FilledPot, ...]]) -> None:
    for room_id, pots in shuffled_pots.items():
        pointer_address = POT_ITEM_POINTER_TABLE + (room_id * 2)
        snes_address = rom.read_byte(pointer_address) | (rom.read_byte(pointer_address + 1) << 8) | (0x01 << 16)
        address = snes_to_pc(snes_address)
        for index, pot in enumerate(pots):
            rom.write_bytes(address + (index * 3), (pot.x, pot.y, pot.item))


def _load_pot_room_data() -> tuple[PotRoomData, ...]:
    raw_data = pkgutil.get_data(__package__, "data/enemizer/pot_shuffle.json")
    if raw_data is None:
        raise FileNotFoundError("Missing vendored Enemizer pot shuffle data required by ALTTP native integration")

    payload = json.loads(raw_data.decode("utf-8"))
    return tuple(
        PotRoomData(
            room_id=room["room_id"],
            pots=tuple(PotData(**pot) for pot in room["pots"]),
            items=tuple(room["items"]),
        )
        for room in payload["rooms"]
    )
