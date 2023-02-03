from BaseClasses import MultiWorld
from .Options import is_option_enabled, get_option_value

joke_hints = [
    ("Quaternions", "break", "my brain"),
    ("Eclipse", "has nothing", "but you should do it anyway"),
    ("", "Beep", ""),
    ("Putting in custom subtitles", "shouldn't have been", "as hard as it was..."),
    ("BK mode", "is right", "around the corner"),
    ("", "You can do it!", ""),
    ("", "I believe in you!", ""),
    ("The person playing", "is", "cute <3"),
    ("dash dot, dash dash dash", "dash, dot dot dot dot, dot dot", "dash dot, dash dash dot"),
    ("When you think about it,", "there are actually a lot of", "bubbles in a stream"),
    ("Never gonna give you up", "Never gonna let you down", "Never gonna run around and desert you"),
    ("Thanks to", "the Archipelago developers", "for making this possible."),
    ("Have you tried ChecksFinder?", "If you like puzzles,", "you might enjoy it!"),
    ("Have you tried Dark Souls III?", "A tough game like this", "feels better when friends are helping you!"),
    ("Have you tried Donkey Kong Country 3?", "A legendary game", "from a golden age of platformers!"),
    ("Have you tried Factorio?", "Alone in an unknown multiworld.", "Sound familiar?"),
    ("Have you tried Final Fantasy?", "Experience a classic game", "improved to fit modern standards!"),
    ("Have you tried Hollow Knight?", "Another independent hit", "revolutionising a genre!"),
    ("Have you tried A Link to the Past?", "The Archipelago game", "that started it all!"),
    ("Have you tried Meritous?", "You should know that obscure games", "are often groundbreaking!"),
    ("Have you tried Ocarine of Time?", "One of the biggest randomizers,", "big inspiration for this one's features!"),
    ("Have you tried Raft?", "Haven't you always wanted to explore", "the ocean surrounding this island?"),
    ("Have you tried Risk of Rain 2?", "I haven't either.", "But I hear it's incredible!"),
    ("Have you tried Rogue Legacy?", "After solving so many puzzles", "it's the perfect way to rest your brain."),
    ("Have you tried Secret of Evermore?", "I haven't either", "But I hear it's great!"),
    ("Have you tried Slay the Spire?", "Experience the thrill of combat", "without needing fast fingers!"),
    ("Have you tried SMZ3?", "Why play one incredible game", "when you can play 2 at once?"),
    ("Have you tried Starcraft 2?", "Use strategy and management", "to crush your enemies!"),
    ("Have you tried Super Mario 64?", "3-dimensional games like this", "owe everything to that game."),
    ("Have you tried Super Metroid?", "A classic game", "that started a whole genre."),
    ("Have you tried Timespinner?", "Everyone who plays it", "ends up loving it!"),
    ("Have you tried VVVVVV?", "Experience the essence of gaming", "distilled into its purest form!"),
    ("Have you tried The Witness?", "Oh. I guess you already have.", " Thanks for playing!"),
    ("Have you tried Super Mario World?", "I don't think I need to tell you", "that it is beloved by many."),
    ("Have you tried Overcooked 2?", "When you're done relaxing with puzzles,",
     "use your energy to yell at your friends."),
    ("Have you tried Zillion?", "Me neither. But it looks fun.", "So, let's try something new together?"),
    ("Have you tried Hylics 2?", "Stop motion might just be", "the epitome of unique art styles."),
    ("Have you tried Pokemon Red&Blue?", "A cute pet collecting game", "that fascinated an entire generation."),
    ("Waiting to get your items?", "Try BK Sudoku!", "Make progress even while stuck."),
    ("One day I was fascinated", "by the subject of", "generation of waves by wind"),
    ("I don't like sandwiches", "Why would you think I like sandwiches?", "Have you ever seen me with a sandwich?"),
    ("Where are you right now?", "I'm at soup!", "What do you mean you're at soup?"),
    ("Remember to ask", "in the Archipelago Discord", "what the Functioning Brain does."),
    ("", "Don't use your puzzle skips", "you might need them later"),
    ("", "For an extra challenge", "Try playing blindfolded"),
    ("Go to the top of the mountain", "and see if you can see", "your house"),
    ("Yellow = Red + Green", "Cyan = Green + Blue", "Magenta = Red + Blue"),
    ("", "Maybe that panel really is unsolvable", ""),
    ("", "Did you make sure it was plugged in?", ""),
    ("", "Do not look into laser with remaining eye", ""),
    ("", "Try pressing Space to jump", ""),
    ("The Witness is a Doom clone.", "Just replace the demons", "with puzzles"),
    ("", "Test Hint please ignore", ""),
    ("Shapers can never be placed", "outside the panel boundaries", "even if subtracted."),
    ("", "The Keep laser panels use", "the same trick on both sides!"),
    ("Can't get past a door? Try going around.", "Can't go around? Try building a", "nether portal."),
    ("", "We've been trying to reach you", "about your car's extended warranty"),
    ("I hate this game. I hate this game.", "I hate this game.", "-chess player Bobby Fischer"),
    ("Dear Mario,", "Please come to the castle.", "I've baked a cake for you!"),
    ("Have you tried waking up?", "", "Yeah, me neither."),
    ("Why do they call it The Witness,", "when wit game the player view", "play of with the game."),
    ("", "THE WIND FISH IN NAME ONLY", "FOR IT IS NEITHER"),
    ("Like this game? Try The Wit.nes,", "Understand, INSIGHT, Taiji", "What the Witness?, and Tametsi."),
    ("", "In a race", "It's survival of the Witnesst"),
    ("", "This hint has been removed", "We apologize for your inconvenience."),
    ("", "O-----------", ""),
    ("Circle is draw", "Square is separate", "Line is win"),
    ("Circle is draw", "Star is pair", "Line is win"),
    ("Circle is draw", "Circle is copy", "Line is win"),
    ("Circle is draw", "Dot is eat", "Line is win"),
    ("Circle is start", "Walk is draw", "Line is win"),
    ("Circle is start", "Line is win", "Witness is you"),
    ("Can't find any items?", "Consider a relaxing boat trip", "around the island"),
    ("", "Don't forget to like, comment, and subscribe", ""),
    ("Ah crap, gimme a second.", "[papers rustling]", "Sorry, nothing."),
    ("", "Trying to get a hint?", "Too bad."),
    ("", "Here's a hint:", "Get good at the game."),
    ("", "I'm still not entirely sure", "what we're witnessing here."),
    ("Have you found a red page yet?", "No?", "Then have you found a blue page?"),
    (
        "And here we see the Witness player,",
        "seeking answers where there are none-",
        "Did someone turn on the loudspeaker?"
    ),
    (
        "Hints suggested by:",
        "IHNN, Beaker, MrPokemon11, Ember, TheM8, NewSoupVi,",
        "KF, Yoshi348, Berserker, BowlinJim, oddGarrett, Pink Switch."
    ),
]


def get_always_hint_items(multiworld: MultiWorld, player: int):
    priority = [
        "Boat",
        "Mountain Bottom Floor Final Room Entry (Door)",
        "Caves Mountain Shortcut (Door)",
        "Caves Swamp Shortcut (Door)",
        "Caves Exits to Main Island",
        "Progressive Dots",
    ]

    difficulty = get_option_value(multiworld, player, "puzzle_randomization")
    discards = is_option_enabled(multiworld, player, "shuffle_discarded_panels")

    if discards:
        if difficulty == 1:
            priority.append("Arrows")
        else:
            priority.append("Triangles")

    return priority


def get_always_hint_locations(multiworld: MultiWorld, player: int):
    return {
        "Swamp Purple Underwater",
        "Shipwreck Vault Box",
        "Challenge Vault Box",
        "Mountain Bottom Floor Discard",
        "Theater Eclipse EP",
        "Shipwreck Couch EP",
        "Mountainside Cloud Cycle EP",
    }


def get_priority_hint_items(multiworld: MultiWorld, player: int):
    priority = {
        "Negative Shapers",
        "Sound Dots",
        "Colored Dots",
        "Stars + Same Colored Symbol",
        "Swamp Entry (Panel)",
        "Swamp Laser Shortcut (Door)",
    }

    if is_option_enabled(multiworld, player, "shuffle_lasers"):
        lasers = {
            "Symmetry Laser",
            "Desert Laser",
            "Town Laser",
            "Keep Laser",
            "Swamp Laser",
            "Treehouse Laser",
            "Monastery Laser",
            "Jungle Laser",
            "Quarry Laser",
            "Bunker Laser",
            "Shadows Laser",
        }

        if get_option_value(multiworld, player, "doors") >= 2:
            priority.add("Desert Laser")
            lasers.remove("Desert Laser")
            priority.update(multiworld.per_slot_randoms[player].sample(lasers, 2))

        else:
            priority.update(multiworld.per_slot_randoms[player].sample(lasers, 3))

    return priority


def get_priority_hint_locations(multiworld: MultiWorld, player: int):
    return {
        "Town RGB Room Left",
        "Town RGB Room Right",
        "Treehouse Green Bridge 7",
        "Treehouse Green Bridge Discard",
        "Shipwreck Discard",
        "Desert Vault Box",
        "Mountainside Vault Box",
        "Mountainside Discard",
        "Tunnels Theater Flowers EP",
        "Boat Shipwreck Green EP",
    }


def make_hint_from_item(multiworld: MultiWorld, player: int, item: str):
    location_obj = multiworld.find_item(item, player).item.location
    location_name = location_obj.name
    if location_obj.player != player:
        location_name += " (" + multiworld.get_player_name(location_obj.player) + ")"

    return location_name, item, location_obj.address if(location_obj.player == player) else -1


def make_hint_from_location(multiworld: MultiWorld, player: int, location: str):
    location_obj = multiworld.get_location(location, player)
    item_obj = multiworld.get_location(location, player).item
    item_name = item_obj.name
    if item_obj.player != player:
        item_name += " (" + multiworld.get_player_name(item_obj.player) + ")"

    return location, item_name, location_obj.address if(location_obj.player == player) else -1


def make_hints(multiworld: MultiWorld, player: int, hint_amount: int):
    hints = list()

    prog_items_in_this_world = {
        item.name for item in multiworld.get_items()
        if item.player == player and item.code and item.advancement
    }
    loc_in_this_world = {
        location.name for location in multiworld.get_locations()
        if location.player == player and location.address
    }

    always_locations = [
        location for location in get_always_hint_locations(multiworld, player)
        if location in loc_in_this_world
    ]
    always_items = [
        item for item in get_always_hint_items(multiworld, player)
        if item in prog_items_in_this_world
    ]
    priority_locations = [
        location for location in get_priority_hint_locations(multiworld, player)
        if location in loc_in_this_world
    ]
    priority_items = [
        item for item in get_priority_hint_items(multiworld, player)
        if item in prog_items_in_this_world
    ]

    always_hint_pairs = dict()

    for item in always_items:
        hint_pair = make_hint_from_item(multiworld, player, item)

        if hint_pair[2] == 158007:  # Tutorial Gate Open
            continue

        always_hint_pairs[hint_pair[0]] = (hint_pair[1], True, hint_pair[2])

    for location in always_locations:
        hint_pair = make_hint_from_location(multiworld, player, location)
        always_hint_pairs[hint_pair[0]] = (hint_pair[1], False, hint_pair[2])

    priority_hint_pairs = dict()

    for item in priority_items:
        hint_pair = make_hint_from_item(multiworld, player, item)

        if hint_pair[2] == 158007:  # Tutorial Gate Open
            continue

        priority_hint_pairs[hint_pair[0]] = (hint_pair[1], True, hint_pair[2])

    for location in priority_locations:
        hint_pair = make_hint_from_location(multiworld, player, location)
        priority_hint_pairs[hint_pair[0]] = (hint_pair[1], False, hint_pair[2])

    for loc, item in always_hint_pairs.items():
        if item[1]:
            hints.append((item[0], "can be found at", loc, item[2]))
        else:
            hints.append((loc, "contains", item[0], item[2]))

    multiworld.per_slot_randoms[player].shuffle(hints)  # shuffle always hint order in case of low hint amount

    next_random_hint_is_item = multiworld.per_slot_randoms[player].randint(0, 2)

    prog_items_in_this_world = sorted(list(prog_items_in_this_world))
    locations_in_this_world = sorted(list(loc_in_this_world))

    multiworld.per_slot_randoms[player].shuffle(prog_items_in_this_world)
    multiworld.per_slot_randoms[player].shuffle(locations_in_this_world)

    while len(hints) < hint_amount:
        if priority_hint_pairs:
            loc = multiworld.per_slot_randoms[player].choice(list(priority_hint_pairs.keys()))
            item = priority_hint_pairs[loc]
            del priority_hint_pairs[loc]

            if item[1]:
                hints.append((item[0], "can be found at", loc, item[2]))
            else:
                hints.append((loc, "contains", item[0], item[2]))
            continue

        if next_random_hint_is_item:
            if not prog_items_in_this_world:
                next_random_hint_is_item = not next_random_hint_is_item
                continue

            hint = make_hint_from_item(multiworld, player, prog_items_in_this_world.pop())
            hints.append((hint[1], "can be found at", hint[0], hint[2]))
        else:
            hint = make_hint_from_location(multiworld, player, locations_in_this_world.pop())
            hints.append((hint[0], "contains", hint[1], hint[2]))

        next_random_hint_is_item = not next_random_hint_is_item

    return hints


def generate_joke_hints(multiworld: MultiWorld, player: int, amount: int):
    return [(x, y, z, -1) for (x, y, z) in multiworld.per_slot_randoms[player].sample(joke_hints, amount)]
