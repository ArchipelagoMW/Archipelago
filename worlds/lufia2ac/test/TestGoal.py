from . import L2ACTestBase


class TestDefault(L2ACTestBase):

    def test_everything(self) -> None:
        self.collect_all_but(["Ancient key"])
        self.assertBeatable(True)

    def test_nothing(self) -> None:
        self.assertBeatable(True)


class TestShuffleCapsuleMonsters(L2ACTestBase):
    options = {
        "shuffle_capsule_monsters": True,
    }

    def test_everything(self) -> None:
        self.collect_all_but(["Ancient key"])
        self.assertBeatable(True)

    def test_best_party(self) -> None:
        self.collect_by_name("DARBI")
        self.assertBeatable(True)

    def test_no_darbi(self) -> None:
        self.collect_all_but(["Ancient key", "DARBI"])
        self.assertBeatable(False)


class TestShufflePartyMembers(L2ACTestBase):
    options = {
        "shuffle_party_members": True,
    }

    def test_everything(self) -> None:
        self.collect_all_but(["Ancient key"])
        self.assertBeatable(True)

    def test_best_party(self) -> None:
        self.collect_by_name(["Dekar", "Guy", "Arty"])
        self.assertBeatable(True)

    def test_no_dekar(self) -> None:
        self.collect_all_but(["Ancient key", "Dekar"])
        self.assertBeatable(False)

    def test_no_guy(self) -> None:
        self.collect_all_but(["Ancient key", "Guy"])
        self.assertBeatable(False)

    def test_no_arty(self) -> None:
        self.collect_all_but(["Ancient key", "Arty"])
        self.assertBeatable(False)


class TestShuffleBoth(L2ACTestBase):
    options = {
        "shuffle_capsule_monsters": True,
        "shuffle_party_members": True,
    }

    def test_everything(self) -> None:
        self.collect_all_but(["Ancient key"])
        self.assertBeatable(True)

    def test_best_party(self) -> None:
        self.collect_by_name(["Dekar", "Guy", "Arty", "DARBI"])
        self.assertBeatable(True)

    def test_no_dekar(self) -> None:
        self.collect_all_but(["Ancient key", "Dekar"])
        self.assertBeatable(False)

    def test_no_guy(self) -> None:
        self.collect_all_but(["Ancient key", "Guy"])
        self.assertBeatable(False)

    def test_no_arty(self) -> None:
        self.collect_all_but(["Ancient key", "Arty"])
        self.assertBeatable(False)

    def test_no_darbi(self) -> None:
        self.collect_all_but(["Ancient key", "DARBI"])
        self.assertBeatable(False)
