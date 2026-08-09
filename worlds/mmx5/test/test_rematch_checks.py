"""Boss Rush rematch checks.

Detection is a client-side watcher (live session 2026-08-08): a rematch runs
in the standard boss-HP slot 0x800920EC, and the fight is IDENTIFIED by the
16-byte fingerprint of the boss module the portal streamed to 0x800FA000.
The kill condition is a conjunction - rush stage + gameplay mode + known
fingerprint + observed HP fill + HP zero + player alive - and every term
exists because dropping it produced (or would produce) a concrete false
check. Those are the traps this file pins:

- the module PERSISTS after a fight, so fingerprint-present must not mean
  fight-in-progress (corridor blips on the stale HP byte);
- a mid-fight player death zeroes nothing we can trust, so it must never
  read as a boss kill;
- own-stage Maverick fights use modules carrying the SAME fingerprints, so
  the stage gate is what keeps normal boss kills from firing rematches;
- Sigma's own fights happen in the SAME stage, so an unknown fingerprint
  must send nothing.
"""
import unittest

import worlds.mmx5.client as c
from worlds.mmx5 import names
from worlds.mmx5.client import MMX5Client
from worlds.mmx5.locations import location_table

from . import MMX5TestBase
from .test_client import FakeContext, make_save, run_watcher

FP = {stage: fp for fp, stage in c.RUSH_FP_TO_STAGE.items()}


class TestRematchChecksOff(MMX5TestBase):
    options = {"rematch_checks": False}

    def test_no_rematch_locations(self) -> None:
        placed = {loc.name for loc in self.multiworld.get_locations(self.player)}
        for stage in names.STAGES:
            self.assertNotIn(names.rematch_location(stage), placed)

    def test_location_count_unchanged(self) -> None:
        real = [l for l in self.multiworld.get_locations(self.player)
                if l.address is not None]
        self.assertEqual(len(real), 48,
                         "default seed (endgame_checks on) must stay at 48")


class TestRematchChecksOn(MMX5TestBase):
    options = {"rematch_checks": True}

    def test_locations_created(self) -> None:
        placed = {loc.name for loc in self.multiworld.get_locations(self.player)}
        for stage in names.STAGES:
            self.assertIn(names.rematch_location(stage), placed)

    def test_adds_eight_locations_and_no_items(self) -> None:
        real = [l for l in self.multiworld.get_locations(self.player)
                if l.address is not None]
        self.assertEqual(len(real), 56)

    def test_gives_the_pool_headroom(self) -> None:
        # Like endgame_checks: locations without items = filler slots. The
        # default seed carries 12 filler (48 - 36); +8 locations makes 20.
        pool = [i.name for i in self.multiworld.itempool]
        filler = sum(1 for n in pool if n == names.SMALL_ENERGY)
        self.assertEqual(filler, 20, "rematch checks should add eight filler slots")

    def test_behind_the_sigma_entrance_rule(self) -> None:
        # The rush is in Zero Space: the locations live in Sigma Stages and
        # inherit the all-8-weapons rule, not stage-select reachability.
        from BaseClasses import CollectionState
        blank = CollectionState(self.multiworld)
        blank.prog_items[self.player].clear()
        for stage in names.STAGES:
            loc = self.multiworld.get_location(
                names.rematch_location(stage), self.player)
            self.assertFalse(loc.can_reach(blank))


class TestRematchIds(unittest.TestCase):
    def test_ids_are_stable_and_unique(self) -> None:
        from worlds.mmx5.items import BASE_ID
        for i, stage in enumerate(names.STAGES):
            self.assertEqual(location_table[names.rematch_location(stage)],
                             BASE_ID + 100 + i * 10 + 6,
                             "rematch ids live in each stage's +6 slot")
        ids = list(location_table.values())
        self.assertEqual(len(ids), len(set(ids)), "duplicate location id")

    def test_fingerprints_cover_all_eight_and_are_distinct(self) -> None:
        self.assertEqual(set(c.RUSH_FP_TO_STAGE.values()), set(names.STAGES))
        self.assertEqual(len(c.RUSH_FP_TO_STAGE), 8)
        for fp in c.RUSH_FP_TO_STAGE:
            self.assertEqual(len(fp), c.RUSH_FP_LEN)


class TestRematchDetection(unittest.IsolatedAsyncioTestCase):
    def _ctx(self, enabled=1) -> FakeContext:
        ctx = FakeContext()
        ctx.slot_data = {"goal": 0, "boss_difficulty": 1,
                         "rematch_checks": enabled}
        return ctx

    def _loc(self, stage) -> int:
        return location_table[names.rematch_location(stage)]

    def _rematch_ids(self, ctx) -> set:
        """Rematch checks sent, ignoring everything else the late-game save
        legitimately fires (bosses, DNA, intro, endgame clears)."""
        all_rematch = {self._loc(s) for s in names.STAGES}
        return ctx.checked_location_ids() & all_rematch

    @staticmethod
    def _save() -> bytes:
        # A late-game save: all weapons, deep ACT. What a player in the rush
        # actually holds; the watcher itself never reads it, but the cycle
        # around it does.
        return make_save(max_hp=0x30, intro=8, weapons=0xFF)

    async def _poll(self, client, ctx, **kw) -> FakeContext:
        return await run_watcher(self._save(), client=client, ctx=ctx,
                                 stage_id=c.SIGMA_STAGE_ID, **kw)

    async def test_fill_then_zero_sends_that_boss(self) -> None:
        client, ctx = MMX5Client(), self._ctx()
        await self._poll(client, ctx, rush_hp=58, rush_fp=FP[names.KRAKEN])
        self.assertNotIn(self._loc(names.KRAKEN), ctx.checked_location_ids())
        await self._poll(client, ctx, rush_hp=0, rush_fp=FP[names.KRAKEN])
        got = ctx.checked_location_ids()
        self.assertIn(self._loc(names.KRAKEN), got)
        for stage in names.STAGES:
            if stage != names.KRAKEN:
                self.assertNotIn(self._loc(stage), got)

    async def test_zero_without_fill_sends_nothing(self) -> None:
        # Entering the corridor with a module resident and the stale HP byte
        # already 0 - the state the rush actually parks in after a fight.
        client, ctx = MMX5Client(), self._ctx()
        await self._poll(client, ctx, rush_hp=0, rush_fp=FP[names.KRAKEN])
        self.assertEqual(self._rematch_ids(ctx), set())

    async def test_corridor_blip_sends_nothing(self) -> None:
        # Observed live: the idle byte blips to 6 and back to 0 in the
        # corridors while a previous fight's module is still resident.
        client, ctx = MMX5Client(), self._ctx()
        await self._poll(client, ctx, rush_hp=6, rush_fp=FP[names.FIREFLY])
        await self._poll(client, ctx, rush_hp=0, rush_fp=FP[names.FIREFLY])
        self.assertEqual(self._rematch_ids(ctx), set())

    async def test_unknown_module_sends_nothing(self) -> None:
        # Sigma's own fights load a module too - same stage, same HP slot,
        # unknown fingerprint. A full fight must produce no rematch check.
        client, ctx = MMX5Client(), self._ctx()
        junk = bytes(range(c.RUSH_FP_LEN))
        await self._poll(client, ctx, rush_hp=127, rush_fp=junk)
        await self._poll(client, ctx, rush_hp=0, rush_fp=junk)
        self.assertEqual(self._rematch_ids(ctx), set())

    async def test_player_death_is_not_a_kill(self) -> None:
        # The module stays resident through a player death; whatever the
        # respawn leaves in the boss-HP byte, it must not read as a kill -
        # not at the death poll, and not at a later boss-0 poll either.
        client, ctx = MMX5Client(), self._ctx()
        await self._poll(client, ctx, rush_hp=58, rush_fp=FP[names.KRAKEN])
        await self._poll(client, ctx, rush_hp=0, rush_fp=FP[names.KRAKEN],
                         player_hp=0)
        self.assertEqual(self._rematch_ids(ctx), set())
        await self._poll(client, ctx, rush_hp=0, rush_fp=FP[names.KRAKEN])
        self.assertEqual(self._rematch_ids(ctx), set(),
                         "a dead fight's peak validated a later zero")

    async def test_own_stage_boss_kill_cannot_fire(self) -> None:
        # Killing Izzy Glow in Izzy Glow's stage: his module is resident and
        # carries the same fingerprint, HP fills and hits zero - only the
        # stage gate stands between this and a phantom rematch.
        client, ctx = MMX5Client(), self._ctx()
        izzy_stage = c.STAGE_ID_BY_NAME[names.FIREFLY]
        await run_watcher(self._save(), client=client, ctx=ctx,
                          stage_id=izzy_stage, rush_hp=53,
                          rush_fp=FP[names.FIREFLY])
        await run_watcher(self._save(), client=client, ctx=ctx,
                          stage_id=izzy_stage, rush_hp=0,
                          rush_fp=FP[names.FIREFLY])
        self.assertEqual(self._rematch_ids(ctx), set())

    async def test_module_swap_resets_the_peak(self) -> None:
        # Fill on boss A, then the player exits and enters boss B's portal:
        # A's fill must not validate a zero read under B's fingerprint.
        client, ctx = MMX5Client(), self._ctx()
        await self._poll(client, ctx, rush_hp=58, rush_fp=FP[names.KRAKEN])
        await self._poll(client, ctx, rush_hp=0, rush_fp=FP[names.GRIZZLY])
        self.assertEqual(self._rematch_ids(ctx), set())

    async def test_option_off_is_inert(self) -> None:
        client, ctx = MMX5Client(), self._ctx(enabled=0)
        await self._poll(client, ctx, rush_hp=58, rush_fp=FP[names.KRAKEN])
        await self._poll(client, ctx, rush_hp=0, rush_fp=FP[names.KRAKEN])
        self.assertEqual(self._rematch_ids(ctx), set())

    async def test_already_checked_is_not_resent(self) -> None:
        client, ctx = MMX5Client(), self._ctx()
        ctx.checked_locations.add(self._loc(names.KRAKEN))
        await self._poll(client, ctx, rush_hp=58, rush_fp=FP[names.KRAKEN])
        await self._poll(client, ctx, rush_hp=0, rush_fp=FP[names.KRAKEN])
        self.assertEqual(self._rematch_ids(ctx), set())
