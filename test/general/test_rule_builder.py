import unittest
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from typing_extensions import override

from Options import Choice, PerGameCommonOptions, Toggle
from rule_builder import And, False_, Has, HasAll, HasAny, OptionFilter, Or, Rule, RuleWorldMixin, True_
from test.general import setup_solo_multiworld
from test.param import classvar_matrix
from worlds import network_data_package
from worlds.AutoWorld import World

if TYPE_CHECKING:
    from BaseClasses import MultiWorld


class ToggleOption(Toggle):
    auto_display_name: ClassVar[bool] = True


class ChoiceOption(Choice):
    option_first: ClassVar[int] = 0
    option_second: ClassVar[int] = 1
    option_third: ClassVar[int] = 2
    default: ClassVar[int] = 0


@dataclass
class RuleBuilderOptions(PerGameCommonOptions):
    toggle_option: ToggleOption
    choice_option: ChoiceOption


class RuleBuilderWorld(RuleWorldMixin, World):
    game: ClassVar[str] = "Rule Builder Test Game"
    item_name_to_id: ClassVar[dict[str, int]] = {}
    location_name_to_id: ClassVar[dict[str, int]] = {}
    hidden: ClassVar[bool] = True
    options_dataclass = RuleBuilderOptions
    options: RuleBuilderOptions  # type: ignore


network_data_package["games"][RuleBuilderWorld.game] = RuleBuilderWorld.get_data_package_data()


@classvar_matrix(
    rules=(
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
    rules: ClassVar[tuple[Rule[RuleBuilderWorld], Rule.Resolved]]

    def test_simplify(self) -> None:
        multiworld = setup_solo_multiworld(RuleBuilderWorld, steps=("generate_early",), seed=0)
        world = multiworld.worlds[1]
        assert isinstance(world, RuleBuilderWorld)
        rule, expected = self.rules
        resolved_rule = rule.resolve(world)
        self.assertEqual(resolved_rule, expected, str(resolved_rule))


class TestOptions(unittest.TestCase):
    multiworld: "MultiWorld"
    world: "RuleBuilderWorld"

    @override
    def setUp(self) -> None:
        self.multiworld = setup_solo_multiworld(RuleBuilderWorld, steps=("generate_early",), seed=0)
        world = self.multiworld.worlds[1]
        assert isinstance(world, RuleBuilderWorld)
        self.world = world
        return super().setUp()

    def test_option_filtering(self) -> None:
        rule = Or(Has("A", options=[OptionFilter(ToggleOption, 0)]), Has("B", options=[OptionFilter(ToggleOption, 1)]))

        self.world.options.toggle_option.value = 0
        self.assertEqual(rule.resolve(self.world), Has.Resolved("A", player=1))

        self.world.options.toggle_option.value = 1
        self.assertEqual(rule.resolve(self.world), Has.Resolved("B", player=1))

    def test_gt_filtering(self) -> None:
        rule = Or(Has("A", options=[OptionFilter(ChoiceOption, 1, operator="gt")]), False_())

        self.world.options.choice_option.value = 0
        self.assertEqual(rule.resolve(self.world), False_.Resolved(player=1))

        self.world.options.choice_option.value = 1
        self.assertEqual(rule.resolve(self.world), False_.Resolved(player=1))

        self.world.options.choice_option.value = 2
        self.assertEqual(rule.resolve(self.world), Has.Resolved("A", player=1))


@classvar_matrix(
    rules=(
        (
            Has("A") & Has("B"),
            And(Has("A"), Has("B")),
        ),
        (
            Has("A") | Has("B"),
            Or(Has("A"), Has("B")),
        ),
        (
            And(Has("A")) & Has("B"),
            And(Has("A"), Has("B")),
        ),
        (
            And(Has("A"), Has("B")) & And(Has("C")),
            And(Has("A"), Has("B"), Has("C")),
        ),
        (
            And(Has("A"), Has("B")) | Or(Has("C"), Has("D")),
            Or(And(Has("A"), Has("B")), Has("C"), Has("D")),
        ),
        (
            Or(Has("A")) | Or(Has("B"), options=[OptionFilter(ToggleOption, 1)]),
            Or(Or(Has("A")), Or(Has("B"), options=[OptionFilter(ToggleOption, 1)])),
        ),
        (
            (
                And(Has("A"), options=[OptionFilter(ToggleOption, 1)])
                & And(Has("B"), options=[OptionFilter(ToggleOption, 1)])
            ),
            And(Has("A"), Has("B"), options=[OptionFilter(ToggleOption, 1)]),
        ),
        (
            Has("A") & Has("B") & Has("C"),
            And(Has("A"), Has("B"), Has("C")),
        ),
        (
            Has("A") & Has("B") | Has("C") & Has("D"),
            Or(And(Has("A"), Has("B")), And(Has("C"), Has("D"))),
        ),
    )
)
class TestComposition(unittest.TestCase):
    rules: ClassVar[tuple[Rule[RuleBuilderWorld], Rule[RuleBuilderWorld]]]

    def test_composition(self) -> None:
        combined_rule, expected = self.rules
        self.assertEqual(combined_rule, expected, str(combined_rule))


class TestHashes(unittest.TestCase):
    def test_hashes(self) -> None:
        rule1 = And.Resolved((True_.Resolved(player=1),), player=1)
        rule2 = And.Resolved((True_.Resolved(player=1),), player=1)
        rule3 = Or.Resolved((True_.Resolved(player=1),), player=1)

        self.assertEqual(hash(rule1), hash(rule2))
        self.assertNotEqual(hash(rule1), hash(rule3))
