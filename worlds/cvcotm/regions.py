from .data import lname
from typing import List, Optional, Dict

# # #    KEY    # # #
# "locations" = The Locations to add to that Region when putting in said Region.
# "entrances" = The Entrances to add to that Region when putting in said Region.
cvcotm_region_info = {
    "Menu": {"entrances": ["At an Old Austrian Castle"]},

    "Catacomb": {"locations": [lname.sr3,
                               lname.cc1,
                               lname.cc3,
                               lname.cc3b,
                               lname.cc4,
                               lname.cc5,
                               lname.cc8,
                               lname.cc8b,
                               lname.cc9,
                               lname.cc10,
                               lname.cc13,
                               lname.cc14,
                               lname.cc14b,
                               lname.cc16,
                               lname.cc20,
                               lname.cc22,
                               lname.cc24,
                               lname.cc25],
                 "entrances": ["Catacomb to Stairway"]},

    "Abyss Stairway": {"locations": [lname.as2,
                                     lname.as3],
                       "entrances": ["Stairway to Audience"]},

    "Audience Room": {"locations": [lname.as4,
                                    lname.as9,
                                    lname.ar4,
                                    lname.ar7,
                                    lname.ar8,
                                    lname.ar9,
                                    lname.ar10,
                                    lname.ar11,
                                    lname.ar14,
                                    lname.ar14b,
                                    lname.ar16,
                                    lname.ar17,
                                    lname.ar17b,
                                    lname.ar18,
                                    lname.ar19,
                                    lname.ar21,
                                    lname.ar25,
                                    lname.ar26,
                                    lname.ar27,
                                    lname.ar30,
                                    lname.ar30b,
                                    lname.ow0,
                                    lname.ow1,
                                    lname.ow2,
                                    lname.th1,
                                    lname.th3],
                      "entrances": ["Audience to Machine Bottom",
                                    "Audience to Machine Top",
                                    "Audience to Chapel",
                                    "Audience to Gallery",
                                    "Audience to Warehouse",
                                    "Audience to Waterway",
                                    "Audience to Observation",
                                    "Ceremonial Door"]},

    "Machine Tower Bottom": {"locations": [lname.mt0,
                                           lname.mt2,
                                           lname.mt3,
                                           lname.mt4,
                                           lname.mt6,
                                           lname.mt8,
                                           lname.mt10,
                                           lname.mt11],
                             "entrances": ["Machine Bottom to Top"]},

    "Machine Tower Top": {"locations": [lname.mt13,
                                        lname.mt14,
                                        lname.mt17,
                                        lname.mt19]},

    "Eternal Corridor Pit": {"locations": [lname.ec5],
                             "entrances": ["Corridor to Gallery"]},

    "Chapel Tower": {"locations": [lname.ec7,
                                   lname.ec9,
                                   lname.ct1,
                                   lname.ct4,
                                   lname.ct5,
                                   lname.ct6,
                                   lname.ct6b,
                                   lname.ct8,
                                   lname.ct10,
                                   lname.ct13,
                                   lname.ct15,
                                   lname.ct16,
                                   lname.ct18,
                                   lname.ct_switch,
                                   lname.ct22],
                     "entrances": ["Into the Corridor Pit",
                                   "Dip Into Waterway End",
                                   "Arena Passage"]},

    "Battle Arena": {"locations": [lname.ct26,
                                   lname.ct26b,
                                   lname.ba24]},

    "Underground Gallery Upper": {"locations": [lname.ug0,
                                                lname.ug1,
                                                lname.ug2,
                                                lname.ug3,
                                                lname.ug3b],
                                  "entrances": ["Gallery to Corridor",
                                                "Gallery Upper to Lower"]},

    "Underground Gallery Lower": {"locations": [lname.ug8,
                                                lname.ug10,
                                                lname.ug13,
                                                lname.ug15,
                                                lname.ug20],
                                  "entrances": ["Gallery Lower to Upper"]},

    "Underground Warehouse Start": {"locations": [lname.uw1],
                                    "entrances": ["Into Warehouse Main"]},

    "Underground Warehouse Main": {"locations": [lname.uw6,
                                                 lname.uw8,
                                                 lname.uw9,
                                                 lname.uw10,
                                                 lname.uw11,
                                                 lname.uw14,
                                                 lname.uw16,
                                                 lname.uw16b,
                                                 lname.uw19,
                                                 lname.uw23,
                                                 lname.uw24,
                                                 lname.uw25]},

    "Underground Waterway Start": {"locations": [lname.uy1],
                                   "entrances": ["Into Waterway Main"]},

    "Underground Waterway Main": {"locations": [lname.uy3,
                                                lname.uy3b,
                                                lname.uy4,
                                                lname.uy5,
                                                lname.uy7,
                                                lname.uy8,
                                                lname.uy9,
                                                lname.uy9b,
                                                lname.uy12b],
                                  "entrances": ["Onward to Waterway End"]},

    "Underground Waterway End": {"locations": [lname.uy12,
                                               lname.uy13,
                                               lname.uy17,
                                               lname.uy18]},

    "Observation Tower": {"locations": [lname.ot1,
                                        lname.ot2,
                                        lname.ot3,
                                        lname.ot5,
                                        lname.ot8,
                                        lname.ot9,
                                        lname.ot12,
                                        lname.ot13,
                                        lname.ot16,
                                        lname.ot20]},

    "Ceremonial Room": {"locations": [lname.cr1,
                                      lname.dracula]},
}

# # #    KEY    # # #
# "connection" = The name of the Region the Entrance connects into.
# "rule" = What rule should be applied to the Entrance during set_rules, as defined in self.rules in the CVCotMRules
#          class definition in rules.py.
cvcotm_entrance_info = {
    "At an Old Austrian Castle": {"destination": "Catacomb"},
    "Catacomb to Stairway": {"destination": "Abyss Stairway", "rule": "Double OR Kick"},
    "Stairway to Audience": {"destination": "Audience Room", "rule": "Double"},
    "Audience to Machine Bottom": {"destination": "Machine Tower Bottom", "rule": "Tackle"},
    "Audience to Machine Top": {"destination": "Machine Tower Top", "rule": "Kick"},
    "Audience to Chapel": {"destination": "Chapel Tower", "rule": "Kick"},
    "Audience to Gallery": {"destination": "Underground Gallery Lower", "rule": "Iron Maiden AND Push"},
    "Audience to Warehouse": {"destination": "Underground Warehouse Start", "rule": "Push"},
    "Audience to Waterway": {"destination": "Underground Waterway Start", "rule": "Iron Maiden"},
    "Audience to Observation": {"destination": "Observation Tower", "rule": "Roc"},
    "Ceremonial Door": {"destination": "Ceremonial Room", "rule": "Last Keys"},
    "Machine Bottom to Top": {"destination": "Machine Tower Top"},
    "Corridor to Gallery": {"destination": "Underground Gallery Upper", "rule": "Iron Maiden"},
    "Arena Passage": {"destination": "Battle Arena", "rule": "Push AND Roc"},
    "Into the Corridor Pit": {"destination": "Eternal Corridor Pit"},
    "Dip Into Waterway End": {"destination": "Underground Waterway End", "rule": "Roc"},
    "Gallery to Corridor": {"destination": "Eternal Corridor Pit"},
    "Gallery Upper to Lower": {"destination": "Underground Gallery Lower", "rule": "Tackle"},
    "Gallery Lower to Upper": {"destination": "Underground Gallery Upper", "rule": "Tackle"},
    "Into Warehouse Main": {"destination": "Underground Warehouse Main", "rule": "Tackle"},
    "Into Waterway Main": {"destination": "Underground Waterway Main", "rule": "Cleansing"},
    "Onward to Waterway End": {"destination": "Underground Waterway End"},
}


def get_region_info(region: str, info: str) -> Optional[List[str]]:
    return cvcotm_region_info[region].get(info, None)


def get_entrance_info(entrance: str, info: str) -> Optional[str]:
    return cvcotm_entrance_info[entrance].get(info, None)


def get_all_region_names() -> List[str]:
    return [reg_name for reg_name in cvcotm_region_info]


def get_named_entrances_data(entrances: List[str]) -> Dict[str, str]:
    entrances_with_destinations = {}

    # Get all the Entrances' destinations and put them in a dict with said Entrance names.
    for ent_name in entrances:
        entrances_with_destinations.update({get_entrance_info(ent_name, "destination"): ent_name})

    return entrances_with_destinations
