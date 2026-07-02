from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from ..constants import Rac5Locations
from .address_maps import BRIGHTNESS_ADDRESS, CHEATS, DREAMTIME_EFFECT

if TYPE_CHECKING:
    from ..interface import Pine

# Data
# TRAP_RESET_LEVEL is intentionally absent below — not functional yet.

# Direct memory-flag traps: write 1 to activate, write 0 to revert.
_DIRECT_ADDRESSES: dict[str, int] = {
    Rac5Locations.TRAP_FEVERDREAMTIME: DREAMTIME_EFFECT,
    Rac5Locations.TRAP_BRIGHTNESS:     BRIGHTNESS_ADDRESS,
}

# Cheat-flag traps: bits OR'd into CHEATS (0x21F4C440) so multiple cheat traps
# can be active at once; reverted by clearing only this trap's bit.
MIRROR_LEVEL_CHEAT_BIT:     int = 0x10
REVERSE_CONTROLS_CHEAT_BIT: int = 0x40
WEAPON_SWITCHING_CHEAT_BIT: int = 0x80

_CHEAT_BITS: dict[str, int] = {
    Rac5Locations.TRAP_MIRROR_LEVEL:     MIRROR_LEVEL_CHEAT_BIT,
    Rac5Locations.TRAP_REVERSE_CONTROLS: REVERSE_CONTROLS_CHEAT_BIT,
    Rac5Locations.TRAP_WEAPON_SWITCHING: WEAPON_SWITCHING_CHEAT_BIT,
}

# Seconds each trap stays active before automatically reverting.
TRAP_DURATIONS: dict[str, float] = {
    Rac5Locations.TRAP_FEVERDREAMTIME:   70,
    Rac5Locations.TRAP_BRIGHTNESS:       70,
    Rac5Locations.TRAP_MIRROR_LEVEL:     70,
    Rac5Locations.TRAP_REVERSE_CONTROLS: 70,
    Rac5Locations.TRAP_WEAPON_SWITCHING: 70,
}

ALL_TRAPS: frozenset[str] = frozenset(TRAP_DURATIONS)

# Per-trap-name bookkeeping so repeated activations of the same trap stack
# (extend the revert deadline) instead of racing independent timers, where
# the first trap's revert would fire early and cancel the effect while a
# later-activated copy is still supposed to be running.
_active_deadlines: dict[str, float] = {}
_revert_handles: dict[str, asyncio.TimerHandle] = {}


# Activation

def activate_trap(pine: Pine, trap_name: str) -> None:
    """Activate a trap by name and schedule it to automatically revert.

    A trap activated again while still active extends its revert deadline by
    another full duration (e.g. two Feverdream traps in a row keep the effect
    active for 140s total) rather than reverting at the first trap's deadline.

    Unknown/unimplemented traps (e.g. Reset Level) are silently ignored.
    """
    duration = TRAP_DURATIONS.get(trap_name)
    if duration is None:
        return

    loop = asyncio.get_event_loop()
    now = loop.time()
    new_deadline = max(_active_deadlines.get(trap_name, now), now) + duration
    _active_deadlines[trap_name] = new_deadline

    existing_handle = _revert_handles.pop(trap_name, None)
    if existing_handle is not None:
        existing_handle.cancel()

    if trap_name in _DIRECT_ADDRESSES:
        address = _DIRECT_ADDRESSES[trap_name]
        pine.write_int8(address, 1)

        def _revert() -> None:
            _active_deadlines.pop(trap_name, None)
            _revert_handles.pop(trap_name, None)
            pine.write_int8(address, 0)

        _revert_handles[trap_name] = loop.call_at(new_deadline, _revert)
        return

    bit = _CHEAT_BITS.get(trap_name)
    if bit is None:
        return
    current = pine.read_int8(CHEATS)
    pine.write_int8(CHEATS, current | bit)

    def _revert() -> None:
        _active_deadlines.pop(trap_name, None)
        _revert_handles.pop(trap_name, None)
        latest = pine.read_int8(CHEATS)
        pine.write_int8(CHEATS, latest & ~bit)

    _revert_handles[trap_name] = loop.call_at(new_deadline, _revert)
