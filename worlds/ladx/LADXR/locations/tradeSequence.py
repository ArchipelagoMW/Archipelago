from .itemInfo import ItemInfo
from .constants import *
from .droppedKey import DroppedKey

TradeRequirements = {
    TRADING_ITEM_YOSHI_DOLL: None,
    TRADING_ITEM_RIBBON: TRADING_ITEM_YOSHI_DOLL,
    TRADING_ITEM_DOG_FOOD: TRADING_ITEM_RIBBON,
    TRADING_ITEM_BANANAS: TRADING_ITEM_DOG_FOOD,
    TRADING_ITEM_STICK: TRADING_ITEM_BANANAS,
    TRADING_ITEM_HONEYCOMB: TRADING_ITEM_STICK,
    TRADING_ITEM_PINEAPPLE: TRADING_ITEM_HONEYCOMB,
    TRADING_ITEM_HIBISCUS: TRADING_ITEM_PINEAPPLE,
    TRADING_ITEM_LETTER: TRADING_ITEM_HIBISCUS,
    TRADING_ITEM_BROOM: TRADING_ITEM_LETTER,
    TRADING_ITEM_FISHING_HOOK: TRADING_ITEM_BROOM,
    TRADING_ITEM_NECKLACE: TRADING_ITEM_FISHING_HOOK,
    TRADING_ITEM_SCALE: TRADING_ITEM_NECKLACE,
    TRADING_ITEM_MAGNIFYING_GLASS: TRADING_ITEM_SCALE,
}
class TradeSequenceItem(DroppedKey):
    def __init__(self, room, default_item):
        self.unadjusted_room = room
        if room == 0x2B2:
            # Offset room for trade items to avoid collisions 
            roomLo = room & 0xFF
            roomHi = room ^ roomLo
            roomLo = (roomLo + 2) & 0xFF
            room = roomHi | roomLo
        super().__init__(room)
        self.default_item = default_item

    def configure(self, options):
        if not options.tradequest:
            self.OPTIONS = [self.default_item]
        super().configure(options)

    #def patch(self, rom, option, *, multiworld=None):
    #    rom.banks[0x3E][self.room + 0x3B16] = CHEST_ITEMS[option]

    def read(self, rom):
        assert(False)
        assert self._location is not None, hex(self.room)
        value = rom.banks[0x3E][self.room + 0x3B16]
        for k, v in CHEST_ITEMS.items():
            if v == value:
                return k
        raise ValueError("Could not find owl statue contents in ROM (0x%02x)" % (value))

    def __repr__(self):
        return "%s:%03x" % (self.__class__.__name__, self.room)

    @property
    def nameId(self):
        return "0x%03X-Trade" % self.unadjusted_room
