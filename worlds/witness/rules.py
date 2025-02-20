"""
Defines the rules by which locations can be accessed,
depending on the items received
"""
from collections import Counter
from typing import TYPE_CHECKING, Dict, List, NamedTuple, Optional, Union

from BaseClasses import CollectionState

from worlds.generic.Rules import CollectionRule, set_rule

from .data import static_logic as static_witness_logic
from .data.utils import WitnessRule
from .player_logic import WitnessPlayerLogic

if TYPE_CHECKING:
    from . import WitnessWorld


class SimpleItemRepresentation(NamedTuple):
    item_name: str
    item_count: int


def _can_do_panel_hunt(world: "WitnessWorld") -> SimpleItemRepresentation:
    required = world.panel_hunt_required_count
    return SimpleItemRepresentation("+1 Panel Hunt", required)


def _has_lasers(amount: int, world: "WitnessWorld", redirect_required: bool) -> CollectionRule:
    if redirect_required:
        return lambda state: state.has_from_list(["+1 Laser", "+1 Laser (Redirected)"], world.player, amount)

    return lambda state: state.has_from_list(["+1 Laser", "+1 Laser (Unredirected)"], world.player, amount)


def _can_do_expert_pp2(state: CollectionState, world: "WitnessWorld") -> bool:
    """
    For Expert PP2, you need a way to access PP2 from the front, and a separate way from the back.
    This condition is quite complicated. We'll attempt to evaluate it as lazily as possible.
    """

    player = world.player
    two_way_entrance_register = world.player_regions.two_way_entrance_register

    front_access = (
        any(e.can_reach(state) for e in two_way_entrance_register["Keep 2nd Pressure Plate", "Keep"])
        and state.can_reach_region("Keep", player)
    )

    # If we don't have front access, we can't do PP2.
    if not front_access:
        return False

    # Front access works. Now, we need to check for the many ways to access PP2 from the back.
    # All of those ways lead through the PP3 exit door from PP4. So we check this first.

    fourth_to_third = any(e.can_reach(state) for e in two_way_entrance_register[
        "Keep 3rd Pressure Plate", "Keep 4th Pressure Plate"
    ])

    # If we can't get from PP4 to PP3, we can't do PP2.
    if not fourth_to_third:
        return False

    # We can go from PP4 to PP3. We now need to find a way to PP4.
    # The shadows shortcut is the simplest way.

    shadows_shortcut = (
        any(e.can_reach(state) for e in two_way_entrance_register["Keep 4th Pressure Plate", "Shadows"])
    )

    if shadows_shortcut:
        return True

    # We don't have the Shadows shortcut. This means we need to come in through the PP4 exit door instead.

    tower_to_pp4 = any(e.can_reach(state) for e in two_way_entrance_register["Keep 4th Pressure Plate", "Keep Tower"])

    # If we don't have the PP4 exit door, we've run out of options.
    if not tower_to_pp4:
        return False

    # We have the PP4 exit door. If we can get to Keep Tower from behind, we can do PP2.
    # The simplest way would be the Tower Shortcut.

    tower_shortcut = any(e.can_reach(state) for e in two_way_entrance_register["Keep", "Keep Tower"])

    if tower_shortcut:
        return True

    # We don't have the Tower shortcut. At this point, there is one possibility remaining:
    # Getting to Keep Tower through the hedge mazes. This can be done in a multitude of ways.
    # No matter what, though, we would need Hedge Maze 4 Exit to Keep Tower.

    tower_access_from_hedges = any(e.can_reach(state) for e in two_way_entrance_register["Keep 4th Maze", "Keep Tower"])

    if not tower_access_from_hedges:
        return False

    # We can reach Keep Tower from Hedge Maze 4. If we now have the Hedge 4 Shortcut, we are immediately good.

    hedge_4_shortcut = any(e.can_reach(state) for e in two_way_entrance_register["Keep 4th Maze", "Keep"])

    # If we have the hedge 4 shortcut, that works.
    if hedge_4_shortcut:
        return True

    # We don't have the hedge 4 shortcut. This means we would now need to come through Hedge Maze 3.

    hedge_3_to_4 = any(e.can_reach(state) for e in two_way_entrance_register["Keep 4th Maze", "Keep 3rd Maze"])

    if not hedge_3_to_4:
        return False

    # We can get to Hedge 4 from Hedge 3. If we have the Hedge 3 Shortcut, we're good.

    hedge_3_shortcut = any(e.can_reach(state) for e in two_way_entrance_register["Keep 3rd Maze", "Keep"])

    if hedge_3_shortcut:
        return True

    # We don't have Hedge 3 Shortcut. This means we would now need to come through Hedge Maze 2.

    hedge_2_to_3 = any(e.can_reach(state) for e in two_way_entrance_register["Keep 3rd Maze", "Keep 2nd Maze"])

    if not hedge_2_to_3:
        return False

    # We can get to Hedge 3 from Hedge 2. If we can get from Keep to Hedge 2, we're good.
    # This covers both Hedge 1 Exit and Hedge 2 Shortcut, because Hedge 1 is just part of the Keep region.

    return any(e.can_reach(state) for e in two_way_entrance_register["Keep 2nd Maze", "Keep"])


def _can_do_theater_to_tunnels(state: CollectionState, world: "WitnessWorld") -> bool:
    """
    To do Tunnels Theater Flowers EP, you need to quickly move from Theater to Tunnels.
    This condition is a little tricky. We'll attempt to evaluate it as lazily as possible.
    """

    # Checking for access to Theater is not necessary, as solvability of Tutorial Video is checked in the other half
    # of the Theater Flowers EP condition.

    two_way_entrance_register = world.player_regions.two_way_entrance_register

    direct_access = (
        any(e.can_reach(state) for e in two_way_entrance_register["Tunnels", "Windmill Interior"])
        and any(e.can_reach(state) for e in two_way_entrance_register["Theater", "Windmill Interior"])
    )

    if direct_access:
        return True

    # We don't have direct access through the shortest path.
    # This means we somehow need to exit Theater to the Main Island, and then enter Tunnels from the Main Island.
    # Getting to Tunnels through Mountain -> Caves -> Tunnels is way too slow, so we only expect paths through Town.

    # We need a way from Theater to Town. This is actually guaranteed, otherwise we wouldn't be in Theater.
    # The only ways to Theater are through Town and Tunnels. We just checked the Tunnels way.
    # This might need to be changed when warps are implemented.

    # We also need a way from Town to Tunnels.

    return (
        any(e.can_reach(state) for e in two_way_entrance_register["Tunnels", "Windmill Interior"])
        and any(e.can_reach(state) for e in two_way_entrance_register["Outside Windmill", "Windmill Interior"])
        or any(e.can_reach(state) for e in two_way_entrance_register["Tunnels", "Town"])
    )


def _has_item(item: str, world: "WitnessWorld",
              player_logic: WitnessPlayerLogic) -> Union[CollectionRule, SimpleItemRepresentation]:
    """
    Convert a single element of a WitnessRule into a CollectionRule, unless it is referring to an item,
    in which case we return it as an item-count pair ("SimpleItemRepresentation"). This allows some optimisation later.
    """

    assert item not in static_witness_logic.ENTITIES_BY_HEX, "Requirements can no longer contain entity hexes directly."

    if item in player_logic.REFERENCE_LOGIC.ALL_REGIONS_BY_NAME:
        region = world.get_region(item)
        return region.can_reach
    if item == "7 Lasers":
        laser_req = world.options.mountain_lasers.value
        return _has_lasers(laser_req, world, False)
    if item == "7 Lasers + Redirect":
        laser_req = world.options.mountain_lasers.value
        return _has_lasers(laser_req, world, True)
    if item == "11 Lasers":
        laser_req = world.options.challenge_lasers.value
        return _has_lasers(laser_req, world, False)
    if item == "11 Lasers + Redirect":
        laser_req = world.options.challenge_lasers.value
        return _has_lasers(laser_req, world, True)
    if item == "Entity Hunt":
        # Right now, panel hunt is the only type of entity hunt. This may need to be changed later
        return _can_do_panel_hunt(world)
    if item == "PP2 Weirdness":
        return lambda state: _can_do_expert_pp2(state, world)
    if item == "Theater to Tunnels":
        return lambda state: _can_do_theater_to_tunnels(state, world)

    actual_item = static_witness_logic.get_parent_progressive_item(item)
    needed_amount = player_logic.PARENT_ITEM_COUNT_PER_BASE_ITEM[item]

    simple_rule: SimpleItemRepresentation = SimpleItemRepresentation(actual_item, needed_amount)
    return simple_rule


def optimize_requirement_option(requirement_option: List[Union[CollectionRule, SimpleItemRepresentation]])\
        -> List[Union[CollectionRule, SimpleItemRepresentation]]:
    """
    This optimises out a requirement like [("Progressive Dots": 1), ("Progressive Dots": 2)] to only the "2" version.
    """

    direct_items = [rule for rule in requirement_option if isinstance(rule, SimpleItemRepresentation)]
    if not direct_items:
        return requirement_option

    max_per_item: Dict[str, int] = Counter()
    for item_rule in direct_items:
        max_per_item[item_rule[0]] = max(max_per_item[item_rule[0]], item_rule[1])

    return [
        rule for rule in requirement_option
        if not (isinstance(rule, SimpleItemRepresentation) and rule[1] < max_per_item[rule[0]])
    ]


def convert_requirement_option(requirement: List[Union[CollectionRule, SimpleItemRepresentation]],
                               player: int) -> List[CollectionRule]:
    """
    Converts a list of CollectionRules and SimpleItemRepresentations to just a list of CollectionRules.
    If the list is ONLY SimpleItemRepresentations, we can just return a CollectionRule based on state.has_all_counts()
    """

    collection_rules = [rule for rule in requirement if not isinstance(rule, SimpleItemRepresentation)]
    item_rules = [rule for rule in requirement if isinstance(rule, SimpleItemRepresentation)]

    if len(item_rules) == 0:
        item_rules_converted = []
    elif len(item_rules) == 1:
        item = item_rules[0][0]
        count = item_rules[0][1]
        item_rules_converted = [lambda state: state.has(item, player, count)]
    else:
        item_counts = {item_rule.item_name: item_rule.item_count for item_rule in item_rules}
        # Sort the list by which item you are least likely to have (E.g. last stage of progressive item chains)
        sorted_item_list = sorted(
            item_counts.keys(),
            key=lambda item_name: item_counts[item_name] if ("Progressive" in item_name) else 1.5,
            reverse=True
            # 1.5 because you are less likely to have a single stage item than one copy of a 2-stage chain
            # I did some testing and every part of this genuinely gives a tiiiiny performance boost over not having it!
        )

        if all(item_count == 1 for item_count in item_counts.values()):
            # If all counts are one, just use state.has_all
            item_rules_converted = [lambda state: state.has_all(sorted_item_list, player)]
        else:
            # If any count is higher than 1, use state.has_all_counts
            sorted_item_counts = {item_name: item_counts[item_name] for item_name in sorted_item_list}
            item_rules_converted = [lambda state: state.has_all_counts(sorted_item_counts, player)]

    return collection_rules + item_rules_converted


def _meets_item_requirements(requirements: WitnessRule, world: "WitnessWorld") -> Optional[CollectionRule]:
    """
    Converts a WitnessRule into a CollectionRule.
    """
    player = world.player

    if requirements == frozenset({frozenset()}):
        return None

    rule_conversion = [
        [_has_item(item, world, world.player_logic) for item in subset]
        for subset in requirements
    ]

    optimized_rule_conversion = [optimize_requirement_option(sublist) for sublist in rule_conversion]

    fully_converted_rules = [convert_requirement_option(sublist, player) for sublist in optimized_rule_conversion]

    if len(fully_converted_rules) == 1:
        if len(fully_converted_rules[0]) == 1:
            return fully_converted_rules[0][0]
        return lambda state: all(condition(state) for condition in fully_converted_rules[0])
    return lambda state: any(
        all(condition(state) for condition in sub_requirement)
        for sub_requirement in fully_converted_rules
    )


def make_lambda(entity_hex: str, world: "WitnessWorld") -> Optional[CollectionRule]:
    """
    Lambdas are created in a for loop so values need to be captured
    """
    entity_req = world.player_logic.REQUIREMENTS_BY_HEX[entity_hex]

    return _meets_item_requirements(entity_req, world)


def set_rules(world: "WitnessWorld") -> None:
    """
    Sets all rules for all locations
    """

    for location in world.player_locations.CHECK_LOCATION_TABLE:
        real_location = location

        if location in world.player_locations.EVENT_LOCATION_TABLE:
            entity_hex = world.player_logic.EVENT_ITEM_PAIRS[location][1]
            real_location = static_witness_logic.ENTITIES_BY_HEX[entity_hex]["checkName"]

        associated_entity = world.player_logic.REFERENCE_LOGIC.ENTITIES_BY_NAME[real_location]
        entity_hex = associated_entity["entity_hex"]

        rule = make_lambda(entity_hex, world)
        if rule is None:
            continue

        location = world.get_location(location)

        set_rule(location, rule)

    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
