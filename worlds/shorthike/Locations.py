from typing import List, TypedDict


class LocationDict(TypedDict):
    name: str
    id: int
    needsShovel: bool
    purchase: bool

# IDs from 81000 to 81131

ID = 81000

location_table: List[LocationDict] = [
    # Original Seashell Locations
    {"name": "Start Beach Seashell", "id": ID + 1, "needsShovel": False, "purchase": False},
    {"name": "Beach Hut Seashell", "id": ID + 2, "needsShovel": False, "purchase": False},
    {"name": "Beach Umbrella Seashell", "id": ID + 3, "needsShovel": False, "purchase": False},
    {"name": "Sid Beach Mound Seashell", "id": ID + 4, "needsShovel": False, "purchase": False},
    {"name": "Sid Beach Seashell", "id": ID + 5, "needsShovel": False, "purchase": False},
    {"name": "Shirley's Point Beach Seashell", "id": ID + 6, "needsShovel": False, "purchase": False},
    {"name": "Shirley's Point Rock Seashell", "id": ID + 7, "needsShovel": False, "purchase": False},
    {"name": "Visitor's Center Beach Seashell", "id": ID + 8, "needsShovel": False, "purchase": False},
    {"name": "West River Seashell", "id": ID + 9, "needsShovel": False, "purchase": False},
    {"name": "West Riverbank Seashell", "id": ID + 10, "needsShovel": False, "purchase": False},
    {"name": "Stone Tower Riverbank Seashell", "id": ID + 11, "needsShovel": False, "purchase": False},
    {"name": "North Beach Seashell", "id": ID + 12, "needsShovel": False, "purchase": False},
    {"name": "North Coast Seashell", "id": ID + 13, "needsShovel": False, "purchase": False},
    {"name": "Boat Cliff Seashell", "id": ID + 14, "needsShovel": False, "purchase": False},
    {"name": "Boat Isle Mound Seashell", "id": ID + 15, "needsShovel": False, "purchase": False},
    {"name": "East Coast Seashell", "id": ID + 16, "needsShovel": False, "purchase": False},
    {"name": "House North Beach Seashell", "id": ID + 17, "needsShovel": False, "purchase": False},
    {"name": "Airstream Island North Seashell", "id": ID + 18, "needsShovel": False, "purchase": False},
    {"name": "Airstream Island South Seashell", "id": ID + 19, "needsShovel": False, "purchase": False},
    {"name": "Secret Island Beach Seashell", "id": ID + 20, "needsShovel": False, "purchase": False},
    {"name": "Meteor Lake Seashell", "id": ID + 126, "needsShovel": False, "purchase": False},
    {"name": "Good Creek Path Seashell", "id": ID + 127, "needsShovel": False, "purchase": False},

    # Visitor's Center Shop
    {"name": "Visitor's Center Shop Golden Feather 1", "id": ID + 21, "needsShovel": False, "purchase": True},
    {"name": "Visitor's Center Shop Golden Feather 2", "id": ID + 22, "needsShovel": False, "purchase": True},
    {"name": "Visitor's Center Shop Hat", "id": ID + 23, "needsShovel": False, "purchase": True},

    # Tough Bird Salesman
    {"name": "Tough Bird Salesman Golden Feather 1", "id": ID + 24, "needsShovel": False, "purchase": True},
    {"name": "Tough Bird Salesman Golden Feather 2", "id": ID + 25, "needsShovel": False, "purchase": True},
    {"name": "Tough Bird Salesman Golden Feather 3", "id": ID + 26, "needsShovel": False, "purchase": True},
    {"name": "Tough Bird Salesman Golden Feather 4", "id": ID + 27, "needsShovel": False, "purchase": True},
    {"name": "Tough Bird Salesman (400 Coins)", "id": ID + 28, "needsShovel": False, "purchase": True},

    # Beachstickball
    {"name": "Beachstickball (10 Hits)", "id": ID + 29, "needsShovel": False, "purchase": False},
    {"name": "Beachstickball (20 Hits)", "id": ID + 30, "needsShovel": False, "purchase": False},
    {"name": "Beachstickball (30 Hits)", "id": ID + 31, "needsShovel": False, "purchase": False},

    # Misc Item Locations
    {"name": "Shovel Kid Trade", "id": ID + 32, "needsShovel": False, "purchase": False},
    {"name": "Compass Guy", "id": ID + 33, "needsShovel": False, "purchase": False},
    {"name": "Hawk Peak Bucket Rock", "id": ID + 34, "needsShovel": False, "purchase": False},
    {"name": "Orange Islands Bucket Rock", "id": ID + 35, "needsShovel": False, "purchase": False},
    {"name": "Bill the Walrus Fisherman", "id": ID + 36, "needsShovel": False, "purchase": False},
    {"name": "Catch 3 Fish Reward", "id": ID + 37, "needsShovel": False, "purchase": False},
    {"name": "Catch All Fish Reward", "id": ID + 38, "needsShovel": False, "purchase": False},
    {"name": "Permit Guy Bribe", "id": ID + 39, "needsShovel": False, "purchase": False},
    {"name": "Catch Fish with Permit", "id": ID + 129, "needsShovel": False, "purchase": False},
    {"name": "Return Camping Permit", "id": ID + 130, "needsShovel": False, "purchase": False},

    # Original Pickaxe Locations
    {"name": "Blocked Mine Pickaxe 1", "id": ID + 40, "needsShovel": False, "purchase": False},
    {"name": "Blocked Mine Pickaxe 2", "id": ID + 41, "needsShovel": False, "purchase": False},
    {"name": "Blocked Mine Pickaxe 3", "id": ID + 42, "needsShovel": False, "purchase": False},

    # Original Toy Shovel Locations
    {"name": "Blackwood Trail Lookout Toy Shovel", "id": ID + 43, "needsShovel": False, "purchase": False},
    {"name": "Shirley's Point Beach Toy Shovel", "id": ID + 44, "needsShovel": False, "purchase": False},
    {"name": "Visitor's Center Rock Toy Shovel", "id": ID + 45, "needsShovel": False, "purchase": False},
    {"name": "Blackwood Trail Rock Toy Shovel", "id": ID + 46, "needsShovel": False, "purchase": False},
    {"name": "Beach Hut Cliff Toy Shovel", "id": ID + 128, "needsShovel": False, "purchase": False},

    # Original Stick Locations
    {"name": "Secret Island Beach Trail Stick", "id": ID + 47, "needsShovel": False, "purchase": False},
    {"name": "Below Lighthouse Walkway Stick", "id": ID + 48, "needsShovel": False, "purchase": False},
    {"name": "Beach Hut Rocky Pool Sand Stick", "id": ID + 49, "needsShovel": False, "purchase": False},
    {"name": "Cliff Overlooking East River Waterfall Stick", "id": ID + 50, "needsShovel": False, "purchase": False},
    {"name": "Trail to Tough Bird Salesman Stick", "id": ID + 51, "needsShovel": False, "purchase": False},
    {"name": "North Beach Stick", "id": ID + 52, "needsShovel": False, "purchase": False},
    {"name": "Beachstickball Court Stick", "id": ID + 53, "needsShovel": False, "purchase": False},
    {"name": "Stick Under Sid Beach Umbrella", "id": ID + 54, "needsShovel": False, "purchase": False},

    # Boating
    {"name": "Boat Rental", "id": ID + 55, "needsShovel": False, "purchase": True},
    {"name": "Boat Challenge Reward", "id": ID + 56, "needsShovel": False, "purchase": False},

    # Original Map Locations
    {"name": "Outlook Point Dog Gift", "id": ID + 57, "needsShovel": False, "purchase": False},

    # Original Clothes Locations
    {"name": "Collect 15 Seashells", "id": ID + 58, "needsShovel": False, "purchase": False},
    {"name": "Taylor the Turtle Headband Gift", "id": ID + 59, "needsShovel": False, "purchase": False},
    {"name": "Sue the Rabbit Shoes Reward", "id": ID + 60, "needsShovel": False, "purchase": False},
    {"name": "Purchase Sunhat", "id": ID + 61, "needsShovel": False, "purchase": True},

    # Original Golden Feather Locations
    {"name": "Blackwood Forest Golden Feather", "id": ID + 62, "needsShovel": False, "purchase": False},
    {"name": "Ranger May Shell Necklace Golden Feather", "id": ID + 63, "needsShovel": False, "purchase": False},
    {"name": "Sand Castle Golden Feather", "id": ID + 64, "needsShovel": False, "purchase": False},
    {"name": "Artist Golden Feather", "id": ID + 65, "needsShovel": False, "purchase": False},
    {"name": "Visitor Camp Rock Golden Feather", "id": ID + 66, "needsShovel": False, "purchase": False},
    {"name": "Outlook Cliff Golden Feather", "id": ID + 67, "needsShovel": False, "purchase": False},
    {"name": "Meteor Lake Cliff Golden Feather", "id": ID + 68, "needsShovel": False, "purchase": False},

    # Original Silver Feather Locations
    {"name": "Secret Island Peak", "id": ID + 69, "needsShovel": False, "purchase": False},
    {"name": "Wristwatch Trade", "id": ID + 70, "needsShovel": False, "purchase": False},

    # Golden Chests
    {"name": "Lighthouse Golden Chest", "id": ID + 71, "needsShovel": False, "purchase": False},
    {"name": "Outlook Golden Chest", "id": ID + 72, "needsShovel": False, "purchase": False},
    {"name": "Stone Tower Golden Chest", "id": ID + 73, "needsShovel": False, "purchase": False},
    {"name": "North Cliff Golden Chest", "id": ID + 74, "needsShovel": False, "purchase": False},

    # Chests
    {"name": "Blackwood Cliff Chest", "id": ID + 75, "needsShovel": False, "purchase": False}, 
    {"name": "White Coast Trail Chest", "id": ID + 76, "needsShovel": False, "purchase": False}, 
    {"name": "Sid Beach Chest", "id": ID + 77, "needsShovel": False, "purchase": False}, 
    {"name": "Sid Beach Buried Treasure Chest", "id": ID + 78, "needsShovel": True, "purchase": False}, 
    {"name": "Sid Beach Cliff Chest", "id": ID + 79, "needsShovel": False, "purchase": False}, 
    {"name": "Visitor's Center Buried Chest", "id": ID + 80, "needsShovel": True, "purchase": False}, 
    {"name": "Visitor's Center Hidden Chest", "id": ID + 81, "needsShovel": False, "purchase": False}, 
    {"name": "Shirley's Point Chest", "id": ID + 82, "needsShovel": False, "purchase": False}, 
    {"name": "Caravan Cliff Chest", "id": ID + 83, "needsShovel": False, "purchase": False}, 
    {"name": "Caravan Arch Chest", "id": ID + 84, "needsShovel": False, "purchase": False}, 
    {"name": "King Buried Treasure Chest", "id": ID + 85, "needsShovel": True, "purchase": False}, 
    {"name": "Good Creek Path Buried Chest", "id": ID + 86, "needsShovel": True, "purchase": False}, 
    {"name": "Good Creek Path West Chest", "id": ID + 87, "needsShovel": False, "purchase": False}, 
    {"name": "Good Creek Path East Chest", "id": ID + 88, "needsShovel": False, "purchase": False}, 
    {"name": "West Waterfall Chest", "id": ID + 89, "needsShovel": False, "purchase": False}, 
    {"name": "Stone Tower West Cliff Chest", "id": ID + 90, "needsShovel": False, "purchase": False}, 
    {"name": "Bucket Path Chest", "id": ID + 91, "needsShovel": False, "purchase": False}, 
    {"name": "Bucket Cliff Chest", "id": ID + 92, "needsShovel": False, "purchase": False}, 
    {"name": "In Her Shadow Buried Treasure Chest", "id": ID + 93, "needsShovel": True, "purchase": False}, 
    {"name": "Meteor Lake Buried Chest", "id": ID + 94, "needsShovel": True, "purchase": False}, 
    {"name": "Meteor Lake Chest", "id": ID + 95, "needsShovel": False, "purchase": False}, 
    {"name": "House North Beach Chest", "id": ID + 96, "needsShovel": False, "purchase": False}, 
    {"name": "East Coast Chest", "id": ID + 97, "needsShovel": False, "purchase": False}, 
    {"name": "Fisherman's Boat Chest 1", "id": ID + 99, "needsShovel": False, "purchase": False}, 
    {"name": "Fisherman's Boat Chest 2", "id": ID + 100, "needsShovel": False, "purchase": False}, 
    {"name": "Airstream Island Chest", "id": ID + 101, "needsShovel": False, "purchase": False}, 
    {"name": "West River Waterfall Head Chest", "id": ID + 102, "needsShovel": False, "purchase": False}, 
    {"name": "Old Building Chest", "id": ID + 103, "needsShovel": False, "purchase": False}, 
    {"name": "Old Building West Chest", "id": ID + 104, "needsShovel": False, "purchase": False}, 
    {"name": "Old Building East Chest", "id": ID + 105, "needsShovel": False, "purchase": False}, 
    {"name": "Hawk Peak West Chest", "id": ID + 106, "needsShovel": False, "purchase": False}, 
    {"name": "Hawk Peak East Buried Chest", "id": ID + 107, "needsShovel": True, "purchase": False}, 
    {"name": "Hawk Peak Northeast Chest", "id": ID + 108, "needsShovel": False, "purchase": False}, 
    {"name": "Northern East Coast Chest", "id": ID + 109, "needsShovel": False, "purchase": False}, 
    {"name": "North Coast Chest", "id": ID + 110, "needsShovel": False, "purchase": False}, 
    {"name": "North Coast Buried Chest", "id": ID + 111, "needsShovel": True, "purchase": False}, 
    {"name": "Small South Island Buried Chest", "id": ID + 112, "needsShovel": True, "purchase": False}, 
    {"name": "Secret Island Bottom Chest", "id": ID + 113, "needsShovel": False, "purchase": False}, 
    {"name": "Secret Island Middle Chest", "id": ID + 114, "needsShovel": False, "purchase": False}, 
    {"name": "Sunhat Island Buried Chest", "id": ID + 115, "needsShovel": True, "purchase": False}, 
    {"name": "Orange Islands South Buried Chest", "id": ID + 116, "needsShovel": True, "purchase": False}, 
    {"name": "Orange Islands West Chest", "id": ID + 117, "needsShovel": False, "purchase": False}, 
    {"name": "Orange Islands North Buried Chest", "id": ID + 118, "needsShovel": True, "purchase": False}, 
    {"name": "Orange Islands East Chest", "id": ID + 119, "needsShovel": False, "purchase": False}, 
    {"name": "Orange Islands South Hidden Chest", "id": ID + 120, "needsShovel": False, "purchase": False}, 
    {"name": "A Stormy View Buried Treasure Chest", "id": ID + 121, "needsShovel": True, "purchase": False}, 
    {"name": "Orange Islands Ruins Buried Chest", "id": ID + 122, "needsShovel": True, "purchase": False}, 

    # Race Rewards
    {"name": "Lighthouse Race Reward", "id": ID + 123, "needsShovel": False, "purchase": False},
    {"name": "Old Building Race Reward", "id": ID + 124, "needsShovel": False, "purchase": False},
    {"name": "Hawk Peak Race Reward", "id": ID + 125, "needsShovel": False, "purchase": False},
    {"name": "Lose Race Gift", "id": ID + 131, "needsShovel": False, "purchase": False},
]