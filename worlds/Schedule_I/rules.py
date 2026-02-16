from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Dict, Any, Union

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule

if TYPE_CHECKING:
    from .world import Schedule1World


def set_all_rules(world: Schedule1World, locationData, regionData, victoryData) -> None:
    # In order for AP to generate an item layout that is actually possible for the player to complete,
    # we need to define rules for our Entrances and Locations.
    # Note: Regions do not have rules, the Entrances connecting them do!
    # We'll do entrances first, then locations, and then finally we set our victory condition.

    set_all_entrance_rules(world, regionData)
    set_all_location_rules(world, locationData)
    set_completion_condition(world, victoryData)


def check_option_enabled(world: Schedule1World, option_name: str) -> bool:
    """Check if an option is enabled based on option name string from JSON."""
    option_map = {
        "randomize_customers": world.options.randomize_customers,
        "randomize_dealers": world.options.randomize_dealers,
        "randomize_suppliers": world.options.randomize_suppliers,
        "randomize_level_unlocks": world.options.randomize_level_unlocks,
        "randomize_cartel_influence": world.options.randomize_cartel_influence,
        "randomize_business_properties": world.options.randomize_business_properties,
        "randomize_drug_making_properties": world.options.randomize_drug_making_properties,
    }
    return bool(option_map.get(option_name, False))


def check_option_condition(world: Schedule1World, condition_key: str) -> bool:
    """
    Parse and evaluate a compound option condition string.
    
    Supports:
    - Simple: "randomize_level_unlocks" (option must be true)
    - Negation: "!randomize_level_unlocks" (option must be false)
    - Compound AND: "randomize_level_unlocks&!randomize_customers" 
      (first must be true AND second must be false)
    
    Returns True if the condition is satisfied, False otherwise.
    """
    # Split by '&' to get individual conditions
    parts = condition_key.split('&')
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        
        # Check for negation prefix
        if part.startswith('!'):
            option_name = part[1:]
            expected_value = False
        else:
            option_name = part
            expected_value = True
        
        # Get the actual option value
        actual_value = check_option_enabled(world, option_name)
        
        # If this part doesn't match expected, the whole condition fails
        if actual_value != expected_value:
            return False
    
    return True


def build_requirement_check(world: Schedule1World, method_name: str, value: Any) -> Callable[[CollectionState], bool]:
    """Build a requirement check function based on the method name and value from JSON."""
    
    if method_name == "has":
        # value is a single item name string
        return lambda state, v=value: state.has(v, world.player)
    
    elif method_name == "has_any":
        # value is a list of lists, e.g. [["Item1", "Item2"]]
        # We take the first list as the items to check
        items = value[0] if isinstance(value[0], list) else value
        return lambda state, v=items: state.has_any(v, world.player)
    
    elif method_name == "has_all":
        # value is a list of item names
        return lambda state, v=value: state.has_all(v, world.player)
    
    elif method_name == "has_all_counts":
        # value is a dict of {item_name: count}
        return lambda state, v=value: state.has_all_counts(v, world.player)
    
    elif method_name == "has_from_list":
        # value can be:
        # - A single dict: {item_name: count, ...} where all counts are the same
        # - A list of dicts: [{item_name: count, ...}, ...] for multiple tiers
        # For a list, we build checks for each dict and require all to pass
        if isinstance(value, list):
            # List of dicts - build a check for each dict
            checks = []
            for tier_dict in value:
                keys = list(tier_dict.keys())
                count = list(tier_dict.values())[0]  # All values in a tier should be the same
                checks.append((keys, count))
            return lambda state, c=checks: all(
                state.has_from_list(keys, world.player, count) for keys, count in c
            )
        else:
            # Single dict
            keys = list(value.keys())
            count = list(value.values())[0]  # All values should be the same count
            return lambda state, k=keys, c=count: state.has_from_list(k, world.player, c)
    
    # Default: always true
    return lambda state: True


def build_rule_from_requirements(world: Schedule1World, requirements: Union[bool, Dict[str, Any]], use_or_logic: bool = False) -> Callable[[CollectionState], bool]:
    """
    Build a rule function from the requirements structure.
    
    requirements can be:
    - True (always accessible)
    - A dict with option conditions as keys
    
    use_or_logic: If True, only ONE condition needs to be satisfied (for Customer/Dealer/Supplier tags)
                  If False, ALL applicable conditions must be satisfied
    """
    if requirements is True:
        return lambda state: True
    
    if not isinstance(requirements, dict):
        return lambda state: True
    
    # Build list of (option_name, checks) pairs
    condition_checks: list[tuple[str, list[Callable[[CollectionState], bool]]]] = []
    
    for option_name, checks in requirements.items():
        if not isinstance(checks, dict):
            continue
        
        check_functions = []
        for method_name, value in checks.items():
            check_func = build_requirement_check(world, method_name, value)
            check_functions.append(check_func)
        
        if check_functions:
            condition_checks.append((option_name, check_functions))
    
    if not condition_checks:
        return lambda state: True
    
    def rule_function(state: CollectionState) -> bool:
        results = []
        
        for condition_key, check_functions in condition_checks:
            if check_option_condition(world, condition_key):
                # This option condition is satisfied, so its checks matter
                # All checks within this condition must pass
                option_result = all(check(state) for check in check_functions)
                results.append(option_result)
        
        if not results:
            # No applicable options enabled - rule passes
            return True
        
        if use_or_logic:
            # For Customer/Dealer/Supplier: only one needs to pass
            return any(results)
        else:
            # For all others: all must pass
            return all(results)
    
    return rule_function


def set_all_entrance_rules(world: Schedule1World, regionData) -> None:
    """Set entrance rules based on region connection requirements from regions.json."""
    
    # Load all entrances into a dictionary once
    entrances_dict: Dict[str, Any] = {}
    
    for region_name, region_info in regionData.regions.items():
        for connected_region_name, requirements in region_info.connections.items():
            entrance_name = f"{region_name} to {connected_region_name}"
            try:
                entrances_dict[entrance_name] = world.get_entrance(entrance_name)
            except KeyError:
                # Entrance might not exist if region wasn't created
                continue
    
    # Set rules for each entrance
    for region_name, region_info in regionData.regions.items():
        for connected_region_name, requirements in region_info.connections.items():
            entrance_name = f"{region_name} to {connected_region_name}"
            
            if entrance_name not in entrances_dict:
                continue
            
            entrance = entrances_dict[entrance_name]
            rule = build_rule_from_requirements(world, requirements, use_or_logic=False)
            set_rule(entrance, rule)


def set_all_location_rules(world: Schedule1World, locationData) -> None:
    """Set location rules based on requirements from locations.json."""
    
    # Build a dict of location name -> location object for locations that exist
    locations_dict: Dict[str, Any] = {}
    
    for loc_name, loc_data in locationData.locations.items():
        # Skip supplier locations if randomize_suppliers is enabled (they don't exist)
        if world.options.randomize_suppliers and "Supplier" in loc_data.tags:
            continue
        
        try:
            locations_dict[loc_name] = world.get_location(loc_name)
        except KeyError:
            # Location might not exist
            continue
    
    # Set rules for each location
    for loc_name, loc_data in locationData.locations.items():
        if loc_name not in locations_dict:
            continue
        
        location = locations_dict[loc_name]
        requirements = loc_data.requirements
        
        # Determine if this location uses OR logic (Customer, Dealer, or Supplier tags)
        tags = loc_data.tags
        use_or_logic = any(tag in tags for tag in ["Customer", "Dealer", "Supplier"])
        
        rule = build_rule_from_requirements(world, requirements, use_or_logic=use_or_logic)
        set_rule(location, rule)


def set_completion_condition(world: Schedule1World, victoryData) -> None:
    # Victory conditions are loaded from victory.json
    # > 0 means cartel is necessary, and we need to check all applicable conditions
    if world.options.goal > 0:
        # Build the victory rule from the requirements in victory.json
        # All applicable option conditions must pass (AND logic)
        rule = build_rule_from_requirements(world, victoryData.requirements, use_or_logic=False)
        world.multiworld.completion_condition[world.player] = rule
    else:
        # Otherwise, money is farmable no matter what.
        world.multiworld.completion_condition[world.player] = lambda state: True