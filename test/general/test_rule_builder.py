import unittest
from typing import ClassVar

from rule_builder import And, Has, HasAll, HasAny, Or, Rule, RuleWorldMixin
from test.general import setup_solo_multiworld
from test.param import classvar_matrix
from worlds.AutoWorld import World


class RuleBuilderWorld(RuleWorldMixin, World):
    game = "Rule Builder Test Game"
    item_name_to_id = {}
    location_name_to_id = {}
    hidden = True


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
