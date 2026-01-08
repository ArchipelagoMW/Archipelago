from typing import NamedTuple
from . import game_data

class MkddRegionData(NamedTuple):
    connecting_regions: list[str] = []
    tags: set[str] = set()

TAG_TIME_TRIALS = "Time Trials"


data_table: dict[str, MkddRegionData] = {}

cup_regions: dict[str, MkddRegionData] = {cup:MkddRegionData() for cup in game_data.CUPS}

course_regions: dict[str, MkddRegionData] = {}
course_gp_regions: dict[str, MkddRegionData] = {}
course_tt_regions: dict[str, MkddRegionData] = {}
for course in game_data.RACE_COURSES:
    course_regions[course.name] = MkddRegionData()
    course_gp_regions[course.name + " GP"] = MkddRegionData([course.name])
    course_tt_regions[course.name + " TT"] = MkddRegionData([course.name], {TAG_TIME_TRIALS})

data_table = {
    "Menu": MkddRegionData([region for region in {**cup_regions, **course_tt_regions}]),
    **cup_regions,
    **course_regions,
    **course_gp_regions,
    **course_tt_regions,
}