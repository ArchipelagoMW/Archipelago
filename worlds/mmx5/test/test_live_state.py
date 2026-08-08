"""The two v0.3.4 fixes, both from one tester report (2026-08-08).

1. A weapon received mid-stage did nothing until the player left and re-entered,
   because grants only ever reached the SAVE struct and the live bitfield is
   what the game consults during play.
2. With pickupsanity on, a capsule stayed inert for the whole run even after
   its check was long since sent - which makes the Boss Rush a slog.

Both fixes are deliberately downstream of state decided elsewhere, so the tests
below pin the *guards* as much as the behaviour: the live mirror must never
invent a weapon the save does not have, and the dispatch toggle must never
relax suppression for a check the server has not confirmed.
"""
import unittest

from worlds.mmx5 import client as mmx5_client
from worlds.mmx5 import pickups
from worlds.mmx5.locations import location_table

from .test_client import FakeContext, MMX5Client, make_save, run_watcher


def stage_locations(stage_id: int) -> list[int]:
    return [location_table[name]
            for stage, _a, _i, _iid, name in pickups.PICKUPS if stage == stage_id]


class TestLiveWeaponMirror(unittest.IsolatedAsyncioTestCase):

    async def test_granted_weapons_reach_the_live_bitfield(self) -> None:
        # Save says two weapons are owned; the live byte was rebuilt without
        # them (the state right after a mid-stage grant).
        client = MMX5Client()
        client.ap_patched = True
        save = bytearray(make_save(max_hp=0x20))
        save[mmx5_client.OFF_AP_WEAPONS] = 0x05
        ctx = await run_watcher(bytes(save), client=client, live_weapons=0x00)
        self.assertIn(0x05, ctx.live_weapon_writes(),
                      "granted weapons never reached the live bitfield")

    async def test_existing_live_bits_are_preserved(self) -> None:
        # OR, never assign: the game owns this byte during play.
        client = MMX5Client()
        client.ap_patched = True
        save = bytearray(make_save(max_hp=0x20))
        save[mmx5_client.OFF_AP_WEAPONS] = 0x01
        ctx = await run_watcher(bytes(save), client=client, live_weapons=0x80)
        self.assertEqual(ctx.live_weapon_writes(), [0x81])

    async def test_no_write_when_already_correct(self) -> None:
        client = MMX5Client()
        client.ap_patched = True
        save = bytearray(make_save(max_hp=0x20))
        save[mmx5_client.OFF_AP_WEAPONS] = 0x03
        ctx = await run_watcher(bytes(save), client=client, live_weapons=0x03)
        self.assertEqual(ctx.live_weapon_writes(), [],
                         "wrote the live byte with nothing to change")

    async def test_never_invents_a_weapon_the_save_lacks(self) -> None:
        # The whole safety argument: this mirror is strictly downstream of the
        # grant path. An empty capability byte must produce no write at all.
        client = MMX5Client()
        client.ap_patched = True
        ctx = await run_watcher(make_save(max_hp=0x20), client=client,
                                live_weapons=0x00)
        self.assertEqual(ctx.live_weapon_writes(), [])

    async def test_not_written_outside_gameplay(self) -> None:
        # 0x9Axxx is garbage outside gameplay; the stage load restores it.
        client = MMX5Client()
        client.ap_patched = True
        save = bytearray(make_save(max_hp=0x20))
        save[mmx5_client.OFF_AP_WEAPONS] = 0x0F
        ctx = await run_watcher(bytes(save), mode=0x0C, client=client,
                                live_weapons=0x00)
        self.assertEqual(ctx.live_weapon_writes(), [],
                         "wrote the volatile block while not in gameplay")

    async def test_vanilla_disc_uses_the_vanilla_capability_byte(self) -> None:
        # Hybrid mode: an unpatched disc keeps capability in 0x1C4C.
        client = MMX5Client()
        client.ap_patched = False
        save = bytearray(make_save(max_hp=0x20, weapons=0x06))
        ctx = await run_watcher(bytes(save), client=client, live_weapons=0x00,
                                patch_probe=mmx5_client.PATCH_PROBE_VANILLA)
        # An unpatched disc is held entirely, so nothing should be written.
        self.assertEqual(ctx.live_weapon_writes(), [])


class TestPickupDispatchToggle(unittest.IsolatedAsyncioTestCase):
    """Per-stage, because the dispatch table is indexed by item KIND - it
    cannot be relaxed for one capsule. Only one stage's placement list is live
    at a time, so a stage is the finest grain available."""

    STAGE = 3            # Duff McWhalen: 4 pickup locations

    def _ctx(self, checked) -> FakeContext:
        ctx = FakeContext()
        ctx.slot_data = {"goal": 0, "boss_difficulty": 1, "pickupsanity": 1}
        ctx.checked_locations = set(checked)
        return ctx

    def _client(self) -> MMX5Client:
        client = MMX5Client()
        client.ap_patched = True
        client.ring2_present = True
        return client

    async def test_vanilla_restored_when_the_stage_is_cleared_out(self) -> None:
        locs = stage_locations(self.STAGE)
        self.assertTrue(locs, "test needs a stage that has pickup locations")
        ctx = await run_watcher(make_save(max_hp=0x20), stage_id=self.STAGE,
                                client=self._client(), ctx=self._ctx(locs))
        self.assertEqual(ctx.dispatch_writes(), mmx5_client.VANILLA_DISPATCH,
                         "a fully-collected stage did not get its capsules back")

    async def test_stub_kept_while_a_check_is_outstanding(self) -> None:
        locs = stage_locations(self.STAGE)
        ctx = await run_watcher(make_save(max_hp=0x20), stage_id=self.STAGE,
                                client=self._client(),
                                ctx=self._ctx(locs[:-1]))   # one still missing
        self.assertEqual(
            set(ctx.dispatch_writes().values()), {mmx5_client.PICKUPSANITY_STUB_ADDR},
            "suppression was relaxed with a check still outstanding")

    async def test_stage_with_no_pickup_locations_gets_vanilla(self) -> None:
        # Squid Adler (5) holds no consumables, and the intro's single capsule
        # is deliberately not a location. Suppressing those was never intended.
        self.assertEqual(stage_locations(5), [])
        ctx = await run_watcher(make_save(max_hp=0x20), stage_id=5,
                                client=self._client(), ctx=self._ctx([]))
        self.assertEqual(ctx.dispatch_writes(), mmx5_client.VANILLA_DISPATCH)

    async def test_stub_kept_outside_gameplay(self) -> None:
        locs = stage_locations(self.STAGE)
        ctx = await run_watcher(make_save(max_hp=0x20), mode=0x0C,
                                stage_id=self.STAGE, client=self._client(),
                                ctx=self._ctx(locs))
        self.assertEqual(
            set(ctx.dispatch_writes().values()), {mmx5_client.PICKUPSANITY_STUB_ADDR},
            "relaxed suppression outside gameplay")

    async def test_untouched_when_pickupsanity_is_off(self) -> None:
        ctx = FakeContext()
        ctx.slot_data = {"goal": 0, "boss_difficulty": 1, "pickupsanity": 0}
        ctx = await run_watcher(make_save(max_hp=0x20), stage_id=self.STAGE,
                                client=self._client(), ctx=ctx)
        self.assertEqual(ctx.dispatch_writes(), {},
                         "wrote the dispatch table on a seed without pickupsanity")

    async def test_untouched_on_a_disc_without_the_stub(self) -> None:
        client = self._client()
        client.ring2_present = False
        ctx = await run_watcher(make_save(max_hp=0x20), stage_id=self.STAGE,
                                client=client, ctx=self._ctx([]))
        self.assertEqual(ctx.dispatch_writes(), {},
                         "wrote the dispatch table on a disc that has no stub")


class TestRing2Classifier(unittest.TestCase):
    """The dispatch entry alone stopped being a safe presence probe once the
    client began rewriting it: restore a cleared stage's capsules, walk out,
    and the gate-transition re-probe would read "vanilla" and switch
    pickupsanity check detection off for the rest of the session."""

    def test_stub_word_wins_over_an_overridden_table(self) -> None:
        self.assertIs(
            MMX5Client._classify_ring2(mmx5_client.RING2_STUB_WORD,
                                       mmx5_client.RING2_PROBE_VANILLA),
            True,
            "our own vanilla override was read back as 'not a pickupsanity disc'")

    def test_real_vanilla_disc(self) -> None:
        self.assertIs(
            MMX5Client._classify_ring2(b"\x00\x00\x00\x00",
                                       mmx5_client.RING2_PROBE_VANILLA),
            False)

    def test_boot_zeros_retry(self) -> None:
        self.assertIsNone(
            MMX5Client._classify_ring2(b"\x00\x00\x00\x00", b"\x00\x00\x00\x00"))

    def test_stub_word_matches_the_disc_patch(self) -> None:
        from worlds.mmx5 import disc
        self.assertEqual(mmx5_client.RING2_STUB_WORD,
                         disc.PICKUPSANITY_STUB[:4],
                         "probe word drifted from the stub the patcher writes")
        self.assertEqual(mmx5_client.PICKUPSANITY_STUB_ADDR,
                         disc.PICKUPSANITY_STUB_ADDR)
        self.assertEqual(mmx5_client.CONSUMABLE_KINDS, disc.CONSUMABLE_KINDS)
        self.assertEqual(mmx5_client.RING2_STUB_PROBE_ADDR,
                         disc.PICKUPSANITY_STUB_ADDR - 0x80000000)
