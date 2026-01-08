import dataclasses
import typing

from dataclasses import dataclass
from Options import Range, Choice, PerGameCommonOptions, Toggle, DeathLink
from .duelists import Duelist
from .utils import Constants


class DuelistProgression(Choice):
    """
    Whenever you receive a "Progressive Duelist" item, the next duelist or group of duelists will be unlocked. This
    setting controls what those duelist groups are.

    "Thematic" places duelists in large groups based on theme. You will start with all of Egypt 1 unlocked, then unlock
    all of World Tournament, then all of Egypt 2, then Final 6 one at a time.

    "Campaign" unlocks duelists roughly the same way as in Campaign mode: you will start with all of Egypt 1 unlocked
    except Seto 1, then unlock Seto 1, then each of the World Tournament duelists one at a time, then Mage Soldier and
    the Jono and Teana refights all together, then 2 random low mage and high mage pairs at the same time, then
    Labryinth Mage, then Seto 2, then the rest of Egypt 2 all at once, then Final 6.

    "Singular" unlocks every duelist one at a time in the same order they're encountered in the campaign up until the
    mages, then unlocks mages one at a time at random without respecting low and high mage pairs.

    Regardless of your choice, you will always have Simon Muran and Duel Master K unlocked, and Heishin 1 is always
    excluded until Heishin 2 is unlocked.
    """
    display_name = "Duelist Progression"
    option_thematic = 0
    option_campaign = 1
    option_singular = 2
    default = 1


always_unlocked_duelists = (Duelist.SIMON_MURAN, Duelist.DUEL_MASTER_K)

# first tuple is the duelists unlocked at the start
duelist_progression_map = {
    DuelistProgression.option_thematic: (
        always_unlocked_duelists +
        (Duelist.TEANA, Duelist.JONO, Duelist.VILLAGER1, Duelist.VILLAGER2, Duelist.VILLAGER3, Duelist.SETO),
        (Duelist.REX_RAPTOR, Duelist.WEEVIL_UNDERWOOD, Duelist.MAI_VALENTINE, Duelist.BANDIT_KEITH,
            Duelist.SHADI, Duelist.YAMI_BAKURA, Duelist.PEGASUS, Duelist.ISIS, Duelist.KAIBA),
        (Duelist.MAGE_SOLDIER, Duelist.JONO_2ND, Duelist.TEANA_2ND, Duelist.OCEAN_MAGE,
            Duelist.HIGH_MAGE_SECMETON, Duelist.FOREST_MAGE, Duelist.HIGH_MAGE_ANUBISIUS, Duelist.MOUNTAIN_MAGE,
            Duelist.HIGH_MAGE_ATENZA, Duelist.DESERT_MAGE, Duelist.HIGH_MAGE_MARTIS, Duelist.MEADOW_MAGE,
            Duelist.HIGH_MAGE_KEPURA, Duelist.LABYRINTH_MAGE, Duelist.SETO_2ND)
    ),
    DuelistProgression.option_campaign: (
        always_unlocked_duelists +
        (Duelist.TEANA, Duelist.JONO, Duelist.VILLAGER1, Duelist.VILLAGER2, Duelist.VILLAGER3),
        (Duelist.SETO,),
        (Duelist.REX_RAPTOR,),
        (Duelist.WEEVIL_UNDERWOOD,),
        (Duelist.MAI_VALENTINE,),
        (Duelist.BANDIT_KEITH,),
        (Duelist.SHADI,),
        (Duelist.YAMI_BAKURA,),
        (Duelist.PEGASUS,),
        (Duelist.ISIS,),
        (Duelist.KAIBA,),
        (Duelist.MAGE_SOLDIER, Duelist.JONO_2ND, Duelist.TEANA_2ND)  # + mages unlocked in random order
    ),
    DuelistProgression.option_singular: (
        always_unlocked_duelists +
        (),
        (Duelist.TEANA,),
        (Duelist.JONO,),
        (Duelist.VILLAGER1,),
        (Duelist.VILLAGER2,),
        (Duelist.VILLAGER3,),
        (Duelist.SETO,),
        (Duelist.REX_RAPTOR,),
        (Duelist.WEEVIL_UNDERWOOD,),
        (Duelist.MAI_VALENTINE,),
        (Duelist.BANDIT_KEITH,),
        (Duelist.SHADI,),
        (Duelist.YAMI_BAKURA,),
        (Duelist.PEGASUS,),
        (Duelist.ISIS,),
        (Duelist.KAIBA,),
        (Duelist.MAGE_SOLDIER,),
        (Duelist.JONO_2ND,),
        (Duelist.TEANA_2ND,)  # + mages unlocked in random order
    )
}


class RandomizeDuelistOrder(Toggle):
    """
    If enabled, the order of the groups of duelists you unlock up until Final 6 will be randomized. Your starting
    group of duelists remains unchanged.

    For "Campaign" and "Singular" progression choices, you are guaranteed to unlock all of the Egypt 1 and
    World Tournament duelists before unlocking any Egypt 2 duelists.
    """
    display_name = "Randomize Duelist Unlock Order"
    default = False


class ItemMode(Choice):
    """
    Selects what type of items to place at checks in addition to the required Progressive Duelist items.

    "Starchips" places a value of starchips behind checks.

    "Cards" splits the pool of accessible checks in half, reserving one half as reward items, and the other half as
    check locations. The reward cards are used to fill the check locations instead of starchips. Using a tracker is
    highly recommended for this setting since there's no other way to determine which cards are randomly selected to be
    the check locations.
    """
    display_name = "Item Mode"
    option_starchips = "Starchips"
    option_cards = "Cards"
    default = option_starchips


class LocalStarchips(Toggle):
    """
    If enabled, 75% of your starchip items will be local to your world.

    Has no effect unless "Starchips" is selected for Item Mode.
    """
    display_name = "Local Starchip Bias"
    default = False


class UnobtainableRewards(Toggle):
    """
    When using the "Cards" Item Mode, normally only cards that would be eligible as checks under your settings can be
    selected as reward items. If this setting is enabled, any card can be selected as a reward, including cards that
    cannot be otherwise obtained by the player like Black Luster Soldier.

    Note that enabling this setting may trivialize the game if cards such as Blue-Eyes Ultimate Dragon or Gate Guardian
    are rolled as item rewards.

    Has no effect unless "Cards" is selected for Item Mode.
    """
    display_name = "Unobtainable Cards As Items"
    default = False


class Final6Progression(Choice):
    """
    "Fixed": The check you receive for defeating a member of Final 6 is guaranteed to unlock the next Final 6 duelist.
    This means you will have Go Mode as soon as the first Final 6 duelist is unlocked.

    "Shuffled": The Progressive Duelist items to unlock each Final 6 duelist are shuffled into the item pool.
    """
    display_name = "Final 6 Progression"
    option_fixed = 0
    option_shuffled = 1
    default = 0


class Final6Sequence(Choice):
    """
    "Vanilla": You will always unlock the Final 6 duelists in this order: Guardian Sebek, Guardian Neku, Heishin 2, Seto
    3, DarkNite, Nitemare.

    "First 5 Shuffled": The order you unlock the Final 6 duelists is randomized, except Nitemare will always be last.

    "All 6 Shuffled": The order you unlock the Final 6 duelists is completely randomized, and you'll reach your goal
    when you defeat the last one. Depending on your other settings, "All 6 Shuffled" could put Nitemare ATecs into logic
    in the lategame.
    """
    display_name = "Final 6 Sequence"
    option_vanilla = 0
    option_first_5_shuffled = 1
    option_all_6_shuffled = 2
    default = 0


class DropRateLogic(Range):
    """
    Prohibits progression items from being placed behind cards with a drop rate at or below the specified value (out of
    2048). This logic takes your duelist progression into account, such that if the duelists you logically have access
    to drop at or below this rate, the card will be excluded until you have access to a duelist with a higher rate if
    one exists, or forever excluded otherwise.
    """
    display_name = "Exclusion Drop Rate"
    range_start = 0
    range_end = 64
    default = 4


class ATecLogic(Choice):
    """
    Sets which duelists' SATec drop pools are considered in logic.

    "Off" means you'll never be expected to do an ATec for progression.

    "Pegasus Only" means only Pegasus's SATec pool is in logic.

    "Hundo ATecs" means that ATecs are in logic for the duelists typically ATec'd during a Hundo run, specifically:
    Pegasus, Kaiba, Mage Soldier, Meadow Mage, and NiteMare.

    "All" means all duelists' SATec pools are in logic.

    Regardless of your choice, you will never be expected to do an ATec until you have access to a duelist who drops a
    trap card of equal strength or stronger than the trap speicified by your "Weakest Trap for ATecs" setting.
    """
    display_name = "ATec Logic"
    option_off = Constants.ATecLogicOptionValues.off
    option_pegasus_only = Constants.ATecLogicOptionValues.pegasus_only
    option_hundo_atecs = Constants.ATecLogicOptionValues.hundo_atecs
    option_all = Constants.ATecLogicOptionValues.all
    default = option_hundo_atecs

    @classmethod
    def get_option_name(cls, value) -> str:
        formatted: str = super().get_option_name(value)
        return formatted.replace("Atec", "ATec")


class ATecTrap(Choice):
    """
    The weakest (i.e. lowest mox Attack Point activation) trap card with which you can be expected to ATec a duelist.
    ATecs will be in logic as soon as you have access to a duelist who drops this card or a stronger trap card,
    excluding their SATec drop pool. Your other ATec settings are still respected.

    Note that Fake Trap puts ATecs in logic right from the start since it drops off of Simon Muran and Simon Muran is
    always unlocked.
    """
    display_name = "Weakest Trap for ATecs"
    option_acid_trap_hole = 2
    option_invisible_wire = 1
    option_fake_trap = 0
    default = option_acid_trap_hole


class ExtraProgressiveDuelists(Range):
    """
    Adds extra Progressive Duelist items into the item pool. Note that this setting can allow all but the final Final 6
    member to be skipped.
    """
    display_name = "Extra Progressive Duelist Items"
    range_start = 0
    range_end = 20
    default = 0


@dataclass
class FMOptions(PerGameCommonOptions):
    duelist_progression: DuelistProgression
    randomize_duelist_order: RandomizeDuelistOrder
    item_mode: ItemMode
    local_starchips: LocalStarchips
    unobtainable_rewards: UnobtainableRewards
    final6_progression: Final6Progression
    final6_sequence: Final6Sequence
    extra_progressive_duelists: ExtraProgressiveDuelists
    atec_logic: ATecLogic
    atec_trap: ATecTrap
    drop_rate_logic: DropRateLogic
    death_link: DeathLink

    def serialize(self) -> typing.Dict[str, int]:
        return {field.name: getattr(self, field.name).value for field in dataclasses.fields(self)}
