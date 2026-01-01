from .droppedKey import DroppedKey


class Instrument(DroppedKey):
    # Thanks to patches, an instrument is just a dropped key as far as the randomizer is concerned.

    def configure(self, options):
        if not options.instruments and not options.goal == "seashells":
            self.OPTIONS = ["INSTRUMENT%d" % (self._location.dungeon)]
