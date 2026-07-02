from __future__ import annotations

from collections.abc import Callable, Iterable

from ...interface import Pine


class MemoryState:
    """Snapshot, clear, and restore a group of int8 memory addresses.

    Accepts a callable so addresses are evaluated lazily — useful when the
    underlying dict (e.g. WEAPONS) is populated after import time.
    """

    def __init__(self, get_addresses: Callable[[], Iterable[int]]) -> None:
        self._get_addresses = get_addresses
        self._saved: dict[int, int] = {}

    def save(self, ipc: Pine) -> None:
        self._saved = {addr: ipc.read_int8(addr) for addr in self._get_addresses()}

    def remove(self, ipc: Pine) -> None:
        for addr in self._get_addresses():
            ipc.write_int8(addr, 0)

    def take(self, ipc: Pine) -> None:
        addrs = list(self._get_addresses())
        self._saved = {addr: ipc.read_int8(addr) for addr in addrs}
        for addr in addrs:
            ipc.write_int8(addr, 0)

    def restore(self, ipc: Pine) -> None:
        if not self._saved:
            return
        for addr, val in self._saved.items():
            ipc.write_int8(addr, val)


class ItemScanner:
    """Detects items written by the game into memory during a pickup window.

    Addresses are evaluated lazily so the scanner works even when the
    underlying dicts (e.g. WEAPONS) are populated after import time.

    Typical usage:
        scanner.clear(ipc)   # on pickup_start: zero addresses for detection
        scanner.scan(ipc)    # on pickup_end:   read and fire on_detected
        scanner.clear(ipc)   # on pickup_end:   zero again before state restore
    """

    def __init__(
        self,
        get_items: Callable[[], dict[str, int]],
        on_detected: Callable[[str, int], None],
    ) -> None:
        self._get_items   = get_items
        self._on_detected = on_detected

    def clear(self, ipc: Pine) -> None:
        for addr in self._get_items().values():
            ipc.write_int8(addr, 0)

    def scan(self, ipc: Pine) -> None:
        for name, addr in self._get_items().items():
            val = ipc.read_int8(addr)
            if val:
                self._on_detected(name, val)


class Int64State:
    """Tracks a single int64 memory address as an OR-accumulating bitmask.

    Designed for bolt-pickup and skill-point registers where each collected
    item is a distinct bit.  apply_or() reads current memory, ORs in the
    tracked bits, writes back, and returns the new value so the caller can
    sync any delta-detection trackers.
    """

    def __init__(
        self,
        address: int,
        name: str = "Int64State",
        debug_log: Callable[[str], None] | None = None,
    ) -> None:
        self._address  = address
        self._value    = 0
        self._name     = name
        self._debug_log = debug_log

    def add(self, bits: int) -> None:
        """OR bits into the tracked value (does not write to memory)."""
        self._value |= bits

    def reset(self) -> None:
        """Clear all tracked bits."""
        self._value = 0

    def apply_or(self, pine: Pine) -> int:
        """Read memory, OR in tracked bits, write back.  Returns new value.

        Using OR means bits already set by the game (e.g. picked up this
        session before connection) are preserved.
        """
        current = pine.read_int64(self._address)
        new_val = current | self._value
        if new_val != current:
            if self._debug_log is not None:
                self._debug_log(f"[{self._name}] restoring 0x{new_val:016X} (was 0x{current:016X})")
            pine.write_int64(self._address, new_val)
        return new_val

    @property
    def value(self) -> int:
        return self._value

    def __repr__(self) -> str:
        return f"{self._name}(0x{self._value:016X})"


class MemoryItemState:
    """Generic tracked state for a named set of int8 PS2 memory addresses.

    Maintains two views:
      _values  — the *desired* state; updated via add() by the owner.
      _prev    — the last-known state in memory; used by update() to detect
                 in-game writes.  Stays in sync after give(), take(), remove(),
                 and restore().

    Typical pickup-window usage
    ---------------------------
        state.take(pine)    # snapshot pre-pickup values, zero addresses,
                            # reset _prev to 0 so new game writes are visible
        # … game runs, writes bitmasks to the zeroed addresses …
        state.update(pine)  # reads addresses; calls on_change(key, new_val)
                            # for every address that changed vs _prev
        state.restore(pine) # put pre-pickup snapshot back into memory

    Contiguous-block optimisation
    -----------------------------
    When all addresses form a consecutive byte run (e.g. the seven armour-set
    bytes at base+0x06 … base+0x0C), give() issues a single write_bytes call
    instead of seven individual write_int8 calls.
    """

    def __init__(
        self,
        addresses: dict[str, int],
        on_change: Callable[[str, int], None] | None = None,
        *,
        name: str = "MemoryItemState",
        debug_log: Callable[[str], None] | None = None,
    ) -> None:
        self._addresses: dict[str, int] = dict(addresses)
        self._values:    dict[str, int] = dict.fromkeys(addresses, 0)
        self._prev:      dict[str, int] = dict.fromkeys(addresses, 0)
        self._on_change                 = on_change
        self._saved:     dict[int, int] = {}
        self._name                      = name
        self._debug_log                 = debug_log

        sorted_addrs = sorted(self._addresses.values())
        self._contiguous: bool = bool(sorted_addrs) and (
            len(sorted_addrs) == 1
            or sorted_addrs[-1] - sorted_addrs[0] == len(sorted_addrs) - 1
        )
        if self._contiguous:
            self._sorted_keys  = sorted(self._addresses, key=lambda k: self._addresses[k])
            self._base_address = sorted_addrs[0]

    # Desired-state management

    def add(self, key: str, value: int) -> None:
        """Set the desired value for *key* (does not write to memory)."""
        if key in self._values:
            self._values[key] = value & 0xFF

    # Memory operations

    def give(self, pine: Pine) -> None:
        """Write every desired value to its address.

        Uses a single write_bytes call when addresses are contiguous;
        otherwise falls back to individual write_int8 calls.
        _prev is synced to _values after writing so update() won't immediately
        re-detect the write.
        """
        if not self._addresses:
            return
        if self._contiguous:
            data = bytes(self._values[k] for k in self._sorted_keys)
            pine.write_bytes(self._base_address, data)
        else:
            for key, addr in self._addresses.items():
                if addr == 0:
                    continue  # placeholder address not yet confirmed
                pine.write_int8(addr, self._values[key])
        self._prev = dict(self._values)

    def update(self, pine: Pine) -> None:
        """Read each address; call on_change(key, new_value) for any that differ
        from _prev.  _prev is updated after each callback fires.

        NOTE: _values is *not* modified — the caller (or the callback) is
        responsible for calling add() to record the change in desired state.
        """
        for key, addr in self._addresses.items():
            current = pine.read_int8(addr) & 0xFF
            if current != self._prev[key]:
                if self._debug_log is not None:
                    self._debug_log(
                        f"[{self._name}] {key}: 0x{self._prev[key]:02X} → 0x{current:02X}"
                    )
                if self._on_change is not None:
                    self._on_change(key, current)
                self._prev[key] = current

    def take(self, pine: Pine) -> None:
        """Snapshot current memory values, zero all addresses, reset _prev to 0.

        After take(), update() detects any write the game makes from a clean
        baseline of 0, regardless of what was in _values before the call.
        """
        self._saved = {}
        for addr in self._addresses.values():
            self._saved[addr] = pine.read_int8(addr) & 0xFF
            pine.write_int8(addr, 0)
        self._prev = dict.fromkeys(self._addresses, 0)

    def remove(self, pine: Pine) -> None:
        """Zero all addresses without snapshotting, reset _prev to 0."""
        for addr in self._addresses.values():
            pine.write_int8(addr, 0)
        self._prev = dict.fromkeys(self._addresses, 0)

    def restore(self, pine: Pine) -> None:
        """Write the snapshot taken by take() back to memory and sync _prev."""
        if not self._saved:
            return
        for addr, val in self._saved.items():
            pine.write_int8(addr, val)
        for key, addr in self._addresses.items():
            if addr in self._saved:
                self._prev[key] = self._saved[addr]

    def update_addresses(self, addresses: dict[str, int]) -> None:
        """Replace the address map. Values and _prev for surviving keys are kept;
        new keys start at 0. Contiguous detection is re-run. Clears _saved."""
        self._addresses = dict(addresses)
        self._values    = {k: self._values.get(k, 0) for k in addresses}
        self._prev      = {k: self._prev.get(k, 0)   for k in addresses}
        self._saved     = {}
        sorted_addrs    = sorted(self._addresses.values())
        self._contiguous = bool(sorted_addrs) and (
            len(sorted_addrs) == 1
            or sorted_addrs[-1] - sorted_addrs[0] == len(sorted_addrs) - 1
        )
        if self._contiguous:
            self._sorted_keys  = sorted(self._addresses, key=lambda k: self._addresses[k])
            self._base_address = sorted_addrs[0]
        else:
            self._sorted_keys  = []
            self._base_address = 0

    # Accessors

    def get(self, key: str, default: int = 0) -> int:
        return self._values.get(key, default)

    @property
    def values(self) -> dict[str, int]:
        """Desired state (_values) — what we intend to write."""
        return dict(self._values)

    @property
    def memory_values(self) -> dict[str, int]:
        """Last-seen memory state (_prev) — updated by update(), give(), take(), restore()."""
        return dict(self._prev)

    def __repr__(self) -> str:
        pairs = ", ".join(
            f"{k}=0x{self._values[k]:02X}"
            for k in self._addresses
            if self._values[k]
        )
        return f"{self._name}({pairs or 'empty'})"
