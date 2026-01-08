from dataclasses import dataclass
from Options import Toggle, Choice, DefaultOnToggle, PerGameCommonOptions
from .constants.difficulties import NORMAL, HARD, EXPERT, LUNATIC
from .constants.versions import MAP_PATCH, FULL_GOLD
from .constants.player_starts import PlayerStarts


class LogicLevel(Choice):
    """
    The overall difficulty of the logic, used to determine the requirements to access locations and regions.

    Normal: Suitable for anyone who has beaten the game. Requires backflips and knowing where everything is.
    Hard: Requires some easier movement tricks such as cling climbing and backwards ultras using solar wind,
          and more nuanced movement like turning during an air kick.
    Expert: Requires more difficult movement tricks such as ultrahops and reverse wallkicks, and obscure knowledge.
    Lunatic: Requires extremely difficult jumps and creative thinking. No holds barred. You have been warned.
    """
    display_name = "Logic Level"
    option_normal = NORMAL
    option_hard = HARD
    option_expert = EXPERT
    option_lunatic = LUNATIC
    default = NORMAL


class ObscureLogic(Toggle):
    """
    Enables logic for obscure knowledge and creative pathing that isn't difficult to execute but may not be obvious or commonly known.
    This option is forced on if logic level is set to Expert or Lunatic.
    """
    display_name = "Obscure Logic"


class SpawnPoint(Choice):
    """
    Determines where you will spawn into the game when creating a new file.

    castle_main: The save point near Memento in Castle Sansa.
    castle_gazebo: The save point in the gazebo in the Castle Sansa courtyard.
    dungeon_mirror: The vanilla starting point in Dilapidated Dungeon. If this option is selected, start_with_breaker
        will be forced on and you will most likely be expected to leave through the dark rooms to The Underbelly. See
        this video for a guide on how to do that: https://youtu.be/Z_a9l2wzd8c
    library: The save point at the start of Listless Library. If this option is selected, either start_with_breaker or
        randomize_books must also be turned on. If both options are off at the start of generation, start_with_breaker
        will be forced on. If just randomize_books is turned on, your sphere one will have a lot of checks but will be
        very short, so keep that in mind if you are playing in a multiworld with other people.
    underbelly_south: The save point near the building at the south of The Underbelly.
    underbelly_big_room: The save point in the big room in the middle of The Underbelly.
    bailey_main: The save point in Empty Bailey.
    keep_main: The save point in the main hallway in Sansa Keep.
    keep_north: The north save point in Sansa Keep.
    theatre_main: The save point in the auditorium in Twilight Theatre. If this option is selected, your starting
        inventory will include Cling Gem/one Cling Shard on normal, or Heliacal Power/one Air Kick on hard+. You will be
        able to leave Twilight Theatre through the big pillar room to the south.
    """
    display_name = "Spawn Point"
    option_castle_main = PlayerStarts.CastleWestSave.value
    option_castle_gazebo = PlayerStarts.CastleGazeboSave.value
    option_dungeon_mirror = PlayerStarts.DungeonMirror.value
    option_library = PlayerStarts.LibraryMainSave.value
    option_underbelly_south = PlayerStarts.UnderbellySouthSave.value
    option_underbelly_big_room = PlayerStarts.UnderbellyCentralSave.value
    option_bailey_main = PlayerStarts.BaileySave.value
    option_keep_main = PlayerStarts.KeepCentralSave.value
    option_keep_north = PlayerStarts.KeepNorthSave.value
    option_theatre_main = PlayerStarts.TheatreSave.value
    default = PlayerStarts.CastleWestSave.value


class SafeSmallKeys(DefaultOnToggle):
    """
    No locked doors are in logic until all small keys are obtainable.
    Prevents potential softlocks when spending small keys out of logic.

    Currently unused.
    """
    display_name = "Safe Small Keys"


class ProgressiveBreaker(DefaultOnToggle):
    """
    Replaces Dream Breaker, Strikebreak, and Soul Cutter with three Progressive Dream Breaker items.
    """
    display_name = "Progressive Dream Breaker"


class ProgressiveSlide(DefaultOnToggle):
    """
    Replaces Slide and Solar Wind with two Progressive Slide items.
    """
    display_name = "Progressive Slide"


class SplitSunGreaves(Toggle):
    """
    Replaces Sun Greaves and Heliacal Power with four individual Air Kicks.
    """
    display_name = "Split Sun Greaves"


class SplitClingGem(Toggle):
    """
    Replaces Cling Gem with three Cling Shard items.
    Each Cling Shard increases your wall run limit by two.
    """
    display_name = "Split Cling Gem"


class GameVersion(Choice):
    """
    The version of Pseudoregalia you will use when playing the game. Different versions have different logic, locations, and items.
    After you connect, the game will warn you if the version you are playing doesn't match this option.

    map_patch: The latest version of the game. Includes time trials and new outfits.
    full_gold: Previous version, accessible using the "fullgoldjump" beta code in Steam.
    """
    display_name = "Game Version"
    option_map_patch = MAP_PATCH
    option_full_gold = FULL_GOLD
    default = MAP_PATCH


class StartWithBreaker(Toggle):
    """
    Places Dream Breaker (or one Progressive Dream Breaker) in the starting inventory.
    """
    display_name = "Start With Breaker"


class StartWithMap(Toggle):
    """
    Places the map item (Memento) in the starting inventory.

    If Full Gold version is selected, this option has no effect.
    """
    display_name = "Start With Map"


class RandomizeTimeTrials(Toggle):
    """
    Opens the time trials for randomization and puts the outfits in the item pool.
    If turned off, the time trials will not have items and the outfits are placed in the starting inventory.

    If Full Gold version is selected, this option has no effect.
    """
    display_name = "Randomize Time Trials"


class RandomizeGoats(Toggle):
    """
    Adds goatlings as locations. Talk to the goatling to get the item.
    This option adds 19 locations on map patch and 17 locations on full gold.
    For each location added, an essentially useless filler item is also added to the item pool.
    """
    display_name = "Randomize Goats"


class RandomizeChairs(Toggle):
    """
    Adds places Sybil can sit as locations. Sit down to get the item.
    This option adds 16 locations.
    For each location added, an essentially useless filler item is also added to the item pool.
    """
    display_name = "Randomize Chairs"


class RandomizeBooks(Toggle):
    """
    Adds books in the library as locations. Read the book to get the item.
    This option adds 13 locations.
    For each location added, an essentially useless filler item is also added to the item pool.
    """
    display_name = "Randomize Books"


class RandomizeNotes(Toggle):
    """
    Adds notes as locations. Read the note to get the item.
    This option adds 4 locations.
    For each location added, an essentially useless filler item is also added to the item pool.
    """
    display_name = "Randomize Notes"


class MajorKeyHints(DefaultOnToggle):
    """
    Changes the text on the tombstones near the Great Door to tell you the locations of your Major Keys.
    Also makes it so reading the tombstones will create hints.
    """
    display_name = "Major Key Hints"


@dataclass
class PseudoregaliaOptions(PerGameCommonOptions):
    game_version: GameVersion
    logic_level: LogicLevel
    obscure_logic: ObscureLogic
    spawn_point: SpawnPoint
    progressive_breaker: ProgressiveBreaker
    progressive_slide: ProgressiveSlide
    split_sun_greaves: SplitSunGreaves
    split_cling_gem: SplitClingGem
    start_with_breaker: StartWithBreaker
    start_with_map: StartWithMap
    randomize_time_trials: RandomizeTimeTrials
    randomize_goats: RandomizeGoats
    randomize_chairs: RandomizeChairs
    randomize_books: RandomizeBooks
    randomize_notes: RandomizeNotes
    major_key_hints: MajorKeyHints

