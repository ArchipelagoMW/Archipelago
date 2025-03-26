from typing import Callable, Dict, List, NamedTuple
from BaseClasses import CollectionState


class WordipelagoRegionData(NamedTuple):
    connecting_regions: List[str] = []
    rules: Dict[str, Callable[[CollectionState], bool]] = None

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


region_data_table: Dict[str, WordipelagoRegionData] = {
    "Menu": WordipelagoRegionData(["Letters"]),
    "Letters": WordipelagoRegionData(
        [ "Word Best", "Green Checks", "Yellow Checks"]
    ),
    "Words": WordipelagoRegionData([]),
    "Green Checks": WordipelagoRegionData(
        ["Green Checks 1"]
    ),
    "Green Checks 1": WordipelagoRegionData(
        ["Green Checks 2"]
    ),
    "Green Checks 2": WordipelagoRegionData(
        ["Green Checks 3"]
    ),
    "Green Checks 3": WordipelagoRegionData(
        ["Green Checks 4"]
    ),
    "Green Checks 4": WordipelagoRegionData(
        ["Green Checks 5"]
    ),
    "Green Checks 5": WordipelagoRegionData(["Words"]),
    "Yellow Checks": WordipelagoRegionData(
        ["Yellow Checks 1"]
    ),
    "Yellow Checks 1": WordipelagoRegionData(
        ["Yellow Checks 2"]
    ),
    "Yellow Checks 2": WordipelagoRegionData(
        ["Yellow Checks 3"]
    ),
    "Yellow Checks 3": WordipelagoRegionData(
        ["Yellow Checks 4"]
    ),
    "Yellow Checks 4": WordipelagoRegionData(
        ["Yellow Checks 5"]
    ),
    "Yellow Checks 5": WordipelagoRegionData([]),
    "Word Best": WordipelagoRegionData([]),
}
