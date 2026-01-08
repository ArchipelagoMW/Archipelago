from dataclasses import dataclass
from enum import IntEnum
from typing import TypedDict, Dict
from BaseClasses import Item
from .Items import item_table, is_joker, stake_to_number, number_to_stake
from .Locations import max_shop_items, max_consumable_items
from Options import DefaultOnToggle, OptionSet, PerGameCommonOptions, Toggle, Range, Choice, Option, FreeText, Visibility
from .BalatroDecks import deck_id_to_name


class Goal(Choice):
    """Goal for this playthrough
        Beat Decks: Win with the specified amount of Decks 
        Unlock Jokers: Unlock the specified amount of Jokers
        Beat Ante: Beat the specified Ante (can be higher than 8)
        Beat Decks on Stake: Win with the specified amount of Decks on the specified Stake (or harder)
        Win with Jokers on Stake: Win with the specified amount of Jokers on the specified Stake (or harder)
        Unique Wins: Win with the specified amount of unique combinations of Decks and Stakes                  
    """
    display_name = "Goal"
    option_beat_decks = 0
    option_unlock_jokers = 1
    option_beat_ante = 2
    option_beat_decks_on_stake = 3
    option_win_with_jokers_on_stake = 4
    option_beat_unique_decks = 5
    default = option_beat_decks


class BeatAnteToWin(Range):
    """If your goal is 'beat ante,' specify the ante you need to beat.
    If your goal isn't 'beat ante', you can ignore this setting."""
    display_name = "Required ante to beat"
    range_start = 1
    range_end = 38
    default = 12


class DecksToWin(Range):
    """If your goal is 'beat Decks' or 'beat decks on stake', specify the number of wins you need to beat.
    If your goal isn't "beat decks" or "beat decks on stake", you can ignore this setting"""
    display_name = "Required decks to win"
    range_start = 1
    range_end = 15
    default = 4


class UniqueDeckWins(Range):
    """If your goal is 'beat unique decks', specify the number of unique decks you need to beat
    This setting can be ignored if your goal isn't "beat unique decks"""
    display_name = "Required unique deck wins for goal"
    range_start = 1
    range_end = 120
    default = 4


class JokerGoal(Range):
    """Number of jokers you need to collect to win.
    If your goal isn't 'unlock jokers' or 'Win with jokers on stake', this setting can be ignored. """
    display_name = "Required jokers to win"
    range_start = 1
    range_end = 150
    default = 75


class RequiredStakeForGoal(OptionSet):
    """The required stake for your goal.
    If no stake is specified or the stake specified is not in the playable stakes it will default to the highest playable one.
    If your goal isn't 'Win with jokers on stake' or 'beat decks on stake', this setting can be ignored."""
    display_name = "Required Stake for goal"
    default = ['White Stake']
    valid_keys = [key for key, _ in stake_to_number.items()]


class JokerBundles(Toggle):
    """Rather than handling each joker as an individual item, you can group them into bundles for quicker progress 
    and fewer items to manage in the world. When enabled, all 150 jokers will be placed into randomly generated bundles. 
    You can also specify the size of these joker bundles"""
    display_name = "Joker Bundles"
    
class JokerBundleSize(Range):
    """Specify the size of Joker Bundles."""
    display_name = "Joker Bundle Size"
    range_start = 5
    range_end = 30
    default = 10

class TarotBundle(Choice):
    """Instead of making every tarot card an individual item, you have the option to put them all in one bundle, 
    that gets placed in the world.
    There is also the possibility to make custom bundles (not recommended)."""
    display_name = "Tarot Bundle"
    option_individual = 0
    option_one_bundle = 1
    option_custom_bundles = 2

class CustomTarotBundles(OptionSet):
    """Only fuck with this if you really want to. You can define up to 5 custom bundles. You have to 
    include every tarot, otherwise it won't work (there is no proper check for this so PLEASE double or triple check yourself). 
    If you have Number of AP consumable items set to greater than 1 you also
    must include the "Archipelago Tarot". Here is a list of all Tarot cards https://balatrogame.fandom.com/wiki/Tarot_Cards.
    The Syntax of this is the following: ['The Fool;The Magician;The High Priestess;The Empress;The Emperor', ...] where the bundles are separated by the commas.
    Make sure to use the right symbols."""
    display_name = "Custom Tarot Bundles"
    default = ["The Fool;The Magician;The High Priestess;The Empress;The Emperor","The Hierophant;The Lovers","The Chariot;Justice;The Hermit;The Wheel of Fortune;Strength;Death","The Hanged Man;Temperance;The Devil;The Tower;The Star","The Moon;The Sun;Judgement;The World"]
    
class PlanetBundle(Choice):
    """Instead of making every planet card an individual item, you have the option to put them all in one bundle, 
    that gets placed in the world.
    There is also the possibility to make custom bundles (not recommended)."""
    display_name = "Planet Bundle"
    option_individual = 0
    option_one_bundle = 1
    option_custom_bundles = 2
    
class CustomPlanetBundles(OptionSet):
    """Only fuck with this if you really want to. You can define up to 5 custom bundles. You have to 
    include every planet, otherwise it won't work. If you have Number of AP consumable items set to greater than 1 you also
    must include the "Archipelago Belt". Here is a list of all Planet cards https://balatrogame.fandom.com/wiki/Planet_Cards.
    For the Syntax refer to Custom Tarot Bundles, it's the same here."""
    display_name = "Custom Planet Bundles"
    default = []

class SpectralBundle(Choice):
    """Instead of making every spectral card an individual item, you have the option to put them all in one bundle, 
    that gets placed in the world.
    There is also the possibility to make custom bundles (not recommended)."""
    display_name = "Spectral Bundle"
    option_individual = 0
    option_one_bundle = 1
    option_custom_bundles = 2

class CustomSpectralBundles(OptionSet):
    """Only fuck with this if you really want to. You can define up to 5 custom bundles. You have to 
    include every spectral, otherwise it won't work. If you have Number of AP consumable items set to greater than 1 you also
    must include the "Archipelago Spectral". Here is a list of all Planet cards https://balatrogame.fandom.com/wiki/Spectral_Cards.
    For the Syntax refer to Custom Tarot Bundles, it's the same here."""
    display_name = "Custom Spectral Bundles"
    default = []

class RemoveOrDebuffJokers(Toggle):
    """Choose whether locked jokers should be completely removed or appear in a debuffed state. 
    Set this to true to remove them entirely, or set it to false to have them appear debuffed."""


class RemoveOrDebuffConsumables(Toggle):
    """Choose whether locked consumables should be completely removed or appear in a debuffed state. 
    Set this to true to remove them entirely, or set it to false to have them appear debuffed."""


class FillerJokers(OptionSet):
    """Which Jokers are supposed to be filler (every Joker not in this list will be considered a progressive item)
    Be careful with this option if your goal is "Unlock Jokers" 

    Valid Jokers:
        "Abstract Joker"
        "Acrobat"
        "Ancient Joker" 
        "....."

        for a full list go to https://balatrogame.fandom.com/wiki/Category:Jokers

    Example: ['Abstract Joker', 'Acrobat', 'Ancient Joker']
    """
    display_name = "Set jokers as filler"
    default = []
    valid_keys = [key for key, _ in item_table.items(
    ) if is_joker(key)] + ["Canio", "Riff-Raff"]


class IncludeDecksMode(Choice):
    """Choose how the playable decks are determined:
    all: All decks will be playable. 
    choose: Select specific decks to be playable from the options below.
    number: Specify how many randomly selected decks will be playable."""
    display_name = "Playable Decks Mode"
    option_all = 0
    option_choose = 1
    option_number = 2
    default = option_all


class IncludeDecksList(OptionSet):
    """Select which decks will be playable in the game. 
    This option is only considered if Playable Decks is set to choose. """
    display_name = "Include selection of playable decks"
    default = [value for key, value in deck_id_to_name.items()]
    valid_keys = [value for key, value in deck_id_to_name.items()]


class IncludeDecksNumber(Range):
    """Specify how many randomly selected decks will be playable.
    This option is only considered if playable Decks is set to number. """
    display_name = "Include number of playable decks"
    range_start = 1
    range_end = 15
    default = 8


class IncludeStakesMode(Choice):
    """Choose how the playable stakes are determined.
    all: All stakes will be playable. 
    choose: Select specific stakes to be playable from the options below.
    number: Specify how many randomly selected stakes will be playable."""
    display_name = "Playable Stakes Mode"
    option_all = 0
    option_choose = 1
    option_number = 2
    default = option_choose


class IncludeStakeList(OptionSet):
    """Select specific stakes to be playable. 
    Example: ['White Stake','Red Stake','Gold Stake']
    This will make those stakes playable and remove the other ones from the game.
    (Also make sure to capitalize the first letters, it's case sensitive.)
    This option is only considered if playable Stakes is set to choose.
    """
    display_name = "Include Stakes to have important Locations"
    default = ["White Stake", "Red Stake"]
    valid_keys = [key for key, _ in stake_to_number.items()]


class IncludeStakesNumber(Range):
    """Specify how many randomly selected stakes will be playable.
    This option is only considered if playable Stakes is set to number. """
    display_name = "Include number of playable stakes"
    range_start = 1
    range_end = 8
    default = 2


class StakeUnlockMode(Choice):
    """Decide how stakes are handled by the Randomizer.
    unlocked: all stakes are unlocked from the start
    vanilla: stakes are progressively unlocked (by beating the previous stake) and in the same order as in the base game
    linear: stakes are progressively unlocked (by beating the previous stake) but in a random order
    stake_as_item: stakes can be found as items and unlock the stake for every deck
    stake_as_item_per_deck: stakes can be found as items but only unlock it for a specific deck"""
    display_name = "Stake Unlock Mode"
    option_unlocked = 0
    option_vanilla = 1
    option_linear = 2
    option_stake_as_item = 3
    option_stake_as_item_per_deck = 4
    default = option_vanilla


class ShopItems(Range):
    """Number of AP Items that will be buyable as vouchers in the shop at each included Stake.
    So for example if you include 3 Stakes and set this option to 11, then there 
    will be 33 findable Shop Items in your game."""
    display_name = "Number of AP shop Items"
    range_start = 0
    range_end = max_shop_items
    default = 15


class MinimumShopPrice(Range):
    """The minimum price for an AP Item Voucher in the shop"""
    display_name = "Minimum Price of AP Item in shop"
    range_start = 1
    range_end = 50
    default = 1


class MaximumShopPrice(Range):
    """The maximum price for an AP Item in the shop"""
    display_name = "Maximum Price of AP Item in shop"
    range_start = 1
    range_end = 100
    default = 10

class ArchipelagoConsumableItems(Range):
    """Number of items that can be received by redeeming 
    an AP planet, tarot or spectral card"""
    display_name = "Number of AP consumable items"
    range_start = 0
    range_end = max_consumable_items # 300
    default = 100

class DecksUnlockedFromStart(Range):
    """Number of random decks you want to start with."""
    display_name = "Number of starting decks"
    range_start = 0
    range_end = 15
    default = 1


class DeathLink(Toggle):
    """When your run ends, everybody will die. When somebody else dies, your run will end."""
    display_name = "Death Link"
    
    
class ForceYaml(Toggle):
    """Some settings (like death link or remove_or_debuff_jokers etc) can be changed in-game after the fact. 
    If you want to disallow this (for a race for example) set this option to true."""
    display_name = "Force Yaml"


class OpFillerAmount(Range):
    """The amount of permanent filler items (like "+1 Hand Size") that is going to be generated.
    If you set this option to 3 for example it's going to fill the world with 3 "+1 Hand Size", 3 "+1 Joker Slot", etc."""
    display_name = "Permanent filler amount"
    range_start = 0
    range_end = 20
    default = 4


class Traps(Choice):
    """How often traps will appear as filler items
        No traps: No traps will appear
        Low traps: 1 in 15 filler items will be traps
        Medium traps: 1 in 7 filler items will be traps
        High traps: 1 in 2 filler items will be traps
        Mayhem: Every filler item will be a trap
    """
    display_name = "Trap Frequency"
    option_no_traps = 0
    option_low_amount = 1
    option_medium_amount = 2
    option_high_amount = 3
    option_mayhem = 4
    default = option_medium_amount


@dataclass
class BalatroOptions(PerGameCommonOptions):

    # goals
    goal: Goal
    ante_win_goal: BeatAnteToWin
    decks_win_goal: DecksToWin
    unique_deck_win_goal: UniqueDeckWins
    jokers_unlock_goal: JokerGoal
    required_stake_for_goal: RequiredStakeForGoal
    
    # decks
    include_decksMode: IncludeDecksMode
    include_deckChoice: IncludeDecksList
    include_deckNumber: IncludeDecksNumber

    # stakes
    stake_unlock_mode: StakeUnlockMode
    include_stakesMode: IncludeStakesMode
    include_stakesList: IncludeStakeList
    include_stakesNumber: IncludeStakesNumber

    # jokers 
    joker_bundles: JokerBundles
    joker_bundle_size : JokerBundleSize
    remove_or_debuff_jokers: RemoveOrDebuffJokers
    
    # consumables    
    tarot_bundle: TarotBundle
    custom_tarot_bundles : CustomTarotBundles
    planet_bundle: PlanetBundle
    custom_planet_bundles : CustomPlanetBundles
    spectral_bundle: SpectralBundle
    custom_spectral_bundles : CustomSpectralBundles
    remove_or_debuff_consumables: RemoveOrDebuffConsumables

    # items
    decks_unlocked_from_start: DecksUnlockedFromStart
    filler_jokers: FillerJokers
    ap_consumable_items: ArchipelagoConsumableItems
    permanent_filler: OpFillerAmount
    shop_items: ShopItems
    minimum_price: MinimumShopPrice
    maximum_price: MaximumShopPrice
    
    # traps
    trap_amount: Traps

    # deathlink
    deathlink: DeathLink
    
    #misc
    forceyaml: ForceYaml
