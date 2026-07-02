from __future__ import annotations

import contextlib
import logging
import threading
from collections.abc import Callable
from dataclasses import dataclass
from enum import IntEnum
from typing import TYPE_CHECKING

from ..constants import Rac5Items
from ..interface_orchestrator.memory.accessor import MemoryAccessor
from ..interface_orchestrator.state.base_state import BaseState
from ..interface_orchestrator.storage.local import LocalStorage
from ..interface_orchestrator.structs.address_map import AddressMap
from .address_maps import (
    MENU_ADDR_BY_PLANET_ID,
    PLANET_STATE_OFFSET,
    PLANET_UNLOCK_ADDRESSES,
)
from .armour import ArmourPiece
from .structs.game import PlanetLoadStruct, PlanetProgressStruct

if TYPE_CHECKING:
    from .armour import ArmourState
    from .display_text import DisplayTextBoxState, TextBoxConfig, TextBoxConfigState
    from .menu import MenuState
    from .player import PlayerState
    from .vendor import ModVendorState, VendorUnlockState, WeaponVendorState
    from .weapons import WeaponState


# Planet data

@dataclass(frozen=True)
class Planet:
    name:      str
    planet_id: int
    menu_addr: int | None = None


class Planets:
    POKITARU        = Planet("Pokitaru",              0x01, menu_addr=MENU_ADDR_BY_PLANET_ID[0x01])
    RYLLUS          = Planet("Ryllus",                0x02, menu_addr=MENU_ADDR_BY_PLANET_ID[0x02])
    KALIDON         = Planet("Kalidon",               0x03, menu_addr=MENU_ADDR_BY_PLANET_ID[0x03])
    METALIS         = Planet("Metalis",               0x04, menu_addr=MENU_ADDR_BY_PLANET_ID[0x04])
    DREAMTIME       = Planet("Dreamtime",             0x05, menu_addr=MENU_ADDR_BY_PLANET_ID[0x05])
    # OUTPOST_OMEGA_1 = Planet("Outpost Omega 1",       0x06)
    CHALLAX         = Planet("Challax",               0x07, menu_addr=MENU_ADDR_BY_PLANET_ID[0x07])
    DAYNI_MOON      = Planet("Dayni Moon",            0x08, menu_addr=MENU_ADDR_BY_PLANET_ID[0x08])
    INSIDE_CLANK    = Planet("Inside Clank",          0x09)
    QUODRONA        = Planet("Quodrona",              0x0A, menu_addr=MENU_ADDR_BY_PLANET_ID[0x0A])
    # GIANT_CLANK_META = Planet("Giant Clank (Metalis)", 0x0F)
    # GIANT_CLANK_CHAL = Planet("Giant Clank (Challax)", 0x15)
    # KALIDON_RACE    = Planet("Kalidon Race Track",    0x16)
    OUTPOST_OMEGA_2 = Planet("Outpost Omega 2",       0x17, menu_addr=MENU_ADDR_BY_PLANET_ID[0x17])


BY_ID: dict[int, Planet] = {
    p.planet_id: p
    for p in vars(Planets).values()
    if isinstance(p, Planet)
}

# Planet unlock data

@dataclass(frozen=True)
class PlanetUnlock:
    """
    Data record for a planet's unlock information.
    This is used for monitoring and modifying planet unlock states in the game.
    """

    unlock_addr:   int
    state_addr:    int
    default_state: int = 0  # minimum value always written to state_addr


_DEFAULT_STATES: dict[str, int] = {
    "DREAMTIME":     3,
    "OUTPOST_OMEGA": 3,
}

PLANET_UNLOCKS: dict[str, PlanetUnlock] = {
    name: PlanetUnlock(
        unlock_addr=addr,
        state_addr=addr + PLANET_STATE_OFFSET,
        default_state=_DEFAULT_STATES.get(name, 0),
    )
    for name, addr in PLANET_UNLOCK_ADDRESSES.items()
}


# Infobots / planet state
# Infobots are AP items given to the player.  When received they set the
# corresponding planet's unlock-status address to INFOBOT_UNLOCK_VALUE (3),
# which allows Ratchet to travel to (or enter) that planet.
#
# Planets that are auto-unlocked from the start (no infobot item):
#   Dreamtime    -- unlocked through Outpost Omega automatically
#   Inside Clank -- entrance only accessible from Dayni Moon; requires Shrink Ray

INFOBOT_UNLOCK_VALUE = 3  # value written to the planet status address

# Display name -> planet key used in PLANET_STATE_ADDRESSES
INFOBOT_ITEM_TO_PLANET: dict[str, str] = {
    Rac5Items.POKITARU:     "pokitaru",
    Rac5Items.RYLLUS:       "ryllus",
    Rac5Items.KALIDON:      "kalidon",
    Rac5Items.METALIS:      "metalis",
    Rac5Items.OUTPOST_OMEGA: "outpost_omega",
    Rac5Items.CHALLAX:      "challax",
    Rac5Items.DAYNI_MOON:   "dayni_moon",
    Rac5Items.QUODRONA:     "quodrona",
}

PLANET_STATE_ADDRESSES: dict[str, int] = {
    "pokitaru":          PLANET_UNLOCK_ADDRESSES["POKITARU"],
    "ryllus":            PLANET_UNLOCK_ADDRESSES["RYLLUS"],
    "kalidon":           PLANET_UNLOCK_ADDRESSES["KALIDON"],
    "metalis":           PLANET_UNLOCK_ADDRESSES["METALIS"],
    "outpost_omega":     PLANET_UNLOCK_ADDRESSES["OUTPOST_OMEGA"],
    "outpost_omega_oo2": 0x21F4C677,  # secondary state set alongside Outpost Omega
    "challax":           PLANET_UNLOCK_ADDRESSES["CHALLAX"],
    "dayni_moon":        PLANET_UNLOCK_ADDRESSES["DAYNI_MOON"],
    "inside_clank":      PLANET_UNLOCK_ADDRESSES["INSIDE_CLANK"],  # unlocked via Dayni Moon infobot
    "quodrona":          PLANET_UNLOCK_ADDRESSES["QUODRONA"],
}

# Planet unlock addresses always forced to INFOBOT_UNLOCK_VALUE because
# these planets have no collectible infobot in the AP item pool.
AUTO_UNLOCK_ADDRESSES: list[int] = [
    0x21F4C661,  # Pokitaru  -- mandatory starting planet, always accessible
    0x21F4C665,  # Dreamtime -- auto-unlocked via Outpost Omega
]


# Planet state (runtime)

logger = logging.getLogger("CommonClient")

_PIECE_ORDER = [ArmourPiece.CHESTPLATE, ArmourPiece.HELMET, ArmourPiece.GLOVES, ArmourPiece.BOOTS]



class PlanetState(BaseState):
    def __init__(
        self,
        accessor: MemoryAccessor,
        addresses: AddressMap,
        storage: LocalStorage,
        name: str,
        planet_id: int,
        menu_addr: int | None = None,
        log: Callable[..., None] | None = None,
    ) -> None:
        super().__init__(accessor, addresses, storage)
        self.name      = name
        self.planet_id = planet_id
        self.menu_addr = menu_addr
        self._log      = log or logger.info

        self._armour:             ArmourState | None           = None
        self._weapons:            WeaponState | None           = None
        self._player:             PlayerState | None           = None
        self._menu:               MenuState | None             = None
        self._weapon_vendor:      WeaponVendorState | None     = None
        self._mod_vendor:         ModVendorState | None        = None
        self._vendor_unlock:      VendorUnlockState | None     = None
        self._display_text:       DisplayTextBoxState | None   = None
        self._displayed_text_box: TextBoxConfigState | None = None
        self._display_text_cfg:   TextBoxConfig | None     = None

        self._reapply_inv:        Callable[[], None]     | None = None
        self._get_checked_locs:   Callable[[], set[str]] | None = None
        self._on_enter_callbacks: list[Callable[[], None]] = []
        self._on_exit_callbacks:  list[Callable[[], None]] = []
        self._vendor_write_lock:  threading.Lock | None = None

        # on_menu_open() temporarily redirects WeaponState's acquisition hooks
        # to vendor-purchase tracking; these hold whatever was wired there
        # before (e.g. the bonus-weapon-pickup chain from _wire_bonus_weapon_hooks)
        # so on_menu_close() can restore it instead of nulling it out forever.
        self._prev_on_weapon_acquired: Callable[[str], None]         | None = None
        self._prev_on_gadget_acquired: Callable[[str], None]         | None = None
        self._prev_on_mod_acquired:    Callable[[str, str], None]    | None = None

    def set_vendor_write_lock(self, lock: threading.Lock) -> None:
        self._vendor_write_lock = lock

    def set_player_state(self, player: PlayerState) -> None:
        self._player = player

    def set_weapon_state(self, weapons: WeaponState) -> None:
        self._weapons = weapons

    def set_armour(self, armour: ArmourState) -> None:
        self._armour = armour

    def set_menu_state(
        self,
        menu: MenuState,
        weapon_vendor: WeaponVendorState,
        mod_vendor: ModVendorState,
    ) -> None:
        self._menu          = menu
        self._weapon_vendor  = weapon_vendor
        self._mod_vendor     = mod_vendor

    def set_vendor_unlock(self, vendor_unlock: VendorUnlockState) -> None:
        self._vendor_unlock = vendor_unlock

    def set_display_text_box(
        self,
        display_text: DisplayTextBoxState,
        config: TextBoxConfig,
    ) -> None:
        self._display_text     = display_text
        self._display_text_cfg = config

    def set_displayed_text_box(self, displayed_text_box: TextBoxConfigState) -> None:
        self._displayed_text_box = displayed_text_box

    def set_inventory_callbacks(
        self,
        reapply_inv: Callable[[], None],
        get_checked_locations: Callable[[], set[str]],
    ) -> None:
        self._reapply_inv      = reapply_inv
        self._get_checked_locs = get_checked_locations

    def add_enter_callback(self, fn: Callable[[], None]) -> None:
        self._on_enter_callbacks.append(fn)

    def add_exit_callback(self, fn: Callable[[], None]) -> None:
        self._on_exit_callbacks.append(fn)

    # planet_enter()/planet_exit() are no longer self-triggered from
    # GameStatusStruct — they're called externally by the transition-gate
    # handler in orchestration/_planet_lifecycle.py, which still reads
    # CURRENT_PLANET_ADDRESS to determine which planet was entered.

    def planet_enter(self) -> None:
        self._log(f"[RAC] [{self.name}] planet_enter")
        for cb in self._on_enter_callbacks:
            cb()
        if self._player is not None:
            self._player.set_planet(self.planet_id)
        if self._menu is not None and self._weapon_vendor is not None and self._mod_vendor is not None:
            self._menu.bind(self._weapon_vendor, self._mod_vendor, self)
        if self._display_text is not None and self._display_text_cfg is not None:
            self._display_text.activate(self._display_text_cfg)
        if self._displayed_text_box is not None and self._display_text_cfg is not None:
            self._displayed_text_box.activate(self._display_text_cfg)
        if self._get_checked_locs is not None and self._weapons is not None:
            self._weapons.sync_from_ap(self._get_checked_locs())
        if self._reapply_inv is not None:
            self._reapply_inv()

    def planet_exit(self) -> None:
        self._log(f"[RAC] [{self.name}] planet_exit")
        for cb in self._on_exit_callbacks:
            cb()
        if self._menu is not None:
            self._menu.on_exit()
        if self._display_text is not None:
            self._display_text.deactivate()
        if self._displayed_text_box is not None:
            self._displayed_text_box.deactivate()

    def _pine_proxy(self):
        accessor = self.accessor

        class _Proxy:
            def read_int8(self, addr: int) -> int:
                raw = accessor.read_raw(addr, 1)
                return raw[0] if raw else 0
            def write_int8(self, addr: int, val: int) -> None:
                accessor.write_raw(addr, bytes([val & 0xFF]))
            def read_int16(self, addr: int) -> int:
                raw = accessor.read_raw(addr, 2)
                return int.from_bytes(raw, "little", signed=True) if len(raw) >= 2 else 0
            def write_int16(self, addr: int, val: int) -> None:
                accessor.write_raw(addr, val.to_bytes(2, "little", signed=True))
            def read_int32(self, addr: int) -> int:
                raw = accessor.read_raw(addr, 4)
                return int.from_bytes(raw, "little", signed=True) if len(raw) >= 4 else 0
            def write_int32(self, addr: int, val: int) -> None:
                accessor.write_raw(addr, val.to_bytes(4, "little", signed=False))
            def read_int64(self, addr: int) -> int:
                raw = accessor.read_raw(addr, 8)
                return int.from_bytes(raw, "little") if len(raw) >= 8 else 0
            def write_int64(self, addr: int, val: int) -> None:
                accessor.write_raw(addr, val.to_bytes(8, "little"))
            def read_bytes(self, addr: int, size: int) -> bytes:
                return accessor.read_raw(addr, size)
            def write_bytes(self, addr: int, data: bytes) -> None:
                accessor.write_raw(addr, data)

        return _Proxy()

    def on_pickup_start(self) -> None:
        self._log(f"[RAC] [{self.name}] Pickup start — zeroing armour for clean pickup read")
        if self._armour is not None:
            self._armour.sync_slots()
            self._armour.clear_all_memory()

    def on_pickup_end(self) -> None:
        self._log(f"[RAC] [{self.name}] Pickup end — reading armour state")
        if self._armour is None:
            return
        self._armour.sync_bitmasks()
        bitmask_summary = {k: hex(v) for k, v in self._armour.sets_bitmask.items() if v}
        self._log(f"[RAC] [{self.name}] Pickup end sets_bitmask: {bitmask_summary}")
        for name, mask in self._armour.sets_bitmask.items():
            new_bits = mask & ~self._armour.world_collected_armour.get(name, 0)
            for piece in _PIECE_ORDER:
                if new_bits & int(piece):
                    self.on_armour_acquired(name, piece)

    def on_armour_acquired(self, _name: str, _piece: ArmourPiece) -> None:
        del _name, _piece

    def _wire_vendor_purchase_callbacks(self, allowed: frozenset[str] | None = None) -> None:
        if self._weapons is None:
            return
        if allowed is None:
            allowed = (
                self._vendor_unlock.allowed_weapons_for_inventory()
                if self._vendor_unlock is not None else frozenset()
            )
        with self._vendor_write_lock or contextlib.nullcontext():
            self._weapons.apply_vendor_locations(allowed)
        self._prev_on_weapon_acquired = self._weapons.on_weapon_acquired
        self._prev_on_gadget_acquired = self._weapons.on_gadget_acquired
        self._prev_on_mod_acquired    = self._weapons.on_mod_acquired
        self._weapons.on_weapon_acquired = lambda name: self.on_vendor_weapon_purchased(name)
        self._weapons.on_gadget_acquired = lambda name: self.on_vendor_gadget_purchased(name)
        self._weapons.on_mod_acquired    = lambda weapon, slot: self.on_vendor_mod_purchased(weapon, slot)
        self._log(
            f"[RAC] [{self.name}] Vendor purchase callbacks wired "
            f"(on_weapon_acquired/on_gadget_acquired/on_mod_acquired)."
        )

    def on_weapon_vendor_open(self) -> None:
        active            = self._weapon_vendor.active if self._weapon_vendor is not None else None
        showing_inventory = bool(self._weapon_vendor is not None and self._weapon_vendor.showing_inventory)
        self._log(
            f"[RAC] [{self.name}] Weapon vendor open "
            f"(weapon_vendor.active={active}, showing_inventory={showing_inventory})."
        )
        if showing_inventory:
            # The D_PAD_RIGHT inventory-view refresh (menu.set_menu) can make
            # the game re-run its own open sequence, which re-fires this same
            # transition. Re-assert the inventory view instead of falling
            # back to _wire_vendor_purchase_callbacks()'s default-view
            # zero/restore and re-wiring purchase tracking back on — that
            # would undo what the D_PAD toggle deliberately set up.
            if self._vendor_unlock is not None:
                self._vendor_unlock.apply_inventory(self.accessor)
            if self._weapons is not None:
                with self._vendor_write_lock or contextlib.nullcontext():
                    self._weapons.sync()
            return
        self._wire_vendor_purchase_callbacks()
        # Weapon vendor only: writes the vendor list/size array
        # (WEAPON_VENDOR_ITEMS/WEAPON_VENDOR_SLOTS). The mod vendor has no
        # equivalent array — mod purchasability lives on the weapon structs
        # themselves (mod_unlock_N), kept correct by the existing inventory
        # sync, not by anything here.
        if self._vendor_unlock is not None:
            self._vendor_unlock.apply(self.accessor)
            for line in self._vendor_unlock.debug_lines():
                self._log(line)

    def on_mod_vendor_open(self) -> None:
        self._log(f"[RAC] [{self.name}] Mod vendor open.")
        # Unlike the weapons vendor, weapon_unlocked here isn't gated on having
        # bought the weapon from ITS OWN vendor — a weapon's mod slot won't
        # render at all if the weapon shows locked, and mods are frequently
        # sold on a different planet than the weapon itself. mod_slot_* (does
        # the player own the mod) is still only restored if purchased from
        # this vendor — owning it via an AP item received elsewhere doesn't
        # restore it (apply_vendor_locations, called below, already does
        # this part unchanged).
        allowed = (
            self._vendor_unlock.mod_vendor_unlock_weapons()
            if self._vendor_unlock is not None else frozenset()
        )
        self._wire_vendor_purchase_callbacks(allowed)
        if self._weapons is not None:
            with self._vendor_write_lock or contextlib.nullcontext():
                self._weapons.zero_unpurchased_mod_slots(allowed)
        if self._vendor_unlock is not None:
            self._vendor_unlock.apply_mod_vendor_weapons(self.accessor)
        # The menu reads unlocked/mod_unlock_N to decide what to render when it
        # opens — our writes above land slightly after that initial read (we're
        # reacting to the same state-change event), so without this the mod
        # vendor can display stale (pre-write) slot visibility. Forcing a
        # refresh here makes it redraw with what we just wrote.
        if self._menu is not None:
            from .menu import MenuStateValue
            self._menu.set_menu(MenuStateValue.MOD_VENDOR)

    def on_menu_close(self) -> None:
        self._log(f"[RAC] [{self.name}] Vendor menu closed — restoring AP inventory.")
        if self._weapons is not None:
            # Restore whatever on_menu_open() displaced (e.g. the bonus-weapon-pickup
            # chain) — resetting to a bare no-op here would permanently kill world
            # pickup detection for the rest of the session after the first vendor visit.
            self._weapons.on_weapon_acquired = self._prev_on_weapon_acquired or (lambda _: None)
            self._weapons.on_gadget_acquired = self._prev_on_gadget_acquired or (lambda _: None)
            self._weapons.on_mod_acquired    = self._prev_on_mod_acquired or (lambda *_: None)
            self._prev_on_weapon_acquired = None
            self._prev_on_gadget_acquired = None
            self._prev_on_mod_acquired    = None
        if self._reapply_inv is not None:
            self._reapply_inv()

    def on_vendor_weapon_purchased(self, _name: str) -> None:
        del _name

    def on_vendor_gadget_purchased(self, _name: str) -> None:
        del _name

    def on_vendor_mod_purchased(self, _weapon: str, _slot: str) -> None:
        del _weapon, _slot

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PlanetState):
            return NotImplemented
        return self.planet_id == other.planet_id

    def __hash__(self) -> int:  # type: ignore[override]
        return hash(self.planet_id)

    def __repr__(self) -> str:
        return f"PlanetState(name={self.name!r}, planet_id={self.planet_id:#04x})"


# Planet load state (runtime)

class PlanetLoadState(BaseState):

    def __init__(
        self,
        accessor: MemoryAccessor,
        addresses: AddressMap,
        storage: LocalStorage,
    ) -> None:
        super().__init__(accessor, addresses, storage)
        self._start_prev:    int = 0
        self._complete_prev: int = 0

        self.on_start_load:    Callable[[], None] = lambda: None
        self.on_load_complete: Callable[[], None] = lambda: None

    def _register_handlers(self) -> None:
        self.accessor.on_struct_change(PlanetLoadStruct, self._on_change)

    def _unregister_handlers(self) -> None:
        self.accessor.remove_struct_handler(PlanetLoadStruct, self._on_change)

    def _on_change(self, _address: int, new_bytes: bytes) -> None:
        instance = PlanetLoadStruct.from_bytes(new_bytes)

        if instance.start_load and not self._start_prev:
            self.on_start_load()

        if instance.load_complete and not self._complete_prev:
            self.on_load_complete()

        self._start_prev    = instance.start_load
        self._complete_prev = instance.load_complete

    def sync(self) -> None:
        instance            = self.accessor.read_struct(PlanetLoadStruct)
        self._start_prev    = instance.start_load
        self._complete_prev = instance.load_complete


# Planet unlock state (runtime)

PLANET_UNLOCK_BASE: int = PlanetProgressStruct.BASE_ADDRESS

class PlanetLockValue(IntEnum):
    LOCKED   = 0x00
    UNLOCKED = 0x03

PLANET_UNLOCK_ORDER: list[str] = list(PlanetProgressStruct.PLANET_NAME_ORDER)

_AUTO_UNLOCK_NAMES: frozenset[str] = frozenset({
    "POKITARU",
    "DREAMTIME",
})

# Planets whose unlock byte the game manages entirely on its own — never
# read, written, or forced by AP. Inside Clank's entrance naturally opens
# once Dayni Moon's own in-game progress (Shrink Ray) allows it; forcing it
# here used to fight that, either locking it back before it should open or
# needlessly rewriting a byte the game already set correctly.
_NATURAL_UNLOCK_NAMES: frozenset[str] = frozenset({"INSIDE_CLANK"})

# Planets auto-unlocked in memory but gated behind different AP progress.
# Maps auto-unlock planet → the planet whose AP status we check for vendor access.
_VENDOR_PLANET_GATE: dict[str, str] = {
    "DREAMTIME":    "OUTPOST_OMEGA",  # reachable only once Outpost Omega infobot received
    "INSIDE_CLANK": "DAYNI_MOON",    # reachable only once Dayni Moon infobot received
}

_COUNT = len(PLANET_UNLOCK_ORDER)

class PlanetUnlockState(BaseState):

    def __init__(
        self,
        accessor: MemoryAccessor,
        addresses: AddressMap,
        storage: LocalStorage,
    ) -> None:
        super().__init__(accessor, addresses, storage)
        self.unlocked: dict[str, bool] = dict.fromkeys(PLANET_UNLOCK_ORDER, False)
        self._desired: dict[str, bool] = {p: p in _AUTO_UNLOCK_NAMES for p in PLANET_UNLOCK_ORDER}
        self._desired["RYLLUS"]        = True
        self._enforce_active: bool     = True
        self._ryllus_released: bool    = False
        self._infobot_planets: set[str] = set()

    def _register_handlers(self) -> None:
        self.accessor.on_struct_change(PlanetProgressStruct, self._on_struct_change)

    def _unregister_handlers(self) -> None:
        self.accessor.remove_struct_handler(PlanetProgressStruct, self._on_struct_change)

    def _on_struct_change(self, address: int, new_bytes: bytes) -> None:
        del address
        instance = PlanetProgressStruct.from_bytes(new_bytes)
        prev = dict(self.unlocked)
        for field, name in zip(PlanetProgressStruct.PLANET_ORDER, PLANET_UNLOCK_ORDER, strict=False):
            self.unlocked[name] = getattr(instance, field) == PlanetLockValue.UNLOCKED

        self._enforce_desired()

        for name in PLANET_UNLOCK_ORDER:
            if self.unlocked[name] and not prev[name]:
                self.on_planet_unlocked(name)
            elif not self.unlocked[name] and prev[name]:
                self.on_planet_locked(name)

    def sync(self) -> None:
        instance = self.accessor.read_struct(PlanetProgressStruct)
        for field, name in zip(PlanetProgressStruct.PLANET_ORDER, PLANET_UNLOCK_ORDER, strict=False):
            self.unlocked[name] = getattr(instance, field) == PlanetLockValue.UNLOCKED
        self._enforce_desired()

    def _enforce_desired(self) -> None:
        if not self._enforce_active:
            return
        names = [n for n in PLANET_UNLOCK_ORDER if n not in _NATURAL_UNLOCK_NAMES]
        if any(self.unlocked[n] != self._desired[n] for n in names):
            self._write_desired(names)
            for name in names:
                self.unlocked[name] = self._desired[name]

    def _write_desired(self, names: list[str]) -> None:
        # Per-field writes rather than one packed write_struct() call, so
        # planets in _NATURAL_UNLOCK_NAMES (e.g. Inside Clank) are never
        # touched at all — a single write_struct() would clobber their live
        # game-managed byte with whatever this instance's default/desired
        # value happened to be.
        for field, name in zip(PlanetProgressStruct.PLANET_ORDER, PLANET_UNLOCK_ORDER, strict=False):
            if name not in names:
                continue
            unlock_val = PlanetLockValue.UNLOCKED if self._desired[name] else PlanetLockValue.LOCKED
            self.accessor.write_field(PlanetProgressStruct, field, unlock_val)
            pu = PLANET_UNLOCKS.get(name)
            if pu is not None:
                state_val = max(int(unlock_val), pu.default_state)
                self.accessor.write_raw(pu.state_addr, bytes([state_val]))

    def set_unlocked_planets(self, planets: set[str]) -> None:
        self._infobot_planets = set(planets)
        for name in PLANET_UNLOCK_ORDER:
            self._desired[name] = name in planets or name in _AUTO_UNLOCK_NAMES
        if not self._ryllus_released:
            self._desired["RYLLUS"] = True

    def on_ryllus_cutscene_ended(self) -> None:
        if self._ryllus_released:
            return
        self._ryllus_released = True
        self._desired["RYLLUS"] = "RYLLUS" in self._infobot_planets

    def reset_session(self) -> None:
        self._ryllus_released = False
        self._desired["RYLLUS"] = True

    def unlock(self, planet: str) -> None:
        self._desired[planet] = True

    def lock(self, planet: str) -> None:
        if planet not in _AUTO_UNLOCK_NAMES:
            self._desired[planet] = False

    def is_unlocked(self, planet: str) -> bool:
        return self._desired.get(planet, False)

    def is_vendor_accessible(self, planet: str) -> bool:
        gate = _VENDOR_PLANET_GATE.get(planet, planet)
        return self._desired.get(gate, False)

    def on_planet_unlocked(self, _planet: str) -> None:
        del _planet

    def on_planet_locked(self, _planet: str) -> None:
        del _planet

    def __repr__(self) -> str:
        count = sum(self.unlocked.values())
        return f"PlanetUnlockState(unlocked={count}/{_COUNT})"
