import math
from collections import Counter, defaultdict
from typing import List, Optional

from BaseClasses import MultiWorld

from worlds.generic.Rules import set_rule

from .YachtWeights import yacht_weights

# This module adds logic to the apworld.
# In short, we ran a simulation for every possible combination of dice and rolls you can have, per category.
# This simulation has a good strategy for locking dice.
# This gives rise to an approximate discrete distribution per category.
# We calculate the distribution of the total score.
# We then pick a correct percentile to reflect the correct score that should be in logic.
# The score is logic is *much* lower than the actual maximum reachable score.


class Category:
    def __init__(self, name, quantity=1):
        self.name = name
        self.quantity = quantity  # how many times you have the category

    # return mean score of a category
    def mean_score(self, num_dice, num_rolls):
        if num_dice <= 0 or num_rolls <= 0:
            return 0
        mean_score = 0
        for key, value in yacht_weights[self.name, min(8, num_dice), min(8, num_rolls)].items():
            mean_score += key * value / 100000
        return mean_score


class ListState:
    def __init__(self, state: List[str]):
        self.state = state
        self.item_counts = Counter(state)

    def count(self, item: str, player: Optional[str] = None) -> int:
        return self.item_counts[item]


def extract_progression(state, player, frags_per_dice, frags_per_roll, allowed_categories):
    """
    method to obtain a list of what items the player has.
    this includes categories, dice, rolls and score multiplier etc.
    First, we convert the state if it's a list, so we can use state.count(item, player)
    """
    if isinstance(state, list):
        state = ListState(state=state)

    number_of_dice = state.count("Dice", player) + state.count("Dice Fragment", player) // frags_per_dice
    number_of_rerolls = state.count("Roll", player) + state.count("Roll Fragment", player) // frags_per_roll
    number_of_fixed_mults = state.count("Fixed Score Multiplier", player)
    number_of_step_mults = state.count("Step Score Multiplier", player)

    categories = [
        Category(category_name, state.count(category_name, player))
        for category_name in allowed_categories
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


def dice_simulation_strings(categories, num_dice, num_rolls, fixed_mult, step_mult, diff, player):
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

    if player not in yachtdice_cache:
        yachtdice_cache[player] = {}

    if tup in yachtdice_cache[player]:
        return yachtdice_cache[player][tup]

    # sort categories because for the step multiplier, you will want low-scoring categories first
    # to avoid errors with order changing when obtaining rolls, we order assuming 4 rolls
    categories.sort(key=lambda category: category.mean_score(num_dice, 4))

    # function to add two discrete distribution.
    # defaultdict is a dict where you don't need to check if an id is present, you can just use += (lot faster)
    def add_distributions(dist1, dist2):
        combined_dist = defaultdict(float)
        for val2, prob2 in dist2.items():
            for val1, prob1 in dist1.items():
                combined_dist[val1 + val2] += prob1 * prob2
        return dict(combined_dist)

    # function to take the maximum of "times" i.i.d. dist1.
    # (I have tried using defaultdict here too but this made it slower.)
    def max_dist(dist1, mults):
        new_dist = {0: 1}
        for mult in mults:
            temp_dist = {}
            for val1, prob1 in new_dist.items():
                for val2, prob2 in dist1.items():
                    new_val = int(max(val1, val2 * mult))
                    new_prob = prob1 * prob2

                    # Update the probability for the new value
                    if new_val in temp_dist:
                        temp_dist[new_val] += new_prob
                    else:
                        temp_dist[new_val] = new_prob
            new_dist = temp_dist

        return new_dist

    # Returns percentile value of a distribution.
    def percentile_distribution(dist, percentile):
        sorted_values = sorted(dist.keys())
        cumulative_prob = 0

        for val in sorted_values:
            cumulative_prob += dist[val]
            if cumulative_prob >= percentile:
                return val

        # Return the last value if percentile is higher than all probabilities
        return sorted_values[-1]

    # parameters for logic.
    # perc_return is, per difficulty, the percentages of total score it returns (it averages out the values)
    # diff_divide determines how many shots the logic gets per category. Lower = more shots.
    perc_return = [[0], [0.1, 0.5], [0.3, 0.7], [0.55, 0.85], [0.85, 0.95]][diff]
    diff_divide = [0, 9, 7, 3, 2][diff]

    # calculate total distribution
    total_dist = {0: 1}
    for j, category in enumerate(categories):
        if num_dice <= 0 or num_rolls <= 0:
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

    # save result into the cache, then return it
    outcome = sum([percentile_distribution(total_dist, perc) for perc in perc_return]) / len(perc_return)
    yachtdice_cache[player][tup] = max(5, math.floor(outcome))  # at least 5.

    # cache management; we rarely/never need more than 400 entries. But if for some reason it became large,
    # delete the first entry of the player cache.
    if len(yachtdice_cache[player]) > 400:
        # Remove the oldest item
        oldest_tup = next(iter(yachtdice_cache[player]))
        del yachtdice_cache[player][oldest_tup]

    return yachtdice_cache[player][tup]


def dice_simulation_fill_pool(state, frags_per_dice, frags_per_roll, allowed_categories, difficulty, player):
    """
    Returns the feasible score that one can reach with the current state, options and difficulty.
    This function is called with state being a list, during filling of item pool.
    """
    categories, num_dice, num_rolls, fixed_mult, step_mult, expoints = extract_progression(
        state, "state_is_a_list", frags_per_dice, frags_per_roll, allowed_categories
    )
    return (
        dice_simulation_strings(categories, num_dice, num_rolls, fixed_mult, step_mult, difficulty, player) + expoints
    )


def dice_simulation_state_change(state, player, frags_per_dice, frags_per_roll, allowed_categories, difficulty):
    """
    Returns the feasible score that one can reach with the current state, options and difficulty.
    This function is called with state being a AP state object, while doing access rules.
    """

    if state.prog_items[player]["state_is_fresh"] == 0:
        state.prog_items[player]["state_is_fresh"] = 1
        categories, num_dice, num_rolls, fixed_mult, step_mult, expoints = extract_progression(
            state, player, frags_per_dice, frags_per_roll, allowed_categories
        )
        state.prog_items[player]["maximum_achievable_score"] = (
            dice_simulation_strings(categories, num_dice, num_rolls, fixed_mult, step_mult, difficulty, player)
            + expoints
        )

    return state.prog_items[player]["maximum_achievable_score"]


def set_yacht_rules(world: MultiWorld, player: int, frags_per_dice, frags_per_roll, allowed_categories, difficulty):
    """
    Sets rules on reaching scores
    """

    for location in world.get_locations(player):
        set_rule(
            location,
            lambda state, curscore=location.yacht_dice_score, player=player: dice_simulation_state_change(
                state, player, frags_per_dice, frags_per_roll, allowed_categories, difficulty
            )
            >= curscore,
        )


def set_yacht_completion_rules(world: MultiWorld, player: int):
    """
    Sets rules on completion condition
    """
    world.completion_condition[player] = lambda state: state.has("Victory", player)
