"""
BizHawk client for Castlevania: Aria of Sorrow.

This client validates the patched ROM, authenticates, connects, and sends location checks for
collected pickups (``game_watcher``). Receiving items, DeathLink, and goal detection are added
in later phases (see worlds/cvaos/ROADMAP.md).
"""
from __future__ import annotations

import base64
from typing import TYPE_CHECKING

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from .locations import flag_offset_to_location_id
from .ram import AoSRAM
from .rom import ARCHIPELAGO_IDENTIFIER, ARCHIPELAGO_IDENTIFIER_START, AUTH_NUMBER_START

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

# GBA header: 12-byte internal game title at 0xA0 (CLIENT_PLAN sec. 5a).
ROM_NAME_START = 0xA0
ROM_NAME = "CASTLEVANIA2"


class CVAOSClient(BizHawkClient):
    game = "Castlevania - Aria of Sorrow"
    system = "GBA"
    patch_suffix = ".apcvaos"

    # Per-session state, (re)initialized in set_auth.
    death_causes: list[str]
    local_checked_locations: set[int]

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger

        try:
            rom_name, identifier = await bizhawk.read(ctx.bizhawk_ctx, [
                (ROM_NAME_START, len(ROM_NAME), "ROM"),
                (ARCHIPELAGO_IDENTIFIER_START, len(ARCHIPELAGO_IDENTIFIER), "ROM"),
            ])
            # Reject anything that isn't Aria of Sorrow.
            if rom_name.decode("ascii", "ignore") != ROM_NAME:
                return False
            # Reject an unpatched ROM (the identifier region is still zeroed).
            if identifier == b"\x00" * len(ARCHIPELAGO_IDENTIFIER):
                logger.info("ERROR: This looks like an unpatched Aria of Sorrow ROM. Generate a "
                            "patch file and use it to create a patched ROM.")
                return False
            # Reject a ROM patched by an incompatible generator/client version.
            if identifier.decode("ascii", "ignore") != ARCHIPELAGO_IDENTIFIER:
                logger.info("ERROR: This ROM was patched by an incompatible version. Check your "
                            "client version against the one used to generate the seed.")
                return False
        except (UnicodeDecodeError, bizhawk.RequestFailedError):
            return False

        ctx.game = self.game
        ctx.items_handling = 0b001  # receive items from other worlds
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125
        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        auth_raw = (await bizhawk.read(ctx.bizhawk_ctx, [(AUTH_NUMBER_START, 16, "ROM")]))[0]
        ctx.auth = base64.b64encode(auth_raw).decode("ascii")
        # Reset per-session state so swapping ROMs without restarting the client can't carry
        # anything stale over.
        self.death_causes = []
        self.local_checked_locations = set()

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        # Queue an incoming DeathLink's cause; game_watcher applies the kill (Phase 4).
        if cmd != "Bounced" or "tags" not in args or ctx.slot is None:
            return
        if "DeathLink" in args["tags"]:
            data = args.get("data", {})
            source = data.get("source", "Another world")
            self.death_causes.append(data.get("cause") or f"{source} killed you without a word!")

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None or ctx.slot is None:
            return
        try:
            ram = AoSRAM(ctx.bizhawk_ctx)
            # Only read/act in normal in-room gameplay (not paused, transitioning, in a menu,
            # or game-over), so we never read garbage or act at an unsafe time.
            if not await ram.is_in_gameplay():
                return

            # Collected-pickup save flags -> AP location checks. Each set bit's index is a
            # pickup's flag_offset. We map it to the AP location id and send it if the server
            # tracks that location for this slot.
            flag_bytes = await ram.read_pickup_flags()
            checked: set[int] = set()
            for flag_offset in AoSRAM.pickup_flag_ids(flag_bytes):
                location_id = flag_offset_to_location_id.get(flag_offset)
                if location_id is not None and location_id in ctx.server_locations:
                    checked.add(location_id)

            new_checks = checked - self.local_checked_locations
            if new_checks:
                self.local_checked_locations |= new_checks
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": sorted(new_checks)}])

            # Receiving items, DeathLink, and goal detection arrive in later phases (ROADMAP).
        except bizhawk.RequestFailedError:
            # Emulator/connection hiccup; retry next tick.
            return
