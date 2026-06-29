from __future__ import annotations

import asyncio
import struct
import time

from ..address_maps import PLANET_MISSION_ADDRESSES, POKITARU_RYLLUS_ALT_TRIGGER
from ..address_maps.planet_map import build_combined_address_map
from ..game_orchestrator import PLANET_NAMES, POLL_INTERVAL
from ..memory import GADGETS, load_weapons_for_planet
from ..planets import Planets
from ..structs.game import (
    TRANSITION_GATE_ARRIVED,
    TRANSITION_GATE_IDLE,
    LoadingPlanetStruct,
    TransitionGateStruct,
)

_OUTPOST_OMEGA_1_ID = 0x06

# Giant Clank on Metalis is unreachable/disabled (no AP location for it — see
# locations.py). Tracked via a bit on the Challax mission address (the game
# shares that progress word between the two Giant Clank sequences); forcing it
# set on every Metalis entry stops the game from triggering the sequence.
_GIANT_CLANK_ADDR = PLANET_MISSION_ADDRESSES["Challax"]
_GIANT_CLANK_MASK = 0x0010


class PlanetLifecycleMixin:
    """Planet enter/exit, address-map swaps, initial load, and transition handling."""

    # Transition gate (0x1EDDAD4)
    # Authoritative source for when writes must stop/resume. Rests at
    # TRANSITION_GATE_IDLE; any change away from idle means a transition has
    # started (block writes now). TRANSITION_GATE_ARRIVED tells us the planet
    # ID at LoadingPlanetStruct (0x1EDDAE4, right beside the gate) is now
    # valid, so we can swap the address map (a local bookkeeping change, not
    # a memory write). Returning to idle means the transition is fully
    # settled — only then do we run the actual write cascade
    # (_finish_planet_enter).

    def _debug_print_transition_gate(self) -> None:
        """Print the gate and loading-planet values once a second, for debugging."""
        now = time.monotonic()
        if now - self._last_gate_debug < 1.0:
            return
        self._last_gate_debug = now
        try:
            gate_raw = self._orchestrator.accessor.read_raw(TransitionGateStruct.BASE_ADDRESS, 4)
            gate_val = int.from_bytes(gate_raw, "little") if gate_raw else 0
        except Exception:
            gate_val = -1
        try:
            planet_raw = self._orchestrator.accessor.read_raw(LoadingPlanetStruct.BASE_ADDRESS, 4)
            planet_val = int.from_bytes(planet_raw, "little") if planet_raw else 0
        except Exception:
            planet_val = -1
        self._log(f"[RAC] Transition debug: gate={gate_val:#010x} loading_planet={planet_val:#010x}")

    def _register_transition_gate(self) -> None:
        self._orchestrator.accessor.on_struct_change(
            TransitionGateStruct, self._on_transition_gate_change
        )

    def _on_transition_gate_change(self, address: int, new_bytes: bytes) -> None:
        del address
        if len(new_bytes) < 4:
            return
        value = struct.unpack_from("<I", new_bytes)[0]
        prev = self._gate_value
        self._gate_value = value
        if value == prev:
            return

        left_idle    = prev == TRANSITION_GATE_IDLE and value != TRANSITION_GATE_IDLE
        back_to_idle = prev != TRANSITION_GATE_IDLE and value == TRANSITION_GATE_IDLE

        if left_idle:
            self._log(f"[RAC] Transition gate left idle ({prev:#010x} -> {value:#010x}) — blocking writes.")
            exiting_id = self._active_planet_id
            if exiting_id in self.planet_states:
                self.planet_states[exiting_id].planet_exit()

        if value == TRANSITION_GATE_ARRIVED:
            try:
                raw = self._orchestrator.accessor.read_raw(LoadingPlanetStruct.BASE_ADDRESS, 4)
                planet_id = raw[0] if raw else 0
            except Exception:
                planet_id = 0
            if planet_id in self.planet_states:
                self._gate_pending_planet_id = planet_id
                self._log(
                    f"[RAC] Transition gate arrived — landed on "
                    f"{PLANET_NAMES.get(planet_id, hex(planet_id))}."
                )

        if back_to_idle:
            pid = self._gate_pending_planet_id
            self._gate_pending_planet_id = 0
            if pid in self.planet_states:
                self._log(
                    f"[RAC] Transition gate settled back to idle — resuming on "
                    f"{PLANET_NAMES.get(pid, hex(pid))}."
                )
                self.planet_states[pid].planet_enter()

    def _on_planet_enter(self, planet_id: int) -> None:
        # Checked against planet_states, not PLANET_NAMES — Outpost Omega 1
        # (0x06) is deliberately absent from the Planets class (it's not a
        # travelable map entry) but does have a planet_states entry, so
        # gating on PLANET_NAMES here would silently drop its transitions.
        if planet_id not in self.planet_states:
            return
        self._transitioning         = False
        self._active_planet_id      = planet_id
        if self._swap_task:
            self._swap_task.cancel()
        self._swap_task = asyncio.create_task(self._finish_planet_enter(planet_id))

    def sync_active_planet(self, planet_id: int) -> None:
        """Catch-up path for planet changes that don't go through the normal
        transition-gate sequence (e.g. a scripted area swap like Outpost
        Omega 1 -> Outpost Omega 2, which doesn't trip the gate the way a
        loading-zone transition does). The client's own CURRENT_PLANET_ADDRESS
        poll calls this on every detected change; it's a no-op if the
        orchestrator already caught the transition via the gate."""
        if planet_id == self._active_planet_id:
            return
        self._log(
            f"[RAC] sync_active_planet: out-of-band planet change to "
            f"{PLANET_NAMES.get(planet_id, hex(planet_id))} — catching up."
        )
        self._on_planet_enter(planet_id)

    async def _finish_planet_enter(self, planet_id: int) -> None:
        # The transition gate has already settled back to idle by the time
        # planet_enter() fires, so it's safe to write immediately — no more
        # artificial settle delay.
        self.clank.write_unlocks()
        self.skyboard.write_defaults()
        self.skin.apply(self._orchestrator.accessor)
        load_weapons_for_planet(planet_id)
        self._on_initial_planet_load(planet_id)
        if planet_id == Planets.METALIS.planet_id:
            self._suppress_giant_clank()
        # Outpost Omega 1 now goes through the same continuous _reapply_inv()
        # path as every other planet — client._rebuild_player_inventory's
        # current_planet == _OUTPOST_OMEGA_1_PLANET_ID override is the only
        # extra condition needed to force-grant the Shrink Ray there.
        if self._initial_load_done:
            self._reapply_inv()
        # See on_respawn in _hooks.py — apply_ap_armour() would zero the
        # armour-set bytes _reapply_inv() just OR-merged AP ownership into
        # (self.ap_armour is permanently empty, nothing ever populates it).
        # restore_equipped_slots() still needs to run for the equipped-slot
        # bytes.
        self.armour.restore_equipped_slots()
        await self._swap_to_planet(planet_id)

    def _suppress_giant_clank(self) -> None:
        """Force the Giant Clank trigger bit set so the game treats it as
        already done and never starts the (unreachable) sequence."""
        try:
            raw = self._orchestrator.accessor.read_raw(_GIANT_CLANK_ADDR, 2)
            if not raw or len(raw) < 2:
                return
            value = struct.unpack_from("<H", raw)[0]
            if not value & _GIANT_CLANK_MASK:
                self._orchestrator.accessor.write_raw(
                    _GIANT_CLANK_ADDR, struct.pack("<H", value | _GIANT_CLANK_MASK)
                )
        except Exception as exc:
            self._log(f"[RAC] _suppress_giant_clank failed: {exc}")

    def _force_shrink_ray(self) -> None:
        """Force-unlock the Shrinkray on Outpost Omega 1 without reapplying
        the rest of the AP weapon/gadget inventory."""
        try:
            shrink_ray = GADGETS.get("shrink_ray")
            if shrink_ray is not None:
                self._orchestrator.accessor.write_raw(shrink_ray.unlocked, bytes([0x01]))
        except Exception as exc:
            self._log(f"[RAC] _force_shrink_ray failed: {exc}")

    def _on_planet_exit(self, planet_id: int) -> None:
        if self._active_planet_id == planet_id:
            self._active_planet_id = 0
        self._transitioning         = True
        self.armour.sync_slots()
        self.quick_select.freeze()
        if self._swap_task:
            self._swap_task.cancel()
            self._swap_task = None
        self._orchestrator.swap_interface(self._pine_iface, self._global_map)
        self._log(
            f"[RAC] Address map reverted to global on exit from "
            f"{PLANET_NAMES.get(planet_id, hex(planet_id))}."
        )

    async def _swap_to_planet(self, planet_id: int) -> None:
        combined = build_combined_address_map(planet_id, self._global_map)
        self._orchestrator.swap_interface(self._pine_iface, combined)
        self._log(f"[RAC] Address map swapped for {PLANET_NAMES.get(planet_id, hex(planet_id))}.")
        await asyncio.sleep(2.0)
        if not self._first_swap_done:
            self._first_swap_done = True
            self.quick_select.zero()
        else:
            # Write the snapshot BEFORE enabling polling so the poller's first
            # read after unfreeze sees our values, not the game's defaults.
            self.quick_select.restore()
            self.quick_select.unfreeze()

    def _on_initial_planet_load(self, planet_id: int) -> None:
        if self._initial_load_done:
            return
        if planet_id not in PLANET_NAMES:
            return
        self._initial_load_done = True
        self._log(f"[RAC] Initial load on {PLANET_NAMES[planet_id]} — applying world state.")
        # RAC3 gospel: this is the "main_menu True -> False" edge — the one
        # moment it tells the server CLIENT_PLAYING and replays the player's
        # full item/location history. _on_initial_load fires that here.
        self._on_initial_load()
        self.clank.write_defaults()
        self.quick_select.zero()
        if planet_id == Planets.POKITARU.planet_id:
            asyncio.create_task(self._monitor_ryllus_cutscene())
        self.missions.preset_missions()
        self.bolts.sync()
        self.skill_points.sync()
        self.armour_sets.sync()
        # See on_respawn in _hooks.py — no apply_ap_armour() call here either,
        # same reason. _finish_planet_enter (the only caller of this method)
        # runs restore_equipped_slots() right after this returns.
        self._reapply_inv()

    async def _monitor_ryllus_cutscene(self) -> None:
        await asyncio.sleep(1.0)
        last = int.from_bytes(
            self._orchestrator.accessor.read_raw(POKITARU_RYLLUS_ALT_TRIGGER, 4), "little"
        )
        while True:
            await asyncio.sleep(POLL_INTERVAL)
            current = int.from_bytes(
                self._orchestrator.accessor.read_raw(POKITARU_RYLLUS_ALT_TRIGGER, 4), "little"
            )
            if last == 0x00 and current != 0x00:
                self.planet_unlock.on_ryllus_cutscene_ended()
                self.planet_unlock.sync()
                return
            last = current
