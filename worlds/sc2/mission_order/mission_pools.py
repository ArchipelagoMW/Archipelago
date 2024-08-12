from enum import IntEnum
from typing import TYPE_CHECKING, Dict, Set, List

from ..mission_tables import SC2Mission, lookup_id_to_mission, lookup_name_to_mission, MissionFlag, SC2Campaign
from worlds.AutoWorld import World

if TYPE_CHECKING:
    from .structs import SC2MOGenMission

class Difficulty(IntEnum):
    RELATIVE = 0
    STARTER = 1
    EASY = 2
    MEDIUM = 3
    HARD = 4
    VERY_HARD = 5

# TODO figure out an organic way to get these
DEFAULT_DIFFICULTY_THRESHOLDS = {
    Difficulty.STARTER: 0,
    Difficulty.EASY: 5,
    Difficulty.MEDIUM: 35,
    Difficulty.HARD: 65,
    Difficulty.VERY_HARD: 95,
    Difficulty.VERY_HARD + 1: 100
}

def modified_difficulty_thresholds(min: Difficulty, max: Difficulty) -> Dict[int, Difficulty]:
    if min == Difficulty.RELATIVE:
        min = Difficulty.STARTER
    if max == Difficulty.RELATIVE:
        max = Difficulty.VERY_HARD
    thresholds: Dict[int, Difficulty] = {}
    min_thresh = DEFAULT_DIFFICULTY_THRESHOLDS[min]
    total_thresh = DEFAULT_DIFFICULTY_THRESHOLDS[max + 1] - min_thresh
    for difficulty in range(min, max + 1):
        threshold = DEFAULT_DIFFICULTY_THRESHOLDS[difficulty] - min_thresh
        threshold *= 100 / total_thresh
        thresholds[int(threshold)] = Difficulty(difficulty)
    return thresholds

class SC2MOGenMissionPools:
    """
    Manages available and used missions for a mission order.
    """
    master_list: Set[int]
    difficulty_pools: Dict[Difficulty, Set[int]]
    _used_flags: Dict[MissionFlag, int]
    _used_missions: Set[SC2Mission]

    def __init__(self) -> None:
        self.master_list = {mission.id for mission in SC2Mission}
        self.difficulty_pools = {
            diff: {mission.id for mission in SC2Mission if mission.pool + 1 == diff}
            for diff in Difficulty if diff != Difficulty.RELATIVE
        }
        self._used_flags = {}
        self._used_missions = set()

    def set_exclusions(self, excluded: List[SC2Mission], unexcluded: List[SC2Mission]) -> None:
        """Prevents all the missions that appear in the `excluded` list, but not in the `unexcluded` list,
        from appearing in the mission order."""
        total_exclusions = [mission.id for mission in excluded if mission not in unexcluded]
        self.master_list.difference_update(total_exclusions)

    def get_allowed_mission_count(self) -> int:
        return len(self.master_list)
    
    def count_allowed_missions(self, campaign: SC2Campaign) -> int:
        allowed_missions = [
            mission_id
            for mission_id in self.master_list
            if lookup_id_to_mission[mission_id].campaign == campaign
        ]
        return len(allowed_missions)

    def move_mission(self, mission: SC2Mission, old_diff: Difficulty, new_diff: Difficulty) -> None:
        """Changes the difficulty of the given `mission`. Does nothing if the mission is not allowed to appear
        or if it isn't set to the `old_diff` difficulty."""
        if mission.id in self.master_list and mission.id in self.difficulty_pools[old_diff]:
            self.difficulty_pools[old_diff].remove(mission.id)
            self.difficulty_pools[new_diff].add(mission.id)

    def get_pool_size(self, diff: Difficulty) -> int:
        """Returns the amount of missions of the given difficulty that are allowed to appear."""
        return len(self.difficulty_pools[diff])
    
    def get_used_flags(self) -> Dict[MissionFlag, int]:
        """Returns a dictionary of all used flags and their appearance count within the mission order.
        Flags that don't appear in the mission order also don't appear in this dictionary."""
        return self._used_flags

    def get_used_missions(self) -> Set[SC2Mission]:
        """Returns a set of all missions used in the mission order."""
        return self._used_missions

    def pull_specific_mission(self, mission: SC2Mission) -> None:
        """Marks the given mission as present in the mission order."""
        # Remove the mission from the master list and whichever difficulty pool it is in
        if mission.id in self.master_list:
            self.master_list.remove(mission.id)
            for diff in self.difficulty_pools:
                if mission.id in self.difficulty_pools[diff]:
                    self.difficulty_pools[diff].remove(mission.id)
                    break
        self._add_mission_stats(mission)
    
    def _add_mission_stats(self, mission: SC2Mission) -> None:
        # Update used flag counts & missions
        for flag in mission.flags:
            self._used_flags.setdefault(flag, 0)
            self._used_flags[flag] += 1
        self._used_missions.add(mission)

    def pull_random_mission(self, world: World, slot: 'SC2MOGenMission') -> SC2Mission:
        """Picks a random mission from the mission pool of the given slot, preferring a mission from `locked_ids` if allowed in the slot,
        and marks it as present in the mission order."""
        # Use a locked mission if possible in this slot
        pool = slot.option_mission_pool.intersection(self.master_list)
        
        difficulty_pools: Dict[int, List[int]] = {
            diff: list(pool.intersection(self.difficulty_pools[diff]))
            for diff in Difficulty if diff != Difficulty.RELATIVE
        }

        # Iteratively look down and up around the slot's desired difficulty
        # Either a difficulty with valid missions is found, or an error is raised
        final_pool: List[int] = []
        final_difficulty = Difficulty.RELATIVE
        desired_diff = slot.option_difficulty
        diff_offset = 0
        while len(final_pool) == 0:
            lower_diff = max(desired_diff - diff_offset, 1)
            higher_diff = min(desired_diff + diff_offset, 5)
            final_pool = difficulty_pools[lower_diff]
            if len(final_pool) > 0:
                final_difficulty = Difficulty(lower_diff)
                break
            final_pool = difficulty_pools[higher_diff]
            if len(final_pool) > 0:
                final_difficulty = Difficulty(higher_diff)
                break
            if lower_diff == Difficulty.STARTER and higher_diff == Difficulty.VERY_HARD:
                raise Exception(f"Slot in layout \"{slot.parent().get_visual_requirement()}\" ran out of possible missions to place.")
            diff_offset += 1
        
        # Remove the mission from the master list
        mission = lookup_id_to_mission[world.random.choice(final_pool)]
        self.master_list.remove(mission.id)
        self.difficulty_pools[final_difficulty].remove(mission.id)
        self._add_mission_stats(mission)
        return mission
