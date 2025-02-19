from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import WordipelagoWorld

def needed_for_words(state, world, vowels, consonants, guesses = 1, yellow = False):
    has_vowels = 0
    if(state.has("The Letter A", world.player)):
        has_vowels += 1
    if(state.has("The Letter E", world.player)):
        has_vowels += 1
    if(state.has("The Letter I", world.player)):
        has_vowels += 1
    if(state.has("The Letter O", world.player)):
        has_vowels += 1
    if(state.has("The Letter U", world.player)):
        has_vowels += 1
    if(state.has("The Letter Y", world.player)):
        has_vowels += 1

    has_strong_letters = 0
    if(state.has("The Letter B", world.player)):
        has_strong_letters += 1
    if(state.has("The Letter c", world.player)):
        has_strong_letters += 1
    if(state.has("The Letter D", world.player)):
        has_strong_letters += 1
    if(state.has("The Letter F", world.player)):
        has_strong_letters += 1
    if(state.has("The Letter G", world.player)):
        has_strong_letters += 1
    if(state.has("The Letter H", world.player)):
        has_strong_letters += 1
    if(state.has("The Letter J", world.player)):
        has_strong_letters += 1
    if(state.has("The Letter K", world.player)):
        has_strong_letters += 1
    if(state.has("The Letter L", world.player)):
        has_strong_letters += 1
    if(state.has("The Letter M", world.player)):
        has_strong_letters += 1
    if(state.has("The Letter N", world.player)):
        has_strong_letters += 1
    if(state.has("The Letter P", world.player)):
        has_strong_letters += 1
    if(state.has("The Letter Q", world.player)):
        has_strong_letters += 1
    if(state.has("The Letter R", world.player)):
        has_strong_letters += 1
    if(state.has("The Letter S", world.player)):
        has_strong_letters += 1
    if(state.has("The Letter T", world.player)):
        has_strong_letters += 1
    if(state.has("The Letter V", world.player)):
        has_strong_letters += 1
    if(state.has("The Letter W", world.player)):
        has_strong_letters += 1
    if(state.has("The Letter X", world.player)):
        has_strong_letters += 1
    if(state.has("The Letter Z", world.player)):
        has_strong_letters += 1

    return has_vowels >= vowels and has_strong_letters >= consonants and (not yellow or state.has('Yellow Letters', world.player)) and state.has('Guess', world.player, guesses - world.options.starting_guesses)

def create_rules(world: "WordipelagoWorld"):
    world.get_location("Used A").access_rule = lambda state: state.has("The Letter A", world.player)
    world.get_location("Used B").access_rule = lambda state: state.has("The Letter B", world.player)
    world.get_location("Used C").access_rule = lambda state: state.has("The Letter C", world.player)
    world.get_location("Used D").access_rule = lambda state: state.has("The Letter D", world.player)
    world.get_location("Used E").access_rule = lambda state: state.has("The Letter E", world.player)
    world.get_location("Used F").access_rule = lambda state: state.has("The Letter F", world.player)
    world.get_location("Used G").access_rule = lambda state: state.has("The Letter G", world.player)
    world.get_location("Used H").access_rule = lambda state: state.has("The Letter H", world.player)
    world.get_location("Used I").access_rule = lambda state: state.has("The Letter I", world.player)
    world.get_location("Used J").access_rule = lambda state: state.has("The Letter J", world.player)
    world.get_location("Used K").access_rule = lambda state: state.has("The Letter K", world.player)
    world.get_location("Used L").access_rule = lambda state: state.has("The Letter L", world.player)
    world.get_location("Used M").access_rule = lambda state: state.has("The Letter M", world.player)
    world.get_location("Used N").access_rule = lambda state: state.has("The Letter N", world.player)
    world.get_location("Used O").access_rule = lambda state: state.has("The Letter O", world.player)
    world.get_location("Used P").access_rule = lambda state: state.has("The Letter P", world.player)
    world.get_location("Used Q").access_rule = lambda state: state.has("The Letter Q", world.player)
    world.get_location("Used R").access_rule = lambda state: state.has("The Letter R", world.player)
    world.get_location("Used S").access_rule = lambda state: state.has("The Letter S", world.player)
    world.get_location("Used T").access_rule = lambda state: state.has("The Letter T", world.player)
    world.get_location("Used U").access_rule = lambda state: state.has("The Letter U", world.player)
    world.get_location("Used V").access_rule = lambda state: state.has("The Letter V", world.player)
    world.get_location("Used W").access_rule = lambda state: state.has("The Letter W", world.player)
    world.get_location("Used X").access_rule = lambda state: state.has("The Letter X", world.player)
    world.get_location("Used Y").access_rule = lambda state: state.has("The Letter Y", world.player)
    world.get_location("Used Z").access_rule = lambda state: state.has("The Letter Z", world.player)
    
    world.get_location("1 Correct Letter In Word").access_rule = lambda state: needed_for_words(state, world, 1, 0)
    world.get_location("2 Correct Letters In Word").access_rule = lambda state: needed_for_words(state, world, 2, 1)
    world.get_location("3 Correct Letters In Word").access_rule = lambda state: needed_for_words(state, world, 2, 4, 2)
    world.get_location("4 Correct Letters In Word").access_rule = lambda state: needed_for_words(state, world, 3, 7, 2)
    world.get_location("5 Correct Letters In Word").access_rule = lambda state: needed_for_words(state, world, 4, 9, 3, True)
    
    for i in range(world.options.words_to_win):
        world.get_location("Word " + str(i + 1)).access_rule = lambda state: needed_for_words(state, world, 4, 9, 3, True)