"""Boss Rush rematch checks.

Detection is a client-side watcher (live session 2026-08-08): a rematch runs
in the standard boss-HP slot 0x800920EC, and the fight is IDENTIFIED by a
fingerprint of the boss module the portal streamed to 0x800FA000. The kill
condition is a conjunction - rush stage + gameplay mode + known fingerprint +
observed HP fill + HP zero + player alive + not already sent this arming -
and every term exists because dropping it produced (or would produce) a
concrete false check. Those are the traps this file pins:

- the module PERSISTS after a fight, so fingerprint-present must not mean
  fight-in-progress (corridor blips on the stale HP byte);
- a mid-fight player death zeroes nothing we can trust, so it must never
  read as a boss kill;
- own-stage Maverick fights use modules carrying the SAME fingerprints, so
  the stage gate is what keeps normal boss kills from firing rematches;
- Sigma's own fights happen in the SAME stage, so an unknown fingerprint
  must send nothing.

REGRESSION, 2026-08-09 - the phantom-check report. v0.4.0 shipped a 16-byte
fingerprint, and a tester received Squid Adler's and The Skiver's rematch
checks without fighting either. Those two values turned out to occur 11 and
40 times on the disc (Skiver's 12 times in the base EXE alone - it is a
function epilogue followed by the next prologue). The window is now 256
bytes, verified unique across the whole disc for all eight bosses, and the
kill additionally requires that the client SAW the bar fill during the
current arming. `test_derives_the_table_from_a_real_disc` re-derives the
shipped table from a disc when one is available.

NOTE ON FIXTURES. The real fingerprints are 256 bytes of verbatim game code
each, so they are stored as sha256 digests in client.py and are NOT
reproduced here - shipping 2 KB of the game's own code in the Archipelago
repo is the same thing the unpatcher's vanilla manifest was kept out for.
The detection tests below therefore run against a SYNTHETIC table; the real
one is covered structurally, and against a disc when present.
"""
import hashlib
import os
import struct
import unittest
from unittest import mock

import worlds.mmx5.client as c
from worlds.mmx5 import names
from worlds.mmx5.client import MMX5Client
from worlds.mmx5.locations import location_table

from . import MMX5TestBase
from .test_client import FakeContext, make_save, run_watcher


def _fake_module(index: int) -> bytes:
    """A stand-in for one boss module's 256-byte window. Distinct per boss and
    deliberately not derived from any real module."""
    return bytes(((index * 37 + i * 5) & 0xFF) for i in range(c.RUSH_FP_LEN))


FP = {stage: _fake_module(i) for i, stage in enumerate(names.STAGES)}
FAKE_TABLE = {hashlib.sha256(b).hexdigest(): stage for stage, b in FP.items()}


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
        self.assertEqual(len(c.RUSH_FP_TO_STAGE), 8,
                         "a duplicate digest would silently drop a boss")
        for digest in c.RUSH_FP_TO_STAGE:
            self.assertRegex(digest, r"^[0-9a-f]{64}$",
                             "table keys are sha256 hexdigests of the window")

    def test_window_is_wide_enough_to_be_an_identity(self) -> None:
        # The v0.4.0 phantom-check bug in one assertion. 16 bytes at a fixed
        # offset is a sample of whatever code sits there: two of the eight
        # shipped values were ordinary function epilogue/prologue boilerplate
        # occurring 11 and 40 times on the disc. Everything is unique from 128
        # bytes; 256 is what ships.
        self.assertGreaterEqual(c.RUSH_FP_LEN, 128)

    def test_peak_threshold_clears_the_documented_stale_value(self) -> None:
        # ram-notes records the boss-HP byte holding stale garbage outside
        # fights, with 16 observed at stage entry. The original threshold of 8
        # sat BELOW that, so a stale byte could validate a kill on its own.
        # Real fights fill to 40+ (Squid 58, Axle 53).
        self.assertGreater(c.RUSH_MIN_PEAK, 16)
        self.assertLess(c.RUSH_MIN_PEAK, 40)

    @unittest.skipUnless(os.environ.get("MMX5_DISC"),
                         "set MMX5_DISC to a Megaman X5 .bin to re-derive")
    def test_derives_the_table_from_a_real_disc(self) -> None:
        """Rebuild RUSH_FP_TO_STAGE from the disc and demand it match.

        This is the only test that can catch a transcription error in the
        shipped digests, because the window is not otherwise reproducible from
        anything in this repo. Skipped by default - a disc is not (and must
        not be) checked in.

        ROCK_X5.BIN: ISO LBA 23693, 676 sectors, Mode2 Form1 (2048 payload
        bytes at +0x18 of each 2352-byte sector). Its directory is 59
        (u32 sector, u32 size) pairs. Boss module = chunk 29 + stage_id,
        loaded at RAM 0x800FA000, so the probe is at module offset 0x300.
        """
        path = os.environ["MMX5_DISC"]
        sector, payload, poff = 2352, 2048, 0x18
        with open(path, "rb") as f:
            f.seek(23693 * sector)
            raw = f.read(676 * sector)
        rock = b"".join(raw[i * sector + poff: i * sector + poff + payload]
                        for i in range(676))

        chunks = []
        for i in range(64):
            sec, size = struct.unpack_from("<II", rock, i * 8)
            if sec == 0 and size == 0:
                break
            chunks.append((sec, size))
        self.assertEqual(len(chunks), 59, "unexpected ROCK_X5.BIN directory")

        probe = c.RUSH_FP_ADDR - 0x0FA000
        derived = {}
        # STAGE_ID_TO_NAME, never enumerate(names.STAGES): that tuple is in
        # stage-SELECT order (Grizzly, Duff, Squid, Izzy, Dizzy, Skiver,
        # Mattrex, Axle), not stage-id order. Writing this test the obvious
        # way mismapped four bosses and it took a disc to notice - the same
        # "never infer a stage id from sequence" trap ram-notes records for
        # the endgame ids.
        for stage_id in range(1, 9):
            stage = c.STAGE_ID_TO_NAME[stage_id]
            sec, size = chunks[29 + stage_id]
            base = sec * payload
            window = rock[base + probe: base + probe + c.RUSH_FP_LEN]
            self.assertEqual(len(window), c.RUSH_FP_LEN)
            derived[hashlib.sha256(window).hexdigest()] = stage
        self.assertEqual(derived, c.RUSH_FP_TO_STAGE,
                         "shipped table does not match this disc")


class TestRematchDetection(unittest.IsolatedAsyncioTestCase):
    """Runs against FAKE_TABLE - see the fixtures note in the module docstring."""

    def setUp(self) -> None:
        patcher = mock.patch.dict(c.RUSH_FP_TO_STAGE, FAKE_TABLE, clear=True)
        patcher.start()
        self.addCleanup(patcher.stop)
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

    def _send_count(self, ctx, stage) -> int:
        """How many times this rematch was SENT, not whether it is checked.
        The distinction matters for the one-send-per-arming rule: the id stays
        in the checked set forever, so only counting messages can show a
        resident module re-firing."""
        loc = self._loc(stage)
        return sum(msg["locations"].count(loc) for msg in ctx.sent_msgs
                   if msg.get("cmd") == "LocationChecks" and loc in msg["locations"])

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
        # TIGHTENED 2026-08-09: this used to be two polls, a filled value then
        # zero. That is no longer a kill, deliberately - the first poll after a
        # module loads is a BASELINE, not evidence, and "arrived at a high
        # value, then zero" is precisely the stale-byte false positive that
        # sent a tester phantom checks. A real fight is observably preceded by
        # a low reading (the byte sits at 0 after the previous kill) or by a
        # rise, so the sequence below is what play actually looks like.
        client, ctx = MMX5Client(), self._ctx()
        await self._poll(client, ctx, rush_hp=0, rush_fp=FP[names.KRAKEN])
        await self._poll(client, ctx, rush_hp=58, rush_fp=FP[names.KRAKEN])
        self.assertNotIn(self._loc(names.KRAKEN), ctx.checked_location_ids())
        await self._poll(client, ctx, rush_hp=0, rush_fp=FP[names.KRAKEN])
        got = ctx.checked_location_ids()
        self.assertIn(self._loc(names.KRAKEN), got)
        for stage in names.STAGES:
            if stage != names.KRAKEN:
                self.assertNotIn(self._loc(stage), got)

    async def test_fill_completed_between_polls_still_counts(self) -> None:
        # The ramp is ~1 second and polls are sparser, so the client will
        # often never see an intermediate value. Arming at 0 (where the byte
        # sits after the previous kill) and then seeing fight-scale HP is
        # enough - otherwise the strict-rise rule would silently drop real
        # kills, and a missed rematch is only recoverable by redoing the rush.
        client, ctx = MMX5Client(), self._ctx()
        await self._poll(client, ctx, rush_hp=0, rush_fp=FP[names.DINOREX])
        await self._poll(client, ctx, rush_hp=53, rush_fp=FP[names.DINOREX])
        await self._poll(client, ctx, rush_hp=0, rush_fp=FP[names.DINOREX])
        self.assertEqual(self._rematch_ids(ctx), {self._loc(names.DINOREX)})

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
        # A full, legitimate fill-and-kill on a location the server already
        # has: the dedup must hold on its own, not because the fill rule
        # happened to reject the sequence.
        client, ctx = MMX5Client(), self._ctx()
        ctx.checked_locations.add(self._loc(names.KRAKEN))
        await self._poll(client, ctx, rush_hp=0, rush_fp=FP[names.KRAKEN])
        await self._poll(client, ctx, rush_hp=58, rush_fp=FP[names.KRAKEN])
        await self._poll(client, ctx, rush_hp=0, rush_fp=FP[names.KRAKEN])
        self.assertEqual(self._rematch_ids(ctx), set())

    # ---- the 2026-08-09 phantom-check regressions -----------------------
    # Each of these is a state the client was actually observed (or proven)
    # to sit in, which the shipped v0.4.0 watcher would have sent a check
    # from. They are the reason the fill and one-send-per-arming terms exist.

    async def test_stale_high_byte_then_zero_sends_nothing(self) -> None:
        # ram-notes: the boss-HP byte holds stale garbage outside fights, 16
        # observed at stage entry. The old threshold was 8, so a stale byte
        # that later dropped to 0 cleared every term on its own. A stale value
        # does not CLIMB, so there is no fill and there must be no check -
        # even when the stale value is above the new threshold.
        client, ctx = MMX5Client(), self._ctx()
        await self._poll(client, ctx, rush_hp=40, rush_fp=FP[names.KRAKEN])
        await self._poll(client, ctx, rush_hp=40, rush_fp=FP[names.KRAKEN])
        await self._poll(client, ctx, rush_hp=0, rush_fp=FP[names.KRAKEN])
        self.assertEqual(self._rematch_ids(ctx), set(),
                         "a stale byte dropping to zero read as a kill")

    async def test_corridor_dump_state_sends_nothing(self) -> None:
        # ramdump_rematch_before_f369766 / _after_f372037, exactly as captured:
        # stage 0x0C, mode 0x0A, a known module resident, boss HP 0, player
        # alive - and no fight happening. Every term of the v0.4.0 conjunction
        # except the peak holds here while simply walking between portals.
        client, ctx = MMX5Client(), self._ctx()
        for _ in range(5):
            await self._poll(client, ctx, rush_hp=0, rush_fp=FP[names.FIREFLY],
                             player_hp=40)
        self.assertEqual(self._rematch_ids(ctx), set())

    async def test_one_send_per_arming(self) -> None:
        # After a kill the module STAYS resident and the byte STAYS 0 for
        # 600+ frames. Every later poll must be silent rather than re-firing.
        client, ctx = MMX5Client(), self._ctx()
        await self._poll(client, ctx, rush_hp=20, rush_fp=FP[names.KRAKEN])
        await self._poll(client, ctx, rush_hp=58, rush_fp=FP[names.KRAKEN])
        await self._poll(client, ctx, rush_hp=0, rush_fp=FP[names.KRAKEN])
        self.assertEqual(self._send_count(ctx, names.KRAKEN), 1)
        for _ in range(3):
            await self._poll(client, ctx, rush_hp=0, rush_fp=FP[names.KRAKEN])
        self.assertEqual(self._send_count(ctx, names.KRAKEN), 1,
                         "resident module re-fired without a new portal")

    async def test_rearming_requires_a_module_change(self) -> None:
        # The rush resets on stage re-entry, so a refight is legitimate - but
        # only after a portal streams the module in again. Same module, second
        # fill, must still be one send; a genuine reload then re-arms.
        client, ctx = MMX5Client(), self._ctx()
        await self._poll(client, ctx, rush_hp=20, rush_fp=FP[names.KRAKEN])
        await self._poll(client, ctx, rush_hp=58, rush_fp=FP[names.KRAKEN])
        await self._poll(client, ctx, rush_hp=0, rush_fp=FP[names.KRAKEN])
        self.assertEqual(self._send_count(ctx, names.KRAKEN), 1)
        # A different module loads (another portal), then Squid's again.
        await self._poll(client, ctx, rush_hp=0, rush_fp=FP[names.GRIZZLY])
        await self._poll(client, ctx, rush_hp=20, rush_fp=FP[names.KRAKEN])
        await self._poll(client, ctx, rush_hp=58, rush_fp=FP[names.KRAKEN])
        await self._poll(client, ctx, rush_hp=0, rush_fp=FP[names.KRAKEN])
        self.assertEqual(self._send_count(ctx, names.KRAKEN), 2,
                         "a genuine refight after a module reload was lost")

    async def test_fill_below_threshold_sends_nothing(self) -> None:
        # A real rise, but nowhere near fight scale. Rematches fill to 40+.
        client, ctx = MMX5Client(), self._ctx()
        await self._poll(client, ctx, rush_hp=4, rush_fp=FP[names.PEGASUS])
        await self._poll(client, ctx, rush_hp=12, rush_fp=FP[names.PEGASUS])
        await self._poll(client, ctx, rush_hp=0, rush_fp=FP[names.PEGASUS])
        self.assertEqual(self._rematch_ids(ctx), set())

    async def test_death_drops_the_fill_not_just_the_peak(self) -> None:
        # A player death mid-fight must retire the WHOLE arming, the observed
        # fill included - not merely the peak.
        #
        # The sequence that separates the two: the player dies, respawns at
        # the portal room with the boss still alive and its bar still high
        # (peak recovers on its own from that reading), then runs out of lives
        # and leaves, which clears the byte without anybody killing anything.
        # If the death only reset the peak, the dead fight's fill would still
        # be on record and that final zero would send a check for a boss that
        # is alive and unbeaten.
        client, ctx = MMX5Client(), self._ctx()
        await self._poll(client, ctx, rush_hp=20, rush_fp=FP[names.KRAKEN])
        await self._poll(client, ctx, rush_hp=58, rush_fp=FP[names.KRAKEN])
        await self._poll(client, ctx, rush_hp=58, rush_fp=FP[names.KRAKEN],
                         player_hp=0)
        # Respawned; boss untouched and still at fight scale.
        await self._poll(client, ctx, rush_hp=58, rush_fp=FP[names.KRAKEN])
        await self._poll(client, ctx, rush_hp=0, rush_fp=FP[names.KRAKEN])
        self.assertEqual(self._rematch_ids(ctx), set(),
                         "a dead fight's observed fill validated a later zero")

    async def test_death_then_a_real_refight_still_counts(self) -> None:
        # The mirror of the above: retiring the arming must not make the boss
        # permanently undetectable. Dying and beating it properly still sends.
        client, ctx = MMX5Client(), self._ctx()
        await self._poll(client, ctx, rush_hp=20, rush_fp=FP[names.KRAKEN])
        await self._poll(client, ctx, rush_hp=58, rush_fp=FP[names.KRAKEN],
                         player_hp=0)
        await self._poll(client, ctx, rush_hp=0, rush_fp=FP[names.KRAKEN])
        await self._poll(client, ctx, rush_hp=58, rush_fp=FP[names.KRAKEN])
        await self._poll(client, ctx, rush_hp=0, rush_fp=FP[names.KRAKEN])
        self.assertEqual(self._rematch_ids(ctx), {self._loc(names.KRAKEN)},
                         "a legitimate kill after a death was lost")

    async def test_every_boss_can_be_detected(self) -> None:
        # A per-boss smoke test: no boss is structurally undetectable (a
        # typo'd or duplicated table entry would drop one silently).
        for stage in names.STAGES:
            client, ctx = MMX5Client(), self._ctx()
            await self._poll(client, ctx, rush_hp=20, rush_fp=FP[stage])
            await self._poll(client, ctx, rush_hp=58, rush_fp=FP[stage])
            await self._poll(client, ctx, rush_hp=0, rush_fp=FP[stage])
            self.assertEqual(self._rematch_ids(ctx), {self._loc(stage)},
                             f"{stage} rematch was not detectable")
