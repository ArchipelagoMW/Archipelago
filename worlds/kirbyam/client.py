import logging
import time
from struct import unpack_from
from typing import TYPE_CHECKING, Optional

import Utils
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

from .data import LocationCategory, data
from .kirby_ap_payload.thumb_branch import is_thumb_bl_instruction
from .options import Goal
from .types import KirbyAmBizHawkClientContext

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
    from worlds.generic.shared_utils import NetworkItem


EXPECTED_ROM_HEADER_TITLE = "agb kirby am"
EXPECTED_ROM_GAME_CODE = "b8ke"
EXPECTED_ROM_MAKER_CODE = "01"
_AUTH_TOKEN_SIZE = 16
_BOSS_MIRROR_TABLE_PROBE_BYTES = 32
_AI_STATE_ADDR_WIDTH = 4
_GOAL_STATE_DARK_MIND_CLEAR = 9999
_GOAL_STATE_FULL_CLEAR = 10000
_MAILBOX_ACK_TIMEOUT_FRAMES = 30
_MAILBOX_ACK_TIMEOUT_SECONDS = 1.0  # Fallback when frame_counter is stuck
_MAILBOX_ACK_RETRY_BACKOFF_SECONDS = 0.5
_MAIN_HOOK_OFFSET = 0x00152696
_PAYLOAD_OFFSET = 0x0015E000
_AI_STATE_CUTSCENE_THRESHOLD = 200
_AI_STATE_NORMAL = 300
_DEMO_PLAYBACK_FLAGS_ADDR_KEY = "demo_playback_flags_native"
_DEMO_PLAYBACK_ACTIVE_FLAG = 0x10
_DEMO_PLAYBACK_FLAGS_WIDTH = 4
_KIRBY_HP_ADDR_KEY = "kirby_hp_native"
_KIRBY_HP_READ_WIDTH = 1
_ROOM_VISIT_FLAGS_ADDR_KEY = "room_visit_flags_native"
_ROOM_VISIT_FLAGS_ENTRY_COUNT = 0x120
_ROOM_VISIT_FLAGS_BIT_MASK = 0x8000
_OPTIONAL_UNSAFE_DELIVERY_COUNTERS = (
    ("shadow_kirby_encounters_native", "shadow_kirby_encounters"),
    ("mirra_encounters_native", "mirra_encounters"),
)
_SEND_NOTIFY_WINDOW_SECONDS = 2.0
_SEND_NOTIFY_MAX_PER_WINDOW = 5
_LOCATION_ID_TO_LABEL: dict[int, str] = {
    loc.location_id: loc.label
    for loc in data.locations.values()
    if loc.location_id is not None
}


def _normalize_gba_rom_address(value: int) -> int:
    if 0x08000000 <= value < 0x0A000000:
        return value - 0x08000000
    if 0x0A000000 <= value < 0x0C000000:
        return value - 0x0A000000
    return value


class KirbyAmClient(BizHawkClient):
    game = "Kirby & The Amazing Mirror"
    system = "GBA"
    patch_suffix = ".apkirbyam"

    def initialize_client(self) -> None:
        # Compatibility state retained for tests and reconnect diagnostics.
        self._checked_location_bits: set[int] = set()

        # Item delivery state
        self._delivered_item_index: int = 0
        self._delivery_pending: bool = False  # True after writing mailbox until ROM clears flag
        self._delivery_pending_frame: int | None = None
        self._delivery_pending_time: float | None = None  # Monotonic time recorded when mailbox write issued
        self._delivery_pending_item_index: int | None = None
        self._delivery_timeout_streak: int = 0
        self._delivery_retry_not_before: float = 0.0
        self._delivery_payload_stall_warned: bool = False
        self._last_hook_heartbeat: int | None = None
        self._hook_heartbeat_stale_ticks: int = 0
        self._delivery_counter_ahead_fallback_active: bool = False
        self._delivery_counter_ahead_resume_logged: bool = False

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
            else:
                self._non_goal_location_ids_sorted.append(loc.location_id)
        # Boss defeat bitfield → location IDs (BOSS_DEFEAT category; polled from boss_defeat_flags)
        self._boss_location_ids_by_bit: dict[int, list[int]] = {}
        for loc in data.locations.values():
            if loc.bit_index is None or loc.category != LocationCategory.BOSS_DEFEAT:
                continue
            self._boss_location_ids_by_bit.setdefault(loc.bit_index, []).append(loc.location_id)

        # Major chest bitfield → location IDs (MAJOR_CHEST category; polled from major_chest_flags)
        # Bit N corresponds to area ID N in enum AreaId (e.g. bit 3 = AREA_CABBAGE_CAVERN).
        self._major_chest_location_ids_by_bit: dict[int, list[int]] = {}
        for loc in data.locations.values():
            if loc.bit_index is None or loc.category != LocationCategory.MAJOR_CHEST:
                continue
            self._major_chest_location_ids_by_bit.setdefault(loc.bit_index, []).append(loc.location_id)

        # Vitality chest bitfield → location IDs (VITALITY_CHEST category; dedicated transport register)
        self._vitality_chest_location_ids_by_bit: dict[int, list[int]] = {}
        for loc in data.locations.values():
            if loc.bit_index is None or loc.category != LocationCategory.VITALITY_CHEST:
                continue
            self._vitality_chest_location_ids_by_bit.setdefault(loc.bit_index, []).append(loc.location_id)

        # Sound Player chest bitfield → location IDs (SOUND_PLAYER_CHEST category).
        self._sound_player_chest_location_ids_by_bit: dict[int, list[int]] = {}
        for loc in data.locations.values():
            if loc.bit_index is None or loc.category != LocationCategory.SOUND_PLAYER_CHEST:
                continue
            self._sound_player_chest_location_ids_by_bit.setdefault(loc.bit_index, []).append(loc.location_id)

        # Room-sanity bitfield index (doorsIdx) → location IDs.
        self._room_sanity_location_ids_by_bit: dict[int, list[int]] = {}
        for loc in data.locations.values():
            if loc.bit_index is None or loc.category != LocationCategory.ROOM_SANITY:
                continue
            self._room_sanity_location_ids_by_bit.setdefault(loc.bit_index, []).append(loc.location_id)
        self._room_sanity_bits_sorted: list[int] = sorted(self._room_sanity_location_ids_by_bit.keys())

        # One-time RAM state load
        self._ram_state_loaded: bool = False

        # Goal reporting
        self._goal_reported: bool = False
        self._goal_location_reported: bool = False
        self._native_goal_signal_seen: bool = False

        # Boss candidate probing state
        self._last_boss_probe_snapshot: bytes | None = None
        self._boss_probe_stream_marker: object = None

        # Runtime gameplay-state gate tracking
        self._last_runtime_gate_reason: str | None = None
        self._watcher_server_ready: bool = False
        self._watcher_requires_bizhawk_resync: bool = False
        self._last_watcher_transport_error: str | None = None

        # Poll diagnostics de-duplication (avoid per-tick log spam)
        self._last_shard_poll_log: tuple[str, tuple[int, ...], tuple[int, ...]] | None = None
        self._last_boss_poll_log: tuple[str, tuple[int, ...], tuple[int, ...]] | None = None
        self._last_major_chest_poll_log: tuple[str, tuple[int, ...], tuple[int, ...]] | None = None
        self._last_vitality_chest_poll_log: tuple[str, tuple[int, ...], tuple[int, ...]] | None = None
        self._last_sound_player_chest_poll_log: tuple[str, tuple[int, ...], tuple[int, ...]] | None = None
        self._last_room_sanity_poll_log: tuple[str, tuple[int, ...], tuple[int, ...]] | None = None

        # Notification pipeline state (Issue #83)
        self._notification_settings_loaded: bool = False
        self._receive_notifications_enabled: bool = True
        self._send_notifications_enabled: bool = True
        self._notified_receive_indices: set[int] = set()
        self._notified_send_keys: set[tuple[int, int, int, int]] = set()
        self._send_notify_window_start: float = 0.0
        self._send_notify_window_count: int = 0
        self._send_notify_window_suppressed: int = 0

        # DeathLink runtime tag synchronization state
        self._death_link_enabled: bool | None = None
        self._incoming_death_link_pending: bool = False
        self._last_incoming_death_link_time: float | None = None
        self._last_local_alive_state: bool | None = None
        self._suppress_next_local_death_send: bool = False

        # Research-first unsafe-delivery candidate probing state (Issue #223)
        self._unsafe_delivery_probe_stream_marker: object = None
        self._last_unsafe_delivery_counter_values: dict[str, int] = {}

        # Gameplay-state logging diagnostics (Issue #477)
        self._debug_gameplay_state_logging_enabled: bool = False
        self._debug_gameplay_states_seen: set[int] = set()

    @staticmethod
    def _server_session_ready(ctx: "BizHawkClientContext") -> bool:
        """Return whether AP connection and slot data are ready for watcher work."""
        server = getattr(ctx, "server", None)
        if server is None:
            return False

        socket = getattr(server, "socket", None)
        if socket is None:
            return False

        if getattr(socket, "closed", True):
            return False

        return getattr(ctx, "slot_data", None) is not None

    def _reset_reconnect_transient_state(self) -> None:
        """Reset transient watcher diagnostics/probes so reconnect starts from clean baselines."""
        self._last_runtime_gate_reason = None
        self._last_shard_poll_log = None
        self._last_boss_poll_log = None
        self._last_major_chest_poll_log = None
        self._last_vitality_chest_poll_log = None
        self._last_sound_player_chest_poll_log = None
        self._last_room_sanity_poll_log = None
        self._last_boss_probe_snapshot = None
        self._boss_probe_stream_marker = None
        self._unsafe_delivery_probe_stream_marker = None
        self._last_unsafe_delivery_counter_values = {}
        self._incoming_death_link_pending = False
        self._last_incoming_death_link_time = None
        self._last_local_alive_state = None
        self._suppress_next_local_death_send = False
        self._delivery_counter_ahead_fallback_active = False
        self._delivery_counter_ahead_resume_logged = False

    def _mark_bizhawk_watcher_transport_error(self, reason: str) -> bool:
        """Prepare handler state for a clean BizHawk-side recovery on the next successful tick."""
        self._watcher_requires_bizhawk_resync = True
        self._ram_state_loaded = False
        self._delivery_pending = False
        self._delivery_pending_frame = None
        self._delivery_pending_time = None
        self._delivery_pending_item_index = None
        self._delivery_timeout_streak = 0
        self._delivery_retry_not_before = 0.0
        self._delivery_payload_stall_warned = False
        self._last_hook_heartbeat = None
        self._hook_heartbeat_stale_ticks = 0

        if self._last_watcher_transport_error == reason:
            return False

        self._last_watcher_transport_error = reason
        return True

    @staticmethod
    def _coerce_bool(value: object, default: bool) -> bool:
        if isinstance(value, bool):
            return value
        if isinstance(value, int):
            if value in {0, 1}:
                return bool(value)
            return default
        if isinstance(value, str):
            lowered = value.strip().lower()
            if lowered in {"1", "true", "yes", "on"}:
                return True
            if lowered in {"0", "false", "no", "off"}:
                return False
        return default

    def _load_notification_settings(self, ctx: "BizHawkClientContext") -> None:
        if self._notification_settings_loaded:
            return

        slot_data = getattr(ctx, "slot_data", None)
        if isinstance(slot_data, dict):
            self._receive_notifications_enabled = self._coerce_bool(
                slot_data.get("enable_receive_notifications", True),
                True,
            )
            self._send_notifications_enabled = self._coerce_bool(
                slot_data.get("enable_send_notifications", True),
                True,
            )

        self._notification_settings_loaded = True

    def _load_debug_settings(self, ctx: "BizHawkClientContext") -> None:
        slot_data = getattr(ctx, "slot_data", None)
        if isinstance(slot_data, dict):
            debug_config = slot_data.get("debug", {})
            if isinstance(debug_config, dict):
                self._debug_gameplay_state_logging_enabled = self._coerce_bool(
                    debug_config.get("gameplay_state_logging", False),
                    False,
                )

    @staticmethod
    def _player_name(ctx: "BizHawkClientContext", player_id: int) -> str:
        if player_id == 0:
            return "Archipelago"
        player_names = getattr(ctx, "player_names", None)
        if isinstance(player_names, dict):
            value = player_names.get(player_id)
            if isinstance(value, str) and value:
                return value
        return f"Player {player_id}"

    @staticmethod
    def _item_name(ctx: "BizHawkClientContext", item_id: int, item_player: int) -> str:
        lookup = getattr(ctx, "item_names", None)
        if lookup is not None:
            try:
                resolved = lookup.lookup_in_slot(item_id, item_player)
                if (
                    isinstance(resolved, str)
                    and resolved
                    and not resolved.startswith("Unknown item (ID:")
                ):
                    return resolved
            except Exception:
                pass
        # Fallback: try direct lookup from KirbyAM data
        item_data = data.items.get(item_id)
        if item_data is not None:
            return item_data.label
        return f"Item {item_id}"

    @staticmethod
    def _location_name(location_id: Optional[int]) -> str:
        """Get location display name from AP location ID (address)."""
        if location_id is None:
            return ""
        label = _LOCATION_ID_TO_LABEL.get(location_id)
        return label if label is not None else f"Location {location_id}"

    async def _emit_receive_notification(self, ctx: "BizHawkClientContext", delivered_index: int) -> None:
        # ACK-gated + index-deduped to avoid replay spam during reconnect
        # rewind/fast-forward reconciliation.
        if not self._receive_notifications_enabled:
            return
        if delivered_index in self._notified_receive_indices:
            return
        if delivered_index < 0 or delivered_index >= len(ctx.items_received):
            return

        item = ctx.items_received[delivered_index]
        item_fields = self._extract_delivery_item_fields(item)
        if item_fields is None:
            return

        self._notified_receive_indices.add(delivered_index)
        item_id, player_id = item_fields
        receiver_slot = self._coerce_u32(getattr(ctx, "slot", None))
        lookup_slot = receiver_slot if receiver_slot is not None else player_id
        item_name = self._item_name(ctx, item_id, lookup_slot)
        sender_name = self._player_name(ctx, player_id)
        message = f"Received {item_name} from {sender_name}"

        from CommonClient import logger

        logger.info(
            "KirbyAM: receive notification queued (index=%s, item=%s, sender=%s, lookup_slot=%s)",
            delivered_index,
            item_name,
            sender_name,
            lookup_slot,
        )
        try:
            await bizhawk.display_message(ctx.bizhawk_ctx, message)
        except Exception:
            logger.warning(
                "KirbyAM: failed to emit receive notification (index=%s)",
                delivered_index,
            )

    def _maybe_emit_send_notification(self, ctx: "BizHawkClientContext", args: dict) -> None:
        if not self._send_notifications_enabled:
            return
        if args.get("type") != "ItemSend":
            return

        item = args.get("item")
        if item is None:
            return

        item_id = self._coerce_u32(getattr(item, "item", None))
        sender_id = self._coerce_u32(getattr(item, "player", None))
        receiver_id = self._coerce_u32(args.get("receiving"))
        location_id = self._coerce_u32(getattr(item, "location", None))
        if item_id is None or sender_id is None or receiver_id is None:
            return
        if sender_id != getattr(ctx, "slot", None):
            return

        send_key = (item_id, sender_id, receiver_id, location_id if location_id is not None else 0xFFFFFFFF)
        if send_key in self._notified_send_keys:
            return
        self._notified_send_keys.add(send_key)

        # ItemSend packets should resolve item names in the receiving slot context.
        item_name = self._item_name(ctx, item_id, receiver_id)
        sender_name = self._player_name(ctx, sender_id)
        receiver_name = self._player_name(ctx, receiver_id)
        location_name = self._location_name(location_id)

        # Build message with location context if available
        if location_name:
            message = f"You sent {item_name} to {receiver_name} at {location_name}"
        else:
            message = f"You sent {item_name} to {receiver_name}"

        from CommonClient import logger

        now = time.monotonic()
        if self._send_notify_window_start == 0.0:
            self._send_notify_window_start = now

        elapsed = now - self._send_notify_window_start
        if elapsed >= _SEND_NOTIFY_WINDOW_SECONDS:
            if self._send_notify_window_suppressed > 0:
                suppressed_count = self._send_notify_window_suppressed
                summary = f"Skipped {suppressed_count} send popup(s) to reduce spam"
                logger.info(
                    "KirbyAM: send notification burst suppression summary (suppressed=%s)",
                    suppressed_count,
                )
                Utils.async_start(bizhawk.display_message(ctx.bizhawk_ctx, summary))
            self._send_notify_window_start = now
            self._send_notify_window_count = 0
            self._send_notify_window_suppressed = 0

        if self._send_notify_window_count >= _SEND_NOTIFY_MAX_PER_WINDOW:
            self._send_notify_window_suppressed += 1
            logger.debug(
                "KirbyAM: send notification suppressed by rate limit (item=%s, sender=%s, receiver=%s)",
                item_name,
                sender_name,
                receiver_name,
            )
            return

        self._send_notify_window_count += 1

        logger.info(
            "KirbyAM: send notification queued (item=%s, sender=%s, receiver=%s, location=%s)",
            item_name,
            sender_name,
            receiver_name,
            location_name,
        )
        Utils.async_start(bizhawk.display_message(ctx.bizhawk_ctx, message))

    async def _display_client_message(self, ctx: "BizHawkClientContext", message: str) -> None:
        """Best-effort popup helper for player-facing messages."""
        from CommonClient import logger

        try:
            await bizhawk.display_message(ctx.bizhawk_ctx, message)
        except Exception:
            logger.warning(
                "KirbyAM: failed to display client popup (message=%r)",
                message,
                exc_info=True,
            )

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        """Validate ROM is Kirby & The Amazing Mirror and initialize client."""
        from CommonClient import logger
        from .rom import KirbyAmProcedurePatch

        async def _fail(reason: str, popup_message: str | None = None) -> bool:
            if popup_message is not None and getattr(self, "_last_validation_failure_reason", None) != reason:
                await self._display_client_message(ctx, popup_message)
            self._last_validation_failure_reason = reason
            return False

        auth_addr = data.rom_addresses.get("gArchipelagoInfo")
        if auth_addr is None:
            logger.error("KirbyAM: missing rom address 'gArchipelagoInfo' in worlds/kirbyam/data/addresses.json")
            return await _fail("missing_auth_address", "Unable to load ROM: patch metadata address is missing.")
        auth_addr = _normalize_gba_rom_address(auth_addr)

        rom_hash = getattr(ctx, "rom_hash", None)
        if isinstance(rom_hash, str) and rom_hash.lower() == KirbyAmProcedurePatch.hash.lower():
            logger.error(
                "You appear to be running an unpatched Kirby & The Amazing Mirror ROM. "
                "Generate a patch file and use it to create a patched ROM before opening the BizHawk client."
            )
            return await _fail(
                "unpatched_base_rom",
                "Unable to load ROM: base ROM detected. Please use a patched ROM.",
            )

        try:
            title_bytes, game_code_bytes, maker_code_bytes = await bizhawk.read(
                ctx.bizhawk_ctx,
                [
                    (0xA0, 12, "ROM"),
                    (0xAC, 4, "ROM"),
                    (0xB0, 2, "ROM"),
                ],
            )
            rom_title = bytes(title_bytes).decode("ascii", errors="ignore").rstrip("\0").lower()
            game_code = bytes(game_code_bytes).decode("ascii", errors="ignore").rstrip("\0").lower()
            maker_code = bytes(maker_code_bytes).decode("ascii", errors="ignore").rstrip("\0")
            if (
                rom_title != EXPECTED_ROM_HEADER_TITLE
                or game_code != EXPECTED_ROM_GAME_CODE
                or maker_code != EXPECTED_ROM_MAKER_CODE
            ):
                logger.info(
                    "KirbyAM: ROM validation failed (title=%r, game_code=%r, maker=%r)",
                    rom_title,
                    game_code,
                    maker_code,
                )
                return await _fail(
                    "header_mismatch",
                    "Unable to load ROM: invalid Kirby and the Amazing Mirror ROM.",
                )
        except bizhawk.RequestFailedError as exc:
            logger.info("KirbyAM: ROM header read failed during validation: %s", exc)
            return await _fail("header_read_failed", "Unable to load ROM: could not read ROM header data.")
        except Exception as exc:
            logger.error("KirbyAM: unexpected error during ROM header validation", exc_info=exc)
            return await _fail("header_validation_exception", "Unable to load ROM: ROM header validation failed.")

        try:
            auth_raw = (await bizhawk.read(ctx.bizhawk_ctx, [(auth_addr, _AUTH_TOKEN_SIZE, "ROM")]))[0]
        except bizhawk.RequestFailedError as exc:
            logger.info("KirbyAM: ROM auth read failed during validation: %s", exc)
            return await _fail("auth_read_failed", "Unable to load ROM: could not read patch metadata.")
        except Exception as exc:
            logger.error("KirbyAM: unexpected error during ROM auth validation", exc_info=exc)
            return await _fail(
                "auth_validation_exception",
                "Unable to load ROM: patch metadata validation failed.",
            )

        if not any(auth_raw):
            if getattr(self, "_last_validation_failure_reason", None) != "missing_patch_metadata":
                logger.error(
                    "KirbyAM patch metadata was missing from the loaded ROM. "
                    "Regenerate the patch and recreate the patched ROM before opening the BizHawk client."
                )
            return await _fail(
                "missing_patch_metadata",
                "Unable to load ROM: missing patch metadata. Rebuild your patched ROM.",
            )

        # Diagnostics: verify the loaded ROM has a patched Thumb BL at the main hook site.
        try:
            hook_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(_MAIN_HOOK_OFFSET, 4, "ROM")]))[0]
            if not is_thumb_bl_instruction(bytes(hook_bytes)):
                logger.warning(
                    "KirbyAM: main hook callsite at 0x%06X is not patched with a Thumb BL "
                    "(found=%s). Loaded ROM may be incompatible with this payload build.",
                    _MAIN_HOOK_OFFSET,
                    bytes(hook_bytes).hex(" "),
                )
        except Exception as exc:
            logger.info("KirbyAM: main hook opcode probe failed during validation: %s", exc)

        self._last_validation_failure_reason = None

        # Minimal AP settings
        ctx.game = self.game
        ctx.items_handling = 0b001
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125

        self.initialize_client()
        logger.info("KirbyAM: ROM validated.")
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
        auth_addr = _normalize_gba_rom_address(auth_addr)

        auth_raw = (await bizhawk.read(ctx.bizhawk_ctx, [(auth_addr, _AUTH_TOKEN_SIZE, "ROM")]))[0]
        ctx.auth = base64.b64encode(auth_raw).decode("utf-8")

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        """Main watcher loop: polls locations, delivers items, reports goal."""
        from CommonClient import logger

        # Only run when connected and slot_data is ready
        if not self._server_session_ready(ctx):
            self._watcher_server_ready = False
            self._watcher_requires_bizhawk_resync = False
            self._last_watcher_transport_error = None
            self._death_link_enabled = None
            self._incoming_death_link_pending = False
            self._last_incoming_death_link_time = None
            self._last_local_alive_state = None
            self._suppress_next_local_death_send = False
            return

        self._load_notification_settings(ctx)
        self._load_debug_settings(ctx)
        await self._sync_death_link_setting(ctx)

        if not self._watcher_server_ready:
            logger.info("KirbyAM: AP session ready; reconnect-safe reconciliation active")
            self._watcher_server_ready = True
            self._reset_reconnect_transient_state()

        try:
            if self._watcher_requires_bizhawk_resync:
                self._reset_reconnect_transient_state()
                self._watcher_requires_bizhawk_resync = False

            # Load persisted state from RAM once per session (after bizhawk_ctx is valid)
            if not self._ram_state_loaded:
                await self._load_persistent_state(ctx)
                self._ram_state_loaded = True

            gameplay_active, defer_reason, ai_state = await self._runtime_gameplay_state(ctx)
            if self._debug_gameplay_state_logging_enabled and ai_state is not None:
                if ai_state not in self._debug_gameplay_states_seen:
                    self._debug_gameplay_states_seen.add(ai_state)
                    logger.info(
                        "KirbyAM debug: observed unique gameplay state (ai_state=%s, gameplay_active=%s, reason=%s)",
                        ai_state,
                        gameplay_active,
                        defer_reason,
                    )
            if not gameplay_active:
                if self._last_runtime_gate_reason != defer_reason:
                    logger.info(
                        "KirbyAM: deferring location polling/new item writes (%s, ai_state=%s)",
                        defer_reason,
                        ai_state if ai_state is not None else "unavailable",
                    )
                    await self._display_client_message(ctx, "Item sending paused by game state")
                    self._last_runtime_gate_reason = defer_reason

                # Preserve mailbox ACK handling while deferring new writes.
                await self._deliver_items(ctx, allow_new_writes=False)
                # Goal detection remains active because native goal signals may only
                # be observable in post-clear non-gameplay phases.
                await self._maybe_report_goal(ctx, ai_state_override=ai_state)
                self._last_watcher_transport_error = None
                return

            if self._last_runtime_gate_reason is not None:
                logger.info("KirbyAM: gameplay-active state restored; resuming normal watcher flow")
                await self._display_client_message(ctx, "Item sending resumed")
                self._last_runtime_gate_reason = None

            await self._apply_pending_death_link(ctx)
            await self._poll_and_send_local_death_link(ctx)

            # Boss defeat location polling via transport register
            await self._poll_boss_defeat_locations(ctx)

            # Major chest location polling via dedicated major_chest_flags transport register
            await self._poll_major_chest_locations(ctx)

            # Vitality chest location polling via dedicated vitality_chest_flags transport register
            await self._poll_vitality_chest_locations(ctx)

            # Sound Player chest location polling via dedicated sound_player_chest_flags register
            await self._poll_sound_player_chest_locations(ctx)

            # Room-sanity location polling via native gVisitedDoors bit 15.
            await self._poll_room_sanity_locations(ctx)

            # Candidate discovery for non-shard boss defeat signals.
            await self._probe_boss_defeat_candidates(ctx)

            # Research-first observational probes for in-game unsafe delivery windows.
            await self._probe_unsafe_delivery_candidates(ctx)

            # Item delivery (mailbox protocol)
            await self._deliver_items(ctx)

            # Goal reporting
            await self._maybe_report_goal(ctx, ai_state_override=ai_state)
            self._last_watcher_transport_error = None
        except bizhawk.RequestFailedError as exc:
            reason = exc.args[0] if exc.args else "request_failed"
            if self._mark_bizhawk_watcher_transport_error(reason):
                logger.info(
                    "KirbyAM: BizHawk request failed during watcher tick; waiting for reconnect (%s)",
                    reason,
                )
            return
        except bizhawk.NotConnectedError:
            if self._mark_bizhawk_watcher_transport_error("not_connected"):
                logger.info("KirbyAM: BizHawk disconnected during watcher tick; waiting for reconnect")
            return

    async def _sync_death_link_setting(self, ctx: "BizHawkClientContext") -> None:
        """Mirror slot_data death_link into AP DeathLink tag state with de-dupe."""
        from CommonClient import logger

        slot_data = getattr(ctx, "slot_data", None)
        enabled = False
        if isinstance(slot_data, dict):
            enabled = self._coerce_bool(slot_data.get("death_link", False), False)

        if self._death_link_enabled is enabled:
            return

        await ctx.update_death_link(enabled)
        self._death_link_enabled = enabled
        if not enabled:
            self._incoming_death_link_pending = False
            self._last_incoming_death_link_time = None
            self._last_local_alive_state = None
            self._suppress_next_local_death_send = False
        logger.info("KirbyAM: DeathLink %s", "enabled" if enabled else "disabled")

    @staticmethod
    def _s8(value: bytes) -> int:
        if not value:
            return 0
        return int.from_bytes(value[:1], "little", signed=True)

    def _queue_incoming_death_link(self, args: dict) -> None:
        """Queue an incoming DeathLink event for safe application during gameplay-active ticks."""
        if self._death_link_enabled is not True:
            return

        tags = args.get("tags")
        if not isinstance(tags, (list, tuple, set)) or "DeathLink" not in tags:
            return

        payload = args.get("data")
        if not isinstance(payload, dict):
            return

        event_time_raw = payload.get("time")
        event_time: float | None = None
        if isinstance(event_time_raw, (int, float)):
            event_time = float(event_time_raw)
        elif isinstance(event_time_raw, str):
            try:
                event_time = float(event_time_raw)
            except ValueError:
                event_time = None

        if (
            event_time is not None
            and self._last_incoming_death_link_time is not None
            and event_time <= self._last_incoming_death_link_time
        ):
            return

        if event_time is not None:
            self._last_incoming_death_link_time = event_time
        self._incoming_death_link_pending = True

    async def _apply_pending_death_link(self, ctx: "BizHawkClientContext") -> None:
        """Apply queued DeathLink by zeroing Kirby HP once gameplay is active."""
        if self._death_link_enabled is not True or not self._incoming_death_link_pending:
            return

        hp_addr = self._native_addr(_KIRBY_HP_ADDR_KEY)
        if hp_addr is None:
            return

        current_hp_raw = (await bizhawk.read(ctx.bizhawk_ctx, [(hp_addr, _KIRBY_HP_READ_WIDTH, "System Bus")]))[0]
        current_hp = self._s8(current_hp_raw)
        if current_hp <= 0:
            self._incoming_death_link_pending = False
            self._last_local_alive_state = False
            return

        from CommonClient import logger

        await bizhawk.write(ctx.bizhawk_ctx, [(hp_addr, (0).to_bytes(1, "little"), "System Bus")])
        self._incoming_death_link_pending = False
        self._suppress_next_local_death_send = True
        logger.info("KirbyAM: applied incoming DeathLink (hp_addr=0x%08X)", hp_addr)

    async def _poll_and_send_local_death_link(self, ctx: "BizHawkClientContext") -> None:
        """Send DeathLink once per alive->dead transition, with loop suppression for received links."""
        if self._death_link_enabled is not True:
            return

        hp_addr = self._native_addr(_KIRBY_HP_ADDR_KEY)
        if hp_addr is None:
            return

        hp_raw = (await bizhawk.read(ctx.bizhawk_ctx, [(hp_addr, _KIRBY_HP_READ_WIDTH, "System Bus")]))[0]
        hp_value = self._s8(hp_raw)
        alive_now = hp_value > 0

        if self._last_local_alive_state is None:
            self._last_local_alive_state = alive_now
            return

        if self._last_local_alive_state and not alive_now:
            if self._suppress_next_local_death_send:
                self._suppress_next_local_death_send = False
            else:
                await ctx.send_death("Kirby was defeated.")

        self._last_local_alive_state = alive_now

    async def _runtime_gameplay_state(self, ctx: KirbyAmBizHawkClientContext) -> tuple[bool, str, int | None]:
        """
        Classify whether gameplay-active polling/delivery is safe for this frame.

        Contract update for Issue #419:
        - known non-gameplay states remain deferred (tutorial/menu, cutscene, goal-clear states)
        - unknown post-300 states fail open to avoid blocking mailbox item delivery
        - fail open when native address is unavailable

        Issue #477 narrowing:
        - title-screen demo playback can also report AI state 300; treat demo playback as non-gameplay
        """
        ai_state_addr = self._native_addr("ai_kirby_state_native")
        if ai_state_addr is None:
            return True, "gate_signal_unavailable", None

        demo_flags_addr = self._native_addr(_DEMO_PLAYBACK_FLAGS_ADDR_KEY)
        reads: list[tuple[int, int, str]] = [(ai_state_addr, _AI_STATE_ADDR_WIDTH, "System Bus")]
        if demo_flags_addr is not None:
            reads.append((demo_flags_addr, _DEMO_PLAYBACK_FLAGS_WIDTH, "System Bus"))

        raw_values = await bizhawk.read(ctx.bizhawk_ctx, reads)
        ai_state = self._u32_le(raw_values[0])

        if ai_state < _AI_STATE_CUTSCENE_THRESHOLD:
            return False, "non_gameplay_tutorial_or_menu", ai_state
        if ai_state < _AI_STATE_NORMAL:
            return False, "non_gameplay_cutscene", ai_state
        if ai_state == _AI_STATE_NORMAL:
            demo_playback_active = False
            if demo_flags_addr is not None and len(raw_values) > 1:
                demo_flags = self._u32_le(raw_values[1])
                demo_playback_active = bool(demo_flags & _DEMO_PLAYBACK_ACTIVE_FLAG)
            if demo_playback_active:
                return False, "non_gameplay_title_demo", ai_state
        if ai_state in (_GOAL_STATE_DARK_MIND_CLEAR, _GOAL_STATE_FULL_CLEAR):
            return False, "non_gameplay_goal_clear", ai_state
        return True, "gameplay_active", ai_state

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

    async def _poll_locations(self, _ctx: KirbyAmBizHawkClientContext) -> None:
        """Mirror shard bits are progression state only; they no longer emit AP location checks."""
        return

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
        already_acknowledged = sorted(mapped_checked_locations & ctx.checked_locations)
        if missing_on_server:
            from CommonClient import logger

            boss_log_state = ("resend", tuple(missing_on_server), tuple(already_acknowledged))
            if boss_log_state != self._last_boss_poll_log:
                logger.info(
                    "KirbyAM: resending boss-defeat LocationChecks missing on server (missing=%s, acked=%s)",
                    missing_on_server,
                    already_acknowledged,
                )
                self._last_boss_poll_log = boss_log_state

            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": missing_on_server}])
        elif mapped_checked_locations:
            from CommonClient import logger

            boss_log_state = ("dedupe", tuple(), tuple(already_acknowledged))
            if boss_log_state != self._last_boss_poll_log:
                logger.debug(
                    "KirbyAM: dedupe suppressed boss-defeat LocationChecks (all RAM-derived checks already acknowledged: %s)",
                    already_acknowledged,
                )
                self._last_boss_poll_log = boss_log_state
        else:
            self._last_boss_poll_log = None

    async def _poll_major_chest_locations(self, ctx: KirbyAmBizHawkClientContext) -> None:
        """
        Read transport major_chest_flags and map set bits to major-chest locations.

        Bit N corresponds to area ID N (enum AreaId): bit 3 = AREA_CABBAGE_CAVERN,
        bit 6 = AREA_OLIVE_OCEAN, bit 7 = AREA_PEPPERMINT_PALACE, etc.
        Multiple physical chest rooms in one area map to the same area-ID bit.

        Mirrors shard/boss polling semantics: RAM-derived checks are resent until
        the server acknowledges them in ctx.checked_locations.

        Source: transport major_chest_flags written by the ROM payload's big chest hook.
        Native gTreasures.bigChestField still reflects in-game map ownership and is no
        longer used as the AP check signal.
        """
        chest_addr = self._transport_addr("major_chest_flags")
        if chest_addr is None:
            return

        raw = (await bizhawk.read(ctx.bizhawk_ctx, [(chest_addr, 4, "System Bus")]))[0]
        chest_bits = self._u32_le(raw)

        mapped_checked_locations: set[int] = set()
        for bit in sorted(self._major_chest_location_ids_by_bit.keys()):
            if (chest_bits >> bit) & 1:
                mapped_checked_locations.update(self._major_chest_location_ids_by_bit.get(bit, []))

        missing_on_server = sorted(mapped_checked_locations - ctx.checked_locations)
        already_acknowledged = sorted(mapped_checked_locations & ctx.checked_locations)
        if missing_on_server:
            from CommonClient import logger

            chest_log_state = ("resend", tuple(missing_on_server), tuple(already_acknowledged))
            if chest_log_state != self._last_major_chest_poll_log:
                logger.info(
                    "KirbyAM: resending major-chest LocationChecks missing on server (missing=%s, acked=%s)",
                    missing_on_server,
                    already_acknowledged,
                )
                self._last_major_chest_poll_log = chest_log_state

            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": missing_on_server}])
        elif mapped_checked_locations:
            from CommonClient import logger

            chest_log_state = ("dedupe", tuple(), tuple(already_acknowledged))
            if chest_log_state != self._last_major_chest_poll_log:
                logger.debug(
                    "KirbyAM: dedupe suppressed major-chest LocationChecks (all RAM-derived checks already acknowledged: %s)",
                    already_acknowledged,
                )
                self._last_major_chest_poll_log = chest_log_state
        else:
            self._last_major_chest_poll_log = None

    async def _poll_vitality_chest_locations(self, ctx: KirbyAmBizHawkClientContext) -> None:
        """
        Read transport vitality_chest_flags and map set bits to vitality-chest locations.

        This register is written by the ROM payload's vitality chest hook, keyed by
        room ID (not area ID). Mirrors shard/boss/major polling semantics: resend
        RAM-derived checks until the server acknowledges them in ctx.checked_locations.
        """
        chest_addr = self._transport_addr("vitality_chest_flags")
        if chest_addr is None:
            return

        raw = (await bizhawk.read(ctx.bizhawk_ctx, [(chest_addr, 4, "System Bus")]))[0]
        chest_bits = self._u32_le(raw)

        mapped_checked_locations: set[int] = set()
        for bit in sorted(self._vitality_chest_location_ids_by_bit.keys()):
            if (chest_bits >> bit) & 1:
                mapped_checked_locations.update(self._vitality_chest_location_ids_by_bit.get(bit, []))

        missing_on_server = sorted(mapped_checked_locations - ctx.checked_locations)
        already_acknowledged = sorted(mapped_checked_locations & ctx.checked_locations)
        if missing_on_server:
            from CommonClient import logger

            chest_log_state = ("resend", tuple(missing_on_server), tuple(already_acknowledged))
            if chest_log_state != self._last_vitality_chest_poll_log:
                logger.info(
                    "KirbyAM: resending vitality-chest LocationChecks missing on server (missing=%s, acked=%s)",
                    missing_on_server,
                    already_acknowledged,
                )
                self._last_vitality_chest_poll_log = chest_log_state

            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": missing_on_server}])
        elif mapped_checked_locations:
            from CommonClient import logger

            chest_log_state = ("dedupe", tuple(), tuple(already_acknowledged))
            if chest_log_state != self._last_vitality_chest_poll_log:
                logger.debug(
                    "KirbyAM: dedupe suppressed vitality-chest LocationChecks (all RAM-derived checks already acknowledged: %s)",
                    already_acknowledged,
                )
                self._last_vitality_chest_poll_log = chest_log_state
        else:
            self._last_vitality_chest_poll_log = None

    async def _poll_sound_player_chest_locations(self, ctx: KirbyAmBizHawkClientContext) -> None:
        """
        Read transport sound_player_chest_flags and map set bits to Sound Player chest locations.

        This register is written by the ROM payload's Sound Player chest hook and mirrors
        the same resend/dedupe semantics used by boss, major, and vitality polling.
        """
        chest_addr = self._transport_addr("sound_player_chest_flags")
        if chest_addr is None:
            return

        raw = (await bizhawk.read(ctx.bizhawk_ctx, [(chest_addr, 4, "System Bus")]))[0]
        chest_bits = self._u32_le(raw)

        mapped_checked_locations: set[int] = set()
        for bit in sorted(self._sound_player_chest_location_ids_by_bit.keys()):
            if (chest_bits >> bit) & 1:
                mapped_checked_locations.update(self._sound_player_chest_location_ids_by_bit.get(bit, []))

        missing_on_server = sorted(mapped_checked_locations - ctx.checked_locations)
        already_acknowledged = sorted(mapped_checked_locations & ctx.checked_locations)
        if missing_on_server:
            from CommonClient import logger

            chest_log_state = ("resend", tuple(missing_on_server), tuple(already_acknowledged))
            if chest_log_state != self._last_sound_player_chest_poll_log:
                logger.info(
                    "KirbyAM: resending sound-player-chest LocationChecks missing on server (missing=%s, acked=%s)",
                    missing_on_server,
                    already_acknowledged,
                )
                self._last_sound_player_chest_poll_log = chest_log_state

            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": missing_on_server}])
        elif mapped_checked_locations:
            from CommonClient import logger

            chest_log_state = ("dedupe", tuple(), tuple(already_acknowledged))
            if chest_log_state != self._last_sound_player_chest_poll_log:
                logger.debug(
                    "KirbyAM: dedupe suppressed sound-player-chest LocationChecks (all RAM-derived checks already acknowledged: %s)",
                    already_acknowledged,
                )
                self._last_sound_player_chest_poll_log = chest_log_state
        else:
            self._last_sound_player_chest_poll_log = None

    async def _poll_room_sanity_locations(self, ctx: KirbyAmBizHawkClientContext) -> None:
        """
        Read native gVisitedDoors[doorsIdx] entries and map visit bit (bit 15) to room-sanity locations.

        The room-sanity location bit_index field stores the native doorsIdx value.
        Polling is level-based and reconnect-safe: checks are resent until the server
        acknowledges them in ctx.checked_locations.
        """
        slot_data = getattr(ctx, "slot_data", None)
        if not isinstance(slot_data, dict):
            return
        if not self._coerce_bool(slot_data.get("room_sanity", False), False):
            return

        if not self._room_sanity_location_ids_by_bit:
            return

        room_visit_addr = self._native_addr(_ROOM_VISIT_FLAGS_ADDR_KEY)
        if room_visit_addr is None:
            return

        read_width = _ROOM_VISIT_FLAGS_ENTRY_COUNT * 2
        raw = (await bizhawk.read(ctx.bizhawk_ctx, [(room_visit_addr, read_width, "System Bus")]))[0]

        if len(raw) != read_width:
            from CommonClient import logger

            logger.warning(
                "KirbyAM: room-sanity poll expected %s bytes from gVisitedDoors, got %s; skipping tick",
                read_width,
                len(raw),
            )
            return

        raw_view = memoryview(raw)

        mapped_checked_locations: set[int] = set()
        for doors_idx in self._room_sanity_bits_sorted:
            if doors_idx < 0 or doors_idx >= _ROOM_VISIT_FLAGS_ENTRY_COUNT:
                continue
            entry_value = unpack_from("<H", raw_view, doors_idx * 2)[0]
            if entry_value & _ROOM_VISIT_FLAGS_BIT_MASK:
                mapped_checked_locations.update(self._room_sanity_location_ids_by_bit.get(doors_idx, []))

        missing_on_server = sorted(mapped_checked_locations - ctx.checked_locations)
        already_acknowledged = sorted(mapped_checked_locations & ctx.checked_locations)
        if missing_on_server:
            from CommonClient import logger

            room_log_state = ("resend", tuple(missing_on_server), tuple(already_acknowledged))
            if room_log_state != self._last_room_sanity_poll_log:
                logger.info(
                    "KirbyAM: resending room-sanity LocationChecks missing on server (missing=%s, acked=%s)",
                    missing_on_server,
                    already_acknowledged,
                )
                self._last_room_sanity_poll_log = room_log_state

            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": missing_on_server}])
        elif mapped_checked_locations:
            from CommonClient import logger

            room_log_state = ("dedupe", tuple(), tuple(already_acknowledged))
            if room_log_state != self._last_room_sanity_poll_log:
                logger.debug(
                    "KirbyAM: dedupe suppressed room-sanity LocationChecks (all RAM-derived checks already acknowledged: %s)",
                    already_acknowledged,
                )
                self._last_room_sanity_poll_log = room_log_state
        else:
            self._last_room_sanity_poll_log = None

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
        # Use direct object reference (not id()) to prevent false negatives when CPython
        # reuses an integer ID for a newly allocated stream after the old one is GC'd.
        stream_marker = getattr(ctx.bizhawk_ctx, "streams", None)
        if self._boss_probe_stream_marker is None:
            self._boss_probe_stream_marker = stream_marker
        elif stream_marker is not self._boss_probe_stream_marker:
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

            logger.debug(
                "KirbyAM: boss candidate probe rising bits: %s",
                ", ".join(rising_edges),
            )

    async def _probe_unsafe_delivery_candidates(self, ctx: KirbyAmBizHawkClientContext) -> None:
        """
        Observe optional native counters relevant to Issue #223 unsafe delivery windows.

        This is research-only scaffolding. It does not block delivery and only logs
        counter changes for candidate miniboss signals when addresses are configured.
        """
        reads: list[tuple[int, int, str]] = []
        labels: list[str] = []
        for key, label in _OPTIONAL_UNSAFE_DELIVERY_COUNTERS:
            addr = self._native_addr(key)
            if addr is None:
                continue
            reads.append((addr, 4, "System Bus"))
            labels.append(label)

        if not reads:
            return

        stream_marker = getattr(ctx.bizhawk_ctx, "streams", None)
        if self._unsafe_delivery_probe_stream_marker is None:
            self._unsafe_delivery_probe_stream_marker = stream_marker
        elif stream_marker is not self._unsafe_delivery_probe_stream_marker:
            self._unsafe_delivery_probe_stream_marker = stream_marker
            self._last_unsafe_delivery_counter_values = {}

        raw_values = await bizhawk.read(ctx.bizhawk_ctx, reads)

        from CommonClient import logger

        for label, raw in zip(labels, raw_values):
            current_value = self._u32_le(raw)
            previous_value = self._last_unsafe_delivery_counter_values.get(label)
            self._last_unsafe_delivery_counter_values[label] = current_value

            if previous_value is None or current_value == previous_value:
                continue

            logger.debug(
                "KirbyAM: unsafe-delivery candidate probe: %s changed %s -> %s",
                label,
                previous_value,
                current_value,
            )

    # --------------------------
    # Item delivery (mailbox protocol)
    # --------------------------

    async def _deliver_items(self, ctx: KirbyAmBizHawkClientContext, allow_new_writes: bool = True) -> None:
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
        from CommonClient import logger

        flag_addr = self._transport_addr("incoming_item_flag")
        counter_addr = self._transport_addr("debug_item_counter")
        id_addr = self._transport_addr("incoming_item_id")
        player_addr = self._transport_addr("incoming_item_player")
        if flag_addr is None or id_addr is None or player_addr is None:
            return

        frame_addr = self._transport_addr("frame_counter")
        heartbeat_addr = self._transport_addr("hook_heartbeat")
        reads: list[tuple[int, int, str]] = [(flag_addr, 4, "System Bus")]
        if counter_addr is not None:
            reads.append((counter_addr, 4, "System Bus"))
        if frame_addr is not None:
            reads.append((frame_addr, 4, "System Bus"))
        if heartbeat_addr is not None:
            reads.append((heartbeat_addr, 4, "System Bus"))
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
            next_read_index += 1

        hook_heartbeat: Optional[int] = None
        if heartbeat_addr is not None and len(raw_values) > next_read_index:
            hook_heartbeat = self._u32_le(raw_values[next_read_index])
            if self._last_hook_heartbeat is None or hook_heartbeat != self._last_hook_heartbeat:
                self._hook_heartbeat_stale_ticks = 0
            else:
                self._hook_heartbeat_stale_ticks += 1
            self._last_hook_heartbeat = hook_heartbeat

        # Auto-resync delivery cursor if ROM item state moved backward (save-loss)
        # or forward (reconnect after stale client state).
        if rom_received_count is not None:
            if rom_received_count > len(ctx.items_received):
                if not self._delivery_counter_ahead_fallback_active:
                    logger.warning(
                        "KirbyAM: ROM delivery counter is ahead of received items (rom=%s, received=%s); "
                        "ignoring ROM counter and continuing mailbox delivery",
                        rom_received_count,
                        len(ctx.items_received),
                    )
                self._delivery_counter_ahead_fallback_active = True
            else:
                if self._delivery_counter_ahead_fallback_active:
                    logger.info(
                        "KirbyAM: ROM delivery counter is back in range (rom=%s, received=%s); "
                        "restoring normal mailbox synchronization",
                        rom_received_count,
                        len(ctx.items_received),
                    )
                self._delivery_counter_ahead_fallback_active = False
                self._delivery_counter_ahead_resume_logged = False

            if rom_received_count < self._delivered_item_index:
                logger.info(
                    "KirbyAM: ROM delivery counter moved backward from %s to %s; rewinding client delivery cursor",
                    self._delivered_item_index,
                    rom_received_count,
                )
                self._delivered_item_index = rom_received_count
                self._delivery_pending = False
                self._delivery_pending_frame = None
                self._delivery_pending_time = None
                self._delivery_pending_item_index = None
                self._delivery_timeout_streak = 0
                self._delivery_retry_not_before = 0.0
                self._delivery_payload_stall_warned = False
                await self._persist_u32(ctx, "delivered_item_index", self._delivered_item_index)
            elif rom_received_count > self._delivered_item_index and rom_received_count <= len(ctx.items_received):
                # Capture pending state before clearing — this counter advance may be the ACK signal.
                _ff_was_pending = self._delivery_pending
                _ff_pending_item_index = self._delivery_pending_item_index
                logger.info(
                    "KirbyAM: ROM delivery counter moved forward from %s to %s; fast-forwarding client delivery cursor",
                    self._delivered_item_index,
                    rom_received_count,
                )
                self._delivered_item_index = rom_received_count
                self._delivery_pending = False
                self._delivery_pending_frame = None
                self._delivery_pending_time = None
                self._delivery_pending_item_index = None
                self._delivery_timeout_streak = 0
                self._delivery_retry_not_before = 0.0
                self._delivery_payload_stall_warned = False
                self._hook_heartbeat_stale_ticks = 0
                await self._persist_u32(ctx, "delivered_item_index", self._delivered_item_index)
                if flag != 0:
                    logger.warning(
                        "KirbyAM: Clearing stale mailbox flag after fast-forward to item index %s",
                        self._delivered_item_index,
                    )
                    await bizhawk.write(ctx.bizhawk_ctx, [
                        (flag_addr, (0).to_bytes(4, "little"), "System Bus"),
                    ])
                # When the ROM counter advances while a delivery was pending and flag == 0,
                # this IS the ACK: the ROM processed our mailbox item and incremented the
                # counter in the same frame as clearing the flag.  Emit the receive
                # notification here so it is not silently dropped by the fast-forward path
                # taking precedence over the 'if self._delivery_pending' block below.
                if _ff_was_pending and flag == 0:
                    _notify_index = _ff_pending_item_index
                    if _notify_index is None:
                        _notify_index = self._delivered_item_index - 1
                    await self._emit_receive_notification(ctx, _notify_index)

        # If an item is pending, wait for ROM to clear the flag (ACK)
        if self._delivery_pending:
            if flag == 0:
                delivered_index = self._delivery_pending_item_index
                if delivered_index is None:
                    delivered_index = self._delivered_item_index
                logger.info("KirbyAM: Mailbox delivery confirmed at item index %s", delivered_index)
                self._delivery_pending = False
                self._delivery_pending_frame = None
                self._delivery_pending_time = None
                self._delivery_pending_item_index = None
                self._delivery_timeout_streak = 0
                self._delivery_retry_not_before = 0.0
                self._delivery_payload_stall_warned = False
                self._hook_heartbeat_stale_ticks = 0
                if rom_received_count is not None and rom_received_count <= len(ctx.items_received):
                    self._delivered_item_index = rom_received_count
                else:
                    self._delivered_item_index += 1
                await self._persist_u32(ctx, "delivered_item_index", self._delivered_item_index)
                await self._emit_receive_notification(ctx, delivered_index)
                return

            # Check for timeout via frame counter OR wall-clock time (fallback if frame_counter stuck)
            timeout_triggered = False
            timeout_reason = ""

            if current_frame is not None and self._delivery_pending_frame is not None:
                elapsed_frames = (current_frame - self._delivery_pending_frame) & 0xFFFFFFFF
                if elapsed_frames >= _MAILBOX_ACK_TIMEOUT_FRAMES:
                    timeout_triggered = True
                    timeout_reason = f"frame timeout ({elapsed_frames} frames >= {_MAILBOX_ACK_TIMEOUT_FRAMES})"

            frame_counter_stuck = (
                current_frame is None
                or self._delivery_pending_frame is None
                or current_frame == self._delivery_pending_frame
            )

            # Fallback: monotonic timeout only when frame counter is unavailable/stuck.
            if not timeout_triggered and frame_counter_stuck and self._delivery_pending_time is not None:
                elapsed_seconds = time.monotonic() - self._delivery_pending_time
                if elapsed_seconds >= _MAILBOX_ACK_TIMEOUT_SECONDS:
                    timeout_triggered = True
                    timeout_reason = f"time timeout ({elapsed_seconds:.1f}s >= {_MAILBOX_ACK_TIMEOUT_SECONDS}s)"

            if timeout_triggered:
                self._delivery_timeout_streak += 1
                logger.warning(
                    "KirbyAM: Mailbox ACK timeout at item index %s; clearing flag and retrying (%s)",
                    self._delivered_item_index,
                    timeout_reason,
                )
                if (
                    not self._delivery_payload_stall_warned
                    and self._delivery_timeout_streak >= 3
                    and current_frame == 0
                    and (self._delivery_pending_frame in (None, 0))
                ):
                    if hook_heartbeat is not None and self._hook_heartbeat_stale_ticks >= 3:
                        logger.warning(
                            "KirbyAM: Repeated mailbox ACK timeouts with frame_counter stuck at 0 and "
                            "hook_heartbeat not advancing (value=%s); payload hook appears inactive",
                            hook_heartbeat,
                        )
                    elif hook_heartbeat is not None:
                        logger.warning(
                            "KirbyAM: Repeated mailbox ACK timeouts with frame_counter stuck at 0 while "
                            "hook_heartbeat advances (value=%s); frame_counter slot may be unstable",
                            hook_heartbeat,
                        )
                    else:
                        logger.warning(
                            "KirbyAM: Repeated mailbox ACK timeouts with frame_counter stuck at 0; "
                            "payload hook may be inactive in the loaded ROM patch"
                        )
                    self._delivery_payload_stall_warned = True
                await bizhawk.write(ctx.bizhawk_ctx, [
                    (flag_addr, (0).to_bytes(4, "little"), "System Bus"),
                ])
                self._delivery_pending = False
                self._delivery_pending_frame = None
                self._delivery_pending_time = None
                self._delivery_pending_item_index = None
                self._delivery_retry_not_before = time.monotonic() + _MAILBOX_ACK_RETRY_BACKOFF_SECONDS
            return

        # No pending item; mailbox must be empty to write
        if flag != 0:
            return

        # Gameplay-state gate can defer new writes while still allowing ACK/recovery handling.
        if not allow_new_writes:
            return

        if self._delivery_retry_not_before > 0.0 and time.monotonic() < self._delivery_retry_not_before:
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
                self._delivery_pending_time = None
                self._delivery_pending_item_index = None
                self._delivery_timeout_streak = 0
                self._delivery_retry_not_before = 0.0
                self._delivery_payload_stall_warned = False
                await self._persist_u32(ctx, "delivered_item_index", self._delivered_item_index)
                continue

            item_id, player_id = item_fields

            if self._delivery_counter_ahead_fallback_active and not self._delivery_counter_ahead_resume_logged:
                logger.info(
                    "KirbyAM: ROM counter fallback active; continuing mailbox delivery at item index %s "
                    "(rom=%s, received=%s)",
                    self._delivered_item_index,
                    rom_received_count,
                    len(ctx.items_received),
                )
                self._delivery_counter_ahead_resume_logged = True

            if logger.isEnabledFor(logging.INFO):
                logger.info(
                    "KirbyAM: Delivering mailbox item index %s (%s from %s)",
                    self._delivered_item_index,
                    self._item_name(ctx, item_id, player_id),
                    self._player_name(ctx, player_id),
                )
            await bizhawk.write(ctx.bizhawk_ctx, [
                (id_addr, item_id.to_bytes(4, "little"), "System Bus"),
                (player_addr, player_id.to_bytes(4, "little"), "System Bus"),
                (flag_addr, (1).to_bytes(4, "little"), "System Bus"),
            ])
            self._delivery_pending = True
            self._delivery_pending_frame = current_frame
            self._delivery_pending_time = time.monotonic()  # Record monotonic time for timeout fallback
            self._delivery_pending_item_index = self._delivered_item_index
            return

    # --------------------------
    # Goal completion condition
    # --------------------------

    async def _native_goal_signal_active(
        self,
        ctx: KirbyAmBizHawkClientContext,
        slot_goal: int,
        ai_state_override: int | None = None,
    ) -> bool:
        """Return whether native goal signal is active for the selected goal mode."""
        if ai_state_override is not None:
            ai_state = ai_state_override
        else:
            ai_state_addr = self._native_addr("ai_kirby_state_native")
            if ai_state_addr is None:
                return False

            raw = (await bizhawk.read(ctx.bizhawk_ctx, [(ai_state_addr, _AI_STATE_ADDR_WIDTH, "System Bus")]))[0]
            ai_state = self._u32_le(raw)

        if slot_goal != Goal.option_dark_mind:
            return False

        # Dark Mind clear is ideally observed at 9999, but live sessions can miss that
        # transient state and only see the subsequent post-clear 10000 signal.
        return ai_state in (_GOAL_STATE_DARK_MIND_CLEAR, _GOAL_STATE_FULL_CLEAR)

    async def _maybe_report_goal(
        self,
        ctx: KirbyAmBizHawkClientContext,
        ai_state_override: int | None = None,
    ) -> None:
        """
        Goal reporting from native signal polling.

        Behavior:
        - For addressless runtime goal events, sends CLIENT_GOAL directly.
        - If a future world version exposes a numeric server goal location, sends
          LocationChecks first and CLIENT_GOAL after server acknowledgement.
        - Falls back to no-op when native addresses are unavailable.
        """
        if self._goal_reported:
            return

        if not self._all_location_ids_sorted:
            return

        slot_goal_raw = ctx.slot_data.get("goal", Goal.option_dark_mind)
        parsed_slot_goal: Optional[int] = None
        clamped_goal = False
        try:
            parsed_slot_goal = int(slot_goal_raw)
        except (TypeError, ValueError):
            clamped_goal = True

        if parsed_slot_goal == Goal.option_dark_mind:
            slot_goal = parsed_slot_goal
        else:
            slot_goal = Goal.option_dark_mind
            clamped_goal = True

        if clamped_goal:
            from CommonClient import logger
            logger.warning(
                "KirbyAM: unexpected slot goal value '%s' (parsed=%s); clamping to Dark Mind. "
                "This may indicate mismatched configs or world versions.",
                slot_goal_raw,
                parsed_slot_goal,
            )

        goal_location_id = self._goal_location_ids_by_option.get(slot_goal)
        if goal_location_id is None:
            return

        server_locations = getattr(ctx, "server_locations", None)
        goal_location_exposed_by_server = (
            isinstance(server_locations, set) and goal_location_id in server_locations
        )

        if not self._native_goal_signal_seen:
            self._native_goal_signal_seen = await self._native_goal_signal_active(
                ctx,
                slot_goal,
                ai_state_override=ai_state_override,
            )
            if self._native_goal_signal_seen:
                from CommonClient import logger
                logger.info(
                    "KirbyAM: native goal signal seen (goal_option=%s)",
                    slot_goal,
                )

        if not self._native_goal_signal_seen:
            return

        if not goal_location_exposed_by_server:
            from CommonClient import logger
            from NetUtils import ClientStatus

            finished_game = getattr(ctx, "finished_game", False)
            if not isinstance(finished_game, bool):
                finished_game = False

            if finished_game:
                self._goal_reported = True
                return

            logger.info(
                "KirbyAM: goal location is addressless in this world; sending CLIENT_GOAL directly (goal_option=%s)",
                slot_goal,
            )
            await self._display_client_message(ctx, "Goal complete")
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
            self._goal_reported = True
            return

        if goal_location_id not in ctx.checked_locations:
            locations_checked = getattr(ctx, "locations_checked", None)
            if not isinstance(locations_checked, set):
                locations_checked = None

            # Prefer reconnect-safe tracking when available.
            if locations_checked is not None:
                if goal_location_id in locations_checked:
                    return
                from CommonClient import logger
                logger.info(
                    "KirbyAM: sending goal location check (location_id=%s)",
                    goal_location_id,
                )
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [goal_location_id]}])
                locations_checked.add(goal_location_id)
            else:
                if not self._goal_location_reported:
                    from CommonClient import logger
                    logger.info(
                        "KirbyAM: sending goal location check (location_id=%s)",
                        goal_location_id,
                    )
                    await ctx.send_msgs([{"cmd": "LocationChecks", "locations": [goal_location_id]}])
                    self._goal_location_reported = True
            return

        if goal_location_id in ctx.checked_locations:
            from CommonClient import logger
            from NetUtils import ClientStatus
            logger.info("KirbyAM: goal complete; sending CLIENT_GOAL status (goal_option=%s)", slot_goal)
            await self._display_client_message(ctx, "Goal complete")
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
            self._goal_reported = True

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        if not self._notification_settings_loaded:
            self._load_notification_settings(ctx)
        if cmd == "Bounced":
            self._queue_incoming_death_link(args)
        if cmd == "PrintJSON":
            self._maybe_emit_send_notification(ctx, args)
