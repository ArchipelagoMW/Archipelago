from .droppedKey import DroppedKey
from .items import *


class HeartContainer(DroppedKey):
    # Due to the patches a heartContainers acts like a dropped key.
    def configure(self, options):
        if options.heartcontainers or options.hpmode == 'extralow':
            super().configure(options)
        elif options.hpmode == 'inverted':
            self.OPTIONS = [BAD_HEART_CONTAINER]
        elif options.hpmode == 'low':
            self.OPTIONS = [HEART_PIECE]
        else:
            self.OPTIONS = [HEART_CONTAINER]
