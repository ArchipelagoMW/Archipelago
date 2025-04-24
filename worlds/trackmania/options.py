from dataclasses import dataclass
from typing import List, Dict, Any
from Options import Toggle, Range, OptionSet, PerGameCommonOptions, OptionGroup, ProgressionBalancing, Accessibility
from .data import get_all_map_tags, get_excluded_map_tags, get_all_map_difficulties, get_default_map_difficulties

#https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/options%20api.md

class TargetTime(Range):
    """Determines what time you must drive on a map for it to be considered completed. 
    You can enter any number from 0 to 300.
    
    0   = Bronze Medal
    100 = Silver Medal
    200 = Gold Medal
    300 = Author Medal

    If you choose a value inbetween two medals, your target time will be a mix of those two medals. 
    For example, a value of 250 will make your target time halfway between the gold and author medals. 
    A value of 120 will make your target time 20% of the way from the silver medal to the gold medal.

    The quickest medal equal to or below your target time is made your progression medal.
    """
    display_name = "Target Time Difficulty"
    range_start = 0
    range_end = 300
    default = 240

class SeriesNumber(Range):
    """Sets the number of series that you must play."""
    display_name = "Number of Series"
    range_start = 1
    range_end = 20
    default = 5

class SeriesMapNumber(Range):
    """Sets the number of maps in each series."""
    display_name = "Number of Maps per Series"
    range_start = 1
    range_end = 20
    default = 10

class MedalRequirement(Range):
    """The number of progression medals required to advance to the next series.
    
    Your progression medal is the quickest medal equal to or below your target time.
    """
    display_name = "Series Medal Requirement"
    range_start = 1
    range_end = 20
    default = 8

class SkipPercentage(Range):
    """The number of map skips in the item pool, calculated as a percentage of the total number of maps.
    
    If a map is broken, impossible, or you get stuck, use the /reroll command in the client to replace
    the currently loaded map with a new one.
    """
    display_name = "Map Skip Item Percentage"
    range_start = 0
    range_end = 100
    default = 10

class ProgressiveTargetTimeChance(Range):
    """Percentage chance that the item received for beating the target time is guaranteed to be a progression item"""
    display_name = "Target Time Progression Item Chance"
    range_start = 0
    range_end = 100
    default = 40

class MapTags(OptionSet):
    """Tags that maps from Trackmania Exchange are allowed to have. If none of these tags are checked, 
    it will default to allowing all tags."""
    display_name = "Allowed TMX Tags"
    valid_keys = get_all_map_tags()

class MapTagsInclusive(Toggle):
    """Enable if maps must have every single tag chosen in Allowed TMX Tags"""
    display_name = "Are TMX Tags Inclusive"

class MapETags(OptionSet):
    """Tags that maps from Trackmania Exchange are *not* allowed to have."""
    display_name = "Excluded TMX Tags"
    valid_keys = get_all_map_tags()
    default = get_excluded_map_tags()

class MapDifficulties(OptionSet):
    """Difficulty Ratings that maps from Trackmania Exchange are allowed to have."""
    display_name = "Allowed TMX Difficulties"
    valid_keys = get_all_map_difficulties()
    default = get_default_map_difficulties()


@dataclass
class TrackmaniaOptions(PerGameCommonOptions):
    progression_balancing: ProgressionBalancing
    accessibility: Accessibility

    target_time: TargetTime
    series_number : SeriesNumber
    series_map_number: SeriesMapNumber
    medal_requirement: MedalRequirement
    skip_percentage: SkipPercentage
    target_progression_chance : ProgressiveTargetTimeChance
    map_tags: MapTags
    map_tags_inclusive: MapTagsInclusive
    map_etags: MapETags
    difficulties: MapDifficulties

option_groups: Dict[str, List[Any]] = {
    "Generation":[ProgressionBalancing, Accessibility],
    "Difficulty":[TargetTime, SkipPercentage, MapDifficulties],
    "Campaign Configuration":[SeriesNumber, SeriesMapNumber, MedalRequirement, ProgressiveTargetTimeChance],
    "Map Tags":[MapTagsInclusive, MapTags, MapETags]
}

def create_option_groups() -> List[OptionGroup]:
    option_group_list: List[OptionGroup] = []
    for name, options in option_groups.items():
        option_group_list.append(OptionGroup(name=name, options=options))

    return option_group_list
