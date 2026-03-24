from random import Random


class LoggingRandom:
    internal_random: Random
    total_calls: int

    def __init__(self, seed):
        # logger.warning(f"Initializing LoggingRandom with seed: {seed}")
        self.internal_random = Random(seed)
        self.total_calls = 0

    def sample(self, population, k, *, counts=None):
        self.total_calls += 1
        return self.internal_random.sample(population=population, k=k, counts=counts)

    def choice(self, seq):
        self.total_calls += 1
        return self.internal_random.choice(seq)

    def choices(self, population, weights=None, *, cum_weights=None, k=1):
        self.total_calls += 1
        return self.internal_random.choices(population=population, weights=weights, cum_weights=cum_weights)

    def randint(self, a, b):
        self.total_calls += 1
        return self.internal_random.randint(a, b)

    def shuffle(self, x):
        self.total_calls += 1
        return self.internal_random.shuffle(x)

    def randrange(self, start, stop=None, step=1):
        self.total_calls += 1
        return self.internal_random.randrange(start=start, stop=stop, step=step)