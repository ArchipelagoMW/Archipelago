import copy
import random
import typing
from .Hint import Hint
from .HintStringLibrary import HintStringLibrary
class HintLibrary:

    class Type:
        FILLER = 1
        TRAP = 2
        PROGRESSIVE = 3

    def __init__(self):
        self.filler: typing.Dict[int,Hint] = dict()
        self.trap: typing.Dict[int, Hint] = dict()
        self.progressive: typing.Dict[int, Hint] = dict()


    def add(self, hint: Hint, type: Type):
        if type == HintLibrary.Type.FILLER:
            self.filler[len(self.filler)] = hint
        if type == HintLibrary.Type.TRAP:
            self.trap[len(self.trap)] = hint
        else:
            self.progressive[len(self.progressive)] = hint

    def getStringLibrary(self, ran: random.Random) -> HintStringLibrary:
        sl: HintStringLibrary = HintStringLibrary(ran)
        for k in self.filler.keys():
            sl.add(self.filler[k], 1)
        for k in self.trap.keys():
            sl.add(self.trap[k], 2)
        for k in self.progressive.keys():
            sl.add(self.progressive[k], 3)

        return sl