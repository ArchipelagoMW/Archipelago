from . import InscryptionTestBase


class GoalTestOrdered(InscryptionTestBase):
    options = {
        "goal": 0,
    }

    def test_beatable(self) -> None:
        for item_name in self.required_items_all_acts:
            item = self.get_item_by_name(item_name)
            self.collect(item)
        for i in range(9):
            item = self.get_item_by_name("Epitaph Piece")
            self.collect(item)
        self.assertBeatable(True)
        for item_name in self.required_items_all_acts:
            item = self.get_item_by_name(item_name)
            self.remove(item)
            self.assertBeatable(False)
            self.collect(item)
        item = self.get_item_by_name("Epitaph Piece")
        self.remove(item)
        self.assertBeatable(False)
        self.collect(item)


class GoalTestUnordered(InscryptionTestBase):
    options = {
        "goal": 1,
    }

    def test_beatable(self) -> None:
        for item_name in self.required_items_all_acts:
            item = self.get_item_by_name(item_name)
            self.collect(item)
        for i in range(9):
            item = self.get_item_by_name("Epitaph Piece")
            self.collect(item)
        self.assertBeatable(True)
        for item_name in self.required_items_all_acts:
            item = self.get_item_by_name(item_name)
            self.remove(item)
            self.assertBeatable(False)
            self.collect(item)
        item = self.get_item_by_name("Epitaph Piece")
        self.remove(item)
        self.assertBeatable(False)
        self.collect(item)


class GoalTestAct1(InscryptionTestBase):
    options = {
        "goal": 2,
    }

    def test_beatable(self) -> None:
        self.assertBeatable(False)
        film_roll = self.get_item_by_name("Film Roll")
        self.collect(film_roll)
        self.assertBeatable(True)


class GoalTestGroupedEpitaphs(InscryptionTestBase):
    options = {
        "epitaph_pieces_randomization": 1,
    }

    def test_beatable(self) -> None:
        for item_name in self.required_items_all_acts:
            item = self.get_item_by_name(item_name)
            self.collect(item)
        for i in range(3):
            item = self.get_item_by_name("Epitaph Pieces")
            self.collect(item)
        self.assertBeatable(True)
        for item_name in self.required_items_all_acts:
            item = self.get_item_by_name(item_name)
            self.remove(item)
            self.assertBeatable(False)
            self.collect(item)
        item = self.get_item_by_name("Epitaph Pieces")
        self.remove(item)
        self.assertBeatable(False)
        self.collect(item)


class GoalTestEpitaphsAsOne(InscryptionTestBase):
    options = {
        "epitaph_pieces_randomization": 2,
    }

    def test_beatable(self) -> None:
        for item_name in self.required_items_all_acts:
            item = self.get_item_by_name(item_name)
            self.collect(item)
        item = self.get_item_by_name("Epitaph Pieces")
        self.collect(item)
        self.assertBeatable(True)
        for item_name in self.required_items_all_acts:
            item = self.get_item_by_name(item_name)
            self.remove(item)
            self.assertBeatable(False)
            self.collect(item)
        item = self.get_item_by_name("Epitaph Pieces")
        self.remove(item)
        self.assertBeatable(False)
        self.collect(item)
