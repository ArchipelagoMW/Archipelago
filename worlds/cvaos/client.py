"""
BizHawk client for Castlevania: Aria of Sorrow.

This client validates the patched ROM, authenticates, connects, sends location checks for
collected pickups, grants received items, and relays DeathLink (``game_watcher``). Goal
detection is added in a later phase (see worlds/cvaos/ROADMAP.md).
"""
from __future__ import annotations

import base64
from typing import TYPE_CHECKING

import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from NetUtils import ClientStatus

from . import item_granting
from .locations import flag_offset_to_location_id
from .options import Goal
from .ram import AoSRAM, addresses as addr
from .rom import ARCHIPELAGO_IDENTIFIER, ARCHIPELAGO_IDENTIFIER_START, AUTH_NUMBER_START

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

# GBA header: 12-byte internal game title at 0xA0 (CLIENT_PLAN sec. 5a).
ROM_NAME_START = 0xA0
ROM_NAME = "CASTLEVANIA2"

# Max items to grant per game_watcher tick, so a large backlog on connect can't stall the watcher
# (each grant is a few BizHawk round-trips). Leftovers are picked up on the following ticks.
MAX_ITEMS_PER_TICK = 10


class CVAOSClient(BizHawkClient):
    game = "Castlevania - Aria of Sorrow"
    system = "GBA"
    patch_suffix = ".apcvaos"

    # Per-session state, (re)initialized in set_auth.
    death_causes: list[str]
    local_checked_locations: set[int]
    currently_dead: bool
    time_of_sent_death: float | None
    goaled: bool

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
        self.local_checked_locations = set()
        # DeathLink: whether we currently consider Soma dead — guards re-sending our own death and
        # re-applying an incoming one until HP recovers.
        self.currently_dead = False
        # AP's timestamp on the death we last sent, so on_package can recognize our own echo.
        self.time_of_sent_death = None
        # Goal: latched True once we've reported completion, so we report it only once.
        self.goaled = False

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        # Queue an incoming DeathLink's cause; game_watcher applies the kill. Skip the echo of our
        # own death (it carries the timestamp we recorded when we sent it) so we never re-kill Soma
        # from our own death after he respawns.
        if cmd != "Bounced" or "tags" not in args or ctx.slot is None:
            return
        if "DeathLink" in args["tags"]:
            data = args.get("data", {})
            if data.get("time") == self.time_of_sent_death:
                return  # our own death, bounced back to us
            source = data.get("source", "Another world")
            self.death_causes.append(data.get("cause") or f"{source} killed you without a word!")

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if ctx.server is None or ctx.slot is None:
            return
        try:
            ram = AoSRAM(ctx.bizhawk_ctx)
            # Only read/act in normal in-room gameplay (not paused, transitioning, in a menu,
            # or game-over), so we never read garbage or act at an unsafe time.
            if not await ram.is_in_gameplay():
                return

            # Collected-pickup save flags -> AP location checks. Each set bit's index is a
            # pickup's flag_offset. We map it to the AP location id and send it if the server
            # tracks that location for this slot.
            flag_bytes = await ram.read_pickup_flags()
            checked: set[int] = set()
            for flag_offset in AoSRAM.pickup_flag_ids(flag_bytes):
                location_id = flag_offset_to_location_id.get(flag_offset)
                if location_id is not None and location_id in ctx.server_locations:
                    checked.add(location_id)

            new_checks = checked - self.local_checked_locations
            if new_checks:
                self.local_checked_locations |= new_checks
                await ctx.send_msgs([{"cmd": "LocationChecks", "locations": sorted(new_checks)}])

            # Receive items from the server: grant each not-yet-given item, then advance the saved
            # received-counter (guarded) so a reload doesn't re-give them. Stop on a lost guarded
            # write (a race with the game's writes, or the counter changing underneath us) and retry.
            received = await ram.get_received_count()
            # Defensive: a counter ahead of everything the server has ever sent could only come from a
            # corrupt save; clamp so we never index past items_received (a real grant rewrites it).
            received = min(received, len(ctx.items_received))
            granted_this_tick = 0
            while received < len(ctx.items_received) and granted_this_tick < MAX_ITEMS_PER_TICK:
                code = ctx.items_received[received].item
                action = item_granting.resolve(code)
                if action is None:
                    # Unreachable today (every item is a pickup); log instead of silently
                    # dropping a received item if a non-pickup item is ever added to the pool.
                    from CommonClient import logger
                    logger.warning("CVAoS: received item code %s has no grant mapping; skipping.", code)
                elif not await item_granting.grant(ram, action):
                    break  # lost a guarded write on the grant; retry next tick without advancing
                # Advance the saved counter, guarded on its prior value so we never blind-stomp it.
                if not await ram.set_received_count(received + 1, expected=received):
                    break  # counter changed underneath us; re-read and retry next tick
                received += 1
                granted_this_tick += 1

            # DeathLink (Strategy A: RAM poke)
            # Enable DeathLink once if the seed wants it; update_death_link adds the "DeathLink"
            # tag, so this won't re-fire on later ticks.
            if ctx.slot_data.get("death_link") and "DeathLink" not in ctx.tags:
                await ctx.update_death_link(True)

            # One HP read drives both directions: broadcast when we hit 0, re-arm when alive again.
            hp = await ram.get_current_hp()
            if "DeathLink" in ctx.tags and hp == 0 and not self.currently_dead:
                # Died on our own. Mark dead BEFORE awaiting so a same-tick re-entry can't double-send.
                self.currently_dead = True
                await ctx.send_death(f"{ctx.player_names[ctx.slot]} was slain. Dracula has won!")
                # Record AP's timestamp so on_package can filter our own echo (overwritten later).
                self.time_of_sent_death = ctx.last_death_link

            if self.death_causes and not self.currently_dead:
                # Apply an incoming death (on_package queued the cause). The currently_dead gate
                # keeps us from re-killing Soma for a death already in progress.
                from CommonClient import logger
                cause = self.death_causes.pop(0)
                await ram.kill_player()
                self.currently_dead = True
                logger.info("CVAoS DeathLink: %s", cause)
            elif hp > 0 and self.currently_dead:
                # Alive again (respawn or reload) — re-arm for the next death in either direction.
                self.currently_dead = False

            # Goal / win condition
            # Report completion once, when the player wins per their Goal: graham -> Graham defeated
            # (BOSS_FLAGS & 0x01); chaos -> the good-ending flag (GLOBAL_FLAGS & 0x4000). Hardware-
            # verified: on the Chaos win the good-ending bit (and the Chaos boss bit BOSS_FLAGS &
            # 0x80, which the decomp's C only shows being cleared) both flip during the post-kill
            # "castle swallowed" cutscene while GAME_STATE is still INGAME and MENU_STATE NORMAL --
            # so this in-gameplay-gated read catches it. We use 0x4000 because it persists (saved),
            # so the goal still registers if that live window is ever missed (e.g. a reconnect after
            # the win). BOSS_FLAG_CHAOS (0x80) is the symmetric alternative -- it flips at the same
            # instant; swap to it, or OR it in, if 0x4000 ever gives trouble. Its only caveat is that
            # it's transient (cleared at the credits transition, and not saved).
            if not ctx.finished_game and not self.goaled:
                goal = ctx.slot_data.get("goal", Goal.option_chaos)
                if goal == Goal.option_graham:
                    won = await ram.has_defeated(addr.BOSS_FLAG_GRAHAM)
                else:  # chaos -> the good ending
                    won = await ram.has_good_ending()
                if won:
                    self.goaled = True
                    ctx.finished_game = True
                    await ctx.send_msgs([{"cmd": "StatusUpdate",
                                          "status": ClientStatus.CLIENT_GOAL}])
        except bizhawk.RequestFailedError:
            # Emulator/connection hiccup; retry next tick.
            return
