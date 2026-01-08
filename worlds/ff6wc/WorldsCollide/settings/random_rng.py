from ..memory.space import Reserve
from ..instruction import asm as asm
from .. import args as args

class RandomRNG:
    def __init__(self):
        if args.random_rng:
            self.mod()

    def mod(self):
        import random
        rng_table = list(range(256))
        random.shuffle(rng_table)

        space = Reserve(0x0fd00, 0x0fdff, "rng table")
        space.write(rng_table)
