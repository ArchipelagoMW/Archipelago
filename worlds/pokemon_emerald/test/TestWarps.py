from argparse import Namespace

from BaseClasses import MultiWorld
from worlds.pokemon_emerald.Warps import get_warp_map, warps_connect_ltr
from test.TestBase import TestBase
from worlds import AutoWorld

class TestWarps(TestBase):
    def test_warps_connect_ltr(self):
        # 2-way
        self.assertTrue(warps_connect_ltr(
            "FAKE_MAP_A:0/FAKE_MAP_B:0",
            "FAKE_MAP_B:0/FAKE_MAP_A:0"
        ))
        self.assertTrue(warps_connect_ltr(
            "FAKE_MAP_A:0/FAKE_MAP_B:2",
            "FAKE_MAP_B:2/FAKE_MAP_A:0"
        ))
        self.assertTrue(warps_connect_ltr(
            "FAKE_MAP_A:0,1/FAKE_MAP_B:2",
            "FAKE_MAP_B:2/FAKE_MAP_A:0"
        ))
        self.assertTrue(warps_connect_ltr(
            "FAKE_MAP_A:0/FAKE_MAP_B:2",
            "FAKE_MAP_B:2,3/FAKE_MAP_A:0"
        ))

        # 1-way
        self.assertTrue(warps_connect_ltr(
            "FAKE_MAP_A:0/FAKE_MAP_B:2",
            "FAKE_MAP_B:2/FAKE_MAP_A:3"
        ))
        self.assertTrue(warps_connect_ltr(
            "FAKE_MAP_A:0,1/FAKE_MAP_B:2",
            "FAKE_MAP_B:2/FAKE_MAP_A:3"
        ))
        self.assertTrue(warps_connect_ltr(
            "FAKE_MAP_A:0/FAKE_MAP_B:2",
            "FAKE_MAP_B:2,3/FAKE_MAP_A:3"
        ))

        # Invalid
        self.assertFalse(warps_connect_ltr(
            "FAKE_MAP_A:0/FAKE_MAP_B:2",
            "FAKE_MAP_B:4/FAKE_MAP_A:0"
        ))
        self.assertFalse(warps_connect_ltr(
            "FAKE_MAP_A:0,4/FAKE_MAP_B:2",
            "FAKE_MAP_B:4/FAKE_MAP_A:0"
        ))
        self.assertFalse(warps_connect_ltr(
            "FAKE_MAP_A:0,4/FAKE_MAP_B:2",
            "FAKE_MAP_C:2/FAKE_MAP_A:0"
        ))

