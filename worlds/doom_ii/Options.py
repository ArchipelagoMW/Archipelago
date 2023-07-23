import typing

from Options import AssembleOptions, Choice, Toggle, DeathLink, DefaultOnToggle, StartInventoryPool


class Difficulty(Choice):
    """
    Choose the difficulty option. Those match DOOM's difficulty options.
    baby (I'm too young to die.) double ammos, half damage, less monsters or strength.
    easy (Hey, not too rough.) less monsters or strength.
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


options: typing.Dict[str, AssembleOptions] = {
    "start_inventory_from_pool": StartInventoryPool,
    "difficulty": Difficulty,
    "random_monsters": RandomMonsters,
    "random_pickups": RandomPickups,
    "flip_levels": FlipLevels,
    "allow_death_logic": AllowDeathLogic,
    "pro": Pro,
    "start_with_computer_area_maps": StartWithComputerAreaMaps,
    "death_link": DeathLink
}
