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


def seed_edits_for(**overrides) -> list:
    """Run patch_rom against a fake world and return its seed edits.

    ONE builder for every test that needs this. Two classes previously rolled
    their own, and both broke the moment a new option was added, because
    patch_rom reads options they had never heard of. Defaults live here so a
    new option needs updating in exactly one place."""
    from .. import Rom
    from ..options import Goal, LaunchOdds, PickupSanity, TextSkip

    opts = {"goal": Goal(Goal.option_sigma),
            "launch_odds": LaunchOdds(LaunchOdds.option_deterministic),
            "text_skip": TextSkip(0),
            "pickupsanity": PickupSanity(0)}
    for key, value in overrides.items():
        cls = {"goal": Goal, "launch_odds": LaunchOdds, "text_skip": TextSkip,
               "pickupsanity": PickupSanity}[key]
        opts[key] = cls(value)

    captured = {}

    class FakePatch:
        @staticmethod
        def write_file(name, data):
            captured[name] = data

    Rom.patch_rom(SimpleNamespace(options=SimpleNamespace(**opts)), FakePatch())
    return json.loads(captured["seed_edits.json"].decode("utf-8"))


# The stamp FakeContext's seed/slot hashes to - what a save this seed has
# already adopted carries.
TEST_SEED_STAMP = MMX5Client._seed_stamp(
    SimpleNamespace(seed_name="TESTSEED", auth="Player1"))


def make_save(max_hp: int, intro: int = 0, weapons: int = 0, hearts: int = 0,
              tanks: int = 0, stamp: int | None = None) -> bytes:
    """`stamp` defaults to TEST_SEED_STAMP - the faithful state of any save
    the client has seen before, since adoption happens at the first trusted
    poll. Pass `stamp=0` to model a save AP has never touched (the A3b hold
    is exactly about those - see test_save_trust.py)."""
    save = bytearray(mmx5_client.SAVE_LEN)
    save[mmx5_client.OFF_MAX_HP_X] = max_hp
    save[mmx5_client.OFF_INTRO] = intro
    save[mmx5_client.OFF_WEAPONS] = weapons
    save[mmx5_client.OFF_HEARTS] = hearts
    save[mmx5_client.OFF_TANKS] = tanks
    save[mmx5_client.OFF_STAMP] = TEST_SEED_STAMP if stamp is None else stamp
    return bytes(save)


async def run_watcher(save: bytes, mode: int = 0x0A, stage_id: int = 0,
                      client: MMX5Client | None = None,
                      ctx: FakeContext | None = None,
                      ring2: bytes | None = None,
                      hub_resident: bool = False,
                      slot_table: bytes | None = None,
                      patch_probe: bytes | None = None,
                      stub_probe: bytes | None = None,
                      settled: bool = True) -> FakeContext:
    """`hub_resident` makes the stage-select slot table's instruction anchor
    read as present, so the stage-unlock writer engages; `slot_table` seeds what
    that table currently holds (defaults to the vanilla ids).

    `patch_probe` overrides the AP-patch probe reply. It defaults to PATCHED,
    which is what normal play looks like - but that default also meant no test
    could reach the unpatched-disc path, and a real bug lived there unnoticed
    until a tester hit it (see test_unpatched_disc.py). `stub_probe` is the
    same override for the pickup-stub probe (default STUBBED), added so the
    stub-absent fallback path is not structurally untestable the way the
    unpatched path was.

    `settled=True` (the default) pre-seeds the full trust state - the
    check-stability signature, the previous-poll-was-gameplay flag and the
    0x0A gameplay anchor - so a single cycle behaves like a client that has
    already been polling in gameplay, which is what the real one does and what
    almost every test here means to simulate. Pass `settled=False` to exercise
    the connect/entry path, where the save is deliberately NOT believed until
    its bytes repeat across two gameplay polls."""
    ctx = ctx or FakeContext()
    client = client or MMX5Client()
    ring = bytes(mmx5_client.RING_SLOTS * 4)
    ring2 = ring2 or bytes(mmx5_client.RING2_SLOTS * 8)
    # The mode read covers 0x0D1C00..0x0D1C0F: mode at +0, stage id at +0x0C.
    mode_block = bytearray(0x10)
    mode_block[0] = mode
    mode_block[0x0C] = stage_id

    # Dispatch on the requested ADDRESS, not the request count - the main
    # cycle and the probe read are both three-wide, so counting would confuse
    # them (and silently did, until a tank test caught it).
    PROBE_REPLY = {
        mmx5_client.PATCH_PROBE_ADDR: (patch_probe if patch_probe is not None
                                       else mmx5_client.PATCH_PROBE_PATCHED),
        mmx5_client.STUB_PROBE_ADDR: (stub_probe if stub_probe is not None
                                      else mmx5_client.STUB_PROBE_STUBBED),
        mmx5_client.TANK_FIX_PROBE_ADDR: (
            mmx5_client.TANK_FIX_PATCHED if getattr(client, "tank_fix_present", None)
            else mmx5_client.TANK_FIX_VANILLA),
        mmx5_client.RING2_PROBE_ADDR: (
            mmx5_client.RING2_PROBE_STUBBED if getattr(client, "ring2_present", None)
            else mmx5_client.RING2_PROBE_VANILLA),
        mmx5_client.SLOT_TABLE_ANCHOR_ADDR: (
            mmx5_client.SLOT_TABLE_ANCHOR if hub_resident else b"\x00\x00\x00\x00"),
        mmx5_client.SLOT_TABLE_ADDR: (
            slot_table if slot_table is not None
            else bytes(mmx5_client.SLOT_TO_STAGE)),
    }

    async def fake_read(_ctx, requests):
        if requests[0][0] == 0x0D1C00:
            return [bytes(mode_block), save, ring, ring2]
        return [PROBE_REPLY.get(r[0], b"\x00\x00\x00\x00") for r in requests]

    async def fake_write(_ctx, writes, *_args, **_kwargs):
        ctx.writes.extend(writes)
        return True

    if settled:
        # Stand in for the previous polls: same bytes (stable), taken in
        # gameplay (prev-poll flag), with a trusted 0x0A already seen this
        # session (the anchor 0x0C trust requires). Without these a one-cycle
        # test can never trust the save.
        client.last_check_sig = (save[mmx5_client.OFF_INTRO], save[mmx5_client.OFF_WEAPONS],
                                 save[mmx5_client.OFF_HEARTS], save[mmx5_client.OFF_TANKS],
                                 save[mmx5_client.OFF_ARMOR])
        client.last_in_gameplay = True
        client.gameplay_anchored = True

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


class TestGoalEmitsNoDiscEdit(unittest.TestCase):
    """all_mavericks used to raise the story-chapter shuttle threshold from 6
    kills to 8. That edit worked exactly as disassembled and STILL did not gate
    the endgame - the chapter ladder never controlled access, so a player at 6
    kills reached Zero Space on a disc carrying it. It only delayed the story
    announcement and Dynamo. The gate is now ACT, client-side.

    This test exists to stop it coming back: no goal may emit a disc edit."""

    def test_no_goal_emits_a_disc_edit(self) -> None:
        from ..options import Goal
        for goal in (Goal.option_sigma, Goal.option_launch,
                     Goal.option_all_mavericks):
            self.assertEqual(seed_edits_for(goal=goal), [],
                             f"goal {goal} emitted a disc edit; the endgame "
                             f"gate belongs in the client (ACT), not the disc")

    def test_the_hub_region_still_resolves_separately(self) -> None:
        # Kept even though nothing patches there now: the hub and results
        # overlays share a RAM base and differ only by sector, and that mapping
        # is load-bearing research. If they ever collapse to one offset, a
        # future edit would silently land in unrelated code.
        from .. import disc
        hub = disc.addr_to_disc(0x800EEFBC, "hub overlay")
        results = disc.addr_to_disc(0x800EEFBC, "results overlay")
        self.assertNotEqual(hub, results)


class TestTextSkipSeedEdits(unittest.TestCase):
    """Text skip is two NOPs in the message state machine. Both must be emitted
    together - instant text without auto-advance just moves the waiting - and
    neither may appear when the option is off."""

    @staticmethod
    def edits_for(text_skip: int, goal_value: int | None = None) -> list:
        from ..options import Goal
        return seed_edits_for(
            text_skip=text_skip,
            goal=goal_value if goal_value is not None else Goal.option_sigma)

    def test_off_emits_no_text_edits(self) -> None:
        from .. import Rom
        addrs = {e["addr"] for e in self.edits_for(0)}
        self.assertNotIn(Rom.TEXT_INSTANT_ADDR, addrs)
        self.assertNotIn(Rom.TEXT_ADVANCE_ADDR, addrs)

    def test_on_emits_both_nops(self) -> None:
        from .. import Rom
        edits = {e["addr"]: e for e in self.edits_for(1)}
        for addr in (Rom.TEXT_INSTANT_ADDR, Rom.TEXT_ADVANCE_ADDR):
            self.assertIn(addr, edits, f"0x{addr:08X} missing")
            self.assertEqual(bytes.fromhex(edits[addr]["hex"]), Rom.TEXT_NOP)
            self.assertEqual(edits[addr]["region"], "SLUS exe")

    def test_the_goal_adds_nothing_to_the_disc(self) -> None:
        # all_mavericks is entirely client-side now, so a seed with it plus
        # text skip carries exactly the two text NOPs and nothing else.
        from ..options import Goal
        from .. import Rom
        addrs = {e["addr"] for e in self.edits_for(1, Goal.option_all_mavericks)}
        self.assertEqual(addrs, {Rom.TEXT_INSTANT_ADDR, Rom.TEXT_ADVANCE_ADDR})

    def test_the_patched_sites_hold_the_expected_vanilla_branches(self) -> None:
        # Guards against the addresses drifting: these are the two `beqz $v1`
        # branches the whole feature depends on. Ground truth is also checked
        # against the real disc by mmx5_build_patch.py's selftest.
        from .. import Rom
        self.assertEqual(Rom.TEXT_INSTANT_VANILLA, bytes.fromhex("02006010"))
        self.assertEqual(Rom.TEXT_ADVANCE_VANILLA, bytes.fromhex("ec006010"))


class TestLaunchOdds(unittest.IsolatedAsyncioTestCase):
    """`vanilla` restores the game's own roll and hands it a SCORE in the band
    matching the parts held, instead of the flat 0/1 that deterministic odds
    use. Bands (resolution ladder at 0x800FA0D8): 0x01-0x14 6.25%,
    0x15-0x28 12.5%, 0x29-0x3C 37.5%, 0x3D-0x50 75%, <=0 never."""

    @staticmethod
    async def score_for(goal: int, odds: int, weapons: int,
                        enigma: int = 0, shuttle: int = 0) -> int:
        ctx = FakeContext()
        ctx.slot_data = {"goal": goal, "boss_difficulty": 1, "launch_odds": odds}
        from ..items import item_table
        code_of = {n: d.code for n, d in item_table.items()}
        id_to_name = {d.code: n for n, d in item_table.items()}
        ctx.items_received = (
            [SimpleNamespace(item=code_of[names.ENIGMA_PART])] * enigma +
            [SimpleNamespace(item=code_of[names.SHUTTLE_PART])] * shuttle)
        ctx.item_names = SimpleNamespace(lookup_in_game=lambda c: id_to_name[c])
        client = MMX5Client()
        client.ap_patched = True
        save = bytearray(make_save(max_hp=0x20, weapons=weapons))
        save[mmx5_client.OFF_SCORE_MOD] = 0xFF   # forces a pin every time
        await run_watcher(bytes(save), client=client, ctx=ctx)
        addr = mmx5_client.SAVE_BASE + mmx5_client.OFF_SCORE_MOD
        writes = [w[1][0] for w in ctx.writes if w[0] == addr]
        return writes[-1] if writes else 0xFF

    async def test_deterministic_is_still_a_flat_flag(self) -> None:
        score = await self.score_for(mmx5_client.GOAL_SIGMA, 0, 0x03, enigma=4)
        self.assertEqual(score, 1, "deterministic odds should pin a flat 1")

    async def test_enigma_bands(self) -> None:
        # No parts -> 6.25%; any parts -> 12.5% (extra Enigma parts add
        # nothing in the original game either).
        V = mmx5_client.LAUNCH_ODDS_VANILLA
        none = await self.score_for(mmx5_client.GOAL_SIGMA, V, 0x03)
        some = await self.score_for(mmx5_client.GOAL_SIGMA, V, 0x03, enigma=1)
        self.assertEqual(none, mmx5_client.LAUNCH_SCORE_6)
        self.assertEqual(some, mmx5_client.LAUNCH_SCORE_12)

    async def test_shuttle_bands(self) -> None:
        V = mmx5_client.LAUNCH_ODDS_VANILLA
        SIX = 0x3F   # 6 kills -> shuttle era
        self.assertEqual(await self.score_for(mmx5_client.GOAL_SIGMA, V, SIX),
                         mmx5_client.LAUNCH_SCORE_12)
        self.assertEqual(await self.score_for(mmx5_client.GOAL_SIGMA, V, SIX, shuttle=2),
                         mmx5_client.LAUNCH_SCORE_37)
        self.assertEqual(await self.score_for(mmx5_client.GOAL_SIGMA, V, SIX, shuttle=3),
                         mmx5_client.LAUNCH_SCORE_75)

    async def test_all_mavericks_gate_beats_vanilla_odds(self) -> None:
        # A successful launch before 8 kills would open the endgame ahead of
        # the goal, so the gate has to win over any odds setting.
        score = await self.score_for(mmx5_client.GOAL_ALL_MAVERICKS,
                                     mmx5_client.LAUNCH_ODDS_VANILLA,
                                     0x3F, shuttle=4)
        self.assertEqual(score, 0,
                         "a launch could succeed before all 8 Mavericks were down")

    def test_vanilla_restores_the_disc_roll(self) -> None:
        from ..options import LaunchOdds
        from .. import Rom
        edits = {e["addr"]: e for e in
                 seed_edits_for(launch_odds=LaunchOdds.option_vanilla)}
        self.assertIn(Rom.LAUNCH_ROLL_ADDR, edits)
        self.assertEqual(bytes.fromhex(edits[Rom.LAUNCH_ROLL_ADDR]["hex"]),
                         Rom.LAUNCH_ROLL_VANILLA)
        self.assertEqual(edits[Rom.LAUNCH_ROLL_ADDR]["region"], "launch overlay")

    def test_deterministic_leaves_the_roll_neutralised(self) -> None:
        from .. import Rom
        addrs = {e["addr"] for e in seed_edits_for()}
        self.assertNotIn(Rom.LAUNCH_ROLL_ADDR, addrs)


class TestEndgameWithholding(unittest.IsolatedAsyncioTestCase):
    """ACT (0x800D1C79) is what actually opens Zero Space - live-verified by
    poking it from 5 to 2 and watching Zero Space vanish. The story-chapter
    ladder does NOT gate access; the disc edit that moved the shuttle era to 8
    kills only delayed the announcement, and a player at 6 kills still reached
    Zero Space. This is the real gate, and it matters because Sigma does not
    respawn: reach him short of 8 and the goal can never fire."""

    @staticmethod
    def ctx_for(goal: int) -> FakeContext:
        ctx = FakeContext()
        ctx.slot_data = {"goal": goal, "boss_difficulty": 1}
        return ctx

    @staticmethod
    def act_writes(ctx: FakeContext) -> list:
        addr = mmx5_client.SAVE_BASE + mmx5_client.OFF_INTRO
        return [w[1][0] for w in ctx.writes if w[0] == addr]

    async def test_endgame_is_withheld_below_eight_kills(self) -> None:
        client = MMX5Client()
        ctx = self.ctx_for(mmx5_client.GOAL_ALL_MAVERICKS)
        # Establish a legitimate pre-endgame ACT, then resolve the colony early.
        await run_watcher(make_save(max_hp=0x20, intro=2, weapons=0x3F),
                          client=client, ctx=ctx)
        await run_watcher(make_save(max_hp=0x20, intro=mmx5_client.ENDGAME_ACT,
                                    weapons=0x3F), client=client, ctx=ctx)
        self.assertIn(2, self.act_writes(ctx),
                      "Zero Space was left open at 6 kills - a player can reach "
                      "Sigma, kill him, and strand the run")

    async def test_it_is_given_back_at_eight(self) -> None:
        client = MMX5Client()
        ctx = self.ctx_for(mmx5_client.GOAL_ALL_MAVERICKS)
        await run_watcher(make_save(max_hp=0x20, intro=2, weapons=0x3F),
                          client=client, ctx=ctx)
        await run_watcher(make_save(max_hp=0x20, intro=mmx5_client.ENDGAME_ACT,
                                    weapons=0x3F), client=client, ctx=ctx)
        await run_watcher(make_save(max_hp=0x20, intro=2, weapons=0xFF),
                          client=client, ctx=ctx)
        self.assertIn(mmx5_client.ENDGAME_ACT, self.act_writes(ctx),
                      "the endgame was never handed back - Sigma unreachable")

    async def test_other_goals_are_untouched(self) -> None:
        for goal in (mmx5_client.GOAL_SIGMA, mmx5_client.GOAL_LAUNCH):
            client = MMX5Client()
            ctx = self.ctx_for(goal)
            await run_watcher(make_save(max_hp=0x20, intro=mmx5_client.ENDGAME_ACT,
                                        weapons=0x3F), client=client, ctx=ctx)
            self.assertEqual(self.act_writes(ctx), [],
                             f"goal {goal} had its story ACT rewritten")

    async def test_training_act_is_never_stored_as_a_restore_value(self) -> None:
        # Training stamps 0x0A into the same byte. It must not be remembered as
        # a legitimate pre-endgame value and written back into a real save.
        client = MMX5Client()
        ctx = self.ctx_for(mmx5_client.GOAL_ALL_MAVERICKS)
        await run_watcher(make_save(max_hp=0x20, intro=mmx5_client.TRAINING_ACT),
                          client=client, ctx=ctx)
        self.assertNotEqual(client.last_pre_endgame_act,
                            mmx5_client.TRAINING_ACT)


class TestStubAbsentFallback(unittest.IsolatedAsyncioTestCase):
    """`run_watcher` used to hard-code the stub probe to STUBBED, which made
    the stub-absent fallback structurally untestable - the same harness
    default that hid the hybrid-mode bug for four releases (see
    test_unpatched_disc.py)."""

    async def test_hearts_come_from_save_bits_without_the_stub(self) -> None:
        client = MMX5Client()
        ctx = await run_watcher(make_save(max_hp=0x20, intro=2, hearts=0x01),
                                client=client,
                                stub_probe=mmx5_client.STUB_PROBE_VANILLA)
        self.assertFalse(client.stub_present)
        stage = mmx5_client.HEART_BIT_TO_STAGE[0]
        self.assertIn(location_table[names.heart_location(stage)],
                      ctx.checked_location_ids(),
                      "without the stub, heart checks must come from save bits")


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
