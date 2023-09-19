from . import InscryptionTestBase


class GoalTestOrdered(InscryptionTestBase):
    options = {
        "goal": 0,
    }

    def test_beatable(self) -> None:
        for item_name in self.required_items_all_acts:
            item = self.get_item_by_name(item_name)
            self.assertBeatable(False)
            self.collect(item)
        self.assertBeatable(True)


class GoalTestUnordered(InscryptionTestBase):
    options = {
        "goal": 1,
    }

    def test_beatable(self) -> None:
        for item_name in self.required_items_all_acts:
            item = self.get_item_by_name(item_name)
            self.assertBeatable(False)
            self.collect(item)
        self.assertBeatable(True)


class GoalTestAct1(InscryptionTestBase):
    options = {
        "goal": 2,
    }

    def test_beatable(self) -> None:
        self.assertBeatable(False)
        film_roll = self.get_item_by_name("Film Roll")
        self.collect(film_roll)
        self.assertBeatable(True)
