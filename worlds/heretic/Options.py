from Options import PerGameCommonOptions, Choice, Toggle, DeathLink, DefaultOnToggle, StartInventoryPool
from dataclasses import dataclass


class Goal(Choice):
    """
    Choose the main goal.
    complete_all_levels: All levels of the selected episodes
    complete_boss_levels: Boss levels (E#M8) of selected episodes
    """
    display_name = "Goal"
    option_complete_all_levels = 0
    option_complete_boss_levels = 1
    default = 0


class Difficulty(Choice):
    """
    Choose the game difficulty. These options match Heretic's skill levels.
    wet nurse (Thou needeth a wet-nurse) - Fewer monsters and more items than medium. Damage taken is halved, and ammo pickups carry twice as much ammo. Any Quartz Flasks and Mystic Urns are automatically used when the player nears death.
    easy (Yellowbellies-r-us) - Fewer monsters and more items than medium.
    medium (Bringest them oneth) - Completely balanced, this is the standard difficulty level.
    hard (Thou art a smite-meister) - More monsters and fewer items than medium.
    black plague (Black plague possesses thee) - Same as hard, but monsters and their projectiles move much faster. Cheating is also disabled.
    """
    display_name = "Difficulty"
    option_wet_nurse = 0
    option_easy = 1
    option_medium = 2
    option_hard = 3
    option_black_plague = 4
    alias_wn = 0
    alias_yru = 1
    alias_bto = 2
    alias_sm = 3
    alias_bp = 4
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
    default = 1


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


class AllowDeathLogic(Toggle):
    """Some locations require a timed puzzle that can only be tried once.
    After which, if the player failed to get it, the location cannot be checked anymore.
    By default, no progression items are placed here. There is a way, hovewer, to still get them:
    Get killed in the current map. The map will reset, you can now attempt the puzzle again."""
    display_name = "Allow Death Logic"

    
class Pro(Toggle):
    """Include difficult tricks into rules. Mostly employed by speed runners.
    i.e.: Leaps across to a locked area, trigger a switch behind a window at the right angle, etc."""
    display_name = "Pro Heretic"


class StartWithMapScrolls(Toggle):
    """Give the player all Map Scroll items from the start."""
    display_name = "Start With Map Scrolls"


class ResetLevelOnDeath(DefaultOnToggle):
    """When dying, levels are reset and monsters respawned. But inventory and checks are kept.
    Turning this setting off is considered easy mode. Good for new players that don't know the levels well."""
    display_name = "Reset Level on Death"

    
class CheckSanity(Toggle):
    """Include redundant checks. This increase total check count for the game.
    i.e.: In a room, there might be 3 checks close to each other. By default, two of them will be remove.
    This was done to lower the total count check for Heretic, as it is quite high compared to other games.
    Check Sanity restores original checks."""
    display_name = "Check Sanity"


class Episode1(DefaultOnToggle):
    """City of the Damned.
    If none of the episodes are chosen, Episode 1 will be chosen by default."""
    display_name = "Episode 1"


class Episode2(DefaultOnToggle):
    """Hell's Maw.
    If none of the episodes are chosen, Episode 1 will be chosen by default."""
    display_name = "Episode 2"


class Episode3(DefaultOnToggle):
    """The Dome of D'Sparil.
    If none of the episodes are chosen, Episode 1 will be chosen by default."""
    display_name = "Episode 3"


class Episode4(Toggle):
    """The Ossuary.
    If none of the episodes are chosen, Episode 1 will be chosen by default."""
    display_name = "Episode 4"


class Episode5(Toggle):
    """The Stagnant Demesne.
    If none of the episodes are chosen, Episode 1 will be chosen by default."""
    display_name = "Episode 5"


@dataclass
class HereticOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    goal: Goal
    difficulty: Difficulty
    random_monsters: RandomMonsters
    random_pickups: RandomPickups
    random_music: RandomMusic
    allow_death_logic: AllowDeathLogic
    pro: Pro
    check_sanity: CheckSanity
    start_with_map_scrolls: StartWithMapScrolls
    reset_level_on_death: ResetLevelOnDeath
    death_link: DeathLink
    episode1: Episode1
    episode2: Episode2
    episode3: Episode3
    episode4: Episode4
    episode5: Episode5
