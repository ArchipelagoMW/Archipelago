import pytest

from test.general import setup_solo_multiworld
from .. import StardewValleyWorld, StardewLocation
from ..data.bundle_data import BundleItem, all_bundle_items_except_money
from ..stardew_rule import MISSING_ITEM, False_

multi_world = setup_solo_multiworld(StardewValleyWorld)
world = multi_world.worlds[1]
logic = world.logic


def collect_all(mw):
    for item in mw.get_items():
        mw.state.collect(item, event=True)


collect_all(multi_world)


@pytest.mark.parametrize("bundle_item", all_bundle_items_except_money,
                         ids=[i.item.name for i in all_bundle_items_except_money])
def test_given_bundle_item_then_is_available_in_logic(bundle_item: BundleItem):
    assert bundle_item.item.name in logic.item_rules


@pytest.mark.parametrize("item", logic.item_rules.keys(), ids=logic.item_rules.keys())
def test_given_item_rule_then_can_be_resolved(item: str):
    rule = logic.item_rules[item]

    assert MISSING_ITEM not in repr(rule)
    assert rule == False_() or rule(multi_world.state), f"Could not resolve rule for {item} {rule}"


@pytest.mark.parametrize("item", logic.building_rules.keys(), ids=logic.building_rules.keys())
def test_given_building_rule_then_can_be_resolved(item: str):
    rule = logic.building_rules[item]

    assert MISSING_ITEM not in repr(rule)
    assert rule == False_() or rule(multi_world.state), f"Could not resolve rule for {item} {rule}"


@pytest.mark.parametrize("item", logic.quest_rules.keys(), ids=logic.quest_rules.keys())
def test_given_quest_rule_then_can_be_resolved(item: str):
    rule = logic.quest_rules[item]

    assert MISSING_ITEM not in repr(rule)
    assert rule == False_() or rule(multi_world.state), f"Could not resolve rule for {item} {rule}"


@pytest.mark.parametrize("location", multi_world.get_locations(1),
                         ids=[loc.name for loc in multi_world.get_locations(1)])
def test_given_location_rule_then_can_be_resolved(location: StardewLocation):
    rule = location.access_rule

    assert MISSING_ITEM not in repr(rule)
    assert rule == False_() or rule(multi_world.state), f"Could not resolve rule for {location} {rule}"
