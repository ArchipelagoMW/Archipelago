import typing
from ..checkMetadata import checkMetadataTable
from .constants import *

custom_name_replacements = {
    '"':"'",
    '_':' ',
}

class ItemInfo:
    MULTIWORLD = True

    def __init__(self, room=None, extra=None):
        self.item = None
        self._location = None
        self.room = room
        self.extra = extra
        self.metadata = checkMetadataTable.get(self.nameId, checkMetadataTable["None"])
        self.forced_item = None
        self.custom_item_name = None
        
        self.event = None
    @property
    def location(self):
        return self._location

    def setLocation(self, location):
        self._location = location

    def setCustomItemName(self, name):
        for key, val in custom_name_replacements.items():
            name = name.replace(key, val)
        self.custom_item_name = name

    def getOptions(self):
        return self.OPTIONS

    def configure(self, options):
        pass

    def read(self, rom):
        raise NotImplementedError()

    def patch(self, rom, option, *, multiworld=None):
        raise NotImplementedError()

    def __repr__(self):
        return self.__class__.__name__
    
    @property
    def nameId(self):
        return "0x%03X" % self.room if self.room is not None else "None"
