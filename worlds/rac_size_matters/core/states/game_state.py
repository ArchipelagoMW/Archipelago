from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...interface import Pine


class PollAddress:
    """Polls a memory address and fires a callback when the value changes.

    PollAddress(addr, callback)           fires callback(old, new) on any change.
    PollAddress(addr, callback, trigger)  fires only when trigger(old, new) is True.

    addr may be a callable for dynamic addresses.
    read_fn(ipc, addr) overrides the default int8 read.
    """

    def __init__(
        self,
        address: int | Callable[[], int],
        callback: Callable[[int, int], None],
        trigger: Callable[[int, int], bool] | None = None,
        *,
        read_fn: Callable[[Pine, int], int] | None = None,
    ) -> None:
        self._addr     = address
        self._callback = callback
        self._trigger  = trigger
        self._read_fn  = read_fn or (lambda ipc, addr: ipc.read_int8(addr))
        self._last: int | None = None

    def tick(self, ipc: Pine) -> None:
        addr = self._addr() if callable(self._addr) else self._addr
        val  = self._read_fn(ipc, addr)
        if self._last is None:
            self._last = val
            return
        old = self._last
        if val != old:
            self._last = val
            if self._trigger is None or self._trigger(old, val):
                self._callback(old, val)

    @property
    def value(self) -> int | None:
        return self._last


@dataclass
class GameState:
    ipc:                    Pine
    tracked_armour:         dict[str, int]         = field(default_factory=dict)
    tracked_weapons:        dict[str, int]         = field(default_factory=dict)
    tracked_gadgets:        dict[str, int]         = field(default_factory=dict)
    tracked_mods:           dict[str, set[str]]    = field(default_factory=dict)
    tracked_weapon_levels:  dict[str, int]         = field(default_factory=dict)
    tracked_vendor_weapons: dict[str, int]         = field(default_factory=dict)
    tracked_vendor_gadgets: dict[str, int]         = field(default_factory=dict)
    tracked_vendor_mods:    dict[str, set[str]]    = field(default_factory=dict)
    picked_up_items:        dict[str, int]         = field(default_factory=dict)
    current_planet:         int                    = 0
    state_addr:             int | None             = None
    tracked_vendor:         int | None             = None
    weapons_ready:          bool                   = False
    goal_reached:           bool                   = False
    on_reward:              Callable[[], None] | None = field(default=None)
