import itertools
import json
from typing import Dict, List

shapesanity_simple: Dict[str, str] = {}
shapesanity_1_4: Dict[str, str] = {}
shapesanity_two_sided: Dict[str, str] = {}
shapesanity_three_parts: Dict[str, str] = {}
shapesanity_four_parts: Dict[str, str] = {}
subshape_names = ["Circle", "Square", "Star", "Windmill"]
color_names = ["Red", "Blue", "Green", "Yellow", "Purple", "Cyan", "White", "Uncolored"]
short_subshapes = ["C", "R", "S", "W"]
short_colors = ["b", "c", "g", "p", "r", "u", "w", "y"]


def color_to_needed_building(color_list: List[str]) -> str:
    for next_color in color_list:
        if next_color in ["Yellow", "Purple", "Cyan", "White", "y", "p", "c", "w"]:
            return "Mixed"
    for next_color in color_list:
        if next_color not in ["Uncolored", "u"]:
            return "Painted"
    return "Uncolored"


def generate_shapesanity_pool() -> None:
    # same shapes && same color
    for color in color_names:
        color_region = color_to_needed_building([color])
        shapesanity_simple[f"{color} Circle"] = f"Shapesanity Full {color_region}"
        shapesanity_simple[f"{color} Square"] = f"Shapesanity Full {color_region}"
        shapesanity_simple[f"{color} Star"] = f"Shapesanity Full {color_region}"
        shapesanity_simple[f"{color} Windmill"] = f"Shapesanity East Windmill {color_region}"
    for shape in subshape_names:
        for color in color_names:
            color_region = color_to_needed_building([color])
            shapesanity_simple[f"Half {color} {shape}"] = f"Shapesanity Half {color_region}"
            shapesanity_simple[f"{color} {shape} Piece"] = f"Shapesanity Piece {color_region}"
            shapesanity_simple[f"Cut Out {color} {shape}"] = f"Shapesanity Stitched {color_region}"
            shapesanity_simple[f"Cornered {color} {shape}"] = f"Shapesanity Stitched {color_region}"

    # one color && 4 shapes (including empty)
    for first_color, second_color, third_color, fourth_color in itertools.combinations(short_colors+["-"], 4):
        colors = [first_color, second_color, third_color, fourth_color]
        color_region = color_to_needed_building(colors)
        shape_regions = ["Stitched", "Stitched"] if fourth_color == "-" else ["Colorful Full", "Colorful East Windmill"]
        color_code = ''.join(colors)
        shapesanity_1_4[f"{color_code} Circle"] = f"Shapesanity {shape_regions[0]} {color_region}"
        shapesanity_1_4[f"{color_code} Square"] = f"Shapesanity {shape_regions[0]} {color_region}"
        shapesanity_1_4[f"{color_code} Star"] = f"Shapesanity {shape_regions[0]} {color_region}"
        shapesanity_1_4[f"{color_code} Windmill"] = f"Shapesanity {shape_regions[1]} {color_region}"

    # one shape && 4 colors (including empty)
    for first_shape, second_shape, third_shape, fourth_shape in itertools.combinations(short_subshapes+["-"], 4):
        for color in color_names:
            shapesanity_1_4[f"{color} {''.join([first_shape, second_shape, third_shape, fourth_shape])}"] \
                = f"Shapesanity Stitched {color_to_needed_building([color])}"

    combos = [shape + color for shape in short_subshapes for color in short_colors]
    for first_combo, second_combo in itertools.permutations(combos, 2):
        # 2-sided shapes
        color_region = color_to_needed_building([first_combo[1], second_combo[1]])
        ordered_combo = " ".join(sorted([first_combo, second_combo]))
        shape_regions = ((["East Windmill", "East Windmill", "Colorful Half"]
                          if first_combo[0] == "W" else ["Colorful Full", "Colorful Full", "Colorful Half"])
                         if first_combo[0] == second_combo[0] else ["Stitched", "Half-Half", "Stitched"])
        shapesanity_two_sided[f"3-1 {first_combo} {second_combo}"] = f"Shapesanity {shape_regions[0]} {color_region}"
        shapesanity_two_sided[f"Half-Half {ordered_combo}"] = f"Shapesanity {shape_regions[1]} {color_region}"
        shapesanity_two_sided[f"Checkered {ordered_combo}"] = f"Shapesanity {shape_regions[0]} {color_region}"
        shapesanity_two_sided[f"Adjacent Singles {ordered_combo}"] = f"Shapesanity {shape_regions[2]} {color_region}"
        shapesanity_two_sided[f"Cornered Singles {ordered_combo}"] = f"Shapesanity Stitched {color_region}"
        shapesanity_two_sided[f"Adjacent 2-1 {first_combo} {second_combo}"] = f"Shapesanity Stitched {color_region}"
        shapesanity_two_sided[f"Cornered 2-1 {first_combo} {second_combo}"] = f"Shapesanity Stitched {color_region}"
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
                shapesanity_three_parts[f"Singles {ordered_all}"] = f"Shapesanity Stitched {color_region}"
            shape_regions = (["Stitched", "Stitched"] if not second_combo[0] == third_combo[0]
                             else ((["East Windmill", "East Windmill"] if first_combo[0] == "W"
                                    else ["Colorful Full", "Colorful Full"])
                                   if first_combo[0] == second_combo[0] else ["Colorful Half-Half", "Stitched"]))
            shapesanity_three_parts[f"Adjacent 2-1-1 {first_combo} {ordered_two}"] \
                = f"Shapesanity {shape_regions[0]} {color_region}"
            shapesanity_three_parts[f"Cornered 2-1-1 {first_combo} {ordered_two}"] \
                = f"Shapesanity {shape_regions[1]} {color_region}"
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
                    shapesanity_four_parts[f"Singles {ordered_all}"] = f"Shapesanity Colorful Half-Half {color_region}"
                else:
                    shapesanity_four_parts[f"Singles {ordered_all}"] = f"Shapesanity Stitched {color_region}"


if __name__ == "__main__":
    generate_shapesanity_pool()
    pool = json.dumps({
        "shapesanity_simple": shapesanity_simple,
        "shapesanity_1_4": shapesanity_1_4,
        "shapesanity_two_sided": shapesanity_two_sided,
        "shapesanity_three_parts": shapesanity_three_parts,
        "shapesanity_four_parts": shapesanity_four_parts
    }, indent=1)
    with open("shapesanity_pool.json", "w") as outfile:
        outfile.write(pool)
