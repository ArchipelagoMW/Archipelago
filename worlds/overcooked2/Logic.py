from BaseClasses import CollectionState
from .Overcooked2Levels import Overcooked2GenericLevel, Overcooked2Dlc, Overcooked2Level
from typing import Dict
from random import Random


def has_requirements_for_level_access(state: CollectionState, level_name: str, previous_level_completed_event_name: str,
                                      required_star_count: int, player: int) -> bool:
    # Check if the ramps in the overworld are set correctly
    if level_name in ramp_logic:
        (ramp_reqs, level_reqs) = ramp_logic[level_name]

        for req in level_reqs:
            if not state.has(req + " Level Complete", player):
                return False  # This level needs another to be beaten first

        for req in ramp_reqs:
            if not state.has(req + " Ramp", player):
                return False  # The player doesn't have the pre-requisite ramp button

    # Kevin Levels Need to have the corresponding items
    if level_name.startswith("K"):
        return state.has(level_name, player)

    # Must have enough stars to purchase level
    star_count = state.item_count("Star", player) + state.item_count("Bonus Star", player)
    if star_count < required_star_count:
        return False

    # If this isn't the first level in a world, it needs the previous level to be unlocked first
    if previous_level_completed_event_name is not None:
        if not state.has(previous_level_completed_event_name, player):
            return False

    # If we made it this far we have all requirements
    return True


def has_requirements_for_level_star(
        state: CollectionState, level: Overcooked2GenericLevel, stars: int, player: int) -> bool:
    assert 0 <= stars <= 3

    # First ensure that previous stars are obtainable
    if stars > 1:
        if not has_requirements_for_level_star(state, level, stars-1, player):
            return False

    # Second, ensure that global requirements are met
    if not meets_requirements(state, "*", stars, player):
        return False

    # Finally, return success only if this level's requirements are met
    return meets_requirements(state, level.shortname, stars, player)


def meets_requirements(state: CollectionState, name: str, stars: int, player: int):
    # Get requirements for level
    (exclusive_reqs, additive_reqs) = level_logic[name][stars-1]

    # print(f"{name} ({stars}-Stars): {exclusive_reqs}|{additive_reqs}")

    # Check if we meet exclusive requirements
    if len(exclusive_reqs) > 0 and not state.has_all(exclusive_reqs, player):
        return False

    # Check if we meet additive requirements
    if len(additive_reqs) == 0:
        return True

    total: float = 0.0
    for (item_name, weight) in additive_reqs:
        for _ in range(0, state.item_count(item_name, player)):
            total += weight
            if total >= 0.99:  # be nice to rounding errors :)
                return True

    return False


def is_item_progression(item_name, level_mapping, include_kevin):
    if item_name.endswith("Emote"):
        return False

    if "Kevin" in item_name or "Ramp" in item_name:
        return True  # always progression

    def item_in_logic(shortname, _item_name):
        for star in range(0, 3):
            (exclusive, additive) = level_logic[shortname][star]

            if _item_name in exclusive:
                return True

            for req in additive:
                if req[0] == _item_name:
                    if req[1] > 0.3:  # this bit smells of a deal with the devil, but it seems to be for the better
                        return True
                    break

        return False

    if item_in_logic("*", item_name):
        return True

    for level in Overcooked2Level():
        if not include_kevin and level.level_id > 36:
            break

        if level_mapping is None:
            unmapped_level = Overcooked2GenericLevel(level.level_id)
        else:
            unmapped_level = level_mapping[level.level_id]

        if item_in_logic(unmapped_level.shortname, item_name):
            return True

    return False


def is_useful(item_name):
    return item_name in [
        "Faster Respawn Time",
        "Fire Extinguisher",
        "Clean Dishes",
        "Larger Tip Jar",
        "Dish Scrubber",
        "Burn Leniency",
        "Sharp Knife",
        "Order Lookahead",
        "Guest Patience",
        "Bonus Star",
    ]


def level_shuffle_factory(
    rng: Random,
    shuffle_prep_levels: bool,
    shuffle_horde_levels: bool,
) -> Dict[int, Overcooked2GenericLevel]:  # return <story_level_id, level>
    # Create a list of all valid levels for selection
    # (excludes tutorial, throne and sometimes horde/prep levels)
    pool = list()
    for dlc in Overcooked2Dlc:
        for level_id in range(dlc.start_level_id, dlc.end_level_id):
            if level_id in dlc.excluded_levels():
                continue

            if not shuffle_horde_levels and level_id in dlc.horde_levels():
                continue

            if not shuffle_prep_levels and level_id in dlc.prep_levels():
                continue

            pool.append(
                Overcooked2GenericLevel(level_id, dlc)
            )

    # Sort the pool to eliminate risk
    pool.sort(key=lambda x: int(x.dlc)*1000 + x.level_id)

    result: Dict[int, Overcooked2GenericLevel] = dict()
    story = Overcooked2Dlc.STORY

    while len(result) == 0 or not meets_minimum_sphere_one_requirements(result):
        result.clear()

        # Shuffle the pool, using the provided RNG
        rng.shuffle(pool)

        # Return the first 44 levels and assign those to each level
        for level_id in range(story.start_level_id, story.end_level_id):
            if level_id not in story.excluded_levels():
                result[level_id] = pool[level_id-1]
            elif level_id == 36:
                # Level 6-6 is exempt from shuffling
                result[level_id] = Overcooked2GenericLevel(level_id)

    return result


def meets_minimum_sphere_one_requirements(
    levels: Dict[int, Overcooked2GenericLevel],
) -> bool:

    # 1-1, 2-1, and 4-1 are garunteed to be accessible on
    # the overworld without requiring a ramp or additional stars
    sphere_one = [1, 7, 19]

    # 1-2, 2-2, 3-1 and 5-1 are almost always the next thing unlocked
    sphere_twoish = [2, 8, 13, 25]

    # Peek the logic for sphere one and see how many are possible
    # with no items
    sphere_one_count = 0
    for level_id in sphere_one:
        if (is_completable_no_items(levels[level_id])):
            sphere_one_count += 1

    sphere_twoish_count = 0
    for level_id in sphere_twoish:
        if (is_completable_no_items(levels[level_id])):
            sphere_twoish_count += 1

    return sphere_one_count >= 2 and \
        sphere_twoish_count >= 2 and \
        sphere_one_count + sphere_twoish_count >= 6


def is_completable_no_items(level: Overcooked2GenericLevel) -> bool:
    one_star_logic = level_logic[level.shortname][0]
    (exclusive, additive) = one_star_logic

    # print(f"\n{level.shortname}: {exclusive} / {additive}")

    return len(exclusive) == 0 and len(additive) == 0


# If key missing, doesn't require a ramp to access (or the logic is handled by a preceeding level)
#
# If empty, a ramp is required to access, but the ramp button is garunteed accessible
#
# If populated, ramp(s) are required to access and the button requires all levels in the
# list to be compelted before it can be pressed
#
ramp_logic = {
    "1-5": (["Yellow"], []),
    "2-2": (["Green"], []),
    "3-1": (["Blue"], []),
    "5-2": (["Purple"], []),
    "6-1": (["Pink"], []),
    "6-2": (["Red", "Purple"], ["5-1"]),  # 5-1 spawns blue button, blue button gets you to red button
    "Kevin-1": (["Dark Green"], []),
    "Kevin-7": (["Purple"], ["5-1"]), # 5-1 spawns blue button,
                                    # press blue button,
                                    # climb blue ramp,
                                    # jump the gap,
                                    # climb wood ramps
    "Kevin-8": (["Red", "Blue"], ["5-1", "6-2"]),  # Same as above, but 6-2 spawns the ramp to K8
}

horde_logic = {  # Additive
    ("Coin Purse", 0.7),
    ("Calmer Unbread", 0.35),
    ("Progressive Dash", 0.2),
    ("Progressive Throw/Catch", 0.15),
    ("Sharp Knife", 0.15),
    ("Dish Scrubber", 0.125),
    ("Burn Leniency", 0.1),
    ("Spare Plate", 0.075),
    ("Clean Dishes", 0.025),
}

# Level 1 - dict keyed by friendly level names
# Level 2 - tuple with 3 elements, one for each star requirement
# Level 3 - tuple with 2 elements, one for exclusive requirements and one for additive requirements
# Level 4 (exclusive) - set of item name strings of items which MUST be in the inventory to allow logical completion
# Level 4 (additive)  - list of tuples containing item name and item weight where the sum of which are in the player's inventory
#                       must be 1.0+ to allow logical completion
#
# Each Star's logical requirements imply any previous requirements
#
level_logic = {
    # "Tutorial": [],
    "*": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive
                ("Progressive Throw/Catch", 0.4),
                ("Progressive Dash", 0.35),
                ("Sharp Knife", 0.3),
                ("Dish Scrubber", 0.25),
                ("Larger Tip Jar", 0.2),
                ("Spare Plate", 0.2),
                ("Burn Leniency", 0.15),
                ("Order Lookahead", 0.15),
                ("Clean Dishes", 0.1),
                ("Guest Patience", 0.1),
            },
        ),
        (  # 3-star
            [  # Exclusive
                "Progressive Dash",
                "Spare Plate",
                "Larger Tip Jar",
                "Progressive Throw/Catch",
            ],
            {  # Additive
                ("Sharp Knife", 1.0),
                ("Dish Scrubber", 1.0),
                ("Clean Dishes", 0.5),
                ("Guest Patience", 0.25),
                ("Burn Leniency", 0.25),
            },
        )
    ),
    "Story 1-1": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 1-2": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 1-3": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 1-4": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 1-5": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 1-6": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 2-1": (
        (  # 1-star
            {  # Exclusive
                "Progressive Throw/Catch",
            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 2-2": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 2-3": (
        (  # 1-star
            {  # Exclusive
                "Progressive Throw/Catch"
            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 2-4": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive
                ("Progressive Throw/Catch", 1.0),
                ("Progressive Dash", 1.0),
            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive
                "Fire Extinguisher",
            },
            [  # Additive

            ]
        )
    ),
    "Story 2-5": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 2-6": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 3-1": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 3-2": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive
                ("Progressive Throw/Catch", 1.0),
                ("Progressive Dash", 0.5),
                ("Sharp Knife", 0.5),
                ("Larger Tip Jar", 0.25),
                ("Dish Scrubber", 0.25),
            },
        ),
        (  # 2-star
            {  # Exclusive
                "Progressive Throw/Catch",
            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 3-3": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 3-4": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive
                "Progressive Throw/Catch",
            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 3-5": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive
                "Progressive Throw/Catch",
            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 3-6": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 4-1": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 4-2": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive
                "Progressive Throw/Catch",
            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 4-3": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 4-4": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 4-5": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 4-6": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 5-1": (
        (  # 1-star
            {  # Exclusive
                "Control Stick Batteries"
            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 5-2": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive
                "Fire Extinguisher",
            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 5-3": (
        (  # 1-star
            {  # Exclusive
                "Control Stick Batteries"
            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 5-4": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 5-5": (
        (  # 1-star
            {  # Exclusive
                "Control Stick Batteries"
            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 5-6": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 6-1": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive
                "Fire Extinguisher",
            },
            {  # Additive

            },
        )
    ),
    "Story 6-2": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 6-3": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 6-4": (
        (  # 1-star
            {  # Exclusive
                "Control Stick Batteries"
            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 6-5": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story 6-6": (
        (  # 1-star
            {  # Exclusive
                "Progressive Throw/Catch",
                "Progressive Dash",
                "Spare Plate",
            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story K-1": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story K-2": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story K-3": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story K-4": (
        (  # 1-star
            {  # Exclusive
                "Fire Extinguisher",
            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story K-5": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story K-6": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story K-7": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Story K-8": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Surf 1-1": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Surf 1-2": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Surf 1-3": (
        (  # 1-star
            {  # Exclusive
                "Progressive Throw/Catch",
            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Surf 1-4": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Surf 2-1": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive
                "Bellows",
            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Surf 2-2": (
        (  # 1-star
            {  # Exclusive
                "Control Stick Batteries"
            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive
                "Bellows",
            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Surf 2-3": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Surf 2-4": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Surf 3-1": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive
                "Bellows",
            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Surf 3-2": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Surf 3-3": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Surf 3-4": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive
                "Bellows",
            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Surf K-1": (
        (  # 1-star
            {  # Exclusive
                "Control Stick Batteries"
            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive
                "Progressive Throw/Catch",
            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Campfire 1-1": (
        (  # 1-star
            {  # Exclusive
                "Wood"
            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Campfire 1-2": (
        (  # 1-star
            {  # Exclusive
                "Wood"
            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Campfire 1-3": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive
                "Lightweight Backpack"
            },
            {  # Additive

            },
        )
    ),
    "Campfire 1-4": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Campfire 2-1": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Campfire 2-2": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive
                "Lightweight Backpack"
            },
            {  # Additive

            },
        )
    ),
    "Campfire 2-3": (
        (  # 1-star
            {  # Exclusive
                "Wood"
            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive
                "Lightweight Backpack"
            },
            {  # Additive

            },
        )
    ),
    "Campfire 2-4": (
        (  # 1-star
            {  # Exclusive
                "Wood"
            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Campfire 3-1": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive
                "Lightweight Backpack"
            },
            {  # Additive

            },
        )
    ),
    "Campfire 3-2": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Campfire 3-3": (
        (  # 1-star
            {  # Exclusive
                "Wood",
            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive
                "Lightweight Backpack",
            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Campfire 3-4": (
        (  # 1-star
            {  # Exclusive
                "Wood",
            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Campfire K-1": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Campfire K-2": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Campfire K-3": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Carnival 1-1": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Carnival 1-2": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Carnival 1-3": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Carnival 1-4": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive
                "Faster Condiment/Drink Switch"
            },
            {  # Additive

            },
        )
    ),
    "Carnival 2-1": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Carnival 2-2": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive
                "Faster Condiment/Drink Switch"
            },
            {  # Additive

            },
        )
    ),
    "Carnival 2-3": (
        (  # 1-star
            {  # Exclusive
                "Control Stick Batteries"
            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Carnival 2-4": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive
                "Faster Condiment/Drink Switch"
            },
            {  # Additive

            },
        )
    ),
    "Carnival 3-1": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Carnival 3-2": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive
                "Faster Condiment/Drink Switch"
            },
            {  # Additive

            },
        )
    ),
    "Carnival 3-3": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive
                "Faster Condiment/Drink Switch"
            },
            {  # Additive

            },
        )
    ),
    "Carnival 3-4": (
        (  # 1-star
            {  # Exclusive
                "Control Stick Batteries"
            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive
                "Faster Condiment/Drink Switch"
            },
            {  # Additive

            },
        )
    ),
    "Carnival K-1": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Carnival K-2": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Carnival K-3": (
        (  # 1-star
            {  # Exclusive
                "Control Stick Batteries"
            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Horde 1-1": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            }
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Horde 1-2": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive
                "Coal Bucket",
            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Horde 1-3": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive
                "Coal Bucket",
            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Horde 2-1": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Horde 2-2": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Horde 2-3": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive
                "Coal Bucket",
            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Horde 3-1": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Horde 3-2": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Horde 3-3": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive
                ("Progressive Throw/Catch", 0.5),
                ("Progressive Dash", 0.5),
                ("Coal Bucket", 0.5),
            },
        ),
        (  # 2-star
            {  # Exclusive
                "Progressive Throw/Catch",
                "Coal Bucket",
            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Horde K-1": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Horde K-2": (
        (  # 1-star
            {  # Exclusive
                "Control Stick Batteries"
            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Horde K-3": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Horde H-1": (
        (  # 1-star
            {  # Exclusive

            },
            horde_logic,
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Horde H-2": (
        (  # 1-star
            {  # Exclusive

            },
            horde_logic,
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Horde H-3": (
        (  # 1-star
            {  # Exclusive

            },
            horde_logic,
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Horde H-4": (
        (  # 1-star
            {  # Exclusive

            },
            horde_logic,
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Horde H-5": (
        (  # 1-star
            {  # Exclusive

            },
            horde_logic,
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Horde H-6": (
        (  # 1-star
            {  # Exclusive

            },
            horde_logic,
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Horde H-7": (
        (  # 1-star
            {  # Exclusive

            },
            horde_logic,
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Horde H-8": (
        (  # 1-star
            {  # Exclusive
                "Coin Purse",
                "Calmer Unbread"
            },
            horde_logic,
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Christmas 1-1": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Christmas 1-2": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Christmas 1-3": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Christmas 1-4": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Christmas 1-5": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Chinese 1-1": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Chinese 1-2": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive
                "Wok Wheels"
            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Chinese 1-3": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Chinese 1-4": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive
                "Wok Wheels"
            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Chinese 1-5": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Chinese 1-6": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Chinese 1-7": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive
                "Wok Wheels"
            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Winter 1-1": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Winter H-2": (
        (  # 1-star
            {  # Exclusive

            },
            horde_logic,
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Winter 1-3": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Winter H-4": (
        (  # 1-star
            {  # Exclusive
                "Coin Purse",
                "Calmer Unbread"
            },
            horde_logic,
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Winter 1-5": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Spring 1-1": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive
                "Wok Wheels"
            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Spring 1-2": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Spring 1-3": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive
                "Wok Wheels"
            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Spring 1-4": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Spring 1-5": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "SOBO 1-1": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive
                "Faster Condiment/Drink Switch"
            },
            {  # Additive

            },
        )
    ),
    "SOBO 1-2": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive
                "Faster Condiment/Drink Switch"
            },
            {  # Additive

            },
        )
    ),
    "SOBO 1-3": (
        (  # 1-star
            {  # Exclusive
                "Control Stick Batteries"
            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive
                "Fire Extinguisher",
            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "SOBO 1-4": (
        (  # 1-star
            {  # Exclusive
                "Fire Extinguisher",
            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive
                "Faster Condiment/Drink Switch"
            },
            {  # Additive

            },
        )
    ),
    "SOBO 1-5": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive
                "Fire Extinguisher",
                "Faster Condiment/Drink Switch",
            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive
            },
            {  # Additive

            },
        )
    ),
    "Moon 1-1": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Moon 1-2": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Moon 1-3": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Moon 1-4": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
    "Moon 1-5": (
        (  # 1-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 2-star
            {  # Exclusive

            },
            {  # Additive

            },
        ),
        (  # 3-star
            {  # Exclusive

            },
            {  # Additive

            },
        )
    ),
}
