import os
from typing import TYPE_CHECKING, List, Optional, Set

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from .data import data

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext


EXPECTED_ROM_NAME_PREFIX = "kirby amazing mirror"  # loosen while you iterate

# DEBUG: Temporary development aid.
# Simulate the player earning one new location every N emulated frames.
# Set KIRBYAM_DEBUG_SIMULATION=1 to enable simulation (falls back to RAM-driven polling by default).
# TODO: Remove simulated location mode entirely once real ROM polling is verified to work correctly.
SIMULATED_LOCATION_EVERY_N_FRAMES = 10000 if os.getenv("KIRBYAM_DEBUG_SIMULATION") else 0


class KirbyAmClient(BizHawkClient):
    game = "Kirby & The Amazing Mirror"
    system = "GBA"
    patch_suffix = ".apkirbyam"

    def initialize_client(self) -> None:
        # Real polling state (shards)
        self._checked_location_bits: set[int] = set()

        # Item delivery state
        self._delivered_item_index: int = 0
        self._delivery_pending: bool = False  # True after writing mailbox until ROM clears flag

        # Simulation state (frame-based cadence + persistent cursor)
        self._last_simulated_frame: int = 0
        self._simulated_location_index: int = 0

        # Deterministic location ordering
        self._all_location_ids_sorted: list[int] = [
            loc.location_id for loc in sorted(data.locations.values(), key=lambda l: l.location_id)
        ]

        # One-time RAM state load
        self._ram_state_loaded: bool = False

        # Goal reporting
        self._goal_reported: bool = False

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger

        try:
            rom_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(0x108, 32, "ROM")]))[0]
            rom_name = bytes([b for b in rom_name_bytes if b != 0]).decode("ascii", errors="ignore").lower()
            if not rom_name.startswith(EXPECTED_ROM_NAME_PREFIX):
                return False
        except Exception:
            return False

        # Minimal AP settings
        ctx.game = self.game
        ctx.items_handling = 0b001
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125

        self.initialize_client()
        logger.info("Kirby client validated ROM.")
        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        """
        Read the per-seed auth token from ROM and use it to authenticate.
        Requires addresses.json to define rom.gArchipelagoInfo (16 bytes).
        """
        import base64

        auth_addr = data.rom_addresses.get("gArchipelagoInfo")
        if auth_addr is None:
            raise Exception("Missing rom address 'gArchipelagoInfo' in worlds/kirbyam/data/addresses.json")

        auth_raw = (await bizhawk.read(ctx.bizhawk_ctx, [(auth_addr, 16, "ROM")]))[0]
        ctx.auth = base64.b64encode(auth_raw).decode("utf-8")

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        # Only run when connected and slot_data is ready
        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None:
            return

        # Load persisted state from RAM once per session (after bizhawk_ctx is valid)
        if not self._ram_state_loaded:
            await self._load_persistent_state(ctx)
            self._ram_state_loaded = True

        # Location checks (real RAM polling; simulation gated behind debug flag)
        if SIMULATED_LOCATION_EVERY_N_FRAMES > 0:
            await self._simulate_locations(ctx)
        else:
            await self._poll_locations(ctx)

        # Item delivery (mailbox protocol)
        await self._deliver_items(ctx)

        # Temporary goal reporting
        await self._maybe_report_goal(ctx)

    # --------------------------
    # Helpers / persistence
    # --------------------------

    @staticmethod
    def _u32_le(b: bytes) -> int:
        return int.from_bytes(b, "little")

    async def _persist_u32(self, ctx: "BizHawkClientContext", key: str, value: int) -> None:
        addr = data.ram_addresses.get(key)
        if addr is None:
            return
        await bizhawk.write(ctx.bizhawk_ctx, [(addr, int(value & 0xFFFFFFFF).to_bytes(4, "little"), "System Bus")])

    async def _load_persistent_state(self, ctx: "BizHawkClientContext") -> None:
        """
        Best-effort load of persistent state from our reserved mailbox RAM block.
        If addresses are missing, this simply does nothing.
        """
        reads = []
        keys_in_order = []

        # Your addresses.json defines:
        # - delivered_item_index
        # - sim_last_frame
        # - sim_next_index  (we will treat this as "simulated next location index cursor")
        for key in ("delivered_item_index", "sim_last_frame", "sim_next_index"):
            addr = data.ram_addresses.get(key)
            if addr is not None:
                reads.append((addr, 4, "System Bus"))
                keys_in_order.append(key)

        if not reads:
            return

        raw_list = await bizhawk.read(ctx.bizhawk_ctx, reads)

        for key, raw in zip(keys_in_order, raw_list):
            val = self._u32_le(raw)
            if key == "delivered_item_index":
                self._delivered_item_index = val
            elif key == "sim_last_frame":
                self._last_simulated_frame = val
            elif key == "sim_next_index":
                # Interpreted as "next simulated location index cursor"
                if self._all_location_ids_sorted:
                    self._simulated_location_index = min(val, len(self._all_location_ids_sorted))
                else:
                    self._simulated_location_index = 0

    # --------------------------
    # Location checking
    # --------------------------

    async def _simulate_locations(self, ctx: "BizHawkClientContext") -> None:
        """
        Temporary: send one new LocationChecks every N emulated frames.

        - Uses frame_counter if present.
        - Deterministic ordering: ascending location_id.
        - Reconnect safe: skips any location already in ctx.checked_locations.
        - Persists last_simulated_frame and the cursor (stored in sim_next_index).
        """
        if not self._all_location_ids_sorted:
            return

        frame_addr = data.ram_addresses.get("frame_counter")
        if frame_addr is None:
            current_frame = (self._last_simulated_frame + 1) & 0xFFFFFFFF
        else:
            raw = (await bizhawk.read(ctx.bizhawk_ctx, [(frame_addr, 4, "System Bus")]))[0]
            current_frame = self._u32_le(raw)

        # Wrap-safe u32 delta
        delta = (current_frame - self._last_simulated_frame) & 0xFFFFFFFF
        if delta < SIMULATED_LOCATION_EVERY_N_FRAMES:
            return

        # Keep cadence stable even if watcher ticks slip
        self._last_simulated_frame = (self._last_simulated_frame + SIMULATED_LOCATION_EVERY_N_FRAMES) & 0xFFFFFFFF
        await self._persist_u32(ctx, "sim_last_frame", self._last_simulated_frame)

        # Find next unchecked location, starting from persisted cursor
        n = len(self._all_location_ids_sorted)
        while self._simulated_location_index < n:
            loc_id = self._all_location_ids_sorted[self._simulated_location_index]
            self._simulated_location_index += 1

            # Persist cursor after moving it, so restarts continue from the same place
            await self._persist_u32(ctx, "sim_next_index", self._simulated_location_index)

            if loc_id in ctx.checked_locations:
                continue

            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [loc_id]}])
            return

        # If we ran out, nothing to do (goal reporting will handle completion)

    async def _poll_locations(self, ctx: "BizHawkClientContext") -> None:
        """
        Long-term plan: read a shard bitfield and map set bits to locations.
        """
        shard_addr = data.ram_addresses["shard_bitfield"]
        raw = (await bizhawk.read(ctx.bizhawk_ctx, [(shard_addr, 4, "System Bus")]))[0]
        shard_bits = self._u32_le(raw)

        newly_checked = []
        for bit in range(32):
            if (shard_bits >> bit) & 1:
                if bit not in self._checked_location_bits:
                    self._checked_location_bits.add(bit)
                    for loc in data.locations.values():
                        if loc.bit_index == bit:
                            newly_checked.append(loc.location_id)

        if newly_checked:
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": newly_checked}])

    # --------------------------
    # Item delivery (mailbox protocol)
    # --------------------------

    async def _deliver_items(self, ctx: "BizHawkClientContext") -> None:
        """
        Mailbox protocol:
        - Client writes item_id + player + flag=1
        - ROM consumes and clears flag back to 0
        We only advance delivered_item_index once we observe the flag was cleared (ACK).
        """
        flag_addr = data.ram_addresses["incoming_item_flag"]
        id_addr = data.ram_addresses["incoming_item_id"]
        player_addr = data.ram_addresses["incoming_item_player"]

        raw_flag = (await bizhawk.read(ctx.bizhawk_ctx, [(flag_addr, 4, "System Bus")]))[0]
        flag = self._u32_le(raw_flag)

        # If an item is pending, wait for ROM to clear the flag (ACK)
        if self._delivery_pending:
            if flag == 0:
                self._delivery_pending = False
                self._delivered_item_index += 1
                await self._persist_u32(ctx, "delivered_item_index", self._delivered_item_index)
            return

        # No pending item; mailbox must be empty to write
        if flag != 0:
            return

        # Nothing to deliver
        if self._delivered_item_index >= len(ctx.items_received):
            return

        itm = ctx.items_received[self._delivered_item_index]

        # Write item and mark mailbox full
        await bizhawk.write(ctx.bizhawk_ctx, [
            (id_addr, int(itm.item).to_bytes(4, "little"), "System Bus"),
            (player_addr, int(itm.player).to_bytes(4, "little"), "System Bus"),
            (flag_addr, (1).to_bytes(4, "little"), "System Bus"),
        ])
        self._delivery_pending = True

    # --------------------------
    # Temporary completion condition
    # --------------------------

    async def _maybe_report_goal(self, ctx: "BizHawkClientContext") -> None:
        """
        Temporary development goal: mark finished when all locations in data.locations are checked.
        """
        if self._goal_reported:
            return

        if not self._all_location_ids_sorted:
            return

        if all(loc_id in ctx.checked_locations for loc_id in self._all_location_ids_sorted):
            from NetUtils import ClientStatus
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            self._goal_reported = True
