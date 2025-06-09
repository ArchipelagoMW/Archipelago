import unittest
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from Options import Choice, PerGameCommonOptions, Toggle
from rule_builder import And, False_, Has, HasAll, HasAny, Or, Rule, RuleWorldMixin
from test.general import setup_solo_multiworld
from test.param import classvar_matrix
from worlds import network_data_package
from worlds.AutoWorld import World

if TYPE_CHECKING:
    from BaseClasses import MultiWorld


class ToggleOption(Toggle):
    auto_display_name = True


class ChoiceOption(Choice):
    option_first = 0
    option_second = 1
    option_third = 2
    default = 0


@dataclass
class RuleBuilderOptions(PerGameCommonOptions):
    toggle_option: ToggleOption
    choice_option: ChoiceOption


class RuleBuilderWorld(RuleWorldMixin, World):
    game = "Rule Builder Test Game"
    item_name_to_id = {}
    location_name_to_id = {}
    hidden = True
    options_dataclass = RuleBuilderOptions
    options: RuleBuilderOptions  # type: ignore


network_data_package["games"][RuleBuilderWorld.game] = RuleBuilderWorld.get_data_package_data()


@classvar_matrix(
    rule=(
        (
            And(Has("A", 1), Has("A", 2)),
            Has.Resolved("A", 2, player=1),
        ),
        (
            And(Has("A"), HasAll("B", "C")),
            HasAll.Resolved(("A", "B", "C"), player=1),
        ),
        (
            Or(Has("A", 1), Has("A", 2)),
            Has.Resolved("A", 1, player=1),
        ),
        (
            Or(Has("A"), HasAny("B", "C")),
            HasAny.Resolved(("A", "B", "C"), player=1),
        ),
        (
            Or(HasAll("A"), HasAll("A", "A")),
            Has.Resolved("A", player=1),
        ),
    )
)
class TestSimplify(unittest.TestCase):
    rule: ClassVar[tuple[Rule, Rule.Resolved]]

    def test_simplify(self) -> None:
        multiworld = setup_solo_multiworld(RuleBuilderWorld, steps=("generate_early",), seed=0)
        world = multiworld.worlds[1]
        rule, expected = self.rule
        self.assertEqual(rule.resolve(world), expected)  # type: ignore


class TestOptions(unittest.TestCase):
    multiworld: "MultiWorld"
    world: "RuleBuilderWorld"

    def setUp(self) -> None:
        self.multiworld = setup_solo_multiworld(RuleBuilderWorld, steps=("generate_early",), seed=0)
        self.world = self.multiworld.worlds[1]  # type: ignore
        return super().setUp()

    def test_option_filtering(self) -> None:
        rule = Or(Has("A", options={"toggle_option": 0}), Has("B", options={"toggle_option": 1}))

        self.world.options.toggle_option.value = 0
        self.assertEqual(rule.resolve(self.world), Has.Resolved("A", player=1))

        self.world.options.toggle_option.value = 1
        self.assertEqual(rule.resolve(self.world), Has.Resolved("B", player=1))

    def test_gt_filtering(self) -> None:
        rule = Or(Has("A", options={"choice_option__gt": 1}), False_())

        self.world.options.choice_option.value = 0
        self.assertEqual(rule.resolve(self.world), False_.Resolved(player=1))

        self.world.options.choice_option.value = 1
        self.assertEqual(rule.resolve(self.world), False_.Resolved(player=1))

        self.world.options.choice_option.value = 2
        self.assertEqual(rule.resolve(self.world), Has.Resolved("A", player=1))
