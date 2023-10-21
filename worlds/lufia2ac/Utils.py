import itertools
from operator import itemgetter
from random import Random
from typing import Dict, Iterable, List, MutableSequence, Sequence, Set, Tuple


def constrained_choices(population: Sequence[int], d: int, *, k: int, random: Random) -> List[int]:
    n: int = len(population)
    constraints: Dict[int, Tuple[int, ...]] = {
        i: tuple(dict.fromkeys(population[j] for j in range(max(0, i - d), min(i + d + 1, n)))) for i in range(n)
    }

    return [random.choice(constraints[i]) for i in range(k)]


def constrained_shuffle(x: MutableSequence[int], d: int, random: Random) -> None:
    n: int = len(x)
    constraints: Dict[int, Set[int]] = {i: set(x[j] for j in range(max(0, i - d), min(i + d + 1, n))) for i in range(n)}

    for _ in range(d * n * n):
        i, j = random.randrange(n), random.randrange(n)
        if x[i] in constraints[j] and x[j] in constraints[i]:
            x[i], x[j] = x[j], x[i]


def weighted_sample(population: Iterable[int], weights: Iterable[float], k: int, *, random: Random) -> List[int]:
    population, keys = zip(*((item, pow(random.random(), 1 / group_weight))
                             for item, group in itertools.groupby(sorted(zip(population, weights)), key=itemgetter(0))
                             if (group_weight := sum(weight for _, weight in group))))
    return sorted(population, key=dict(zip(population, keys)).__getitem__)[-k:]
