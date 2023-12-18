
from typing import Mapping, Iterable, Optional, Tuple, Union
from BaseClasses import CollectionState, MultiWorld

from . import items
from .types import AccessRule, ItemType, Passage
from .locations import location_table as w4_locations


RequiredItem = Union[str, Tuple[str, int]]


helpers: Mapping[str, RequiredItem] = {
    'Ground Pound':        'Progressive Ground Pound',
    'Super Ground Pound': ('Progressive Ground Pound', 2),
    'Grab':                'Progressive Grab',
    'Heavy Grab':         ('Progressive Grab', 2)
}


def resolve_helper(item_name: RequiredItem):
    requirement = helpers.get(item_name, item_name)
    if isinstance(requirement, str):
        return (requirement, 1)
    else:
        return requirement


def needs_items(player: int, requirements: Iterable[Iterable[RequiredItem]]) -> AccessRule:
    def has_requirements(state: CollectionState):
        def has_item(requirement: RequiredItem):
            item, count = resolve_helper(requirement)
            return state.has(item, player, count)
        return any(map(lambda all_list: all(map(has_item, all_list)), requirements))
    return has_requirements


def _get_escape_region(level_name: str, lookup: Mapping[str, Optional[str]]):
    region = lookup[level_name]
    if region is None:
        region = level_name
    else:
        region = f'{level_name} - {lookup[level_name]}'
    return region


def get_keyzer_region(level_name: str):
    return _get_escape_region(level_name, keyzer_regions)


def get_frog_switch_region(level_name: str):
    return _get_escape_region(level_name, frog_switch_regions)


def get_access_rule(player: int, region_name: str):
    rule = region_rules[region_name]
    if rule is None:
        return None
    return needs_items(player, rule)


def make_boss_access_rule(player: int, passage: Passage, jewels_needed: int):
    jewel_list = [[(name, jewels_needed)
                  for name in items.filter_item_names(type=ItemType.JEWEL, passage=passage)]]
    return needs_items(player, jewel_list)


def set_access_rules(multiworld: MultiWorld, player: int):
    location_rules = difficulty_location_rules[multiworld.difficulty[player].value]
    for name, items in location_rules.items():
        try:
            location = multiworld.get_location(name, player)
            location.access_rule = needs_items(player, items)
        except KeyError as k:
            # Raise for invalid location names, not ones that aren't in this player's world
            if name not in w4_locations:
                raise ValueError(f'Location {name} does not exist') from k


escape_regions = {
    'Hall of Hieroglyphs':    None,

    'Palm Tree Paradise':     None,
    'Wildflower Fields':     'After Sunflower',
    'Mystic Lake':           'Depths',
    'Monsoon Jungle':        'Lower',

    'The Curious Factory':    None,
    'The Toxic Landfill':     None,
    '40 Below Fridge':        None,
    'Pinball Zone':          'Escape',

    'Toy Block Tower':        None,
    'The Big Board':          None,
    'Doodle Woods':           None,
    'Domino Row':            'After Lake',

    'Crescent Moon Village': 'Lower',
    'Fiery Cavern':          'Frozen',
}

keyzer_regions = {
    **escape_regions,
    'Arabian Night':         'Town',
    'Hotel Horror':          'Hotel',
    'Golden Passage':        'Keyzer Area',
}

frog_switch_regions = {
    **escape_regions,
    'Arabian Night':         'Sewer',
    'Hotel Horror':          'Switch Room',
    'Golden Passage':        'Passage',
}


# Regions are linear, so each region from the same level adds to the previous
region_rules = {
    'Hall of Hieroglyphs':                  [['Dash Attack', 'Grab', 'Super Ground Pound']],

    'Palm Tree Paradise':                     None,
    'Wildflower Fields - Before Sunflower':   None,
    'Wildflower Fields - After Sunflower':  [['Super Ground Pound', 'Swim']],
    'Mystic Lake - Shore':                    None,
    'Mystic Lake - Shallows':               [['Swim']],
    'Mystic Lake - Depths':                 [['Head Smash']],
    'Monsoon Jungle - Upper':                 None,
    'Monsoon Jungle - Lower':               [['Ground Pound']],

    'The Curious Factory':                    None,
    'The Toxic Landfill':                   [['Dash Attack', 'Super Ground Pound', 'Head Smash']],
    '40 Below Fridge':                      [['Super Ground Pound']],
    'Pinball Zone - Early Rooms':           [['Grab']],
    'Pinball Zone - Late Rooms':            [['Ground Pound']],
    'Pinball Zone - Escape':                [['Head Smash']],

    'Toy Block Tower':                      [['Heavy Grab']],
    'The Big Board':                        [['Ground Pound']],
    'Doodle Woods':                           None,
    'Domino Row - Before Lake':               None,
    # Note: You can also open the way to the exit by throwing a Toy Car across
    # the green room, but that feels obscure enough that I should just ignore it
    'Domino Row - After Lake':              [['Swim', 'Ground Pound'], ['Swim', 'Head Smash']],

    'Crescent Moon Village - Upper':        [['Head Smash']],
    'Crescent Moon Village - Lower':        [['Dash Attack']],
    'Arabian Night - Town':                   None,
    'Arabian Night - Sewer':                [['Swim']],
    'Fiery Cavern - Flaming':                 None,
    'Fiery Cavern - Frozen':                [['Ground Pound', 'Dash Attack', 'Head Smash']],
    'Hotel Horror - Hotel':                   None,
    'Hotel Horror - Switch Room':           [['Heavy Grab']],

    'Golden Passage - Passage':             [['Swim']],
    'Golden Passage - Keyzer Area':         [['Ground Pound', 'Grab']],
}


location_rules_all = {
    'Cractus':       [['Ground Pound']],
    'Cuckoo Condor': [['Grab']],
    'Aerodent':      [['Grab']],
    'Catbat':        [['Ground Pound']],
    'Golden Diva':   [['Grab']],

    'Mystic Lake - Large Cave Box':                   [['Head Smash']],
    'Mystic Lake - Small Cave Box':                   [['Dash Attack']],
    'Mystic Lake - Rock Cave Box':                    [['Grab']],
    'Mystic Lake - CD Box':                           [['Dash Attack']],
    'Monsoon Jungle - Puffy Hallway Box':             [['Dash Attack']],
    'Monsoon Jungle - Full Health Item Box':          [['Swim']],
    'Monsoon Jungle - CD Box':                        [['Ground Pound']],

    'The Curious Factory - Gear Elevator Box':        [['Dash Attack']],
    'The Toxic Landfill - Current Circle Box':        [['Swim']],
    'The Toxic Landfill - Transformation Puzzle Box': [['Heavy Grab'], ['Enemy Jump']],
    '40 Below Fridge - CD Box':                       [['Head Smash']],
    'Pinball Zone - Full Health Item Box':            [['Super Ground Pound']],
    'Pinball Zone - Pink Room Full Health Item Box':  [['Super Ground Pound']],

    'Toy Block Tower - Digging Room Box':             [['Dash Attack']],
    'Toy Block Tower - Full Health Item Box':         [['Dash Attack']],
    'The Big Board - Hard Enemy Room Box':            [['Grab']],
    'The Big Board - Full Health Item Box':           [['Grab', 'Enemy Jump']],
    'Doodle Woods - Blue Circle Box':                 [['Enemy Jump']],
    'Doodle Woods - Pink Circle Box':                 [['Ground Pound']],
    'Doodle Woods - Gray Square Box':                 [['Ground Pound']],
    'Domino Row - Keyzer Room Box':                   [['Ground Pound']],

    'Crescent Moon Village - Agile Bat Hidden Box':   [['Ground Pound', 'Grab']],
    'Crescent Moon Village - Sewer Box':              [['Swim']],
    'Arabian Night - Flying Carpet Dash Attack Box':  [['Dash Attack']],
    'Arabian Night - Kool-Aid Box':                   [['Dash Attack']],

    'Golden Passage - Mad Scienstein Box':            [['Ground Pound']],
}


location_rules_normal = {
    **location_rules_all,

    'Mystic Lake - Full Health Item Box': [['Grab']],
    'Doodle Woods - CD Box':              [['Ground Pound']],
    'Domino Row - Swimming Detour Box':   [['Head Smash']],
}

location_rules_hard = {
    **location_rules_all,

    'Wildflower Fields - 8-Shaped Cave Box': [['Super Ground Pound', 'Grab']],
    'Mystic Lake - Full Health Item Box':    [['Grab']],
    'Monsoon Jungle - Fat Plummet Box':      [['Ground Pound']],
    'Monsoon Jungle - Buried Cave Box':      [['Grab']],

    'Domino Row - Swimming Detour Box':      [['Head Smash']],

    'Arabian Night - Onomi Box':             [['Ground Pound'], ['Head Smash']],
    'Arabian Night - Sewer Box':             [['Super Ground Pound']],
}

location_rules_s_hard = {
    **location_rules_all,

    'Wildflower Fields - 8-Shaped Cave Box': [['Super Ground Pound', 'Heavy Grab']],
    'Mystic Lake - Rock Cave Box':           [['Grab']],
    # HACK: It should be in the depths, but I don't have handling for this
    # box's region varying with difficulty
    'Mystic Lake - Full Health Item Box':    [['Swim', 'Head Smash', 'Dash Attack']],
    'Monsoon Jungle - Fat Plummet Box':      [['Ground Pound']],
    'Monsoon Jungle - Buried Cave Box':      [['Grab']],

    'Arabian Night - Onomi Box':             [['Ground Pound'], ['Head Smash']],
    'Arabian Night - Sewer Box':             [['Super Ground Pound']],
}

difficulty_location_rules = (
    location_rules_normal,
    location_rules_hard,
    location_rules_s_hard,
)
