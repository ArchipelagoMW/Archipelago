"""Life Energy delivery — heal first, spill into an owned sub-tank.

Guards the 2026-08-13 fix. The client used to write received energy into
0x1C76 + charIdx as if those were per-character refill queues; they are the
two SUB-TANKS' fill bytes (sub-tank pickup handler 0x80054264 selects the byte
from the pickup id, 0x27 -> 0x1C76 / 0x28 -> 0x1C77). The old code therefore
healed nothing at any HP, wrote the wrong tank whenever Zero was selected,
ignored tank ownership, and clamped to 0x7F against the engine's own 0x20 cap.

Reference behaviour is the vanilla pickup helper 0x80053E3C:
  HP < max            -> heal, clamped to max HP
  HP == max           -> +2 into the first owned tank with fill < 0x20
  no room anywhere    -> discarded
and the store is always `fill | 0x80` (0x80053FA4 / 0x80053FB4).
"""
import unittest

from .. import client as client_mod
from ..client import (MMX5Client, SAVE_BASE, SMALL_ENERGY_HEAL, SUB_TANK_FILL_MAX,
                      SUB_TANK_FILL_PER_ENERGY, SUB_TANK_BYTE_BITS,
                      OFF_SUB_TANK_FILL, SAVE_LEN)
from .test_client import FakeContext, make_save, run_watcher

TANK1, TANK2 = SUB_TANK_BYTE_BITS
MAX_HP = 0x20


def plan(count, hp_raw, max_hp=MAX_HP, tanks=0, fills=(0, 0), can_heal=True):
    return MMX5Client._energy_plan(count, hp_raw, max_hp, tanks, fills, can_heal)


class TestEnergyConstants(unittest.TestCase):
    """These are facts about the game, not tunables.

    Every other test here spells the constants symbolically, so a wrong value
    would sail through all of them. Pin the numbers to the disassembly.
    """

    def test_heal_matches_the_small_capsule(self):
        # 0x80054184: `addiu $a1, $zero, 4` - the amount the kind-2 handler
        # hands to the pickup helper 0x80053E3C.
        self.assertEqual(SMALL_ENERGY_HEAL, 4)

    def test_spill_matches_what_a_capsule_adds_to_a_tank(self):
        # 0x80053F74: `sll $v0, $s5, 1` with s5 = 1 for life energy - the
        # tank gains 2, not the 4 HP the same capsule would have healed.
        self.assertEqual(SUB_TANK_FILL_PER_ENERGY, 2)

    def test_cap_matches_the_engine(self):
        # 0x80053F6C / 0x80053F84: `slti $v1, $s0, 0x20`. The old code used
        # 0x7F, which is what overfilled testers' tanks.
        self.assertEqual(SUB_TANK_FILL_MAX, 0x20)


class TestEnergyHeals(unittest.TestCase):
    def test_heals_below_max(self):
        hp, fills = plan(1, 0x10, tanks=TANK1)
        self.assertEqual(hp, 0x10 + SMALL_ENERGY_HEAL)
        self.assertEqual(fills, [None, None], "healing must not touch a tank")

    def test_heal_clamps_to_max_hp(self):
        hp, _ = plan(4, MAX_HP - 1)
        self.assertEqual(hp, MAX_HP)

    def test_preserves_the_just_damaged_flag(self):
        # bit 7 of the live HP byte is the damage flag; the engine's own heal
        # re-ORs it back on (0x800342D0). Dropping it would clear game state.
        hp, _ = plan(1, 0x80 | 0x10)
        self.assertEqual(hp, 0x80 | (0x10 + SMALL_ENERGY_HEAL))

    def test_leftover_of_a_partial_heal_is_not_banked(self):
        # Vanilla is per-pickup: a capsule that only restores 1 of its 4 is
        # spent. The second item then finds full HP and spills.
        hp, fills = plan(2, MAX_HP - 1, tanks=TANK1)
        self.assertEqual(hp, MAX_HP)
        self.assertEqual(fills[0], SUB_TANK_FILL_PER_ENERGY | 0x80)


class TestEnergySpills(unittest.TestCase):
    def test_full_hp_fills_the_first_owned_tank(self):
        hp, fills = plan(1, MAX_HP, tanks=TANK1 | TANK2)
        self.assertIsNone(hp, "no HP write at full health")
        self.assertEqual(fills[0], SUB_TANK_FILL_PER_ENERGY | 0x80)
        self.assertIsNone(fills[1], "tank 2 must not take it while tank 1 has room")

    def test_moves_to_tank_two_when_tank_one_is_full(self):
        _, fills = plan(1, MAX_HP, tanks=TANK1 | TANK2,
                        fills=(SUB_TANK_FILL_MAX, 0))
        self.assertIsNone(fills[0])
        self.assertEqual(fills[1], SUB_TANK_FILL_PER_ENERGY | 0x80)

    def test_skips_a_tank_that_is_not_owned(self):
        # Owning only tank 2 must fill tank 2 - the old bug wrote a byte the
        # player did not own, so the energy vanished.
        _, fills = plan(1, MAX_HP, tanks=TANK2)
        self.assertIsNone(fills[0])
        self.assertEqual(fills[1], SUB_TANK_FILL_PER_ENERGY | 0x80)

    def test_discarded_when_no_tank_is_owned(self):
        hp, fills = plan(3, MAX_HP, tanks=0)
        self.assertIsNone(hp)
        self.assertEqual(fills, [None, None],
                         "must never write a tank byte the player does not own")

    def test_never_exceeds_the_engine_cap(self):
        _, fills = plan(64, MAX_HP, tanks=TANK1 | TANK2)
        self.assertEqual(fills, [SUB_TANK_FILL_MAX | 0x80, SUB_TANK_FILL_MAX | 0x80])

    def test_clamps_from_a_partly_drained_tank(self):
        # A tank drains 1/tick, so its fill can be ODD. Filling from 0x1F
        # overshoots the cap by one unless the add is clamped - and a tank
        # topped up from 0 only ever lands on even values, so the plain
        # "fill it 64 times" test cannot see this.
        _, fills = plan(1, MAX_HP, tanks=TANK1, fills=(SUB_TANK_FILL_MAX - 1, 0))
        self.assertEqual(fills[0], SUB_TANK_FILL_MAX | 0x80)

    def test_leaves_an_already_overfilled_tank_alone(self):
        # Residue of the old bug: fill can be up to 0x7F. Do not add to it
        # (the standalone repair clamps it; this path must not make it worse).
        _, fills = plan(1, MAX_HP, tanks=TANK1, fills=(0x7F, 0))
        self.assertIsNone(fills[0])

    def test_fill_write_carries_the_present_bit(self):
        _, fills = plan(1, MAX_HP, tanks=TANK1)
        self.assertTrue(fills[0] & 0x80,
                        "engine stores fill | 0x80; a bare fill loses the tank")


class TestEnergyRefusesUntrustedHP(unittest.TestCase):
    def test_results_screen_never_writes_hp(self):
        # save_trusted covers mode 0x0C (results), where the player object is
        # not live. The energy must go to a tank instead of a stale HP byte.
        hp, fills = plan(1, 0x10, tanks=TANK1, can_heal=False)
        self.assertIsNone(hp)
        self.assertEqual(fills[0], SUB_TANK_FILL_PER_ENERGY | 0x80)

    def test_dead_or_wiped_player_block_never_heals(self):
        hp, fills = plan(1, 0x00, tanks=TANK1)
        self.assertIsNone(hp)
        self.assertEqual(fills[0], SUB_TANK_FILL_PER_ENERGY | 0x80)

    def test_impossible_hp_reading_never_heals(self):
        # HP above max means we are not looking at a live player.
        hp, fills = plan(1, MAX_HP + 1, tanks=TANK1)
        self.assertIsNone(hp)
        self.assertEqual(fills[0], SUB_TANK_FILL_PER_ENERGY | 0x80)


class TestEnergyNoOps(unittest.TestCase):
    def test_zero_items_writes_nothing(self):
        self.assertEqual(plan(0, 0x10, tanks=TANK1 | TANK2), (None, [None, None]))

    def test_unchanged_bytes_are_not_rewritten(self):
        # Full HP, both tanks full: nothing may be written at all.
        hp, fills = plan(2, MAX_HP, tanks=TANK1 | TANK2,
                         fills=(SUB_TANK_FILL_MAX, SUB_TANK_FILL_MAX))
        self.assertIsNone(hp)
        self.assertEqual(fills, [None, None])


class TestSubTankOvercapRepair(unittest.TestCase):
    """Repairs saves the old energy path poisoned (fill up to 0x7F)."""

    @staticmethod
    def save_with(fill1, fill2):
        save = bytearray(SAVE_LEN)
        save[OFF_SUB_TANK_FILL[0]] = fill1
        save[OFF_SUB_TANK_FILL[1]] = fill2
        return bytes(save)

    def test_clamps_an_overfilled_tank(self):
        writes = MMX5Client._sub_tank_overcap_writes(self.save_with(0x7F | 0x80, 0))
        self.assertEqual(writes, [(SAVE_BASE + OFF_SUB_TANK_FILL[0],
                                   [SUB_TANK_FILL_MAX | 0x80], "MainRAM")])

    def test_clamps_both_tanks(self):
        writes = MMX5Client._sub_tank_overcap_writes(self.save_with(0x60, 0x40))
        self.assertEqual(len(writes), 2)

    def test_a_legal_tank_is_never_rewritten(self):
        # Exactly at the cap, and a normal part-full tank. Rewriting these
        # every poll would fight the engine as the player drains one.
        for fill in (0, 1, SUB_TANK_FILL_MAX - 1, SUB_TANK_FILL_MAX):
            with self.subTest(fill=fill):
                save = self.save_with(fill | 0x80, fill)
                self.assertEqual(MMX5Client._sub_tank_overcap_writes(save), [])

    def test_the_present_bit_is_not_mistaken_for_fill(self):
        # 0x80 = owned and EMPTY. Reading the raw byte instead of `& 0x7F`
        # makes every owned tank look overfilled and clamps it to full.
        self.assertEqual(MMX5Client._sub_tank_overcap_writes(self.save_with(0x80, 0x80)), [])


class TestEnergyThroughTheWatcher(unittest.IsolatedAsyncioTestCase):
    """End to end through game_watcher.

    The plan is pure and heavily unit-tested, but every one of its arguments
    is wired up at the call site - live HP, max HP for the SELECTED character,
    post-grant tank ownership, and whether this poll is gameplay or the
    results screen. A swapped or stale argument passes every unit test above.
    """

    @staticmethod
    def energy_ctx(count=1):
        from types import SimpleNamespace
        from ..items import item_table
        from .. import names as item_names
        code = item_table[item_names.SMALL_ENERGY].code
        id_to_name = {data.code: name for name, data in item_table.items()}
        ctx = FakeContext()
        ctx.items_received = [SimpleNamespace(item=code)] * count
        ctx.item_names = SimpleNamespace(lookup_in_game=lambda c: id_to_name[c])
        return ctx

    @staticmethod
    def save_for(tanks=0, fills=(0, 0), char=0):
        save = bytearray(make_save(max_hp=MAX_HP, tanks=tanks))
        save[client_mod.OFF_MAX_HP_Z] = MAX_HP
        save[client_mod.OFF_CHAR] = char
        save[OFF_SUB_TANK_FILL[0]] = fills[0]
        save[OFF_SUB_TANK_FILL[1]] = fills[1]
        return bytes(save)

    @staticmethod
    def patched_client():
        c = MMX5Client()
        c.tank_fix_present = True   # keeps the tank-withhold path out of the way
        return c

    def writes_to(self, ctx, addr):
        return [w[1][0] for w in ctx.writes if w[0] == addr]

    async def test_energy_heals_the_live_player(self):
        ctx = await run_watcher(self.save_for(), ctx=self.energy_ctx(),
                                client=self.patched_client(), player_hp=0x10)
        self.assertEqual(self.writes_to(ctx, client_mod.PLAYER_HP_ADDR),
                         [0x10 + SMALL_ENERGY_HEAL],
                         "received Life Energy did not heal the player")

    async def test_energy_at_full_hp_fills_the_owned_tank(self):
        ctx = await run_watcher(self.save_for(tanks=TANK1),
                                ctx=self.energy_ctx(),
                                client=self.patched_client(), player_hp=MAX_HP)
        self.assertEqual(self.writes_to(ctx, SAVE_BASE + OFF_SUB_TANK_FILL[0]),
                         [SUB_TANK_FILL_PER_ENERGY | 0x80])
        self.assertEqual(self.writes_to(ctx, client_mod.PLAYER_HP_ADDR), [])

    async def test_playing_zero_still_fills_tank_one(self):
        # THE REGRESSION. The old code indexed the fill byte by CHARACTER, so
        # selecting Zero wrote Sub-Tank 2 - a tank the player here does not
        # even own.
        ctx = await run_watcher(self.save_for(tanks=TANK1, char=1),
                                ctx=self.energy_ctx(),
                                client=self.patched_client(), player_hp=MAX_HP)
        self.assertEqual(self.writes_to(ctx, SAVE_BASE + OFF_SUB_TANK_FILL[0]),
                         [SUB_TANK_FILL_PER_ENERGY | 0x80])
        self.assertEqual(self.writes_to(ctx, SAVE_BASE + OFF_SUB_TANK_FILL[1]), [],
                         "energy went to Sub-Tank 2 because Zero was selected")

    async def test_the_heal_is_guarded_on_the_hp_it_was_computed_from(self):
        # The written value is `HP-as-read + 4`, off a read taken at the top
        # of the poll. Unguarded, damage taken in between is partly undone -
        # the write puts HP back above what the player actually has.
        ctx = await run_watcher(self.save_for(), ctx=self.energy_ctx(),
                                client=self.patched_client(), player_hp=0x10)
        guarded = [g for batch in ctx.write_guards for g in batch
                   if g[0] == client_mod.PLAYER_HP_ADDR]
        self.assertEqual(guarded, [(client_mod.PLAYER_HP_ADDR, bytes([0x10]), "MainRAM")])

    async def test_no_hp_guard_when_no_heal_is_written(self):
        # Guarding on HP when we are not writing it would stall every grant
        # batch that happens to land while the player is taking damage.
        ctx = await run_watcher(self.save_for(tanks=TANK1), ctx=self.energy_ctx(),
                                client=self.patched_client(), player_hp=MAX_HP)
        guarded = [g for batch in ctx.write_guards for g in batch
                   if g[0] == client_mod.PLAYER_HP_ADDR]
        self.assertEqual(guarded, [])

    async def test_fills_a_tank_that_carries_the_present_bit(self):
        # A tank picked up in game reads 0x80 - present, empty. Passing the
        # raw byte as the fill makes every real tank look over the 0x20 cap,
        # so the energy silently goes nowhere. A test seeded with a bare 0x00
        # cannot see that: it is a state only a save AP wrote ever has.
        ctx = await run_watcher(self.save_for(tanks=TANK1, fills=(0x80, 0)),
                                ctx=self.energy_ctx(),
                                client=self.patched_client(), player_hp=MAX_HP)
        self.assertEqual(self.writes_to(ctx, SAVE_BASE + OFF_SUB_TANK_FILL[0]),
                         [SUB_TANK_FILL_PER_ENERGY | 0x80])

    async def test_zeros_own_max_hp_is_the_clamp(self):
        # X and Zero have separate max HP. Clamping Zero's heal against X's
        # would cap him at 0x20 here. Both bytes exist in every save, so a
        # test where they are equal cannot tell the two apart.
        save = bytearray(self.save_for(char=1))
        save[client_mod.OFF_MAX_HP_Z] = 0x40
        ctx = await run_watcher(bytes(save), ctx=self.energy_ctx(4),
                                client=self.patched_client(), player_hp=0x1F)
        self.assertEqual(self.writes_to(ctx, client_mod.PLAYER_HP_ADDR),
                         [0x1F + 4 * SMALL_ENERGY_HEAL])

    async def test_no_hp_write_on_the_results_screen(self):
        # 0x0C is trusted for the save struct but the player object is not
        # live there, so HP must not be touched - it spills instead.
        ctx = await run_watcher(self.save_for(tanks=TANK1), mode=0x0C,
                                ctx=self.energy_ctx(),
                                client=self.patched_client(), player_hp=0x10)
        self.assertEqual(self.writes_to(ctx, client_mod.PLAYER_HP_ADDR), [],
                         "wrote HP off a player object that is not resident")
        self.assertEqual(self.writes_to(ctx, SAVE_BASE + OFF_SUB_TANK_FILL[0]),
                         [SUB_TANK_FILL_PER_ENERGY | 0x80])

    async def test_a_tank_granted_in_the_same_batch_can_take_the_spill(self):
        # Ownership must come from the POST-grant value: receiving a Sub-Tank
        # and energy together in one batch is ordinary multiworld traffic.
        from types import SimpleNamespace
        from ..items import item_table
        from .. import names as item_names
        id_to_name = {data.code: name for name, data in item_table.items()}
        ctx = FakeContext()
        ctx.items_received = [
            SimpleNamespace(item=item_table[item_names.SUB_TANK].code),
            SimpleNamespace(item=item_table[item_names.SMALL_ENERGY].code)]
        ctx.item_names = SimpleNamespace(lookup_in_game=lambda c: id_to_name[c])
        ctx = await run_watcher(self.save_for(tanks=0), ctx=ctx,
                                client=self.patched_client(), player_hp=MAX_HP)
        self.assertEqual(self.writes_to(ctx, SAVE_BASE + OFF_SUB_TANK_FILL[0]),
                         [SUB_TANK_FILL_PER_ENERGY | 0x80])

    async def test_the_repair_does_not_stall_the_rest_of_the_cycle(self):
        # The repair used to `return` after writing. If that write ever failed
        # to stick, every poll would bail at that line and the client would
        # stop sending checks entirely - a hard stall. The cycle must carry on
        # in the SAME poll, which the grant batch's processed-count write
        # proves: it happens further down the same function.
        ctx = await run_watcher(self.save_for(tanks=TANK1, fills=(0x7F, 0)),
                                ctx=self.energy_ctx(),
                                client=self.patched_client(), player_hp=0x10)
        self.assertEqual(self.writes_to(ctx, SAVE_BASE + OFF_SUB_TANK_FILL[0]),
                         [SUB_TANK_FILL_MAX | 0x80], "the tank was not repaired")
        self.assertNotEqual(
            self.writes_to(ctx, SAVE_BASE + client_mod.OFF_PROCESSED), [],
            "the grant batch never ran - the cycle stalled at the repair")

    async def test_a_poisoned_tank_is_clamped_on_sight(self):
        # No energy received at all: the repair is not part of the grant path.
        ctx = await run_watcher(self.save_for(tanks=TANK1, fills=(0x7F, 0)),
                                client=self.patched_client(), player_hp=MAX_HP)
        self.assertEqual(self.writes_to(ctx, SAVE_BASE + OFF_SUB_TANK_FILL[0]),
                         [SUB_TANK_FILL_MAX | 0x80])

    async def test_a_legal_tank_is_left_alone(self):
        ctx = await run_watcher(self.save_for(tanks=TANK1, fills=(0x10 | 0x80, 0)),
                                client=self.patched_client(), player_hp=MAX_HP)
        self.assertEqual(self.writes_to(ctx, SAVE_BASE + OFF_SUB_TANK_FILL[0]), [])


if __name__ == "__main__":
    unittest.main()
