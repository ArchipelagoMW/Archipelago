from worlds.ys_chronicles.test.bases import YsChroniclesTestBase
from BaseClasses import CollectionState


class TestLocationRules(YsChroniclesTestBase):
    def test_dark_fact_requires_blue_amulet(self) -> None:
        self.multiworld.state = CollectionState(self.multiworld)
        # Get to Tower Upper
        self.collect_by_name([
            "Silver Sword", "Silver Shield", "Silver Armor",
            "Book of Ys (Hadal)", "Book of Ys (Tovah)", "Book of Ys (Dabbie)",
            "Darm Key", "Hammer", "Rod",
        ])
        self.assertFalse(self.can_reach_location("Boss: Dark Fact"))

        self.collect_by_name("Blue Amulet")
        self.assertTrue(self.can_reach_location("Boss: Dark Fact"))

    def test_locked_chests_require_treasure_box_key(self) -> None:
        self.multiworld.state = CollectionState(self.multiworld)
        self.assertFalse(self.can_reach_location("Minea Fields - Locked Chest"))

        self.collect_by_name("Treasure Box Key")
        self.assertTrue(self.can_reach_location("Minea Fields - Locked Chest"))

    def test_shrine_shield_ring_requires_treasure_box_key(self) -> None:
        self.multiworld.state = CollectionState(self.multiworld)
        self.collect_by_name(["Sara's Crystal", "Shrine Key"])
        self.assertFalse(self.can_reach_location("Shrine F1 - Shield Ring Chest"))

        self.collect_by_name("Treasure Box Key")
        self.assertTrue(self.can_reach_location("Shrine F1 - Shield Ring Chest"))

    def test_roda_tree_requires_seed_and_harmonica(self) -> None:
        self.multiworld.state = CollectionState(self.multiworld)
        self.assertFalse(self.can_reach_location("Southern Roda Tree"))

        self.collect_by_name("Roda Tree Seed")
        self.assertFalse(self.can_reach_location("Southern Roda Tree"))

        self.collect_by_name("Silver Harmonica")
        self.assertTrue(self.can_reach_location("Southern Roda Tree"))

    def test_silver_bell_reward(self) -> None:
        self.multiworld.state = CollectionState(self.multiworld)
        self.assertFalse(self.can_reach_location("Silver Bell Reward"))

        self.collect_by_name("Silver Bell")
        self.assertTrue(self.can_reach_location("Silver Bell Reward"))

    def test_raba_trade_requires_idol_and_mask(self) -> None:
        self.multiworld.state = CollectionState(self.multiworld)
        # Need to be in tower first
        self.collect_by_name([
            "Silver Sword", "Silver Shield", "Silver Armor",
            "Book of Ys (Hadal)", "Book of Ys (Tovah)", "Book of Ys (Dabbie)",
            "Darm Key",
        ])
        self.assertFalse(self.can_reach_location("Raba Trade"))

        self.collect_by_name(["Idol", "Mask of Eyes"])
        self.assertTrue(self.can_reach_location("Raba Trade"))

    def test_tower_battle_armor_requires_blue_necklace(self) -> None:
        self.multiworld.state = CollectionState(self.multiworld)
        # Need to reach Tower Upper
        self.collect_by_name([
            "Silver Sword", "Silver Shield", "Silver Armor",
            "Book of Ys (Hadal)", "Book of Ys (Tovah)", "Book of Ys (Dabbie)",
            "Darm Key", "Hammer", "Rod",
        ])
        self.assertFalse(self.can_reach_location("Tower F19 - Battle Armor Chest"))

        self.collect_by_name("Blue Necklace")
        self.assertTrue(self.can_reach_location("Tower F19 - Battle Armor Chest"))

    def test_reahs_gift_requires_evil_ring_and_necklace(self) -> None:
        self.multiworld.state = CollectionState(self.multiworld)
        # Reah is in Tower Mid — need tower access first
        self.collect_by_name([
            "Silver Sword", "Silver Shield", "Silver Armor",
            "Book of Ys (Hadal)", "Book of Ys (Tovah)", "Book of Ys (Dabbie)",
            "Darm Key",
        ])
        self.assertFalse(self.can_reach_location("Reah's Gift"))

        self.collect_by_name("Evil Ring")
        self.assertFalse(self.can_reach_location("Reah's Gift"))

        self.collect_by_name("Blue Necklace")
        self.assertTrue(self.can_reach_location("Reah's Gift"))

    def test_franz_gift_requires_book_hadal(self) -> None:
        self.multiworld.state = CollectionState(self.multiworld)
        self.assertFalse(self.can_reach_location("Franz's Gift"))

        self.collect_by_name("Book of Ys (Hadal)")
        self.assertTrue(self.can_reach_location("Franz's Gift"))
