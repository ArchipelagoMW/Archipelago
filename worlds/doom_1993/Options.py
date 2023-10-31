import typing

from Options import AssembleOptions, Choice, Toggle, DeathLink, DefaultOnToggle


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
    """
    display_name = "Random Monsters"
    option_vanilla = 0
    option_shuffle = 1
    option_random_balanced = 2
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


class AllowDeathLogic(Toggle):
    """Some locations require a timed puzzle that can only be tried once.
    After which, if the player failed to get it, the location cannot be checked anymore.
    By default, no progression items are placed here. There is a way, hovewer, to still get them:
    Get killed in the current map. The map will reset, you can now attempt the puzzle again."""
    display_name = "Allow Death Logic"


class StartWithComputerAreaMaps(Toggle):
    """Give the player all Computer Area Map items from the start."""
    display_name = "Start With Computer Area Maps"


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


options: typing.Dict[str, AssembleOptions] = {
    "difficulty": Difficulty,
    "random_monsters": RandomMonsters,
    "random_pickups": RandomPickups,
    "allow_death_logic": AllowDeathLogic,
    "start_with_computer_area_maps": StartWithComputerAreaMaps,
    "death_link": DeathLink,
    "episode1": Episode1,
    "episode2": Episode2,
    "episode3": Episode3,
    "episode4": Episode4
}
