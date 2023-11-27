from typing import Tuple, List, TYPE_CHECKING

from BaseClasses import Item

if TYPE_CHECKING:
    from . import WitnessWorld

joke_hints = [
    "Quaternions break my brain",
    "Eclipse has nothing, but you should do it anyway.",
    "Beep",
    "Putting in custom subtitles shouldn't have been as hard as it was...",
    "BK mode is right around the corner.",
    "You can do it!",
    "I believe in you!",
    "The person playing is cute. <3",
    "dash dot, dash dash dash,\ndash, dot dot dot dot, dot dot,\ndash dot, dash dash dot",
    "When you think about it, there are actually a lot of bubbles in a stream.",
    "Never gonna give you up\nNever gonna let you down\nNever gonna run around and desert you",
    "Thanks to the Archipelago developers for making this possible.",
    "Have you tried ChecksFinder?\nIf you like puzzles, you might enjoy it!",
    "Have you tried Dark Souls III?\nA tough game like this feels better when friends are helping you!",
    "Have you tried Donkey Kong Country 3?\nA legendary game from a golden age of platformers!",
    "Have you tried Factorio?\nAlone in an unknown multiworld. Sound familiar?",
    "Have you tried Final Fantasy?\nExperience a classic game improved to fit modern standards!",
    "Have you tried Hollow Knight?\nAnother independent hit revolutionising a genre!",
    "Have you tried A Link to the Past?\nThe Archipelago game that started it all!",
    "Have you tried Meritous?\nYou should know that obscure games are often groundbreaking!",
    "Have you tried Ocarina of Time?\nOne of the biggest randomizers, big inspiration for this one's features!",
    "Have you tried Raft?\nHaven't you always wanted to explore the ocean surrounding this island?",
    "Have you tried Risk of Rain 2?\nI haven't either. But I hear it's incredible!",
    "Have you tried Rogue Legacy?\nAfter solving so many puzzles it's the perfect way to rest your \"thinking\" brain.",
    "Have you tried Secret of Evermore?\nI haven't either. But I hear it's great!",
    "Have you tried Slay the Spire?\nExperience the thrill of combat without needing fast fingers!",
    "Have you tried SMZ3?\nWhy play one incredible game when you can play 2 at once?",
    "Have you tried Starcraft 2?\nUse strategy and management to crush your enemies!",
    "Have you tried Super Mario 64?\n3-dimensional games like this owe everything to that game.",
    "Have you tried Super Metroid?\nA classic game, yet still one of the best in the genre.",
    "Have you tried Timespinner?\nEveryone who plays it ends up loving it!",
    "Have you tried VVVVVV?\nExperience the essence of gaming distilled into its purest form!",
    "Have you tried The Witness?\nOh. I guess you already have. Thanks for playing!",
    "Have you tried Super Mario World?\nI don't think I need to tell you that it is beloved by many.",
    "Have you tried Overcooked 2?\nWhen you're done relaxing with puzzles, use your energy to yell at your friends.",
    "Have you tried Zillion?\nMe neither. But it looks fun. So, let's try something new together?",
    "Have you tried Hylics 2?\nStop motion might just be the epitome of unique art styles.",
    "Have you tried Pokemon Red&Blue?\nA cute pet collecting game that fascinated an entire generation.",
    "Have you tried Lufia II?\nRoguelites are not just a 2010s phenomenon, turns out.",
    "Have you tried Minecraft?\nI have recently learned this is a question that needs to be asked.",
    "Have you tried Subnautica?\nIf you like this game's lonely atmosphere, I would suggest you try it.",

    "Have you tried Sonic Adventure 2?\nIf the silence on this island is getting to you, "
    "there aren't many games more energetic.",

    "Waiting to get your items?\nTry BK Sudoku! Make progress even while stuck.",

    "Have you tried Adventure?\n...Holy crud, that game is 17 years older than me.",
    "Have you tried Muse Dash?\nRhythm game with cute girls!\n(Maybe skip if you don't like the Jungle panels)",
    "Have you tried Clique?\nIt's certainly a lot less complicated than this game!",
    "Have you tried Bumper Stickers?\nDecades after its inception, people are still inventing unique twists on the match-3 genre.",
    "Have you tried DLC Quest?\nI know you all like parody games.\nI got way too many requests to make a randomizer for \"The Looker\".",
    "Have you tried Doom?\nI wonder if a smart fridge can connect to Archipelago.",
    "Have you tried Kingdom Hearts II?\nI'll wait for you to name a more epic crossover.",
    "Have you tried Link's Awakening DX?\nHopefully, Link won't be obsessed with circles when he wakes up.",
    "Have you tried The Messenger?\nOld ideas made new again. It's how all art is made.",
    "Have you tried Mega Man Battle Network 3?\nIt's a Mega Man RPG. How could you not want to try that?",
    "Have you tried Noita?\nIf you like punishing yourself, you will like it.",
    "Have you tried Stardew Valley?\nThe Farming game that gave a damn. It's so easy to lose hours and days to it...",
    "Have you tried The Legend of Zelda?\nIn some sense, it was the starting point of \"adventure\" in video games.",
    "Have you tried Undertale?\nI hope I'm not the 10th person to ask you that. But it's, like, really good.",
    "Have you tried Wargroove?\nI'm glad that for every abandoned series, enough people are yearning for its return that one of them will know how to code.",
    "Have you tried Blasphemous?\nYou haven't? Blasphemy!\n...Sorry. You should try it, though!",
    "Have you tried Doom II?\nGot a good game on your hands? Just make it bigger and better.",
    "Have you tried Lingo?\nIt's an open world puzzle game. It features panels with non-verbally explained mechanics.\nIf you like this game, you'll like Lingo too.",
    "(Middle Yellow)\nYOU AILED OVERNIGHT\nH--- --- ----- -----?",
    "Have you tried Bumper Stickers?\nMaybe after spending so much time on this island, you are longing for a simpler puzzle game.",
    "Have you tried Pokemon Emerald?\nI'm going to say it: 10/10, just the right amount of water.",
    "Have you tried Terraria?\nA prime example of a survival sandbox game that beats the \"Wide as an ocean, deep as a puddle\" allegations.",
    
    "One day I was fascinated by the subject of generation of waves by wind.",
    "I don't like sandwiches. Why would you think I like sandwiches? Have you ever seen me with a sandwich?",
    "Where are you right now?\nI'm at soup!\nWhat do you mean you're at soup?",
    "Remember to ask in the Archipelago Discord what the Functioning Brain does.",
    "Don't use your puzzle skips, you might need them later.",
    "For an extra challenge, try playing blindfolded.",
    "Go to the top of the mountain and see if you can see your house.",
    "Yellow = Red + Green\nCyan = Green + Blue\nMagenta = Red + Blue",
    "Maybe that panel really is unsolvable.",
    "Did you make sure it was plugged in?",
    "Do not look into laser with remaining eye.",
    "Try pressing Space to jump.",
    "The Witness is a Doom clone.\nJust replace the demons with puzzles",
    "Test Hint please ignore",
    "Shapers can never be placed outside the panel boundaries, even if subtracted.",
    "The Keep laser panels use the same trick on both sides!",
    "Can't get past a door? Try going around. Can't go around? Try building a nether portal.",
    "We've been trying to reach you about your car's extended warranty.",
    "I hate this game. I hate this game. I hate this game.\n- Chess player Bobby Fischer",
    "Dear Mario,\nPlease come to the castle. I've baked a cake for you!",
    "Have you tried waking up?\nYeah, me neither.",
    "Why do they call it The Witness, when wit game the player view play of with the game.",
    "THE WIND FISH IN NAME ONLY, FOR IT IS NEITHER",
    "Like this game?\nTry The Wit.nes, Understand, INSIGHT, Taiji What the Witness?, and Tametsi.",
    "In a race, It's survival of the Witnesst.",
    "This hint has been removed. We apologize for your inconvenience.",
    "O-----------",
    "Circle is draw\nSquare is separate\nLine is win",
    "Circle is draw\nStar is pair\nLine is win",
    "Circle is draw\nCircle is copy\nLine is win",
    "Circle is draw\nDot is eat\nLine is win",
    "Circle is start\nWalk is draw\nLine is win",
    "Circle is start\nLine is win\nWitness is you",
    "Can't find any items?\nConsider a relaxing boat trip around the island!",
    "Don't forget to like, comment, and subscribe.",
    "Ah crap, gimme a second.\n[papers rustling]\nSorry, nothing.",
    "Trying to get a hint? Too bad.",
    "Here's a hint: Get good at the game.",
    "I'm still not entirely sure what we're witnessing here.",
    "Have you found a red page yet? No? Then have you found a blue page?",
    "And here we see the Witness player, seeking answers where there are none-\nDid someone turn on the loudspeaker?",

    "Be quiet. I can't hear the elevator.",
    "Witness me.\n- The famous last words of John Witness.",
    "It's okay, I always have to skip the Rotated Shaper puzzles too.",
    "Alan please add hint.",
    "Rumor has it there's an audio log with a hint nearby.",
    "In the future, war will break out between obelisk_sides and individual EP players.\nWhich side are you on?",
    "Droplets: Low, High, Mid.\nAmbience: Mid, Low, Mid, High.",
    "Name a better game involving lines. I'll wait.",
    "\"You have to draw a line in the sand.\"\n- Arin \"Egoraptor\" Hanson",
    "Have you tried?\nThe puzzles tend to get easier if you do.",
    "Sorry, I accidentally left my phone in the Jungle.\nAnd also all my fragile dishes.",
    "Winner of the \"Most Irrelevant PR in AP History\" award!",
    "I bet you wish this was a real hint :)",
    "\"This hint is an impostor.\"- Junk hint submitted by T1mshady.\n...wait, I'm not supposed to say that part?",
    "Wouldn't you like to know, weather buoy?",
    "Give me a few minutes, I should have better material by then.",
    "Just pet the doggy! You know you want to!!!",
    "ceci n'est pas une metroidvania",
    "HINT is MELT\nYOU is HOT",
    "Who's that behind you?",
    ":3",
    "^v ^^v> >>^>v\n^^v>v ^v>> v>^> v>v^",
    "Statement #0162601, regarding a strange island that--\nOh, wait, sorry. I'm not supposed to be here.",
    "Hollow Bastion has 6 progression items.\nOr maybe it doesn't.\nI wouldn't know.",
    "Set your hint count lower so I can tell you more jokes next time.",
    "A non-edge start point is similar to a cat.\nIt must be either inside or outside, it can't be both.",
    "What if we kissed on the Bunker Laser Platform?\nJk... unless?",
    "You don't have Boat? Invisible boat time!\nYou do have boat? Boat clipping time!",
    "Cet indice est en français. Nous nous excusons de tout inconvénients engendrés par cela.",
    "How many of you have personally witnessed a total solar eclipse?",
    "In the Treehouse area, you will find \n[Error: Data not found] progression items.",
    "Lingo\nLingoing\nLingone",
    "The name of the captain was Albert Einstein.",
    "Panel impossible Sigma plz fix",
    "Welcome Back! (:",
    "R R R U L L U L U R U R D R D R U U",
    "Have you tried checking your tracker?",
    
    "Hints suggested by:\nIHNN, Beaker, MrPokemon11, Ember, TheM8, NewSoupVi, Jasper Bird, T1mshady,"
    "KF, Yoshi348, Berserker, BowlinJim, oddGarrett, Pink Switch, Rever, Ishigh, snolid.",
]


def get_always_hint_items(world: "WitnessWorld"):
    always = [
        "Boat",
        "Caves Shortcuts",
        "Progressive Dots",
    ]

    difficulty = world.options.puzzle_randomization
    discards = world.options.shuffle_discarded_panels
    wincon = world.options.victory_condition

    if discards:
        if difficulty == 1:
            always.append("Arrows")
        else:
            always.append("Triangles")

    if wincon == 0:
        always += ["Mountain Bottom Floor Final Room Entry (Door)", "Mountain Bottom Floor Doors"]

    if wincon == 1:
        always += ["Challenge Entry (Panel)", "Caves Panels"]

    return always


def get_always_hint_locations(_: "WitnessWorld"):
    return {
        "Challenge Vault Box",
        "Mountain Bottom Floor Discard",
        "Theater Eclipse EP",
        "Shipwreck Couch EP",
        "Mountainside Cloud Cycle EP",
    }


def get_priority_hint_items(world: "WitnessWorld"):
    priority = {
        "Caves Mountain Shortcut (Door)",
        "Caves Swamp Shortcut (Door)",
        "Swamp Entry (Panel)",
        "Swamp Laser Shortcut (Door)",
    }

    if world.options.shuffle_symbols:
        symbols = [
            "Progressive Dots",
            "Progressive Stars",
            "Shapers",
            "Rotated Shapers",
            "Negative Shapers",
            "Arrows",
            "Triangles",
            "Eraser",
            "Black/White Squares",
            "Colored Squares",
            "Colored Dots",
            "Sound Dots",
            "Symmetry"
        ]

        priority.update(world.random.sample(symbols, 5))

    if world.options.shuffle_lasers:
        lasers = [
            "Symmetry Laser",
            "Town Laser",
            "Keep Laser",
            "Swamp Laser",
            "Treehouse Laser",
            "Monastery Laser",
            "Jungle Laser",
            "Quarry Laser",
            "Bunker Laser",
            "Shadows Laser",
        ]

        if world.options.shuffle_doors >= 2:
            priority.add("Desert Laser")
            priority.update(world.random.sample(lasers, 5))

        else:
            lasers.append("Desert Laser")
            priority.update(world.random.sample(lasers, 6))

    return priority


def get_priority_hint_locations(_: "WitnessWorld"):
    return {
        "Swamp Purple Underwater",
        "Shipwreck Vault Box",
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
        "Quarry Stoneworks Control Room Left",
    }


def make_hint_from_item(world: "WitnessWorld", item_name: str, own_itempool: List[Item]):
    locations = [item.location for item in own_itempool if item.name == item_name and item.location]

    if not locations:
        return None

    location_obj = world.random.choice(locations)
    location_name = location_obj.name

    if location_obj.player != world.player:
        location_name += " (" + world.multiworld.get_player_name(location_obj.player) + ")"

    return location_name, item_name, location_obj.address if (location_obj.player == world.player) else -1


def make_hint_from_location(world: "WitnessWorld", location: str):
    location_obj = world.multiworld.get_location(location, world.player)
    item_obj = world.multiworld.get_location(location, world.player).item
    item_name = item_obj.name
    if item_obj.player != world.player:
        item_name += " (" + world.multiworld.get_player_name(item_obj.player) + ")"

    return location, item_name, location_obj.address if (location_obj.player == world.player) else -1


def make_hints(world: "WitnessWorld", hint_amount: int, own_itempool: List[Item]):
    hints = list()

    prog_items_in_this_world = {
        item.name for item in own_itempool if item.advancement and item.code and item.location
    }
    loc_in_this_world = {
        location.name for location in world.multiworld.get_locations(world.player) if location.address
    }

    always_locations = [
        location for location in get_always_hint_locations(world)
        if location in loc_in_this_world
    ]
    always_items = [
        item for item in get_always_hint_items(world)
        if item in prog_items_in_this_world
    ]
    priority_locations = [
        location for location in get_priority_hint_locations(world)
        if location in loc_in_this_world
    ]
    priority_items = [
        item for item in get_priority_hint_items(world)
        if item in prog_items_in_this_world
    ]

    always_hint_pairs = dict()

    for item in always_items:
        hint_pair = make_hint_from_item(world, item, own_itempool)

        if not hint_pair or hint_pair[2] == 158007:  # Tutorial Gate Open
            continue

        always_hint_pairs[hint_pair[0]] = (hint_pair[1], True, hint_pair[2])

    for location in always_locations:
        hint_pair = make_hint_from_location(world, location)
        always_hint_pairs[hint_pair[0]] = (hint_pair[1], False, hint_pair[2])

    priority_hint_pairs = dict()

    for item in priority_items:
        hint_pair = make_hint_from_item(world, item, own_itempool)

        if not hint_pair or hint_pair[2] == 158007:  # Tutorial Gate Open
            continue

        priority_hint_pairs[hint_pair[0]] = (hint_pair[1], True, hint_pair[2])

    for location in priority_locations:
        hint_pair = make_hint_from_location(world, location)
        priority_hint_pairs[hint_pair[0]] = (hint_pair[1], False, hint_pair[2])

    already_hinted_locations = set()

    for loc, item in always_hint_pairs.items():
        if loc in already_hinted_locations:
            continue

        if item[1]:
            hints.append((f"{item[0]} can be found at {loc}.", item[2]))
        else:
            hints.append((f"{loc} contains {item[0]}.", item[2]))

        already_hinted_locations.add(loc)

    world.random.shuffle(hints)  # shuffle always hint order in case of low hint amount

    remaining_hints = hint_amount - len(hints)
    priority_hint_amount = int(max(0.0, min(len(priority_hint_pairs) / 2, remaining_hints / 2)))

    prog_items_in_this_world = sorted(list(prog_items_in_this_world))
    locations_in_this_world = sorted(list(loc_in_this_world))

    world.random.shuffle(prog_items_in_this_world)
    world.random.shuffle(locations_in_this_world)

    priority_hint_list = list(priority_hint_pairs.items())
    world.random.shuffle(priority_hint_list)
    for _ in range(0, priority_hint_amount):
        next_priority_hint = priority_hint_list.pop()
        loc = next_priority_hint[0]
        item = next_priority_hint[1]

        if loc in already_hinted_locations:
            continue

        if item[1]:
            hints.append((f"{item[0]} can be found at {loc}.", item[2]))
        else:
            hints.append((f"{loc} contains {item[0]}.", item[2]))

        already_hinted_locations.add(loc)

    next_random_hint_is_item = world.random.randrange(0, 2)

    while len(hints) < hint_amount:
        if next_random_hint_is_item:
            if not prog_items_in_this_world:
                next_random_hint_is_item = not next_random_hint_is_item
                continue

            hint = make_hint_from_item(world, prog_items_in_this_world.pop(), own_itempool)

            if not hint or hint[0] in already_hinted_locations:
                continue

            hints.append((f"{hint[1]} can be found at {hint[0]}.", hint[2]))

            already_hinted_locations.add(hint[0])
        else:
            hint = make_hint_from_location(world, locations_in_this_world.pop())

            if hint[0] in already_hinted_locations:
                continue

            hints.append((f"{hint[0]} contains {hint[1]}.", hint[2]))

            already_hinted_locations.add(hint[0])

        next_random_hint_is_item = not next_random_hint_is_item

    return hints


def generate_joke_hints(world: "WitnessWorld", amount: int) -> List[Tuple[str, int]]:
    return [(x, -1) for x in world.random.sample(joke_hints, amount)]
