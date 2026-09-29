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
from unittest import mock

import worlds.mmx5.client as c
from worlds.mmx5 import names
from worlds.mmx5.client import MMX5Client
from worlds.mmx5.locations import location_table
from worlds.mmx5.reploids import REPLOIDS

from . import MMX5TestBase
from .test_client import FakeContext, make_save, run_watcher

IZZY_STAGE = c.STAGE_ID_BY_NAME[names.FIREFLY]
SKIVER_STAGE = c.STAGE_ID_BY_NAME[names.PEGASUS]
KRAKEN_STAGE = c.STAGE_ID_BY_NAME[names.KRAKEN]
# The Skiver's 1 (896,1616) and 2 (984,1616) are 88px apart - stand between.
SKIVER_PAIR_X, SKIVER_PAIR_Y = 940, 1616
# Squid Adler's 3 (6992,1008), 4 (6768,1120) and 5 (6976,1216) are mutually
# within one radius; this point sees all three and nothing else.
SQUID_CLUSTER_X, SQUID_CLUSTER_Y = 6900, 1110


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

    # ---- the 9-life cap (tester report, 2026-08-10) --------------------
    # At 9 lives the rescue handler clamps back to 9 and jumps over the sound
    # (0x800F16D8 / 0x800F16E4) while the animation after 0x800F16F8 still
    # runs: the Reploid is consumed and the player gets no life, no sound and
    # no check. Re-entering repeats it, so the check is uncollectable. The
    # client makes the handler's own precondition (lives + 1 < 10) true.

    def _lives_writes(self, ctx) -> list:
        addr = c.SAVE_BASE + c.OFF_LIVES
        return [w[1][0] for w in ctx.writes if w[0] == addr]

    async def test_held_below_the_cap_near_an_outstanding_reploid(self) -> None:
        client, ctx = MMX5Client(), self._ctx()
        # Izzy Reploid 1 is at (384, 651).
        await self._poll(client, ctx, lives=9, player_x=380, player_y=650)
        self.assertEqual(self._lives_writes(ctx), [8],
                         "left the player at 9, where the rescue is discarded")

    async def test_not_held_away_from_every_reploid(self) -> None:
        client, ctx = MMX5Client(), self._ctx()
        await self._poll(client, ctx, lives=9, player_x=9000, player_y=9000)
        self.assertEqual(self._lives_writes(ctx), [],
                         "took a life with no Reploid anywhere near")

    async def test_not_held_when_the_stage_is_already_collected(self) -> None:
        client, ctx = MMX5Client(), self._ctx()
        ctx.checked_locations = {self._loc(n)
                                 for _s, _i, _x, _y, n in REPLOIDS}
        await self._poll(client, ctx, lives=9, player_x=380, player_y=650)
        self.assertEqual(self._lives_writes(ctx), [],
                         "took a life for checks that were already sent")

    async def test_not_held_below_the_cap(self) -> None:
        client, ctx = MMX5Client(), self._ctx()
        await self._poll(client, ctx, lives=8, player_x=380, player_y=650)
        self.assertEqual(self._lives_writes(ctx), [])

    async def test_headroom_covers_a_whole_cluster(self) -> None:
        """Reploids come in clusters, and one free life only covers one rescue.

        The Skiver's 1 and 2 are 88px apart and Squid Adler's 3/4/5 are all
        within one radius; the client polls far more slowly than a player
        crosses 88px, so with a single life freed the second rescue lands back
        at the cap and is discarded exactly as before the fix.
        """
        client, ctx = MMX5Client(), self._ctx()
        # The Skiver 1 (896, 1015) and 2 (984, 1015) - stand between them.
        await self._poll(client, ctx, lives=9, stage_id=SKIVER_STAGE,
                         player_x=SKIVER_PAIR_X, player_y=SKIVER_PAIR_Y)
        self.assertEqual(self._lives_writes(ctx), [7],
                         "only freed one life beside two Reploids")

    async def test_headroom_applies_below_the_cap_too(self) -> None:
        # At 8 lives with two adjacent Reploids the SECOND is still discarded,
        # so the trigger cannot be "lives == 9".
        client, ctx = MMX5Client(), self._ctx()
        await self._poll(client, ctx, lives=8, stage_id=SKIVER_STAGE,
                         player_x=SKIVER_PAIR_X, player_y=SKIVER_PAIR_Y)
        self.assertEqual(self._lives_writes(ctx), [7])

    async def test_no_write_when_headroom_is_already_enough(self) -> None:
        client, ctx = MMX5Client(), self._ctx()
        await self._poll(client, ctx, lives=7, stage_id=SKIVER_STAGE,
                         player_x=SKIVER_PAIR_X, player_y=SKIVER_PAIR_Y)
        self.assertEqual(self._lives_writes(ctx), [],
                         "took lives that were not needed")

    async def test_two_rescues_in_one_window_both_send(self) -> None:
        client, ctx = MMX5Client(), self._ctx()
        await self._poll(client, ctx, lives=9, stage_id=SKIVER_STAGE,
                         player_x=SKIVER_PAIR_X, player_y=SKIVER_PAIR_Y)
        self.assertEqual(self._lives_writes(ctx), [7])
        # Both rescued between polls: 7 -> 9.
        await self._poll(client, ctx, lives=9, stage_id=SKIVER_STAGE,
                         player_x=SKIVER_PAIR_X, player_y=SKIVER_PAIR_Y)
        got = self._reploid_ids(ctx)
        self.assertEqual(len(got), 2, f"only {len(got)} of 2 rescues registered")

    async def test_never_strands_the_player_at_zero(self) -> None:
        """The floor, exercised against a dataset dense enough to reach it.

        With the shipped Reploid data the deepest cluster any position can see
        is 3, so the arithmetic never gets near zero and this test would pass
        with the floor deleted - i.e. prove nothing. Patch in a pathological
        stage instead, so the guard is actually under test rather than merely
        present.
        """
        dense = [(0, 0, n) for _s, _i, _x, _y, n in REPLOIDS]   # 14, co-located
        with mock.patch.dict(c.REPLOID_RECORDS_BY_STAGE,
                             {IZZY_STAGE: dense}, clear=False):
            client, ctx = MMX5Client(), self._ctx()
            await self._poll(client, ctx, lives=9, player_x=0, player_y=0)
        writes = self._lives_writes(ctx)
        self.assertEqual(writes, [1],
                         f"floor did not hold with {len(dense)} Reploids in "
                         f"range - wrote {writes}")

    async def test_not_held_outside_gameplay(self) -> None:
        # Writing lives is a write to the SAVE STRUCT, so it inherits the same
        # rule as every other one: only when the struct is provably live. A
        # menu or a stage load can sit on stale bytes that look like 9 lives
        # next to a Reploid, and taking a life there would be a silent theft
        # with nothing to show for it.
        client, ctx = MMX5Client(), self._ctx()
        await run_watcher(make_save(max_hp=0x30, lives=9), mode=0x0C,
                          client=client, ctx=ctx, stage_id=IZZY_STAGE,
                          player_x=380, player_y=650)
        self.assertEqual(self._lives_writes(ctx), [],
                         "took a life while not in gameplay")

    async def test_not_held_before_the_save_is_trusted(self) -> None:
        client, ctx = MMX5Client(), self._ctx()
        await run_watcher(make_save(max_hp=0x30, lives=9), client=client,
                          ctx=ctx, stage_id=IZZY_STAGE, settled=False,
                          player_x=380, player_y=650)
        self.assertEqual(self._lives_writes(ctx), [],
                         "took a life off an untrusted save struct")

    async def test_rescue_at_the_cap_now_produces_a_check(self) -> None:
        """End to end: the case the tester could not collect at all."""
        client, ctx = MMX5Client(), self._ctx()
        # Arrives at 9 lives; the client drops them to 8...
        await self._poll(client, ctx, lives=9, player_x=380, player_y=650)
        self.assertEqual(self._lives_writes(ctx), [8])
        # ...so the rescue is granted, taking them back to 9, and is seen.
        await self._poll(client, ctx, lives=9, player_x=380, player_y=650)
        self.assertIn(self._loc('Izzy Glow - Reploid 1'),
                      ctx.checked_location_ids())

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
