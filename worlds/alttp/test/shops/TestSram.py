from ...Shops import shop_table
from ..bases import TestBase


class TestSram(TestBase):
    def testUniqueOffset(self):
        sram_ids = set()
        for shop_name, shopdata in shop_table.items():
            for x in range(3):
                new = shopdata.sram_offset + x
                with self.subTest(shop_name, slot=x + 1, offset=new):
                    self.assertNotIn(new, sram_ids)
                sram_ids.add(new)
