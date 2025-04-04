from dataclasses import dataclass
from Options import (PerGameCommonOptions, Toggle, Choice, Range, NamedRange, FreeText, TextChoice, DeathLink,
                     ItemsAccessibility)


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


class EliteFourBadgesCondition(Range):
    """Number of badges required to challenge the Elite Four once the Indigo Plateau has been reached.
    Your rival will reveal the amount needed on the first Route 22 battle (after turning in Oak's Parcel)."""
    display_name = "Elite Four Badges Condition"
    range_start = 0
    range_end = 8
    default = 8


class EliteFourKeyItemsCondition(Range):
    """Percentage of available key items (not counting items you can lose) required to challenge the Elite Four. Does
    not count HMs. Evolution stones and Exp. All are key items in Archipelago."""
    display_name = "Elite Four Key Items Condition"
    range_start = 0
    range_end = 100
    default = 0
    total = 0


class EliteFourPokedexCondition(Range):
    """Percentage of logically-reachable Pokemon that must be registered as "owned" in the Pokedex in order to
    challenge the Elite Four."""
    display_name = "Elite Four Pokedex Condition"
    range_start = 0
    range_end = 100
    default = 0
    total = 0


class VictoryRoadCondition(Range):
    """Number of badges required to reach the front entrance of Victory Road."""
    display_name = "Route 23 Condition"
    range_start = 0
    range_end = 8
    default = 7


class Route22GateCondition(Range):
    """Number of badges required to pass through the Route 22 Gate"""
    display_name = "Route 22 Gate Condition"
    range_start = 0
    range_end = 7
    default = 7


class ViridianGymCondition(Range):
    """Number of badges required to enter Viridian Gym."""
    display_name = "Viridian Gym Condition"
    range_start = 0
    range_end = 7
    default = 7


class CeruleanCaveBadgesCondition(Range):
    """Number of badges needed to access the Cerulean Cave entrance in addition to the required Key Items."""
    display_name = "Cerulean Cave Badges Condition"
    range_start = 0
    range_end = 8
    default = 4


class CeruleanCaveKeyItemsCondition(Range):
    """Percentage of available key items (not counting items you can lose) required to access the Cerulean Cave
    entrance in addition to the required badges. Does not count HMs.
    Evolution stones and Exp. All are key items in Archipelago."""
    display_name = "Cerulean Cave Key Items Condition"
    range_start = 0
    range_end = 100
    default = 50
    total = 0


class Route3Condition(Choice):
    """Set a condition to pass through from Pewter City to Route 3."""
    display_name = "Route 3 Condition"
    option_open = 0
    option_defeat_brock = 1
    option_defeat_any_gym = 2
    option_boulder_badge = 3
    option_any_badge = 4
    default = 1


class RobbedHouseOfficer(Toggle):
    """You can disable to remove the requirement to help Bill before you can enter the robbed house in Cerulean City."""
    display_name = "Robbed House Officer"
    default = 1


class SecondFossilCheckCondition(Range):
    """After choosing one of the fossil location items, you can obtain the remaining item from the Cinnabar Lab
    Scientist after reviving this number of fossils."""
    display_name = "Second Fossil Check Condition"
    range_start = 0
    range_end = 3
    default = 3


class FossilCheckItemTypes(Choice):
    """The two fossil checks always contain items for your own game. Here, you can choose what types of items can
    appear. Key Items means only advancement items can appear. Unique means key items or TMs may appear. No Key Items
    means no advancement items may appear."""
    display_name = "Fossil Check Item Types"
    option_any = 0
    option_key_items = 1
    option_unique_items = 2
    option_no_key_items = 3
    default = 0


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


class ExpAll(Choice):
    """Choose how the Exp. All item is handled. It can be removed entirely, shuffled into the item pool, or you can
    start with it."""
    display_name = "Exp. All"
    option_remove = 0
    option_randomize = 1
    option_start_with = 2
    default = 1


class RandomizePokedex(Choice):
    """Randomize the location of the Pokedex, or start with it."""
    display_name = "Randomize Pokedex"
    option_vanilla = 0
    option_randomize = 1
    option_start_with = 2
    default = 0


class KeyItemsOnly(Toggle):
    """Shuffle only Key Items. This overrides Randomize Hidden Items, Trainersanity, and Dexsanity.
    Sets all non-excluded locations in your game to Priority Locations.
    May have high generation failure rates for solo games or small multiworlds, especially with Door Shuffle."""
    display_name = "Key Items Only"
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


class SplitCardKey(Choice):
    """Splits the Card Key item into 10 different Keys, one for each Silph Co floor 2F through 11F.
    Adds location checks to 9 NPCs in Silph Co.
    With Progressive, you will always obtain the keys in order from 2F to 11F."""
    display_name = "Split Card Key"
    option_off = 0
    option_on = 1
    option_progressive = 2
    default = 0


class AllElevatorsLocked(Toggle):
    """Adds requirements to the Celadon Department Store elevator and Silph Co elevators to have the Lift Key.
    No logical implications normally, but may have a significant impact on some Door Shuffle options."""
    display_name = "All Elevators Locked"
    default = 1


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


class PrizeSanity(Toggle):
    """Shuffles the TM prizes at the Celadon Prize Corner into the item pool."""
    display_name = "Prizesanity"
    default = 0


class TrainerSanity(NamedRange):
    """Add location checks to trainers, which can be obtained by talking to a trainer after defeating them. Does not
    affect gym leaders and some scripted event battles. You may specify a number of trainers to have checks, and in
    this case they will be randomly selected. There is no in-game indication as to which trainers have checks."""
    display_name = "Trainersanity"
    default = 0
    range_start = 0
    range_end = 317
    special_range_names = {
        "disabled": 0,
        "full": 317
    }


class RequirePokedex(Toggle):
    """Require the Pokedex to obtain items from Oak's Aides or from Dexsanity checks."""
    display_name = "Require Pokedex"
    default = 1


class AllPokemonSeen(Toggle):
    """Start with all Pokemon "seen" in your Pokedex. This allows you to see where Pokemon can be encountered in the
    wild. Pokemon found by fishing or in the Cerulean Cave are not displayed.
    The Pokedex also shows which HMs can be learned by Pokemon registered as seen."""
    default = 0
    display_name = "All Pokemon Seen"


class DexSanity(NamedRange):
    """Adds location checks for Pokemon flagged "owned" on your Pokedex. You may specify the exact number of Dexsanity
    checks to add, and they will be distributed to Pokemon randomly.
    If Accessibility is set to Full, Dexsanity checks for Pokemon that are not logically reachable will be removed,
    so the number could be lower than you specified.
    If Pokedex is required, the Dexsanity checks for Pokemon you acquired before acquiring the Pokedex can be found by
    talking to Professor Oak or evaluating the Pokedex via Oak's PC."""
    display_name = "Dexsanity"
    default = 0
    range_start = 0
    range_end = 151
    special_range_names = {
        "disabled": 0,
        "full": 151
    }


class FreeFlyLocation(Toggle):
    """One random Fly destination will be unlocked by default."""
    display_name = "Free Fly Location"
    default = 1


class TownMapFlyLocation(Toggle):
    """One random Fly destination will be unlocked when you obtain the Town Map."""
    display_name = "Town Map Fly Location"
    default = 0


class DoorShuffle(Choice):
    """Simple: entrances are randomized together in groups: Pokemarts, Gyms, single exit dungeons, dual exit dungeons,
    single exit misc interiors, dual exit misc interiors are all shuffled separately. Safari Zone is not shuffled.
    On Simple only, the Town Map will be updated to show the new locations for each dungeon.
    Interiors: Any outdoor entrance may lead to any interior, but intra-interior doors are not shuffled. Previously
    named Full.
    Full: Exterior to interior entrances are shuffled, and interior to interior doors are shuffled, separately.
    Insanity: All doors in the game are shuffled.
    Decoupled: Doors may be decoupled from each other, so that leaving through an exit may not return you to the
    door you entered from."""
    display_name = "Door Shuffle"
    option_off = 0
    option_simple = 1
    option_interiors = 2
    option_full = 3
    option_insanity = 4
    option_decoupled = 5
    default = 0


class WarpTileShuffle(Choice):
    """Vanilla: The warp tiles in Silph Co and Sabrina's Gym are not changed.
    Shuffle: The warp tile destinations are shuffled among themselves.
    Mixed: The warp tiles are mixed into the pool of available doors for Full, Insanity, and Decoupled. Same as Shuffle
    for any other door shuffle option."""
    display_name = "Warp Tile Shuffle"
    default = 0
    option_vanilla = 0
    option_shuffle = 1
    option_mixed = 2
    alias_true = 1
    alias_on = 1
    alias_off = 0
    alias_false = 0


class RandomizeRockTunnel(Toggle):
    """Randomize the layout of Rock Tunnel. If Full, Insanity, or Decoupled Door Shuffle is on, this will cause only the
    main entrances to Rock Tunnel to be shuffled."""
    display_name = "Randomize Rock Tunnel"
    default = 0


class DarkRockTunnelLogic(Toggle):
    """Logically require Flash to traverse the Rock Tunnel, so you are never forced to traverse it in the dark."""
    display_name = "Dark Rock Tunnel Logic"
    default = 1


class OaksAidRt2(Range):
    """Number of Pokemon registered in the Pokedex required to receive the item from Oak's Aide on Route 2.
    Vanilla is 10."""
    display_name = "Oak's Aide Route 2"
    range_start = 1
    range_end = 80
    default = 10


class OaksAidRt11(Range):
    """Number of Pokemon registered in the Pokedex required to receive the item from Oak's Aide on Route 11.
    Vanilla is 30."""
    display_name = "Oak's Aide Route 11"
    range_start = 1
    range_end = 80
    default = 20


class OaksAidRt15(Range):
    """Number of Pokemon registered in the Pokedex required to receive the item from Oak's Aide on Route 15.
    Vanilla is 50."""
    display_name = "Oak's Aide Route 15"
    range_start = 1
    range_end = 80
    default = 30


class Stonesanity(Toggle):
    """Removes the four evolution stones from the Celadon Department Store and replaces four of the five Moon Stones
    in the item pool with the four shop stones. If randomize_hidden_items is off, this will cause the two hidden
    Moon Stone locations to be randomized anyway. These are in Pokemon Mansion 1F and Mt Moon B2F."""
    display_name = "Stonesanity"
    default = 0


class LevelScaling(Choice):
    """Off: Encounters use vanilla game levels.
    By Spheres: Levels are scaled by access sphere. Areas reachable in later spheres will have higher levels.
    By Spheres and Distance: Levels are scaled by access spheres as well as distance from Pallet Town, measured by
    number  of internal region connections. This is a much more severe curving of levels and may lead to much less
    variation in levels found in a particular map. However, it may make the higher door shuffle settings significantly
    more bearable, as these options more often result in a smaller number of larger access spheres.
    Auto: Scales by Spheres if Door Shuffle is off or on Simple, otherwise scales by Spheres and Distance"""
    display_name = "Level Scaling"
    option_off = 0
    option_by_spheres = 1
    option_by_spheres_and_distance = 2
    option_auto = 3
    default = 3


class ExpModifier(NamedRange):
    """Modifier for EXP gained. When specifying a number, exp is multiplied by this amount and divided by 16."""
    display_name = "Exp Modifier"
    default = 16
    range_start = default // 4
    range_end = 255
    special_range_names = {
        "half": default // 2,
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


class Area1To1Mapping(Toggle):
    """When randomizing wild Pokemon, for each zone, all instances of a particular Pokemon will be replaced with the
    same Pokemon, resulting in fewer Pokemon in each area."""
    default = 1
    display_name = "Area 1-to-1 Mapping"


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
    battle. If you move into and out of their line of sight without stopping, this chance will only trigger once.
    Trainers which have Trainersanity location checks ignore the Blind Trainers setting."""
    display_name = "Blind Trainers"
    range_start = 0
    range_end = 100
    default = 0


class MinimumStepsBetweenEncounters(Range):
    """Minimum number of steps between wild Pokemon encounters."""
    display_name = "Minimum Steps Between Encounters"
    default = 3
    range_start = 1
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


class MoveBalancing(Toggle):
    """All one-hit-KO moves and fixed-damage moves become normal damaging moves.
    Blizzard, and moves that cause sleep have their accuracy reduced."""
    display_name = "Move Balancing"
    default = 0


class FixCombatBugs(Toggle):
    """Fixes a variety of combat-related bugs. Note that this fixes the Focus Energy bug. The Focus Energy bug causes
    critical strike chances to be doubled when Focus Energy has not been used and halved when it is used.
    Fixing this bug means critical strike chances outside the use of Focus Energy are quartered from the vanilla rate."""
    display_name = "Fix Combat Bugs"
    default = 1


class RandomizePokemonMovesets(Choice):
    """Randomize the moves learned by Pokemon. prefer_types will prefer moves that match the type of the Pokemon."""
    display_name = "Randomize Pokemon Movesets"
    option_vanilla = 0
    option_prefer_types = 1
    option_completely_random = 2
    default = 0


class ConfineTranstormToDitto(Toggle):
    """Regardless of moveset randomization, will keep Ditto's first move as Transform no others will learn it.
    If an enemy Pokemon uses transform before you catch it, it will permanently change to Ditto after capture."""
    display_name = "Confine Transform to Ditto"
    default = 1


class StartWithFourMoves(Toggle):
    """If movesets are randomized, this will give all Pokemon 4 starting moves."""
    display_name = "Start With Four Moves"
    default = 0


class SameTypeAttackBonus(Toggle):
    """Here you can disable Same Type Attack Bonus, so that a move matching a Pokemon's type has no benefit.
    If disabled, all moves will gain 25% extra damage, instead of same type moves gaining 50% extra damage."""
    display_name = "Same Type Attack Bonus"
    default = 1


class RandomizeTMMoves(Toggle):
    """Randomize the moves taught by TMs.
    All TM items will be flagged as 'filler' items regardless of how good the move they teach are."""
    display_name = "Randomize TM Moves"


class TMHMCompatibility(NamedRange):
    range_start = 0
    range_end = 100
    special_range_names = {
        "vanilla": -1,
        "none": 0,
        "full": 100
    }
    default = -1


class TMSameTypeCompatibility(TMHMCompatibility):
    """Chance of each TM being usable on each Pokemon whose type matches the move."""
    display_name = "TM Same-Type Compatibility"


class TMNormalTypeCompatibility(TMHMCompatibility):
    """Chance of each TM being usable on each Pokemon if the move is Normal type and the Pokemon is not."""
    display_name = "TM Normal-Type Compatibility"


class TMOtherTypeCompatibility(TMHMCompatibility):
    """Chance of each TM being usable on each Pokemon if the move a type other than Normal or one of the Pokemon's types."""
    display_name = "TM Other-Type Compatibility"


class HMSameTypeCompatibility(TMHMCompatibility):
    """Chance of each HM being usable on each Pokemon whose type matches the move.
    At least one Pokemon will always be able to learn the moves needed to meet your accessibility requirements."""
    display_name = "HM Same-Type Compatibility"


class HMNormalTypeCompatibility(TMHMCompatibility):
    """Chance of each HM being usable on each Pokemon if the move is Normal type and the Pokemon is not.
    At least one Pokemon will always be able to learn the moves needed to meet your accessibility requirements."""
    display_name = "HM Normal-Type Compatibility"


class HMOtherTypeCompatibility(TMHMCompatibility):
    """Chance of each HM being usable on each Pokemon if the move a type other than Normal or one of the Pokemon's types.
    At least one Pokemon will always be able to learn the moves needed to meet your accessibility requirements."""
    display_name = "HM Other-Type Compatibility"


class InheritTMHMCompatibility(Toggle):
    """If on, evolved Pokemon will inherit their pre-evolved form's TM and HM compatibilities.
    They will then roll the above set chances again at a 50% lower rate for all TMs and HMs their predecessor could not
    learn, unless the evolved form has additional or different types, then moves of those new types will be rolled
    at the full set chance."""
    display_name = "Inherit TM/HM Compatibility"


class RandomizePokemonTypes(Choice):
    """Randomize the types of each Pokemon. Follow Evolutions will ensure Pokemon's types remain the same when evolving
    (except possibly gaining a type)."""
    display_name = "Pokemon Types"
    option_vanilla = 0
    option_follow_evolutions = 1
    option_randomize = 2
    default = 0


class RandomizeMoveTypes(Toggle):
    """Randomize the types of each move."""
    display_name = "Randomize Move Types"
    default = 0


class SecondaryTypeChance(NamedRange):
    """If randomize_pokemon_types is on, this is the chance each Pokemon will have a secondary type. If follow_evolutions
    is selected, it is the chance a second type will be added at each evolution stage. vanilla will give secondary types
    to Pokemon that normally have a secondary type."""
    display_name = "Secondary Type Chance"
    range_start = 0
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


class TypeChartSeed(FreeText):
    """You can enter a number to use as a seed for the type chart. If you enter anything besides a number or "random",
    it will be used as a type chart group name, and everyone using the same group name will get the same type chart,
    made using the type chart options of one random player within the group. If a group name is used, the type matchup
    information will not be made available for trackers."""
    display_name = "Type Chart Seed"
    default = "random"


class NormalMatchups(Range):
    """If 'randomize' is chosen for Randomize Type Chart, this will be the weight for neutral matchups.
    No effect if 'chaos' is chosen"""
    display_name = "Normal Matchups"
    default = 143
    range_start = 0
    range_end = 225


class SuperEffectiveMatchups(Range):
    """If 'randomize' is chosen for Randomize Type Chart, this will be the weight for super effective matchups.
    No effect if 'chaos' is chosen"""
    display_name = "Super Effective Matchups"
    default = 38
    range_start = 0
    range_end = 225


class NotVeryEffectiveMatchups(Range):
    """If 'randomize' is chosen for Randomize Type Chart, this will be the weight for not very effective matchups.
    No effect if 'chaos' is chosen"""
    display_name = "Not Very Effective Matchups"
    default = 38
    range_start = 0
    range_end = 225


class ImmunityMatchups(Range):
    """If 'randomize' is chosen for Randomize Type Chart, this will be the exact number of immunities.
    No effect if 'chaos' is chosen"""
    display_name = "Immunity Matchups"
    default = 6
    range_start = 0
    range_end = 100


class SafariZoneNormalBattles(Toggle):
    """Change the Safari Zone to have standard wild Pokemon battles."""
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
    """Price for Master Balls. Can only be bought if Better Shops is set to Add Master Ball, but this will affect the
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


class SleepTrapWeight(TrapWeight):
    """Weights for Sleep Traps. These apply the Sleep status to all your party members, for randomly between 1 and 7 turns."""
    display_name = "Sleep Trap Weight"


class IceTrapWeight(TrapWeight):
    """Weights for Ice Traps. These apply the Ice status to all your party members. Don't forget to buy Ice Heals!"""
    display_name = "Ice Trap Weight"
    default = 0


class PokeDollSkip(Choice):
    """Patch out the Pokemon Tower Poke Doll skip or have this skip considered in logic."""
    display_name = "Poke Doll Skip"
    option_patched = 0
    option_in_logic = 1
    default = 0


class BicycleGateSkips(Choice):
    """Patch out the Route 16/18 Bicycle Gate skips or have these skips considered in logic."""
    display_name = "Bicycle Gate Skips"
    option_patched = 0
    option_in_logic = 1
    default = 0


class RandomizePokemonPalettes(Choice):
    """Modify Super Gameboy palettes of Pokemon. Primary Type will set Pokemons' palettes based on their primary type,
    Follow Evolutions will randomize palettes but they will remain the same through evolutions (except Eeveelutions),
    Completely Random will randomize all Pokemons' palettes individually"""
    display_name = "Randomize Pokemon Palettes"
    option_vanilla = 0
    option_primary_type = 1
    option_follow_evolutions = 2
    option_completely_random = 3


@dataclass
class PokemonRBOptions(PerGameCommonOptions):
    accessibility: ItemsAccessibility
    game_version: GameVersion
    trainer_name: TrainerName
    rival_name: RivalName
    # goal: Goal
    elite_four_badges_condition: EliteFourBadgesCondition
    elite_four_key_items_condition: EliteFourKeyItemsCondition
    elite_four_pokedex_condition: EliteFourPokedexCondition
    victory_road_condition: VictoryRoadCondition
    route_22_gate_condition: Route22GateCondition
    viridian_gym_condition: ViridianGymCondition
    cerulean_cave_badges_condition: CeruleanCaveBadgesCondition
    cerulean_cave_key_items_condition: CeruleanCaveKeyItemsCondition
    route_3_condition: Route3Condition
    robbed_house_officer: RobbedHouseOfficer
    second_fossil_check_condition: SecondFossilCheckCondition
    fossil_check_item_types: FossilCheckItemTypes
    exp_all: ExpAll
    old_man: OldMan
    badgesanity: BadgeSanity
    badges_needed_for_hm_moves: BadgesNeededForHMMoves
    key_items_only: KeyItemsOnly
    tea: Tea
    extra_key_items: ExtraKeyItems
    split_card_key: SplitCardKey
    all_elevators_locked: AllElevatorsLocked
    extra_strength_boulders: ExtraStrengthBoulders
    require_item_finder: RequireItemFinder
    randomize_hidden_items: RandomizeHiddenItems
    prizesanity: PrizeSanity
    trainersanity: TrainerSanity
    dexsanity: DexSanity
    randomize_pokedex: RandomizePokedex
    require_pokedex: RequirePokedex
    all_pokemon_seen: AllPokemonSeen
    oaks_aide_rt_2: OaksAidRt2
    oaks_aide_rt_11: OaksAidRt11
    oaks_aide_rt_15: OaksAidRt15
    stonesanity: Stonesanity
    door_shuffle: DoorShuffle
    warp_tile_shuffle: WarpTileShuffle
    randomize_rock_tunnel: RandomizeRockTunnel
    dark_rock_tunnel_logic: DarkRockTunnelLogic
    free_fly_location: FreeFlyLocation
    town_map_fly_location: TownMapFlyLocation
    blind_trainers: BlindTrainers
    minimum_steps_between_encounters: MinimumStepsBetweenEncounters
    level_scaling: LevelScaling
    exp_modifier: ExpModifier
    randomize_wild_pokemon: RandomizeWildPokemon
    area_1_to_1_mapping: Area1To1Mapping
    randomize_starter_pokemon: RandomizeStarterPokemon
    randomize_static_pokemon: RandomizeStaticPokemon
    randomize_legendary_pokemon: RandomizeLegendaryPokemon
    catch_em_all: CatchEmAll
    randomize_pokemon_stats: RandomizePokemonStats
    randomize_pokemon_catch_rates: RandomizePokemonCatchRates
    minimum_catch_rate: MinimumCatchRate
    randomize_trainer_parties: RandomizeTrainerParties
    trainer_legendaries: TrainerLegendaries
    move_balancing: MoveBalancing
    fix_combat_bugs: FixCombatBugs
    randomize_pokemon_movesets: RandomizePokemonMovesets
    confine_transform_to_ditto: ConfineTranstormToDitto
    start_with_four_moves: StartWithFourMoves
    same_type_attack_bonus: SameTypeAttackBonus
    randomize_tm_moves: RandomizeTMMoves
    tm_same_type_compatibility: TMSameTypeCompatibility
    tm_normal_type_compatibility: TMNormalTypeCompatibility
    tm_other_type_compatibility: TMOtherTypeCompatibility
    hm_same_type_compatibility: HMSameTypeCompatibility
    hm_normal_type_compatibility: HMNormalTypeCompatibility
    hm_other_type_compatibility: HMOtherTypeCompatibility
    inherit_tm_hm_compatibility: InheritTMHMCompatibility
    randomize_move_types: RandomizeMoveTypes
    randomize_pokemon_types: RandomizePokemonTypes
    secondary_type_chance: SecondaryTypeChance
    randomize_type_chart: RandomizeTypeChart
    normal_matchups: NormalMatchups
    super_effective_matchups: SuperEffectiveMatchups
    not_very_effective_matchups: NotVeryEffectiveMatchups
    immunity_matchups: ImmunityMatchups
    type_chart_seed: TypeChartSeed
    safari_zone_normal_battles: SafariZoneNormalBattles
    normalize_encounter_chances: NormalizeEncounterChances
    reusable_tms: ReusableTMs
    better_shops: BetterShops
    master_ball_price: MasterBallPrice
    starting_money: StartingMoney
    lose_money_on_blackout: LoseMoneyOnBlackout
    poke_doll_skip: PokeDollSkip
    bicycle_gate_skips: BicycleGateSkips
    trap_percentage: TrapPercentage
    poison_trap_weight: PoisonTrapWeight
    fire_trap_weight: FireTrapWeight
    paralyze_trap_weight: ParalyzeTrapWeight
    sleep_trap_weight: SleepTrapWeight
    ice_trap_weight: IceTrapWeight
    randomize_pokemon_palettes: RandomizePokemonPalettes
    death_link: DeathLink
