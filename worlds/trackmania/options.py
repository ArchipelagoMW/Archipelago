from dataclasses import dataclass
from datetime import datetime  # for custom_series: uploaded_before and uploaded_after
from schema import Schema, And, Or, Optional  # for custom series validation
from typing import List, Dict, Any
from Options import Toggle, Range, OptionSet, OptionDict, PerGameCommonOptions, OptionGroup, ProgressionBalancing, Accessibility, Visibility#, PlandoItems
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

class SeriesMinimumMapNumber(Range):
    """Sets the minimum number of maps in each series."""
    display_name = "Minimum Number of Maps per Series"
    range_start = 1
    range_end = 20
    default = 5

class SeriesMaximumMapNumber(Range):
    """Sets the maximum number of maps in each series."""
    display_name = "Maximum Number of Maps per Series"
    range_start = 1
    range_end = 20
    default = 15

class RandomSeriesTags(Toggle):
    """Enable to pick one of your tags at random to use for each series, instead of using all tags for each series"""
    display_name = "Pick Random Tag for each Series"

class FirstSeriesSize(Range):
    """This is an override setting to manually set the size of the first series. Some games, like Super Metroid, work best with small first areas. This setting is here to enable that!

    Set this to zero to have the first series randomized the same as all the others.
    """
    display_name = "Size of First Series"
    range_start = 0
    range_end = 20
    default = 0

class MedalRequirement(Range):
    """Percentage of maps in each series you must get the progression medal from.
    
    Your progression medal is the quickest medal equal to or below your target time.
    """
    display_name = "Series Medal Percentage"
    range_start = 1
    range_end = 100
    default = 80

class SkipPercentage(Range):
    """The number of map skips in the item pool, calculated as a percentage of the total number of maps.
    
    If a map is broken, impossible, or you get stuck, use the /reroll command in the client to replace
    the currently loaded map with a new one.
    """
    display_name = "Map Skip Item Percentage"
    range_start = 0
    range_end = 100
    default = 5

class DiscountPercentage(Range):
    """The number of target time discounts in the item pool, calculated as a percentage of the total number of maps.
    
    This item decreases your personal best time used by this plugin by 1.5% (by default). That might not sound like a lot, but it helps!
    """
    display_name = "PB Discount Item Percentage"
    range_start = 0
    range_end = 100
    default = 20


class DiscountAmount(Range):
    """The strength of PB Discount Items. The discount is calculated by dividing this setting by 10 and multiplying it by the author time. For example, the default setting of 15 becomes 1.5% of the author time.
    """
    display_name = "PB Discount Item Strength"
    range_start = 1
    range_end = 100
    default = 15

class ProgressiveTargetTimeChance(Range):
    """Percentage chance that the item received for beating the target time is guaranteed to be a progression item"""
    display_name = "Target Time Progression Item Chance"
    range_start = 0
    range_end = 100
    default = 20

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


class MapMaximumLength(Range):
    """The maximum length a map can be in seconds.
    """
    display_name = "Maximum Map Length"
    range_start = 1
    range_end = 2000
    default = 300

class MapMinimumLength(Range):
    """The minimum length a map can be in seconds.
    """
    display_name = "Minimum Map Length"
    range_start = 0
    range_end = 2000
    default = 0

class HasAward(Toggle):
    """Enable to guarantee every rolled track will have at least one award on Trackmania Exchange."""
    display_name = "Must Be Awarded"

class DisableBronzeLocations(Toggle):
    """Disable Bronze Medal times from counting as locations."""
    display_name = "Remove Bronze Locations"

class DisableBronzeMedals(Toggle):
    """Remove all Bronze Medals from the Item Pool (unless it is the progression medal)."""
    display_name = "Remove Bronze Medals"


class DisableSilverLocations(Toggle):
    """Disable Silver Medal times from counting as locations."""
    display_name = "Remove Silver Locations"


class DisableSilverMedals(Toggle):
    """Remove all Silver Medals from the Item Pool (unless it is the progression medal)."""
    display_name = "Remove Silver Medals"


class DisableGoldLocations(Toggle):
    """Disable Gold Medal times from counting as locations."""
    display_name = "Remove Gold Locations"


class DisableGoldMedals(Toggle):
    """Remove all Gold Medals from the Item Pool (unless it is the progression medal)."""
    display_name = "Remove Gold Medals"


class DisableAuthorLocations(Toggle):
    """Disable Author Medal times from counting as locations."""
    display_name = "Remove Bronze Locations"

# Schema for custom series options below.
LuaBool = Or(bool, And(int, lambda v: v in (0, 1)))
MapIdList = And([int], lambda v: len(v) <= 100)
TagList = And([And(str, lambda v: v in get_all_map_tags())], lambda v: len(v) <= 100)
DifficultyList = And([And(str, lambda v: v in get_all_map_difficulties())], lambda v: len(v) <= 4)
DateTimeString = And(str, lambda v: datetime.fromisoformat(v))

class CustomSeries(OptionDict):
    """Define custom search parameters for Trackmania Exchange for each series.

    The expected format is a dictionary containing the series number you wish to customize, followed by a list of
    options and search parameters. The series number may also be "all", to customize all series at once.

    The following options may be redefined on a per-series basis to override them:
    - "map_tags"
    - "map_etags"
    - "map_tags_inclusive"
    - "difficulties"
    - "has_award"

    In addition, the following custom search parameters are available:
    - "map_ids": A list of specific map IDs to randomly choose between (max 100)
    - "name": The name of the map must contain the given string (partial search)
    - "author": The map must be authored by the given user on TMX (by ID, not name)
    - "map_pack": The map must be in the given map pack on TMX (by ID, not name)
    - "uploaded_after": The map must have been uploaded after the given date
    - "uploaded_before": The map must have been uploaded before the given date
    - "min_length": The author time of the map must be longer than the given time, in milliseconds
    - "max_length": The author time of the map must be shorter than the given time, in milliseconds
    - "has_replay": If true, the map must have at least 1 replay

    Example:
    ```
    custom_series:
      all:
        has_award: true
      1:
        map_tags: ["LOL"]
        difficulties: ["Beginner", "Intermediate"]
        uploaded_after: "2019-12-31"
      2:
        map_tags: ["Tech"]
        min_length: 40000
        max_length: 75000
    ```

    All Current Valid Tags:
    Race,FullSpeed,Tech,RPG,LOL,Press Forward,SpeedTech,MultiLap,
    Offroad,Trial,ZrT,SpeedFun,Competitive,Ice,Dirt,Stunt,Reactor,
    Platform,Slow Motion,Bumper,Fragile,Scenery,Kacky,Endurance,Mini,
    Remake,Mixed,Nascar,SpeedDrift,Minigame,Obstacle,Transitional,Grass,
    Backwards,EngineOff,Signature,Royal,Water,Plastic,Arena,Freestyle,
    Educational,Sausage,Bobsleigh,Pathfinding,FlagRush,Puzzle,Freeblocking,
    Altered Nadeo,SnowCar,Wood,Underwater,Turtle,RallyCar,MixedCar,
    Bugslide,Mudslide,Moving Items,DesertCar,SpeedMapping,NoBrake,CruiseControl,
    NoSteer,RPG-Immersive,Pipes,Magnet,NoGrip
    TM2 Exclusive Tags:
    Glass,Sand,Cobblestone,ForceAccel
    """
    display_name = "Custom Series"
    visibility = Visibility.template|Visibility.spoiler
    default = {}
    schema = Schema({
        Optional(Or("all", And(int, lambda v: 1 <= v <= SeriesNumber.range_end))): {
            # Duplicates of options normally present, for overriding
            Optional("map_tags"): TagList,
            Optional("map_etags"): TagList,
            Optional("map_tags_inclusive"): LuaBool,
            Optional("difficulties"): DifficultyList,

            # Advanced search parameters
            Optional("map_ids"): MapIdList,  # API ref: `id`
            Optional("name"): str,  # API ref: `name` - Full text search by name, partial
            Optional("author"): int,  # API ref: `authoruserid`
            Optional("map_pack"): int,  # API ref: `mappackid`
            Optional("uploaded_after"): DateTimeString,  # API ref: `uploadedafter`
            Optional("uploaded_before"): DateTimeString,  # API ref: `uploadedbefore`
            Optional("min_length"): int,  # API ref: `authortimemin`
            Optional("max_length"): int,  # API ref: `authortimemax`
            Optional("has_award"): LuaBool,  # API ref: `inlatestawardedauthor`
            Optional("has_replay"): LuaBool,  # API ref: `inhasreplay`
        }
    })


@dataclass
class TrackmaniaOptions(PerGameCommonOptions):
    progression_balancing: ProgressionBalancing
    accessibility: Accessibility

    target_time: TargetTime
    series_number : SeriesNumber
    series_minimum_map_number: SeriesMinimumMapNumber
    series_maximum_map_number: SeriesMaximumMapNumber
    random_series_tags: RandomSeriesTags
    first_series_size: FirstSeriesSize
    medal_requirement: MedalRequirement
    skip_percentage: SkipPercentage
    discount_percentage: DiscountPercentage
    discount_amount: DiscountAmount
    target_progression_chance : ProgressiveTargetTimeChance
    map_tags: MapTags
    map_tags_inclusive: MapTagsInclusive
    map_etags: MapETags
    map_max_length: MapMaximumLength
    map_min_length: MapMinimumLength
    difficulties: MapDifficulties
    has_award: HasAward
    disable_bronze_locations: DisableBronzeLocations
    disable_bronze_medals: DisableBronzeMedals
    disable_silver_locations: DisableSilverLocations
    disable_silver_medals: DisableSilverMedals
    disable_gold_locations: DisableGoldLocations
    disable_gold_medals: DisableGoldMedals
    disable_author_locations: DisableAuthorLocations

    custom_series: CustomSeries

option_groups: Dict[str, List[Any]] = {
    "Generation":[ProgressionBalancing, Accessibility],
    "Difficulty":[TargetTime, SkipPercentage, DiscountPercentage, DiscountAmount, MapDifficulties],
    "Campaign Configuration":[MedalRequirement, ProgressiveTargetTimeChance, SeriesNumber, SeriesMinimumMapNumber, SeriesMaximumMapNumber],
    "Map Search Settings":[MapTags, MapETags, MapTagsInclusive, RandomSeriesTags, HasAward, MapMinimumLength, MapMaximumLength],
    "Advanced":[FirstSeriesSize, DisableBronzeLocations, DisableBronzeMedals, DisableSilverLocations, DisableSilverMedals, DisableGoldLocations, DisableGoldMedals, DisableAuthorLocations, CustomSeries]#, PlandoItems]
}

def create_option_groups() -> List[OptionGroup]:
    option_group_list: List[OptionGroup] = []
    for name, options in option_groups.items():
        option_group_list.append(OptionGroup(name=name, options=options))

    return option_group_list
