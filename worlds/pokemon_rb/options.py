
from Options import Toggle, Choice, Range, SpecialRange, TextChoice, DeathLink


class GameVersion(Choice):
    """Select Red or Blue version."""
    display_name = "Game Version"
    option_red = 1
    option_blue = 0
    default = "random"


class TrainerName(TextChoice):
    """Your trainer name. If not set to choose_in_game, must be a name not exceeding 7 characters, and the prompt to
    name your character in-game will be skipped. See the setup guide on archipelago.gg for a list of allowed characters."""
    display_name = "Trainer Name"
    option_choose_in_game = -1
    default = -1


class RivalName(TextChoice):
    """Your rival's name. If not set to choose_in_game, must be a name not exceeding 7 characters, and the prompt to
    name your rival in-game will be skipped. See the setup guide on archipelago.gg for a list of allowed characters."""
    display_name = "Rival's Name"
    option_choose_in_game = -1
    default = -1


class Goal(Choice):
    """If Professor Oak is selected, your victory condition will require challenging and defeating Oak after becoming
    Champion and defeating or capturing the Pokemon at the end of Cerulean Cave."""
    display_name = "Goal"
    option_pokemon_league = 0
    option_professor_oak = 1
    default = 0


class EliteFourCondition(Range):
    """Number of badges required to challenge the Elite Four once the Indigo Plateau has been reached.
    Your rival will reveal the amount needed on the first Route 22 battle (after turning in Oak's Parcel)."""
    display_name = "Elite Four Condition"
    range_start = 0
    range_end = 8
    default = 8


class VictoryRoadCondition(Range):
    """Number of badges required to reach Victory Road."""
    display_name = "Victory Road Condition"
    range_start = 0
    range_end = 8
    default = 8


class ViridianGymCondition(Range):
    """Number of badges required to enter Viridian Gym."""
    display_name = "Viridian Gym Condition"
    range_start = 0
    range_end = 7
    default = 7


class CeruleanCaveCondition(Range):
    """Number of badges, HMs, and key items (not counting items you can lose) required to access Cerulean Cave.
    If extra_key_items is turned on, the number chosen will be increased by 4."""
    display_name = "Cerulean Cave Condition"
    range_start = 0
    range_end = 25
    default = 20


class SecondFossilCheckCondition(Range):
    """After choosing one of the fossil location items, you can obtain the remaining item from the Cinnabar Lab
    Scientist after reviving this number of fossils."""
    display_name = "Second Fossil Check Condition"
    range_start = 0
    range_end = 3
    default = 3


class BadgeSanity(Toggle):
    """Shuffle gym badges into the general item pool. If turned off, badges will be shuffled across the 8 gyms."""
    display_name = "Badgesanity"
    default = 0


class BadgesNeededForHMMoves(Choice):
    """Off will remove the requirement for badges to use HM moves. Extra will give the Marsh, Volcano, and Earth Badges
    a random HM move to enable. Extra Plus will additionally pick two random badges to enable a second HM move.
    You will only need one of the required badges to use the HM move."""
    display_name = "Badges Needed For HM Moves"
    default = 1
    option_on = 1
    alias_true = 1
    option_off = 0
    alias_false = 0
    option_extra = 2
    option_extra_plus = 3


class OldMan(Choice):
    """With Open Viridian City, the Old Man will let you through without needing to turn in Oak's Parcel.
    Early Parcel will ensure Oak's Parcel is available at the beginning of your game."""
    display_name = "Old Man"
    option_vanilla = 0
    option_early_parcel = 1
    option_open_viridian_city = 2
    default = 1


class RandomizePokedex(Choice):
    """Randomize the location of the Pokedex, or start with it. It is required to receive items from Oak's Aides."""
    display_name = "Randomize Pokedex"
    option_vanilla = 0
    option_randomize = 1
    option_start_with = 2
    default = 0


class Tea(Toggle):
    """Adds a Tea item to the item pool which the Saffron guards require instead of the vending machine drinks.
    Adds a location check to the Celadon Mansion 1F, where Tea is acquired in FireRed and LeafGreen."""
    display_name = "Tea"
    default = 0


class ExtraKeyItems(Toggle):
    """Adds key items that are required to access the Rocket Hideout, Cinnabar Mansion, Safari Zone, and Power Plant.
    Adds four item pickups to Rock Tunnel B1F."""
    display_name = "Extra Key Items"
    default = 0


class ExtraStrengthBoulders(Toggle):
    """Adds Strength Boulders blocking the Route 11 gate, and in Route 13 (can be bypassed with Surf).
    This potentially increases the usefulness of Strength as well as the Bicycle."""
    display_name = "Extra Strength Boulders"
    default = 0


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


class TrainerSanity(Toggle):
    """Add a location check to every trainer in the game, which can be obtained by talking to a trainer after defeating
    them. Does not affect gym leaders and some scripted event battles (including all Rival, Giovanni, and
    Cinnabar Gym battles)."""
    display_name = "Trainersanity"
    default = 0


class FreeFlyLocation(Toggle):
    """One random fly destination will be unlocked by default."""
    display_name = "Free Fly Location"
    default = 1


class OaksAidRt2(Range):
    """Number of Pokemon registered in the Pokedex required to receive the item from Oak's Aide on Route 2.
    Vanilla is 10."""
    display_name = "Oak's Aide Route 2"
    range_start = 0
    range_end = 80
    default = 10


class OaksAidRt11(Range):
    """Number of Pokemon registered in the Pokedex required to receive the item from Oak's Aide on Route 11.
    Vanilla is 30."""
    display_name = "Oak's Aide Route 11"
    range_start = 0
    range_end = 80
    default = 20


class OaksAidRt15(Range):
    """Number of Pokemon registered in the Pokedex required to receive the item from Oak's Aide on Route 15.
    Vanilla is 50."""
    display_name = "Oak's Aide Route 15"
    range_start = 0
    range_end = 80
    default = 30


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
    """Randomize all wild Pokemon and game corner prize Pokemon. match_types will select a Pokemon with at least one
    type matching the original type of the original Pokemon. match_base_stats will prefer Pokemon with closer base stat
    totals. match_types_and_base_stats will match types and will weight towards similar base stats, but there may not be
    many to choose from."""
    display_name = "Randomize Wild Pokemon"
    default = 0
    option_vanilla = 0
    option_match_types = 1
    option_match_base_stats = 2
    option_match_types_and_base_stats = 3
    option_completely_random = 4


class RandomizeStarterPokemon(Choice):
    """Randomize the starter Pokemon choices."""
    display_name = "Randomize Starter Pokemon"
    default = 0
    option_vanilla = 0
    option_match_types = 1
    option_match_base_stats = 2
    option_match_types_and_base_stats = 3
    option_completely_random = 4


class RandomizeStaticPokemon(Choice):
    """Randomize one-time gift and encountered Pokemon. These will always be first evolution stage Pokemon."""
    display_name = "Randomize Static Pokemon"
    default = 0
    option_vanilla = 0
    option_match_types = 1
    option_match_base_stats = 2
    option_match_types_and_base_stats = 3
    option_completely_random = 4


class RandomizeLegendaryPokemon(Choice):
    """Randomize Legendaries. Mew has been added as an encounter at the Vermilion dock truck.
    Shuffle will shuffle the legendaries with each other. Static will shuffle them into other static Pokemon locations.
    'Any' will allow legendaries to appear anywhere based on wild and static randomization options, and their locations
    will be randomized according to static Pokemon randomization options."""
    display_name = "Randomize Legendary Pokemon"
    default = 0
    option_vanilla = 0
    option_shuffle = 1
    option_static = 2
    option_any = 3


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


class TrainerLegendaries(Toggle):
    """Allow legendary Pokemon in randomized trainer parties."""
    display_name = "Trainer Legendaries"
    default = 0


class BlindTrainers(Range):
    """Chance each frame that you are standing on a tile in a trainer's line of sight that they will fail to initiate a
    battle. If you move into and out of their line of sight without stopping, this chance will only trigger once."""
    display_name = "Blind Trainers"
    range_start = 0
    range_end = 100
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


class SameTypeAttackBonus(Toggle):
    """Here you can disable Same Type Attack Bonus, so that a move matching a Pokemon's type has no benefit.
    If disabled, all moves will gain 25% extra damage, instead of same type moves gaining 50% extra damage."""
    display_name = "Same Type Attack Bonus"
    default = 1


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


class RandomizeTypeChart(Choice):
    """Randomize the type chart. If 'randomize' is chosen, the matchup weight options will determine the weights.
    If the numbers chosen across the 4 settings add up to exactly 225, they will be the exact numbers of those matchups.
    Otherwise, the normal super effective, and not very effective matchup settings will be used as weights.
    The immunities option will always be the exact amount of immunity matchups.
    If 'chaos' is chosen, the matchup settings will be ignored and every type matchup will be given a random damage
    modifier anywhere between 0 to 200% damage, in 10% increments."""
    display_name = "Randomize Type Chart"
    option_vanilla = 0
    option_randomize = 1
    option_chaos = 2
    default = 0


class NormalMatchups(Range):
    """If 'randomize' is chosen for randomize_type_chart, this will be the weight for neutral matchups.
    No effect if 'chaos' is chosen"""
    display_name = "Normal Matchups"
    default = 143
    range_start = 0
    range_end = 225


class SuperEffectiveMatchups(Range):
    """If 'randomize' is chosen for randomize_type_chart, this will be the weight for super effective matchups.
    No effect if 'chaos' is chosen"""
    display_name = "Super Effective Matchups"
    default = 38
    range_start = 0
    range_end = 225


class NotVeryEffectiveMatchups(Range):
    """If 'randomize' is chosen for randomize_type_chart, this will be the weight for not very effective matchups.
    No effect if 'chaos' is chosen"""
    display_name = "Not Very Effective Matchups"
    default = 38
    range_start = 0
    range_end = 225


class ImmunityMatchups(Range):
    """If 'randomize' is chosen for randomize_type_chart, this will be the exact number of immunities.
    No effect if 'chaos' is chosen"""
    display_name = "Immunity Matchups"
    default = 6
    range_start = 0
    range_end = 100


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


class BetterShops(Choice):
    """Change every town's Pokemart to contain all normal Pokemart items. Additionally, you can add the Master Ball
    to these shops."""
    display_name = "Better Shops"
    option_off = 0
    option_on = 1
    option_add_master_ball = 2
    default = 0


class MasterBallPrice(Range):
    """Price for Master Balls. Can only be bought if better_shops is set to add_master_ball, but this will affect the
    sell price regardless. Vanilla is 0"""
    display_name = "Master Ball Price"
    range_end = 999999
    default = 5000


class StartingMoney(Range):
    """The amount of money you start with."""
    display_name = "Starting Money"
    default = 3000
    range_start = 0
    range_end = 999999


class LoseMoneyOnBlackout(Toggle):
    """Lose half your money when blacking out, as in vanilla."""
    display_name = "Lose Money on Blackout"
    default = 1


class TrapPercentage(Range):
    """Chance for each filler item to be replaced with trap items. Keep in mind that trainersanity vastly increases the
    number of filler items. The trap weight options will determine which traps can be chosen from and at what likelihood."""
    display_name = "Trap Percentage"
    range_end = 100
    default = 0


class TrapWeight(Choice):
    option_low = 1
    option_medium = 3
    option_high = 5
    option_disabled = 0
    default = 3


class PoisonTrapWeight(TrapWeight):
    """Weights for Poison Traps. These apply the Poison status to all your party members."""
    display_name = "Poison Trap Weight"


class FireTrapWeight(TrapWeight):
    """Weights for Fire Traps. These apply the Burn status to all your party members."""
    display_name = "Fire Trap Weight"


class ParalyzeTrapWeight(TrapWeight):
    """Weights for Paralyze Traps. These apply the Paralyze status to all your party members."""
    display_name = "Paralyze Trap Weight"


class IceTrapWeight(TrapWeight):
    """Weights for Ice Traps. These apply the Ice status to all your party members. Don't forget to buy Ice Heals!"""
    display_name = "Ice Trap Weight"
    default = 0


pokemon_rb_options = {
    "game_version": GameVersion,
    "trainer_name": TrainerName,
    "rival_name": RivalName,
    #"goal": Goal,
    "elite_four_condition": EliteFourCondition,
    "victory_road_condition": VictoryRoadCondition,
    "viridian_gym_condition": ViridianGymCondition,
    "cerulean_cave_condition": CeruleanCaveCondition,
    "second_fossil_check_condition": SecondFossilCheckCondition,
    "badgesanity": BadgeSanity,
    "old_man": OldMan,
    "randomize_pokedex": RandomizePokedex,
    "tea": Tea,
    "extra_key_items": ExtraKeyItems,
    "extra_strength_boulders": ExtraStrengthBoulders,
    "require_item_finder": RequireItemFinder,
    "randomize_hidden_items": RandomizeHiddenItems,
    "trainersanity": TrainerSanity,
    "badges_needed_for_hm_moves": BadgesNeededForHMMoves,
    "free_fly_location": FreeFlyLocation,
    "oaks_aide_rt_2": OaksAidRt2,
    "oaks_aide_rt_11": OaksAidRt11,
    "oaks_aide_rt_15": OaksAidRt15,
    "blind_trainers": BlindTrainers,
    "minimum_steps_between_encounters": MinimumStepsBetweenEncounters,
    "exp_modifier": ExpModifier,
    "randomize_wild_pokemon": RandomizeWildPokemon,
    "randomize_starter_pokemon": RandomizeStarterPokemon,
    "randomize_static_pokemon": RandomizeStaticPokemon,
    "randomize_legendary_pokemon": RandomizeLegendaryPokemon,
    "catch_em_all": CatchEmAll,
    "randomize_pokemon_stats": RandomizePokemonStats,
    "randomize_pokemon_catch_rates": RandomizePokemonCatchRates,
    "minimum_catch_rate": MinimumCatchRate,
    "randomize_trainer_parties": RandomizeTrainerParties,
    "trainer_legendaries": TrainerLegendaries,
    "randomize_pokemon_movesets": RandomizePokemonMovesets,
    "start_with_four_moves": StartWithFourMoves,
    "same_type_attack_bonus": SameTypeAttackBonus,
    "tm_compatibility": TMCompatibility,
    "hm_compatibility": HMCompatibility,
    "randomize_pokemon_types": RandomizePokemonTypes,
    "secondary_type_chance": SecondaryTypeChance,
    "randomize_type_chart": RandomizeTypeChart,
    "normal_matchups": NormalMatchups,
    "super_effective_matchups": SuperEffectiveMatchups,
    "not_very_effective_matchups": NotVeryEffectiveMatchups,
    "immunity_matchups": ImmunityMatchups,
    "safari_zone_normal_battles": SafariZoneNormalBattles,
    "normalize_encounter_chances": NormalizeEncounterChances,
    "reusable_tms": ReusableTMs,
    "better_shops": BetterShops,
    "master_ball_price": MasterBallPrice,
    "starting_money": StartingMoney,
    "lose_money_on_blackout": LoseMoneyOnBlackout,
    "trap_percentage": TrapPercentage,
    "poison_trap_weight": PoisonTrapWeight,
    "fire_trap_weight": FireTrapWeight,
    "paralyze_trap_weight": ParalyzeTrapWeight,
    "ice_trap_weight": IceTrapWeight,
    "death_link": DeathLink
}
