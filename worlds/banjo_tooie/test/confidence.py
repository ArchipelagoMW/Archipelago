"""
    This function can be used to test world.random.choices
    Don't use this directly in tests, instead, you can run it locally to make sure the generated numbers
    make sense.
"""

import math


def count_confidence_interval(weights, N, z=3.48076):
    """
    Computes the confidence interval for the counts of each item in a weighted random selection process.

    Parameters:
        weights (dict): A dictionary where keys are item names and values are their weights.
        N (int): The total number of selections.
        z (float): The z score (default to the z score for a confidence of 99.9%).

    Returns:
        dict: A dictionary where keys are items and values are (lower_bound, upper_bound) tuples.

    Remarks:
        You can find z by: sqrt(2) * inverfc((1 - <confidence>)/2)
    """

    total_weight = sum(weights.values())
    probabilities = {item: w / total_weight for item, w in weights.items()}

    intervals = {}
    for item, p in probabilities.items():
        mu = N * p
        sigma = math.sqrt(N * p * (1 - p))
        lower_bound = max(0, mu - z * sigma)  # Counts cannot be negative
        upper_bound = min(N, mu + z * sigma)  # Counts cannot exceed N
        intervals[item] = (round(lower_bound), round(upper_bound))

    return intervals


# Example usage:
weights = {
        "egg_nests_weight": 1,
        "feather_nests_weight": 1,
}
N = 687 - 30
confidence_intervals = count_confidence_interval(weights, N)
