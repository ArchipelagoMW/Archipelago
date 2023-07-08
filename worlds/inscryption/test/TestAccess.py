from . import InscryptionTestBase


class AccessTest(InscryptionTestBase):

    def testDagger(self) -> None:
        self.assertAccessDependency(["Act 1 - Magnificus Eye"], [["Dagger"]])

    def testCagedWolf(self) -> None:
        self.assertAccessDependency(["Act 1 - Dagger"], [["Caged Wolf Card"]])

    def testMagnificusEye(self) -> None:
        self.assertAccessDependency(["Act 1 - Clock Main Compartment"], [["Magnificus Eye"]])

    def testWardrobeKey(self) -> None:
        self.assertAccessDependency(
            ["Act 1 - Wardrobe Drawer 1", "Act 1 - Wardrobe Drawer 2",
             "Act 1 - Wardrobe Drawer 3", "Act 1 - Wardrobe Drawer 4"],
            [["Wardrobe Key"]]
        )

    def testBridgeRequirement(self) -> None:
        self.assertAccessDependency(
            ["Act 2 - Battle Pike Mage", "Act 2 - Battle Goobert", "Act 2 - Battle Lonely Wizard",
             "Act 2 - Battle Inspector", "Act 2 - Battle Melter", "Act 2 - Battle Dredger",
             "Act 2 - Tower Chest 1", "Act 2 - Tower Chest 2", "Act 2 - Tower Chest 3",
             "Act 2 - Tower Bath", "Act 2 - Factory Trash Can", "Act 2 - Factory Drawer 1",
             "Act 2 - Factory Drawer 2", "Act 2 - Factory Chest 1", "Act 2 - Factory Chest 2",
             "Act 2 - Factory Chest 3", "Act 2 - Factory Chest 4", "Act 2 - Monocle"],
            [["Epitaph Piece 1", "Epitaph Piece 2", "Epitaph Piece 3", "Epitaph Piece 4",
              "Epitaph Piece 5", "Epitaph Piece 6", "Epitaph Piece 7", "Epitaph Piece 8",
              "Epitaph Piece 9", "Camera Replica", "Pile Of Meat"]]
        )


