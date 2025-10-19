from BaseClasses import Item
import copy
from .Constants import Scenario_Items
from .data.item_info import item_info
from .Options import *

def get_dlc_items():
    """Get all DLC items from item_info"""
    dlc_items = []
    
    # Taste of Adventures DLC items
    if "taste_of_adventures_dlc" in item_info:
        for category in item_info["taste_of_adventures_dlc"]:
            dlc_items.extend(item_info["taste_of_adventures_dlc"][category])
    
    # Booms and Blooms DLC items
    if "booms_and_blooms_dlc" in item_info:
        for category in item_info["booms_and_blooms_dlc"]:
            dlc_items.extend(item_info["booms_and_blooms_dlc"][category])
    
    return dlc_items

def filter_items_by_dlc(items, dlc_value):
    """Filter out DLC items based on DLC selection"""
    dlc_items = get_dlc_items()
    
    # If no DLCs are selected (value 0), remove all DLC items
    if dlc_value == 0:
        return [item for item in items if item not in dlc_items]
    
    # If all DLCs are selected (value 1), keep all items
    if dlc_value == 1:
        return items
    
    # Filter based on specific DLC selection
    taste_of_adventures_items = []
    booms_and_blooms_items = []
    filtered_items = items[:]
    
    # Get items for each DLC
    if "taste_of_adventures_dlc" in item_info:
        for category in item_info["taste_of_adventures_dlc"]:
            taste_of_adventures_items.extend(item_info["taste_of_adventures_dlc"][category])
    
    if "booms_and_blooms_dlc" in item_info:
        for category in item_info["booms_and_blooms_dlc"]:
            booms_and_blooms_items.extend(item_info["booms_and_blooms_dlc"][category])

    if dlc_value != DLC.taste_of_adventures.value:
        filtered_items = [item for item in filtered_items if item not in taste_of_adventures_items]

    if dlc_value != DLC.booms_and_blooms.value:
        filtered_items = [item for item in filtered_items if item not in booms_and_blooms_items]
    
    return filtered_items

class ParkitectItem(Item):
    game: str = "Parkitect"

def set_parkitect_items(world):
    parkitect_items = copy.deepcopy(Scenario_Items[world.options.scenario.value]) # Attractions and Shops!
    
    # Filter out DLC items based on DLC selection
    parkitect_items = filter_items_by_dlc(parkitect_items, world.options.dlc.value)

    for each in range(world.options.trap_player_money.value):
        parkitect_items.append("Player Money Trap")

    for each in range(world.options.trap_attraction_breakdown.value):
        parkitect_items.append("Attraction Breakdown Trap")

    for each in range(world.options.trap_attraction_voucher.value):
        parkitect_items.append("Attraction Voucher Trap")

    for each in range(world.options.trap_shops_ingredient.value):
        parkitect_items.append("Shop Ingredients Trap")

    for each in range(world.options.trap_shops_clean.value):
        parkitect_items.append("Shop Cleaning Trap")

    for each in range(world.options.trap_shops_voucher.value):
        parkitect_items.append("Shop Voucher Trap")

    for each in range(world.options.trap_employees_hiring.value):
        parkitect_items.append("Employee Hiring Trap")

    for each in range(world.options.trap_employees_training.value):
        parkitect_items.append("Employee Training Trap")

    for each in range(world.options.trap_employees_tired.value):
        parkitect_items.append("Employee Tiredness Trap")

    for each in range(world.options.trap_weather.value):
        parkitect_items.append("Weather Rainy Trap")
        parkitect_items.append("Weather Stormy Trap")
        parkitect_items.append("Weather Cloudy Trap")
        parkitect_items.append("Weather Sunny Trap")

    for each in range(world.options.trap_guests_spawn.value):
        parkitect_items.append("Guest Spawn Trap")

    for each in range(world.options.trap_guests_kill.value):
        parkitect_items.append("Guest Kill Trap")

    for each in range(world.options.trap_guests_money.value):
        parkitect_items.append("Guest Money Trap")

    for each in range(world.options.trap_guests_hunger.value):
        parkitect_items.append("Guest Hunger Trap")

    for each in range(world.options.trap_guests_thirst.value):
        parkitect_items.append("Guest Thirst Trap")

    for each in range(world.options.trap_guests_bathroom.value):
        parkitect_items.append("Guest Bathroom Trap")

    for each in range(world.options.trap_guests_vomit.value):
        parkitect_items.append("Guest Vomiting Trap")

    for each in range(world.options.trap_guests_happiness.value):
        parkitect_items.append("Guest Happiness Trap")

    for each in range(world.options.trap_guests_tiredness.value):
        parkitect_items.append("Guest Tiredness Trap")

    for each in range(world.options.trap_guests_vandal.value):
        parkitect_items.append("Guest Vandal Trap")

    for each in range(world.options.challenge_skips.value):
        parkitect_items.append("Skip")

    if (world.options.progressive_speedups.value == 1):
        for each in range(6):
            parkitect_items.append("Progressive Speed")

    items = item_info["Rides"] + item_info["Shops"]
    
    # Filter items based on DLC selection for starting ride selection
    items = filter_items_by_dlc(items, world.options.dlc.value)

    candidates = [item for item in parkitect_items if item in items]
    candidate = world.random.choice(candidates)
    starter = candidate
    parkitect_items.remove(candidate)

    return parkitect_items, starter