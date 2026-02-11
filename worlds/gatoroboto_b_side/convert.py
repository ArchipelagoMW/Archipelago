import re

translation_table = {
    "&": "and",
    "\\|": "or",
    "Any": "True",
    "Rocket": "state.has(\"Rocket\", world.player)",
    "Dash": "state.has(\"Dash\", world.player)",
    "Spinjump": "state.has(\"Spin Jump\", world.player)",
    "Cooler": "state.has(\"Cooler\", world.player)",
    "Hopper": "state.has(\"Hopper\", world.player)",
    "WaterLevel x1": "state.has(\"Water Level\", world.player, 1)",
    "WaterLevel x2": "state.has(\"Water Level\", world.player, 2)",
    "WaterLevel x3": "state.has(\"Water Level\", world.player, 3)",
    "<\"Lava Cooled\">": "state.has(\"Lava Cooled\", world.player)",
    "VentLevel x1": "state.has(\"Vent Level\", world.player, 1)",
    "VentLevel x2": "state.has(\"Vent Level\", world.player, 2)",
    "VentLevel x3": "state.has(\"Vent Level\", world.player, 3)",
    "<\"Completed all Areas\">": "state.has(\"<Completed all areas>\", world.player)",
    "<\"Smallmech entry\">": "state.has(\"<Smallmech entry>\", world.player)",
    "VHS x7": "state.has_from_list(vhs, world.player, 7))",
    "VHS x14": "state.has_all(vhs, world.player))",
    "\"Smallmech\"": "world.options.use_smallmech",
    "\"Watermech\"": "world.options.use_watermech",
    "\"Hard\"": "(world.options.gato_tech >= 2)",
    "\"Vanilla\"": "(world.options.gato_tech == 3)",
    "\"Not Vanilla\"": "(world.options.gato_tech <= 2)",
    "\"Upwarp\"": "True",
    "\"Ultrahard\"": "False",
}

def as_comment(string: str) -> str:
    return f"\033[37m{string}\033[0m"

def as_color(string: str, color: str) -> str:
    if color == "blue":
        return f"\033[94m{string}\033[0m"
    elif color == "green":
        return f"\033[92m{string}\033[0m"
    elif color == "purple":
        return f"\033[95m{string}\033[0m"
    elif color == "red":
        return f"\033[31m{string}\033[0m"
    return f"\033[0m{string}\033[0m"

tabs = "    "
with open("gatologic.txt", "r") as f:
    for x in f:
        x = x.strip()
        # Empty line
        if len(x) == 0:
            print(tabs + "")
            continue
        # Not a real location
        if x.find(": ") == -1:
            print(tabs + as_comment("# " + x))
            continue
        # Commented out
        if x.startswith("#"):
            print(tabs + as_comment(x))
            continue


        loc, rule = tuple(x.split(": ", 1))
        if loc.startswith("* "):
            loc = loc[2:]
        if loc.startswith("("):
            # Pre-notes
            pre_notes, loc =  tuple(loc.split(")", 1))
            print(tabs + as_color("# " + pre_notes + ")", "red"))
        if loc.startswith("'"):
            # Regions
            print(tabs + as_color("# " + loc.strip("'")[:-7], "purple"))
            continue
        else:
            # Normal location check
            # Format rules
            # Remove out-of-logic
            rule = re.sub(r" \| \(\[.*", "", rule)
            # Format to code
            for regex, replacement in translation_table.items():
                rule = re.sub(regex, replacement, rule)
            print(f"{tabs}current_location = world.get_location({as_color('"' + loc + '"', "blue")})\n"
                  f"{tabs}set_rule(current_location, lambda state: {as_color(rule, "green")})")
