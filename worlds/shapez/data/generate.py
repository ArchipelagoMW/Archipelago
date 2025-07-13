import itertools
import time
from typing import Dict, List

from worlds.shapez.data.strings import SHAPESANITY, REGIONS

shapesanity_simple: Dict[str, str] = {}
shapesanity_1_4: Dict[str, str] = {}
shapesanity_two_sided: Dict[str, str] = {}
shapesanity_three_parts: Dict[str, str] = {}
shapesanity_four_parts: Dict[str, str] = {}
subshape_names = [SHAPESANITY.circle, SHAPESANITY.square, SHAPESANITY.star, SHAPESANITY.windmill]
color_names = [SHAPESANITY.red, SHAPESANITY.blue, SHAPESANITY.green, SHAPESANITY.yellow, SHAPESANITY.purple,
               SHAPESANITY.cyan, SHAPESANITY.white, SHAPESANITY.uncolored]
short_subshapes = ["C", "R", "S", "W"]
short_colors = ["b", "c", "g", "p", "r", "u", "w", "y"]


def color_to_needed_building(color_list: List[str]) -> str:
    for next_color in color_list:
        if next_color in [SHAPESANITY.yellow, SHAPESANITY.purple, SHAPESANITY.cyan, SHAPESANITY.white,
                          "y", "p", "c", "w"]:
            return REGIONS.mixed
    for next_color in color_list:
        if next_color not in [SHAPESANITY.uncolored, "u"]:
            return REGIONS.painted
    return REGIONS.uncol


def generate_shapesanity_pool() -> None:
    # same shapes && same color
    for color in color_names:
        color_region = color_to_needed_building([color])
        shapesanity_simple[SHAPESANITY.full(color, SHAPESANITY.circle)] = REGIONS.sanity(REGIONS.full, color_region)
        shapesanity_simple[SHAPESANITY.full(color, SHAPESANITY.square)] = REGIONS.sanity(REGIONS.full, color_region)
        shapesanity_simple[SHAPESANITY.full(color, SHAPESANITY.star)] = REGIONS.sanity(REGIONS.full, color_region)
        shapesanity_simple[SHAPESANITY.full(color, SHAPESANITY.windmill)] = REGIONS.sanity(REGIONS.east_wind, color_region)
    for shape in subshape_names:
        for color in color_names:
            color_region = color_to_needed_building([color])
            shapesanity_simple[SHAPESANITY.half(color, shape)] = REGIONS.sanity(REGIONS.half, color_region)
            shapesanity_simple[SHAPESANITY.piece(color, shape)] = REGIONS.sanity(REGIONS.piece, color_region)
            shapesanity_simple[SHAPESANITY.cutout(color, shape)] = REGIONS.sanity(REGIONS.stitched, color_region)
            shapesanity_simple[SHAPESANITY.cornered(color, shape)] = REGIONS.sanity(REGIONS.stitched, color_region)

    # one color && 4 shapes (including empty)
    for first_color, second_color, third_color, fourth_color in itertools.combinations(short_colors+["-"], 4):
        colors = [first_color, second_color, third_color, fourth_color]
        color_region = color_to_needed_building(colors)
        shape_regions = [REGIONS.stitched, REGIONS.stitched] if fourth_color == "-" else [REGIONS.col_full, REGIONS.col_east_wind]
        color_code = ''.join(colors)
        shapesanity_1_4[SHAPESANITY.full(color_code, SHAPESANITY.circle)] = REGIONS.sanity(shape_regions[0], color_region)
        shapesanity_1_4[SHAPESANITY.full(color_code, SHAPESANITY.square)] = REGIONS.sanity(shape_regions[0], color_region)
        shapesanity_1_4[SHAPESANITY.full(color_code, SHAPESANITY.star)] = REGIONS.sanity(shape_regions[0], color_region)
        shapesanity_1_4[SHAPESANITY.full(color_code, SHAPESANITY.windmill)] = REGIONS.sanity(shape_regions[1], color_region)

    # one shape && 4 colors (including empty)
    for first_shape, second_shape, third_shape, fourth_shape in itertools.combinations(short_subshapes+["-"], 4):
        for color in color_names:
            shapesanity_1_4[SHAPESANITY.full(color, ''.join([first_shape, second_shape, third_shape, fourth_shape]))] \
                = REGIONS.sanity(REGIONS.stitched, color_to_needed_building([color]))

    combos = [shape + color for shape in short_subshapes for color in short_colors]
    for first_combo, second_combo in itertools.permutations(combos, 2):
        # 2-sided shapes
        color_region = color_to_needed_building([first_combo[1], second_combo[1]])
        ordered_combo = " ".join(sorted([first_combo, second_combo]))
        shape_regions = (([REGIONS.east_wind, REGIONS.east_wind, REGIONS.col_half]
                          if first_combo[0] == "W" else [REGIONS.col_full, REGIONS.col_full, REGIONS.col_half])
                         if first_combo[0] == second_combo[0] else [REGIONS.stitched, REGIONS.half_half, REGIONS.stitched])
        shapesanity_two_sided[SHAPESANITY.three_one(first_combo, second_combo)] = REGIONS.sanity(shape_regions[0], color_region)
        shapesanity_two_sided[SHAPESANITY.halfhalf(ordered_combo)] = REGIONS.sanity(shape_regions[1], color_region)
        shapesanity_two_sided[SHAPESANITY.checkered(ordered_combo)] = REGIONS.sanity(shape_regions[0], color_region)
        shapesanity_two_sided[SHAPESANITY.singles(ordered_combo, SHAPESANITY.adjacent_pos)] = REGIONS.sanity(shape_regions[2], color_region)
        shapesanity_two_sided[SHAPESANITY.singles(ordered_combo, SHAPESANITY.cornered_pos)] = REGIONS.sanity(REGIONS.stitched, color_region)
        shapesanity_two_sided[SHAPESANITY.two_one(first_combo, second_combo, SHAPESANITY.adjacent_pos)] = REGIONS.sanity(REGIONS.stitched, color_region)
        shapesanity_two_sided[SHAPESANITY.two_one(first_combo, second_combo, SHAPESANITY.cornered_pos)] = REGIONS.sanity(REGIONS.stitched, color_region)
        for third_combo in combos:
            if third_combo in [first_combo, second_combo]:
                continue
            # 3-part shapes
            colors = [first_combo[1], second_combo[1], third_combo[1]]
            color_region = color_to_needed_building(colors)
            ordered_two = " ".join(sorted([second_combo, third_combo]))
            if not (first_combo[1] == second_combo[1] == third_combo[1] or
                    first_combo[0] == second_combo[0] == third_combo[0]):
                ordered_all = " ".join(sorted([first_combo, second_combo, third_combo]))
                shapesanity_three_parts[SHAPESANITY.singles(ordered_all)] = REGIONS.sanity(REGIONS.stitched, color_region)
            shape_regions = ([REGIONS.stitched, REGIONS.stitched] if not second_combo[0] == third_combo[0]
                             else (([REGIONS.east_wind, REGIONS.east_wind] if first_combo[0] == "W"
                                    else [REGIONS.col_full, REGIONS.col_full])
                                   if first_combo[0] == second_combo[0] else [REGIONS.col_half_half, REGIONS.stitched]))
            shapesanity_three_parts[SHAPESANITY.two_one_one(first_combo, ordered_two, SHAPESANITY.adjacent_pos)] \
                = REGIONS.sanity(shape_regions[0], color_region)
            shapesanity_three_parts[SHAPESANITY.two_one_one(first_combo, ordered_two, SHAPESANITY.cornered_pos)] \
                = REGIONS.sanity(shape_regions[1], color_region)
            for fourth_combo in combos:
                if fourth_combo in [first_combo, second_combo, third_combo]:
                    continue
                if (first_combo[1] == second_combo[1] == third_combo[1] == fourth_combo[1] or
                    first_combo[0] == second_combo[0] == third_combo[0] == fourth_combo[0]):
                    continue
                colors = [first_combo[1], second_combo[1], third_combo[1], fourth_combo[1]]
                color_region = color_to_needed_building(colors)
                ordered_all = " ".join(sorted([first_combo, second_combo, third_combo, fourth_combo]))
                if ((first_combo[0] == second_combo[0] and third_combo[0] == fourth_combo[0]) or
                    (first_combo[0] == third_combo[0] and second_combo[0] == fourth_combo[0]) or
                    (first_combo[0] == fourth_combo[0] and third_combo[0] == second_combo[0])):
                    shapesanity_four_parts[SHAPESANITY.singles(ordered_all)] = REGIONS.sanity(REGIONS.col_half_half, color_region)
                else:
                    shapesanity_four_parts[SHAPESANITY.singles(ordered_all)] = REGIONS.sanity(REGIONS.stitched, color_region)


if __name__ == "__main__":
    start = time.time()
    generate_shapesanity_pool()
    print(time.time() - start)
    with open("shapesanity_pool.py", "w") as outfile:
        outfile.writelines(["shapesanity_simple = {\n"]
                           + [f"    \"{name}\": \"{shapesanity_simple[name]}\",\n"
                              for name in shapesanity_simple]
                           + ["}\n\nshapesanity_1_4 = {\n"]
                           + [f"    \"{name}\": \"{shapesanity_1_4[name]}\",\n"
                              for name in shapesanity_1_4]
                           + ["}\n\nshapesanity_two_sided = {\n"]
                           + [f"    \"{name}\": \"{shapesanity_two_sided[name]}\",\n"
                              for name in shapesanity_two_sided]
                           + ["}\n\nshapesanity_three_parts = {\n"]
                           + [f"    \"{name}\": \"{shapesanity_three_parts[name]}\",\n"
                              for name in shapesanity_three_parts]
                           + ["}\n\nshapesanity_four_parts = {\n"]
                           + [f"    \"{name}\": \"{shapesanity_four_parts[name]}\",\n"
                              for name in shapesanity_four_parts]
                           + ["}\n"])
