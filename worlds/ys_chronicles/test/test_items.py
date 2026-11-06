from worlds.ys_chronicles.test.bases import YsChroniclesTestBase
from BaseClasses import ItemClassification


class TestItemClassification(YsChroniclesTestBase):
    def test_keys_are_progression(self) -> None:
        keys = [
            "Treasure Box Key", "Prison Key", "Shrine Key",
            "Ivory Key", "Marble Key", "Darm Key",
        ]
        for name in keys:
            item = self.world.create_item(name)
            self.assertTrue(item.advancement, f"{name} should be progression")

    def test_books_are_progression(self) -> None:
        books = [
            "Book of Ys (Hadal)", "Book of Ys (Tovah)", "Book of Ys (Dabbie)",
            "Book of Ys (Mesa)", "Book of Ys (Gemma)", "Book of Ys (Fact)",
        ]
        for name in books:
            item = self.world.create_item(name)
            self.assertTrue(item.advancement, f"{name} should be progression")

    def test_quest_items_are_progression(self) -> None:
        quest = [
            "Sara's Crystal", "Roda Tree Seed", "Silver Bell",
            "Silver Harmonica", "Idol", "Rod", "Monocle",
            "Blue Amulet", "Mask of Eyes", "Blue Necklace", "Hammer",
        ]
        for name in quest:
            item = self.world.create_item(name)
            self.assertTrue(item.advancement, f"{name} should be progression")

    def test_silver_equipment_is_progression(self) -> None:
        silver = ["Silver Sword", "Silver Shield", "Silver Armor"]
        for name in silver:
            item = self.world.create_item(name)
            self.assertTrue(item.advancement, f"{name} should be progression")

    def test_filler_items(self) -> None:
        filler = ["Heal Potion", "Bestiary Potion", "Piece of Paper"]
        for name in filler:
            item = self.world.create_item(name)
            self.assertEqual(
                item.classification, ItemClassification.filler,
                f"{name} should be filler",
            )

    def test_useful_items(self) -> None:
        useful = [
            "Short Sword", "Long Sword", "Talwar",
            "Small Shield", "Middle Shield", "Large Shield",
            "Chain Mail", "Plate Mail", "Reflex",
            "Power Ring", "Shield Ring", "Timer Ring", "Heal Ring",
            "Wing", "Mirror", "Ruby", "Golden Vase", "Necklace",
        ]
        for name in useful:
            item = self.world.create_item(name)
            self.assertEqual(
                item.classification, ItemClassification.useful,
                f"{name} should be useful",
            )

    def test_evil_ring_is_progression(self) -> None:
        item = self.world.create_item("Evil Ring")
        self.assertTrue(item.advancement, "Evil Ring should be progression (needed for Reah)")

    def test_battle_equipment_is_progression(self) -> None:
        for name in ["Battle Shield", "Battle Armor", "Flame Sword"]:
            item = self.world.create_item(name)
            self.assertTrue(item.advancement, f"{name} should be progression")

    def test_no_duplicate_item_codes(self) -> None:
        from worlds.ys_chronicles.items import YS1_ITEMS
        codes = [d.code for d in YS1_ITEMS.values()]
        self.assertEqual(len(codes), len(set(codes)), "Duplicate AP item codes found")

    def test_no_duplicate_game_ids(self) -> None:
        from worlds.ys_chronicles.items import YS1_ITEMS
        game_ids = [d.game_id for d in YS1_ITEMS.values()]
        self.assertEqual(len(game_ids), len(set(game_ids)), "Duplicate game IDs found")
