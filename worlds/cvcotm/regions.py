from .data import lname
from typing import Dict, List, Optional, TypedDict, Union


class RegionInfo(TypedDict, total=False):
    locations: List[str]
    entrances: Dict[str, str]


# # #    KEY    # # #
# "locations" = A list of the Locations to add to that Region when adding said Region.
# "entrances" = A dict of the connecting Regions to the Entrances' names to add to that Region when adding said Region.
cvcotm_region_info: Dict[str, RegionInfo] = {
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
                 "entrances": {"Abyss Stairway": "Catacomb to Stairway"}},

    "Abyss Stairway": {"locations": [lname.as2,
                                     lname.as3],
                       "entrances": {"Audience Room": "Stairway to Audience"}},

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
                      "entrances": {"Machine Tower Bottom": "Audience to Machine Bottom",
                                    "Machine Tower Top": "Audience to Machine Top",
                                    "Chapel Tower Bottom": "Audience to Chapel",
                                    "Underground Gallery Lower": "Audience to Gallery",
                                    "Underground Warehouse Start": "Audience to Warehouse",
                                    "Underground Waterway Start": "Audience to Waterway",
                                    "Observation Tower": "Audience to Observation",
                                    "Ceremonial Room": "Ceremonial Door"}},

    "Machine Tower Bottom": {"locations": [lname.mt0,
                                           lname.mt2,
                                           lname.mt3,
                                           lname.mt4,
                                           lname.mt6,
                                           lname.mt8,
                                           lname.mt10,
                                           lname.mt11],
                             "entrances": {"Machine Tower Top": "Machine Bottom to Top"}},

    "Machine Tower Top": {"locations": [lname.mt13,
                                        lname.mt14,
                                        lname.mt17,
                                        lname.mt19]},

    "Eternal Corridor Pit": {"locations": [lname.ec5],
                             "entrances": {"Underground Gallery Upper": "Corridor to Gallery",
                                           "Chapel Tower Bottom": "Escape the Gallery Pit"}},

    "Chapel Tower Bottom": {"locations": [lname.ec7,
                                          lname.ec9,
                                          lname.ct1,
                                          lname.ct4,
                                          lname.ct5,
                                          lname.ct6,
                                          lname.ct6b,
                                          lname.ct8,
                                          lname.ct10,
                                          lname.ct13,
                                          lname.ct15],
                            "entrances": {"Eternal Corridor Pit": "Into the Corridor Pit",
                                          "Underground Waterway End": "Dip Into Waterway End",
                                          "Chapel Tower Top": "Climb to Chapel Top"}},

    "Chapel Tower Top": {"locations": [lname.ct16,
                                       lname.ct18,
                                       lname.ct21,
                                       lname.ct22],
                         "entrances": {"Battle Arena": "Arena Passage"}},

    "Battle Arena": {"locations": [lname.ct26,
                                   lname.ct26b,
                                   lname.ba24,
                                   lname.arena_victory]},

    "Underground Gallery Upper": {"locations": [lname.ug0,
                                                lname.ug1,
                                                lname.ug2,
                                                lname.ug3,
                                                lname.ug3b],
                                  "entrances": {"Eternal Corridor Pit": "Gallery to Corridor",
                                                "Underground Gallery Lower": "Gallery Upper to Lower"}},

    "Underground Gallery Lower": {"locations": [lname.ug8,
                                                lname.ug10,
                                                lname.ug13,
                                                lname.ug15,
                                                lname.ug20],
                                  "entrances": {"Underground Gallery Upper": "Gallery Lower to Upper"}},

    "Underground Warehouse Start": {"locations": [lname.uw1],
                                    "entrances": {"Underground Warehouse Main": "Into Warehouse Main"}},

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
                                   "entrances": {"Underground Waterway Main": "Into Waterway Main"}},

    "Underground Waterway Main": {"locations": [lname.uy3,
                                                lname.uy3b,
                                                lname.uy4,
                                                lname.uy5,
                                                lname.uy7,
                                                lname.uy8,
                                                lname.uy9,
                                                lname.uy9b,
                                                lname.uy12],
                                  "entrances": {"Underground Waterway End": "Onward to Waterway End"}},

    "Underground Waterway End": {"locations": [lname.uy12b,
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


def get_region_info(region: str, info: str) -> Optional[Union[List[str], Dict[str, str]]]:
    return cvcotm_region_info[region].get(info, None)


def get_all_region_names() -> List[str]:
    return [reg_name for reg_name in cvcotm_region_info]
