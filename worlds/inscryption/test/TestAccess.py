from . import InscryptionTestBase


class AccessTest(InscryptionTestBase):

    def testDagger(self) -> None:
        self.assertAccessDependency(["Act 1 Magnificus Eye"], [["Dagger"]])

    def testCagedWolf(self) -> None:
        self.assertAccessDependency(["Act 1 Dagger"], [["Caged Wolf Card"]])

    def testMagnificusEye(self) -> None:
        self.assertAccessDependency(["Act 1 Clock Main Compartment"], [["Magnificus Eye"]])

    def testWardrobeKey(self) -> None:
        self.assertAccessDependency(
            ["Act 1 Wardrobe Drawer 1", "Act 1 Wardrobe Drawer 2",
             "Act 1 Wardrobe Drawer 3", "Act 1 Wardrobe Drawer 4"],
            [["Wardrobe Key"]]
        )
