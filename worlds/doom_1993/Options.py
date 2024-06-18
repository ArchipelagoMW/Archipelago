from Options import PerGameCommonOptions, Range, Choice, Toggle, DeathLink, DefaultOnToggle, StartInventoryPool
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


class FlipLevels(Choice):
    """
    Flip levels on one axis.
    vanilla: No flipping
    flipped: All levels are flipped
    randomly_flipped: Random levels are flipped
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
    """Knee-Deep in the Dead.
    If none of the episodes are chosen, Episode 1 will be chosen by default."""
    display_name = "Episode 1"


class Episode2(DefaultOnToggle):
    """The Shores of Hell.
    If none of the episodes are chosen, Episode 1 will be chosen by default."""
    display_name = "Episode 2"


class Episode3(DefaultOnToggle):
    """Inferno.
    If none of the episodes are chosen, Episode 1 will be chosen by default."""
    display_name = "Episode 3"


class Episode4(Toggle):
    """Thy Flesh Consumed.
    If none of the episodes are chosen, Episode 1 will be chosen by default."""
    display_name = "Episode 4"


class SplitBackpack(Toggle):
    """Split the Backpack into four individual items, each one increasing ammo capacity for one type of weapon only."""
    display_name = "Split Bag of Holding"


class BackpackCount(Range):
    """How many Backpacks will be available.
    If Split Backpack is set, this will be the number of each capacity upgrade available."""
    display_name = "Backpack Count"
    range_start = 0
    range_end = 10
    default = 1


class BulletCapacity(Range):
    """Set the starting ammo capacity for bullets."""
    display_name = "Bullet Capacity"
    range_start = 200
    range_end = 999
    default = 200


class ShellCapacity(Range):
    """Set the starting ammo capacity for shotgun shells."""
    display_name = "Shotgun Shell Capacity"
    range_start = 50
    range_end = 999
    default = 50


class RocketCapacity(Range):
    """Set the starting ammo capacity for rockets."""
    display_name = "Rocket Capacity"
    range_start = 50
    range_end = 999
    default = 50


class EnergyCellCapacity(Range):
    """Set the starting ammo capacity for energy cells."""
    display_name = "Energy Cell Capacity"
    range_start = 300
    range_end = 999
    default = 300


class BulletIncrease(Range):
    """Set the amount of bullet capacity gained when collecting a backpack."""
    display_name = "Bullet Backpack Increase"
    range_start = 20
    range_end = 999
    default = 200


class ShellIncrease(Range):
    """Set the amount of shotgun shell capacity gained when collecting a backpack."""
    display_name = "Shotgun Shell Backpack Increase"
    range_start = 5
    range_end = 999
    default = 50


class RocketIncrease(Range):
    """Set the amount of rocket capacity gained when collecting a backpack."""
    display_name = "Rocket Backpack Increase"
    range_start = 5
    range_end = 999
    default = 50


class EnergyCellIncrease(Range):
    """Set the amount of energy cell capacity gained when collecting a backpack."""
    display_name = "Energy Cell Backpack Increase"
    range_start = 30
    range_end = 999
    default = 300


@dataclass
class DOOM1993Options(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    goal: Goal
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
    episode4: Episode4

    split_backpack: SplitBackpack
    backpack_count: BackpackCount
    bullet_capacity: BulletCapacity
    bullet_backpack_increase: BulletIncrease
    shell_capacity: ShellCapacity
    shell_backpack_increase: ShellIncrease
    rocket_capacity: RocketCapacity
    rocket_backpack_increase: RocketIncrease
    energy_cell_capacity: EnergyCellCapacity
    energy_cell_backpack_increase: EnergyCellIncrease

