from collections.abc import Iterable
from typing import TypedDict, TypeVar

from test.bases import WorldTestBase
from typing_extensions import Unpack

T = TypeVar("T")


def all_pairwise_combinations(*possible_items: T) -> Iterable[tuple[T, T]]:
    for i in range(1, len(possible_items)):
        second = possible_items[i]
        for j in range(i):
            first = possible_items[j]
            yield first, second


class CollectKwargs(TypedDict):
    collect: bool | None


class AccessTest(WorldTestBase):
    game = "Autopelago"

    def setUp(self):
        super().setUp()
        self.pack_rat = self.world.create_item("Pack Rat")
        self.rat_pack = self.world.create_item("Rat Pack")

    def collect_rats(self, rat_count: int):
        self.collect(self.pack_rat for _ in range(rat_count))

    def remove_rats(self, rat_count: int):
        self.remove(self.pack_rat for _ in range(rat_count))

    def assert_and_collect_access_dependency_from_here(self, location: str, *possible_items: str | list[str],
                                                       **kwargs: Unpack[CollectKwargs]):
        for original_item_list in possible_items:
            item_list = (original_item_list,) if original_item_list is str else original_item_list
            self.assertFalse(self.can_reach_location(location))
            self.collect_by_name(item_list)
            self.assertTrue(self.can_reach_location(location))
            self.remove_by_name(item_list)
        if ("collect" not in kwargs) or kwargs["collect"]:
            self.collect_by_name(possible_items[0])

    def assert_and_collect_additional_rats_from_here(self, location: str, rat_count: int, collect=True):
        self.collect_rats(max(0, rat_count - 5))
        self.assertFalse(self.can_reach_location(location))
        self.collect(self.rat_pack)
        self.assertTrue(self.can_reach_location(location))
        self.remove(self.rat_pack)
        self.collect_rats(min(rat_count, 5))
        self.assertTrue(self.can_reach_location(location))
        if not collect:
            self.remove_rats(rat_count)

    def test_top_branches(self) -> None:
        # World 1
        self.assert_and_collect_additional_rats_from_here(
            "Basketball", 5)
        self.assert_and_collect_access_dependency_from_here(
            "Prawn Stars", "Premium Can of Prawn Food", "Priceless Antique")
        self.assert_and_collect_access_dependency_from_here(
            "Angry Turtles", "Pizza Rat", "Ninja Rat", collect=False)
        self.assert_and_collect_access_dependency_from_here(
            "Pirate Bake Sale", "Pie Rat")
        self.assert_and_collect_additional_rats_from_here(
            "Bowling Ball Door", 4)
        self.assert_and_collect_access_dependency_from_here(
            "Captured Goldfish", "Giant Novelty Scissors")

        # World 2
        self.assert_and_collect_access_dependency_from_here(
            "Computer Interface", "Computer Rat")
        self.assert_and_collect_access_dependency_from_here(
            "Kart Races", "Blue Turtle Shell", "Banana Peel")
        self.assert_and_collect_access_dependency_from_here(
            "Daring Adventurer", "Masterful Longsword", "MacGuffin", collect=False)
        self.assert_and_collect_additional_rats_from_here(
            "Broken-Down Bus", 14)
        self.assert_and_collect_access_dependency_from_here(
            "Copyright Mouse", "Fake Mouse Ears", "Legally Binding Contract")
        self.assert_and_collect_additional_rats_from_here(
            "Room Full of Typewriters", 12, collect=False)
        self.assert_and_collect_access_dependency_from_here(
            "Binary Tree", "Child's First Hand Axe")
        self.assert_and_collect_access_dependency_from_here(
            "Rat Rap Battle", "Fifty Cents", "Notorious R.A.T.")
        self.assert_and_collect_access_dependency_from_here(
            "Secret Cache", "Virtual Key", "Map of the Entire Internet")

        # World 3
        self.assert_and_collect_access_dependency_from_here(
            "Makeshift Rocket Ship", *all_pairwise_combinations(
            "Energy Drink that is Pure Rocket Fuel", "Pile of Scrap Metal in the Shape of a Rocket Ship",
            "Ratstronaut", "Turbo Encabulator"))
        self.assert_and_collect_access_dependency_from_here(
            "Robo-Clop: The Robot War Horse", "Quantum Sugar Cube")
        self.assert_and_collect_access_dependency_from_here(
            "Homeless Mummy", "Pharaoh-Not Anti-Mummy Spray", "Ziggu Rat", collect=False)
        self.assert_and_collect_additional_rats_from_here(
            "Stalled Rocket", 15)
        self.assert_and_collect_access_dependency_from_here(
            "Seal of Fortune", "Constellation Prize", "Free Vowel")
        self.assert_and_collect_additional_rats_from_here(
            "Space Opera", 9)
        self.assert_and_collect_access_dependency_from_here(
            "Minotaur Labyrinth", "Red Matador's Cape", "Lab Rat", collect=False)
        self.assertBeatable(False)
        self.assert_and_collect_access_dependency_from_here(
            "Snakes on a Planet", "Mongoose in a Combat Spacecraft")
        self.assertBeatable(True)

    def test_bottom_branches(self) -> None:
        # World 1
        self.assert_and_collect_additional_rats_from_here(
            "Basketball", 5)
        self.assert_and_collect_access_dependency_from_here(
            "Angry Turtles", "Pizza Rat", "Ninja Rat")
        self.assert_and_collect_access_dependency_from_here(
            "Prawn Stars", "Premium Can of Prawn Food", "Priceless Antique", collect=False)
        self.assert_and_collect_access_dependency_from_here(
            "Restaurant", "Chef Rat")
        self.assert_and_collect_additional_rats_from_here(
            "Bowling Ball Door", 3)
        self.assert_and_collect_access_dependency_from_here(
            "Captured Goldfish", "Giant Novelty Scissors")

        # World 2
        self.assert_and_collect_access_dependency_from_here(
            "Computer Interface", "Computer Rat")
        self.assert_and_collect_access_dependency_from_here(
            "Daring Adventurer", "Masterful Longsword", "MacGuffin")
        self.assert_and_collect_access_dependency_from_here(
            "Kart Races", "Blue Turtle Shell", "Banana Peel", collect=False)
        self.assert_and_collect_additional_rats_from_here(
            "Overweight Boulder", 14)
        self.assert_and_collect_access_dependency_from_here(
            "Blue-Colored Screen Interface", "Lost CTRL Key", "Hammer of Problem-Solving")
        self.assert_and_collect_access_dependency_from_here(
            "Trapeze", "Acro Rat", collect=False)
        self.assert_and_collect_access_dependency_from_here(
            "Computer Ram", "Artificial Grass")
        self.assert_and_collect_access_dependency_from_here(
            "Stack of Crates", "Forklift Certification", "Gym Rat")
        self.assert_and_collect_access_dependency_from_here(
            "Secret Cache", "Virtual Key", "Map of the Entire Internet")

        # World 3
        self.assert_and_collect_access_dependency_from_here(
            "Makeshift Rocket Ship", *all_pairwise_combinations(
            "Energy Drink that is Pure Rocket Fuel", "Pile of Scrap Metal in the Shape of a Rocket Ship",
            "Ratstronaut", "Turbo Encabulator"))
        self.assert_and_collect_access_dependency_from_here(
            "Robo-Clop: The Robot War Horse", "Quantum Sugar Cube")
        self.assert_and_collect_additional_rats_from_here(
            "Stalled Rocket", 15, collect=False)
        self.assert_and_collect_access_dependency_from_here(
            "Homeless Mummy", "Pharaoh-Not Anti-Mummy Spray", "Ziggu Rat")
        self.assert_and_collect_access_dependency_from_here(
            "Frozen Assets", "Playing with Fire For Dummies", collect=False)
        self.assert_and_collect_access_dependency_from_here(
            "Alien Vending Machine", "Foreign Coin", collect=False)
        self.assert_and_collect_access_dependency_from_here(
            "Seal of Fortune", "Constellation Prize", "Free Vowel")
        self.assert_and_collect_access_dependency_from_here(
            "Minotaur Labyrinth", "Red Matador's Cape", "Lab Rat")
        self.assert_and_collect_additional_rats_from_here(
            "Space Opera", 24, collect=False)
        self.assert_and_collect_access_dependency_from_here(
            "Asteroid with Pants", "Asteroid Belt", "Moon Shaped Like a Butt", collect=False)
        self.assertBeatable(False)
        self.assert_and_collect_access_dependency_from_here(
            "Snakes on a Planet", "Mongoose in a Combat Spacecraft")
        self.assertBeatable(True)
