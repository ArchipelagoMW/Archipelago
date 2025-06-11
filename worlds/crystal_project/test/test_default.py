from .bases import CrystalProjectTestBase
from ..constants.key_items import *
from ..constants.keys import *
from ..constants.mounts import *
from ..constants.regions import *


class TestDefault(CrystalProjectTestBase):
    run_default_tests = True

    def test_region_accessibility(self):
        self.assertBeatable(False)
        self.collect_all_but("")
        self.assertBeatable(True)