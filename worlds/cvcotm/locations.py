from BaseClasses import Location
from .data import lname, iname
from .options import CVCotMOptions, CompletionGoal

from typing import Dict, List, Union, Tuple, Optional, Set, NamedTuple

base_id = 0xD55C0000


class CVCotMLocation(Location):
    game: str = "Castlevania Circle of the Moon"


class CVCotMLocationData(NamedTuple):
    code: Union[int, str]
    offset: Optional[int]
    countdown: Optional[int]
    room_gfx: Optional[int]
    rule: Optional[str] = None
    type: Optional[str] = None
# code = The unique part of the Location's AP code attribute, as well as the in-game bitflag index starting from
#        0x02025374 that indicates the Location has been checked. Add this + base_id to get the actual AP code.
#        If we put an Item name string here instead of an int, then it is an event Location and that Item should be
#        forced on it while calling the actual code None.
# offset = The offset in the ROM to overwrite to change the Item on that Location.
# countdown = The index of the Countdown number region it contributes to.
# room_gfx = The offset of the Location's room entry to change to fix the magic item graphics (if 0xFFFF is there).
# rule = What rule should be applied to the Location during set_rules, as defined in self.rules in the CVCotMRules class
#        definition in rules.py.
# event = What event Item to place on that Location, for Locations that are events specifically.
# type = Anything special about this Location that should be considered, whether it be a boss Location, etc.


cvcotm_location_info: Dict[str, CVCotMLocationData] = {
    # Sealed Room
    lname.sr3:   CVCotMLocationData(0x35, 0xD0310,  0, 0xD7E56, rule="Roc"),
    # Catacombs
    lname.cc1:   CVCotMLocationData(0x37, 0xD0658,  1, 0xD7EC6, rule="Push"),
    lname.cc3:   CVCotMLocationData(0x43, 0xD0370,  1, 0xD7E8E, rule="Double"),
    lname.cc3b:  CVCotMLocationData(0x36, 0xD0364,  1, 0xD7E8E, rule="Double AND Freeze"),
    lname.cc4:   CVCotMLocationData(0xA8, 0xD0934,  1, 0xD7F52, type="magic item"),
    lname.cc5:   CVCotMLocationData(0x38, 0xD0DE4,  1, 0xD8032, rule="Tackle"),
    lname.cc8:   CVCotMLocationData(0x3A, 0xD1078,  1, 0xD80BE),
    lname.cc8b:  CVCotMLocationData(0x3B, 0xD1084,  1, 0xD80BE, rule="Kick"),
    lname.cc9:   CVCotMLocationData(0x40, 0xD0F94,  1, 0xD8086),
    lname.cc10:  CVCotMLocationData(0x39, 0xD12C4,  1, 0xD812E),
    lname.cc13:  CVCotMLocationData(0x41, 0xD0DA8,  1, 0xD8016),
    lname.cc14:  CVCotMLocationData(0x3C, 0xD1168,  1, 0xD80DA),
    lname.cc14b: CVCotMLocationData(0x3D, 0xD1174,  1, 0xD80DA, rule="Double OR Kick"),
    lname.cc16:  CVCotMLocationData(0x3E, 0xD0C40,  1, 0xD7FA6),
    lname.cc20:  CVCotMLocationData(0x42, 0xD103C,  1, 0xD80A2),
    lname.cc22:  CVCotMLocationData(0x3F, 0xD07C0,  1, 0xD7EFE),
    lname.cc24:  CVCotMLocationData(0xA9, 0xD1288,  1, 0xD80F6, type="boss"),
    lname.cc25:  CVCotMLocationData(0x44, 0xD12A0,  1, 0xD8112, rule="Double"),
    # Abyss Staircase
    lname.as2:   CVCotMLocationData(0x47, 0xD181C,  2, 0xD822A),
    lname.as3:   CVCotMLocationData(0x45, 0xD1774,  2, 0xD81D6),
    lname.as4:   CVCotMLocationData(0x46, 0xD1678,  2, 0xD8182, rule="Roc"),
    lname.as9:   CVCotMLocationData(0x48, 0xD17EC,  2, 0xD820E),
    # Audience Room
    lname.ar4:   CVCotMLocationData(0x53, 0xD2344,  3, 0xD84AE),
    lname.ar7:   CVCotMLocationData(0x54, 0xD2368,  3, 0xD84CA),
    lname.ar8:   CVCotMLocationData(0x51, 0xD1BF4,  3, 0xD82EE),
    lname.ar9:   CVCotMLocationData(0x4B, 0xD1E1C,  3, 0xD8342, rule="Push"),
    lname.ar10:  CVCotMLocationData(0x4A, 0xD1DE0,  3, 0xD830A),
    lname.ar11:  CVCotMLocationData(0x49, 0xD1E58,  3, 0xD8342, rule="Tackle"),
    lname.ar14:  CVCotMLocationData(0x4D, 0xD2158,  3, 0xD845A),
    lname.ar14b: CVCotMLocationData(0x4C, 0xD214C,  3, 0xD845A, rule="Roc"),
    lname.ar16:  CVCotMLocationData(0x52, 0xD20BC,  3, 0xD843E),
    lname.ar17:  CVCotMLocationData(0x50, 0xD2290,  3, 0xD8492),
    lname.ar17b: CVCotMLocationData(0x4F, 0xD2284,  3, 0xD8492, rule="Kick"),
    lname.ar18:  CVCotMLocationData(0x4E, 0xD1FA8,  3, 0xD83EA),
    lname.ar19:  CVCotMLocationData(0x6A, 0xD44A4,  7, 0xD8B22, rule="Kick"),
    lname.ar21:  CVCotMLocationData(0x55, 0xD238C,  3, 0xD84E6),
    lname.ar25:  CVCotMLocationData(0xAA, 0xD1E04,  3, 0xD8326, type="boss"),
    lname.ar26:  CVCotMLocationData(0x59, 0xD3370,  5, 0xD87A2, rule="Tackle AND Roc"),
    lname.ar27:  CVCotMLocationData(0x58, 0xD34E4,  5, 0xD87DA, rule="Tackle AND Push"),
    lname.ar30:  CVCotMLocationData(0x99, 0xD6A24, 11, 0xD93FE, rule="Roc"),
    lname.ar30b: CVCotMLocationData(0x9A, 0xD6A30, 11, 0xD93FE, rule="Roc"),
    # Outer Wall
    lname.ow0:   CVCotMLocationData(0x97, 0xD6BEC, 11, 0xD9452, rule="Roc"),
    lname.ow1:   CVCotMLocationData(0x98, 0xD6CE8, 11, 0xD946E, rule="Freeze"),
    lname.ow2:   CVCotMLocationData(0x9E, 0xD6DE4, 11, 0xD948A),
    # Triumph Hallway
    lname.th1:   CVCotMLocationData(0x57, 0xD26D4,  4, 0xD8556),
    lname.th3:   CVCotMLocationData(0x56, 0xD23C8,  4, 0xD8502, rule="Kick AND Freeze"),
    # Machine Tower
    lname.mt0:   CVCotMLocationData(0x61, 0xD307C,  5, 0xD8716),
    lname.mt2:   CVCotMLocationData(0x62, 0xD32A4,  5, 0xD876A),
    lname.mt3:   CVCotMLocationData(0x5B, 0xD3244,  5, 0xD874E, rule="Kick"),
    lname.mt4:   CVCotMLocationData(0x5A, 0xD31FC,  5, 0xD8732),
    lname.mt6:   CVCotMLocationData(0x5F, 0xD2F38,  5, 0xD86FA, rule="Kick"),
    lname.mt8:   CVCotMLocationData(0x5E, 0xD2EC0,  5, 0xD86DE),
    lname.mt10:  CVCotMLocationData(0x63, 0xD3550,  5, 0xD8812),
    lname.mt11:  CVCotMLocationData(0x5D, 0xD2D88,  5, 0xD86A6),
    lname.mt13:  CVCotMLocationData(0x5C, 0xD3580,  5, 0xD882E),
    lname.mt14:  CVCotMLocationData(0x60, 0xD2A64,  5, 0xD8636, rule="Tackle"),
    lname.mt17:  CVCotMLocationData(0x64, 0xD3520,  5, 0xD87F6),
    lname.mt19:  CVCotMLocationData(0xAB, 0xD283C,  5, 0xD85AA, type="boss"),
    # Eternal Corridor
    lname.ec5:   CVCotMLocationData(0x66, 0xD3B50,  6, 0xD890E),
    lname.ec7:   CVCotMLocationData(0x65, 0xD3A90,  6, 0xD88F2),
    lname.ec9:   CVCotMLocationData(0x67, 0xD3B98,  6, 0xD892A),
    # Chapel Tower
    lname.ct1:   CVCotMLocationData(0x68, 0xD40F0,  7, 0xD8A5E, rule="Freeze"),
    lname.ct4:   CVCotMLocationData(0x69, 0xD4630,  7, 0xD8B5A, rule="Push"),
    lname.ct5:   CVCotMLocationData(0x72, 0xD481C,  7, 0xD8C1E),
    lname.ct6:   CVCotMLocationData(0x6B, 0xD4294,  7, 0xD8AB2),
    lname.ct6b:  CVCotMLocationData(0x6C, 0xD42A0,  7, 0xD8AB2),
    lname.ct8:   CVCotMLocationData(0x6D, 0xD4330,  7, 0xD8ACE),
    lname.ct10:  CVCotMLocationData(0x6E, 0xD415C,  7, 0xD8A7A, rule="Push"),
    lname.ct13:  CVCotMLocationData(0x6F, 0xD4060,  7, 0xD8A42, rule="Freeze"),
    lname.ct15:  CVCotMLocationData(0x73, 0xD47F8,  7, 0xD8C02),
    lname.ct16:  CVCotMLocationData(0x70, 0xD3DA8,  7, 0xD89D2),
    lname.ct18:  CVCotMLocationData(0x74, 0xD47C8,  7, 0xD8BE6),
    lname.ct_switch: CVCotMLocationData(iname.ironmaidens, None, None, None),
    lname.ct22:  CVCotMLocationData(0x71, 0xD3CF4,  7, 0xD89B6, type="max up boss"),
    lname.ct26:  CVCotMLocationData(0x9C, 0xD6ACC, 11, 0xD941A),
    lname.ct26b: CVCotMLocationData(0x9B, 0xD6AC0, 11, 0xD941A),
    # Underground Gallery
    lname.ug0:   CVCotMLocationData(0x82, 0xD5944,  9, 0xD9046),
    lname.ug1:   CVCotMLocationData(0x83, 0xD5890,  9, 0xD902A, rule="Push"),
    lname.ug2:   CVCotMLocationData(0x81, 0xD5A1C,  9, 0xD9062, rule="Push"),
    lname.ug3:   CVCotMLocationData(0x85, 0xD56A4,  9, 0xD8FD6, rule="Kick AND Freeze"),
    lname.ug3b:  CVCotMLocationData(0x84, 0xD5698,  9, 0xD8FD6, rule="Kick AND Freeze"),
    lname.ug8:   CVCotMLocationData(0x86, 0xD5E30,  9, 0xD915E, rule="Tackle"),
    lname.ug10:  CVCotMLocationData(0x87, 0xD5F68,  9, 0xD9196),
    lname.ug13:  CVCotMLocationData(0x88, 0xD5AB8,  9, 0xD907E),
    lname.ug15:  CVCotMLocationData(0x89, 0xD5BD8,  9, 0xD90EE),
    lname.ug20:  CVCotMLocationData(0xAC, 0xD5470,  9, 0xD8F2E, type="boss"),
    # Underground Warehouse
    lname.uw1:   CVCotMLocationData(0x75, 0xD48DC,  8, 0xD8C72),
    lname.uw6:   CVCotMLocationData(0x76, 0xD4D20,  8, 0xD8D36),
    lname.uw8:   CVCotMLocationData(0x77, 0xD4BA0,  8, 0xD8CFE),
    lname.uw9:   CVCotMLocationData(0x7E, 0xD53EC,  8, 0xD8EDA),
    lname.uw10:  CVCotMLocationData(0x78, 0xD4C84,  8, 0xD8D1A, rule="Roc"),
    lname.uw11:  CVCotMLocationData(0x79, 0xD4EC4,  8, 0xD8D6E),
    lname.uw14:  CVCotMLocationData(0x7F, 0xD5410,  8, 0xD8EF6, rule="Freeze"),
    lname.uw16:  CVCotMLocationData(0x7A, 0xD5050,  8, 0xD8DC2),
    lname.uw16b: CVCotMLocationData(0x7B, 0xD505C,  8, 0xD8DC2, rule="Roc"),
    lname.uw19:  CVCotMLocationData(0x7C, 0xD5344,  8, 0xD8E4E),
    lname.uw23:  CVCotMLocationData(0xAE, 0xD53B0,  8, 0xD8EA2, type="boss"),
    lname.uw24:  CVCotMLocationData(0x80, 0xD5434,  8, 0xD8F12),
    lname.uw25:  CVCotMLocationData(0x7D, 0xD4FC0,  8, 0xD8DA6),
    # Underground Waterway
    lname.uy1:   CVCotMLocationData(0x93, 0xD5F98, 10, 0xD91CE),
    lname.uy3:   CVCotMLocationData(0x8B, 0xD5FEC, 10, 0xD9206),
    lname.uy3b:  CVCotMLocationData(0x8A, 0xD5FE0, 10, 0xD9206),
    lname.uy4:   CVCotMLocationData(0x94, 0xD697C, 10, 0xD93AA),
    lname.uy5:   CVCotMLocationData(0x8C, 0xD6214, 10, 0xD923E, rule="Freeze"),
    lname.uy7:   CVCotMLocationData(0x8D, 0xD65A4, 10, 0xD9292),
    lname.uy8:   CVCotMLocationData(0x95, 0xD69A0, 10, 0xD93C6, rule="Roc"),
    lname.uy9:   CVCotMLocationData(0x8E, 0xD640C, 10, 0xD9276),
    lname.uy9b:  CVCotMLocationData(0x8F, 0xD6418, 10, 0xD9276),
    lname.uy12:  CVCotMLocationData(0x90, 0xD6730, 10, 0xD92E6),
    lname.uy12b: CVCotMLocationData(0x91, 0xD673C, 10, 0xD92E6, rule="Cleansing"),
    lname.uy13:  CVCotMLocationData(0x92, 0xD685C, 10, 0xD9302, rule="Roc"),
    lname.uy17:  CVCotMLocationData(0xAF, 0xD6940, 10, 0xD9372, rule="Cleansing", type="boss"),
    lname.uy18:  CVCotMLocationData(0x96, 0xD69C4, 10, 0xD93E2, rule="Roc"),
    # Observation Tower
    lname.ot1:   CVCotMLocationData(0x9D, 0xD6B38, 11, 0xD9436),
    lname.ot2:   CVCotMLocationData(0xA4, 0xD760C, 12, 0xD96D6),
    lname.ot3:   CVCotMLocationData(0x9F, 0xD72E8, 12, 0xD9612),
    lname.ot5:   CVCotMLocationData(0xA5, 0xD75E8, 12, 0xD96BA),
    lname.ot8:   CVCotMLocationData(0xA0, 0xD71EC, 12, 0xD95DA),
    lname.ot9:   CVCotMLocationData(0xA2, 0xD6FE8, 12, 0xD9586),
    lname.ot12:  CVCotMLocationData(0xA6, 0xD75C4, 12, 0xD969E),
    lname.ot13:  CVCotMLocationData(0xA3, 0xD6F64, 12, 0xD954E),
    lname.ot16:  CVCotMLocationData(0xA1, 0xD751C, 12, 0xD9682),
    lname.ot20:  CVCotMLocationData(0xB0, 0xD6E20, 12, 0xD94A6, type="boss"),
    # Ceremonial Room
    lname.cr1:   CVCotMLocationData(0xA7, 0xD7690, 13, 0xD972A, rule="Kick"),
    lname.dracula: CVCotMLocationData(iname.dracula, None, None, None, rule="Roc"),
    # Battle Arena
    lname.ba24:  CVCotMLocationData(iname.shinning_armor, None, None, None),
 }


def get_location_names_to_ids() -> Dict[str, int]:
    return {name: cvcotm_location_info[name].code+base_id for name in cvcotm_location_info
            if isinstance(cvcotm_location_info[name].code, int)}


def get_locations_by_area() -> Dict[str, Set[str]]:
    areas_to_locations = {}

    for loc_name in cvcotm_location_info:
        # If we are looking at an event Location, don't include it.
        if isinstance(cvcotm_location_info[loc_name].code, str):
            continue

        # The part of the Location name's string before the colon is its area name.
        area_name = loc_name.split(":")[0]

        if area_name not in areas_to_locations:
            areas_to_locations[area_name] = {loc_name}
        else:
            areas_to_locations[area_name].add(loc_name)

    return areas_to_locations


def get_named_locations_data(locations: List[str], options: CVCotMOptions) -> \
        Tuple[Dict[str, Optional[int]], Dict[str, str]]:
    locations_with_ids = {}
    locked_items = {}

    for loc in locations:
        # If Break Iron Maidens is on, don't place the Broke Iron Maidens Location.
        if loc == lname.ct_switch and options.break_iron_maidens:
            continue

        # Don't place the Dracula Location if our Completion Goal is the Battle Arena only.
        if loc == lname.dracula and options.completion_goal == CompletionGoal.option_battle_arena:
            continue

        # Don't place the Battle Arena Location if our Completion Goal is Dracula only.
        if loc == lname.ba24 and options.completion_goal == CompletionGoal.option_dracula:
            continue

        loc_code = cvcotm_location_info[loc].code

        # If we are looking at an event Location, add its associated event Item to the events' dict.
        # Otherwise, add the base_id to the Location's code.
        if isinstance(loc_code, str):
            locked_items[loc] = loc_code
            locations_with_ids.update({loc: None})
        else:
            loc_code += base_id
            locations_with_ids.update({loc: loc_code})

        # If the Require All Bosses option is on, add a Last Key to the events dict for all Locations marked "boss" for
        # their type.
        if options.require_all_bosses and cvcotm_location_info[loc].type in ["boss", "max up boss"]:
            locked_items[loc] = iname.last_key

    return locations_with_ids, locked_items
