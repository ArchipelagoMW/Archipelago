import unittest
from worlds import subnautica


class SubnauticaTest(unittest.TestCase):
    # This is an assumption in the mod side
    scancutoff: int = 33999

    def testIDRange(self):
        for name, id in subnautica.SubnauticaWorld.location_name_to_id.items():
            with self.subTest(item=name):
                if "Scan" in name:
                    self.assertLess(self.scancutoff, id)
                else:
                    self.assertGreater(self.scancutoff, id)
