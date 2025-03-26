from typing import TYPE_CHECKING
from worlds.generic.Rules import set_rule

if TYPE_CHECKING:
    from . import WordipelagoWorld

def all_needed_locations_checked(state, player):
    return state.has("Word Master", player)

def needed_for_words(state, player, vowels, score, guesses = 1, yellow = False):
    possible_score = 0
    vowels_items = ["Letter A", "Letter E", "Letter I", "Letter O", "Letter U", "Letter Y"]
    if(state.has("Letter A", player)):
        possible_score += 10
    if(state.has("Letter E", player)):
        possible_score += 10
    if(state.has("Letter I", player)):
        possible_score += 10
    if(state.has("Letter O", player)):
        possible_score += 10
    if(state.has("Letter U", player)):
        possible_score += 10
    if(state.has("Letter Y", player)):
        possible_score += 7

    has_strong_letters = 0
    if(state.has("Letter B", player)):
        possible_score += 8
    if(state.has("Letter c", player)):
        possible_score += 8
    if(state.has("Letter D", player)):
        possible_score += 9
    if(state.has("Letter F", player)):
        possible_score += 7
    if(state.has("Letter G", player)):
        possible_score += 9
    if(state.has("Letter H", player)):
        possible_score += 7
    if(state.has("Letter J", player)):
        possible_score += 3
    if(state.has("Letter K", player)):
        possible_score += 6
    if(state.has("Letter L", player)):
        possible_score += 10
    if(state.has("Letter M", player)):
        possible_score += 8
    if(state.has("Letter N", player)):
        possible_score += 10
    if(state.has("Letter P", player)):
        possible_score += 8
    if(state.has("Letter Q", player)):
        possible_score += 1
    if(state.has("Letter R", player)):
        possible_score += 10
    if(state.has("Letter S", player)):
        possible_score += 10
    if(state.has("Letter T", player)):
        possible_score += 10
    if(state.has("Letter V", player)):
        possible_score += 7
    if(state.has("Letter W", player)):
        possible_score += 7
    if(state.has("Letter X", player)):
        possible_score += 3
    if(state.has("Letter Z", player)):
        possible_score += 1

    return state.has_from_list_unique(vowels_items, player, vowels) and possible_score >= score and (not yellow or state.has('Yellow Letters', player)) and state.has('Guess', player, guesses)

def create_rules(world: "WordipelagoWorld"):
    multiworld = world.multiworld
    player = world.player

    multiworld.get_region("Menu", player).add_exits(['Letters'])
    multiworld.get_region("Letters", player).add_exits(
        [ "Word Best", "Green Checks", "Yellow Checks"]
    )
    
    multiworld.get_region("Green Checks", player).add_exits(
        ['Green Checks 1'],
        {"Green Checks 1": lambda state: needed_for_words(state, world.player, 0, 0, 1)}
    )
    multiworld.get_region("Green Checks 1", player).add_exits(
        ['Green Checks 2'],
        {"Green Checks 2": lambda state: needed_for_words(state, world.player, 1, 30, 1)}
    )
    multiworld.get_region("Green Checks 2", player).add_exits(
        ['Green Checks 3'],
        {"Green Checks 3": lambda state: needed_for_words(state, world.player, 2, 60, 2)}
    )
    multiworld.get_region("Green Checks 3", player).add_exits(
        ['Green Checks 4'],
        {"Green Checks 4": lambda state: needed_for_words(state, world.player, 3, 80, 3)}
    )
    multiworld.get_region("Green Checks 4", player).add_exits(
        ['Green Checks 5'],
        {"Green Checks 5": lambda state: needed_for_words(state, world.player, 4, 100, 4, True)}
    )
    multiworld.get_region("Green Checks 5", player).add_exits(
        ['Words']
    )

    multiworld.get_region("Yellow Checks", player).add_exits(
        ['Yellow Checks 1'],
        {"Yellow Checks 1": lambda state: needed_for_words(state, world.player, 0, 6, 1, True)}
    )
    multiworld.get_region("Yellow Checks 1", player).add_exits(
        ['Yellow Checks 2'],
        {"Yellow Checks 2": lambda state: needed_for_words(state, world.player, 2, 30, 1, True)}
    )
    multiworld.get_region("Yellow Checks 2", player).add_exits(
        ['Yellow Checks 3'],
        {"Yellow Checks 3": lambda state: needed_for_words(state, world.player, 2, 60, 2, True)}
    )
    multiworld.get_region("Yellow Checks 3", player).add_exits(
        ['Yellow Checks 4'],
        {"Yellow Checks 4": lambda state: needed_for_words(state, world.player, 3, 80, 2, True)}
    )
    multiworld.get_region("Yellow Checks 4", player).add_exits(
        ['Yellow Checks 5'],
        {"Yellow Checks 5": lambda state: needed_for_words(state, world.player, 4, 100, 4, True)}
    )
    
    if(world.options.letter_checks >= 1):
        world.get_location("Used A").access_rule = lambda state: state.has("Letter A", world.player)
        world.get_location("Used E").access_rule = lambda state: state.has("Letter E", world.player)
        world.get_location("Used I").access_rule = lambda state: state.has("Letter I", world.player)
        world.get_location("Used O").access_rule = lambda state: state.has("Letter O", world.player)
        world.get_location("Used U").access_rule = lambda state: state.has("Letter U", world.player)
        world.get_location("Used Y").access_rule = lambda state: state.has("Letter Y", world.player)
        world.get_location("Used A").item_rule = lambda item: item.name != "Letter A"
        world.get_location("Used E").item_rule = lambda item: item.name != "Letter E"
        world.get_location("Used I").item_rule = lambda item: item.name != "Letter I"
        world.get_location("Used O").item_rule = lambda item: item.name != "Letter O"
        world.get_location("Used U").item_rule = lambda item: item.name != "Letter U"
        world.get_location("Used Y").item_rule = lambda item: item.name != "Letter Y"
        
    if(world.options.letter_checks >= 2):
        world.get_location("Used B").access_rule = lambda state: state.has("Letter B", world.player)
        world.get_location("Used C").access_rule = lambda state: state.has("Letter C", world.player)
        world.get_location("Used D").access_rule = lambda state: state.has("Letter D", world.player)
        world.get_location("Used F").access_rule = lambda state: state.has("Letter F", world.player)
        world.get_location("Used G").access_rule = lambda state: state.has("Letter G", world.player)
        world.get_location("Used H").access_rule = lambda state: state.has("Letter H", world.player)
        world.get_location("Used L").access_rule = lambda state: state.has("Letter L", world.player)
        world.get_location("Used M").access_rule = lambda state: state.has("Letter M", world.player)
        world.get_location("Used N").access_rule = lambda state: state.has("Letter N", world.player)
        world.get_location("Used P").access_rule = lambda state: state.has("Letter P", world.player)
        world.get_location("Used R").access_rule = lambda state: state.has("Letter R", world.player)
        world.get_location("Used S").access_rule = lambda state: state.has("Letter S", world.player)
        world.get_location("Used T").access_rule = lambda state: state.has("Letter T", world.player)
        world.get_location("Used B").item_rule = lambda item: item.name != "Letter B"
        world.get_location("Used C").item_rule = lambda item: item.name != "Letter C"
        world.get_location("Used D").item_rule = lambda item: item.name != "Letter D"
        world.get_location("Used F").item_rule = lambda item: item.name != "Letter F"
        world.get_location("Used G").item_rule = lambda item: item.name != "Letter G"
        world.get_location("Used H").item_rule = lambda item: item.name != "Letter H"
        world.get_location("Used L").item_rule = lambda item: item.name != "Letter L"
        world.get_location("Used M").item_rule = lambda item: item.name != "Letter M"
        world.get_location("Used N").item_rule = lambda item: item.name != "Letter N"
        world.get_location("Used P").item_rule = lambda item: item.name != "Letter P"
        world.get_location("Used R").item_rule = lambda item: item.name != "Letter R"
        world.get_location("Used S").item_rule = lambda item: item.name != "Letter S"
        world.get_location("Used T").item_rule = lambda item: item.name != "Letter T"
        
    if(world.options.letter_checks == 3):
        world.get_location("Used V").access_rule = lambda state: state.has("Letter V", world.player)
        world.get_location("Used W").access_rule = lambda state: state.has("Letter W", world.player)
        world.get_location("Used X").access_rule = lambda state: state.has("Letter X", world.player)
        world.get_location("Used Z").access_rule = lambda state: state.has("Letter Z", world.player)
        world.get_location("Used Q").access_rule = lambda state: state.has("Letter Q", world.player)
        world.get_location("Used J").access_rule = lambda state: state.has("Letter J", world.player)
        world.get_location("Used K").access_rule = lambda state: state.has("Letter K", world.player)
        world.get_location("Used J").item_rule = lambda item: item.name != "Letter J"
        world.get_location("Used K").item_rule = lambda item: item.name != "Letter K"
        world.get_location("Used Q").item_rule = lambda item: item.name != "Letter Q"
        world.get_location("Used V").item_rule = lambda item: item.name != "Letter V"
        world.get_location("Used W").item_rule = lambda item: item.name != "Letter W"
        world.get_location("Used X").item_rule = lambda item: item.name != "Letter X"
        world.get_location("Used Z").item_rule = lambda item: item.name != "Letter Z"

    if(world.options.yellow_checks == 1):
        # Deny yellow letters being placed behind yellow positional checks
        world.get_location("----Y").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("---Y-").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("---YY").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("--Y--").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("--Y-Y").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("--YY-").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("--YYY").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("-Y---").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("-Y--Y").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("-Y-Y-").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("-Y-YY").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("-YY--").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("-YY-Y").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("-YYY-").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("-YYYY").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("Y----").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("Y---Y").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("Y--Y-").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("Y--YY").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("Y-Y--").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("Y-Y-Y").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("Y-YY-").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("Y-YYY").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("YY---").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("YY--Y").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("YY-Y-").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("YY-YY").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("YYY--").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("YYY-Y").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("YYYY-").item_rule = lambda item: item.name != 'Yellow Letters'
        world.get_location("YYYYY").item_rule = lambda item: item.name != 'Yellow Letters'
    

    world.multiworld.completion_condition[world.player] = lambda state: all_needed_locations_checked(state, world.player)