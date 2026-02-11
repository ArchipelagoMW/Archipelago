from typing import TYPE_CHECKING
from BaseClasses import LocationProgressType
from worlds.generic.Rules import set_rule
from .logicrules import letter_scores, rule_logic

if TYPE_CHECKING:
    from . import WordipelagoWorld

def end_game_event_check(state, world):
    win_condition = world.options.win_condition.value
    if(win_condition == 0):
        return state.has(str(world.options.word_checks) + ' Words', world.player)
    if(win_condition == 1):
        return state.has(str(world.options.word_streak_checks) + ' Streaks', world.player)
    if(win_condition == 2):
        return state.has(str(world.options.word_checks) + " Words", world.player) and state.has(str(world.options.word_streak_checks) + ' Streaks', world.player)

def all_needed_locations_checked(state, player):
    return state.has("Word Master", player)

alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

def needed_for_words(state, player, vowels, score, guesses = 1, yellow = False, min_letters = 1):
    possible_score = 0
    vowels_items = ["Letter A", "Letter E", "Letter I", "Letter O", "Letter U", "Letter Y"]
    letter_count = 0
    for key in alphabet:
        if(state.has("Letter " + key, player)):
            letter_count += 1
            possible_score += letter_scores["Letter " + key]

    return state.has_from_list_unique(vowels_items, player, vowels) and possible_score >= score and (not yellow or state.has('Yellow Letters', player)) and state.has('Guess', player, guesses) and min_letters <= letter_count

def needed_for_letter(state, player, letter):
    return state.has("Letter " + letter, player)
    
def create_rules(world: "WordipelagoWorld"):
    multiworld = world.multiworld
    player = world.player
    rules_for_difficulty = rule_logic[world.options.logic_difficulty.value]

    multiworld.get_region("Menu", player).add_exits(['Letters'])
    multiworld.get_region("Letters", player).add_exits(
        [ "Word Best", "Green Checks", "Yellow Checks", 'Point Shop'],
        {"Point Shop": lambda state: needed_for_words(state, world.player, *(rules_for_difficulty["green"][str(world.options.point_shop_logic_level.value)]))}
    )
    
    multiworld.get_region("Green Checks", player).add_exits(
        ['Green Checks 1'],
        {"Green Checks 1": lambda state: needed_for_words(state, world.player, *(rules_for_difficulty["green"]["1"]))}
    )
    multiworld.get_region("Green Checks 1", player).add_exits(
        ['Green Checks 2'],
        {"Green Checks 2": lambda state: needed_for_words(state, world.player, *(rules_for_difficulty["green"]["2"]))}
    )
    multiworld.get_region("Green Checks 2", player).add_exits(
        ['Green Checks 3'],
        {"Green Checks 3": lambda state: needed_for_words(state, world.player, *(rules_for_difficulty["green"]["3"]))}
    )
    multiworld.get_region("Green Checks 3", player).add_exits(
        ['Green Checks 4'],
        {
            "Green Checks 4": lambda state: needed_for_words(state, world.player, *(rules_for_difficulty["green"]["4"])),
        }
    )
    multiworld.get_region("Green Checks 4", player).add_exits(
        ['Green Checks 5'],
        {"Green Checks 5": lambda state: needed_for_words(state, world.player, *(rules_for_difficulty["green"]["5"]))}
    )
    multiworld.get_region("Green Checks 5", player).add_exits(
        ['Words', 'Streaks', 'Words Chunk 1', 'Streaks Chunk 1']
    )
    # Word Chunks
    multiworld.get_region("Words Chunk 1", player).add_exits(
        ['Words Chunk 2'],
        {"Words Chunk 2": lambda state: state.has(str((world.options.word_checks // 5 + (world.options.word_checks % 5 > 0) ) * 1) + ' Words', player)}
    )
    multiworld.get_region("Words Chunk 2", player).add_exits(
        ['Words Chunk 3'],
        {"Words Chunk 3": lambda state: state.has(str((world.options.word_checks // 5 + (world.options.word_checks % 5 > 0) ) * 2) + ' Words', player)}
    )
    multiworld.get_region("Words Chunk 3", player).add_exits(
        ['Words Chunk 4'],
        {"Words Chunk 4": lambda state: state.has(str((world.options.word_checks // 5 + (world.options.word_checks % 5 > 0) ) * 3) + ' Words', player)}
    )
    multiworld.get_region("Words Chunk 4", player).add_exits(
        ['Words Chunk 5'],
        {"Words Chunk 5": lambda state: state.has(str((world.options.word_checks // 5 + (world.options.word_checks % 5 > 0) ) * 4) + ' Words', player)}
    )
    
    # Streak Chunks
    multiworld.get_region("Streaks Chunk 1", player).add_exits(
        ['Streaks Chunk 2'],
        {"Streaks Chunk 2": lambda state: state.has(str((world.options.word_streak_checks // 5 + (world.options.word_streak_checks % 5 > 0) ) * 1) + ' Streaks', player)}
    )
    multiworld.get_region("Streaks Chunk 2", player).add_exits(
        ['Streaks Chunk 3'],
        {"Streaks Chunk 3": lambda state: state.has(str((world.options.word_streak_checks // 5 + (world.options.word_streak_checks % 5 > 0) ) * 2) + ' Streaks', player)}
    )
    multiworld.get_region("Streaks Chunk 3", player).add_exits(
        ['Streaks Chunk 4'],
        {"Streaks Chunk 4": lambda state: state.has(str((world.options.word_streak_checks // 5 + (world.options.word_streak_checks % 5 > 0) ) * 3) + ' Streaks', player)}
    )
    multiworld.get_region("Streaks Chunk 4", player).add_exits(
        ['Streaks Chunk 5'],
        {"Streaks Chunk 5": lambda state: state.has(str((world.options.word_streak_checks // 5 + (world.options.word_streak_checks % 5 > 0) ) * 4) + ' Streaks', player)}
    )

    multiworld.get_region("Yellow Checks", player).add_exits(
        ['Yellow Checks 1'],
        {"Yellow Checks 1": lambda state: needed_for_words(state, world.player, *(rules_for_difficulty["yellow"]["1"]), 2)}
    )
    multiworld.get_region("Yellow Checks 1", player).add_exits(
        ['Yellow Checks 2'],
        {"Yellow Checks 2": lambda state: needed_for_words(state, world.player, *(rules_for_difficulty["yellow"]["2"]))}
    )
    multiworld.get_region("Yellow Checks 2", player).add_exits(
        ['Yellow Checks 3'],
        {"Yellow Checks 3": lambda state: needed_for_words(state, world.player, *(rules_for_difficulty["yellow"]["3"]))}
    )
    multiworld.get_region("Yellow Checks 3", player).add_exits(
        ['Yellow Checks 4'],
        {"Yellow Checks 4": lambda state: needed_for_words(state, world.player, *(rules_for_difficulty["yellow"]["4"]))}
    )
    multiworld.get_region("Yellow Checks 4", player).add_exits(
        ['Yellow Checks 5'],
        {"Yellow Checks 5": lambda state: needed_for_words(state, world.player, *(rules_for_difficulty["yellow"]["5"]))}
    )
    
    letter_checks = []
    if(world.options.letter_checks >= 1):
        letter_checks = [*letter_checks, "A", "E", "I", "O", "U", "Y"]
    if(world.options.letter_checks >= 2):
        letter_checks = [*letter_checks, "B", "C", "D", "F", "G", "H", "L", "M", "N", "P", "R", "S", "T"]  
    if(world.options.letter_checks == 3):
        letter_checks = [*letter_checks, "V", "W", "X", "Z", "Q", "J", "K"]
        
    for key in letter_checks:
        world.get_location("Used " + key).access_rule = lambda state, world=world, key=key: needed_for_letter(state, world.player, key)
        world.get_location("Used " + key).item_rule = lambda item, key=key: item.name != "Letter " + key
        
    for shop_check in range(world.options.minimum_point_shop_checks):
        # if(shop_check % 2 == 0 and shop_check <= 10):
        #     world.get_location("Point Shop Purchase " + str(shop_check + 1)).progress_type = LocationProgressType.PRIORITY
        # else:
        world.get_location("Point Shop Purchase " + str(shop_check + 1)).item_rule =  lambda item: item.name != 'Shop Points'

    if(world.options.yellow_checks.value == 1):
        
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
        
    # Events
    world.get_location('Goal Event Location').access_rule = lambda state, world=world: end_game_event_check(state, world)
    

    world.multiworld.completion_condition[world.player] = lambda state, world=world: all_needed_locations_checked(state, world.player)