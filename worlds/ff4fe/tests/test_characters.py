from . import FF4FETestBase
from . import option_presets
from .. import locations
from .. import items


class TestCharacters(FF4FETestBase):
    options = option_presets.default_options

    def test_character_counts(self) -> None:
        """Test that default options fill up all character slots"""
        total_character_count = 18
        valid_characters = [character for character in items.characters if character != "None"]
        all_placed_characters = [item.name for item in self.multiworld.get_items() if item.player == self.player and item.name in valid_characters]
        self.assertEqual(total_character_count, len(all_placed_characters))

    def test_exclusive_characters(self) -> None:
        """Test that exclusive slots don't share characters"""
        self.setUp()
        for pair in locations.mutually_exclusive_slots:
            self.assertFalse(
                self.get_location(pair[0], self.player).item.name == self.get_location(pair[1], self.player).item.name and
                self.get_location(pair[0], self.player).item.name == self.get_location(pair[1], self.player).item.name)
