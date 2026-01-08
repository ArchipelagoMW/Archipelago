from .droppedKey import DroppedKey
from .items import *


class HeartPiece(DroppedKey):
    # Due to the patches a heartPiece acts like a dropped key.

    def configure(self, options):
        if options.heartpiece:
            super().configure(options)
        else:
            self.OPTIONS = [HEART_PIECE]
