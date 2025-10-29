from BaseClasses import Item
import copy
from .Constants import Scenario_Items
from .data.item_info import item_info
from .Options import *

def get_dlc_items():
    """Get all DLC items from item_info."""
    dlc_items = {}

    if "taste_of_adventures_dlc" in item_info:
        dlc_items["taste_of_adventures"] = [
            item for category in item_info["taste_of_adventures_dlc"]
            for item in item_info["taste_of_adventures_dlc"][category]
        ]
    
    if "booms_and_blooms_dlc" in item_info:
        dlc_items["booms_and_blooms"] = [
            item for category in item_info["booms_and_blooms_dlc"]
            for item in item_info["booms_and_blooms_dlc"][category]
        ]
    
    if "dinos_and_dynasties_dlc" in item_info:
        dlc_items["dinos_and_dynasties"] = [
            item for category in item_info["dinos_and_dynasties_dlc"]
            for item in item_info["dinos_and_dynasties_dlc"][category]
        ]

    return dlc_items

def filter_items_by_dlc(items, dlc1_value, dlc2_value, dlc3_value):
    """Filter items based on which DLCs are active."""
    dlc_items = get_dlc_items()
    filtered_items = items[:]

    # Remove DLC1 items if not selected
    if not dlc1_value and "taste_of_adventures" in dlc_items:
        filtered_items = [
            item for item in filtered_items
            if item not in dlc_items["taste_of_adventures"]
        ]

    # Remove DLC2 items if not selected
    if not dlc2_value and "booms_and_blooms" in dlc_items:
        filtered_items = [
            item for item in filtered_items
            if item not in dlc_items["booms_and_blooms"]
        ]

    # Remove DLC3 items if not selected
    if not dlc3_value and "dinos_and_dynasties" in dlc_items:
        filtered_items = [
            item for item in filtered_items
            if item not in dlc_items["dinos_and_dynasties"]
        ]

    return filtered_items

class ParkitectItem(Item):
    game: str = "Parkitect"

def set_parkitect_items(world):
    parkitect_items = copy.deepcopy(Scenario_Items[world.options.scenario.value])
    
    # Filter out DLC items based on DLC selection
    parkitect_items = filter_items_by_dlc(parkitect_items, world.options.dlc1.value, world.options.dlc2.value, world.options.dlc3.value)

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
    items = filter_items_by_dlc(items, world.options.dlc1.value, world.options.dlc2.value, world.options.dlc3.value)

    candidates = [item for item in parkitect_items if item in items]
    candidate = world.random.choice(candidates)
    starter = candidate
    parkitect_items.remove(candidate)

    return parkitect_items, starter