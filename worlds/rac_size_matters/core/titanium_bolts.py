from __future__ import annotations

from dataclasses import dataclass

from ..constants import Rac5Planets, Rac5TBolts
from ..interface_orchestrator.memory.accessor import MemoryAccessor
from ..interface_orchestrator.state.base_state import BaseState
from ..interface_orchestrator.storage.local import LocalStorage
from ..interface_orchestrator.structs.address_map import AddressMap
from .structs.pickups import TitaniumBoltStruct

__all__ = [
    "TitaniumBolt",
    "TitaniumBoltAddresses",
    "TITANIUM_BOLTS",
    "BOLT_BY_PLANET_AND_DELTA",
    "TitaniumBoltState",
]


# Address resolver

class TitaniumBoltAddresses:
    """Resolves titanium bolt field addresses from a single base address.

    Layout (identical on PSP and PS2):
      +0x00  pickup  — increments each time a bolt is picked up
      +0x05  total   — cumulative bolt count
    """

    def __init__(self, base: int) -> None:
        self.base   = base
        self.pickup = base + 0x00
        self.total  = base + 0x05


# Data

@dataclass(frozen=True)
class TitaniumBolt:
    # Usually a single planet ID; some locations (e.g. Outpost Omega Dream,
    # reachable from both the first and second Outpost Omega visit) can be
    # picked up while registered under more than one planet ID for the same
    # physical location — pass a tuple in that case.
    planet_id: int | tuple[int, ...]
    bit:       int  # bit position in the pickup int64
    region:    str  # AP region name

    @property
    def delta(self) -> int:
        return 1 << self.bit

    @property
    def planet_ids(self) -> tuple[int, ...]:
        return self.planet_id if isinstance(self.planet_id, tuple) else (self.planet_id,)


TITANIUM_BOLTS: dict[str, TitaniumBolt] = {
    Rac5TBolts.POKITARU_ZIPLINE:   TitaniumBolt(0x01,  0, Rac5Planets.POKITARU),
    Rac5TBolts.POKITARU_HUT:       TitaniumBolt(0x01,  1, Rac5Planets.POKITARU),
    Rac5TBolts.RYLLUS_CLIFF:       TitaniumBolt(0x02,  4, Rac5Planets.RYLLUS),
    Rac5TBolts.RYLLUS_WALL:        TitaniumBolt(0x02,  5, Rac5Planets.RYLLUS),
    Rac5TBolts.KALIDON_SHIP:       TitaniumBolt(0x03,  8, Rac5Planets.KALIDON),
    Rac5TBolts.KALIDON_FACTORY:    TitaniumBolt(0x03, 10, Rac5Planets.KALIDON),
    Rac5TBolts.KALIDON_RAMP:       TitaniumBolt(0x03,  9, Rac5Planets.KALIDON),
    Rac5TBolts.METALIS_DOOR:       TitaniumBolt(0x04, 12, Rac5Planets.METALIS),
    Rac5TBolts.DREAMTIME_HAT:      TitaniumBolt(0x05, 16, Rac5Planets.DREAMTIME),
    Rac5TBolts.DREAMTIME_GARAGE:   TitaniumBolt(0x05, 17, Rac5Planets.DREAMTIME),
    Rac5TBolts.DREAMTIME_CRAB:     TitaniumBolt(0x05, 18, Rac5Planets.DREAMTIME),
    Rac5TBolts.OUTPOST_OMEGA_DREAM:TitaniumBolt((0x06, 0x17), 20, Rac5Planets.OUTPOST_OMEGA),
    Rac5TBolts.CHALLAX_MECH_PAD:   TitaniumBolt(0x07, 24, Rac5Planets.CHALLAX),
    Rac5TBolts.CHALLAX_ROOM:       TitaniumBolt(0x07, 25, Rac5Planets.CHALLAX),
    Rac5TBolts.CHALLAX_PLANT:      TitaniumBolt(0x07, 26, Rac5Planets.CHALLAX),
    Rac5TBolts.DAYNI_MOON_BARN:    TitaniumBolt(0x08, 28, Rac5Planets.DAYNI_MOON),
    Rac5TBolts.DAYNI_MOON_MIMIC:   TitaniumBolt(0x08, 29, Rac5Planets.DAYNI_MOON),
    Rac5TBolts.INSIDE_CLANK_LADDER:TitaniumBolt(0x09, 32, Rac5Planets.INSIDE_CLANK),
    Rac5TBolts.INSIDE_CLANK_WALL:  TitaniumBolt(0x09, 33, Rac5Planets.INSIDE_CLANK),
    Rac5TBolts.QUODRONA_DUMMIES:   TitaniumBolt(0x0A, 36, Rac5Planets.QUODRONA),
}

# (planet_id, delta) → location name — used by the client for unambiguous detection
BOLT_BY_PLANET_AND_DELTA: dict[tuple[int, int], str] = {
    (planet_id, bolt.delta): name
    for name, bolt in TITANIUM_BOLTS.items()
    for planet_id in bolt.planet_ids
}


# State (runtime)

class TitaniumBoltState(BaseState):

    def __init__(
        self,
        accessor: MemoryAccessor,
        addresses: AddressMap,
        storage: LocalStorage,
    ) -> None:
        super().__init__(accessor, addresses, storage)
        self._poll_last:   int = 0
        self._synced_mask: int = 0

    def _register_handlers(self) -> None:
        self.accessor.on_struct_change(TitaniumBoltStruct, self._on_struct_change)

    def _unregister_handlers(self) -> None:
        self.accessor.remove_struct_handler(TitaniumBoltStruct, self._on_struct_change)

    def _on_struct_change(self, address: int, new_bytes: bytes) -> None:
        del address
        current = int.from_bytes(new_bytes[:5], "little")
        delta   = current - self._poll_last
        self._poll_last = current
        if delta > 0 and (delta & (delta - 1)) == 0:
            self.on_bolt_delta(delta)

    def sync(self) -> None:
        raw     = self.accessor.read_raw(TitaniumBoltStruct.BASE_ADDRESS, 5)
        current = int.from_bytes(raw, "little") if raw else 0
        self._poll_last = current
        new_val = current | self._synced_mask
        if new_val != current:
            self.accessor.write_raw(TitaniumBoltStruct.BASE_ADDRESS, new_val.to_bytes(5, "little"))

    def sync_from_ap(self, checked_location_names: set[str]) -> None:
        mask = 0
        for loc_name, bolt in TITANIUM_BOLTS.items():
            if loc_name in checked_location_names:
                mask |= bolt.delta
        self._synced_mask = mask

    def on_bolt_delta(self, _delta: int) -> None:
        del _delta

    def __repr__(self) -> str:
        collected = bin(self._poll_last).count("1")
        return f"TitaniumBoltState(collected={collected}/{len(TITANIUM_BOLTS)})"
