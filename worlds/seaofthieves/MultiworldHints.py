
from .Hint import Hint, hint_from_location
import typing
from BaseClasses import CollectionState, Item, Location, LocationProgressType, MultiWorld, ItemClassification
import random

class MultiworldHints:

    def __init__(self, multiworld: MultiWorld, player: int, rand: random.Random, hint_limit: int = 1000):
        self.generalHints: typing.Dict[int, str] = {}
        self.personalProgressiveHints: typing.Dict[int, str] = {}

        self.populateAllHintTypes(multiworld, player, rand, hint_limit)
        pass

    def populateAllHintTypes(self, multiworld: MultiWorld, player: int, rand: random.Random, hintLimit: int = 1000):
        self.populateGeneralHints(multiworld, player, rand, hintLimit)
        self.populateProgressionHints(multiworld, player, rand, hintLimit)

    def populateGeneralHints(self, multiworld: MultiWorld, player: int, rand: random.Random, hintLimit: int = 1000):
        cnt: int = 0
        for sphere in multiworld.get_spheres():
            for sphere_location in sphere:
                if sphere_location.player == player:
                    if len(self.generalHints) >= hintLimit:
                        return
                    ret = hint_from_location(sphere_location).get(rand)
                    self.generalHints[cnt] = ret
                    cnt += 1


    def populateProgressionHints(self, multiworld: MultiWorld, player: int, rand: random.Random, hintLimit: int = 1000):
        cnt: int = 0
        for sphere in multiworld.get_spheres():
            for sphere_location in sphere:
                if sphere_location.player == player and sphere_location.item.classification == ItemClassification.progression:
                    if len(self.personalProgressiveHints) >= hintLimit:
                        return
                    self.personalProgressiveHints[cnt] = hint_from_location(sphere_location).get(rand)
                    cnt += 1
