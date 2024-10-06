import random
import typing
from .Hint import Hint
class HintStringLibrary:

    def __init__(self, ran: random.Random):
        self.filler: typing.Dict[int,str] = dict()
        self.trap: typing.Dict[int, str] = dict()
        self.progressive: typing.Dict[int, str] = dict()
        self.ran: random.Random = ran

    def add(self, hint: Hint, type: int):
        if type == 1:
            self.filler[len(self.filler)] = hint.get(self.ran)
        if type == 2:
            self.trap[len(self.trap)] = hint.get(self.ran)
        else:
            self.progressive[len(self.progressive)] = hint.get(self.ran)