from typing import NamedTuple, Optional, Sequence, Tuple, Union

from BaseClasses import Location, MultiWorld, Region

from .data import ap_id_offset
from .types import Difficulty, ItemFlag, LocationType, Passage


class LocationData(NamedTuple):
    source: LocationType
    status_bit: Tuple[Passage, int, ItemFlag]
    region_in_level: Optional[str]
    difficulties: Sequence[Difficulty]

    def passage(self):
        return self.status_bit[0]

    def level(self):
        return self.status_bit[1]

    def flag(self):
        return self.status_bit[2]

    def level_id(self):
        return self.status_bit[0:2]


_NORMAL = (Difficulty.NORMAL,)
_HARD = (Difficulty.HARD,)
_S_HARD = (Difficulty.S_HARD,)
_EASIER = (Difficulty.NORMAL, Difficulty.HARD)
_HARDER = (Difficulty.HARD, Difficulty.S_HARD)
_ALL = (Difficulty.NORMAL, Difficulty.HARD, Difficulty.S_HARD)


    # Location                                                         Source              Passage        Level  Bit in level data       Region              Difficulties
location_table = {
    # Entry Passage
    # Hall of Hieroglyphs
    'Hall of Hieroglyphs - First Jewel Box':              LocationData(LocationType.BOX,  (Passage.ENTRY,    0, ItemFlag.JEWEL_NE),       None,              _ALL),
    'Hall of Hieroglyphs - Second Jewel Box':             LocationData(LocationType.BOX,  (Passage.ENTRY,    0, ItemFlag.JEWEL_SE),       None,              _ALL),
    'Hall of Hieroglyphs - Third Jewel Box':              LocationData(LocationType.BOX,  (Passage.ENTRY,    0, ItemFlag.JEWEL_SW),       None,              _ALL),
    'Hall of Hieroglyphs - Fourth Jewel Box':             LocationData(LocationType.BOX,  (Passage.ENTRY,    0, ItemFlag.JEWEL_NW),       None,              _ALL),
    'Hall of Hieroglyphs - Full Health Item Box':         LocationData(LocationType.BOX,  (Passage.ENTRY,    0, ItemFlag.FULL_HEALTH),    None,              _ALL),

    'Spoiled Rotten':                                     LocationData(LocationType.BOSS, (Passage.ENTRY,    4, ItemFlag.KEYZER),         None,              _ALL),

    # Emerald Passage
    # Palm Tree Paradise
    'Palm Tree Paradise - First Box':                     LocationData(LocationType.BOX,  (Passage.EMERALD,  0, ItemFlag.JEWEL_NE),       None,              _NORMAL),
    'Palm Tree Paradise - Ledge Box':                     LocationData(LocationType.BOX,  (Passage.EMERALD,  0, ItemFlag.JEWEL_NE),       None,              _HARD),
    'Palm Tree Paradise - Dead End Box':                  LocationData(LocationType.BOX,  (Passage.EMERALD,  0, ItemFlag.JEWEL_NE),       None,              _S_HARD),
    'Palm Tree Paradise - Box Before Cave':               LocationData(LocationType.BOX,  (Passage.EMERALD,  0, ItemFlag.JEWEL_SE),       None,              _NORMAL),
    'Palm Tree Paradise - Hidden Box':                    LocationData(LocationType.BOX,  (Passage.EMERALD,  0, ItemFlag.JEWEL_SE),       None,              _HARDER),
    'Palm Tree Paradise - Platform Cave Jewel Box':       LocationData(LocationType.BOX,  (Passage.EMERALD,  0, ItemFlag.JEWEL_SW),       None,              _ALL),
    'Palm Tree Paradise - Ladder Cave Box':               LocationData(LocationType.BOX,  (Passage.EMERALD,  0, ItemFlag.JEWEL_NW),       None,              _ALL),
    'Palm Tree Paradise - CD Box':                        LocationData(LocationType.BOX,  (Passage.EMERALD,  0, ItemFlag.CD),             None,              _ALL),
    'Palm Tree Paradise - Full Health Item Box':          LocationData(LocationType.BOX,  (Passage.EMERALD,  0, ItemFlag.FULL_HEALTH),    None,              _ALL),

    # Wildflower Fields
    'Wildflower Fields - Current Cave Box':               LocationData(LocationType.BOX,  (Passage.EMERALD,  1, ItemFlag.JEWEL_NE),      'After Sunflower',  _ALL),
    'Wildflower Fields - Sunflower Jewel Box':            LocationData(LocationType.BOX,  (Passage.EMERALD,  1, ItemFlag.JEWEL_SE),      'After Sunflower',  _NORMAL),
    'Wildflower Fields - Sunflower Box':                  LocationData(LocationType.BOX,  (Passage.EMERALD,  1, ItemFlag.JEWEL_SE),      'After Sunflower',  _HARDER),
    'Wildflower Fields - Slope Room Box':                 LocationData(LocationType.BOX,  (Passage.EMERALD,  1, ItemFlag.JEWEL_SW),      'After Sunflower',  _NORMAL),
    'Wildflower Fields - 8-Shaped Cave Box':              LocationData(LocationType.BOX,  (Passage.EMERALD,  1, ItemFlag.JEWEL_SW),      'Before Sunflower', _HARDER),
    'Wildflower Fields - Beezley Box':                    LocationData(LocationType.BOX,  (Passage.EMERALD,  1, ItemFlag.JEWEL_NW),      'After Sunflower',  _ALL),
    'Wildflower Fields - CD Box':                         LocationData(LocationType.BOX,  (Passage.EMERALD,  1, ItemFlag.CD),            'Before Sunflower', _ALL),
    'Wildflower Fields - Full Health Item Box':           LocationData(LocationType.BOX,  (Passage.EMERALD,  1, ItemFlag.FULL_HEALTH),   'After Sunflower',  _NORMAL),

    # Mystic Lake
    'Mystic Lake - Air Pocket Box':                       LocationData(LocationType.BOX,  (Passage.EMERALD,  2, ItemFlag.JEWEL_NE),      'Shallows',         _NORMAL),
    'Mystic Lake - Large Cave Box':                       LocationData(LocationType.BOX,  (Passage.EMERALD,  2, ItemFlag.JEWEL_NE),      'Shallows',         _HARDER),
    'Mystic Lake - Hill Room Box':                        LocationData(LocationType.BOX,  (Passage.EMERALD,  2, ItemFlag.JEWEL_SE),      'Depths',           _NORMAL),
    'Mystic Lake - Small Cave Box':                       LocationData(LocationType.BOX,  (Passage.EMERALD,  2, ItemFlag.JEWEL_SE),      'Depths',           _HARD),
    'Mystic Lake - Rock Cave Box':                        LocationData(LocationType.BOX,  (Passage.EMERALD,  2, ItemFlag.JEWEL_SE),      'Shore',            _S_HARD),
    'Mystic Lake - Cavern Box':                           LocationData(LocationType.BOX,  (Passage.EMERALD,  2, ItemFlag.JEWEL_SW),      'Depths',           _NORMAL),
    'Mystic Lake - Spring Cave Box':                      LocationData(LocationType.BOX,  (Passage.EMERALD,  2, ItemFlag.JEWEL_SW),      'Depths',           _HARDER),
    'Mystic Lake - Box Before Bridge':                    LocationData(LocationType.BOX,  (Passage.EMERALD,  2, ItemFlag.JEWEL_NW),      'Depths',           _NORMAL),
    'Mystic Lake - Lake Exit Bubble Box':                 LocationData(LocationType.BOX,  (Passage.EMERALD,  2, ItemFlag.JEWEL_NW),      'Depths',           _HARDER),
    'Mystic Lake - CD Box':                               LocationData(LocationType.BOX,  (Passage.EMERALD,  2, ItemFlag.CD),            'Depths',           _ALL),
    'Mystic Lake - Full Health Item Box':                 LocationData(LocationType.BOX,  (Passage.EMERALD,  2, ItemFlag.FULL_HEALTH),   'Shore',            _ALL),

    # Monsoon Jungle
    'Monsoon Jungle - Spiky Box':                         LocationData(LocationType.BOX,  (Passage.EMERALD,  3, ItemFlag.JEWEL_NE),      'Lower',            _NORMAL),
    'Monsoon Jungle - Escape Climb Box':                  LocationData(LocationType.BOX,  (Passage.EMERALD,  3, ItemFlag.JEWEL_NE),      'Lower',            _HARD),
    'Monsoon Jungle - Brown Pipe Cave Box':               LocationData(LocationType.BOX,  (Passage.EMERALD,  3, ItemFlag.JEWEL_NE),      'Lower',            _S_HARD),
    'Monsoon Jungle - Fat Plummet Box':                   LocationData(LocationType.BOX,  (Passage.EMERALD,  3, ItemFlag.JEWEL_SE),      'Upper',            _ALL),
    'Monsoon Jungle - Descent Box':                       LocationData(LocationType.BOX,  (Passage.EMERALD,  3, ItemFlag.JEWEL_SW),      'Lower',            _NORMAL),
    'Monsoon Jungle - Puffy Hallway Box':                 LocationData(LocationType.BOX,  (Passage.EMERALD,  3, ItemFlag.JEWEL_SW),      'Lower',            _HARDER),
    'Monsoon Jungle - Buried Cave Box':                   LocationData(LocationType.BOX,  (Passage.EMERALD,  3, ItemFlag.JEWEL_NW),      'Lower',            _ALL),
    'Monsoon Jungle - CD Box':                            LocationData(LocationType.BOX,  (Passage.EMERALD,  3, ItemFlag.CD),            'Upper',            _ALL),
    'Monsoon Jungle - Full Health Item Box':              LocationData(LocationType.BOX,  (Passage.EMERALD,  3, ItemFlag.FULL_HEALTH),   'Upper',            _ALL),

    'Cractus':                                            LocationData(LocationType.BOSS, (Passage.EMERALD,  4, ItemFlag.KEYZER),         None,              _ALL),

    # Ruby Passage
    # The Curious Factory
    'The Curious Factory - First Drop Box':               LocationData(LocationType.BOX,  (Passage.RUBY,     0, ItemFlag.JEWEL_NE),       None,              _NORMAL),
    'The Curious Factory - Thin Gap Box':                 LocationData(LocationType.BOX,  (Passage.RUBY,     0, ItemFlag.JEWEL_NE),       None,              _HARDER),
    'The Curious Factory - Early Escape Box':             LocationData(LocationType.BOX,  (Passage.RUBY,     0, ItemFlag.JEWEL_SE),       None,              _NORMAL),
    'The Curious Factory - Conveyor Room Box':            LocationData(LocationType.BOX,  (Passage.RUBY,     0, ItemFlag.JEWEL_SE),       None,              _HARDER),
    'The Curious Factory - Late Escape Box':              LocationData(LocationType.BOX,  (Passage.RUBY,     0, ItemFlag.JEWEL_SW),       None,              _NORMAL),
    'The Curious Factory - Underground Chamber Box':      LocationData(LocationType.BOX,  (Passage.RUBY,     0, ItemFlag.JEWEL_SW),       None,              _HARDER),
    'The Curious Factory - Frog Switch Room Box':         LocationData(LocationType.BOX,  (Passage.RUBY,     0, ItemFlag.JEWEL_NW),       None,              _NORMAL),
    'The Curious Factory - Gear Elevator Box':            LocationData(LocationType.BOX,  (Passage.RUBY,     0, ItemFlag.JEWEL_NW),       None,              _HARDER),
    'The Curious Factory - CD Box':                       LocationData(LocationType.BOX,  (Passage.RUBY,     0, ItemFlag.CD),             None,              _ALL),

    # The Toxic Landfill
    'The Toxic Landfill - Portal Room Box':               LocationData(LocationType.BOX,  (Passage.RUBY,     1, ItemFlag.JEWEL_NE),       None,              _NORMAL),
    'The Toxic Landfill - Box Above Portal':              LocationData(LocationType.BOX,  (Passage.RUBY,     1, ItemFlag.JEWEL_NE),       None,              _HARDER),
    'The Toxic Landfill - Fat Room Box':                  LocationData(LocationType.BOX,  (Passage.RUBY,     1, ItemFlag.JEWEL_SE),       None,              _ALL),
    'The Toxic Landfill - Spring Room Box':               LocationData(LocationType.BOX,  (Passage.RUBY,     1, ItemFlag.JEWEL_SW),       None,              _NORMAL),
    'The Toxic Landfill - Current Circle Box':            LocationData(LocationType.BOX,  (Passage.RUBY,     1, ItemFlag.JEWEL_SW),       None,              _HARDER),
    'The Toxic Landfill - Ledge Box':                     LocationData(LocationType.BOX,  (Passage.RUBY,     1, ItemFlag.JEWEL_NW),       None,              _NORMAL),
    'The Toxic Landfill - Transformation Puzzle Box':     LocationData(LocationType.BOX,  (Passage.RUBY,     1, ItemFlag.JEWEL_NW),       None,              _HARDER),
    'The Toxic Landfill - CD Box':                        LocationData(LocationType.BOX,  (Passage.RUBY,     1, ItemFlag.CD),             None,              _ALL),
    'The Toxic Landfill - Full Health Item Box':          LocationData(LocationType.BOX,  (Passage.RUBY,     1, ItemFlag.FULL_HEALTH),    None,              _NORMAL),

    # 40 Below Fridge
    '40 Below Fridge - Looping Room Box':                 LocationData(LocationType.BOX,  (Passage.RUBY,     2, ItemFlag.JEWEL_NE),       None,              _ALL),
    '40 Below Fridge - Maze Room Box':                    LocationData(LocationType.BOX,  (Passage.RUBY,     2, ItemFlag.JEWEL_SE),       None,              _ALL),
    '40 Below Fridge - Snowman Puzzle Upper Box':         LocationData(LocationType.BOX,  (Passage.RUBY,     2, ItemFlag.JEWEL_SW),       None,              _ALL),
    '40 Below Fridge - Snowman Puzzle Lower Box':         LocationData(LocationType.BOX,  (Passage.RUBY,     2, ItemFlag.JEWEL_NW),       None,              _ALL),
    '40 Below Fridge - CD Box':                           LocationData(LocationType.BOX,  (Passage.RUBY,     2, ItemFlag.CD),             None,              _ALL),

    # Pinball Zone
    'Pinball Zone - Rolling Room Box':                    LocationData(LocationType.BOX,  (Passage.RUBY,     3, ItemFlag.JEWEL_NE),      'Early Rooms',      _EASIER),
    'Pinball Zone - Switch Room Box':                     LocationData(LocationType.BOX,  (Passage.RUBY,     3, ItemFlag.JEWEL_NE),      'Late Rooms',       _S_HARD),
    'Pinball Zone - Fruit Room Box':                      LocationData(LocationType.BOX,  (Passage.RUBY,     3, ItemFlag.JEWEL_SE),      'Early Rooms',      _ALL),
    'Pinball Zone - Jungle Room Box':                     LocationData(LocationType.BOX,  (Passage.RUBY,     3, ItemFlag.JEWEL_SW),      'Late Rooms',       _ALL),
    'Pinball Zone - Snow Room Box':                       LocationData(LocationType.BOX,  (Passage.RUBY,     3, ItemFlag.JEWEL_NW),      'Late Rooms',       _ALL),
    'Pinball Zone - CD Box':                              LocationData(LocationType.BOX,  (Passage.RUBY,     3, ItemFlag.CD),            'Late Rooms',       _ALL),
    'Pinball Zone - Full Health Item Box':                LocationData(LocationType.BOX,  (Passage.RUBY,     3, ItemFlag.FULL_HEALTH),   'Late Rooms',       _EASIER),
    'Pinball Zone - Pink Room Full Health Item Box':      LocationData(LocationType.BOX,  (Passage.RUBY,     3, ItemFlag.FULL_HEALTH),   'Late Rooms',       _S_HARD),
    'Pinball Zone - Rolling Room Full Health Item Box':   LocationData(LocationType.BOX,  (Passage.RUBY,     3, ItemFlag.FULL_HEALTH_2), 'Early Rooms',      _S_HARD),

    'Cuckoo Condor':                                      LocationData(LocationType.BOSS, (Passage.RUBY,     4, ItemFlag.KEYZER),         None,              _ALL),

    # Topaz Passage
    # Toy Block Tower
    'Toy Block Tower - Toy Car Overhang Box':             LocationData(LocationType.BOX,  (Passage.TOPAZ,    0, ItemFlag.JEWEL_NE),       None,              _EASIER),
    'Toy Block Tower - Tower Exterior Top Box':           LocationData(LocationType.BOX,  (Passage.TOPAZ,    0, ItemFlag.JEWEL_NE),       None,              _S_HARD),
    'Toy Block Tower - Hidden Tower Room Box':            LocationData(LocationType.BOX,  (Passage.TOPAZ,    0, ItemFlag.JEWEL_SE),       None,              _NORMAL),
    'Toy Block Tower - Digging Room Box':                 LocationData(LocationType.BOX,  (Passage.TOPAZ,    0, ItemFlag.JEWEL_SE),       None,              _HARDER),
    'Toy Block Tower - Fire Box':                         LocationData(LocationType.BOX,  (Passage.TOPAZ,    0, ItemFlag.JEWEL_SW),       None,              _NORMAL),
    'Toy Block Tower - Hidden Falling Block Door Box':    LocationData(LocationType.BOX,  (Passage.TOPAZ,    0, ItemFlag.JEWEL_SW),       None,              _HARD),
    'Toy Block Tower - Bonfire Block Box':                LocationData(LocationType.BOX,  (Passage.TOPAZ,    0, ItemFlag.JEWEL_SW),       None,              _S_HARD),
    'Toy Block Tower - Red Pipe Box':                     LocationData(LocationType.BOX,  (Passage.TOPAZ,    0, ItemFlag.JEWEL_NW),       None,              _NORMAL),
    'Toy Block Tower - Escape Ledge Box':                 LocationData(LocationType.BOX,  (Passage.TOPAZ,    0, ItemFlag.JEWEL_NW),       None,              _HARDER),
    'Toy Block Tower - CD Box':                           LocationData(LocationType.BOX,  (Passage.TOPAZ,    0, ItemFlag.CD),             None,              _ALL),
    'Toy Block Tower - Full Health Item Box':             LocationData(LocationType.BOX,  (Passage.TOPAZ,    0, ItemFlag.FULL_HEALTH),    None,              _EASIER),

    # The Big Board
    'The Big Board - First Box':                          LocationData(LocationType.BOX,  (Passage.TOPAZ,    1, ItemFlag.JEWEL_NE),       None,              _NORMAL),
    'The Big Board - Hard Fire Room Box':                 LocationData(LocationType.BOX,  (Passage.TOPAZ,    1, ItemFlag.JEWEL_NE),       None,              _HARDER),
    'The Big Board - Normal Fire Room Box':               LocationData(LocationType.BOX,  (Passage.TOPAZ,    1, ItemFlag.JEWEL_SE),       None,              _NORMAL),
    'The Big Board - Hard Enemy Room Box':                LocationData(LocationType.BOX,  (Passage.TOPAZ,    1, ItemFlag.JEWEL_SE),       None,              _HARDER),
    'The Big Board - Normal Enemy Room Box':              LocationData(LocationType.BOX,  (Passage.TOPAZ,    1, ItemFlag.JEWEL_SW),       None,              _NORMAL),
    'The Big Board - Fat Room Box':                       LocationData(LocationType.BOX,  (Passage.TOPAZ,    1, ItemFlag.JEWEL_SW),       None,              _HARDER),
    'The Big Board - Toy Car Box':                        LocationData(LocationType.BOX,  (Passage.TOPAZ,    1, ItemFlag.JEWEL_NW),       None,              _NORMAL),
    'The Big Board - Flat Room Box':                      LocationData(LocationType.BOX,  (Passage.TOPAZ,    1, ItemFlag.JEWEL_NW),       None,              _HARDER),
    'The Big Board - CD Box':                             LocationData(LocationType.BOX,  (Passage.TOPAZ,    1, ItemFlag.CD),             None,              _ALL),
    'The Big Board - Full Health Item Box':               LocationData(LocationType.BOX,  (Passage.TOPAZ,    1, ItemFlag.FULL_HEALTH),    None,              _EASIER),

    # Doodle Woods
    'Doodle Woods - Box Behind Wall':                     LocationData(LocationType.BOX,  (Passage.TOPAZ,    2, ItemFlag.JEWEL_NE),       None,              _NORMAL),
    'Doodle Woods - Gray Square Box':                     LocationData(LocationType.BOX,  (Passage.TOPAZ,    2, ItemFlag.JEWEL_NE),       None,              _HARDER),
    'Doodle Woods - Orange Escape Box':                   LocationData(LocationType.BOX,  (Passage.TOPAZ,    2, ItemFlag.JEWEL_SE),       None,              _NORMAL),
    'Doodle Woods - Pink Circle Box':                     LocationData(LocationType.BOX,  (Passage.TOPAZ,    2, ItemFlag.JEWEL_SE),       None,              _HARDER),
    'Doodle Woods - Buried Door Box':                     LocationData(LocationType.BOX,  (Passage.TOPAZ,    2, ItemFlag.JEWEL_SW),       None,              _NORMAL),
    'Doodle Woods - Purple Square Box':                   LocationData(LocationType.BOX,  (Passage.TOPAZ,    2, ItemFlag.JEWEL_SW),       None,              _HARDER),
    'Doodle Woods - Blue Escape Box':                     LocationData(LocationType.BOX,  (Passage.TOPAZ,    2, ItemFlag.JEWEL_NW),       None,              _NORMAL),
    'Doodle Woods - Blue Circle Box':                     LocationData(LocationType.BOX,  (Passage.TOPAZ,    2, ItemFlag.JEWEL_NW),       None,              _HARDER),
    'Doodle Woods - CD Box':                              LocationData(LocationType.BOX,  (Passage.TOPAZ,    2, ItemFlag.CD),             None,              _ALL),

    # Domino Row
    'Domino Row - Racing Box':                            LocationData(LocationType.BOX,  (Passage.TOPAZ,    3, ItemFlag.JEWEL_NE),      'Before Lake',      _ALL),
    'Domino Row - Rolling Box':                           LocationData(LocationType.BOX,  (Passage.TOPAZ,    3, ItemFlag.JEWEL_SE),      'After Lake',       _ALL),
    'Domino Row - Swimming Detour Box':                   LocationData(LocationType.BOX,  (Passage.TOPAZ,    3, ItemFlag.JEWEL_SW),      'After Lake',       _EASIER),
    'Domino Row - Swimming Room Escape Box':              LocationData(LocationType.BOX,  (Passage.TOPAZ,    3, ItemFlag.JEWEL_SW),      'After Lake',       _S_HARD),
    'Domino Row - Keyzer Room Box':                       LocationData(LocationType.BOX,  (Passage.TOPAZ,    3, ItemFlag.JEWEL_NW),      'After Lake',       _ALL),
    'Domino Row - CD Box':                                LocationData(LocationType.BOX,  (Passage.TOPAZ,    3, ItemFlag.CD),            'After Lake',       _ALL),

    'Aerodent':                                           LocationData(LocationType.BOSS, (Passage.TOPAZ,    4, ItemFlag.KEYZER),         None,              _ALL),

    # Sapphire Passage
    # Crescent Moon Village
    'Crescent Moon Village - Agile Bat Box':              LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 0, ItemFlag.JEWEL_NE),      'Upper',            _NORMAL),
    'Crescent Moon Village - Agile Bat Hidden Box':       LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 0, ItemFlag.JEWEL_NE),      'Upper',            _HARDER),
    'Crescent Moon Village - Metal Platform Box':         LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 0, ItemFlag.JEWEL_SE),      'Lower',            _NORMAL),
    'Crescent Moon Village - Metal Platform Rolling Box': LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 0, ItemFlag.JEWEL_SE),      'Lower',            _HARDER),
    'Crescent Moon Village - Rolling Box':                LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 0, ItemFlag.JEWEL_SW),      'Lower',            _NORMAL),
    'Crescent Moon Village - !-Switch Rolling Box':       LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 0, ItemFlag.JEWEL_SW),      'Lower',            _HARDER),
    'Crescent Moon Village - Sewer Box':                  LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 0, ItemFlag.JEWEL_NW),      'Lower',            _ALL),
    'Crescent Moon Village - CD Box':                     LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 0, ItemFlag.CD),            'Lower',            _ALL),

    # Arabian Night
    'Arabian Night - Onomi Box':                          LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 1, ItemFlag.JEWEL_NE),      'Town',             _ALL),
    'Arabian Night - Flying Carpet Overhang Box':         LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 1, ItemFlag.JEWEL_SE),      'Town',             _NORMAL),
    'Arabian Night - Flying Carpet Dash Attack Box':      LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 1, ItemFlag.JEWEL_SE),      'Town',             _HARDER),
    'Arabian Night - Zombie Plummet Box':                 LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 1, ItemFlag.JEWEL_SW),      'Town',             _NORMAL),
    'Arabian Night - Kool-Aid Box':                       LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 1, ItemFlag.JEWEL_SW),      'Town',             _HARDER),
    'Arabian Night - Sewer Box':                          LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 1, ItemFlag.JEWEL_NW),      'Sewer',            _ALL),
    'Arabian Night - CD Box':                             LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 1, ItemFlag.CD),            'Sewer',            _ALL),

    # Fiery Cavern
    'Fiery Cavern - Lava Dodging Box':                    LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 2, ItemFlag.JEWEL_NE),      'Flaming',          _NORMAL),
    'Fiery Cavern - Ice Beyond Door Box':                 LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 2, ItemFlag.JEWEL_NE),      'Frozen',           _HARDER),
    'Fiery Cavern - Long Lava Geyser Box':                LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 2, ItemFlag.JEWEL_SE),      'Flaming',          _ALL),
    'Fiery Cavern - Ice Detour Box':                      LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 2, ItemFlag.JEWEL_SW),      'Frozen',           _ALL),
    'Fiery Cavern - Snowman Box':                         LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 2, ItemFlag.JEWEL_NW),      'Frozen',           _ALL),
    'Fiery Cavern - CD Box':                              LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 2, ItemFlag.CD),            'Frozen',           _ALL),

    # Hotel Horror
    'Hotel Horror - 1F Hallway Box':                      LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 3, ItemFlag.JEWEL_NE),      'Hotel',            _NORMAL),
    'Hotel Horror - Room 102 Box':                        LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 3, ItemFlag.JEWEL_NE),      'Hotel',            _HARDER),
    'Hotel Horror - 2F Hallway Box':                      LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 3, ItemFlag.JEWEL_SE),      'Hotel',            _NORMAL),
    'Hotel Horror - Room 303 Box':                        LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 3, ItemFlag.JEWEL_SE),      'Hotel',            _HARDER),
    'Hotel Horror - 3F Hallway Box':                      LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 3, ItemFlag.JEWEL_SW),      'Hotel',            _NORMAL),
    'Hotel Horror - Room 402 Box':                        LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 3, ItemFlag.JEWEL_SW),      'Hotel',            _HARDER),
    'Hotel Horror - 4F Hallway Box':                      LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 3, ItemFlag.JEWEL_NW),      'Hotel',            _NORMAL),
    'Hotel Horror - Exterior Box':                        LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 3, ItemFlag.JEWEL_NW),      'Hotel',            _HARDER),
    'Hotel Horror - CD Box':                              LocationData(LocationType.BOX,  (Passage.SAPPHIRE, 3, ItemFlag.CD),            'Switch Room',      _ALL),

    'Catbat':                                             LocationData(LocationType.BOSS, (Passage.SAPPHIRE, 4, ItemFlag.KEYZER),         None,              _ALL),

    # Golden Pyramid
    # Golden Passage
    'Golden Passage - Current Puzzle Box':                LocationData(LocationType.BOX,  (Passage.GOLDEN,   0, ItemFlag.JEWEL_NE),       'Passage',         _ALL),
    'Golden Passage - River Box':                         LocationData(LocationType.BOX,  (Passage.GOLDEN,   0, ItemFlag.JEWEL_SE),       'Passage',         _ALL),
    'Golden Passage - Bat Room Box':                      LocationData(LocationType.BOX,  (Passage.GOLDEN,   0, ItemFlag.JEWEL_SW),       'Passage',         _ALL),
    'Golden Passage - Mad Scienstein Box':                LocationData(LocationType.BOX,  (Passage.GOLDEN,   0, ItemFlag.JEWEL_NW),       'Passage',         _ALL),

    'Golden Diva':                                        LocationData(LocationType.BOSS, (Passage.GOLDEN,   4, 0x10),                    None,              _ALL),
}


location_name_to_id = {name: (ap_id_offset + index) for (index, name) in enumerate(location_table)}


class WL4Location(Location):
    game: str = 'Wario Land 4'

    def __init__(self, player: int, name: str, code: Optional[int], parent: Optional[Region],
                 type: LocationType, status_position: Tuple[Passage, int, int],
                 difficulty: Difficulty):
        super().__init__(player, name, code, parent)
        self.type = type
        self.passage, self.level, self.flag = status_position
        self.difficulty = difficulty
        if type in (LocationType.BOSS, LocationType.KEYZER) or code is None:
            self.address = None
            self.event = True

    @classmethod
    def from_name(cls, player: int, name: str, parent: Optional[Region] = None):
        type, status, _, difficulty = location_table[name]
        return cls(player, name, location_name_to_id[name], parent, type,
                   status, difficulty)

    def entry_offset(self):
        if self.flag == ItemFlag.KEYZER:
            return None
        return self.flag.bit_length() - (1 if self.flag < ItemFlag.KEYZER else 2)

    def level_offset(self):
        return (self.passage * 4 + self.level) * (len(ItemFlag) - 1)

def get_level_locations(passage: Passage, level: int):
    return map(lambda l: l[0], get_level_location_data(passage, level))

def get_level_location_data(passage: Passage, level: int):
    return filter(lambda l: l[1].level_id() == (passage, level), location_table.items())

def setup_locations(world: MultiWorld, player: int):
    return {name for name in location_name_to_id
            if world.difficulty[player].value in location_table[name].difficulties}
