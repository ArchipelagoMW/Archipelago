"""Ultimate Armor / Black Zero as optional pool items.

Grant sites come from the Zero Space capsule's own code (id 8, disasm
2026-08-01): char 0 (X) -> 0x800D1C4B = 1, otherwise 0x800D1C4A |= 0x10.
"""
import unittest
from types import SimpleNamespace

import worlds.mmx5.client as c
from worlds.mmx5 import names
from worlds.mmx5.client import MMX5Client
from worlds.mmx5.items import item_table

from . import MMX5TestBase
from .test_client import FakeContext, make_save, run_watcher


class TestSecretArmorsOff(MMX5TestBase):
    options = {"secret_armors_in_pool": False}

    def test_not_in_pool(self) -> None:
        pool = {i.name for i in self.multiworld.itempool}
        self.assertNotIn(names.ULTIMATE_ARMOR, pool)
        self.assertNotIn(names.BLACK_ZERO, pool)


class TestSecretArmorsOn(MMX5TestBase):
    options = {"secret_armors_in_pool": True}

    def test_in_pool_exactly_once(self) -> None:
        pool = [i.name for i in self.multiworld.itempool]
        self.assertEqual(pool.count(names.ULTIMATE_ARMOR), 1)
        self.assertEqual(pool.count(names.BLACK_ZERO), 1)

    def test_pool_still_matches_locations(self) -> None:
        real = [l for l in self.multiworld.get_locations(self.player)
                if l.address is not None]
        self.assertEqual(len(self.multiworld.itempool), len(real),
                         "adding the armors unbalanced the pool")

    def test_not_progression(self) -> None:
        # Nothing may require them: each only helps one character, and a seed
        # played entirely as X would otherwise be unwinnable behind Black Zero.
        for name in (names.ULTIMATE_ARMOR, names.BLACK_ZERO):
            self.assertFalse(self.multiworld.worlds[self.player]
                             .create_item(name).advancement,
                             f"{name} must never be progression")


class TestSecretArmorIds(unittest.TestCase):
    def test_ids_are_stable_and_unique(self) -> None:
        from worlds.mmx5.items import BASE_ID
        self.assertEqual(item_table[names.ULTIMATE_ARMOR].code, BASE_ID + 28)
        self.assertEqual(item_table[names.BLACK_ZERO].code, BASE_ID + 29)
        codes = [d.code for d in item_table.values() if d.code is not None]
        self.assertEqual(len(codes), len(set(codes)), "duplicate item id")

    def test_table_count_is_zero(self) -> None:
        # They are added by create_items under the option, so a nonzero count
        # here would put them in every seed.
        self.assertEqual(item_table[names.ULTIMATE_ARMOR].count, 0)
        self.assertEqual(item_table[names.BLACK_ZERO].count, 0)


class TestSecretArmorGrants(unittest.IsolatedAsyncioTestCase):
    def _ctx(self, *received) -> FakeContext:
        ctx = FakeContext()
        ctx.slot_data = {"goal": 0, "boss_difficulty": 1}
        names_by_code = {1: names.ULTIMATE_ARMOR, 2: names.BLACK_ZERO}
        ctx.item_names = SimpleNamespace(
            lookup_in_game=lambda code: names_by_code.get(code, ""))
        ctx.items_received = [SimpleNamespace(item=code) for code in received]
        return ctx

    def _writes(self, ctx, offset) -> list:
        addr = c.SAVE_BASE + offset
        return [w[1][0] for w in ctx.writes if w[0] == addr]

    async def test_ultimate_sets_its_byte(self) -> None:
        ctx = await run_watcher(make_save(max_hp=0x20, intro=2, weapons=1),
                                client=MMX5Client(), ctx=self._ctx(1))
        self.assertIn(c.ULTIMATE_ON, self._writes(ctx, c.OFF_ULTIMATE))

    async def test_black_zero_ors_its_bit(self) -> None:
        ctx = await run_watcher(make_save(max_hp=0x20, intro=2, weapons=1),
                                client=MMX5Client(), ctx=self._ctx(2))
        written = self._writes(ctx, c.OFF_SETFLAGS)
        self.assertTrue(written)
        self.assertTrue(all(v & c.BLACK_ZERO_BIT for v in written))

    async def test_black_zero_preserves_armor_set_flags(self) -> None:
        # 0x1C4A also carries the Falcon/Gaea set-completion bits the results
        # overlay owns - clobbering them would un-complete an armor set.
        save = bytearray(make_save(max_hp=0x20, intro=2, weapons=1))
        save[c.OFF_SETFLAGS] = 0x06        # Falcon + Gaea complete
        ctx = await run_watcher(bytes(save), client=MMX5Client(),
                                ctx=self._ctx(2))
        for v in self._writes(ctx, c.OFF_SETFLAGS):
            self.assertEqual(v & 0x06, 0x06, "clobbered armor set flags")
            self.assertTrue(v & c.BLACK_ZERO_BIT)

    async def test_no_write_when_not_received(self) -> None:
        ctx = await run_watcher(make_save(max_hp=0x20, intro=2, weapons=1),
                                client=MMX5Client(), ctx=self._ctx())
        self.assertEqual(self._writes(ctx, c.OFF_ULTIMATE), [])

    async def test_idempotent_when_already_set(self) -> None:
        save = bytearray(make_save(max_hp=0x20, intro=2, weapons=1))
        save[c.OFF_ULTIMATE] = c.ULTIMATE_ON
        save[c.OFF_SETFLAGS] = c.BLACK_ZERO_BIT
        ctx = await run_watcher(bytes(save), client=MMX5Client(),
                                ctx=self._ctx(1, 2))
        self.assertEqual(self._writes(ctx, c.OFF_ULTIMATE), [])
        self.assertEqual(self._writes(ctx, c.OFF_SETFLAGS), [])
