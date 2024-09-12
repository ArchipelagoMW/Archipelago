from typing import List

from BaseClasses import CollectionState
from ..Data import get_era_required_items_data
from ..Enum import EraType
from ..ProgressiveDistricts import convert_items_to_have_progression
from ..Items import get_item_by_civ_name
from . import CivVITestBase


def collect_items_for_era(test: CivVITestBase, era: EraType) -> None:
    era_required_items = get_era_required_items_data()
    items = [get_item_by_civ_name(item, test.world.item_table).name for item in era_required_items[era.value]]
    test.collect_by_name(items)


def collect_items_for_era_progressive(test: CivVITestBase, era: EraType) -> None:
    era_progression_items = get_era_required_items_data()
    progressive_items = convert_items_to_have_progression(
        era_progression_items[era.value])
    items = [get_item_by_civ_name(item, test.world.item_table).name for item in progressive_items]
    test.collect_by_name(items)


def verify_eras_accessible(test: CivVITestBase, state: CollectionState, collect_func):
    for era in EraType:
        if era == EraType.ERA_ANCIENT:
            test.assertTrue(state.can_reach(
                era.value, "Region", test.player))
        else:
            test.assertFalse(state.can_reach(
                era.value, "Region", test.player))

    collect_func(test, EraType.ERA_ANCIENT)
    test.assertTrue(state.can_reach(
        EraType.ERA_CLASSICAL.value, "Region", test.player))

    collect_func(test, EraType.ERA_CLASSICAL)
    test.assertTrue(state.can_reach(
        EraType.ERA_MEDIEVAL.value, "Region", test.player))

    collect_func(test, EraType.ERA_MEDIEVAL)
    test.assertTrue(state.can_reach(
        EraType.ERA_RENAISSANCE.value, "Region", test.player))

    collect_func(test, EraType.ERA_RENAISSANCE)
    test.assertTrue(state.can_reach(
        EraType.ERA_INDUSTRIAL.value, "Region", test.player))

    collect_func(test, EraType.ERA_INDUSTRIAL)
    test.assertTrue(state.can_reach(
        EraType.ERA_MODERN.value, "Region", test.player))

    collect_func(test, EraType.ERA_MODERN)
    test.assertTrue(state.can_reach(
        EraType.ERA_ATOMIC.value, "Region", test.player))

    collect_func(test, EraType.ERA_ATOMIC)
    test.assertTrue(state.can_reach(
        EraType.ERA_INFORMATION.value, "Region", test.player))

    collect_func(test, EraType.ERA_INFORMATION)
    test.assertTrue(state.can_reach(
        EraType.ERA_FUTURE.value, "Region", test.player))


class TestNonProgressiveRegionRequirements(CivVITestBase):
    options = {
        "pre_hint_items": "all",
        "progression_style": "none",
        "death_link": "false",
        "death_link_effect": "unit_killed",
        "boostsanity": "false",
    }

    def test_eras_are_accessible_without_progressive_districts(self) -> None:
        state = self.multiworld.state
        verify_eras_accessible(self, state, collect_items_for_era)


class TestNonProgressiveRegionRequirementsWithBoostsanity(CivVITestBase):
    options = {
        "pre_hint_items": "all",
        "progression_style": "none",
        "death_link": "false",
        "death_link_effect": "unit_killed",
        "boostsanity": "true",
    }

    def test_eras_are_accessible_without_progressive_districts(self) -> None:
        state = self.multiworld.state
        verify_eras_accessible(self, state, collect_items_for_era)


class TestProgressiveDistrictRequirementsWithBoostsanity(CivVITestBase):
    options = {
        "pre_hint_items": "all",
        "progression_style": "districts_only",
        "death_link": "false",
        "death_link_effect": "unit_killed",
        "boostsanity": "true",
    }

    def test_eras_are_accessible_with_progressive_districts(self) -> None:
        state = self.multiworld.state
        verify_eras_accessible(self, state, collect_items_for_era_progressive)


class TestProgressiveDistrictRequirements(CivVITestBase):
    options = {
        "pre_hint_items": "all",
        "progression_style": "districts_only",
        "death_link": "false",
        "death_link_effect": "unit_killed",
        "boostsanity": "false",
    }

    def test_eras_are_accessible_with_progressive_districts(self) -> None:
        state = self.multiworld.state
        verify_eras_accessible(self, state, collect_items_for_era_progressive)


class TestProgressiveEraRequirements(CivVITestBase):
    options = {
        "pre_hint_items": "all",
        "progression_style": "eras_and_districts",
        "death_link": "false",
        "death_link_effect": "unit_killed"
    }

    def test_eras_are_accessible_with_progressive_eras(self) -> None:
        state = self.multiworld.state
        self.collect_all_but(["Progressive Era"])

        def check_eras_accessible(eras: List[EraType]):
            for era in EraType:
                if era in eras:
                    self.assertTrue(state.can_reach(
                        era.value, "Region", self.player))
                else:
                    self.assertFalse(state.can_reach(
                        era.value, "Region", self.player))

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
        "pre_hint_items": "all",
        "progression_style": "eras_and_districts",
        "death_link": "false",
        "death_link_effect": "unit_killed",
        "boostsanity": "true",
    }

    def test_eras_are_accessible_with_progressive_eras(self) -> None:
        state = self.multiworld.state
        self.collect_all_but(["Progressive Era"])

        def check_eras_accessible(eras: List[EraType]):
            for era in EraType:
                if era in eras:
                    self.assertTrue(state.can_reach(
                        era.value, "Region", self.player))
                else:
                    self.assertFalse(state.can_reach(
                        era.value, "Region", self.player))

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

