import math
from collections import Counter, defaultdict
from typing import List, Optional

from BaseClasses import MultiWorld

from worlds.generic.Rules import set_rule

from .YachtWeights import yacht_weights
import numpy as np


# This module adds logic to the apworld.
# In short, we ran a simulation for every possible combination of dice and rolls you can have, per category.
# This simulation has a good strategy for locking dice.
# This gives rise to an approximate discrete distribution per category.
# We calculate the distribution of the total score.
# We then pick a correct percentile to reflect the correct score that should be in logic.
# The score is logic is *much* lower than the actual maximum reachable score.

# List of categories, and the name of the logic class associated with it
category_mappings = {
    "Category Ones": "Ones",
    "Category Twos": "Twos",
    "Category Threes": "Threes",
    "Category Fours": "Fours",
    "Category Fives": "Fives",
    "Category Sixes": "Sixes",
    "Category Choice": "Choice",
    "Category Inverse Choice": "Choice",
    "Category Pair": "Pair",
    "Category Three of a Kind": "ThreeOfAKind",
    "Category Four of a Kind": "FourOfAKind",
    "Category Tiny Straight": "TinyStraight",
    "Category Small Straight": "SmallStraight",
    "Category Large Straight": "LargeStraight",
    "Category Full House": "FullHouse",
    "Category Yacht": "Yacht",
    "Category Distincts": "Distincts",
    "Category Two times Ones": "Twos",  # same weights as twos category
    "Category Half of Sixes": "Threes",  # same weights as threes category
    "Category Twos and Threes": "TwosAndThrees",
    "Category Sum of Odds": "SumOfOdds",
    "Category Sum of Evens": "SumOfEvens",
    "Category Double Threes and Fours": "DoubleThreesAndFours",
    "Category Quadruple Ones and Twos": "QuadrupleOnesAndTwos",
    "Category Micro Straight": "MicroStraight",
    "Category Three Odds": "ThreeOdds",
    "Category 1-2-1 Consecutive": "OneTwoOneConsecutive",
    "Category Three Distinct Dice": "ThreeDistinctDice",
    "Category Two Pair": "TwoPair",
    "Category 2-1-2 Consecutive": "TwoOneTwoConsecutive",
    "Category Five Distinct Dice": "FiveDistinctDice",
    "Category 4&5 Full House": "FourAndFiveFullHouse",
}


class Category:
    def __init__(self, name, quantity=1):
        self.name = name
        self.quantity = quantity  # how many times you have the category

    # return mean score of a category
    def mean_score(self, num_dice, num_rolls):
        if num_dice == 0 or num_rolls == 0:
            return 0
        mean_score = 0
        for key, value in yacht_weights[self.name, min(8, num_dice), min(8, num_rolls)].items():
            mean_score += key * value / 100000
        return mean_score * self.quantity


class ListState:
    def __init__(self, state: List[str]):
        self.state = state
        self.item_counts = Counter(state)

    def count(self, item: str, player: Optional[str] = None) -> int:
        return self.item_counts[item]


def extract_progression(state, player, options):
    """
    method to obtain a list of what items the player has.
    this includes categories, dice, rolls and score multiplier etc.
    First, we convert the state if it's a list, so we can use state.count(item, player)
    """
    if isinstance(state, list):
        state = ListState(state=state)

    number_of_dice = (
        state.count("Dice", player)
        + state.count("Dice Fragment", player) // options.number_of_dice_fragments_per_dice.value
    )
    number_of_rerolls = (
        state.count("Roll", player)
        + state.count("Roll Fragment", player) // options.number_of_roll_fragments_per_roll.value
    )
    number_of_fixed_mults = state.count("Fixed Score Multiplier", player)
    number_of_step_mults = state.count("Step Score Multiplier", player)

    categories = [
        Category(category_value, state.count(category_name, player))
        for category_name, category_value in category_mappings.items()
        if state.count(category_name, player)  # want all categories that have count >= 1
    ]

    extra_points_in_logic = state.count("1 Point", player)
    extra_points_in_logic += state.count("10 Points", player) * 10
    extra_points_in_logic += state.count("100 Points", player) * 100

    return (
        categories,
        number_of_dice,
        number_of_rerolls,
        number_of_fixed_mults * 0.1,
        number_of_step_mults * 0.01,
        extra_points_in_logic,
    )


# We will store the results of this function as it is called often for the same parameters.


yachtdice_cache = {}


def dice_simulation_strings(categories, num_dice, num_rolls, fixed_mult, step_mult, diff):
    """
    Function that returns the feasible score in logic based on items obtained.
    """
    tup = (
        tuple([c.name + str(c.quantity) for c in categories]),
        num_dice,
        num_rolls,
        fixed_mult,
        step_mult,
        diff,
    )  # identifier

    # if already computed, return the result
    if tup in yachtdice_cache:
        return yachtdice_cache[tup]

    # sort categories because for the step multiplier, you will want low-scoring categories first
    categories.sort(key=lambda category: category.mean_score(num_dice, num_rolls))

    # we have two ways to store a distribution (example, 0 with probability 0.4, 10 with probability 0.6):
    # dict: {0: 0.4, 10: 0.6}
    # pmf (probability mass function): [0.4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.6] (numpy array)
    # adding two distributions works fast with pmf's and numpy's convolve method.
    # maximizing two distributions (with multipliers) seems to work fastest with dictionaries.

    def dict_to_pmf(dist):
        """
        Convert dict-distribution to pmf-distribution
        """
        max_value = max(dist) + 1
        return np.array([dist.get(i, 0) for i in range(max_value)])

    def pmf_to_dict(pmf):
        """
        Convert pmf-distribution to dict-distribution
        """
        sum_values = np.arange(0, len(pmf) + 1)
        sum_dist = {v: p for v, p in zip(sum_values, pmf)}
        return sum_dist

    def add_distributions(pmf1, dic2):
        """
        function to add two discrete distributions. The first in pmf form, the second in dict form, returns pmf.
        """
        pmf2 = dict_to_pmf(dic2)

        # Sum the two distributions using convolution
        sum_pmf = np.convolve(pmf1, pmf2)

        return sum_pmf

    def max_dist(dist1, mults):
        """
        function to take the maximum of "times" i.i.d. dist1.
        dist1 is a dict-distribution
        (I have tried using defaultdict here too but this made it slower.)
        """
        new_dist = {0: 1}
        for mult in mults:
            c = new_dist.copy()
            new_dist = {}
            for val1, prob1 in c.items():
                for val2, prob2 in dist1.items():
                    new_val = int(max(val1, val2 * mult))
                    new_prob = prob1 * prob2

                    # Update the probability for the new value
                    if new_val in new_dist:
                        new_dist[new_val] += new_prob
                    else:
                        new_dist[new_val] = new_prob

        return new_dist

    # Returns percentile value of a distribution.
    def percentile_distribution(dist, percentile):
        cumdist = np.cumsum(dist)

        # Return the last value if percentile is higher than all probabilities
        return np.argmax(cumdist > percentile)

    # parameters for logic.
    # perc_return is, per difficulty, the percentages of total score it returns (it averages out the values)
    # diff_divide determines how many shots the logic gets per category. Lower = more shots.
    perc_return = [[0], [0.1, 0.5], [0.3, 0.7], [0.55, 0.85], [0.85, 0.95]][diff]
    diff_divide = [0, 9, 7, 3, 2][diff]

    # calculate total distribution, start in pmf-form
    total_dist = [1]
    for j, category in enumerate(categories):
        if num_dice == 0 or num_rolls == 0:
            dist = {0: 100000}
        else:
            dist = yacht_weights[category.name, min(8, num_dice), min(8, num_rolls)].copy()

        for key in dist.keys():
            dist[key] /= 100000

        cat_mult = 2 ** (category.quantity - 1)

        # for higher difficulties, the simulation gets multiple tries for categories.
        max_tries = j // diff_divide
        mults = [(1 + fixed_mult + step_mult * ii) * cat_mult for ii in range(max(0, j - max_tries), j + 1)]
        dist = max_dist(dist, mults)

        total_dist = add_distributions(total_dist, dist)

    # note, total_dist is in pmf-form
    outcome = sum([percentile_distribution(total_dist, perc) for perc in perc_return]) / len(perc_return)
    # save result into the cache, then return it
    yachtdice_cache[tup] = max(5, math.floor(outcome))  # at least 5.

    return yachtdice_cache[tup]


def dice_simulation(state, player, options):
    """
    Returns the feasible score that one can reach with the current state, options and difficulty.
    """
    # if the player is called "state_is_a_list", we are filling the itempool and want to calculate anyways.
    if player == "state_is_a_list":
        categories, num_dice, num_rolls, fixed_mult, step_mult, expoints = extract_progression(state, player, options)
        return (
            dice_simulation_strings(
                categories, num_dice, num_rolls, fixed_mult, step_mult, options.game_difficulty.value
            )
            + expoints
        )

    if state.prog_items[player]["state_is_fresh"] == 0:
        state.prog_items[player]["state_is_fresh"] = 1
        categories, num_dice, num_rolls, fixed_mult, step_mult, expoints = extract_progression(state, player, options)
        state.prog_items[player]["maximum_achievable_score"] = (
            dice_simulation_strings(
                categories, num_dice, num_rolls, fixed_mult, step_mult, options.game_difficulty.value
            )
            + expoints
        )

    return state.prog_items[player]["maximum_achievable_score"]


def set_yacht_rules(world: MultiWorld, player: int, options):
    """
    Sets rules on entrances and advancements that are always applied
    """

    for location in world.get_locations(player):
        set_rule(
            location,
            lambda state, curscore=location.yacht_dice_score, player=player: dice_simulation(state, player, options)
            >= curscore,
        )


def set_yacht_completion_rules(world: MultiWorld, player: int):
    """
    Sets rules on completion condition
    """
    world.completion_condition[player] = lambda state: state.has("Victory", player)
