from __future__ import annotations

import asyncio
import random

from ..core import (
    ALL_TRAPS,
    ARMOUR_ADDRESSES,
    ARMOUR_FLAG_TO_LOCATION,
    AUTO_UNLOCK_ADDRESSES,
    GADGETS,
    INFOBOT_ITEM_TO_PLANET,
    INFOBOT_UNLOCK_VALUE,
    PLAYER_ARMOUR_SLOTS,
    SKILL_POINTS,
    TITANIUM_BOLTS,
    WEAPON_MAX_LEVELS,
    WEAPON_MOD_COUNTS,
    WEAPONS,
    ArmourPiece,
    SmallTextBoxAddrs,
    TextColour,
    activate_trap,
    colored_text,
)
from ..core.address_maps import BOLT_PICKUP_MASK, PLAYER_BOLT_COUNT
from ..core.memory.singletons import _ARMOUR_PIECES, _ARMOUR_SET_ORDER, _PIECE_TO_SLOTS
from ..core.vendor import MenuStateValue
from ..items import (
    ARMOUR_DISPLAY_TO_INTERNAL,
    ARMOUR_PIECE_BITMASKS,
    ARMOUR_SET_DISPLAY_TO_INTERNAL,
    GADGET_DISPLAY_TO_INTERNAL,
    PROGRESSIVE_ARMOUR_NAME,
    PROGRESSIVE_MOD_NAME,
    PROGRESSIVE_WEAPON_NAME,
    WEAPON_DISPLAY_TO_INTERNAL,
    WEAPON_MOD_NAME_TO_SLOT,
)
from ..locations import (
    GADGET_INTERNAL_TO_LOCATION,
    MOD_INTERNAL_TO_VENDOR_SLOT_LOCATION,
    VENDOR_GADGET_LOC,
    VENDOR_WEAPON_LOC,
    WEAPON_INTERNAL_TO_LOCATION,
)

_SMALL_BOX_BY_PLANET = {tb.planet_id: tb for tb in SmallTextBoxAddrs}

# Mirrors _OUTPOST_OMEGA_1_ID in core/orchestration/_planet_lifecycle.py.
_OUTPOST_OMEGA_1_PLANET_ID = 0x06

PROGRESSIVE_WEAPON_NAME_REVERSE = {v: k for k, v in PROGRESSIVE_WEAPON_NAME.items()}
PROGRESSIVE_ARMOUR_NAME_REVERSE = {v: k for k, v in PROGRESSIVE_ARMOUR_NAME.items()}
PROGRESSIVE_MOD_NAME_REVERSE = {v: k for k, v in PROGRESSIVE_MOD_NAME.items()}


# Vendor handler

class VendorHandlerMixin:
    async def _send_vendor_hints(self) -> None:
        """Send AP location hints for all currently purchasable vendor items.

        Called each time the vendor menu opens. Skips locations that have already
        been hinted or checked this session.
        """
        if self.slot is None or not self.pine_connected:
            return
        if self._wiring.weapon_vendor.active:
            vendor_type = MenuStateValue.WEAPONS_VENDOR
        elif self._wiring.mod_vendor.active:
            vendor_type = MenuStateValue.MOD_VENDOR
        else:
            vendor_type = None
        loc_names = self._wiring.vendor_unlock.purchasable_loc_names(vendor_type)
        checked   = self.checked_locations | self._locally_checked_locations
        server_locations = getattr(self, "server_locations", None)
        new_ids: list[int] = []
        for name in loc_names:
            loc_id = self._location_name_to_id.get(name)
            if loc_id is None or loc_id in self._already_hinted or loc_id in checked:
                continue
            # Not every location in the static table exists in this seed —
            # e.g. mods/armour-set/skyboard checks disabled by slot options
            # remove them from the world entirely. Don't hint a location the
            # server doesn't know about for this slot.
            if server_locations is not None and loc_id not in server_locations:
                continue
            new_ids.append(loc_id)
        if not new_ids:
            return
        await self.send_msgs([
            {"cmd": "LocationScouts", "locations": new_ids, "create_as_hint": 2}
        ])
        self._already_hinted.update(new_ids)


# Inventory

# AP location name → (internal weapon, "one"/"two"/"three") — for inventory sync
_VENDOR_MOD_LOC: dict[str, tuple[str, str]] = {
    v: k for k, v in MOD_INTERNAL_TO_VENDOR_SLOT_LOCATION.items()
}

_LOCATION_TO_ARMOUR: dict[str, tuple[str, int]] = {
    name: (set_key, int(piece))
    for (set_key, piece), name in ARMOUR_FLAG_TO_LOCATION.items()
}

_MOD_SLOT_ATTRS = ("mod_slot_one", "mod_slot_two", "mod_slot_three")


def _build_weapon_addresses() -> dict[str, int]:
    """Build key→address map for PlayerWeaponState from the currently-loaded WEAPONS."""
    addrs: dict[str, int] = {}
    for name, w in WEAPONS.items():
        addrs[name] = w.unlocked
        for i, attr in enumerate(_MOD_SLOT_ATTRS, 1):
            if i <= WEAPON_MOD_COUNTS.get(name, 0):
                addrs[f"{name}_mod_{i}"] = getattr(w, attr)
    return addrs


def _build_gadget_addresses() -> dict[str, int]:
    return {name: g.unlocked for name, g in GADGETS.items()}


class InventoryMixin:
    async def _apply_inventory_after_pickup(self) -> None:
        """Deferred inventory flush called after pickup ends.

        GameWiring's on_pickup_end reads armour from memory after a 0.3 s sleep.
        We wait 0.5 s so that detection window has closed before we write AP items,
        preventing false armour-pickup location checks.
        """
        await asyncio.sleep(0.5)
        if not self._pending_item_apply or self._wiring.is_picking_up:
            return
        async with self._pine_lock:
            self._apply_world_states_sync()
            self._apply_player_inventory_sync()
        self._pending_item_apply = False

    async def force_sync(self) -> None:
        """Force the player's in-game state to match what was received from AP,
        regardless of pickup/menu guards or what's already been applied."""
        if not self.pine_connected:
            return
        async with self._pine_lock:
            self._apply_player_inventory_sync()
            self._apply_world_states_sync()
        self._pending_item_apply = False

    async def _apply_received_items(self) -> None:
        if not self.pine_connected:
            self._pending_item_apply = True
            return
        if not self.items_received:
            return
        async with self._pine_lock:
            # Always rebuild internal inventory state (weapons/armour/gadgets)
            # so it is up-to-date even during a pickup animation.
            # _apply_player_inventory_sync guards game-memory writes internally
            # when is_picking_up is True, so only the state rebuild runs.
            self._apply_player_inventory_sync()
            # Bolts/traps don't depend on the weapon/armour pickup-detection
            # window, so apply them immediately rather than deferring behind
            # is_picking_up — otherwise a trap received mid-pickup-animation
            # sits pending indefinitely (the post-pickup retry path doesn't
            # re-check for new bolts/traps).
            if self._filler_checkpoint_synced:
                self._grant_new_bolt_items()
                self._grant_new_trap_items()
                await self._persist_filler_checkpoint()
            if self._wiring.is_picking_up:
                self._pending_item_apply = True
                return
            self._apply_world_states_sync()
        self._show_new_item_notifications()
        self._pending_item_apply = False

    async def _persist_filler_checkpoint(self) -> None:
        """Persist how far into items_received bolts/traps have been granted,
        so a client restart can resume from here instead of re-granting
        everything or losing track of what's actually been applied (see
        _filler_applied_key/_filler_checkpoint_synced in context.py).

        "max" rather than "replace" guards against this client racing a
        slightly-behind stale read of its own previous checkpoint.
        """
        checkpoint = max(self._processed_item_count, self._processed_trap_count)
        await self.send_msgs([{
            "cmd": "Set",
            "key": self._filler_applied_key(),
            "default": 0,
            "want_reply": False,
            "operations": [{"operation": "max", "value": checkpoint}],
        }])

    # Rebuild from received AP items

    def _rebuild_player_inventory(self) -> None:
        """Recompute all three player states from items_received."""
        # Reset armour and planet states
        for key in ARMOUR_ADDRESSES:
            self._player_armour_state.add(key, 0)
        for key in self._planet_state.values:
            self._planet_state.add(key, 0)

        weapon_prog_counts:     dict[str, int] = {}
        weapon_mod_prog_counts: dict[str, int] = {}
        armour_prog_counts:     dict[str, int] = {}
        weapon_unlocked:        dict[str, int] = {}
        gadget_unlocked:        dict[str, int] = {}
        weapon_mod_slots:       dict[str, set[int]] = {}  # internal_name → unlocked 1-indexed slots

        infobot_planets: set[str] = set()
        for network_item in self.items_received:
            item_name = self.item_names[self.game].get(network_item.item, "")

            if item_name in PROGRESSIVE_WEAPON_NAME_REVERSE:
                display = PROGRESSIVE_WEAPON_NAME_REVERSE[item_name]
                weapon_prog_counts[display] = weapon_prog_counts.get(display, 0) + 1
                continue
            if item_name in PROGRESSIVE_MOD_NAME_REVERSE:
                display = PROGRESSIVE_MOD_NAME_REVERSE[item_name]
                weapon_mod_prog_counts[display] = weapon_mod_prog_counts.get(display, 0) + 1
                continue
            if item_name in WEAPON_MOD_NAME_TO_SLOT:
                mod_display, slot = WEAPON_MOD_NAME_TO_SLOT[item_name]
                mod_internal = WEAPON_DISPLAY_TO_INTERNAL.get(mod_display)
                if mod_internal:
                    weapon_mod_slots.setdefault(mod_internal, set()).add(slot)
                continue
            if item_name in PROGRESSIVE_ARMOUR_NAME_REVERSE:
                display = PROGRESSIVE_ARMOUR_NAME_REVERSE[item_name]
                armour_prog_counts[display] = armour_prog_counts.get(display, 0) + 1
                continue

            if item_name in INFOBOT_ITEM_TO_PLANET:
                planet_key = INFOBOT_ITEM_TO_PLANET[item_name]
                self._planet_state.add(planet_key, INFOBOT_UNLOCK_VALUE)
                if planet_key == "outpost_omega":
                    self._planet_state.add("outpost_omega_oo2", INFOBOT_UNLOCK_VALUE)
                infobot_planets.add(planet_key.upper())
            elif item_name in WEAPON_DISPLAY_TO_INTERNAL:
                weapon_unlocked[WEAPON_DISPLAY_TO_INTERNAL[item_name]] = 1
            elif item_name in GADGET_DISPLAY_TO_INTERNAL:
                gadget_unlocked[GADGET_DISPLAY_TO_INTERNAL[item_name]] = 1
            elif item_name in ARMOUR_DISPLAY_TO_INTERNAL:
                set_key, piece = ARMOUR_DISPLAY_TO_INTERNAL[item_name]
                self._player_armour_state.add(
                    set_key,
                    self._player_armour_state.get(set_key) | int(piece),
                )

        self._wiring.planet_unlock.set_unlocked_planets(infobot_planets)

        # Progressive armour
        for display, count in armour_prog_counts.items():
            internal = ARMOUR_SET_DISPLAY_TO_INTERNAL.get(display)
            if not internal:
                continue
            bitmask = 0
            for i, bit in enumerate(ARMOUR_PIECE_BITMASKS):
                if i < count:
                    bitmask |= bit
            self._player_armour_state.add(internal, bitmask)

        # Progressive weapons: first copy unlocks, each further copy levels up
        weapon_levels: dict[str, int] = {}
        for display, count in weapon_prog_counts.items():
            internal = WEAPON_DISPLAY_TO_INTERNAL.get(display)
            if not internal:
                continue
            if count >= 1:
                weapon_unlocked[internal] = 1
            weapon_levels[internal] = min(max(0, count - 1), WEAPON_MAX_LEVELS.get(internal, 1) - 1)
        self._gs.tracked_weapon_levels = weapon_levels

        # Progressive mods: each copy unlocks the next mod slot in sequence
        for display, count in weapon_mod_prog_counts.items():
            internal = WEAPON_DISPLAY_TO_INTERNAL.get(display)
            if not internal:
                continue
            n_mods = WEAPON_MOD_COUNTS.get(internal, 0)
            weapon_mod_slots.setdefault(internal, set()).update(range(1, min(count, n_mods) + 1))

        # Populate weapon/gadget player states (updates addresses if weapons are loaded)
        if WEAPONS:
            self._player_weapon_state.update_addresses(_build_weapon_addresses())
            for name in WEAPONS:
                self._player_weapon_state.add(name, weapon_unlocked.get(name, 0))
                slots = weapon_mod_slots.get(name, set())
                for i in range(1, WEAPON_MOD_COUNTS.get(name, 0) + 1):
                    self._player_weapon_state.add(f"{name}_mod_{i}", 1 if i in slots else 0)

        if GADGETS:
            self._player_gadget_state.update_addresses(_build_gadget_addresses())
            for name in GADGETS:
                self._player_gadget_state.add(name, gadget_unlocked.get(name, 0))
            # Outpost Omega 1's facility puzzle requires the Shrink Ray regardless
            # of AP ownership. Force it on here (not via gadget_unlocked, which
            # would also mark the AP item as owned) so every re-apply of player
            # state on this planet keeps it unlocked without granting the item.
            if self._gs.current_planet == _OUTPOST_OMEGA_1_PLANET_ID and "shrink_ray" in GADGETS:
                self._player_gadget_state.add("shrink_ray", 1)

        self._sync_game_state_inventory()

    # Pickup state seed

    def _seed_armour_pickup_state(self) -> None:
        """OR already-checked armour-pickup locations into the pickup state."""
        checked = self.checked_locations | self._locally_checked_locations
        for loc_name, (set_key, piece) in _LOCATION_TO_ARMOUR.items():
            loc_id = self._location_name_to_id.get(loc_name)
            if loc_id and loc_id in checked:
                self._armour_pickup_state.add(
                    set_key,
                    self._armour_pickup_state.get(set_key) | piece,
                )

    # Game-state sync

    def _sync_game_state_inventory(self) -> None:
        self._seed_armour_pickup_state()

        self._gs.tracked_armour = {
            key: self._player_armour_state.get(key) | self._armour_pickup_state.get(key)
            for key in ARMOUR_ADDRESSES
        }

        # tracked_weapons / tracked_gadgets come from player states
        self._gs.tracked_weapons = {
            name: self._player_weapon_state.get(name) for name in WEAPONS
        }
        self._gs.tracked_gadgets = {
            name: self._player_gadget_state.get(name) for name in GADGETS
        }

        # tracked_mods: convert mod_i keys back to the "one/two/three" scheme
        # used by restore_tracked_weapon_state
        slot_names = {1: "one", 2: "two", 3: "three"}
        tracked_mods: dict[str, set[str]] = {}
        for name in WEAPONS:
            for i in range(1, WEAPON_MOD_COUNTS.get(name, 0) + 1):
                if self._player_weapon_state.get(f"{name}_mod_{i}", 0):
                    tracked_mods.setdefault(name, set()).add(slot_names[i])
        self._gs.tracked_mods = tracked_mods

        # Vendor baseline from completed vendor location checks
        checked = self.checked_locations | self._locally_checked_locations
        vendor_weapons: dict[str, int] = {}
        vendor_gadgets: dict[str, int] = {}
        vendor_mods: dict[str, set[str]] = {}
        for loc_name, internal in VENDOR_WEAPON_LOC.items():
            loc_id = self._location_name_to_id.get(loc_name)
            if loc_id and loc_id in checked:
                vendor_weapons[internal] = 1
        for loc_name, internal in VENDOR_GADGET_LOC.items():
            loc_id = self._location_name_to_id.get(loc_name)
            if loc_id and loc_id in checked:
                vendor_gadgets[internal] = 1
        for loc_name, (internal, slot) in _VENDOR_MOD_LOC.items():
            loc_id = self._location_name_to_id.get(loc_name)
            if loc_id and loc_id in checked:
                vendor_mods.setdefault(internal, set()).add(slot)
        self._gs.tracked_vendor_weapons = vendor_weapons
        self._gs.tracked_vendor_gadgets = vendor_gadgets
        self._gs.tracked_vendor_mods    = vendor_mods

    # Slot state

    def _sync_armour_slot_state(self) -> None:
        """Compute slot values from tracked_armour and store them in _armour_slot_state.

        The value written to each slot address is the 1-based set index — the slot
        address itself (chestplate/helmet/boots/…) encodes which piece it is, so the
        value only needs to identify the set (wildfire=1, sludge=2, …).
        """
        slot_vals: dict[str, int] = dict.fromkeys(PLAYER_ARMOUR_SLOTS, 0)
        for set_idx, set_name in enumerate(_ARMOUR_SET_ORDER):
            val = self._gs.tracked_armour.get(set_name, 0)
            if not val:
                continue
            slot_value = set_idx + 1
            for piece in _ARMOUR_PIECES:
                if piece in ArmourPiece(val):
                    for slot in _PIECE_TO_SLOTS[piece]:
                        slot_vals[slot] = slot_value
        for slot, v in slot_vals.items():
            self._armour_slot_state.add(slot, v)

    # Write to game memory

    def _apply_player_inventory_sync(self) -> None:
        """Rebuild from items_received, sync addresses, and write all states to memory.

        Rebuilding here ensures every call site (respawn, pickup end, planet load,
        AP item receive) always uses a fresh inventory — never stale values.
        """
        self._rebuild_player_inventory()
        if WEAPONS:
            self._player_weapon_state.update_addresses(_build_weapon_addresses())
        if GADGETS:
            self._player_gadget_state.update_addresses(_build_gadget_addresses())
        # _rebuild_player_inventory already called _sync_game_state_inventory;
        # re-run it here to pick up the freshly updated weapon/gadget addresses.
        self._sync_game_state_inventory()
        if self._wiring.is_picking_up:
            return
        # Armour/planet-state addresses are global — safe to write at any time,
        # transition or not.
        self._planet_state.give(self.pine)
        for key, addr in ARMOUR_ADDRESSES.items():
            ap_val = self._player_armour_state.get(key)
            existing = self.pine.read_int8(addr)
            self.pine.write_int8(addr, existing | ap_val)
        # Weapon/gadget addresses are per-planet (a different array per planet) —
        # only safe to write once the transition gate has settled on this planet.
        if self._wiring.writes_blocked:
            self._log("[RAC] _apply_player_inventory_sync: weapon/gadget write blocked — planet transition in progress")
            return
        # mod_unlock_N isn't part of apply_vendor_locations's zero-then-restore
        # display logic (it never touches those bytes), so unlike unlocked/
        # mod_slot_*, there's no race to guard against here — write it
        # regardless of vendor state. Gating it the same way as the weapon/
        # gadget restore below would mean receiving the qualifying item while
        # already standing at the vendor leaves you stuck until you back out.
        self._apply_mod_unlock_flags()
        # This and the orchestrator's vendor open/close zero-then-restore
        # writes both run on the event loop thread, but interleaved across
        # separate await points. Take the same lock and re-check the vendor
        # guard *inside* it — otherwise a write that passed the guard just
        # before the vendor opened can land right after, re-showing an
        # unpurchased mod.
        with self._wiring.vendor_write_lock:
            # Never write weapons or gadgets while vendor owns the weapon state.
            if self._wiring.vendor_active:
                self._log(f"[RAC] _apply_player_inventory_sync: weapon write blocked — "
                          f"vendor_active={self._wiring.vendor_active}")
                return
            unlocked = [k for k, v in self._player_weapon_state.values.items() if v and "_mod_" not in k]
            self._log(f"[RAC] _apply_player_inventory_sync: writing {len(unlocked)} AP weapons: {unlocked}")
            if WEAPONS:
                self._player_weapon_state.give(self.pine)
                for name, level in self._gs.tracked_weapon_levels.items():
                    if name in WEAPONS:
                        self.pine.write_int32(WEAPONS[name].level, level)
            if GADGETS:
                self._player_gadget_state.give(self.pine)

    # Mod-unlock flags

    def _apply_mod_unlock_flags(self) -> None:
        """Write the mod_unlock_N "purchasable" byte for every weapon mod slot
        in the game — 1 once that mod's vendor planet is AP-accessible
        (regardless of whether the player owns the parent weapon yet,
        matching VendorUnlockState.mod_vendor_unlock_weapons()), and, for
        whichever of those slots is sold on Challax, Shrink Ray + Polarizer
        too, mirroring rules/challax.py."""
        # Local import: these are populated lazily by WeaponState's
        # _ensure_loc_data() — importing at module top-level here would bind
        # to the pre-population empty dicts and never see the real values.
        from ..core.vendor import is_mod_region_accessible
        from ..core.weapons import MOD_UNLOCK_EXTRA_GADGETS, MOD_UNLOCK_PLANET
        for (weapon, attr), region in MOD_UNLOCK_PLANET.items():
            if weapon not in WEAPONS:
                self._log(
                    f"[RAC] _apply_mod_unlock_flags: {weapon!r} not in WEAPONS for "
                    f"current planet {self.current_planet!r} (WEAPONS keys={list(WEAPONS)})"
                )
                continue
            accessible = is_mod_region_accessible(self._wiring.planet_unlock, region)
            extra_gadgets = MOD_UNLOCK_EXTRA_GADGETS.get(region, ())
            gadget_state = {g: self._gs.tracked_gadgets.get(g, False) for g in extra_gadgets}
            unlocked = accessible and all(gadget_state.values())
            addr = getattr(WEAPONS[weapon], attr)
            self._log(
                f"[RAC] _apply_mod_unlock_flags: {weapon}.{attr} (sold on {region}) @ {addr:#010x} "
                f"accessible={accessible} extra_gadgets={gadget_state} -> writing {int(unlocked)}"
            )
            self.pine.write_int8(addr, 1 if unlocked else 0)

    # Bonus weapon pickup / intro-scripted vendor locations

    def _grant_random_bonus_item(self, trigger_name: str) -> None:
        """Called whenever lacerator/acid_bomb_glove/concussion_gun's unlocked
        bit transitions 0->1 in memory — both when the player picks one at
        Pokitaru's intro kiosk (a scripted event, not a normal vendor menu
        purchase — see _wire_planet_hooks/PlanetState._wire_vendor_purchase_callbacks,
        neither of which ever engage for it) and when we ourselves re-write
        that same bit while re-applying an already-AP-owned weapon.

        Only the former is a real pickup: if trigger_name is already AP-owned
        the transition can only be our own write, so skip both the bonus
        grant (this used to fire on every re-apply, not just the real pick)
        and the location check below.
        """
        if not self.pine_connected or self._wiring.writes_blocked:
            return
        if self._gs.tracked_weapons.get(trigger_name):
            return
        loc = WEAPON_INTERNAL_TO_LOCATION.get(trigger_name)
        if loc:
            self._log(f"[RAC] Intro weapon picked: {trigger_name!r} -> loc={loc!r}")
            self._append_location_by_name(loc)
        candidates: list[int] = []
        for name, unlocked in self._gs.tracked_weapons.items():
            if unlocked and name in WEAPONS and name != trigger_name:
                candidates.append(WEAPONS[name].unlocked)
        for name, unlocked in self._gs.tracked_gadgets.items():
            if unlocked and name in GADGETS:
                candidates.append(GADGETS[name].unlocked)
        if not candidates:
            return
        addr = random.choice(candidates)
        try:
            self.pine.write_int8(addr, 1)
        except Exception:
            pass

    def _handle_scripted_gadget_pickup(self, trigger_name: str) -> None:
        """Called whenever hypershot's unlocked bit transitions 0->1.

        Hypershot is handed to the player during Pokitaru's tutorial as a
        scripted event, not a normal gadget-vendor purchase, so (like the
        three intro weapons above) it never goes through
        PlanetState._wire_vendor_purchase_callbacks's vendor-menu redirect.
        Same not-yet-AP-owned guard as _grant_random_bonus_item, for the same
        reason — this also fires on our own re-apply writes.
        """
        if not self.pine_connected or self._wiring.writes_blocked:
            return
        if self._gs.tracked_gadgets.get(trigger_name):
            return
        loc = GADGET_INTERNAL_TO_LOCATION.get(trigger_name)
        if loc:
            self._log(f"[RAC] Intro gadget picked: {trigger_name!r} -> loc={loc!r}")
            self._append_location_by_name(loc)

    # Notification helper

    def _write_notification_text(self, msg: bytes) -> None:
        if not self.pine_connected:
            return
        if self._wiring.is_in_menu or self._wiring.is_transitioning:
            return
        tb = _SMALL_BOX_BY_PLANET.get(self._prev_planet)
        if tb is None:
            return
        try:
            tb.write_text(self.pine, msg)
        except Exception:
            pass

    # Item notifications

    def _show_new_item_notifications(self) -> None:
        new_items = self.items_received[self._notification_item_index:]
        self._notification_item_index = len(self.items_received)
        if not new_items or not self.pine_connected:
            return
        net_item = new_items[-1]
        item_name   = self.item_names[self.game].get(net_item.item, "???")
        player_name = self.player_names.get(net_item.player, f"Player {net_item.player}")
        msg = colored_text(
            "Received ", TextColour.PURPLE, item_name,
            TextColour.WHITE, " from ", TextColour.ORANGE, player_name, TextColour.WHITE,
        )
        self._write_notification_text(msg)

    # Bolt items

    def _grant_new_bolt_items(self) -> None:
        # PLAYER_BOLT_COUNT is a global address — safe to write during a transition.
        new_items = self.items_received[self._processed_item_count:]
        self._processed_item_count = len(self.items_received)

        bolt_items_to_grant = 0
        starting_bolts = int(self.slot_data.get("starting_bolts", 0))
        for network_item in new_items:
            item_name = self.item_names[self.game].get(network_item.item, "")
            if item_name != "Bolts":
                continue
            if starting_bolts and not self._starting_bolts_granted:
                self._starting_bolts_granted = True
                # On a fresh client process, items_received replays from
                # scratch and _starting_bolts_granted resets to False, so this
                # precollected item would look "new" again. If any location
                # has already been checked, this isn't actually a fresh start
                # (starting bolts were granted in an earlier session) — skip,
                # and don't fall through to the filler-bolts branch either.
                if self.checked_locations:
                    continue
                if not self.pine_connected:
                    continue
                try:
                    current = self.pine.read_int32(PLAYER_BOLT_COUNT)
                    self.pine.write_int32(PLAYER_BOLT_COUNT, current + starting_bolts)
                except Exception as exc:
                    self._log(f"[RAC] Could not grant bolts: {exc}", "warning")
            else:
                bolt_items_to_grant += 1

        if bolt_items_to_grant <= 0 or not self.pine_connected:
            return
        try:
            current = self.pine.read_int32(PLAYER_BOLT_COUNT)
            for _ in range(bolt_items_to_grant):
                grant = min(200000, max(75000, int(current * 0.2)))
                current += grant
            self.pine.write_int32(PLAYER_BOLT_COUNT, current)
        except Exception as exc:
            self._log(f"[RAC] Could not grant bolts: {exc}", "warning")

    # Trap items

    def _grant_new_trap_items(self) -> None:
        # Trap addresses (DREAMTIME_EFFECT, BRIGHTNESS_ADDRESS, CHEATS) are all
        # global — safe to write during a transition.
        new_items = self.items_received[self._processed_trap_count:]
        self._processed_trap_count = len(self.items_received)

        if not self.pine_connected:
            return
        for network_item in new_items:
            item_name = self.item_names[self.game].get(network_item.item, "")
            if item_name not in ALL_TRAPS:
                continue
            try:
                activate_trap(self.pine, item_name)
            except Exception as exc:
                self._log(f"[RAC] Could not activate trap {item_name!r}: {exc}", "warning")

    # World-state restore (crash recovery)

    def _seed_world_states(self) -> None:
        """Compute bolt and skill-point states from already-completed locations."""
        self._titanium_bolt_state.reset()
        self._skill_point_state.reset()
        checked = self.checked_locations | self._locally_checked_locations
        for loc_name, bolt in TITANIUM_BOLTS.items():
            loc_id = self._location_name_to_id.get(loc_name)
            if loc_id and loc_id in checked:
                self._titanium_bolt_state.add(bolt.delta)
        for loc_name, sp in SKILL_POINTS.items():
            loc_id = self._location_name_to_id.get(loc_name)
            if loc_id and loc_id in checked:
                self._skill_point_state.add(sp.mask)

    def _apply_world_states_sync(self) -> None:
        """Write bolt, skill-point, and infobot states to memory.

        All of these (titanium bolts, skill points, planet/infobot state) are
        global addresses, so this is safe to run during a transition.
        """
        self._seed_world_states()
        new_bolt = self._titanium_bolt_state.apply_or(self.pine)
        self._prev_bolt_pickup = new_bolt & BOLT_PICKUP_MASK
        new_sp   = self._skill_point_state.apply_or(self.pine)
        self._prev_skill_points = new_sp
        # Write infobot-unlocked planet states (populated by _rebuild_player_inventory).
        self._planet_state.give(self.pine)
        # Force-unlock planets that have no collectible infobot in the AP world.
        for address in AUTO_UNLOCK_ADDRESSES:
            self.pine.write_int8(address, INFOBOT_UNLOCK_VALUE)
        self._log(
            f"[RAC] World state restored: {self._titanium_bolt_state!r}"
            f"  {self._skill_point_state!r}"
        )

    async def _restore_world_states(self) -> None:
        """Seed and apply bolt/skill-point states.  Called only on connection events."""
        if not self.pine_connected:
            return
        async with self._pine_lock:
            self._apply_world_states_sync()
