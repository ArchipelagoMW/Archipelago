from dataclasses import dataclass
from typing import Dict, Any
from Options import Range, Toggle, DeathLink, Choice, StartInventoryPool, PerGameCommonOptions,  OptionGroup, \
    DefaultOnToggle

# -----------------------Settings for Gameplay decisions ---------------


class InitialWeapon(Choice):
    """
    Chooses your initial weapon. Note you are not be able to equip the sword in the weapon hub in WeaponSanity until
    you unlock it.
    """
    display_name = "Weapon"
    option_Sword = 0
    option_Bow = 1
    option_Spear = 2
    option_Shield = 3
    option_Fist = 4
    option_Gun = 5


class LocationSystem(Choice):
    """
    Chooses how the game gives you items. (1) RoomBased gives items on every new room completed. (2) ScoreBased
    gives items according to score obtained by clearing rooms (even repeated ones). (3) RoomWeaponBased gives
    items on every new room completed with a new weapon (so more locations than the original room based system).
    """
    display_name = "Location System"
    option_room_based = 1
    option_score_based = 2
    option_room_weapon_based = 3
    default = 1


class ScoreRewardsAmount(Range):
    """
    When using score based system, this sets how many checks are available based on the score.
    Each room in hades gives "its depth" in score when completed, and each new check needs one more
    point to be unlocked (so check 10 needs 10 points, which can be obtained, for example,
    by completing rooms 5 and 6)
    """
    display_name = "ScoreRewardsAmount"
    range_start = 72
    range_end = 1000
    default = 150


class KeepsakeSanity(DefaultOnToggle):
    """
    Shuffles NPCs' keepsakes into the item pool, and makes each keepsake location a check. 
    For simplicity this does not affects Hades and Persephone.
    """
    display_name = "KeepsakeSanity"
    

class WeaponSanity(DefaultOnToggle):
    """
    Shuffles weapons (except your initial weapon) into the item pool, and makes obtaining
    each weapon at the House Contractor's shop a check.
    Need to be sent the weapon item to gain the skill to equip them.
    """
    display_name = "WeaponSanity"
    

class HiddenAspectSanity(DefaultOnToggle):
    """
    Shuffles weapon aspects into the item pool, and makes obtaining each aspect a check 
    (which needs to be unlocked before being able to be bought).
    """
    display_name = "HiddenAspectSanity"


class StoreSanity(DefaultOnToggle):
    """
    Shuffles important items from the House Contractor's shop in the item pool.
    Need to be sent the items to gain the different perks that make runs easier.
    """
    display_name = "StoreSanity"
    

class FateSanity(DefaultOnToggle):
    """
    Shuffles most rewards from the Fated List of Prophecies into the item pool, 
    and makes the corresponding items from the list a check. 
    Can make the games significantly longer.
    """
    display_name = "FateSanity"

# -------------------- Endgame settings


class HadesDefeatsNeeded(Range):
    """
    How many times you need to defeat Hades to win the world. 10 is for credits.
    """
    display_name = "HadesDefeatsNeeded"
    range_start = 1
    range_end = 20
    default = 1


class WeaponsClearsNeeded(Range):
    """
    How many different weapons clears are needed to win the world.
    """
    display_name = "WeaponsClearsNeeded"
    range_start = 1
    range_end = 6
    default = 1
    

class KeepsakesNeeded(Range):
    """
    How many different keepsake unlocks are needed to win the world.
    """
    display_name = "KeepsakesNeeded"
    range_start = 0
    range_end = 23
    default = 0


class FatesNeeded(Range):
    """
    How many different Fated List completions are needed to win the world.
    """
    display_name = "FatesNeeded"
    range_start = 0
    range_end = 35
    default = 0


# -----------------------Settings for Pact levels ---------------

class HeatSystem(Choice):
    """
    Choose either ReverseHeat (1), MinimalHeat (2) or VanillaHeat(3) for the game.
    In ReverseHeat you start with heat pacts that cannot be disabled until you get the corresponding pact item.
    In Minimal the settings for the PactsAmounts below set your minimal heat to be set, and cannot go below that level.
    If not wanting to have one of this heat systems on, chose Vanilla heat 
    (then the following options related to pacts do nothing).
    """
    display_name = "Heat System"
    option_reverse_heat = 1
    option_minimal_heat = 2
    option_vanillla_heat = 3
    default = 1


class HardLaborPactAmount(Range):
    """
    Choose the amount of Hard Labor pacts in the pool.
    """
    display_name = "Hard Labor Pact Amount"
    range_start = 0
    range_end = 5
    default = 3


class LastingConsequencesPactAmount(Range):
    """
    Choose the amount of Lasting Consequences pacts in the pool.
    """
    display_name = "Lasting Consequences Pact Amount"
    range_start = 0
    range_end = 4
    default = 2


class ConvenienceFeePactAmount(Range):
    """
    Choose the amount of Convenience Fee pacts in the pool.
    """
    display_name = "Convenience Fee Pact Amount"
    range_start = 0
    range_end = 2
    default = 1


class JurySummonsPactAmount(Range):
    """
    Choose the amount of Jury Summons pacts in the pool.
    """
    display_name = "Jury Summons Pact Amount"
    range_start = 0
    range_end = 3
    default = 2


class ExtremeMeasuresPactAmount(Range):
    """
    Choose the amount of Extreme Measures pacts in the pool.
    """
    display_name = "Extreme Measures Pact Amount"
    range_start = 0
    range_end = 4
    default = 2


class CalisthenicsProgramPactAmount(Range):
    """
    Choose the amount of Calisthenics Program pacts in the pool.
    """
    display_name = "Calisthenics Program Pact Amount"
    range_start = 0
    range_end = 2
    default = 1


class BenefitsPackagePactAmount(Range):
    """
    Choose the amount of Benefits Package pacts in the pool.
    """
    display_name = "Benefits Package Pact Amount"
    range_start = 0
    range_end = 2
    default = 1


class MiddleManagementPactAmount(Range):
    """
    Choose the amount of Middle Management pacts in the pool.
    """
    display_name = "Middle Management Pact Amount"
    range_start = 0
    range_end = 1
    default = 1


class UnderworldCustomsPactAmount(Range):
    """
    Choose the amount of Underworld Customs pacts in the pool.
    """
    display_name = "Underworld Customs Pact Amount"
    range_start = 0
    range_end = 1
    default = 1


class ForcedOvertimePactAmount(Range):
    """
    Choose the amount of Forced Overtime pacts in the pool.
    """
    display_name = "Forced Overtime Pact Amount"
    range_start = 0
    range_end = 2
    default = 1


class HeightenedSecurityPactAmount(Range):
    """
    Choose the amount of Heightened Security pacts in the pool.
    """
    display_name = "Heightened Security Pact Amount"
    range_start = 0
    range_end = 1
    default = 1


class RoutineInspectionPactAmount(Range):
    """
    Choose the amount of Routine Inspection pacts in the pool.
    """
    display_name = "Routine Inspection Pact Amount"
    range_start = 0
    range_end = 4
    default = 3


class DamageControlPactAmount(Range):
    """
    Choose the amount of Damage Control pacts in the pool.
    """
    display_name = "Damage Control Pact Amount"
    range_start = 0
    range_end = 2
    default = 1


class ApprovalProcessPactAmount(Range):
    """
    Choose the amount of Approval Process pacts in the pool.
    """
    display_name = "Approval Process Pact Amount"
    range_start = 0
    range_end = 2
    default = 1


class TightDeadlinePactAmount(Range):
    """
    Choose the amount of Tight Deadline pacts in the pool.
    """
    display_name = "Tight Deadline Pact Amount"
    range_start = 0
    range_end = 3
    default = 2


class PersonalLiabilityPactAmount(Range):
    """
    Choose the amount of Personal Liability pacts in the pool.
    """
    display_name = "Personal Liability Pact Amount"
    range_start = 0
    range_end = 1
    default = 0


# -----------------------Settings for Filler items ---------------

class DarknessPackValue(Range):
    """
    Choose the value (amount of darkness) of each darkness pack in the pool. 
    If set to 0 Darkness will not appear in the pool.
    """
    display_name = "Darkness Pack Value"
    range_start = 0
    range_end = 10000
    default = 1000


class KeysPackValue(Range):
    """
    Choose the value(amount of Keys) of each Keys pack in the pool.
    If set to 0 Keys will not appear in the pool.
    """
    display_name = "Keys Pack Value"
    range_start = 0
    range_end = 500
    default = 20


class GemstonesPackValue(Range):
    """
    Choose the value(amount of Gemstones) of each Gemstone pack in the pool. 
    If set to 0 Gems will not appear in the pool.
    """
    display_name = "Gemstone Pack Value"
    range_start = 0
    range_end = 2500
    default = 100


class DiamondsPackValue(Range):
    """
    Choose the value(amount of diamonds) of each diamond pack in the pool. 
    If set to 0 Diamonds will not appear in the pool.
    """
    display_name = "Diamonds Pack Value"
    range_start = 0
    range_end = 100
    default = 15


class TitanBloodPackValue(Range):
    """
    Choose the value(amount of Titan blood) of each Titan blood pack in the pool. 
    If set to 0 Titan blood will not appear in the pool.
    """
    display_name = "Titan Blood Pack Value"
    range_start = 0
    range_end = 50
    default = 3


class NectarPackValue(Range):
    """
    Choose the value(amount of Nectar) of each Nectar pack in the pool. 
    If set to 0 Nectar will not appear in the pool.
    """
    display_name = "Nectar Pack Value"
    range_start = 0
    range_end = 50
    default = 3


class AmbrosiaPackValue(Range):
    """
    Choose the value(amount of Ambrosia) of each Ambrosia pack in the pool. 
    If set to 0 Ambrosia will not appear in the pool.
    """
    display_name = "Ambrosia Pack Value"
    range_start = 0
    range_end = 50
    default = 3

# -----------------------Settings for Helpers -------------------------


class FillerHelperPercentage(Range):
    """
    Choose the percentage of filler items in the pool that will be to helpers instead. 
    Helpers give a boost to your max Health or boost the chance of obtaining rare Boons.
    """
    display_name = "Filler Helper Percentage"
    range_start = 0
    range_end = 100
    default = 0


class MaxHealthHelperPercentage(Range):
    """
    Choose the percentage of helper items that will boost your max health.
    """
    display_name = "Max Health Helper Percentage"
    range_start = 0
    range_end = 100
    default = 35


class InitialMoneyHelperPercentage(Range):
    """
    Choose the percentage of helper items that will boost your initial money by 25 each run.
    This gets capped by the percentage being left from the MaxHealthHelpers. 
    What percentage remains from this and the MaxHealthHelpers will give you items that boost the 
    rarity of the boons obtained in runs.
    """
    display_name = "Initial Money Helper Percentage"
    range_start = 0
    range_end = 100
    default = 35

# -----------------------Settings for Trap -------------------------


class FillerTrapPercentage(Range):
    """
    Choose the percentage of filler items in the pool that will be traps instead. 
    Traps diminish your money or health during a run.
    """
    display_name = "Filler Trap Percentage"
    range_start = 0
    range_end = 100
    default = 5

# -----------------------Settings for QoL -------------------------


class ReverseOrderExtremeMeasure(DefaultOnToggle):
    """
    When true the order in which extreme meassures applied is reverse 
    so level 1 is applied to Hades, instead to Meg/The Furies). 
    For a more balanced experience.
    """
    display_name = "Reverse Order Extreme Measure"


class IgnoreGreeceDeaths(DefaultOnToggle):
    """
    If deaths on Greece are ignored for deathlink. Leave off for the memes.
    """
    display_name = "Ignore Greece Deaths"


class StoreGiveHints(DefaultOnToggle):
    """
    If seeing an item on the House Contractor's shop/Fated List of Prophecies 
    should give a hint for it on the multiworld.
    """
    display_name = "Store Give Hints"


class AutomaticRoomsFinishOnHadesDefeat(Toggle):
    """
    If defeating Hades should give all room clears on Room based location mode 
    or all rooms clears with the equipped weapon on Room weapon based location mode. 
    """
    display_name = "Automatic Room Finish On Hades Defeat"
    default = 0


# ------------------------------ Building dictionary ------------------------

@dataclass
class HadesOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    initial_weapon: InitialWeapon
    location_system: LocationSystem
    score_rewards_amount: ScoreRewardsAmount
    keepsakesanity: KeepsakeSanity
    weaponsanity: WeaponSanity
    hidden_aspectsanity: HiddenAspectSanity
    storesanity: StoreSanity
    fatesanity: FateSanity
    hades_defeats_needed: HadesDefeatsNeeded
    weapons_clears_needed: WeaponsClearsNeeded
    keepsakes_needed: KeepsakesNeeded
    fates_needed: FatesNeeded
    heat_system: HeatSystem
    hard_labor_pact_amount: HardLaborPactAmount
    lasting_consequences_pact_amount: LastingConsequencesPactAmount
    convenience_fee_pact_amount: ConvenienceFeePactAmount
    jury_summons_pact_amount: JurySummonsPactAmount
    extreme_measures_pact_amount: ExtremeMeasuresPactAmount
    calisthenics_program_pact_amount: CalisthenicsProgramPactAmount
    benefits_package_pact_amount: BenefitsPackagePactAmount
    middle_management_pact_amount: MiddleManagementPactAmount
    underworld_customs_pact_amount: UnderworldCustomsPactAmount
    forced_overtime_pact_amount: ForcedOvertimePactAmount
    heightened_security_pact_amount: HeightenedSecurityPactAmount
    routine_inspection_pact_amount: RoutineInspectionPactAmount
    damage_control_pact_amount: DamageControlPactAmount
    approval_process_pact_amount: ApprovalProcessPactAmount
    tight_deadline_pact_amount: TightDeadlinePactAmount
    personal_liability_pact_amount: PersonalLiabilityPactAmount
    darkness_pack_value: DarknessPackValue
    keys_pack_value: KeysPackValue
    gemstones_pack_value: GemstonesPackValue
    diamonds_pack_value: DiamondsPackValue
    titan_blood_pack_value: TitanBloodPackValue
    nectar_pack_value: NectarPackValue
    ambrosia_pack_value: AmbrosiaPackValue
    filler_helper_percentage: FillerHelperPercentage
    max_health_helper_percentage: MaxHealthHelperPercentage
    initial_money_helper_percentage: InitialMoneyHelperPercentage
    filler_trap_percentage: FillerTrapPercentage
    reverse_order_em: ReverseOrderExtremeMeasure
    ignore_greece_deaths: IgnoreGreeceDeaths
    store_give_hints: StoreGiveHints
    automatic_rooms_finish_on_hades_defeat: AutomaticRoomsFinishOnHadesDefeat
    death_link: DeathLink

# ------------------------------ Options groups


hades_option_groups = [
    OptionGroup("Game Options", [
        InitialWeapon,
        LocationSystem,
        ScoreRewardsAmount,
        KeepsakeSanity,
        WeaponSanity,
        HiddenAspectSanity,
        StoreSanity,
        FateSanity,
        DeathLink,
    ]),
    OptionGroup("Goal Options", [
        HadesDefeatsNeeded,
        WeaponsClearsNeeded,
        KeepsakesNeeded,
        FatesNeeded,
    ]),
    OptionGroup("Heat Options", [
        HeatSystem,
        HardLaborPactAmount,
        LastingConsequencesPactAmount,
        ConvenienceFeePactAmount,
        JurySummonsPactAmount,
        ExtremeMeasuresPactAmount,
        CalisthenicsProgramPactAmount,
        BenefitsPackagePactAmount,
        MiddleManagementPactAmount,
        UnderworldCustomsPactAmount,
        ForcedOvertimePactAmount,
        HeightenedSecurityPactAmount,
        RoutineInspectionPactAmount,
        DamageControlPactAmount,
        ApprovalProcessPactAmount,
        TightDeadlinePactAmount,
        PersonalLiabilityPactAmount,
    ]),
    OptionGroup("Filler Options", [
        DarknessPackValue,
        KeysPackValue,
        GemstonesPackValue,
        DiamondsPackValue,
        TitanBloodPackValue,
        NectarPackValue,
        AmbrosiaPackValue
    ]),
    OptionGroup("Helpers and Trap Options", [
        FillerHelperPercentage,
        MaxHealthHelperPercentage,
        InitialMoneyHelperPercentage,
        FillerTrapPercentage,
    ]),
    OptionGroup("Quality of Life Options", [
        ReverseOrderExtremeMeasure,
        IgnoreGreeceDeaths,
        StoreGiveHints,
        AutomaticRoomsFinishOnHadesDefeat
    ]),
]


# ------------------------------ Presets

hades_option_presets: Dict[str, Dict[str, Any]] = {
    "Easy": {
        "score_rewards_amount": 100,
        "hidden_aspectsanity": False,
        "fatesanity": False,
        "heat_system": "reverse_heat",
        "hard_labor_pact_amount": 2,
        "lasting_consequences_pact_amount": 1,
        "convenience_fee_pact_amount": 1,
        "jury_summons_pact_amount": 1,
        "extreme_measures_pact_amount": 0,
        "calisthenics_program_pact_amount": 1,
        "benefits_package_pact_amount": 1,
        "middle_management_pact_amount": 1,
        "underworld_customs_pact_amount": 1,
        "forced_overtime_pact_amount": 1,
        "heightened_security_pact_amount": 1,
        "routine_inspection_pact_amount": 1,
        "damage_control_pact_amount": 1,
        "approval_process_pact_amount": 1,
        "tight_deadline_pact_amount": 0,
        "personal_liability_pact_amount": 0,
        "darkness_pack_value": 500,
        "keys_pack_value": 10,
        "gemstones_pack_value": 50,
        "diamonds_pack_value": 3,
        "titan_blood_pack_value": 3,
        "nectar_pack_value": 3,
        "ambrosia_pack_value": 3,
        "filler_helper_percentage": 10,
        "max_health_helper_percentage": 40,
        "initial_money_helper_percentage": 30,
        "filler_trap_percentage": 0,
        "automatic_rooms_finish_on_hades_defeat": True,
    },
    "Normal": {
        "score_rewards_amount": 100,
        "hidden_aspectsanity": True,
        "fatesanity": False,
        "heat_system": "reverse_heat",
        "hard_labor_pact_amount": 3,
        "lasting_consequences_pact_amount": 2,
        "convenience_fee_pact_amount": 1,
        "jury_summons_pact_amount": 2,
        "extreme_measures_pact_amount": 2,
        "calisthenics_program_pact_amount": 1,
        "benefits_package_pact_amount": 1,
        "middle_management_pact_amount": 1,
        "underworld_customs_pact_amount": 1,
        "forced_overtime_pact_amount": 1,
        "heightened_security_pact_amount": 1,
        "routine_inspection_pact_amount": 3,
        "damage_control_pact_amount": 1,
        "approval_process_pact_amount": 1,
        "tight_deadline_pact_amount": 2,
        "personal_liability_pact_amount": 0,
        "darkness_pack_value": 300,
        "keys_pack_value": 5,
        "gemstones_pack_value": 25,
        "diamonds_pack_value": 2,
        "titan_blood_pack_value": 2,
        "nectar_pack_value": 2,
        "ambrosia_pack_value": 2,
        "filler_helper_percentage": 0,
        "filler_trap_percentage": 5,
        "automatic_rooms_finish_on_hades_defeat": True,
    },
    "Hard": {
        "score_rewards_amount": 100,
        "hidden_aspectsanity": True,
        "fatesanity": True,
        "heat_system": "reverse_heat",
        "hard_labor_pact_amount": 5,
        "lasting_consequences_pact_amount": 4,
        "convenience_fee_pact_amount": 2,
        "jury_summons_pact_amount": 3,
        "extreme_measures_pact_amount": 4,
        "calisthenics_program_pact_amount": 2,
        "benefits_package_pact_amount": 2,
        "middle_management_pact_amount": 1,
        "underworld_customs_pact_amount": 1,
        "forced_overtime_pact_amount": 2,
        "heightened_security_pact_amount": 1,
        "routine_inspection_pact_amount": 4,
        "damage_control_pact_amount": 2,
        "approval_process_pact_amount": 2,
        "tight_deadline_pact_amount": 3,
        "personal_liability_pact_amount": 1,
        "darkness_pack_value": 200,
        "keys_pack_value": 3,
        "gemstones_pack_value": 10,
        "diamonds_pack_value": 1,
        "titan_blood_pack_value": 1,
        "nectar_pack_value": 1,
        "ambrosia_pack_value": 1,
        "filler_helper_percentage": 0,
        "filler_trap_percentage": 10,
        "automatic_rooms_finish_on_hades_defeat": False,
    },
}