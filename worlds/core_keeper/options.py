from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle


class LicenseToggle(Toggle):
    """Adds this crafting-station license as a progression reward and locks the station behind it."""


class WorkbenchLicense(LicenseToggle):
    """Adds progressive workbench tiers as rewards and locks those tiers behind them."""
    display_name = "Progressive Workbench License"
    default = 1


class AnvilLicense(LicenseToggle):
    """Adds progressive anvil tiers as rewards and locks those tiers behind them."""
    display_name = "Progressive Anvil License"
    default = 1


class PouchWorkbenchLicense(LicenseToggle):
    """Adds the Pouch Workbench license as a reward and locks the station behind it."""
    display_name = "Pouch Workbench License"
    default = 0


class TableSawLicense(LicenseToggle):
    """Adds the Table Saw license as a reward and locks the station behind it."""
    display_name = "Table Saw License"
    default = 1


class CookingPotLicense(LicenseToggle):
    """Adds the Cooking Pot license as a reward and locks the station behind it."""
    display_name = "Cooking Pot License"
    default = 1


class JewelryWorkbenchLicense(LicenseToggle):
    """Adds progressive jewelry workbench tiers as rewards and locks those tiers behind them."""
    display_name = "Progressive Jewelry Workbench License"
    default = 0


class CarpenterTableLicense(LicenseToggle):
    """Adds the Carpenter's Table license as a reward and locks the station behind it."""
    display_name = "Carpenter's Table License"
    default = 0


class AlchemyTableLicense(LicenseToggle):
    """Adds progressive alchemy table tiers as rewards and locks those tiers behind them."""
    display_name = "Progressive Alchemy Table License"
    default = 0


class DistilleryTableLicense(LicenseToggle):
    """Adds the Distillery Table license as a reward and locks the station behind it."""
    display_name = "Distillery Table License"
    default = 0


class ElectronicsTableLicense(LicenseToggle):
    """Adds the Electronics Table license as a reward and locks the station behind it."""
    display_name = "Electronics Table License"
    default = 0


class AutomationTableLicense(LicenseToggle):
    """Adds progressive automation table tiers as rewards and locks those tiers behind them."""
    display_name = "Progressive Automation Table License"
    default = 0


class RailwayForgeLicense(LicenseToggle):
    """Adds the Railway Forge license as a reward and locks the station behind it."""
    display_name = "Railway Forge License"
    default = 0


class BoatWorkbenchLicense(LicenseToggle):
    """Adds the Boat Workbench license as a reward and locks the station behind it."""
    display_name = "Boat Workbench License"
    default = 0


class GoKartWorkbenchLicense(LicenseToggle):
    """Adds the Go-Kart Workbench license as a reward and locks the station behind it."""
    display_name = "Go-Kart Workbench License"
    default = 0


class LoomLicense(LicenseToggle):
    """Adds the Loom license as a reward and locks the station behind it."""
    display_name = "Loom License"
    default = 0


class MusicWorkbenchLicense(LicenseToggle):
    """Adds the Music Workbench license as a reward and locks the station behind it."""
    display_name = "Music Workbench License"
    default = 0


class LivestockWorkbenchLicense(LicenseToggle):
    """Adds the Livestock Workbench license as a reward and locks the station behind it."""
    display_name = "Livestock Workbench License"
    default = 0


class GlassWorkbenchLicense(LicenseToggle):
    """Adds the Glass Workbench license as a reward and locks the station behind it."""
    display_name = "Glass Workbench License"
    default = 0


class FishingWorkbenchLicense(LicenseToggle):
    """Adds the Fishing Workbench license as a reward and locks the station behind it."""
    display_name = "Fishing Workbench License"
    default = 1


class EggIncubatorLicense(LicenseToggle):
    """Adds the Egg Incubator license as a reward and locks the station behind it."""
    display_name = "Egg Incubator License"
    default = 1


class KeyCastingTableLicense(LicenseToggle):
    """Adds the Key Casting Table license as a reward and locks the station behind it."""
    display_name = "Key Casting Table License"
    default = 1


class PainterTableLicense(LicenseToggle):
    """Adds the Painter's Table license as a reward and locks the station behind it."""
    display_name = "Painter's Table License"
    default = 0


class SmithingTableLicense(LicenseToggle):
    """Adds progressive smithing table tiers as rewards and locks those tiers behind them."""
    display_name = "Progressive Smithing Table License"
    default = 0


class FurnaceLicense(LicenseToggle):
    """Adds progressive furnace tiers as rewards and locks those tiers behind them."""
    display_name = "Progressive Furnace License"
    default = 1


class GlassSmelterLicense(LicenseToggle):
    """Adds the Glass Smelter license as a reward and locks the station behind it."""
    display_name = "Glass Smelter License"
    default = 0


class HologramLicense(LicenseToggle):
    """Adds the Ancient Hologram Pod license as a reward and locks the station behind it."""
    display_name = "Ancient Hologram Pod License"
    default = 1


class RiftStatueLicense(LicenseToggle):
    """Adds the Rift Statue license as a reward and locks the station behind it."""
    display_name = "Rift Statue License"
    default = 0


class UpgradeStationLicense(LicenseToggle):
    """Adds the Upgrade Station license as a reward and locks the station behind it."""
    display_name = "Upgrade Station License"
    default = 0


class RepairSalvageLicense(LicenseToggle):
    """Adds the Salvage and Repair Station license as a reward and locks the station behind it."""
    display_name = "Salvage and Repair Station License"
    default = 1


class Goal(Choice):
    """(20 Checks) Defeat All Bosses - Find and defeat all bosses including optional bosses.
    (12 Checks) Defeat S.A.H.A.B.A.R - Find and defeat S.A.H.A.B.A.R.
    (10 Checks) Defeat Core Commander - Find and defeat all of the Titans and Core Commander.
    (3 Checks) Lower Wall - Find and defeat Glurch, Ghorm, and Malugaz."""

    display_name = "Goal"
    # Requested reverse order: All Bosses, S.A.H.A.B.A.R, Core Commander,
    # Lower Wall.
    option_defeat_all_bosses = 0
    option_defeat_sahabar = 1
    option_defeat_core_commander = 2
    option_lower_wall = 3
    default = 2

    @classmethod
    def get_option_name(cls, value: int) -> str:
        return {
            0: "Defeat All Bosses",
            1: "Defeat S.A.H.A.B.A.R",
            2: "Defeat Core Commander",
            3: "Lower Wall",
        }[value]


class SkillXpMultiplier(Choice):
    """Multiplies skill experience gains by 1x - 10x."""
    display_name = "Skill XP Multiplier"
    option_1x = 0
    option_1_5x = 1
    option_2x = 2
    option_2_5x = 3
    option_3x = 4
    option_3_5x = 5
    option_4x = 6
    option_4_5x = 7
    option_5x = 8
    option_5_5x = 9
    option_6x = 10
    option_6_5x = 11
    option_7x = 12
    option_7_5x = 13
    option_8x = 14
    option_8_5x = 15
    option_9x = 16
    option_9_5x = 17
    option_10x = 18
    default = 4

    @classmethod
    def get_option_name(cls, value: int) -> str:
        return f"{1 + value * 0.5:g}x"


class SkillPoints(Toggle):
    """Suppresses level-earned talent points and adds five +5 rewards for each skill."""
    display_name = "Skill Points"
    default = 0


class DeathLink(Choice):
    """Shares deaths with other Death Link players.
    Keep Inventory prevents Death Link deaths from dropping the players inventory."""
    display_name = "Death Link"
    option_off = 0
    option_death_link = 1
    option_death_link_keep_inventory = 2
    default = 0

    @classmethod
    def get_option_name(cls, value: int) -> str:
        return {0: "Off", 1: "Death Link", 2: "Death Link (Keep Inventory)"}[value]


class SoulSeekerCache(Toggle):
    """Adds one cache that always awards Soul Seeker."""
    display_name = "Soul Seeker Cache"
    default = 1


class TitanBreathCache(Toggle):
    """Adds one cache that always awards Titan Breath."""
    display_name = "Titan Breath Cache"
    default = 1


class PhantomSparkCache(Toggle):
    """Adds one cache that always awards Phantom Spark."""
    display_name = "Phantom Spark Cache"
    default = 1


class RuneSongCache(Toggle):
    """Adds one cache that always awards Rune Song."""
    display_name = "Rune Song Cache"
    default = 1


class CredenceOfRuinCache(Toggle):
    """Adds one cache that always awards Credence of Ruin."""
    display_name = "Credence of Ruin Cache"
    default = 1


class StormbringerCache(Toggle):
    """Adds one cache that always awards Stormbringer."""
    display_name = "Stormbringer Cache"
    default = 1


class RewardTools(Toggle):
    """Adds all tools as rewards, randomly cuts access."""
    display_name = "Tools"
    default = 0


class RewardWeapons(Toggle):
    """Adds all weapons as rewards, randomly cuts access."""
    display_name = "Weapons"
    default = 0


class RewardJewelry(Toggle):
    """Adds all necklaces and rings as rewards, randomly cuts access."""
    display_name = "Jewelry"
    default = 0


class RewardAccessories(Toggle):
    """Adds all accessories as rewards, randomly cuts access."""
    display_name = "Accessories"
    default = 0


class RewardArmor(Toggle):
    """Adds all armors as rewards, randomly cuts access."""
    display_name = "Armor"
    default = 0


class EarlyRepairAndSalvage(Toggle):
    """Guarantees the Salvage and Repair Station and first Furnace licenses in local starting spheres when enabled."""
    display_name = "Early Repair and Salvage"
    default = 1


class PreventPriorityInSanity(Toggle):
    """Prefers progression items outside opt-in sanity checks, allowing only required overflow."""
    display_name = "Prevent Progression in Sanity"
    default = 1


class PreventPriorityInOptionalChecks(Toggle):
    """Prefers progression items outside opt-in optional checks, allowing only required overflow."""
    display_name = "Prevent Progression in Optional Checks"
    default = 1


class InfiniteMerchantStock(Toggle):
    """Restocks currently available merchant offers to their normal maximum."""
    display_name = "Infinite Merchant Stock"
    default = 1


class MerchantSellsCrownSummon(Toggle):
    """Moves Caveling Bread to the Fishing Merchant and sells the crown summon at the Cloaked Merchant."""
    display_name = "Merchant Sells Crown Summon"
    default = 1


class RandomizeEnemies(Toggle):
    """Seeded one-to-one permutation of eligible ordinary enemy spawn slots.

    Bosses, livestock, pets, merchants, structural spawners, and scripted actors are excluded.
    """

    display_name = "Randomize Enemies"
    default = 0


class RandomizeBosses(Toggle):
    """Moves every boss into a different boss encounter.

    The mapping preserves a one-to-one set and scales combat to the destination slot.
    """

    display_name = "Randomize Bosses"
    default = 0


class RandomizerDifficulty(Choice):
    """Controls enemy-map safety weighting and combat normalization.

    Easy strongly discourages later-region enemies in earlier slots. Medium relaxes that protection. Hard removes
    progression weighting. Masochist also keeps replacement health and damage at native values.
    """

    display_name = "Randomizer Difficulty"
    option_easy = 0
    option_medium = 1
    option_hard = 2
    option_masochist = 3
    default = 0


class Bosses(Toggle):
    """Adds optional boss checks such as Ivy, Atlantean Worm, and Urschleim.
    All Bosses - Added by goal
    SAHABAR - 6 Checks
    Core Commander - 6 Checks
    Lower Wall - 2 Checks"""
    display_name = "Optional Bosses"
    default = 0


class RawMaterials(Toggle):
    """Adds raw material checks such as Ancient Coin, Wood, Ores, and Slime.
    All Bosses - 34 Checks
    SAHABAR - 34 Checks
    Core Commander - 29 Checks
    Lower Wall - 13 Checks"""

    display_name = "Raw Materials"
    default = 1


class RefinedMaterials(Toggle):
    """Adds refined material checks such as Glass Piece, Planks, and Bars.
    All Bosses - 14 Checks
    SAHABAR - 14 Checks
    Core Commander - 12 Checks
    Lower Wall - 6 Checks"""

    display_name = "Refined Materials"
    default = 1


class UniqueMaterials(Toggle):
    """Adds unique material checks such as weapon components and boss crafting parts.
    All Bosses - 19 Checks
    SAHABAR - 18 Checks
    Core Commander - 15 Checks
    Lower Wall - 1 Checks"""

    display_name = "Unique Materials"
    default = 0


class KeyItems(Toggle):
    """Adds key item checks such as Glurch Eye, Admin Key, and Brood Void Neuron.
    All Bosses - 9 Checks
    SAHABAR - 9 Checks
    Core Commander - 7 Checks
    Lower Wall - 3 Checks"""

    display_name = "Key Items"
    default = 0


class Seeds(Toggle):
    """Adds seed checks such as Heart Berry Seed, Pinegrapple Seed, and Gleam Wood Seed.
    All Bosses - 14 Checks
    SAHABAR - 14 Checks
    Core Commander - 14 Checks
    Lower Wall - 6 Checks"""

    display_name = "Seeds"
    default = 1


class Food(Toggle):
    """Adds food checks such as Mushroom, Sunrice, and Atlantean Worm Heart.
    All Bosses - 22 Checks
    SAHABAR - 22 Checks
    Core Commander - 20 Checks
    Lower Wall - 10 Checks"""

    display_name = "Food"
    default = 1


class Critters(Toggle):
    """Adds critter capture checks such as Yellow Glowbug, Ice Wind, and Drape Ray.
    All Bosses - 25 Checks
    SAHABAR - 25 Checks
    Core Commander - 23 Checks
    Lower Wall - 6 Checks"""

    display_name = "Critters"
    default = 0


class Goldensanity(Toggle):
    """Adds golden crop checks such as Golden Heart Berry, Golden Puffungi, and Golden Pewpaya.
    All Bosses - 11 Checks
    SAHABAR - 11 Checks
    Core Commander - 11 Checks
    Lower Wall - 4 Checks"""

    display_name = "Golden Food"
    default = 0


class Cardsanity(Toggle):
    """Adds nine Oracle Card checks and the completed Oracle Deck.
    All Bosses - 10 Checks
    SAHABAR - 10 Checks
    Core Commander - 10 Checks
    Lower Wall - 3 Checks"""

    display_name = "Cardsanity"
    default = 0


class Blocksanity(Toggle):
    """Adds wall-block check such as Dirt Block, Metropolis Block, and Fossil Block.
    All Bosses - 23 Checks
    SAHABAR - 23 Checks
    Core Commander - 18 Checks
    Lower Wall - 7 Checks"""

    display_name = "Blocks"
    default = 0


class Fishsanity(Toggle):
    """Adds fishing checks such as Rock Jaw, Silver Dart, and Starlight Nautilus.
    All Bosses - 44 Checks
    SAHABAR - 44 Checks
    Core Commander - 39 Checks
    Lower Wall - 12 Checks"""

    display_name = "Fishsanity"
    default = 0


class Figurinesanity(Toggle):
    """Adds enemy and boss figurine checks.
    All Bosses - 71 Checks
    SAHABAR - 71 Checks
    Core Commander - 55 Checks
    Lower Wall - 22 Checks"""

    display_name = "Figurinesanity"
    default = 0


class Valuablesanity(Toggle):
    """Adds valuable-item checks such as Ammonite, Polished Shell, and Disabled Datapad.
    All Bosses - 116 Checks
    SAHABAR - 116 Checks
    Core Commander - 113 Checks
    Lower Wall - 40 Checks"""

    display_name = "Valuablesanity"
    default = 0


class Toolsanity(Toggle):
    """Adds tool checks such as Wood Pickaxe, Bug Net, and Octarine Fishing Pole.
    All Bosses - 41 Checks
    SAHABAR - 41 Checks
    Core Commander - 41 Checks
    Lower Wall - 23 Checks"""

    display_name = "Toolsanity"
    default = 0


class Weaponsanity(Toggle):
    """Adds weapon checks such as Rusty Dagger, Burnzooka, and Tome of the Deep.
    All Bosses - 75 Checks
    SAHABAR - 75 Checks
    Core Commander - 69 Checks
    Lower Wall - 32 Checks"""

    display_name = "Weaponsanity"
    default = 0


class Accessanity(Toggle):
    """Adds accessory checks such as Small Backpack, Medium Potion Pouch, and Royal Gel.
    All Bosses - 59 Checks
    SAHABAR - 59 Checks
    Core Commander - 58 Checks
    Lower Wall - 25 Checks"""

    display_name = "Accessanity"
    default = 0


class Jewelrysanity(Toggle):
    """Adds necklace and ring checks such as Cave Guppy Necklace and Skull Ring.
    All Bosses - 97 Checks
    SAHABAR - 97 Checks
    Core Commander - 94 Checks
    Lower Wall - 40 Checks"""

    display_name = "Jewelrysanity"
    default = 0


class Armorsanity(Toggle):
    """Adds armor checks such as Wood Helm, Magma Torso Armor, and Welder Leggings.
    All Bosses - 188 Checks
    SAHABAR - 188 Checks
    Core Commander - 170 Checks
    Lower Wall - 60 Checks"""

    display_name = "Armorsanity"
    default = 0


class Petsanity(Toggle):
    """Adds egg collection and pet hatching checks such as Collect Loyal Egg and Hatch Pheromoth.
    All Bosses - 28 Checks
    SAHABAR - 28 Checks
    Core Commander - 26 Checks
    Lower Wall - 14 Checks"""

    display_name = "Pets"
    default = 0


class Merchantsanity(Toggle):
    """Adds merchant checks for speaking with each of the 5 merchants.
    All Bosses - 5 Checks
    SAHABAR - 4 Checks
    Core Commander - 4 Checks
    Lower Wall - 2 Checks"""

    display_name = "Merchants"
    default = 0


class Enemies(Toggle):
    """Adds enemy checks for slaying each of the basic enemies.
    All Bosses - 49 Checks
    SAHABAR - 49 Checks
    Core Commander - 37 Checks
    Lower Wall - 18 Checks"""

    display_name = "Enemies"
    default = 1


class CattleMutilation(Toggle):
    """Adds checks for slaying the 7 livestock types such as Moolin, Dodo, and Crystal Snail.
    All Bosses - 7 Checks
    SAHABAR - 7 Checks
    Core Commander - 7 Checks
    Lower Wall - 3 Checks"""

    display_name = "Cattle Mutilation"
    default = 0


class LockedChests(Toggle):
    """Adds key and locked-chest unlock checks.
    All Bosses - 14 Checks
    SAHABAR - 14 Checks
    Core Commander - 12 Checks
    Lower Wall - 4 Checks"""

    display_name = "Locked Chests"
    default = 1


class Skillsanity(Toggle):
    """Adds checks every 10 levels for all twelve skills.
    All Bosses - 120 Checks
    SAHABAR - 108 Checks
    Core Commander - 72 Checks
    Lower Wall - 36 Checks"""

    display_name = "Skillsanity"
    default = 0


class RawMaterialCacheWeight(Range):
    """Relative filler weight for Raw Material Cache. All cache weights are normalized together."""
    display_name = "Raw Material Cache Weight"
    range_start = 0
    range_end = 100
    default = 25


class RefinedMaterialCacheWeight(Range):
    """Relative filler weight for Refined Material Cache. All cache weights are normalized together."""
    display_name = "Refined Material Cache Weight"
    range_start = 0
    range_end = 100
    default = 25


class PotionsCacheWeight(Range):
    """Relative filler weight for Potions Cache. All cache weights are normalized together."""
    display_name = "Potions Cache Weight"
    range_start = 0
    range_end = 100
    default = 10


class PetCacheWeight(Range):
    """Relative filler weight for Pet Cache. All cache weights are normalized together."""
    display_name = "Pet Cache Weight"
    range_start = 0
    range_end = 100
    default = 10


class MoneyCacheWeight(Range):
    """Relative filler weight for Money Cache. All cache weights are normalized together."""
    display_name = "Money Cache Weight"
    range_start = 0
    range_end = 100
    default = 20


class AutomationCacheWeight(Range):
    """Relative filler weight for Automation Cache. All cache weights are normalized together."""
    display_name = "Automation Cache Weight"
    range_start = 0
    range_end = 100
    default = 10


class EmptyCacheWeight(Range):
    """Relative filler weight for Empty Cache.

    Forced blank reward slots still become Empty Caches when every weight is zero.
    """
    display_name = "Empty Cache Weight"
    range_start = 0
    range_end = 100
    default = 0


# Tracker order is the canonical presentation order for the independent
# station-license options. Item generation, logic, and slot data consume this
# table so the settings page cannot silently drift from the tracker.
LICENSE_OPTIONS = (
    ("Progressive Workbench License", "workbench_license", 7),
    ("Progressive Anvil License", "anvil_license", 7),
    ("Progressive Furnace License", "furnace_license", 3),
    ("Salvage and Repair Station License", "repair_salvage_license", 1),
    ("Cooking Pot License", "cooking_pot_license", 1),
    ("Ancient Hologram Pod License", "hologram_license", 1),
    ("Table Saw License", "table_saw_license", 1),
    ("Fishing Workbench License", "fishing_workbench_license", 1),
    ("Egg Incubator License", "egg_incubator_license", 1),
    ("Key Casting Table License", "key_casting_table_license", 1),
    ("Progressive Alchemy Table License", "alchemy_table_license", 2),
    ("Progressive Jewelry Workbench License", "jewelry_workbench_license", 2),
    ("Progressive Automation Table License", "automation_table_license", 2),
    ("Progressive Smithing Table License", "smithing_table_license", 2),
    ("Boat Workbench License", "boat_workbench_license", 1),
    ("Electronics Table License", "electronics_table_license", 1),
    ("Pouch Workbench License", "pouch_workbench_license", 1),
    ("Glass Smelter License", "glass_smelter_license", 1),
    ("Distillery Table License", "distillery_table_license", 1),
    ("Rift Statue License", "rift_statue_license", 1),
    ("Upgrade Station License", "upgrade_station_license", 1),
    ("Glass Workbench License", "glass_workbench_license", 1),
    ("Railway Forge License", "railway_forge_license", 1),
    ("Loom License", "loom_license", 1),
    ("Go-Kart Workbench License", "go_kart_workbench_license", 1),
    ("Carpenter's Table License", "carpenter_table_license", 1),
    ("Livestock Workbench License", "livestock_workbench_license", 1),
    ("Painter's Table License", "painter_table_license", 1),
    ("Music Workbench License", "music_workbench_license", 1),
)

LICENSE_OPTION_BY_ITEM = {item: option for item, option, _ in LICENSE_OPTIONS}


def license_enabled(options, item_name: str) -> bool:
    return bool(getattr(options, LICENSE_OPTION_BY_ITEM[item_name]))


@dataclass
class CoreKeeperOptions(PerGameCommonOptions):
    """Options for the validated end-to-end main-version slice."""

    goal: Goal
    raw_materials: RawMaterials
    refined_materials: RefinedMaterials
    locked_chests: LockedChests
    seeds: Seeds
    food: Food
    enemies: Enemies
    unique_materials: UniqueMaterials
    key_items: KeyItems
    bosses: Bosses
    merchantsanity: Merchantsanity
    petsanity: Petsanity
    blocksanity: Blocksanity
    goldensanity: Goldensanity
    critters: Critters
    cattle_mutilation: CattleMutilation
    skillsanity: Skillsanity
    fishsanity: Fishsanity
    figurinesanity: Figurinesanity
    cardsanity: Cardsanity
    valuablesanity: Valuablesanity
    toolsanity: Toolsanity
    weaponsanity: Weaponsanity
    jewelrysanity: Jewelrysanity
    accessanity: Accessanity
    armorsanity: Armorsanity
    workbench_license: WorkbenchLicense
    anvil_license: AnvilLicense
    furnace_license: FurnaceLicense
    repair_salvage_license: RepairSalvageLicense
    cooking_pot_license: CookingPotLicense
    hologram_license: HologramLicense
    table_saw_license: TableSawLicense
    fishing_workbench_license: FishingWorkbenchLicense
    egg_incubator_license: EggIncubatorLicense
    key_casting_table_license: KeyCastingTableLicense
    alchemy_table_license: AlchemyTableLicense
    jewelry_workbench_license: JewelryWorkbenchLicense
    automation_table_license: AutomationTableLicense
    smithing_table_license: SmithingTableLicense
    boat_workbench_license: BoatWorkbenchLicense
    electronics_table_license: ElectronicsTableLicense
    pouch_workbench_license: PouchWorkbenchLicense
    glass_smelter_license: GlassSmelterLicense
    distillery_table_license: DistilleryTableLicense
    rift_statue_license: RiftStatueLicense
    upgrade_station_license: UpgradeStationLicense
    glass_workbench_license: GlassWorkbenchLicense
    railway_forge_license: RailwayForgeLicense
    loom_license: LoomLicense
    go_kart_workbench_license: GoKartWorkbenchLicense
    carpenter_table_license: CarpenterTableLicense
    livestock_workbench_license: LivestockWorkbenchLicense
    painter_table_license: PainterTableLicense
    music_workbench_license: MusicWorkbenchLicense
    skill_points: SkillPoints
    reward_tools: RewardTools
    reward_weapons: RewardWeapons
    reward_jewelry: RewardJewelry
    reward_accessories: RewardAccessories
    reward_armor: RewardArmor
    soul_seeker_cache: SoulSeekerCache
    titan_breath_cache: TitanBreathCache
    phantom_spark_cache: PhantomSparkCache
    rune_song_cache: RuneSongCache
    credence_of_ruin_cache: CredenceOfRuinCache
    stormbringer_cache: StormbringerCache
    raw_material_cache_weight: RawMaterialCacheWeight
    refined_material_cache_weight: RefinedMaterialCacheWeight
    potions_cache_weight: PotionsCacheWeight
    pet_cache_weight: PetCacheWeight
    money_cache_weight: MoneyCacheWeight
    automation_cache_weight: AutomationCacheWeight
    empty_cache_weight: EmptyCacheWeight
    death_link: DeathLink
    skill_xp_multiplier: SkillXpMultiplier
    infinite_merchant_stock: InfiniteMerchantStock
    merchant_sells_crown_summon: MerchantSellsCrownSummon
    early_repair_and_salvage: EarlyRepairAndSalvage
    prevent_priority_in_optional_checks: PreventPriorityInOptionalChecks
    prevent_priority_in_sanity: PreventPriorityInSanity


option_groups = [
    OptionGroup("Goals", [Goal]),
    OptionGroup("Checks (Default)", [
        RawMaterials,
        RefinedMaterials,
        LockedChests,
        Seeds,
        Food,
        Enemies,
    ]),
    OptionGroup("Checks (Optional)", [
        UniqueMaterials,
        KeyItems,
        Bosses,
        Merchantsanity,
        Petsanity,
        Blocksanity,
        Goldensanity,
        Critters,
        CattleMutilation,
    ]),
    OptionGroup("Checks (Sanity)", [
        Skillsanity,
        Fishsanity,
        Figurinesanity,
        Cardsanity,
        Valuablesanity,
        Toolsanity,
        Weaponsanity,
        Jewelrysanity,
        Accessanity,
        Armorsanity,
    ]),
    OptionGroup("Rewards (Licenses)", [
        WorkbenchLicense,
        AnvilLicense,
        FurnaceLicense,
        RepairSalvageLicense,
        CookingPotLicense,
        HologramLicense,
        TableSawLicense,
        FishingWorkbenchLicense,
        EggIncubatorLicense,
        KeyCastingTableLicense,
        AlchemyTableLicense,
        JewelryWorkbenchLicense,
        AutomationTableLicense,
        SmithingTableLicense,
        BoatWorkbenchLicense,
        ElectronicsTableLicense,
        PouchWorkbenchLicense,
        GlassSmelterLicense,
        DistilleryTableLicense,
        RiftStatueLicense,
        UpgradeStationLicense,
        GlassWorkbenchLicense,
        RailwayForgeLicense,
        LoomLicense,
        GoKartWorkbenchLicense,
        CarpenterTableLicense,
        LivestockWorkbenchLicense,
        PainterTableLicense,
        MusicWorkbenchLicense,
    ]),
    OptionGroup("Rewards (Items)", [
        SkillPoints,
        RewardTools,
        RewardWeapons,
        RewardJewelry,
        RewardAccessories,
        RewardArmor,
    ]),
    OptionGroup("Rewards (Caches)", [
        RawMaterialCacheWeight,
        RefinedMaterialCacheWeight,
        PotionsCacheWeight,
        PetCacheWeight,
        MoneyCacheWeight,
        AutomationCacheWeight,
        EmptyCacheWeight,
        SoulSeekerCache,
        TitanBreathCache,
        PhantomSparkCache,
        RuneSongCache,
        CredenceOfRuinCache,
        StormbringerCache,
    ]),
    OptionGroup("Game Options", [DeathLink]),
    OptionGroup("Quality of Life", [
        SkillXpMultiplier,
        InfiniteMerchantStock,
        MerchantSellsCrownSummon,
        EarlyRepairAndSalvage,
        PreventPriorityInOptionalChecks,
        PreventPriorityInSanity,
    ]),
]
