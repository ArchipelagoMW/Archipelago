from typing import TYPE_CHECKING, Optional

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from .data import LocationCategory, data
from .options import Goal
from .types import KirbyAmBizHawkClientContext

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
    from worlds.generic.shared_utils import NetworkItem


EXPECTED_ROM_NAME_PREFIX = "kirby amazing mirror"  # loosen while you iterate
_BOSS_MIRROR_TABLE_PROBE_BYTES = 32
_AI_STATE_ADDR_WIDTH = 4
_GOAL_STATE_DARK_MIND_CLEAR = 9999
_GOAL_STATE_FULL_CLEAR = 10000
_MAILBOX_ACK_TIMEOUT_FRAMES = 30


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
        self._delivery_pending_frame: int | None = None

        # Deterministic location ordering
        self._all_location_ids_sorted: list[int] = [
            loc.location_id for loc in sorted(data.locations.values(), key=lambda l: l.location_id)
        ]
        self._goal_location_ids_by_option: dict[int, int] = {}
        self._non_goal_location_ids_sorted: list[int] = []
        for loc in sorted(data.locations.values(), key=lambda l: l.location_id):
            if loc.category.name == "GOAL":
                if loc.name == "GOAL_DARK_MIND":
                    self._goal_location_ids_by_option[Goal.option_dark_mind] = loc.location_id
                elif loc.name == "GOAL_100_PERCENT":
                    self._goal_location_ids_by_option[Goal.option_100] = loc.location_id
            else:
                self._non_goal_location_ids_sorted.append(loc.location_id)
        # Shard bitfield → location IDs (SHARD category only; BOSS_DEFEAT uses separate bitfield)
        self._location_ids_by_bit: dict[int, list[int]] = {}
        for loc in data.locations.values():
            if loc.bit_index is None or loc.category != LocationCategory.SHARD:
                continue
            self._location_ids_by_bit.setdefault(loc.bit_index, []).append(loc.location_id)

        # Boss defeat bitfield → location IDs (BOSS_DEFEAT category; polled from boss_defeat_flags)
        self._boss_location_ids_by_bit: dict[int, list[int]] = {}
        for loc in data.locations.values():
            if loc.bit_index is None or loc.category != LocationCategory.BOSS_DEFEAT:
                continue
            self._boss_location_ids_by_bit.setdefault(loc.bit_index, []).append(loc.location_id)

        # One-time RAM state load
        self._ram_state_loaded: bool = False

        # Goal reporting
        self._goal_reported: bool = False
        self._goal_location_reported: bool = False
        self._native_goal_signal_seen: bool = False

        # Boss candidate probing state
        self._last_boss_probe_snapshot: bytes | None = None
        self._boss_probe_stream_marker: int | None = None

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        """Validate ROM is Kirby & The Amazing Mirror and initialize client."""
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
        """Main watcher loop: polls locations, delivers items, reports goal."""
        # Only run when connected and slot_data is ready
        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None:
            return

        # Load persisted state from RAM once per session (after bizhawk_ctx is valid)
        if not self._ram_state_loaded:
            await self._load_persistent_state(ctx)
            self._ram_state_loaded = True

        # Location checks (real RAM polling)
        await self._poll_locations(ctx)

        # Boss defeat location polling via transport register
        await self._poll_boss_defeat_locations(ctx)

        # Candidate discovery for non-shard boss defeat signals.
        await self._probe_boss_defeat_candidates(ctx)

        # Item delivery (mailbox protocol)
        await self._deliver_items(ctx)

        # Goal reporting
        await self._maybe_report_goal(ctx)

    # --------------------------
    # Helpers / persistence
    # --------------------------

    @staticmethod
    def _u32_le(b: bytes) -> int:
        return int.from_bytes(b, "little")

    @staticmethod
    def _transport_addr(key: str) -> Optional[int]:
        if key in data.transport_ram_addresses:
            return data.transport_ram_addresses[key]
        return data.ram_addresses.get(key)

    @staticmethod
    def _native_addr(key: str) -> Optional[int]:
        if key in data.native_ram_addresses:
            return data.native_ram_addresses[key]
        return None

    @staticmethod
    def _coerce_u32(value: object) -> int | None:
        try:
            parsed = int(value)
        except (TypeError, ValueError):
            return None
        if 0 <= parsed <= 0xFFFFFFFF:
            return parsed
        return None

    @classmethod
    def _extract_delivery_item_fields(cls, network_item: object) -> tuple[int, int] | None:
        item_value = cls._coerce_u32(getattr(network_item, "item", None))
        player_value = cls._coerce_u32(getattr(network_item, "player", None))
        if item_value is None or player_value is None:
            return None
        return item_value, player_value

    async def _persist_u32(self, ctx: KirbyAmBizHawkClientContext, key: str, value: int) -> None:
        """Persist a 32-bit value to RAM by address key."""
        addr = self._transport_addr(key)
        if addr is None:
            return
        await bizhawk.write(ctx.bizhawk_ctx, [(addr, int(value & 0xFFFFFFFF).to_bytes(4, "little"), "System Bus")])

    async def _load_persistent_state(self, ctx: KirbyAmBizHawkClientContext) -> None:
        """
        Best-effort load of persistent state from our reserved mailbox RAM block.
        If addresses are missing, this simply does nothing.
        """
        reads = []
        keys_in_order = []

        # Your addresses.json defines delivered_item_index.
        for key in ("delivered_item_index",):
            addr = self._transport_addr(key)
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

    # --------------------------
    # Location checking
    # --------------------------

    async def _poll_locations(self, ctx: KirbyAmBizHawkClientContext) -> None:
        """
        Primary location polling: read shard bitfield and map set bits to locations.
        
        Behavior:
        - Reads shard_bitfield_native from native RAM when available
        - Falls back to shard_bitfield transport mirror for compatibility
        - Each mapped bit can correspond to one or more AP location ids
        - RAM state is authoritative for local checks
        - Sends LocationChecks for any RAM-derived checks missing from server checked state
        """
        read_size = 1
        shard_addr = self._native_addr("shard_bitfield_native")
        if shard_addr is None:
            read_size = 4
            shard_addr = self._transport_addr("shard_bitfield")
        if shard_addr is None:
            return
        raw = (await bizhawk.read(ctx.bizhawk_ctx, [(shard_addr, read_size, "System Bus")]))[0]
        shard_bits = self._u32_le(raw.ljust(4, b"\x00"))

        # Track only mapped bits so reserved bits do not pollute checked state.
        mapped_bits = sorted(self._location_ids_by_bit.keys())

        mapped_checked_locations: set[int] = set()
        for bit in mapped_bits:
            if (shard_bits >> bit) & 1:
                self._checked_location_bits.add(bit)
                mapped_checked_locations.update(self._location_ids_by_bit.get(bit, []))

        # Reconnect-safe behavior: if server state is missing RAM-derived checks,
        # resend them until the server acknowledges and reflects them.
        missing_on_server = sorted(mapped_checked_locations - ctx.checked_locations)

        if missing_on_server:
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": missing_on_server}])

    async def _poll_boss_defeat_locations(self, ctx: KirbyAmBizHawkClientContext) -> None:
        """
        Read boss_defeat_flags transport bitfield and map set bits to boss-defeat locations.

        This mirrors shard polling semantics: RAM-derived checks are resent until the
        server acknowledges them in ctx.checked_locations.
        """
        boss_addr = data.transport_ram_addresses.get("boss_defeat_flags")
        if boss_addr is None:
            return

        raw = (await bizhawk.read(ctx.bizhawk_ctx, [(boss_addr, 4, "System Bus")]))[0]
        boss_bits = self._u32_le(raw)

        mapped_checked_locations: set[int] = set()
        for bit in sorted(self._boss_location_ids_by_bit.keys()):
            if (boss_bits >> bit) & 1:
                mapped_checked_locations.update(self._boss_location_ids_by_bit.get(bit, []))

        missing_on_server = sorted(mapped_checked_locations - ctx.checked_locations)
        if missing_on_server:
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": missing_on_server}])

    async def _probe_boss_defeat_candidates(self, ctx: KirbyAmBizHawkClientContext) -> None:
        """
        Probe native candidate boss table bytes and log rising-edge bit transitions.

        This is intentionally observational: it does not send AP location checks yet.
        The logs are meant to support live BizHawk address verification for Issue #110.
        """
        base_addr = self._native_addr("boss_mirror_table_native")
        if base_addr is None:
            return

        # Re-baseline on BizHawk reconnect by tracking the stream object identity.
        stream_marker = id(getattr(ctx.bizhawk_ctx, "streams", None))
        if self._boss_probe_stream_marker is None:
            self._boss_probe_stream_marker = stream_marker
        elif stream_marker != self._boss_probe_stream_marker:
            self._boss_probe_stream_marker = stream_marker
            self._last_boss_probe_snapshot = None

        raw = (await bizhawk.read(
            ctx.bizhawk_ctx,
            [(base_addr, _BOSS_MIRROR_TABLE_PROBE_BYTES, "System Bus")],
        ))[0]

        if self._last_boss_probe_snapshot is None:
            self._last_boss_probe_snapshot = raw
            return

        old = self._last_boss_probe_snapshot
        self._last_boss_probe_snapshot = raw

        # Pad to equal width defensively if emulator returned an unexpected size.
        width = max(len(old), len(raw))
        old = old.ljust(width, b"\x00")
        raw = raw.ljust(width, b"\x00")

        rising_edges: list[str] = []
        for byte_index in range(width):
            prev_byte = old[byte_index]
            new_byte = raw[byte_index]
            rising_mask = (~prev_byte & 0xFF) & new_byte
            if rising_mask == 0:
                continue

            for bit in range(8):
                if (rising_mask >> bit) & 1:
                    absolute_addr = base_addr + byte_index
                    rising_edges.append(f"0x{absolute_addr:08X}[bit{bit}]")

        if rising_edges:
            from CommonClient import logger

            logger.info(
                "KirbyAM boss candidate probe detected rising bits: %s",
                ", ".join(rising_edges),
            )

    # --------------------------
    # Item delivery (mailbox protocol)
    # --------------------------

    async def _deliver_items(self, ctx: KirbyAmBizHawkClientContext) -> None:
        """
        Deliver items via mailbox protocol.
        
        Protocol:
        1. Client writes item_id + player to mailbox
        2. Client sets flag=1 to signal ROM
        3. ROM reads mailbox, applies item, clears flag=0 (ACK)
        4. Client observes flag=0, advances index
        
        State machine:
        - If _delivery_pending: wait for ROM to ACK (flag -> 0)
        - If flag=0 and items available: write next item (set flag -> 1)
        - Otherwise: wait
        """
        flag_addr = self._transport_addr("incoming_item_flag")
        counter_addr = self._transport_addr("debug_item_counter")
        id_addr = self._transport_addr("incoming_item_id")
        player_addr = self._transport_addr("incoming_item_player")
        if flag_addr is None or id_addr is None or player_addr is None:
            return

        from CommonClient import logger

        frame_addr = self._transport_addr("frame_counter")
        reads: list[tuple[int, int, str]] = [(flag_addr, 4, "System Bus")]
        if counter_addr is not None:
            reads.append((counter_addr, 4, "System Bus"))
        if frame_addr is not None:
            reads.append((frame_addr, 4, "System Bus"))
        raw_values = await bizhawk.read(ctx.bizhawk_ctx, reads)

        flag = self._u32_le(raw_values[0])
        next_read_index = 1
        rom_received_count: Optional[int] = None
        if counter_addr is not None and len(raw_values) > next_read_index:
            rom_received_count = self._u32_le(raw_values[next_read_index])
            next_read_index += 1
        current_frame: Optional[int] = None
        if frame_addr is not None and len(raw_values) > next_read_index:
            current_frame = self._u32_le(raw_values[next_read_index])

        # Auto-resync delivery cursor if ROM item state moved backward (save-loss)
        # or forward (reconnect after stale client state).
        if rom_received_count is not None:
            if rom_received_count > len(ctx.items_received):
                if self._delivered_item_index != len(ctx.items_received):
                    self._delivered_item_index = len(ctx.items_received)
                    await self._persist_u32(ctx, "delivered_item_index", self._delivered_item_index)
                self._delivery_pending = False
                self._delivery_pending_frame = None
                return
            if rom_received_count < self._delivered_item_index:
                logger.info(
                    "KirbyAM: ROM item counter regressed from %s to %s; rewinding delivery cursor",
                    self._delivered_item_index,
                    rom_received_count,
                )
                self._delivered_item_index = rom_received_count
                self._delivery_pending = False
                self._delivery_pending_frame = None
                await self._persist_u32(ctx, "delivered_item_index", self._delivered_item_index)
            elif rom_received_count > self._delivered_item_index and rom_received_count <= len(ctx.items_received):
                logger.info(
                    "KirbyAM: ROM item counter advanced from %s to %s; fast-forwarding delivery cursor",
                    self._delivered_item_index,
                    rom_received_count,
                )
                self._delivered_item_index = rom_received_count
                self._delivery_pending = False
                self._delivery_pending_frame = None
                await self._persist_u32(ctx, "delivered_item_index", self._delivered_item_index)
                if flag != 0:
                    logger.warning(
                        "KirbyAM: Clearing stale mailbox flag after fast-forward to item index %s",
                        self._delivered_item_index,
                    )
                    await bizhawk.write(ctx.bizhawk_ctx, [
                        (flag_addr, (0).to_bytes(4, "little"), "System Bus"),
                    ])

        # If an item is pending, wait for ROM to clear the flag (ACK)
        if self._delivery_pending:
            if flag == 0:
                logger.info("KirbyAM: Mailbox ACK observed at item index %s", self._delivered_item_index)
                self._delivery_pending = False
                self._delivery_pending_frame = None
                if rom_received_count is not None and rom_received_count <= len(ctx.items_received):
                    self._delivered_item_index = rom_received_count
                else:
                    self._delivered_item_index += 1
                await self._persist_u32(ctx, "delivered_item_index", self._delivered_item_index)
                return

            if current_frame is not None and self._delivery_pending_frame is not None:
                elapsed_frames = (current_frame - self._delivery_pending_frame) & 0xFFFFFFFF
                if elapsed_frames >= _MAILBOX_ACK_TIMEOUT_FRAMES:
                    logger.warning(
                        "KirbyAM: Mailbox ACK timeout after %s frames at item index %s; clearing flag and retrying",
                        elapsed_frames,
                        self._delivered_item_index,
                    )
                    await bizhawk.write(ctx.bizhawk_ctx, [
                        (flag_addr, (0).to_bytes(4, "little"), "System Bus"),
                    ])
                    self._delivery_pending = False
                    self._delivery_pending_frame = None
            return

        # No pending item; mailbox must be empty to write
        if flag != 0:
            return

        # Nothing to deliver
        if self._delivered_item_index >= len(ctx.items_received):
            return

        while self._delivered_item_index < len(ctx.items_received):
            itm = ctx.items_received[self._delivered_item_index]
            item_fields = self._extract_delivery_item_fields(itm)
            if item_fields is None:
                logger.warning(
                    "KirbyAM: Skipping malformed ReceivedItems entry at index %s: %r",
                    self._delivered_item_index,
                    itm,
                )
                self._delivered_item_index += 1
                self._delivery_pending = False
                await self._persist_u32(ctx, "delivered_item_index", self._delivered_item_index)
                continue

            item_id, player_id = item_fields

            logger.info(
                "KirbyAM: Writing mailbox item index %s (item=%s, player=%s)",
                self._delivered_item_index,
                item_id,
                player_id,
            )
            await bizhawk.write(ctx.bizhawk_ctx, [
                (id_addr, item_id.to_bytes(4, "little"), "System Bus"),
                (player_addr, player_id.to_bytes(4, "little"), "System Bus"),
                (flag_addr, (1).to_bytes(4, "little"), "System Bus"),
            ])
            self._delivery_pending = True
            self._delivery_pending_frame = current_frame
            return

    # --------------------------
    # Goal completion condition
    # --------------------------

    async def _native_goal_signal_active(self, ctx: KirbyAmBizHawkClientContext, slot_goal: int) -> bool:
        """Return whether native goal signal is active for the selected goal mode."""
        ai_state_addr = self._native_addr("ai_kirby_state_native")
        if ai_state_addr is None:
            return False

        raw = (await bizhawk.read(ctx.bizhawk_ctx, [(ai_state_addr, _AI_STATE_ADDR_WIDTH, "System Bus")]))[0]
        ai_state = self._u32_le(raw)

        if slot_goal == Goal.option_dark_mind:
            # Dark Mind clear is anchored to 9999. The 10000 state is post-clear progression
            # and should not be used as the first-clear trigger for this goal mode.
            return ai_state == _GOAL_STATE_DARK_MIND_CLEAR

        if slot_goal == Goal.option_100:
            return ai_state == _GOAL_STATE_FULL_CLEAR

        return False

    async def _maybe_report_goal(self, ctx: KirbyAmBizHawkClientContext) -> None:
        """
        Goal reporting from native signal polling.

        Behavior:
        - Reports selected goal location when the corresponding native signal is active.
        - Sends CLIENT_GOAL once server acknowledges the selected goal location.
        - Falls back to no-op when native addresses are unavailable.
        """
        if self._goal_reported:
            return

        if not self._all_location_ids_sorted:
            return

        slot_goal_raw = ctx.slot_data.get("goal", Goal.option_dark_mind)
        try:
            slot_goal = int(slot_goal_raw)
        except (TypeError, ValueError):
            slot_goal = Goal.option_dark_mind

        goal_location_id = self._goal_location_ids_by_option.get(slot_goal)
        if goal_location_id is None:
            return

        if not self._native_goal_signal_seen:
            self._native_goal_signal_seen = await self._native_goal_signal_active(ctx, slot_goal)

        if not self._native_goal_signal_seen:
            return

        if goal_location_id not in ctx.checked_locations:
            locations_checked = getattr(ctx, "locations_checked", None)
            if not isinstance(locations_checked, set):
                locations_checked = None

            # Prefer reconnect-safe tracking when available.
            if locations_checked is not None:
                if goal_location_id in locations_checked:
                    return
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [goal_location_id]}])
                locations_checked.add(goal_location_id)
            else:
                if not self._goal_location_reported:
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [goal_location_id]}])
                    self._goal_location_reported = True
            return

        if goal_location_id in ctx.checked_locations:
            from NetUtils import ClientStatus
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            self._goal_reported = True
