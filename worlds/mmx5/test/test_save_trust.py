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

from .test_client import make_save, run_watcher

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
