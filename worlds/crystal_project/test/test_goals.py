from .bases import CrystalProjectTestBase
from ..options import *
from ..constants.key_items import *
from ..constants.keys import *
from ..constants.mounts import *
from ..constants.ap_regions import *
from BaseClasses import CollectionState


class TestTrueAstleyBeginner(CrystalProjectTestBase):
    options = {
        "goal": Goal.option_true_astley,
        "included_regions": IncludedRegions.option_beginner,

    }

    def test_completability(self):
        self.collect_all_but("")
        self.assertBeatable(True)