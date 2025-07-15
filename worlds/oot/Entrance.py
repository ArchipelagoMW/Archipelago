from BaseClasses import Entrance

class OOTEntrance(Entrance): 
    game: str = 'Ocarina of Time'

    def __init__(self, player, multiworld, name='', parent=None):
        super(OOTEntrance, self).__init__(player, name, parent)
        self.multiworld = multiworld
        self.access_rules = []
        self.reverse = None
        self.replaces = None
        self.assumed = None
        self.type = None
        self.shuffled = False
        self.data = None
        self.primary = False
        self.always = False
        self.never = False

    def bind_two_way(self, other_entrance):
        self.reverse = other_entrance
        other_entrance.reverse = self

    def disconnect(self):
        self.connected_region.entrances.remove(self)
        previously_connected = self.connected_region
        self.connected_region = None
        return previously_connected

    def get_new_target(self, pool_type):
        root = self.multiworld.get_region('Root Exits', self.player)
        target_entrance = OOTEntrance(self.player, self.multiworld, f'Root -> ({self.name}) ({pool_type})', root)
        target_entrance.connect(self.connected_region)
        target_entrance.replaces = self
        root.exits.append(target_entrance)
        return target_entrance

    def assume_reachable(self, pool_type):
        if self.assumed == None:
            self.assumed = self.get_new_target(pool_type)
            self.disconnect()
        return self.assumed
