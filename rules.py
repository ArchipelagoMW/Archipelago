from __future__ import annotations

import functools
from typing import Callable, Mapping, NamedTuple, Optional, Sequence, Tuple, Union, TYPE_CHECKING

from BaseClasses import CollectionState
from Options import Option

from . import items, locations, options
from .types import ItemType, Passage

if TYPE_CHECKING:
    from . import WL4World


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


class Requirement(NamedTuple):
    inner: Callable[[WL4World, CollectionState], bool]

    def __or__(self, rhs: Requirement):
        return Requirement(lambda w, s: self.inner(w, s) or rhs.inner(w, s))

    def __and__(self, rhs: Requirement):
        return Requirement(lambda w, s: self.inner(w, s) and rhs.inner(w, s))

    def apply_world(self, world: WL4World):
        return functools.partial(self.inner, world)


def has(item_name: str) -> Requirement:
    item, count = resolve_helper(item_name)
    return Requirement(lambda w, s: s.has(item, w.player, count))

def has_all(items: Sequence[str]) -> Requirement:
    return Requirement(lambda w, s: all(has(item).inner(w, s) for item in items))

def has_any(items: Sequence[str]) -> Requirement:
    return Requirement(lambda w, s: any(has(item).inner(w, s) for item in items))


def option(option_name: str, choice: Option):
    return Requirement(lambda w, _: getattr(w.options, option_name) == choice)

def difficulty(difficulty: options.Difficulty):
    return option('difficulty', difficulty)

def logic(logic: options.Logic):
    return option('logic', logic)


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


def get_access_rule(world: WL4World, region_name: str):
    rule = region_rules[region_name]
    if rule is None:
        return None
    return rule.apply_world(world)


def make_boss_access_rule(world: WL4World, passage: Passage, jewels_needed: int):
    jewel_list = [(name, jewels_needed)
                  for name in items.filter_item_names(type=ItemType.JEWEL, passage=passage)]
    return has_all(jewel_list).apply_world(world)


def set_access_rules(world: WL4World):
    for name, rule in location_rules.items():
        try:
            location = world.multiworld.get_location(name, world.player)
            location.access_rule = rule.apply_world(world)
        except KeyError as k:
            # Raise for invalid location names, not ones that aren't in this player's world
            if name not in locations.location_table:
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


normal = options.Difficulty.option_normal
hard = options.Difficulty.option_hard
s_hard = options.Difficulty.option_s_hard
basic = options.Logic.option_basic
advanced = options.Logic.option_advanced


# Regions are linear, so each region from the same level adds to the previous
region_rules: Mapping[str, Requirement] = {
    'Hall of Hieroglyphs':                  has_all(['Dash Attack', 'Grab', 'Super Ground Pound']),

    'Palm Tree Paradise':                   None,
    'Wildflower Fields - Before Sunflower': None,
    'Wildflower Fields - After Sunflower':  has_all(['Super Ground Pound', 'Swim']),
    'Mystic Lake - Shore':                  None,
    'Mystic Lake - Shallows':               has('Swim'),
    'Mystic Lake - Depths':                 has('Head Smash'),
    'Monsoon Jungle - Upper':               None,
    'Monsoon Jungle - Lower':               has('Ground Pound'),

    'The Curious Factory':                  None,
    'The Toxic Landfill':                   has_all(['Dash Attack', 'Super Ground Pound', 'Head Smash']),
    '40 Below Fridge':                      has('Super Ground Pound'),
    'Pinball Zone - Early Rooms':           has('Grab'),
    'Pinball Zone - Jungle Room':           has('Ground Pound') | logic(advanced),
    'Pinball Zone - Late Rooms':            has('Ground Pound') | logic(advanced) & has('Heavy Grab'),
    'Pinball Zone - Escape':                has_all(['Ground Pound', 'Head Smash']),

    'Toy Block Tower':                      has('Heavy Grab'),
    'The Big Board':                        has('Ground Pound'),
    'Doodle Woods':                         None,
    'Domino Row - Before Lake':             None,
    'Domino Row - After Lake':
            has('Swim') & (has('Ground Pound') | logic(advanced) & has_any(['Head Smash', 'Grab'])),
    'Crescent Moon Village - Upper':        has('Head Smash'),
    'Crescent Moon Village - Lower':        has('Dash Attack'),
    'Arabian Night - Town':                 None,
    'Arabian Night - Sewer':                has('Swim'),
    'Fiery Cavern - Flaming':               None,
    'Fiery Cavern - Frozen':                has_all(['Ground Pound', 'Dash Attack', 'Head Smash']),
    'Hotel Horror - Hotel':                 None,
    'Hotel Horror - Switch Room':           has('Heavy Grab') | difficulty(s_hard),

    'Golden Passage - Passage':             has('Swim'),
    'Golden Passage - Keyzer Area':         has_all(['Ground Pound', 'Grab']),
}


location_rules: Mapping[str, Requirement] = {
    'Cractus':       has('Ground Pound'),
    'Cuckoo Condor': has('Grab'),
    'Aerodent':      has('Grab'),
    'Catbat':        has('Ground Pound') & (has('Enemy Jump') | logic(advanced)),
    'Golden Diva':   has('Grab'),

    'Wildflower Fields - 8-Shaped Cave Box':
            has('Super Ground Pound') & ((difficulty(hard) & has('Grab')) | (difficulty(s_hard) & has('Heavy Grab'))),
    'Mystic Lake - Large Cave Box':                   has('Head Smash'),
    'Mystic Lake - Small Cave Box':                   has('Dash Attack'),
    'Mystic Lake - Rock Cave Box':                    has('Grab'),
    'Mystic Lake - CD Box':                           has('Dash Attack'),
    # HACK: It should be in the depths on S-Hard, but I don't have handling for
    # this box's region varying with difficulty
    'Mystic Lake - Full Health Item Box':
            ((difficulty(normal) | difficulty(hard)) & has('Grab')) |
            (difficulty(s_hard) & has_all(['Swim', 'Head Smash', 'Dash Attack'])),
    'Monsoon Jungle - Fat Plummet Box':
            difficulty(normal) | (difficulty(hard) | difficulty(s_hard)) & has('Ground Pound'),
    'Monsoon Jungle - Buried Cave Box':
            difficulty(normal) | (difficulty(hard) | difficulty(s_hard)) & has('Grab'),
    'Monsoon Jungle - Puffy Hallway Box':             has('Dash Attack'),
    'Monsoon Jungle - Full Health Item Box':          has('Swim'),
    'Monsoon Jungle - CD Box':                        has('Ground Pound'),

    'The Curious Factory - Gear Elevator Box':        has('Dash Attack'),
    'The Toxic Landfill - Current Circle Box':        has('Swim'),
    'The Toxic Landfill - Transformation Puzzle Box': has_any(['Heavy Grab', 'Enemy Jump']),
    '40 Below Fridge - CD Box':                       has('Head Smash'),
    'Pinball Zone - Full Health Item Box':            has('Super Ground Pound'),
    'Pinball Zone - Pink Room Full Health Item Box':  has('Super Ground Pound'),

    'Toy Block Tower - Digging Room Box':             has('Dash Attack'),
    'Toy Block Tower - Full Health Item Box':         has('Dash Attack'),
    'The Big Board - Hard Enemy Room Box':            has('Grab'),
    'The Big Board - Full Health Item Box':           has_all(['Grab', 'Enemy Jump']),
    'Doodle Woods - Blue Circle Box':                 has('Enemy Jump'),
    'Doodle Woods - Pink Circle Box':                 has('Ground Pound'),
    'Doodle Woods - Gray Square Box':
            has('Ground Pound') | logic(advanced) & has('Grab'),
    'Doodle Woods - CD Box':
            difficulty(normal) & (has('Ground Pound') | logic(advanced) & has('Grab')) |
            difficulty(hard) | difficulty(s_hard),
    'Domino Row - Swimming Detour Box':               has('Head Smash'),
    'Domino Row - Swimming Room Escape Box':          has('Ground Pound'),
    'Domino Row - Keyzer Room Box':                   has('Ground Pound'),

    'Crescent Moon Village - Agile Bat Hidden Box':   has_all(['Ground Pound', 'Grab']),
    'Crescent Moon Village - Sewer Box':              has('Swim'),
    'Arabian Night - Onomi Box':
            difficulty(normal) | (difficulty(hard) | difficulty(s_hard)) & has_any(['Ground Pound', 'Head Smash']),
    'Arabian Night - Sewer Box':
            difficulty(normal) | ((difficulty(hard) | difficulty(s_hard)) & has('Super Ground Pound')),
    'Arabian Night - Flying Carpet Dash Attack Box':  has('Dash Attack'),
    'Arabian Night - Kool-Aid Box':                   has('Dash Attack'),

    'Golden Passage - Mad Scienstein Box':            has('Ground Pound'),
}
