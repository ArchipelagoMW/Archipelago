from typing import List

from BaseClasses import Item, Location
from test.bases import WorldTestBase


class TestPrizes(WorldTestBase):
    game = "A Link to the Past"

    def test_item_rules(self):
        prize_locations: List[Location] = [
            self.multiworld.get_location("Eastern Palace - Prize", 1),
            self.multiworld.get_location("Desert Palace - Prize", 1),
            self.multiworld.get_location("Tower of Hera - Prize", 1),
            self.multiworld.get_location("Palace of Darkness - Prize", 1),
            self.multiworld.get_location("Swamp Palace - Prize", 1),
            self.multiworld.get_location("Thieves\' Town - Prize", 1),
            self.multiworld.get_location("Skull Woods - Prize", 1),
            self.multiworld.get_location("Ice Palace - Prize", 1),
            self.multiworld.get_location("Misery Mire - Prize", 1),
            self.multiworld.get_location("Turtle Rock - Prize", 1),
        ]
        prize_items: List[Item] = [
            self.get_item_by_name("Green Pendant"),
            self.get_item_by_name("Blue Pendant"),
            self.get_item_by_name("Red Pendant"),
            self.get_item_by_name("Crystal 1"),
            self.get_item_by_name("Crystal 2"),
            self.get_item_by_name("Crystal 3"),
            self.get_item_by_name("Crystal 4"),
            self.get_item_by_name("Crystal 5"),
            self.get_item_by_name("Crystal 6"),
            self.get_item_by_name("Crystal 7"),
        ]

        for item in self.multiworld.get_items():
            for prize_location in prize_locations:
                self.assertEqual(item in prize_items, prize_location.item_rule(item),
                                 f"{item} must {'' if item in prize_items else 'not '}be allowed in {prize_location}.")
