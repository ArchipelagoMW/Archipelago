from __future__ import annotations

import asyncio
from collections.abc import Callable
from typing import Any

tracker_loaded: bool = False
try:
    from worlds.tracker.TrackerClient import TrackerGameContext as CommonContext
    tracker_loaded = True
except ImportError:
    from CommonClient import CommonContext
from CommonClient import logger

from ..core import (
    ARMOUR_ADDRESSES,
    BOLTS,
    PLANET_STATE_ADDRESSES,
    PLAYER_ARMOUR_SLOTS,
    SKILL_POINT_ADDRESS,
    Int64State,
    MemoryItemState,
    TextColour,
    colored_text,
)
from ..core.game_orchestrator import GameOrchestrator as GameWiring
from ..core.states.game_state import GameState
from ..locations import ALL_LOCATIONS
from ..pcsx2_interface.pine import Pine
from .command_processor import RACCommandProcessor
from .constants import EXPECTED_GAME_ID, GAME_NAME
from .deathlink import DeathLinkMixin
from .handlers import CutsceneHandlerMixin, EventsHandlerMixin
from .pine_mixin import PineMixin
from .vendor import InventoryMixin, VendorHandlerMixin


class RACContext(
    PineMixin, CutsceneHandlerMixin, EventsHandlerMixin,
    DeathLinkMixin, VendorHandlerMixin, InventoryMixin, CommonContext,
):
    game = GAME_NAME
    command_processor = RACCommandProcessor
    items_handling = 0b111
    current_planet: str = "Galaxy"
    tags = CommonContext.tags - {"Tracker"}

    def __init__(self, server_address: str | None, password: str | None) -> None:
        super().__init__(server_address, password)

        self.pine = Pine()
        self.pine_connected = False
        self._pine_lock = asyncio.Lock()
        self.slot_data: dict[str, Any] = {}

        self._location_name_to_id = {name: data.code for name, data in ALL_LOCATIONS.items()}
        self._locally_checked_locations: set[int] = set()

        self._prev_skill_points = 0
        self._prev_bolt_pickup = 0
        self._planet_state = MemoryItemState(
            PLANET_STATE_ADDRESSES,
            name="PlanetState",
            debug_log=self._log,
        )
        self._prev_planet = 0

        self._armour_pickup_state = MemoryItemState(
            ARMOUR_ADDRESSES,
            on_change=self._on_armour_pickup_update,
            name="ArmourPickupState",
            debug_log=self._log,
        )
        self._player_armour_state = MemoryItemState(
            ARMOUR_ADDRESSES,
            name="PlayerArmourState",
            debug_log=self._log,
        )
        self._player_weapon_state = MemoryItemState(
            {},
            name="PlayerWeaponState",
            debug_log=self._log,
        )
        self._player_gadget_state = MemoryItemState(
            {},
            name="PlayerGadgetState",
            debug_log=self._log,
        )
        self._armour_slot_state = MemoryItemState(
            PLAYER_ARMOUR_SLOTS,
            name="ArmourSlotState",
            debug_log=self._log,
        )
        self._titanium_bolt_state = Int64State(
            BOLTS.pickup,
            name="TitaniumBoltState",
            debug_log=self._log,
        )
        self._skill_point_state = Int64State(
            SKILL_POINT_ADDRESS,
            name="SkillPointState",
            debug_log=self._log,
        )
        self._pending_armour_pickup_locs: list[str] = []
        self._processed_item_count = 0
        self._processed_trap_count = 0
        # Whether the persisted "how many items_received have already had
        # their bolts/traps granted to the live PS2 memory" checkpoint has
        # been fetched from the AP server's data storage yet (see
        # _filler_applied_key). items_received alone can't tell us what's
        # actually been written to the game, since a fresh client process
        # always replays the entire history from index 0 — without this, a
        # client restart would either re-grant every historical bolt/trap (no
        # local counter survives the restart) or, with the old "assume a full
        # resync means everything already happened" heuristic, silently skip
        # ones that were received but never actually applied (e.g. PCSX2
        # wasn't connected yet). Granting is gated on this being True so we
        # never grant against the wrong (zero) starting point.
        self._filler_checkpoint_synced = False
        self._starting_bolts_granted = False
        self._death_count = 0
        self._weapon_array_base: int | None = None
        self._pending_item_apply = True
        self._already_hinted: set[int] = set()
        self._notification_item_index: int = 0
        self._last_mod_unlock_write: float = 0.0
        self._armour_set_checks_enabled = False
        self._gs = GameState(ipc=self.pine)

        self._death_link_enabled = False
        self._last_death_link = 0.0
        self._debug_messages = False
        self._challenge_defaults_written = False

        self._wiring = GameWiring(
            self.pine, log=self._log,
            expected_game_id=EXPECTED_GAME_ID,
            on_wrong_game=self._on_wrong_game_detected,
            pine_lock=self._pine_lock,
        )

    async def _guarded_wiring_call(self, fn: Callable[[], None]) -> None:
        """Runs a synchronous GameOrchestrator call under the PINE lock so it
        can't interleave PINE requests with game_watcher's poll loop.

        Does NOT skip when PCSX2 isn't connected — callers include pure
        in-memory bookkeeping (e.g. on_ap_connected's sync_from_ap calls,
        which never touch self.pine) that must still run before the first
        PINE connect attempt completes, since that's now triggered from the
        same "Connected" handler that calls this. A connection drop mid-call
        (for callers that do touch self.pine, e.g. reapply_inv) is still
        treated as a soft flag, not a crash, same as game_watcher's poll loop.

        Runs fn() in-line rather than via run_in_executor — same reasoning as
        PineMixin._attempt_pine_connect: a thread-pool worker stuck inside a
        slow/timing-out PINE call would hold _pine_lock for the entire 5s
        socket timeout, freezing every other PINE consumer (poll loop, vendor
        sync, deathlink) behind it for that whole window. RAC3's equivalent
        calls are all in-line on its single coroutine for the same reason.
        """
        async with self._pine_lock:
            try:
                fn()
            except Exception as exc:
                # Not a full disconnect — GameWiring's own poll loop keeps running
                # independently of pine_connected, so pickup detection isn't
                # affected by this alone. This just stops this context's own
                # planet-poll/mod-unlock writes until the next successful call.
                logger.warning(f"[RAC] PINE call failed during wiring sync: {exc}. "
                                "If syncing stops working, use /reconnect.")
                self.pine_connected = False

    def _filler_applied_key(self) -> str:
        """AP data-storage key for the persisted bolts/traps-applied checkpoint,
        scoped per team+slot so it survives client process restarts."""
        return f"racsm_filler_applied_{self.team}_{self.slot}"

    def _checked_location_names(self) -> set[str]:
        id_to_name = {v: k for k, v in self._location_name_to_id.items()}
        return {
            id_to_name[lid]
            for lid in (self.checked_locations | self._locally_checked_locations)
            if lid in id_to_name
        }

    def _log(self, msg: str, level: str = "info") -> None:
        if not self._debug_messages:
            return
        if level == "warning":
            logger.warning(msg)
        else:
            logger.info(msg)

    async def server_auth(self, password_requested: bool = False) -> None:
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect(game=self.game)

    def on_package(self, cmd: str, args: dict[str, Any]) -> None:
        super().on_package(cmd, args)

        if cmd == "Connected":
            self.slot_data = args.get("slot_data", {})
            self._already_hinted.clear()
            self._death_link_enabled = bool(self.slot_data.get("death_link", False))
            self._armour_set_checks_enabled = bool(self.slot_data.get("armour_set_checks", False))
            self._wiring.clank.set_mode(int(self.slot_data.get("clank_challenges", 1)))
            self._wiring.skyboard.set_enabled(int(self.slot_data.get("skyboard_challenges", 0)) >= 1)
            self._wiring.skill_points.set_enabled(
                int(self.slot_data.get("skill_points", 0)) >= 1
                or bool(self.slot_data.get("enable_clank_challenge_skill_points", False))
                or bool(self.slot_data.get("enable_skyboard_challenge_skill_points", False)),
                planet_loaded=self._wiring._initial_load_done,
            )
            self._wiring.skin.set_skin_by_option(int(self.slot_data.get("starting_skin", 0)))
            if self._death_link_enabled:
                asyncio.create_task(self.send_msgs([{"cmd": "ConnectUpdate", "tags": ["DeathLink"]}]))
            self._wiring.wire(
                send_location      = self._append_location_by_name,
                send_deathlink     = self._send_death_link_from_sync,
                kill_player        = self._kill_player_sync,
                reapply_inv        = self._apply_player_inventory_sync,
                death_amnesty      = lambda: int(self.slot_data.get("death_amnesty", 1)),
                death_link_enabled = lambda: self._death_link_enabled,
                on_goal            = lambda: asyncio.create_task(self._send_goal_status()),
                on_vendor_open     = lambda: asyncio.create_task(self._send_vendor_hints()),
                on_vendor_close    = self._on_menu_close_for_armour_sets,
                on_bonus_weapon_pickup = self._grant_random_bonus_item,
                on_scripted_gadget_pickup = self._handle_scripted_gadget_pickup,
                on_initial_load    = lambda: asyncio.create_task(self._send_playing_status()),
            )
            checked = self._checked_location_names()
            asyncio.create_task(self._guarded_wiring_call(
                lambda: self._wiring.on_ap_connected(self.slot_data, checked)
            ))
            self._pending_item_apply = True
            asyncio.create_task(self._apply_received_items())
            self._write_notification_text(colored_text(
                "Connected to ", TextColour.YELLOW, "Archipelago", TextColour.WHITE,
            ))
            if not self.pine_connected:
                asyncio.create_task(self._attempt_pine_connect(), name="PCSX2 PINE connect")
            else:
                # PCSX2 never dropped, so _attempt_pine_connect's own
                # _send_map_page call (which only fires on a PINE reconnect)
                # won't run here. current_planet is always kept fresh by the
                # independent PINE poll loop regardless of the AP server
                # connection, so re-push it now rather than leaving the
                # server's stored value stuck at whatever it was before this
                # AP (re)connect — it's not something to persist and trust,
                # it's something to always re-check and re-send on connect.
                asyncio.create_task(self._send_map_page(self.current_planet))
            # Fetch the persisted filler-applied checkpoint from the AP server
            # (see _filler_applied_key/_filler_checkpoint_synced). team/slot
            # are only known now that the base handler above has set them, so
            # this can't be registered any earlier than here. set_notify keeps
            # it up to date for the rest of this connection; the explicit Get
            # is needed because set_notify's own Get/SetNotify batch already
            # fired inside super().on_package() before this key existed.
            self.set_notify(self._filler_applied_key())
            asyncio.create_task(self.send_msgs([{"cmd": "Get", "keys": [self._filler_applied_key()]}]))
            return

        if cmd in ("Retrieved", "SetReply") and not self._filler_checkpoint_synced:
            key = self._filler_applied_key()
            if key in self.stored_data:
                checkpoint = min(int(self.stored_data[key] or 0), len(self.items_received))
                self._processed_item_count = checkpoint
                self._processed_trap_count = checkpoint
                self._filler_checkpoint_synced = True
                self._pending_item_apply = True
                asyncio.create_task(self._apply_received_items())
            return

        if cmd == "ReceivedItems":
            if args.get("index", 0) == 0:
                # Full resync (initial connect or reconnect). The base handler
                # just rebuilt items_received from scratch with the player's
                # entire history — none of these are newly received this
                # session, so baseline the notification index past them to
                # avoid replaying old notifications. Bolts/traps are NOT
                # baselined here — _filler_checkpoint_synced gates their
                # granting until the real server-persisted checkpoint (above)
                # arrives, instead of guessing.
                self._notification_item_index = len(self.items_received)
            checked = self._checked_location_names()
            asyncio.create_task(self._guarded_wiring_call(
                lambda: self._wiring.on_ap_received_items(checked)
            ))
            self._pending_item_apply = True
            asyncio.create_task(self._apply_received_items())
            return

        if cmd == "Bounced" and self._death_link_enabled and "DeathLink" in args.get("tags", []):
            data = args.get("data", {})
            if data.get("source") != self.auth:
                asyncio.create_task(self._receive_death_link(data))

    def on_connection_closed(self) -> None:
        super().on_connection_closed()
        self._write_notification_text(colored_text(
            "Disconnected from ", TextColour.YELLOW, "Archipelago", TextColour.WHITE,
        ))

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = "Archipelago R&C: Size Matters Client"
        return ui
