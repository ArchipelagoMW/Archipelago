"""Boss HP randomization: rolls, the restore that prevents compounding.

The lever is 0x800D1CA2 (live-proven boss max HP, 2026-08-05). It is ALSO the
Boss-Level accumulator - `0x1CA2 = min(0x1CA2 + level_raw, 0x7F)` at each stage
start - so the client must put the vanilla value back on leaving gameplay.
Without that the multiplier compounds every stage and pins to 127; the
compounding test below is the regression guard for exactly that.
"""
import unittest

import worlds.mmx5.client as c
from worlds.mmx5.client import MMX5Client

from .test_client import FakeContext, make_save, run_watcher

REGULAR = 2
CHAOTIC = 4


def save_with_boss_hp(value: int, **kw) -> bytes:
    save = bytearray(make_save(max_hp=0x20, intro=2, weapons=0x23, **kw))
    save[c.OFF_BOSS_HP] = value
    return bytes(save)


class TestBossHPRoll(unittest.TestCase):
    """The roll itself - no emulator involved."""

    def setUp(self) -> None:
        self.client = MMX5Client()
        self.ctx = FakeContext()
        self.ctx.slot_data = {"goal": 0, "boss_difficulty": 1,
                              "boss_hp_randomization": REGULAR}

    def test_off_returns_vanilla(self) -> None:
        self.ctx.slot_data["boss_hp_randomization"] = 0
        self.assertEqual(self.client._boss_hp_roll(self.ctx, 1, 75), 75)

    def test_deterministic(self) -> None:
        a = self.client._boss_hp_roll(self.ctx, 1, 75)
        b = self.client._boss_hp_roll(self.ctx, 1, 75)
        self.assertEqual(a, b, "same situation must give the same fight")

    def test_differs_by_stage(self) -> None:
        rolls = {self.client._boss_hp_roll(self.ctx, s, 75) for s in range(1, 9)}
        self.assertGreater(len(rolls), 1, "every stage rolled identically")

    def test_within_band(self) -> None:
        lo, hi = c.BOSS_HP_BANDS[REGULAR]
        for vanilla in (20, 40, 75, 100):
            r = self.client._boss_hp_roll(self.ctx, 3, vanilla)
            self.assertGreaterEqual(r, round(vanilla * lo) - 1)
            self.assertLessEqual(r, round(vanilla * hi) + 1)

    def test_clamped_to_engine_range(self) -> None:
        self.ctx.slot_data["boss_hp_randomization"] = CHAOTIC
        for vanilla in (1, 2, 120, 127):
            for stage in range(1, 20):
                r = self.client._boss_hp_roll(self.ctx, stage, vanilla)
                self.assertGreaterEqual(r, c.BOSS_HP_MIN)
                self.assertLessEqual(r, c.BOSS_HP_MAX)

    def test_never_zero(self) -> None:
        # A 0 would make bosses die instantly - the kill-boss cheat value.
        self.ctx.slot_data["boss_hp_randomization"] = CHAOTIC
        for stage in range(1, 30):
            self.assertGreater(self.client._boss_hp_roll(self.ctx, stage, 1), 0)


class TestBossHPApply(unittest.IsolatedAsyncioTestCase):
    def _ctx(self, mode=REGULAR) -> FakeContext:
        ctx = FakeContext()
        ctx.slot_data = {"goal": 0, "boss_difficulty": 1,
                         "boss_hp_randomization": mode}
        return ctx

    def _writes_to_boss_hp(self, ctx) -> list:
        addr = c.SAVE_BASE + c.OFF_BOSS_HP
        return [w[1][0] for w in ctx.writes if w[0] == addr]

    async def test_writes_rolled_value_in_gameplay(self) -> None:
        client = MMX5Client()
        ctx = await run_watcher(save_with_boss_hp(75), mode=0x0A,
                                stage_id=1, client=client, ctx=self._ctx())
        written = self._writes_to_boss_hp(ctx)
        self.assertTrue(written, "no boss HP write in gameplay")
        self.assertNotEqual(written[-1], 75)
        self.assertEqual(written[-1],
                         client._boss_hp_roll(ctx, 1, 75))

    async def test_option_off_writes_nothing(self) -> None:
        ctx = await run_watcher(save_with_boss_hp(75), mode=0x0A, stage_id=1,
                                client=MMX5Client(), ctx=self._ctx(mode=0))
        self.assertEqual(self._writes_to_boss_hp(ctx), [])

    async def test_restores_vanilla_on_leaving_gameplay(self) -> None:
        client = MMX5Client()
        ctx = self._ctx()
        await run_watcher(save_with_boss_hp(75), mode=0x0A, stage_id=1,
                          client=client, ctx=ctx)
        rolled = client.boss_hp_written
        self.assertIsNotNone(rolled)
        ctx2 = self._ctx()
        await run_watcher(save_with_boss_hp(rolled), mode=0x0C, stage_id=1,
                          client=client, ctx=ctx2)
        self.assertIn(75, self._writes_to_boss_hp(ctx2),
                      "vanilla value was not restored on leaving gameplay")

    async def test_does_not_compound_across_stages(self) -> None:
        """THE regression test. Overwriting without restoring makes our value
        the base for the next stage's accumulate; a few stages of that pins
        every boss at the 127 ceiling."""
        client = MMX5Client()
        vanilla = 40
        for stage in range(1, 7):
            ctx = self._ctx()
            await run_watcher(save_with_boss_hp(vanilla), mode=0x0A,
                              stage_id=stage, client=client, ctx=ctx)
            rolled = self._writes_to_boss_hp(ctx)[-1]
            self.assertLess(rolled, c.BOSS_HP_MAX,
                            f"stage {stage}: hit the 127 ceiling - compounding")
            # leave the stage; the game then accumulates from the RESTORED
            # vanilla, exactly as it would with no client attached
            ctx = self._ctx()
            await run_watcher(save_with_boss_hp(rolled), mode=0x0C,
                              stage_id=stage, client=client, ctx=ctx)
            restored = self._writes_to_boss_hp(ctx)
            self.assertIn(vanilla, restored, f"stage {stage}: no restore")
            vanilla = min(0x7F, vanilla + 11)   # the game's own accumulate

    async def test_savestate_load_midstage_reapplies_not_rerolls(self) -> None:
        """Savestates restore 0x1CA2 with the rest of RAM. A state taken
        earlier in the same stage hands back a STALE value; treating that as a
        fresh vanilla baseline would reroll from the wrong base and then
        restore the wrong number to the game's accumulator on exit."""
        client = MMX5Client()
        ctx = await run_watcher(save_with_boss_hp(75), mode=0x0A, stage_id=5,
                                client=client, ctx=self._ctx())
        rolled = self._writes_to_boss_hp(ctx)[-1]
        self.assertNotEqual(rolled, 75)
        # state load inside the same stage restores the pre-write value
        ctx2 = self._ctx()
        await run_watcher(save_with_boss_hp(75), mode=0x0A, stage_id=5,
                          client=client, ctx=ctx2)
        self.assertEqual(self._writes_to_boss_hp(ctx2)[-1], rolled,
                         "re-applied a different value after a state load")
        self.assertEqual(client.boss_hp_vanilla, 75,
                         "stale savestate value was adopted as vanilla")

    async def test_reentering_same_stage_takes_fresh_baseline(self) -> None:
        # Leaving and re-entering the SAME stage recomputes 0x1CA2, so the
        # client must not keep the old baseline just because the id matches.
        client = MMX5Client()
        await run_watcher(save_with_boss_hp(40), mode=0x0A, stage_id=2,
                          client=client, ctx=self._ctx())
        rolled = client.boss_hp_written
        await run_watcher(save_with_boss_hp(rolled), mode=0x0C, stage_id=2,
                          client=client, ctx=self._ctx())
        ctx = self._ctx()
        await run_watcher(save_with_boss_hp(51), mode=0x0A, stage_id=2,
                          client=client, ctx=ctx)
        self.assertEqual(client.boss_hp_vanilla, 51,
                         "did not re-baseline on re-entering the same stage")

    async def test_zero_baseline_is_never_adopted(self) -> None:
        """Seen live 2026-08-05: entering Grizzly Slash logged
        `boss HP stage 1: 0 -> 0`. The stage id flips during the stage load
        before the Boss Level function recomputes 0x1CA2, so a poll can catch a
        zeroed byte. Adopting 0 is doubly bad: 0 is the kill-boss value, and
        the restore-on-exit would then write 0 over a legitimate number and
        poison the game's accumulator."""
        client = MMX5Client()
        ctx = await run_watcher(save_with_boss_hp(0), mode=0x0A, stage_id=1,
                                client=client, ctx=self._ctx())
        self.assertEqual(self._writes_to_boss_hp(ctx), [],
                         "wrote a boss HP value off a zero baseline")
        self.assertIsNone(client.boss_hp_vanilla,
                          "adopted 0 as a vanilla baseline")
        # and once a real value shows up, it is adopted normally
        ctx2 = self._ctx()
        await run_watcher(save_with_boss_hp(51), mode=0x0A, stage_id=1,
                          client=client, ctx=ctx2)
        self.assertEqual(client.boss_hp_vanilla, 51)
        self.assertTrue(self._writes_to_boss_hp(ctx2))

    async def test_zero_baseline_does_not_corrupt_restore(self) -> None:
        # The dangerous half: a 0 must never end up being "restored" later.
        client = MMX5Client()
        await run_watcher(save_with_boss_hp(0), mode=0x0A, stage_id=3,
                          client=client, ctx=self._ctx())
        ctx = self._ctx()
        await run_watcher(save_with_boss_hp(60), mode=0x0C, stage_id=3,
                          client=client, ctx=ctx)
        self.assertNotIn(0, self._writes_to_boss_hp(ctx),
                         "restored a zero over a legitimate accumulator value")

    async def test_retry_gives_same_fight(self) -> None:
        client = MMX5Client()
        first = await run_watcher(save_with_boss_hp(75), mode=0x0A, stage_id=4,
                                  client=client, ctx=self._ctx())
        again = await run_watcher(save_with_boss_hp(75), mode=0x0A, stage_id=4,
                                  client=client, ctx=self._ctx())
        self.assertEqual(self._writes_to_boss_hp(first)[-1],
                         self._writes_to_boss_hp(again)[-1])
