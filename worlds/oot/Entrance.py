
from BaseClasses import Entrance
from .Regions import TimeOfDay

class OOTEntrance(Entrance): 
    game: str = 'Ocarina of Time'

    def __init__(self, player, name='', parent=None): 
        super(OOTEntrance, self).__init__(player, name, parent)
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
