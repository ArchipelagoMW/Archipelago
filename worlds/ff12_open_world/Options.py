from typing import Dict
from dataclasses import dataclass
from Options import Choice, Toggle, PerGameCommonOptions


class AllowSeitengrat(Toggle):
    """Allow Seitengrat to appear in the item pool and bazaars."""
    display_name = "Allow Seitengrat"
    default = 0


class ShuffleMainParty(Toggle):
    """Shuffle the 6 main party members around."""
    display_name = "Shuffle Main Party"
    default = 1


class CharacterProgressionScaling(Toggle):
    """In addition to the progression scaling, also scale the progression based on the number of party members
       and if the second license board has been unlocked."""
    display_name = "Character Progression Scaling"
    default = 1


class IncludeTreasures(Toggle):
    """Allows treasures to contain progression and useful items."""
    display_name = "Treasures"
    default = 0


class IncludeChops(Toggle):
    """Allows pinewood chops and sandalwood chop checks to contain progression and useful items.
    Note: The Bahamut Unlock Goal for collecting pinewood chops will still
    require the player to collect the 28 chops for the Writ of Transit."""
    display_name = "Chops"
    default = 0


class IncludeBlackOrbs(Toggle):
    """Allows Pharos floor 1 and Subterra black orb checks to contain progression and useful items."""
    display_name = "Black Orbs"
    default = 0


class IncludeTrophyRareGames(Toggle):
    """Allows trophy rare game checks to contain progression and useful items.
    Includes: Rare Game drops and Number of Rare Game Killed checks."""
    display_name = "Trophy Rare Games"
    default = 0


class IncludeHuntRewards(Toggle):
    """Allows Hunt rewards and drops to contain progression and useful items."""
    display_name = "Hunt Rewards and Drops"
    default = 0


class IncludeClanHallRewards(Toggle):
    """Allows Clan Hall rewards to contain progression and useful items."""
    display_name = "Clan Hall Rewards"
    default = 0


class BahamutUnlock(Choice):
    """Determines where the Writ of Transit is placed to unlock travel to the Bahamut to beat the game.
    Defeat Cid 2: Climb the Pharos and defeat Cid 2 (Requires 2 magicites and 1 story sword).
    Collect Pinewood Chops: Collect 28 pinewood chops from the multiworld and turn in for the Sandalwood Chop check.
    Collect Espers: Collect all 13 espers and turn in for the Clan Hall Control 13 Espers check.
    Random Location: The Writ of Transit can be anywhere in the multiworld."""
    display_name = "Bahamut Unlock Goal"
    option_defeat_cid_2 = 0
    option_collect_pinewood_chops = 1
    option_collect_espers = 2
    option_random_location = 3
    default = 0


@dataclass
class FF12OpenWorldGameOptions(PerGameCommonOptions):
    shuffle_main_party: ShuffleMainParty
    character_progression_scaling: CharacterProgressionScaling
    include_treasures: IncludeTreasures
    include_chops: IncludeChops
    include_black_orbs: IncludeBlackOrbs
    include_trophy_rare_games: IncludeTrophyRareGames
    include_hunt_rewards: IncludeHuntRewards
    include_clan_hall_rewards: IncludeClanHallRewards
    allow_seitengrat: AllowSeitengrat
    bahamut_unlock: BahamutUnlock
