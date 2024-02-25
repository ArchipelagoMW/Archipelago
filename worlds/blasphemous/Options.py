from Options import Choice, Toggle, DefaultOnToggle, DeathLink, StartInventoryPool
import random


class ChoiceIsRandom(Choice):
    randomized: bool = False

    @classmethod
    def from_text(cls, text: str) -> Choice:
        text = text.lower()
        if text == "random":
            cls.randomized = True
            return cls(random.choice(list(cls.name_lookup)))
        for option_name, value in cls.options.items():
            if option_name == text:
                return cls(value)
        raise KeyError(
            f'Could not find option "{text}" for "{cls.__name__}", '
            f'known options are {", ".join(f"{option}" for option in cls.name_lookup.values())}')


class PrieDieuWarp(DefaultOnToggle):
    """Automatically unlocks the ability to warp between Prie Dieu shrines."""
    display_name = "Unlock Fast Travel"


class SkipCutscenes(DefaultOnToggle):
    """Automatically skips most cutscenes."""
    display_name = "Auto Skip Cutscenes"


class CorpseHints(DefaultOnToggle):
    """Changes the 34 corpses in game to give various hints about item locations."""
    display_name = "Corpse Hints"


class Difficulty(Choice):
    """Adjusts the overall difficulty of the randomizer, including upgrades required to defeat bosses 
    and advanced movement tricks or glitches."""
    display_name = "Difficulty"
    option_easy = 0
    option_normal = 1
    option_hard = 2
    default = 1


class Penitence(Toggle):
    """Allows one of the three Penitences to be chosen at the beginning of the game."""
    display_name = "Penitence"


class StartingLocation(ChoiceIsRandom):
    """Choose where to start the randomizer. Note that some starting locations cannot be chosen with certain 
    other options.
    Specifically, Brotherhood and Mourning And Havoc cannot be chosen if Shuffle Dash is enabled, and Grievance Ascends 
    cannot be chosen if Shuffle Wall Climb is enabled."""
    display_name = "Starting Location"
    option_brotherhood = 0
    option_albero = 1
    option_convent = 2
    option_grievance = 3
    option_knot_of_words = 4
    option_rooftops = 5
    option_mourning_havoc = 6
    default = 0


class Ending(Choice):
    """Choose which ending is required to complete the game.
    Talking to Tirso in Albero will tell you the selected ending for the current game.
    Ending A: Collect all thorn upgrades.
    Ending C: Collect all thorn upgrades and the Holy Wound of Abnegation."""
    display_name = "Ending"
    option_any_ending = 0
    option_ending_a = 1
    option_ending_c = 2
    default = 0


class SkipLongQuests(Toggle):
    """Ensures that the rewards for long quests will be filler items.
    Affected locations: \"Albero: Donate 50000 Tears\", \"Ossuary: 11th reward\", \"AtTotS: Miriam's gift\", 
    \"TSC: Jocinero's final reward\""""
    display_name = "Skip Long Quests"


class ThornShuffle(Choice):
    """Shuffles the Thorn given by Deogracias and all Thorn upgrades into the item pool."""
    display_name = "Shuffle Thorn"
    option_anywhere = 0
    option_local_only = 1
    option_vanilla = 2
    default = 0


class DashShuffle(Toggle):
    """Turns the ability to dash into an item that must be found in the multiworld."""
    display_name = "Shuffle Dash"


class WallClimbShuffle(Toggle):
    """Turns the ability to climb walls with your sword into an item that must be found in the multiworld."""
    display_name = "Shuffle Wall Climb"


class ReliquaryShuffle(DefaultOnToggle):
    """Adds the True Torment exclusive Reliquary rosary beads into the item pool."""
    display_name = "Shuffle Penitence Rewards"


class CustomItem1(Toggle):
    """Adds the custom relic Boots of Pleading into the item pool, which grants the ability to fall onto spikes 
    and survive.
    Must have the \"Blasphemous-Boots-of-Pleading\" mod installed to connect to a multiworld."""
    display_name = "Boots of Pleading"


class CustomItem2(Toggle):
    """Adds the custom relic Purified Hand of the Nun into the item pool, which grants the ability to jump 
    a second time in mid-air.
    Must have the \"Blasphemous-Double-Jump\" mod installed to connect to a multiworld."""
    display_name = "Purified Hand of the Nun"


class StartWheel(Toggle):
    """Changes the beginning gift to The Young Mason's Wheel."""
    display_name = "Start with Wheel"


class SkillRando(Toggle):
    """Randomizes the abilities from the skill tree into the item pool."""
    display_name = "Skill Randomizer"


class EnemyRando(Choice):
    """Randomizes the enemies that appear in each room.
    Shuffled: Enemies will be shuffled amongst each other, but can only appear as many times as they do in 
    a standard game.
    Randomized: Every enemy is completely random, and can appear any number of times.
    Some enemies will never be randomized."""
    display_name = "Enemy Randomizer"
    option_disabled = 0
    option_shuffled = 1
    option_randomized = 2
    default = 0


class EnemyGroups(DefaultOnToggle):
    """Randomized enemies will chosen from sets of specific groups. 
    (Weak, normal, large, flying)
    Has no effect if Enemy Randomizer is disabled."""
    display_name = "Enemy Groups"


class EnemyScaling(DefaultOnToggle):
    """Randomized enemies will have their stats increased or decreased depending on the area they appear in.
    Has no effect if Enemy Randomizer is disabled."""
    display_name = "Enemy Scaling"


class BlasphemousDeathLink(DeathLink):
    """When you die, everyone dies. The reverse is also true.
    Note that Guilt Fragments will not appear when killed by Death Link."""


blasphemous_options = {
    "prie_dieu_warp": PrieDieuWarp,
    "skip_cutscenes": SkipCutscenes,
    "corpse_hints": CorpseHints,
    "difficulty": Difficulty,
    "penitence": Penitence,
    "starting_location": StartingLocation,
    "ending": Ending,
    "skip_long_quests": SkipLongQuests,
    "thorn_shuffle" : ThornShuffle,
    "dash_shuffle": DashShuffle,
    "wall_climb_shuffle": WallClimbShuffle,
    "reliquary_shuffle": ReliquaryShuffle,
    "boots_of_pleading": CustomItem1,
    "purified_hand": CustomItem2,
    "start_wheel": StartWheel,
    "skill_randomizer": SkillRando,
    "enemy_randomizer": EnemyRando,
    "enemy_groups": EnemyGroups,
    "enemy_scaling": EnemyScaling,
    "death_link": BlasphemousDeathLink,
    "start_inventory": StartInventoryPool
}