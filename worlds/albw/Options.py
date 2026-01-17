from dataclasses import dataclass
from typing import Dict
from Options import PerGameCommonOptions, Choice, Range, Toggle
import albwrandomizer

class LogicMode(Choice):
    """Logic to use for item placement.
    normal: Standard gameplay, no tricky item use or glitches. If unsure, choose this.
    hard: Adds tricks that aren't technically glitches. Lamp + Net considered as weapons. No glitches.
    glitched: Includes the above plus a selection of easy-to-learn glitches.
    adv_glitched: Includes the above plus "advanced" glitches that may be a challenge to master.
    hell: Includes every known RTA-viable glitch. Don't choose this."""
    display_name = "Logic Mode"
    option_normal = 0
    option_hard = 1
    option_glitched = 2
    option_adv_glitched = 3
    option_hell = 4
    default = 0

class RandomizeDungeonPrizes(Toggle):
    """This shuffles all Sage Portraits and Pendants among themselves."""
    display_name = "Randomize Dungeon Prizes"

class LoruleCastleRequirement(Range):
    """Choose how many Portraits are needed to enter Lorule Castle and fight Yuganon."""
    display_name = "Lorule Castle Requirement"
    range_start = 0
    range_end = 7
    default = 7

class PedestalRequirement(Choice):
    """Choose which Pendants are required to reach the Master Sword Pedestal.
    vanilla: Only the Pendants of Power and Wisdom are required.
    standard: All Pendants are required."""
    display_name = "Pedestal Requirement"
    option_vanilla = 0
    option_standard = 1
    default = 1

class NiceItems(Choice):
    """Choose how to handle Nice Items.
    vanilla: Nice Items are obtained as upgrades from Mother Maiamai.
    shuffled: Freely shuffles two progressive copies of each Ravio Item.
    off: Removes Nice Items from the game."""
    display_name = "Nice Items"
    option_vanilla = 0
    option_shuffled = 1
    option_off = 2
    default = 0

class SuperItems(Toggle):
    """This shuffles a second progressive copy of the Lamp and Net into the general item pool."""
    display_name = "Super Items"

class LampAndNetAsWeapons(Toggle):
    """Treat the base Lamp and Net as damage-dealing weapons?
    - The red base Lamp and Net each deal 1/2 the damage of the Forgotten Sword (i.e. they're VERY BAD weapons).
    - The blue Super Lamp and Super Net each deal 4 damage (same as MS Lv3) and are always considered weapons, regardless of this setting."""
    display_name = "Lamp and Net as Weapons"

class NoProgressionEnemies(Toggle):
    """Removes Enemies from dungeons that are themselves Progression (e.g.: Bawbs, the bomb enemy).
    Logic will be adjusted to require the player's items instead."""
    display_name = "No Progression Enemies"

class AssuredWeapon(Toggle):
    """"If enabled at least one weapon is guaranteed to be placed in Ravio's Shop."""
    display_name = "Assured Weapon"

class MaiamaiMayhem(Toggle):
    """This shuffles Maiamai into the pool, adding 100 more locations."""
    display_name = "Maiamai Mayhem"

class InitialCrackState(Choice):
    """Choose the initial Crack state:
    closed: All Cracks except the Hyrule Castle Crack (and its pair) remain closed until the Quake Item is found.
    open: All Cracks are open from the start of the game, and the Quake Item is not in the item pool."""
    display_name = "Initial Crack State"
    option_closed = 0
    option_open = 1
    default = 1

class CrackShuffle(Choice):
    """Choose how to shuffle Cracks:
    off: Cracks are not shuffled.
    cross_world_pairs: Cracks are shuffled, but remain in Hyrule/Lorule pairs.
    any_world_pairs: Cracks are shuffled freely, and can lead to the same or opposite world.
    mirrored_cross_world_pairs: Same as Cross World Pairs, but each pair's vanilla counterparts will be in a matching pair.
    mirrored_any_world_pairs: Same as Any World Pairs, but each pair's vanilla counterparts will be in a matching pair."""
    display_name = "Crack Shuffle"
    option_off = 0
    option_cross_world_pairs = 1
    option_any_world_pairs = 2
    option_mirrored_cross_world_pairs = 3
    option_mirrored_any_world_pairs = 4
    default = 0

class MinigamesExcluded(Toggle):
    """Excludes the following: Octoball Derby, Dodge the Cuccos, Hyrule Hotfoot, Treacherous Tower, and both Rupee Rushes."""
    display_name = "Minigames Excluded"

class SkipBigBombFlower(Toggle):
    """Skips the Big Bomb Flower by removing the 5 Big Rocks in Lorule Field.
    (Does not affect Lorule Castle Bomb Trial)"""
    display_name = "Skip Big Bomb Flower"

class TrialsRequired(Range):
    """Choose the number of (randomly selected) trials required to open the Lorule Castle Trials Door."""
    display_name = "Trials Required"
    range_start = 0
    range_end = 4
    default = 4

class OpenTrialsDoor(Toggle):
    """Makes the Lorule Castle Trials Door automatically open from both sides.
    This may require entering Lorule Castle early via the crack.
    If turned on, this overrides the Trials Required setting."""
    display_name = "Open Trials Door"

class BowOfLightInCastle(Toggle):
    """Limits the Bow of Light's placement to somewhere in Lorule Castle (including possibly Zelda)."""
    display_name = "Bow of Light in Castle"

class WeatherVanes(Choice):
    """Choose Weather Vanes behavior. Logic may require using them to progress.
    standard: Start with only the standard complimentary Weather Vanes (Link's House & Vacant House)
    shuffled: Weather Vane destinations are shuffled into random pairs
    convenient: Start with convenient Weather Vanes that don't affect logic
    hyrule: Start with the 9 Hyrule Weather Vanes (and Vacant House)
    lorule: Start with the 13 Lorule Weather Vanes (and Link's House)
    all: Start with all 22 Weather Vanes"""
    display_name = "Weather Vanes"
    option_standard = 0
    option_shuffled = 1
    option_convenient = 2
    option_hyrule = 3
    option_lorule = 4
    option_all = 5
    default = 0

class DarkRoomsLampless(Toggle):
    """If enabled the logic may expect players to cross Dark Rooms without the Lamp.
    Not for beginners and those who like being able to see things."""
    display_name = "Dark Rooms Lampless"

class SwordlessMode(Toggle):
    """Removes *ALL* Swords from the game.
    The Bug Net becomes a required item to play Dead Man's Volley against Yuga Ganon."""
    display_name = "Swordless Mode"

class ChestSizeMatchesContents(Toggle):
    """All chests containing progression items will become large, and others will be made small.
    Note: Some large chests will have a reduced hitbox to prevent negative gameplay interference."""
    display_name = "Chest Size Matches Contents"

class TreacherousTowerFloors(Range):
    """Choose how many floors the Treacherous Tower should have (2-66)."""
    display_name = "Treacherous Tower Floors"
    range_start = 2
    range_end = 66
    default = 5

class PurplePotionBottles(Toggle):
    """Fills all Empty Bottles with a free Purple Potion."""
    display_name = "Purple Potion Bottles"

class Keysy(Choice):
    """This setting removes keys and locked doors from dungeons if enabled."""
    display_name = "Keysy"
    option_off = 0
    option_small = 1
    option_big = 2
    option_all = 3

@dataclass
class ALBWSpecificOptions:
    logic_mode: LogicMode
    randomize_dungeon_prizes: RandomizeDungeonPrizes
    lorule_castle_requirement: LoruleCastleRequirement
    pedestal_requirement: PedestalRequirement
    nice_items: NiceItems
    super_items: SuperItems
    lamp_and_net_as_weapons: LampAndNetAsWeapons
    no_progression_enemies: NoProgressionEnemies
    assured_weapon: AssuredWeapon
    maiamai_mayhem: MaiamaiMayhem
    initial_crack_state: InitialCrackState
    crack_shuffle: CrackShuffle
    minigames_excluded: MinigamesExcluded
    skip_big_bomb_flower: SkipBigBombFlower
    trials_required: TrialsRequired
    open_trials_door: OpenTrialsDoor
    bow_of_light_in_castle: BowOfLightInCastle
    weather_vanes: WeatherVanes
    dark_rooms_lampless: DarkRoomsLampless
    swordless_mode: SwordlessMode
    chest_size_matches_contents: ChestSizeMatchesContents
    treacherous_tower_floors: TreacherousTowerFloors
    purple_potion_bottles: PurplePotionBottles
    keysy: Keysy

@dataclass
class ALBWOptions(PerGameCommonOptions, ALBWSpecificOptions):
    pass

def create_randomizer_settings(options: ALBWSpecificOptions) -> albwrandomizer.Settings:
    settings = albwrandomizer.Settings()

    settings.dev_mode = False
    settings.lc_requirement = options.lorule_castle_requirement.value
    settings.yuganon_requirement = options.lorule_castle_requirement.value
    settings.dark_rooms_lampless = bool(options.dark_rooms_lampless.value)
    settings.dungeon_prize_shuffle = bool(options.randomize_dungeon_prizes.value)
    settings.maiamai_limit = 100
    settings.maiamai_madness = bool(options.maiamai_mayhem.value)
    settings.super_items = bool(options.super_items.value)
    settings.lamp_and_net_as_weapons = bool(options.lamp_and_net_as_weapons.value)
    settings.ravios_shop = albwrandomizer.RaviosShop.Open
    settings.bow_of_light_in_castle = bool(options.bow_of_light_in_castle.value)
    settings.no_progression_enemies = bool(options.no_progression_enemies.value)
    settings.progressive_bow_of_light = False
    settings.swordless_mode = bool(options.swordless_mode.value)
    settings.start_with_merge = False
    settings.start_with_pouch = False
    settings.bell_in_shop = False
    settings.sword_in_shop = False
    settings.boots_in_shop = False
    settings.assured_weapon = bool(options.assured_weapon.value)
    settings.chest_size_matches_contents = bool(options.chest_size_matches_contents.value)
    settings.minigames_excluded = bool(options.minigames_excluded.value)
    settings.skip_big_bomb_flower = bool(options.skip_big_bomb_flower.value)
    settings.treacherous_tower_floors = options.treacherous_tower_floors.value
    settings.purple_potion_bottles = bool(options.purple_potion_bottles.value)
    settings.night_mode = False
    settings.user_exclusions = set()

    if options.logic_mode.value == LogicMode.option_normal:
        settings.logic_mode = albwrandomizer.LogicMode.Normal
    elif options.logic_mode.value == LogicMode.option_hard:
        settings.logic_mode = albwrandomizer.LogicMode.Hard
    elif options.logic_mode.value == LogicMode.option_glitched:
        settings.logic_mode = albwrandomizer.LogicMode.Glitched
    elif options.logic_mode.value == LogicMode.option_adv_glitched:
        settings.logic_mode = albwrandomizer.LogicMode.AdvGlitched
    elif options.logic_mode.value == LogicMode.option_hell:
        settings.logic_mode = albwrandomizer.LogicMode.Hell
    
    if options.pedestal_requirement == PedestalRequirement.option_vanilla:
        settings.ped_requirement = albwrandomizer.PedestalSetting.Vanilla
    elif options.pedestal_requirement == PedestalRequirement.option_standard:
        settings.ped_requirement = albwrandomizer.PedestalSetting.Standard
    
    if options.nice_items == NiceItems.option_vanilla:
        settings.nice_items = albwrandomizer.NiceItems.Vanilla
    elif options.nice_items == NiceItems.option_shuffled:
        settings.nice_items = albwrandomizer.NiceItems.Shuffled
    elif options.nice_items == NiceItems.option_off:
        settings.nice_items = albwrandomizer.NiceItems.Off

    if options.initial_crack_state == InitialCrackState.option_closed:
        settings.cracks = albwrandomizer.Cracks.Closed
    elif options.initial_crack_state == InitialCrackState.option_open:
        settings.cracks = albwrandomizer.Cracks.Open
    
    if options.crack_shuffle == CrackShuffle.option_off:
        settings.cracksanity = albwrandomizer.Cracksanity.Off
    elif options.crack_shuffle == CrackShuffle.option_cross_world_pairs:
        settings.cracksanity = albwrandomizer.Cracksanity.CrossWorldPairs
    elif options.crack_shuffle == CrackShuffle.option_any_world_pairs:
        settings.cracksanity = albwrandomizer.Cracksanity.AnyWorldPairs
    elif options.crack_shuffle == CrackShuffle.option_mirrored_cross_world_pairs:
        settings.cracksanity = albwrandomizer.Cracksanity.MirroredCrossWorldPairs
    elif options.crack_shuffle == CrackShuffle.option_mirrored_any_world_pairs:
        settings.cracksanity = albwrandomizer.Cracksanity.MirroredAnyWorldPairs
    
    if options.weather_vanes == WeatherVanes.option_standard:
        settings.weather_vanes = albwrandomizer.WeatherVanes.Standard
    elif options.weather_vanes == WeatherVanes.option_shuffled:
        settings.weather_vanes = albwrandomizer.WeatherVanes.Shuffled
    elif options.weather_vanes == WeatherVanes.option_convenient:
        settings.weather_vanes = albwrandomizer.WeatherVanes.Convenient
    elif options.weather_vanes == WeatherVanes.option_hyrule:
        settings.weather_vanes = albwrandomizer.WeatherVanes.Hyrule
    elif options.weather_vanes == WeatherVanes.option_lorule:
        settings.weather_vanes = albwrandomizer.WeatherVanes.Lorule
    elif options.weather_vanes == WeatherVanes.option_all:
        settings.weather_vanes = albwrandomizer.WeatherVanes.All

    if options.keysy == Keysy.option_off:
        settings.keysy = albwrandomizer.Keysy.Off
    elif options.keysy == Keysy.option_small:
        settings.keysy = albwrandomizer.Keysy.SmallKeysy
    elif options.keysy == Keysy.option_big:
        settings.keysy = albwrandomizer.Keysy.BigKeysy
    elif options.keysy == Keysy.option_all:
        settings.keysy = albwrandomizer.Keysy.AllKeysy
    
    if options.trials_required == 0:
        settings.trials_door = albwrandomizer.TrialsDoor.OpenFromInsideOnly
    elif options.trials_required == 1:
        settings.trials_door = albwrandomizer.TrialsDoor.OneTrialRequired
    elif options.trials_required == 2:
        settings.trials_door = albwrandomizer.TrialsDoor.TwoTrialsRequired
    elif options.trials_required == 3:
        settings.trials_door = albwrandomizer.TrialsDoor.ThreeTrialsRequired
    elif options.trials_required == 4:
        settings.trials_door = albwrandomizer.TrialsDoor.AllTrialsRequired

    if options.open_trials_door:
        settings.trials_door = albwrandomizer.TrialsDoor.OpenFromBothSides

    return settings
