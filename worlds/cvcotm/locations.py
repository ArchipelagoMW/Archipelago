from BaseClasses import Location
from .data import lname, iname
from .options import CVCotMOptions

from typing import Dict, Union, List, Tuple, Optional, Set

base_id = 0xD55C0000


class CVCotMLocation(Location):
    game: str = "Castlevania Circle of the Moon"


# # #    KEY    # # #
# "code" = The unique part of the Location's AP code attribute, as well as the in-game bitflag index starting from
#          0x80389BE4 that indicates the Location has been checked. Add this + base_id to get the actual AP code.
# "offset" = The offset in the ROM to overwrite to change the Item on that Location.
# "room gfx" = The offset of the Location's room entry to change to fix the magic item graphics (if 0xFFFF is there).
# "rule" = What rule should be applied to the Location during set_rules, as defined in self.rules in the CVCotMRules
#          class definition in rules.py.
# "event" = What event Item to place on that Location, for Locations that are events specifically.
# "type" = Anything special about this Location that should be considered, whether it be a boss Location, etc.
# "countdown" = What Countdown number in the array of Countdown numbers that Location contributes to.
location_info = {
    # Sealed Room
    lname.sr3:   {"code": 0x35, "offset": 0xD0310, "room gfx": 0xD7E56, "rule": "Roc"},
    # Catacombs
    lname.cc1:   {"code": 0x37, "offset": 0xD0658, "room gfx": 0xD7EC6, "rule": "Push"},
    lname.cc3:   {"code": 0x43, "offset": 0xD0370, "room gfx": 0xD7E8E, "rule": "Double"},
    lname.cc3b:  {"code": 0x36, "offset": 0xD0364, "room gfx": 0xD7E8E, "rule": "Double AND Freeze"},
    lname.cc4:   {"code": 0xA8, "offset": 0xD0934, "room gfx": 0xD7F52, "type": "magic item"},
    lname.cc5:   {"code": 0x38, "offset": 0xD0DE4, "room gfx": 0xD8032, "rule": "Tackle"},
    lname.cc8:   {"code": 0x3A, "offset": 0xD1078, "room gfx": 0xD80BE},
    lname.cc8b:  {"code": 0x3B, "offset": 0xD1084, "room gfx": 0xD80BE, "rule": "Kick"},
    lname.cc9:   {"code": 0x40, "offset": 0xD0F94, "room gfx": 0xD8086},
    lname.cc10:  {"code": 0x39, "offset": 0xD12C4, "room gfx": 0xD812E},
    lname.cc13:  {"code": 0x41, "offset": 0xD0DA8, "room gfx": 0xD8016},
    lname.cc14:  {"code": 0x3C, "offset": 0xD1168, "room gfx": 0xD80DA},
    lname.cc14b: {"code": 0x3D, "offset": 0xD1174, "room gfx": 0xD80DA, "rule": "Double OR Kick"},
    lname.cc16:  {"code": 0x3E, "offset": 0xD0C40, "room gfx": 0xD7FA6},
    lname.cc20:  {"code": 0x42, "offset": 0xD103C, "room gfx": 0xD80A2},
    lname.cc22:  {"code": 0x3F, "offset": 0xD07C0, "room gfx": 0xD7EFE},
    lname.cc24:  {"code": 0xA9, "offset": 0xD1288, "room gfx": 0xD80F6, "type": "boss"},
    lname.cc25:  {"code": 0x44, "offset": 0xD12A0, "room gfx": 0xD8112, "rule": "Double"},
    # Abyss Staircase
    lname.as2:   {"code": 0x47, "offset": 0xD181C, "room gfx": 0xD822A},
    lname.as3:   {"code": 0x45, "offset": 0xD1774, "room gfx": 0xD81D6},
    lname.as4:   {"code": 0x46, "offset": 0xD1678, "room gfx": 0xD8182, "rule": "Roc"},
    lname.as9:   {"code": 0x48, "offset": 0xD17EC, "room gfx": 0xD820E},
    # Audience Room
    lname.ar4:   {"code": 0x53, "offset": 0xD2344, "room gfx": 0xD84AE},
    lname.ar7:   {"code": 0x54, "offset": 0xD2368, "room gfx": 0xD84CA},
    lname.ar8:   {"code": 0x51, "offset": 0xD1BF4, "room gfx": 0xD82EE},
    lname.ar9:   {"code": 0x4B, "offset": 0xD1E1C, "room gfx": 0xD8342, "rule": "Push"},
    lname.ar10:  {"code": 0x4A, "offset": 0xD1DE0, "room gfx": 0xD830A},
    lname.ar11:  {"code": 0x49, "offset": 0xD1E58, "room gfx": 0xD8342, "rule": "Tackle"},
    lname.ar14:  {"code": 0x4D, "offset": 0xD2158, "room gfx": 0xD845A},
    lname.ar14b: {"code": 0x4C, "offset": 0xD214C, "room gfx": 0xD845A, "rule": "Roc"},
    lname.ar16:  {"code": 0x52, "offset": 0xD20BC, "room gfx": 0xD843E},
    lname.ar17:  {"code": 0x50, "offset": 0xD2290, "room gfx": 0xD8492},
    lname.ar17b: {"code": 0x4F, "offset": 0xD2284, "room gfx": 0xD8492},
    lname.ar18:  {"code": 0x4E, "offset": 0xD1FA8, "room gfx": 0xD83EA},
    lname.ar19:  {"code": 0x6A, "offset": 0xD44A4, "room gfx": 0xD8B22, "rule": "Kick"},
    lname.ar21:  {"code": 0x55, "offset": 0xD238C, "room gfx": 0xD84E6},
    lname.ar25:  {"code": 0xAA, "offset": 0xD1E04, "room gfx": 0xD8326, "type": "boss"},
    lname.ar26:  {"code": 0x59, "offset": 0xD3370, "room gfx": 0xD87A2, "rule": "Tackle AND Roc"},
    lname.ar27:  {"code": 0x58, "offset": 0xD34E4, "room gfx": 0xD87DA, "rule": "Tackle AND Push"},
    lname.ar30:  {"code": 0x99, "offset": 0xD6A24, "room gfx": 0xD93FE, "rule": "Roc"},
    lname.ar30b: {"code": 0x9A, "offset": 0xD6A30, "room gfx": 0xD93FE, "rule": "Roc"},
    # Outer Wall
    lname.ow0:   {"code": 0x97, "offset": 0xD6BEC, "room gfx": 0xD9452, "rule": "Roc"},
    lname.ow1:   {"code": 0x98, "offset": 0xD6CE8, "room gfx": 0xD946E, "rule": "Freeze"},
    lname.ow2:   {"code": 0x9E, "offset": 0xD6DE4, "room gfx": 0xD948A},
    # Triumph Hallway
    lname.th1:   {"code": 0x57, "offset": 0xD26D4, "room gfx": 0xD8556},
    lname.th3:   {"code": 0x56, "offset": 0xD23C8, "room gfx": 0xD8502, "rule": "Kick AND Freeze"},
    # Machine Tower
    lname.mt0:   {"code": 0x61, "offset": 0xD307C, "room gfx": 0xD8716},
    lname.mt2:   {"code": 0x62, "offset": 0xD32A4, "room gfx": 0xD876A},
    lname.mt3:   {"code": 0x5B, "offset": 0xD3244, "room gfx": 0xD874E, "rule": "Kick"},
    lname.mt4:   {"code": 0x5A, "offset": 0xD31FC, "room gfx": 0xD8732},
    lname.mt6:   {"code": 0x5F, "offset": 0xD2F38, "room gfx": 0xD86FA, "rule": "Kick"},
    lname.mt8:   {"code": 0x5E, "offset": 0xD2EC0, "room gfx": 0xD86DE},
    lname.mt10:  {"code": 0x63, "offset": 0xD3550, "room gfx": 0xD8812},
    lname.mt11:  {"code": 0x5D, "offset": 0xD2D88, "room gfx": 0xD86A6},
    lname.mt13:  {"code": 0x5C, "offset": 0xD3580, "room gfx": 0xD882E},
    lname.mt14:  {"code": 0x60, "offset": 0xD2A64, "room gfx": 0xD8636, "rule": "Tackle"},
    lname.mt17:  {"code": 0x64, "offset": 0xD3520, "room gfx": 0xD87F6},
    lname.mt19:  {"code": 0xAB, "offset": 0xD283C, "room gfx": 0xD85AA, "type": "boss"},
    # Eternal Corridor
    lname.ec5:   {"code": 0x66, "offset": 0xD3B50, "room gfx": 0xD890E},
    lname.ec7:   {"code": 0x65, "offset": 0xD3A90, "room gfx": 0xD88F2},
    lname.ec9:   {"code": 0x67, "offset": 0xD3B98, "room gfx": 0xD892A},
    # Chapel Tower
    lname.ct1:   {"code": 0x68, "offset": 0xD40F0, "room gfx": 0xD8A5E, "rule": "Freeze"},
    lname.ct4:   {"code": 0x69, "offset": 0xD4630, "room gfx": 0xD8B5A, "rule": "Push"},
    lname.ct5:   {"code": 0x72, "offset": 0xD481C, "room gfx": 0xD8C1E},
    lname.ct6:   {"code": 0x6B, "offset": 0xD4294, "room gfx": 0xD8AB2},
    lname.ct6b:  {"code": 0x6C, "offset": 0xD42A0, "room gfx": 0xD8AB2},
    lname.ct8:   {"code": 0x6D, "offset": 0xD4330, "room gfx": 0xD8ACE},
    lname.ct10:  {"code": 0x6E, "offset": 0xD415C, "room gfx": 0xD8A7A, "rule": "Push"},
    lname.ct13:  {"code": 0x6F, "offset": 0xD4060, "room gfx": 0xD8A42, "rule": "Freeze"},
    lname.ct15:  {"code": 0x73, "offset": 0xD47F8, "room gfx": 0xD8C02},
    lname.ct16:  {"code": 0x70, "offset": 0xD3DA8, "room gfx": 0xD89D2},
    lname.ct18:  {"code": 0x74, "offset": 0xD47C8, "room gfx": 0xD8BE6},
    lname.ct_switch: {"event": iname.ironmaidens},
    lname.ct22:  {"code": 0x71, "offset": 0xD3CF4, "room gfx": 0xD89B6, "type": "max up boss"},
    lname.ct26:  {"code": 0x9C, "offset": 0xD6ACC, "room gfx": 0xD941A, "rule": "Roc"},
    lname.ct26b: {"code": 0x9B, "offset": 0xD6AC0, "room gfx": 0xD941A, "rule": "Roc"},
    # Underground Gallery
    lname.ug0:   {"code": 0x82, "offset": 0xD5944, "room gfx": 0xD9046},
    lname.ug1:   {"code": 0x83, "offset": 0xD5890, "room gfx": 0xD902A, "rule": "Push"},
    lname.ug2:   {"code": 0x81, "offset": 0xD5A1C, "room gfx": 0xD9062, "rule": "Push"},
    lname.ug3:   {"code": 0x85, "offset": 0xD56A4, "room gfx": 0xD8FD6, "rule": "Kick AND Freeze"},
    lname.ug3b:  {"code": 0x84, "offset": 0xD5698, "room gfx": 0xD8FD6, "rule": "Kick AND Freeze"},
    lname.ug8:   {"code": 0x86, "offset": 0xD5E30, "room gfx": 0xD915E, "rule": "Tackle"},
    lname.ug10:  {"code": 0x87, "offset": 0xD5F68, "room gfx": 0xD9196},
    lname.ug13:  {"code": 0x88, "offset": 0xD5AB8, "room gfx": 0xD907E},
    lname.ug15:  {"code": 0x89, "offset": 0xD5BD8, "room gfx": 0xD90EE},
    lname.ug20:  {"code": 0xAC, "offset": 0xD5470, "room gfx": 0xD8F2E, "type": "boss"},
    # Underground Warehouse
    lname.uw1:   {"code": 0x75, "offset": 0xD48DC, "room gfx": 0xD8C72},
    lname.uw6:   {"code": 0x76, "offset": 0xD4D20, "room gfx": 0xD8D36},
    lname.uw8:   {"code": 0x77, "offset": 0xD4BA0, "room gfx": 0xD8CFE},
    lname.uw9:   {"code": 0x7E, "offset": 0xD53EC, "room gfx": 0xD8EDA},
    lname.uw10:  {"code": 0x78, "offset": 0xD4C84, "room gfx": 0xD8D1A, "rule": "Roc"},
    lname.uw11:  {"code": 0x79, "offset": 0xD4EC4, "room gfx": 0xD8D6E},
    lname.uw14:  {"code": 0x7F, "offset": 0xD5410, "room gfx": 0xD8EF6},
    lname.uw16:  {"code": 0x7A, "offset": 0xD5050, "room gfx": 0xD8DC2},
    lname.uw16b: {"code": 0x7B, "offset": 0xD505C, "room gfx": 0xD8DC2, "rule": "Roc"},
    lname.uw19:  {"code": 0x7C, "offset": 0xD5344, "room gfx": 0xD8E4E},
    lname.uw23:  {"code": 0xAE, "offset": 0xD53B0, "room gfx": 0xD8EA2, "type": "boss"},
    lname.uw24:  {"code": 0x80, "offset": 0xD5434, "room gfx": 0xD8F12},
    lname.uw25:  {"code": 0x7D, "offset": 0xD4FC0, "room gfx": 0xD8DA6},
    # Underground Waterway
    lname.uy1:   {"code": 0x93, "offset": 0xD5F98, "room gfx": 0xD91CE},
    lname.uy3:   {"code": 0x8B, "offset": 0xD5FEC, "room gfx": 0xD9206},
    lname.uy3b:  {"code": 0x8A, "offset": 0xD5FE0, "room gfx": 0xD9206},
    lname.uy4:   {"code": 0x94, "offset": 0xD697C, "room gfx": 0xD93AA},
    lname.uy5:   {"code": 0x8C, "offset": 0xD6214, "room gfx": 0xD923E, "rule": "Freeze"},
    lname.uy7:   {"code": 0x8D, "offset": 0xD65A4, "room gfx": 0xD9292},
    lname.uy8:   {"code": 0x95, "offset": 0xD69A0, "room gfx": 0xD93C6, "rule": "Roc"},
    lname.uy9:   {"code": 0x8E, "offset": 0xD640C, "room gfx": 0xD9276},
    lname.uy9b:  {"code": 0x8F, "offset": 0xD6418, "room gfx": 0xD9276},
    lname.uy12:  {"code": 0x91, "offset": 0xD673C, "room gfx": 0xD92E6, "rule": "Cleansing"},
    lname.uy12b: {"code": 0x90, "offset": 0xD6730, "room gfx": 0xD92E6},
    lname.uy13:  {"code": 0x92, "offset": 0xD685C, "room gfx": 0xD9302, "rule": "Roc"},
    lname.uy17:  {"code": 0xAF, "offset": 0xD6940, "room gfx": 0xD9372, "rule": "Cleansing", "type": "boss"},
    lname.uy18:  {"code": 0x96, "offset": 0xD69C4, "room gfx": 0xD93E2, "rule": "Roc"},
    # Observation Tower
    lname.ot1:   {"code": 0x9D, "offset": 0xD6B38, "room gfx": 0xD9436},
    lname.ot2:   {"code": 0xA4, "offset": 0xD760C, "room gfx": 0xD96D6},
    lname.ot3:   {"code": 0x9F, "offset": 0xD72E8, "room gfx": 0xD9612},
    lname.ot5:   {"code": 0xA5, "offset": 0xD75E8, "room gfx": 0xD96BA},
    lname.ot8:   {"code": 0xA0, "offset": 0xD71EC, "room gfx": 0xD95DA},
    lname.ot9:   {"code": 0xA2, "offset": 0xD6FE8, "room gfx": 0xD9586},
    lname.ot12:  {"code": 0xA6, "offset": 0xD75C4, "room gfx": 0xD969E},
    lname.ot13:  {"code": 0xA3, "offset": 0xD6F64, "room gfx": 0xD954E},
    lname.ot16:  {"code": 0xA1, "offset": 0xD751C, "room gfx": 0xD9682},
    lname.ot20:  {"code": 0xB0, "offset": 0xD6E20, "room gfx": 0xD94A6, "type": "boss"},
    # Ceremonial Room
    lname.cr1:   {"code": 0xA7, "offset": 0xD7690, "room gfx": 0xD972A},
    lname.victory: {"event": iname.victory}
    # Battle Arena
    # lname.ba24:  {"code": 0xB2, "offset": 0xD7D20, "room gfx": 0xD99E6},
 }


def get_location_info(location: str, info: str) -> Union[int, str, List[str], None]:
    return location_info[location].get(info, None)


def get_all_location_names() -> List[str]:
    return [loc_name for loc_name in location_info]


def get_location_names_to_ids() -> Dict[str, int]:
    return {name: get_location_info(name, "code")+base_id for name in location_info if get_location_info(name, "code")
            is not None}


def get_locations_by_area() -> Dict[str, Set[str]]:
    areas_to_locations = {}

    for loc_name in location_info:
        # If we are looking at an event Location, don't include it.
        if get_location_info(loc_name, "event") is not None:
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
    events = {}

    for loc in locations:
        # If Break Iron Maidens is on, don't place the Broke Iron Maidens Location.
        if loc == lname.ct_switch and options.break_iron_maidens:
            continue

        loc_code = get_location_info(loc, "code")

        # If we are looking at an event Location, add its associated event Item to the events' dict.
        # Otherwise, add the base_id to the Location's code.
        if loc_code is None:
            events[loc] = get_location_info(loc, "event")
        else:
            loc_code += base_id
        locations_with_ids.update({loc: loc_code})

        # If Require All Bosses is on, add a Last Key to the events dict for all Locations marked "boss" for their type.
        if options.require_all_bosses and get_location_info(loc, "type") in ["boss", "max up boss"]:
            events[loc] = iname.last_key

    return locations_with_ids, events
