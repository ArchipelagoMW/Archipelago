from typing import TYPE_CHECKING, Optional

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from .data import data
from .options import Goal
from .types import KirbyAmBizHawkClientContext

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
    from worlds.generic.shared_utils import NetworkItem


EXPECTED_ROM_NAME_PREFIX = "kirby amazing mirror"  # loosen while you iterate


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
        self._location_ids_by_bit: dict[int, list[int]] = {}
        for loc in data.locations.values():
            if loc.bit_index is None:
                continue
            self._location_ids_by_bit.setdefault(loc.bit_index, []).append(loc.location_id)

        # One-time RAM state load
        self._ram_state_loaded: bool = False

        # Goal reporting
        self._goal_reported: bool = False

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

        reads: list[tuple[int, int, str]] = [(flag_addr, 4, "System Bus")]
        if counter_addr is not None:
            reads.append((counter_addr, 4, "System Bus"))
        raw_values = await bizhawk.read(ctx.bizhawk_ctx, reads)

        flag = self._u32_le(raw_values[0])
        rom_received_count: Optional[int] = None
        if counter_addr is not None and len(raw_values) > 1:
            rom_received_count = self._u32_le(raw_values[1])

        # Auto-resync delivery cursor if ROM item state moved backward (save-loss)
        # or forward (reconnect after stale client state).
        if rom_received_count is not None:
            if rom_received_count > len(ctx.items_received):
                if self._delivered_item_index != len(ctx.items_received):
                    self._delivered_item_index = len(ctx.items_received)
                    await self._persist_u32(ctx, "delivered_item_index", self._delivered_item_index)
                self._delivery_pending = False
                return
            if rom_received_count < self._delivered_item_index:
                self._delivered_item_index = rom_received_count
                self._delivery_pending = False
                await self._persist_u32(ctx, "delivered_item_index", self._delivered_item_index)
            elif rom_received_count > self._delivered_item_index and rom_received_count <= len(ctx.items_received):
                self._delivered_item_index = rom_received_count
                self._delivery_pending = False
                await self._persist_u32(ctx, "delivered_item_index", self._delivered_item_index)

        # If an item is pending, wait for ROM to clear the flag (ACK)
        if self._delivery_pending:
            if flag == 0:
                self._delivery_pending = False
                if rom_received_count is not None and rom_received_count <= len(ctx.items_received):
                    self._delivered_item_index = rom_received_count
                else:
                    self._delivered_item_index += 1
                await self._persist_u32(ctx, "delivered_item_index", self._delivered_item_index)
            return

        # No pending item; mailbox must be empty to write
        if flag != 0:
            return

        # Nothing to deliver
        if self._delivered_item_index >= len(ctx.items_received):
            return

        from CommonClient import logger

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

            # Write item and mark mailbox full
            await bizhawk.write(ctx.bizhawk_ctx, [
                (id_addr, item_id.to_bytes(4, "little"), "System Bus"),
                (player_addr, player_id.to_bytes(4, "little"), "System Bus"),
                (flag_addr, (1).to_bytes(4, "little"), "System Bus"),
            ])
            self._delivery_pending = True
            return

    # --------------------------
    # Temporary completion condition
    # --------------------------

    async def _maybe_report_goal(self, ctx: KirbyAmBizHawkClientContext) -> None:
        """
        Temporary goal reporting: mark finished when all locations are checked.
        
        Current Implementation (PLACEHOLDER):
        - Reports goal once all location IDs in data.locations checked
        
        TODO:
        - Replace with actual Dark Mind defeat signal from ROM
        - See issue #38 for final implementation
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

        if goal_location_id not in ctx.checked_locations:
            if all(loc_id in ctx.checked_locations for loc_id in self._non_goal_location_ids_sorted):
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [goal_location_id]}])
            return

        required_completion_ids = [*self._non_goal_location_ids_sorted, goal_location_id]
        if all(loc_id in ctx.checked_locations for loc_id in required_completion_ids):
            from NetUtils import ClientStatus
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            self._goal_reported = True
