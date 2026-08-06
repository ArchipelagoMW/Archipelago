"""Stage unlocks: eight Access Codes items, enforced by zeroing the hub's
slot -> stage-id table at 0x800F5050.

The game's own `beqz` at 0x800EFCA4 makes a zeroed slot's confirm a no-op
(ghidra-findings §9.14), so the whole in-game half is an 8-byte write.
"""
import unittest
from types import SimpleNamespace

from BaseClasses import CollectionState, ItemClassification

import worlds.mmx5.client as c
from worlds.mmx5 import names
from worlds.mmx5.client import MMX5Client
from worlds.mmx5.items import BASE_ID, item_table

from . import MMX5TestBase
from .test_client import FakeContext, make_save, run_watcher


class TestStageUnlocksOff(MMX5TestBase):
    options = {"stage_unlocks": False}

    def test_no_access_items(self) -> None:
        pool = {i.name for i in self.multiworld.itempool}
        for name in names.ACCESS_ITEMS:
            self.assertNotIn(name, pool)

    def test_stages_reachable_with_nothing(self) -> None:
        state = self.multiworld.get_all_state(False)
        for stage in names.STAGES:
            self.assertTrue(
                self.multiworld.get_entrance(f"Stage Select -> {stage}",
                                             self.player).access_rule(state))


class TestStageUnlocksOn(MMX5TestBase):
    options = {"stage_unlocks": True}

    def test_seven_in_pool_one_precollected(self) -> None:
        pool = [i.name for i in self.multiworld.itempool]
        start = {i.name for i in self.multiworld.precollected_items[self.player]}
        world = self.multiworld.worlds[self.player]
        starting = names.access_item(world.starting_stage)
        self.assertIn(starting, start)
        self.assertNotIn(starting, pool)
        for stage in names.STAGES:
            name = names.access_item(stage)
            if name != starting:
                self.assertEqual(pool.count(name), 1, f"{name} not shuffled")

    def test_pool_still_matches_locations(self) -> None:
        real = [l for l in self.multiworld.get_locations(self.player)
                if l.address is not None]
        self.assertEqual(len(self.multiworld.itempool), len(real),
                         "adding access items unbalanced the pool")

    def _blank(self) -> CollectionState:
        """A state holding nothing at all - not even the precollected codes."""
        state = CollectionState(self.multiworld)
        state.prog_items[self.player].clear()
        return state

    def test_stage_locked_without_its_codes(self) -> None:
        blank = self._blank()
        for stage in names.STAGES:
            entrance = self.multiworld.get_entrance(
                f"Stage Select -> {stage}", self.player)
            self.assertFalse(entrance.access_rule(blank),
                             f"{stage} was enterable with no items at all")

    def test_codes_open_exactly_their_own_stage(self) -> None:
        blank = self._blank()
        target = names.STAGES[3]
        blank.collect(self.multiworld.worlds[self.player]
                      .create_item(names.access_item(target)), True)
        for stage in names.STAGES:
            entrance = self.multiworld.get_entrance(
                f"Stage Select -> {stage}", self.player)
            self.assertEqual(entrance.access_rule(blank), stage == target,
                             f"{target} codes gave the wrong answer for {stage}")

    def test_stage_locations_inherit_the_lock(self) -> None:
        # One entrance rule has to cover the boss, heart, capsule, tank, DNA
        # and (when on) pickupsanity checks - they all live in the region.
        world = self.multiworld.worlds[self.player]
        stage = next(s for s in names.STAGES if s != world.starting_stage)
        blank = self._blank()
        loc = self.multiworld.get_location(names.boss_location(stage), self.player)
        self.assertFalse(loc.can_reach(blank),
                         f"{stage}'s boss check was reachable with no codes")
        blank.collect(world.create_item(names.access_item(stage)), True)
        self.assertTrue(loc.can_reach(blank),
                        f"{stage}'s boss check stayed unreachable with its codes")


class TestStageUnlocksFill(MMX5TestBase):
    """A stage's codes must never end up inside that stage, directly or behind
    a chain that needs them.

    The rules make this structurally impossible - every requirement in this
    world is an ITEM, so the whole graph is one dependency AP's fill respects -
    but the invariant is worth pinning, because it is what a future rules
    change would quietly break. Run with pickupsanity on: that adds 32
    locations inside the locked regions, which is where a self-lock would hide.
    """
    options = {"stage_unlocks": True, "pickupsanity": True}

    def test_no_stage_holds_its_own_codes(self) -> None:
        from Fill import distribute_items_restrictive
        distribute_items_restrictive(self.multiworld)
        for loc in self.multiworld.get_locations(self.player):
            item = loc.item
            if item is None or item.name not in names.ACCESS_ITEMS:
                continue
            stage = item.name.removesuffix(" Access Codes")
            self.assertFalse(
                loc.name.startswith(stage + " -"),
                f"{item.name} was placed at {loc.name}, inside the stage it unlocks")

    def test_seed_is_beatable_from_nothing(self) -> None:
        from Fill import distribute_items_restrictive
        distribute_items_restrictive(self.multiworld)
        self.assertTrue(self.multiworld.can_beat_game(),
                        "stage locks made the seed unwinnable")


class TestAccessItemIds(unittest.TestCase):
    def test_ids_are_stable_and_unique(self) -> None:
        for i, name in enumerate(names.ACCESS_ITEMS):
            self.assertEqual(item_table[name].code, BASE_ID + 30 + i)
        codes = [d.code for d in item_table.values() if d.code is not None]
        self.assertEqual(len(codes), len(set(codes)), "duplicate item id")

    def test_table_count_is_zero(self) -> None:
        # create_items adds them under the option; a nonzero count here would
        # put access items in every seed.
        for name in names.ACCESS_ITEMS:
            self.assertEqual(item_table[name].count, 0)

    def test_progression(self) -> None:
        for name in names.ACCESS_ITEMS:
            self.assertEqual(item_table[name].classification,
                             ItemClassification.progression)


class TestSlotTable(unittest.TestCase):
    def test_covers_all_eight_stages_once(self) -> None:
        self.assertEqual(sorted(c.SLOT_TO_STAGE), list(range(1, 9)))

    def test_every_slot_id_has_a_name(self) -> None:
        for sid in c.SLOT_TO_STAGE:
            self.assertIn(sid, c.STAGE_ID_TO_NAME)


class TestStageUnlockWrites(unittest.IsolatedAsyncioTestCase):
    """The in-game half: 0x800F5050 holds the id of unlocked stages and 0 for
    the rest, but only while the hub overlay is actually the resident module."""

    def _ctx(self, *stages) -> FakeContext:
        ctx = FakeContext()
        ctx.slot_data = {"goal": 0, "boss_difficulty": 1, "stage_unlocks": 1}
        by_code = {BASE_ID + 30 + i: name
                   for i, name in enumerate(names.ACCESS_ITEMS)}
        ctx.item_names = SimpleNamespace(
            lookup_in_game=lambda code: by_code.get(code, ""))
        ctx.items_received = [
            SimpleNamespace(item=BASE_ID + 30 + names.STAGES.index(s))
            for s in stages]
        return ctx

    def _table_writes(self, ctx) -> list:
        return [bytes(w[1]) for w in ctx.writes if w[0] == c.SLOT_TABLE_ADDR]

    def _expected(self, *stages) -> bytes:
        held = {c.STAGE_ID_BY_NAME[s] for s in stages}
        return bytes(sid if sid in held else 0 for sid in c.SLOT_TO_STAGE)

    async def test_all_locked_with_no_codes(self) -> None:
        ctx = await run_watcher(make_save(max_hp=0x20, intro=2, weapons=1),
                                mode=0x13, stage_id=0x0D, hub_resident=True,
                                client=MMX5Client(), ctx=self._ctx())
        self.assertEqual(self._table_writes(ctx), [bytes(8)])

    async def test_only_held_stages_keep_their_id(self) -> None:
        ctx = await run_watcher(make_save(max_hp=0x20, intro=2, weapons=1),
                                mode=0x13, stage_id=0x0D, hub_resident=True,
                                client=MMX5Client(),
                                ctx=self._ctx(names.GRIZZLY, names.DINOREX))
        self.assertEqual(self._table_writes(ctx),
                         [self._expected(names.GRIZZLY, names.DINOREX)])

    async def test_no_write_when_table_already_correct(self) -> None:
        want = self._expected(names.GRIZZLY)
        ctx = await run_watcher(make_save(max_hp=0x20, intro=2, weapons=1),
                                mode=0x13, stage_id=0x0D, hub_resident=True,
                                slot_table=want, client=MMX5Client(),
                                ctx=self._ctx(names.GRIZZLY))
        self.assertEqual(self._table_writes(ctx), [])

    async def test_nothing_written_outside_the_hub(self) -> None:
        # Every other overlay maps different code at the anchor. Writing 8
        # bytes into whatever lives at 0x800F5050 in a stage would corrupt it.
        ctx = await run_watcher(make_save(max_hp=0x20, intro=2, weapons=1),
                                mode=0x0A, stage_id=1, hub_resident=False,
                                client=MMX5Client(), ctx=self._ctx())
        self.assertEqual(self._table_writes(ctx), [])

    async def test_inert_when_option_off(self) -> None:
        ctx = self._ctx()
        ctx.slot_data["stage_unlocks"] = 0
        ctx = await run_watcher(make_save(max_hp=0x20, intro=2, weapons=1),
                                mode=0x13, stage_id=0x0D, hub_resident=True,
                                client=MMX5Client(), ctx=ctx)
        self.assertEqual(self._table_writes(ctx), [])

    async def test_blocked_confirm_does_not_leave_stage_id_zero(self) -> None:
        # 0x800EFC98 stores the id BEFORE the game's zero test, so confirming a
        # locked icon parks 0 in 0x800D1C0C - a value vanilla never writes, and
        # one an in-hub save would commit to the memory card.
        client = MMX5Client()
        client.hub_stage_id = 0x0D
        ctx = await run_watcher(make_save(max_hp=0x20, intro=2, weapons=1),
                                mode=0x13, stage_id=0x00, hub_resident=True,
                                client=client, ctx=self._ctx())
        restored = [w[1][0] for w in ctx.writes if w[0] == 0x0D1C0C]
        self.assertEqual(restored, [0x0D])

    async def test_real_stage_id_is_left_alone(self) -> None:
        ctx = await run_watcher(make_save(max_hp=0x20, intro=2, weapons=1),
                                mode=0x13, stage_id=0x0D, hub_resident=True,
                                client=MMX5Client(), ctx=self._ctx())
        self.assertEqual([w for w in ctx.writes if w[0] == 0x0D1C0C], [])
