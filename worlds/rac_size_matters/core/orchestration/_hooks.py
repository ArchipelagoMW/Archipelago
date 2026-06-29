from __future__ import annotations

import asyncio

from CommonClient import logger

from ...constants import Rac5Locations, Rac5CutsceneLocations
from ...locations import (
    GADGET_INTERNAL_TO_LOCATION,
    MOD_INTERNAL_TO_LOCATION,
    WEAPON_INTERNAL_TO_LOCATION,
)
from ..armour import ARMOUR_FLAG_TO_LOCATION, ArmourPiece
from ..planets import PlanetState
from ..player import PlayerMovementState
from ..titanium_bolts import BOLT_BY_PLANET_AND_DELTA


class HooksMixin:
    """Wires state callbacks to game events."""

    def _wire_hooks(self) -> None:
        self._wire_player_hooks()
        self._wire_bolt_hooks()
        self._wire_skill_point_hooks()
        self._wire_armour_set_hooks()
        self._wire_challenge_hooks()
        self._wire_mission_hooks()
        self._wire_menu_hooks()
        self._wire_planet_hooks()
        self._wire_bonus_weapon_hooks()

    # Player

    def _wire_player_hooks(self) -> None:
        def on_death(cause: PlayerMovementState) -> None:
            self.armour.freeze_slots()
            self.armour.clear_all_memory()
            self.armour.apply_world_armour()
            if not self._death_link_enabled():
                return
            self._death_count += 1
            amnesty = self._death_amnesty()
            if self._death_count > amnesty:
                logger.info(f"[RAC] Death {self._death_count} ({cause.name}): above amnesty.")
                self._send_deathlink(int(cause))
            else:
                logger.info(f"[RAC] Death {self._death_count} ({cause.name}): within amnesty.")

        def on_respawn() -> None:
            self._death_count = 0
            # _reapply_inv() already OR-merges AP-owned armour sets into memory
            # (client._apply_player_inventory_sync's ARMOUR_ADDRESSES write).
            # apply_ap_armour() used to run right after it and zero those same
            # set bytes straight back out — self.ap_armour is only ever
            # populated through sync_from_ap's armour_item_pickups param,
            # which no call site passes, so it's permanently empty. Don't call
            # it here; restore_equipped_slots() below still needs to run to
            # put the equipped-slot bytes back.
            self._reapply_inv()
            self.armour.restore_equipped_slots()

        def on_pickup_start() -> None:
            if self.vendor_active:
                return
            self._pickup_detection_active = True
            ps = self.planet_states.get(self._active_planet_id)
            if ps:
                ps.on_pickup_start()

        def on_pickup_end() -> None:
            if self.vendor_active:
                return
            ps = self.planet_states.get(self._active_planet_id)
            if ps:
                asyncio.create_task(_delayed_pickup_end(ps))

        async def _delayed_pickup_end(ps: PlanetState) -> None:
            await asyncio.sleep(0.3)
            ps.on_pickup_end()                    # scan memory, detect new pieces, fire location hooks
            self._pickup_detection_active = False # unblock AP inventory writes now that detection is done
            self.armour.clear_all_memory()        # zero before writing AP state
            await asyncio.sleep(0.2)
            self._reapply_inv()                   # write AP armour set bitmasks
            self.armour.restore_equipped_slots()  # restore slot bytes last, after all bitmask writes

        self.player.on_death        = on_death
        self.player.on_respawn      = on_respawn
        self.player.on_pickup_start = on_pickup_start
        self.player.on_pickup_end   = on_pickup_end

    # Collectibles

    def _wire_bolt_hooks(self) -> None:
        def on_bolt_delta(delta: int) -> None:
            name = BOLT_BY_PLANET_AND_DELTA.get((self._active_planet_id, delta))
            if name:
                self._log(f"[RAC] Titanium bolt collected: {name}")
                self._send_location(name)
            else:
                logger.warning(f"[RAC] Unknown bolt delta {delta} on {self._active_planet_id:#04x}")

        self.bolts.on_bolt_delta = on_bolt_delta

    def _wire_skill_point_hooks(self) -> None:
        def on_skill_point_earned(name: str) -> None:
            self._log(f"[RAC] Skill point earned: {name}")
            self._send_location(name)

        self.skill_points.on_skill_point_earned = on_skill_point_earned

    def _wire_armour_set_hooks(self) -> None:
        def on_armour_set_collected(name: str) -> None:
            self._log(f"[RAC] Armour set collected: {name}")
            self._send_location(name)

        self.armour_sets.on_location_check = on_armour_set_collected

    def _wire_challenge_hooks(self) -> None:
        self.clank.set_location_check_callback(
            lambda name: (self._log(f"[RAC] Clank challenge completed: {name}"),
                          self._send_location(name))
        )
        self.skyboard.set_location_check_callback(
            lambda name: (self._log(f"[RAC] Skyboard race completed: {name}"),
                          self._send_location(name))
        )

    # Missions

    # Missions that coincide with a gadget pickup: fire both the gadget
    # location and the mission location when complete.
    _MISSION_GADGET_LOCATION: dict[str, str] = {
        Rac5CutsceneLocations.RYLLUS_BUZZING: Rac5Locations.RYLLUS_SPROUT,
        Rac5CutsceneLocations.KALIDON_WIN:    Rac5Locations.KALIDON_SHRINK,
        # Rac5CutsceneLocations.METALIS_WAR:    Rac5Locations.METALIS_GLOVES,  # Giant Clank disabled — unreachable
    }

    def _wire_mission_hooks(self) -> None:
        def on_mission_complete(name: str) -> None:
            self._log(f"[RAC] Mission complete: {name}")
            self._send_location(name)
            gadget_loc = self._MISSION_GADGET_LOCATION.get(name)
            if gadget_loc:
                self._send_location(gadget_loc)
            if name == Rac5CutsceneLocations.QUODRONA_GOAL:
                self._on_goal()

        self.missions.set_mission_complete_callback(on_mission_complete)

    # Menus

    def _wire_menu_hooks(self) -> None:
        self.weapon_vendor.on_menu_open  = lambda: (self.quick_select.freeze(), self._on_vendor_open())
        self.weapon_vendor.on_menu_close = lambda: (self.quick_select.unfreeze(), self._on_vendor_close())
        self.mod_vendor.on_menu_open     = lambda: (self.quick_select.freeze(), self._on_vendor_open())
        self.mod_vendor.on_menu_close    = lambda: (self.quick_select.unfreeze(), self._on_vendor_close())
        self.menu.set_pause_close_callback(lambda: self._on_pause_close())

    # Planet (armour / vendor purchases)

    def _wire_planet_hooks(self) -> None:
        for planet_id, ps in self.planet_states.items():
            def make_armour_hook(pid: int):
                def on_armour_acquired(name: str, piece: ArmourPiece) -> None:
                    self.armour.add_world_armour_piece(name, piece)
                    loc = ARMOUR_FLAG_TO_LOCATION.get((name, piece))
                    if loc:
                        self._log(f"[RAC] Armour acquired on {pid:#04x}: {loc}")
                        self._send_location(loc)
                return on_armour_acquired
            ps.on_armour_acquired = make_armour_hook(planet_id)

            def make_weapon_hook(pid: int):
                def on_weapon_purchased(name: str) -> None:
                    loc = WEAPON_INTERNAL_TO_LOCATION.get(name)
                    self._log(f"[RAC] Vendor weapon purchased on {pid:#04x}: {name!r} -> loc={loc!r}")
                    if loc:
                        self._send_location(loc)
                return on_weapon_purchased
            ps.on_vendor_weapon_purchased = make_weapon_hook(planet_id)

            def make_gadget_hook(pid: int):
                def on_gadget_purchased(name: str) -> None:
                    loc = GADGET_INTERNAL_TO_LOCATION.get(name)
                    self._log(f"[RAC] Vendor gadget purchased on {pid:#04x}: {name!r} -> loc={loc!r}")
                    if loc:
                        self._send_location(loc)
                return on_gadget_purchased
            ps.on_vendor_gadget_purchased = make_gadget_hook(planet_id)

            def make_mod_hook(pid: int):
                def on_mod_purchased(weapon: str, slot: str) -> None:
                    loc = MOD_INTERNAL_TO_LOCATION.get((weapon, slot))
                    self._log(
                        f"[RAC] Vendor mod purchased on {pid:#04x}: {weapon!r}.{slot!r} -> loc={loc!r}"
                    )
                    if loc:
                        self._send_location(loc)
                return on_mod_purchased
            ps.on_vendor_mod_purchased = make_mod_hook(planet_id)

    # Bonus weapon pickup (Pokitaru starter weapons) / other intro-scripted
    # pickups that bypass the normal vendor-menu purchase path entirely.

    _BONUS_TRIGGER_WEAPONS: frozenset[str] = frozenset({
        "lacerator", "acid_bomb_glove", "concussion_gun",
    })

    # Hypershot is handed to the player as a scripted Pokitaru tutorial event,
    # not a normal gadget-vendor purchase, so its vendor location also needs
    # detecting off the raw unlocked-bit transition instead of the vendor-menu
    # redirect in PlanetState._wire_vendor_purchase_callbacks.
    _SCRIPTED_PICKUP_GADGETS: frozenset[str] = frozenset({"hypershot"})

    def _wire_bonus_weapon_hooks(self) -> None:
        prev_on_weapon_acquired = self.weapons.on_weapon_acquired

        def on_weapon_acquired(name: str) -> None:
            prev_on_weapon_acquired(name)
            if name in self._BONUS_TRIGGER_WEAPONS:
                self._on_bonus_weapon_pickup(name)

        self.weapons.on_weapon_acquired = on_weapon_acquired

        prev_on_gadget_acquired = self.weapons.on_gadget_acquired

        def on_gadget_acquired(name: str) -> None:
            prev_on_gadget_acquired(name)
            if name in self._SCRIPTED_PICKUP_GADGETS:
                self._on_scripted_gadget_pickup(name)

        self.weapons.on_gadget_acquired = on_gadget_acquired
