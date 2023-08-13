from typing import List, TypedDict


class LocationDict(TypedDict):
    name: str
    id: int
    needsShovel: bool
    purchase: bool

# base_ids from 81000 to 81131

base_id = 81000

location_table: List[LocationDict] = [
    # Original Seashell Locations
    {"name": "Start Beach Seashell", "id": base_id + 1, "needsShovel": False, "purchase": False},
    {"name": "Beach Hut Seashell", "id": base_id + 2, "needsShovel": False, "purchase": False},
    {"name": "Beach Umbrella Seashell", "id": base_id + 3, "needsShovel": False, "purchase": False},
    {"name": "Sid Beach Mound Seashell", "id": base_id + 4, "needsShovel": False, "purchase": False},
    {"name": "Sid Beach Seashell", "id": base_id + 5, "needsShovel": False, "purchase": False},
    {"name": "Shirley's Point Beach Seashell", "id": base_id + 6, "needsShovel": False, "purchase": False},
    {"name": "Shirley's Point Rock Seashell", "id": base_id + 7, "needsShovel": False, "purchase": False},
    {"name": "Visitor's Center Beach Seashell", "id": base_id + 8, "needsShovel": False, "purchase": False},
    {"name": "West River Seashell", "id": base_id + 9, "needsShovel": False, "purchase": False},
    {"name": "West Riverbank Seashell", "id": base_id + 10, "needsShovel": False, "purchase": False},
    {"name": "Stone Tower Riverbank Seashell", "id": base_id + 11, "needsShovel": False, "purchase": False},
    {"name": "North Beach Seashell", "id": base_id + 12, "needsShovel": False, "purchase": False},
    {"name": "North Coast Seashell", "id": base_id + 13, "needsShovel": False, "purchase": False},
    {"name": "Boat Cliff Seashell", "id": base_id + 14, "needsShovel": False, "purchase": False},
    {"name": "Boat Isle Mound Seashell", "id": base_id + 15, "needsShovel": False, "purchase": False},
    {"name": "East Coast Seashell", "id": base_id + 16, "needsShovel": False, "purchase": False},
    {"name": "House North Beach Seashell", "id": base_id + 17, "needsShovel": False, "purchase": False},
    {"name": "Airstream Island North Seashell", "id": base_id + 18, "needsShovel": False, "purchase": False},
    {"name": "Airstream Island South Seashell", "id": base_id + 19, "needsShovel": False, "purchase": False},
    {"name": "Secret Island Beach Seashell", "id": base_id + 20, "needsShovel": False, "purchase": False},
    {"name": "Meteor Lake Seashell", "id": base_id + 126, "needsShovel": False, "purchase": False},
    {"name": "Good Creek Path Seashell", "id": base_id + 127, "needsShovel": False, "purchase": False},

    # Visitor's Center Shop
    {"name": "Visitor's Center Shop Golden Feather 1", "id": base_id + 21, "needsShovel": False, "purchase": True},
    {"name": "Visitor's Center Shop Golden Feather 2", "id": base_id + 22, "needsShovel": False, "purchase": True},
    {"name": "Visitor's Center Shop Hat", "id": base_id + 23, "needsShovel": False, "purchase": True},

    # Tough Bird Salesman
    {"name": "Tough Bird Salesman Golden Feather 1", "id": base_id + 24, "needsShovel": False, "purchase": True},
    {"name": "Tough Bird Salesman Golden Feather 2", "id": base_id + 25, "needsShovel": False, "purchase": True},
    {"name": "Tough Bird Salesman Golden Feather 3", "id": base_id + 26, "needsShovel": False, "purchase": True},
    {"name": "Tough Bird Salesman Golden Feather 4", "id": base_id + 27, "needsShovel": False, "purchase": True},
    {"name": "Tough Bird Salesman (400 Coins)", "id": base_id + 28, "needsShovel": False, "purchase": True},

    # Beachstickball
    {"name": "Beachstickball (10 Hits)", "id": base_id + 29, "needsShovel": False, "purchase": False},
    {"name": "Beachstickball (20 Hits)", "id": base_id + 30, "needsShovel": False, "purchase": False},
    {"name": "Beachstickball (30 Hits)", "id": base_id + 31, "needsShovel": False, "purchase": False},

    # Misc Item Locations
    {"name": "Shovel Kid Trade", "id": base_id + 32, "needsShovel": False, "purchase": False},
    {"name": "Compass Guy", "id": base_id + 33, "needsShovel": False, "purchase": False},
    {"name": "Hawk Peak Bucket Rock", "id": base_id + 34, "needsShovel": False, "purchase": False},
    {"name": "Orange Islands Bucket Rock", "id": base_id + 35, "needsShovel": False, "purchase": False},
    {"name": "Bill the Walrus Fisherman", "id": base_id + 36, "needsShovel": False, "purchase": False},
    {"name": "Catch 3 Fish Reward", "id": base_id + 37, "needsShovel": False, "purchase": False},
    {"name": "Catch All Fish Reward", "id": base_id + 38, "needsShovel": False, "purchase": False},
    {"name": "Permit Guy Bribe", "id": base_id + 39, "needsShovel": False, "purchase": False},
    {"name": "Catch Fish with Permit", "id": base_id + 129, "needsShovel": False, "purchase": False},
    {"name": "Return Camping Permit", "id": base_id + 130, "needsShovel": False, "purchase": False},

    # Original Pickaxe Locations
    {"name": "Blocked Mine Pickaxe 1", "id": base_id + 40, "needsShovel": False, "purchase": False},
    {"name": "Blocked Mine Pickaxe 2", "id": base_id + 41, "needsShovel": False, "purchase": False},
    {"name": "Blocked Mine Pickaxe 3", "id": base_id + 42, "needsShovel": False, "purchase": False},

    # Original Toy Shovel Locations
    {"name": "Blackwood Trail Lookout Toy Shovel", "id": base_id + 43, "needsShovel": False, "purchase": False},
    {"name": "Shirley's Point Beach Toy Shovel", "id": base_id + 44, "needsShovel": False, "purchase": False},
    {"name": "Visitor's Center Beach Toy Shovel", "id": base_id + 45, "needsShovel": False, "purchase": False},
    {"name": "Blackwood Trail Rock Toy Shovel", "id": base_id + 46, "needsShovel": False, "purchase": False},
    {"name": "Beach Hut Cliff Toy Shovel", "id": base_id + 128, "needsShovel": False, "purchase": False},

    # Original Stick Locations
    {"name": "Secret Island Beach Trail Stick", "id": base_id + 47, "needsShovel": False, "purchase": False},
    {"name": "Below Lighthouse Walkway Stick", "id": base_id + 48, "needsShovel": False, "purchase": False},
    {"name": "Beach Hut Rocky Pool Sand Stick", "id": base_id + 49, "needsShovel": False, "purchase": False},
    {"name": "Cliff Overlooking West River Waterfall Stick", "id": base_id + 50, "needsShovel": False, "purchase": False},
    {"name": "Trail to Tough Bird Salesman Stick", "id": base_id + 51, "needsShovel": False, "purchase": False},
    {"name": "North Beach Stick", "id": base_id + 52, "needsShovel": False, "purchase": False},
    {"name": "Beachstickball Court Stick", "id": base_id + 53, "needsShovel": False, "purchase": False},
    {"name": "Stick Under Sid Beach Umbrella", "id": base_id + 54, "needsShovel": False, "purchase": False},

    # Boating
    {"name": "Boat Rental", "id": base_id + 55, "needsShovel": False, "purchase": True},
    {"name": "Boat Challenge Reward", "id": base_id + 56, "needsShovel": False, "purchase": False},

    # Original Map Locations
    {"name": "Outlook Point Dog Gift", "id": base_id + 57, "needsShovel": False, "purchase": False},

    # Original Clothes Locations
    {"name": "Collect 15 Seashells", "id": base_id + 58, "needsShovel": False, "purchase": False},
    {"name": "Taylor the Turtle Headband Gift", "id": base_id + 59, "needsShovel": False, "purchase": False},
    {"name": "Sue the Rabbit Shoes Reward", "id": base_id + 60, "needsShovel": False, "purchase": False},
    {"name": "Purchase Sunhat", "id": base_id + 61, "needsShovel": False, "purchase": True},

    # Original Golden Feather Locations
    {"name": "Blackwood Forest Golden Feather", "id": base_id + 62, "needsShovel": False, "purchase": False},
    {"name": "Ranger May Shell Necklace Golden Feather", "id": base_id + 63, "needsShovel": False, "purchase": False},
    {"name": "Sand Castle Golden Feather", "id": base_id + 64, "needsShovel": False, "purchase": False},
    {"name": "Artist Golden Feather", "id": base_id + 65, "needsShovel": False, "purchase": False},
    {"name": "Visitor Camp Rock Golden Feather", "id": base_id + 66, "needsShovel": False, "purchase": False},
    {"name": "Outlook Cliff Golden Feather", "id": base_id + 67, "needsShovel": False, "purchase": False},
    {"name": "Meteor Lake Cliff Golden Feather", "id": base_id + 68, "needsShovel": False, "purchase": False},

    # Original Silver Feather Locations
    {"name": "Secret Island Peak", "id": base_id + 69, "needsShovel": False, "purchase": False},
    {"name": "Wristwatch Trade", "id": base_id + 70, "needsShovel": False, "purchase": False},

    # Golden Chests
    {"name": "Lighthouse Golden Chest", "id": base_id + 71, "needsShovel": False, "purchase": False},
    {"name": "Outlook Golden Chest", "id": base_id + 72, "needsShovel": False, "purchase": False},
    {"name": "Stone Tower Golden Chest", "id": base_id + 73, "needsShovel": False, "purchase": False},
    {"name": "North Cliff Golden Chest", "id": base_id + 74, "needsShovel": False, "purchase": False},

    # Chests
    {"name": "Blackwood Cliff Chest", "id": base_id + 75, "needsShovel": False, "purchase": False}, 
    {"name": "White Coast Trail Chest", "id": base_id + 76, "needsShovel": False, "purchase": False}, 
    {"name": "Sid Beach Chest", "id": base_id + 77, "needsShovel": False, "purchase": False}, 
    {"name": "Sid Beach Buried Treasure Chest", "id": base_id + 78, "needsShovel": True, "purchase": False}, 
    {"name": "Sid Beach Cliff Chest", "id": base_id + 79, "needsShovel": False, "purchase": False}, 
    {"name": "Visitor's Center Buried Chest", "id": base_id + 80, "needsShovel": True, "purchase": False}, 
    {"name": "Visitor's Center Hidden Chest", "id": base_id + 81, "needsShovel": False, "purchase": False}, 
    {"name": "Shirley's Point Chest", "id": base_id + 82, "needsShovel": False, "purchase": False}, 
    {"name": "Caravan Cliff Chest", "id": base_id + 83, "needsShovel": False, "purchase": False}, 
    {"name": "Caravan Arch Chest", "id": base_id + 84, "needsShovel": False, "purchase": False}, 
    {"name": "King Buried Treasure Chest", "id": base_id + 85, "needsShovel": True, "purchase": False}, 
    {"name": "Good Creek Path Buried Chest", "id": base_id + 86, "needsShovel": True, "purchase": False}, 
    {"name": "Good Creek Path West Chest", "id": base_id + 87, "needsShovel": False, "purchase": False}, 
    {"name": "Good Creek Path East Chest", "id": base_id + 88, "needsShovel": False, "purchase": False}, 
    {"name": "West Waterfall Chest", "id": base_id + 89, "needsShovel": False, "purchase": False}, 
    {"name": "Stone Tower West Cliff Chest", "id": base_id + 90, "needsShovel": False, "purchase": False}, 
    {"name": "Bucket Path Chest", "id": base_id + 91, "needsShovel": False, "purchase": False}, 
    {"name": "Bucket Cliff Chest", "id": base_id + 92, "needsShovel": False, "purchase": False}, 
    {"name": "In Her Shadow Buried Treasure Chest", "id": base_id + 93, "needsShovel": True, "purchase": False}, 
    {"name": "Meteor Lake Buried Chest", "id": base_id + 94, "needsShovel": True, "purchase": False}, 
    {"name": "Meteor Lake Chest", "id": base_id + 95, "needsShovel": False, "purchase": False}, 
    {"name": "House North Beach Chest", "id": base_id + 96, "needsShovel": False, "purchase": False}, 
    {"name": "East Coast Chest", "id": base_id + 97, "needsShovel": False, "purchase": False}, 
    {"name": "Fisherman's Boat Chest 1", "id": base_id + 99, "needsShovel": False, "purchase": False}, 
    {"name": "Fisherman's Boat Chest 2", "id": base_id + 100, "needsShovel": False, "purchase": False}, 
    {"name": "Airstream Island Chest", "id": base_id + 101, "needsShovel": False, "purchase": False}, 
    {"name": "West River Waterfall Head Chest", "id": base_id + 102, "needsShovel": False, "purchase": False}, 
    {"name": "Old Building Chest", "id": base_id + 103, "needsShovel": False, "purchase": False}, 
    {"name": "Old Building West Chest", "id": base_id + 104, "needsShovel": False, "purchase": False}, 
    {"name": "Old Building East Chest", "id": base_id + 105, "needsShovel": False, "purchase": False}, 
    {"name": "Hawk Peak West Chest", "id": base_id + 106, "needsShovel": False, "purchase": False}, 
    {"name": "Hawk Peak East Buried Chest", "id": base_id + 107, "needsShovel": True, "purchase": False}, 
    {"name": "Hawk Peak Northeast Chest", "id": base_id + 108, "needsShovel": False, "purchase": False}, 
    {"name": "Northern East Coast Chest", "id": base_id + 109, "needsShovel": False, "purchase": False}, 
    {"name": "North Coast Chest", "id": base_id + 110, "needsShovel": False, "purchase": False}, 
    {"name": "North Coast Buried Chest", "id": base_id + 111, "needsShovel": True, "purchase": False}, 
    {"name": "Small South Island Buried Chest", "id": base_id + 112, "needsShovel": True, "purchase": False}, 
    {"name": "Secret Island Bottom Chest", "id": base_id + 113, "needsShovel": False, "purchase": False}, 
    {"name": "Secret Island Middle Chest", "id": base_id + 114, "needsShovel": False, "purchase": False}, 
    {"name": "Sunhat Island Buried Chest", "id": base_id + 115, "needsShovel": True, "purchase": False}, 
    {"name": "Orange Islands South Buried Chest", "id": base_id + 116, "needsShovel": True, "purchase": False}, 
    {"name": "Orange Islands West Chest", "id": base_id + 117, "needsShovel": False, "purchase": False}, 
    {"name": "Orange Islands North Buried Chest", "id": base_id + 118, "needsShovel": True, "purchase": False}, 
    {"name": "Orange Islands East Chest", "id": base_id + 119, "needsShovel": False, "purchase": False}, 
    {"name": "Orange Islands South Hidden Chest", "id": base_id + 120, "needsShovel": False, "purchase": False}, 
    {"name": "A Stormy View Buried Treasure Chest", "id": base_id + 121, "needsShovel": True, "purchase": False}, 
    {"name": "Orange Islands Ruins Buried Chest", "id": base_id + 122, "needsShovel": True, "purchase": False}, 

    # Race Rewards
    {"name": "Lighthouse Race Reward", "id": base_id + 123, "needsShovel": False, "purchase": False},
    {"name": "Old Building Race Reward", "id": base_id + 124, "needsShovel": False, "purchase": False},
    {"name": "Hawk Peak Race Reward", "id": base_id + 125, "needsShovel": False, "purchase": False},
    {"name": "Lose Race Gift", "id": base_id + 131, "needsShovel": False, "purchase": False},
]