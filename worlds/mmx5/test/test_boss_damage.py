"""Boss Damage — scaling the eight Maverick attack tables on the disc.

Each boss's init installs its own attack table into `obj+0x58`, the same
per-entity mechanism the player's table uses. Those eight tables are
contiguous and identically sized (160 bytes, 0xA0 stride, 0x80075C00 to
0x80076100), so the whole set is a single EXE write.

The dangerous part is what must NOT be scaled: the tables bosses SHARE with
other things. `0x80074EE0`, `0x800750C0`, `0x800767E0`, the all-instakill
block `0x80074E40`, and `0x80074DA0` — which is the PLAYER's, referenced
directly by several boss sub-objects. Scaling the region by one byte too many
reaches into `0x80076100`, and one table too early would hit `0x80075B60`.

Research: ghidra-findings §9.18, external-findings §1.1 and §2.3.
"""
import os
import random
import unittest

from ..Rom import (BOSS_DAMAGE_ADDR, BOSS_DAMAGE_NEXT_ADDR,
                   BOSS_DAMAGE_NEXT_VANILLA, BOSS_DAMAGE_RANGES,
                   BOSS_DAMAGE_STRIDE, BOSS_DAMAGE_VANILLA,
                   WEAPON_DAMAGE_ADDR, WEAPON_DAMAGE_MAX, WEAPON_DAMAGE_MIN,
                   boss_damage_tables)
from ..options import BossDamage
from .test_client import seed_edits_for

MODES = (BossDamage.option_weak, BossDamage.option_regular,
         BossDamage.option_strong, BossDamage.option_chaotic)
TABLES = len(BOSS_DAMAGE_VANILLA) // BOSS_DAMAGE_STRIDE


class FixedRandom:
    """`random` stand-in: one known draw per boss, in table order."""

    def __init__(self, factors):
        self.factors, self.calls = list(factors), 0

    def uniform(self, low, high):
        f = self.factors[self.calls % len(self.factors)]
        self.calls += 1
        return f


def rolled(mode, seed=1):
    return boss_damage_tables(mode, random.Random(seed))


def table(data, index):
    lo = index * BOSS_DAMAGE_STRIDE
    chunk = data[lo:lo + BOSS_DAMAGE_STRIDE]
    return [(chunk[i], chunk[i + 1]) for i in range(0, len(chunk), 2)]


class TestLayout(unittest.TestCase):
    def test_eight_tables_of_eighty_entries(self):
        self.assertEqual(TABLES, 8)
        self.assertEqual(BOSS_DAMAGE_STRIDE, 0xA0)
        self.assertEqual(len(BOSS_DAMAGE_VANILLA), 8 * 0xA0)

    def test_the_region_does_not_touch_the_player_table(self):
        # 0x80074DA0 is the PLAYER's table and several boss sub-objects use it
        # directly. It must sit outside this write entirely.
        end = BOSS_DAMAGE_ADDR + len(BOSS_DAMAGE_VANILLA)
        self.assertLess(WEAPON_DAMAGE_ADDR, BOSS_DAMAGE_ADDR)
        self.assertEqual((BOSS_DAMAGE_ADDR, end), (0x80075C00, 0x80076100))

    def test_length_is_unchanged_by_rolling(self):
        for mode in MODES:
            self.assertEqual(len(rolled(mode)), len(BOSS_DAMAGE_VANILLA))


class TestWhatIsLeftAlone(unittest.TestCase):
    def test_sta_bytes_are_never_touched(self):
        for mode in MODES:
            for seed in range(20):
                out = rolled(mode, seed)
                self.assertEqual([out[i] for i in range(0, len(out), 2)],
                                 [BOSS_DAMAGE_VANILLA[i]
                                  for i in range(0, len(BOSS_DAMAGE_VANILLA), 2)])

    def test_non_damage_entries_are_identical(self):
        for mode in MODES:
            for seed in range(20):
                out = rolled(mode, seed)
                for i in range(0, len(out), 2):
                    sta, dmg = BOSS_DAMAGE_VANILLA[i], BOSS_DAMAGE_VANILLA[i + 1]
                    if sta != 0 or dmg == 0 or dmg == 0x7F:
                        self.assertEqual(out[i + 1], dmg,
                                         f"byte {i + 1} (STA {sta:02X}) was scaled")

    def test_bounds_hold_everywhere(self):
        for mode in MODES:
            for seed in range(60):
                out = rolled(mode, seed)
                for i in range(0, len(out), 2):
                    sta, van = BOSS_DAMAGE_VANILLA[i], BOSS_DAMAGE_VANILLA[i + 1]
                    if sta == 0 and WEAPON_DAMAGE_MIN <= van <= WEAPON_DAMAGE_MAX:
                        self.assertTrue(WEAPON_DAMAGE_MIN <= out[i + 1] <= WEAPON_DAMAGE_MAX)


class TestGuardsAgainstSyntheticTables(unittest.TestCase):
    """None of the eight shipped tables contains an instakill entry, so that
    guard is unreachable with real data and would rot untested — exactly how
    the player-table version nearly shipped. Feed it entry shapes the boss
    tables do not happen to contain."""

    @staticmethod
    def one_table(pairs):
        data = bytearray()
        while len(data) < BOSS_DAMAGE_STRIDE:
            for sta, dmg in pairs:
                data += bytes([sta, dmg])
        return bytes(data[:BOSS_DAMAGE_STRIDE])

    def test_an_instakill_entry_survives(self):
        t = self.one_table([(0x00, 0x7F), (0x00, 0x04)])
        for mode in MODES:
            for seed in range(30):
                out = boss_damage_tables(mode, random.Random(seed), t)
                for i in range(0, len(out), 2):
                    if t[i + 1] == 0x7F:
                        self.assertEqual(out[i + 1], 0x7F,
                                         "an instant kill was turned into a number")

    def test_a_no_damage_entry_survives(self):
        t = self.one_table([(0x02, 0x05), (0xFF, 0x03)])
        for mode in MODES:
            self.assertEqual(boss_damage_tables(mode, random.Random(2), t), t)

    def test_a_high_entry_clamps_instead_of_wrapping(self):
        # Boss tables top out at 0x0A, so the ceiling is unreachable with real
        # data. Without the clamp the value wraps to a byte and can land on
        # 0x7F, handing a boss an instant kill.
        t = self.one_table([(0x00, 0x70)])
        out = boss_damage_tables(BossDamage.option_chaotic,
                                 FixedRandom([2.5] * 8), t)
        for i in range(0, len(out), 2):
            self.assertEqual(out[i + 1], WEAPON_DAMAGE_MAX)

    def test_one_damage_never_rounds_away(self):
        t = self.one_table([(0x00, 0x01)])
        for seed in range(200):
            out = boss_damage_tables(BossDamage.option_chaotic, random.Random(seed), t)
            self.assertTrue(all(out[i + 1] >= 1 for i in range(0, len(out), 2)))


class TestOneRollPerBoss(unittest.TestCase):
    """A boss keeps the shape of its own move set: light pokes stay light next
    to its big attack. An independent roll per entry passes every other test
    in this file, so this is what proves the sharing."""

    def test_each_table_scales_by_its_own_factor(self):
        factors = [0.5, 2.0, 0.5, 2.0, 0.5, 2.0, 0.5, 2.0]
        out = boss_damage_tables(BossDamage.option_chaotic, FixedRandom(factors))
        for t in range(TABLES):
            want = factors[t]
            for (sta, van), (_, got) in zip(table(BOSS_DAMAGE_VANILLA, t),
                                            table(out, t)):
                if sta == 0 and WEAPON_DAMAGE_MIN <= van <= WEAPON_DAMAGE_MAX:
                    self.assertEqual(got, max(WEAPON_DAMAGE_MIN,
                                              min(WEAPON_DAMAGE_MAX, round(van * want))),
                                     f"table {t} entry did not use its own factor")

    def test_tables_are_rolled_independently(self):
        # Table 0 at 0.5 and table 1 at 2.0 must not come out equal.
        out = boss_damage_tables(BossDamage.option_chaotic,
                                 FixedRandom([0.5, 2.0] * 4))
        self.assertNotEqual(table(out, 0), table(out, 1))

    def test_one_draw_per_boss(self):
        rng = FixedRandom([1.0] * 8)
        boss_damage_tables(BossDamage.option_regular, rng)
        self.assertEqual(rng.calls, TABLES,
                         "expected exactly one multiplier per boss")

    def test_ordering_inside_a_table_is_preserved(self):
        for mode in MODES:
            for seed in range(30):
                out = rolled(mode, seed)
                for t in range(TABLES):
                    van, got = table(BOSS_DAMAGE_VANILLA, t), table(out, t)
                    dmg = [(v[1], g[1]) for v, g in zip(van, got)
                           if v[0] == 0 and WEAPON_DAMAGE_MIN <= v[1] <= WEAPON_DAMAGE_MAX]
                    for (va, ga) in dmg:
                        for (vb, gb) in dmg:
                            if va <= vb:
                                self.assertLessEqual(ga, gb)


class TestModes(unittest.TestCase):
    @staticmethod
    def total(data):
        return sum(data[i + 1] for i in range(0, len(data), 2)
                   if BOSS_DAMAGE_VANILLA[i] == 0
                   and BOSS_DAMAGE_VANILLA[i + 1] not in (0, 0x7F))

    def test_weak_is_weaker_and_strong_is_stronger(self):
        base = self.total(BOSS_DAMAGE_VANILLA)
        for seed in range(10):
            self.assertLess(self.total(rolled(BossDamage.option_weak, seed)), base)
            self.assertGreater(self.total(rolled(BossDamage.option_strong, seed)), base)

    def test_ranges_cover_every_option_value(self):
        for name in ("weak", "regular", "strong", "chaotic"):
            self.assertIn(getattr(BossDamage, "option_" + name), BOSS_DAMAGE_RANGES)
        self.assertNotIn(BossDamage.option_off, BOSS_DAMAGE_RANGES)

    def test_a_seed_is_reproducible(self):
        for mode in MODES:
            self.assertEqual(rolled(mode, 5), rolled(mode, 5))


class TestSeedEdits(unittest.TestCase):
    def test_off_emits_no_edit(self):
        addrs = {e["addr"] for e in seed_edits_for(boss_damage=0)}
        self.assertNotIn(BOSS_DAMAGE_ADDR, addrs)

    def test_on_emits_one_write_in_the_exe(self):
        edits = [e for e in seed_edits_for(boss_damage=BossDamage.option_strong)
                 if e["addr"] == BOSS_DAMAGE_ADDR]
        self.assertEqual(len(edits), 1)
        self.assertEqual(edits[0]["region"], "SLUS exe")
        self.assertEqual(len(bytes.fromhex(edits[0]["hex"])), len(BOSS_DAMAGE_VANILLA))

    def test_it_does_not_also_write_the_player_table(self):
        addrs = {e["addr"] for e in seed_edits_for(boss_damage=BossDamage.option_chaotic)}
        self.assertNotIn(WEAPON_DAMAGE_ADDR, addrs,
                         "boss damage must not touch the player's weapons")


@unittest.skipUnless(os.environ.get("MMX5_DISC"),
                     "set MMX5_DISC=<path to a clean .bin> to re-derive from the disc")
class TestAgainstTheRealDisc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(os.environ["MMX5_DISC"], "rb") as f:
            cls.image = f.read()

    def read(self, addr, length):
        from .. import disc
        return bytes(self.image[disc.addr_to_disc(addr + i, "SLUS exe")]
                     for i in range(length))

    def test_vanilla_tables_match_the_disc(self):
        self.assertEqual(self.read(BOSS_DAMAGE_ADDR, len(BOSS_DAMAGE_VANILLA)),
                         BOSS_DAMAGE_VANILLA)

    def test_the_block_after_the_region_matches(self):
        self.assertEqual(self.read(BOSS_DAMAGE_NEXT_ADDR,
                                   len(BOSS_DAMAGE_NEXT_VANILLA)),
                         BOSS_DAMAGE_NEXT_VANILLA)

    def test_a_patched_disc_leaves_the_neighbours_alone(self):
        from .. import disc
        from ..Rom import WEAPON_DAMAGE_VANILLA
        edit = next(e for e in seed_edits_for(boss_damage=BossDamage.option_chaotic)
                    if e["addr"] == BOSS_DAMAGE_ADDR)
        patched = disc.apply_basepatch(
            self.image,
            [(edit["addr"], bytes.fromhex(edit["hex"]), edit["region"])])

        def after(addr, length):
            return bytes(patched[disc.addr_to_disc(addr + i, "SLUS exe")]
                         for i in range(length))

        self.assertEqual(after(BOSS_DAMAGE_NEXT_ADDR, len(BOSS_DAMAGE_NEXT_VANILLA)),
                         BOSS_DAMAGE_NEXT_VANILLA, "the write ran past the tables")
        self.assertEqual(after(WEAPON_DAMAGE_ADDR, len(WEAPON_DAMAGE_VANILLA)),
                         WEAPON_DAMAGE_VANILLA, "the write reached the player table")


if __name__ == "__main__":
    unittest.main()
