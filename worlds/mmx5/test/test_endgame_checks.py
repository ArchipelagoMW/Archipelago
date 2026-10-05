"""Zero Space clear checks.

Detection rides the story ACT byte (0x800D1C79), which the hub's stage-select
confirm handler uses to pick the endgame destination: 5 -> Zero Space 1,
6 -> Zero Space 2, 7 -> X vs Zero, anything else -> Sigma. So a clear is
"ACT reached the next rung".

Two other things write that byte, and both are traps this file pins:
the all_mavericks goal pushes ACT back below 5 to hold the endgame shut, and
training mode parks 0x0A in it - which is above every threshold here.
"""
import unittest
from types import SimpleNamespace

import worlds.mmx5.client as c
from worlds.mmx5 import names
from worlds.mmx5.client import MMX5Client
from worlds.mmx5.locations import location_table

from . import MMX5TestBase
from .test_client import FakeContext, make_save, run_watcher


class TestEndgameChecksOff(MMX5TestBase):
    options = {"endgame_checks": False}

    def test_no_endgame_locations(self) -> None:
        placed = {loc.name for loc in self.multiworld.get_locations(self.player)}
        for stage in names.ENDGAME_STAGES:
            self.assertNotIn(names.endgame_clear_location(stage), placed)

    def test_location_count_matches_0_2_0(self) -> None:
        real = [l for l in self.multiworld.get_locations(self.player)
                if l.address is not None]
        self.assertEqual(len(real), 45, "seeds with the option off must match 0.2.0")


class TestEndgameChecksOn(MMX5TestBase):
    options = {"endgame_checks": True}

    def test_locations_created(self) -> None:
        placed = {loc.name for loc in self.multiworld.get_locations(self.player)}
        for stage in names.ENDGAME_STAGES:
            self.assertIn(names.endgame_clear_location(stage), placed)

    def test_adds_three_locations_and_no_items(self) -> None:
        real = [l for l in self.multiworld.get_locations(self.player)
                if l.address is not None]
        self.assertEqual(len(real), 48)

    def test_gives_the_pool_headroom(self) -> None:
        # The only option so far that widens capacity: +3 locations, +0 real
        # items, so filler grows. That is what lets other options stack.
        pool = [i.name for i in self.multiworld.itempool]
        filler = sum(1 for n in pool if n == names.SMALL_ENERGY)
        self.assertEqual(filler, 12, "endgame checks should add three filler slots")

    def test_behind_the_sigma_entrance_rule(self) -> None:
        # They live in Sigma Stages, so they inherit the all-8-weapons rule
        # rather than being reachable from the stage select with nothing.
        from BaseClasses import CollectionState
        blank = CollectionState(self.multiworld)
        blank.prog_items[self.player].clear()
        for stage in names.ENDGAME_STAGES:
            loc = self.multiworld.get_location(
                names.endgame_clear_location(stage), self.player)
            self.assertFalse(loc.can_reach(blank))


class TestEndgameIds(unittest.TestCase):
    def test_ids_are_stable_and_unique(self) -> None:
        from worlds.mmx5.items import BASE_ID
        for i, stage in enumerate(names.ENDGAME_STAGES):
            self.assertEqual(
                location_table[names.endgame_clear_location(stage)],
                BASE_ID + 180 + i)
        ids = list(location_table.values())
        self.assertEqual(len(ids), len(set(ids)), "duplicate location id")

    def test_thresholds_are_the_confirm_handler_ladder(self) -> None:
        self.assertEqual(c.ENDGAME_CLEAR_ACT[names.ZERO_SPACE_1], 6)
        self.assertEqual(c.ENDGAME_CLEAR_ACT[names.ZERO_SPACE_2], 7)
        self.assertEqual(c.ENDGAME_CLEAR_ACT[names.ZERO_SPACE_X_VS_ZERO], 8)


class TestEndgameDetection(unittest.IsolatedAsyncioTestCase):
    def _ctx(self, enabled=1, goal=0) -> FakeContext:
        ctx = FakeContext()
        ctx.slot_data = {"goal": goal, "boss_difficulty": 1,
                         "endgame_checks": enabled}
        return ctx

    def _ids(self, ctx) -> set:
        return ctx.checked_location_ids()

    def _loc(self, stage) -> int:
        return location_table[names.endgame_clear_location(stage)]

    async def test_act_6_sends_only_zero_space_1(self) -> None:
        ctx = await run_watcher(make_save(max_hp=0x20, intro=6, weapons=0xFF),
                                client=MMX5Client(), ctx=self._ctx())
        got = self._ids(ctx)
        self.assertIn(self._loc(names.ZERO_SPACE_1), got)
        self.assertNotIn(self._loc(names.ZERO_SPACE_2), got)
        self.assertNotIn(self._loc(names.ZERO_SPACE_X_VS_ZERO), got)

    async def test_act_8_sends_all_three(self) -> None:
        ctx = await run_watcher(make_save(max_hp=0x20, intro=8, weapons=0xFF),
                                client=MMX5Client(), ctx=self._ctx())
        got = self._ids(ctx)
        for stage in names.ENDGAME_STAGES:
            self.assertIn(self._loc(stage), got)

    async def test_act_5_sends_none(self) -> None:
        # ACT 5 is "Zero Space 1 is open", not "cleared".
        ctx = await run_watcher(make_save(max_hp=0x20, intro=5, weapons=0xFF),
                                client=MMX5Client(), ctx=self._ctx())
        got = self._ids(ctx)
        for stage in names.ENDGAME_STAGES:
            self.assertNotIn(self._loc(stage), got)

    async def test_training_cannot_fire_them(self) -> None:
        # Training parks ACT 0x0A - above every threshold. It fired a phantom
        # intro check once already; this is the same shape of bug.
        ctx = await run_watcher(make_save(max_hp=0x20, intro=c.TRAINING_ACT,
                                          weapons=0),
                                client=MMX5Client(), ctx=self._ctx())
        got = self._ids(ctx)
        for stage in names.ENDGAME_STAGES:
            self.assertNotIn(self._loc(stage), got)

    async def test_stale_save_cannot_fire_them(self) -> None:
        ctx = await run_watcher(make_save(max_hp=0x00, intro=0xFF, weapons=0xFF),
                                client=MMX5Client(), ctx=self._ctx())
        self.assertEqual(self._ids(ctx), set())

    async def test_inert_when_option_off(self) -> None:
        ctx = await run_watcher(make_save(max_hp=0x20, intro=8, weapons=0xFF),
                                client=MMX5Client(), ctx=self._ctx(enabled=0))
        got = self._ids(ctx)
        for stage in names.ENDGAME_STAGES:
            self.assertNotIn(self._loc(stage), got)

    async def test_all_mavericks_withhold_cannot_unsend_a_clear(self) -> None:
        # The goal pushes ACT back below 5 when the colony resolves early. A
        # LIVE read would lose an already-earned clear; the high-water mark
        # must not. Drive one cycle at ACT 8, then one at the withheld value.
        client = MMX5Client()
        ctx = self._ctx(goal=c.GOAL_ALL_MAVERICKS)
        await run_watcher(make_save(max_hp=0x20, intro=8, weapons=0xFF),
                          client=client, ctx=ctx)
        self.assertEqual(client.max_act_seen, 8)
        await run_watcher(make_save(max_hp=0x20, intro=2, weapons=0x03),
                          client=client, ctx=ctx)
        self.assertEqual(client.max_act_seen, 8,
                         "the withhold lowered the latched ACT")
