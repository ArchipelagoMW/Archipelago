from typing import TYPE_CHECKING
from worlds.generic.Rules import set_rule

if TYPE_CHECKING:
    from . import WordipelagoWorld

def needed_for_words(state, world, vowels, score, guesses = 1, yellow = False):
    possible_score = 0
    has_vowels = 0
    if(state.has("Letter A", world.player)):
        has_vowels += 1
        possible_score += 10
    if(state.has("Letter E", world.player)):
        has_vowels += 1
        possible_score += 10
    if(state.has("Letter I", world.player)):
        has_vowels += 1
        possible_score += 10
    if(state.has("Letter O", world.player)):
        has_vowels += 1
        possible_score += 10
    if(state.has("Letter U", world.player)):
        has_vowels += 1
        possible_score += 10
    if(state.has("Letter Y", world.player)):
        has_vowels += 1
        possible_score += 7

    has_strong_letters = 0
    if(state.has("Letter B", world.player)):
        possible_score += 8
    if(state.has("Letter c", world.player)):
        possible_score += 8
    if(state.has("Letter D", world.player)):
        possible_score += 9
    if(state.has("Letter F", world.player)):
        possible_score += 7
    if(state.has("Letter G", world.player)):
        possible_score += 9
    if(state.has("Letter H", world.player)):
        possible_score += 7
    if(state.has("Letter J", world.player)):
        possible_score += 3
    if(state.has("Letter K", world.player)):
        possible_score += 6
    if(state.has("Letter L", world.player)):
        possible_score += 10
    if(state.has("Letter M", world.player)):
        possible_score += 8
    if(state.has("Letter N", world.player)):
        possible_score += 10
    if(state.has("Letter P", world.player)):
        possible_score += 8
    if(state.has("Letter Q", world.player)):
        possible_score += 1
    if(state.has("Letter R", world.player)):
        possible_score += 10
    if(state.has("Letter S", world.player)):
        possible_score += 10
    if(state.has("Letter T", world.player)):
        possible_score += 10
    if(state.has("Letter V", world.player)):
        possible_score += 7
    if(state.has("Letter W", world.player)):
        possible_score += 7
    if(state.has("Letter X", world.player)):
        possible_score += 3
    if(state.has("Letter Z", world.player)):
        possible_score += 1

    return has_vowels >= vowels and possible_score >= score and (not yellow or world.options.yellow_unlocked or state.has('Yellow Letters', world.player)) and state.has('Guess', world.player, guesses - world.options.starting_guesses)

def create_rules(world: "WordipelagoWorld"):
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

    # Green position checks
    if(world.options.green_checks == 2 or world.options.green_checks == 3):
        world.get_location("----G").access_rule = lambda state: needed_for_words(state, world, 1, 20)
        world.get_location("---G-").access_rule = lambda state: needed_for_words(state, world, 1, 20)
        world.get_location("---GG").access_rule = lambda state: needed_for_words(state, world, 2, 30)
        world.get_location("--G--").access_rule = lambda state: needed_for_words(state, world, 1, 20)
        world.get_location("--G-G").access_rule = lambda state: needed_for_words(state, world, 2, 30)
        world.get_location("--GG-").access_rule = lambda state: needed_for_words(state, world, 2, 30)
        world.get_location("--GGG").access_rule = lambda state: needed_for_words(state, world, 2, 60, 2)
        world.get_location("-G---").access_rule = lambda state: needed_for_words(state, world, 1, 20)
        world.get_location("-G--G").access_rule = lambda state: needed_for_words(state, world, 2, 30)
        world.get_location("-G-G-").access_rule = lambda state: needed_for_words(state, world, 2, 30)
        world.get_location("-G-GG").access_rule = lambda state: needed_for_words(state, world, 2, 60, 2)
        world.get_location("-GG--").access_rule = lambda state: needed_for_words(state, world, 2, 30)
        world.get_location("-GG-G").access_rule = lambda state: needed_for_words(state, world, 2, 60, 2)
        world.get_location("-GGG-").access_rule = lambda state: needed_for_words(state, world, 2, 60, 2)
        world.get_location("-GGGG").access_rule = lambda state: needed_for_words(state, world, 3, 80, 3)
        world.get_location("G----").access_rule = lambda state: needed_for_words(state, world, 1, 20)
        world.get_location("G---G").access_rule = lambda state: needed_for_words(state, world, 2, 30)
        world.get_location("G--G-").access_rule = lambda state: needed_for_words(state, world, 2, 30)
        world.get_location("G--GG").access_rule = lambda state: needed_for_words(state, world, 2, 60, 2)
        world.get_location("G-G--").access_rule = lambda state: needed_for_words(state, world, 2, 30)
        world.get_location("G-G-G").access_rule = lambda state: needed_for_words(state, world, 2, 60, 2)
        world.get_location("G-GG-").access_rule = lambda state: needed_for_words(state, world, 2, 60, 2)
        world.get_location("G-GGG").access_rule = lambda state: needed_for_words(state, world, 3, 80, 3)
        world.get_location("GG---").access_rule = lambda state: needed_for_words(state, world, 2, 30)
        world.get_location("GG--G").access_rule = lambda state: needed_for_words(state, world, 2, 60, 2)
        world.get_location("GG-G-").access_rule = lambda state: needed_for_words(state, world, 2, 60, 2)
        world.get_location("GG-GG").access_rule = lambda state: needed_for_words(state, world, 3, 80, 3)
        world.get_location("GGG--").access_rule = lambda state: needed_for_words(state, world, 2, 60, 2)
        world.get_location("GGG-G").access_rule = lambda state: needed_for_words(state, world, 3, 80, 3)
        world.get_location("GGGG-").access_rule = lambda state: needed_for_words(state, world, 3, 80, 3)
        world.get_location("GGGGG").access_rule = lambda state: needed_for_words(state, world, 4, 100, 4, True)

    # Yellow positional checks
    if(world.options.yellow_checks == 1):
        world.get_location("----Y").access_rule = lambda state: needed_for_words(state, world, 1, 0, 1, True)
        world.get_location("---Y-").access_rule = lambda state: needed_for_words(state, world, 1, 0, 1, True)
        world.get_location("---YY").access_rule = lambda state: needed_for_words(state, world, 2, 30, 1, True)
        world.get_location("--Y--").access_rule = lambda state: needed_for_words(state, world, 1, 0, 1, True)
        world.get_location("--Y-Y").access_rule = lambda state: needed_for_words(state, world, 2, 30, 1, True)
        world.get_location("--YY-").access_rule = lambda state: needed_for_words(state, world, 2, 30, 1, True)
        world.get_location("--YYY").access_rule = lambda state: needed_for_words(state, world, 2, 60, 2, True)
        world.get_location("-Y---").access_rule = lambda state: needed_for_words(state, world, 1, 0, 1, True)
        world.get_location("-Y--Y").access_rule = lambda state: needed_for_words(state, world, 1, 0, 1, True)
        world.get_location("-Y-Y-").access_rule = lambda state: needed_for_words(state, world, 2, 30, 1, True)
        world.get_location("-Y-YY").access_rule = lambda state: needed_for_words(state, world, 2, 60, 2, True)
        world.get_location("-YY--").access_rule = lambda state: needed_for_words(state, world, 2, 30, 1, True)
        world.get_location("-YY-Y").access_rule = lambda state: needed_for_words(state, world, 2, 60, 2, True)
        world.get_location("-YYY-").access_rule = lambda state: needed_for_words(state, world, 2, 60, 2, True)
        world.get_location("-YYYY").access_rule = lambda state: needed_for_words(state, world, 3, 80, 2, True)
        world.get_location("Y----").access_rule = lambda state: needed_for_words(state, world, 1, 0, 1, True)
        world.get_location("Y---Y").access_rule = lambda state: needed_for_words(state, world, 1, 0, 1, True)
        world.get_location("Y--Y-").access_rule = lambda state: needed_for_words(state, world, 1, 0, 1, True)
        world.get_location("Y--YY").access_rule = lambda state: needed_for_words(state, world, 2, 30, 1, True)
        world.get_location("Y-Y--").access_rule = lambda state: needed_for_words(state, world, 2, 30, 1, True)
        world.get_location("Y-Y-Y").access_rule = lambda state: needed_for_words(state, world, 2, 60, 2, True)
        world.get_location("Y-YY-").access_rule = lambda state: needed_for_words(state, world, 2, 60, 2, True)
        world.get_location("Y-YYY").access_rule = lambda state: needed_for_words(state, world, 3, 80, 2, True)
        world.get_location("YY---").access_rule = lambda state: needed_for_words(state, world, 2, 30, 1, True)
        world.get_location("YY--Y").access_rule = lambda state: needed_for_words(state, world, 2, 30, 1, True)
        world.get_location("YY-Y-").access_rule = lambda state: needed_for_words(state, world, 2, 60, 2, True)
        world.get_location("YY-YY").access_rule = lambda state: needed_for_words(state, world, 3, 80, 2, True)
        world.get_location("YYY--").access_rule = lambda state: needed_for_words(state, world, 2, 60, 2, True)
        world.get_location("YYY-Y").access_rule = lambda state: needed_for_words(state, world, 3, 80, 2, True)
        world.get_location("YYYY-").access_rule = lambda state: needed_for_words(state, world, 3, 80, 2, True)
        world.get_location("YYYYY").access_rule = lambda state: needed_for_words(state, world, 4, 100, 4, True)
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
    
    if(world.options.green_checks == 1 or world.options.green_checks == 3):
        world.get_location("1 Correct Letter In Word").access_rule = lambda state: needed_for_words(state, world, 1, 0)
        world.get_location("2 Correct Letters In Word").access_rule = lambda state: needed_for_words(state, world, 2, 30)
        world.get_location("3 Correct Letters In Word").access_rule = lambda state: needed_for_words(state, world, 2, 60, 2)
        world.get_location("4 Correct Letters In Word").access_rule = lambda state: needed_for_words(state, world, 3, 80, 2)
        world.get_location("5 Correct Letters In Word").access_rule = lambda state: needed_for_words(state, world, 4, 100, 3, True)

    for i in range(world.options.words_to_win):
        world.get_location("Word " + str(i + 1)).access_rule = lambda state: needed_for_words(state, world, 4, 100, 3, True)