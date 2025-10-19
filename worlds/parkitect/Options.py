from enum import IntEnum
from Options import Range, Choice, PerGameCommonOptions, OptionGroup, OptionCounter
from dataclasses import dataclass

# Helpers
class Scenario(IntEnum):
    lakeside_gardens = 0
    dusty_ridge_ranch = 1

class Difficulty(IntEnum):
    easy = 0
    medium = 1
    hard = 2
    extreme = 3

class DLC(IntEnum):
    taste_of_adventures = 2
    booms_and_blooms = 3

# Selectable options
class SelectedScenario(Choice):
    """
    Choose which scenario you'd like to play!
    """
    display_name = "Scenario"
    option_lakeside_gardens = Scenario.lakeside_gardens.value
    option_dusty_ridge_ranch = Scenario.dusty_ridge_ranch.value

class SelectedDifficulty(Choice):
    """
    Choose a difficulty for the randomization. This will make Checks harder to complete.
    """
    display_name = "Difficulty"
    option_easy = Difficulty.easy.value
    option_medium = Difficulty.medium.value
    option_hard = Difficulty.hard.value
    option_extreme = Difficulty.extreme.value
    default = Difficulty.medium.value

class SelectedDLC(Choice):
    """
    DLC's have extra rides and shops.
    """
    display_name = "DLCs"
    option_none = 0
    option_all = 1
    option_taste_of_adventures = DLC.taste_of_adventures.value
    option_booms_and_blooms = DLC.booms_and_blooms.value
    default = 0

# Goals
class GoalGuests(Range): # GuestsInParkGoal
    """
    Choose how many guests are required to win the scenario
    """
    display_name = "Guest Goal"
    range_start = 1
    range_end = 5000
    default = 1000

class GoalMoney(Range): # MoneyGoal
    """
    Choose how much money is required to win the scenario
    """
    display_name = "Money Goal"
    range_start = 50000
    range_end = 500000
    default = 100000

class GoalCoasters(Range): # CoastersGoal
    """
    Choose how many coasters are required to win the scenario
    """
    display_name = "Roller Coaster Goal"
    range_start = 0
    range_end = 12
    default = 4

class GoalCoasterExcitement(Range):
    """
    Select the minimum excitement 😀 for a coaster to count towards your objective. 0 will disable a minimum excitement rating.
    """
    display_name = "Excitement Rating"
    range_start = 0
    range_end = 80
    default = 50

class GoalCoasterIntensity(Range):
    """
    Select the minimum intensity 😬 for a coaster to count towards your objective. 0 will disable a minimum intensity rating.
    """
    display_name = "Intensity Rating"
    default = 50
    range_start = 0
    range_end = 80

class GoalRideProfit(Range): # RideProfitGoal
    """
    Choose how much profit you need from all rides to win the scenario
    """
    display_name = "Ride Profit Goal"
    default = 500
    range_start = 0
    range_end = 10000

class GoalParkTickets(Range): # ParkTicketsGoal
    """
    Choose how many park tickets has to be sold to win the scenario
    """
    display_name = "Park Tickets Goal"
    default = 0
    range_start = 0
    range_end = 20000

class GoalShops(Range): # ShopsCountGoal
    """
    Choose how many shops are required to win the scenario
    """
    display_name = "Shops Goal"
    default = 15
    range_start = 0
    range_end = 100

class GoalShopProfit(Range): # ShopProfitGoal
    """
    Choose how much profit you need from shops to win the scenario
    """
    display_name = "Shop Profit Goal"
    default = 500
    range_start = 0
    range_end = 5000

# Challenge
class ChallengeMaximumExcitement(Range):
    """
    If a challenge determines you need a rollercoaster with a maximum excitement, this value will be the lowest it can ask for.
    If this value is higher than the maximum, the generator will assume it is a mistake and set it to 0.
    """
    display_name = "Challenge: Maximum Ride Excitement"
    range_start = 0
    range_end = 80
    default = 0

class ChallengeMaximumIntensity(Range):
    """
    If a challenge determines you need a rollercoaster with a maximum intensity, this value will be the lowest it can ask for.
    If this value is higher than the maximum, the generator will assume it is a mistake and set it to 0.
    """
    display_name = "Challenge: Maximum Ride Intensity"
    range_start = 0
    range_end = 80
    default = 0

class ChallengeMaximumNausea(Range):
    """
    If a challenge determines you need a rollercoaster with a maximum nausea, this value will be the lowest it can ask for.
    If this value is higher than the maximum, the generator will assume it is a mistake and set it to 0.
    """
    display_name = "Challenge: Maximum Ride Nausea"
    range_start = 0
    range_end = 70
    default = 0

class ChallengeMaximumSatisfaction(Range):
    """
    If a challenge determines you need a rollercoaster with a maximum satisfaction, this value will be the lowest it can ask for.
    If this value is higher than the maximum, the generator will assume it is a mistake and set it to 0.
    """
    display_name = "Challenge: Maximum Ride Satisfaction"
    range_start = 0
    range_end = 80
    default = 0

class ChallengeCustomers(Range):
    """
    If a challenge determines you need a ride or shop with a maximum amount of customers, this value will be the lowest it can ask for.
    If this value is higher than the maximum, the generator will assume it is a mistake and set it to 0.
    """
    display_name = "Challenge: Maximum Customers"
    range_start = 0
    range_end = 1000
    default = 0

class ChallengeMaximumRideRevenue(Range):
    """
    If a challenge determines you need a rollercoaster with a total revenue, this value will be the lowest it can ask for.
    If this value is higher than the maximum, the generator will assume it is a mistake and set it to 0.
    """
    display_name = "Challenge: Total Ride Revenue"
    range_start = 0
    range_end = 5000
    default = 0

class ChallengeMaximumShopRevenue(Range):
    """
    If a challenge determines you need a shop with a total revenue, this value will be the lowest it can ask for.
    If this value is higher than the maximum, the generator will assume it is a mistake and set it to 0.
    """
    display_name = "Challenge: Total Shop Revenue"
    range_start = 0
    range_end = 2500
    default = 0

class ChallengeSkips(Range):
    """
    by default, every game start with 5 skips to, well, skip a challenge. This will add additional skips to be found in the item pool.
    """
    display_name = "Skips"
    range_start = 0
    range_end = 15
    default = 5

# Traps
# Traps - Player
class TrapPlayerMoney(Range):
    """
    When found, little Money is added to your Bank Account! Adding traps will increase the total number of items in the world.
    """
    display_name = "Player Money Trap"
    range_start = 0
    range_end = 20
    default = 5

# Traps - Attraction
class TrapAttractionBreakdown(Range):
    """
    When found, instantly break specific amount of Attraction/s! Adding traps will increase the total number of items in the world.
    """
    display_name = "Attraction Breakdown Trap"
    range_start = 0
    range_end = 20
    default = 5

class TrapAttractionVoucher(Range):
    """
    When found, few Guests will receive an Attraction Voucher in your Park! Adding traps will increase the total number of items in the world.
    """
    display_name = "Attraction Voucher Trap"
    range_start = 0
    range_end = 20
    default = 5

# Traps - Shop
class TrapShopsIngredient(Range):
    """
    When found, ProductShops ingredients needs to be restocked! Adding traps will increase the total number of items in the world.
    """
    display_name = "Shop Ingredients Trap"
    range_start = 0
    range_end = 20
    default = 5

class TrapShopsClean(Range):
    """
    When found, Shops needs to be cleaned! Adding traps will increase the total number of items in the world.
    """
    display_name = "Shop Cleaning Trap"
    range_start = 0
    range_end = 20
    default = 5

class TrapShopsVoucher(Range):
    """
    When found, some Guests will receive a Shop Voucher in your Park! Adding traps will increase the total number of items in the world.
    """
    display_name = "Shop Voucher Trap"
    range_start = 0
    range_end = 20
    default = 5

# Traps - Employee
class TrapEmployeesHiring(Range):
    """
    When found, instantly Hire randomly picked Employees in your park! Adding traps will increase the total number of items in the world.
    The difficulty decides how many of them will be hired!
    """
    display_name = "Employee Hiring Trap"
    range_start = 0
    range_end = 20
    default = 10

class TrapEmployeesTraining(Range):
    """
    When found, instantly send randomly picked Employees to the training room! Adding traps will increase the total number of items in the world.
    The difficulty decides how many of them will be training!
    """
    display_name = "Employee Training Trap"
    range_start = 0
    range_end = 20
    default = 5

class TrapEmployeesTired(Range):
    """
    When found, instantly raise Employes tiredness! Adding traps will increase the total number of items in the world.
    The difficulty decides how many of them will be tired!
    """
    display_name = "Employee Tiredness Trap"
    range_start = 0
    range_end = 20
    default = 5

# Traps - Weather
class TrapWeather(Range):
    """
    When found, Rainy, Cloudy, Sunny or Stormy Weather is comming over! Adding traps will increase the total number of items in the world.
    """
    display_name = "Weather Trap"
    range_start = 0
    range_end = 30
    default = 10

# Traps - Guests
class TrapGuestsSpawn(Range):
    """
    When found, a wave of new Guests appears in your Scenario! Adding traps will increase the total number of items in the world.
    """
    display_name = "Guest Spawn Trap"
    range_start = 0
    range_end = 30
    default = 10

class TrapGuestsKill(Range):
    """
    When found, few Guests will disappears in your Scenario! Adding traps will increase the total number of items in the world.
    """
    display_name = "Guest Kill Trap"
    range_start = 0
    range_end = 15
    default = 5

class TrapGuestsMoney(Range):
    """
    When found, few Guests will receive or lose their Money in your Park! Adding traps will increase the total number of items in the world.
    """
    display_name = "Guest Money Trap"
    range_start = 0
    range_end = 15
    default = 5

class TrapGuestsMoneyFlux(Choice):
    f"""
    (If Guest Money Trap is enabled!)
    Decides if the Guest receive or/and lose money.
    """
    display_name = "Guest Money Flux"
    default = 2
    option_adding = 0
    option_removing = 1
    option_mixed = 2

class TrapGuestsHunger(Range):
    """
    When found, Guests will be hungry! Adding traps will increase the total number of items in the world.
    """
    display_name = "Guest Hunger Trap"
    range_start = 0
    range_end = 15
    default = 5

class TrapGuestsThirst(Range):
    """
    When found, Guests will be thirsty! Adding traps will increase the total number of items in the world.
    """
    display_name = "Guest Thirst Trap"
    range_start = 0
    range_end = 15
    default = 5

class TrapGuestsBathroom(Range):
    """
    When found, alot of Guests will be running to the next toilet! Adding traps will increase the total number of items in the world.
    """
    display_name = "Guest Bathroom Trap"
    range_start = 0
    range_end = 15
    default = 5

class TrapGuestsVomit(Range):
    """
    When found, Too many Guests will try to find the next First-Aid room or Trashcan! Adding traps will increase the total number of items in the world.
    """
    display_name = "Guest Vomiting Trap"
    range_start = 0
    range_end = 15
    default = 5

class TrapGuestsHappiness(Range):
    """
    When found, few Guests will just be happy! Adding traps will increase the total number of items in the world.
    """
    display_name = "Guest Happiness Trap"
    range_start = 0
    range_end = 15
    default = 5

class TrapGuestsTiredness(Range):
    """
    When found, few Guests will just be tired! Adding traps will increase the total number of items in the world.
    """
    display_name = "Guest Tiredness Trap"
    range_start = 0
    range_end = 15
    default = 5

class TrapGuestsVandal(Range):
    """
    When found, few Guests will be a Vandal! Adding traps will increase the total number of items in the world.
    The difficulty decides how many Guests vandalising your Park!
    """
    display_name = "Guest Vandal Trap"
    range_start = 0
    range_end = 30
    default = 10
    
class SelectedProgressiveSpeedups(Choice):
    """
    If included, the ability to use the speedups at the window will be restricted behind an item. 6 items total will be added, each progressively unlocking a faster speed.
    Game Speedups (0x, 1x, 2x, 3x) are always usable.
    """
    display_name = "Progressive Speedups"
    option_no = 0
    option_yes = 1
    default = 0

parkitect_option_groups = [
    OptionGroup("Scenario Options", [
        SelectedScenario,
        SelectedDifficulty,
        SelectedDLC
    ]),
    OptionGroup("Goal Options", [
        GoalGuests,
        GoalMoney,
        GoalCoasters,
        GoalCoasterExcitement,
        GoalCoasterIntensity,
        GoalRideProfit,
        GoalParkTickets,
        GoalShops,
        GoalShopProfit
    ]),
    OptionGroup("Traps", [
        TrapPlayerMoney,
        TrapAttractionBreakdown,
        TrapAttractionVoucher,
        TrapShopsIngredient,
        TrapShopsClean,
        TrapShopsVoucher,
        TrapEmployeesHiring,
        TrapEmployeesTraining,
        TrapEmployeesTired,
        TrapWeather,
        TrapGuestsSpawn,
        TrapGuestsKill,
        TrapGuestsMoney,
        TrapGuestsHunger,
        TrapGuestsThirst,
        TrapGuestsBathroom,
        TrapGuestsVomit,
        TrapGuestsHappiness,
        TrapGuestsTiredness,
        TrapGuestsVandal
    ]),
    OptionGroup("Challenges", [
        ChallengeCustomers,
        ChallengeMaximumExcitement,
        ChallengeMaximumIntensity,
        ChallengeMaximumNausea,
        ChallengeMaximumSatisfaction,
        ChallengeMaximumRideRevenue,
        ChallengeMaximumShopRevenue,
        ChallengeSkips,
    ]),
    OptionGroup("Rules", [
        TrapGuestsMoneyFlux,
        SelectedProgressiveSpeedups
    ]),
]

@dataclass
class ParkitectOptions(PerGameCommonOptions):
    difficulty: SelectedDifficulty
    scenario: SelectedScenario
    dlc: SelectedDLC

    # traps
    trap_player_money: TrapPlayerMoney
    trap_attraction_breakdown: TrapAttractionBreakdown
    trap_attraction_voucher: TrapAttractionVoucher
    trap_shops_ingredient: TrapShopsIngredient
    trap_shops_clean: TrapShopsClean
    trap_shops_voucher: TrapShopsVoucher
    trap_employees_hiring: TrapEmployeesHiring
    trap_employees_training: TrapEmployeesTraining
    trap_employees_tired: TrapEmployeesTired
    trap_weather: TrapWeather
    trap_guests_spawn: TrapGuestsSpawn
    trap_guests_kill: TrapGuestsKill
    trap_guests_money: TrapGuestsMoney
    trap_guests_hunger: TrapGuestsHunger
    trap_guests_thirst: TrapGuestsThirst
    trap_guests_bathroom: TrapGuestsBathroom
    trap_guests_vomit: TrapGuestsVomit
    trap_guests_happiness: TrapGuestsHappiness
    trap_guests_tiredness: TrapGuestsTiredness
    trap_guests_vandal: TrapGuestsVandal

    # Parkitect Mod rules.
    guests_money_flux: TrapGuestsMoneyFlux
    progressive_speedups: SelectedProgressiveSpeedups

    # challenges
    challenge_customers: ChallengeCustomers
    challenge_maximum_excitement: ChallengeMaximumExcitement
    challenge_maximum_intensity: ChallengeMaximumIntensity
    challenge_maximum_nausea: ChallengeMaximumNausea
    challenge_maximum_satisfaction: ChallengeMaximumSatisfaction
    challenge_maximum_ride_revenue: ChallengeMaximumRideRevenue
    challenge_maximum_shop_revenue: ChallengeMaximumShopRevenue
    challenge_skips: ChallengeSkips
    
    # the obvious
    goal_guests: GoalGuests
    goal_money: GoalMoney
    goal_coasters: GoalCoasters
    goal_coaster_excitement: GoalCoasterExcitement
    goal_coaster_intensity: GoalCoasterIntensity
    goal_ride_profit: GoalRideProfit
    goal_park_tickets: GoalParkTickets
    goal_shops: GoalShops
    goal_shop_profit: GoalShopProfit