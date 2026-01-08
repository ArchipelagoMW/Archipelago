from typing import NamedTuple, TYPE_CHECKING

from BaseClasses import Location
from . import game_data, items

if TYPE_CHECKING:
    from . import MkddWorld


TAG_CUP_PERFECT = "Perfect Cup"
TAG_CUP_GOLD = "Gold Cup"
TAG_CUP_SILVER = "Silver Cup"
TAG_CUP_BRONZE = "Bronze Cup"
TAG_CUP_FINISH = "Finish Cup"
TAG_CUP_TROPHY = "Cup Trophy"
TAG_COURSE_FIRST = "Finish First"
TAG_COURSE_LEAD = "Take The Lead"
TAG_COURSE_FINISH = "Finish Course"
TAG_WIN_COMBO = "Win With Certain Characters"
TAG_TT = "Time Trial"
TAG_TT_GOOD = "Time Trial Good Time"
TAG_TT_GHOST = "Time Trial Staff Ghost"


class MkddLocation(Location):
    game = "Mario Kart Double Dash"


class MkddLocationData(NamedTuple):
    name: str
    difficulty: int = 0
    region: str = "Menu"
    required_items: dict[str, int] = {}
    tags: set[str] = {}

def get_loc_name_cup(cup: str, ranking: int, vehicle_class: int) -> str:
    try:
        rank_name = ["Gold", "Silver", "Bronze"][ranking]
        class_name = ["50cc", "100cc", "150cc", "Mirror"][vehicle_class]
        return f"{cup} {rank_name} {class_name}"
    except:
        return ""

def get_loc_name_trophy(cup: str, vehicle_class: int) -> str:
    try:
        class_name = ["50cc", "100cc", "150cc", "Mirror"][vehicle_class]
        return f"{cup} Gold {class_name} (Trophy)"
    except:
        return ""

def get_loc_name_perfect(cup: str) -> str:
    return f"{cup} Perfect"

def get_loc_name_finish(course_or_cup: str) -> str:
    return f"{course_or_cup} Finish"

def get_loc_name_lead(course: str) -> str:
    return f"{course} Take The Lead"

def get_loc_name_first(course: str) -> str:
    return f"{course} 1st"

def get_loc_name_good_time(course: game_data.Course) -> str:
    seconds = course.good_time
    minutes = int(seconds / 60)
    seconds -= minutes * 60
    return f"{course.name} Time Trial in {minutes}:{seconds:02d}"

def get_loc_name_ghost(course: str) -> str:
    return f"{course} Defeat Staff Ghost"

def get_loc_name_win_char_kart(character: str, kart: str) -> str:
    return f"Win With {character} Driving {kart}"

def get_loc_name_win_characters(character1: str, character2: str) -> str:
    return f"Win With {character1} and {character2}"

def get_loc_name_win_course_char(course: game_data.Course) -> str:
    characters = [game_data.CHARACTERS[character].name for character in course.owners]
    if len(characters) == 1:
        return f"Win in {course.name} With {characters[0]}"
    else:
        return f"Win in {course.name} With {characters[0]} and {characters[1]}"


data_table: list[MkddLocationData] = [MkddLocationData("", 0)] # Id 0 is reserved.

# Cup related locations.
for cup in game_data.NORMAL_CUPS:
    data_table.append(MkddLocationData(get_loc_name_finish(cup), 0, cup, tags = {cup, TAG_CUP_FINISH}))
    data_table.append(MkddLocationData(get_loc_name_perfect(cup), 70, cup, tags = {cup, TAG_CUP_PERFECT}))
    # 50cc
    data_table.append(MkddLocationData(get_loc_name_cup(cup, 2, 0), 10, cup, tags = {cup, TAG_CUP_BRONZE}))
    data_table.append(MkddLocationData(get_loc_name_cup(cup, 1, 0), 20, cup, tags = {cup, TAG_CUP_SILVER}))
    data_table.append(MkddLocationData(get_loc_name_cup(cup, 0, 0), 40, cup, tags = {cup, TAG_CUP_GOLD}))
    data_table.append(MkddLocationData(get_loc_name_trophy(cup, 0), 40, cup, tags = {TAG_CUP_TROPHY}))
    # 100cc
    data_table.append(MkddLocationData(get_loc_name_cup(cup, 2, 1), 40, cup, {items.PROGRESSIVE_CLASS:1}, {cup, TAG_CUP_BRONZE}))
    data_table.append(MkddLocationData(get_loc_name_cup(cup, 1, 1), 60, cup, {items.PROGRESSIVE_CLASS:1}, {cup, TAG_CUP_SILVER}))
    data_table.append(MkddLocationData(get_loc_name_cup(cup, 0, 1), 70, cup, {items.PROGRESSIVE_CLASS:1}, {cup, TAG_CUP_GOLD}))
    data_table.append(MkddLocationData(get_loc_name_trophy(cup, 1), 70, cup, {items.PROGRESSIVE_CLASS:1}, {TAG_CUP_TROPHY}))
    # 150cc
    data_table.append(MkddLocationData(get_loc_name_cup(cup, 2, 2), 60, cup, {items.PROGRESSIVE_CLASS:2}, {cup, TAG_CUP_BRONZE}))
    data_table.append(MkddLocationData(get_loc_name_cup(cup, 1, 2), 80, cup, {items.PROGRESSIVE_CLASS:2}, {cup, TAG_CUP_SILVER}))
    data_table.append(MkddLocationData(get_loc_name_cup(cup, 0, 2), 90, cup, {items.PROGRESSIVE_CLASS:2}, {cup, TAG_CUP_GOLD}))
    data_table.append(MkddLocationData(get_loc_name_trophy(cup, 2), 90, cup, {items.PROGRESSIVE_CLASS:2}, {TAG_CUP_TROPHY}))
    # Mirror
    data_table.append(MkddLocationData(get_loc_name_cup(cup, 2, 3), 70, cup, {items.PROGRESSIVE_CLASS:3}, {cup, TAG_CUP_BRONZE}))
    data_table.append(MkddLocationData(get_loc_name_cup(cup, 1, 3), 90, cup, {items.PROGRESSIVE_CLASS:3}, {cup, TAG_CUP_SILVER}))
    data_table.append(MkddLocationData(get_loc_name_cup(cup, 0, 3), 100, cup, {items.PROGRESSIVE_CLASS:3}, {cup, TAG_CUP_GOLD}))
    data_table.append(MkddLocationData(get_loc_name_trophy(cup, 3), 100, cup, {items.PROGRESSIVE_CLASS:3}, {TAG_CUP_TROPHY}))

# Course related locations.
for course in game_data.RACE_COURSES:
    data_table.append(MkddLocationData(get_loc_name_finish(course.name), 0, course.name, tags = {course.name, TAG_COURSE_FINISH}))
    data_table.append(MkddLocationData(get_loc_name_lead(course.name), 30, course.name + " GP", tags = {course.name, TAG_COURSE_LEAD}))
    data_table.append(MkddLocationData(get_loc_name_first(course.name), 40, course.name + " GP", tags = {course.name, TAG_COURSE_FIRST}))
    data_table.append(MkddLocationData(get_loc_name_good_time(course), 60, course.name + " TT", tags = {course.name, TAG_TT, TAG_TT_GOOD}))
    data_table.append(MkddLocationData(get_loc_name_ghost(course.name), 100, course.name + " TT", tags = {course.name, TAG_TT, TAG_TT_GHOST}))

# Win with default character pairs.
for character_id in range(0, len(game_data.CHARACTERS), 2):
    character1 = game_data.CHARACTERS[character_id]
    character2 = game_data.CHARACTERS[character_id + 1]
    data_table.append(MkddLocationData(get_loc_name_win_characters(character1.name, character2.name), 40, "Menu", {character1.name:1, character2.name:1}, {TAG_WIN_COMBO}))

# Win with a default kart + character combination.
for character in game_data.CHARACTERS:
    kart = game_data.KARTS[character.default_kart]
    data_table.append(MkddLocationData(get_loc_name_win_char_kart(character.name, kart.name), 40, "Menu", {character.name:1, kart.name:1}, {TAG_WIN_COMBO}))

# Win courses with certain characters.
for course in [course for course in game_data.RACE_COURSES if len(course.owners) > 0]:
    data_table.append(MkddLocationData(get_loc_name_win_course_char(course), 40, course.name + " GP", {game_data.CHARACTERS[o].name:1 for o in course.owners}, {course.name, TAG_WIN_COMBO}))

# Misc locations.
GOLD_LIGHT = "Win Gold With a Light Kart"
GOLD_MEDIUM = "Win Gold With a Medium Kart"
GOLD_HEAVY = "Win Gold With a Heavy Kart"
GOLD_PARADE = "Win Gold With Parade Kart"
TROPHY_GOAL = "Trophy Goal Completed"
WIN_ALL_CUP_TOUR = "All Cup Tour Gold"

# Don't define difficulty here, it will be handled by rules.
data_table.append(MkddLocationData(GOLD_LIGHT, 0))
data_table.append(MkddLocationData(GOLD_MEDIUM, 0))
data_table.append(MkddLocationData(GOLD_HEAVY, 0))
data_table.append(MkddLocationData(GOLD_PARADE, 40, required_items = {"Parade Kart":1}))
data_table.append(MkddLocationData(TROPHY_GOAL, 0))
data_table.append(MkddLocationData(WIN_ALL_CUP_TOUR, 0, game_data.CUPS[game_data.CUP_ALL_CUP_TOUR]))

name_to_id: dict[str, int] = {data.name:id for (id, data) in enumerate(data_table) if id > 0}

group_names: set[str] = set()
for data in data_table:
    group_names.update(data.tags)
groups: dict[str: set[str]] = {
    group:{data.name for data in data_table if group in data.tags} 
    for group in group_names
}