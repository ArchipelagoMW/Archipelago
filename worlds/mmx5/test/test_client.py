"""Regression tests for the bugs found in the v0.1.0 test release.

Each test here corresponds to a failure a tester actually hit. They are
written to FAIL against v0.1.0 and pass after the fixes.
"""
import unittest
from types import SimpleNamespace
from unittest import mock

import worlds._bizhawk as bizhawk
from worlds.LauncherComponents import components

from .. import client as mmx5_client
from ..client import MMX5Client
from ..locations import location_table
from .. import names


class FakeContext:
    """Minimal stand-in for BizHawkClientContext."""

    def __init__(self) -> None:
        self.server = object()
        self.slot = 1
        self.bizhawk_ctx = object()
        self.checked_locations = set()
        self.slot_data = {"goal": 0, "boss_difficulty": 1}
        self.seed_name = "TESTSEED"
        self.auth = "Player1"
        self.items_received = []
        self.item_names = SimpleNamespace(lookup_in_game=lambda code: "")
        self.sent_msgs = []

    async def send_msgs(self, msgs) -> None:
        self.sent_msgs.extend(msgs)

    def checked_location_ids(self) -> set:
        ids = set()
        for msg in self.sent_msgs:
            if msg.get("cmd") == "LocationChecks":
                ids.update(msg["locations"])
        return ids


def make_save(max_hp: int, intro: int = 0, weapons: int = 0, hearts: int = 0) -> bytes:
    save = bytearray(mmx5_client.SAVE_LEN)
    save[mmx5_client.OFF_MAX_HP_X] = max_hp
    save[mmx5_client.OFF_INTRO] = intro
    save[mmx5_client.OFF_WEAPONS] = weapons
    save[mmx5_client.OFF_HEARTS] = hearts
    return bytes(save)


async def run_watcher(save: bytes, mode: int = 0x0A) -> FakeContext:
    ctx = FakeContext()
    client = MMX5Client()
    ring = bytes(mmx5_client.RING_SLOTS * 4)

    async def fake_read(_ctx, requests):
        # 3 reads = the main (mode, save, ring) cycle; 2 = the disc-mode probes.
        if len(requests) == 3:
            return [bytes([mode]), save, ring]
        return [b"\x00\x00\x00\x00"] * len(requests)

    async def fake_write(*_args, **_kwargs):
        return True

    with mock.patch.object(bizhawk, "read", fake_read), \
            mock.patch.object(bizhawk, "write", fake_write), \
            mock.patch.object(bizhawk, "guarded_write", fake_write):
        await client.game_watcher(ctx)
    return ctx


class TestCheckDetectionGating(unittest.IsolatedAsyncioTestCase):
    """A tester got a phantom "Intro Stage - Clear" while the save-struct gate
    was logging False (max HP 0x00) - checks were being derived from stale RAM
    left over from a previous session, before any save was resident."""

    async def test_no_checks_from_unloaded_save_struct(self) -> None:
        # Max HP 0x00 => struct not resident. The other bytes are stale
        # garbage that happens to look like real progress.
        ctx = await run_watcher(make_save(max_hp=0x00, intro=0x05))
        self.assertEqual(ctx.checked_location_ids(), set(),
                         "checks were sent from a save struct that is not resident")

    async def test_stale_weapon_byte_cannot_fire_boss_checks(self) -> None:
        # The dangerous case: stale 0xFF in the weapons byte would have
        # falsely completed all 8 bosses plus their DNA locations.
        ctx = await run_watcher(make_save(max_hp=0x00, intro=0xFF, weapons=0xFF, hearts=0xFF))
        self.assertEqual(ctx.checked_location_ids(), set(),
                         "stale RAM falsely completed boss/DNA/heart checks")

    async def test_checks_still_sent_from_a_resident_save(self) -> None:
        # The fix must not break real detection: a loaded save reads sane.
        ctx = await run_watcher(make_save(max_hp=0x20, intro=0x01))
        self.assertIn(location_table[names.INTRO_CLEAR], ctx.checked_location_ids(),
                      "intro check was not sent from a valid save")

    async def test_boss_checks_from_a_resident_save(self) -> None:
        ctx = await run_watcher(make_save(max_hp=0x20, weapons=0x01))
        sent = ctx.checked_location_ids()
        stage = next(s for s, w in names.BOSS_WEAPON.items()
                     if w == mmx5_client.WEAPON_BITS[0])
        self.assertIn(location_table[names.boss_location(stage)], sent)
        self.assertIn(location_table[names.dna_location(stage)], sent)


class TestLauncherRegistration(unittest.TestCase):
    """v0.1.0 never registered its patch suffix, so the Launcher's Open Patch
    dialog did not list .apmmx5 and could not route the file to a handler."""

    def test_patch_suffix_declared(self) -> None:
        self.assertEqual(MMX5Client.patch_suffix, ".apmmx5")

    def test_suffix_reaches_the_bizhawk_launcher_component(self) -> None:
        bizhawk_components = [c for c in components if c.script_name == "BizHawkClient"]
        self.assertTrue(bizhawk_components, "BizHawk Client component missing")
        suffixes = bizhawk_components[0].file_identifier.suffixes
        self.assertIn(".apmmx5", suffixes,
                      "Open Patch will not offer .apmmx5 to players")

    def test_suffix_matches_the_patch_file_ending(self) -> None:
        from ..Rom import MMX5ProcedurePatch
        self.assertEqual(MMX5Client.patch_suffix, MMX5ProcedurePatch.patch_file_ending)


if __name__ == "__main__":
    unittest.main()
