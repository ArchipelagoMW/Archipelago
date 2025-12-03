from enum import IntEnum
from Options import DefaultOnToggle, Toggle, Range, Choice, PerGameCommonOptions, OptionGroup, Visibility as OptionVisibility
from dataclasses import dataclass

class Scenario(IntEnum):
    forest_frontiers = 0
    dynamite_dunes = 1
    leafy_lake = 2
    diamond_heights = 3
    evergreen_gardens = 4
    bumbly_beach = 5
    trinity_islands = 6
    katies_world = 7
    dinky_park = 8
    aqua_park = 9
    millennium_mines = 10
    karts_and_coasters = 11
    mels_world = 12
    mothball_mountain = 13
    pacific_pyramids = 14
    crumbly_woods = 15
    big_pier = 16
    lightning_peaks = 17
    ivory_towers = 18
    rainbow_valley = 19
    thunder_rock = 20
    mega_park = 21
    whispering_cliffs = 22
    three_monkeys_park = 23
    canary_mines = 24
    barony_bridge = 25
    funtopia = 26
    haunted_harbor = 27
    fun_fortress = 28
    future_world = 29
    gentle_glen = 30
    jolly_jungle = 31
    hydro_hills = 32
    sprightly_park = 33
    magic_quarters = 34
    fruit_farm = 35
    butterfly_dam = 36
    coaster_canyon = 37
    thunderstorm_park = 38
    harmonic_hills = 39
    roman_village = 40
    swamp_cove = 41
    adrenaline_heights = 42
    utopia_park = 43
    rotting_heights = 44
    fiasco_forest = 45
    pickle_park = 46
    giggle_downs = 47
    mineral_park = 48
    coaster_crazy = 49
    urban_park = 50
    geoffery_gardens = 51
    iceberg_islands = 52
    volcania = 53
    arid_heights = 54
    razor_rocks = 55
    crater_lake = 56
    vertigo_views = 57
    big_pier_2 = 58
    dragons_cove = 59
    good_knight_park = 60
    wacky_warren = 61
    grand_glacier = 62
    crazy_craters = 63
    dusty_desert = 64
    woodworm_park = 65
    icarus_park = 66
    sunny_swamps = 67
    frightmare_hills = 68
    thunder_rocks = 69
    octagon_park = 70
    pleasure_island = 71
    icicle_worlds = 72
    southern_sands = 73
    tiny_towers = 74
    nevermore_park = 75
    pacifica = 76
    urban_jungle = 77
    terror_town = 78
    megaworld_park = 79
    venus_ponds = 80
    micro_park = 81
    electric_fields = 82
    factory_capers = 83
    crazy_castle = 84
    dusty_greens = 85
    bumbly_bazzar = 86
    infernal_views = 87
    lucky_lake = 88
    botany_breakers = 89
    alpine_adventures = 90
    gravity_gardens = 91
    extreme_heights = 92
    amity_airfield = 93
    ghost_town = 94
    fungus_woods = 95
    rainbow_summit = 96
    over_the_edge = 97
    great_wall_of_china = 98
    canyon_calamities = 99
    sugarloaf_shores = 100
    mines_of_africa = 101
    park_maharaja = 102
    ayers_adventure = 103
    european_extravaganza = 104
    rollercoaster_heaven = 105
    lost_city_founder = 106
    mirage_madness = 107
    icy_adventures = 108
    okinawa_coast = 109
    beach_barbecue_blast = 110
    from_the_ashes = 111
    wacky_waikiki = 112
    rainforest_romp = 113
    sherwood_forest = 114
    crater_carnage = 115
    alcatraz = 116
    woodstock = 117
    cliffside_castle = 118
    extraterrestrial_extravaganza = 119
    animatronic_antics = 120
    coastersaurus = 121
    schneider_shores = 122
    gemini_city = 123
    mythological_madness = 124
    rocky_rambles = 125
    metropolis = 126
    rock_n_roll_revival = 127
    alton_towers = 128
    blackpool_pleasure_beach = 129
    heide_park = 130
    six_flags_belgium = 131
    six_flags_great_adventure = 132
    six_flags_holland = 133
    six_flags_magic_mountain = 134
    six_flags_over_texas = 135
    fort_anachronism = 136
    build_your_own_six_flags_belgium = 137
    build_your_own_six_flags_great_adventure = 138
    build_your_own_six_flags_holland = 139
    build_your_own_six_flags_magic_mountain = 140
    build_your_own_six_flags_park = 141
    build_your_own_six_flags_over_texas = 142
    random_RCT1 = 143
    random_loopy_landscapes = 144
    random_corkscrew_follies = 145
    random_RCT2 = 146
    random_wacky_worlds = 147
    random_time_twister = 148
    random_RCT1_expansions = 149
    random_RCT2_expansions = 150
    archipelago_madness_vanilla = 151
    archipelago_madness_expansions = 152

class DeathLinkMode(IntEnum):
    disabled = 0
    enabled = 1

class Visibility(IntEnum):
    nothing = 0
    progression = 1
    recipient = 2
    progression_recipient = 3
    full = 4

class Awards(IntEnum):
    all_awards = 0
    positive = 1
    none = 2

class Difficulty(IntEnum):
    very_easy = 0
    easy = 1
    medium = 2
    hard = 3
    extreme = 4

class PreferredIntensity(IntEnum):
    less_intense = 0
    normal = 1
    more_intense = 2

class RandomizationRange(IntEnum):
    none = 0
    low = 1
    medium = 2
    high = 3
    extreme = 4

class ScenarioLength(IntEnum):
    synchronous_short = 0
    synchronous_long = 1
    lengthy = 2
    marathon = 3
    
class StatReRolls(IntEnum):
    never = 0
    infrequent = 1
    semi_frequent = 2
    frequent = 3
    very_frequent = 4
    extremely_frequent = 5

class DifficultGuestGeneration(IntEnum):
    off = 0
    unlockable = 1
    on = 2

class DifficultParkRating(IntEnum):
    off = 0
    unlockable = 1
    on = 2

class ForbidHighConstruction(IntEnum):
    off = 0
    unlockable = 1
    on = 2

class ForbidLandscapeChanges(IntEnum):
    off = 0
    unlockable = 1
    on = 2

class ForbidMarketingCampaigns(IntEnum):
    off = 0
    unlockable = 1
    on = 2

class ForbidTreeRemoval(IntEnum):
    off = 0
    unlockable = 1
    on = 2

class OpenRCT2OnToggle(DefaultOnToggle):
    @property
    def result(self) -> bool:
        return self.value


class OpenRCT2Toggle(Toggle):
    @property
    def result(self) -> bool:
        return self.value


class SelectedScenario(Choice):
    """Choose which scenario you'd like to play! Random won't choose scenarios that are unreasonably difficult/tedious.
    Future updates will allow custom scenarios.
    """
    display_name = "Scenario"
    option_random_RCT1 = Scenario.random_RCT1.value
    option_random_loopy_landscapes = Scenario.random_loopy_landscapes.value
    option_random_corkscrew_follies = Scenario.random_corkscrew_follies.value
    option_random_RCT2 = Scenario.random_RCT2.value
    option_random_wacky_worlds = Scenario.random_wacky_worlds.value
    option_random_time_twister = Scenario.random_time_twister.value
    option_random_RCT1_expansions = Scenario.random_RCT1_expansions.value
    option_random_RCT2_expansions = Scenario.random_RCT2_expansions.value
    option_archipelago_madness_vanilla = Scenario.archipelago_madness_vanilla.value
    option_archipelago_madness_expansions = Scenario.archipelago_madness_expansions.value
    option_forest_frontiers = Scenario.forest_frontiers.value
    option_dynamite_dunes = Scenario.dynamite_dunes.value
    option_leafy_lake = Scenario.leafy_lake.value
    option_diamond_heights = Scenario.diamond_heights.value
    option_evergreen_gardens = Scenario.evergreen_gardens.value
    option_bumbly_beach = Scenario.bumbly_beach.value
    option_trinity_islands = Scenario.trinity_islands.value
    option_katies_world = Scenario.katies_world.value
    option_dinky_park = Scenario.dinky_park.value
    option_aqua_park = Scenario.aqua_park.value
    option_millennium_mines = Scenario.millennium_mines.value
    option_karts_and_coasters = Scenario.karts_and_coasters.value
    option_mels_world = Scenario.mels_world.value
    option_mothball_mountain = Scenario.mothball_mountain.value
    option_pacific_pyramids = Scenario.pacific_pyramids.value
    option_crumbly_woods = Scenario.crumbly_woods.value
    # option_big_pier = Scenario.big_pier.value
    option_lightning_peaks = Scenario.lightning_peaks.value
    option_ivory_towers = Scenario.ivory_towers.value
    option_rainbow_valley = Scenario.rainbow_valley.value
    option_thunder_rock = Scenario.thunder_rock.value
    option_mega_park = Scenario.mega_park.value
    option_whispering_cliffs = Scenario.whispering_cliffs.value
    option_three_monkeys_park = Scenario.three_monkeys_park.value
    option_canary_mines = Scenario.canary_mines.value
    option_barony_bridge = Scenario.barony_bridge.value
    option_funtopia = Scenario.funtopia.value
    option_haunted_harbor = Scenario.haunted_harbor.value
    option_fun_fortress = Scenario.fun_fortress.value
    option_future_world = Scenario.future_world.value
    option_gentle_glen = Scenario.gentle_glen.value
    # option_jolly_jungle = Scenario.jolly_jungle.value #Impossible with the right settings
    option_hydro_hills = Scenario.hydro_hills.value
    option_sprightly_park = Scenario.sprightly_park.value
    option_magic_quarters = Scenario.magic_quarters.value
    option_fruit_farm = Scenario.fruit_farm.value
    option_butterfly_dam = Scenario.butterfly_dam.value
    option_coaster_canyon = Scenario.coaster_canyon.value
    option_thunderstorm_park = Scenario.thunderstorm_park.value
    option_harmonic_hills = Scenario.harmonic_hills.value
    option_roman_village = Scenario.roman_village.value
    option_swamp_cove = Scenario.swamp_cove.value
    option_adrenaline_heights = Scenario.adrenaline_heights.value
    option_utopia_park = Scenario.utopia_park.value
    option_rotting_heights = Scenario.rotting_heights.value
    option_fiasco_forest = Scenario.fiasco_forest.value
    option_pickle_park = Scenario.pickle_park.value
    option_giggle_downs = Scenario.giggle_downs.value
    option_mineral_park = Scenario.mineral_park.value
    option_coaster_crazy = Scenario.coaster_crazy.value
    # option_urban_park = Scenario.urban_park.value #Impossible with the right settings
    option_geoffery_gardens = Scenario.geoffery_gardens.value
    option_iceberg_islands = Scenario.iceberg_islands.value
    option_volcania = Scenario.volcania.value
    option_arid_heights = Scenario.arid_heights.value
    option_razor_rocks = Scenario.razor_rocks.value
    option_crater_lake = Scenario.crater_lake.value
    option_vertigo_views = Scenario.vertigo_views.value
    # option_big_pier_2 = Scenario.big_pier_2.value
    option_dragons_cove = Scenario.dragons_cove.value
    option_good_knight_park = Scenario.good_knight_park.value
    option_wacky_warren = Scenario.wacky_warren.value
    option_grand_glacier = Scenario.grand_glacier.value
    option_crazy_craters = Scenario.crazy_craters.value
    option_dusty_desert = Scenario.dusty_desert.value
    option_woodworm_park = Scenario.woodworm_park.value
    option_icarus_park = Scenario.icarus_park.value
    option_sunny_swamps = Scenario.sunny_swamps.value
    option_frightmare_hills = Scenario.frightmare_hills.value
    option_thunder_rocks = Scenario.thunder_rocks.value
    option_octagon_park = Scenario.octagon_park.value
    option_pleasure_island = Scenario.pleasure_island.value
    option_icicle_worlds = Scenario.icicle_worlds.value
    option_southern_sands = Scenario.southern_sands.value
    option_tiny_towers = Scenario.tiny_towers.value
    option_nevermore_park = Scenario.nevermore_park.value
    option_pacifica = Scenario.pacifica.value
    option_urban_jungle = Scenario.urban_jungle.value
    option_terror_town = Scenario.terror_town.value
    # option_megaworld_park = Scenario.megaworld_park.value #Nothing but Logic Breaks
    option_venus_ponds = Scenario.venus_ponds.value
    # option_micro_park = Scenario.micro_park.value #Impossible with the right settings
    option_electric_fields = Scenario.electric_fields.value
    option_factory_capers = Scenario.factory_capers.value
    option_crazy_castle = Scenario.crazy_castle.value
    option_dusty_greens = Scenario.dusty_greens.value
    option_bumbly_bazzar = Scenario.bumbly_bazzar.value
    option_infernal_views = Scenario.infernal_views.value
    option_lucky_lake = Scenario.lucky_lake.value
    option_botany_breakers = Scenario.botany_breakers.value
    option_alpine_adventures = Scenario.alpine_adventures.value
    option_gravity_gardens = Scenario.gravity_gardens.value
    option_extreme_heights = Scenario.extreme_heights.value
    option_amity_airfield = Scenario.amity_airfield.value
    option_ghost_town = Scenario.ghost_town.value
    # option_fungus_woods = Scenario.fungus_woods.value #Impossible with the right settings
    option_rainbow_summit = Scenario.rainbow_summit.value
    option_over_the_edge = Scenario.over_the_edge.value
    option_great_wall_of_china = Scenario.great_wall_of_china.value
    option_canyon_calamities = Scenario.canyon_calamities.value
    option_sugarloaf_shores = Scenario.sugarloaf_shores.value
    option_mines_of_africa = Scenario.mines_of_africa.value
    option_park_maharaja = Scenario.park_maharaja.value
    option_ayers_adventure = Scenario.ayers_adventure.value
    option_european_extravaganza = Scenario.european_extravaganza.value
    option_rollercoaster_heaven = Scenario.rollercoaster_heaven.value
    option_lost_city_founder = Scenario.lost_city_founder.value
    option_mirage_madness = Scenario.mirage_madness.value
    option_icy_adventures = Scenario.icy_adventures.value
    option_okinawa_coast = Scenario.okinawa_coast.value
    option_beach_barbecue_blast = Scenario.beach_barbecue_blast.value
    option_from_the_ashes = Scenario.from_the_ashes.value
    option_wacky_waikiki = Scenario.wacky_waikiki.value
    option_rainforest_romp = Scenario.rainforest_romp.value
    option_sherwood_forest = Scenario.sherwood_forest.value
    option_crater_carnage = Scenario.crater_carnage.value
    option_alcatraz = Scenario.alcatraz.value
    option_woodstock = Scenario.woodstock.value
    option_cliffside_castle = Scenario.cliffside_castle.value
    option_extraterrestrial_extravaganza = Scenario.extraterrestrial_extravaganza.value
    option_animatronic_antics = Scenario.animatronic_antics.value
    option_coastersaurus = Scenario.coastersaurus.value
    option_schneider_shores = Scenario.schneider_shores.value
    option_gemini_city = Scenario.gemini_city.value
    option_mythological_madness = Scenario.mythological_madness.value
    option_rocky_rambles = Scenario.rocky_rambles.value
    option_metropolis = Scenario.metropolis.value
    option_rock_n_roll_revival = Scenario.rock_n_roll_revival.value
    # option_alton_towers = Scenario.alton_towers.value #Impossible with the right settings
    # option_blackpool_pleasure_beach = Scenario.blackpool_pleasure_beach.value #Impossible with the right settings
    # option_heide_park = Scenario.heide_park.value #Impossible with the right settings
    option_six_flags_belgium = Scenario.six_flags_belgium.value
    option_six_flags_great_adventure = Scenario.six_flags_great_adventure.value
    option_six_flags_holland = Scenario.six_flags_holland.value
    option_six_flags_magic_mountain = Scenario.six_flags_magic_mountain.value
    option_six_flags_over_texas = Scenario.six_flags_over_texas.value
    option_fort_anachronism = Scenario.fort_anachronism.value
    option_build_your_own_six_flags_belgium = Scenario.build_your_own_six_flags_belgium.value
    option_build_your_own_six_flags_great_adventure = Scenario.build_your_own_six_flags_great_adventure.value
    option_build_your_own_six_flags_holland = Scenario.build_your_own_six_flags_holland.value
    option_build_your_own_six_flags_magic_mountain = Scenario.build_your_own_six_flags_magic_mountain.value
    option_build_your_own_six_flags_park = Scenario.build_your_own_six_flags_park.value
    option_build_your_own_six_flags_over_texas = Scenario.build_your_own_six_flags_over_texas.value
    default = Scenario.archipelago_madness_vanilla.value    

class DeathLink(Choice):
    """If you die, everybody dies, and vise versa!
    - This manifests itself in exploding rides. Somebody dying will cause a random ride to crash,
    and building rides badly will cause others to die. There's a 20 second timer between deathlink events.
    Fix that coaster quickly! This option can be enabled/disabled in game as well by typing !!toggledeathlink
    in the chat tab of the unlock shop.
    """
    display_name = "DeathLink"
    option_disabled = DeathLinkMode.disabled.value
    option_enabled = DeathLinkMode.enabled.value
    default = DeathLinkMode.enabled.value

class SelectedVisibility(Choice):
    """Choose how much the unlock shop displays. 

    "Nothing" tells you nothing about the item you'll purchase. 

    Progression tells you what class of item (Normal, Progression, Useful Trap) you're sending.
    
    Recipient tells you who will receive the item, but not what they'll receive. 

    Progression Recipient tells you both the class of item and who receives it.
    
    Full tells you what you're buying and who receives it.
    """
    display_name = "Visibility"
    option_nothing = Visibility.nothing.value
    option_progression = Visibility.progression.value
    option_recipient = Visibility.recipient.value
    option_progression_recipient = Visibility.progression_recipient.value
    option_full = Visibility.full.value
    default = Visibility.recipient.value

class Awards(Choice):
    """Choose what types (if any) of awards will have checks behind them. 
    Negative awards will always reward a trap item, even if they're otherwise disabled!

    All Awards will have a check behind every award in the game. 

    Positive will only place a check behind awards with positive attributes.
    
    None will not place checks behind awards.
    """
    display_name = "Awards"
    option_all = Awards.all_awards.value
    option_positive = Awards.positive.value
    option_none = Awards.none.value
    default = Awards.all_awards.value

class ExcludeSafestPark(OpenRCT2Toggle):
    """Exclude the Safest Park Award from having a check. This may be useful depending on deathlink settings."""
    display_name = "Exclude Safest Park Award"

class SelectedDifficulty(Choice):
    """Choose a difficulty for the randomization. This will make rides have more difficult stat results (If that's enabled), as well as affect
    things like the loan interest rate.
    """
    display_name = "Difficulty"
    option_very_easy = Difficulty.very_easy.value
    option_easy = Difficulty.easy.value
    option_medium = Difficulty.medium.value
    option_hard = Difficulty.hard.value
    option_extreme = Difficulty.extreme.value
    default = Difficulty.medium.value

class SelectedIntensity(Choice):
    """Choose a preferred intensity for your guests. Less intense will limit guests to a maximum of 4 intensity, and more intense will limit guests
    to a minimum of 8 intensity in most circumstances. Normal is highly recommended for most players! Seriously, unless you really know what you 
    are doing and want the (likely very tedious) challenge, you shouldn't change this.
    """
    display_name = "Preferred Intensity"
    option_less_intense = PreferredIntensity.less_intense.value
    option_normal = PreferredIntensity.normal.value
    option_more_intense = PreferredIntensity.more_intense.value
    default = PreferredIntensity.normal.value

class SelectedRandomizationRange(Choice):
    """Influences how spread random values will be (Mostly this affects the excitement, intensity, and nausea ratings). The more extreme this value,
    the more extreme the difficulty will swing, with easy becoming much easier and hard becoming much more difficult.
    """
    display_name = "Randomization Range"
    option_none = RandomizationRange.none.value
    option_low = RandomizationRange.low.value
    option_medium = RandomizationRange.medium.value
    option_high = RandomizationRange.high.value
    option_extreme = RandomizationRange.extreme.value
    default = RandomizationRange.medium.value

class IgnoreRideStatChanges(OpenRCT2Toggle):
    """Disables changes to base ride stats. If enabled, rides will always behave like they do in the base game."""
    display_name = "Ignore Ride Stat Changes"

class SelectedScenarioLength(Choice):
    """Choose how long this game will last. This will affect things such as unlock shop prices and if prerequisites are required before purchase. It's recommended to choose based on how long other worlds in the multi-world take to complete.
    Synchronous Short: Around 2 hours to complete.
    Synchronous Long: Around 4 hours to complete.
    Lengthy: Recommended for Asyncs.
    Marathon: Recommended for Asyncs.
    """
    display_name = "Scenario Length"
    option_synchronous_short = ScenarioLength.synchronous_short.value
    option_synchronous_long = ScenarioLength.synchronous_long.value
    option_lengthy = ScenarioLength.lengthy.value
    option_marathon = ScenarioLength.marathon.value
    default = ScenarioLength.synchronous_short.value

class SelectedStatReRolls(Choice):
    """How often to re-randomize the stats for ride types. Build the Theme Park of Theseus!
    """
    display_name = "Stat Re-Rolls"
    option_never = StatReRolls.never.value
    option_infrequent = StatReRolls.infrequent.value
    option_semi_frequent = StatReRolls.semi_frequent.value
    option_frequent = StatReRolls.frequent.value
    option_very_frequent = StatReRolls.very_frequent.value
    option_extremely_frequent = StatReRolls.extremely_frequent.value
    default = StatReRolls.infrequent.value

class SelectedDifficultGuestGeneration(Choice):
    """Makes guests harder to generate. Unlockable puts an item in generation that disables the rule when found."""
    display_name = "Difficult Guest Generation"
    option_off = DifficultGuestGeneration.off.value
    option_unlockable = DifficultGuestGeneration.unlockable.value
    option_on = DifficultGuestGeneration.on.value
    default = DifficultGuestGeneration.unlockable.value

class SelectedDifficultParkRating(Choice):
    """Makes park rating harder to improve. Unlockable puts an item in generation that disables the rule when found."""
    display_name = "Difficult Park Rating"
    option_off = DifficultParkRating.off.value
    option_unlockable = DifficultParkRating.unlockable.value
    option_on = DifficultParkRating.on.value
    default = DifficultParkRating.unlockable.value

class SelectedForbidHighConstruction(Choice):
    """Limits building to tree height. Unlockable puts an item in generation that disables the rule when found."""
    display_name = "Forbid High Construction"
    option_off = ForbidHighConstruction.off.value
    option_unlockable = ForbidHighConstruction.unlockable.value
    option_on = ForbidHighConstruction.on.value
    default = ForbidHighConstruction.unlockable.value

class SelectedForbidLandscapeChanges(Choice):
    """Forbids the landscape from being altered. Unlockable puts an item in generation that disables the rule when found."""
    display_name = "Forbid Landscape Changes"
    option_off = ForbidLandscapeChanges.off.value
    option_unlockable = ForbidLandscapeChanges.unlockable.value
    option_on = ForbidLandscapeChanges.on.value
    default = ForbidLandscapeChanges.unlockable.value

class SelectedForbidMarketingCampaigns(Choice):
    """Forbids marketing campaigns. Unlockable puts an item in generation that disables the rule when found."""
    display_name = "Forbid Marketing Campaigns"
    option_off = ForbidMarketingCampaigns.off.value
    option_unlockable = ForbidMarketingCampaigns.unlockable.value
    option_on = ForbidMarketingCampaigns.on.value
    default = ForbidMarketingCampaigns.unlockable.value

class SelectedForbidTreeRemoval(Choice):
    """Forbids removing trees. Unlockable puts an item in generation that disables the rule when found."""
    display_name = "Forbid Tree Removal"
    option_off = ForbidTreeRemoval.off.value
    option_unlockable = ForbidTreeRemoval.unlockable.value
    option_on = ForbidTreeRemoval.on.value
    default = ForbidTreeRemoval.unlockable.value


class RandomizeParkValues(OpenRCT2OnToggle):
    """Randomizes values such as starting cash, starting bank loan amount, and the max bank loan"""
    display_name = "Randomize Park Values"

# class Include_Guest_Objective(OpenRCT2OnToggle):
#     """Include an objective to reach a certain number of guests. Multiple objectives can be enabled!"""
#     display_name = "Include Guest Objective"

class GuestObjective(Range):
    """Choose how many guests are required to win the scenario"""
    display_name = "Guest Objective"
    range_start = 1
    range_end = 7500
    default = 1000

# class Include_Park_Value_Objective(OpenRCT2OnToggle):
#     """Include an objective to achieve a certain park value in Dollars (The game will adjust to your local currency). Multiple objectives can be enabled!"""
#     display_name = "Include Park Value Objective"

class ParkValueObjective(Range):
    """If enabled, choose what park value (In USD) is required to win the scenario."""
    display_name = "Park Value Objective"
    range_start = 0
    range_end = 1000000
    default = 200000

# class Include_Roller_Coaster_Objective(OpenRCT2OnToggle):
#     """Include an objective to build a certain number of Roller Coasters with optional parameters. Multiple objectives can be enabled!"""
#     display_name = "Include Roller Coaster Objective"

class RollerCoasterObjective(Range):
    """If enabled, choose how many coasters, and what prerequisites they need to beat the scenario."""
    display_name = "Roller Coaster Objective"
    range_start = 0
    range_end = 20
    default = 5

class RollerCoasterExcitement(Range):
    """Select the minimum excitement 😀 for a coaster to count towards your objective. 0 will disable a minimum excitement rating."""
    display_name = "Excitement Requirement"
    range_start = 0
    range_end = 9
    default = 5

class RollerCoasterIntensity(Range):
    """Select the minimum intensity 😬 for a coaster to count towards your objective. 0 will disable a minimum intensity rating."""
    display_name = "Intensity Requirement"
    range_start = 0
    range_end = 9
    default = 5

class RollerCoasterNausea(Range):
    """Select the minimum nausea 🤢 for a coaster to count towards your objective. 0 will disable a minimum nausea rating."""
    display_name = "Nausea Requirement"
    range_start = 0
    range_end = 6
    default = 4

class ShopMinimumExcitement(Range):
    """If the shop determines you need a ride with a minimum excitement, this value will be the lowest it can ask for.
    If this value is higher than the maximum, the generator will assume it is a mistake and set it to 0.
    """
    display_name = "Minimum Shop Excitement Requirement"
    range_start = 0
    range_end = 10
    default = 0

class ShopMinimumIntensity(Range):
    """If the shop determines you need a ride with a minimum intensity, this value will be the lowest it can ask for.
    If this value is higher than the maximum, the generator will assume it is a mistake and set it to 0.
    """
    display_name = "Minimum Shop Intensity Requirement"
    range_start = 0
    range_end = 7
    default = 0

class ShopMinimumNausea(Range):
    """If the shop determines you need a ride with a minimum nausea, this value will be the lowest it can ask for.
    If this value is higher than the maximum, the generator will assume it is a mistake and set it to 0.
    """
    display_name = "Minimum Shop Nausea Requirement"
    range_start = 0
    range_end = 4
    default = 0

class ShopMinimumLength(Range):
    """If the shop determines you need a ride with a minimum length (In Meters), this value in meters will 
    be the lowest it can ask for. If this value is higher than the maximum, the generator will assume it is a 
    mistake and set it to 0.
    """
    display_name = "Minimum Shop Length Requirement"
    range_start = 0
    range_end = 2500
    default = 0

class ShopMinimumTotalCustomers(Range):
    """If the shop determines you need a ride with a minimum total number of customers, this value will be the 
    lowest it can ask for. If this value is higher than the maximum, the generator will assume it is a mistake and 
    set it to 0.
    """
    display_name = "Minimum Shop Customers Requirement"
    range_start = 0
    range_end = 1000
    default = 0

class ShopMaximumExcitement(Range):
    """If the shop determines you need a ride with a minimum excitement, this value will be the highest it can ask for.
    """
    display_name = "Maximum Shop Excitement Requirement"
    range_start = 0
    range_end = 10
    default = 5

class ShopMaximumIntensity(Range):
    """If the shop determines you need a ride with a minimum intensity, this value will be the highest it can ask for.
    """
    display_name = "Maximum Shop Intensity Requirement"
    range_start = 0
    range_end = 7
    default = 5

class ShopMaximumNausea(Range):
    """If the shop determines you need a ride with a minimum nausea, this value will be the highest it can ask for.
    """
    display_name = "Maximum Shop Nausea Requirement"
    range_start = 0
    range_end = 4
    default = 4

class ShopMaximumLength(Range):
    """If the shop determines you need a ride with a minimum length (In Meters), 
    this value will be the highest it can ask for.
    """
    display_name = "Maximum Shop Length Requirement"
    range_start = 0
    range_end = 2500
    default = 500

class ShopMaximumTotalCustomers(Range):
    """If the shop determines you need a ride with a minimum total number of customers, this value will be the 
    highest it can ask for.
    """
    display_name = "Maximum Shop Total Customers Requirement"
    range_start = 0
    range_end = 1000
    default = 400

class BalanceGuestCounts(OpenRCT2OnToggle):
    """Attempts to balance the minimum guest requirements to the ride they're attached to. Low throughput rides
    like Spiral Slides will tend towards the minimum, while high throughput rides like roller coasters will 
    tend towards the maximum.
    """
    display_name = "Balance Guest Counts"

class RequiredUniqueRides(Range):
    """Requires specific rides to be built before scenario completion is awarded. These will tend to appear in the later half of the game.
    It's highly recommended to have this set to at least 1!"""
    display_name = "Unique Ride Requirement"
    range_start = 0
    range_end = 10
    default = 5

class LocalityOfUniqueRides(Choice):
    """No-op; still here to prevent old YAMLs from breaking"""
    display_name = "Placement of Unique Rides"
    option_off = 0
    option_local = 1
    option_remote = 2
    default = 0
    visibility = OptionVisibility.none

class ParkRatingObjective(Range):
    """If enabled, choose the minimum park rating needed to beat the scenario."""
    display_name = "Park Rating Objective"
    range_start = 0
    range_end = 999
    default = 800

class PayOffLoan(OpenRCT2OnToggle):
    """Require Loan to be paid off before scenario completion is awarded. Multiple objectives can be enabled!"""
    display_name = "Pay Off Loan"

class MonopolyMode(OpenRCT2Toggle):
    """Monopoly Mode is a new objective type. Every unowned tile will be set to purchasable (Or purchasable construction rights for any unowned tile with a grounded path. Elevated paths will not be purchasable). To complete the objective, all tiles on the map must be purchased. Multiple Objectives can be enabled!"""
    display_name = "Monopoly Mode"

class Fireworks(OpenRCT2OnToggle):
    """Have an explosive firework display on victory! Strongly discouraged if you intend to keep playing after victory or if you expect to have a huge park."""
    display_name = "Fireworks"

class IncludeGamespeedItems(OpenRCT2OnToggle):
    """If included, the ability to use the speed toggle will be restricted behind an item. 4 items total will be added, each progressively unlocking a faster speed."""
    display_name = "Include Gamespeed Items"

class FurryConventionTraps(Range):
    """When found, instantly hosts a furry convention in your park! Adding traps will increase the total number of items in the world."""
    display_name = "Furry Convention Trap"
    range_start = 0
    range_end = 20
    default = 5

class BathroomTraps(Range):
    """When found, instantly maxes out the bathroom stat of every guest! Adding traps will increase the total number of items in the world."""
    display_name = "Bathroom Trap"
    range_start = 0
    range_end = 20
    default = 5

class SpamTraps(Range):
    """When found, spams ads all over the screen! Adding traps will increase the total number of items in the world."""
    display_name = "Spam Trap"
    range_start = 0
    range_end = 20
    default = 5

class LoanSharkTraps(Range):
    """When found, increases your loan! Adding traps will increase the total number of items in the world."""
    display_name = "Loan Shark Trap"
    range_start = 0
    range_end = 20
    default = 5

class Filler(Range):
    """How many extra filler items to add to the mix as a percentage. This will mostly consist of Cash Bonuses."""
    display_name = "Filler"
    range_start = 1
    range_end = 50
    default = 10

class IncludeATM(OpenRCT2OnToggle):
    """Includes an ATM in the item list, regardless of whether it normally appears in the chosen scenario."""
    display_name = "Include ATM"

class IncludeFirstAid(OpenRCT2OnToggle):
    """Includes a First Aid Room in the item list, regardless of whether it normally appears in the chosen scenario."""
    display_name = "Include First Aid Room"

class AllRidesAndSceneryBase(OpenRCT2Toggle):
    """Adds every ride and scenery pack in the base game to the item pool. This will make for a significantly longer scenario."""
    display_name = "Include All Rides and Scenery (Base Game)"

class AllRidesAndSceneryExpansion(OpenRCT2Toggle):
    """Adds every ride and scenery pack in the RCT2 Expansion Packs to the item pool. If this is true the base game rides and 
    scenery will also be included. This will make for a significantly longer scenario."""
    display_name = "Include All Rides and Scenery (Expansion Packs)"

class Skips(Range):
    """By default, every game starts with a single skip to ignore a shop requirement. This will add additional skips to 
    be found in the item pool."""
    display_name = "Skips"
    range_start = 0
    range_end = 100
    default = 7

openrct2_option_groups = [
    OptionGroup("Scenario Options", [
        SelectedScenario,
        SelectedDifficulty,
        SelectedScenarioLength,
        SelectedRandomizationRange,
        RandomizeParkValues,
        SelectedIntensity,
        SelectedStatReRolls,
    ]),
    OptionGroup("Goal Options", [
        GuestObjective,
        ParkValueObjective,
        RollerCoasterObjective,
        RollerCoasterExcitement,
        RollerCoasterIntensity,
        RollerCoasterNausea,
        RequiredUniqueRides,
        LocalityOfUniqueRides,
        ParkRatingObjective,
        PayOffLoan,
        MonopolyMode,
        Fireworks
    ]),
    OptionGroup("Rules", [
        SelectedDifficultGuestGeneration,
        SelectedDifficultParkRating,
        SelectedForbidHighConstruction,
        SelectedForbidLandscapeChanges,
        SelectedForbidMarketingCampaigns,
        SelectedForbidTreeRemoval
    ]),
    OptionGroup("Shop Options", [
        ShopMinimumExcitement,
        ShopMaximumExcitement,
        ShopMinimumIntensity,
        ShopMaximumIntensity,
        ShopMinimumNausea,
        ShopMaximumNausea,
        ShopMinimumLength,
        ShopMaximumLength,
        ShopMinimumTotalCustomers,
        ShopMaximumTotalCustomers,
        BalanceGuestCounts,
        SelectedVisibility,
        Awards,
        ExcludeSafestPark
    ]),
    OptionGroup("Item & Trap Options", [
        Filler,
        IncludeATM,
        IncludeFirstAid,
        IncludeGamespeedItems,
        Skips,
        FurryConventionTraps,
        BathroomTraps,
        SpamTraps,
        LoanSharkTraps,
        AllRidesAndSceneryBase,
        AllRidesAndSceneryExpansion
    ]),
]

@dataclass
class openRCT2Options(PerGameCommonOptions):
    # generator options
    # location_balancing: LocationBalancing
    difficulty: SelectedDifficulty
    shop_minimum_excitement: ShopMinimumExcitement
    shop_maximum_excitement: ShopMaximumExcitement
    shop_minimum_intensity: ShopMinimumIntensity
    shop_maximum_intensity: ShopMaximumIntensity
    shop_minimum_nausea: ShopMinimumNausea
    shop_maximum_nausea: ShopMaximumNausea
    shop_minimum_length: ShopMinimumLength
    shop_maximum_length: ShopMaximumLength
    shop_minimum_total_customers: ShopMinimumTotalCustomers
    shop_maximum_total_customers: ShopMaximumTotalCustomers
    balance_guest_counts: BalanceGuestCounts
    awards: Awards
    exclude_safest_park: ExcludeSafestPark
    ignore_ride_stat_changes: IgnoreRideStatChanges
    scenario_length: SelectedScenarioLength
    scenario: SelectedScenario
    filler: Filler
    include_atm: IncludeATM
    include_first_aid: IncludeFirstAid
    all_rides_and_scenery_base: AllRidesAndSceneryBase
    all_rides_and_scenery_expansion: AllRidesAndSceneryExpansion
    skips: Skips

    # deathlink
    death_link: DeathLink

    # traps
    furry_convention_traps: FurryConventionTraps
    bathroom_traps: BathroomTraps
    spam_traps: SpamTraps
    loan_shark_traps: LoanSharkTraps

    # in-game options. All Archipelago needs to do with these is pass them to OpenRCT2. The game will handle the rest
    randomization_range: SelectedRandomizationRange
    stat_rerolls: SelectedStatReRolls
    randomize_park_values: RandomizeParkValues
    visibility: SelectedVisibility
    preferred_intensity: SelectedIntensity
    # include_guest_objective: Include_Guest_Objective
    guest_objective: GuestObjective
    # include_park_value_objective: Include_Park_Value_Objective
    park_value_objective: ParkValueObjective
    # include_roller_coaster_objective: Include_Roller_Coaster_Objective
    roller_coaster_objective: RollerCoasterObjective
    roller_coaster_excitement: RollerCoasterExcitement
    roller_coaster_intensity: RollerCoasterIntensity
    roller_coaster_nausea: RollerCoasterNausea
    required_unique_rides: RequiredUniqueRides
    unique_rides_placement: LocalityOfUniqueRides
    # include_park_rating_objective: Include_Park_Rating_Objective
    park_rating_objective: ParkRatingObjective
    pay_off_loan: PayOffLoan
    monopoly_mode: MonopolyMode
    fireworks: Fireworks
    include_gamespeed_items: IncludeGamespeedItems
    # park rules. Depending on the option, these may affect which items are created
    difficult_guest_generation: SelectedDifficultGuestGeneration
    difficult_park_rating: SelectedDifficultParkRating
    forbid_high_construction: SelectedForbidHighConstruction
    forbid_landscape_changes: SelectedForbidLandscapeChanges
    forbid_marketing_campaigns: SelectedForbidMarketingCampaigns
    forbid_tree_removal: SelectedForbidTreeRemoval

