from worlds.ys_chronicles.test.bases import YsChroniclesTestBase
from BaseClasses import CollectionState


class TestRegionAccess(YsChroniclesTestBase):
    def test_towns_freely_accessible(self) -> None:
        self.multiworld.state = CollectionState(self.multiworld)
        for region in ["Minea", "Barbado", "Zepik", "Minea Fields"]:
            self.assertTrue(
                self.can_reach_region(region),
                f"{region} should be reachable from the start",
            )

    def test_shrine_requires_crystal_and_key(self) -> None:
        self.multiworld.state = CollectionState(self.multiworld)
        self.assertFalse(self.can_reach_region("Shrine"))

        self.collect_by_name("Sara's Crystal")
        self.assertFalse(self.can_reach_region("Shrine"))

        self.collect_by_name("Shrine Key")
        self.assertTrue(self.can_reach_region("Shrine"))

    def test_shrine_b3_requires_ivory_and_marble(self) -> None:
        self.multiworld.state = CollectionState(self.multiworld)
        self.collect_by_name(["Sara's Crystal", "Shrine Key"])
        self.assertTrue(self.can_reach_region("Shrine B2"))
        self.assertFalse(self.can_reach_region("Shrine B3"))

        self.collect_by_name("Ivory Key")
        self.assertFalse(self.can_reach_region("Shrine B3"))

        self.collect_by_name("Marble Key")
        self.assertTrue(self.can_reach_region("Shrine B3"))

    def test_mine_freely_accessible(self) -> None:
        self.multiworld.state = CollectionState(self.multiworld)
        for region in ["Mine F1", "Mine B1", "Mine B2"]:
            self.assertTrue(
                self.can_reach_region(region),
                f"{region} should be reachable from the start",
            )

    def test_tower_requires_full_silver_set_and_books(self) -> None:
        self.multiworld.state = CollectionState(self.multiworld)
        self.assertFalse(self.can_reach_region("Tower Lower"))

        # Give silver equipment but not books or key
        self.collect_by_name(["Silver Sword", "Silver Shield", "Silver Armor"])
        self.assertFalse(self.can_reach_region("Tower Lower"))

        # Add books
        self.collect_by_name([
            "Book of Ys (Hadal)", "Book of Ys (Tovah)", "Book of Ys (Dabbie)",
        ])
        self.assertFalse(self.can_reach_region("Tower Lower"))

        # Add Darm Key — now should work
        self.collect_by_name("Darm Key")
        self.assertTrue(self.can_reach_region("Tower Lower"))

    def test_tower_mid_requires_hammer(self) -> None:
        self.multiworld.state = CollectionState(self.multiworld)
        # Get into the tower
        self.collect_by_name([
            "Silver Sword", "Silver Shield", "Silver Armor",
            "Book of Ys (Hadal)", "Book of Ys (Tovah)", "Book of Ys (Dabbie)",
            "Darm Key",
        ])
        self.assertTrue(self.can_reach_region("Tower F8"))
        self.assertFalse(self.can_reach_region("Tower F14"))

        self.collect_by_name("Hammer")
        self.assertTrue(self.can_reach_region("Tower F14"))

    def test_tower_upper_requires_rod(self) -> None:
        self.multiworld.state = CollectionState(self.multiworld)
        self.collect_by_name([
            "Silver Sword", "Silver Shield", "Silver Armor",
            "Book of Ys (Hadal)", "Book of Ys (Tovah)", "Book of Ys (Dabbie)",
            "Darm Key", "Hammer",
        ])
        self.assertTrue(self.can_reach_region("Tower F14"))
        self.assertFalse(self.can_reach_region("Tower Upper"))

        self.collect_by_name("Rod")
        self.assertTrue(self.can_reach_region("Tower Upper"))

    def test_tower_blocked_without_each_silver_piece(self) -> None:
        """Each silver equipment piece is individually required for tower."""
        base_items = [
            "Book of Ys (Hadal)", "Book of Ys (Tovah)", "Book of Ys (Dabbie)",
            "Darm Key",
        ]
        silver = ["Silver Sword", "Silver Shield", "Silver Armor"]
        for missing in silver:
            self.multiworld.state = CollectionState(self.multiworld)
            have = [s for s in silver if s != missing] + base_items
            self.collect_by_name(have)
            self.assertFalse(
                self.can_reach_region("Tower Lower"),
                f"Tower should be blocked without {missing}",
            )

    def test_thieves_den_freely_accessible(self) -> None:
        self.multiworld.state = CollectionState(self.multiworld)
        self.assertTrue(self.can_reach_region("Thieve's Den"))
