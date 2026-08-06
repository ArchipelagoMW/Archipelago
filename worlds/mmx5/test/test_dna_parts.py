"""DNA Parts as pool items.

16 Parts live in bits 2..17 of the u32 0x800D1C84. Vanilla yields only 8 per
run - each Maverick offers two and Alia's Life+/Energy+ prompt makes you give
up the other - so the seed picks one from each pair and shuffles those.

The client write does double duty: OR in what the player received, clear what
the game granted. That second half is the suppression.
"""
import unittest
from types import SimpleNamespace

import worlds.mmx5.client as c
from worlds.mmx5 import names
from worlds.mmx5.client import MMX5Client
from worlds.mmx5.items import BASE_ID, item_table

from . import MMX5TestBase
from .test_client import FakeContext, make_save, run_watcher


class TestPartsOff(MMX5TestBase):
    options = {"dna_parts_in_pool": False}

    def test_not_in_pool(self) -> None:
        pool = {i.name for i in self.multiworld.itempool}
        for p in names.DNA_PARTS:
            self.assertNotIn(p, pool)


class TestPartsOn(MMX5TestBase):
    options = {"dna_parts_in_pool": True}

    def test_exactly_one_per_pair(self) -> None:
        pool = [i.name for i in self.multiworld.itempool]
        for boss, pair in names.PART_PAIRS.items():
            got = [p for p in pair if p in pool]
            self.assertEqual(len(got), 1,
                             f"{boss} contributed {got}, expected exactly one")

    def test_eight_parts_total(self) -> None:
        pool = [i.name for i in self.multiworld.itempool]
        self.assertEqual(sum(1 for n in pool if n in names.DNA_PARTS), 8)

    def test_no_duplicates(self) -> None:
        pool = [i.name for i in self.multiworld.itempool]
        parts = [n for n in pool if n in names.DNA_PARTS]
        self.assertEqual(len(parts), len(set(parts)))

    def test_pool_still_matches_locations(self) -> None:
        real = [l for l in self.multiworld.get_locations(self.player)
                if l.address is not None]
        self.assertEqual(len(self.multiworld.itempool), len(real))

    def test_never_progression(self) -> None:
        # Six only work for one character; requiring any would strand a
        # single-character run.
        world = self.multiworld.worlds[self.player]
        for p in names.DNA_PARTS:
            self.assertFalse(world.create_item(p).advancement, f"{p} is progression")


class TestPoolCapacity(unittest.TestCase):
    """Every item needs a location, and overshooting used to pass silently.

    parts + stage_unlocks + secret_armors produced 53 items for 48 locations,
    generated without complaint, and simply dropped Ultimate Armor and a DNA
    Part. The guard has to sit in generate_early: Generate.py RETRIES a world
    that raises later, so an error from create_items spins instead of
    surfacing.
    """

    def _build(self, **opts):
        from test.bases import WorldTestBase

        class T(WorldTestBase):
            game = "Mega Man X5"
            options = opts
        t = T()
        t.setUp()
        return t

    def _assert_balanced(self, **opts) -> None:
        t = self._build(**opts)
        pool = list(t.multiworld.itempool)
        locs = [l for l in t.multiworld.get_locations(t.player)
                if l.address is not None]
        self.assertEqual(len(pool), len(locs), f"unbalanced pool for {opts}")

    def test_fits_stay_balanced(self) -> None:
        self._assert_balanced(dna_parts_in_pool=True)
        self._assert_balanced(dna_parts_in_pool=True, secret_armors_in_pool=True)
        self._assert_balanced(dna_parts_in_pool=True, stage_unlocks=True,
                              secret_armors_in_pool=True, pickupsanity=True)

    def test_overflow_is_refused_not_silently_dropped(self) -> None:
        from Options import OptionError
        for opts in (
            dict(dna_parts_in_pool=True, stage_unlocks=True),
            dict(dna_parts_in_pool=True, stage_unlocks=True,
                 secret_armors_in_pool=True),
            dict(dna_parts_in_pool=True, stage_unlocks=True,
                 secret_armors_in_pool=True, endgame_checks=False),
        ):
            with self.assertRaises(OptionError, msg=f"{opts} should not generate"):
                self._build(**opts)

    def test_error_names_a_remedy(self) -> None:
        from Options import OptionError
        with self.assertRaises(OptionError) as cm:
            self._build(dna_parts_in_pool=True, stage_unlocks=True)
        msg = str(cm.exception)
        self.assertIn("pickupsanity", msg)
        self.assertIn("locations", msg)


class TestPartsData(unittest.TestCase):
    def test_sixteen_parts_all_distinct(self) -> None:
        self.assertEqual(len(names.DNA_PARTS), 16)
        self.assertEqual(len(set(names.DNA_PARTS)), 16)

    def test_every_part_has_a_unique_bit_in_2_17(self) -> None:
        bits = [c.PART_TO_BIT[p] for p in names.DNA_PARTS]
        self.assertEqual(sorted(bits), list(range(2, 18)))

    def test_character_locked_parts_are_bits_11_to_16(self) -> None:
        # Capcom grouped them, and that grouping is what corroborates the
        # name->bit mapping read off the Parts screen (findings §9.15).
        locked = names.X_ONLY_PARTS | names.ZERO_ONLY_PARTS
        self.assertEqual(sorted(c.PART_TO_BIT[p] for p in locked),
                         list(range(11, 17)))
        self.assertEqual(sorted(c.PART_TO_BIT[p] for p in names.X_ONLY_PARTS),
                         [11, 12, 13])
        self.assertEqual(sorted(c.PART_TO_BIT[p] for p in names.ZERO_ONLY_PARTS),
                         [14, 15, 16])

    def test_mask_matches_the_bits(self) -> None:
        m = 0
        for b in c.PART_TO_BIT.values():
            m |= 1 << b
        self.assertEqual(m, c.PARTS_MASK)

    def test_ids_stable_and_unique(self) -> None:
        for i, name in enumerate(names.DNA_PARTS):
            self.assertEqual(item_table[name].code, BASE_ID + 50 + i)
        codes = [d.code for d in item_table.values() if d.code is not None]
        self.assertEqual(len(codes), len(set(codes)))

    def test_table_count_is_zero(self) -> None:
        for name in names.DNA_PARTS:
            self.assertEqual(item_table[name].count, 0)


class TestPartsGrantAndSuppression(unittest.IsolatedAsyncioTestCase):
    def _ctx(self, *parts, enabled=1) -> FakeContext:
        ctx = FakeContext()
        ctx.slot_data = {"goal": 0, "boss_difficulty": 1,
                         "dna_parts_in_pool": enabled}
        by_code = {BASE_ID + 50 + i: n for i, n in enumerate(names.DNA_PARTS)}
        ctx.item_names = SimpleNamespace(
            lookup_in_game=lambda code: by_code.get(code, ""))
        ctx.items_received = [
            SimpleNamespace(item=BASE_ID + 50 + names.DNA_PARTS.index(p))
            for p in parts]
        return ctx

    def _written(self, ctx):
        addr = c.SAVE_BASE + c.OFF_PARTS
        return [int.from_bytes(bytes(w[1]), "little")
                for w in ctx.writes if w[0] == addr]

    def _save(self, parts_word=0):
        s = bytearray(make_save(max_hp=0x20, intro=2, weapons=1))
        s[c.OFF_PARTS:c.OFF_PARTS + 4] = parts_word.to_bytes(4, "little")
        return bytes(s)

    async def test_grants_the_received_part(self) -> None:
        ctx = await run_watcher(self._save(), client=MMX5Client(),
                                ctx=self._ctx(names.HYPER_DASH))
        self.assertEqual(self._written(ctx), [1 << c.PART_TO_BIT[names.HYPER_DASH]])

    async def test_suppresses_a_vanilla_grant(self) -> None:
        # The game handed out Speedster; the player was never sent it.
        vanilla = 1 << c.PART_TO_BIT[names.SPEEDSTER]
        ctx = await run_watcher(self._save(vanilla), client=MMX5Client(),
                                ctx=self._ctx())
        self.assertEqual(self._written(ctx), [0])

    async def test_keeps_received_and_drops_vanilla_in_one_write(self) -> None:
        vanilla = 1 << c.PART_TO_BIT[names.SPEEDSTER]
        ctx = await run_watcher(self._save(vanilla), client=MMX5Client(),
                                ctx=self._ctx(names.JUMPER))
        self.assertEqual(self._written(ctx), [1 << c.PART_TO_BIT[names.JUMPER]])

    async def test_preserves_bits_outside_the_parts_mask(self) -> None:
        # Bits 0-1 and 18+ have no known meaning. Assuming they are spare is
        # the kind of guess that has cost this project before.
        other = 0x80000003
        ctx = await run_watcher(self._save(other), client=MMX5Client(),
                                ctx=self._ctx(names.JUMPER))
        got = self._written(ctx)[0]
        self.assertEqual(got & ~c.PARTS_MASK, other & ~c.PARTS_MASK)

    async def test_no_write_when_already_correct(self) -> None:
        want = 1 << c.PART_TO_BIT[names.JUMPER]
        ctx = await run_watcher(self._save(want), client=MMX5Client(),
                                ctx=self._ctx(names.JUMPER))
        self.assertEqual(self._written(ctx), [])

    async def test_inert_when_option_off(self) -> None:
        vanilla = 1 << c.PART_TO_BIT[names.SPEEDSTER]
        ctx = await run_watcher(self._save(vanilla), client=MMX5Client(),
                                ctx=self._ctx(enabled=0))
        self.assertEqual(self._written(ctx), [])

    async def test_stale_save_is_not_touched(self) -> None:
        s = bytearray(make_save(max_hp=0x00, intro=0xFF, weapons=0xFF))
        s[c.OFF_PARTS:c.OFF_PARTS + 4] = (0xFFFFFFFF).to_bytes(4, "little")
        ctx = await run_watcher(bytes(s), client=MMX5Client(),
                                ctx=self._ctx(names.JUMPER))
        self.assertEqual(self._written(ctx), [])
