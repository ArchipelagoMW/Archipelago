import os
import json
import pkgutil

def load_data_file(*args) -> dict:
    fname = os.path.join("data", *args)
    return json.loads(pkgutil.get_data(__name__, fname).decode())

# ID of first item and location, could be hard-coded but code may be easier
# to read with this as a propery.
base_id = 2000000


item_info = load_data_file("items.json")
location_info = load_data_file("locations.json")


#Lists of Scenarios and the unlockables associated with them
ForestFrontiers = ['Merry Go Round','Suspended Swinging Coaster','Swinging Ship','Twist','Ferris Wheel','Classic Mini Roller Coaster','Information Kiosk','Food Stall','Food Stall','Steeplechase','Spinning Wild Mouse','Food Stall','Shop','Drink Stall','Monorail','Classic Wooden Roller Coaster','Stand Up Roller Coaster','Classic Mini Roller Coaster','Chairlift','Observation Tower','Log Flume','Boat Hire','Spiral Slide','Dodgems','Looping Roller Coaster','Space Rings','Wooden Wild Mouse','Maze','Miniature Railway','Monorail','Wooden Wild Mouse','Dinghy Slide','Toilets','Car Ride','Car Ride','Steeplechase','Haunted House','Food Stall','Food Stall','Food Stall','Car Ride']