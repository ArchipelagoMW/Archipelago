"""This module represents options definitions for Trails in the Sky the 3rd"""
from dataclasses import dataclass

from Options import Choice, DefaultOnToggle, PerGameCommonOptions, Toggle, Visibility


class NameSpoilerOption(Toggle):
    """
    Replace character and some area names with spoiler free name.
    """

    display_name = "Hide Spoiler Names"


class ChestItemPoolOptions(Choice):
    """
    Determine the treasure chest item pool

    - Vanilla Shuffle: Shuffle the vanilla chest items into the item pool.
    - Completely Random: Generate new item pool.
    """

    display_name = "Treasure Chests Items"
    default = 0
    option_vanilla_shuffle = 0
    option_completely_random = 1


class StartingCharactersOptions(Choice):
    """
    Randomize who you start the game with.

    - Vanilla: Start the game with Kevin and Ries
    - Set: Start the game with specific character(s)
    - Completely Random: Start the game with completely random characters
    """

    display_name = "Randomize Starting Characters"
    default = 2
    option_vanilla = 0
    option_set = 1
    option_completely_random = 2


class FirstStartingCharacter(Choice):
    """
    Pick the first character to start the game with.
    Only used when Randomize Starting Character is set to Set.
    """

    visibility = Visibility.all & ~Visibility.spoiler
    display_name = "First Starting Characters"
    default = 8
    option_tita = 6
    option_kevin = 8
    option_julia = 13
    option_ries = 14


class SecondStartingCharacter(Choice):
    """
    Pick the second character to start the game with.
    Only used when Randomize Starting Character is set to Set.
    If the same character from the previous option is picked, it will be treated as random.
    """

    visibility = Visibility.all & ~Visibility.spoiler
    display_name = "Second Starting Characters"
    default = 14
    option_tita = 6
    option_kevin = 8
    option_julia = 13
    option_ries = 14


class SealingStoneCharactersOptions(Choice):
    """
    Randomize what you get from interacting with a sealing stone.

    - Vanilla: Sealing Stones will unlock their respective character. Will be replace with Kevin and Ries if the character is selected as a starting character.
    - Shuffle: Sealing Stones will unlock random characters.
    - Charactersanity: Sealing Stones will give random items. Characters are in the general item pool.
    """

    display_name = "Sealing Stone Characters Unlock"
    default = 2
    option_vanilla = 0
    option_shuffle = 1
    option_charactersanity = 2


class CharacterStartingQuartzOptions(Choice):
    """
    Determine the character starting quartz pool. They are obtained by interacting with the respective character's sealing stone.

    - Vanilla: Character Sealing Stone will give out the default quartz loadout for that character.
    - Vanilla Shuffle: The default starting quartz will be added to the general item pool. Character Sealing Stone will give out a completely random item for each starting quartz the character has in vanilla.
    - Random Quartz: Character Sealing Stone will give out a random quartz for each starting quartz the character has in vanilla.
    - Completely Random: Character Sealing Stone will give out a completely random item for each starting quartz the character has in vanilla.
    """

    display_name = "Character Starting Quartz"
    default = 1
    option_vanilla = 0
    option_vanilla_shuffle = 1
    option_random_quartz = 2
    option_completely_random = 3


@dataclass
class TitsThe3rdOptions(PerGameCommonOptions):
    """Trails in the Sky the 3rd options Definition"""
    name_spoiler_option: NameSpoilerOption
    chest_itempool_option: ChestItemPoolOptions
    starting_character_option: StartingCharactersOptions
    first_starting_character: FirstStartingCharacter
    second_starting_character: SecondStartingCharacter
    sealing_stone_character_options: SealingStoneCharactersOptions
    character_starting_quartz_options: CharacterStartingQuartzOptions
