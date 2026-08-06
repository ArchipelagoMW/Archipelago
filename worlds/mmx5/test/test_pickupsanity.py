"""Pickupsanity: location set, id stability, stub integrity, disc edits."""
import unittest

from worlds.mmx5 import disc, pickups
from worlds.mmx5.items import BASE_ID
from worlds.mmx5.locations import location_table

from . import MMX5TestBase
from .test_client import FakeContext, MMX5Client, make_save, run_watcher

BASE_LOCATION_COUNT = 45          # v0.2.0 shipped count (incl. event-free real locations)
PICKUP_COUNT = 32                 # 33 freestanding consumables minus the intro's


class TestPickupsanityOff(MMX5TestBase):
    options = {"pickupsanity": False}

    def test_no_pickup_locations(self) -> None:
        placed = {loc.name for loc in self.multiworld.get_locations(self.player)}
        for name in pickups.RECORD_TO_LOCATION.values():
            self.assertNotIn(name, placed,
                             "pickup location created with the option off")


class TestPickupsanityOn(MMX5TestBase):
    # endgame_checks off on purpose: this class pins the 45 + 32 arithmetic, so
    # it has to hold the rest of the world still. Its own count is covered in
    # test_endgame_checks.
    options = {"pickupsanity": True, "endgame_checks": False}

    def test_pickup_locations_created(self) -> None:
        placed = {loc.name for loc in self.multiworld.get_locations(self.player)}
        for name in pickups.RECORD_TO_LOCATION.values():
            self.assertIn(name, placed, f"missing pickup location {name}")

    def test_location_count(self) -> None:
        real = [loc for loc in self.multiworld.get_locations(self.player)
                if loc.address is not None]
        self.assertEqual(len(real), BASE_LOCATION_COUNT + PICKUP_COUNT)

    def test_pool_fills(self) -> None:
        # Filler must top the pool up to the new location count - a mismatch
        # here means create_items and the location set disagree.
        real = [loc for loc in self.multiworld.get_locations(self.player)
                if loc.address is not None]
        pool = [i for i in self.multiworld.itempool]
        self.assertEqual(len(pool), len(real))

    def test_all_reachable(self) -> None:
        # With every progression item collected, every pickup location must be
        # reachable - the endgame ones through the Sigma Stages entrance rule.
        state = self.multiworld.get_all_state(False)
        for name in pickups.RECORD_TO_LOCATION.values():
            self.assertTrue(
                self.multiworld.get_location(name, self.player).can_reach(state),
                f"{name} unreachable even with everything")


class TestPickupData(MMX5TestBase):
    """Dataset invariants - no multiworld needed but the base class is cheap."""
    options = {}

    def test_count_and_ids(self) -> None:
        self.assertEqual(len(pickups.PICKUPS), PICKUP_COUNT)
        # Id layout: BASE_ID + 200 + list position, append-only.
        for i, (_s, _a, _idx, _iid, name) in enumerate(pickups.PICKUPS):
            self.assertEqual(location_table[name], BASE_ID + 200 + i)

    def test_no_intro_pickup(self) -> None:
        # The intro capsule is permanently missable (stage not re-enterable)
        # and must never become a location.
        for stage, _a, _idx, _iid, _name in pickups.PICKUPS:
            self.assertNotEqual(stage, 0, "intro pickup must stay excluded")

    def test_record_addresses_unique(self) -> None:
        self.assertEqual(len(pickups.RECORD_TO_LOCATION), len(pickups.PICKUPS))

    def test_stage_ids_are_mapped(self) -> None:
        for stage, _a, _idx, _iid, name in pickups.PICKUPS:
            self.assertIn(stage, pickups.STAGE_PREFIX)
            self.assertEqual(pickups.LOCATION_STAGE_ID[name], stage)

    def test_stub_and_edits(self) -> None:
        # 21 words, ends with j 0x800543C8 (consume tail) + delay-slot commit.
        self.assertEqual(len(disc.PICKUPSANITY_STUB), 21 * 4)
        self.assertEqual(len(disc.PICKUPSANITY_STUB) % 4, 0)
        tail_j = int.from_bytes(disc.PICKUPSANITY_STUB[-8:-4], "little")
        self.assertEqual(tail_j, 0x08000000 | ((0x800543C8 >> 2) & 0x03FFFFFF))
        # Stub must fit inside the verified free-space run (zeros to 0x77800).
        self.assertLessEqual(disc.PICKUPSANITY_STUB_ADDR + len(disc.PICKUPSANITY_STUB),
                             0x80077800)
        edits = disc.pickupsanity_edits()
        # stub + 7 dispatch redirects, every redirect pointing at the stub.
        self.assertEqual(len(edits), 1 + len(disc.CONSUMABLE_KINDS))
        for addr, payload, region in edits[1:]:
            self.assertEqual(payload,
                             disc.PICKUPSANITY_STUB_ADDR.to_bytes(4, "little"))
            self.assertEqual(region, "SLUS exe")
            kind = (addr - disc.DISPATCH_TABLE_ADDR) // 4
            self.assertIn(kind, disc.CONSUMABLE_KINDS)

    def test_ring2_no_overlap_with_ring1(self) -> None:
        # Ring 1: 16*4 at 0x801FA020, count 0x801FA080.
        # Ring 2: 32*8 at 0x801FA100, count 0x801FA200.
        ring2_lo, ring2_hi = 0x801FA100, 0x801FA100 + 32 * 8
        self.assertGreaterEqual(ring2_lo, 0x801FA084)
        self.assertLessEqual(ring2_hi, 0x801FA200)


def ring2_with(records: list[tuple[int, int, int, int]]) -> bytes:
    """Build a ring2 image: (stage, kind, item_id, recptr) per record."""
    import worlds.mmx5.client as c
    ring = bytearray(c.RING2_SLOTS * 8)
    for slot, (stage, kind, iid, recptr) in enumerate(records):
        base = slot * 8
        ring[base:base + 4] = bytes([stage, kind, iid, 0x80 | slot])
        ring[base + 4:base + 8] = recptr.to_bytes(4, "little")
    return bytes(ring)


class TestPickupsanityClient(unittest.IsolatedAsyncioTestCase):
    """Ring-2 record -> location check, via the same harness as the other
    client regression tests."""

    PICKUP = pickups.PICKUPS[0]     # Grizzly Slash - Large Life Energy

    def _ctx(self) -> FakeContext:
        ctx = FakeContext()
        ctx.slot_data = {"goal": 0, "boss_difficulty": 1, "pickupsanity": 1}
        return ctx

    def _client(self) -> MMX5Client:
        client = MMX5Client()
        client.ring2_present = True
        return client

    async def test_record_sends_check(self) -> None:
        stage, area, idx, iid, name = self.PICKUP
        recptr = pickups.record_addr(stage, area, idx)
        ring2 = ring2_with([(stage, 0x3, iid, recptr)])
        ctx = await run_watcher(make_save(max_hp=0x20, intro=2, weapons=1),
                                client=self._client(), ctx=self._ctx(),
                                ring2=ring2)
        self.assertIn(location_table[name], ctx.checked_location_ids())

    async def test_stage_mismatch_does_not_send(self) -> None:
        # A pointer that maps but a stage byte that disagrees is corruption,
        # not a check - it must be dropped, not mis-sent.
        stage, area, idx, iid, name = self.PICKUP
        recptr = pickups.record_addr(stage, area, idx)
        ring2 = ring2_with([(stage + 1, 0x3, iid, recptr)])
        ctx = await run_watcher(make_save(max_hp=0x20, intro=2, weapons=1),
                                client=self._client(), ctx=self._ctx(),
                                ring2=ring2)
        self.assertNotIn(location_table[name], ctx.checked_location_ids())

    async def test_option_off_ignores_ring(self) -> None:
        # Records with the option off (stale RAM, wrong slot_data) must not
        # send anything.
        stage, area, idx, iid, name = self.PICKUP
        recptr = pickups.record_addr(stage, area, idx)
        ring2 = ring2_with([(stage, 0x3, iid, recptr)])
        ctx = self._ctx()
        ctx.slot_data["pickupsanity"] = 0
        ctx = await run_watcher(make_save(max_hp=0x20, intro=2, weapons=1),
                                client=self._client(), ctx=ctx, ring2=ring2)
        self.assertNotIn(location_table[name], ctx.checked_location_ids())

    async def test_confirmed_location_acks_record(self) -> None:
        import worlds.mmx5.client as c
        stage, area, idx, iid, name = self.PICKUP
        recptr = pickups.record_addr(stage, area, idx)
        ring2 = ring2_with([(stage, 0x3, iid, recptr)])
        ctx = self._ctx()
        ctx.checked_locations = {location_table[name]}
        ctx = await run_watcher(make_save(max_hp=0x20, intro=2, weapons=1),
                                client=self._client(), ctx=ctx, ring2=ring2)
        ack_addrs = [w[0] for w in ctx.writes]
        self.assertIn(c.RING2_ADDR + 0 * 8 + 3, ack_addrs,
                      "confirmed record was not acked")
