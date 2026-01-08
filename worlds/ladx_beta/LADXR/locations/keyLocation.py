from .itemInfo import ItemInfo


class KeyLocation(ItemInfo):
    OPTIONS = []

    def __init__(self, key):
        super().__init__()
        self.event = key

    def patch(self, rom, option, *, multiworld=None):
        pass

    def read(self, rom):
        return self.OPTIONS[0]

    def configure(self, options):
        pass
