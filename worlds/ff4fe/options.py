import typing
from dataclasses import dataclass
from .items import sellable_item_names
from Options import (Toggle, Range, Choice, PerGameCommonOptions, DefaultOnToggle, StartInventoryPool, OptionGroup,
                     OptionSet, Visibility)


class ForgeTheCrystal(Toggle):
    """Bring the Adamant and Legend Sword to clear this objective.
    Forces the objective reward to be the Crystal."""
    display_name = "Forge the Crystal"

class ConquerTheGiant(Toggle):
    """Clear the Giant of Bab-il to clear this objective.
    No character will be available from the Giant with this objective."""
    display_name = "Conquer the Giant"

class DefeatTheFiends(Toggle):
    """Defeat every elemental fiend to clear this objective.
    Your targets are Milon, Milon Z., Kainazzo, Valvalis, Rubicant, and the Elements bosses. Good hunting."""
    display_name = "Defeat The Fiends"

class FindTheDarkMatter(Toggle):
    """Find thirty Dark Matters and deliver them to Kory in Agart to clear this objective.
    There are forty-five Dark Matters in total."""
    display_name = "Find The Dark Matter"

class AdditionalObjectives(Range):
    """The number of additional random objectives. Can be quests, boss fights, or character recruitments. Note that
    no matter what this is set to, no more than thirty-two objectives will be set."""
    display_name = "Additional Objectives"
    range_start = 0
    range_end = 32
    default = 0

class RequiredObjectiveCount(Range):
    """The number of objectives required for victory. Note that this is ignored when no objectives are set. If this
    count is greater than the total number of objectives available, then it will be reduced to match the number of
    available objectives."""
    display_name = "Max Number of Required Objectives"
    range_start = 1
    range_end = 32
    default = 32

class ObjectiveReward(Choice):
    """The reward for clearing all objectives. Note that this is ignored when no objectives are set,
    and Forge the Crystal forces this to the Crystal setting."""
    display_name = "Objective Reward"
    option_crystal = 0
    option_win = 1
    default = 0

class ItemPlacement(Choice):
    """Where items can and will be placed.
    Setting this to Full Shuffle will allow any items to be anywhere.
    Setting this to Major Minor Split will force all non-major locations to never have progression.
    In either case, major locations can only have useful or progression items.
    Major locations are any MIAB or event locations."""
    display_name = "Item Placement"
    option_full_shuffle = 0
    option_major_minor_split = 1
    default = 0

class EnableDefaultPriorityLocations(DefaultOnToggle):
    """If set, major event locations and Monster-In-A-Box locations will be guaranteed to have
    useful or progression items."""
    display_name = "Enable Default Priority Locations"

class NoFreeCharacters(Toggle):
    """If set, characters will not be available at locations with no requirements or bosses. These locations are
    Mysidia, Damcyan Watery Pass, and Mt. Ordeals."""
    display_name = "No Free Characters"

class NoEarnedCharacters(Toggle):
    """If set, characters will not be available at locations with requirements or bosses. These locations are Mist,
    Kaipo, Mt. Hobs, Baron, the Tower of Zot, Cave Eblana, Lunar Palace, and the Giant of Bab-il."""
    display_name = "No Earned Characters"

class HeroChallenge(Choice):
    """Enable the Hero Challenge. In Hero Challenge, your starting character is your main character and cannot be
    dismissed. They will face the top of Mt. Ordeals on their own, and Kokkol will forge a weapon from FFIV Advance
    for them (unless Forge the Crystal is set)."""
    display_name = "Hero Challenge"
    option_none = 0
    option_cecil = 1
    option_kain = 2
    option_rydia = 3
    option_tellah = 4
    option_edward = 5
    option_rosa = 6
    option_yang = 7
    option_palom = 8
    option_porom = 9
    option_cid = 10
    option_edge = 11
    option_fusoya = 12
    option_random_character = 13
    default = 0

class PassEnabled(Toggle):
    """Will the Pass be included in the Key Item Pool?"""
    display_name = "Pass In Key Item Pool"

class UnsafeKeyItemPlacement(Toggle):
    """Normally, underground access is guaranteed to be available without taking a trip to the moon.
    Toggling this on disables this check."""
    display_name = "Unsafe Key Item Placement"

class PassInShops(Toggle):
    """Can the pass show up in shops? This is a convenience feature and will never be required by the logic."""
    display_name = "Enable Pass in Shops"

class AllowedCharacters(OptionSet):
    """Pool of characters allowed to show up. Note that if Hero Challenge is enabled, your hero will still appear."""
    display_name = "Allowed Characters"
    valid_keys = ["Cecil", "Kain", "Rydia", "Tellah", "Edward", "Rosa", "Yang", "Palom", "Porom", "Cid", "Edge", "Fusoya"]
    default = ["Cecil", "Kain", "Rydia", "Tellah", "Edward", "Rosa", "Yang", "Palom", "Porom", "Cid", "Edge", "Fusoya"]

class EnsureAllCharacters(DefaultOnToggle):
    """Ensure at least one instance of each allowed character is available, if possible."""
    display_name = "Ensure All Characters"

class AllowDuplicateCharacters(DefaultOnToggle):
    """Allows multiple instances of the same character to join your party."""
    display_name = "Allow Duplicate Characters"

class RestrictedCharacters(OptionSet):
    """List of characters that can't appear in the easiest to access locations if possible."""
    display_name = "Restricted Characters"
    valid_keys = ["Cecil", "Kain", "Rydia", "Tellah", "Edward", "Rosa", "Yang", "Palom", "Porom", "Cid", "Edge", "Fusoya"]
    default = ["Edge", "Fusoya"]

class PartySize(Range):
    """Maximum party size."""
    display_name = "Party Size"
    range_start = 1
    range_end = 5
    default = 5

class CharactersPermajoin(Toggle):
    """If enabled, characters may not be dismissed from the party."""
    display_name = "Characters Permanently Join"

class CharactersPermadie(Choice):
    """If enabled, characters petrified or dead at the end of battle will be removed from your party forever.
    On Extreme difficulty, this also includes "cutscene" fights (Mist, Dark Elf, etc.)"""
    display_name = "Characters Permanently Die"
    option_no = 0
    option_yes = 1
    option_extreme = 2
    default = 0

class ItemRandomization(Choice):
    """Affects item pool"""
    display_name = "Item Randomization"
    option_standard = 0
    option_wild = 1
    option_pro = 2
    option_wildish = 3
    default = 1

class MinTier(Range):
    """The minimum tier of items that can appear in the item pool."""
    display_name = "Minimum Treasure Tier"
    range_start = 1
    range_end = 4
    default = 1

class MaxTier(Range):
    """The maximum tier of items that can appear in the item pool."""
    display_name = "Maximum Treasure Tier"
    range_start = 5
    range_end = 8
    default = 8

class JunkTier(Range):
    """Items of this tier or below will automatically be sold for cold hard cash."""
    display_name = "Junk Tier"
    range_start = 0
    range_end = 8
    default = 1

class JItems(Choice):
    """Affects whether items not in the US release of FF4 will appear in shops or the item pool.
    Does not affect enemy drops/steals."""
    display_name = "J Items"
    option_allow = 0
    option_no_shops = 1
    option_no_itempool = 2
    option_none = 3

class MIABRandomization(Choice):
    """Affects where MIABs are randomized to and their contents.
    Randomized will randomize the location of MIAB chests, while Vanilla keeps them in their default location.
    Vanilla Exclude acts as vanilla, but progression will never be placed in their locations."""
    display_name = "MIAB Randomization"
    option_randomized = 0
    option_vanilla = 1
    option_vanilla_exclude = 2

class ShopRandomization(Choice):
    """Affects the placement of items in shops. See FE documentation for more for now."""
    display_name = "Shop Randomization"
    option_vanilla = 0
    option_shuffle = 1
    option_standard = 2
    option_pro = 3
    option_wild = 4
    option_cabins = 5
    default = 4

class FreeShops(Toggle):
    """Everything must go!"""
    display_name = "Free Shops"

class NoAdamantArmors(Toggle):
    """Remove Adamant Armor from the item and shop pool."""
    display_name = "No Adamant Armor"

class KeepDoorsBehemoths(Toggle):
    """Should Trap Door and Behemoth Fights be enabled even when encounters are off?"""
    display_name = "Keep TrapDoor and Behemoth Fights"

class NoFreeBosses(Toggle):
    """Removes alternate win conditions for bosses other than good old fashioned violence."""
    display_name = "No Free Bosses"

class WackyChallenge(Choice):
    """Wacky challenges are not fair, balanced, stable, or even necessarily interesting.
    They are, however, quite wacky. See FE documentation for more info, or pick one for a fun surprise!"""
    display_name = "Wacky Challenge"
    option_none = 0
    option_afflicted = 1
    option_battle_scars = 2
    option_the_bodyguard = 3
    option_enemy_unknown = 4
    option_ff4_the_musical = 5
    option_fist_fight = 6
    option_forward_is_the_new_back = 7
    option_friendly_fire = 8
    option_the_floor_is_made_of_lava = 9
    option_gotta_go_fast = 10
    option_holy_onomatopoeia_batman = 11
    option_imaginary_numbers = 12
    option_is_this_even_randomized = 13
    option_kleptomania = 14
    option_men_are_pigs = 15
    option_misspelled = 16
    option_a_much_bigger_magnet = 17
    option_mystery_juice = 18
    option_neat_freak = 19
    option_night_mode = 20
    option_omnidextrous = 21
    option_payable_golbez = 22
    option_save_us_big_chocobo = 23
    option_six_legged_race = 24
    option_the_sky_warriors = 25
    option_something_worth_fighting_for = 26
    option_the_tellah_maneuver = 27
    option_three_point_system = 28
    option_time_is_money = 29
    option_unstackable = 30
    option_world_championship_of_darts = 31
    option_zombies = 32
    option_random_challenge = 33

class StarterKitOne(Choice):
    """FE Starter Kit 1. See FE Documentation for details. Or just pick one, they can't hurt you."""
    display_name = "Starter Kit One"
    option_none = 0
    option_basic = 1
    option_better = 2
    option_loaded = 3
    option_cata = 4
    option_freedom = 5
    option_cid = 6
    option_yang = 7
    option_money = 8
    option_grab_Bag = 9
    option_MIAB = 10
    option_archer = 11
    option_fabul = 12
    option_castlevania = 13
    option_summon = 14
    option_not_Deme = 15
    option_meme = 16
    option_defense = 17
    option_mist = 18
    option_mysidia = 19
    option_baron = 20
    option_dwarf = 21
    option_eblan = 22
    option_libra = 23
    option_99 = 24
    option_green_names = 25
    option_random_kit = 26
    default = 0

class StarterKitTwo(Choice):
    """FE Starter Kit 2. See FE Documentation for details. Or just pick one, they can't hurt you."""
    display_name = "Starter Kit Two"
    option_none = 0
    option_basic = 1
    option_better = 2
    option_loaded = 3
    option_cata = 4
    option_freedom = 5
    option_cid = 6
    option_yang = 7
    option_money = 8
    option_grab_Bag = 9
    option_MIAB = 10
    option_archer = 11
    option_fabul = 12
    option_castlevania = 13
    option_summon = 14
    option_not_Deme = 15
    option_meme = 16
    option_defense = 17
    option_mist = 18
    option_mysidia = 19
    option_baron = 20
    option_dwarf = 21
    option_eblan = 22
    option_libra = 23
    option_99 = 24
    option_green_names = 25
    option_random_kit = 26
    default = 0

class StarterKitThree(Choice):
    """FE Starter Kit 3. See FE Documentation for details. Or just pick one, they can't hurt you."""
    display_name = "Starter Kit Three"
    option_none = 0
    option_basic = 1
    option_better = 2
    option_loaded = 3
    option_cata = 4
    option_freedom = 5
    option_cid = 6
    option_yang = 7
    option_money = 8
    option_grab_bag = 9
    option_MIAB = 10
    option_archer = 11
    option_fabul = 12
    option_castlevania = 13
    option_summon = 14
    option_not_deme = 15
    option_meme = 16
    option_defense = 17
    option_mist = 18
    option_mysidia = 19
    option_baron = 20
    option_dwarf = 21
    option_eblan = 22
    option_libra = 23
    option_99 = 24
    option_green_names = 25
    option_random_kit = 26
    default = 0

class JunkedItems(OptionSet):
    """Items that will always be sold for GP regardless of your junk tier settings."""
    display_name = "Junked Items"
    valid_keys = sorted(sellable_item_names)
    visibility = Visibility.complex_ui | Visibility.template | Visibility.spoiler

class KeptItems(OptionSet):
    """Items that will never be sold for GP regardless of your junk tier settings. Takes priority over Junked Items."""
    display_name = "Kept Items"
    valid_keys = sorted(sellable_item_names)
    visibility = Visibility.complex_ui | Visibility.template | Visibility.spoiler

@dataclass
class FF4FEOptions(PerGameCommonOptions):
    ForgeTheCrystal: ForgeTheCrystal
    ConquerTheGiant: ConquerTheGiant
    DefeatTheFiends: DefeatTheFiends
    FindTheDarkMatter: FindTheDarkMatter
    AdditionalObjectives: AdditionalObjectives
    RequiredObjectiveCount: RequiredObjectiveCount
    ObjectiveReward: ObjectiveReward
    ItemPlacement: ItemPlacement
    EnableDefaultPriorityLocations: EnableDefaultPriorityLocations
    NoFreeCharacters: NoFreeCharacters
    NoEarnedCharacters: NoEarnedCharacters
    HeroChallenge: HeroChallenge
    PassEnabled: PassEnabled
    UnsafeKeyItemPlacement: UnsafeKeyItemPlacement
    PassInShops: PassInShops
    AllowedCharacters: AllowedCharacters
    EnsureAllCharacters: EnsureAllCharacters
    AllowDuplicateCharacters: AllowDuplicateCharacters
    RestrictedCharacters: RestrictedCharacters
    PartySize: PartySize
    CharactersPermajoin: CharactersPermajoin
    CharactersPermadie: CharactersPermadie
    MIABRandomization: MIABRandomization
    ItemRandomization: ItemRandomization
    MinTier: MinTier
    MaxTier: MaxTier
    JunkTier: JunkTier
    JItems: JItems
    ShopRandomization: ShopRandomization
    FreeShops: FreeShops
    NoAdamantArmors: NoAdamantArmors
    KeepDoorsBehemoths: KeepDoorsBehemoths
    NoFreeBosses: NoFreeBosses
    WackyChallenge: WackyChallenge
    StarterKitOne: StarterKitOne
    StarterKitTwo: StarterKitTwo
    StarterKitThree: StarterKitThree
    JunkedItems: JunkedItems
    KeptItems: KeptItems
    start_inventory_from_pool: StartInventoryPool

ff4fe_option_groups = [
    OptionGroup("Objective Options", [
        ForgeTheCrystal,
        ConquerTheGiant,
        DefeatTheFiends,
        FindTheDarkMatter,
        AdditionalObjectives,
        RequiredObjectiveCount,
        ObjectiveReward
    ]),
    OptionGroup("Character Options", [
        NoFreeCharacters,
        NoEarnedCharacters,
        AllowedCharacters,
        EnsureAllCharacters,
        AllowDuplicateCharacters,
        RestrictedCharacters
    ]),
    OptionGroup("Item Options", [
        ItemPlacement,
        ItemRandomization,
        EnableDefaultPriorityLocations,
        PassEnabled,
        PassInShops,
        MinTier,
        MaxTier,
        JunkTier,
        JunkedItems,
        KeptItems,
        JItems
    ]),
    OptionGroup("Challenge Flags", [
        HeroChallenge,
        PartySize,
        CharactersPermajoin,
        CharactersPermadie,
        UnsafeKeyItemPlacement,
        NoAdamantArmors,
        KeepDoorsBehemoths,
        NoFreeBosses,
        WackyChallenge
    ]),
    OptionGroup("Miscellaneous Flags", [
        MIABRandomization,
        ShopRandomization,
        FreeShops,
        StarterKitOne,
        StarterKitTwo,
        StarterKitThree
    ])
]

ff4fe_options_presets: dict[str, dict[str, typing.Any]] = {
    "Remixed": {
        "UnsafeKeyItemPlacement": True,
        "HeroChallenge": "random_character",
        "AdditionalObjectives": 8,
        "RequiredObjectiveCount": 5,
        "ObjectiveReward": "crystal",
        "NoAdamantArmors": True,
        "ItemRandomization": "pro",
        "ShopRandomization": "pro",
        "FreeShops": True,
        "EnsureAllCharacters": False,
        "NoFreeCharacters": True,
        "StarterKitOne": "random_kit"
    },
    "Dark Matter Hunt Plus": {
        "FindTheDarkMatter": True,
        "AdditionalObjectives": 3,
        "RequiredObjectiveCount": 4,
        "ObjectiveReward": "win",
        "StarterKitOne": "random_kit",
        "StarterKitTwo": "random_kit"
    },
    "Objective Mania": {
        "AdditionalObjectives": 32,
        "RequiredObjectiveCount": 32,
        "ObjectiveReward": "win"
    }
}