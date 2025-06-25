import unittest
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from typing_extensions import override

from BaseClasses import Item, ItemClassification, Location, Region
from Options import Choice, PerGameCommonOptions, Toggle
from rule_builder import (
    And,
    CanReachLocation,
    CanReachRegion,
    False_,
    Has,
    HasAll,
    HasAny,
    OptionFilter,
    Or,
    Rule,
    RuleWorldMixin,
    True_,
)
from test.general import setup_solo_multiworld
from test.param import classvar_matrix
from worlds import network_data_package
from worlds.AutoWorld import World

if TYPE_CHECKING:
    from BaseClasses import CollectionState, MultiWorld


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


GAME = "Rule Builder Test Game"
LOC_COUNT = 5


class RuleBuilderItem(Item):
    game: str = GAME


class RuleBuilderLocation(Location):
    game: str = GAME


class RuleBuilderWorld(RuleWorldMixin, World):  # pyright: ignore[reportUnsafeMultipleInheritance]
    game: ClassVar[str] = GAME
    item_name_to_id: ClassVar[dict[str, int]] = {f"Item {i}": i for i in range(1, LOC_COUNT + 1)}
    location_name_to_id: ClassVar[dict[str, int]] = {f"Location {i}": i for i in range(1, LOC_COUNT + 1)}
    hidden: ClassVar[bool] = True
    options_dataclass: "ClassVar[type[PerGameCommonOptions]]" = RuleBuilderOptions
    options: RuleBuilderOptions  # type: ignore # pyright: ignore[reportIncompatibleVariableOverride]
    origin_region_name: str = "Region 1"

    @override
    def create_item(self, name: str) -> "RuleBuilderItem":
        classification = ItemClassification.filler if name == "Filler" else ItemClassification.progression
        return RuleBuilderItem(name, classification, self.item_name_to_id[name], self.player)

    @override
    def get_filler_item_name(self) -> str:
        return "Filler"


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
    multiworld: "MultiWorld"  # pyright: ignore[reportUninitializedInstanceVariable]
    world: "RuleBuilderWorld"  # pyright: ignore[reportUninitializedInstanceVariable]

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


class TestCaching(unittest.TestCase):
    multiworld: "MultiWorld"  # pyright: ignore[reportUninitializedInstanceVariable]
    world: "RuleBuilderWorld"  # pyright: ignore[reportUninitializedInstanceVariable]
    state: "CollectionState"  # pyright: ignore[reportUninitializedInstanceVariable]
    player: int = 1

    @override
    def setUp(self) -> None:
        self.multiworld = setup_solo_multiworld(RuleBuilderWorld, seed=0)
        world = self.multiworld.worlds[1]
        assert isinstance(world, RuleBuilderWorld)
        self.world = world
        self.state = self.multiworld.state

        region1 = Region("Region 1", self.player, self.multiworld)
        region2 = Region("Region 2", self.player, self.multiworld)
        region3 = Region("Region 3", self.player, self.multiworld)
        self.multiworld.regions.extend([region1, region2, region3])

        region1.add_locations({"Location 1": 1, "Location 2": 2}, RuleBuilderLocation)
        region2.add_locations({"Location 3": 3, "Location 4": 4}, RuleBuilderLocation)
        region3.add_locations({"Location 5": 5}, RuleBuilderLocation)

        world.create_entrance(region1, region2, Has("Item 1"))
        world.create_entrance(region1, region3, HasAny("Item 3", "Item 4"))
        world.set_rule(world.get_location("Location 2"), CanReachRegion("Region 2") & Has("Item 2"))
        world.set_rule(world.get_location("Location 4"), HasAll("Item 2", "Item 3"))
        world.set_rule(world.get_location("Location 5"), CanReachLocation("Location 4"))

        for i in range(1, LOC_COUNT + 1):
            self.multiworld.itempool.append(world.create_item(f"Item {i}"))

        world.register_location_dependencies()

        return super().setUp()

    def test_item_cache_busting(self) -> None:
        entrance = self.world.get_entrance("Region 1 -> Region 2")
        self.assertFalse(entrance.can_reach(self.state))  # populates cache
        self.assertFalse(self.state.rule_cache[1][id(entrance.resolved_rule)])

        self.state.collect(self.world.create_item("Item 1"))  # clears cache, item directly needed
        self.assertNotIn(id(entrance.resolved_rule), self.state.rule_cache[1])
        self.assertTrue(entrance.can_reach(self.state))

    def test_region_cache_busting(self) -> None:
        location = self.world.get_location("Location 2")
        self.state.collect(self.world.create_item("Item 2"))  # item directly needed for location rule
        self.assertFalse(location.can_reach(self.state))  # populates cache
        self.assertFalse(self.state.rule_cache[1][id(location.resolved_rule)])

        self.state.collect(self.world.create_item("Item 1"))  # clears cache, item only needed for region 2 access
        # cache gets cleared during the can_reach
        self.assertTrue(location.can_reach(self.state))
        self.assertTrue(self.state.rule_cache[1][id(location.resolved_rule)])

    def test_location_cache_busting(self) -> None:
        location = self.world.get_location("Location 5")
        self.state.collect(self.world.create_item("Item 1"))  # access to region 2
        self.state.collect(self.world.create_item("Item 3"))  # access to region 3
        self.assertFalse(location.can_reach(self.state))  # populates cache
        self.assertFalse(self.state.rule_cache[1][id(location.resolved_rule)])

        self.state.collect(self.world.create_item("Item 2"))  # clears cache, item only needed for location 2 access
        # self.assertNotIn(id(location.resolved_rule), self.state.rule_cache[1])
        self.assertTrue(location.can_reach(self.state))
