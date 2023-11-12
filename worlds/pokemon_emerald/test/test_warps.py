from test.TestBase import TestBase
from ..data import Warp


class TestWarps(TestBase):
    def test_warps_connect_ltr(self) -> None:
        # 2-way
        self.assertTrue(Warp("FAKE_MAP_A:0/FAKE_MAP_B:0").connects_to(Warp("FAKE_MAP_B:0/FAKE_MAP_A:0")))
        self.assertTrue(Warp("FAKE_MAP_A:0/FAKE_MAP_B:2").connects_to(Warp("FAKE_MAP_B:2/FAKE_MAP_A:0")))
        self.assertTrue(Warp("FAKE_MAP_A:0,1/FAKE_MAP_B:2").connects_to(Warp("FAKE_MAP_B:2/FAKE_MAP_A:0")))
        self.assertTrue(Warp("FAKE_MAP_A:0/FAKE_MAP_B:2").connects_to(Warp("FAKE_MAP_B:2,3/FAKE_MAP_A:0")))

        # 1-way
        self.assertTrue(Warp("FAKE_MAP_A:0/FAKE_MAP_B:2!").connects_to(Warp("FAKE_MAP_B:2/FAKE_MAP_A:3")))
        self.assertTrue(Warp("FAKE_MAP_A:0,1/FAKE_MAP_B:2!").connects_to(Warp("FAKE_MAP_B:2/FAKE_MAP_A:3")))
        self.assertTrue(Warp("FAKE_MAP_A:0/FAKE_MAP_B:2!").connects_to(Warp("FAKE_MAP_B:2,3/FAKE_MAP_A:3")))

        # Invalid
        self.assertFalse(Warp("FAKE_MAP_A:0/FAKE_MAP_B:2").connects_to(Warp("FAKE_MAP_B:4/FAKE_MAP_A:0")))
        self.assertFalse(Warp("FAKE_MAP_A:0,4/FAKE_MAP_B:2").connects_to(Warp("FAKE_MAP_B:4/FAKE_MAP_A:0")))
        self.assertFalse(Warp("FAKE_MAP_A:0,4/FAKE_MAP_B:2").connects_to(Warp("FAKE_MAP_C:2/FAKE_MAP_A:0")))
