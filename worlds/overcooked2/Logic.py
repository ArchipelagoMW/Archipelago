from BaseClasses import CollectionState, Region
from .Overcooked2Levels import Overcooked2GenericLevel
from .Items import item_frequencies


def has_requirements_for_level_access(state: CollectionState, level_name: str, previous_level_name: str,
                                      required_star_count: int, player: int) -> bool:
    # Check if the ramps in the overworld are set correctly
    if level_name in ramp_logic:
        if not state.has("Ramp Button", player):
            return False # need the item to use ramps

        for req in ramp_logic[level_name]:
             # TODO: while entirely logical, the spoiler might show some checks slightly out of order
            if not state.can_reach(state.world.get_location(req + " Completed", player)):
                return False # This level needs another to be beaten first

    # Kevin Levels Need to have the corresponding items
    if level_name.startswith("K"):
        return state.has(level_name, player)
    
    # Must have enough stars to purchase level
    star_count = state.item_count("Star", player) + state.item_count("Bonus Star", player)
    if star_count < required_star_count:
        return False

    # If this isn't the first level in a world, it needs the previous level to be unlocked first
    if previous_level_name is not None:
        previous_level: Region = state.world.get_region(previous_level_name, player)
        # TODO: while entirely logical, the spoiler might show some checks slightly out of order
        if not state.can_reach(previous_level):
            return False

    # If we made it this far we have all requirements
    return True


def has_requirements_for_level_star(
        state: CollectionState, level: Overcooked2GenericLevel, stars: int, player: int) -> bool:
    assert stars >= 0 and stars <= 3

    # First ensure that previous stars are obtainable
    if stars > 1:
        if not has_requirements_for_level_star(state, level, stars-1, player):
            return False
    
    # Second, ensure that global requirements are met
    if not meets_requirements(state, "*", stars, player):
        return False

    # Finally, return success only if this level's requirements are met
    return meets_requirements(state, level.shortname(), stars, player)


def meets_requirements(state: CollectionState, name: str, stars: int, player: int):
    # Get requirements for level
    (exclusive_reqs, additive_reqs) = level_logic[name][stars-1]

    # print(f"{name} ({stars}-Stars): {exclusive_reqs}|{additive_reqs}")

    # Check if we meet exclusive requirements
    if len(exclusive_reqs) > 0 and not state.has_all(exclusive_reqs, player):
        return False

    for item_name in item_frequencies:
        if item_name in exclusive_reqs:
            if not state.has(item_name, player, item_frequencies[item_name]):
                return False # need to have all variants of a progressive item to get the score

    # Check if we meet additive requirements
    if len(additive_reqs) == 0:
        return True

    total: float = 0.0
    for (item_name, weight) in additive_reqs:
        for _ in range(0, state.item_count(item_name, player)):
            total += weight
            if total >= 0.99:
                return True

    return False # be nice to rounding errors :)

# If key missing, doesn't require a ramp to access (or the logic is handled by a preceeding level)
#
# If empty, a ramp is required to access, but the ramp button is garunteed accessible
#
# If populated, a ramp is required to access and the button requires all levels in the
# list to be compelted before it can be pressed
#
ramp_logic = {
    "1-5": [],
    "2-2": [],
    "3-1": [],
    "5-2": [],
    "6-1": [],
    "6-2": ["5-1"], # 5-1 spawns blue button, blue button gets you to red button
    "Kevin-1": [],
    "Kevin-7": ["5-1"], # 5-1 spawns blue button,
                        # press blue button,
                        # climb blue ramp,
                        # jump the gap,
                        # climb wood ramps
    "Kevin-8": ["5-1", "6-2"], # Same as above, but 6-2 spawns the ramp to K8
}

# 1, 2, 3, 4, 5, 6

# Level 1 - dict keyed by friendly level names
# Level 2 - tuple with 3 elements, one for each star requirement
# Level 3 - tuple with 3 elements, one for exclusive requirements and one for additive requirements
# Level 4 (exclusive) - set of item name strings of items which MUST be in the inventory to allow logical completion
# Level 4 (additive)  - list of tuples containing item name and item weight where the sum of which are in the player's inventory
#                       must be 1.0+ to allow logical completion 
# 
# Each Star's logical requirements imply any previous requirements
# 
level_logic = {
    # "Tutorial": [],
    "*": (
        ( # 1-star
            { # Exclusive
                
            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive
                ("Spare Plate", 0.4),
                ("Sharp Knife", 0.2),
                ("Burn Leniency", 0.2),
                ("Larger Tip Jar", 0.3),
                ("Dish Scrubber", 0.2),
                ("Progressive Dash", 0.3),
                ("Throw", 0.5),
                ("Catch", 0.1),
                ("Clean Dishes", 0.1),
                ("Guest Patience", 0.1),
                ("Order Lookahead", 0.2),
            },
        ),
        ( # 3-star
            [ # Exclusive
                "Progressive Dash",
                "Spare Plate",
                "Larger Tip Jar",
                "Throw",
            ],
            { # Additive
            },
        )
    ),
    "Story 1-1": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 1-2": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 1-3": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 1-4": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 1-5": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 1-6": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 2-1": (
        ( # 1-star
            { # Exclusive
                "Throw",
            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 2-2": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 2-3": (
        ( # 1-star
            { # Exclusive
                "Throw"
            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 2-4": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive
                "Fire Extinguisher",
            },
            [ # Additive
                
            ]
        )
    ),
    "Story 2-5": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 2-6": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 3-1": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 3-2": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive
                ("Throw", 1.0),
                ("Progressive Dash", 0.5),
                ("Sharp Knife", 0.5),
                ("Larger Tip Jar", 0.25),
                ("Dish Scrubber", 0.25),
            },
        ),
        ( # 2-star
            { # Exclusive
                "Throw",
            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 3-3": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 3-4": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive
                "Throw",
            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 3-5": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive
                "Throw",
            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 3-6": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 4-1": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 4-2": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive
                "Throw",
            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 4-3": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 4-4": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 4-5": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 4-6": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 5-1": (
        ( # 1-star
            { # Exclusive
                "Remote Control Batteries"
            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 5-2": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive
                "Fire Extinguisher",
            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 5-3": (
        ( # 1-star
            { # Exclusive
                "Remote Control Batteries"
            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 5-4": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 5-5": (
        ( # 1-star
            { # Exclusive
                "Remote Control Batteries"
            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 5-6": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 6-1": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive
                "Fire Extinguisher",
            },
            { # Additive

            },
        )
    ),
    "Story 6-2": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 6-3": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 6-4": (
        ( # 1-star
            { # Exclusive
                "Remote Control Batteries"
            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 6-5": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story 6-6": (
        ( # 1-star
            { # Exclusive
                "Throw",
                "Progressive Dash",
                "Spare Plate",
            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story K-1": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story K-2": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story K-3": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story K-4": (
        ( # 1-star
            { # Exclusive
                "Fire Extinguisher",
            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story K-5": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story K-6": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story K-7": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Story K-8": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Surf 1-1": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Surf 1-2": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Surf 1-3": (
        ( # 1-star
            { # Exclusive
                "Throw",
            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Surf 1-4": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Surf 2-1": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive
                "Bellows",
            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Surf 2-2": (
        ( # 1-star
            { # Exclusive
                "Remote Control Batteries"
            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive
                "Bellows",
            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Surf 2-3": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Surf 2-4": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Surf 3-1": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive
                "Bellows",
            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Surf 3-2": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Surf 3-3": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Surf 3-4": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive
                "Bellows",
            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Surf K-1": (
        ( # 1-star
            { # Exclusive
                "Remote Control Batteries"
            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive
                "Throw",
            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Campfire 1-1": (
        ( # 1-star
            { # Exclusive
                "Wood"
            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive
                
            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Campfire 1-2": (
        ( # 1-star
            { # Exclusive
                "Wood"
            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Campfire 1-3": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive
                "Lightweight Backpack"
            },
            { # Additive

            },
        )
    ),
    "Campfire 1-4": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Campfire 2-1": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Campfire 2-2": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive
                "Lightweight Backpack"
            },
            { # Additive

            },
        )
    ),
    "Campfire 2-3": (
        ( # 1-star
            { # Exclusive
                "Wood"
            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive
                "Lightweight Backpack"
            },
            { # Additive

            },
        )
    ),
    "Campfire 2-4": (
        ( # 1-star
            { # Exclusive
                "Wood"
            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Campfire 3-1": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive
                "Lightweight Backpack"
            },
            { # Additive

            },
        )
    ),
    "Campfire 3-2": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Campfire 3-3": (
        ( # 1-star
            { # Exclusive
                "Wood",
            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive
                "Lightweight Backpack",
            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive
                
            },
            { # Additive

            },
        )
    ),
    "Campfire 3-4": (
        ( # 1-star
            { # Exclusive
                "Wood",
            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Campfire K-1": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Campfire K-2": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Campfire K-3": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Carnival 1-1": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Carnival 1-2": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Carnival 1-3": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Carnival 1-4": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive
                "Faster Condiment/Drink Switch"
            },
            { # Additive

            },
        )
    ),
    "Carnival 2-1": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Carnival 2-2": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive
                "Faster Condiment/Drink Switch"
            },
            { # Additive

            },
        )
    ),
    "Carnival 2-3": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Carnival 2-4": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive
                "Faster Condiment/Drink Switch"
            },
            { # Additive

            },
        )
    ),
    "Carnival 3-1": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Carnival 3-2": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive
                "Faster Condiment/Drink Switch"
            },
            { # Additive

            },
        )
    ),
    "Carnival 3-3": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive
                "Faster Condiment/Drink Switch"
            },
            { # Additive

            },
        )
    ),
    "Carnival 3-4": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive
                "Faster Condiment/Drink Switch"
            },
            { # Additive

            },
        )
    ),
    "Carnival K-1": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Carnival K-2": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Carnival K-3": (
        ( # 1-star
            { # Exclusive
                "Remote Control Batteries"
            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Horde 1-1": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Horde 1-2": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive
                "Coal Bucket",
            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Horde 1-3": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive
                "Coal Bucket",
            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Horde 2-1": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Horde 2-2": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Horde 2-3": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive
                "Coal Bucket",
            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Horde 3-1": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Horde 3-2": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Horde 3-3": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive
                ("Throw", 0.5),
                ("Progressive Dash", 0.5),
                ("Coal Bucket", 0.5),
            },
        ),
        ( # 2-star
            { # Exclusive
                "Throw",
                "Coal Bucket",
            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Horde K-1": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Horde K-2": (
        ( # 1-star
            { # Exclusive
                "Remote Control Batteries"
            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Horde K-3": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Horde H-1": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Horde H-2": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Horde H-3": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Horde H-4": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Horde H-5": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Horde H-6": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Horde H-7": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Horde H-8": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Christmas 1-1": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Christmas 1-2": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Christmas 1-3": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Christmas 1-4": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Christmas 1-5": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Chinese 1-1": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Chinese 1-2": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive
                "Wok Wheels"
            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Chinese 1-3": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Chinese 1-4": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive
                "Wok Wheels"
            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Chinese 1-5": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Chinese 1-6": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Chinese 1-7": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive
                "Wok Wheels"
            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Winter 1-1": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Winter H-2": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Winter 1-3": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Winter H-4": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Winter 1-5": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Spring 1-1": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive
                "Wok Wheels"
            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Spring 1-2": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Spring 1-3": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive
                "Wok Wheels"
            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Spring 1-4": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Spring 1-5": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "SOBO 1-1": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive
                "Faster Condiment/Drink Switch"
            },
            { # Additive

            },
        )
    ),
    "SOBO 1-2": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive
                "Faster Condiment/Drink Switch"
            },
            { # Additive

            },
        )
    ),
    "SOBO 1-3": (
        ( # 1-star
            { # Exclusive
                "Remote Control Batteries"
            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive
                "Fire Extinguisher",
            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "SOBO 1-4": (
        ( # 1-star
            { # Exclusive
                "Fire Extinguisher",
            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive
                "Faster Condiment/Drink Switch"
            },
            { # Additive

            },
        )
    ),
    "SOBO 1-5": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive
                "Fire Extinguisher",
                "Faster Condiment/Drink Switch",
            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive
            },
            { # Additive

            },
        )
    ),
    "Moon 1-1": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Moon 1-2": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Moon 1-3": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Moon 1-4": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
    "Moon 1-5": (
        ( # 1-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 2-star
            { # Exclusive

            },
            { # Additive

            },
        ),
        ( # 3-star
            { # Exclusive

            },
            { # Additive

            },
        )
    ),
}
