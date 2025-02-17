from typing import List, NamedTuple, Union
from BaseClasses import ItemClassification, Location
from worlds.AutoWorld import World
from .Options import HintClarity
from .Items import moves_table, bk_moves_table, progressive_ability_table
from .Locations import all_location_table
from .Names import locationName

TOTAL_HINTS = 61

class HintData(NamedTuple):
    text: str # The displayed text in the game.
    location_id: Union[int, None] = None
    location_player_id: Union[int, None] = None

def generate_hints(world: World):
    hint_datas: List[HintData] = []

    generate_move_hints(world, hint_datas)
    generate_slow_locations_hints(world, hint_datas)
    generate_joke_hints(world, hint_datas)

    assign_hints_to_locations(world, hint_datas)

def assign_hints_to_locations(world: World, hint_datas: List[HintData]):
    world.random.shuffle(hint_datas)

    hint_location_ids = get_signpost_location_ids()

    # It is done this way to keep the order of the signposts intact in the spoiler log.
    chosen_locations_ids = hint_location_ids[::]
    world.random.shuffle(chosen_locations_ids)
    placed_hints = 0
    for id in hint_location_ids:
        if id not in chosen_locations_ids:
            continue
        world.hints.update({id: hint_datas[placed_hints]})
        placed_hints += 1

def generate_joke_hints(world: World, hint_datas: List[HintData]):
    # Fills the rest of the signposts with jokes.
    if len(hint_datas) == TOTAL_HINTS:
        return
    generate_suggestion_hint(world, hint_datas)
    generate_forced_joke_hint(world, hint_datas)
    generate_generic_joke_hint(world, hint_datas)

def generate_forced_joke_hint(world: World, hint_datas: List[HintData]):
    if len(hint_datas) == TOTAL_HINTS:
        return
    hint_datas.append(HintData(f"Sorry {world.player_name}, but we are not adding that feature in this game."))

def generate_generic_joke_hint(world: World, hint_datas: List[HintData]):
    selected_jokes = (world.random.choices([
        "A hint is what you want, but instead here's a taunt.",
        "This is an information signpost.",
        "This joke hint features no newline.",
        "Press \x86 to read this signpost.",
        "Banjo-Kazooie: Grunty's Revenge is a collectathon that was released on the GBA.",
        "Did you know that Banjo-Kazooie had 2 mobile games? Me neither.",
        "After collecting all 9 black jinjos, enter their house for a happy sound.",
        "Made you look!",
        "Developer jjjj12212 was a good developer... until he got shot with an arrow in the knee.",

        # The following are quotes from other video games (or something inspired from them).
        "Thank you Banjo, but your hint is on another signpost!",
        "It's dangerous to go alone, read this!",
        "I like shorts! They're comfy and easy to wear!",
        "Press F to pay respects.",
        "Press \x86 to doubt.",
        "The sign is a lie",
    ], k = TOTAL_HINTS - len(hint_datas)))

    for joke in selected_jokes:
        hint_datas.append(HintData(joke))

def generate_suggestion_hint(world: World, hint_datas: List[HintData]):
    non_tooie_player_names = [world.player_name for world in world.multiworld.worlds.values() if world.game != "Banjo-Tooie"]
    if not non_tooie_player_names:
        return
    hint = "You should suggest {} to try the Banjo-Tooie Randomizer.".format(world.random.choice(non_tooie_player_names))
    hint_datas.append(HintData(hint))

def generate_slow_locations_hints(world: World, hint_datas: List[HintData]):
    hinted_location_names_in_own_world = [location_id_to_name(world, hint_data.location_id)\
                                        for hint_data in hint_datas if hint_data.location_player_id == world.player]

    worst_locations_names = [location_name for location_name in get_worst_location_names(world)\
                             if location_name not in hinted_location_names_in_own_world]

    hinted_location_names_in_own_world.extend(worst_locations_names)

    newHints = [generate_hint_data_from_location(world, get_location_by_name(world, location_name))\
                for location_name in worst_locations_names if get_location_by_name(world, location_name)]

    if len(newHints) + len(hint_datas) >= world.options.signpost_hints:
        world.random.shuffle(newHints)
        while len(hint_datas) < world.options.signpost_hints:
            hint_datas.append(newHints.pop())
        return
    hint_datas.extend(newHints)

    bad_locations_names = [location_name for location_name in get_bad_location_names(world) if location_name not in hinted_location_names_in_own_world]
    hinted_location_names_in_own_world.extend(bad_locations_names)
    newHints = [generate_hint_data_from_location(world, get_location_by_name(world, location_name))\
                for location_name in bad_locations_names if get_location_by_name(world, location_name)]
    if len(newHints) + len(hint_datas) >= world.options.signpost_hints:
        world.random.shuffle(newHints)
        while len(hint_datas) < world.options.signpost_hints:
            hint_datas.append(newHints.pop())
        return
    hint_datas.extend(newHints)

    # At this point, we went through all the bad locations, and we still don't have enough hints.
    # So we just hint random locations in our own world that have not been picked.
    remaining_locations = [location for location in get_player_hintable_locations(world) if location.name not in hinted_location_names_in_own_world]
    world.random.shuffle(remaining_locations)

    while len(hint_datas) < world.options.signpost_hints:
        hint_datas.append(generate_hint_data_from_location(world, remaining_locations.pop()))

def location_id_to_name(world: World, location_id: int):
    return world.location_id_to_name[location_id]

def get_location_by_id(world: World, location_id: int):
    return list(filter(lambda location: location.address == location_id, get_player_hintable_locations(world)))[0]

def get_worst_location_names(world: World):
    slow_location_names = []

    slow_location_names.extend([
        locationName.JIGGYMT5,

        locationName.JIGGYGM5,

        locationName.JIGGYWW2,
        locationName.JIGGYWW3,
        locationName.JIGGYWW4,
        locationName.JIGGYWW7,

        locationName.JIGGYJR7,
        locationName.JIGGYJR9,

        locationName.JIGGYTD3,
        locationName.JIGGYTD7,

        locationName.JIGGYGI1,
        locationName.JIGGYGI2,
        locationName.JIGGYGI3,
        locationName.JIGGYGI4,

        locationName.JIGGYHP1,
        locationName.JIGGYHP5,
        locationName.JIGGYHP9,

        locationName.JIGGYCC1,
        locationName.JIGGYCC7,

        locationName.SCRAT,
    ])

    if world.options.randomize_jinjos:
        slow_location_names.extend([
            locationName.JIGGYIH6,
            locationName.JIGGYIH7,
            locationName.JIGGYIH8,
            locationName.JIGGYIH9,

            locationName.JINJOGI3,
            locationName.JINJOGI5,
        ])

    if world.options.randomize_glowbos:
        slow_location_names.extend([
            locationName.GLOWBOMEG,
        ])

    if world.options.randomize_cheato:
        slow_location_names.extend([
            locationName.CHEATOWW3,
            locationName.CHEATOJR1,
            locationName.CHEATOGI3,
            locationName.CHEATOCC1,
        ])

    # The 5 most expensive silos
    if world.options.randomize_moves:
        sorted_silos = [k for k, v in sorted(world.jamjars_siloname_costs.items(), key=lambda item: item[1])]
        for i in range(5):
            slow_location_names.append(sorted_silos.pop())

    if world.options.cheato_rewards:
        slow_location_names.extend([
            locationName.CHEATOR4,
            locationName.CHEATOR5,
        ])

    if world.options.honeyb_rewards:
        slow_location_names.extend([
            locationName.HONEYBR5,
        ])

    return slow_location_names


def get_bad_location_names(world: World):
    slow_location_names = []

    slow_location_names.extend([
        locationName.JIGGYMT1,
        locationName.JIGGYMT3,

        locationName.JIGGYGM5,

        locationName.JIGGYWW1,
        locationName.JIGGYWW5,

        locationName.JIGGYJR1,
        locationName.JIGGYJR3,

        locationName.JIGGYTD2,
        locationName.JIGGYTD9,

        locationName.JIGGYGI6,
        locationName.JIGGYGI9,

        locationName.JIGGYHP3,
        locationName.JIGGYHP6,
        locationName.JIGGYHP10,

        locationName.JIGGYCC4,

        locationName.SCRUT,
    ])
    # TODO: continue here
    if world.options.randomize_jinjos:
        slow_location_names.extend([
        ])

    if world.options.randomize_glowbos:
        slow_location_names.extend([
        ])

    if world.options.randomize_cheato:
        slow_location_names.extend([
        ])

    # The next 5 most expensive silos
    if world.options.randomize_moves:
        sorted_silos = [k for k, v in sorted(world.jamjars_siloname_costs.items(), key=lambda item: item[1])]
        for i in range(6, 10):
            slow_location_names.append(sorted_silos.pop())

    if world.options.cheato_rewards:
        slow_location_names.extend([
            locationName.CHEATOR3,
        ])

    if world.options.honeyb_rewards:
        slow_location_names.extend([
            locationName.HONEYBR4,
        ])
    return slow_location_names

def generate_move_hints(world: World, hint_datas: List[HintData]):
    move_locations = get_move_locations(world)
    for location in move_locations:
        hint_datas.append(generate_hint_data_from_location(world, location))

# TODO: have some fun with Grunty's rhymes here
def generate_hint_data_from_location(world: World, location: Location) -> HintData:
    text = ""
    if world.options.hint_clarity == HintClarity.option_clear:
        text = "{}'s {} has {}'s {}.".format(player_id_to_name(world, location.player),\
            location.name, player_id_to_name(world, location.item.player), location.item.name)
    else:
        text = generate_cryptic_hint_text(world, location)

    return HintData(text, location.address, location.player)

def generate_cryptic_hint_text(world: World, location: Location) -> str:
    if location.item.classification in (ItemClassification.progression, ItemClassification.progression_skip_balancing):
        return "{}'s {} has a wonderful item.".format(player_id_to_name(world, location.player), location.name)
    if location.item.classification == ItemClassification.useful:
        return "{}'s {} has a good item.".format(player_id_to_name(world, location.player), location.name)
    if location.item.classification == ItemClassification.filler:
        return "{}'s {} has an okay item.".format(player_id_to_name(world, location.player), location.name)
    if location.item.classification == ItemClassification.trap:
        return "{}'s {} has a bad item.".format(player_id_to_name(world, location.player), location.name)

    # Not sure what actually fits in a multi-flag classification
    return "{}'s {} has a devilishly good item.".format(player_id_to_name(world, location.player), location.name)

def get_move_locations(world: World) -> List[Location]:
    all_moves_names = []
    if world.options.randomize_moves:
        all_moves_names.extend(moves_table.keys()) # We don't want BT moves to be hinted when they're in the vanilla location.
    all_moves_names.extend(bk_moves_table.keys())
    all_moves_names.extend(progressive_ability_table.keys())

    all_move_locations = [location for location in get_all_hintable_locations(world)\
            if location.item.name in all_moves_names and location.item.player == world.player]
    world.random.shuffle(all_move_locations)
    selected_move_locations = []

    for location in all_move_locations:
        if len(selected_move_locations) >= min(world.options.signpost_move_hints, world.options.signpost_hints):
            return selected_move_locations
        selected_move_locations.append(location)
    return selected_move_locations

def get_location_by_name(world: World, name: str) -> Location:
    potential_match = list(filter(lambda location: location.name == name, get_player_hintable_locations(world)))
    if potential_match:
        return potential_match[0]
    return None

def get_all_hintable_locations(world: World) -> List[Location]:
    return [location for location in world.multiworld.get_locations() if location.item and location.address]

def get_player_hintable_locations(world: World) -> List[Location]:
    return [location for location in world.multiworld.get_locations(world.player) if location.item and location.address]

def player_id_to_name(world: World, id: int) -> str:
    return world.multiworld.player_name[id]

def get_signpost_location_ids() -> List[int]:
    location_datas = list(filter(lambda location_data: location_data.group == "Signpost", all_location_table.values()))
    return [location_data.btid for location_data in location_datas]
