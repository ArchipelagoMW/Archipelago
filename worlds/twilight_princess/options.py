from dataclasses import dataclass

from Options import (
    Choice,
    DeathLink,
    OptionGroup,
    PerGameCommonOptions,
    StartInventoryPool,
    Toggle,
)


# Logic Settings
class LogicRules(Choice):
    """
    Controls what types of tricks the logic can expect you to perform.

    - Glitchless: Only intended mechanics are required
    - Glitched: Some glitches may be required
    """

    # - No Logic: No logical requirements are enforced

    display_name = "Logic Rules"
    option_glitchless = 0
    option_glitched = 1
    # option_no_logic = 2
    default = 0


# region Generation
class TrapFrequency(Choice):
    """
    Controls the frequency of traps in the game.
    """

    display_name = "Trap Frequency"
    option_no_traps = 0
    option_few = 1
    option_many = 3
    option_mayhem = 7
    option_nightmare = 100
    default = 0


class GoldenBugsShuffled(Toggle):
    """
    If enabled, golden bugs will be shuffled into the itempool.
    If disabled, bugs will be vanilla and agitha will not be progression
    """

    display_name = "Golden Bugs"
    default = True


class SkyCharactersShuffled(Toggle):
    """
    If enabled, sky characters will be shuffled into the itempool.
    If disabled, sky characters will be vanilla.
    """

    display_name = "Sky Characters"
    default = True


class NpcItemsShuffled(Toggle):
    """
    If enabled, Gifts from NPCs can be progression items.
    """

    display_name = "Gifts from NPCs"
    default = True


class ShopItemsShuffled(Toggle):
    """
    If enabled, Shop Items can be progression items.
    """

    display_name = "Shop Items"
    default = True


class HiddenSkillsShuffled(Toggle):
    """
    If enabled, golden wolfs can be progression items.
    \\*Hidden skills will always be shuffled into item pool.
    """

    display_name = "Hidden Skills"
    default = True


class PoeShuffled(Toggle):
    """
    If enabled, Poes will be shuffled into the itempool.
    If disabled, Poes will be vanilla.
    """

    display_name = "Poe Shuffled"
    default = True


class HeartPieceShuffled(Toggle):
    """
    If enabled, Heart Piece locations can contain progression items.
    """

    display_name = "Heart Pieces"
    default = True


class DungeonsShuffled(Toggle):
    """
    If enabled, Dungeons locations can contain progression items.
    Cannot be disabled if Overworld shuffle is disabled
    """

    display_name = "Dungeons Shuffled"
    default = True


class OverWoldShuffled(Toggle):
    """
    If enabled, Overworld locations can contain progression items.
    Cannot be disabled if Dungeon shuffle is disabled
    Note:
    Disabling may lead to generation failures as the possible location count is reduced dramtically.
    """

    display_name = "Overworld Items"
    default = True


class EarlyShadowCrystal(Toggle):
    """
    When Enabled Shadow Crystal will be placed into Sphere 1 of the local world
    """

    display_name = "Early Shadow Crystal"
    default = False


# endregion
# region Dungeon Items


class DungeonItem(Choice):
    value: int
    option_vanilla = 0
    option_own_dungeon = 1
    option_any_dungeon = 2
    option_anywhere = 3
    option_startwith = 4
    default = 0

    @property
    def in_dungeon(self) -> bool:
        return self.value in (0, 1, 2)


class SmallKeySettings(DungeonItem):
    """
    Controls how small keys are randomized.

    - **Start With Small Keys:** You will start the game with the small keys for all dungeons.
    - **Vanilla Small Keys:** Small keys will be kept in their vanilla location (non-randomized).
    - **Own Dungeon Small Keys:** Small keys will be randomized locally within their own dungeon.
    - **Any Dungeon Small Keys:** Small keys will be randomized locally within any dungeon.
    - **Anywhere:** Small keys can be found in any progression location, if dungeons are randomized.

    Note:
    Not shuffling Dungeons will overwrite this to vanilla, unless you selected start with
    """

    item_name_group = "Small Keys"
    display_name = "Randomize Small Keys"


class BigKeySettings(DungeonItem):
    """
    Controls how big keys are randomized.

    - **Start With Big Keys:** You will start the game with the big keys for all dungeons.
    - **Vanilla Big Keys:** Big keys will be kept in their vanilla location (non-randomized).
    - **Own Dungeon Big Keys:** Big keys will be randomized locally within their own dungeon.
    - **Any Dungeon Big Keys:** Big keys will be randomized locally within any dungeon.
    - **Anywhere:** Big keys can be found in any progression location.

    Note:
    Not shuffling Dungeons will overwrite this to vanilla, unless you selected start with
    """

    item_name_group = "Big Keys"
    display_name = "Randomize Big Keys"


class MapAndCompassSettings(DungeonItem):
    """
    Controls how dungeon maps and compasses are randomized.

    - **Start With Maps & Compasses:** You will start the game with the dungeon maps and compasses for all dungeons.
    - **Vanilla Maps & Compasses:** Dungeon maps and compasses will be kept in their vanilla location (non-randomized).
    - **Own Dungeon Maps & Compasses:** Dungeon maps and compasses will be randomized locally within their own dungeon.
    - **Any Dungeon Maps & Compasses:** Dungeon maps and compasses will be randomized locally within any dungeon.
    - **Anywhere:** Dungeon maps and compasses can be found anywhere, without restriction.

    Note:
    Not shuffling Dungeons will overwrite this to vanilla, unless you selected start with
    """

    item_name_group = "Maps and Compasses"
    display_name = "Randomize Maps & Compasses"


class DungeonRewardsProgression(Toggle):
    """
    Controls whether dungeon reward and heart containers are forced to have progression items.

    """

    display_name = "Dungeon Rewards are prgression"
    default = True


class SmallKeysOnBosses(Toggle):
    """
    If disabled, Small keys cannot be placed on boss rewards
    """

    display_name = "Small Keys on Bosses"
    default = False


# endregion
# region Access Settings


class CastleRequirements(Choice):
    """
    NON-DEFAULT CHOICE NOT REPRESENTED IN GAME (must self enforce if changed from default)
    Controls requirements for accessing Hyrule Castle.

    - Open: No requirements
    - Fused Shadows: Requires all Fused Shadows
    - Mirror Shards: Requires all Mirror Shards
    - All Dungeons: Requires completing all dungeons
    - Vanilla: Beat Palace of Twilight

    Note:
    Choosing All Dungeons or Vanilla will force dungeons items to be in Hyrule Castle if Any Dungeon is chosen for them
    \\*This also removes Hyrule castle from list of dungeons for other of that dungeon item to be in
    """

    display_name = "Castle Requirements"
    option_open = 0
    option_fused_shadows = 1
    option_mirror_shards = 2
    option_all_dungeons = 3
    option_vanilla = 4
    default = 0


class PalaceRequirements(Choice):
    """
    NON-DEFAULT CHOICE NOT REPRESENTED IN GAME (must self enforce if changed from default)
    Controls requirements for accessing Palace of Twilight.

    - Open: No requirements
    - Fused Shadows: Requires all Fused Shadows
    - Mirror Shards: Requires all Mirror Shards
    - Vanilla: Beat City in the Sky

    Note:
    Choosing Vanilla will force dungeons items to be in Palace of Twilight if Any Dungeon is chosen for them
    \\*This also removes Palace of Twilight from list of dungeons for other of that dungeon item to be in
    """

    display_name = "Palace Requirements"
    option_open = 0
    option_fused_shadows = 1
    option_mirror_shards = 2
    option_vanilla = 3
    default = 0


class FaronWoodsLogic(Choice):
    """
    NON-DEFAULT CHOICE NOT REPRESENTED IN GAME (must self enforce if changed from default)
    Controls logic for accessing Faron Woods.

    - Open: No special requirements
    - Closed: Requires forest temple to be beaten before leaving faron woods

    Note:
    Choosing Closed will force dungeons items to be in Forest Temple if Any Dungeon is chosen for them
    \\*This also removes Forest Temple from list of dungeons for other of that dungeon item to be in
    """

    display_name = "Faron Woods Logic"
    option_open = 0
    option_closed = 1
    default = 0


# endregion
# region Intro

# Timesavers
# class SkipPrologue(Toggle):
#     """
#     NON-DEFAULT CHOICE NOT REPRESENTED IN GAME (must self enforce if changed from default)
#     Controls whether the prologue is skipped.
#     """

#     display_name = "Skip Prologue"
#     default = True


# class FaronTwilightCleared(Toggle):
#     """
#     NON-DEFAULT CHOICE NOT REPRESENTED IN GAME (must self enforce if changed from default)
#     Controls whether Faron Twilight is cleared.
#     """

#     display_name = "Faron Twilight Cleared"
#     default = True


# class EldinTwilightCleared(Toggle):
#     """
#     NON-DEFAULT CHOICE NOT REPRESENTED IN GAME (must self enforce if changed from default)
#     Controls whether Eldin Twilight is cleared.
#     """

#     display_name = "Eldin Twilight Cleared"
#     default = True


# class LanayruTwilightCleared(Toggle):
#     """
#     NON-DEFAULT CHOICE NOT REPRESENTED IN GAME (must self enforce if changed from default)
#     Controls whether Lanayru Twilight is cleared.
#     """

#     display_name = "Lanayru Twilight Cleared"
#     default = True


# class SkipMdh(Toggle):
#     """
#     NON-DEFAULT CHOICE NOT REPRESENTED IN GAME (must self enforce if changed from default)
#     Controls whether the Midna's Darkest Hour is skipped.
#     """

#     display_name = "Skip Midna's Darkest Hour"
#     default = True

# endregion
# region Timesavers


class SkipMinorCutscenes(Toggle):
    """
    NON-DEFAULT CHOICE NOT REPRESENTED IN GAME (must self enforce if changed from default)
    If enabled, minor cutscenes are skipped.
    """

    display_name = "Skip Minor Cutscenes"
    default = True


class FastIronBoots(Toggle):
    """
    NON-DEFAULT CHOICE NOT REPRESENTED IN GAME (must self enforce if changed from default)
    If enabled, movement is not slowed when wearing Iron Boots.
    """

    display_name = "Fast Iron Boots"
    default = True


class QuickTransform(Toggle):
    """
    NON-DEFAULT CHOICE NOT REPRESENTED IN GAME (must self enforce if changed from default)
    If enabled, you can quickly transform by pressing R + Y.
    """

    display_name = "Quick Transform"
    default = True


class TransformAnywhere(Toggle):
    """
    NON-DEFAULT CHOICE NOT REPRESENTED IN GAME (must self enforce if changed from default)
    If enabled, the player can transform anywhere.
    """

    display_name = "Transform Anywhere"
    default = True


class IncreaseWalletCapacity(Toggle):
    """
    NON-DEFAULT CHOICE NOT REPRESENTED IN GAME (must self enforce if changed from default)
    If enabled, the wallet capacity is increased.
    """

    display_name = "Increase Wallet Capacity"
    default = True


class ModifyShopModels(Toggle):
    """
    NON-DEFAULT CHOICE NOT REPRESENTED IN GAME (must self enforce if changed from default)
    If enabled, swap shop models with the items that are placed there.
    """

    display_name = "Modify Shop Models"
    default = False


class GoronMinesEntrance(Choice):
    """
    NON-DEFAULT CHOICE NOT REPRESENTED IN GAME (must self enforce if changed from default)
    Controls requirements for accessing the Goron Mines.

    - **Closed:** Player must wrestle Gor Coron to enter the mines.
    - **No Wrestling:** Player does not have to wrestle Gor Coron.
    - **Open:** Same as No Wrestling but you can use the elevator immediately.
    """

    display_name = "Goron Mines Entrance"
    option_closed = 0
    option_no_wrestling = 1
    option_open = 2
    default = 2


class SkipLakebedEntrance(Toggle):
    """
    NON-DEFAULT CHOICE NOT REPRESENTED IN GAME (must self enforce if changed from default)
    If enabled, the Lakebed does not require water bombs.
    """

    display_name = "Lakebed Does not require water bombs"
    default = True


class SkipArbitersGroundsEntrance(Toggle):
    """
    NON-DEFAULT CHOICE NOT REPRESENTED IN GAME (must self enforce if changed from default)
    If enabled, entering Arbiters Grounds does not require defeating King Bublin.
    """

    display_name = "Arbiters Grounds Does not require Bublin Camp"
    default = True


class SkipSnowpeakEntrance(Toggle):
    """
    NON-DEFAULT CHOICE NOT REPRESENTED IN GAME (must self enforce if changed from default)
    If enabled, Snowpeak does not require Reekfish Scent.
    """

    display_name = "Snowpeak Does not require Reekfish Scent"
    default = True


class TotEntrance(Choice):
    """
    NON-DEFAULT CHOICE NOT REPRESENTED IN GAME (must self enforce if changed from default)
    Controls requirements for accessing the Temple of Time.

    - **Closed:** Player must defeat Skull Kid to access Sacred Grove. Master Sword needed to access Past.
    - **Open Grove:** Player doesn't need to defeat Skull Kid. Master Sword needed to access Past.
    - **Open:** Open Grove but player does not need Master Sword to access Past.
    """

    display_name = "Temple of Time Entrance"
    option_closed = 0
    option_open_grove = 1
    option_open = 2
    default = 2


class SkipCityInTheSkyEntrance(Toggle):
    """
    NON-DEFAULT CHOICE NOT REPRESENTED IN GAME (must self enforce if changed from default)
    If enabled, City in The Sky does not require filled Skybook.
    """

    display_name = "City in The Sky Does not require filled Skybook"
    default = True


class InstantMessageText(Toggle):
    """
    NON-DEFAULT CHOICE NOT REPRESENTED IN GAME (must self enforce if changed from default)
    If enabled, message text is instant.
    """

    display_name = "Instant Message Text"
    default = True


class OpenMap(Toggle):
    """
    NON-DEFAULT CHOICE NOT REPRESENTED IN GAME (must self enforce if changed from default)
    If enabled, Map areas are unlocked and portals unlocked.
    """

    display_name = "Open Map"
    default = True


class IncreaseSpinnerSpeed(Toggle):
    """
    NON-DEFAULT CHOICE NOT REPRESENTED IN GAME (must self enforce if changed from default)
    If enabled, spinner speed is increased.
    \\*Spinner speed not taken into account in logic.
    """

    display_name = "Increase Spinner Speed"
    default = True


class OpenDoorOfTime(Toggle):
    """
    NON-DEFAULT CHOICE NOT REPRESENTED IN GAME (must self enforce if changed from default)
    If enabled, the Door of Time is open.
    """

    display_name = "Open Door of Time"
    default = True


class DamageMagnification(Choice):
    """
    NON-DEFAULT CHOICE NOT REPRESENTED IN GAME (must self enforce if changed from default)
    Multiplies the damage the player takes.
    """

    display_name = "Damage Multiplier"
    option_vanilla = 1
    option_double = 2
    option_triple = 3
    option_quadruple = 4
    option_ohko = 5
    default = 1


class BonksDoDamage(Toggle):
    """
    NON-DEFAULT CHOICE NOT REPRESENTED IN GAME (must self enforce if changed from default)
    If enabled, bonks do damage.
    """

    display_name = "Bonks Do Damage"
    default = False


class SkipMajorCutscenes(Toggle):
    """
    NON-DEFAULT CHOICE NOT REPRESENTED IN GAME (must self enforce if changed from default)
    If enabled, major cutscenes are skipped.
    """

    display_name = "Skip Major Cutscenes"
    default = True


class StartingToD(Choice):
    """
    NON-DEFAULT CHOICE NOT REPRESENTED IN GAME (must self enforce if changed from default)
    Controls the starting time of day.
    """

    display_name = "Starting Time of Day"
    option_morning = 0
    option_noon = 1
    option_evening = 2
    option_night = 3
    default = 0


# endregion


@dataclass
class TPOptions(PerGameCommonOptions):
    """
    A data class that encapsulates all configuration options for The Wind Waker.
    """

    start_inventory_from_pool: StartInventoryPool
    death_link: DeathLink

    # Item Pool Settings
    golden_bugs_shuffled: GoldenBugsShuffled
    sky_characters_shuffled: SkyCharactersShuffled
    npc_items_shuffled: NpcItemsShuffled
    shop_items_shuffled: ShopItemsShuffled
    hidden_skills_shuffled: HiddenSkillsShuffled
    poe_shuffled: PoeShuffled
    heart_piece_shuffled: HeartPieceShuffled
    overworld_shuffled: OverWoldShuffled
    dungeons_shuffled: DungeonsShuffled

    # Dungeon Items
    small_key_settings: SmallKeySettings
    big_key_settings: BigKeySettings
    map_and_compass_settings: MapAndCompassSettings
    dungeon_rewards_progression: DungeonRewardsProgression
    small_keys_on_bosses: SmallKeysOnBosses

    # Logic Settings
    logic_rules: LogicRules
    castle_requirements: CastleRequirements
    palace_requirements: PalaceRequirements
    faron_woods_logic: FaronWoodsLogic

    # Timesavers
    # skip_prologue: SkipPrologue  #
    # faron_twilight_cleared: FaronTwilightCleared  #
    # eldin_twilight_cleared: EldinTwilightCleared  #
    # lanayru_twilight_cleared: LanayruTwilightCleared  #
    # skip_mdh: SkipMdh  #
    skip_minor_cutscenes: SkipMinorCutscenes
    skip_major_cutscenes: SkipMajorCutscenes
    fast_iron_boots: FastIronBoots
    quick_transform: QuickTransform
    instant_message_text: InstantMessageText
    open_map: OpenMap
    increase_spinner_speed: IncreaseSpinnerSpeed
    open_door_of_time: OpenDoorOfTime
    increase_wallet: IncreaseWalletCapacity

    # Additional Settings
    transform_anywhere: TransformAnywhere
    modify_shop_models: ModifyShopModels
    bonks_do_damage: BonksDoDamage
    trap_frequency: TrapFrequency
    damage_magnification: DamageMagnification
    starting_tod: StartingToD
    # hint_distribution: HintDistribution

    # Dungeon Entrance Settings
    skip_lakebed_entrance: SkipLakebedEntrance
    skip_arbiters_grounds_entrance: SkipArbitersGroundsEntrance
    skip_snowpeak_entrance: SkipSnowpeakEntrance
    skip_city_in_the_sky_entrance: SkipCityInTheSkyEntrance
    goron_mines_entrance: GoronMinesEntrance
    tot_entrance: TotEntrance

    early_shadow_crystal: EarlyShadowCrystal


tp_option_groups: list[OptionGroup] = [
    OptionGroup(
        "Item Pool / Location Settings",
        [
            GoldenBugsShuffled,
            SkyCharactersShuffled,
            NpcItemsShuffled,
            ShopItemsShuffled,
            HiddenSkillsShuffled,
            PoeShuffled,
            HeartPieceShuffled,
            OverWoldShuffled,
            DungeonsShuffled,
        ],
        start_collapsed=True,
    ),
    OptionGroup(
        "Logic Settings",
        [
            LogicRules,
            CastleRequirements,
            PalaceRequirements,
            FaronWoodsLogic,
        ],
        start_collapsed=True,
    ),
    OptionGroup(
        "Dungeon Items",
        [
            SmallKeySettings,
            BigKeySettings,
            MapAndCompassSettings,
            DungeonRewardsProgression,
        ],
        start_collapsed=True,
    ),
    OptionGroup(
        "Timesavers",
        [
            # SkipPrologue,
            # FaronTwilightCleared,
            # EldinTwilightCleared,
            # LanayruTwilightCleared,
            # SkipMdh,
            SkipMinorCutscenes,
            SkipMajorCutscenes,
            FastIronBoots,
            QuickTransform,
            # UnrequiredDungeonAreBarren,
            InstantMessageText,
            OpenMap,
            IncreaseSpinnerSpeed,
            OpenDoorOfTime,
            EarlyShadowCrystal,
        ],
        start_collapsed=True,
    ),
    OptionGroup(
        "Additional Settings",
        [
            TransformAnywhere,
            IncreaseWalletCapacity,
            BonksDoDamage,
            TrapFrequency,
            DamageMagnification,
            StartingToD,
            # HintDistribution,
        ],
        start_collapsed=True,
    ),
    OptionGroup(
        "Dungeon Entrance Settings",
        [
            SkipLakebedEntrance,
            SkipArbitersGroundsEntrance,
            SkipSnowpeakEntrance,
            SkipCityInTheSkyEntrance,
            GoronMinesEntrance,
            TotEntrance,
        ],
        start_collapsed=True,
    ),
]
