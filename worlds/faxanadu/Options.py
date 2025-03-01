from Options import PerGameCommonOptions, Toggle, DefaultOnToggle, StartInventoryPool, Choice
from dataclasses import dataclass


class KeepShopRedPotions(Toggle):
    """
    Prevents the Shop's Red Potions from being shuffled. Those locations
    will have purchasable Red Potion as usual for their usual price.
    """
    display_name = "Keep Shop Red Potions"


class IncludePendant(Toggle):
    """
    Pendant is an item that boosts your attack power permanently when picked up.
    However, due to a programming error in the original game, it has the reverse
    effect. You start with the Pendant power, and lose it when picking
    it up. So this item is essentially a trap.
    There is a setting in the client to reverse the effect back to its original intend.
    This could be used in conjunction with this option to increase or lower difficulty.
    """
    display_name = "Include Pendant"


class IncludePoisons(DefaultOnToggle):
    """
    Whether or not to include Poison Potions in the pool of items. Including them
    effectively turn them into traps in multiplayer.
    """
    display_name = "Include Poisons"


class RequireDragonSlayer(Toggle):
    """
    Requires the Dragon Slayer to be available before fighting the final boss is required.
    Turning this on will turn Progressive Shields into progression items.

    This setting does not force you to use Dragon Slayer to kill the final boss.
    Instead, it ensures that you will have the Dragon Slayer and be able to equip
    it before you are expected to beat the final boss.
    """
    display_name = "Require Dragon Slayer"


class RandomMusic(Toggle):
    """
    All levels' music is shuffled. Except the title screen because it's finite.
    This is an aesthetic option and doesn't affect gameplay.
    """
    display_name = "Random Musics"


class RandomSound(Toggle):
    """
    All sounds are shuffled.
    This is an aesthetic option and doesn't affect gameplay.
    """
    display_name = "Random Sounds"


class RandomNPC(Toggle):
    """
    NPCs and their portraits are shuffled.
    This is an aesthetic option and doesn't affect gameplay.
    """
    display_name = "Random NPCs"


class RandomMonsters(Choice):
    """
    Choose how monsters are randomized.
    "Vanilla": No randomization
    "Level Shuffle": Monsters are shuffled within a level
    "Level Random": Monsters are picked randomly, balanced based on the ratio of the current level
    "World Shuffle": Monsters are shuffled across the entire world
    "World Random": Monsters are picked randomly, balanced based on the ratio of the entire world
    "Chaotic": Completely random, except big vs small ratio is kept. Big are mini-bosses.
    """
    display_name = "Random Monsters"
    option_vanilla = 0
    option_level_shuffle = 1
    option_level_random = 2
    option_world_shuffle = 3
    option_world_random = 4
    option_chaotic = 5
    default = 0


class RandomRewards(Toggle):
    """
    Monsters drops are shuffled.
    """
    display_name = "Random Rewards"


@dataclass
class FaxanaduOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    keep_shop_red_potions: KeepShopRedPotions
    include_pendant: IncludePendant
    include_poisons: IncludePoisons
    require_dragon_slayer: RequireDragonSlayer
    random_musics: RandomMusic
    random_sounds: RandomSound
    random_npcs: RandomNPC
    random_monsters: RandomMonsters
    random_rewards: RandomRewards
