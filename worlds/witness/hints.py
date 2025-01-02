import logging
import math
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, Tuple, Union, cast

from BaseClasses import CollectionState, Item, Location, MultiWorld, Region

from .data import static_logic as static_witness_logic
from .data.utils import weighted_sample
from .player_items import WitnessItem

if TYPE_CHECKING:
    from . import WitnessWorld

CompactHintArgs = Tuple[Union[str, int], Union[str, int]]
CompactHintData = Tuple[str, Union[str, int], Union[str, int]]


@dataclass
class WitnessLocationHint:
    location: Location
    hint_came_from_location: bool

    # If a hint gets added to a set twice, but once as an item hint and once as a location hint, those are the same
    def __hash__(self) -> int:
        return hash(self.location)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, WitnessLocationHint):
            return False
        return self.location == other.location


@dataclass
class WitnessWordedHint:
    wording: str
    location: Optional[Location] = None
    area: Optional[str] = None
    area_amount: Optional[int] = None
    area_hunt_panels: Optional[int] = None
    vague_location_hint: bool = False


def get_always_hint_items(world: "WitnessWorld") -> List[str]:
    always = world.options.always_hint_items.value.copy()

    difficulty = world.options.puzzle_randomization
    discards = world.options.shuffle_discarded_panels
    wincon = world.options.victory_condition

    if discards and world.options.discard_symbol_hint == "always_hint":
        if difficulty in ("sigma_expert", "umbra_variety"):
            always.add("Arrows")
        if difficulty in ("none", "sigma_normal", "umbra_variety"):
            always.add("Triangles")

    if world.options.final_door_hint == "priority_hint":
        if wincon == "elevator":
            always |= {"Mountain Bottom Floor Pillars Room Entry (Door)", "Mountain Bottom Floor Doors"}

        if wincon == "challenge":
            always |= {"Challenge Entry (Panel)", "Caves Panels", "Challenge Entry (Door)", "Caves Doors"}

    return sorted(always)


def get_always_hint_locations(world: "WitnessWorld") -> List[str]:
    always = sorted(world.options.always_hint_locations.value)

    # For EPs, also make their obelisk side an always hint
    for location_name in always:
        location_obj = static_witness_logic.ENTITIES_BY_NAME[location_name]
        if location_obj["entityType"] != "EP":
            continue
        if location_obj["entity_hex"] in world.player_logic.COMPLETELY_DISABLED_ENTITIES:
            continue

        corresponding_obelisk_side = static_witness_logic.EP_TO_OBELISK_SIDE[location_obj["entity_hex"]]
        always.append(static_witness_logic.ENTITIES_BY_ID[corresponding_obelisk_side]["checkName"])

    return always


def get_priority_hint_items(world: "WitnessWorld") -> List[str]:
    priority = world.options.priority_hint_items.value.copy()

    difficulty = world.options.puzzle_randomization
    discards = world.options.shuffle_discarded_panels
    wincon = world.options.victory_condition

    existing_items_lookup = {item.name for item in world.own_itempool}

    if discards and world.options.discard_symbol_hint == "always_hint":
        if difficulty in ("sigma_expert", "umbra_variety"):
            priority.add("Arrows")
        if difficulty in ("none", "sigma_normal", "umbra_variety"):
            priority.add("Triangles")

    if world.options.final_door_hint == "priority_hint":
        if wincon == "elevator":
            priority |= {"Mountain Bottom Floor Pillars Room Entry (Door)", "Mountain Bottom Floor Doors"}

        if wincon == "challenge":
            priority |= {"Challenge Entry (Panel)", "Caves Panels", "Challenge Entry (Door)", "Caves Doors"}

    # Add symbols and lasers in accordance with Priority Symbols and Priority Lasers options

    number_of_symbols = sum(item in world.item_name_groups["Symbols"] for item in priority)
    number_of_lasers = sum(item in world.item_name_groups["Lasers"] for item in priority)

    needed_symbols = world.options.priority_symbols - number_of_symbols
    needed_lasers = world.options.priority_lasers - number_of_lasers

    possible_symbols = sorted(world.item_name_groups["Symbols"] & existing_items_lookup - priority)
    possible_lasers = sorted(world.item_name_groups["Lasers"] & existing_items_lookup - priority)

    if needed_symbols > 0:
        priority.update(world.random.sample(possible_symbols, min(len(possible_symbols), needed_symbols)))

    if needed_lasers > 0:
        priority.update(world.random.sample(possible_lasers, min(len(possible_lasers), needed_lasers)))

    return sorted(priority)


def get_priority_hint_locations(world: "WitnessWorld") -> List[str]:
    priority = sorted(world.options.priority_hint_locations.value)

    # For EPs, also make their obelisk side a priority hint
    for location_name in priority:
        location_obj = static_witness_logic.ENTITIES_BY_NAME[location_name]
        if location_obj["entityType"] != "EP":
            continue
        if location_obj["entity_hex"] in world.player_logic.COMPLETELY_DISABLED_ENTITIES:
            continue

        corresponding_obelisk_side = static_witness_logic.EP_TO_OBELISK_SIDE[location_obj["entity_hex"]]
        priority.append(static_witness_logic.ENTITIES_BY_ID[corresponding_obelisk_side]["checkName"])

    return priority


def try_getting_location_group_for_location(world: "WitnessWorld", hint_loc: Location) -> Tuple[str, str]:
    allow_regions = world.options.vague_hints == "experimental"
    containing_world = world.multiworld.worlds[hint_loc.player]

    possible_location_groups = {
        group_name: group_locations
        for group_name, group_locations in containing_world.location_name_groups.items()
        if hint_loc.name in group_locations
    }

    locations_in_that_world = {
        location.name for location in world.multiworld.get_locations(hint_loc.player) if not location.is_event
    }

    valid_location_groups: Dict[str, int] = {}

    # Find valid location groups.
    for group, locations in possible_location_groups.items():
        if group == "Everywhere":
            continue
        present_locations = sum(location in locations_in_that_world for location in locations)
        valid_location_groups[group] = present_locations

    # If there are valid location groups, use a random one.
    if valid_location_groups:
        # If there are location groups with more than 1 location, remove any that only have 1.
        if any(num_locs > 1 for num_locs in valid_location_groups.values()):
            valid_location_groups = {name: num_locs for name, num_locs in valid_location_groups.items() if num_locs > 1}

        location_groups_with_weights = {
            # Listen. Just don't worry about it. :)))
            location_group: (x ** 0.6) * math.e ** (- (x / 7) ** 0.6) if x > 6 else x / 6
            for location_group, x in valid_location_groups.items()
        }

        logging.debug(
            f"Eligible location groups for location "
            f'"{hint_loc}" ({containing_world.game}): {location_groups_with_weights}.'
        )

        location_groups = list(location_groups_with_weights.keys())
        weights = list(location_groups_with_weights.values())

        return world.random.choices(location_groups, weights, k=1)[0], "Group"

    logging.debug(
        f"Couldn't find suitable location group for location \"{hint_loc}\" ({containing_world.game})."
    )
    if allow_regions:
        logging.debug(f'Falling back on parent region "{hint_loc.parent_region}".')
        return cast(Region, hint_loc.parent_region).name, "Region"

    logging.debug('Falling back on hinting the "Everywhere" group.')
    return "Everywhere", "Everywhere"


def word_direct_hint(world: "WitnessWorld", hint: WitnessLocationHint) -> WitnessWordedHint:
    location_name = hint.location.name
    if hint.location.player != world.player:
        location_name += " (" + world.multiworld.get_player_name(hint.location.player) + ")"

    item = hint.location.item

    item_name = "Nothing"
    if item is not None:
        item_name = item.name

        if item.player != world.player:
            item_name += " (" + world.multiworld.get_player_name(item.player) + ")"

    hint_text = ""
    area: Optional[str] = None

    if world.options.vague_hints:
        chosen_group, group_type = try_getting_location_group_for_location(world, hint.location)

        logging.debug(
            f'Vague hints: Chose group "{chosen_group}" of type "{group_type}" for location "{hint.location}".'
        )

        if hint.location.player == world.player:
            area = chosen_group

            # local locations should only ever return a location group, as Witness defines groups for every location.
            hint_text = f"{item_name} can be found in the {area} area."
        else:
            player_name = world.multiworld.get_player_name(hint.location.player)

            if group_type == "Everywhere":
                location_name = f"a location in {player_name}'s world"
            elif group_type == "Group":
                location_name = f"a \"{chosen_group}\" location in {player_name}'s world"
            elif group_type == "Region":
                origin_region_name = world.multiworld.worlds[hint.location.player].origin_region_name
                if chosen_group == origin_region_name:
                    location_name = (
                        f"a location in the origin region of {player_name}'s world (\"{origin_region_name}\" region)"
                    )
                else:
                    location_name = f"a location in {player_name}'s \"{chosen_group}\" region"

    if hint_text == "":
        if hint.hint_came_from_location:
            hint_text = f"{location_name} contains {item_name}."
        else:
            hint_text = f"{item_name} can be found at {location_name}."

    return WitnessWordedHint(hint_text, hint.location, area=area, vague_location_hint=bool(world.options.vague_hints))


def hint_from_item(world: "WitnessWorld", item_name: str,
                   own_itempool: List["WitnessItem"]) -> Optional[WitnessLocationHint]:
    def get_real_location(multiworld: MultiWorld, location: Location) -> Location:
        """If this location is from an item_link pseudo-world, get the location that the item_link item is on.
        Return the original location otherwise / as a fallback."""
        if location.player not in world.multiworld.groups:
            return location

        try:
            if not location.item:
                return location
            return multiworld.find_item(location.item.name, location.player)
        except StopIteration:
            return location

    locations = [
        get_real_location(world.multiworld, item.location)
        for item in own_itempool if item.name == item_name and item.location
    ]

    if not locations:
        return None

    location_obj = world.random.choice(locations)

    return WitnessLocationHint(location_obj, False)


def hint_from_location(world: "WitnessWorld", location: str) -> Optional[WitnessLocationHint]:
    return WitnessLocationHint(world.get_location(location), True)


def get_item_and_location_names_in_random_order(world: "WitnessWorld",
                                                own_itempool: List["WitnessItem"]) -> Tuple[List[str], List[str]]:
    progression_item_names_in_this_world = [
        item.name for item in own_itempool
        if item.advancement and item.code and item.location
    ]
    world.random.shuffle(progression_item_names_in_this_world)

    locations_in_this_world = [
        location for location in world.multiworld.get_locations(world.player)
        if location.item and not location.is_event
    ]
    world.random.shuffle(locations_in_this_world)

    if world.options.vague_hints:
        locations_in_this_world.sort(key=lambda location: cast(Item, location.item).advancement)

    location_names_in_this_world = [location.name for location in locations_in_this_world]

    return progression_item_names_in_this_world, location_names_in_this_world


def make_always_and_priority_hints(world: "WitnessWorld", own_itempool: List["WitnessItem"],
                                   already_hinted_locations: Set[Location]
                                   ) -> Tuple[List[WitnessLocationHint], List[WitnessLocationHint]]:

    progression_items_in_this_world, locations_in_this_world = get_item_and_location_names_in_random_order(
        world, own_itempool
    )

    always_items = [
        item for item in get_always_hint_items(world)
        if item in progression_items_in_this_world
    ]
    priority_items = [
        item for item in get_priority_hint_items(world)
        if item in progression_items_in_this_world
    ]

    logging.debug(f"Always item hints: {always_items}")
    logging.debug(f"Priority item hints: {priority_items}")

    if world.options.vague_hints:
        always_locations, priority_locations = [], []

        logging.debug("No always / priority location hints because this world wants vague hints.")
    else:
        always_locations = [
            location for location in get_always_hint_locations(world)
            if location in locations_in_this_world
        ]
        priority_locations = [
            location for location in get_priority_hint_locations(world)
            if location in locations_in_this_world
        ]

        logging.debug(f"Always location hints: {always_locations}")
        logging.debug(f"Priority location hints: {priority_locations}")

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

    logging.debug(
        f"Finalized always hints: "
        f"{[f'{hint.location.item} on {hint.location}' for hint in always_hints]}"
    )
    logging.debug(
        f"Finalized priority hint candidates: "
        f"{[f'{hint.location.item} on {hint.location}' for hint in priority_hints]}"
    )

    return always_hints, priority_hints


def make_extra_location_hints(world: "WitnessWorld", hint_amount: int, own_itempool: List["WitnessItem"],
                              already_hinted_locations: Set[Location], hints_to_use_first: List[WitnessLocationHint],
                              unhinted_locations_for_hinted_areas: Dict[str, Set[Location]]) -> List[WitnessWordedHint]:
    progression_items_in_this_world, locations_in_this_world = get_item_and_location_names_in_random_order(
        world, own_itempool
    )

    next_random_hint_is_location = world.random.randrange(0, 100) >= world.options.random_hints_are_items_weight

    hints: List[WitnessWordedHint] = []

    # This is a way to reverse a Dict[a,List[b]] to a Dict[b,a]
    area_reverse_lookup = {
        unhinted_location: hinted_area
        for hinted_area, unhinted_locations in unhinted_locations_for_hinted_areas.items()
        for unhinted_location in unhinted_locations
    }

    while len(hints) < hint_amount:
        if not progression_items_in_this_world and not locations_in_this_world and not hints_to_use_first:
            logging.warning(f"Ran out of items/locations to hint for player {world.player_name}.")
            break

        location_hint: Optional[WitnessLocationHint]
        if hints_to_use_first:
            location_hint = hints_to_use_first.pop()
        elif next_random_hint_is_location and locations_in_this_world:
            location_hint = hint_from_location(world, locations_in_this_world.pop())
        elif not next_random_hint_is_location and progression_items_in_this_world:
            location_hint = hint_from_item(world, progression_items_in_this_world.pop(), own_itempool)
        # The list that the hint was supposed to be taken from was empty.
        # Try the other list, which has to still have something, as otherwise, all lists would be empty,
        # which would have triggered the guard condition above.
        else:
            next_random_hint_is_location = not next_random_hint_is_location
            continue

        if location_hint is None or location_hint.location in already_hinted_locations:
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

    logging.debug(
        f"Remaining hints: "
        f"{[f'{hint.location.item} on {hint.location}' for hint in hints]}"
    )

    return hints


def choose_areas(world: "WitnessWorld", amount: int, locations_per_area: Dict[str, List[Location]],
                 already_hinted_locations: Set[Location]) -> Tuple[List[str], Dict[str, Set[Location]]]:
    """
    Choose areas to hint.
    This takes into account that some areas may already have had items hinted in them through location hints.
    When this happens, they are made less likely to receive an area hint.
    """

    unhinted_locations_per_area = {}
    unhinted_location_percentage_per_area = {}

    for area_name, locations in locations_per_area.items():
        not_yet_hinted_locations = sum(location not in already_hinted_locations for location in locations)
        unhinted_locations_per_area[area_name] = {loc for loc in locations if loc not in already_hinted_locations}
        unhinted_location_percentage_per_area[area_name] = not_yet_hinted_locations / len(locations)

    items_per_area = {area_name: [location.item for location in locations]
                      for area_name, locations in locations_per_area.items()}

    areas = sorted(area for area in items_per_area if unhinted_location_percentage_per_area[area])
    weights = [unhinted_location_percentage_per_area[area] for area in areas]

    logging.debug(f"Area weights: {unhinted_location_percentage_per_area}")

    amount = min(amount, len(weights))

    hinted_areas = weighted_sample(world.random, areas, weights, amount)

    logging.debug(f"Chosen area hints ({len(hinted_areas)}): {hinted_areas}")

    return hinted_areas, unhinted_locations_per_area


def get_hintable_areas(world: "WitnessWorld") -> Tuple[Dict[str, List[Location]], Dict[str, List[Item]]]:
    potential_areas = list(static_witness_logic.ALL_AREAS_BY_NAME.keys())

    locations_per_area = {}
    items_per_area = {}

    for area in potential_areas:
        regions = [
            world.get_region(region)
            for region in static_witness_logic.ALL_AREAS_BY_NAME[area]["regions"]
            if region in world.player_regions.created_region_names
        ]
        locations = [location for region in regions for location in region.get_locations() if not location.is_event]

        if locations:
            locations_per_area[area] = locations
            items_per_area[area] = [location.item for location in locations]

    return locations_per_area, items_per_area


def word_area_hint(world: "WitnessWorld", hinted_area: str, area_items: List[Item]) -> Tuple[str, int, Optional[int]]:
    """
    Word the hint for an area using natural sounding language.
    This takes into account how much progression there is, how much of it is local/non-local, and whether there are
    any local lasers to be found in this area.
    """

    local_progression = sum(item.player == world.player and item.advancement for item in area_items)
    non_local_progression = sum(item.player != world.player and item.advancement for item in area_items)

    laser_names = {"Symmetry Laser", "Desert Laser", "Quarry Laser", "Shadows Laser", "Town Laser", "Monastery Laser",
                   "Jungle Laser", "Bunker Laser", "Swamp Laser", "Treehouse Laser", "Keep Laser", }

    local_lasers = sum(
        item.player == world.player and item.name in laser_names
        for item in area_items
    )

    total_progression = non_local_progression + local_progression

    player_count = world.multiworld.players

    area_progression_word = "Both" if total_progression == 2 else "All"

    hint_string = f"In the {hinted_area} area, you will find "

    hunt_panels = None
    if world.options.victory_condition == "panel_hunt":
        hunt_panels = sum(
            static_witness_logic.ENTITIES_BY_HEX[hunt_entity]["area"]["name"] == hinted_area
            for hunt_entity in world.player_logic.HUNT_ENTITIES
        )

        if not hunt_panels:
            hint_string += "no Hunt Panels and "

        elif hunt_panels == 1:
            hint_string += "1 Hunt Panel and "

        else:
            hint_string += f"{hunt_panels} Hunt Panels and "

    if not total_progression:
        hint_string += "no progression items."

    elif total_progression == 1:
        hint_string += "1 progression item."

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
        hint_string += f"{total_progression} progression items."

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

    logging.debug(f'Wording area hint for {hinted_area} as: "{hint_string}"')

    return hint_string, total_progression, hunt_panels


def make_area_hints(world: "WitnessWorld", amount: int, already_hinted_locations: Set[Location]
                    ) -> Tuple[List[WitnessWordedHint], Dict[str, Set[Location]]]:
    locs_per_area, items_per_area = get_hintable_areas(world)

    hinted_areas, unhinted_locations_per_area = choose_areas(world, amount, locs_per_area, already_hinted_locations)

    hints = []

    for hinted_area in hinted_areas:
        hint_string, progression_amount, hunt_panels = word_area_hint(world, hinted_area, items_per_area[hinted_area])

        hints.append(
            WitnessWordedHint(hint_string, None, f"hinted_area:{hinted_area}", progression_amount, hunt_panels)
        )

    if len(hinted_areas) < amount:
        logging.warning(f"Was not able to make {amount} area hints for player {world.player_name}. "
                        f"Made {len(hinted_areas)} instead, and filled the rest with random location hints.")

    return hints, unhinted_locations_per_area


def create_all_hints(world: "WitnessWorld", hint_amount: int, area_hints: int,
                     already_hinted_locations: Set[Location]) -> List[WitnessWordedHint]:
    start_line = f"Witness hints: {world.player_name} start"
    dashes = "-" * len(start_line)
    logging.debug(f"{dashes}\n{start_line}\n{dashes}")

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

    priority_cap_possible = possible_priority_hints * world.options.priority_hints_percentage_out_of_possible / 100
    priority_cap_remain = remaining_location_hints * world.options.priority_hints_percentage_out_of_remaining / 100

    priority_hints_to_use = int(max(0.0, min(priority_cap_possible, priority_cap_remain)))

    amount_of_priority_hint_candidates = len(priority_hints)

    logging.debug(
        f"Using {priority_hints_to_use} priority out of {amount_of_priority_hint_candidates} candidates. "
        f"This is the floor of the lower number out of\n"
        f"1. {world.options.priority_hints_percentage_out_of_possible}% of {possible_priority_hints} "
        f"possible priority hints, which is {priority_cap_possible}.\n"
        f"2. {world.options.priority_hints_percentage_out_of_remaining}% of {remaining_location_hints} "
        f"remaining hint slots after area and always hints, which is {priority_cap_remain}."
    )

    for _ in range(always_hints_to_use):
        location_hint = always_hints.pop()
        generated_hints.append(word_direct_hint(world, location_hint))
        already_hinted_locations.add(location_hint.location)

    for _ in range(priority_hints_to_use):
        location_hint = priority_hints.pop()
        generated_hints.append(word_direct_hint(world, location_hint))
        already_hinted_locations.add(location_hint.location)

    location_hints_created_in_round_1 = len(generated_hints)

    unhinted_locations_per_area: Dict[str, Set[Location]] = {}

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
        remaining_location_hints = intended_location_hints - always_hints_to_use

        priority_cap_possible = possible_priority_hints * world.options.priority_hints_percentage_out_of_possible / 100
        priority_cap_remain = remaining_location_hints * world.options.priority_hints_percentage_out_of_remaining / 100

        priority_hints_to_use = int(max(0.0, min(priority_cap_possible, priority_cap_remain)))

        # If we now need more always hints and priority hints than we thought previously, make some more.
        more_always_hints = always_hints_to_use - amt_of_used_always_hints
        more_priority_hints = priority_hints_to_use - amt_of_used_priority_hints

        if more_always_hints or more_priority_hints:
            logging.debug(
                f"Reusing always and priority hints as fallback after not enough area hints could be made. "
                f"There are {remaining_needed_location_hints} more hints to make now."
            )

            logging.debug(
                f"Now, we will actually use {priority_hints_to_use} out of {amount_of_priority_hint_candidates} "
                f"priority candidates. This is the floor of the lower number out of\n"
                f"1. {world.options.priority_hints_percentage_out_of_possible}% of {possible_priority_hints} "
                f"possible priority hints, which is {priority_cap_possible}.\n"
                f"2. {world.options.priority_hints_percentage_out_of_remaining}% of {remaining_location_hints} "
                f"remaining hint slots after area and always hints, which is {priority_cap_remain}."
            )

        extra_always_and_priority_hints: List[WitnessLocationHint] = []

        for _ in range(more_always_hints):
            extra_always_hint = always_hints.pop()

            logging.debug(
                f"Adding late always hint: "
                f"{extra_always_hint.location.item} on {extra_always_hint.location}"
            )

            extra_always_and_priority_hints.append(extra_always_hint)

        for _ in range(more_priority_hints):
            extra_priority_hint = priority_hints.pop()

            logging.debug(
                f"Adding late priority hint: "
                f"{extra_priority_hint.location.item} on {extra_priority_hint.location}"
            )

            extra_always_and_priority_hints.append(extra_priority_hint)

        generated_hints += make_extra_location_hints(
            world, hint_amount - len(generated_hints), world.own_itempool, already_hinted_locations,
            extra_always_and_priority_hints, unhinted_locations_per_area
        )

    # If we still don't have enough for whatever reason, throw a warning, proceed with the lower amount
    if len(generated_hints) != hint_amount:
        logging.warning(f"Couldn't generate {hint_amount} hints for player {world.player_name}. "
                        f"Generated {len(generated_hints)} instead.")

    end_line = f"Witness hints: {world.player_name} end"
    dashes = "-" * len(end_line)
    logging.debug(f"{dashes}\n{end_line}\n{dashes}")

    return generated_hints


def get_compact_hint_args(hint: WitnessWordedHint, local_player_number: int) -> CompactHintArgs:
    """
    Arg reference:

    Area Hint: 1st Arg is the amount of area progression and hunt panels. 2nd Arg is the name of the area.
    Location Hint: 1st Arg is the location's address, second arg is the player number the location belongs to.
    Junk Hint: 1st Arg is -1, second arg is this slot's player number.
    """

    # Is Area Hint
    if hint.area_amount is not None:
        area_amount = hint.area_amount
        hunt_panels = hint.area_hunt_panels

        area_and_hunt_panels = area_amount
        # Encode amounts together
        if hunt_panels:
            area_and_hunt_panels += 0x100 * hunt_panels

        return hint.area, area_and_hunt_panels

    location = hint.location

    # Is location hint
    if location and location.address is not None:
        if hint.vague_location_hint and location.player == local_player_number:
            assert hint.area is not None  # A local vague location hint should have an area argument
            return location.address, "containing_area:" + hint.area
        return location.address, location.player  # Scouting does not matter for other players (currently)

    # Is junk / undefined hint
    return -1, local_player_number


def make_compact_hint_data(hint: WitnessWordedHint, local_player_number: int) -> CompactHintData:
    compact_arg_1, compact_arg_2 = get_compact_hint_args(hint, local_player_number)
    return hint.wording, compact_arg_1, compact_arg_2


def make_laser_hints(world: "WitnessWorld", laser_names: List[str]) -> Dict[str, WitnessWordedHint]:
    laser_hints_by_name = {}

    for item_name in laser_names:
        location_hint = hint_from_item(world, item_name, world.own_itempool)
        if not location_hint:
            continue

        laser_hints_by_name[item_name] = word_direct_hint(world, location_hint)

    return laser_hints_by_name
