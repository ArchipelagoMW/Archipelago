
from typing import Mapping, Iterable, Tuple, Union
from BaseClasses import CollectionState, MultiWorld

from .types import AccessRule
from .locations import location_table as w4_locations


RequiredItem = Union[str, Tuple[str, int]]


helpers: Mapping[str, RequiredItem] = {
    'Ground Pound':        'Progressive Ground Pound',
    'Super Ground Pound': ('Progressive Ground Pound', 2),
    'Grab':                'Progressive Grab',
    'Heavy Grab':         ('Progressive Grab', 2)
}


def needs_items(player: int, requirements: Iterable[Iterable[RequiredItem]]) -> AccessRule:
    def has_requirements(state: CollectionState):
        def has_item(requirement: RequiredItem):
            requirement = helpers.get(requirement, requirement)
            if isinstance(requirement, str):
                item = requirement
                count = 1
            else:
                item, count = requirement
            return state.has(item, player, count)
        return any(map(lambda all_list: all(map(has_item, all_list)), requirements))
    return has_requirements


def set_access_rules(multiworld: MultiWorld, player: int):
    for level, items in level_rules.items():
        region = multiworld.get_region(level, player)
        region.clear_rule = needs_items(player, items)

    location_rules = difficulty_location_rules[multiworld.difficulty[player].value]
    for name, items in location_rules.items():
        try:
            location = multiworld.get_location(name, player)
            location.access_rule = needs_items(player, items)
        except KeyError as k:
            # Raise for invalid location names, not ones that aren't in this player's world
            if name not in w4_locations:
                raise ValueError(f'Location {name} does not exist') from k


level_rules = {
    'Hall of Hieroglyphs':   [['Dash Attack', 'Grab', 'Super Ground Pound']],

    #Palm Tree Paradise         None
    'Wildflower Fields':     [['Super Ground Pound', 'Swim']],
    'Mystic Lake':           [['Swim', 'Head Smash']],
    'Monsoon Jungle':        [['Ground Pound']],

    #The Curious Factory        None
    'The Toxic Landfill':    [['Dash Attack', 'Super Ground Pound', 'Head Smash']],
    '40 Below Fridge':       [['Super Ground Pound']],
    'Pinball Zone':          [['Grab', 'Ground Pound', 'Head Smash']],

    'Toy Block Tower':       [['Heavy Grab']],
    'The Big Board':         [['Ground Pound']],
    #Doodle Woods               None
    'Domino Row':            [['Swim']],

    'Crescent Moon Village': [['Head Smash', 'Dash Attack']],
    'Arabian Night':         [['Swim']],
    'Fiery Cavern':          [['Ground Pound', 'Dash Attack']],
    'Hotel Horror':          [['Heavy Grab']],

    # This one's weird. You need swim to get anything, but Keyzer is the only
    # thing that requires grab in there.
    # Logic considers the escape necessary to get the items in a level and
    # Keyzer to advance, but Golden Passage is the only level where the two have
    # different requirements.
    # When more settings like level shuffle and always-open portals get added,
    # it'll probably be best for logic to have them as separate events.
    'Golden Passage':        [['Swim', 'Grab']],
}


location_rules_all = {
    'Cractus':       [['Ground Pound']],
    'Cuckoo Condor': [['Grab']],
    'Aerodent':      [['Grab']],
    'Catbat':        [['Ground Pound']],
    'Golden Diva':   [['Grab']],

    'Wildflower Fields - 8-Shaped Cave Box':          [['Grab']],
    'Mystic Lake - Small Cave Box':                   [['Dash Attack']],
    'Mystic Lake - CD Box':                           [['Dash Attack']],
    'Mystic Lake - Full Health Item Box':             [['Grab']],
    'Monsoon Jungle - Buried Cave Box':               [['Grab', 'Ground Pound']],
    'Monsoon Jungle - Puffy Hallway Box':             [['Dash Attack']],
    'Monsoon Jungle - Full Health Item Box':          [['Swim']],

    'The Curious Factory - Gear Elevator Box':        [['Dash Attack']],
    'The Toxic Landfill - Current Circle Box':        [['Swim']],
    'The Toxic Landfill - Transformation Puzzle Box': [['Heavy Grab'], ['Enemy Jump']],
    '40 Below Fridge - CD Box':                       [['Head Smash']],
    'Pinball Zone - Full Health Item Box':            [['Super Ground Pound']],

    'Toy Block Tower - Digging Room Box':             [['Dash Attack']],
    'Toy Block Tower - Full Health Item Box':         [['Dash Attack']],
    'The Big Board - Hard Enemy Room Box':            [['Grab']],
    'The Big Board - Full Health Item Box':           [['Grab', 'Enemy Jump']],
    'Doodle Woods - Blue Circle Box':                 [['Enemy Jump']],
    'Doodle Woods - Pink Circle Box':                 [['Ground Pound']],
    'Doodle Woods - Gray Square Box':                 [['Ground Pound'], ['Grab']],
    'Domino Row - Keyzer Room Box':                   [['Ground Pound']],

    'Crescent Moon Village - Agile Bat Hidden Box':   [['Ground Pound', 'Grab']],
    'Crescent Moon Village - Sewer Box':              [['Swim']],
    'Arabian Night - Flying Carpet Dash Attack Box':  [['Dash Attack']],
    'Arabian Night - Kool-Aid Box':                   [['Dash Attack']],
}


location_rules_normal = {
    **location_rules_all,

    'Doodle Woods - CD Box': [['Ground Pound'], ['Grab']],
}

location_rules_hard = {
    **location_rules_all,

    'Arabian Night - Onomi Box': [['Ground Pound'], ['Head Smash']],
    'Arabian Night - Sewer Box': [['Super Ground Pound']],
}

location_rules_s_hard = {
    **location_rules_all,

    # TODO
}

difficulty_location_rules = (
    location_rules_normal,
    location_rules_hard,
    location_rules_s_hard,
)
