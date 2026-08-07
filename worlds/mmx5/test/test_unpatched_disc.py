"""An unpatched disc must hold everything, not run in "hybrid mode".

REPORTED LIVE 2026-08-06. A tester in an 8-player multiworld saw their world
blast items out to everyone the moment they started: every Boss Defeated, DNA
Reward and DNA Part check fired without a single boss being beaten. The first
guess was a reused save; it was not.

The mechanism: on a disc the probe reported as vanilla, the client wrote
AP-granted weapons into 0x800D1C4C - the byte the game uses to record boss
kills, and the byte check detection reads as ground truth for all 24 of those
locations. So each weapon received from the multiworld marked its boss defeated
and fired three checks. Eight weapons, 24 false checks, items released to seven
other players, unrecoverable.

Hybrid mode predates the disc patch and the module header always called it
interim. Every supported flow produces a patched disc - the .apmmx5 IS the
delivery mechanism - so it was unreachable in correct use and destructive in
incorrect use. It is now refused.

Note these tests could not have been written before `run_watcher` grew a
`patch_probe` parameter: the harness hard-coded a PATCHED probe, so nothing in
the suite could reach this path at all. A test default that silently excludes a
whole code path is how this survived to a release.
"""
import unittest
from types import SimpleNamespace

import worlds.mmx5.client as c
from worlds.mmx5 import names
from worlds.mmx5.client import MMX5Client
from worlds.mmx5.items import item_table
from worlds.mmx5.locations import location_table

from .test_client import FakeContext, make_save, run_watcher

WEAPON_CODES = {item_table[w].code: w for w in c.WEAPON_TO_BIT}


def ctx_with_all_weapons() -> FakeContext:
    """A player who has RECEIVED all 8 weapons and beaten nothing."""
    ctx = FakeContext()
    ctx.slot_data = {"goal": 0, "boss_difficulty": 1}
    ctx.item_names = SimpleNamespace(
        lookup_in_game=lambda code: WEAPON_CODES.get(code, ""))
    ctx.items_received = [SimpleNamespace(item=code) for code in WEAPON_CODES]
    return ctx


BOSS_IDS = {location_table[names.boss_location(s)] for s in names.STAGES}
DNA_IDS = {location_table[names.dna_location(s)] for s in names.STAGES}
PART_IDS = {location_table[names.dna_part_location(s)] for s in names.STAGES}


class TestUnpatchedDiscHoldsEverything(unittest.IsolatedAsyncioTestCase):
    async def test_no_checks_at_all_on_an_unpatched_disc(self) -> None:
        ctx = await run_watcher(make_save(max_hp=0x20, intro=2, weapons=0x00),
                                client=MMX5Client(), ctx=ctx_with_all_weapons(),
                                patch_probe=c.PATCH_PROBE_VANILLA)
        self.assertEqual(ctx.checked_location_ids(), set(),
                         "an unpatched disc sent checks")

    async def test_never_writes_the_vanilla_kill_byte(self) -> None:
        # This is the write that caused the incident: granted weapons landing
        # in 0x1C4C, which detection then reads back as boss kills.
        ctx = await run_watcher(make_save(max_hp=0x20, intro=2, weapons=0x00),
                                client=MMX5Client(), ctx=ctx_with_all_weapons(),
                                patch_probe=c.PATCH_PROBE_VANILLA)
        addr = c.SAVE_BASE + c.OFF_WEAPONS
        self.assertEqual([w for w in ctx.writes if w[0] == addr], [],
                         "granted weapons were written into the boss-kill byte")

    async def test_a_save_already_poisoned_cannot_fire_either(self) -> None:
        # Someone who already played a hybrid session has 0x1C4C = 0xFF sitting
        # in their save. Gating only the grants would let it re-fire on the
        # next connect, so detection is gated too.
        ctx = await run_watcher(make_save(max_hp=0x20, intro=2, weapons=0xFF),
                                client=MMX5Client(), ctx=ctx_with_all_weapons(),
                                patch_probe=c.PATCH_PROBE_VANILLA)
        self.assertEqual(ctx.checked_location_ids(), set(),
                         "a poisoned save re-fired its false checks")

    async def test_it_says_why(self) -> None:
        client = MMX5Client()
        with self.assertLogs("Client", level="ERROR") as logs:
            await run_watcher(make_save(max_hp=0x20, intro=2, weapons=0x00),
                              client=client, ctx=ctx_with_all_weapons(),
                              patch_probe=c.PATCH_PROBE_VANILLA)
        joined = " ".join(logs.output)
        self.assertIn("NOT AP-patched", joined)
        self.assertIn(".apmmx5", joined)   # names the remedy, not just the fault


class TestUnpatchedDiscWritesNothing(unittest.IsolatedAsyncioTestCase):
    """The hard stop must precede every writer. It used to sit BELOW the
    boss-HP / DNA-Part / stage-unlock blocks, so an unpatched disc still had
    Parts granted, vanilla Parts suppressed and stages locked - "holds all
    checks and items" was not actually true."""

    async def test_no_writes_at_all(self) -> None:
        ctx = ctx_with_all_weapons()
        ctx.slot_data = {"goal": 0, "boss_difficulty": 1,
                         "dna_parts_in_pool": 1, "stage_unlocks": 1,
                         "boss_hp_randomization": 1}
        # A received DNA Part is what the parts writer would commit to
        # 0x1C84 if it still ran ahead of the stop.
        part_code = item_table[names.SPEEDSTER].code
        lookup = dict(WEAPON_CODES)
        lookup[part_code] = names.SPEEDSTER
        ctx.item_names = SimpleNamespace(
            lookup_in_game=lambda code: lookup.get(code, ""))
        ctx.items_received.append(SimpleNamespace(item=part_code))
        await run_watcher(make_save(max_hp=0x20, intro=2),
                          client=MMX5Client(), ctx=ctx,
                          patch_probe=c.PATCH_PROBE_VANILLA)
        self.assertEqual(ctx.writes, [],
                         "an unpatched disc still wrote into the game")

    async def test_cannot_goal(self) -> None:
        # A goal can RELEASE every remaining location in this world - the
        # same blast radius as the phantom-check incident - so an unpatched
        # playthrough must not complete it.
        client = MMX5Client()
        ctx = FakeContext()
        # First poll resolves the probe to vanilla; second is the ending.
        await run_watcher(make_save(max_hp=0x20, intro=2), client=client,
                          ctx=ctx, patch_probe=c.PATCH_PROBE_VANILLA)
        await run_watcher(make_save(max_hp=0x00), mode=0x10, client=client,
                          ctx=ctx, patch_probe=c.PATCH_PROBE_VANILLA)
        self.assertFalse(
            any(m.get("cmd") == "StatusUpdate" for m in ctx.sent_msgs),
            "an unpatched disc completed the goal")


class TestPatchedDiscIsUnaffected(unittest.IsolatedAsyncioTestCase):
    """The fix must not cost a correctly-patched player anything."""

    async def test_receiving_weapons_fires_no_boss_checks(self) -> None:
        ctx = await run_watcher(make_save(max_hp=0x20, intro=2, weapons=0x00),
                                client=MMX5Client(), ctx=ctx_with_all_weapons(),
                                patch_probe=c.PATCH_PROBE_PATCHED)
        sent = ctx.checked_location_ids()
        self.assertEqual(sent & (BOSS_IDS | DNA_IDS | PART_IDS), set())
        self.assertIn(location_table[names.INTRO_CLEAR], sent)

    async def test_real_kills_still_fire_all_three_checks(self) -> None:
        ctx = await run_watcher(make_save(max_hp=0x20, intro=2, weapons=0xFF),
                                client=MMX5Client(), ctx=ctx_with_all_weapons(),
                                patch_probe=c.PATCH_PROBE_PATCHED)
        sent = ctx.checked_location_ids()
        self.assertEqual(len(sent & BOSS_IDS), 8)
        self.assertEqual(len(sent & DNA_IDS), 8)
        self.assertEqual(len(sent & PART_IDS), 8)

    async def test_grants_go_to_the_ap_byte(self) -> None:
        ctx = await run_watcher(make_save(max_hp=0x20, intro=2, weapons=0x00),
                                client=MMX5Client(), ctx=ctx_with_all_weapons(),
                                patch_probe=c.PATCH_PROBE_PATCHED)
        ap = [w for w in ctx.writes if w[0] == c.SAVE_BASE + c.OFF_AP_WEAPONS]
        vanilla = [w for w in ctx.writes if w[0] == c.SAVE_BASE + c.OFF_WEAPONS]
        self.assertTrue(ap, "weapons were not granted on a patched disc")
        self.assertEqual(vanilla, [], "granted weapons touched the kill byte")
