# not a "real" distribution, the discretization and clamping skew it
def truncated_discrete_distribution(mean, stddev, minimum = None, maximum = None):
    import random
    result = round(random.gauss(mean, stddev))
    if minimum and result < minimum:
        return truncated_discrete_distribution(mean, stddev, minimum, maximum)
    if maximum and result > maximum:
        return truncated_discrete_distribution(mean, stddev, minimum, maximum)
    return result
