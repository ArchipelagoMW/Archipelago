from typing import Dict, Any, List

from BaseClasses import CollectionState, Location,  MultiWorld

ALWAYS_HINT = ["Madame Clairvoya", "Foyer Toad", "Wardrobe Balcony Toad", "1F Washroom Toad", "Courtyard Toad",
               "Left Telephone", "Center Telephone", "Right Telephone"]

PORTRAIT_HINTS = ["Neville", "Lydia", "Chauncey", "Male Whirlinda", "Female Whirlinda", "Shivers", "Melody", "Luggs",
                  "Spooky", "Atlas", "Bankshot", "Petunia", "Nana", "Sue Pea", "Henry", "Orville", "Grimmly", "Jarvis",
                  "Vincent", "Weston", "Clockwork Blue", "Clockwork Pink", "Clockwork Green", "Bogmire", "Boolossus"]


def get_progression_only_items(multiworld: MultiWorld, player: int, loc, hinted_loc) -> Location:
    prog_items = [item for item in multiworld.get_items() if item.advancement]
    prog_items_no_skip = [items for items in prog_items if items.classification != 0b1001]
    while loc is None:
        item = multiworld.worlds[player].random.choice(prog_items_no_skip)
        if item.location not in hinted_loc and item.code is not None:
            loc: Location = item.location
    return loc


def get_other_items(multiworld: MultiWorld, player: int, loc, hinted_loc) -> Location:
    other_items = [item for item in multiworld.get_items() if not item.advancement]
    while loc is None:
        item = multiworld.worlds[player].random.choice(other_items)
        if item.location not in hinted_loc and item.code is not None:
            loc: Location = item.location
    return loc


def get_hints_by_option(multiworld: MultiWorld, player: int) -> Dict[str, Dict[str, Any]]:
    state = CollectionState(multiworld)
    world = multiworld.worlds[player]
    hint_data = {}
    already_hinted_locations: List[Location] = []
    hint_list = ALWAYS_HINT
    if world.options.portrait_hints == 1:
        hint_list = [*ALWAYS_HINT, *PORTRAIT_HINTS]
    for name in hint_list:
        if name == "Madame Clairvoya":
            if world.open_doors[72] == 0:
                loc: Location = multiworld.find_item("Spade Key", player)
                reg = loc.parent_region
                game = reg.multiworld.worlds[reg.player]
                hintfo = {"Item": loc.item.name,
                          "Player": game.player_name,
                          "Location": loc.name,
                          "Region": reg.name,
                          "Game": game.game
                          }
            else:
                name: str = world.random.choice(["Mario's Glove", "Mario's Letter", "Mario's Cap", "Mario's Glove",
                                                 "Mario's Shoe"])
                loc: Location = multiworld.find_item(name, player)
                reg = loc.parent_region
                game = reg.multiworld.worlds[reg.player]
                hintfo = {"Item": loc.item.name,
                          "Player": game.player_name,
                          "Location": loc.name,
                          "Region": reg.name,
                          "Game": game.game
                          }
            hint = {name: hintfo}
            already_hinted_locations.append(loc)
            hint_data.update(hint)
        else:
            loc: Any = None
            if world.options.hint_distribution == 0 or world.options.hint_distribution == 4:
                hint_type = world.random.choices(["Prog", "Other"], [60, 40], k=1)[0]
                if hint_type == "Prog":
                    loc = get_progression_only_items(multiworld, player, loc, already_hinted_locations)
                else:
                    loc = get_other_items(multiworld, player, loc, already_hinted_locations)
            elif world.options.hint_distribution == 3:
                hint_type = world.random.choices(["Prog", "Other"], [90, 10], k=1)[0]
                if hint_type == "Prog":
                    loc = get_progression_only_items(multiworld, player, loc, already_hinted_locations)
                else:
                    loc = get_other_items(multiworld, player, loc, already_hinted_locations)
            elif world.options.hint_distribution == 2:
                while loc is None:
                    item = multiworld.worlds[player].random.choice(multiworld.get_items())
                    if item.location not in already_hinted_locations:
                        loc: Location = item.location
            reg = loc.parent_region
            game = reg.multiworld.worlds[reg.player]
            hintfo = {"Item": loc.item.name,
                      "Player": game.player_name,
                      "Location": loc.name,
                      "Region": reg.name,
                      "Game": game.game
                      }
            hint = {name: hintfo}
            already_hinted_locations.append(loc)
            hint_data.update(hint)

    return hint_data
