from dataclasses import dataclass

from Options import OptionGroup, Choice, Range, DefaultOnToggle, Toggle, DeathLink, OptionSet
from Options import PerGameCommonOptions


class GoalRequiresLevels(DefaultOnToggle):
    """If enabled, you have to complete action stages to unlock the last fight."""
    display_name = "Goal Requires Levels"


class LevelPercentage(Range):
    """If Levels are part of the goal, Percentage of the available levels that needed to be completed to unlock the final story."""
    display_name = "Level Requirement Percentage"
    range_start = 25
    range_end = 100
    default = 100


class GoalRequiresChaosEmeralds(Toggle):
    """
    If enabled, you have to collect all the Chaos Emeralds to unlock the last fight.
    Keep in mind selecting emerald hunt will require enough checks to add the 7 emeralds to the pool.
    """
    display_name = "Goal Requires Chaos Emeralds"


class GoalRequiresEmblems(DefaultOnToggle):
    """
    If enabled, you have to collect a certain number of emblems to unlock the last fight.
    The emblems are extra items added to the item pool, so they scale with the number of checks.
    """
    display_name = "Goal Requires Emblems"


class MaximumEmblemCap(Range):
    """
    If Emblems are part of the goal, determines the maximum number of emblems that can be in the item pool.
    If fewer available locations exist in the pool than this number, the number of available locations will be used instead.
    """
    display_name = "Max Emblem Cap"
    range_start = 20
    range_end = 1500
    default = 130


class EmblemPercentage(Range):
    """If Emblems are part of the goal, percentage of the available emblems needed to unlock the final story."""
    display_name = "Emblem Requirement Percentage"
    range_start = 1
    range_end = 90
    default = 75


class GoalRequiresMissions(Toggle):
    """If enabled, you have to complete missions to unlock the last fight."""
    display_name = "Goal Requires Missions"


class MissionPercentage(Range):
    """If Missions are part of the goal, Percentage of the available missions that needed to be completed to unlock the final story."""
    display_name = "Mission Requirement Percentage"
    range_start = 25
    range_end = 100
    default = 100


class GoalRequiresBosses(Toggle):
    """If enabled, you have to beat all the bosses to unlock the last fight."""
    display_name = "Goal Requires Bosses"


class BossPercentage(Range):
    """If Bosses are part of the goal, Percentage of the available bosses that needed to be completed to unlock the final story."""
    display_name = "Boss Requirement Percentage"
    range_start = 25
    range_end = 100
    default = 100


class GoalRequiresChaoRaces(Toggle):
    """If enabled, you have to beat all the chao races to unlock the last fight."""
    display_name = "Goal Requires Chao Races"


class LogicLevel(Choice):
    """
    Determines the logic the randomizer will use.
    Normal Logic (0): Very forgiving, ideal if you are not used to this game or its location checks.
    Hard Logic (1): Less forgiving logic, some checks require performing spindash jumps or dying to get the check.
    Expert DC Logic (2): The most unforgiving logic, some checks require performing out-of-bounds jumps (DC conversion).
    Expert DX Logic (3): The most unforgiving logic, some checks require performing out-of-bounds jumps (vanilla DX).
    Expert+ DX Logic (4): Same as Expert DX but with extra speed runner level tricks (vanilla DX).
    """
    display_name = "Logic Level"
    option_normal_logic = 0
    option_hard_logic = 1
    option_expert_dc_logic = 2
    option_expert_dx_logic = 3
    option_expert_plus_dx_logic = 4
    default = 0


class StartingCharacterOption(Choice):
    """
    Select which the character you will start with.
    Choose between Random (0), Sonic (1), Tails (2), Knuckles (3), Amy (4), Big (5), and Gamma (6).
    """
    display_name = "Starting Character"
    option_random_character = 0
    option_sonic = 1
    option_tails = 2
    option_knuckles = 3
    option_amy = 4
    option_big = 5
    option_gamma = 6
    default = 0


class StartingLocationOption(Choice):
    """
    Select in which location you would like to start.
    Station Square Main (0): Vanilla starting location and default value.
    Random (1): Start in a random location (same for all characters).
    Random per Character (2): Each character starts in a different random location.
    """
    display_name = "Starting Location"
    option_station_square_main = 0
    option_random_location = 1
    option_random_location_per_character = 2
    default = 0


class EntranceRandomizer(Choice):
    """
    Randomizes the entrances to action stages, bosses, sublevels and Chao Gardens.
    Disabled (0): No entrance randomization.
    Stages (1): Only action stages entrances are randomized.
    Stages and Bosses (2): Action stages, bosses, sublevels and Chao Gardens entrances are randomized.
    """
    display_name = "Entrance Randomizer"
    option_disabled = 0
    option_stages = 1
    option_stages_and_bosses = 2
    default = 0
    alias_false = 0
    alias_true = 1


class GatingMode(Choice):
    """
    Determines how the rando will close off parts of the adventure field.
    Emblems (0): Areas are gated based on the number of emblems collected.
    KeyItems (1): Areas are gated based on key items like the Train or Station Key
    """
    display_name = "Gating Mode"
    option_emblems_gating = 0
    option_key_items_gating = 1
    default = 0


class SendDeathLinkChance(Range):
    """When dying, the chance of sending a death link to another player."""
    display_name = "Send Death Link Chance"
    range_start = 1
    range_end = 100
    default = 100


class ReceiveDeathLinkChance(Range):
    """When receiving a death link, the chance of dying."""
    display_name = "Receive Death Link Chance"
    range_start = 1
    range_end = 100
    default = 100


class RingLink(Choice):
    """
    Whether your in-level ring gain/loss is linked to other players.
    Disabled (0): Ring Link is disabled.
    Enabled (1): Rings are sent and received in normal situations.
    Enabled Casinopolis (2): Rings are sent and received in most situations, plus while playing Sonic's Casinopolis.
    Enabled Hard (3): Rings are sent and received when including finishing a level and during the Perfect Chaos fight.

    """
    display_name = "Ring Link"
    option_disabled = 0
    option_enabled = 1
    option_enabled_casinopolis = 2
    option_enabled_hard = 3
    default = 0
    alias_false = 0
    alias_true = 1


class RingLoss(Choice):
    """
    How taking damage is handled.
    Classic (0): You lose all of your rings when hit.
    Modern (1): You lose 20 rings when hit.
    One Hit K.O. (2): You die immediately when hit.
    One Hit K.O. No Shields (3): You die immediately when hit, and you can't use shields or invincibility power ups.
    """
    display_name = "Ring Loss"
    option_classic = 0
    option_modern = 1
    option_one_hit_k_o = 2
    option_one_hit_k_o_no_shields = 3
    default = 0


class TrapLink(Toggle):
    """
    Whether your received traps are linked to other players
    """
    display_name = "Trap Link"


class PlayableSonic(DefaultOnToggle):
    """Determines whether Sonic is playable."""
    display_name = "Playable Sonic"


class PlayableTails(DefaultOnToggle):
    """Determines whether Tails is playable."""
    display_name = "Playable Tails"


class PlayableKnuckles(DefaultOnToggle):
    """Determines whether Knuckles is playable."""
    display_name = "Playable Knuckles"


class PlayableAmy(DefaultOnToggle):
    """Determines whether Amy is playable."""
    display_name = "Playable Amy"


class PlayableGamma(DefaultOnToggle):
    """Determines whether Gamma is playable."""
    display_name = "Playable Gamma"


class PlayableBig(DefaultOnToggle):
    """Determines whether Big is playable."""
    display_name = "Playable Big"


class BaseActionStageMissionChoice(Choice):
    """
        For missions, the options range from 0 to 4.
        0 means no missions at all (You can still play the character if they are enabled).
        1 means Mission C.
        2 means Missions B and C.
        3 means Missions A, B, and C.
        4 means Missions S, A, B, and C. S missions are extra hard times added by the mod. Not available in normal logic.
    """
    option_none = 0
    option_c = 1
    option_c_b = 2
    option_c_b_a = 3
    option_c_b_a_s = 4
    default = 1


class SonicActionStageMissions(BaseActionStageMissionChoice):
    """Choose what action stage missions will be a location check for Sonic."""
    display_name = "Sonic's Action Stage Missions"


class TailsActionStageMissions(BaseActionStageMissionChoice):
    """Choose what action stage missions will be a location check for Tails."""
    display_name = "Tails' Action Stage Missions"


class KnucklesActionStageMissions(BaseActionStageMissionChoice):
    """Choose what action stage missions will be a location check for Knuckles."""
    display_name = "Knuckles' Action Stage Missions"


class AmyActionStageMissions(BaseActionStageMissionChoice):
    """Choose what action stage missions will be a location check for Amy."""
    display_name = "Amy's Action Stage Missions"


class GammaActionStageMissions(BaseActionStageMissionChoice):
    """Choose what action stage missions will be a location check for Gamma."""
    display_name = "Gamma's Action Stage Missions"


class BigActionStageMissions(BaseActionStageMissionChoice):
    """Choose what action stage missions will be a location check for Big."""
    display_name = "Big's Action Stage Missions"


class MusicSource(Choice):
    """
    Selects the source of the game's music.

    You can mix and match music from SADX, SA2B, and custom tracks.
    Custom songs are mapped to the Sonic Heroes soundtrack by default,
    but you're free to replace them with any songs you prefer.

    Choose between: SADX (0), SA2B (1), Custom (2), SADX + SA2B (3), SADX + Custom (4), SA2B + Custom (5),
    or SADX + SA2B + Custom (6).

    NOTE: You must own SA2B and/or Sonic Heroes on PC to use their music.
    """
    display_name = "MusicSource"
    option_sadx = 0
    option_sa2b = 1
    option_custom = 2
    option_sadx_sa2b = 3
    option_sadx_custom = 4
    option_sa2b_custom = 5
    option_sadx_sa2b_custom = 6
    default = 0


class MusicShuffle(Choice):
    """
    Controls how music is randomized in the game.

    Disabled (0 - default): Use original tracks without randomization.
    Curated (1): Randomize music using a hand-picked list that fits the original tone.
    By Type (2): Randomize songs within the same category (e.g., levels, bosses).
    Full (3): Randomize across the entire pool of available tracks.
    Singularity (4): Replace every song with the same single track.

    Options 1 and 2 are recommended for the most coherent experience.
    """
    display_name = "Music Shuffle"
    option_disabled = 0
    option_curated = 1
    option_by_type = 2
    option_full = 3
    option_singularity = 4
    default = 0


class MusicShuffleConsistency(Choice):
    """
    Defines how frequently music changes during gameplay.

    Static (0 - default): Music remains the same for the seed/slot.
    On Restart (1): Music is reshuffled every time the game is restarted.
    Per Play (2): Music changes every time it starts playing.

    Note: Shuffling is handled on the client side, using the seed and song.json file.
    """
    display_name = "Music Shuffle Consistency"
    option_static = 0
    option_on_restart = 1
    option_per_play = 2
    default = 0


class LifeCapsulesChangeSongs(Toggle):
    """
    If enabled, collecting a Life Capsule will trigger a music change, based on your current Music Shuffle settings.
    Only available if Music Shuffle is consistency is set to Per Play (2).
    """
    display_name = "Life Capsules Change Songs"


class RandomizedUpgrades(DefaultOnToggle):
    """Determines whether upgrades are randomized and sent to the item pool."""
    display_name = "Randomize Everyone's Upgrades"


class BossChecks(DefaultOnToggle):
    """Determines whether beating a boss grants a check (15 Locations)."""
    display_name = "Boss Checks"


class UnifyChaos4(Toggle):
    """Determines whether the Chaos 4 fight counts as a single location or three (Sonic, Tails, and Knuckles)."""
    display_name = "Unify Chaos 4"


class UnifyChaos6(Toggle):
    """Determines whether the Chaos 6 fight counts as a single location or three (Sonic, Big, and Knuckles)."""
    display_name = "Unify Chaos 6"


class UnifyEggHornet(Toggle):
    """Determines whether the Egg Hornet fight counts as a single location or two (Sonic, Tails)."""
    display_name = "Unify Egg Hornet"


class FieldEmblemsChecks(DefaultOnToggle):
    """Determines whether collecting field emblems grants checks (12 Locations)."""
    display_name = "Field Emblems Checks"


class SecretChaoEggs(Toggle):
    """Determines whether getting the 3 secret chao eggs grants checks (3 Locations)."""
    display_name = "Secret Chao Egg Checks"


class ChaoRacesChecks(Toggle):
    """Determines whether winning the chao races grants checks (5 Locations)."""
    display_name = "Chao Races Checks"


class ChaoRacesLevelsToAccessPercentage(Range):
    """
    Percentage of the available levels accessible for the chao races to be in logic.
    Higher values means races are required later in the game.
    """
    display_name = "Level Access Percentage for Chao Races"
    range_start = 25
    range_end = 100
    default = 100


class MissionChecks(Toggle):
    """Determines whether completing missions grants checks (60 Locations)."""
    display_name = "Enable Mission Checks"


class AutoStartMissions(Toggle):
    """Determines whether missions will start already activated."""
    display_name = "Auto Start Missions"


class MissionBlackList(OptionSet):
    """Determines what missions are blacklisted. The default are:
    Mission 49 (Flags in the Kart section of Twinkle Park).
    Mission 53 (Triple Jump in the Snowboard section of Ice Cap).
    Mission 54 (Flags in the Snowboard section of Ice Cap).
    Mission 58 (Flags in the rolling bounce section of Lost World).
    Also, you can blacklist all the missions by using the character names. i.e. {'Big', 'Sonic'}
    """
    display_name = "Mission Blacklist"
    default = {'49', '53', '54', '58'}
    valid_keys = [str(i) for i in range(1, 61)] + ["Sonic", "Tails", "Knuckles", "Amy", "Big", "Gamma"]


class TwinkleCircuitChecks(Choice):
    """
    Determines whether beating Twinkle Circuit grants a checks
    Disabled (0): Twinkle Circuit disabled.
    Enabled (1): Twinkle Circuit enabled (1 location).
    Enabled Multiple (2): Enable a different track for each character as well (+5 locations).
    """
    display_name = "Twinkle Circuit Check"
    option_disabled = 0
    option_enabled = 1
    option_enabled_multiple = 2
    default = 1
    alias_false = 0
    alias_true = 1


class SandHillChecks(Choice):
    """
    Determines whether beating Sand Hill grants a check:
    Disabled (0): Sand Hill disabled.
    Enabled (1): Sand Hill enabled (1 location).
    Enabled Hard (2): Harder (points-based) Sand Hill mission enabled (+1 location).
    """
    display_name = "Sand Hill Check"
    option_disabled = 0
    option_enabled = 1
    option_enabled_hard = 2
    default = 1
    alias_false = 0
    alias_true = 1


class SkyChaseChecks(Choice):
    """
    Determines whether beating Sky Chase grants a check:
    Disabled (0): Sky Chase disabled.
    Enabled (1): Sky Chase Act 1 and 2 enabled (2 locations).
    Enabled Hard (2): Harder (points-based) Sky Chase missions enabled (+2 locations).
    """
    display_name = "Sky Chase Checks"
    option_disabled = 0
    option_enabled = 1
    option_enabled_hard = 2
    default = 1
    alias_false = 0
    alias_true = 1


class EnemySanity(Toggle):
    """
    Determines whether destroying enemies grants checks (710 Locations).
    You need to enable enemy-sanity for some characters for it to work.
    """
    display_name = "Enemy Sanity"


class EnemySanityList(OptionSet):
    """
    Determines which enemies are included in enemy-sanity.
    Character names are used as values
    """
    display_name = "EnemySanityList"
    default = {'Sonic', 'Tails', 'Knuckles', 'Amy', 'Big', 'Gamma'}
    valid_keys = ['Sonic', 'Tails', 'Knuckles', 'Amy', 'Big', 'Gamma']


class MissableEnemies(DefaultOnToggle):
    """Determines whether enemies in missable locations grant checks. This includes:
    - Enemies in the Casinopolis Sewers (Sonic and Tails)
    - Enemies in the Kart section of Sonic's Twinkle Park
    """
    display_name = "Include Missable Capsules"


class CapsuleSanity(Toggle):
    """
    Determines whether destroying capsules grants checks (692 Locations).
    You need to enable capsule-sanity for some characters and some types for it to work.
    """
    display_name = "Capsule Sanity"


class CapsuleSanityList(OptionSet):
    """
    Determines which capsules are included in capsule-sanity.
    You can sue Character name and capsule type as values.
    X-Life, X-Shield, X-PowerUp, and X-Ring with X being the character name (i.e. 'Sonic-PowerUp')
    """
    display_name = "CapsuleSanityList"
    default = {'Sonic-Life', 'Sonic-Shield', 'Sonic-PowerUp', 'Sonic-Ring',
               'Tails-Life', 'Tails-Shield', 'Tails-PowerUp', 'Tails-Ring',
               'Knuckles-Life', 'Knuckles-Shield', 'Knuckles-PowerUp', 'Knuckles-Ring',
               'Amy-Life', 'Amy-Shield', 'Amy-PowerUp', 'Amy-Ring',
               'Big-Life', 'Big-Shield', 'Big-PowerUp', 'Big-Ring',
               'Gamma-Life', 'Gamma-Shield', 'Gamma-PowerUp', 'Gamma-Ring'}
    valid_keys = ['Sonic-Life', 'Sonic-Shield', 'Sonic-PowerUp', 'Sonic-Ring',
                  'Tails-Life', 'Tails-Shield', 'Tails-PowerUp', 'Tails-Ring',
                  'Knuckles-Life', 'Knuckles-Shield', 'Knuckles-PowerUp', 'Knuckles-Ring',
                  'Amy-Life', 'Amy-Shield', 'Amy-PowerUp', 'Amy-Ring',
                  'Big-Life', 'Big-Shield', 'Big-PowerUp', 'Big-Ring',
                  'Gamma-Life', 'Gamma-Shield', 'Gamma-PowerUp', 'Gamma-Ring']


class MissableCapsules(DefaultOnToggle):
    """Determines whether capsules in missable locations grant checks. This includes:
    - Capsules in the Casinopolis Sewers (Sonic and Tails)
    - Capsules in the Kart section of Sonic's Twinkle Park
    - Capsules in the 'Going Down?' section of Sonic's Speed Highway
    - Capsules in the Boulder section of Sonic's Lost World
    """
    display_name = "Include Missable Capsules"


class PinballCapsules(Toggle):
    """Determines whether pinball's capsules grant checks (5 Locations)."""
    display_name = "Include Pinball's Capsules"


class FishSanity(Toggle):
    """Determines whether catching every type of fish grants checks (23 Locations)."""
    display_name = "Fish Sanity"


class LazyFishing(Choice):
    """
    Enabling Lazy Fishing grants infinite tension during fishing if you have the Power Rod upgrade.
    Depending on your option, the Power Rod will be a logic requirement or not for your locations:
    0: Disabled (default).
    1: Enabled, no requirements (Power Rod is not a logic requirement for any location check).
    2: Enabled, fishsanity (Power Rod is a logic requirement for fish-sanity only).
    3: Enabled, all (Power Rod is a logic requirement for fish-sanity, B/A/S ranks and every "Keeper" mission for Big).
    """
    display_name = "Lazy Fishing"
    option_disabled = 0
    option_enabled_no_requirements = 1
    option_enabled_fishsanity = 2
    option_enabled_all = 3
    default = 0


class JunkFillPercentage(Range):
    """
    Replace a percentage of non-required emblems in the item pool with random junk items.
    """
    display_name = "Junk Fill Percentage"
    range_start = 0
    range_end = 100
    default = 50


class TrapFillPercentage(Range):
    """
    Replace a percentage of junk items in the item pool with random traps.
    """
    display_name = "Trap Fill Percentage"
    range_start = 0
    range_end = 100
    default = 0


class BaseTrapWeight(Choice):
    """
    Base class for trap weights.
    The available options are 0 (off), 1 (low), 2 (medium), and 4 (high).
    """
    option_none = 0
    option_low = 1
    option_medium = 2
    option_high = 4
    default = 2


class IceTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap that freezes the player in place.
    """
    display_name = "Ice Trap Weight"


class SpringTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap that spawns a spring that sends the player flying in the opposite direction.
    """
    display_name = "Spring Trap Weight"


class PoliceTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap that spawns a lot of Cop Speeder enemies.
    """
    display_name = "Police Trap Weight"


class BuyonTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap that spawns a lot of Buyon enemies.
    """
    display_name = "Buyon Trap Weight"


class ReverseTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap that reverses your controls.
    """
    display_name = "Reverse Controls Trap Weight"


class GravityTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap that increments your gravity.
    """
    display_name = "Gravity Trap Weight"


class ReverseControlTrapDuration(Range):
    """
    How many seconds the reverse control trap will last. If set to 0, the trap will last until you die or change level.
    """
    display_name = "Reverse Control Trap Duration"
    range_start = 0
    range_end = 60
    default = 10


class TrapsAndFillerOnAdventureFields(DefaultOnToggle):
    """If enabled, traps and filler can activate in the adventure field."""
    display_name = "Traps and filler on Adventure Fields"


class TrapsAndFillerOnBossFights(DefaultOnToggle):
    """If enabled, traps and filler can activate during boss fights."""
    display_name = "Traps and filler on Boss Fights"


class TrapsAndFillerOnPerfectChaosFight(Toggle):
    """
    If enabled, traps and filler can activate during the Perfect Chaos fight.
    Keep in mind that enemy traps will subtract rings from the player.
    """
    display_name = "Traps and filler on Perfect Chaos Fight"


@dataclass
class SonicAdventureDXOptions(PerGameCommonOptions):
    goal_requires_levels: GoalRequiresLevels
    levels_percentage: LevelPercentage
    goal_requires_chaos_emeralds: GoalRequiresChaosEmeralds
    goal_requires_emblems: GoalRequiresEmblems
    max_emblem_cap: MaximumEmblemCap
    emblems_percentage: EmblemPercentage
    goal_requires_missions: GoalRequiresMissions
    mission_percentage: MissionPercentage
    goal_requires_bosses: GoalRequiresBosses
    boss_percentage: BossPercentage
    goal_requires_chao_races: GoalRequiresChaoRaces

    logic_level: LogicLevel
    starting_character: StartingCharacterOption
    starting_location: StartingLocationOption
    entrance_randomizer: EntranceRandomizer
    gating_mode: GatingMode

    death_link: DeathLink
    send_death_link_chance: SendDeathLinkChance
    receive_death_link_chance: ReceiveDeathLinkChance
    ring_link: RingLink
    ring_loss: RingLoss
    trap_link: TrapLink

    playable_sonic: PlayableSonic
    playable_tails: PlayableTails
    playable_knuckles: PlayableKnuckles
    playable_amy: PlayableAmy
    playable_big: PlayableBig
    playable_gamma: PlayableGamma

    sonic_action_stage_missions: SonicActionStageMissions
    tails_action_stage_missions: TailsActionStageMissions
    knuckles_action_stage_missions: KnucklesActionStageMissions
    amy_action_stage_missions: AmyActionStageMissions
    big_action_stage_missions: BigActionStageMissions
    gamma_action_stage_missions: GammaActionStageMissions

    music_source: MusicSource
    music_shuffle: MusicShuffle
    music_shuffle_consistency: MusicShuffleConsistency
    life_capsules_change_songs: LifeCapsulesChangeSongs

    randomized_upgrades: RandomizedUpgrades

    boss_checks: BossChecks
    unify_chaos4: UnifyChaos4
    unify_chaos6: UnifyChaos6
    unify_egg_hornet: UnifyEggHornet

    field_emblems_checks: FieldEmblemsChecks
    chao_egg_checks: SecretChaoEggs
    chao_races_checks: ChaoRacesChecks
    chao_races_levels_to_access_percentage: ChaoRacesLevelsToAccessPercentage
    mission_mode_checks: MissionChecks
    auto_start_missions: AutoStartMissions
    mission_blacklist: MissionBlackList
    twinkle_circuit_checks: TwinkleCircuitChecks
    sand_hill_checks: SandHillChecks
    sky_chase_checks: SkyChaseChecks

    enemy_sanity: EnemySanity
    enemy_sanity_list: EnemySanityList
    missable_enemies: MissableEnemies

    capsule_sanity: CapsuleSanity
    capsule_sanity_list: CapsuleSanityList
    missable_capsules: MissableCapsules
    pinball_capsules: PinballCapsules

    fish_sanity: FishSanity
    lazy_fishing: LazyFishing

    junk_fill_percentage: JunkFillPercentage
    trap_fill_percentage: TrapFillPercentage
    ice_trap_weight: IceTrapWeight
    spring_trap_weight: SpringTrapWeight
    police_trap_weight: PoliceTrapWeight
    buyon_trap_weight: BuyonTrapWeight
    reverse_trap_weight: ReverseTrapWeight
    gravity_trap_weight: GravityTrapWeight

    reverse_trap_duration: ReverseControlTrapDuration
    traps_and_filler_on_adventure_fields: TrapsAndFillerOnAdventureFields
    traps_and_filler_on_boss_fights: TrapsAndFillerOnBossFights
    traps_and_filler_on_perfect_chaos_fight: TrapsAndFillerOnPerfectChaosFight


sadx_option_groups = [
    OptionGroup("General Options", [
        LogicLevel,
        GatingMode,
        GoalRequiresLevels,
        LevelPercentage,
        GoalRequiresChaosEmeralds,
        GoalRequiresEmblems,
        MaximumEmblemCap,
        EmblemPercentage,
        GoalRequiresMissions,
        MissionPercentage,
        GoalRequiresBosses,
        BossPercentage,
        GoalRequiresChaoRaces,
        StartingCharacterOption,
        StartingLocationOption,
        EntranceRandomizer,
        SendDeathLinkChance,
        ReceiveDeathLinkChance,
        RingLoss,
    ]),
    OptionGroup("Characters Options", [
        PlayableSonic,
        PlayableTails,
        PlayableKnuckles,
        PlayableAmy,
        PlayableBig,
        PlayableGamma,
    ]),
    OptionGroup("Stage Options", [
        SonicActionStageMissions,
        TailsActionStageMissions,
        KnucklesActionStageMissions,
        AmyActionStageMissions,
        BigActionStageMissions,
        GammaActionStageMissions
    ]),
    OptionGroup("Music Options", [
        MusicSource,
        MusicShuffle,
        MusicShuffleConsistency,
        LifeCapsulesChangeSongs,
    ]),
    OptionGroup("Bosses Options", [
        BossChecks,
        UnifyChaos4,
        UnifyChaos6,
        UnifyEggHornet,
    ]),

    OptionGroup("Sanity Options", [
        EnemySanity,
        EnemySanityList,
        MissableEnemies,
        CapsuleSanity,
        CapsuleSanityList,
        MissableCapsules,
        PinballCapsules,
        FishSanity,
        LazyFishing,
    ]),

    OptionGroup("Extra locations", [
        RandomizedUpgrades,
        FieldEmblemsChecks,
        SecretChaoEggs,
        ChaoRacesChecks,
        ChaoRacesLevelsToAccessPercentage,
        MissionChecks,
        AutoStartMissions,
        MissionBlackList,
        TwinkleCircuitChecks,
        SandHillChecks,
        SkyChaseChecks,
    ]),

    OptionGroup("Junk Options", [
        JunkFillPercentage,
        TrapFillPercentage,
        IceTrapWeight,
        SpringTrapWeight,
        PoliceTrapWeight,
        BuyonTrapWeight,
        ReverseTrapWeight,
        GravityTrapWeight,
        ReverseControlTrapDuration,
        TrapsAndFillerOnAdventureFields,
        TrapsAndFillerOnBossFights,
        TrapsAndFillerOnPerfectChaosFight
    ]),

]
