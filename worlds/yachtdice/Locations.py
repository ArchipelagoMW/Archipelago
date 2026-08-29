import typing

from BaseClasses import Location


class LocData(typing.NamedTuple):
    id: int
    region: str
    score: int


class YachtDiceLocation(Location):
    game: str = "Yacht Dice"

    def __init__(self, player: int, name: str, score: int, address: typing.Optional[int], parent):
        super().__init__(player, name, address, parent)
        self.yacht_dice_score = score


all_locations = {}
starting_index = 16871244500  # 500 more than the starting index for items (not necessary, but this is what it is now)


def all_locations_fun(max_score):
    """
    Function that is called when this file is loaded, which loads in ALL possible locations, score 1 to 1000
    """
    return {f"{i} score": LocData(starting_index + i, "Board", i) for i in range(1, max_score + 1)}


def ini_locations(goal_score, max_score, number_of_locations, dif, skip_early_locations, number_of_players):
    """
    function that loads in all locations necessary for the game, so based on options.
    will make sure that goal_score and max_score are included locations
    """
    scaling = 2  # parameter that determines how many low-score location there are.
    # need more low-score locations or lower difficulties:
    if dif == 1:
        scaling = 3
    elif dif == 2:
        scaling = 2.3

    scores = []
    # the scores follow the function int( 1 + (percentage ** scaling) * (max_score-1) )
    # however, this will have many low values, sometimes repeating.
    # to avoid repeating scores, highest_score keeps tracks of the highest score location
    # and the next score will always be at least highest_score + 1
    # note that current_score is at most max_score-1
    highest_score = 0
    start_score = 0

    if skip_early_locations:
        scaling = 1.95
        if number_of_players > 2:
            scaling = max(1.2, 2.2 - number_of_players * 0.1)

    for i in range(number_of_locations - 1):
        percentage = i / number_of_locations
        current_score = int(start_score + 1 + (percentage**scaling) * (max_score - start_score - 2))
        if current_score <= highest_score:
            current_score = highest_score + 1
        highest_score = current_score
        scores += [current_score]

    if goal_score != max_score:
        # if the goal score is not in the list, find the closest one and make it the goal.
        if goal_score not in scores:
            closest_num = min(scores, key=lambda x: abs(x - goal_score))
            scores[scores.index(closest_num)] = goal_score

    scores += [max_score]

    location_table = {f"{score} score": LocData(starting_index + score, "Board", score) for score in scores}

    return location_table


# we need to run this function to initialize all scores from 1 to 1000, even though not all are used
all_locations = all_locations_fun(1000)
