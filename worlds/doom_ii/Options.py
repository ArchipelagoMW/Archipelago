import typing

from Options import PerGameCommonOptions, Choice, Toggle, DeathLink, DefaultOnToggle, StartInventoryPool
from dataclasses import dataclass


class Difficulty(Choice):
    """
    Choose the game difficulty. These options match DOOM's skill levels.
    baby (I'm too young to die.) Same as easy, with double ammo pickups and half damage taken.
    easy (Hey, not too rough.) Less monsters or strength.
    medium (Hurt me plenty.) Default.
    hard (Ultra-Violence.) More monsters or strength.
    nightmare (Nightmare!) Monsters attack more rapidly and respawn.
    """
    display_name = "Difficulty"
    option_baby = 0
    option_easy = 1
    option_medium = 2
    option_hard = 3
    option_nightmare = 4
    alias_itytd = 0
    alias_hntr = 1
    alias_hmp = 2
    alias_uv = 3
    alias_nm = 4
    default = 2


class RandomMonsters(Choice):
    """
    Choose how monsters are randomized.
    vanilla: No randomization
    shuffle: Monsters are shuffled within the level
    random_balanced: Monsters are completely randomized, but balanced based on existing ratio in the level. (Small monsters vs medium vs big)
    random_chaotic: Monsters are completely randomized, but balanced based on existing ratio in the entire game.
    """
    display_name = "Random Monsters"
    option_vanilla = 0
    option_shuffle = 1
    option_random_balanced = 2
    option_random_chaotic = 3
    default = 2


class RandomPickups(Choice):
    """
    Choose how pickups are randomized.
    vanilla: No randomization
    shuffle: Pickups are shuffled within the level
    random_balanced: Pickups are completely randomized, but balanced based on existing ratio in the level. (Small pickups vs Big)
    """
    display_name = "Random Pickups"
    option_vanilla = 0
    option_shuffle = 1
    option_random_balanced = 2
    default = 1


class RandomMusic(Choice):
    """
    Level musics will be randomized.
    vanilla: No randomization
    shuffle_selected: Selected episodes' levels will be shuffled
    shuffle_game: All the music will be shuffled
    """
    display_name = "Random Music"
    option_vanilla = 0
    option_shuffle_selected = 1
    option_shuffle_game = 2
    default = 0
    

class FlipLevels(Choice):
    """
    Flip levels on one axis.
    vanilla: No flipping
    flipped: All levels are flipped
    random: Random levels are flipped
    """
    display_name = "Flip Levels"
    option_vanilla = 0
    option_flipped = 1
    option_randomly_flipped = 2
    default = 0


class AllowDeathLogic(Toggle):
    """Some locations require a timed puzzle that can only be tried once.
    After which, if the player failed to get it, the location cannot be checked anymore.
    By default, no progression items are placed here. There is a way, hovewer, to still get them:
    Get killed in the current map. The map will reset, you can now attempt the puzzle again."""
    display_name = "Allow Death Logic"

    
class Pro(Toggle):
    """Include difficult tricks into rules. Mostly employed by speed runners.
    i.e.: Leaps across to a locked area, trigger a switch behind a window at the right angle, etc."""
    display_name = "Pro Doom"


class StartWithComputerAreaMaps(Toggle):
    """Give the player all Computer Area Map items from the start."""
    display_name = "Start With Computer Area Maps"


class ResetLevelOnDeath(DefaultOnToggle):
    """When dying, levels are reset and monsters respawned. But inventory and checks are kept.
    Turning this setting off is considered easy mode. Good for new players that don't know the levels well."""
    display_name = "Reset Level on Death"


class Episode1(DefaultOnToggle):
    """Subterranean and Outpost.
    If none of the episodes are chosen, Episode 1 will be chosen by default."""
    display_name = "Episode 1"


class Episode2(DefaultOnToggle):
    """City.
    If none of the episodes are chosen, Episode 1 will be chosen by default."""
    display_name = "Episode 2"


class Episode3(DefaultOnToggle):
    """Hell.
    If none of the episodes are chosen, Episode 1 will be chosen by default."""
    display_name = "Episode 3"


class SecretLevels(Toggle):
    """Secret levels.
    This is too short to be an episode. It's additive.
    Another episode will have to be selected along with this one.
    Otherwise episode 1 will be added."""
    display_name = "Secret Levels"


@dataclass
class DOOM2Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    difficulty: Difficulty
    random_monsters: RandomMonsters
    random_pickups: RandomPickups
    random_music: RandomMusic
    flip_levels: FlipLevels
    allow_death_logic: AllowDeathLogic
    pro: Pro
    start_with_computer_area_maps: StartWithComputerAreaMaps
    death_link: DeathLink
    reset_level_on_death: ResetLevelOnDeath
    episode1: Episode1
    episode2: Episode2
    episode3: Episode3
    episode4: SecretLevels
