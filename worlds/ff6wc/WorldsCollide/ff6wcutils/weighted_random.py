# https://eli.thegreenplace.net/2010/01/22/weighted-random-generation-in-python/
def weighted_random(weights):
    import random
    rnd = random.random() * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return i
