from typing import Callable, List

from BaseClasses import CollectionState
from ..Data import get_era_required_items_data
from ..Enum import EraType
from ..ProgressiveDistricts import convert_items_to_progressive_items
from ..Items import get_item_by_civ_name
from . import CivVITestBase


def collect_items_for_era(test: CivVITestBase, era: EraType) -> None:
    era_required_items = get_era_required_items_data()
    items = [
        get_item_by_civ_name(item, test.world.item_table).name
        for item in era_required_items[era.value]
    ]
    test.collect_by_name(items)


def collect_items_for_era_progressive(test: CivVITestBase, era: EraType) -> None:
    era_progression_items = get_era_required_items_data()
    progressive_items = convert_items_to_progressive_items(
        era_progression_items[era.value]
    )
    items = [
        get_item_by_civ_name(item, test.world.item_table).name
        for item in progressive_items
    ]
    for item in items:
        test.collect(test.get_item_by_name(item))


def verify_eras_accessible(
    test: CivVITestBase,
    state: CollectionState,
    collect_func: Callable[[CivVITestBase, EraType], None],
) -> None:
    """Collect for an era, then check if the next era is accessible and the one after that is not"""
    for era in EraType:
        if era == EraType.ERA_ANCIENT:
            test.assertTrue(state.can_reach(era.value, "Region", test.player))
        else:
            test.assertFalse(state.can_reach(era.value, "Region", test.player))

    eras = [
        EraType.ERA_ANCIENT,
        EraType.ERA_CLASSICAL,
        EraType.ERA_MEDIEVAL,
        EraType.ERA_RENAISSANCE,
        EraType.ERA_INDUSTRIAL,
        EraType.ERA_MODERN,
        EraType.ERA_ATOMIC,
        EraType.ERA_INFORMATION,
        EraType.ERA_FUTURE,
    ]

    for i in range(len(eras) - 1):
        collect_func(test, eras[i])
        test.assertTrue(state.can_reach(eras[i + 1].value, "Region", test.player))
        if i + 2 < len(eras):
            test.assertFalse(state.can_reach(eras[i + 2].value, "Region", test.player))


class TestNonProgressiveRegionRequirements(CivVITestBase):
    options = {
        "progression_style": "none",
        "boostsanity": "false",
    }

    def test_eras_are_accessible_without_progressive_districts(self) -> None:
        state = self.multiworld.state
        verify_eras_accessible(self, state, collect_items_for_era)


class TestNonProgressiveRegionRequirementsWithBoostsanity(CivVITestBase):
    options = {
        "progression_style": "none",
        "boostsanity": "true",
    }

    def test_eras_are_accessible_without_progressive_districts(self) -> None:
        state = self.multiworld.state
        verify_eras_accessible(self, state, collect_items_for_era)


class TestProgressiveDistrictRequirementsWithBoostsanity(CivVITestBase):
    options = {
        "progression_style": "districts_only",
        "boostsanity": "true",
    }

    def test_eras_are_accessible_with_progressive_districts(self) -> None:
        state = self.multiworld.state
        verify_eras_accessible(self, state, collect_items_for_era_progressive)


class TestProgressiveDistrictRequirements(CivVITestBase):
    options = {
        "progression_style": "districts_only",
        "boostsanity": "false",
    }

    def test_eras_are_accessible_with_progressive_districts(self) -> None:
        state = self.multiworld.state
        verify_eras_accessible(self, state, collect_items_for_era_progressive)

    def test_progressive_districts_are_required(self) -> None:
        state = self.multiworld.state
        self.collect_all_but(["Progressive Encampment"])
        self.assertFalse(state.can_reach("ERA_CLASSICAL", "Region", self.player))
        self.assertFalse(state.can_reach("ERA_RENAISSANCE", "Region", self.player))
        self.assertFalse(state.can_reach("ERA_MODERN", "Region", self.player))

        self.collect(self.get_item_by_name("Progressive Encampment"))
        self.assertTrue(state.can_reach("ERA_CLASSICAL", "Region", self.player))
        self.assertFalse(state.can_reach("ERA_RENAISSANCE", "Region", self.player))
        self.assertFalse(state.can_reach("ERA_MODERN", "Region", self.player))

        self.collect(self.get_item_by_name("Progressive Encampment"))
        self.assertTrue(state.can_reach("ERA_RENAISSANCE", "Region", self.player))
        self.assertFalse(state.can_reach("ERA_MODERN", "Region", self.player))

        self.collect(self.get_item_by_name("Progressive Encampment"))
        self.assertTrue(state.can_reach("ERA_MODERN", "Region", self.player))


class TestProgressiveEraRequirements(CivVITestBase):
    options = {
        "progression_style": "eras_and_districts",
    }

    def test_eras_are_accessible_with_progressive_eras(self) -> None:
        state = self.multiworld.state
        self.collect_all_but(["Progressive Era"])

        def check_eras_accessible(eras: List[EraType]):
            for era in EraType:
                if era in eras:
                    self.assertTrue(state.can_reach(era.value, "Region", self.player))
                else:
                    self.assertFalse(state.can_reach(era.value, "Region", self.player))

        progresive_era_item = self.get_item_by_name("Progressive Era")
        accessible_eras = [EraType.ERA_ANCIENT]
        check_eras_accessible(accessible_eras)

        # Classical era requires 2 progressive era items
        self.collect(progresive_era_item)
        accessible_eras += [EraType.ERA_CLASSICAL]
        check_eras_accessible(accessible_eras)

        self.collect(progresive_era_item)
        accessible_eras += [EraType.ERA_MEDIEVAL]
        check_eras_accessible(accessible_eras)

        self.collect(progresive_era_item)
        accessible_eras += [EraType.ERA_RENAISSANCE]
        check_eras_accessible(accessible_eras)

        self.collect(progresive_era_item)
        accessible_eras += [EraType.ERA_INDUSTRIAL]
        check_eras_accessible(accessible_eras)

        self.collect(progresive_era_item)
        accessible_eras += [EraType.ERA_MODERN]
        check_eras_accessible(accessible_eras)

        self.collect(progresive_era_item)
        accessible_eras += [EraType.ERA_ATOMIC]
        check_eras_accessible(accessible_eras)

        # Since we collect 2 in the ancient era, information and future era have same logic requirement
        self.collect(progresive_era_item)
        accessible_eras += [EraType.ERA_INFORMATION]
        accessible_eras += [EraType.ERA_FUTURE]
        check_eras_accessible(accessible_eras)


class TestProgressiveEraRequirementsWithBoostsanity(CivVITestBase):
    options = {
        "progression_style": "eras_and_districts",
        "boostsanity": "true",
    }

    def test_eras_are_accessible_with_progressive_eras(self) -> None:
        state = self.multiworld.state
        self.collect_all_but(["Progressive Era"])

        def check_eras_accessible(eras: List[EraType]):
            for era in EraType:
                if era in eras:
                    self.assertTrue(
                        state.can_reach(era.value, "Region", self.player),
                        "Failed for era: " + era.value,
                    )
                else:
                    self.assertFalse(
                        state.can_reach(era.value, "Region", self.player),
                        "Failed for era: " + era.value,
                    )

        progresive_era_item = self.get_item_by_name("Progressive Era")
        accessible_eras = [EraType.ERA_ANCIENT]
        check_eras_accessible(accessible_eras)

        self.collect(progresive_era_item)
        accessible_eras += [EraType.ERA_CLASSICAL]
        check_eras_accessible(accessible_eras)

        self.collect(progresive_era_item)
        accessible_eras += [EraType.ERA_MEDIEVAL]
        check_eras_accessible(accessible_eras)

        self.collect(progresive_era_item)
        accessible_eras += [EraType.ERA_RENAISSANCE]
        check_eras_accessible(accessible_eras)

        self.collect(progresive_era_item)
        accessible_eras += [EraType.ERA_INDUSTRIAL]
        check_eras_accessible(accessible_eras)

        self.collect(progresive_era_item)
        accessible_eras += [EraType.ERA_MODERN]
        check_eras_accessible(accessible_eras)

        self.collect(progresive_era_item)
        accessible_eras += [EraType.ERA_ATOMIC]
        check_eras_accessible(accessible_eras)

        # Since we collect 2 in the ancient era, information and future era have same logic requirement
        self.collect(progresive_era_item)
        accessible_eras += [EraType.ERA_INFORMATION]
        accessible_eras += [EraType.ERA_FUTURE]
        check_eras_accessible(accessible_eras)
