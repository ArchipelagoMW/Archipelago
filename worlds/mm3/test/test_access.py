from .bases import MM3TestBase

class TestAccess(MM3TestBase):
    options = {
        "consumables": "all"
    }

    def test_wily3_hard_knuckle(self):
        locations = ["Wily Stage 3 - Weapon Energy 1", "Wily Stage 3 - Weapon Energy 2",
                     "Wily Stage 3 - Mystery Tank 1", "Wily Stage 3 - Mystery Tank 2"]
        items = [["Hard Knuckle"]]
        self.assertAccessDependency(locations, items, True)