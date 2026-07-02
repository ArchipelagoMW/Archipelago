from enum import IntFlag

from ..interface import Pine
from .address_maps import PLANET_ADDRESSES

"""
Controller Logic
Holding L1 + L2 + R1 + R2 + START is the hotkey to force-open the Planet Menu
(see PLANET_MENU_HOTKEY / GlobalButtonState.opens_planet_menu).
"""
class PauseSelectButtons(IntFlag):
    SELECT = 0x01
    START  = 0x08
    D_PAD_UP    = 0x10
    D_PAD_DOWN  = 0x40
    D_PAD_LEFT  = 0x80
    D_PAD_RIGHT = 0x20


class ControllerButtons(IntFlag):
    L1       = 0x01
    R1       = 0x02
    L2       = 0x04
    R2       = 0x08
    TRIANGLE = 0x10
    CIRCLE   = 0x20
    CROSS    = 0x40
    SQUARE   = 0x80


# Held together, forces the Planet Menu open via MenuState.set_menu(PLANET_MENU).
PLANET_MENU_HOTKEY: tuple[PauseSelectButtons | ControllerButtons, ...] = (
    ControllerButtons.L1,
    ControllerButtons.L2,
    ControllerButtons.R1,
    ControllerButtons.R2,
    PauseSelectButtons.SELECT,
)


class GlobalButtonState:
    """Snapshot of both controller bytes, read each tick.

    These bytes start at 0xFF (nothing held) and are decremented by a
    button's PauseSelectButtons/ControllerButtons bit value while it's held,
    so a bit reads 0 when pressed and 1 when released. The address is
    per-planet (PlanetAddresses.controller_pause_select_v2, buttons byte at
    +1) and is not yet captured for Outpost Omega.
    """

    def __init__(self, pause_sel: int, buttons: int) -> None:
        self.pause_sel = PauseSelectButtons(~pause_sel & 0xFF)
        self.buttons   = ControllerButtons(~buttons & 0xFF)

    @classmethod
    def read(cls, ipc: Pine, planet_id: int) -> "GlobalButtonState":
        pause_select_addr = PLANET_ADDRESSES[planet_id].controller_pause_select_v2
        if pause_select_addr is None:
            raise ValueError(f"No controller_pause_select_v2 mapped for planet {planet_id:#x}")
        # Values in the table are stored short-form (no 0x20 EE-RAM prefix),
        # matching the convention used for controller_pause_select.
        full_addr = 0x20000000 | pause_select_addr
        return cls(
            ipc.read_int8(full_addr),
            ipc.read_int8(full_addr + 1),
        )

    def pressed(self, *flags: PauseSelectButtons | ControllerButtons) -> bool:
        """Return True if every supplied flag is currently held."""
        for f in flags:
            if isinstance(f, PauseSelectButtons):
                if not (self.pause_sel & f):
                    return False
            else:
                if not (self.buttons & f):
                    return False
        return True

    @property
    def opens_planet_menu(self) -> bool:
        """True while the Planet Menu hotkey combo is held."""
        return self.pressed(*PLANET_MENU_HOTKEY)

    def __repr__(self) -> str:
        # !r forces repr() (which still includes flag names) — since Python 3.11,
        # IntFlag's __str__/__format__ behave like a plain int for backward compat,
        # so neither f"{x}" nor f"{x!s}" show the names anymore.
        return f"GlobalButtonState(pause_sel={self.pause_sel!r}, buttons={self.buttons!r})"
