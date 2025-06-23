from BaseClasses import Location
from .data import lname, iname
from .options import CVCotMOptions, CompletionGoal, IronMaidenBehavior, RequiredSkirmishes

from typing import Dict, List, Union, Tuple, Optional, Set, NamedTuple

BASE_ID = 0xD55C0000


class CVCotMLocation(Location):
    game: str = "Castlevania - Circle of the Moon"


class CVCotMLocationData(NamedTuple):
    code: Union[int, str]
    offset: Optional[int]
    countdown: Optional[int]
    type: Optional[str] = None
# code = The unique part of the Location's AP code attribute, as well as the in-game bitflag index starting from
#        0x02025374 that indicates the Location has been checked. Add this + base_id to get the actual AP code.
#        If we put an Item name string here instead of an int, then it is an event Location and that Item should be
#        forced on it while calling the actual code None.
# offset = The offset in the ROM to overwrite to change the Item on that Location.
# countdown = The index of the Countdown number region it contributes to.
# rule = What rule should be applied to the Location during set_rules, as defined in self.rules in the CVCotMRules class
#        definition in rules.py.
# event = What event Item to place on that Location, for Locations that are events specifically.
# type = Anything special about this Location that should be considered, whether it be a boss Location, etc.


cvcotm_location_info: Dict[str, CVCotMLocationData] = {
    # Sealed Room
    lname.sr3:   CVCotMLocationData(0x35, 0xD0310,  0),
    # Catacombs
    lname.cc1:   CVCotMLocationData(0x37, 0xD0658,  1),
    lname.cc3:   CVCotMLocationData(0x43, 0xD0370,  1),
    lname.cc3b:  CVCotMLocationData(0x36, 0xD0364,  1),
    lname.cc4:   CVCotMLocationData(0xA8, 0xD0934,  1, type="magic item"),
    lname.cc5:   CVCotMLocationData(0x38, 0xD0DE4,  1),
    lname.cc8:   CVCotMLocationData(0x3A, 0xD1078,  1),
    lname.cc8b:  CVCotMLocationData(0x3B, 0xD1084,  1),
    lname.cc9:   CVCotMLocationData(0x40, 0xD0F94,  1),
    lname.cc10:  CVCotMLocationData(0x39, 0xD12C4,  1),
    lname.cc13:  CVCotMLocationData(0x41, 0xD0DA8,  1),
    lname.cc14:  CVCotMLocationData(0x3C, 0xD1168,  1),
    lname.cc14b: CVCotMLocationData(0x3D, 0xD1174,  1),
    lname.cc16:  CVCotMLocationData(0x3E, 0xD0C40,  1),
    lname.cc20:  CVCotMLocationData(0x42, 0xD103C,  1),
    lname.cc22:  CVCotMLocationData(0x3F, 0xD07C0,  1),
    lname.cc24:  CVCotMLocationData(0xA9, 0xD1288,  1, type="boss"),
    lname.cc25:  CVCotMLocationData(0x44, 0xD12A0,  1),
    # Abyss Staircase
    lname.as2:   CVCotMLocationData(0x47, 0xD181C,  2),
    lname.as3:   CVCotMLocationData(0x45, 0xD1774,  2),
    lname.as4:   CVCotMLocationData(0x46, 0xD1678,  2),
    lname.as9:   CVCotMLocationData(0x48, 0xD17EC,  2),
    # Audience Room
    lname.ar4:   CVCotMLocationData(0x53, 0xD2344,  3),
    lname.ar7:   CVCotMLocationData(0x54, 0xD2368,  3),
    lname.ar8:   CVCotMLocationData(0x51, 0xD1BF4,  3),
    lname.ar9:   CVCotMLocationData(0x4B, 0xD1E1C,  3),
    lname.ar10:  CVCotMLocationData(0x4A, 0xD1DE0,  3),
    lname.ar11:  CVCotMLocationData(0x49, 0xD1E58,  3),
    lname.ar14:  CVCotMLocationData(0x4D, 0xD2158,  3),
    lname.ar14b: CVCotMLocationData(0x4C, 0xD214C,  3),
    lname.ar16:  CVCotMLocationData(0x52, 0xD20BC,  3),
    lname.ar17:  CVCotMLocationData(0x50, 0xD2290,  3),
    lname.ar17b: CVCotMLocationData(0x4F, 0xD2284,  3),
    lname.ar18:  CVCotMLocationData(0x4E, 0xD1FA8,  3),
    lname.ar19:  CVCotMLocationData(0x6A, 0xD44A4,  7),
    lname.ar21:  CVCotMLocationData(0x55, 0xD238C,  3),
    lname.ar25:  CVCotMLocationData(0xAA, 0xD1E04,  3, type="boss"),
    lname.ar26:  CVCotMLocationData(0x59, 0xD3370,  5),
    lname.ar27:  CVCotMLocationData(0x58, 0xD34E4,  5),
    lname.ar30:  CVCotMLocationData(0x99, 0xD6A24, 11),
    lname.ar30b: CVCotMLocationData(0x9A, 0xD6A30, 11),
    # Outer Wall
    lname.ow0:   CVCotMLocationData(0x97, 0xD6BEC, 11),
    lname.ow1:   CVCotMLocationData(0x98, 0xD6CE8, 11),
    lname.ow2:   CVCotMLocationData(0x9E, 0xD6DE4, 11),
    # Triumph Hallway
    lname.th1:   CVCotMLocationData(0x57, 0xD26D4,  4),
    lname.th3:   CVCotMLocationData(0x56, 0xD23C8,  4),
    # Machine Tower
    lname.mt0:   CVCotMLocationData(0x61, 0xD307C,  5),
    lname.mt2:   CVCotMLocationData(0x62, 0xD32A4,  5),
    lname.mt3:   CVCotMLocationData(0x5B, 0xD3244,  5),
    lname.mt4:   CVCotMLocationData(0x5A, 0xD31FC,  5),
    lname.mt6:   CVCotMLocationData(0x5F, 0xD2F38,  5),
    lname.mt8:   CVCotMLocationData(0x5E, 0xD2EC0,  5),
    lname.mt10:  CVCotMLocationData(0x63, 0xD3550,  5),
    lname.mt11:  CVCotMLocationData(0x5D, 0xD2D88,  5),
    lname.mt13:  CVCotMLocationData(0x5C, 0xD3580,  5),
    lname.mt14:  CVCotMLocationData(0x60, 0xD2A64,  5),
    lname.mt17:  CVCotMLocationData(0x64, 0xD3520,  5),
    lname.mt19:  CVCotMLocationData(0xAB, 0xD283C,  5, type="boss"),
    # Eternal Corridor
    lname.ec5:   CVCotMLocationData(0x66, 0xD3B50,  6),
    lname.ec7:   CVCotMLocationData(0x65, 0xD3A90,  6),
    lname.ec9:   CVCotMLocationData(0x67, 0xD3B98,  6),
    # Chapel Tower
    lname.ct1:   CVCotMLocationData(0x68, 0xD40F0,  7),
    lname.ct4:   CVCotMLocationData(0x69, 0xD4630,  7),
    lname.ct5:   CVCotMLocationData(0x72, 0xD481C,  7),
    lname.ct6:   CVCotMLocationData(0x6B, 0xD4294,  7),
    lname.ct6b:  CVCotMLocationData(0x6C, 0xD42A0,  7),
    lname.ct8:   CVCotMLocationData(0x6D, 0xD4330,  7),
    lname.ct10:  CVCotMLocationData(0x6E, 0xD415C,  7),
    lname.ct13:  CVCotMLocationData(0x6F, 0xD4060,  7),
    lname.ct15:  CVCotMLocationData(0x73, 0xD47F8,  7),
    lname.ct16:  CVCotMLocationData(0x70, 0xD3DA8,  7),
    lname.ct18:  CVCotMLocationData(0x74, 0xD47C8,  7),
    lname.ct21:  CVCotMLocationData(0xF0, 0xD47B0,  7, type="maiden switch"),
    lname.ct22:  CVCotMLocationData(0x71, 0xD3CF4,  7, type="max up boss"),
    lname.ct26:  CVCotMLocationData(0x9C, 0xD6ACC, 11),
    lname.ct26b: CVCotMLocationData(0x9B, 0xD6AC0, 11),
    # Underground Gallery
    lname.ug0:   CVCotMLocationData(0x82, 0xD5944,  9),
    lname.ug1:   CVCotMLocationData(0x83, 0xD5890,  9),
    lname.ug2:   CVCotMLocationData(0x81, 0xD5A1C,  9),
    lname.ug3:   CVCotMLocationData(0x85, 0xD56A4,  9),
    lname.ug3b:  CVCotMLocationData(0x84, 0xD5698,  9),
    lname.ug8:   CVCotMLocationData(0x86, 0xD5E30,  9),
    lname.ug10:  CVCotMLocationData(0x87, 0xD5F68,  9),
    lname.ug13:  CVCotMLocationData(0x88, 0xD5AB8,  9),
    lname.ug15:  CVCotMLocationData(0x89, 0xD5BD8,  9),
    lname.ug20:  CVCotMLocationData(0xAC, 0xD5470,  9, type="boss"),
    # Underground Warehouse
    lname.uw1:   CVCotMLocationData(0x75, 0xD48DC,  8),
    lname.uw6:   CVCotMLocationData(0x76, 0xD4D20,  8),
    lname.uw8:   CVCotMLocationData(0x77, 0xD4BA0,  8),
    lname.uw9:   CVCotMLocationData(0x7E, 0xD53EC,  8),
    lname.uw10:  CVCotMLocationData(0x78, 0xD4C84,  8),
    lname.uw11:  CVCotMLocationData(0x79, 0xD4EC4,  8),
    lname.uw14:  CVCotMLocationData(0x7F, 0xD5410,  8),
    lname.uw16:  CVCotMLocationData(0x7A, 0xD5050,  8),
    lname.uw16b: CVCotMLocationData(0x7B, 0xD505C,  8),
    lname.uw19:  CVCotMLocationData(0x7C, 0xD5344,  8),
    lname.uw23:  CVCotMLocationData(0xAE, 0xD53B0,  8, type="boss"),
    lname.uw24:  CVCotMLocationData(0x80, 0xD5434,  8),
    lname.uw25:  CVCotMLocationData(0x7D, 0xD4FC0,  8),
    # Underground Waterway
    lname.uy1:   CVCotMLocationData(0x93, 0xD5F98, 10),
    lname.uy3:   CVCotMLocationData(0x8B, 0xD5FEC, 10),
    lname.uy3b:  CVCotMLocationData(0x8A, 0xD5FE0, 10),
    lname.uy4:   CVCotMLocationData(0x94, 0xD697C, 10),
    lname.uy5:   CVCotMLocationData(0x8C, 0xD6214, 10),
    lname.uy7:   CVCotMLocationData(0x8D, 0xD65A4, 10),
    lname.uy8:   CVCotMLocationData(0x95, 0xD69A0, 10),
    lname.uy9:   CVCotMLocationData(0x8E, 0xD640C, 10),
    lname.uy9b:  CVCotMLocationData(0x8F, 0xD6418, 10),
    lname.uy12:  CVCotMLocationData(0x90, 0xD6730, 10),
    lname.uy12b: CVCotMLocationData(0x91, 0xD673C, 10),
    lname.uy13:  CVCotMLocationData(0x92, 0xD685C, 10),
    lname.uy17:  CVCotMLocationData(0xAF, 0xD6940, 10, type="boss"),
    lname.uy18:  CVCotMLocationData(0x96, 0xD69C4, 10),
    # Observation Tower
    lname.ot1:   CVCotMLocationData(0x9D, 0xD6B38, 11),
    lname.ot2:   CVCotMLocationData(0xA4, 0xD760C, 12),
    lname.ot3:   CVCotMLocationData(0x9F, 0xD72E8, 12),
    lname.ot5:   CVCotMLocationData(0xA5, 0xD75E8, 12),
    lname.ot8:   CVCotMLocationData(0xA0, 0xD71EC, 12),
    lname.ot9:   CVCotMLocationData(0xA2, 0xD6FE8, 12),
    lname.ot12:  CVCotMLocationData(0xA6, 0xD75C4, 12),
    lname.ot13:  CVCotMLocationData(0xA3, 0xD6F64, 12),
    lname.ot16:  CVCotMLocationData(0xA1, 0xD751C, 12),
    lname.ot20:  CVCotMLocationData(0xB0, 0xD6E20, 12, type="boss"),
    # Ceremonial Room
    lname.cr1:   CVCotMLocationData(0xA7, 0xD7690, 13),
    lname.dracula: CVCotMLocationData(iname.dracula, None, None),
    # Battle Arena
    lname.ba24:  CVCotMLocationData(0xB2, 0xD7D20, 14, type="arena"),
    lname.arena_victory:  CVCotMLocationData(iname.shinning_armor, None, None),
 }


def get_location_names_to_ids() -> Dict[str, int]:
    return {name: cvcotm_location_info[name].code+BASE_ID for name in cvcotm_location_info
            if isinstance(cvcotm_location_info[name].code, int)}


def get_location_name_groups() -> Dict[str, Set[str]]:
    loc_name_groups: Dict[str, Set[str]] = {"Breakable Secrets": set(),
                                            "Bosses": set()}

    for loc_name in cvcotm_location_info:
        # If we are looking at an event Location, don't include it.
        if isinstance(cvcotm_location_info[loc_name].code, str):
            continue

        # The part of the Location name's string before the colon is its area name.
        area_name = loc_name.split(":")[0]

        # Add each Location to its corresponding area name group.
        if area_name not in loc_name_groups:
            loc_name_groups[area_name] = {loc_name}
        else:
            loc_name_groups[area_name].add(loc_name)

        # If the word "fake" is in the Location's name, add it to the "Breakable Walls" Location group.
        if "fake" in loc_name.casefold():
            loc_name_groups["Breakable Secrets"].add(loc_name)

        # If it's a behind boss Location, add it to the "Bosses" Location group.
        if cvcotm_location_info[loc_name].type in ["boss", "max up boss"]:
            loc_name_groups["Bosses"].add(loc_name)

    return loc_name_groups


def get_named_locations_data(locations: List[str], options: CVCotMOptions) -> \
        Tuple[Dict[str, Optional[int]], Dict[str, str]]:
    locations_with_ids = {}
    locked_pairs = {}
    locked_key_types = []

    # Decide which Location types should have locked Last Keys placed on them, if skirmishes are required.
    # If the Maiden Detonator is in the pool, Adramelech's key should be on the switch instead of behind the maiden.
    if options.required_skirmishes:
        locked_key_types += ["boss"]
        if options.iron_maiden_behavior == IronMaidenBehavior.option_detonator_in_pool:
            locked_key_types += ["maiden switch"]
        else:
            locked_key_types += ["max up boss"]
        # If all bosses and the Arena is required, the Arena end reward should have a Last Key as well.
        if options.required_skirmishes == RequiredSkirmishes.option_all_bosses_and_arena:
            locked_key_types += ["arena"]

    for loc in locations:
        if loc == lname.ct21:
            # If the maidens are pre-broken, don't create the iron maiden switch Location at all.
            if options.iron_maiden_behavior == IronMaidenBehavior.option_start_broken:
                continue
            # If the maiden behavior is vanilla, lock the Maiden Detonator on this Location.
            if options.iron_maiden_behavior == IronMaidenBehavior.option_vanilla:
                locked_pairs[loc] = iname.ironmaidens

        # Don't place the Dracula Location if our Completion Goal is the Battle Arena only.
        if loc == lname.dracula and options.completion_goal == CompletionGoal.option_battle_arena:
            continue

        # Don't place the Battle Arena normal Location if the Arena is not required by the Skirmishes option.
        if loc == lname.ba24 and options.required_skirmishes != RequiredSkirmishes.option_all_bosses_and_arena:
            continue

        # Don't place the Battle Arena event Location if our Completion Goal is Dracula only.
        if loc == lname.arena_victory and options.completion_goal == CompletionGoal.option_dracula:
            continue

        loc_code = cvcotm_location_info[loc].code

        # If we are looking at an event Location, add its associated event Item to the events' dict.
        # Otherwise, add the base_id to the Location's code.
        if isinstance(loc_code, str):
            locked_pairs[loc] = loc_code
            locations_with_ids.update({loc: None})
        else:
            loc_code += BASE_ID
            locations_with_ids.update({loc: loc_code})

        # Place a locked Last Key on this Location if its of a type that should have one.
        if cvcotm_location_info[loc].type in locked_key_types:
            locked_pairs[loc] = iname.last_key

    return locations_with_ids, locked_pairs
