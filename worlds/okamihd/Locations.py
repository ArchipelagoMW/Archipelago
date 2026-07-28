from BaseClasses import Region, Location, ItemClassification, LocationProgressType
from rule_builder.rules import Rule, HasAny, Has, HasAll, And, Or
from .Enums.BrushTechniques import BrushTechniques
from .Enums.LocationType import LocationType
from .Rules import has_divine_instrument_tier, long_swim_rule, has_portable_fire_source
from .Types import LocData, OkamiLocation, OkamiItem, resolve_option_callable, EventData
from typing import TYPE_CHECKING, List
from .RegionsData import okami_locations, okami_events, okami_shop_locations

if TYPE_CHECKING:
    from . import OkamiWorld


def get_location_names():
    # ALL Locations are in this table, even events and shops
    location_names = {}
    for region_key, region_locations in okami_locations.items():
        for location_name, location_data in region_locations.items():
            location_names[location_name] = location_data.id
    for region_key, region_events in okami_events.items():
        for event_name, event_data in region_events.items():
            location_names[event_name] = event_data.id
    # Include all possible shop locations (they're conditionally created based on options)
    for region_key, region_shop_locations in okami_shop_locations.items():
        for location_name, location_data in region_shop_locations.items():
            location_names[location_name] = location_data.id
    return location_names


def create_region_locations(reg: Region, world: "OkamiWorld"):
    if reg.name in okami_locations:
        for (location_name, location_data) in okami_locations[reg.name].items():
            # if location_data.praise_sanity  <= world.options.PraiseSanity:
            create_location(location_name, location_data, reg, world)

    # Create shop locations if RandomizeShops is enabled
    if world.options.RandomizeShops and reg.name in okami_shop_locations:
        shop_slots = world.options.ShopSlots.value
        created_count = 0
        for (location_name, location_data) in okami_shop_locations[reg.name].items():
            if location_data.type == LocationType.SHOP and created_count < shop_slots:
                create_location(location_name, location_data, reg, world)
                created_count += 1


def create_location(location_name: str, location_data: EventData | LocData, reg: Region, world: "OkamiWorld"):
    location = OkamiLocation(world.player, location_name, location_data.id, reg)
    # Set location
    progress_type = resolve_option_callable(location_data.progress_type, world)
    location.progress_type = progress_type
    apply_event_or_location_rules(location, location_name, location_data, world)
    reg.locations.append(location)
    return location


def create_region_events(reg: Region, world: "OkamiWorld"):
    if reg.name in okami_events:
        for (event_name, event_data) in okami_events[reg.name].items():

            precollected_item_event_state = resolve_option_callable(event_data.precollected, world)

            is_event_item_state = resolve_option_callable(event_data.is_event_item, world)

            if not precollected_item_event_state and not is_event_item_state:
                # It's a true event, we need to create it as such.
                event_location = create_event(event_name,
                                              event_data.event_item_name if event_data.event_item_name else event_name,
                                              None, reg, event_data,
                                              world)

            elif is_event_item_state:
                create_location(event_name, event_data, reg, world)


def create_event(location_name: str, item_name: str, code: int | None, region: Region, data: LocData,
                 world: "OkamiWorld") -> Location:
    event = OkamiLocation(world.player, location_name, None, region)
    event.show_in_spoiler = False
    apply_event_or_location_rules(event, location_name, data, world)
    region.locations.append(event)
    event.place_locked_item(OkamiItem(item_name, ItemClassification.progression, code, world.player))
    return event


# Remember to update me when adding locations that aren't always randomized.
def get_total_locations(world: "OkamiWorld") -> int:
    location_count = 0
    event_item_location_count = 0
    for _, region_locations in okami_locations.items():
        location_count += len(region_locations)
    for region_key, region_events in okami_events.items():
        for _, event_data in region_events.items():
            if resolve_option_callable(event_data.is_event_item, world):
                location_count += 1
                event_item_location_count += 1
    # Count shop locations if RandomizeShops is enabled
    if world.options.RandomizeShops:
        shop_slots = world.options.ShopSlots.value
        num_shops = len(okami_shop_locations)  # Number of regions with shops
        location_count += num_shops * shop_slots
    return location_count


def get_unfilled_locations_count(world: "OkamiWorld"):
    count = 0
    count_events = 0
    count_excluded = 0
    for l in world.get_locations():
        if l.item is None and l.progress_type != LocationProgressType.EXCLUDED:
            count += 1
        elif l.item is not None:
            count_events += 1
        else:
            count_excluded += 1
    return count + count_excluded


def apply_event_or_location_rules(loc: Location, name: str, data: LocData | EventData, world: "OkamiWorld"):
    ## RULE BUILDER REWORK:
    # - FOR EACH LOCATION, BUILD AN ARRAY OF RULES THAT WILL BE ADDED TO THE world.set_rule(loc,AND(*Rules))

    debug_rule = False

    rules: List[Rule] = []

    required_techinques = []
    required_power_slash_level = data.power_slash_level
    required_cherry_bomb_level = data.cherry_bomb_level

    if len(data.mandatory_enemies) > 0:
        weapon_tier_required = 0
        for e in data.mandatory_enemies:
            weapon_tier_required = max(weapon_tier_required, e.value.required_weapon_tier)
            if e.value.defeat_condition is not None:
                rules.append(e.value.defeat_condition)

        if weapon_tier_required > 0:
            rules.append(has_divine_instrument_tier(weapon_tier_required))

    required_techinques += data.required_brush_techniques

    match data.type:
        case LocationType.TREASURE_BUD:
            required_techinques += [BrushTechniques.GREENSPROUT_BLOOM]
        case LocationType.BURIED_UNDER_LEAF_PILE:
            rules.append(HasAny(BrushTechniques.GALESTORM, BrushTechniques.WHIRLWIND,BrushTechniques.INFERNO,BrushTechniques.FIREBURST))
        case LocationType.BURIED_UNDER_LEAF_PILE_NO_FIRE_SOURCE:
            rules.append(Or(HasAny(BrushTechniques.GALESTORM,BrushTechniques.WHIRLWIND),has_portable_fire_source))
        case LocationType.BURIED_CHEST:
            if world.options.NightTimeChecksRequireCrescent:
                required_techinques += [BrushTechniques.CRESCENT]
        case LocationType.STONE_BURIED_CHEST:
            # Digging Champ Requirement
            rules.append(Has("Digging Champ"))
            if world.options.NightTimeChecksRequireCrescent:
                required_techinques += [BrushTechniques.CRESCENT]
        case LocationType.BURNING_CHEST:
            rules.append(HasAny(BrushTechniques.GALESTORM, BrushTechniques.WATERSPOUT, BrushTechniques.WHIRLWIND,
                                BrushTechniques.DELUGE))
        case LocationType.BURNING_CHEST_NO_WATER:
            rules.append(HasAny(BrushTechniques.GALESTORM, BrushTechniques.WHIRLWIND, BrushTechniques.DELUGE))
        case LocationType.UNDERWATER_CHEST:
            required_power_slash_level = max(required_power_slash_level, 1)
        case LocationType.UNDERWATER_CHEST_SHALLOW:
            rules.append(HasAny(BrushTechniques.POWER_SLASH, BrushTechniques.CHERRY_BOMB))
        case LocationType.DIGGING_MINIGAME_EARLY:
            required_power_slash_level = max(required_power_slash_level, 1)
            required_cherry_bomb_level = max(required_cherry_bomb_level, 1)
            required_techinques += [BrushTechniques.GREENSPROUT_BLOOM]
        case LocationType.DIGGING_MINIGAME_LATER:
            required_power_slash_level = max(required_power_slash_level, 1)
            required_cherry_bomb_level = max(required_cherry_bomb_level, 1)
            required_techinques += [BrushTechniques.GREENSPROUT_BLOOM, BrushTechniques.WATERSPOUT,
                                    BrushTechniques.GALESTORM]
        case LocationType.DIGGING_MINIGAME_HARD:
            required_power_slash_level = max(required_power_slash_level, 1)
            required_cherry_bomb_level = max(required_cherry_bomb_level, 1)
            required_techinques += [BrushTechniques.GREENSPROUT_BLOOM, BrushTechniques.WATERSPOUT,
                                    BrushTechniques.GALESTORM]
            rules.append(HasAll("Holy Eagle", "Golden Ink Pot"))
        case LocationType.FROZEN_CHEST:
            rules.append(HasAny(BrushTechniques.INFERNO, BrushTechniques.FIREBURST))
        case LocationType.FISHING_MINIGAME:
            required_power_slash_level = max(required_power_slash_level, 1)
        case LocationType.THUNDER_CHEST:
            rules.append(HasAny(BrushTechniques.THUNDERBOLT, BrushTechniques.THUNDERSTORM))

        case _:
            required_techinques += []

    if data.needs_long_swim:
        rules.append(long_swim_rule)

    if len(required_techinques) > 0:
        rules.append(HasAll(*required_techinques))

    if required_power_slash_level > 0:
        rules.append(Has(BrushTechniques.POWER_SLASH, count=required_power_slash_level))

    if required_cherry_bomb_level > 0:
        rules.append(Has(BrushTechniques.CHERRY_BOMB, count=required_cherry_bomb_level))

    if len(data.required_items_events) > 0:
        rules.append(HasAll(*data.required_items_events))

    if data.special_rule is not None:
        # Append special rule if it's defined
        rules.append(data.special_rule)

    # Set the location to require all concatenated rule
    if len(rules) > 0:
        final_rule = And(*rules)
        world.set_rule(loc, final_rule)
        if debug_rule:
            print("[Debug] - Rule for " + loc.name)
            print(final_rule)
