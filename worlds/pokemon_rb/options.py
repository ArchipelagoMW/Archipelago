
from Options import Toggle, DefaultOnToggle, DeathLink, Choice, Range, Option, OptionDict, SpecialRange, FreeText


class GameVersion(Choice):
    """Select Red or Blue version."""
    display_name = "Game Version"
    option_red = 1
    option_blue = 0
    #default = "random"
    default = 0


class TrainerName(FreeText):
    """Your trainer name. Cannot exceed 7 characters."""
    display_name = "Trainer Name"
    default = "ASH"


class RivalName(FreeText):
    """Your rival's name. Cannot exceed 7 characters."""
    display_name = "Rival's Name"
    default = "GARY"


class Goal(Choice):
    """If Professor Oak is selected, your victory condition will require challenging and defeating Oak after becoming"""
    """Champion and defeating or capturing the Pokemon at the end of Cerulean Cave."""
    display_name = "Goal"
    option_pokemon_league = 0
    option_professor_oak = 1
    default = 0


class VictoryRoadCondition(Range):
    """Number of badges required to reach Victory Road. One fewer will be required to enter the Viridian Gym."""
    display_name = "Badge Goal"
    range_start = 2
    range_end = 8
    default = 8


class CeruleanCaveCondition(Range):
    """Number of badges, HMs, and key items (not counting items you can lose) required to access Cerulean Cave."""
    """If extra_key_items is turned on, the number chosen will be increased by 4."""
    display_name = "Cerulean Cave Condition"
    range_start = 0
    range_end = 25
    default = 20


class BadgeSanity(Toggle):
    """Shuffle gym badges into the general item pool. If turned off, badges will be shuffled across the 8 gyms."""
    display_name = "Badgesanity"
    default = 0


class BadgesNeededForHMMoves(Choice):
    """Off will remove the requirement for badges to use HM moves. Extra will give the Marsh, Volcano, and Earth
    Badges a random HM move to enable. Extra Plus will additionally pick two random badges to enable a second HM move.
    A man in Cerulean City will reveal the moves enabled by each Badge."""
    display_name = "Badges Needed For HM Moves"
    default = 1
    option_on = 1
    alias_true = 1
    option_off = 0
    alias_false = 0
    option_extra = 2
    option_extra_plus = 3


class OldMan(Choice):
    """With Open Viridian City, the Old Man will let you through without needing to turn in Oak's Parcel."""
    """Early Parcel will ensure Oak's Parcel is available at the beginning of your game."""
    display_name = "Old Man"
    option_vanilla = 0
    option_early_parcel = 1
    option_open_viridian_city = 2
    default = 2


class ExtraKeyItems(Toggle):
    """Adds key items that are required to access the Rocket Hideout, Cinnabar Mansion, Safari Zone, and Power Plant.
    Adds four item pickups to Rock Tunnel B1F."""
    display_name = "Extra Key Items"
    default = 1


class ExtraStrengthBoulders(Toggle):
    """Adds Strength Boulders blocking the Route 11 gate, and in Route 13 (can be bypassed with Surf).
    This potentially increases the usefulness of Strength as well as the Bicycle."""
    display_name = "Extra Strength Boulders"
    default = 1


class RequireItemFinder(Toggle):
    """Require Item Finder to pick up hidden items."""
    display_name = "Require Item Finder"
    default = 0


class RandomizeHiddenItems(Choice):
    """Randomize hidden items. If you choose exclude, they will be randomized but will be guaranteed junk items."""
    display_name = "Randomize Hidden Items"
    option_on = 1
    option_off = 0
    alias_true = 1
    alias_false = 0
    option_exclude = 2
    default = 0


class FreeFlyLocation(Toggle):
    """One random fly destination will be unlocked by default."""
    display_name = "Free Fly Location"
    default = 1


class OaksAidRt2(Range):
    """Number of Pokemon registered in the Pokedex required to receive the item from Oak's Aide on Route 2"""
    display_name = "Oak's Aide Route 2"
    range_start = 0
    range_end = 80
    default = 10


class OaksAidRt11(Range):
    """Number of Pokemon registered in the Pokedex required to receive the item from Oak's Aide on Route 11"""
    display_name = "Oak's Aide Route 2"
    range_start = 0
    range_end = 80
    default = 30


class OaksAidRt15(Range):
    """Number of Pokemon registered in the Pokedex required to receive the item from Oak's Aide on Route 15"""
    display_name = "Oak's Aide Route 2"
    range_start = 0
    range_end = 80
    default = 50

class ExpModifier(SpecialRange):
    """Modifier for EXP gained. When specifying a number, exp is multiplied by this amount and divided by 16."""
    display_name = "Exp Modifier"
    range_start = 0
    range_end = 255
    default = 16
    special_range_names = {
        "half": default / 2,
        "normal": default,
        "double": default * 2,
        "triple": default * 3,
        "quadruple": default * 4,
        "quintuple": default * 5,
        "sextuple": default * 6,
        "septuple": default * 7,
        "octuple": default * 8,
    }


class RandomizeWildPokemon(Choice):
    """Randomize all wild Pokemon. match_types will select a Pokemon with at least one type matching
    the original type of the original pokemon. match_base_stats will prefer Pokemon with closer base stat totals.
    match_types_and_base_stats will match types and will weight towards similar base stats, but there may not be many
    to choose from."""
    display_name = "Randomize Wild Pokemon"
    default = 0
    option_vanilla = 0
    option_match_types = 1
    option_match_base_stats = 2
    option_match_types_and_base_stats = 3
    option_completely_random = 4


class RandomizeStaticPokemon(Choice):
    """Randomize all one-time gift and encountered Pokemon, except legendaries.
    These will always be first evolution stage Pokemon."""
    display_name = "Randomize Static Pokemon"
    default = 0
    option_vanilla = 0
    option_match_types = 1
    option_match_base_stats = 2
    option_match_types_and_base_stats = 3
    option_completely_random = 4


class CatchEmAll(Choice):
    """Guarantee all first evolution stage Pokemon are available, or all Pokemon of all stages.
    Currently only has an effect if wild Pokemon are randomized."""
    display_name = "Catch 'Em All"
    default = 0
    option_off = 0
    alias_false = 0
    option_first_stage = 1
    option_all_pokemon = 2


class RandomizeTrainerParties(Choice):
    """Randomize enemy Pokemon encountered in trainer battles."""
    display_name = "Randomize Trainer Parties"
    default = 0
    option_vanilla = 0
    option_match_types = 1
    option_match_base_stats = 2
    option_match_types_and_base_stats = 3
    option_completely_random = 4


class BlindTrainers(Choice):
    """Prevent most trainers from initiating battles, all the time or while holding B."""
    display_name = "Blind Trainers"
    option_on = 2
    option_hold_b = 1
    option_off = 0
    alias_true = 2
    alias_false = 0
    default = 0


class MinimumStepsBetweenEncounters(Range):
    """Minimum number of steps between wild Pokemon encounters."""
    display_name = "Minimum Steps Between Encounters"
    default = 3
    range_start = 0
    range_end = 255


class RandomizePokemonStats(Choice):
    """Randomize base stats for each Pokemon. Shuffle will shuffle the 5 base stat values amongst each other. Randomize
    will completely randomize each stat, but will still add up to the same base stat total."""
    display_name = "Randomize Pokemon Stats"
    default = 0
    option_vanilla = 0
    option_shuffle = 1
    option_randomize = 2


class RandomizePokemonCatchRates(Toggle):
    """Randomize the catch rate for each Pokemon."""
    display_name = "Randomize Catch Rates"
    default = 0


class MinimumCatchRate(Range):
    """Minimum catch rate for each Pokemon. If randomize_catch_rates is on, this will be the minimum value that can be
    chosen. Otherwise, it will raise any Pokemon's catch rate up to this value if its normal catch rate is lower."""
    display_name = "Minimum Catch Rate"
    range_start = 1
    range_end = 255
    default = 3


class RandomizePokemonMovesets(Choice):
    """Randomize the moves learned by Pokemon. prefer_types will prefer moves that match the type of the Pokemon."""
    display_name = "Randomize Pokemon Movesets"
    option_vanilla = 0
    option_prefer_types = 1
    option_completely_random = 2
    default = 0


class StartWithFourMoves(Toggle):
    """If movesets are randomized, this will give all Pokemon 4 starting moves."""
    display_name = "Start With Four Moves"
    default = 0


class TMCompatibility(Choice):
    """Randomize which Pokemon can learn each TM. prefer_types: 90% chance if Pokemon's type matches the move,
    50% chance if move is Normal type and the Pokemon is not, and 25% chance otherwise. Pokemon will retain the same
    TM compatibility when they evolve if the evolved form has the same type(s). Mew will always be able to learn
    every TM."""
    display_name = "TM Compatibility"
    default = 0
    option_vanilla = 0
    option_prefer_types = 1
    option_completely_random = 2
    option_full_compatibility = 3


class HMCompatibility(Choice):
    """Randomize which Pokemon can learn each HM. prefer_types: 100% chance if Pokemon's type matches the move,
    75% chance if move is Normal type and the Pokemon is not, and 25% chance otherwise. Pokemon will retain the same
    HM compatibility when they evolve if the evolved form has the same type(s). Mew will always be able to learn
    every HM."""
    display_name = "HM Compatibility"
    default = 0
    option_vanilla = 0
    option_prefer_types = 1
    option_completely_random = 2
    option_full_compatibility = 3


class RandomizePokemonTypes(Choice):
    """Randomize the types of each Pokemon. Follow Evolutions will ensure Pokemon's types remain the same when evolving
    (except possibly gaining a type)."""
    display_name = "Pokemon Types"
    option_vanilla = 0
    option_follow_evolutions = 1
    option_randomize = 2
    default = 0


class SecondaryTypeChance(SpecialRange):
    """If randomize_pokemon_types is on, this is the chance each Pokemon will have a secondary type. If follow_evolutions
    is selected, it is the chance a second type will be added at each evolution stage. vanilla will give secondary types
    to Pokemon that normally have a secondary type."""
    display_name = "Secondary Type Chance"
    range_start = -1
    range_end = 100
    default = -1
    special_range_names = {
        "vanilla": -1
    }


# class RandomizeTypeChartAttackingTypes(Choice):
#     """The game's type chart consists of 3 columns: attacking type, defending type, and type effectiveness.
#        Matchups that have regular type effectiveness are not in the chart. Shuffle will shuffle the attacking types
#        across the attacking type column (so for example Normal type will still have exactly 2 types that it deals
#        non-regular damage to). Randomize will randomize each type in the column to any random type."""
#     display_name = "Randomize Type Chart Attacking Types"
#     option_vanilla = 0
#     option_shuffle = 1
#     option_randomize = 2
#     default = 0
#
#
# class RandomizeTypeChartDefendingTypes(Choice):
#     """The game's type chart consists of 3 columns: attacking type, defending type, and type effectiveness.
#        Matchups that have regular type effectiveness are not in the chart. Shuffle will shuffle the defending types
#        across the defending type column (so for example Normal type will still have exactly 2 types that it receives
#        non-regular damage from). Randomize will randomize each type in the column to any random type."""
#     display_name = "Randomize Type Chart Attacking Types"
#     option_vanilla = 0
#     option_shuffle = 1
#     option_randomize = 2
#     default = 0

class RandomizeTypeChartTypes(Choice):
    """The game's type chart consists of 3 columns: attacking type, defending type, and type effectiveness.
       Matchups that have regular type effectiveness are not in the chart. Shuffle will shuffle the attacking types
       across the attacking type column and the defending types across the defending type column (so for example Normal
       type will still have exactly 2 types that it receives non-regular damage from, and 2 types it deals non-regular
       damage to). Randomize will randomize each type in both columns to any random type."""
    display_name = "Randomize Type Chart Attacking Types"
    option_vanilla = 0
    option_shuffle = 1
    option_randomize = 2
    default = 0


class RandomizeTypeChartTypeEffectiveness(Choice):
    """The game's type chart consists of 3 columns: attacking type, defending type, and type effectiveness.
       Matchups that have regular type effectiveness are not in the chart. Shuffle will shuffle the type effectiveness
       across the type effectiveness column (so for example there will always be 6 type immunities). Randomize will
       randomize each entry in the table to no effect, not very effective, or super effective; with no effect occurring
       at a low chance. Chaos will randomize the values to anywhere between 0% and 200% damage, in 10% increments."""
    display_name = "Randomize Type Chart Type Effectiveness"
    option_vanilla = 0
    option_shuffle = 1
    option_randomize = 2
    option_chaos = 3
    default = 0


class SafariZoneNormalBattles(Toggle):
    """Change the Safari Zone to have standard wild pokemon battles."""
    display_name = "Safari Zone Normal Battles"
    default = 0


class NormalizeEncounterChances(Toggle):
    """Each wild encounter table has 10 slots for Pokemon. Normally the chance for each being chosen ranges from
    19.9% to 1.2%. Turn this on to normalize them all to 10% each."""
    display_name = "Normalize Encounter Chances"
    default = 0


class ReusableTMs(Toggle):
    """Makes TMs reusable, so they will not be consumed upon use."""
    display_name = "Reusable TMs"
    default = 0

class StartingMoney(Range):
    """The amount of money you start with."""
    display_name = "Starting Money"
    default = 3000
    range_start = 0
    range_end = 999999

pokemon_rb_options = {
    "game_version": GameVersion,
    #"goal": Goal,
    "victory_road_condition": VictoryRoadCondition,
    "cerulean_cave_condition": CeruleanCaveCondition,
    "badgesanity": BadgeSanity,
    "badges_needed_for_hm_moves": BadgesNeededForHMMoves,
    "old_man": OldMan,
    "extra_key_items": ExtraKeyItems,
    "extra_strength_boulders": ExtraStrengthBoulders,
    "require_item_finder": RequireItemFinder,
    "randomize_hidden_items": RandomizeHiddenItems,
    "free_fly_location": FreeFlyLocation,
    "oaks_aide_rt_2": OaksAidRt2,
    "oaks_aide_rt_11": OaksAidRt11,
    "oaks_aide_rt_15": OaksAidRt15,
    "blind_trainers": BlindTrainers,
    "minimum_steps_between_encounters": MinimumStepsBetweenEncounters,
    "exp_modifier": ExpModifier,
    "randomize_wild_pokemon": RandomizeWildPokemon,
    "randomize_static_pokemon": RandomizeStaticPokemon,
    "catch_em_all": CatchEmAll,
    "randomize_pokemon_stats": RandomizePokemonStats,
    "randomize_pokemon_catch_rates": RandomizePokemonCatchRates,
    "minimum_catch_rate": MinimumCatchRate,
    "randomize_trainer_parties": RandomizeTrainerParties,
    "randomize_pokemon_movesets": RandomizePokemonMovesets,
    "start_with_four_moves": StartWithFourMoves,
    "tm_compatibility": TMCompatibility,
    "hm_compatibility": HMCompatibility,
    "randomize_pokemon_types": RandomizePokemonTypes,
    "secondary_type_chance": SecondaryTypeChance,
    "randomize_type_matchup_types": RandomizeTypeChartTypes,
    "randomize_type_matchup_type_effectiveness": RandomizeTypeChartTypeEffectiveness,
    "safari_zone_normal_battles": SafariZoneNormalBattles,
    "normalize_encounter_chances": NormalizeEncounterChances,
    "reusable_tms": ReusableTMs,
    "starting_money": StartingMoney,
}