"""Weapon Damage — scaling the player attack table on the disc.

The table is 80 `(STA, DMG)` entries at 0x80074DA0, reached by the engine as
`[entity+0x58] + attack_id*2` (0x80031FA4). Three facts make this dangerous to
get wrong, and each has a test here:

* `DMG == 0x7F` is an **instakill sentinel** — the resolver `FUN_80031670`
  passes it through untouched. Emitting one would one-shot every boss.
* `STA == 2` means "this attack deals no damage" (0x80031FC4 returns early);
  `STA == 0xFF` marks unused slots. Neither is a quantity to scale.
* The table ENDS at 0x80074E40, where a different all-`(00,7F)` block starts.

Research: ghidra-findings §9.18, external-findings §1.1.
"""
import os
import random
import unittest

from .. import Rom
from ..Rom import (WEAPON_DAMAGE_ADDR, WEAPON_DAMAGE_MAX, WEAPON_DAMAGE_MIN,
                   WEAPON_DAMAGE_NEXT_ADDR, WEAPON_DAMAGE_NEXT_VANILLA,
                   WEAPON_DAMAGE_RANGES, WEAPON_DAMAGE_VANILLA,
                   weapon_damage_table)
from ..options import WeaponDamage
from .test_client import seed_edits_for

MODES = (WeaponDamage.option_weak, WeaponDamage.option_regular,
         WeaponDamage.option_strong, WeaponDamage.option_chaotic)


class FixedRandom:
    """`random` stand-in with a known draw order.

    The roller draws one multiplier per weapon family first (buster, then the
    eight specials), then one per remaining loose entry — so `first` lands on
    the buster family and `rest` on everything after it.
    """

    def __init__(self, first: float, rest: float):
        self.first, self.rest, self.calls = first, rest, 0

    def uniform(self, low: float, high: float) -> float:
        self.calls += 1
        return self.first if self.calls == 1 else self.rest


def rolled(mode, seed=1):
    return weapon_damage_table(mode, random.Random(seed))


def entries(table):
    return [(table[i], table[i + 1]) for i in range(0, len(table), 2)]


class TestTableShape(unittest.TestCase):
    def test_length_is_unchanged(self):
        for mode in MODES:
            with self.subTest(mode=mode):
                self.assertEqual(len(rolled(mode)), len(WEAPON_DAMAGE_VANILLA))

    def test_vanilla_table_is_eighty_entries(self):
        self.assertEqual(len(WEAPON_DAMAGE_VANILLA), 160)

    def test_the_next_block_is_not_part_of_the_table(self):
        # If the table length were wrong the scaler would run into this block
        # and rewrite instakill entries as ordinary damage.
        self.assertEqual(WEAPON_DAMAGE_NEXT_ADDR, 0x80074E40)
        self.assertTrue(all(v in (0x00, 0x7F) for v in WEAPON_DAMAGE_NEXT_VANILLA))


class TestWhatIsLeftAlone(unittest.TestCase):
    def test_sta_is_never_touched(self):
        for mode in MODES:
            for seed in range(20):
                out = rolled(mode, seed)
                self.assertEqual([e[0] for e in entries(out)],
                                 [e[0] for e in entries(WEAPON_DAMAGE_VANILLA)],
                                 "the STA byte is not a quantity")

    def test_non_damage_entries_are_identical(self):
        for mode in MODES:
            for seed in range(20):
                out = entries(rolled(mode, seed))
                for i, (sta, dmg) in enumerate(entries(WEAPON_DAMAGE_VANILLA)):
                    if sta != 0 or dmg == 0 or dmg == 0x7F:
                        self.assertEqual(out[i], (sta, dmg),
                                         f"entry {i} ({sta:02X},{dmg:02X}) was scaled")

    def test_instakill_entries_survive(self):
        # 0x7F is a sentinel, not a big number. Scaling it down turns an
        # instant kill into 60-odd damage; there are four in the table.
        want = sum(1 for sta, dmg in entries(WEAPON_DAMAGE_VANILLA)
                   if sta == 0 and dmg == 0x7F)
        self.assertEqual(want, 4, "vanilla instakill count changed - re-check the table")
        for mode in MODES:
            got = sum(1 for sta, dmg in entries(rolled(mode)) if sta == 0 and dmg == 0x7F)
            self.assertEqual(got, want, f"mode {mode} lost or invented an instakill")


class TestBounds(unittest.TestCase):
    def test_never_emits_the_instakill_sentinel(self):
        # The chaotic ceiling is 250%, and the table holds a 0x20 (Nova
        # Strike) and a 0x10 - well short of 0x7F - so this has to be checked
        # by construction, not by sampling luck.
        for mode in MODES:
            for seed in range(200):
                for i, (sta, dmg) in enumerate(entries(rolled(mode, seed))):
                    if sta == 0 and entries(WEAPON_DAMAGE_VANILLA)[i][1] != 0x7F:
                        self.assertLessEqual(dmg, WEAPON_DAMAGE_MAX)

    def test_never_rolls_a_weapon_to_zero(self):
        for mode in MODES:
            for seed in range(200):
                out = entries(rolled(mode, seed))
                for i, (sta, dmg) in enumerate(entries(WEAPON_DAMAGE_VANILLA)):
                    if sta == 0 and WEAPON_DAMAGE_MIN <= dmg <= WEAPON_DAMAGE_MAX:
                        self.assertGreaterEqual(out[i][1], WEAPON_DAMAGE_MIN,
                                                "a weapon that deals 0 is a dead weapon")

    def test_every_byte_is_a_byte(self):
        for mode in MODES:
            for seed in range(50):
                self.assertTrue(all(0 <= b <= 0xFF for b in rolled(mode, seed)))


class TestGuardsAgainstSyntheticEntries(unittest.TestCase):
    """The shipped table has no `STA != 0` entry that also carries damage, so
    those guards are unreachable with real data — dropping them entirely
    changes nothing observable, which is exactly how a guard rots. Feed the
    scaler entry shapes the real table does not contain.

    The bounds are pinned as literals here on purpose: every other test reads
    them from the module, so a wrong value would sail through all of them.
    """

    def test_bounds_match_the_engine(self):
        # 1: FUN_80031670 already refuses to deal less, so 0 is not reachable
        # behaviour - it just makes a dead weapon.
        self.assertEqual(WEAPON_DAMAGE_MIN, 1)
        # 0x7E: 0x7F is the instakill sentinel the resolver passes through.
        self.assertEqual(WEAPON_DAMAGE_MAX, 0x7E)

    def test_a_damaging_no_damage_entry_is_left_alone(self):
        # STA == 2 means "deals no damage" whatever DMG says.
        table = bytes([0x02, 0x05] * 8)
        for mode in MODES:
            for seed in range(30):
                self.assertEqual(weapon_damage_table(mode, random.Random(seed), table),
                                 table, "STA == 2 entry was scaled")

    def test_an_unused_slot_carrying_damage_is_left_alone(self):
        table = bytes([0xFF, 0x04] * 8)
        for mode in MODES:
            for seed in range(30):
                self.assertEqual(weapon_damage_table(mode, random.Random(seed), table),
                                 table, "unused slot was scaled")

    def test_one_damage_never_rounds_away(self):
        # chaotic's floor is 25%, so 1 * roll rounds to 0 without the clamp.
        table = bytes([0x00, 0x01] * 8)
        for seed in range(300):
            out = weapon_damage_table(WeaponDamage.option_chaotic,
                                      random.Random(seed), table)
            self.assertTrue(all(out[i + 1] >= 1 for i in range(0, len(out), 2)),
                            "a 1-damage attack rolled to 0")

    def test_a_high_entry_clamps_instead_of_wrapping(self):
        # Unreachable with the shipped table - the biggest entry is Nova
        # Strike at 0x20 and 250% of that is 0x50 - so this guard has to be
        # driven synthetically. It matters because without the ceiling the
        # value does not merely exceed the cap, it WRAPS to a byte: 0x70 at
        # 250% is 280, and 280 & 0xFF is 24. A wrap can also land exactly on
        # 0x7F, which would hand a weapon the instakill sentinel.
        table = bytes([0x00, 0x70] * 4)
        out = weapon_damage_table(WeaponDamage.option_chaotic,
                                  FixedRandom(2.5, 2.5), table)
        for _, dmg in entries(out):
            self.assertEqual(dmg, WEAPON_DAMAGE_MAX)

    def test_a_sentinel_only_table_is_untouched(self):
        table = bytes([0x00, 0x7F] * 8)
        for mode in MODES:
            self.assertEqual(weapon_damage_table(mode, random.Random(3), table), table)


class TestChargeLevelsStayOrdered(unittest.TestCase):
    """A charged shot must never roll below its own uncharged shot.

    The table is two parallel 9-entry blocks (0-8 uncharged, 9-17 charged),
    so entry k and entry k+9 are one weapon. They share a multiplier; these
    tests are what proves the sharing actually happens, since an independent
    roll passes every other test in this file.
    """

    PAIRS = tuple((k, k + 9) for k in range(9))

    def test_vanilla_pairs_are_the_shape_we_think(self):
        # If this fails the block layout changed and the families are wrong.
        v = entries(WEAPON_DAMAGE_VANILLA)
        self.assertEqual((v[0][1], v[9][1]), (3, 5), "X Buster uncharged/mid")
        for k in range(1, 9):
            unch, ch = v[k][1], v[k + 9][1]
            self.assertTrue(ch >= unch,
                            f"vanilla special {k}: charged {ch} < uncharged {unch}")

    def test_charged_never_rolls_below_uncharged(self):
        for mode in MODES:
            for seed in range(200):
                got = entries(rolled(mode, seed))
                for unch, ch in self.PAIRS:
                    self.assertGreaterEqual(
                        got[ch][1], got[unch][1],
                        f"mode {mode} seed {seed}: charged entry {ch} "
                        f"({got[ch][1]}) below uncharged {unch} ({got[unch][1]})")

    def test_a_family_scales_as_one(self):
        # Exact, not approximate: recovering the multiplier from a 3-damage
        # entry is quantized to steps of 1/6, which is far too coarse to say
        # anything about a 15-damage entry. Hand the roller a known sequence
        # instead - the first draw goes to the buster family, everything
        # after it to the specials and loose entries.
        v = entries(WEAPON_DAMAGE_VANILLA)
        rng = FixedRandom(first=2.0, rest=0.5)
        got = entries(weapon_damage_table(WeaponDamage.option_chaotic, rng))

        for entry in (0, 9, 18, 19, 20):
            self.assertEqual(got[entry][1], round(v[entry][1] * 2.0),
                             f"buster entry {entry} did not take the family roll")
        for entry in (1, 10):
            self.assertEqual(got[entry][1], round(v[entry][1] * 0.5),
                             f"special entry {entry} took the wrong roll")

    def test_a_special_weapon_pair_scales_as_one(self):
        v = entries(WEAPON_DAMAGE_VANILLA)
        # First draw = buster family, second = special #1 (entries 1 and 10).
        rng = FixedRandom(first=0.5, rest=2.0)
        got = entries(weapon_damage_table(WeaponDamage.option_chaotic, rng))
        self.assertEqual(got[0][1], round(v[0][1] * 0.5), "buster took the wrong roll")
        self.assertEqual(got[1][1], round(v[1][1] * 2.0))
        self.assertEqual(got[10][1], round(v[10][1] * 2.0),
                         "the charged half did not follow its uncharged half")

    def test_vanilla_ordering_is_preserved_inside_every_family(self):
        from ..Rom import WEAPON_DAMAGE_FAMILIES
        v = entries(WEAPON_DAMAGE_VANILLA)
        for mode in MODES:
            for seed in range(100):
                got = entries(rolled(mode, seed))
                for family in WEAPON_DAMAGE_FAMILIES:
                    for a in family:
                        for b in family:
                            if v[a][1] <= v[b][1]:
                                self.assertLessEqual(got[a][1], got[b][1])


class TestModesDiffer(unittest.TestCase):
    @staticmethod
    def total(mode, seed):
        return sum(dmg for sta, dmg in entries(rolled(mode, seed))
                   if sta == 0 and dmg != 0x7F)

    def test_weak_is_weaker_and_strong_is_stronger(self):
        vanilla = sum(dmg for sta, dmg in entries(WEAPON_DAMAGE_VANILLA)
                      if sta == 0 and dmg != 0x7F)
        for seed in range(10):
            with self.subTest(seed=seed):
                self.assertLess(self.total(WeaponDamage.option_weak, seed), vanilla)
                self.assertGreater(self.total(WeaponDamage.option_strong, seed), vanilla)

    def test_ranges_cover_every_option_value(self):
        for name in ("weak", "regular", "strong", "chaotic"):
            self.assertIn(getattr(WeaponDamage, "option_" + name), WEAPON_DAMAGE_RANGES)
        self.assertNotIn(WeaponDamage.option_off, WEAPON_DAMAGE_RANGES)

    def test_a_seed_is_reproducible(self):
        for mode in MODES:
            self.assertEqual(rolled(mode, 7), rolled(mode, 7),
                             "the same seed must rebuild the same disc")


class TestSeedEdits(unittest.TestCase):
    def test_off_emits_no_edit(self):
        addrs = {e["addr"] for e in seed_edits_for(weapon_damage=0)}
        self.assertNotIn(WEAPON_DAMAGE_ADDR, addrs)

    def test_on_emits_one_table_write_in_the_exe(self):
        edits = [e for e in seed_edits_for(weapon_damage=WeaponDamage.option_strong)
                 if e["addr"] == WEAPON_DAMAGE_ADDR]
        self.assertEqual(len(edits), 1)
        self.assertEqual(edits[0]["region"], "SLUS exe")
        self.assertEqual(len(bytes.fromhex(edits[0]["hex"])), len(WEAPON_DAMAGE_VANILLA))

    def test_the_edit_is_not_just_vanilla(self):
        edit = next(e for e in seed_edits_for(weapon_damage=WeaponDamage.option_chaotic)
                    if e["addr"] == WEAPON_DAMAGE_ADDR)
        self.assertNotEqual(bytes.fromhex(edit["hex"]), WEAPON_DAMAGE_VANILLA)


@unittest.skipUnless(os.environ.get("MMX5_DISC"),
                     "set MMX5_DISC=<path to a clean .bin> to re-derive from the disc")
class TestAgainstTheRealDisc(unittest.TestCase):
    """The constant is a copy of game data; prove it still matches the disc.

    Everything above tests the scaler against WEAPON_DAMAGE_VANILLA. If that
    constant were mistyped, all of it would pass and the patch would corrupt
    the table. This is the only test that can catch it.
    """

    @classmethod
    def setUpClass(cls):
        with open(os.environ["MMX5_DISC"], "rb") as f:
            cls.image = f.read()

    def read(self, addr, length):
        from .. import disc
        return bytes(self.image[disc.addr_to_disc(addr + i, "SLUS exe")]
                     for i in range(length))

    def test_vanilla_table_matches_the_disc(self):
        self.assertEqual(self.read(WEAPON_DAMAGE_ADDR, len(WEAPON_DAMAGE_VANILLA)),
                         WEAPON_DAMAGE_VANILLA)

    def test_the_block_after_the_table_matches(self):
        self.assertEqual(self.read(WEAPON_DAMAGE_NEXT_ADDR,
                                   len(WEAPON_DAMAGE_NEXT_VANILLA)),
                         WEAPON_DAMAGE_NEXT_VANILLA)

    def test_a_patched_disc_leaves_the_next_block_alone(self):
        from .. import disc
        edit = next(e for e in seed_edits_for(weapon_damage=WeaponDamage.option_chaotic)
                    if e["addr"] == WEAPON_DAMAGE_ADDR)
        patched = disc.apply_basepatch(
            self.image,
            [(edit["addr"], bytes.fromhex(edit["hex"]), edit["region"])])
        after = bytes(patched[disc.addr_to_disc(WEAPON_DAMAGE_NEXT_ADDR + i, "SLUS exe")]
                      for i in range(len(WEAPON_DAMAGE_NEXT_VANILLA)))
        self.assertEqual(after, WEAPON_DAMAGE_NEXT_VANILLA,
                         "the write ran past the end of the table")


if __name__ == "__main__":
    unittest.main()
