from . import InscryptionTestBase


class AccessTestGeneral(InscryptionTestBase):

    def test_dagger(self) -> None:
        self.assertAccessDependency(["Act 1 - Magnificus Eye"], [["Dagger"]])

    def test_caged_wolf(self) -> None:
        self.assertAccessDependency(["Act 1 - Dagger"], [["Caged Wolf Card"]])

    def test_magnificus_eye(self) -> None:
        self.assertAccessDependency(["Act 1 - Clock Main Compartment"], [["Magnificus Eye"]])

    def test_wardrobe_key(self) -> None:
        self.assertAccessDependency(
            ["Act 1 - Wardrobe Drawer 1", "Act 1 - Wardrobe Drawer 2",
             "Act 1 - Wardrobe Drawer 3", "Act 1 - Wardrobe Drawer 4"],
            [["Wardrobe Key"]]
        )

    def test_ancient_obol(self) -> None:
        self.assertAccessDependency(
            ["Act 2 - Bone Lord Femur", "Act 2 - Bone Lord Horn", "Act 2 - Bone Lord Holo Key"],
            [["Ancient Obol"]]
        )

    def test_holo_pelt(self) -> None:
        self.assertAccessDependency(
            ["Act 3 - Trader 1", "Act 3 - Trader 2", "Act 3 - Trader 3", "Act 3 - Trader 4", "Act 3 - Trader 5"],
            [["Holo Pelt"]]
        )

    def test_inspectometer_battery(self) -> None:
        self.assertAccessDependency(
            ["Act 3 - Boss Photographer", "Act 3 - Boss Archivist", "Act 3 - Boss Unfinished", "Act 3 - Boss G0lly",
             "Act 3 - Trader 1", "Act 3 - Trader 2", "Act 3 - Trader 3", "Act 3 - Trader 4", "Act 3 - Trader 5",
             "Act 3 - Shop Holo Pelt", "Act 3 - Middle Holo Pelt", "Act 3 - Forest Holo Pelt", "Act 3 - Clock",
             "Act 3 - Crypt Holo Pelt", "Act 3 - Gems Drone", "Act 3 - Nano Armor Generator", "Act 3 - Extra Battery",
             "Act 3 - Tower Holo Pelt", "Act 3 - The Great Transcendence", "Act 3 - Boss Mycologists",
             "Act 3 - Bone Lord Room", "Act 3 - Well", "Act 3 - Luke's File Entry 1", "Act 3 - Luke's File Entry 2",
             "Act 3 - Luke's File Entry 3", "Act 3 - Luke's File Entry 4", "Act 3 - Goobert's Painting"],
            [["Inspectometer Battery"]]
        )

    def test_gem_drone(self) -> None:
        self.assertAccessDependency(
            ["Act 3 - Boss Unfinished", "Act 3 - Boss G0lly", "Act 3 - Trader 1", "Act 3 - Trader 2",
             "Act 3 - Trader 3", "Act 3 - Trader 4", "Act 3 - Trader 5", "Act 3 - Shop Holo Pelt", "Act 3 - Clock",
             "Act 3 - Tower Holo Pelt", "Act 3 - The Great Transcendence", "Act 3 - Luke's File Entry 4",
             "Act 3 - Boss Mycologists", "Act 3 - Nano Armor Generator", "Act 3 - Goobert's Painting"],
            [["Gems Module"]]
        )

    def test_mycologists_holo_key(self) -> None:
        self.assertAccessDependency(
            ["Act 3 - Boss Mycologists"],
            [["Mycologists Holo Key"]]
        )

    def test_bone_lord_holo_key(self) -> None:
        self.assertAccessDependency(
            ["Act 3 - Bone Lord Room"],
            [["Bone Lord Holo Key"]]
        )

    def test_quill(self) -> None:
        self.assertAccessDependency(
            ["Act 3 - Boss Archivist", "Act 3 - Luke's File Entry 1", "Act 3 - Luke's File Entry 2",
             "Act 3 - Luke's File Entry 3", "Act 3 - Luke's File Entry 4", "Act 3 - The Great Transcendence",
             "Act 3 - Boss Mycologists"],
            [["Quill"]]
        )


class AccessTestOrdered(InscryptionTestBase):
    options = {
        "goal": 0,
    }

    def test_film_roll(self) -> None:
        self.assertAccessDependency(
            ["Act 2 - Battle Prospector", "Act 2 - Battle Angler", "Act 2 - Battle Trapper", "Act 2 - Battle Sawyer",
             "Act 2 - Battle Royal", "Act 2 - Battle Kaycee", "Act 2 - Battle Pike Mage", "Act 2 - Battle Goobert",
             "Act 2 - Battle Lonely Wizard", "Act 2 - Battle Inspector", "Act 2 - Battle Melter",
             "Act 2 - Battle Dredger", "Act 2 - Tower Chest 1", "Act 2 - Tower Chest 2", "Act 2 - Tower Chest 3",
             "Act 2 - Forest Meadow Chest", "Act 2 - Forest Cabin Chest", "Act 2 - Cabin Wardrobe Drawer",
             "Act 2 - Cabin Safe", "Act 2 - Crypt Casket 1", "Act 2 - Crypt Casket 2", "Act 2 - Crypt Well",
             "Act 2 - Camera Replica", "Act 2 - Clover", "Act 2 - Epitaph Piece 1", "Act 2 - Epitaph Piece 2",
             "Act 2 - Epitaph Piece 3", "Act 2 - Epitaph Piece 4", "Act 2 - Epitaph Piece 5", "Act 2 - Epitaph Piece 6",
             "Act 2 - Epitaph Piece 7", "Act 2 - Epitaph Piece 8", "Act 2 - Epitaph Piece 9", "Act 2 - Dock Chest",
             "Act 2 - Tentacle", "Act 2 - Factory Trash Can", "Act 2 - Factory Drawer 1",
             "Act 2 - Ancient Obol", "Act 2 - Factory Drawer 2", "Act 2 - Factory Chest 1", "Act 2 - Factory Chest 2",
             "Act 2 - Factory Chest 3", "Act 2 - Factory Chest 4", "Act 2 - Monocle", "Act 2 - Boss Leshy",
             "Act 2 - Boss Grimora", "Act 2 - Boss Magnificus", "Act 2 - Boss P03", "Act 2 - Mycologists Holo Key",
             "Act 2 - Bone Lord Femur", "Act 2 - Bone Lord Horn", "Act 2 - Bone Lord Holo Key",
             "Act 3 - Boss Photographer", "Act 3 - Boss Archivist", "Act 3 - Boss Unfinished", "Act 3 - Boss G0lly",
             "Act 3 - Boss Mycologists", "Act 3 - Bone Lord Room", "Act 3 - Shop Holo Pelt", "Act 3 - Middle Holo Pelt",
             "Act 3 - Forest Holo Pelt", "Act 3 - Crypt Holo Pelt", "Act 3 - Tower Holo Pelt", "Act 3 - Trader 1",
             "Act 3 - Trader 2", "Act 3 - Trader 3", "Act 3 - Trader 4", "Act 3 - Trader 5", "Act 3 - Drawer 1",
             "Act 3 - Drawer 2", "Act 3 - Clock", "Act 3 - Extra Battery", "Act 3 - Nano Armor Generator",
             "Act 3 - Chest", "Act 3 - Goobert's Painting", "Act 3 - Luke's File Entry 1", "Act 3 - Gems Drone",
             "Act 3 - Luke's File Entry 2", "Act 3 - Luke's File Entry 3", "Act 3 - Luke's File Entry 4",
             "Act 3 - Inspectometer Battery", "Act 3 - Gems Drone", "Act 3 - The Great Transcendence", "Act 3 - Well"],
            [["Film Roll"]]
        )

    def test_epitaphs_and_forest_items(self) -> None:
        self.assertAccessDependency(
            ["Act 2 - Battle Prospector", "Act 2 - Battle Angler", "Act 2 - Battle Trapper",
             "Act 2 - Battle Pike Mage", "Act 2 - Battle Goobert", "Act 2 - Battle Lonely Wizard",
             "Act 2 - Battle Inspector", "Act 2 - Battle Melter", "Act 2 - Battle Dredger",
             "Act 2 - Tower Chest 1", "Act 2 - Tower Chest 2", "Act 2 - Tower Chest 3", "Act 2 - Forest Meadow Chest",
             "Act 2 - Tentacle", "Act 2 - Factory Trash Can", "Act 2 - Factory Drawer 1", "Act 2 - Ancient Obol",
             "Act 2 - Factory Drawer 2", "Act 2 - Factory Chest 1", "Act 2 - Factory Chest 2",
             "Act 2 - Factory Chest 3", "Act 2 - Factory Chest 4", "Act 2 - Monocle", "Act 2 - Boss Leshy",
             "Act 2 - Boss Grimora", "Act 2 - Boss Magnificus", "Act 2 - Boss P03", "Act 2 - Mycologists Holo Key",
             "Act 3 - Boss Photographer", "Act 3 - Boss Archivist", "Act 3 - Boss Unfinished", "Act 3 - Boss G0lly",
             "Act 3 - Boss Mycologists", "Act 3 - Bone Lord Room", "Act 3 - Shop Holo Pelt", "Act 3 - Middle Holo Pelt",
             "Act 3 - Forest Holo Pelt", "Act 3 - Crypt Holo Pelt", "Act 3 - Tower Holo Pelt", "Act 3 - Trader 1",
             "Act 3 - Trader 2", "Act 3 - Trader 3", "Act 3 - Trader 4", "Act 3 - Trader 5", "Act 3 - Drawer 1",
             "Act 3 - Drawer 2", "Act 3 - Clock", "Act 3 - Extra Battery", "Act 3 - Nano Armor Generator",
             "Act 3 - Chest", "Act 3 - Goobert's Painting", "Act 3 - Luke's File Entry 1", "Act 3 - Gems Drone",
             "Act 3 - Luke's File Entry 2", "Act 3 - Luke's File Entry 3", "Act 3 - Luke's File Entry 4",
             "Act 3 - Inspectometer Battery", "Act 3 - Gems Drone", "Act 3 - The Great Transcendence", "Act 3 - Well"],
            [["Epitaph Piece", "Camera Replica", "Pile Of Meat"]]
        )

    def test_epitaphs(self) -> None:
        self.assertAccessDependency(
            ["Act 2 - Boss Grimora",
             "Act 3 - Boss Photographer", "Act 3 - Boss Archivist", "Act 3 - Boss Unfinished", "Act 3 - Boss G0lly",
             "Act 3 - Boss Mycologists", "Act 3 - Bone Lord Room", "Act 3 - Shop Holo Pelt", "Act 3 - Middle Holo Pelt",
             "Act 3 - Forest Holo Pelt", "Act 3 - Crypt Holo Pelt", "Act 3 - Tower Holo Pelt", "Act 3 - Trader 1",
             "Act 3 - Trader 2", "Act 3 - Trader 3", "Act 3 - Trader 4", "Act 3 - Trader 5", "Act 3 - Drawer 1",
             "Act 3 - Drawer 2", "Act 3 - Clock", "Act 3 - Extra Battery", "Act 3 - Nano Armor Generator",
             "Act 3 - Chest", "Act 3 - Goobert's Painting", "Act 3 - Luke's File Entry 1", "Act 3 - Gems Drone",
             "Act 3 - Luke's File Entry 2", "Act 3 - Luke's File Entry 3", "Act 3 - Luke's File Entry 4",
             "Act 3 - Inspectometer Battery", "Act 3 - Gems Drone", "Act 3 - The Great Transcendence", "Act 3 - Well"],
            [["Epitaph Piece"]]
        )

    def test_forest_items(self) -> None:
        self.assertAccessDependency(
            ["Act 2 - Battle Prospector", "Act 2 - Battle Angler", "Act 2 - Battle Trapper",
             "Act 2 - Boss Leshy", "Act 2 - Forest Meadow Chest",
             "Act 3 - Boss Photographer", "Act 3 - Boss Archivist", "Act 3 - Boss Unfinished", "Act 3 - Boss G0lly",
             "Act 3 - Boss Mycologists", "Act 3 - Bone Lord Room", "Act 3 - Shop Holo Pelt", "Act 3 - Middle Holo Pelt",
             "Act 3 - Forest Holo Pelt", "Act 3 - Crypt Holo Pelt", "Act 3 - Tower Holo Pelt", "Act 3 - Trader 1",
             "Act 3 - Trader 2", "Act 3 - Trader 3", "Act 3 - Trader 4", "Act 3 - Trader 5", "Act 3 - Drawer 1",
             "Act 3 - Drawer 2", "Act 3 - Clock", "Act 3 - Extra Battery", "Act 3 - Nano Armor Generator",
             "Act 3 - Chest", "Act 3 - Goobert's Painting", "Act 3 - Luke's File Entry 1", "Act 3 - Gems Drone",
             "Act 3 - Luke's File Entry 2", "Act 3 - Luke's File Entry 3", "Act 3 - Luke's File Entry 4",
             "Act 3 - Inspectometer Battery", "Act 3 - Gems Drone", "Act 3 - The Great Transcendence", "Act 3 - Well"],
            [["Camera Replica", "Pile Of Meat"]]
        )

    def test_monocle(self) -> None:
        self.assertAccessDependency(
            ["Act 2 - Battle Goobert", "Act 2 - Battle Pike Mage", "Act 2 - Battle Lonely Wizard",
             "Act 2 - Boss Magnificus", "Act 2 - Tower Chest 2", "Act 2 - Tower Chest 3",
             "Act 2 - Tentacle", "Act 2 - Ancient Obol", "Act 2 - Mycologists Holo Key",
             "Act 3 - Boss Photographer", "Act 3 - Boss Archivist", "Act 3 - Boss Unfinished", "Act 3 - Boss G0lly",
             "Act 3 - Boss Mycologists", "Act 3 - Bone Lord Room", "Act 3 - Shop Holo Pelt", "Act 3 - Middle Holo Pelt",
             "Act 3 - Forest Holo Pelt", "Act 3 - Crypt Holo Pelt", "Act 3 - Tower Holo Pelt", "Act 3 - Trader 1",
             "Act 3 - Trader 2", "Act 3 - Trader 3", "Act 3 - Trader 4", "Act 3 - Trader 5", "Act 3 - Drawer 1",
             "Act 3 - Drawer 2", "Act 3 - Clock", "Act 3 - Extra Battery", "Act 3 - Nano Armor Generator",
             "Act 3 - Chest", "Act 3 - Goobert's Painting", "Act 3 - Luke's File Entry 1", "Act 3 - Gems Drone",
             "Act 3 - Luke's File Entry 2", "Act 3 - Luke's File Entry 3", "Act 3 - Luke's File Entry 4",
             "Act 3 - Inspectometer Battery", "Act 3 - Gems Drone", "Act 3 - The Great Transcendence", "Act 3 - Well"],
            [["Monocle"]]
        )


class AccessTestUnordered(InscryptionTestBase):
    options = {
        "goal": 1,
    }

    def test_epitaphs_and_forest_items(self) -> None:
        self.assertAccessDependency(
            ["Act 2 - Battle Prospector", "Act 2 - Battle Angler", "Act 2 - Battle Trapper",
             "Act 2 - Battle Pike Mage", "Act 2 - Battle Goobert", "Act 2 - Battle Lonely Wizard",
             "Act 2 - Battle Inspector", "Act 2 - Battle Melter", "Act 2 - Battle Dredger",
             "Act 2 - Tower Chest 1", "Act 2 - Tower Chest 2", "Act 2 - Tower Chest 3", "Act 2 - Forest Meadow Chest",
             "Act 2 - Tentacle", "Act 2 - Factory Trash Can", "Act 2 - Factory Drawer 1", "Act 2 - Ancient Obol",
             "Act 2 - Factory Drawer 2", "Act 2 - Factory Chest 1", "Act 2 - Factory Chest 2",
             "Act 2 - Factory Chest 3", "Act 2 - Factory Chest 4", "Act 2 - Monocle", "Act 2 - Boss Leshy",
             "Act 2 - Boss Grimora", "Act 2 - Boss Magnificus", "Act 2 - Boss P03", "Act 2 - Mycologists Holo Key"],
            [["Epitaph Piece", "Camera Replica", "Pile Of Meat"]]
        )

    def test_epitaphs(self) -> None:
        self.assertAccessDependency(
            ["Act 2 - Boss Grimora"],
            [["Epitaph Piece"]]
        )

    def test_forest_items(self) -> None:
        self.assertAccessDependency(
            ["Act 2 - Battle Prospector", "Act 2 - Battle Angler", "Act 2 - Battle Trapper",
             "Act 2 - Boss Leshy", "Act 2 - Forest Meadow Chest"],
            [["Camera Replica", "Pile Of Meat"]]
        )

    def test_monocle(self) -> None:
        self.assertAccessDependency(
            ["Act 2 - Battle Goobert", "Act 2 - Battle Pike Mage", "Act 2 - Battle Lonely Wizard",
             "Act 2 - Boss Magnificus", "Act 2 - Tower Chest 2", "Act 2 - Tower Chest 3",
             "Act 2 - Tentacle", "Act 2 - Ancient Obol", "Act 2 - Mycologists Holo Key"],
            [["Monocle"]]
        )

class AccessTestBalancedPaintings(InscryptionTestBase):
    options = {
        "painting_checks_balancing": 1,
    }

    def test_paintings(self) -> None:
        self.assertAccessDependency(["Act 1 - Painting 2", "Act 1 - Painting 3"],
                                    [["Oil Painting's Clover Plant", "Squirrel Totem Head"]])
