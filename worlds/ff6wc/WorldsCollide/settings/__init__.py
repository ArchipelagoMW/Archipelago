from ..settings.initial_spells import InitialSpells
from ..settings.movement import Movement
from ..settings.random_rng import RandomRNG
from ..settings.permadeath import Permadeath
from ..settings.y_npc import YNPC
from ..settings.config import Config

from ..memory.space import Reserve
from ..instruction import asm as asm

__all__ = ["Settings"]
class Settings:
    def __init__(self):
        self.initial_spells = InitialSpells()
        self.movement = Movement()
        self.random_rng = RandomRNG()
        self.permadeath = Permadeath()
        self.y_npc = YNPC()
        self.config = Config()

        # do not auto load save file after game over
        space = Reserve(0x00c4fe, 0x00c500, "load where to return to after game over", asm.NOP())
        space.write(
            asm.LDA(0xff, asm.IMM8), # do not auto load save file after game over
        )

        space = Reserve(0x2e8393, 0x2e8393, "wor overworld song")
        space.write(0x4c) # change from dark world to searching for friends
