import unittest
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, ClassVar

from typing_extensions import override

from BaseClasses import Item, ItemClassification, Location, Region
from Options import Choice, PerGameCommonOptions, Toggle
from rule_builder import (
    And,
    CanReachEntrance,
    CanReachLocation,
    CanReachRegion,
    False_,
    Has,
    HasAll,
    HasAllCounts,
    HasAny,
    HasAnyCount,
    HasFromList,
    HasFromListUnique,
    HasGroup,
    HasGroupUnique,
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
LOC_COUNT = 6


class RuleBuilderItem(Item):
    game: str = GAME


class RuleBuilderLocation(Location):
    game: str = GAME


class RuleBuilderWorld(RuleWorldMixin, World):  # pyright: ignore[reportUnsafeMultipleInheritance]
    game: ClassVar[str] = GAME
    item_name_to_id: ClassVar[dict[str, int]] = {f"Item {i}": i for i in range(1, LOC_COUNT + 1)}
    location_name_to_id: ClassVar[dict[str, int]] = {f"Location {i}": i for i in range(1, LOC_COUNT + 1)}
    item_name_groups: ClassVar[dict[str, set[str]]] = {"Group 1": {"Item 1", "Item 2", "Item 3"}}
    hidden: ClassVar[bool] = True
    options_dataclass: "ClassVar[type[PerGameCommonOptions]]" = RuleBuilderOptions
    options: RuleBuilderOptions  # pyright: ignore[reportIncompatibleVariableOverride]
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
        (
            Or(
                Has("A"),
                Or(
                    True_(options=[OptionFilter(ChoiceOption, 0)]),
                    HasAny("B", "C", options=[OptionFilter(ChoiceOption, 0, "gt")]),
                    options=[OptionFilter(ToggleOption, 1)],
                ),
                And(Has("D"), Has("E"), options=[OptionFilter(ToggleOption, 0)]),
                Has("F"),
            ),
            Or.Resolved(
                (
                    HasAll.Resolved(("D", "E"), player=1),
                    HasAny.Resolved(("A", "F"), player=1),
                ),
                player=1,
            ),
        ),
        (
            Or(
                Has("A"),
                Or(
                    True_(options=[OptionFilter(ChoiceOption, 0, "gt")]),
                    HasAny("B", "C", options=[OptionFilter(ChoiceOption, 0)]),
                    options=[OptionFilter(ToggleOption, 0)],
                ),
                And(Has("D"), Has("E"), options=[OptionFilter(ToggleOption, 1)]),
                Has("F"),
            ),
            HasAny.Resolved(("A", "B", "C", "F"), player=1),
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
        resolved_rule = world.resolve_rule(rule)
        self.assertEqual(resolved_rule, expected, f"\n{resolved_rule}\n{expected}")


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
        self.assertEqual(self.world.resolve_rule(rule), Has.Resolved("A", player=1))

        self.world.options.toggle_option.value = 1
        self.assertEqual(self.world.resolve_rule(rule), Has.Resolved("B", player=1))

    def test_gt_filtering(self) -> None:
        rule = Or(Has("A", options=[OptionFilter(ChoiceOption, 1, operator="gt")]), False_())

        self.world.options.choice_option.value = 0
        self.assertEqual(self.world.resolve_rule(rule), False_.Resolved(player=1))

        self.world.options.choice_option.value = 1
        self.assertEqual(self.world.resolve_rule(rule), False_.Resolved(player=1))

        self.world.options.choice_option.value = 2
        self.assertEqual(self.world.resolve_rule(rule), Has.Resolved("A", player=1))


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
    def test_and_hash(self) -> None:
        rule1 = And.Resolved((True_.Resolved(player=1),), player=1)
        rule2 = And.Resolved((True_.Resolved(player=1),), player=1)
        rule3 = Or.Resolved((True_.Resolved(player=1),), player=1)

        self.assertEqual(hash(rule1), hash(rule2))
        self.assertNotEqual(hash(rule1), hash(rule3))

    def test_has_all_hash(self) -> None:
        multiworld = setup_solo_multiworld(RuleBuilderWorld, steps=("generate_early",), seed=0)
        world = multiworld.worlds[1]
        assert isinstance(world, RuleBuilderWorld)

        rule1 = HasAll("1", "2")
        rule2 = HasAll("2", "2", "2", "1")
        self.assertEqual(hash(world.resolve_rule(rule1)), hash(world.resolve_rule(rule2)))


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

        region1.add_locations({"Location 1": 1, "Location 2": 2, "Location 6": 6}, RuleBuilderLocation)
        region2.add_locations({"Location 3": 3, "Location 4": 4}, RuleBuilderLocation)
        region3.add_locations({"Location 5": 5}, RuleBuilderLocation)

        world.create_entrance(region1, region2, Has("Item 1"))
        world.create_entrance(region1, region3, HasAny("Item 3", "Item 4"))
        world.set_rule(world.get_location("Location 2"), CanReachRegion("Region 2") & Has("Item 2"))
        world.set_rule(world.get_location("Location 4"), HasAll("Item 2", "Item 3"))
        world.set_rule(world.get_location("Location 5"), CanReachLocation("Location 4"))
        world.set_rule(world.get_location("Location 6"), CanReachEntrance("Region 1 -> Region 2") & Has("Item 2"))

        for i in range(1, LOC_COUNT + 1):
            self.multiworld.itempool.append(world.create_item(f"Item {i}"))

        world.register_dependencies()

        return super().setUp()

    def test_item_cache_busting(self) -> None:
        entrance = self.world.get_entrance("Region 1 -> Region 2")
        self.assertFalse(entrance.can_reach(self.state))  # populates cache
        self.assertFalse(self.state.rule_cache[1][id(entrance.access_rule)])

        self.state.collect(self.world.create_item("Item 1"))  # clears cache, item directly needed
        self.assertNotIn(id(entrance.access_rule), self.state.rule_cache[1])
        self.assertTrue(entrance.can_reach(self.state))

    def test_region_cache_busting(self) -> None:
        location = self.world.get_location("Location 2")
        self.state.collect(self.world.create_item("Item 2"))  # item directly needed for location rule
        self.assertFalse(location.can_reach(self.state))  # populates cache
        self.assertFalse(self.state.rule_cache[1][id(location.access_rule)])

        self.state.collect(self.world.create_item("Item 1"))  # clears cache, item only needed for region 2 access
        # cache gets cleared during the can_reach
        self.assertTrue(location.can_reach(self.state))
        self.assertTrue(self.state.rule_cache[1][id(location.access_rule)])

    def test_location_cache_busting(self) -> None:
        location = self.world.get_location("Location 5")
        self.state.collect(self.world.create_item("Item 1"))  # access to region 2
        self.state.collect(self.world.create_item("Item 3"))  # access to region 3
        self.assertFalse(location.can_reach(self.state))  # populates cache
        self.assertFalse(self.state.rule_cache[1][id(location.access_rule)])

        self.state.collect(self.world.create_item("Item 2"))  # clears cache, item only needed for location 2 access
        self.assertNotIn(id(location.access_rule), self.state.rule_cache[1])
        self.assertTrue(location.can_reach(self.state))

    def test_entrance_cache_busting(self) -> None:
        location = self.world.get_location("Location 6")
        self.state.collect(self.world.create_item("Item 2"))  # item directly needed for location rule
        self.assertFalse(location.can_reach(self.state))  # populates cache
        self.assertFalse(self.state.rule_cache[1][id(location.access_rule)])

        self.state.collect(self.world.create_item("Item 1"))  # clears cache, item only needed for entrance access
        self.assertNotIn(id(location.access_rule), self.state.rule_cache[1])
        self.assertTrue(location.can_reach(self.state))


class TestCacheDisabled(unittest.TestCase):
    multiworld: "MultiWorld"  # pyright: ignore[reportUninitializedInstanceVariable]
    world: "RuleBuilderWorld"  # pyright: ignore[reportUninitializedInstanceVariable]
    state: "CollectionState"  # pyright: ignore[reportUninitializedInstanceVariable]
    player: int = 1

    @override
    def setUp(self) -> None:
        self.multiworld = setup_solo_multiworld(RuleBuilderWorld, seed=0)
        world = self.multiworld.worlds[1]
        assert isinstance(world, RuleBuilderWorld)
        world.rule_caching_enabled = False  # pyright: ignore[reportAttributeAccessIssue]
        self.world = world
        self.state = self.multiworld.state

        region1 = Region("Region 1", self.player, self.multiworld)
        region2 = Region("Region 2", self.player, self.multiworld)
        region3 = Region("Region 3", self.player, self.multiworld)
        self.multiworld.regions.extend([region1, region2, region3])

        region1.add_locations({"Location 1": 1, "Location 2": 2, "Location 6": 6}, RuleBuilderLocation)
        region2.add_locations({"Location 3": 3, "Location 4": 4}, RuleBuilderLocation)
        region3.add_locations({"Location 5": 5}, RuleBuilderLocation)

        world.create_entrance(region1, region2, Has("Item 1"))
        world.create_entrance(region1, region3, HasAny("Item 3", "Item 4"))
        world.set_rule(world.get_location("Location 2"), CanReachRegion("Region 2") & Has("Item 2"))
        world.set_rule(world.get_location("Location 4"), HasAll("Item 2", "Item 3"))
        world.set_rule(world.get_location("Location 5"), CanReachLocation("Location 4"))
        world.set_rule(world.get_location("Location 6"), CanReachEntrance("Region 1 -> Region 2") & Has("Item 2"))

        for i in range(1, LOC_COUNT + 1):
            self.multiworld.itempool.append(world.create_item(f"Item {i}"))

        world.register_dependencies()

        return super().setUp()

    def test_item_logic(self) -> None:
        entrance = self.world.get_entrance("Region 1 -> Region 2")
        self.assertFalse(entrance.can_reach(self.state))
        self.assertFalse(self.state.rule_cache[1])

        self.state.collect(self.world.create_item("Item 1"))  # item directly needed
        self.assertFalse(self.state.rule_cache[1])
        self.assertTrue(entrance.can_reach(self.state))

    def test_region_logic(self) -> None:
        location = self.world.get_location("Location 2")
        self.state.collect(self.world.create_item("Item 2"))  # item directly needed for location rule
        self.assertFalse(location.can_reach(self.state))
        self.assertFalse(self.state.rule_cache[1])

        self.state.collect(self.world.create_item("Item 1"))  # item only needed for region 2 access
        self.assertTrue(location.can_reach(self.state))
        self.assertFalse(self.state.rule_cache[1])

    def test_location_logic(self) -> None:
        location = self.world.get_location("Location 5")
        self.state.collect(self.world.create_item("Item 1"))  # access to region 2
        self.state.collect(self.world.create_item("Item 3"))  # access to region 3
        self.assertFalse(location.can_reach(self.state))
        self.assertFalse(self.state.rule_cache[1])

        self.state.collect(self.world.create_item("Item 2"))  # item only needed for location 2 access
        self.assertFalse(self.state.rule_cache[1])
        self.assertTrue(location.can_reach(self.state))

    def test_entrance_logic(self) -> None:
        location = self.world.get_location("Location 6")
        self.state.collect(self.world.create_item("Item 2"))  # item directly needed for location rule
        self.assertFalse(location.can_reach(self.state))
        self.assertFalse(self.state.rule_cache[1])

        self.state.collect(self.world.create_item("Item 1"))  # item only needed for entrance access
        self.assertFalse(self.state.rule_cache[1])
        self.assertTrue(location.can_reach(self.state))


class TestRules(unittest.TestCase):
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

    def test_true(self) -> None:
        rule = True_()
        resolved_rule = self.world.resolve_rule(rule)
        self.world.register_rule_dependencies(resolved_rule)
        self.assertTrue(resolved_rule(self.state))

    def test_false(self) -> None:
        rule = False_()
        resolved_rule = self.world.resolve_rule(rule)
        self.world.register_rule_dependencies(resolved_rule)
        self.assertFalse(resolved_rule(self.state))

    def test_has(self) -> None:
        rule = Has("Item 1")
        resolved_rule = self.world.resolve_rule(rule)
        self.world.register_rule_dependencies(resolved_rule)
        self.assertFalse(resolved_rule(self.state))
        item = self.world.create_item("Item 1")
        self.state.collect(item)
        self.assertTrue(resolved_rule(self.state))
        self.state.remove(item)
        self.assertFalse(resolved_rule(self.state))

    def test_has_all(self) -> None:
        rule = HasAll("Item 1", "Item 2")
        resolved_rule = self.world.resolve_rule(rule)
        self.world.register_rule_dependencies(resolved_rule)
        self.assertFalse(resolved_rule(self.state))
        item1 = self.world.create_item("Item 1")
        self.state.collect(item1)
        self.assertFalse(resolved_rule(self.state))
        item2 = self.world.create_item("Item 2")
        self.state.collect(item2)
        self.assertTrue(resolved_rule(self.state))
        self.state.remove(item1)
        self.assertFalse(resolved_rule(self.state))

    def test_has_any(self) -> None:
        item_names = ("Item 1", "Item 2")
        rule = HasAny(*item_names)
        resolved_rule = self.world.resolve_rule(rule)
        self.world.register_rule_dependencies(resolved_rule)
        self.assertFalse(resolved_rule(self.state))

        for item_name in item_names:
            item = self.world.create_item(item_name)
            self.state.collect(item)
            self.assertTrue(resolved_rule(self.state))
            self.state.remove(item)
            self.assertFalse(resolved_rule(self.state))

    def test_has_all_counts(self) -> None:
        rule = HasAllCounts({"Item 1": 1, "Item 2": 2})
        resolved_rule = self.world.resolve_rule(rule)
        self.world.register_rule_dependencies(resolved_rule)
        self.assertFalse(resolved_rule(self.state))
        item1 = self.world.create_item("Item 1")
        self.state.collect(item1)
        self.assertFalse(resolved_rule(self.state))
        item2 = self.world.create_item("Item 2")
        self.state.collect(item2)
        self.assertFalse(resolved_rule(self.state))
        item2 = self.world.create_item("Item 2")
        self.state.collect(item2)
        self.assertTrue(resolved_rule(self.state))
        self.state.remove(item2)
        self.assertFalse(resolved_rule(self.state))

    def test_has_any_count(self) -> None:
        item_counts = {"Item 1": 1, "Item 2": 2}
        rule = HasAnyCount(item_counts)
        resolved_rule = self.world.resolve_rule(rule)
        self.world.register_rule_dependencies(resolved_rule)

        for item_name, count in item_counts.items():
            item = self.world.create_item(item_name)
            for _ in range(count):
                self.assertFalse(resolved_rule(self.state))
                self.state.collect(item)
            self.assertTrue(resolved_rule(self.state))
            self.state.remove(item)
            self.assertFalse(resolved_rule(self.state))

    def test_has_from_list(self) -> None:
        item_names = ("Item 1", "Item 2", "Item 3")
        rule = HasFromList(*item_names, count=2)
        resolved_rule = self.world.resolve_rule(rule)
        self.world.register_rule_dependencies(resolved_rule)
        self.assertFalse(resolved_rule(self.state))

        items: list[Item] = []
        for i, item_name in enumerate(item_names):
            item = self.world.create_item(item_name)
            self.state.collect(item)
            items.append(item)
            if i == 0:
                self.assertFalse(resolved_rule(self.state))
            else:
                self.assertTrue(resolved_rule(self.state))

        for i in range(2):
            self.state.remove(items[i])
        self.assertFalse(resolved_rule(self.state))

    def test_has_from_list_unique(self) -> None:
        item_names = ("Item 1", "Item 1", "Item 2")
        rule = HasFromListUnique(*item_names, count=2)
        resolved_rule = self.world.resolve_rule(rule)
        self.world.register_rule_dependencies(resolved_rule)
        self.assertFalse(resolved_rule(self.state))

        items: list[Item] = []
        for i, item_name in enumerate(item_names):
            item = self.world.create_item(item_name)
            self.state.collect(item)
            items.append(item)
            if i < 2:
                self.assertFalse(resolved_rule(self.state))
            else:
                self.assertTrue(resolved_rule(self.state))

        self.state.remove(items[0])
        self.assertTrue(resolved_rule(self.state))
        self.state.remove(items[1])
        self.assertFalse(resolved_rule(self.state))

    def test_has_group(self) -> None:
        rule = HasGroup("Group 1", count=2)
        resolved_rule = self.world.resolve_rule(rule)
        self.world.register_rule_dependencies(resolved_rule)

        items: list[Item] = []
        for item_name in ("Item 1", "Item 2"):
            self.assertFalse(resolved_rule(self.state))
            item = self.world.create_item(item_name)
            self.state.collect(item)
            items.append(item)

        self.assertTrue(resolved_rule(self.state))
        self.state.remove(items[0])
        self.assertFalse(resolved_rule(self.state))

    def test_has_group_unique(self) -> None:
        rule = HasGroupUnique("Group 1", count=2)
        resolved_rule = self.world.resolve_rule(rule)
        self.world.register_rule_dependencies(resolved_rule)

        items: list[Item] = []
        for item_name in ("Item 1", "Item 1", "Item 2"):
            self.assertFalse(resolved_rule(self.state))
            item = self.world.create_item(item_name)
            self.state.collect(item)
            items.append(item)

        self.assertTrue(resolved_rule(self.state))
        self.state.remove(items[0])
        self.assertTrue(resolved_rule(self.state))
        self.state.remove(items[1])
        self.assertFalse(resolved_rule(self.state))


class TestSerialization(unittest.TestCase):
    maxDiff: int | None = None

    rule: ClassVar[Rule[Any]] = And(
        Or(
            Has("i1", count=4),
            HasFromList("i2", "i3", "i4", count=2),
            HasAnyCount({"i5": 2, "i6": 3}),
            options=[OptionFilter(ToggleOption, 0)],
        ),
        Or(
            HasAll("i7", "i8"),
            HasAllCounts({"i9": 1, "i10": 5}, options=[OptionFilter(ToggleOption, 1, operator="ne")]),
            CanReachRegion("r1"),
            HasGroup("g1"),
        ),
        And(
            HasAny("i11", "i12"),
            CanReachLocation("l1", "r2"),
            HasFromListUnique("i13", "i14"),
            options=[
                OptionFilter(ToggleOption, ToggleOption.option_false),
                OptionFilter(ChoiceOption, ChoiceOption.option_second, "ge"),
            ],
        ),
        CanReachEntrance("e1"),
        HasGroupUnique("g2", count=5),
    )

    rule_dict: ClassVar[dict[str, Any]] = {
        "rule": "And",
        "options": [],
        "children": [
            {
                "rule": "Or",
                "options": [
                    {
                        "option": "test.general.test_rule_builder.ToggleOption",
                        "value": 0,
                        "operator": "eq",
                    },
                ],
                "children": [
                    {
                        "rule": "Has",
                        "options": [],
                        "args": {"item_name": "i1", "count": 4},
                    },
                    {
                        "rule": "HasFromList",
                        "options": [],
                        "args": {"item_names": ("i2", "i3", "i4"), "count": 2},
                    },
                    {
                        "rule": "HasAnyCount",
                        "options": [],
                        "args": {"item_counts": {"i5": 2, "i6": 3}},
                    },
                ],
            },
            {
                "rule": "Or",
                "options": [],
                "children": [
                    {
                        "rule": "HasAll",
                        "options": [],
                        "args": {"item_names": ("i7", "i8")},
                    },
                    {
                        "rule": "HasAllCounts",
                        "options": [
                            {
                                "option": "test.general.test_rule_builder.ToggleOption",
                                "value": 1,
                                "operator": "ne",
                            },
                        ],
                        "args": {"item_counts": {"i9": 1, "i10": 5}},
                    },
                    {
                        "rule": "CanReachRegion",
                        "options": [],
                        "args": {"region_name": "r1"},
                    },
                    {
                        "rule": "HasGroup",
                        "options": [],
                        "args": {"item_name_group": "g1", "count": 1},
                    },
                ],
            },
            {
                "rule": "And",
                "options": [
                    {
                        "option": "test.general.test_rule_builder.ToggleOption",
                        "value": 0,
                        "operator": "eq",
                    },
                    {
                        "option": "test.general.test_rule_builder.ChoiceOption",
                        "value": 1,
                        "operator": "ge",
                    },
                ],
                "children": [
                    {
                        "rule": "HasAny",
                        "options": [],
                        "args": {"item_names": ("i11", "i12")},
                    },
                    {
                        "rule": "CanReachLocation",
                        "options": [],
                        "args": {"location_name": "l1", "parent_region_name": "r2", "skip_indirect_connection": False},
                    },
                    {
                        "rule": "HasFromListUnique",
                        "options": [],
                        "args": {"item_names": ("i13", "i14"), "count": 1},
                    },
                ],
            },
            {
                "rule": "CanReachEntrance",
                "options": [],
                "args": {"entrance_name": "e1", "parent_region_name": ""},
            },
            {
                "rule": "HasGroupUnique",
                "options": [],
                "args": {"item_name_group": "g2", "count": 5},
            },
        ],
    }

    def test_serialize(self) -> None:
        serialized_rule = self.rule.to_dict()
        self.assertDictEqual(serialized_rule, self.rule_dict)

    def test_deserialize(self) -> None:
        multiworld = setup_solo_multiworld(RuleBuilderWorld, steps=(), seed=0)
        world = multiworld.worlds[1]
        assert isinstance(world, RuleBuilderWorld)

        deserialized_rule = world.rule_from_dict(self.rule_dict)
        self.assertEqual(deserialized_rule, self.rule, str(deserialized_rule))
