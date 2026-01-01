from .droppedKey import DroppedKey
from .constants import *


class FishingMinigame(DroppedKey):
    def __init__(self):
        super().__init__(0x2B1)

    def configure(self, options):
        if options.heartpiece:
            super().configure(options)
        else:
            self.OPTIONS = [HEART_PIECE]
