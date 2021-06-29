from enum import Enum
from BaseClasses import Location

class DisableType(Enum): 
    ENABLED = 0
    PENDING = 1
    DISABLED = 2

class OOTLocation(Location): 
    def __init__(self, player, name='', address=None, address2=None, default=None, type='Chest', scene=None, parent=None, filter_tags=None, internal=False):
        super(OOTLocation, self).__init__(player, name, address, parent)
        self.address2 = address2
        self.default = default
        self.type = type
        self.scene = scene
        self.internal = internal
        # is staleness_count equivalent to recursion_count?
        self.access_rules = []
        self.locked = False
        self.price = None
        self.minor_only = False
        self.world = None # probably superseded by self.player
        self.disabled = DisableType.ENABLED
        self.always = False
        self.never = False
        if filter_tags is None: 
            self.filter_tags = None
        else: 
            self.filter_tags = list(filter_tags)

    # def copy(self, new_region):




