from typing import TypedDict, Iterable, TypeVar
from typing_extensions import Unpack

from test.bases import WorldTestBase

T = TypeVar('T')


def all_pairwise_combinations(*possible_items: T) -> Iterable[tuple[T, T]]:
    for i in range(1, len(possible_items)):
        second = possible_items[i]
        for j in range(i):
            first = possible_items[j]
            yield first, second


class CollectKwargs(TypedDict):
    collect: bool | None


class AccessTest(WorldTestBase):
    game = 'Autopelago'

    def setUp(self):
        super(AccessTest, self).setUp()
        self.pack_rat = self.world.create_item('Pack Rat')
        self.rat_pack = self.world.create_item('Rat Pack')

    def collectRats(self, rat_count: int):
        self.collect((self.pack_rat for _ in range(rat_count)))

    def removeRats(self, rat_count: int):
        self.remove((self.pack_rat for _ in range(rat_count)))

    def assertAndCollectAccessDependencyFromHere(self, location: str, *possible_items: str | list[str],
                                                 **kwargs: Unpack[CollectKwargs]):
        for item_list in possible_items:
            if item_list is str:
                item_list = (item_list,)

            self.assertFalse(self.can_reach_location(location))
            self.collect_by_name(item_list)
            self.assertTrue(self.can_reach_location(location))
            self.remove_by_name(item_list)
        if ('collect' not in kwargs) or kwargs['collect']:
            self.collect_by_name(possible_items[0])

    def assertAndCollectAdditionalRatsFromHere(self, location: str, rat_count: int, collect=True):
        self.collectRats(max(0, rat_count - 5))
        self.assertFalse(self.can_reach_location(location))
        self.collect(self.rat_pack)
        self.assertTrue(self.can_reach_location(location))
        self.remove(self.rat_pack)
        self.collectRats(min(rat_count, 5))
        self.assertTrue(self.can_reach_location(location))
        if not collect:
            self.removeRats(rat_count)

    def testTopBranches(self) -> None:
        # World 1
        self.assertAndCollectAdditionalRatsFromHere('Basketball', 5)
        self.assertAndCollectAccessDependencyFromHere('Prawn Stars', 'Premium Can of Prawn Food', 'Priceless Antique')
        self.assertAndCollectAccessDependencyFromHere('Angry Turtles', 'Pizza Rat', 'Ninja Rat', collect=False)
        self.assertAndCollectAccessDependencyFromHere('Pirate Bake Sale', 'Pie Rat')
        self.assertAndCollectAdditionalRatsFromHere('Bowling Ball Door', 4)
        self.assertAndCollectAccessDependencyFromHere('Captured Goldfish', 'Giant Novelty Scissors')

        # World 2
        self.assertAndCollectAccessDependencyFromHere('Computer Interface', 'Computer Rat')
        self.assertAndCollectAccessDependencyFromHere('Kart Races', 'Blue Turtle Shell', 'Banana Peel')
        self.assertAndCollectAccessDependencyFromHere('Daring Adventurer', 'Masterful Longsword', 'MacGuffin',
                                                      collect=False)
        self.assertAndCollectAdditionalRatsFromHere('Broken-Down Bus', 14)
        self.assertAndCollectAccessDependencyFromHere('Copyright Mouse', 'Fake Mouse Ears', 'Legally Binding Contract')
        self.assertAndCollectAdditionalRatsFromHere('Room Full of Typewriters', 12, collect=False)
        self.assertAndCollectAccessDependencyFromHere('Binary Tree', 'Child\'s First Hand Axe')
        self.assertAndCollectAccessDependencyFromHere('Rat Rap Battle', 'Fifty Cents', 'Notorious R.A.T.')
        self.assertAndCollectAccessDependencyFromHere('Secret Cache', 'Virtual Key', 'Map of the Entire Internet')

        # World 3
        self.assertAndCollectAccessDependencyFromHere('Makeshift Rocket Ship', *all_pairwise_combinations(
            'Energy Drink that is Pure Rocket Fuel', 'Pile of Scrap Metal in the Shape of a Rocket Ship',
            'Ratstronaut', 'Turbo Encabulator'))
        self.assertAndCollectAccessDependencyFromHere('Robo-Clop: The Robot War Horse', 'Quantum Sugar Cube')
        self.assertAndCollectAccessDependencyFromHere('Homeless Mummy', 'Pharaoh-Not Anti-Mummy Spray', 'Ziggu Rat',
                                                      collect=False)
        self.assertAndCollectAdditionalRatsFromHere('Stalled Rocket', 15)
        self.assertAndCollectAccessDependencyFromHere('Seal of Fortune', 'Constellation Prize', 'Free Vowel')
        self.assertAndCollectAdditionalRatsFromHere('Space Opera', 9)
        self.assertAndCollectAccessDependencyFromHere('Minotaur Labyrinth', 'Red Matador\'s Cape', 'Lab Rat',
                                                      collect=False)
        self.assertBeatable(False)
        self.assertAndCollectAccessDependencyFromHere('Snakes on a Planet', 'Mongoose in a Combat Spacecraft')
        self.assertBeatable(True)

    def testBottomBranches(self) -> None:
        # World 1
        self.assertAndCollectAdditionalRatsFromHere('Basketball', 5)
        self.assertAndCollectAccessDependencyFromHere('Angry Turtles', 'Pizza Rat', 'Ninja Rat')
        self.assertAndCollectAccessDependencyFromHere('Prawn Stars', 'Premium Can of Prawn Food', 'Priceless Antique',
                                                      collect=False)
        self.assertAndCollectAccessDependencyFromHere('Restaurant', 'Chef Rat')
        self.assertAndCollectAdditionalRatsFromHere('Bowling Ball Door', 3)
        self.assertAndCollectAccessDependencyFromHere('Captured Goldfish', 'Giant Novelty Scissors')

        # World 2
        self.assertAndCollectAccessDependencyFromHere('Computer Interface', 'Computer Rat')
        self.assertAndCollectAccessDependencyFromHere('Daring Adventurer', 'Masterful Longsword', 'MacGuffin')
        self.assertAndCollectAccessDependencyFromHere('Kart Races', 'Blue Turtle Shell', 'Banana Peel', collect=False)
        self.assertAndCollectAdditionalRatsFromHere('Overweight Boulder', 14)
        self.assertAndCollectAccessDependencyFromHere('Blue-Colored Screen Interface', 'Lost CTRL Key',
                                                      'Hammer of Problem-Solving')
        self.assertAndCollectAccessDependencyFromHere('Trapeze', 'Acro Rat', collect=False)
        self.assertAndCollectAccessDependencyFromHere('Computer Ram', 'Artificial Grass')
        self.assertAndCollectAccessDependencyFromHere('Stack of Crates', 'Forklift Certification', 'Gym Rat')
        self.assertAndCollectAccessDependencyFromHere('Secret Cache', 'Virtual Key', 'Map of the Entire Internet')

        # World 3
        self.assertAndCollectAccessDependencyFromHere('Makeshift Rocket Ship', *all_pairwise_combinations(
            'Energy Drink that is Pure Rocket Fuel', 'Pile of Scrap Metal in the Shape of a Rocket Ship',
            'Ratstronaut', 'Turbo Encabulator'))
        self.assertAndCollectAccessDependencyFromHere('Robo-Clop: The Robot War Horse', 'Quantum Sugar Cube')
        self.assertAndCollectAdditionalRatsFromHere('Stalled Rocket', 15, collect=False)
        self.assertAndCollectAccessDependencyFromHere('Homeless Mummy', 'Pharaoh-Not Anti-Mummy Spray', 'Ziggu Rat')
        self.assertAndCollectAccessDependencyFromHere('Frozen Assets', 'Playing with Fire For Dummies', collect=False)
        self.assertAndCollectAccessDependencyFromHere('Alien Vending Machine', 'Foreign Coin', collect=False)
        self.assertAndCollectAccessDependencyFromHere('Seal of Fortune', 'Constellation Prize', 'Free Vowel')
        self.assertAndCollectAccessDependencyFromHere('Minotaur Labyrinth', 'Red Matador\'s Cape', 'Lab Rat')
        self.assertAndCollectAdditionalRatsFromHere('Space Opera', 24, collect=False)
        self.assertAndCollectAccessDependencyFromHere('Asteroid with Pants', 'Asteroid Belt', 'Moon Shaped Like a Butt',
                                                      collect=False)
        self.assertBeatable(False)
        self.assertAndCollectAccessDependencyFromHere('Snakes on a Planet', 'Mongoose in a Combat Spacecraft')
        self.assertBeatable(True)
