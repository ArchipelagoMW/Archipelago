"""
BizHawk client for Castlevania: Aria of Sorrow.

Phase 1 scope (see worlds/cvaos/ROADMAP.md): validate the patched ROM, authenticate, and
connect. Reading game state, sending location checks, receiving items, DeathLink, and goal
detection are added in later phases; ``game_watcher`` is intentionally idle for now.
"""
from __future__ import annotations

import base64
from typing import TYPE_CHECKING

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

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

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        # Queue an incoming DeathLink's cause; game_watcher applies the kill (Phase 4).
        if cmd != "Bounced" or "tags" not in args or ctx.slot is None:
            return
        if "DeathLink" in args["tags"]:
            data = args.get("data", {})
            source = data.get("source", "Another world")
            self.death_causes.append(data.get("cause") or f"{source} killed you without a word!")

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        # Phase 1: connectable only. Location-sending, item-receiving, DeathLink, and goal
        # detection arrive in later phases (ROADMAP §2-5). Intentionally idle for now.
        return
