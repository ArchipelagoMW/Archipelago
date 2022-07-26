from enum import unique, Enum

from BaseClasses import Region


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

    def __init__(self, name: str, player: int, world):
        super(OOTRegion, self).__init__(name, player, world)
        self.hint = None
        self.price = None
        self.time_passes = False
        self.provides_time = TimeOfDay.NONE
        self.scene = None
        self.dungeon = None
        self.pretty_name = None
        self.font_color = None

    def get_scene(self): 
        if self.scene: 
            return self.scene
        elif self.dungeon: 
            return self.dungeon.name
        else: 
            return None

    def can_reach(self, state):
        if state.stale[self.player]:
            stored_age = state.age[self.player]
            state._oot_update_age_reachable_regions(self.player)
            state.age[self.player] = stored_age
        if state.age[self.player] == 'child': 
            return self in state.child_reachable_regions[self.player]
        elif state.age[self.player] == 'adult': 
            return self in state.adult_reachable_regions[self.player]
        else: # we don't care about age
            return self in state.child_reachable_regions[self.player] or self in state.adult_reachable_regions[self.player]

