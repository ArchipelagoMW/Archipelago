from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass
class SimulatedHGSSInterface:
    """
    Temporary fake game interface.

    Later, this will be replaced or expanded with an emulator-backed interface
    that reads HGSS memory.

    For now, it pretends that listed game event keys become completed over time.
    """

    simulated_event_keys: list[str]
    delay_seconds: float = 2.0
    start_time: float = field(default_factory=time.monotonic)

    def get_completed_event_keys(self) -> list[str]:
        if not self.simulated_event_keys:
            return []

        if self.delay_seconds <= 0:
            return list(self.simulated_event_keys)

        elapsed_time = time.monotonic() - self.start_time

        completed_count = int(elapsed_time // self.delay_seconds) + 1
        completed_count = min(
            completed_count,
            len(self.simulated_event_keys),
        )

        return self.simulated_event_keys[:completed_count]