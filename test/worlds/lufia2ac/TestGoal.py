from . import L2ACTestBase


class TestDefault(L2ACTestBase):
    options = {}

    def testEverything(self):
        self.collect_all_but(["Boss victory"])
        self.assertBeatable(True)

    def testNothing(self):
        self.assertBeatable(True)


class TestShuffleCapsuleMonsters(L2ACTestBase):
    options = {
        "shuffle_capsule_monsters": True,
    }

    def testEverything(self):
        self.collect_all_but(["Boss victory"])
        self.assertBeatable(True)

    def testBestParty(self):
        self.collect_by_name("DARBI")
        self.assertBeatable(True)

    def testNoDarbi(self):
        self.collect_all_but(["Boss victory", "DARBI"])
        self.assertBeatable(False)


class TestShufflePartyMembers(L2ACTestBase):
    options = {
        "shuffle_party_members": True,
    }

    def testEverything(self):
        self.collect_all_but(["Boss victory"])
        self.assertBeatable(True)

    def testBestParty(self):
        self.collect_by_name(["Dekar", "Guy", "Arty"])
        self.assertBeatable(True)

    def testNoDekar(self):
        self.collect_all_but(["Boss victory", "Dekar"])
        self.assertBeatable(False)

    def testNoGuy(self):
        self.collect_all_but(["Boss victory", "Guy"])
        self.assertBeatable(False)

    def testNoArty(self):
        self.collect_all_but(["Boss victory", "Arty"])
        self.assertBeatable(False)


class TestShuffleBoth(L2ACTestBase):
    options = {
        "shuffle_capsule_monsters": True,
        "shuffle_party_members": True,
    }

    def testEverything(self):
        self.collect_all_but(["Boss victory"])
        self.assertBeatable(True)

    def testBestParty(self):
        self.collect_by_name(["Dekar", "Guy", "Arty", "DARBI"])
        self.assertBeatable(True)

    def testNoDekar(self):
        self.collect_all_but(["Boss victory", "Dekar"])
        self.assertBeatable(False)

    def testNoGuy(self):
        self.collect_all_but(["Boss victory", "Guy"])
        self.assertBeatable(False)

    def testNoArty(self):
        self.collect_all_but(["Boss victory", "Arty"])
        self.assertBeatable(False)

    def testNoDarbi(self):
        self.collect_all_but(["Boss victory", "DARBI"])
        self.assertBeatable(False)
