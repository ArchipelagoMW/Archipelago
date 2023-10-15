
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


def needs_all(player: int, requirements: Iterable[RequiredItem]) -> AccessRule:
    def has_requirements(state: CollectionState):
        for requirement in requirements:
            requirement = helpers.get(requirement, requirement)
            if isinstance(requirement, str):
                item = requirement
                count = 1
            else:
                item, count = requirement
            if not state.has(item, player, count):
                return False
        return True
    return has_requirements


def set_access_rules(multiworld: MultiWorld, player: int):
    for level, items in level_rules.items():
        region = multiworld.get_region(level, player)
        region.clear_rule = needs_all(player, items)

    location_rules = difficulty_location_rules[multiworld.difficulty[player].value]
    for name, items in location_rules.items():
        try:
            location = multiworld.get_location(name, player)
            location.access_rule = needs_all(player, items)
        except KeyError as k:
            # Raise for invalid location names, not ones that aren't in this player's world
            if name not in w4_locations:
                raise ValueError(f'Location {name} does not exist') from k


level_rules = {
    'Hall of Hieroglyphs':   ['Dash Attack', 'Grab', 'Super Ground Pound'],

    #Palm Tree Paradise        None
    'Wildflower Fields':     ['Super Ground Pound', 'Swim'],
    'Mystic Lake':           ['Swim', 'Head Smash'],
    'Monsoon Jungle':        ['Ground Pound'],

    #The Curious Factory       None
    'The Toxic Landfill':    ['Dash Attack', 'Super Ground Pound', 'Head Smash'],
    '40 Below Fridge':       ['Super Ground Pound'],
    'Pinball Zone':          ['Grab', 'Ground Pound', 'Head Smash'],

    'Toy Block Tower':       ['Heavy Grab'],
    'The Big Board':         ['Ground Pound'],
    #Doodle Woods              None
    'Domino Row':            ['Swim'],

    'Crescent Moon Village': ['Head Smash', 'Dash Attack'],
    'Arabian Night': ['Swim'],
    'Fiery Cavern': ['Ground Pound', 'Dash Attack'],
    'Hotel Horror': ['Heavy Grab'],

    # This one's weird. You need swim to get anything, but Keyzer is the only
    # thing that requires grab in there.
    # Logic considers the escape necessary to get the items in a level and
    # Keyzer to advance, but Golden Passage is the only level where the two have
    # different requirements.
    # When more settings like level shuffle and always-open portals get added,
    # it'll probably be best for logic to have them as separate events.
    'Golden Passage': ['Swim', 'Grab'],
}


location_rules_all = {
    'Cractus':       ['Ground Pound'],
    'Cuckoo Condor': ['Grab'],
    'Aerodent':      ['Grab'],
    'Catbat':        ['Ground Pound'],
    'Golden Diva':   ['Grab'],

    'Monsoon Jungle - Buried Cave Box':      ['Grab', 'Ground Pound'],
    'Domino Row - Keyzer Room Box':          ['Ground Pound'],
    'Crescent Moon Village - Sewer Box':     ['Swim'],
}


location_rules_normal = {
    **location_rules_all,

    'Mystic Lake - CD Box':                   ['Dash Attack'],
    'Mystic Lake - Full Health Item Box':     ['Grab'],
    'Monsoon Jungle - Full Health Item Box':  ['Swim'],

    '40 Below Fridge - CD Box':               ['Head Smash'],
    'Pinball Zone - Full Health Item Box':    ['Super Ground Pound'],

    'Toy Block Tower - Full Health Item Box': ['Dash Attack'],
    'The Big Board - Full Health Item Box':   ['Progressive Grab', 'Enemy Jump'],
    'Doodle Woods - CD Box':                  ['Ground Pound'],
}

location_rules_hard = {
    **location_rules_all,

    # TODO
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
