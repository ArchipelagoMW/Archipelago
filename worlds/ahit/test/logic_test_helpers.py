from contextlib import contextmanager
from typing import Literal, Union, Dict, Hashable, NamedTuple, cast, Sequence, Iterable, Tuple, List, Any

from .. import HatInTimeWorld, Regions
from .. import Rules as HatInTimeRules
from BaseClasses import Location, Entrance, Region, CollectionState
from worlds.generic import World
from worlds.generic.Rules import set_rule

from . import HatInTimeTestBase

SpotType = Literal["Location", "Entrance", "Region", "RandomizedRegion"]
"""String used to identify the type of a spot."""
Spot = Union[Location, Entrance, Region]
# For grouping purposes, all option values must currently be hashable.
TestOptions = Dict[str, Hashable]
# Real options can contain dictionaries, lists and sets, which are not hashable.
AnyOptions = Dict[str, Any]


class SpotData(NamedTuple):
    """SpotType and the name of the spot."""
    type: SpotType
    name: str

    def get_spot(self, world: HatInTimeWorld) -> Spot:
        spot_type = self.type
        if spot_type == "Location":
            return world.get_location(self.name)
        elif spot_type == "Entrance":
            return world.get_entrance(self.name)
        elif spot_type == "Region":
            return world.get_region(self.name)
        elif spot_type == "RandomizedRegion":
            return world.get_region(Regions.get_region_shuffled_to(world, self.name))
        else:
            raise AssertionError(f"'{spot_type}' is not a valid spot type")

    def unrandomize(self, test_base: HatInTimeTestBase) -> "SpotData":
        if self.type != "RandomizedRegion":
            raise TypeError(f"Only RandomizedRegion can be unrandomized, but got {self}")
        world = cast(HatInTimeWorld, test_base.world)
        return SpotData("Region", Regions.get_region_shuffled_to(world, self.name))


def block_access_rule(state: CollectionState):
    """
    Simple access rule used to block access to locations and entrances and avoid creating lots of `lambda state: False`.
    """
    return False


def block_access(spot: Union[Location, Entrance]):
    """Small helper to block access to a location or entrance."""
    set_rule(spot, block_access_rule)


class TestConditions(NamedTuple):
    """The test conditions to set up for a SpotTest"""

    possible_items: Sequence[Sequence[str]]
    """
    The spot should be inaccessible without all of the required items, and accessible with any one subsequence of
    required items.
    """

    access_regions: Sequence[Sequence[str]]
    """
    The spot should be accessible with any one of the subsequences of Regions, and all Regions within a subsequence
    should be required.

    This is slightly different from possible_items because there cannot be duplicate Regions. 
    """

    options: TestOptions
    """
    World options to use during the subtest.

    Each unique dictionary of options results in a new test world being set up.

    Non-hashable option values are not currently supported.
    """

    required_clearable_acts: Sequence[str]
    """
    The spot should be inaccessible without all of these required acts being clearable.

    These requirements are only used for act entrances within telescopes and for time rift entrances.

    There are no cases where there are multiple different sets of required clearable acts that would each give access,
    so this is a flat sequence, unlike the other conditions.

    See `Rules.act_connections` and `Rules.set_rift_rules()`/`Rules.set_default_rift_rules()`, or directly see use of
    `Rules.can_clear_required_act()`.
    """

    negative: bool = False
    """
    When True, tests for a spot being unreachable with the given access regions and all items, except for each set of
    items to collect.

    Tests that check for spots being accessible already check that the spot is unreachable if one of the
    required items is missing, so this bool is more useful for testing that specific region and/or option combinations
    are insufficient to reach a spot even with all items.
    """

    @staticmethod
    def parse_strings(strings: Union[Iterable[Union[Iterable[str], str]], str, None]) -> Sequence[Tuple[str, ...]]:
        """
        Helper that parses inputs strings in a mix of formats into a sequence of tuples of strings.
        s1 -> [(s1,)]
        [s1, s2, s3] -> [(s1,), (s2,), (s3,)]
        [s1, [s2, s3]] ->  [(s1,), (s2, s3)]
        [[s1, s2, s3]] -> [(s1, s2, s3)]
        """
        if strings is None:
            return []
        if isinstance(strings, str):
            return [(strings,)]
        return [(s,) if isinstance(s, str) else tuple(s) for s in strings]

    @classmethod
    def new(cls,
            negative: bool,
            access_regions: Union[Iterable[Union[Iterable[str], str]], str, None],
            required_items: Union[Iterable[Union[Iterable[str], str]], str, None],
            required_clearable_acts: Union[Iterable[str], str, None],
            options: TestOptions) -> "TestConditions":
        possible_items = cls.parse_strings(required_items)
        access_regions = cls.parse_strings(access_regions)
        if required_clearable_acts is None:
            required_clearable_acts = ()
        elif isinstance(required_clearable_acts, str):
            required_clearable_acts = (required_clearable_acts,)
        else:
            required_clearable_acts = tuple(required_clearable_acts)
        return cls(possible_items, access_regions, options, required_clearable_acts, negative)

    @classmethod
    def always(cls,
               access_regions: Union[Iterable[Union[Iterable[str], str]], str, None],
               required_items: Union[Iterable[Union[Iterable[str], str]], str, None] = None,
               required_clearable_acts: Union[Iterable[str], str, None] = None,
               **options: Hashable):
        return cls.new(False, access_regions, required_items, required_clearable_acts, options)

    @classmethod
    def always_on_difficulties(cls,
                               access_regions: Union[Iterable[Union[Iterable[str], str]], str, None],
                               required_items: Union[Iterable[Union[Iterable[str], str]], str, None] = None,
                               required_clearable_acts: Union[Iterable[str], str, None] = None,
                               min_difficulty: Literal[None, "moderate", "hard", "expert"] = None,
                               max_difficulty: Literal["normal", "moderate", "hard", None] = None,
                               **options: Hashable) -> "List[TestConditions]":
        # Specifying a `min_difficulty` of "normal" or a `max_difficulty` of "expert" would be redundant, so they are
        # not present in the type hints and are chosen when no argument is provided.
        if min_difficulty is None:
            min_difficulty_ = "normal"
        else:
            min_difficulty_ = min_difficulty
        if max_difficulty is None:
            max_difficulty_ = "expert"
        else:
            max_difficulty_ = max_difficulty

        conditions_list = []
        if "LogicDifficulty" in options:
            raise RuntimeError("LogicDifficulty should not be provided when using always_on_difficulties, use the"
                               " `min_difficulty` and `max_difficulty` arguments instead.")
        difficulties = ("normal", "moderate", "hard", "expert")
        start = difficulties.index(min_difficulty_)
        end = difficulties.index(max_difficulty_)
        for difficulty in difficulties[start:end+1]:
            conditions = cls.always(access_regions, required_items, required_clearable_acts, LogicDifficulty=difficulty,
                                    **options)
            conditions_list.append(conditions)
        return conditions_list

    @classmethod
    def never(cls,
              access_regions: Union[Iterable[Union[Iterable[str], str]], str, None],
              collect_all_but_items: Union[Iterable[Union[Iterable[str], str]], str, None] = None,
              required_clearable_acts: Union[Iterable[str], str, None] = None,
              **options: Hashable):
        return cls.new(True, access_regions, collect_all_but_items, required_clearable_acts, options)

    @classmethod
    def never_on_difficulties(cls,
                              access_regions: Union[Iterable[Union[Iterable[str], str]], str, None],
                              collect_all_but_items: Union[Iterable[Union[Iterable[str], str]], str, None] = None,
                              required_clearable_acts: Union[Iterable[str], str, None] = None,
                              max_difficulty: Literal["normal", "moderate", "hard", "expert"] = "expert",
                              **options: Hashable) -> "List[TestConditions]":
        conditions_list = []
        if "LogicDifficulty" in options:
            raise RuntimeError("LogicDifficulty should not be provided when using never_on_difficulties, use the"
                               "`max_difficulty` argument instead.")
        for difficulty in ("normal", "moderate", "hard", "expert"):
            conditions = cls.never(access_regions, collect_all_but_items, required_clearable_acts,
                                   LogicDifficulty=difficulty, **options)
            conditions_list.append(conditions)
            if difficulty == max_difficulty:
                break
        return conditions_list


TestDataKey = Union[str, Tuple[str, ...]]
TestDataValue = List[TestConditions]
TestData = Dict[TestDataKey, TestDataValue]


@contextmanager
def mock_region_access(world: World, region_name: str):
    """
    Context manager that temporarily grants access to the given region and revokes access when exiting the context.
    """
    origin_region = world.get_region(world.origin_region_name)
    target_region = world.get_region(region_name)
    new_entrance = origin_region.connect(target_region)
    try:
        yield
    finally:
        origin_region.exits.remove(new_entrance)
        target_region.entrances.remove(new_entrance)
        # There should not be anything that can still use the entrance after is has been removed, but block access
        # to be extra sure.
        block_access(new_entrance)


@contextmanager
def mock_no_region_access(world: World, region_name: str):
    """
    Context manager that blocks all entrances to the given region and unblocks the entrances when exiting the
    context.
    """
    target_region = world.get_region(region_name)
    entrances = []
    for entrance in target_region.entrances:
        # Store the old access rule.
        entrances.append((entrance, entrance.access_rule))
        block_access(entrance)
    try:
        yield
    finally:
        # Restore the old access rules.
        for entrance, access_rule in entrances:
            entrance.access_rule = access_rule


@contextmanager
def mock_can_clear_acts(act_names: Iterable[str]):
    original = HatInTimeRules.can_clear_required_act

    act_names = set(act_names)

    def replacement(state: CollectionState, world: HatInTimeWorld, act_entrance: str) -> bool:
        return act_entrance in act_names

    HatInTimeRules.can_clear_required_act = replacement
    try:
        yield
    finally:
        # Restore the old function.
        HatInTimeRules.can_clear_required_act = original


@contextmanager
def mock_can_clear_all_acts():
    original = HatInTimeRules.can_clear_required_act

    HatInTimeRules.can_clear_required_act = lambda state, world, act_entrance: True
    try:
        yield
    finally:
        # Restore the old function.
        HatInTimeRules.can_clear_required_act = original


def hashable_vanilla_act_plando(*act_names: str) -> frozenset[tuple[str, str]]:
    """
    To properly test insanity act plando, it is sometimes necessary to prevent the act randomization from being able to
    create an alternate path to reach the region that is being tested.

    Options used in tests need to be hashable so that tests requiring the same options can be grouped together, so this
    returns a frozenset(tuple[str, str]), which can be reconstructed into an ActPlando dict later on.
    """
    # {entrance_name: act_to_place}
    act_plando_dict = {name: name for name in act_names}
    return frozenset(act_plando_dict.items())
