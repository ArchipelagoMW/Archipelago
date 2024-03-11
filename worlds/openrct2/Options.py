from enum import IntEnum
from typing import TypedDict
from Options import DefaultOnToggle, Toggle, Range, Choice, OptionSet, PerGameCommonOptions
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
    africa_victoria_falls = 97
    asia_great_wall_of_china_tourism_enhancement = 98
    north_america_grand_canyon = 99
    south_america_rio_carnival = 100
    africa_african_diamond_mine = 101
    asia_maharaja_palace = 102
    australasia_ayers_rock = 103
    europe_european_cultural_festival = 104
    north_america_rollercoaster_heaven = 105
    south_america_inca_lost_city = 106
    africa_oasis = 107
    antartic_ecological_salvage = 108
    asia_japanese_costal_reclaim = 109
    australasia_fun_at_the_beach = 110
    europe_renovation = 111
    n_america_extreme_hawaiian_island = 112
    south_america_rain_forest_plateau = 113
    dark_age_robin_hood = 114
    prehistoric_after_the_asteroid = 115
    roaring_twenties_prison_island = 116
    rock_n_roll_flower_power = 117
    dark_age_castle = 118
    future_first_encounters = 119
    mythological_animatronic_film_set = 120
    jurassic_safari = 121
    roaring_twenties_schneider_cup = 122
    future_future_world = 123
    mythological_cradle_of_civilization = 124
    prehistoric_stone_age = 125
    roaring_twenties_skyscrapers = 126
    rock_n_roll_rock_n_roll = 127
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
    
class LocationBalancingMode(IntEnum):
    disabled = 0
    compromise = 1
    full = 2


class DeathLinkMode(IntEnum):
    disabled = 0
    enabled = 1

class Visibility(IntEnum):
    nothing = 0
    recipient = 1
    full = 2

class Difficulty(IntEnum):
    very_easy = 0
    easy = 1
    medium = 2
    hard = 3
    extreme = 4

class Preferred_Intensity(IntEnum):
    less_intense = 0
    normal = 1
    more_intense = 2

class Randomization_Range(IntEnum):
    none = 0
    low = 1
    medium = 2
    high = 3
    extreme = 4

class Scenario_Length(IntEnum):
    synchronous_short = 0
    synchronous_long = 1
    lengthy = 2
    marathon = 3
    
class Stat_ReRolls(IntEnum):
    never = 0
    infrequent = 1
    semi_frequent = 2
    frequent = 3
    very_frequent = 4
    extremely_frequent = 5

class Difficult_Guest_Generation(IntEnum):
    off = 0
    unlockable = 1
    on = 2

class Difficult_Park_Rating(IntEnum):
    off = 0
    unlockable = 1
    on = 2

class Forbid_High_Construction(IntEnum):
    off = 0
    unlockable = 1
    on = 2

class Forbid_Landscape_Changes(IntEnum):
    off = 0
    unlockable = 1
    on = 2

class Forbid_Marketing_Campaigns(IntEnum):
    off = 0
    unlockable = 1
    on = 2

class Forbid_Tree_Removal(IntEnum):
    off = 0
    unlockable = 1
    on = 2

class OpenRCT2OnToggle(DefaultOnToggle):
    @property
    def result(self) -> bool:
        return bool(self.value)


class OpenRCT2Toggle(Toggle):
    @property
    def result(self) -> bool:
        return bool(self.value)


class LocationBalancing(Choice):
    """Location balancing affects the density of progression items found in your world relative to other worlds. This setting changes nothing for solo games.

    - Disabled: Location density in your world can fluctuate greatly depending on the settings of other players. In extreme cases, your world may be entirely populated with filler items

    - Compromise: Locations are balanced to a midpoint between "fair" and "natural"

    - Full: Locations are balanced in an attempt to make the number of progression items sent out and received equal over the entire game"""
    auto_display_name = True
    display_name = "Location Balancing"
    option_disabled = LocationBalancingMode.disabled.value
    option_compromise = LocationBalancingMode.compromise.value
    option_full = LocationBalancingMode.full.value
    default = LocationBalancingMode.compromise.value

class SelectedScenario(Choice):
    """Choose which scenario you'd like to play! Random won't choose scenarios that are unreasonably difficult/tedious.
    Future updates will allow custom scenarios.
    """
    auto_display_name = True
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
    option_africa_victoria_falls = Scenario.africa_victoria_falls.value
    option_asia_great_wall_of_china_tourism_enhancement = Scenario.asia_great_wall_of_china_tourism_enhancement.value
    option_north_america_grand_canyon = Scenario.north_america_grand_canyon.value
    option_south_america_rio_carnival = Scenario.south_america_rio_carnival.value
    option_africa_african_diamond_mine = Scenario.africa_african_diamond_mine.value
    option_asia_maharaja_palace = Scenario.asia_maharaja_palace.value
    option_australasia_ayers_rock = Scenario.australasia_ayers_rock.value
    option_europe_european_cultural_festival = Scenario.europe_european_cultural_festival.value
    option_north_america_rollercoaster_heaven = Scenario.north_america_rollercoaster_heaven.value
    option_south_america_inca_lost_city = Scenario.south_america_inca_lost_city.value
    option_africa_oasis = Scenario.africa_oasis.value
    option_antartic_ecological_salvage = Scenario.antartic_ecological_salvage.value
    option_asia_japanese_costal_reclaim = Scenario.asia_japanese_costal_reclaim.value
    option_australasia_fun_at_the_beach = Scenario.australasia_fun_at_the_beach.value
    option_europe_renovation = Scenario.europe_renovation.value
    option_n_america_extreme_hawaiian_island = Scenario.n_america_extreme_hawaiian_island.value
    option_south_america_rain_forest_plateau = Scenario.south_america_rain_forest_plateau.value
    option_dark_age_robin_hood = Scenario.dark_age_robin_hood.value
    option_prehistoric_after_the_asteroid = Scenario.prehistoric_after_the_asteroid.value
    option_roaring_twenties_prison_island = Scenario.roaring_twenties_prison_island.value
    option_rock_n_roll_flower_power = Scenario.rock_n_roll_flower_power.value
    option_dark_age_castle = Scenario.dark_age_castle.value
    option_future_first_encounters = Scenario.future_first_encounters.value
    option_mythological_animatronic_film_set = Scenario.mythological_animatronic_film_set.value
    option_jurassic_safari = Scenario.jurassic_safari.value
    option_roaring_twenties_schneider_cup = Scenario.roaring_twenties_schneider_cup.value
    option_future_future_world = Scenario.future_future_world.value
    option_mythological_cradle_of_civilization = Scenario.mythological_cradle_of_civilization.value
    option_prehistoric_stone_age = Scenario.prehistoric_stone_age.value
    option_roaring_twenties_skyscrapers = Scenario.roaring_twenties_skyscrapers.value
    option_rock_n_roll_rock_n_roll = Scenario.rock_n_roll_rock_n_roll.value
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
    """DeathLink is an opt-in feature for Multiworlds where individual death events are propagated to all games with DeathLink enabled.

    - Disabled: No changes to base game.

    - Enabled: When any ride crashes, everybody (with DeathLink enabled) dies. Inversely, when anybody (again, with DeathLink enabled) dies, a random ride will explode.

    When enabled, there is a 20 second rest period between any deathlink event. Fix that coaster quickly!
    """
    auto_display_name = True
    display_name = "DeathLink"
    option_disabled = DeathLinkMode.disabled.value
    option_enabled = DeathLinkMode.enabled.value
    default = DeathLinkMode.enabled.value

class SelectedVisibility(Choice):
    """Choose how much the unlock shop displays. 

    "Nothing" tells you nothing about the item you'll purchase. 
    
    Recipient tells you who will recieve the item, but not what they'll receive. 
    
    Full tells you what you're buying and who recieves it.
    """
    auto_display_name = True
    display_name = "Visibility"
    option_nothing = Visibility.nothing.value
    option_recipient = Visibility.recipient.value
    option_full = Visibility.full.value
    default = Visibility.recipient.value

class SelectedDifficulty(Choice):
    """Choose a difficulty for the randomization. This will make rides have more difficult stat results (If that's enabled), as well as affect
    things like the loan interest rate.
    """
    auto_display_name = True
    display_name = "Difficulty"
    option_very_easy = Difficulty.very_easy.value
    option_easy = Difficulty.easy.value
    option_medium = Difficulty.medium.value
    option_hard = Difficulty.hard.value
    option_extreme = Difficulty.extreme.value
    default = Difficulty.medium.value

class SelectedIntensity(Choice):
    """Choose a prefered intensity for your guests. Less intense will limit guests to a maximum of 4 intensity, and more intense will limit guests
    to a minimum of 8 intensity in most circumstances. Normal is reccommended for most players.
    """
    option_less_intense = Preferred_Intensity.less_intense.value
    option_normal = Preferred_Intensity.normal.value
    option_more_intense = Preferred_Intensity.more_intense.value
    default = Preferred_Intensity.normal.value

class SelectedRandomizationRange(Choice):
    """Influences how spread random values will be (Mostly this affects the excitement, intensity, and nausea ratings). The more extreme this value,
    the more extreme the difficulty will swing, with easy becoming much easier and hard becoming much more difficult.
    """
    auto_display_name = True
    display_name = "Randomization Range"
    option_none = Randomization_Range.none.value
    option_low = Randomization_Range.low.value
    option_medium = Randomization_Range.medium.value
    option_high = Randomization_Range.high.value
    option_extreme = Randomization_Range.extreme.value
    default = Randomization_Range.medium.value

class Ignore_Ride_Stat_Changes(OpenRCT2Toggle):
    """Disables changes to base ride stats. If enabled, rides will always behave like they do in the base game."""
    display_name = "Ignore Ride Stat Changes"

class SelectedScenarioLength(Choice):
    """Choose how long this game will last. This will affect things such as unlock shop prices and if prerequisites are required before purchase. It's reccomended to choose based on how long other worlds in the multi-world take to complete.
    Synchronus Short: Around 2 hours to complete.
    Synchronus Long: Around 4 hours to complete.
    Lengthy: Recommended for Asynchs.
    Marathon: Recommended for Asynchs.
    """
    auto_display_name = True
    display_name = "Scenario Length"
    option_synchronous_short = Scenario_Length.synchronous_short.value
    option_synchronous_long = Scenario_Length.synchronous_long.value
    option_lengthy = Scenario_Length.lengthy.value
    option_marathon = Scenario_Length.marathon.value
    default = Scenario_Length.synchronous_short.value

class SelectedStatReRolls(Choice):
    """How often to rerandomize the stats for ride types. Build the Theme Park of Theseus!
    """
    auto_display_name = True
    display_name = "Stat Re-Rolls"
    option_never = Stat_ReRolls.never.value
    option_infrequent = Stat_ReRolls.infrequent.value
    option_semi_frequent = Stat_ReRolls.semi_frequent.value
    option_frequent = Stat_ReRolls.frequent.value
    option_very_frequent = Stat_ReRolls.very_frequent.value
    option_extremely_frequent = Stat_ReRolls.extremely_frequent.value
    default = Stat_ReRolls.infrequent.value

class SelectedDifficultGuestGeneration(Choice):
    """Makes guests harder to generate. Unlockable puts an item in generation that disables the rule when found."""
    display_name = "Difficult Guest Generation"
    option_off = Difficult_Guest_Generation.off.value
    option_unlockable = Difficult_Guest_Generation.unlockable.value
    option_on = Difficult_Guest_Generation.on.value
    default = Difficult_Guest_Generation.unlockable.value

class SelectedDifficultParkRating(Choice):
    """Makes park rating harder to improve. Unlockable puts an item in generation that disables the rule when found."""
    display_name = "Difficult Park Rating"
    option_off = Difficult_Park_Rating.off.value
    option_unlockable = Difficult_Park_Rating.unlockable.value
    option_on = Difficult_Park_Rating.on.value
    default = Difficult_Park_Rating.unlockable.value

class SelectedForbidHighConstruction(Choice):
    """Limits building to tree height. Unlockable puts an item in generation that disables the rule when found."""
    display_name = "Forbid High Construction"
    option_off = Forbid_High_Construction.off.value
    option_unlockable = Forbid_High_Construction.unlockable.value
    option_on = Forbid_High_Construction.on.value
    default = Forbid_High_Construction.unlockable.value

class SelectedForbidLandscapeChanges(Choice):
    """Forbids the landscape from being altered. Unlockable puts an item in generation that disables the rule when found."""
    display_name = "Forbid Landscape Changes"
    option_off = Forbid_Landscape_Changes.off.value
    option_unlockable = Forbid_Landscape_Changes.unlockable.value
    option_on = Forbid_Landscape_Changes.on.value
    default = Forbid_Landscape_Changes.unlockable.value

class SelectedForbidMarketingCampaigns(Choice):
    """Forbids marketing campaigns. Unlockable puts an item in generation that disables the rule when found."""
    display_name = "Forbid Marketing Campaigns"
    option_off = Forbid_Marketing_Campaigns.off.value
    option_unlockable = Forbid_Marketing_Campaigns.unlockable.value
    option_on = Forbid_Marketing_Campaigns.on.value
    default = Forbid_Marketing_Campaigns.unlockable.value

class SelectedForbidTreeRemoval(Choice):
    """Forbids removing trees. Unlockable puts an item in generation that disables the rule when found."""
    display_name = "Forbid Tree Removal"
    option_off = Forbid_Tree_Removal.off.value
    option_unlockable = Forbid_Tree_Removal.unlockable.value
    option_on = Forbid_Tree_Removal.on.value
    default = Forbid_Tree_Removal.unlockable.value


class Randomize_Park_Values(OpenRCT2OnToggle):
    """Randomizes values such as starting cash, starting bank loan amount, and the max bank loan"""
    display_name = "Randomize Park Values"

# class Include_Guest_Objective(OpenRCT2OnToggle):
#     """Include an objective to reach a certain number of guests. Multiple objectives can be enabled!"""
#     display_name = "Include Guest Objective"

class Guest_Objective(Range):
    """Choose how many guests are required to win the scenario"""
    display_name = "Guest Objective"
    range_start = 1
    range_end = 7500
    default = 1000

# class Include_Park_Value_Objective(OpenRCT2OnToggle):
#     """Include an objective to achive a certain park value in Dollars (The game will adjust to your local currency). Multiple objectives can be enabled!"""
#     display_name = "Include Park Value Objective"

class Park_Value_Objective(Range):
    """If enabled, choose what park value (In USD) is required to win the scenario."""
    display_name = "Park Value Objective"
    range_start = 0
    range_end = 1000000
    default = 200000

# class Include_Roller_Coaster_Objective(OpenRCT2OnToggle):
#     """Include an objective to build a certain number of Roller Coasters with optional Paramaters. Multiple objectives can be enabled!"""
#     display_name = "Include Roller Coaster Objective"

class Roller_Coaster_Objective(Range):
    """If enabled, choose how many coasters, and what prerequisites they need to beat the scenario."""
    display_name = "Roller Coaster Objective"
    range_start = 0
    range_end = 20
    default = 5

class Roller_Coaster_Excitement(Range):
    """Select the minimum excitement 😀 for a coaster to count towards your objective. 0 will disable a minimum excitement rating."""
    display_name = "Excitement Requirement"
    range_start = 0
    range_end = 10
    default = 5

class Roller_Coaster_Intensity(Range):
    """Select the minimum intensity 😬 for a coaster to count towards your objective. 0 will disable a minimum intensity rating."""
    display_name = "Intensity Requirement"
    range_start = 0
    range_end = 10
    default = 5

class Roller_Coaster_Nausea(Range):
    """Select the minimum nausea 🤢 for a coaster to count towards your objective. 0 will disable a minimum nausea rating."""
    display_name = "Nausea Requirement"
    range_start = 0
    range_end = 10
    default = 4

class Shop_Minimum_Excitement(Range):
    """If the shop determines you need a ride with a minimum excitement, this value will be the lowest it can ask for.
    If this value is higher than the maximum, the generator will assume it is a mistake and set it to 0.
    """
    display_name = "Minimum Shop Excitement Requirement"
    range_start = 0
    range_end = 10
    default = 0

class Shop_Minimum_Intensity(Range):
    """If the shop determines you need a ride with a minimum intensity, this value will be the lowest it can ask for.
    If this value is higher than the maximum, the generator will assume it is a mistake and set it to 0.
    """
    display_name = "Minimum Shop Intensity Requirement"
    range_start = 0
    range_end = 7
    default = 0

class Shop_Minimum_Nausea(Range):
    """If the shop determines you need a ride with a minimum nausea, this value will be the lowest it can ask for.
    If this value is higher than the maximum, the generator will assume it is a mistake and set it to 0.
    """
    display_name = "Minimum Shop Nausea Requirement"
    range_start = 0
    range_end = 4
    default = 0

class Shop_Maximum_Excitement(Range):
    """If the shop determines you need a ride with a maximum excitement, this value will be the highest it can ask for.
    """
    display_name = "Maximum Shop Excitement Requirement"
    range_start = 0
    range_end = 10
    default = 5

class Shop_Maximum_Intensity(Range):
    """If the shop determines you need a ride with a maximum intensity, this value will be the highest it can ask for.
    """
    display_name = "Maximum Shop Intensity Requirement"
    range_start = 0
    range_end = 7
    default = 5

class Shop_Maximum_Nausea(Range):
    """If the shop determines you need a ride with a maximum nausea, this value will be the highest it can ask for.
    """
    display_name = "Maximum Shop Nausea Requirement"
    range_start = 0
    range_end = 4
    default = 4


class Required_Unique_Rides(Range):
    """Requires specific rides to be built before scenario completion is awarded. These will tend to appear in the later half of the game.
    It's highly recommended to have this set to at least 1!"""
    display_name = "Uniqe Ride Requirement"
    range_start = 0
    range_end = 10
    default = 5

class Park_Rating_Objective(Range):
    """If enabled, choose the minimum park rating needed to beat the scenario."""
    display_name = "Park Rating Objective"
    range_start = 0
    range_end = 999
    default = 800

class Pay_Off_Loan(OpenRCT2OnToggle):
    """Require Loan to be paid off before scenario completion is awarded. Multiple objectives can be enabled!"""
    display_name = "Pay Off Loan"

class Monopoly_Mode(OpenRCT2Toggle):
    """Monopoly Mode is a new objective type. Every unowned tile will be set to purchasable (Or purchasable construction rights for any unowned tile with a grounded path. Elevated paths will not be purchasable). To complete the objective, all tiles on the map must be purchased. Multiple Objectives can be enabled!"""
    display_name = "Monopoly Mode"

class Include_Gamespeed_Items(OpenRCT2OnToggle):
    """If included, the ability to use the speed toggle will be restricted behind an item. 4 items total will be added, each progressively unlocking a faster speed."""
    display_name = "Include Gamespeed Items"

class Furry_Convention_Traps(Range):
    """When found, instantly hosts a furry convention in your park! Adding traps will increase the total number of items in the world."""
    display_name = "Furry Convention Trap"
    range_start = 0
    range_end = 20
    default = 5

class Bathroom_Traps(Range):
    """When found, instantly maxes out the bathroom stat of every guest! Adding traps will increase the total number of items in the world."""
    display_name = "Bathroom Trap"
    range_start = 0
    range_end = 20
    default = 5

class Spam_Traps(Range):
    """When found, spams ads all over the screen! Adding traps will increase the total number of items in the world."""
    display_name = "Spam Trap"
    range_start = 0
    range_end = 20
    default = 5

class Filler(Range):
    """How many extra filler items to add to the mix as a percentage. This will mostly consist of Cash Bonuses"""
    display_name = "Filler"
    range_start = 1
    range_end = 50
    default = 10

class Skips(Range):
    """By default, every game starts with a single skip to ignore a shop requirement. This will add additional skips to 
    be found in the item pool."""
    display_name = "Skips"
    range_start = 0
    range_end = 10
    default = 3
@dataclass
class openRCT2Options(PerGameCommonOptions):
    # generator options
    location_balancing: LocationBalancing
    difficulty: SelectedDifficulty
    shop_minimum_excitement: Shop_Minimum_Excitement
    shop_maximum_excitement: Shop_Maximum_Excitement
    shop_minimum_intensity: Shop_Minimum_Intensity
    shop_maximum_intensity: Shop_Maximum_Intensity
    shop_minimum_nausea: Shop_Minimum_Nausea
    shop_maximum_nausea: Shop_Maximum_Nausea
    ignore_ride_stat_changes: Ignore_Ride_Stat_Changes
    scenario_length: SelectedScenarioLength
    scenario: SelectedScenario
    filler: Filler
    skips: Skips

    # deathlink
    deathlink: DeathLink

    # traps
    furry_convention_traps: Furry_Convention_Traps
    bathroom_traps: Bathroom_Traps
    spam_traps: Spam_Traps

    # in-game options. All Archipelago needs to do with these is pass them to OpenRCT2. The game will handle the rest
    randomization_range: SelectedRandomizationRange
    stat_rerolls: SelectedStatReRolls
    randomize_park_values: Randomize_Park_Values
    visibility: SelectedVisibility
    preferred_intensity: SelectedIntensity
    # include_guest_objective: Include_Guest_Objective
    guest_objective: Guest_Objective
    # include_park_value_objective: Include_Park_Value_Objective
    park_value_objective: Park_Value_Objective
    # include_roller_coaster_objective: Include_Roller_Coaster_Objective
    roller_coaster_objective: Roller_Coaster_Objective
    roller_coaster_excitement: Roller_Coaster_Excitement
    roller_coaster_intensity: Roller_Coaster_Intensity
    roller_coaster_nausea: Roller_Coaster_Nausea
    required_unique_rides: Required_Unique_Rides
    # include_park_rating_objective: Include_Park_Rating_Objective
    park_rating_objective: Park_Rating_Objective
    pay_off_loan: Pay_Off_Loan
    monopoly_mode: Monopoly_Mode
    include_gamespeed_items: Include_Gamespeed_Items
    # park rules. Depending on the option, these may affect which items are created
    difficult_guest_generation: SelectedDifficultGuestGeneration
    difficult_park_rating: SelectedDifficultParkRating
    forbid_high_construction: SelectedForbidHighConstruction
    forbid_landscape_changes: SelectedForbidLandscapeChanges
    forbid_marketing_campaigns: SelectedForbidMarketingCampaigns
    forbid_tree_removal: SelectedForbidTreeRemoval

