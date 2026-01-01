from enum import unique, Enum

from BaseClasses import Region, MultiWorld
from .Hints import HintArea


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

    def __init__(self, name: str, player: int, multiworld: MultiWorld):
        super(OOTRegion, self).__init__(name, player, multiworld)
        self._oot_hint = None
        self.alt_hint = None
        self.price = None
        self.time_passes = False
        self.provides_time = TimeOfDay.NONE
        self.scene = None
        self.dungeon = None
        self.pretty_name = None
        self.font_color = None
        self.is_boss_room = False

    # This is too generic of a name to risk not breaking in the future.
    # This lets us possibly switch it out later if AP starts using it.
    @property
    def hint(self):
        return self._oot_hint

    @hint.setter
    def hint(self, value):
        self._oot_hint = value

    def get_scene(self):
        if self.scene: 
            return self.scene
        elif self.dungeon: 
            return self.dungeon.name
        else: 
            return None

    def can_reach(self, state):
        if state._oot_stale[self.player]:
            stored_age = state.age[self.player]
            state._oot_update_age_reachable_regions(self.player)
            state.age[self.player] = stored_age
        if state.age[self.player] == 'child': 
            return self in state.child_reachable_regions[self.player]
        elif state.age[self.player] == 'adult': 
            return self in state.adult_reachable_regions[self.player]
        else: # we don't care about age
            return self in state.child_reachable_regions[self.player] or self in state.adult_reachable_regions[self.player]

    def set_hint_data(self, hint):
        if self.dungeon:
            self._oot_hint = HintArea.for_dungeon(self.dungeon)
        else:
            self._oot_hint = HintArea[hint]
        self._hint_text = str(self._oot_hint)
