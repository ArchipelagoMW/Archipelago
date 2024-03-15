import logging
from dataclasses import dataclass
from typing import Tuple, List, TYPE_CHECKING, Set, Dict, Optional, Union
from BaseClasses import Item, ItemClassification, Location, LocationProgressType, CollectionState
from . import StaticWitnessLogic
from .utils import weighted_sample

if TYPE_CHECKING:
    from . import WitnessWorld

CompactItemData = Tuple[str, Union[str, int], int]

joke_hints = [
    "Have you tried Adventure?\n...Holy crud, that game is 17 years older than me.",
    "Have you tried A Link to the Past?\nThe Archipelago game that started it all!",
    "Waiting to get your items?\nTry BK Sudoku! Make progress even while stuck.",
    "Have you tried Blasphemous?\nYou haven't? Blasphemy!\n...Sorry. You should try it, though!",
    "Have you tried Bumper Stickers?\nDecades after its inception, people are still inventing unique twists on the match-3 genre.",
    "Have you tried Bumper Stickers?\nMaybe after spending so much time on this island, you are longing for a simpler puzzle game.",
    "Have you tried Celeste 64?\nYou need smol low-poly Madeline in your life. TRUST ME.",
    "Have you tried ChecksFinder?\nIf you like puzzles, you might enjoy it!",
    "Have you tried Clique?\nIt's certainly a lot less complicated than this game!",
    "Have you tried Dark Souls III?\nA tough game like this feels better when friends are helping you!",
    "Have you tried Donkey Kong Country 3?\nA legendary game from a golden age of platformers!",
    "Have you tried DLC Quest?\nI know you all like parody games.\nI got way too many requests to make a randomizer for \"The Looker\".",
    "Have you tried Doom?\nI wonder if a smart fridge can connect to Archipelago.",
    "Have you tried Doom II?\nGot a good game on your hands? Just make it bigger and better.",
    "Have you tried Factorio?\nAlone in an unknown multiworld. Sound familiar?",
    "Have you tried Final Fantasy?\nExperience a classic game improved to fit modern standards!",
    "Have you tried Final Fantasy Mystic Quest?\nApparently, it was made in an attempt to simplify Final Fantasy for the western market.\nThey were right, I suck at RPGs.",
    "Have you tried Heretic?\nWait, there is a Doom Engine game where you can look UP AND DOWN???",
    "Have you tried Hollow Knight?\nAnother independent hit revolutionising a genre!",
    "Have you tried Hylics 2?\nStop motion might just be the epitome of unique art styles.",
    "Have you tried Kirby's Dream Land 3?\nAll good things must come to an end, including Nintendo's SNES library.\nWent out with a bang though!",
    "Have you tried Kingdom Hearts II?\nI'll wait for you to name a more epic crossover.",
    "Have you tried Link's Awakening DX?\nHopefully, Link won't be obsessed with circles when he wakes up.",
    "Have you tried Landstalker?\nThe Witness player's greatest fear: A diagonal movement grid...\nWait, I guess we have the Monastery puzzles.",
    "Have you tried Lingo?\nIt's an open world puzzle game. It features puzzle panels with non-verbally explained mechanics.\nIf you like this game, you'll like Lingo too.",
    "(Middle Yellow)\nYOU AILED OVERNIGHT\nH--- --- ----- -----?",
    "Have you tried Lufia II?\nRoguelites are not just a 2010s phenomenon, turns out.",
    "Have you tried Meritous?\nYou should know that obscure games are often groundbreaking!",
    "Have you tried The Messenger?\nOld ideas made new again. It's how all art is made.",
    "Have you tried Minecraft?\nI have recently learned this is a question that needs to be asked.",
    "Have you tried Mega Man Battle Network 3?\nIt's a Mega Man RPG. How could you not want to try that?",
    "Have you tried Muse Dash?\nRhythm game with cute girls!\n(Maybe skip if you don't like the Jungle panels)",
    "Have you tried Noita?\nIf you like punishing yourself, you will like it.",
    "Have you tried Ocarina of Time?\nOne of the biggest randomizers, big inspiration for this one's features!",
    "Have you tried Overcooked 2?\nWhen you're done relaxing with puzzles, use your energy to yell at your friends.",
    "Have you tried Pokemon Emerald?\nI'm going to say it: 10/10, just the right amount of water.",
    "Have you tried Pokemon Red&Blue?\nA cute pet collecting game that fascinated an entire generation.",
    "Have you tried Raft?\nHaven't you always wanted to explore the ocean surrounding this island?",
    "Have you tried Rogue Legacy?\nAfter solving so many puzzles it's the perfect way to rest your \"thinking\" brain.",
    "Have you tried Risk of Rain 2?\nI haven't either. But I hear it's incredible!",
    "Have you tried Sonic Adventure 2?\nIf the silence on this island is getting to you, there aren't many games more energetic.",
    "Have you tried Starcraft 2?\nUse strategy and management to crush your enemies!",
    "Have you tried Shivers?\nWitness 2 should totally feature a haunted museum.",
    "Have you tried Super Metroid?\nA classic game, yet still one of the best in the genre.",
    "Have you tried Super Mario 64?\n3-dimensional games like this owe everything to that game.",
    "Have you tried Super Mario World?\nI don't think I need to tell you that it is beloved by many.",
    "Have you tried SMZ3?\nWhy play one incredible game when you can play 2 at once?",
    "Have you tried Secret of Evermore?\nI haven't either. But I hear it's great!",
    "Have you tried Slay the Spire?\nExperience the thrill of combat without needing fast fingers!",
    "Have you tried Stardew Valley?\nThe Farming game that gave a damn. It's so easy to lose hours and days to it...",
    "Have you tried Subnautica?\nIf you like this game's lonely atmosphere, I would suggest you try it.",
    "Have you tried Terraria?\nA prime example of a survival sandbox game that beats the \"Wide as an ocean, deep as a puddle\" allegations.",
    "Have you tried Timespinner?\nEveryone who plays it ends up loving it!",
    "Have you tried The Legend of Zelda?\nIn some sense, it was the starting point of \"adventure\" in video games.",
    "Have you tried TUNC?\nWhat? No, I'm pretty sure I spelled that right.",
    "Have you tried TUNIC?\nRemember what discovering your first Environmental Puzzle was like?\nTUNIC will make you feel like that at least 5 times over.",
    "Have you tried Undertale?\nI hope I'm not the 10th person to ask you that. But it's, like, really good.",
    "Have you tried VVVVVV?\nExperience the essence of gaming distilled into its purest form!",
    "Have you tried Wargroove?\nI'm glad that for every abandoned series, enough people are yearning for its return that one of them will know how to code.",
    "Have you tried The Witness?\nOh. I guess you already have. Thanks for playing!",
    "Have you tried Zillion?\nMe neither. But it looks fun. So, let's try something new together?",
    "Have you tried Zork: Grand Inquisitor?\nThis 1997 game uses Z-Vision technology to simulate 3D environments.\nCome on, I know you wanna find out what \"Z-Vision\" is.",

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
    "In the Treehouse area, you will find 69 progression items.\nNice.\n(Source: Just trust me)",
    "Lingo\nLingoing\nLingone",
    "The name of the captain was Albert Einstein.",
    "Panel impossible Sigma plz fix",
    "Welcome Back! (:",
    "R R R U L L U L U R U R D R D R U U",
    "Have you tried checking your tracker?",
    "Lines are drawn on grids\nAll symbols must be obeyed\nIt's snowing on Mt. Fuji",
    "If you're BK, you could try today's Wittle:\nhttps://www.fourisland.com/wittle/",
    "They say that plundering Outside Ganon's Castle is a foolish choice.",
    "You should try to BLJ. Maybe that'll get you through that door.",
    "Error: Witness Randomizer disconnected from Archipelago.\n(lmao gottem)",
    "You have found: One (1) Audio Log!\nSeries of 49! Collect them all!",
    "In the Town area, you will find 1 good boi.\nGo pet him.",
    "If you're ever stuck on a panel, feel free to ask Rever.\nSurely you'll understand his drawing!",
    "[This hint has been removed as part of the Witness Protection Program]",
    "Panel Diddle",
    "Witness AP when",
    "This game is my favorite walking simulator.",
    "Did you hear that? It said --\n\nCosmic background radiation is a riot!",
    "Well done solving those puzzles.\nPray return to the Waking Sands.",
    "Having trouble finding your checks?\nTry the PopTracker pack!\nIt's got auto-tracking and a detailed map.",

    "Hints suggested by:\nIHNN, Beaker, MrPokemon11, Ember, TheM8, NewSoupVi, Jasper Bird, T1mshady, "
    "KF, Yoshi348, Berserker, BowlinJim, oddGarrett, Pink Switch, Rever, Ishigh, snolid.",
]


@dataclass
class WitnessLocationHint:
    location: Location
    hint_came_from_location: bool

    # If a hint gets added to a set twice, but once as an item hint and once as a location hint, those are the same
    def __hash__(self):
        return hash(self.location)

    def __eq__(self, other):
        return self.location == other.location


@dataclass
class WitnessWordedHint:
    wording: str
    location: Optional[Location] = None
    area: Optional[str] = None
    area_amount: Optional[int] = None


def get_always_hint_items(world: "WitnessWorld") -> List[str]:
    always = [
        "Boat",
        "Caves Shortcuts",
        "Progressive Dots",
    ]

    difficulty = world.options.puzzle_randomization
    discards = world.options.shuffle_discarded_panels
    wincon = world.options.victory_condition

    if discards:
        if difficulty == "sigma_expert":
            always.append("Arrows")
        else:
            always.append("Triangles")

    if wincon == "elevator":
        always += ["Mountain Bottom Floor Pillars Room Entry (Door)", "Mountain Bottom Floor Doors"]

    if wincon == "challenge":
        always += ["Challenge Entry (Panel)", "Caves Panels"]

    return always


def get_always_hint_locations(world: "WitnessWorld") -> List[str]:
    always = [
        "Challenge Vault Box",
        "Mountain Bottom Floor Discard",
        "Theater Eclipse EP",
        "Shipwreck Couch EP",
        "Mountainside Cloud Cycle EP",
    ]

    # Add Obelisk Sides that contain EPs that are meant to be hinted, if they are necessary to complete the Obelisk Side
    if "0x339B6" not in world.player_logic.COMPLETELY_DISABLED_ENTITIES:
        always.append("Town Obelisk Side 6")  # Eclipse EP

    if "0x3388F" not in world.player_logic.COMPLETELY_DISABLED_ENTITIES:
        always.append("Treehouse Obelisk Side 4")  # Couch EP

    if "0x335AE" not in world.player_logic.COMPLETELY_DISABLED_ENTITIES:
        always.append("Mountainside Obelisk Side 1")  # Cloud Cycle EP.

    return always


def get_priority_hint_items(world: "WitnessWorld") -> List[str]:
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
            "Sound Dots",
            "Progressive Symmetry"
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

    return sorted(priority)


def get_priority_hint_locations(world: "WitnessWorld") -> List[str]:
    priority = [
        "Tutorial Patio Floor",
        "Tutorial Patio Flowers EP",
        "Swamp Purple Underwater",
        "Shipwreck Vault Box",
        "Town RGB House Upstairs Left",
        "Town RGB House Upstairs Right",
        "Treehouse Green Bridge 7",
        "Treehouse Green Bridge Discard",
        "Shipwreck Discard",
        "Desert Vault Box",
        "Mountainside Vault Box",
        "Mountainside Discard",
        "Tunnels Theater Flowers EP",
        "Boat Shipwreck Green EP",
        "Quarry Stoneworks Control Room Left",
    ]
    
    # Add Obelisk Sides that contain EPs that are meant to be hinted, if they are necessary to complete the Obelisk Side
    if "0x33A20" not in world.player_logic.COMPLETELY_DISABLED_ENTITIES:
        priority.append("Town Obelisk Side 6")  # Theater Flowers EP

    if "0x28B29" not in world.player_logic.COMPLETELY_DISABLED_ENTITIES:
        priority.append("Treehouse Obelisk Side 4")  # Shipwreck Green EP

    if "0x33600" not in world.player_logic.COMPLETELY_DISABLED_ENTITIES:
        priority.append("Town Obelisk Side 2")  # Tutorial Patio Flowers EP.

    return priority


def word_direct_hint(world: "WitnessWorld", hint: WitnessLocationHint):
    location_name = hint.location.name
    if hint.location.player != world.player:
        location_name += " (" + world.multiworld.get_player_name(hint.location.player) + ")"

    item = hint.location.item
    item_name = item.name
    if item.player != world.player:
        item_name += " (" + world.multiworld.get_player_name(item.player) + ")"

    if hint.hint_came_from_location:
        hint_text = f"{location_name} contains {item_name}."
    else:
        hint_text = f"{item_name} can be found at {location_name}."

    return WitnessWordedHint(hint_text, hint.location)


def hint_from_item(world: "WitnessWorld", item_name: str, own_itempool: List[Item]) -> Optional[WitnessLocationHint]:

    locations = [item.location for item in own_itempool if item.name == item_name and item.location]

    if not locations:
        return None

    location_obj = world.random.choice(locations)
    location_name = location_obj.name

    if location_obj.player != world.player:
        location_name += " (" + world.multiworld.get_player_name(location_obj.player) + ")"

    return WitnessLocationHint(location_obj, False)


def hint_from_location(world: "WitnessWorld", location: str) -> Optional[WitnessLocationHint]:
    location_obj = world.multiworld.get_location(location, world.player)
    item_obj = world.multiworld.get_location(location, world.player).item
    item_name = item_obj.name
    if item_obj.player != world.player:
        item_name += " (" + world.multiworld.get_player_name(item_obj.player) + ")"

    return WitnessLocationHint(location_obj, True)


def get_items_and_locations_in_random_order(world: "WitnessWorld", own_itempool: List[Item]):
    prog_items_in_this_world = sorted(
        item.name for item in own_itempool
        if item.advancement and item.code and item.location
    )
    locations_in_this_world = sorted(
        location.name for location in world.multiworld.get_locations(world.player)
        if location.address and location.progress_type != LocationProgressType.EXCLUDED
    )

    world.random.shuffle(prog_items_in_this_world)
    world.random.shuffle(locations_in_this_world)

    return prog_items_in_this_world, locations_in_this_world


def make_always_and_priority_hints(world: "WitnessWorld", own_itempool: List[Item],
                                   already_hinted_locations: Set[Location]
                                   ) -> Tuple[List[WitnessLocationHint], List[WitnessLocationHint]]:
    prog_items_in_this_world, loc_in_this_world = get_items_and_locations_in_random_order(world, own_itempool)

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

    # Get always and priority location/item hints
    always_location_hints = {hint_from_location(world, location) for location in always_locations}
    always_item_hints = {hint_from_item(world, item, own_itempool) for item in always_items}
    priority_location_hints = {hint_from_location(world, location) for location in priority_locations}
    priority_item_hints = {hint_from_item(world, item, own_itempool) for item in priority_items}

    # Combine the sets. This will get rid of duplicates
    always_hints_set = always_item_hints | always_location_hints
    priority_hints_set = priority_item_hints | priority_location_hints

    # Make sure priority hints doesn't contain any hints that are already always hints.
    priority_hints_set -= always_hints_set

    always_generator = [hint for hint in always_hints_set if hint and hint.location not in already_hinted_locations]
    priority_generator = [hint for hint in priority_hints_set if hint and hint.location not in already_hinted_locations]

    # Convert both hint types to list and then shuffle. Also, get rid of None and Tutorial Gate Open.
    always_hints = sorted(always_generator, key=lambda h: h.location)
    priority_hints = sorted(priority_generator, key=lambda h: h.location)
    world.random.shuffle(always_hints)
    world.random.shuffle(priority_hints)

    return always_hints, priority_hints


def make_extra_location_hints(world: "WitnessWorld", hint_amount: int, own_itempool: List[Item],
                              already_hinted_locations: Set[Location], hints_to_use_first: List[WitnessLocationHint],
                              unhinted_locations_for_hinted_areas: Dict[str, Set[Location]]) -> List[WitnessWordedHint]:
    prog_items_in_this_world, locations_in_this_world = get_items_and_locations_in_random_order(world, own_itempool)

    next_random_hint_is_location = world.random.randrange(0, 2)

    hints = []

    # This is a way to reverse a Dict[a,List[b]] to a Dict[b,a]
    area_reverse_lookup = {v: k for k, l in unhinted_locations_for_hinted_areas.items() for v in l}

    while len(hints) < hint_amount:
        if not prog_items_in_this_world and not locations_in_this_world and not hints_to_use_first:
            player_name = world.multiworld.get_player_name(world.player)
            logging.warning(f"Ran out of items/locations to hint for player {player_name}.")
            break

        if hints_to_use_first:
            location_hint = hints_to_use_first.pop()
        elif next_random_hint_is_location and locations_in_this_world:
            location_hint = hint_from_location(world, locations_in_this_world.pop())
        elif not next_random_hint_is_location and prog_items_in_this_world:
            location_hint = hint_from_item(world, prog_items_in_this_world.pop(), own_itempool)
        # The list that the hint was supposed to be taken from was empty.
        # Try the other list, which has to still have something, as otherwise, all lists would be empty,
        # which would have triggered the guard condition above.
        else:
            next_random_hint_is_location = not next_random_hint_is_location
            continue

        if not location_hint or location_hint.location in already_hinted_locations:
            continue

        # Don't hint locations in areas that are almost fully hinted out already
        if location_hint.location in area_reverse_lookup:
            area = area_reverse_lookup[location_hint.location]
            if len(unhinted_locations_for_hinted_areas[area]) == 1:
                continue
            del area_reverse_lookup[location_hint.location]
            unhinted_locations_for_hinted_areas[area] -= {location_hint.location}

        hints.append(word_direct_hint(world, location_hint))
        already_hinted_locations.add(location_hint.location)

        next_random_hint_is_location = not next_random_hint_is_location

    return hints


def generate_joke_hints(world: "WitnessWorld", amount: int) -> List[Tuple[str, int, int]]:
    return [(x, -1, -1) for x in world.random.sample(joke_hints, amount)]


def choose_areas(world: "WitnessWorld", amount: int, locations_per_area: Dict[str, List[Location]],
                 already_hinted_locations: Set[Location]) -> Tuple[List[str], Dict[str, Set[Location]]]:
    """
    Choose areas to hint.
    This takes into account that some areas may already have had items hinted in them through location hints.
    When this happens, they are made less likely to receive an area hint.
    """

    unhinted_locations_per_area = dict()
    unhinted_location_percentage_per_area = dict()

    for area_name, locations in locations_per_area.items():
        not_yet_hinted_locations = sum(location not in already_hinted_locations for location in locations)
        unhinted_locations_per_area[area_name] = {loc for loc in locations if loc not in already_hinted_locations}
        unhinted_location_percentage_per_area[area_name] = not_yet_hinted_locations / len(locations)

    items_per_area = {area_name: [location.item for location in locations]
                      for area_name, locations in locations_per_area.items()}

    areas = sorted(area for area in items_per_area if unhinted_location_percentage_per_area[area])
    weights = [unhinted_location_percentage_per_area[area] for area in areas]

    amount = min(amount, len(weights))

    hinted_areas = weighted_sample(world.random, areas, weights, amount)

    return hinted_areas, unhinted_locations_per_area


def get_hintable_areas(world: "WitnessWorld") -> Tuple[Dict[str, List[Location]], Dict[str, List[Item]]]:
    potential_areas = list(StaticWitnessLogic.ALL_AREAS_BY_NAME.keys())

    locations_per_area = dict()
    items_per_area = dict()

    for area in potential_areas:
        regions = [
            world.regio.created_regions[region]
            for region in StaticWitnessLogic.ALL_AREAS_BY_NAME[area]["regions"]
            if region in world.regio.created_regions
        ]
        locations = [location for region in regions for location in region.get_locations() if location.address]

        if locations:
            locations_per_area[area] = locations
            items_per_area[area] = [location.item for location in locations]

    return locations_per_area, items_per_area


def word_area_hint(world: "WitnessWorld", hinted_area: str, corresponding_items: List[Item]) -> Tuple[str, int]:
    """
    Word the hint for an area using natural sounding language.
    This takes into account how much progression there is, how much of it is local/non-local, and whether there are
    any local lasers to be found in this area.
    """

    local_progression = sum(item.player == world.player and item.advancement for item in corresponding_items)
    non_local_progression = sum(item.player != world.player and item.advancement for item in corresponding_items)

    laser_names = {"Symmetry Laser", "Desert Laser", "Quarry Laser", "Shadows Laser", "Town Laser", "Monastery Laser",
                   "Jungle Laser", "Bunker Laser", "Swamp Laser", "Treehouse Laser", "Keep Laser", }

    local_lasers = sum(
        item.player == world.player and item.name in laser_names
        for item in corresponding_items
    )

    total_progression = non_local_progression + local_progression

    player_count = world.multiworld.players

    area_progression_word = "Both" if total_progression == 2 else "All"

    if not total_progression:
        hint_string = f"In the {hinted_area} area, you will find no progression items."

    elif total_progression == 1:
        hint_string = f"In the {hinted_area} area, you will find 1 progression item."

        if player_count > 1:
            if local_lasers:
                hint_string += "\nThis item is a laser for this world."
            elif non_local_progression:
                other_player_str = "the other player" if player_count == 2 else "another player"
                hint_string += f"\nThis item is for {other_player_str}."
            else:
                hint_string += "\nThis item is for this world."
        else:
            if local_lasers:
                hint_string += "\nThis item is a laser."

    else:
        hint_string = f"In the {hinted_area} area, you will find {total_progression} progression items."

        if local_lasers == total_progression:
            sentence_end = (" for this world." if player_count > 1 else ".")
            hint_string += f"\nAll of them are lasers" + sentence_end

        elif player_count > 1:
            if local_progression and non_local_progression:
                if non_local_progression == 1:
                    other_player_str = "the other player" if player_count == 2 else "another player"
                    hint_string += f"\nOne of them is for {other_player_str}."
                else:
                    other_player_str = "the other player" if player_count == 2 else "other players"
                    hint_string += f"\n{non_local_progression} of them are for {other_player_str}."
            elif non_local_progression:
                other_players_str = "the other player" if player_count == 2 else "other players"
                hint_string += f"\n{area_progression_word} of them are for {other_players_str}."
            elif local_progression:
                hint_string += f"\n{area_progression_word} of them are for this world."

            if local_lasers == 1:
                if not non_local_progression:
                    hint_string += "\nAlso, one of them is a laser."
                else:
                    hint_string += "\nAlso, one of them is a laser for this world."
            elif local_lasers:
                if not non_local_progression:
                    hint_string += f"\nAlso, {local_lasers} of them are lasers."
                else:
                    hint_string += f"\nAlso, {local_lasers} of them are lasers for this world."

        else:
            if local_lasers == 1:
                hint_string += "\nOne of them is a laser."
            elif local_lasers:
                hint_string += f"\n{local_lasers} of them are lasers."

    return hint_string, total_progression


def make_area_hints(world: "WitnessWorld", amount: int, already_hinted_locations: Set[Location]
                    ) -> Tuple[List[WitnessWordedHint], Dict[str, Set[Location]]]:
    locs_per_area, items_per_area = get_hintable_areas(world)

    hinted_areas, unhinted_locations_per_area = choose_areas(world, amount, locs_per_area, already_hinted_locations)

    hints = []

    for hinted_area in hinted_areas:
        hint_string, prog_amount = word_area_hint(world, hinted_area, items_per_area[hinted_area])

        hints.append(WitnessWordedHint(hint_string, None, f"hinted_area:{hinted_area}", prog_amount))

    if len(hinted_areas) < amount:
        player_name = world.multiworld.get_player_name(world.player)
        logging.warning(f"Was not able to make {amount} area hints for player {player_name}. "
                        f"Made {len(hinted_areas)} instead, and filled the rest with random location hints.")

    return hints, unhinted_locations_per_area


def create_all_hints(world: "WitnessWorld", hint_amount: int, area_hints: int,
                     already_hinted_locations: Set[Location]) -> List[WitnessWordedHint]:
    generated_hints: List[WitnessWordedHint] = []

    state = CollectionState(world.multiworld)

    # Keep track of already hinted locations. Consider early Tutorial as "already hinted"

    already_hinted_locations |= {
        loc for loc in world.multiworld.get_reachable_locations(state, world.player)
        if loc.address and StaticWitnessLogic.ENTITIES_BY_NAME[loc.name]["area"]["name"] == "Tutorial (Inside)"
    }

    intended_location_hints = hint_amount - area_hints

    # First, make always and priority hints.

    always_hints, priority_hints = make_always_and_priority_hints(
        world, world.own_itempool, already_hinted_locations
    )

    generated_always_hints = len(always_hints)
    possible_priority_hints = len(priority_hints)

    # Make as many always hints as possible
    always_hints_to_use = min(intended_location_hints, generated_always_hints)

    # Make up to half of the rest of the location hints priority hints, using up to half of the possibly priority hints
    remaining_location_hints = intended_location_hints - always_hints_to_use
    priority_hints_to_use = int(max(0.0, min(possible_priority_hints / 2, remaining_location_hints / 2)))

    for _ in range(always_hints_to_use):
        location_hint = always_hints.pop()
        generated_hints.append(word_direct_hint(world, location_hint))
        already_hinted_locations.add(location_hint.location)

    for _ in range(priority_hints_to_use):
        location_hint = priority_hints.pop()
        generated_hints.append(word_direct_hint(world, location_hint))
        already_hinted_locations.add(location_hint.location)

    location_hints_created_in_round_1 = len(generated_hints)

    unhinted_locations_per_area: Dict[str, Set[Location]] = dict()

    # Then, make area hints.
    if area_hints:
        generated_area_hints, unhinted_locations_per_area = make_area_hints(world, area_hints, already_hinted_locations)
        generated_hints += generated_area_hints

    # If we don't have enough hints yet, recalculate always and priority hints, then fill with random hints
    if len(generated_hints) < hint_amount:
        remaining_needed_location_hints = hint_amount - len(generated_hints)

        # Save old values for used always and priority hints for later calculations
        amt_of_used_always_hints = always_hints_to_use
        amt_of_used_priority_hints = priority_hints_to_use

        # Recalculate how many always hints and priority hints are supposed to be used
        intended_location_hints = remaining_needed_location_hints + location_hints_created_in_round_1

        always_hints_to_use = min(intended_location_hints, generated_always_hints)
        priority_hints_to_use = int(max(0.0, min(possible_priority_hints / 2, remaining_location_hints / 2)))

        # If we now need more always hints and priority hints than we thought previously, make some more.
        more_always_hints = always_hints_to_use - amt_of_used_always_hints
        more_priority_hints = priority_hints_to_use - amt_of_used_priority_hints

        extra_always_and_priority_hints: List[WitnessLocationHint] = []

        for _ in range(more_always_hints):
            extra_always_and_priority_hints.append(always_hints.pop())

        for _ in range(more_priority_hints):
            extra_always_and_priority_hints.append(priority_hints.pop())

        generated_hints += make_extra_location_hints(
            world, hint_amount - len(generated_hints), world.own_itempool, already_hinted_locations,
            extra_always_and_priority_hints, unhinted_locations_per_area
        )

    # If we still don't have enough for whatever reason, throw a warning, proceed with the lower amount
    if len(generated_hints) != hint_amount:
        player_name = world.multiworld.get_player_name(world.player)
        logging.warning(f"Couldn't generate {hint_amount} hints for player {player_name}. "
                        f"Generated {len(generated_hints)} instead.")

    return generated_hints


def make_compact_hint_data(hint: WitnessWordedHint, local_player_number: int) -> CompactItemData:
    location = hint.location
    area_amount = hint.area_amount

    # None if junk hint, address if location hint, area string if area hint
    arg_1 = location.address if location else (hint.area if hint.area else None)

    # self.player if junk hint, player if location hint, progression amount if area hint
    arg_2 = area_amount if area_amount is not None else (location.player if location else local_player_number)

    return hint.wording, arg_1, arg_2


def make_laser_hints(world: "WitnessWorld", laser_names: List[str]) -> Dict[str, WitnessWordedHint]:
    laser_hints_by_name = dict()

    for item_name in laser_names:
        location_hint = hint_from_item(world, item_name, world.own_itempool)
        if not location_hint:
            continue

        laser_hints_by_name[item_name] = word_direct_hint(world, location_hint)

    return laser_hints_by_name
