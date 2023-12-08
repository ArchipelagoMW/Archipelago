from Options import Choice, FreeText, Toggle, Range


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
    display_name = "Logic"


class BrownBoxes(Choice):
    """Include the 201 brown box locations from the original game. Brown Boxes are all the boxes that contained a
    consumable in the original game. If shuffle is chosen, the consumables contained will be shuffled but the brown
    boxes will not be Archipelago location checks."""
    option_exclude = 0
    option_include = 1
    option_shuffle = 2
    default = 1
    display_name = "Brown Boxes"


class SkyCoinMode(Choice):
    """Configure how the Sky Coin is acquired. With standard, the Sky Coin will be placed randomly. With Start With, the
    Sky Coin will be in your inventory at the start of the game. With Save The Crystals, the Sky Coin will be acquired
    once you save all 4 crystals. With Shattered Sky Coin, the Sky Coin is split in 40 fragments; you can enter Doom
    Castle once the required amount is found. Shattered Sky Coin will force brown box locations to be included."""
    option_standard = 0
    option_start_with = 1
    option_save_the_crystals = 2
    option_shattered_sky_coin = 3
    default = 0
    display_name = "Sky Coin Mode"


class ShatteredSkyCoinQuantity(Choice):
    """Configure the number of the 40 Sky Coin Fragments required to enter the Doom Castle. Only has an effect if
    Sky Coin Mode is set to shattered. Low: 16. Mid: 24. High: 32. Random Narrow: random between 16 and 32.
    Random Wide: random between 10 and 38."""
    option_low_16 = 0
    option_mid_24 = 1
    option_high_32 = 2
    option_random_narrow = 3
    option_random_wide = 4
    default = 1
    display_name = "Shattered Sky Coin"


class StartingWeapon(Choice):
    """Choose your starting weapon."""
    display_name = "Starting Weapon"
    option_steel_sword = 0
    option_axe = 1
    option_cat_claw = 2
    option_bomb = 3
    default = "random"


class ProgressiveGear(Toggle):
    """Pieces of gear are always acquired from weakest to strongest in a set."""
    display_name = "Progressive Gear"


class EnemiesDensity(Choice):
    """Set how many of the original enemies are on each map."""
    display_name = "Enemies Density"
    option_all = 0
    option_three_quarter = 1
    option_half = 2
    option_quarter = 3
    option_none = 4


class EnemyScaling(Choice):
    """Superclass for enemy scaling options."""
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
    """Randomly adjust enemies stats by the selected range percentage. Include mini-bosses' weaker clones."""
    display_name = "Enemies Scaling Lower"
    default = 0


class EnemiesScalingUpper(EnemyScaling):
    """Randomly adjust enemies stats by the selected range percentage. Include mini-bosses' weaker clones."""
    display_name = "Enemies Scaling Upper"
    default = 4


class BossesScalingLower(EnemyScaling):
    """Randomly adjust bosses stats by the selected range percentage. Include Mini-Bosses, Bosses, Bosses' refights and
    the Dark King."""
    display_name = "Bosses Scaling Lower"
    default = 0


class BossesScalingUpper(EnemyScaling):
    """Randomly adjust bosses stats by the selected range percentage. Include Mini-Bosses, Bosses, Bosses' refights and
    the Dark King."""
    display_name = "Bosses Scaling Upper"
    default = 4


class EnemizerAttacks(Choice):
    """Shuffles enemy attacks. Standard: No shuffle. Safe: Randomize every attack but leave out self-destruct and Dark
    King attacks. Chaos: Randomize and include self-destruct and Dark King attacks. Self Destruct: Every enemy
    self-destructs. Simple Shuffle: Instead of randomizing, shuffle one monster's attacks to another. Dark King is left
    vanilla."""
    display_name = "Enemizer Attacks"
    option_normal = 0
    option_safe = 1
    option_chaos = 2
    option_self_destruct = 3
    option_simple_shuffle = 4
    default = 0


class EnemizerGroups(Choice):
    """Set which enemy groups will be affected by Enemizer."""
    display_name = "Enemizer Groups"
    option_mobs_only = 0
    option_mobs_and_bosses = 1
    option_mobs_bosses_and_dark_king = 2
    default = 1


class ShuffleResWeakType(Toggle):
    """Resistance and Weakness types are shuffled for all enemies."""
    display_name = "Shuffle Resistance/Weakness Types"
    default = 0


class ShuffleEnemiesPositions(Toggle):
    """Instead of their original position in a given map, enemies are randomly placed."""
    display_name = "Shuffle Enemies' Positions"
    default = 1


class ProgressiveFormations(Choice):
    """Enemies' formations are selected by regions, with the weakest formations always selected in Foresta and the
    strongest in Windia. Disabled: Standard formations are used. Regions Strict: Formations will come exclusively
    from the current region, whatever the map is. Regions Keep Type: Formations will keep the original formation type
    and match with the nearest power level."""
    display_name = "Progressive Formations"
    option_disabled = 0
    option_regions_strict = 1
    option_regions_keep_type = 2


class DoomCastle(Choice):
    """Configure how you reach the Dark King. With Standard, you need to defeat all four bosses and their floors to
    reach the Dark King. With Boss Rush, only the bosses are blocking your way in the corridor to the Dark King's room.
    With Dark King Only, the way to the Dark King is free of any obstacle."""
    display_name = "Doom Castle"
    option_standard = 0
    option_boss_rush = 1
    option_dark_king_only = 2


class DoomCastleShortcut(Toggle):
    """Create a shortcut granting access from the start to Doom Castle at Focus Tower's entrance.
    Also modify the Desert floor, so it can be navigated without the Mega Grenades and the Dragon Claw."""
    display_name = "Doom Castle Shortcut"


class TweakFrustratingDungeons(Toggle):
    """Make some small changes to a few of the most annoying dungeons. Ice Pyramid: Add 3 shortcuts on the 1st floor.
    Giant Tree: Add shortcuts on the 1st and 4th floors and curtail mushrooms population.
    Pazuzu's Tower: Staircases are devoid of enemies (regardless of Enemies Density settings)."""
    display_name = "Tweak Frustrating Dungeons"


class MapShuffle(Choice):
    """None: No shuffle. Overworld: Only shuffle the Overworld locations. Dungeons: Only shuffle the dungeons' floors
    amongst themselves. Temples and Towns aren't included. Overworld And Dungeons: Shuffle the Overworld and dungeons
    at the same time. Everything: Shuffle the Overworld, dungeons, temples and towns all amongst each others.
    When dungeons are shuffled, defeating Pazuzu won't teleport you to the 7th floor, you have to get there normally to
    save the Crystal and get Pazuzu's Chest."""
    display_name = "Map Shuffle"
    option_none = 0
    option_overworld = 1
    option_dungeons = 2
    option_overworld_and_dungeons = 3
    option_everything = 4
    default = 0


class CrestShuffle(Toggle):
    """Shuffle the Crest tiles amongst themselves."""
    display_name = "Crest Shuffle"


class MapShuffleSeed(FreeText):
    """If this is a number, it will be used as a set seed number for Map, Crest, and Battlefield Reward shuffles.
    If this is "random" the seed will be chosen randomly. If it is any other text, it will be used as a seed group name.
    All players using the same seed group name will get the same shuffle results, as long as their Map Shuffle,
    Crest Shuffle, and Shuffle Battlefield Rewards settings are the same."""
    display_name = "Map Shuffle Seed"
    default = "random"


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
    default = 4


class ShuffleBattlefieldRewards(Toggle):
    """Shuffle the type of reward (Item, XP, GP) given by battlefields and color code them by reward type.
    Blue: Give an item. Grey: Give XP. Green: Give GP."""
    display_name = "Shuffle Battlefield Rewards"


class BattlefieldsBattlesQuantities(Choice):
    """Adjust the number of battles that need to be fought to get a battlefield's reward."""
    display_name = "Battlefields Battles Quantity"
    option_ten = 0
    option_seven = 1
    option_five = 2
    option_three = 3
    option_one = 4
    option_random_one_through_five = 5
    option_random_one_through_ten = 6


class CompanionLevelingType(Choice):
    """Set how companions gain levels.
    Quests: Complete each companion's individual quest for them to promote to their second version.
    Quests Extended: Each companion has four exclusive quests, leveling each time a quest is completed.
    Save the Crystals (All): Each time a Crystal is saved, all companions gain levels.
    Save the Crystals (Individual): Each companion will level to their second version when a specific Crystal is saved.
    Benjamin Level: Companions' level tracks Benjamin's."""
    option_quests = 0
    option_quests_extended = 1
    option_save_crystals_individual = 2
    option_save_crystals_all = 3
    option_benjamin_level = 4
    option_benjamin_level_plus_5 = 5
    option_benjamin_level_plus_10 = 6
    default = 0
    display_name = "Companion Leveling Type"


class CompanionSpellbookType(Choice):
    """Update companions' spellbook.
    Standard: Original game spellbooks.
    Standard Extended: Add some extra spells. Tristam gains Exit and Quake and Reuben gets Blizzard.
    Random Balanced: Randomize the spellbooks with an appropriate mix of spells.
    Random Chaos: Randomize the spellbooks in total free-for-all."""
    option_standard = 0
    option_standard_extended = 1
    option_random_balanced = 2
    option_random_chaos = 3
    default = 0
    display_name = "Companion Spellbook Type"


class StartingCompanion(Choice):
    """Set a companion to start with.
    Random Companion: Randomly select one companion.
    Random Plus None: Randomly select a companion, with the possibility of none selected."""
    display_name = "Starting Companion"
    default = 0
    option_none = 0
    option_kaeli = 1
    option_tristam = 2
    option_phoebe = 3
    option_reuben = 4
    option_random_companion = 5
    option_random_plus_none = 6


class AvailableCompanions(Range):
    """Select randomly which companions will join your party. Unavailable companions can still be reached to get their items and complete their quests if needed.
    Note: If a Starting Companion is selected, it will always be available, regardless of this setting."""
    display_name = "Available Companions"
    default = 4
    range_start = 0
    range_end = 4


class CompanionsLocations(Choice):
    """Set the primary location of companions. Their secondary location is always the same.
    Standard: Companions will be at the same locations as in the original game.
    Shuffled: Companions' locations are shuffled amongst themselves.
    Shuffled Extended: Add all the Temples, as well as Phoebe's House and the Rope Bridge as possible locations."""
    display_name = "Companions' Locations"
    default = 0
    option_standard = 0
    option_shuffled = 1
    option_shuffled_extended = 2


class KaelisMomFightsMinotaur(Toggle):
    """Transfer Kaeli's requirements (Tree Wither, Elixir) and the two items she's giving to her mom.
    Kaeli will be available to join the party right away without the Tree Wither."""
    display_name = "Kaeli's Mom Fights Minotaur"
    default = 0


option_definitions = {
    "logic": Logic,
    "brown_boxes": BrownBoxes,
    "sky_coin_mode": SkyCoinMode,
    "shattered_sky_coin_quantity": ShatteredSkyCoinQuantity,
    "starting_weapon": StartingWeapon,
    "progressive_gear": ProgressiveGear,
    "leveling_curve": LevelingCurve,
    "starting_companion": StartingCompanion,
    "available_companions": AvailableCompanions,
    "companions_locations": CompanionsLocations,
    "kaelis_mom_fight_minotaur": KaelisMomFightsMinotaur,
    "companion_leveling_type": CompanionLevelingType,
    "companion_spellbook_type": CompanionSpellbookType,
    "enemies_density": EnemiesDensity,
    "enemies_scaling_lower": EnemiesScalingLower,
    "enemies_scaling_upper": EnemiesScalingUpper,
    "bosses_scaling_lower": BossesScalingLower,
    "bosses_scaling_upper": BossesScalingUpper,
    "enemizer_attacks": EnemizerAttacks,
    "enemizer_groups": EnemizerGroups,
    "shuffle_res_weak_types": ShuffleResWeakType,
    "shuffle_enemies_position": ShuffleEnemiesPositions,
    "progressive_formations": ProgressiveFormations,
    "doom_castle_mode": DoomCastle,
    "doom_castle_shortcut": DoomCastleShortcut,
    "tweak_frustrating_dungeons": TweakFrustratingDungeons,
    "map_shuffle": MapShuffle,
    "crest_shuffle": CrestShuffle,
    "shuffle_battlefield_rewards": ShuffleBattlefieldRewards,
    "map_shuffle_seed": MapShuffleSeed,
    "battlefields_battles_quantities": BattlefieldsBattlesQuantities,
}
