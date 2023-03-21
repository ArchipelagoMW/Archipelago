from Options import Choice, Range, Toggle


class Logic(Choice):
    """Placement logic sets the rules that will be applied when placing items. Friendly: Required Items to clear a
    dungeon will never be placed in that dungeon to avoid the need to revisit it. Also, the Magic Mirror and the Mask
    will always be available before Ice Pyramid and Volcano, respectively. Note: If Dungeons are shuffled, Friendly
    logic will only ensure the availability of the Mirror and the Mask. Standard: Items are randomly placed and logic
    merely verifies that they're all accessible. As for Region access, only the Coins are considered. Expert: Same as
    Standard, but Items Placement logic also includes other routes than Coins: the Crests Teleporters, the
    Fireburg-Aquaria Lava bridge and the Sealed Temple Exit trick."""
    option_friendly = 0
    option_standard = 1
    option_expert = 2
    default = 1


class OriginalChests(Toggle):
    """Prioritize the original 29 red chest locations. Does not include the Venus Key Chest in Focus Tower or the new
    locked chest in Spencer's Place. If enabled, they will all be guaranteed to have progression or useful items.
    However, if brown boxes are also included, 87 non-prioritized locations will be forced to contain unimportant filler
    items."""
    default = 0


class NPCs(Toggle):
    """Prioritize the 16 NPC locations. These include the NPC locations from the original game, as well as the new
    Rueben item in the Mine, the Venus Key Chest in Focus Tower, and the new locked chest in Spencer's Place.
    If enabled, they will all be guaranteed to have progression or useful items. However, if brown boxes
    are also included, 48 non-prioritized locations will be forced to contain unimportant filler items"""
    default = 0


class Battlefields(Toggle):
    """Prioritize the 5 Battlefield locations. Battlefields are all the battlefields that gave a quest item in the
    original game. If Shuffle Battlefields Rewards is enabled, the locations will change, but the same number of
    battlefields will offer an item. If enabled, they will all be guaranteed to have progression or useful items.
    However, if brown boxes are also included, 15 non-prioritized locations will be forced to contain unimportant
    filler items"""
    default = 0


class BrownBoxes(Choice):
    """Include the 201 brown box locations from the original game. Brown Boxes are all the boxes that contained a
    consumable in the original game. If shuffle is chosen, the consumables contained will be shuffled but the brown
    boxes will not be Archipelago location checks."""
    option_exclude = 0
    option_include = 1
    option_shuffle = 2
    default = 2


class SkyCoinMode(Choice):
    """Configure how the Sky Coin is acquired. With standard, the Sky Coin will placed randomly. With start_with, the
    Sky Coin will be in your inventory at the start of the game. With save_the_crystals, the Sky Coin will be acquired
    once you save all 4 crystals. With shattered, the Sky Coin is split in 40 fragments; you can enter Doom Castle once
    the required amount is found.
    shattered will force brown box locations to be included."""
    option_standard = 0
    option_start_with = 1
    option_save_the_crystals = 2
    option_shattered = 3
    default = 0


class ShatteredSkyCoinQuantity(Range):
    """Configure the number of the 40 Sky Coin Fragments required to enter the Doom Castle. Only has an effect if
    sky_coin_mode is set to shattered. low: 16. mid: 24. high: 32. random_narrow: random between 16 and 32.
    random_wide: random between 10 and 38"""
    option_low_16 = 0
    option_mid_24 = 1
    option_high_32 = 2
    option_random_narrow = 3
    option_random_wide = 4
    default = 1


class StartingWeapon(Choice):
    option_steel_sword = 0
    option_axe = 1
    option_cat_claw = 2
    option_bomb = 3
    default = "random"


class ProgressiveGear(Toggle):
    """"""


class EnemiesDensity(Choice):
    """Set how many of the original enemies are on each map."""
    display_name = "Enemies Density"
    option_all = 0
    option_three_quarter = 1
    option_half = 2
    option_quarter = 3
    option_none = 4


class EnemyScaling(Choice):
    option_quarter = 0
    option_half = 1
    option_three_quarter = 2
    option_normal = 3
    option_one_and_quarter = 4
    option_one_and_half = 5
    option_double = 6
    option_double_and_half = 7
    option_triple = 8


class EnemiesScalingLower(EnemyScaling):
    display_name = "Enemies Scaling Lower"
    default = 0


class EnemiesScalingUpper(EnemyScaling):
    display_name = "Enemies Scaling Upper"
    default = 4


class BossesScalingLower(EnemyScaling):
    display_name = "Bosses Scaling Lower"
    default = 0


class BossesScalingUpper(EnemyScaling):
    display_name = "Bosses Scaling Upper"
    default = 4


class EnemizerAttacks(Choice):
    """Shuffles enemy attacks. standard: No shuffle. safe: Randomize every attack but leave out self-destruct and Dark
    King attacks. chaos: Randomize and include self-destruct and Dark King attacks. self_destruct: Every enemy
    self-destructs. simple_shuffle: Instead of randomizing, shuffle one monster's attacks to another. Dark King is left
    vanilla."""
    display_name = "Enemizer Attacks"
    option_normal = 0
    option_safe = 1
    option_chaos = 2
    option_self_destruct = 3
    option_simple_shuffle = 4
    default = 0


class ShuffleEnemiesPositions(Toggle):
    """Instead of their original position in a given map, enemies are randomly placed."""
    display_name = "Shuffle Enemies' Positions"
    default = 1


class ProgressiveFormations(Choice):
    """Enemies' formations are selected by regions, with the weakest formations always selected in Foresta and the
    strongest in Windia. disabled: Standard formations are used. by_regions_strict: Formations will come exclusively
    from the current region, whatever the map is. by_regions_keep_type: Formations will keep the original formation type
    and match with the nearest power level."""
    display_name = "Progressive Formations"
    option_disabled = 0
    option_by_regions_strict = 1
    option_by_regions_keep_type = 2


class DoomCastle(Choice):
    """Change how you reach the Dark King. With standard, you need to defeat all four bosses and their floors to reach
    the Dark King. With boss_rush, only the bosses are blocking your way in the corridor to the Dark King's room.
    With dark_king_only, the way to the Dark King is free of any obstacle."""
    display_name = "Doom Castle"
    option_standard = 0
    option_boss_rush = 1
    option_dark_king_only = 2


class TweakFrustratingDungeons(Toggle):
    """Make some small changes to a few of the most annoying dungeons. Ice Pyramid: Add 3 shortcuts on the 1st floor.
    Giant Tree: Add shortcuts on the 1st and 4th floors and curtail mushrooms population.
    Pazuzu's Tower: Staircases are devoid of enemies (regardless of Enemies Density settings)."""
    display_name = "Tweak Frustrating Dungeons"


class MapShuffle(Choice):
    """"""
    display_name = "Map Shuffle"
    option_none = 0


class CrestShuffle(Toggle):
    """Shuffle the Crest tiles amongst themselves."""
    display_name = "Crest Shuffle"


class LevelingCurve(Choice):
    """Adjust the level gain rate."""
    display_name = "Leveling Curve"
    option_half = 0
    option_normal = 1
    option_one_and_half = 2
    option_double = 3
    option_double_and_half = 4
    option_triple = 5
    option_quadruple = 6


class ShuffleBattlefieldRewards(Toggle):
    """Shuffle the type of reward (Item, XP, GP) given by battlefields and color code them by reward type.
    Blue: Give an item. Grey: Give XP. Green: Give GP."""
    display_name = "Shuffle Battlefield Rewards"


class BattlefieldsBattlesQuantities(Choice):
    option_ten = 0
    option_seven = 1
    option_five = 2
    option_three = 3
    option_one = 4
    option_random_one_through_five = 5
    option_random_one_through_ten = 6


class RandomizeBenjaminsPalette(Toggle):
    """Randomly select Benjamin's palette, giving him a brand new look!"""
    display_name = "Randomize Benjamin's Palette"


class RandomizeMusic(Toggle):
    """Shuffle the music tracks."""
    display_name = "Randomize Music"

option_definitions = {
    "logic": Logic,
    "prioritize_chests": OriginalChests,
    "prioritize_npcs": NPCs,
    "prioritize_battlefields": Battlefields,
    "brown_boxes": BrownBoxes,
    "sky_coin_mode": SkyCoinMode,
    "shattered_sky_coin_quantity": ShatteredSkyCoinQuantity,
    "starting_weapon": StartingWeapon,
    "progressive_gear": ProgressiveGear,
    "enemies_density": EnemiesDensity,
    "enemies_scaling_lower": EnemiesScalingLower,
    "enemies_scaling_upper": EnemiesScalingUpper,
    "bosses_scaling_lower": BossesScalingLower,
    "bosses_scaling_upper": BossesScalingUpper,
    "enemizer_attacks": EnemizerAttacks,
    "shuffle_enemies_position": ShuffleEnemiesPositions,
    "progressive_formations": ProgressiveFormations,
    "doom_castle": DoomCastle,
    "tweak_frustrating_dungeons": TweakFrustratingDungeons,
    "map_shuffle": MapShuffle,
    "crest_shuffle": CrestShuffle,
    "leveling_curve": LevelingCurve,
    "shuffle_battlefield_rewards": ShuffleBattlefieldRewards,
    "battlefields_battles_quantities": BattlefieldsBattlesQuantities,
    "randomize_benjamins_palette": RandomizeBenjaminsPalette,
    "randomize_music": RandomizeMusic


}