from __future__ import annotations

import asyncio
import time

from CommonClient import logger

from ..core import CURRENT_PLANET_ADDRESS, TextColour, colored_text, load_weapons_for_planet
from ..universal_tracker import PLANET_ID_TO_REGION
from .constants import EXPECTED_GAME_ID, POLL_INTERVAL
from .other_ratchet_games import GAME_ID_TO_OTHER_RATCHET

# Failsafe re-write cadence for mod_unlock_N bytes — these live in
# WeaponStruct's per-planet weapon array, and something (the game's own
# level-load init, most likely) can clobber them back to 0 between the
# reactive writes in _apply_player_inventory_sync. Re-asserting on a timer
# guarantees they self-correct rather than staying wrong until the next
# item-receive/planet-load event.
MOD_UNLOCK_WRITE_INTERVAL_S: float = 1.0


class PineMixin:
    async def _teardown_pine_connection(self) -> None:
        """Fully tear down a PINE connection: stop wiring (unregisters all struct-change
        hooks so none can fire against whatever's loaded next), then drop the raw socket.
        Without this, a hook registered by an earlier successful session (e.g. reapply_inv,
        which writes to self.pine unconditionally) could keep firing after rejection/loss."""
        self.pine_connected = False
        try:
            await self._wiring.stop()
        except Exception:
            pass
        try:
            self.pine.disconnect()
        except Exception:
            pass

    async def reconnect_pine(self) -> None:
        async with self._pine_lock:
            await self._teardown_pine_connection()
        await self._attempt_pine_connect(is_reconnect=True)

    def _on_wrong_game_detected(self, game_id: str) -> None:
        """Called from GameWiring's poll loop (on the event loop thread) once
        it notices PCSX2 is no longer running Size Matters. Scheduled as a
        task since the actual teardown needs to await the PINE lock."""
        asyncio.create_task(self._handle_wrong_game(game_id), name="PCSX2 wrong-game disconnect")

    async def _handle_wrong_game(self, game_id: str) -> None:
        known_game = GAME_ID_TO_OTHER_RATCHET.get(game_id)
        logger.warning(
            f"[RAC] PCSX2 is now running {known_game or game_id} — Size Matters client disconnected. "
            "Use /reconnect once R&C: Size Matters is loaded again."
        )
        async with self._pine_lock:
            await self._teardown_pine_connection()

    async def _attempt_pine_connect(self, is_reconnect: bool = False) -> None:
        # PINE calls run in-line on the event loop thread, never via
        # run_in_executor — same as RAC3's single-coroutine pcsx2_sync_task.
        # A thread-pool worker blocked inside a 5s-timeout PINE call would
        # hold _pine_lock for that whole window, freezing every other PINE
        # consumer (poll loop, vendor sync, deathlink) behind it. Calling
        # in-line means a slow PCSX2 response only stalls this one coroutine,
        # exactly like it would stall RAC3's.
        async with self._pine_lock:
            try:
                self.pine.connect()
                game_id = self.pine.get_game_id()
            except Exception:
                logger.warning("[RAC] Could not connect to PCSX2. Use /reconnect once the emulator is running.")
                await self._teardown_pine_connection()
                return

            if game_id != EXPECTED_GAME_ID:
                known_game = GAME_ID_TO_OTHER_RATCHET.get(game_id)
                if known_game:
                    logger.warning(
                        f"[RAC] Wrong game in PCSX2: detected {known_game} [{game_id}]. This client is for "
                        f"Ratchet & Clank: Size Matters [{EXPECTED_GAME_ID}]. Connection rejected."
                    )
                else:
                    logger.warning(f"[RAC] Wrong game in PCSX2: {game_id!r} (expected {EXPECTED_GAME_ID!r}). "
                                    "Connection rejected.")
                await self._teardown_pine_connection()
                return

            logger.info(
                "[RAC] Reconnected to PCSX2 - R&C: Size Matters detected."
                if is_reconnect else
                "[RAC] Connected to PCSX2 - R&C: Size Matters detected."
            )
            self.pine_connected = True
            try:
                self._read_initial_state_sync()
            except Exception as exc:
                logger.warning(
                    f"[RAC] Initial state read failed: {exc}. Use /reconnect once the game is fully loaded."
                )
                await self._teardown_pine_connection()
                return
            # Confirm the connection in-game immediately — PINE has connected, the
            # right game is loaded, and initial state read succeeded, so show this
            # now rather than after the wiring-startup steps below, which can still
            # fail transiently (e.g. a response timeout) without PINE itself having
            # actually been lost.
            self._write_notification_text(colored_text(
                "Reconnected to " if is_reconnect else "Connected to ", TextColour.YELLOW,
                "PCSX2", TextColour.WHITE,
            ))
        try:
            # GameWiring.start() does a couple of raw PINE reads before its own
            # poll loop (which serializes on this same lock) takes over — hold
            # the lock here too so those startup reads can't interleave with
            # another in-flight PINE call from a packet that arrived while
            # reconnecting (e.g. a vendor purchase or wiring sync).
            async with self._pine_lock:
                await self._wiring.start()
            # Baseline before applying so the catch-up batch of items already
            # received before this PCSX2 connection doesn't pop a notification.
            self._notification_item_index = len(self.items_received)
            await self._apply_received_items()
            await self._send_map_page(self.current_planet)
        except Exception as exc:
            logger.warning(f"[RAC] Lost PCSX2 connection while starting up: {exc}. Use /reconnect.")
            async with self._pine_lock:
                await self._teardown_pine_connection()

    async def _read_initial_state(self) -> None:
        try:
            async with self._pine_lock:
                self._read_initial_state_sync()
        except Exception as exc:
            self._log(f"[RAC] Initial state read failed: {exc}", "warning")

    def _read_initial_state_sync(self) -> None:
        self._prev_planet = self.pine.read_int8(CURRENT_PLANET_ADDRESS)
        self.current_planet = PLANET_ID_TO_REGION.get(self._prev_planet, "Galaxy")
        self._gs.weapons_ready = load_weapons_for_planet(self._prev_planet)
        self._gs.current_planet = self._prev_planet
        self._apply_player_inventory_sync()
        self._apply_world_states_sync()

    async def game_watcher(self) -> None:
        while not self.exit_event.is_set():
            await asyncio.sleep(POLL_INTERVAL)
            if not self.pine_connected:
                continue
            try:
                await self._poll_game()
            except Exception as exc:
                # Soft flag only — do NOT tear down wiring here. GameWiring's own
                # poll loop/struct-change hooks (started by _wiring.start()) are a
                # separate mechanism that detects pickups/locations; stopping them
                # on every transient blip here (e.g. a bad read during a planet
                # load) would silently kill pickup detection until a manual
                # /reconnect. A genuinely dead socket will keep failing every
                # subsequent _poll_game call too, so /reconnect remains available.
                logger.warning(f"[RAC] Lost PINE connection or poll failed: {exc}")
                self.pine_connected = False

    async def _poll_game(self) -> None:
        prev_planet = self.current_planet
        async with self._pine_lock:
            checks = self._poll_game_sync()
        if self.current_planet != prev_planet:
            await self._send_map_page(self.current_planet)
        if checks:
            await self._check_locations(checks)

    async def _send_map_page(self, planet: str) -> None:
        if self.slot is None:
            return
        team = getattr(self, "team", 0)
        await self.send_msgs([{
            "cmd": "Set",
            "key": f"rsm_current_planet_{self.slot}_{team}",
            "default": "Galaxy",
            "want_reply": False,
            "operations": [{"operation": "replace", "value": planet}],
        }])

    @property
    def _on_known_planet(self) -> bool:
        return self._prev_planet in PLANET_ID_TO_REGION

    def _poll_game_sync(self) -> list[int]:
        planet = self.pine.read_int8(CURRENT_PLANET_ADDRESS)
        if planet != self._prev_planet:
            self._prev_planet = planet
            self._gs.current_planet = planet
            self.current_planet = PLANET_ID_TO_REGION.get(planet, "Galaxy")
            load_weapons_for_planet(planet)
            # Catch the orchestrator up too — this poll can detect a planet
            # change the transition-gate sequence never tripped for (e.g. a
            # scripted area swap), and _active_planet_id staying stale there
            # breaks every per-planet guard downstream.
            self._wiring.sync_active_planet(planet)
        self._maybe_apply_mod_unlock_flags()
        return []

    def _maybe_apply_mod_unlock_flags(self) -> None:
        now = time.monotonic()
        if now - self._last_mod_unlock_write < MOD_UNLOCK_WRITE_INTERVAL_S:
            return
        self._last_mod_unlock_write = now
        # No vendor-state guard here on purpose — mod_unlock_N isn't touched by
        # apply_vendor_locations's zero-then-restore display logic, so there's
        # no race to protect against, and gating it the same way would leave
        # you stuck if you receive the qualifying item while already standing
        # at the vendor.
        if self._wiring.writes_blocked or self._wiring.is_picking_up:
            self._log(
                f"[RAC] _maybe_apply_mod_unlock_flags: blocked — "
                f"writes_blocked={self._wiring.writes_blocked}, is_picking_up={self._wiring.is_picking_up}"
            )
            return
        self._apply_mod_unlock_flags()

    def _append_location_by_name(self, name: str) -> None:
        """Single-name variant used by GameWiring hooks — dispatches async immediately."""
        checks: list[int] = []
        self._append_location(checks, name, "GameWiring")
        if checks:
            asyncio.create_task(self._check_locations(checks))

    def _append_location(self, checks: list[int], name: str, kind: str) -> None:
        loc_id = self._location_name_to_id.get(name)
        if loc_id is None:
            logger.warning(f"[RAC] {kind}: unknown location {name!r} — not in location table")
            return
        if loc_id in self._locally_checked_locations or loc_id in self.checked_locations:
            return
        server_locations = getattr(self, "server_locations", None)
        if server_locations is not None and loc_id not in server_locations:
            logger.warning(f"[RAC] {kind}: {name!r} (id={loc_id}) not in server locations"
                           " — was game generated with the current options?")
            return
        checks.append(loc_id)
        self._log(f"[RAC] {kind} checked: {name}")

    async def _check_locations(self, locations: list[int]) -> None:
        unique_locations = set(locations) - self._locally_checked_locations
        if not unique_locations:
            return
        self._locally_checked_locations.update(unique_locations)
        # Refresh the wiring's vendor-purchase cache immediately, rather than
        # waiting for the next ReceivedItems/Connected packet — apply_vendor_locations
        # and apply_mod_vendor_locations read WeaponState.vendor_locations live
        # whenever the vendor menu opens, so a check made just before opening it
        # (e.g. buying a mod, then immediately re-opening the menu) must be
        # visible right away.
        self._wiring.weapons.sync_from_ap(self._checked_location_names())
        await self.check_locations(unique_locations)

