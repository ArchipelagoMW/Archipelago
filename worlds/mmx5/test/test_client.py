"""Regression tests for the bugs found in the v0.1.0 test release.

Each test here corresponds to a failure a tester actually hit. They are
written to FAIL against v0.1.0 and pass after the fixes.
"""
import json
import unittest
from types import SimpleNamespace
from unittest import mock

import worlds._bizhawk as bizhawk
from NetUtils import ClientStatus
from worlds.LauncherComponents import components

from .. import client as mmx5_client
from ..client import MMX5Client
from ..locations import location_table
from .. import names


class FakeContext:
    """Minimal stand-in for BizHawkClientContext."""

    def __init__(self) -> None:
        self.server = object()
        self.slot = 1
        self.bizhawk_ctx = object()
        self.checked_locations = set()
        self.slot_data = {"goal": 0, "boss_difficulty": 1}
        self.seed_name = "TESTSEED"
        self.auth = "Player1"
        self.items_received = []
        self.item_names = SimpleNamespace(lookup_in_game=lambda code: "")
        self.sent_msgs = []
        self.writes = []

    async def send_msgs(self, msgs) -> None:
        self.sent_msgs.extend(msgs)

    def tank_writes(self):
        """Values written to the tank-ownership byte, in order."""
        addr = mmx5_client.SAVE_BASE + mmx5_client.OFF_TANKS
        return [w[1][0] for w in self.writes if w[0] == addr]

    def checked_location_ids(self) -> set:
        ids = set()
        for msg in self.sent_msgs:
            if msg.get("cmd") == "LocationChecks":
                ids.update(msg["locations"])
        return ids


def make_save(max_hp: int, intro: int = 0, weapons: int = 0, hearts: int = 0,
              tanks: int = 0) -> bytes:
    save = bytearray(mmx5_client.SAVE_LEN)
    save[mmx5_client.OFF_MAX_HP_X] = max_hp
    save[mmx5_client.OFF_INTRO] = intro
    save[mmx5_client.OFF_WEAPONS] = weapons
    save[mmx5_client.OFF_HEARTS] = hearts
    save[mmx5_client.OFF_TANKS] = tanks
    return bytes(save)


async def run_watcher(save: bytes, mode: int = 0x0A, stage_id: int = 0,
                      client: MMX5Client | None = None,
                      ctx: FakeContext | None = None) -> FakeContext:
    ctx = ctx or FakeContext()
    client = client or MMX5Client()
    ring = bytes(mmx5_client.RING_SLOTS * 4)
    # The mode read covers 0x0D1C00..0x0D1C0F: mode at +0, stage id at +0x0C.
    mode_block = bytearray(0x10)
    mode_block[0] = mode
    mode_block[0x0C] = stage_id

    # Dispatch on the requested ADDRESS, not the request count - the main
    # cycle and the probe read are both three-wide, so counting would confuse
    # them (and silently did, until a tank test caught it).
    PROBE_REPLY = {
        mmx5_client.PATCH_PROBE_ADDR: mmx5_client.PATCH_PROBE_PATCHED,
        mmx5_client.STUB_PROBE_ADDR: mmx5_client.STUB_PROBE_STUBBED,
        mmx5_client.TANK_FIX_PROBE_ADDR: (
            mmx5_client.TANK_FIX_PATCHED if getattr(client, "tank_fix_present", None)
            else mmx5_client.TANK_FIX_VANILLA),
    }

    async def fake_read(_ctx, requests):
        if requests[0][0] == 0x0D1C00:
            return [bytes(mode_block), save, ring]
        return [PROBE_REPLY.get(r[0], b"\x00\x00\x00\x00") for r in requests]

    async def fake_write(_ctx, writes, *_args, **_kwargs):
        ctx.writes.extend(writes)
        return True

    with mock.patch.object(bizhawk, "read", fake_read), \
            mock.patch.object(bizhawk, "write", fake_write), \
            mock.patch.object(bizhawk, "guarded_write", fake_write):
        await client.game_watcher(ctx)
    return ctx


class TestCheckDetectionGating(unittest.IsolatedAsyncioTestCase):
    """A tester got a phantom "Intro Stage - Clear" while the save-struct gate
    was logging False (max HP 0x00) - checks were being derived from stale RAM
    left over from a previous session, before any save was resident."""

    async def test_no_checks_from_unloaded_save_struct(self) -> None:
        # Max HP 0x00 => struct not resident. The other bytes are stale
        # garbage that happens to look like real progress.
        ctx = await run_watcher(make_save(max_hp=0x00, intro=0x05))
        self.assertEqual(ctx.checked_location_ids(), set(),
                         "checks were sent from a save struct that is not resident")

    async def test_stale_weapon_byte_cannot_fire_boss_checks(self) -> None:
        # The dangerous case: stale 0xFF in the weapons byte would have
        # falsely completed all 8 bosses plus their DNA locations.
        ctx = await run_watcher(make_save(max_hp=0x00, intro=0xFF, weapons=0xFF, hearts=0xFF))
        self.assertEqual(ctx.checked_location_ids(), set(),
                         "stale RAM falsely completed boss/DNA/heart checks")

    async def test_checks_still_sent_from_a_resident_save(self) -> None:
        # The fix must not break real detection: a loaded save reads sane.
        ctx = await run_watcher(make_save(max_hp=0x20, intro=0x01))
        self.assertIn(location_table[names.INTRO_CLEAR], ctx.checked_location_ids(),
                      "intro check was not sent from a valid save")

    async def test_boss_checks_from_a_resident_save(self) -> None:
        # One kill sends THREE checks - boss, DNA reward, DNA Part - all keyed
        # on the weapon bit alone. The reward prompt needs boss level 4+ and the
        # Part needs level 8+, so anything keyed on those would go missable on
        # an early kill or a `relaxed` seed. Hunter Rank feeds that same level
        # (SA +2 / GA +4 / PA +8), which is why it cannot gate a check either.
        ctx = await run_watcher(make_save(max_hp=0x20, weapons=0x01))
        sent = ctx.checked_location_ids()
        stage = next(s for s, w in names.BOSS_WEAPON.items()
                     if w == mmx5_client.WEAPON_BITS[0])
        self.assertIn(location_table[names.boss_location(stage)], sent)
        self.assertIn(location_table[names.dna_location(stage)], sent)
        self.assertIn(location_table[names.dna_part_location(stage)], sent,
                      "the level-8+ Part check did not ride the boss kill")


class TestTrainingMode(unittest.IsolatedAsyncioTestCase):
    """Training mode builds a pseudo-save in the same struct. Byte values here
    are taken from a live capture (Scripts/mmx5_act_log.txt, 2026-08-03):
    selecting Training wrote ACT=0x0A and max HP=0x20 in one frame, which
    satisfied the 0.1.1 residency gate and sent a phantom Intro Clear."""

    async def test_no_checks_in_training_mode(self) -> None:
        ctx = await run_watcher(make_save(max_hp=0x20, intro=0x0A))
        self.assertEqual(ctx.checked_location_ids(), set(),
                         "training mode sent checks into a real seed")

    async def test_real_save_still_sends_intro(self) -> None:
        # The same capture read ACT=0x02 / maxhp=0x2E / kills=0x23 off a
        # genuine mid-game save. That must keep working.
        ctx = await run_watcher(make_save(max_hp=0x2E, intro=0x02, weapons=0x23))
        self.assertIn(location_table[names.INTRO_CLEAR], ctx.checked_location_ids(),
                      "a real campaign save stopped sending the intro check")

    async def test_fresh_post_intro_save_still_sends_intro(self) -> None:
        # The tightest case: just after the intro, a real save looks like
        # training except for the ACT value (1 vs 0x0A) - kills are 0 in both.
        ctx = await run_watcher(make_save(max_hp=0x20, intro=0x01))
        self.assertIn(location_table[names.INTRO_CLEAR], ctx.checked_location_ids(),
                      "training detection swallowed a legitimate intro check")

    async def test_training_act_with_progress_is_not_treated_as_training(self) -> None:
        # Guard on the belt-and-braces term: if some late-game state ever did
        # reach ACT 0x0A, a save carrying real kills must NOT be suppressed.
        ctx = await run_watcher(make_save(max_hp=0x2E, intro=0x0A, weapons=0x23))
        self.assertIn(location_table[names.INTRO_CLEAR], ctx.checked_location_ids(),
                      "a save with real progress was misread as training")


class TestTankPickupProtection(unittest.IsolatedAsyncioTestCase):
    """A tank you already own is deleted by the item init one frame after it
    spawns (live capture 2026-08-03: owned Sub-Tank lived 2 frames, an un-owned
    Heart Tank 47). The client grants tanks by setting exactly those ownership
    bits, so receiving a tank destroyed the pickup that IS its check - making
    the location permanently uncollectable, and it can hold progression.

    On a disc carrying the fix none of this is needed. On an older disc the
    client withholds the one bit while the player stands in that stage."""

    GRIZZLY_ID = 1          # STAGE_ID_TO_NAME[1] == Grizzly Slash
    SUB1 = 0x10             # its tank bit

    async def _run(self, tank_fix: bool, stage_id: int, tanks: int,
                   checked=()) -> FakeContext:
        client = MMX5Client()
        client.ap_patched = True
        client.stub_present = True
        client.tank_fix_present = tank_fix
        ctx = FakeContext()
        ctx.checked_locations = set(checked)
        return await run_watcher(make_save(max_hp=0x20, tanks=tanks),
                                 stage_id=stage_id, client=client, ctx=ctx)

    async def test_bit_withheld_in_the_stage_that_owns_an_unchecked_tank(self) -> None:
        ctx = await self._run(tank_fix=False, stage_id=self.GRIZZLY_ID, tanks=self.SUB1)
        self.assertIn(0x00, ctx.tank_writes(),
                      "tank bit was not cleared, so the pickup will be deleted")

    async def test_not_withheld_once_the_location_is_checked(self) -> None:
        checked = {location_table[names.tank_location(names.GRIZZLY)]}
        ctx = await self._run(tank_fix=False, stage_id=self.GRIZZLY_ID,
                              tanks=self.SUB1, checked=checked)
        self.assertNotIn(0x00, ctx.tank_writes(),
                         "tank was withheld even though its check is already collected")

    async def test_not_withheld_in_a_different_stage(self) -> None:
        ctx = await self._run(tank_fix=False, stage_id=3, tanks=self.SUB1)
        self.assertNotIn(0x00, ctx.tank_writes(),
                         "tank withheld in a stage that does not own that pickup")

    async def test_patched_disc_never_withholds(self) -> None:
        # The whole point of the probe: on a fixed disc, withholding a tank
        # would be a pure downgrade for no benefit.
        ctx = await self._run(tank_fix=True, stage_id=self.GRIZZLY_ID, tanks=self.SUB1)
        self.assertNotIn(0x00, ctx.tank_writes(),
                         "patched disc should never withhold a tank")


class TestTankFixProbe(unittest.TestCase):
    def test_probe_words_match_the_disc_patch(self) -> None:
        from .. import disc
        patched = dict((a, p) for a, p, _r in disc.BASE_EDITS)
        addr = 0x80000000 + mmx5_client.TANK_FIX_PROBE_ADDR
        self.assertIn(addr, patched,
                      "client probes an address the disc patch does not touch")
        self.assertEqual(patched[addr], mmx5_client.TANK_FIX_PATCHED,
                         "probe's 'patched' word disagrees with what disc.py writes")

    def test_all_three_tank_masks_are_zeroed(self) -> None:
        from .. import disc
        patched = dict((a, p) for a, p, _r in disc.BASE_EDITS)
        for addr, why in ((0x80053804, "sub-tanks"), (0x80053838, "W-Tank"),
                          (0x80053848, "EX-Tank")):
            self.assertIn(addr, patched, f"{why} ownership mask not patched")
            word = int.from_bytes(patched[addr], "little")
            self.assertEqual(word & 0xFFFF, 0,
                             f"{why} mask immediate is not zero: {word:08X}")


class TestCapsuleArmorProtection(unittest.IsolatedAsyncioTestCase):
    """Owning the armor part a capsule grants can hide the vanilla route to
    that capsule. Live-proven 2026-08-03 in Squid Adler: with 0x1CA1 = 00 the
    jet-bike energy balls gating the capsule are present; granting Falcon Head
    (0x01) and re-entering makes them vanish, so the check is uncollectable."""

    SQUID_ID = 5            # STAGE_ID_TO_NAME[5] == Squid Adler
    FALCON_HEAD = 0x01

    async def _run(self, stage_id: int, armor: int, checked=()) -> FakeContext:
        client = MMX5Client()
        client.ap_patched = True
        client.stub_present = True
        client.tank_fix_present = True
        ctx = FakeContext()
        ctx.checked_locations = set(checked)
        save = bytearray(make_save(max_hp=0x20))
        save[mmx5_client.OFF_ARMOR] = armor
        return await run_watcher(bytes(save), stage_id=stage_id,
                                 client=client, ctx=ctx)

    def _armor_writes(self, ctx):
        addr = mmx5_client.SAVE_BASE + mmx5_client.OFF_ARMOR
        return [w[1][0] for w in ctx.writes if w[0] == addr]

    async def test_part_withheld_in_the_stage_its_capsule_belongs_to(self) -> None:
        ctx = await self._run(self.SQUID_ID, self.FALCON_HEAD)
        self.assertIn(0x00, self._armor_writes(ctx),
                      "Falcon Head not withheld - the capsule route stays hidden")

    async def test_not_withheld_once_the_capsule_is_checked(self) -> None:
        checked = {location_table[names.capsule_location(names.KRAKEN)]}
        ctx = await self._run(self.SQUID_ID, self.FALCON_HEAD, checked=checked)
        self.assertNotIn(0x00, self._armor_writes(ctx),
                         "armor withheld even though the capsule is already collected")

    async def test_not_withheld_in_other_stages(self) -> None:
        ctx = await self._run(1, self.FALCON_HEAD)     # Grizzly Slash
        self.assertNotIn(0x00, self._armor_writes(ctx),
                         "armor withheld in a stage whose capsule does not grant it")

    async def test_other_parts_are_left_alone(self) -> None:
        # Only the one bit may be cleared: stripping armor a player needs to
        # REACH a capsule would be worse than the bug being fixed.
        ctx = await self._run(self.SQUID_ID, 0xFF)
        for value in self._armor_writes(ctx):
            self.assertEqual(value, 0xFF & ~self.FALCON_HEAD,
                             f"withheld more than Falcon Head: {value:02X}")


class TestLaunchGoal(unittest.IsolatedAsyncioTestCase):
    """Vanilla launches the shuttle by itself once all eight Mavericks are
    down. The client used to fire the launch goal on that success flag alone,
    so a tester completed the goal holding 3 of 8 parts - contradicting the
    world's own completion_condition, which requires all 8."""

    def _save(self):
        save = bytearray(make_save(max_hp=0x20))
        save[mmx5_client.OFF_LAUNCH_FLAGS] = 0x80    # a launch succeeded
        return bytes(save)

    async def _run(self, enigma: int, shuttle: int) -> FakeContext:
        client = MMX5Client()
        client.ap_patched = True
        client.stub_present = True
        client.tank_fix_present = True
        ctx = FakeContext()
        ctx.slot_data = {"goal": mmx5_client.GOAL_LAUNCH, "boss_difficulty": 1}
        parts = ([names.ENIGMA_PART] * enigma) + ([names.SHUTTLE_PART] * shuttle)
        ctx.items_received = [SimpleNamespace(item=i) for i in range(len(parts))]
        ctx.item_names = SimpleNamespace(lookup_in_game=lambda code: parts[code])
        return await run_watcher(self._save(), client=client, ctx=ctx)

    def _goal_sent(self, ctx) -> bool:
        return any(m.get("cmd") == "StatusUpdate" for m in ctx.sent_msgs)

    async def test_story_launch_without_the_parts_does_not_complete(self) -> None:
        ctx = await self._run(enigma=2, shuttle=1)   # the tester's 3 of 8
        self.assertFalse(self._goal_sent(ctx),
                         "launch goal completed without collecting the 8 parts")

    async def test_launch_with_all_eight_parts_completes(self) -> None:
        ctx = await self._run(enigma=4, shuttle=4)
        self.assertTrue(self._goal_sent(ctx),
                        "launch goal did not complete with all 8 parts in hand")

    async def test_partial_set_still_not_enough(self) -> None:
        ctx = await self._run(enigma=4, shuttle=3)
        self.assertFalse(self._goal_sent(ctx),
                         "7 of 8 parts should not complete the launch goal")


class TestLauncherRegistration(unittest.TestCase):
    """v0.1.0 never registered its patch suffix, so the Launcher's Open Patch
    dialog did not list .apmmx5 and could not route the file to a handler."""

    def test_patch_suffix_declared(self) -> None:
        self.assertEqual(MMX5Client.patch_suffix, ".apmmx5")

    def test_suffix_reaches_the_bizhawk_launcher_component(self) -> None:
        bizhawk_components = [c for c in components if c.script_name == "BizHawkClient"]
        self.assertTrue(bizhawk_components, "BizHawk Client component missing")
        suffixes = bizhawk_components[0].file_identifier.suffixes
        self.assertIn(".apmmx5", suffixes,
                      "Open Patch will not offer .apmmx5 to players")

    def test_suffix_matches_the_patch_file_ending(self) -> None:
        from ..Rom import MMX5ProcedurePatch
        self.assertEqual(MMX5Client.patch_suffix, MMX5ProcedurePatch.patch_file_ending)


class TestAllMavericksGoal(unittest.IsolatedAsyncioTestCase):
    """The all_mavericks goal must not fire on an endgame the player reached
    early. Vanilla opens Zero Space when the colony situation resolves, and the
    story ladder (fn 0x800EEF14, popcount of 0x800D1C4C) offers the Enigma at 2
    kills and the shuttle at 6 - so failing both at 6 kills reaches Sigma two
    Mavericks short. Sigma does not respawn, so firing the goal there, or
    quietly doing nothing, both end the run: the first wrongly, the second
    permanently. The client holds the goal and says why."""

    @staticmethod
    def ctx_for(goal: int) -> FakeContext:
        ctx = FakeContext()
        ctx.slot_data = {"goal": goal, "boss_difficulty": 1}
        return ctx

    @staticmethod
    def goal_sent(ctx: FakeContext) -> bool:
        return any(m.get("cmd") == "StatusUpdate"
                   and m.get("status") == ClientStatus.CLIENT_GOAL
                   for m in ctx.sent_msgs)

    async def test_all_eight_then_the_ending_completes_the_goal(self) -> None:
        # The tally is taken during play and must survive into the ending,
        # where the save struct no longer reads sane.
        client = MMX5Client()
        ctx = self.ctx_for(mmx5_client.GOAL_ALL_MAVERICKS)
        await run_watcher(make_save(max_hp=0x20, weapons=0xFF), client=client, ctx=ctx)
        await run_watcher(make_save(max_hp=0x00), mode=0x10, client=client, ctx=ctx)
        self.assertTrue(self.goal_sent(ctx),
                        "goal did not fire after 8 kills - the tally did not "
                        "survive the ending, where the save reads insane")

    async def test_six_kills_does_not_complete_the_goal(self) -> None:
        client = MMX5Client()
        ctx = self.ctx_for(mmx5_client.GOAL_ALL_MAVERICKS)
        await run_watcher(make_save(max_hp=0x20, weapons=0x3F), client=client, ctx=ctx)
        await run_watcher(make_save(max_hp=0x00), mode=0x10, client=client, ctx=ctx)
        self.assertFalse(self.goal_sent(ctx),
                         "all_mavericks completed from a 6-kill endgame")

    async def test_the_sigma_goal_still_ignores_the_kill_count(self) -> None:
        # The permissive goal is unchanged: reaching the ending is the whole
        # requirement, however the player got there.
        client = MMX5Client()
        ctx = self.ctx_for(mmx5_client.GOAL_SIGMA)
        await run_watcher(make_save(max_hp=0x20, weapons=0x3F), client=client, ctx=ctx)
        await run_watcher(make_save(max_hp=0x00), mode=0x10, client=client, ctx=ctx)
        self.assertTrue(self.goal_sent(ctx),
                        "the sigma goal stopped firing on a valid ending")

    async def test_stale_ram_at_the_ending_cannot_fake_a_full_set(self) -> None:
        # Same failure shape as the phantom intro check: 0xFF in an unloaded
        # save struct scores 8. The tally only ever advances from a sane read.
        client = MMX5Client()
        ctx = self.ctx_for(mmx5_client.GOAL_ALL_MAVERICKS)
        await run_watcher(make_save(max_hp=0x00, weapons=0xFF), mode=0x10,
                          client=client, ctx=ctx)
        self.assertFalse(self.goal_sent(ctx),
                         "stale 0xFF in the weapons byte completed the goal")


class TestAllMavericksEndgameGate(unittest.IsolatedAsyncioTestCase):
    """Two independent doors open the endgame early, and each needs its own
    fix. The disc edit moves the shuttle era from 6 kills to 8. This covers the
    other one: a SUCCESSFUL Enigma resolves the colony by itself and is offered
    from 2 kills, so early launcher parts could open Zero Space without the
    shuttle ever being reached."""

    @staticmethod
    def ctx_with_parts(goal: int, part_name: str, count: int = 4,
                       noise: int = 3) -> FakeContext:
        """Build a context from the world's REAL item ids and a REAL name
        lookup, not a stub that answers every code with one name.

        A constant lambda hides the failure that actually matters: the client
        counts parts by mapping received item CODES through lookup_in_game, so
        a wrong id or a lookup that answers differently than expected breaks
        the count while a stubbed test still passes. The inventory below also
        carries unrelated items, because "count only the right ones" is the
        real job."""
        from ..items import item_table
        code_of = {name: data.code for name, data in item_table.items()}
        id_to_name = {data.code: name for name, data in item_table.items()}

        received = [SimpleNamespace(item=code_of[part_name])] * count
        # Unrelated items that must NOT be counted as launcher parts.
        for filler in (names.CSHOT, names.DARK_HOLD, names.SMALL_ENERGY)[:noise]:
            received.append(SimpleNamespace(item=code_of[filler]))
        # The OTHER launcher part must not be counted as this one either.
        other = (names.SHUTTLE_PART if part_name == names.ENIGMA_PART
                 else names.ENIGMA_PART)
        received.append(SimpleNamespace(item=code_of[other]))

        ctx = FakeContext()
        ctx.slot_data = {"goal": goal, "boss_difficulty": 1}
        ctx.items_received = received
        ctx.item_names = SimpleNamespace(
            lookup_in_game=lambda code: id_to_name[code])
        return ctx

    @staticmethod
    def score_mod_writes(ctx: FakeContext) -> list:
        addr = mmx5_client.SAVE_BASE + mmx5_client.OFF_SCORE_MOD
        return [w[1][0] for w in ctx.writes if w[0] == addr]

    async def run_powered(self, ctx: FakeContext, weapons: int,
                          score_mod: int) -> int:
        """Effective launch-score modifier after one cycle: the last value the
        client pinned, or the starting value if it left the byte alone. The
        client only writes on a difference, so "no write" is a RESULT, not an
        absence of one - asserting on writes alone would misread it."""
        client = MMX5Client()
        client.ap_patched = True
        save = bytearray(make_save(max_hp=0x20, weapons=weapons))
        save[mmx5_client.OFF_SCORE_MOD] = score_mod
        await run_watcher(bytes(save), client=client, ctx=ctx)
        writes = self.score_mod_writes(ctx)
        return writes[-1] if writes else score_mod

    async def test_enigma_is_not_powered_before_all_eight(self) -> None:
        ctx = self.ctx_with_parts(mmx5_client.GOAL_ALL_MAVERICKS, names.ENIGMA_PART)
        # 2 kills, full Enigma set, and the score already powered - the client
        # must pin it back down.
        powered = await self.run_powered(ctx, weapons=0x03, score_mod=1)
        self.assertEqual(powered, 0,
                         "a full Enigma set powered a launch at 2 kills, which "
                         "resolves the colony and opens the endgame early")

    async def test_the_full_set_still_powers_a_launch(self) -> None:
        # Positive control: at 8 kills the shuttle era is live and a complete
        # shuttle set must still work, or the goal becomes unreachable.
        ctx = self.ctx_with_parts(mmx5_client.GOAL_ALL_MAVERICKS, names.SHUTTLE_PART)
        powered = await self.run_powered(ctx, weapons=0xFF, score_mod=0)
        self.assertEqual(powered, 1,
                         "a full shuttle set did not power a launch at 8 kills")

    async def test_the_sigma_goal_still_powers_the_enigma_early(self) -> None:
        # The permissive goal keeps vanilla's story flavour untouched.
        ctx = self.ctx_with_parts(mmx5_client.GOAL_SIGMA, names.ENIGMA_PART)
        powered = await self.run_powered(ctx, weapons=0x03, score_mod=0)
        self.assertEqual(powered, 1,
                         "the sigma goal stopped powering the Enigma early")


class TestShuttleGateSeedEdit(unittest.TestCase):
    """The disc half of the gate. Goal-conditional: the launch goal NEEDS the
    shuttle at 6 kills and the sigma goal permits finishing short, so only
    all_mavericks gets the stricter disc."""

    @staticmethod
    def edits_for(goal_value: int) -> list:
        from ..options import Goal
        from .. import Rom
        captured = {}

        class FakePatch:
            @staticmethod
            def write_file(name, data):
                captured[name] = data

        world = SimpleNamespace(options=SimpleNamespace(goal=Goal(goal_value)))
        Rom.patch_rom(world, FakePatch())
        return json.loads(captured["seed_edits.json"].decode("utf-8"))

    def test_all_mavericks_moves_the_shuttle_era_to_eight(self) -> None:
        from ..options import Goal
        from .. import Rom
        edits = self.edits_for(Goal.option_all_mavericks)
        self.assertEqual(len(edits), 1, "expected exactly the shuttle-era edit")
        self.assertEqual(edits[0]["addr"], Rom.SHUTTLE_THRESHOLD_ADDR)
        self.assertEqual(edits[0]["region"], "hub overlay")
        self.assertEqual(bytes.fromhex(edits[0]["hex"]),
                         Rom.SHUTTLE_THRESHOLD_ALL_8)

    def test_other_goals_leave_the_disc_alone(self) -> None:
        from ..options import Goal
        for goal in (Goal.option_sigma, Goal.option_launch):
            self.assertEqual(self.edits_for(goal), [],
                             f"goal {goal} emitted a disc edit it did not ask for")

    def test_the_edit_resolves_through_the_hub_module(self) -> None:
        # The hub and results overlays load at the SAME RAM base from
        # DIFFERENT sectors, so naming the wrong region silently patches
        # unrelated code. These must not resolve to the same disc offset.
        from .. import disc, Rom
        hub = disc.addr_to_disc(Rom.SHUTTLE_THRESHOLD_ADDR, "hub overlay")
        results = disc.addr_to_disc(Rom.SHUTTLE_THRESHOLD_ADDR, "results overlay")
        self.assertNotEqual(hub, results,
                            "hub and results overlays resolved to one offset - "
                            "the region map no longer distinguishes them")


class TestGoalOptionWiring(unittest.TestCase):
    """The option values and the client's goal constants are declared in two
    places and must agree - slot_data carries the raw int between them."""

    def test_default_goal_is_all_mavericks(self) -> None:
        from ..options import Goal
        self.assertEqual(Goal.default, Goal.option_all_mavericks)

    def test_client_constants_match_the_option_values(self) -> None:
        from ..options import Goal
        self.assertEqual(mmx5_client.GOAL_SIGMA, Goal.option_sigma)
        self.assertEqual(mmx5_client.GOAL_LAUNCH, Goal.option_launch)
        self.assertEqual(mmx5_client.GOAL_ALL_MAVERICKS, Goal.option_all_mavericks)


if __name__ == "__main__":
    unittest.main()
