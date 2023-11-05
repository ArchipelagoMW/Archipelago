from .map import Map
from .roomtype.town import Town
from .roomtype.mountain import Mountain, MountainEgg
from .roomtype.forest import Forest
from .roomtype.base import RoomType
from .roomtype.water import Water, Beach
import random


def is_area_clear(the_map: Map, x, y, w, h):
    for y0 in range(y, y+h):
        for x0 in range(x, x+w):
            if 0 <= x0 < the_map.w and 0 <= y0 < the_map.h:
                if the_map.get(x0, y0).room_type is not None:
                    return False
    return True


def find_random_clear_area(the_map: Map, w, h, *, tries):
    for n in range(tries):
        x = random.randint(0, the_map.w - w)
        y = random.randint(0, the_map.h - h)
        if is_area_clear(the_map, x - 1, y - 1, w + 2, h + 2):
            return x, y
    return None, None


def setup_room_types(the_map: Map):
    # Always make the rop row mountains.
    egg_x = the_map.w // 2
    for x in range(the_map.w):
        if x == egg_x:
            MountainEgg(the_map.get(x, 0))
        else:
            Mountain(the_map.get(x, 0))

    # Add some beach.
    width = the_map.w if random.random() < 0.5 else random.randint(max(2, the_map.w // 4), the_map.w // 2)
    beach_x = 0  # current tileset doesn't allow anything else
    for x in range(beach_x, beach_x+width):
        # Beach(the_map.get(x, the_map.h - 2))
        Beach(the_map.get(x, the_map.h - 1))
    the_map.get(beach_x + width - 1, the_map.h - 1).edge_right.force_solid()

    town_x, town_y = find_random_clear_area(the_map, 2, 2, tries=20)
    if town_x is not None:
        for y in range(town_y, town_y + 2):
            for x in range(town_x, town_x + 2):
                Town(the_map.get(x, y))

    forest_w, forest_h = 2, 2
    if random.random() < 0.5:
        forest_w += 1
    else:
        forest_h += 1
    forest_x, forest_y = find_random_clear_area(the_map, forest_w, forest_h, tries=20)
    if forest_x is None:
        forest_w, forest_h = 2, 2
        forest_x, forest_y = find_random_clear_area(the_map, forest_w, forest_h, tries=20)
    if forest_x is not None:
        for y in range(forest_y, forest_y + forest_h):
            for x in range(forest_x, forest_x + forest_w):
                Forest(the_map.get(x, y))

    # for n in range(5):
    #     water_w, water_h = 2, 1
    #     if random.random() < 0.5:
    #         water_w, water_h = water_h, water_w
    #     water_x, water_y = find_random_clear_area(the_map, water_w, water_h, tries=20)
    #     if water_x is not None:
    #         for y in range(water_y, water_y + water_h):
    #             for x in range(water_x, water_x + water_w):
    #                 Water(the_map.get(x, y))

    for y in range(the_map.h):
        for x in range(the_map.w):
            if the_map.get(x, y).room_type is None:
                RoomType(the_map.get(x, y))
