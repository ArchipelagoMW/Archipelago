from __future__ import annotations

import time
from collections.abc import Callable

from ..interface_orchestrator.memory.accessor import MemoryAccessor
from ..interface_orchestrator.state.base_state import BaseState
from ..interface_orchestrator.storage.local import LocalStorage
from ..interface_orchestrator.structs.address_map import AddressMap
from .structs.game import QuickSelectStruct

_ZERO_BYTES = bytes(4 * len(QuickSelectStruct.SLOT_ORDER))

# After writing the snapshot, ignore incoming changes for this long.  This
# prevents the game from overwriting specific slots (e.g. gadget defaults at
# the left / bottom-left positions) from polluting the snapshot immediately
# after our write.
_WRITE_COOLDOWN_S: float = 0.3


class QuickSelectState(BaseState):

    def __init__(
        self,
        accessor: MemoryAccessor,
        addresses: AddressMap,
        storage: LocalStorage,
    ) -> None:
        super().__init__(accessor, addresses, storage)
        self._snapshot: dict[str, int] = dict.fromkeys(QuickSelectStruct.SLOT_ORDER, 0)
        self._polling = False
        self._write_time: float = 0.0
        self.on_save: Callable[[dict[str, int]], None] = lambda _: None

    def on_exit(self) -> None:
        self._stop_polling()

    def load(self, data: dict[str, int]) -> None:
        """Load a saved quick-select snapshot (e.g. from AP data storage)."""
        for name in QuickSelectStruct.SLOT_ORDER:
            if name in data:
                self._snapshot[name] = int(data[name])

    def push_save(self) -> None:
        """Push the current snapshot to AP data storage. Called explicitly
        (e.g. on pause-menu close) rather than on every poll-detected change,
        since that would echo back via set_notify and re-trigger restores."""
        self.on_save(dict(self._snapshot))

    # Starts frozen — polling only begins after zero() is called on first planet load.
    def _register_handlers(self) -> None:
        pass

    def _unregister_handlers(self) -> None:
        self._stop_polling()

    def freeze(self) -> None:
        """Stop updating the snapshot (planet transition or vendor open)."""
        self._stop_polling()

    def unfreeze(self) -> None:
        """Resume snapshot updates."""
        self._start_polling()

    def _start_polling(self) -> None:
        if not self._polling:
            self.accessor.on_struct_change(QuickSelectStruct, self._on_change)
            self._polling = True

    def _stop_polling(self) -> None:
        if self._polling:
            self.accessor.remove_struct_handler(QuickSelectStruct, self._on_change)
            self._polling = False

    def _on_change(self, _address: int, new_bytes: bytes) -> None:
        # Suppress changes that arrive in the cooldown window after our own write.
        # The game sometimes reassigns default gadgets to specific wheel positions
        # immediately after we restore the snapshot; this prevents that from
        # overwriting what the player deliberately put there.
        if time.monotonic() - self._write_time < _WRITE_COOLDOWN_S:
            return
        instance = QuickSelectStruct.from_bytes(new_bytes)
        for name in QuickSelectStruct.SLOT_ORDER:
            self._snapshot[name] = getattr(instance, name)

    def sync(self) -> None:
        instance = self.accessor.read_struct(QuickSelectStruct)
        for name in QuickSelectStruct.SLOT_ORDER:
            self._snapshot[name] = getattr(instance, name)

    def zero(self) -> None:
        """Zero all slots in memory, then start polling.

        The in-memory snapshot is preserved so that a previously saved loadout
        (restored via on_enter) can be written back by the following restore().
        """
        self._write_time = time.monotonic()
        self.accessor.write_raw(QuickSelectStruct.BASE_ADDRESS, _ZERO_BYTES)
        self._start_polling()

    def restore(self) -> None:
        """Write the current snapshot to memory without checking polling state.

        Call this BEFORE unfreeze() when resuming after a planet transition so
        the poller's first read sees our values, not game-default values.
        """
        self._write_time = time.monotonic()
        instance = QuickSelectStruct()
        for name in QuickSelectStruct.SLOT_ORDER:
            setattr(instance, name, self._snapshot[name])
        self.accessor.write_struct(instance)

    def apply(self) -> None:
        """Write the current snapshot back to memory, zeroing any empty slots."""
        if not self._polling:
            return
        self._write_time = time.monotonic()
        instance = QuickSelectStruct()
        for name in QuickSelectStruct.SLOT_ORDER:
            setattr(instance, name, self._snapshot[name])
        self.accessor.write_struct(instance)
