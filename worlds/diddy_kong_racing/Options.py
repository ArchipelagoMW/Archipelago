from dataclasses import dataclass

from Options import Choice, DefaultOnToggle, OptionGroup, PerGameCommonOptions, Range, Toggle


class VictoryCondition(Choice):
    """
    The victory condition for the seed:
        Beat Wizpig 1: Find the 4 Wizpig amulet pieces and beat the first Wizpig race. Future Fun Land items will not be randomized.
        Beat Wizpig 2: Get access to Future Fun Land, find the 4 T.T. amulet pieces and all 47 golden balloons, and beat the second Wizpig race.
    """
    display_name = "Victory condition"
    option_beat_wizpig_1 = 0
    option_beat_wizpig_2 = 1
    default = option_beat_wizpig_1


class ShuffleWizpigAmulet(Toggle):
    """Shuffle the 4 Wizpig amulet pieces into the item pool"""
    display_name = "Shuffle Wizpig amulet"


class ShuffleTTAmulet(Toggle):
    """Shuffle the 4 T.T. amulet pieces into the item pool"""
    display_name = "Shuffle T.T. amulet"


class OpenWorlds(Toggle):
    """All worlds, including Future Fun Land, will be open from the start"""
    display_name = "Open worlds"


class DoorRequirementProgression(Choice):
    """
    The progression of door requirement amounts:
        Vanilla: Same requirement amounts as vanilla, roughly exponential with a big jump at the end of Dragon Forest
            Looks like this: [1, 1, 2, 2, 2, 3, 3, 5, 6, 6, 7, 8, 9, 10, 10, 10, 10, 11, 11, 13, 14, 16, 16, 16, 16, 17, 17, 18, 20, 20, 22, 22, 23, 24, 30, 37, 39, 40, 41, 42, 43, 44, 45, 46]
        Linear: Door requirements go up at a consistent rate
            Looks like this if max door requirement = 46: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 46]
        Exponential: Door requirements are clustered towards lower numbers, same trend as vanilla but without big gaps
            Looks like this if max door requirement = 46: [1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 5, 5, 5, 6, 7, 7, 8, 8, 9, 10, 11, 12, 12, 13, 14, 16, 17, 18, 19, 21, 22, 24, 25, 27, 29, 31, 33, 36, 38, 41, 44, 46]
    """
    display_name = "Door requirement progression"
    option_vanilla = 0
    option_linear = 1
    option_exponential = 2
    default = option_vanilla


class MaximumDoorRequirement(Range):
    """Maximum balloon requirement for a numbered door (does not include the Wizpig 2 door). Only used if door requirement progression is not vanilla."""
    display_name = "Maximum door requirement"
    range_start = 1
    range_end = 46
    default = range_end


class ShuffleDoorRequirements(Toggle):
    """The balloon requirements to open all numbered doors will be shuffled"""
    display_name = "Shuffle door requirements"


class ShuffleRaceEntrances(Toggle):
    """The race entrances behind all numbered doors will be shuffled"""
    display_name = "Shuffle race entrances"


class Boss1RegionalBalloons(Range):
    """The number of regional balloons required to unlock boss race 1 for that region"""
    display_name = "Boss 1 regional balloons"
    range_start = 0
    range_end = 4
    default = range_end


class Boss2RegionalBalloons(Range):
    """The number of regional balloons required to unlock boss race 2 for that region"""
    display_name = "Boss 2 regional balloons"
    range_start = 0
    range_end = 8
    default = range_end


class Wizpig1AmuletPieces(Range):
    """The number of Wizpig amulet pieces required to unlock Wizpig race 1"""
    display_name = "Wizpig 1 amulet pieces"
    range_start = 0
    range_end = 4
    default = range_end


class Wizpig2AmuletPieces(Range):
    """The number of T.T. amulet pieces required to unlock Wizpig race 2, along with the balloon requirement"""
    display_name = "Wizpig 2 amulet pieces"
    range_start = 0
    range_end = 4
    default = range_end


class Wizpig2Balloons(Range):
    """The number of balloons required to unlock Wizpig race 2, along with the T.T. amulet piece requirement"""
    display_name = "Wizpig 2 balloons"
    range_start = 0
    range_end = 47
    default = range_end


class TrackVersion(Choice):
    """Whether regular race tracks will be Adventure 1 (normal) or Adventure 2 (faster CPUs, mirrored tracks, and harder silver coin placements)"""
    display_name = "Track version"
    option_adventure_1 = 0
    option_adventure_2 = 1
    option_random_per_track = 2


class PowerUpBalloonType(Choice):
    """
    Alter the power-up balloons in races (does not affect boss races):
        Random (visible): Power-up balloons will visually shuffle between all types.
        Random (hidden): Power-up balloons will shuffle between all types, but always appear rainbow.
    """
    display_name = "Power-up balloon type"
    option_vanilla = 0
    option_random_visible = 1
    option_random_hidden = 2
    default = option_vanilla


class RandomizeCharacterOnMapChange(Toggle):
    """Randomly change your character every time the map is changed"""
    display_name = "Randomize character on map change"


class RandomizeMusic(Toggle):
    """Randomize music"""
    display_name = "Randomize music"


class SkipTrophyRaces(DefaultOnToggle):
    """Start with all 1st place trophies, so you only need to beat Wizpig 1 to unlock Future Fun Land"""
    display_name = "Skip trophy races"


@dataclass
class DiddyKongRacingOptions(PerGameCommonOptions):
    victory_condition: VictoryCondition
    shuffle_wizpig_amulet: ShuffleWizpigAmulet
    shuffle_tt_amulet: ShuffleTTAmulet
    open_worlds: OpenWorlds
    door_requirement_progression: DoorRequirementProgression
    maximum_door_requirement: MaximumDoorRequirement
    shuffle_door_requirements: ShuffleDoorRequirements
    shuffle_race_entrances: ShuffleRaceEntrances
    boss_1_regional_balloons: Boss1RegionalBalloons
    boss_2_regional_balloons: Boss2RegionalBalloons
    wizpig_1_amulet_pieces: Wizpig1AmuletPieces
    wizpig_2_amulet_pieces: Wizpig2AmuletPieces
    wizpig_2_balloons: Wizpig2Balloons
    track_version: TrackVersion
    power_up_balloon_type: PowerUpBalloonType
    randomize_character_on_map_change: RandomizeCharacterOnMapChange
    randomize_music: RandomizeMusic
    skip_trophy_races: SkipTrophyRaces


OPTION_GROUPS: list[OptionGroup] = [
    OptionGroup("Victory", [
        VictoryCondition
    ]),
    OptionGroup("Items", [
        ShuffleWizpigAmulet,
        ShuffleTTAmulet
    ]),
    OptionGroup("Doors", [
        OpenWorlds,
        DoorRequirementProgression,
        MaximumDoorRequirement,
        ShuffleDoorRequirements,
        ShuffleRaceEntrances
    ]),
    OptionGroup("Bosses", [
        Boss1RegionalBalloons,
        Boss2RegionalBalloons,
        Wizpig1AmuletPieces,
        Wizpig2AmuletPieces,
        Wizpig2Balloons
    ]),
    OptionGroup("Gameplay", [
        TrackVersion,
        PowerUpBalloonType,
        RandomizeCharacterOnMapChange
    ]),
    OptionGroup("Other", [
        RandomizeMusic,
        SkipTrophyRaces
    ])
]
