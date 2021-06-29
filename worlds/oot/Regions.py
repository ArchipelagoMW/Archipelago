from enum import unique, Enum

from BaseClasses import Region
# from .Location import LocationFactory

# probably move this out to Utils later


# copied from OoT-Randomizer/Region.py
@unique
class RegionType(Enum):

    Overworld = 1
    Interior = 2
    Dungeon = 3
    Grotto = 4


    @property
    def is_indoors(self):
        """Shorthand for checking if Interior or Dungeon"""
        return self in (RegionType.Interior, RegionType.Dungeon, RegionType.Grotto)

# Pretends to be an enum, but when the values are raw ints, it's much faster
class TimeOfDay(object):
    NONE = 0
    DAY = 1
    DAMPE = 2
    ALL = DAY | DAMPE




class OOTRegion(Region):
    game: str = "Ocarina of Time"

    def __init__(self, name: str, type, hint, player: int): 
        super(OOTRegion, self).__init__(name, type, hint, player)
        self.price = None
        self.time_passes = False
        self.provides_time = TimeOfDay.NONE
        self.scene = None

    # def copy(self, new_world): # don't know if I need this

    def get_scene(self): 
        if self.scene: 
            return self.scene
        elif self.dungeon: 
            return self.dungeon.name
        else: 
            return None

