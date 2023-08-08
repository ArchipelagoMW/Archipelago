from typing import List, TypedDict


class LocationDict(TypedDict):
    name: str
    id: int

# IDs from 81000 to 81125

ID = 81000

location_table: List[LocationDict] = [
    # Original Seashell Locations
    {"name": "Start Beach Seashell", "id": ID + ID + 1},
    {"name": "Beach Hut Seashell", "id": ID + 2},
    {"name": "Beach Umbrella Seashell", "id": ID + 3},
    {"name": "Sid Beach Mound Seashell", "id": ID + 4},
    {"name": "Sid Beach Seashell", "id": ID + 5},
    {"name": "Shirley's Point Beach Seashell", "id": ID + 6},
    {"name": "Shirley's Point Rock Seashell", "id": ID + 7},
    {"name": "Visitor's Center Beach Seashell", "id": ID + 8},
    {"name": "West River Seashell", "id": ID + 9},
    {"name": "West Riverbank Seashell", "id": ID + 10},
    {"name": "Stone Tower Riverbank Seashell", "id": ID + 11},
    {"name": "North Beach Seashell", "id": ID + 12},
    {"name": "North Coast Seashell", "id": ID + 13},
    {"name": "Boat Cliff Seashell", "id": ID + 14},
    {"name": "Boat Isle Mound Seashell", "id": ID + 15},
    {"name": "East Coast Seashell", "id": ID + 16},
    {"name": "House North Beach Seashell", "id": ID + 17},
    {"name": "Airstream Island North Seashell", "id": ID + 18},
    {"name": "Airstream Island South Seashell", "id": ID + 19},
    {"name": "Secret Island Beach Seashell", "id": ID + 20},

    # Visitor's Center Shop
    {"name": "Visitor's Center Shop Golden Feather 1", "id": ID + 21},
    {"name": "Visitor's Center Shop Golden Feather 2", "id": ID + 22},
    {"name": "Visitor's Center Shop Hat", "id": ID + 23},

    # Tough Bird Salesman
    {"name": "Tough Bird Salesman Golden Feather 1", "id": ID + 24},
    {"name": "Tough Bird Salesman Golden Feather 2", "id": ID + 25},
    {"name": "Tough Bird Salesman Golden Feather 3", "id": ID + 26},
    {"name": "Tough Bird Salesman Golden Feather 4", "id": ID + 27},
    {"name": "Tough Bird Salesman (400 Coins)", "id": ID + 28},

    # Beachstickball
    {"name": "Beachstickball (10 Hits)", "id": ID + 29},
    {"name": "Beachstickball (20 Hits)", "id": ID + 30},
    {"name": "Beachstickball (30 Hits)", "id": ID + 31},

    # Misc Item Locations
    {"name": "Shovel Kid Trade", "id": ID + 32},
    {"name": "Compass Guy", "id": ID + 33},
    {"name": "Hawk Peak Bucket Rock", "id": ID + 34},
    {"name": "Orange Islands Bucket Rock", "id": ID + 35},
    {"name": "Bill the Walrus Fisherman", "id": ID + 36},
    {"name": "Catch 3 Fish Reward", "id": ID + 37},
    {"name": "Catch All Fish Reward", "id": ID + 38},
    {"name": "Permit Guy Bribe", "id": ID + 39},

    # Original Pickaxe Locations
    {"name": "Blocked Mine Pickaxe 1", "id": ID + 40},
    {"name": "Blocked Mine Pickaxe 2", "id": ID + 41},
    {"name": "Blocked Mine Pickaxe 3", "id": ID + 42},

    # Original Toy Shovel Locations
    {"name": "Blackwood Trail Lookout Toy Shovel", "id": ID + 43},
    {"name": "Shirley's Point Beach Toy Shovel", "id": ID + 44},
    {"name": "Visitor's Center Rock Toy Shovel", "id": ID + 45},
    {"name": "Blackwood Trail Rock Toy Shovel", "id": ID + 46},

    # Original Stick Locations
    {"name": "Secret Island Beach Trail Stick", "id": ID + 47},
    {"name": "Below Lighthouse Walkway Stick", "id": ID + 48},
    {"name": "Beach Hut Rocky Pool Sand Stick", "id": ID + 49},
    {"name": "Cliff Overlooking East River Waterfall Stick", "id": ID + 50},
    {"name": "Trail to Tough Bird Salesman Stick", "id": ID + 51},
    {"name": "North Beach Stick", "id": ID + 52},
    {"name": "Beachstickball Court Stick", "id": ID + 53},
    {"name": "Stick Under Sid Beach Umbrella", "id": ID + 54},

    # Boating
    {"name": "Boat Rental", "id": ID + 55},
    {"name": "Boat Challenge Reward", "id": ID + 56},

    # Original Map Locations
    {"name": "Outlook Point Dog Gift", "id": ID + 57},

    # Original Clothes Locations
    {"name": "Collect 15 Seashells", "id": ID + 58},
    {"name": "Taylor the Turtle Headband Gift", "id": ID + 59},
    {"name": "Sue the Rabbit Shoes Reward", "id": ID + 60},
    {"name": "Purchase Sunhat", "id": ID + 61},

    # Original Golden Feather Locations
    {"name": "Blackwood Forest Golden Feather", "id": ID + 62},
    {"name": "Ranger May Shell Necklace Golden Feather", "id": ID + 63},
    {"name": "Sand Castle Golden Feather", "id": ID + 64},
    {"name": "Artist Golden Feather", "id": ID + 65},
    {"name": "Visitor Camp Rock Golden Feather", "id": ID + 66},
    {"name": "Outlook Cliff Golden Feather", "id": ID + 67},
    {"name": "Meteor Lake Cliff Golden Feather", "id": ID + 68},

    # Original Silver Feather Locations
    {"name": "Secret Island Peak", "id": ID + 69},
    {"name": "Wristwatch Trade", "id": ID + 70},

    # Golden Chests
    {"name": "Lighthouse Golden Chest", "id": ID + 71},
    {"name": "Outlook Golden Chest", "id": ID + 72},
    {"name": "Stone Tower Golden Chest", "id": ID + 73},
    {"name": "North Cliff Golden Chest", "id": ID + 74},

    # Chests
    {"name": "Blackwood Cliff Chest", "id": ID + 75},
    {"name": "White Coast Trail Chest", "id": ID + 76},
    {"name": "Sid Beach Chest", "id": ID + 77},
    {"name": "Sid Beach Buried Treasure Chest", "id": ID + 78},
    {"name": "Sid Beach Cliff Chest", "id": ID + 79},
    {"name": "Visitor's Center Buried Chest", "id": ID + 80},
    {"name": "Visitor's Center Hidden Chest", "id": ID + 81},
    {"name": "Shirley's Point Chest", "id": ID + 82},
    {"name": "Caravan Cliff Chest", "id": ID + 83},
    {"name": "Caravan Arch Chest", "id": ID + 84},
    {"name": "King Buried Treasure Chest", "id": ID + 85},
    {"name": "Good Creek Path Buried Chest", "id": ID + 86},
    {"name": "Good Creek Path West Chest", "id": ID + 87},
    {"name": "Good Creek Path East Chest", "id": ID + 88},
    {"name": "West Waterfall Chest", "id": ID + 89},
    {"name": "Stone Tower West Cliff Chest", "id": ID + 90},
    {"name": "Bucket Path Chest", "id": ID + 91},
    {"name": "Bucket Cliff Chest", "id": ID + 92},
    {"name": "In Her Shadow Buried Treasure Chest", "id": ID + 93},
    {"name": "Meteor Lake Buried Chest", "id": ID + 94},
    {"name": "Meteor Lake Chest", "id": ID + 95},
    {"name": "House North Beach Chest", "id": ID + 96},
    {"name": "East Coast Chest", "id": ID + 97},
    {"name": "East Coast Buried Chest", "id": ID + 98},
    {"name": "Fisherman's Boat Chest 1", "id": ID + 99},
    {"name": "Fisherman's Boat Chest 2", "id": ID + 100},
    {"name": "Airstream Island Chest", "id": ID + 101},
    {"name": "West River Waterfall Head Chest", "id": ID + 102},
    {"name": "Old Building Chest", "id": ID + 103},
    {"name": "Old Building West Chest", "id": ID + 104},
    {"name": "Old Building East Chest", "id": ID + 105},
    {"name": "Hawk Peak West Chest", "id": ID + 106},
    {"name": "Hawk Peak East Chest", "id": ID + 107},
    {"name": "Hawk Peak Northeast Chest", "id": ID + 108},
    {"name": "Northern East Coast Chest", "id": ID + 109},
    {"name": "North Coast Chest", "id": ID + 110},
    {"name": "North Coast Buried Chest", "id": ID + 111},
    {"name": "Small South Island Chest", "id": ID + 112},
    {"name": "Secret Island Bottom Chest", "id": ID + 113},
    {"name": "Secret Island Middle Chest", "id": ID + 114},
    {"name": "Sunhat Island Chest", "id": ID + 115},
    {"name": "Orange Islands South Buried Chest", "id": ID + 116},
    {"name": "Orange Islands West Chest", "id": ID + 117},
    {"name": "Orange Islands North Buried Chest", "id": ID + 118},
    {"name": "Orange Islands East Chest", "id": ID + 119},
    {"name": "Orange Islands South Hidden Chest", "id": ID + 120},
    {"name": "A Stormy View Buried Treasure Chest", "id": ID + 121},
    {"name": "Orange Islands Ruins Buried Chest", "id": ID + 122},

    # Race Rewards
    {"name": "Lighthouse Race Reward", "id": ID + 123},
    {"name": "Old Building Race Reward", "id": ID + 124},
    {"name": "Hawk Peak Race Reward", "id": ID + 125},
]