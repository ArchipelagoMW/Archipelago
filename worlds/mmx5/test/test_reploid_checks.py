"""Reploid rescue checks.

A rescue's only footprint is lives += 1 (no persistent record exists), so
detection is: lives rose during trusted gameplay in a Reploid stage while the
player stands on a Reploid record. The dataset (reploids.py) is the 14
`gate 4, id 0x00` records proven real in the 2026-08-08 live session.

The traps this file pins:
- lives rise for OTHER reasons (1-UP pickups, savestate loads, menu/stage
  transitions) - position and the trusted-gameplay tracker must silence them;
- the tracker must reset outside trusted gameplay so the first poll after a
  menu can never diff against stale lives;
- two rescues in one poll window (Skiver's adjacent pair) must send both.
"""
import unittest

import worlds.mmx5.client as c
from worlds.mmx5 import names
from worlds.mmx5.client import MMX5Client
from worlds.mmx5.locations import location_table
from worlds.mmx5.reploids import REPLOIDS

from . import MMX5TestBase
from .test_client import FakeContext, make_save, run_watcher

IZZY_STAGE = c.STAGE_ID_BY_NAME[names.FIREFLY]
SKIVER_STAGE = c.STAGE_ID_BY_NAME[names.PEGASUS]


class TestReploidChecksOff(MMX5TestBase):
    options = {"reploid_checks": False}

    def test_no_reploid_locations(self) -> None:
        placed = {loc.name for loc in self.multiworld.get_locations(self.player)}
        for _s, _i, _x, _y, name in REPLOIDS:
            self.assertNotIn(name, placed)


class TestReploidChecksOn(MMX5TestBase):
    options = {"reploid_checks": True}

    def test_locations_created(self) -> None:
        placed = {loc.name for loc in self.multiworld.get_locations(self.player)}
        for _s, _i, _x, _y, name in REPLOIDS:
            self.assertIn(name, placed)

    def test_adds_fourteen_locations_and_no_items(self) -> None:
        real = [l for l in self.multiworld.get_locations(self.player)
                if l.address is not None]
        self.assertEqual(len(real), 62)  # 48 default + 14

    def test_reploids_live_in_their_stage_regions(self) -> None:
        for stage, _i, _x, _y, name in REPLOIDS:
            loc = self.multiworld.get_location(name, self.player)
            self.assertEqual(loc.parent_region.name, stage)


class TestReploidDataset(unittest.TestCase):
    def test_ids_are_stable_and_unique(self) -> None:
        from worlds.mmx5.items import BASE_ID
        for i, (_s, _idx, _x, _y, name) in enumerate(REPLOIDS):
            self.assertEqual(location_table[name], BASE_ID + 250 + i)
        ids = list(location_table.values())
        self.assertEqual(len(ids), len(set(ids)), "duplicate location id")

    def test_counts_match_the_census(self) -> None:
        per_stage = {}
        for stage, _i, _x, _y, _n in REPLOIDS:
            per_stage[stage] = per_stage.get(stage, 0) + 1
        self.assertEqual(per_stage, {names.KRAKEN: 6, names.FIREFLY: 3,
                                     names.PEGASUS: 5})

    def test_live_proven_records_are_present(self) -> None:
        # The four rescues actually performed on 2026-08-08, by record
        # identity. If a refactor loses one of these, the dataset no longer
        # matches the evidence it rests on.
        proven = {(names.FIREFLY, 20, 384, 651), (names.FIREFLY, 21, 1776, 248),
                  (names.FIREFLY, 22, 3432, 283), (names.PEGASUS, 37, 896, 1616)}
        have = {(s, i, x, y) for s, i, x, y, _n in REPLOIDS}
        self.assertTrue(proven <= have, f"missing: {proven - have}")


class TestReploidDetection(unittest.IsolatedAsyncioTestCase):
    def _ctx(self, enabled=1) -> FakeContext:
        ctx = FakeContext()
        ctx.slot_data = {"goal": 0, "boss_difficulty": 1,
                         "reploid_checks": enabled}
        return ctx

    def _reploid_ids(self, ctx) -> set:
        all_ids = {location_table[n] for _s, _i, _x, _y, n in REPLOIDS}
        return ctx.checked_location_ids() & all_ids

    def _loc(self, name) -> int:
        return location_table[name]

    async def _poll(self, client, ctx, lives, stage_id=IZZY_STAGE, **kw):
        return await run_watcher(make_save(max_hp=0x30, lives=lives),
                                 client=client, ctx=ctx,
                                 stage_id=stage_id, **kw)

    async def test_rescue_on_the_record_sends_it(self) -> None:
        client, ctx = MMX5Client(), self._ctx()
        # Izzy Reploid 1 is at (384, 651); the live rescue read (409, 651).
        await self._poll(client, ctx, lives=2, player_x=380, player_y=650)
        await self._poll(client, ctx, lives=3, player_x=409, player_y=651)
        self.assertEqual(self._reploid_ids(ctx),
                         {self._loc(f"{names.FIREFLY} - Reploid 1")})

    async def test_walkaway_within_radius_still_matches(self) -> None:
        client, ctx = MMX5Client(), self._ctx()
        await self._poll(client, ctx, lives=2, player_x=384, player_y=651)
        # By the next poll the player has moved ~200px right of the rescue.
        await self._poll(client, ctx, lives=3, player_x=584, player_y=640)
        self.assertEqual(self._reploid_ids(ctx),
                         {self._loc(f"{names.FIREFLY} - Reploid 1")})

    async def test_one_up_away_from_records_sends_nothing(self) -> None:
        client, ctx = MMX5Client(), self._ctx()
        await self._poll(client, ctx, lives=2, player_x=2600, player_y=200)
        await self._poll(client, ctx, lives=3, player_x=2600, player_y=200)
        self.assertEqual(self._reploid_ids(ctx), set())

    async def test_double_rescue_sends_the_adjacent_pair(self) -> None:
        # Skiver's pair at x=896/984 is 88px apart - two rescues can land in
        # one poll window and both must send.
        client, ctx = MMX5Client(), self._ctx()
        await self._poll(client, ctx, lives=2, stage_id=SKIVER_STAGE,
                         player_x=896, player_y=1616)
        await self._poll(client, ctx, lives=4, stage_id=SKIVER_STAGE,
                         player_x=940, player_y=1611)
        self.assertEqual(self._reploid_ids(ctx),
                         {self._loc(f"{names.PEGASUS} - Reploid 1"),
                          self._loc(f"{names.PEGASUS} - Reploid 2")})

    async def test_single_rescue_near_pair_sends_only_nearest(self) -> None:
        client, ctx = MMX5Client(), self._ctx()
        await self._poll(client, ctx, lives=2, stage_id=SKIVER_STAGE,
                         player_x=980, player_y=1616)
        await self._poll(client, ctx, lives=3, stage_id=SKIVER_STAGE,
                         player_x=980, player_y=1616)
        self.assertEqual(self._reploid_ids(ctx),
                         {self._loc(f"{names.PEGASUS} - Reploid 2")})

    async def test_lives_jump_across_stage_change_sends_nothing(self) -> None:
        # Different stage between polls: the tracker must not diff across it,
        # even standing on a (different stage's) record position.
        client, ctx = MMX5Client(), self._ctx()
        await self._poll(client, ctx, lives=2, stage_id=SKIVER_STAGE,
                         player_x=896, player_y=1616)
        await self._poll(client, ctx, lives=3, stage_id=IZZY_STAGE,
                         player_x=384, player_y=651)
        self.assertEqual(self._reploid_ids(ctx), set())

    async def test_lives_jump_after_menu_sends_nothing(self) -> None:
        # A savestate load or menu visit breaks trust for a poll; the first
        # trusted poll after it must re-baseline, not diff. run_watcher with
        # settled=False models the untrusted re-entry poll.
        client, ctx = MMX5Client(), self._ctx()
        await self._poll(client, ctx, lives=2, player_x=384, player_y=651)
        await run_watcher(make_save(max_hp=0x30, lives=9), client=client,
                          ctx=ctx, stage_id=IZZY_STAGE, mode=0x04,
                          player_x=384, player_y=651)
        await self._poll(client, ctx, lives=9, player_x=384, player_y=651)
        self.assertEqual(self._reploid_ids(ctx), set())

    async def test_non_reploid_stage_sends_nothing(self) -> None:
        client, ctx = MMX5Client(), self._ctx()
        grizzly = c.STAGE_ID_BY_NAME[names.GRIZZLY]
        await self._poll(client, ctx, lives=2, stage_id=grizzly,
                         player_x=384, player_y=651)
        await self._poll(client, ctx, lives=3, stage_id=grizzly,
                         player_x=384, player_y=651)
        self.assertEqual(self._reploid_ids(ctx), set())

    async def test_option_off_is_inert(self) -> None:
        client, ctx = MMX5Client(), self._ctx(enabled=0)
        await self._poll(client, ctx, lives=2, player_x=384, player_y=651)
        await self._poll(client, ctx, lives=3, player_x=409, player_y=651)
        self.assertEqual(self._reploid_ids(ctx), set())
