from pkgutil import get_data
from typing import Dict, Any, List

from BaseClasses import Location,  MultiWorld

ALWAYS_HINT = ["Madame Clairvoya", "Foyer Toad", "Wardrobe Balcony Toad", "1F Washroom Toad", "Courtyard Toad",
               "Left Telephone", "Center Telephone", "Right Telephone"]

PORTRAIT_HINTS = ["Neville", "Lydia", "Chauncey", "Male Whirlinda", "Female Whirlinda", "Shivers", "Melody", "Luggs",
                  "Spooky", "Atlas", "Bankshot", "Petunia", "Nana", "Sue Pea", "Henry", "Orville", "Grimmly", "Jarvis",
                  "Vincent", "Weston", "Clockwork Blue", "Clockwork Pink", "Clockwork Green", "Bogmire", "Boolossus"]


def get_progression_only_items(multiworld: MultiWorld, player: int, loc, hinted_loc, prog_items_no_skip) -> Location:
    while loc is None:
        item = multiworld.worlds[player].random.choice(prog_items_no_skip)
        if item.location not in hinted_loc and item.code is not None and (item.player == player or item.location.player == player):
            loc: Location = item.location
    return loc


def get_other_items(multiworld: MultiWorld, player: int, loc, hinted_loc, other_items) -> Location:
    while loc is None:
        item = multiworld.worlds[player].random.choice(other_items)
        if item.location not in hinted_loc and item.code is not None and (item.player == player or item.location.player == player):
            loc: Location = item.location
    return loc


def get_hints_by_option(multiworld: MultiWorld, player: int) -> Dict[str, Dict[str, Any]]:
    world = multiworld.worlds[player]
    hint_data = {}
    already_hinted_locations: List[Location] = []
    hint_list = ALWAYS_HINT
    jokes = get_data(__name__, "data/jokes.txt").decode('utf-8')
    prog_items = [item for item in multiworld.get_items() if item.advancement]
    prog_no_skip = [items for items in prog_items if not items.skip_in_prog_balancing]
    other_items = [item for item in multiworld.get_items() if not item.advancement]
    if world.options.portrait_hints == 1:
        hint_list = [*ALWAYS_HINT, *PORTRAIT_HINTS]
    for name in hint_list:
        if name == "Madame Clairvoya":
            if world.open_doors[72] == 0:
                loc: Location = multiworld.find_item("Spade Key", player)
            else:
                iname: str = world.random.choice(["Mario's Glove", "Mario's Letter", "Mario's Hat", "Mario's Star",
                                                 "Mario's Shoe"])
                loc: Location = multiworld.find_item(iname, player)
            if world.options.hint_distribution.value == 4:
                hintfo = f"<SAY><COLOR>(7){multiworld.player_name[loc.item.player]}'s<COLOR>(5)\\n{loc.item.name}"+ \
                    f"\n<ANYKEY>\n<SAY><COLOR>(0)is somewhere in<COLOR>(3)\\n{multiworld.player_name[loc.player]}'s\\n{loc.game}"
            elif world.options.hint_distribution.value == 1:
                joke = world.random.choice(str.splitlines(jokes)).replace("\\n", "\n")
                hintfo = f"<SAY><COLOR>(0){joke}"
            elif world.options.hint_distribution.value == 5:
                hintfo = "<SAY><COLOR>(2)I see you've turned off hints"
            else:
                hintfo = f"<SAY><COLOR>(7){multiworld.player_name[loc.item.player]}'s<COLOR>(5)\\n{loc.item.name}" + \
                    f"\n<ANYKEY>\n<SAY><COLOR>(0)can be found at<COLOR>(1)\\n{multiworld.player_name[loc.player]}'s" + \
                    f"\\n{loc.name}"
            hint = {name: hintfo}
            already_hinted_locations.append(loc)
            hint_data.update(hint)
        else:
            loc: Any = None
            if world.options.hint_distribution.value == 0 or world.options.hint_distribution.value == 4:
                hint_type = world.random.choices(["Prog", "Other"], [60, 40], k=1)[0]
                if hint_type == "Prog":
                    loc = get_progression_only_items(multiworld, player, loc, already_hinted_locations, prog_no_skip)
                else:
                    loc = get_other_items(multiworld, player, loc, already_hinted_locations, other_items)
            elif world.options.hint_distribution.value == 3 or world.options.hint_distribution.value == 1:
                hint_type = world.random.choices(["Prog", "Other"], [90, 10], k=1)[0]
                if hint_type == "Prog":
                    loc = get_progression_only_items(multiworld, player, loc, already_hinted_locations, prog_no_skip)
                else:
                    loc = get_other_items(multiworld, player, loc, already_hinted_locations, other_items)
            elif world.options.hint_distribution.value == 2 or world.options.hint_distribution.value == 5:
                while loc is None:
                    item = multiworld.worlds[player].random.choice(multiworld.get_items())
                    if item.location not in already_hinted_locations:
                        loc: Location = item.location
            if loc.item.advancement:
                icolor = 5
            elif loc.item.trap:
                icolor = 2
            else:
                icolor = 6
            if world.options.hint_distribution == 4:
                hintfo = f"<SAY><COLOR>(7){multiworld.player_name[loc.item.player]}'s<COLOR>({icolor})\\n" + \
                    f"{loc.item.name}\n<ANYKEY>\n<SAY><COLOR>(0)is somewhere in<COLOR>(3)\\n " + \
                    f"{multiworld.player_name[loc.player]}'s\\n{loc.game}"
            elif world.options.hint_distribution == 5:
                hintfo = "<SAY><COLOR>(2)I see you've turned off hints"
            elif world.options.hint_distribution.value == 1:
                joke = world.random.choice(str.splitlines(jokes)).replace("\\n", "\n")
                hintfo = f"<SAY><COLOR>(0){joke}"
            else:
                hintfo = f"<SAY><COLOR>(7){multiworld.player_name[loc.item.player]}'s<COLOR>(5)\\n " + \
                    f"{loc.item.name}\n<ANYKEY>\n<SAY><COLOR>(0)can be found at<COLOR>(1)\\n " + \
                    f"{multiworld.player_name[loc.player]}'s\\n {loc.name}"
            hint = {name: hintfo}
            already_hinted_locations.append(loc)
            hint_data.update(hint)

    return hint_data
