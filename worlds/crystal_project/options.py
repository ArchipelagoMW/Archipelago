from dataclasses import dataclass
from typing import Any, List
from typing import Dict

from Options import PerGameCommonOptions, StartInventoryPool
from Options import Toggle, DefaultOnToggle, Choice, Range, OptionGroup


def create_option_groups() -> List[OptionGroup]:
    option_group_list: List[OptionGroup] = []
    for name, options in crystal_project_option_groups.items():
        option_group_list.append(OptionGroup(name=name, options=options))

    return option_group_list
#"""Goal Options"""
class Goal(Choice):
    """
    Choose what is required to complete the game.
    
    Checking the first sign in the Spawning Meadows will tell you the selected goal. A goal items counter is displayed on the in-game party screen in the menu.
    
    Astley: Defeat Astley in the New World. The throne room in The New World will unlock once you have found enough Jobs (starting Jobs don't count).

    True Astley: A saga awaits you! Collect 4 Deity Eyes and the STEM WARD to challenge Gabriel for the Old World Stone. Then travel to the Old World to defeat Periculum and earn the Proof of Merit.
    Along the way, gather enough Jobs to unlock the throne room in The New World. Then, venture there to defeat true Astley to win!
    
    Clamshells: Collect enough clamshells for Mañana Man in Seaside Cliffs.
    """
    display_name = "Goal"
    option_astley = 0
    option_true_astley = 1
    option_clamshells = 2
    default = 0

class AstleyJobQuantity(Range):
    """
    If your goal is Astley or True Astley, select how many Jobs you need to find to unlock the throne room for the final fight.

    This option is validated at generation time, and if it is higher than the number of Jobs you can obtain, it will be capped to what is possible. By default, the maximum you can obtain is 18.

    Picking Job Rando: Full and decreasing the Starting Job Quantity will increase the maximum by that much. It will also increase if you enable mods that give you more.

    Picking Job Rando: None and Included Regions: Beginner or Advanced will reduce the maximum number available to 4 or 11, respectively.
    """
    display_name = "Job count that unlocks Astley's throne room"
    range_start = 1
    range_end = 99
    default = 18

class ClamshellGoalQuantity(Range):
    """
    If your goal is Clamshells, select how many you need to win.

    (If your goal is not Clamshells, this setting does nothing. 3 Clamshells will be placed in your pool and the Mañana Man will ask for 2. Don't worry, he's cool with it.)
    """
    display_name = "Clamshells needed to win"
    range_start = 1
    range_end = 99
    default = 13
    
class ExtraClamshellsInPool(Range):
    """
    If your goal is Clamshells, pick how many more Clamshells than your goal value to have in the item pool.
    This option makes it so that you don't have to find every single Clamshell in your pool to win.

    (If your goal is not Clamshells, this setting does nothing.)
    """
    display_name = "Extra Clamshells in the pool"
    range_start = 0
    range_end = 99
    default = 6

#"""Location Options"""
class IncludedRegions(Choice):
    """
    Choose which regions to play in! Only locations within your chosen regions will give you checks; the rest will be empty.
    This can be used to adjust the difficulty and length of your game.

    NOTE: Make sure to include the region that has the finish line of your chosen goal in it!
    Example: if your goal is Astley, Advanced is considered to have that finish line, so you can pick Advanced, Expert, or All.

    Beginner: Only regions up through the end of Skumparadise will have checks. Finish Line: Clamshells

    Advanced: Regions up to Salmon Bay will have checks. Finish Line: Astley (Note: Level Gating's Level Catch-Up Option is recommended for Astley on Advanced.)

    Expert: Regions up to The Deep Sea will have checks. (Note: The Depths will not be included.)

    All: Every region is included. Finish Line: True Astley
    """
    display_name = "Regions to include in game"
    option_beginner = 0
    option_advanced = 1
    option_expert = 2
    option_all = 3
    default = 3

class JobRando(Choice):
    """
    None: all Jobs are at their normal crystal locations in the vanilla game.

    Crystal: all vanilla Jobs normally received from crystals are chucked into the item pool.

    Full: your starting jobs are randomized, and the rest of the vanilla Jobs are added to the item pool.
    Adjust the Starting Job Quantity (see below) for how many random Jobs you start with.
    """
    display_name = "Job Rando"
    option_none = 0
    option_crystal = 1
    option_full = 2
    default = 2

class StartingJobQuantity(Range):
    """
    Select how many Jobs you start with. (This setting only does anything if JobRando is set to Full.)
    """
    display_name = "Starting Job Quantity"
    range_start = 1
    range_end = 6
    default = 6

class DisableSparks(Toggle):
    """
    When enabled, enemy sparks are disabled: enemies will completely ignore the player, and touching them does not start combat.
    An Enable/Disable Sparks button will appear in the game's Archipelago menu that you can use to toggle spark disabling on and off.
    Explore unbothered by fiery plebeians, re-enable them when you deign to grind XP or earn money, and re-disable them when you've had enough of their nonsense!

    However: if Kill Bosses is enabled, then boss sparks still have your number (a.k.a. chase you and start combat). They can sense your murderous intent.
    """
    display_name = "Disable Sparks"

class KillBossesMode(Toggle):
    """
    When enabled, defeating a boss will provide checks.

    WARNING: If you restrict the Included Regions to Beginner or Advanced, checks will require defeating level 50+ bosses in some of the early areas!
    You may want to set the Level Gating option to Level Catch-Up.  Without it, you are signing up to either grind or fight the bosses under-leveled.
    """
    display_name = "Kill Bosses Mode"

class Shopsanity(Choice):
    """
    When enabled, all shop inventories will be replaced with checks. Be prepared, adventurer.

    Choosing "enabled and hint" will, when you CLOSE the store, automatically create a hint for every item you did not purchase
    so other players will realize you have betrayed them by refusing to purchase their key progression item!
    """
    display_name = "Shopsanity"
    option_disabled = 0
    option_enabled = 1
    option_enabled_and_hint = 2
    default = 0

class Regionsanity(Choice):
    """
    Nothing I have tried has been able to drive the citizens of Sequoia to collect enough crystals!
    Adventurers have had TOO MUCH freedom!  From now on, you will adventure where I tell you to.
    Unless you have a pass from ME, you won't be able to do any adventuring!
    - Grandmaster

    When enabled, the grandmaster will not permit you to interact with anything in a region
    without receiving his "official permission" (i.e. "Item - Spawning Meadows Pass").
    However, the Overpass and Underpass are regions of lawlessness where the Grandmaster has no authority! ;)
    (You're also still allowed to use the save points, we won't tell.)

    If you put any region pass items in your starting inventory, the first one will be chosen as your starting region.

    If Regionsanity is set to Extreme, the Grandmaster won't even let you walk through regions you don't have the pass for.
    Spend more than 10 seconds in a region without a pass and the Grandmaster will teleport you!

    You will start the game in a random region with a pass. You will be leveled appropriately.
    """
    display_name = "Regionsanity"
    option_disabled = 0
    option_enabled = 1
    option_extreme = 2
    default = 0

class RegionsanityStarterRegionMinLevel(Range):
    """
    This sets the lowest possible level your random starter region could be in Regionsanity.
    All regions without combat have a level of 0 (e.g. Capital Sequoia and Eastern Chasm). Otherwise, Beginner Regions start at level 3, Advanced at 18, Expert at 36, and End-Game at 60.
    """
    display_name = "Regionsanity Starter Region Minimum Level"
    range_start = 0
    range_end = 63
    default = 0

class RegionsanityStarterRegionMaxLevel(Range):
    """
    This sets the highest possible level your random starter region could be in Regionsanity.
    Beginner Regions end at level 15, Advanced at level 38 (except Capital Pipeline at level 50 lol), Expert at 60, and End-Game at 63.
    (The Old World is not allowed to be your starter region. Sorry if you just really wanted to fight Periculum with no gear right off the bat.)
    """
    display_name = "Regionsanity Starter Region Maximum Level"
    range_start = 0
    range_end = 63
    default = 30

class HomePointHustle(Choice):
    """
    When enabled, every Home Point will give you a check the first time you interact with it, and Home Point teleport items will be added to the pool.
    
    Mixed: You can teleport to any Home Point that you have interacted with or have the teleport item for.
    Hustle Only: You can ONLY teleport to a Home Point after getting its matching teleport item.
    """
    display_name = "Home Point Hustle"
    option_disabled = 0
    option_mixed = 1
    option_hustle_only = 2
    default = 0

#"""Progression Options"""
class ProgressiveMountMode(DefaultOnToggle):
    """
    When enabled, all mount items are combined into a Progressive Mount Instrument and will be received in the approximate order you would receive them in the vanilla game:
       Quintar Pass -> Quintar Flute -> Ibek Bell -> Owl Drum -> Salmon Violin -> Salmon Cello -> Quintar Ocarina

    When disabled, different mount types are separated:
       Progressive Quintar Flute (Quintar Pass -> Quintar Flute -> Quintar Ocarina),
       Progressive Salmon Violin (Salmon Violin -> Salmon Cello),
       Ibek Bell,
       and Owl Drum.
    """
    display_name = "Progressive Mount Mode"

class StartingLevel(Range):
    """
    Choose what level your party starts at.

    NOTE: If any variant of Regionsanity is enabled, you may start at a higher level based on the level of your random starter region. See Regionsanity settings above.
    """
    display_name = "Starting Level"
    range_start = 3
    range_end = 99
    default = 3

class LevelGating(Choice):
    """
    When enabled, the party's level is considered for Archipelago logic, and Progressive Level items are added to the pool. (This won't stop you from beating the game at level 3. ^_^)

    None: Level gating is disabled. No Progressive Levels in the pool.

    Level Passes: Progressive Levels are added to the pool. They do not affect the party's actual level or level cap. Archipelago will expect you to collect them to access level-gated areas,
    and in-game tracking will light up checks that you have access to based on that level.

    Level Capped: The party's maximum level is hard capped. Progressive Levels are added to the pool. Collecting them allows your party to gain more levels, and in-game tracking will light up
    checks that you have access to based on that max level.

    Level Catch-Up: Progressive Levels are added to the pool. Collecting them will help your party catch up in levels (and LP!) based on the number you've collected. 2 LP are granted per 1 level granted.
    For example, if your Starting Level is 3 (above) and Progressive Level Size (below) is 6, 1 Progressive Level will bring your party's level up to 9. If your party has already reached that level,
    no extra levels will be granted. In-game tracking will light up checks that you have access to based on the number you have collected.

    Level Set: A combination of Level Catch-Up and Capped. The player will always be at the level set by the Progressive Level. There is no escape.

    For example, if your Starting Level (above) is 3 and Progressive Level Size (below) is 6, the Level Gating options would behave like this:
       Level Passes - Your party's level starts at 3. The first Progressive Level you collect will signal that areas up to 9 are now logic, the second up to 15, etc.
       Level Capped - Your party's level and level cap start at 3. The first Progressive Level you collect will increase your party's level cap to 9, the second to 15, and so on.
       Level Catch-Up - Your party's level starts at 3. The first Progressive Level you collect will bring your party's level up to 9 if it isn't already, the second up to 15, and so on.
       Level Set - Your party's level and level cap start at 3. The first Progressive Level you collect will increase your party's level and level cap to 9, the second to 15, and so on.
    """
    display_name = "Level Gating"
    option_none = 0
    option_level_passes = 1
    option_level_capped = 2
    option_level_catch_up = 3
    option_level_set = 4
    default = 3

class LevelComparedToEnemies(Range):
    """
    If Level Gating is on, this option changes what level you're expected to fight enemies. In Regionsanity, it will be added to your starting level.
    Set it higher if you want to be a higher level than enemies when you enter a region, or lower if you want to be lower.

    For example, if this is set to 5, and the enemy level of a region is 12, then the Level Gating options would require you to unlock level 17 (or for Level Capped, max level 17) for that region.
    If it's set to -5, and the enemy level of a region is 12, then the Level Gating options would require you to unlock level 7 (or for Level Capped, max level 7) for that region.

    Default is 0, or on-level for the enemy level of a region.

    Note: Remember to increase your Max Level (see below) if you want regions with high-level enemies to still be lower level than you.
    Note #2: Spark color changes: red at -10 levels, orange at -5, green at +3, and grey +10. (Though enemies can be 3-5 levels above the min enemy level for a region.)
    """
    display_name = "Level Compared to Enemies"
    range_start = -10
    range_end = 10
    default = 0

class ProgressiveLevelSize(Range):
    """
    If Level Gating is on, Progressive Levels will be added to the item pool. This sets the number of levels that an individual Progressive Level will grant.
    """
    display_name = "Progressive Level Size"
    range_start = 1
    range_end = 10
    default = 6

class MaxLevel(Range):
    """
    This allows your party to level past the default maximum level of 60. If Level Gating is on, increasing this number will also put more Progressive Levels in your pool.

    Set it below 60 at your own risk <3
    """
    display_name = "Max Level"
    range_start = 3
    range_end = 99
    default = 60

class StartingPassivePoints(Range):
    """
    The number of Passive Points each party member starts with. Default is the vanilla value of 10.
    """
    display_name = "Starting Passive Points"
    range_start = 0
    range_end = 50
    default = 10

class MaximumPassivePoints(Range):
    """
    The maximum number of Passive Points each party member can have. Default is the vanilla value of 10.

    If you set your Maximum Passive Points higher than your Starting Passive Points, Passive Point Boosts will be added to the item pool that increase your party's available Passive Points when found.
    """
    display_name = "Maximum Passive Points"
    range_start = 0
    range_end = 50
    default = 10

class PassivePointBoostSize(Range):
    """
    This sets the number of Passive Points you gain per Passive Point Boost.
    """
    display_name = "Passive Point Boost Size"
    range_start = 1
    range_end = 10
    default = 2

class KeyMode(Choice):
    """
    Skeleton Key: Only the Skeleton Key, which can open any locked door, will be in your item pool.

    Key Ring: Keys for individual dungeons will be grouped into Key Rings. Each Key Ring will give all keys needed to complete one dungeon. The Skeleton Key will still be in the pool.

    Vanilla: All vanilla keys will be in the item pool.

    Skelefree: Same as the named mode, but removes the Skeleton Key.
    """
    display_name = "Key Mode"
    option_skeleton = 0
    option_key_ring = 1
    option_vanilla = 2
    option_key_ring_skelefree = 3
    option_vanilla_skelefree = 4
    default = 2

class ObscureRoutes(Toggle):
    """
    When enabled, connections between regions that are difficult to find will be expected in logic.
    """
    display_name = "Obscure Routes"

class HopToIt(Choice):
    """
    No Tricks: No fancy hops expected.
    Fancy Footwork: Above-average jumping skill expected, e.g. jumping past the pushblocks in Eaclaneya with no mounts or Auto-Jump-level jumping precision.
    One Hop Beyond: More jumping tricks expected, like ibek jumping up from underneath a ledge.
    Pray: You didn't *want* the Golden Quintar for the Sequoia, did you?
    """
    display_name = "Hop To It"
    option_no_tricks = 0
    option_fancy_footwork = 1
    option_one_hop_beyond = 2
    option_pray = 3
    default = 0

class PrioritizeCrystals(DefaultOnToggle):
    """
    When enabled, crystals will be prioritized when placing progression items.

    While you're here, did you know that all YAMLs for all worlds include a priority_locations and an exclude_locations option?
    You can use these to flag any individual location or a location group as priority or excluded.
    Priority locations will be chosen first when placing progression items, and excluded locations will be chosen last.

    Here's an example:
    priority_locations = ["Crystals", "Region Completions", "Bosses", "Salmon River NPC - Win the Salmon Race"]

    Crystal Project's location groups:
      - Every region and subregion; e.g. Shoudu Province, Sky Arena
      - Base groups: Crystals, Mount Instruments, Purple Chests, Ore Nodes
      - Collectible groups: Collectible Turn-ins; Black Squirrels, Dog Bones, Clamshells, Penguins, Quintar Sheddings, Secret Herbs, Undersea Crabs
      - Special access groups: Salmon Race Prizes, Luxury Pass Required
      - NPC groups: Bribe Quests (pay NPC money), Challenge Quests (do a challenge like complete a number of Sky Arena fights,
        complete an ice block pushing puzzle, or answer Quizard questions), Fetch Quests (give NPC one or more items),
        Gifts (NPC gives you an item), Job Checkers (find a certain number of Jobs to get an item), Fishers
      - Relevant Depending On Your Other Options:
          - Home Point Hustle: Home Points
          - Kill Bosses: Bosses, Summons, End-Game Bosses
          - Regionsanity: Region Completions
          - Shopsanity: Shops
    """
    display_name = "Prioritize Crystals"

class AutoSpendLP(Toggle):
    """
    When enabled, every time a character earns LP, it will automatically spend LP on abilities or passives.
    Extra LP earned on a job that is maxed will be sent to your sub job or, if that is also maxed, a random un-maxed job.
    """
    display_name = "Automatically Spend LP"

class AutoEquipPassives(Toggle):
    """
    When enabled, every time a character unlocks a new passive, it will equip it immediately if enough passive points are available.
    Passives with drawbacks, that enable equipping more gear types, or that modify threat are not automatically equipped.
    If mods are enabled, all passives are auto-equipped with no exclusions.
    """
    display_name = "Automatically Equip Passives"

class EasyLeveling(Toggle):
    """
    When enabled, characters will not receive reduced experience for being dead or for being a higher level than the fought enemy.
    """
    display_name = "Easy Leveling"

#"""Item Pool Options"""
class ProgressiveEquipmentMode(DefaultOnToggle):
    """
    When enabled, each category of weapon and armor will be sent to the player in progressive order from weakest to strongest.

    When disabled, weapons and armor are fully randomized.
    """
    display_name = "Progressive Equipment"

class StartWithTreasureFinder(DefaultOnToggle):
    """
    When enabled, the player will start with the Treasure Finder in their inventory. When disabled, it will be in the item pool.

    NOTE: Having the Treasure Finder is required for the in-game minimap to display nearby checks.
    """
    display_name = "Begin with Treasure Finder"

class StartWithMaps(DefaultOnToggle):
    """
    When enabled, the player will start with all maps in their inventory.

    Note: The in-game minimap hides when in an area without its map. The world map will display check location icons but will not draw an area without its map.
    """
    display_name = "Begin with Area Maps"

class FillFullMap(Toggle):
    """
    When enabled, the world map will start filled in for areas that the player has a map item for.
    """
    display_name = "Fill Full Map"

class IncludeSummonAbilities(DefaultOnToggle):
    """
    When enabled, Summons are added to the item pool.

    Note: It is not recommended to turn this off with Job Rando: Full and a low number of starting Jobs. You don't want to get stuck with just a Summoner who can only summon Pinga!
    (I'm sorry, Pinga.)
    """
    display_name = "Include Summons in the item pool"
    
class IncludeScholarAbilities(DefaultOnToggle):
    """
    When enabled, Scholar abilities are added to the item pool. They can still be learned as normal from enemies.
    """
    display_name = "Include Scholar Abilities in the item pool"

#"""Bonus Fun"""
class TrapLikelihood(Range):
    """
    This is the likelihood that a trap will replace a filler check. A value of 0 means no traps.
    """
    display_name = "Trap Likelihood"
    range_start = 0
    range_end = 100
    default = 0

class ItemInfoMode(Choice):
    """
    For Full, all treasure and store icons on the map will display if they are progression, useful, or filler items.

    For Earned, all treasure and store icons on the map will display as mimics until you complete 50% of your checks.

    For Obscured, all treasure and store icons on the map will display as mimics permanently.
    If you find skipping treasures is distasteful but part of your brain always wants to be efficient, this option is for you!
    It's also good for a race environment.
    """
    display_name = "Item Info Mode"
    option_full = 0
    option_earned = 1
    option_obscured = 2
    default = 0

class RandomizeMusic(Toggle):
    """
    When enabled, music will be randomized upon connecting to the AP World. (This toggles the base game's Randomize Music function.)
    """
    display_name = "Randomize Music"

class UseMods(Toggle):
    """
    WARNING: This setting is very in beta right now! Enabling it is not recommended for: multiworlds that do not allow releasing items or with Regionsanity enabled
    (some mods add items to regions but don't place them anywhere near that region).

    When enabled, items and locations added by other Crystal Project mods will be added to the item and location pools at generation. Mods newer than Editor version 30 are incompatible.

    Multiworld host instructions:
    1. In order to select the mods you'd like to include in randomization, make a folder named "crystal_project_mods" inside your root Archipelago directory.
    2. Go to your Steam installation folder for Crystal Project (<YourSteamInstallFolder>/steamapps/workshop/content/1637730) and find the individual folders for the mods you'd like to include.
    3. Inside each mod's folder is a mod json. Copy that json to the crystal_project_mods folder you made inside the Archipelago directory.
    4. If you have a specific order you want to apply the mods, rename the jsons such that they are in alphabetical order in the order you want them to be applied.
       E.g. name the first mod a_modname, the second b_modname, etc.

    NOTE: When this setting is on, all Crystal Project players in the multiworld with this setting enabled MUST use the same mods.

    The in-game tracking will use special icons for modded locations that will not display their accessibility (as we can only guess at how accessible they are based on coordinates,
    and would prefer the tracking to be as accurate as possible).

    When disabled, only base game locations and items will be randomized. You can still use other mods - at your own risk, adventurer - they just won't add checks.

    The game will warn you if you open a game with mods that don't match the mods used to generate the multiworld. It will warn you even if this setting is disabled for you, if you start playing with mods.
    """
    display_name = "Use Mods"

@dataclass
class CrystalProjectOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    goal: Goal
    astley_job_quantity: AstleyJobQuantity
    clamshell_goal_quantity: ClamshellGoalQuantity
    extra_clamshells_in_pool: ExtraClamshellsInPool
    job_rando: JobRando
    starting_job_quantity: StartingJobQuantity
    disable_sparks: DisableSparks
    kill_bosses_mode: KillBossesMode
    shopsanity: Shopsanity
    regionsanity: Regionsanity
    regionsanity_starter_region_min_level: RegionsanityStarterRegionMinLevel
    regionsanity_starter_region_max_level: RegionsanityStarterRegionMaxLevel
    home_point_hustle: HomePointHustle
    included_regions: IncludedRegions
    progressive_mount_mode: ProgressiveMountMode
    starting_level: StartingLevel
    level_gating: LevelGating
    level_compared_to_enemies: LevelComparedToEnemies
    progressive_level_size: ProgressiveLevelSize
    max_level: MaxLevel
    starting_passive_points: StartingPassivePoints
    maximum_passive_points: MaximumPassivePoints
    passive_point_boost_size: PassivePointBoostSize
    key_mode: KeyMode
    obscure_routes: ObscureRoutes
    hop_to_it: HopToIt
    prioritize_crystals: PrioritizeCrystals
    auto_spend_lp: AutoSpendLP
    auto_equip_passives: AutoEquipPassives
    easy_leveling: EasyLeveling
    progressive_equipment_mode: ProgressiveEquipmentMode
    start_with_treasure_finder: StartWithTreasureFinder
    start_with_maps: StartWithMaps
    fill_full_map: FillFullMap
    include_summon_abilities: IncludeSummonAbilities
    include_scholar_abilities: IncludeScholarAbilities
    trap_likelihood: TrapLikelihood
    item_info_mode: ItemInfoMode
    randomize_music: RandomizeMusic
    use_mods: UseMods

crystal_project_option_groups: Dict[str, List[Any]] = {
    "Goal Options": [Goal, ClamshellGoalQuantity, ExtraClamshellsInPool, AstleyJobQuantity],
    "Location Options": [IncludedRegions, JobRando, StartingJobQuantity, DisableSparks, KillBossesMode, Shopsanity, Regionsanity, RegionsanityStarterRegionMinLevel, RegionsanityStarterRegionMaxLevel, HomePointHustle],
    "Progression Options": [ProgressiveMountMode, StartingLevel, LevelGating, LevelComparedToEnemies, ProgressiveLevelSize, MaxLevel, StartingPassivePoints, MaximumPassivePoints, PassivePointBoostSize, KeyMode, ObscureRoutes, HopToIt, PrioritizeCrystals, AutoSpendLP, AutoEquipPassives, EasyLeveling],
    "Item Pool Options": [ProgressiveEquipmentMode, StartWithTreasureFinder, StartWithMaps, FillFullMap, IncludeSummonAbilities, IncludeScholarAbilities],
    "Bonus Fun": [ItemInfoMode, RandomizeMusic, UseMods]
}