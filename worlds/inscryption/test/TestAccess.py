from . import InscryptionTestBase
from ..Rules import inscryption_rules


class AccessTest(InscryptionTestBase):

    def testDagger(self) -> None:
        self.assertAccessDependency(["Magnificus Eye"], [["Dagger"]])

    def testCagedWolf(self) -> None:
        self.assertAccessDependency(["Dagger"], [["Caged Wolf Card"]])

    def testMagnificusEye(self) -> None:
        self.assertAccessDependency(["Cabin Clock Main Compartment"], [["Magnificus Eye"]])

    def testWardrobeKey(self) -> None:
        self.assertAccessDependency(
            ["Wardrobe Drawer 1", "Wardrobe Drawer 2", "Wardrobe Drawer 3", "Wardrobe Drawer 4"],
            [["Wardrobe Key"]]
        )
