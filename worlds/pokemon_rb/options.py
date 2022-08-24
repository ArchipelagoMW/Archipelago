
from Options import Toggle, DefaultOnToggle, DeathLink, Choice, Range, Option, OptionDict, SpecialRange


class GameVersion(Choice):
    """Select Red or Blue version."""
    display_name = "Game Version"
    option_red = 1
    option_blue = 0
    #default = "random"
    default = 0


class Goal(Choice):
    """If Professor Oak is selected, your victory condition will require challenging and defeating Oak after becoming"""
    """Champion and defeating or capturing the Pokemon at the end of Cerulean Cave."""
    display_name = "Goal"
    option_pokemon_league = 0
    option_professor_oak = 1
    default = 0


class BadgeGoal(Range):
    """Number of badges required to reach Victory Road. One fewer will be required to enter the Viridian Gym."""
    display_name = "Badge Goal"
    range_start = 2
    range_end = 8
    default = 8


class CeruleanCaveGoal(Range):
    """Number of badges, gyms defeeated, and key items (not counting items you can lose) required to access Cerulean Cave."""
    """If extra_key_items is turned off, HMs will count in their place."""
    display_name = "Cerulean Cave Condition"
    range_start = 16
    range_end = 32
    default = 24


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
    """Adds key items that are required to access the Rocket Hideout, Cinnabar Mansion, Safari Zone, and Power Plant."""
    display_name = "Extra Key Items"
    default = 1

class ExtraStrengthBoulders(Toggle):
    """Adds Strength Boulders blocking the Route 11 gate, and in Route 13 (can be bypassed with Surf)."""
    """This potentially increases the usefulness of Strength as well as the Bicycle."""
    display_name = "Extra Strength Boulders"
    default = 1

class RandomizeHiddenItems(Choice):
    """Randomize hidden items. If you choose exclude, they will be randomized but will be guaranteed junk items."""
    """Hidden items require the Item Finder to pick up."""
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


base_exp = 16


class ExpModifier(SpecialRange):
    """Modifier for EXP gained."""
    display_name = "Exp Modifier"
    range_start = 0
    range_end = 255
    default = 16
    special_range_names = {
        "half": base_exp / 2,
        "normal": base_exp,
        "double": base_exp * 2,
        "triple": base_exp * 3,
        "quadruple": base_exp * 4,
        "quintuple": base_exp * 5,
        "sextuple": base_exp * 6,
        "suptuple": base_exp * 7,
        "octuple": base_exp * 8,
    }


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
    """Minimum number of steps between wild Pokmon encounters."""
    display_name = "Minimum Steps Between Encounters"
    default = 3
    range_start = 0
    range_end = 255


class RandomizeTypeChartAttackingTypes(Choice):
    """The game's type chart consists of 3 columns: attacking type, defending type, and type effectiveness.
       Matchups that have regular type effectiveness are not in the chart. Shuffle will shuffle the attacking types
       across the attacking type column (so for example Normal type will still have exactly 2 types that it deals
       non-regular damage to). Randomize will randomize each type in the column to any random type."""
    display_name = "Randomize Type Chart Attacking Types"
    option_vanilla = 0
    option_shuffle = 1
    option_randomize = 2
    default = 0

class RandomizeTypeChartDefendingTypes(Choice):
    """The game's type chart consists of 3 columns: attacking type, defending type, and type effectiveness.
       Matchups that have regular type effectiveness are not in the chart. Shuffle will shuffle the defending types
       across the defending type column (so for example Normal type will still have exactly 2 types that it receives
       non-regular damage from). Randomize will randomize each type in the column to any random type."""
    display_name = "Randomize Type Chart Attacking Types"
    option_vanilla = 0
    option_shuffle = 1
    option_randomize = 2
    default = 0

pokemon_rb_options = {
    "game_version": GameVersion,
    #"goal": Goal,
    "badge_goal": BadgeGoal,
    "cerulean_cave_goal": CeruleanCaveGoal,
    "badgesanity": BadgeSanity,
    "badges_needed_for_hm_moves": BadgesNeededForHMMoves,
    "old_man": OldMan,
    "extra_key_items": ExtraKeyItems,
    "extra_strength_boulders": ExtraStrengthBoulders,
    "randomize_hidden_items": RandomizeHiddenItems,
    "free_fly_location": FreeFlyLocation,
    "blind_trainers": BlindTrainers,
    "minimum_steps_between_encounters": MinimumStepsBetweenEncounters,
    "exp_modifier": ExpModifier,
    "randomize_type_matchup_attacking_types": RandomizeTypeChartAttackingTypes,
    "randomize_type_matchup_defending_types": RandomizeTypeChartDefendingTypes,
}