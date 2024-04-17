import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, List, Optional, Set, Tuple, Union

from BaseClasses import CollectionState, Item, Location, LocationProgressType

from .data import static_logic as static_witness_logic
from .data.utils import weighted_sample

if TYPE_CHECKING:
    from . import WitnessWorld

CompactItemData = Tuple[str, Union[str, int], int]


@dataclass
class WitnessLocationHint:
    location: Location
    hint_came_from_location: bool

    # If a hint gets added to a set twice, but once as an item hint and once as a location hint, those are the same
    def __hash__(self) -> int:
        return hash(self.location)

    def __eq__(self, other) -> bool:
        return self.location == other.location


@dataclass
class WitnessWordedHint:
    wording: str
    location: Optional[Location] = None
    area: Optional[str] = None
    area_amount: Optional[int] = None


def get_always_hint_items(world: "WitnessWorld") -> List[str]:
    always = [
        "Boat",
        "Caves Shortcuts",
        "Progressive Dots",
    ]

    difficulty = world.options.puzzle_randomization
    discards = world.options.shuffle_discarded_panels
    wincon = world.options.victory_condition

    if discards:
        if difficulty == "sigma_expert":
            always.append("Arrows")
        else:
            always.append("Triangles")

    if wincon == "elevator":
        always += ["Mountain Bottom Floor Pillars Room Entry (Door)", "Mountain Bottom Floor Doors"]

    if wincon == "challenge":
        always += ["Challenge Entry (Panel)", "Caves Panels"]

    return always


def get_always_hint_locations(world: "WitnessWorld") -> List[str]:
    always = [
        "Challenge Vault Box",
        "Mountain Bottom Floor Discard",
        "Theater Eclipse EP",
        "Shipwreck Couch EP",
        "Mountainside Cloud Cycle EP",
    ]

    # Add Obelisk Sides that contain EPs that are meant to be hinted, if they are necessary to complete the Obelisk Side
    if "0x339B6" not in world.player_logic.COMPLETELY_DISABLED_ENTITIES:
        always.append("Town Obelisk Side 6")  # Eclipse EP

    if "0x3388F" not in world.player_logic.COMPLETELY_DISABLED_ENTITIES:
        always.append("Treehouse Obelisk Side 4")  # Couch EP

    if "0x335AE" not in world.player_logic.COMPLETELY_DISABLED_ENTITIES:
        always.append("Mountainside Obelisk Side 1")  # Cloud Cycle EP.

    return always


def get_priority_hint_items(world: "WitnessWorld") -> List[str]:
    priority = {
        "Caves Mountain Shortcut (Door)",
        "Caves Swamp Shortcut (Door)",
        "Swamp Entry (Panel)",
        "Swamp Laser Shortcut (Door)",
    }

    if world.options.shuffle_symbols:
        symbols = [
            "Progressive Dots",
            "Progressive Stars",
            "Shapers",
            "Rotated Shapers",
            "Negative Shapers",
            "Arrows",
            "Triangles",
            "Eraser",
            "Black/White Squares",
            "Colored Squares",
            "Sound Dots",
            "Progressive Symmetry"
        ]

        priority.update(world.random.sample(symbols, 5))

    if world.options.shuffle_lasers:
        lasers = [
            "Symmetry Laser",
            "Town Laser",
            "Keep Laser",
            "Swamp Laser",
            "Treehouse Laser",
            "Monastery Laser",
            "Jungle Laser",
            "Quarry Laser",
            "Bunker Laser",
            "Shadows Laser",
        ]

        if world.options.shuffle_doors >= 2:
            priority.add("Desert Laser")
            priority.update(world.random.sample(lasers, 5))

        else:
            lasers.append("Desert Laser")
            priority.update(world.random.sample(lasers, 6))

    return sorted(priority)


def get_priority_hint_locations(world: "WitnessWorld") -> List[str]:
    priority = [
        "Tutorial Patio Floor",
        "Tutorial Patio Flowers EP",
        "Swamp Purple Underwater",
        "Shipwreck Vault Box",
        "Town RGB House Upstairs Left",
        "Town RGB House Upstairs Right",
        "Treehouse Green Bridge 7",
        "Treehouse Green Bridge Discard",
        "Shipwreck Discard",
        "Desert Vault Box",
        "Mountainside Vault Box",
        "Mountainside Discard",
        "Tunnels Theater Flowers EP",
        "Boat Shipwreck Green EP",
        "Quarry Stoneworks Control Room Left",
    ]

    # Add Obelisk Sides that contain EPs that are meant to be hinted, if they are necessary to complete the Obelisk Side
    if "0x33A20" not in world.player_logic.COMPLETELY_DISABLED_ENTITIES:
        priority.append("Town Obelisk Side 6")  # Theater Flowers EP

    if "0x28B29" not in world.player_logic.COMPLETELY_DISABLED_ENTITIES:
        priority.append("Treehouse Obelisk Side 4")  # Shipwreck Green EP

    if "0x33600" not in world.player_logic.COMPLETELY_DISABLED_ENTITIES:
        priority.append("Town Obelisk Side 2")  # Tutorial Patio Flowers EP.

    return priority


def word_direct_hint(world: "WitnessWorld", hint: WitnessLocationHint) -> WitnessWordedHint:
    location_name = hint.location.name
    if hint.location.player != world.player:
        location_name += " (" + world.multiworld.get_player_name(hint.location.player) + ")"

    item = hint.location.item
    item_name = item.name
    if item.player != world.player:
        item_name += " (" + world.multiworld.get_player_name(item.player) + ")"

    if hint.hint_came_from_location:
        hint_text = f"{location_name} contains {item_name}."
    else:
        hint_text = f"{item_name} can be found at {location_name}."

    return WitnessWordedHint(hint_text, hint.location)


def hint_from_item(world: "WitnessWorld", item_name: str, own_itempool: List[Item]) -> Optional[WitnessLocationHint]:

    locations = [item.location for item in own_itempool if item.name == item_name and item.location]

    if not locations:
        return None

    location_obj = world.random.choice(locations)
    location_name = location_obj.name

    if location_obj.player != world.player:
        location_name += " (" + world.multiworld.get_player_name(location_obj.player) + ")"

    return WitnessLocationHint(location_obj, False)


def hint_from_location(world: "WitnessWorld", location: str) -> Optional[WitnessLocationHint]:
    location_obj = world.get_location(location)
    item_obj = location_obj.item
    item_name = item_obj.name
    if item_obj.player != world.player:
        item_name += " (" + world.multiworld.get_player_name(item_obj.player) + ")"

    return WitnessLocationHint(location_obj, True)


def get_items_and_locations_in_random_order(world: "WitnessWorld",
                                            own_itempool: List[Item]) -> Tuple[List[str], List[str]]:
    prog_items_in_this_world = sorted(
        item.name for item in own_itempool
        if item.advancement and item.code and item.location
    )
    locations_in_this_world = sorted(
        location.name for location in world.multiworld.get_locations(world.player)
        if location.address and location.progress_type != LocationProgressType.EXCLUDED
    )

    world.random.shuffle(prog_items_in_this_world)
    world.random.shuffle(locations_in_this_world)

    return prog_items_in_this_world, locations_in_this_world


def make_always_and_priority_hints(world: "WitnessWorld", own_itempool: List[Item],
                                   already_hinted_locations: Set[Location]
                                   ) -> Tuple[List[WitnessLocationHint], List[WitnessLocationHint]]:
    prog_items_in_this_world, loc_in_this_world = get_items_and_locations_in_random_order(world, own_itempool)

    always_locations = [
        location for location in get_always_hint_locations(world)
        if location in loc_in_this_world
    ]
    always_items = [
        item for item in get_always_hint_items(world)
        if item in prog_items_in_this_world
    ]
    priority_locations = [
        location for location in get_priority_hint_locations(world)
        if location in loc_in_this_world
    ]
    priority_items = [
        item for item in get_priority_hint_items(world)
        if item in prog_items_in_this_world
    ]

    # Get always and priority location/item hints
    always_location_hints = {hint_from_location(world, location) for location in always_locations}
    always_item_hints = {hint_from_item(world, item, own_itempool) for item in always_items}
    priority_location_hints = {hint_from_location(world, location) for location in priority_locations}
    priority_item_hints = {hint_from_item(world, item, own_itempool) for item in priority_items}

    # Combine the sets. This will get rid of duplicates
    always_hints_set = always_item_hints | always_location_hints
    priority_hints_set = priority_item_hints | priority_location_hints

    # Make sure priority hints doesn't contain any hints that are already always hints.
    priority_hints_set -= always_hints_set

    always_generator = [hint for hint in always_hints_set if hint and hint.location not in already_hinted_locations]
    priority_generator = [hint for hint in priority_hints_set if hint and hint.location not in already_hinted_locations]

    # Convert both hint types to list and then shuffle. Also, get rid of None and Tutorial Gate Open.
    always_hints = sorted(always_generator, key=lambda h: h.location)
    priority_hints = sorted(priority_generator, key=lambda h: h.location)
    world.random.shuffle(always_hints)
    world.random.shuffle(priority_hints)

    return always_hints, priority_hints


def make_extra_location_hints(world: "WitnessWorld", hint_amount: int, own_itempool: List[Item],
                              already_hinted_locations: Set[Location], hints_to_use_first: List[WitnessLocationHint],
                              unhinted_locations_for_hinted_areas: Dict[str, Set[Location]]) -> List[WitnessWordedHint]:
    prog_items_in_this_world, locations_in_this_world = get_items_and_locations_in_random_order(world, own_itempool)

    next_random_hint_is_location = world.random.randrange(0, 2)

    hints = []

    # This is a way to reverse a Dict[a,List[b]] to a Dict[b,a]
    area_reverse_lookup = {
        unhinted_location: hinted_area
        for hinted_area, unhinted_locations in unhinted_locations_for_hinted_areas.items()
        for unhinted_location in unhinted_locations
    }

    while len(hints) < hint_amount:
        if not prog_items_in_this_world and not locations_in_this_world and not hints_to_use_first:
            player_name = world.multiworld.get_player_name(world.player)
            logging.warning(f"Ran out of items/locations to hint for player {player_name}.")
            break

        if hints_to_use_first:
            location_hint = hints_to_use_first.pop()
        elif next_random_hint_is_location and locations_in_this_world:
            location_hint = hint_from_location(world, locations_in_this_world.pop())
        elif not next_random_hint_is_location and prog_items_in_this_world:
            location_hint = hint_from_item(world, prog_items_in_this_world.pop(), own_itempool)
        # The list that the hint was supposed to be taken from was empty.
        # Try the other list, which has to still have something, as otherwise, all lists would be empty,
        # which would have triggered the guard condition above.
        else:
            next_random_hint_is_location = not next_random_hint_is_location
            continue

        if not location_hint or location_hint.location in already_hinted_locations:
            continue

        # Don't hint locations in areas that are almost fully hinted out already
        if location_hint.location in area_reverse_lookup:
            area = area_reverse_lookup[location_hint.location]
            if len(unhinted_locations_for_hinted_areas[area]) == 1:
                continue
            del area_reverse_lookup[location_hint.location]
            unhinted_locations_for_hinted_areas[area] -= {location_hint.location}

        hints.append(word_direct_hint(world, location_hint))
        already_hinted_locations.add(location_hint.location)

        next_random_hint_is_location = not next_random_hint_is_location

    return hints


def choose_areas(world: "WitnessWorld", amount: int, locations_per_area: Dict[str, List[Location]],
                 already_hinted_locations: Set[Location]) -> Tuple[List[str], Dict[str, Set[Location]]]:
    """
    Choose areas to hint.
    This takes into account that some areas may already have had items hinted in them through location hints.
    When this happens, they are made less likely to receive an area hint.
    """

    unhinted_locations_per_area = dict()
    unhinted_location_percentage_per_area = dict()

    for area_name, locations in locations_per_area.items():
        not_yet_hinted_locations = sum(location not in already_hinted_locations for location in locations)
        unhinted_locations_per_area[area_name] = {loc for loc in locations if loc not in already_hinted_locations}
        unhinted_location_percentage_per_area[area_name] = not_yet_hinted_locations / len(locations)

    items_per_area = {area_name: [location.item for location in locations]
                      for area_name, locations in locations_per_area.items()}

    areas = sorted(area for area in items_per_area if unhinted_location_percentage_per_area[area])
    weights = [unhinted_location_percentage_per_area[area] for area in areas]

    amount = min(amount, len(weights))

    hinted_areas = weighted_sample(world.random, areas, weights, amount)

    return hinted_areas, unhinted_locations_per_area


def get_hintable_areas(world: "WitnessWorld") -> Tuple[Dict[str, List[Location]], Dict[str, List[Item]]]:
    potential_areas = list(static_witness_logic.ALL_AREAS_BY_NAME.keys())

    locations_per_area = dict()
    items_per_area = dict()

    for area in potential_areas:
        regions = [
            world.player_regions.created_regions[region]
            for region in static_witness_logic.ALL_AREAS_BY_NAME[area]["regions"]
            if region in world.player_regions.created_regions
        ]
        locations = [location for region in regions for location in region.get_locations() if location.address]

        if locations:
            locations_per_area[area] = locations
            items_per_area[area] = [location.item for location in locations]

    return locations_per_area, items_per_area


def word_area_hint(world: "WitnessWorld", hinted_area: str, corresponding_items: List[Item]) -> Tuple[str, int]:
    """
    Word the hint for an area using natural sounding language.
    This takes into account how much progression there is, how much of it is local/non-local, and whether there are
    any local lasers to be found in this area.
    """

    local_progression = sum(item.player == world.player and item.advancement for item in corresponding_items)
    non_local_progression = sum(item.player != world.player and item.advancement for item in corresponding_items)

    laser_names = {"Symmetry Laser", "Desert Laser", "Quarry Laser", "Shadows Laser", "Town Laser", "Monastery Laser",
                   "Jungle Laser", "Bunker Laser", "Swamp Laser", "Treehouse Laser", "Keep Laser", }

    local_lasers = sum(
        item.player == world.player and item.name in laser_names
        for item in corresponding_items
    )

    total_progression = non_local_progression + local_progression

    player_count = world.multiworld.players

    area_progression_word = "Both" if total_progression == 2 else "All"

    if not total_progression:
        hint_string = f"In the {hinted_area} area, you will find no progression items."

    elif total_progression == 1:
        hint_string = f"In the {hinted_area} area, you will find 1 progression item."

        if player_count > 1:
            if local_lasers:
                hint_string += "\nThis item is a laser for this world."
            elif non_local_progression:
                other_player_str = "the other player" if player_count == 2 else "another player"
                hint_string += f"\nThis item is for {other_player_str}."
            else:
                hint_string += "\nThis item is for this world."
        else:
            if local_lasers:
                hint_string += "\nThis item is a laser."

    else:
        hint_string = f"In the {hinted_area} area, you will find {total_progression} progression items."

        if local_lasers == total_progression:
            sentence_end = (" for this world." if player_count > 1 else ".")
            hint_string += "\nAll of them are lasers" + sentence_end

        elif player_count > 1:
            if local_progression and non_local_progression:
                if non_local_progression == 1:
                    other_player_str = "the other player" if player_count == 2 else "another player"
                    hint_string += f"\nOne of them is for {other_player_str}."
                else:
                    other_player_str = "the other player" if player_count == 2 else "other players"
                    hint_string += f"\n{non_local_progression} of them are for {other_player_str}."
            elif non_local_progression:
                other_players_str = "the other player" if player_count == 2 else "other players"
                hint_string += f"\n{area_progression_word} of them are for {other_players_str}."
            elif local_progression:
                hint_string += f"\n{area_progression_word} of them are for this world."

            if local_lasers == 1:
                if not non_local_progression:
                    hint_string += "\nAlso, one of them is a laser."
                else:
                    hint_string += "\nAlso, one of them is a laser for this world."
            elif local_lasers:
                if not non_local_progression:
                    hint_string += f"\nAlso, {local_lasers} of them are lasers."
                else:
                    hint_string += f"\nAlso, {local_lasers} of them are lasers for this world."

        else:
            if local_lasers == 1:
                hint_string += "\nOne of them is a laser."
            elif local_lasers:
                hint_string += f"\n{local_lasers} of them are lasers."

    return hint_string, total_progression


def make_area_hints(world: "WitnessWorld", amount: int, already_hinted_locations: Set[Location]
                    ) -> Tuple[List[WitnessWordedHint], Dict[str, Set[Location]]]:
    locs_per_area, items_per_area = get_hintable_areas(world)

    hinted_areas, unhinted_locations_per_area = choose_areas(world, amount, locs_per_area, already_hinted_locations)

    hints = []

    for hinted_area in hinted_areas:
        hint_string, prog_amount = word_area_hint(world, hinted_area, items_per_area[hinted_area])

        hints.append(WitnessWordedHint(hint_string, None, f"hinted_area:{hinted_area}", prog_amount))

    if len(hinted_areas) < amount:
        player_name = world.multiworld.get_player_name(world.player)
        logging.warning(f"Was not able to make {amount} area hints for player {player_name}. "
                        f"Made {len(hinted_areas)} instead, and filled the rest with random location hints.")

    return hints, unhinted_locations_per_area


def create_all_hints(world: "WitnessWorld", hint_amount: int, area_hints: int,
                     already_hinted_locations: Set[Location]) -> List[WitnessWordedHint]:
    generated_hints: List[WitnessWordedHint] = []

    state = CollectionState(world.multiworld)

    # Keep track of already hinted locations. Consider early Tutorial as "already hinted"

    already_hinted_locations |= {
        loc for loc in world.multiworld.get_reachable_locations(state, world.player)
        if loc.address and static_witness_logic.ENTITIES_BY_NAME[loc.name]["area"]["name"] == "Tutorial (Inside)"
    }

    intended_location_hints = hint_amount - area_hints

    # First, make always and priority hints.

    always_hints, priority_hints = make_always_and_priority_hints(
        world, world.own_itempool, already_hinted_locations
    )

    generated_always_hints = len(always_hints)
    possible_priority_hints = len(priority_hints)

    # Make as many always hints as possible
    always_hints_to_use = min(intended_location_hints, generated_always_hints)

    # Make up to half of the rest of the location hints priority hints, using up to half of the possibly priority hints
    remaining_location_hints = intended_location_hints - always_hints_to_use
    priority_hints_to_use = int(max(0.0, min(possible_priority_hints / 2, remaining_location_hints / 2)))

    for _ in range(always_hints_to_use):
        location_hint = always_hints.pop()
        generated_hints.append(word_direct_hint(world, location_hint))
        already_hinted_locations.add(location_hint.location)

    for _ in range(priority_hints_to_use):
        location_hint = priority_hints.pop()
        generated_hints.append(word_direct_hint(world, location_hint))
        already_hinted_locations.add(location_hint.location)

    location_hints_created_in_round_1 = len(generated_hints)

    unhinted_locations_per_area: Dict[str, Set[Location]] = dict()

    # Then, make area hints.
    if area_hints:
        generated_area_hints, unhinted_locations_per_area = make_area_hints(world, area_hints, already_hinted_locations)
        generated_hints += generated_area_hints

    # If we don't have enough hints yet, recalculate always and priority hints, then fill with random hints
    if len(generated_hints) < hint_amount:
        remaining_needed_location_hints = hint_amount - len(generated_hints)

        # Save old values for used always and priority hints for later calculations
        amt_of_used_always_hints = always_hints_to_use
        amt_of_used_priority_hints = priority_hints_to_use

        # Recalculate how many always hints and priority hints are supposed to be used
        intended_location_hints = remaining_needed_location_hints + location_hints_created_in_round_1

        always_hints_to_use = min(intended_location_hints, generated_always_hints)
        priority_hints_to_use = int(max(0.0, min(possible_priority_hints / 2, remaining_location_hints / 2)))

        # If we now need more always hints and priority hints than we thought previously, make some more.
        more_always_hints = always_hints_to_use - amt_of_used_always_hints
        more_priority_hints = priority_hints_to_use - amt_of_used_priority_hints

        extra_always_and_priority_hints: List[WitnessLocationHint] = []

        for _ in range(more_always_hints):
            extra_always_and_priority_hints.append(always_hints.pop())

        for _ in range(more_priority_hints):
            extra_always_and_priority_hints.append(priority_hints.pop())

        generated_hints += make_extra_location_hints(
            world, hint_amount - len(generated_hints), world.own_itempool, already_hinted_locations,
            extra_always_and_priority_hints, unhinted_locations_per_area
        )

    # If we still don't have enough for whatever reason, throw a warning, proceed with the lower amount
    if len(generated_hints) != hint_amount:
        player_name = world.multiworld.get_player_name(world.player)
        logging.warning(f"Couldn't generate {hint_amount} hints for player {player_name}. "
                        f"Generated {len(generated_hints)} instead.")

    return generated_hints


def make_compact_hint_data(hint: WitnessWordedHint, local_player_number: int) -> CompactItemData:
    location = hint.location
    area_amount = hint.area_amount

    # None if junk hint, address if location hint, area string if area hint
    arg_1 = location.address if location else (hint.area if hint.area else None)

    # self.player if junk hint, player if location hint, progression amount if area hint
    arg_2 = area_amount if area_amount is not None else (location.player if location else local_player_number)

    return hint.wording, arg_1, arg_2


def make_laser_hints(world: "WitnessWorld", laser_names: List[str]) -> Dict[str, WitnessWordedHint]:
    laser_hints_by_name = dict()

    for item_name in laser_names:
        location_hint = hint_from_item(world, item_name, world.own_itempool)
        if not location_hint:
            continue

        laser_hints_by_name[item_name] = word_direct_hint(world, location_hint)

    return laser_hints_by_name
