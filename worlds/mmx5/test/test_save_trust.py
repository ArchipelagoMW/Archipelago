"""The save struct is only believed when it is provably a live save.

`save_sane` was the only gate for years, and its residency test is just
0x10 <= maxHP <= 0x40. RAM left over from a previous game satisfies that
exactly, and RAM survives a soft reset - so "I started a new save" says nothing
about what the struct held when the client read it.

A tester's world sent 24 phantom checks into an 8-player multiworld on
2026-08-06. On a patched disc the client cannot have written those bits, so
something was read that was not a live save. Rather than keep guessing which
route, these tests close the class:

  (a) checks require GAMEPLAY (mode 0x0A/0x0C), not merely a plausible-looking
      struct - the title screen, data-select menu and attract demo are exactly
      where leftover RAM gets mistaken for progress;
  (b) checks require the driving bytes to REPEAT across two polls, which
      removes the window where a struct being written mid-load reads as a
      plausible half-state.
"""
import unittest

import worlds.mmx5.client as c
from worlds.mmx5 import names
from worlds.mmx5.client import MMX5Client
from worlds.mmx5.locations import location_table

from .test_client import TEST_SEED_STAMP, make_save, run_watcher

BOSS = {location_table[names.boss_location(s)] for s in names.STAGES}
DNA = {location_table[names.dna_location(s)] for s in names.STAGES}
PART = {location_table[names.dna_part_location(s)] for s in names.STAGES}
ALL24 = BOSS | DNA | PART

# A save that looks completely finished. This is what stale RAM from someone
# else's playthrough looks like to the client.
FULL = dict(max_hp=0x20, intro=0x05, weapons=0xFF, hearts=0xFF, tanks=0xFF)


class TestChecksRequireGameplay(unittest.IsolatedAsyncioTestCase):
    async def _sent(self, mode):
        ctx = await run_watcher(make_save(**FULL), mode=mode, client=MMX5Client())
        return ctx.checked_location_ids()

    async def test_title_and_menu_modes_send_nothing(self) -> None:
        # Anything that is not gameplay or results. These are the states where
        # a soft-reset leaves the previous game's struct sitting in RAM.
        for mode in (0x00, 0x01, 0x02, 0x13, 0x14, 0x15):
            with self.subTest(mode=hex(mode)):
                self.assertEqual(await self._sent(mode), set(),
                                 f"mode {mode:#04x} sent checks outside gameplay")

    async def test_gameplay_and_results_do_send(self) -> None:
        for mode in (0x0A, 0x0C):
            with self.subTest(mode=hex(mode)):
                sent = await self._sent(mode)
                self.assertEqual(len(sent & ALL24), 24,
                                 f"mode {mode:#04x} failed to send real checks")


class TestChecksRequireAStableRead(unittest.IsolatedAsyncioTestCase):
    async def test_first_read_after_connect_is_not_believed(self) -> None:
        ctx = await run_watcher(make_save(**FULL), client=MMX5Client(),
                                settled=False)
        self.assertEqual(ctx.checked_location_ids(), set(),
                         "believed the save on the very first poll")

    async def test_second_identical_read_is_believed(self) -> None:
        client = MMX5Client()
        save = make_save(**FULL)
        await run_watcher(save, client=client, settled=False)     # poll 1
        ctx = await run_watcher(save, client=client, settled=False)  # poll 2
        self.assertEqual(len(ctx.checked_location_ids() & ALL24), 24,
                         "a stable save was still not believed")

    async def test_a_changing_struct_is_not_believed(self) -> None:
        # A struct mid-write reads differently each poll. Never trust it.
        client = MMX5Client()
        await run_watcher(make_save(max_hp=0x20, intro=1, weapons=0x00),
                          client=client, settled=False)
        ctx = await run_watcher(make_save(max_hp=0x20, intro=5, weapons=0xFF),
                                client=client, settled=False)
        self.assertEqual(ctx.checked_location_ids() & ALL24, set(),
                         "believed a struct whose bytes were still changing")


class TestTrustNeedsTwoGameplayPolls(unittest.IsolatedAsyncioTestCase):
    """The stability signature is recorded on menu polls too, and stale RAM
    never changes - so stability alone buys nothing against leftover RAM: a
    single poll landing in a gameplay mode would be trusted instantly off a
    signature the title screen established. Trust therefore also requires the
    PREVIOUS poll to have been gameplay."""

    async def test_first_gameplay_poll_off_a_menu_signature_is_not_believed(self) -> None:
        client = MMX5Client()
        save = make_save(**FULL)
        # Title screen: not trusted, but the signature gets recorded - and
        # stale RAM will read identical (= stable) forever after.
        await run_watcher(save, mode=0x13, client=client, settled=False)
        ctx = await run_watcher(save, mode=0x0A, client=client, settled=False)
        self.assertEqual(ctx.checked_location_ids(), set(),
                         "a single gameplay poll was believed off a signature "
                         "established at the title screen")
        ctx = await run_watcher(save, mode=0x0A, client=client, settled=False)
        self.assertEqual(len(ctx.checked_location_ids() & ALL24), 24,
                         "the second consecutive gameplay poll should be believed")

    async def test_results_mode_cannot_open_a_session(self) -> None:
        # 0x0C is not uniquely the results screen: it appears in the
        # stage-LOAD mode walk (0A->0B->0C->0E->..., ram-notes), where the
        # previous session's struct can still be resident. However long the
        # loader parks there, 0x0C must extend a live session (one trusted
        # 0x0A poll), never start one.
        client = MMX5Client()
        save = make_save(**FULL)
        await run_watcher(save, mode=0x13, client=client, settled=False)
        for poll in range(3):
            ctx = await run_watcher(save, mode=0x0C, client=client, settled=False)
            self.assertEqual(ctx.checked_location_ids(), set(),
                             f"0x0C poll {poll} was believed before any "
                             f"trusted gameplay this session")
        # Real gameplay anchors the session...
        await run_watcher(save, mode=0x0A, client=client, settled=False)
        ctx = await run_watcher(save, mode=0x0A, client=client, settled=False)
        self.assertEqual(len(ctx.checked_location_ids() & ALL24), 24)
        # ...and only then is a results screen believed (boss kills commit
        # there, so it must not stay distrusted once anchored).
        ctx = await run_watcher(save, mode=0x0C, client=client, settled=False)
        self.assertEqual(len(ctx.checked_location_ids() & ALL24), 24,
                         "an anchored results screen should be believed")


class TestUnstampedProgressIsHeld(unittest.IsolatedAsyncioTestCase):
    """Fix B stops STALE RAM; it deliberately trusts a genuinely resident
    save - and a save with pre-AP progress is exactly that (a vanilla
    playthrough on a cloned memcard, "Continue" on the wrong slot, a
    savestate predating this seed's first connect). The A3 stamp gate cannot
    catch those: a save this seed never touched is stamped 0, which passes.
    So an unstamped save that is already progressed is held until the player
    says adopting it is deliberate; a fresh one is stamped on first trusted
    sight."""

    async def test_progressed_unstamped_save_is_held(self) -> None:
        with self.assertLogs("Client", level="ERROR") as logs:
            ctx = await run_watcher(make_save(stamp=0, **FULL),
                                    client=MMX5Client())
        self.assertEqual(ctx.checked_location_ids(), set(),
                         "a progressed save this seed never touched fired checks")
        joined = " ".join(logs.output)
        self.assertIn("never been used", joined)
        self.assertIn("writebyte", joined)   # names the adoption remedy

    async def test_progressed_unstamped_save_receives_no_grants(self) -> None:
        from .test_unpatched_disc import ctx_with_all_weapons
        ctx = await run_watcher(make_save(stamp=0, **FULL),
                                client=MMX5Client(), ctx=ctx_with_all_weapons())
        self.assertEqual(ctx.writes, [],
                         "a held save was still written to")

    async def test_starting_the_game_before_connecting_is_not_held(self) -> None:
        # Boot the game, play the intro, THEN open the client - an ordinary
        # order of operations. ACT is 1 by then. Holding on ACT alone put that
        # player behind a Lua console command for a save that can claim
        # exactly one location, so ACT is not counted as progress.
        for act in (0x01, 0x02):
            with self.subTest(act=act):
                ctx = await run_watcher(make_save(max_hp=0x20, intro=act, stamp=0),
                                        client=MMX5Client())
                addr = c.SAVE_BASE + c.OFF_STAMP
                self.assertTrue([w for w in ctx.writes if w[0] == addr],
                                "a save with only the intro cleared was held")

    async def test_real_progress_is_still_held_whatever_act_says(self) -> None:
        ctx = await run_watcher(make_save(max_hp=0x20, intro=0x00, weapons=0x01,
                                          stamp=0), client=MMX5Client())
        self.assertEqual(ctx.checked_location_ids(), set(),
                         "a save with a boss kill was adopted silently")

    async def test_fresh_save_is_stamped_and_plays(self) -> None:
        ctx = await run_watcher(make_save(max_hp=0x20, stamp=0),
                                client=MMX5Client())
        addr = c.SAVE_BASE + c.OFF_STAMP
        self.assertEqual([w for w in ctx.writes if w[0] == addr],
                         [(addr, [TEST_SEED_STAMP], "MainRAM")],
                         "a fresh save was not adopted on first trusted sight")

    async def test_stamped_save_resumes_normally(self) -> None:
        # The stamped counterpart of the held case: same progress, this
        # seed's stamp - an ordinary resumed session must be untouched.
        ctx = await run_watcher(make_save(**FULL), client=MMX5Client())
        self.assertEqual(len(ctx.checked_location_ids() & ALL24), 24)


class TestEndgameLatchNeedsTrust(unittest.IsolatedAsyncioTestCase):
    """The Zero Space checks latch a high-water ACT, so a bad read there is
    permanent for the session - it cannot be undone by a later good read."""

    async def test_untrusted_read_does_not_latch_act(self) -> None:
        client = MMX5Client()
        await run_watcher(make_save(max_hp=0x20, intro=0x09, weapons=0xFF),
                          mode=0x13, client=client)      # hub: not gameplay
        self.assertEqual(client.max_act_seen, 0,
                         "latched ACT from a read that was not trusted")

    async def test_trusted_read_does_latch(self) -> None:
        client = MMX5Client()
        await run_watcher(make_save(max_hp=0x20, intro=0x09, weapons=0xFF),
                          mode=0x0A, client=client)
        self.assertEqual(client.max_act_seen, 0x09)


class TestNoRegressionForRealPlay(unittest.IsolatedAsyncioTestCase):
    async def test_ordinary_progress_still_reports(self) -> None:
        ctx = await run_watcher(
            make_save(max_hp=0x22, intro=0x02, weapons=0x03, hearts=0x01),
            mode=0x0A, client=MMX5Client())
        sent = ctx.checked_location_ids()
        self.assertIn(location_table[names.INTRO_CLEAR], sent)
        self.assertEqual(len(sent & BOSS), 2, "two kills should send two boss checks")

    async def test_training_still_blocked(self) -> None:
        ctx = await run_watcher(make_save(max_hp=0x20, intro=c.TRAINING_ACT,
                                          weapons=0x00),
                                mode=0x0A, client=MMX5Client())
        self.assertEqual(ctx.checked_location_ids(), set())
