from .droppedKey import DroppedKey
from .items import *


class Seashell(DroppedKey):
    # Thanks to patches, a seashell is just a dropped key as far as the randomizer is concerned.

    def configure(self, options):
        if not options.seashells:
            self.OPTIONS = [SEASHELL]


class SeashellMansion(DroppedKey):
    pass
