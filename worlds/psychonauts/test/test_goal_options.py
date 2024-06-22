from typing import ClassVar, Iterable
from random import shuffle

from . import PsychonautsTestBase
from .. import Options
from ..Items import BRAIN_JARS
from ..Names import ItemName


# Goal items. Where applicable, specified in the order that they are required to progress towards the goal.
_BRAIN_HUNT_GOAL_ITEMS = set(BRAIN_JARS)
_BRAIN_TANK_GOAL_ITEMS = {
    ItemName.SashaButton,  # Access to GPC+Wilderness
    ItemName.OarsmansBadge,  # Access to Boathouse+Lake
    ItemName.LungfishCall,  # Access to Asylum Grounds and Asylum courtyard
    ItemName.StraightJacket,  # 1/3 Access to Asylum Upper Floors
    ItemName.GloriasTrophy,  # 2/3 Access to Asylum Upper Floors
    ItemName.LobotoPainting,  # 3/3 Access to Asylum Upper Floors
    ItemName.Levitation,  # Required halfway through Asylum Upper Floors
    ItemName.Telekinesis,  # Required near the end of Asylum Upper Floors (also required to beat the boss)
    ItemName.Cake,  # Required to progress through Asylum Lab
    ItemName.Pyrokinesis,  # Required to beat the Brain Tank boss
}
_MEAT_CIRCUS_GOAL_ITEMS = {
    ItemName.OlyMind,  # Access to the Meat Circus level
    ItemName.CobwebDuster,  # Access to the Tent City area of Meat Circus
    ItemName.Telekinesis,  # Required to progress through the escort sequence (also required to beat the boss)
    ItemName.Levitation,  # Required to progress through the escort sequence
}


def _get_random_default_brains():
    """Get a set of random brains with length equal to the default number of brains required for the Brain Hunt goal"""
    brains = list(_BRAIN_HUNT_GOAL_ITEMS)
    shuffle(brains)
    return set(brains[:Options.BrainsRequired.default])


class PsychonautsMinimalVictoryTestBase(PsychonautsTestBase):
    victory_items: ClassVar[Iterable[str]] = set()
    """The exact items required for victory from a minimal starting state"""

    @classmethod
    def setUpClass(cls):
        # For minimal tests, no starting items are allowed.
        cls.options.update({
            "RandomStartingMinds": 0,
            "StartingLevitation": False,
            "StartingMentalMagnet": False,
            "StartingCobwebDuster": False,
        })
        super().setUpClass()

    @property
    def run_default_tests(self) -> bool:
        # This is a base class for Victory tests and does not need to run tests itself
        return type(self) is not PsychonautsMinimalVictoryTestBase and super().run_default_tests

    def test_minimal_victory(self):
        """Ensure victory is possible with only the items required for victory"""
        if not self.run_default_tests:
            return

        victory_items = list(self.victory_items)
        self.assertTrue(victory_items, "victory_items must not be empty")

        # Collect one item at a time.
        for item_name in victory_items:
            self.assertBeatable(False)
            self.collect_by_name(item_name)
        # Only once all the victory items have been collected should victory be possible.
        self.assertBeatable(True)


class TestGoalBrainHuntMinimum(PsychonautsMinimalVictoryTestBase):
    options = {
        "Goal": Options.Goal.option_brainhunt,
        "BrainsRequired": 1,
        "RequireMeatCircus": False,
    }

    def test_minimal_victory(self):
        # Test that each brain individually allows for victory.
        for brain_jar in _BRAIN_HUNT_GOAL_ITEMS:
            self.world_setup()
            self.assertBeatable(False)
            self.collect_by_name(brain_jar)
            self.assertBeatable(True)


class TestGoalBrainHuntMaximum(PsychonautsMinimalVictoryTestBase):
    options = {
        "Goal": Options.Goal.option_brainhunt,
        "BrainsRequired": Options.BrainsRequired.range_end,
        "RequireMeatCircus": False,
    }
    victory_items = _BRAIN_HUNT_GOAL_ITEMS

    def test_unique_brains_only(self):
        """Ensure the Brain Hunt goal only counts unique brains"""
        first_brain, *remaining_brains = _BRAIN_HUNT_GOAL_ITEMS
        for brain_jar in remaining_brains:
            for _ in range(len(_BRAIN_HUNT_GOAL_ITEMS)):
                self.collect_by_name(brain_jar)
        self.assertBeatable(False)
        self.collect_by_name(first_brain)
        self.assertBeatable(True)


class TestGoalBrainHuntDefault(PsychonautsMinimalVictoryTestBase):
    options = {
        "Goal": Options.Goal.option_brainhunt,
        "RequireMeatCircus": False,
    }
    victory_items = _get_random_default_brains()


class TestGoalBrainTank(PsychonautsMinimalVictoryTestBase):
    options = {
        "Goal": Options.Goal.option_braintank,
        "RequireMeatCircus": False,
    }
    victory_items = _BRAIN_TANK_GOAL_ITEMS


class TestGoalBrainHuntAndBrainTank(PsychonautsMinimalVictoryTestBase):
    options = {
        "Goal": Options.Goal.option_braintank_and_brainhunt,
        "RequireMeatCircus": False,
    }
    victory_items = _get_random_default_brains() | _BRAIN_TANK_GOAL_ITEMS


class TestGoalMeatCircusWithBrainHunt(PsychonautsMinimalVictoryTestBase):
    options = {
        "RequireMeatCircus": True,
        "Goal": Options.Goal.option_brainhunt,
    }
    victory_items = _get_random_default_brains() | _MEAT_CIRCUS_GOAL_ITEMS


class TestGoalMeatCircusWithBrainTank(PsychonautsMinimalVictoryTestBase):
    options = {
        "RequireMeatCircus": True,
        "Goal": Options.Goal.option_braintank,
    }
    victory_items = _BRAIN_TANK_GOAL_ITEMS | _MEAT_CIRCUS_GOAL_ITEMS


class TestGoalMeatCircusWithBrainTankAndBrainHunt(PsychonautsMinimalVictoryTestBase):
    options = {
        "RequireMeatCircus": True,
        "Goal": Options.Goal.option_braintank_and_brainhunt,
    }
    victory_items = _get_random_default_brains() | _BRAIN_TANK_GOAL_ITEMS | _MEAT_CIRCUS_GOAL_ITEMS
    extra_possible_victory_items = _BRAIN_HUNT_GOAL_ITEMS
