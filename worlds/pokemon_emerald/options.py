"""
Option definitions for Pokemon Emerald
"""
from dataclasses import dataclass

from Options import (Choice, DeathLink, DefaultOnToggle, OptionSet, NamedRange, Range, Toggle, FreeText,
                     PerGameCommonOptions)

from .data import data


class Goal(Choice):
    """
    Determines what your goal is to consider the game beaten.

    - Champion: Become the champion and enter the hall of fame
    - Steven: Defeat Steven in Meteor Falls
    - Norman: Defeat Norman in Petalburg Gym
    - Legendary Hunt: Defeat or catch legendary pokemon (or whatever was randomized into their encounters)
    """
    display_name = "Goal"
    default = 0
    option_champion = 0
    option_steven = 1
    option_norman = 2
    option_legendary_hunt = 3


class RandomizeBadges(Choice):
    """
    Adds Badges to the pool.

    - Vanilla: Gym leaders give their own badge
    - Shuffle: Gym leaders give a random badge
    - Completely Random: Badges can be found anywhere
    """
    display_name = "Randomize Badges"
    default = 2
    option_vanilla = 0
    option_shuffle = 1
    option_completely_random = 2


class RandomizeHms(Choice):
    """
    Adds HMs to the pool.

    - Vanilla: HMs are at their vanilla locations
    - Shuffle: HMs are shuffled among vanilla HM locations
    - Completely Random: HMs can be found anywhere
    """
    display_name = "Randomize HMs"
    default = 2
    option_vanilla = 0
    option_shuffle = 1
    option_completely_random = 2


class RandomizeKeyItems(DefaultOnToggle):
    """
    Adds most key items to the pool.

    These are usually required to unlock a location or region (e.g. Devon Scope, Letter, Basement Key).
    """
    display_name = "Randomize Key Items"


class RandomizeBikes(Toggle):
    """
    Adds the Mach Bike and Acro Bike to the pool.
    """
    display_name = "Randomize Bikes"


class RandomizeEventTickets(Toggle):
    """
    Adds the event tickets to the pool, which let you access legendaries by sailing from Lilycove.
    """
    display_name = "Randomize Event Tickets"


class RandomizeRods(Toggle):
    """
    Adds fishing rods to the pool.
    """
    display_name = "Randomize Fishing Rods"


class RandomizeOverworldItems(DefaultOnToggle):
    """
    Adds items on the ground with a Pokeball sprite to the pool.
    """
    display_name = "Randomize Overworld Items"


class RandomizeHiddenItems(Toggle):
    """
    Adds hidden items to the pool.
    """
    display_name = "Randomize Hidden Items"


class RandomizeNpcGifts(Toggle):
    """
    Adds most gifts received from NPCs to the pool (not including key items or HMs).
    """
    display_name = "Randomize NPC Gifts"


class RandomizeBerryTrees(Toggle):
    """
    Adds berry trees to the pool. Empty soil patches are converted to locations and contribute Sitrus Berries to the pool.
    """
    display_name = "Randomize Berry Trees"


class Dexsanity(Toggle):
    """
    Adding a "caught" pokedex entry gives you an item (catching, evolving, trading, etc.). Only wild encounters are considered logical access to a species.

    Blacklisting wild encounters removes the dexsanity location.

    Defeating gym leaders provides dex info, allowing you to see where on the map you can catch species you need.

    Each pokedex entry adds a Poke Ball, Great Ball, or Ultra Ball to the pool.

    Warning: This adds a lot of locations and will slow you down significantly.
    """
    display_name = "Dexsanity"


class Trainersanity(Toggle):
    """
    Defeating a trainer gives you an item.

    Trainers are no longer missable. Trainers no longer give you money for winning. Each trainer adds a valuable item (Nugget, Stardust, etc.) to the pool.

    Warning: This adds a lot of locations and will slow you down significantly.
    """
    display_name = "Trainersanity"


class ItemPoolType(Choice):
    """
    Determines which non-progression items get put into the item pool.

    - Shuffled: Item pool consists of shuffled vanilla items
    - Diverse Balanced: Item pool consists of random items approximately proportioned according to what they're replacing
    - Diverse: Item pool consists of uniformly random (non-unique) items
    """
    display_name = "Item Pool Type"
    default = 0
    option_shuffled = 0
    option_diverse_balanced = 1
    option_diverse = 2


class HiddenItemsRequireItemfinder(DefaultOnToggle):
    """
    The Itemfinder is logically required to pick up hidden items.
    """
    display_name = "Require Itemfinder"


class DarkCavesRequireFlash(Choice):
    """
    Determines whether HM05 Flash is logically required to navigate a dark cave.
    """
    display_name = "Require Flash"
    default = 3
    option_neither = 0
    option_only_granite_cave = 1
    option_only_victory_road = 2
    option_both = 3


class EliteFourRequirement(Choice):
    """
    Sets the requirements to challenge the elite four.

    - Badges: Obtain some number of badges
    - Gyms: Defeat some number of gyms
    """
    display_name = "Elite Four Requirement"
    default = 0
    option_badges = 0
    option_gyms = 1


class EliteFourCount(Range):
    """
    Sets the number of badges/gyms required to challenge the elite four.
    """
    display_name = "Elite Four Count"
    range_start = 0
    range_end = 8
    default = 8


class NormanRequirement(Choice):
    """
    Sets the requirements to challenge the Petalburg Gym.

    - Badges: Obtain some number of badges
    - Gyms: Defeat some number of gym leaders
    """
    display_name = "Norman Requirement"
    default = 0
    option_badges = 0
    option_gyms = 1


class NormanCount(Range):
    """
    Sets the number of badges/gyms required to challenge the Petalburg Gym.
    """
    display_name = "Norman Count"
    range_start = 0
    range_end = 7
    default = 4


class LegendaryHuntCatch(Toggle):
    """
    Sets whether legendaries need to be caught to satisfy the Legendary Hunt win condition.

    Defeated legendaries can be respawned by defeating the Elite 4.
    """
    display_name = "Legendary Hunt Requires Catching"


class LegendaryHuntCount(Range):
    """
    Sets the number of legendaries that must be caught/defeated for the Legendary Hunt goal.
    """
    display_name = "Legendary Hunt Count"
    range_start = 1
    range_end = 12
    default = 3


class AllowedLegendaryHuntEncounters(OptionSet):
    """
    Sets which legendary encounters can contribute to the Legendary Hunt goal.

    Latias will always be at Southern Island. Latios will always be the roamer. The TV broadcast describing the roamer gives you "seen" info for Latios.

    The braille puzzle in Sealed Chamber gives you "seen" info for Wailord and Relicanth. The move tutor in Fortree City always teaches Dig.
    """
    display_name = "Allowed Legendary Hunt Encounters"
    valid_keys = [
        "Groudon",
        "Kyogre",
        "Rayquaza",
        "Latios",
        "Latias",
        "Regirock",
        "Registeel",
        "Regice",
        "Ho-Oh",
        "Lugia",
        "Deoxys",
        "Mew",
    ]
    default = valid_keys.copy()


class RandomizeWildPokemon(Choice):
    """
    Randomizes wild pokemon encounters (grass, caves, water, fishing).

    Warning: Matching both base stats and type may severely limit the variety for certain pokemon.

    - Vanilla: Wild encounters are unchanged
    - Match Base Stats: Wild pokemon are replaced with species with approximately the same bst
    - Match Type: Wild pokemon are replaced with species that share a type with the original
    - Match Base Stats and Type: Apply both Match Base Stats and Match Type
    - Completely Random: There are no restrictions
    """
    display_name = "Randomize Wild Pokemon"
    default = 0
    option_vanilla = 0
    option_match_base_stats = 1
    option_match_type = 2
    option_match_base_stats_and_type = 3
    option_completely_random = 4


class WildEncounterBlacklist(OptionSet):
    """
    Prevents listed species from appearing in the wild when wild encounters are randomized.

    May be overridden if enforcing other restrictions in combination with this blacklist is impossible.

    Use "_Legendaries" as a shortcut for all legendary pokemon.
    """
    display_name = "Wild Encounter Blacklist"
    valid_keys = ["_Legendaries"] + sorted([species.label for species in data.species.values()])


class RandomizeStarters(Choice):
    """
    Randomizes the starter pokemon in Professor Birch's bag.

    - Vanilla: Starters are unchanged
    - Match Base Stats: Starters are replaced with species with approximately the same bst
    - Match Type: Starters are replaced with species that share a type with the original
    - Match Base Stats and Type: Apply both Match Base Stats and Match Type
    - Completely Random: There are no restrictions
    """
    display_name = "Randomize Starters"
    default = 0
    option_vanilla = 0
    option_match_base_stats = 1
    option_match_type = 2
    option_match_base_stats_and_type = 3
    option_completely_random = 4


class StarterBlacklist(OptionSet):
    """
    Prevents listed species from appearing as starters when starters are randomized.

    May be overridden if enforcing other restrictions in combination with this blacklist is impossible.

    Use "_Legendaries" as a shortcut for all legendary pokemon.
    """
    display_name = "Starter Blacklist"
    valid_keys = ["_Legendaries"] + sorted([species.label for species in data.species.values()])


class RandomizeTrainerParties(Choice):
    """
    Randomizes the parties of all trainers.

    Warning: Matching both base stats and type may severely limit the variety for certain pokemon.

    - Vanilla: Parties are unchanged
    - Match Base Stats: Trainer pokemon are replaced with species with approximately the same bst
    - Match Type: Trainer pokemon are replaced with species that share a type with the original
    - Match Base Stats and Type: Apply both Match Base Stats and Match Type
    - Completely Random: There are no restrictions
    """
    display_name = "Randomize Trainer Parties"
    default = 0
    option_vanilla = 0
    option_match_base_stats = 1
    option_match_type = 2
    option_match_base_stats_and_type = 3
    option_completely_random = 4


class TrainerPartyBlacklist(OptionSet):
    """
    Prevents listed species from appearing in opponent trainers' parties if opponent parties are randomized.

    May be overridden if enforcing other restrictions in combination with this blacklist is impossible.

    Use "_Legendaries" as a shortcut for all legendary pokemon.
    """
    display_name = "Trainer Party Blacklist"
    valid_keys = ["_Legendaries"] + sorted([species.label for species in data.species.values()])


class ForceFullyEvolved(Range):
    """
    When an opponent uses a pokemon of the specified level or higher, restricts the species to only fully evolved pokemon.

    Only applies when trainer parties are randomized.

    Warning: Combining a low value with matched base stats may severely limit the variety for certain pokemon.
    """
    display_name = "Force Fully Evolved"
    range_start = 1
    range_end = 100
    default = 100


class RandomizeLegendaryEncounters(Choice):
    """
    Randomizes legendary encounters (Rayquaza, Regice, Latias, etc.). The roamer will always be Latios during legendary hunts.

    - Vanilla: Legendary encounters are unchanged
    - Shuffle: Legendary encounters are shuffled between each other
    - Match Base Stats: Legendary encounters are replaced with species with approximately the same bst
    - Match Type: Legendary encounters are replaced with species that share a type with the original
    - Match Base Stats and Type: Apply both Match Base Stats and Match Type
    - Completely Random: There are no restrictions
    """
    display_name = "Randomize Legendary Encounters"
    default = 0
    option_vanilla = 0
    option_shuffle = 1
    option_match_base_stats = 2
    option_match_type = 3
    option_match_base_stats_and_type = 4
    option_completely_random = 5


class RandomizeMiscPokemon(Choice):
    """
    Randomizes non-legendary static encounters. May grow to include other pokemon like trades or gifts.

    - Vanilla: Species are unchanged
    - Shuffle: Species are shuffled between each other
    - Match Base Stats: Species are replaced with species with approximately the same bst
    - Match Type: Species are replaced with species that share a type with the original
    - Match Base Stats and Type: Apply both Match Base Stats and Match Type
    - Completely Random: There are no restrictions
    """
    display_name = "Randomize Misc Pokemon"
    default = 0
    option_vanilla = 0
    option_shuffle = 1
    option_match_base_stats = 2
    option_match_type = 3
    option_match_base_stats_and_type = 4
    option_completely_random = 5


class RandomizeTypes(Choice):
    """
    Randomizes the type(s) of every pokemon. Each species will have the same number of types.

    - Vanilla: Types are unchanged
    - Shuffle: Types are shuffled globally for all species (e.g. every Water-type pokemon becomes Fire-type)
    - Completely Random: Each species has its type(s) randomized
    - Follow Evolutions: Types are randomized per evolution line instead of per species
    """
    display_name = "Randomize Types"
    default = 0
    option_vanilla = 0
    option_shuffle = 1
    option_completely_random = 2
    option_follow_evolutions = 3


class RandomizeAbilities(Choice):
    """
    Randomizes abilities of every species. Each species will have the same number of abilities.

    - Vanilla: Abilities are unchanged
    - Completely Random: Each species has its abilities randomized
    - Follow Evolutions: Abilities are randomized, but if a pokemon would normally retain its ability when evolving, the random ability will also be retained
    """
    display_name = "Randomize Abilities"
    default = 0
    option_vanilla = 0
    option_completely_random = 1
    option_follow_evolutions = 2


class AbilityBlacklist(OptionSet):
    """
    Prevent species from being given these abilities.

    Has no effect if abilities are not randomized.
    """
    display_name = "Ability Blacklist"
    valid_keys = sorted([ability.label for ability in data.abilities])


class LevelUpMoves(Choice):
    """
    Randomizes the moves a pokemon learns when they reach a level where they would learn a move. Your starter is guaranteed to have a usable damaging move.

    - Vanilla: Learnset is unchanged
    - Randomized: Moves are randomized
    - Start with Four Moves: Moves are randomized and all Pokemon know 4 moves at level 1
    """
    display_name = "Level Up Moves"
    default = 0
    option_vanilla = 0
    option_randomized = 1
    option_start_with_four_moves = 2


class MoveMatchTypeBias(Range):
    """
    Sets the probability that a learned move will be forced match one of the types of a pokemon.

    If a move is not forced to match type, it will roll for Normal type bias.
    """
    display_name = "Move Match Type Bias"
    range_start = 0
    range_end = 100
    default = 0


class MoveNormalTypeBias(Range):
    """
    After it has been decided that a move will not be forced to match types, sets the probability that a learned move will be forced to be the Normal type.

    If a move is not forced to be Normal, it will be completely random.
    """
    display_name = "Move Normal Type Bias"
    range_start = 0
    range_end = 100
    default = 0


class MoveBlacklist(OptionSet):
    """
    Prevents species from learning these moves via learnsets, TMs, and move tutors.

    HM moves are already banned.
    """
    display_name = "Move Blacklist"
    valid_keys = sorted(data.move_labels.keys())


class HmCompatibility(NamedRange):
    """
    Sets the percent chance that a given HM is compatible with a species.

    Some opponents like gym leaders are allowed to use HMs. This option can affect the moves they know.
    """
    display_name = "HM Compatibility"
    default = -1
    range_start = 50
    range_end = 100
    special_range_names = {
        "vanilla": -1,
        "full": 100,
    }


class TmTutorCompatibility(NamedRange):
    """
    Sets the percent chance that a given TM or move tutor is compatible with a species.

    Some opponents like gym leaders are allowed to use TMs. This option can affect the moves they know.
    """
    display_name = "TM/Tutor Compatibility"
    default = -1
    range_start = 0
    range_end = 100
    special_range_names = {
        "vanilla": -1,
        "full": 100,
    }


class TmTutorMoves(Toggle):
    """
    Randomizes the moves taught by TMs and move tutors.

    Some opponents like gym leaders are allowed to use TMs. This option can affect the moves they know.
    """
    display_name = "TM/Tutor Moves"


class ReusableTmsTutors(Toggle):
    """
    Sets TMs to not break after use (they remain sellable). Sets move tutors to infinite use.
    """
    display_name = "Reusable TMs and Tutors"


class MinCatchRate(Range):
    """
    Sets the minimum catch rate a pokemon can have. Any pokemon with a catch rate below this floor will have it raised to this value.

    Legendaries are often in the single digits
    Fully evolved pokemon are often double digits
    Pidgey is 255
    """
    display_name = "Minimum Catch Rate"
    range_start = 3
    range_end = 255
    default = 3


class GuaranteedCatch(Toggle):
    """
    Every throw is guaranteed to catch a wild pokemon.
    """
    display_name = "Guaranteed Catch"


class NormalizeEncounterRates(Toggle):
    """
    Make every slot on an encounter table approximately equally likely.

    This does NOT mean each species is equally likely. In the vanilla game, each species may occupy more than one slot, and slots vary in probability.
    
    Species will still occupy the same slots as vanilla, but the slots will be equally weighted. The minimum encounter rate will be 8% (higher in water).
    """
    display_name = "Normalize Encounter Rates"


class ExpModifier(Range):
    """
    Multiplies gained experience by a percentage.

    100 is default
    50 is half
    200 is double
    etc.
    """
    display_name = "Exp Modifier"
    range_start = 0
    range_end = 1000
    default = 100


class BlindTrainers(Toggle):
    """
    Trainers will not start a battle with you unless you talk to them.
    """
    display_name = "Blind Trainers"


class PurgeSpinners(Toggle):
    """
    Trainers will rotate in predictable patterns on a set interval instead of randomly and don't turn toward you when you run.
    """
    display_name = "Purge Spinners"


class MatchTrainerLevels(Choice):
    """
    When you start a battle with a trainer, your party's levels will be automatically set to match that trainer's highest level pokemon.

    The experience you receive will match your party's average actual level, and will only be awarded when you win the battle.

    This is a pseudo-replacement for a level cap and makes every trainer battle a fair fight while still allowing you to level up.

    - Off: The vanilla experience
    - Additive: The modifier you apply to your team is a flat bonus
    - Multiplicative: The modifier you apply to your team is a percent bonus
    """
    display_name = "Match Trainer Levels"
    default = 0
    option_off = 0
    option_additive = 1
    option_multiplicative = 2


class MatchTrainerLevelsBonus(Range):
    """
    A level bonus (or penalty) to apply to your team when matching an opponent's levels.

    When the match trainer levels option is "additive", this value is added to your team's levels during a battle.
        For example, if this value is 5 (+5 levels), you'll have a level 25 team against a level 20 team, and a level 45 team against a level 40 team.

    When the match trainer levels option is "multiplicative", this is a percent bonus.
        For example, if this value is 5 (+5%), you'll have a level 21 team against a level 20 team, and a level 42 team against a level 40 team.
    """
    display_name = "Match Trainer Levels Modifier"
    range_start = -100
    range_end = 100
    default = 0


class DoubleBattleChance(Range):
    """
    The percent chance that a trainer with more than 1 pokemon will be converted into a double battle.

    If these trainers would normally approach you, they will only do so if you have 2 unfainted pokemon.

    They can be battled by talking to them no matter what.
    """
    display_name = "Double Battle Chance"
    range_start = 0
    range_end = 100
    default = 0


class BetterShops(Toggle):
    """
    Pokemarts sell every item that can be obtained in a pokemart (except mail, which is still unique to the relevant city).
    """
    display_name = "Better Shops"


class RemoveRoadblocks(OptionSet):
    """
    Removes specific NPCs that normally stand in your way until certain events are completed.

    This can open up the world a bit and make your playthrough less linear, but be careful how many you remove; it may make too much of your world accessible upon receiving Surf.
    """
    display_name = "Remove Roadblocks"
    valid_keys = [
        "Route 110 Aqua Grunts",
        "Route 112 Magma Grunts",
        "Route 119 Aqua Grunts",
        "Safari Zone Construction Workers",
        "Lilycove City Wailmer",
        "Aqua Hideout Grunts",
        "Seafloor Cavern Aqua Grunt",
    ]


class ExtraBoulders(Toggle):
    """
    Places strength boulders on Route 115 which block access to Meteor Falls from the beach.

    This aims to take some power away from Surf by restricting how much it allows you to access.
    """
    display_name = "Extra Boulders"


class ExtraBumpySlope(Toggle):
    """
    Adds a bumpy slope to Route 115 which allows access to Meteor Falls if you have the Acro Bike.

    This aims to take some power away from Surf by adding a new way to exit the Rustboro area.
    """
    display_name = "Extra Bumpy Slope"


class ModifyRoute118(Toggle):
    """
    Changes the layout of Route 118 so that it must be crossed with the Acro Bike instead of Surf.

    This aims to take some power away from Surf by restricting how much it allows you to access.
    """
    display_name = "Modify Route 118"


class FreeFlyLocation(Toggle):
    """
    Enables flying to one random location (excluding cities reachable with no items).
    """
    display_name = "Free Fly Location"


class HmRequirements(Choice):
    """
    Sets the requirements to use HMs outside of battle.
    """
    display_name = "HM Requirements"
    default = 0
    option_vanilla = 0
    option_fly_without_badge = 1


class TurboA(Toggle):
    """
    Holding A will advance most text automatically.
    """
    display_name = "Turbo A"


class ReceiveItemMessages(Choice):
    """
    Determines whether you receive an in-game notification when receiving an item. Items can still only be received in the overworld.

    - All: Every item shows a message
    - Progression: Only progression items show a message
    - None: All items are added to your bag silently (badges will still show).
    """
    display_name = "Receive Item Messages"
    default = 0
    option_all = 0
    option_progression = 1
    option_none = 2


class RemoteItems(Toggle):
    """
    Instead of placing your own items directly into the ROM, all items are received from the server, including items you find for yourself.

    This enables co-op of a single slot and recovering more items after a lost save file (if you're so unlucky).

    But it changes pickup behavior slightly and requires connection to the server to receive any items.
    """
    display_name = "Remote Items"


class RandomizeMusic(Toggle):
    """
    Shuffles music played in any situation where it loops. Includes many FRLG tracks.
    """
    display_name = "Randomize Music"


class RandomizeFanfares(Toggle):
    """
    Shuffles fanfares for item pickups, healing at the pokecenter, etc.

    When this option is enabled, pressing B will interrupt most fanfares.
    """
    display_name = "Randomize Fanfares"


class WonderTrading(DefaultOnToggle):
    """
    Allows participation in wonder trading with other players in your current multiworld. Speak with the center receptionist on the second floor of any pokecenter.

    Wonder trading NEVER affects logic.

    Certain aspects of a pokemon species are per-game, not per-pokemon. As a result, some things are not retained during a trade, including type, ability, level up learnset, and so on.

    Receiving a pokemon this way does not mark it as found in your pokedex.

    Trade evolutions do not evolve this way; they retain their modified methods (level ups and item use).
    """
    display_name = "Wonder Trading"


class EasterEgg(FreeText):
    """
    Enter certain phrases and something special might happen.

    All secret phrases are something that could be a trendy phrase in Dewford Town. They are case insensitive.
    """
    display_name = "Easter Egg"
    default = "EMERALD SECRET"


@dataclass
class PokemonEmeraldOptions(PerGameCommonOptions):
    goal: Goal

    badges: RandomizeBadges
    hms: RandomizeHms
    key_items: RandomizeKeyItems
    bikes: RandomizeBikes
    event_tickets: RandomizeEventTickets
    rods: RandomizeRods
    overworld_items: RandomizeOverworldItems
    hidden_items: RandomizeHiddenItems
    npc_gifts: RandomizeNpcGifts
    berry_trees: RandomizeBerryTrees
    dexsanity: Dexsanity
    trainersanity: Trainersanity
    item_pool_type: ItemPoolType

    require_itemfinder: HiddenItemsRequireItemfinder
    require_flash: DarkCavesRequireFlash
    elite_four_requirement: EliteFourRequirement
    elite_four_count: EliteFourCount
    norman_requirement: NormanRequirement
    norman_count: NormanCount
    legendary_hunt_catch: LegendaryHuntCatch
    legendary_hunt_count: LegendaryHuntCount
    allowed_legendary_hunt_encounters: AllowedLegendaryHuntEncounters

    wild_pokemon: RandomizeWildPokemon
    wild_encounter_blacklist: WildEncounterBlacklist
    starters: RandomizeStarters
    starter_blacklist: StarterBlacklist
    trainer_parties: RandomizeTrainerParties
    trainer_party_blacklist: TrainerPartyBlacklist
    force_fully_evolved: ForceFullyEvolved
    legendary_encounters: RandomizeLegendaryEncounters
    misc_pokemon: RandomizeMiscPokemon
    types: RandomizeTypes
    abilities: RandomizeAbilities
    ability_blacklist: AbilityBlacklist

    level_up_moves: LevelUpMoves
    move_match_type_bias: MoveMatchTypeBias
    move_normal_type_bias: MoveNormalTypeBias
    tm_tutor_compatibility: TmTutorCompatibility
    hm_compatibility: HmCompatibility
    tm_tutor_moves: TmTutorMoves
    reusable_tms_tutors: ReusableTmsTutors
    move_blacklist: MoveBlacklist

    min_catch_rate: MinCatchRate
    guaranteed_catch: GuaranteedCatch
    normalize_encounter_rates: NormalizeEncounterRates
    exp_modifier: ExpModifier
    blind_trainers: BlindTrainers
    purge_spinners: PurgeSpinners
    match_trainer_levels: MatchTrainerLevels
    match_trainer_levels_bonus: MatchTrainerLevelsBonus
    double_battle_chance: DoubleBattleChance
    better_shops: BetterShops

    remove_roadblocks: RemoveRoadblocks
    extra_boulders: ExtraBoulders
    extra_bumpy_slope: ExtraBumpySlope
    modify_118: ModifyRoute118
    free_fly_location: FreeFlyLocation
    hm_requirements: HmRequirements

    turbo_a: TurboA
    receive_item_messages: ReceiveItemMessages
    remote_items: RemoteItems

    music: RandomizeMusic
    fanfares: RandomizeFanfares

    death_link: DeathLink

    enable_wonder_trading: WonderTrading
    easter_egg: EasterEgg
