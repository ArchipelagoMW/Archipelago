from typing import List, TypedDict


class LocationDict(TypedDict):
    name: str
    id: int
    inGameId: str
    needsShovel: bool
    purchase: bool

# base_ids from 81000 to 81131

base_id = 81000

location_table: List[LocationDict] = [
    # Original Seashell Locations
    {"name": "Start Beach Seashell", "id": base_id + 1, "inGameId": "(706.2, 7.3, 344.4)", "needsShovel": False, "purchase": False},
    {"name": "Beach Hut Seashell", "id": base_id + 2, "inGameId": "(522.8, 7.3, 120.5)", "needsShovel": False, "purchase": False},
    {"name": "Beach Umbrella Seashell", "id": base_id + 3, "inGameId": "(407.7, 8.5, 127.1)", "needsShovel": False, "purchase": False},
    {"name": "Sid Beach Mound Seashell", "id": base_id + 4, "inGameId": "(402.0, 21.6, 11.9)", "needsShovel": False, "purchase": False},
    {"name": "Sid Beach Seashell", "id": base_id + 5, "inGameId": "(348.9, 8.5, 40.0)", "needsShovel": False, "purchase": False},
    {"name": "Shirley's Point Beach Seashell", "id": base_id + 6, "inGameId": "(56.8, 8.4, 135.0)", "needsShovel": False, "purchase": False},
    {"name": "Shirley's Point Rock Seashell", "id": base_id + 7, "inGameId": "(94.3, 9.9, 77.8)", "needsShovel": False, "purchase": False},
    {"name": "Visitor's Center Beach Seashell", "id": base_id + 8, "inGameId": "(26.7, 8.4, 245.2)", "needsShovel": False, "purchase": False},
    {"name": "West River Seashell", "id": base_id + 9, "inGameId": "(137.7, 53.9, 357.9)", "needsShovel": False, "purchase": False},
    {"name": "West Riverbank Seashell", "id": base_id + 10, "inGameId": "(131.9, 88.3, 421.7)", "needsShovel": False, "purchase": False},
    {"name": "Stone Tower Riverbank Seashell", "id": base_id + 11, "inGameId": "(179.9, 191.2, 573.1)", "needsShovel": False, "purchase": False},
    {"name": "North Beach Seashell", "id": base_id + 12, "inGameId": "(61.3, 8.5, 866.1)", "needsShovel": False, "purchase": False},
    {"name": "North Coast Seashell", "id": base_id + 13, "inGameId": "(483.7, 10.1, 1027.9)", "needsShovel": False, "purchase": False},
    {"name": "Boat Cliff Seashell", "id": base_id + 14, "inGameId": "(587.7, 62.9, 751.4)", "needsShovel": False, "purchase": False},
    {"name": "Boat Isle Mound Seashell", "id": base_id + 15, "inGameId": "(667.4, 19.7, 767.2)", "needsShovel": False, "purchase": False},
    {"name": "East Coast Seashell", "id": base_id + 16, "inGameId": "(765.8, 7.5, 630.5)", "needsShovel": False, "purchase": False},
    {"name": "House North Beach Seashell", "id": base_id + 17, "inGameId": "(760.7, 9.6, 488.2)", "needsShovel": False, "purchase": False},
    {"name": "Airstream Island North Seashell", "id": base_id + 18, "inGameId": "(870.7, 19.8, 567.3)", "needsShovel": False, "purchase": False},
    {"name": "Airstream Island South Seashell", "id": base_id + 19, "inGameId": "(848.4, 18.9, 396.0)", "needsShovel": False, "purchase": False},
    {"name": "Secret Island Beach Seashell", "id": base_id + 20, "inGameId": "(775.7, 21.2, 80.2)", "needsShovel": False, "purchase": False},
    {"name": "Meteor Lake Seashell", "id": base_id + 126, "inGameId": "(589.0, 95.6, 621.1)", "needsShovel": False, "purchase": False},
    {"name": "Good Creek Path Seashell", "id": base_id + 127, "inGameId": "(322.4, 135.8, 408.9)", "needsShovel": False, "purchase": False},

    # Visitor's Center Shop
    {"name": "Visitor's Center Shop Golden Feather 1", "id": base_id + 21, "inGameId": "CampRangerNPC[0]", "needsShovel": False, "purchase": True},
    {"name": "Visitor's Center Shop Golden Feather 2", "id": base_id + 22, "inGameId": "CampRangerNPC[1]", "needsShovel": False, "purchase": True},
    {"name": "Visitor's Center Shop Hat", "id": base_id + 23, "inGameId": "CampRangerNPC[9]", "needsShovel": False, "purchase": True},

    # Tough Bird Salesman
    {"name": "Tough Bird Salesman Golden Feather 1", "id": base_id + 24, "inGameId": "ToughBirdNPC (1)[0]", "needsShovel": False, "purchase": True},
    {"name": "Tough Bird Salesman Golden Feather 2", "id": base_id + 25, "inGameId": "ToughBirdNPC (1)[1]", "needsShovel": False, "purchase": True},
    {"name": "Tough Bird Salesman Golden Feather 3", "id": base_id + 26, "inGameId": "ToughBirdNPC (1)[2]", "needsShovel": False, "purchase": True},
    {"name": "Tough Bird Salesman Golden Feather 4", "id": base_id + 27, "inGameId": "ToughBirdNPC (1)[3]", "needsShovel": False, "purchase": True},
    {"name": "Tough Bird Salesman (400 Coins)", "id": base_id + 28, "inGameId": "ToughBirdNPC (1)[9]", "needsShovel": False, "purchase": True},

    # Beachstickball
    {"name": "Beachstickball (10 Hits)", "id": base_id + 29, "inGameId": "VolleyballOpponent[0]", "needsShovel": False, "purchase": False},
    {"name": "Beachstickball (20 Hits)", "id": base_id + 30, "inGameId": "VolleyballOpponent[1]", "needsShovel": False, "purchase": False},
    {"name": "Beachstickball (30 Hits)", "id": base_id + 31, "inGameId": "VolleyballOpponent[2]", "needsShovel": False, "purchase": False},

    # Misc Item Locations
    {"name": "Shovel Kid Trade", "id": base_id + 32, "inGameId": "Frog_StandingNPC[0]", "needsShovel": False, "purchase": False},
    {"name": "Compass Guy", "id": base_id + 33, "inGameId": "Fox_WalkingNPC[0]", "needsShovel": False, "purchase": False},
    {"name": "Hawk Peak Bucket Rock", "id": base_id + 34, "inGameId": "(473.4, 242.8, 648.4)", "needsShovel": False, "purchase": False},
    {"name": "Orange Islands Bucket Rock", "id": base_id + 35, "inGameId": "(266.3, 13.3, 1396.9)", "needsShovel": False, "purchase": False},
    {"name": "Bill the Walrus Fisherman", "id": base_id + 36, "inGameId": "SittingNPC (1)[0]", "needsShovel": False, "purchase": False},
    {"name": "Catch 3 Fish Reward", "id": base_id + 37, "inGameId": "FishBuyer[0]", "needsShovel": False, "purchase": False},
    {"name": "Catch All Fish Reward", "id": base_id + 38, "inGameId": "FishBuyer[1]", "needsShovel": False, "purchase": False},
    {"name": "Permit Guy Bribe", "id": base_id + 39, "inGameId": "CamperNPC[0]", "needsShovel": False, "purchase": False},
    {"name": "Catch Fish with Permit", "id": base_id + 129, "inGameId": "Player[0]", "needsShovel": False, "purchase": False},
    {"name": "Return Camping Permit", "id": base_id + 130, "inGameId": "CamperNPC[1]", "needsShovel": False, "purchase": False},

    # Original Pickaxe Locations
    {"name": "Blocked Mine Pickaxe 1", "id": base_id + 40, "inGameId": "(515.8, 31.1, 954.4)", "needsShovel": False, "purchase": False},
    {"name": "Blocked Mine Pickaxe 2", "id": base_id + 41, "inGameId": "(505.4, 31.1, 964.5)", "needsShovel": False, "purchase": False},
    {"name": "Blocked Mine Pickaxe 3", "id": base_id + 42, "inGameId": "(498.8, 46.1, 941.0)", "needsShovel": False, "purchase": False},

    # Original Toy Shovel Locations
    {"name": "Blackwood Trail Lookout Toy Shovel", "id": base_id + 43, "inGameId": "(204.3, 108.9, 277.4)", "needsShovel": False, "purchase": False},
    {"name": "Shirley's Point Beach Toy Shovel", "id": base_id + 44, "inGameId": "(54.4, 8.4, 129.5)", "needsShovel": False, "purchase": False},
    {"name": "Visitor's Center Beach Toy Shovel", "id": base_id + 45, "inGameId": "(27.0, 8.4, 254.3)", "needsShovel": False, "purchase": False},
    {"name": "Blackwood Trail Rock Toy Shovel", "id": base_id + 46, "inGameId": "(364.0, 85.1, 268.2)", "needsShovel": False, "purchase": False},
    {"name": "Beach Hut Cliff Toy Shovel", "id": base_id + 128, "inGameId": "(422.3, 38.2, 175.1)", "needsShovel": False, "purchase": False},

    # Original Stick Locations
    {"name": "Secret Island Beach Trail Stick", "id": base_id + 47, "inGameId": "(776.3, 9.2, 140.7)", "needsShovel": False, "purchase": False},
    {"name": "Below Lighthouse Walkway Stick", "id": base_id + 48, "inGameId": "(566.2, 74.5, 325.2)", "needsShovel": False, "purchase": False},
    {"name": "Beach Hut Rocky Pool Sand Stick", "id": base_id + 49, "inGameId": "(510.9, 10.4, 191.0)", "needsShovel": False, "purchase": False},
    {"name": "Cliff Overlooking West River Waterfall Stick", "id": base_id + 50, "inGameId": "(84.4, 112.9, 464.1)", "needsShovel": False, "purchase": False},
    {"name": "Trail to Tough Bird Salesman Stick", "id": base_id + 51, "inGameId": "(268.6, 265.9, 535.0)", "needsShovel": False, "purchase": False},
    {"name": "North Beach Stick", "id": base_id + 52, "inGameId": "(37.9, 9.0, 853.0)", "needsShovel": False, "purchase": False},
    {"name": "Beachstickball Court Stick", "id": base_id + 53, "inGameId": "(117.3, 10.7, 1008.8)", "needsShovel": False, "purchase": False},
    {"name": "Stick Under Sid Beach Umbrella", "id": base_id + 54, "inGameId": "(441.5, 9.1, 126.4)", "needsShovel": False, "purchase": False},

    # Boating
    {"name": "Boat Rental", "id": base_id + 55, "inGameId": "DadDeer[0]", "needsShovel": False, "purchase": True},
    {"name": "Boat Challenge Reward", "id": base_id + 56, "inGameId": "DeerKidBoat[0]", "needsShovel": False, "purchase": False},

    # Original Map Locations
    {"name": "Outlook Point Dog Gift", "id": base_id + 57, "inGameId": "Dog_WalkingNPC_BlueEyed[0]", "needsShovel": False, "purchase": False},

    # Original Clothes Locations
    {"name": "Collect 15 Seashells", "id": base_id + 58, "inGameId": "LittleKidNPCVariant (1)[0]", "needsShovel": False, "purchase": False},
    {"name": "Taylor the Turtle Headband Gift", "id": base_id + 59, "inGameId": "Turtle_WalkingNPC[0]", "needsShovel": False, "purchase": False},
    {"name": "Sue the Rabbit Shoes Reward", "id": base_id + 60, "inGameId": "Bunny_WalkingNPC (1)[0]", "needsShovel": False, "purchase": False},
    {"name": "Purchase Sunhat", "id": base_id + 61, "inGameId": "SittingNPC[0]", "needsShovel": False, "purchase": True},

    # Original Golden Feather Locations
    {"name": "Blackwood Forest Golden Feather", "id": base_id + 62, "inGameId": "(460.1, 93.6, 240.8)", "needsShovel": False, "purchase": False},
    {"name": "Ranger May Shell Necklace Golden Feather", "id": base_id + 63, "inGameId": "AuntMayNPC[0]", "needsShovel": False, "purchase": False},
    {"name": "Sand Castle Golden Feather", "id": base_id + 64, "inGameId": "(376.7, 14.0, 51.7)", "needsShovel": False, "purchase": False},
    {"name": "Artist Golden Feather", "id": base_id + 65, "inGameId": "StandingNPC[0]", "needsShovel": False, "purchase": False},
    {"name": "Visitor Camp Rock Golden Feather", "id": base_id + 66, "inGameId": "(123.2, 35.0, 168.2)", "needsShovel": False, "purchase": False},
    {"name": "Outlook Cliff Golden Feather", "id": base_id + 67, "inGameId": "(209.2, 149.3, 340.0)", "needsShovel": False, "purchase": False},
    {"name": "Meteor Lake Cliff Golden Feather", "id": base_id + 68, "inGameId": "(521.0, 208.7, 691.6)", "needsShovel": False, "purchase": False},

    # Original Silver Feather Locations
    {"name": "Secret Island Peak", "id": base_id + 69, "inGameId": "(864.3, 219.4, 85.4)", "needsShovel": False, "purchase": False},
    {"name": "Wristwatch Trade", "id": base_id + 70, "inGameId": "Goat_StandingNPC[0]", "needsShovel": False, "purchase": False},

    # Golden Chests
    {"name": "Lighthouse Golden Chest", "id": base_id + 71, "inGameId": "(594.7, 143.3, 345.6)", "needsShovel": False, "purchase": False},
    {"name": "Outlook Golden Chest", "id": base_id + 72, "inGameId": "(260.3, 251.8, 355.1)", "needsShovel": False, "purchase": False},
    {"name": "Stone Tower Golden Chest", "id": base_id + 73, "inGameId": "(129.7, 143.8, 513.2)", "needsShovel": False, "purchase": False},
    {"name": "North Cliff Golden Chest", "id": base_id + 74, "inGameId": "(380.2, 186.0, 1040.6)", "needsShovel": False, "purchase": False},

    # Chests
    {"name": "Blackwood Cliff Chest", "id": base_id + 75, "inGameId": "(416.0, 57.9, 203.0)", "needsShovel": False, "purchase": False}, 
    {"name": "White Coast Trail Chest", "id": base_id + 76, "inGameId": "(482.4, 14.4, 26.8)", "needsShovel": False, "purchase": False}, 
    {"name": "Sid Beach Chest", "id": base_id + 77, "inGameId": "(387.7, 8.8, 60.4)", "needsShovel": False, "purchase": False}, 
    {"name": "Sid Beach Buried Treasure Chest", "id": base_id + 78, "inGameId": "(274.2, 10.0, 30.4)", "needsShovel": True, "purchase": False}, 
    {"name": "Sid Beach Cliff Chest", "id": base_id + 79, "inGameId": "(261.6, 32.1, 41.0)", "needsShovel": False, "purchase": False}, 
    {"name": "Visitor's Center Buried Chest", "id": base_id + 80, "inGameId": "(233.6, 47.2, 58.1)", "needsShovel": True, "purchase": False}, 
    {"name": "Visitor's Center Hidden Chest", "id": base_id + 81, "inGameId": "(165.7, 31.1, 137.8)", "needsShovel": False, "purchase": False}, 
    {"name": "Shirley's Point Chest", "id": base_id + 82, "inGameId": "(40.2, 46.4, 61.9)", "needsShovel": False, "purchase": False}, 
    {"name": "Caravan Cliff Chest", "id": base_id + 83, "inGameId": "(206.3, 48.8, 185.6)", "needsShovel": False, "purchase": False}, 
    {"name": "Caravan Arch Chest", "id": base_id + 84, "inGameId": "(293.6, 37.5, 206.5)", "needsShovel": False, "purchase": False}, 
    {"name": "King Buried Treasure Chest", "id": base_id + 85, "inGameId": "(138.3, 96.0, 298.3)", "needsShovel": True, "purchase": False}, 
    {"name": "Good Creek Path Buried Chest", "id": base_id + 86, "inGameId": "(292.8, 165.4, 327.3)", "needsShovel": True, "purchase": False}, 
    {"name": "Good Creek Path West Chest", "id": base_id + 87, "inGameId": "(315.7, 164.8, 444.6)", "needsShovel": False, "purchase": False}, 
    {"name": "Good Creek Path East Chest", "id": base_id + 88, "inGameId": "(358.3, 102.9, 473.8)", "needsShovel": False, "purchase": False}, 
    {"name": "West Waterfall Chest", "id": base_id + 89, "inGameId": "(-5.3, 10.4, 495.1)", "needsShovel": False, "purchase": False}, 
    {"name": "Stone Tower West Cliff Chest", "id": base_id + 90, "inGameId": "(53.6, 185.8, 540.4)", "needsShovel": False, "purchase": False}, 
    {"name": "Bucket Path Chest", "id": base_id + 91, "inGameId": "(429.7, 259.3, 602.4)", "needsShovel": False, "purchase": False}, 
    {"name": "Bucket Cliff Chest", "id": base_id + 92, "inGameId": "(386.7, 319.5, 609.5)", "needsShovel": False, "purchase": False}, 
    {"name": "In Her Shadow Buried Treasure Chest", "id": base_id + 93, "inGameId": "(590.3, 123.6, 410.7)", "needsShovel": True, "purchase": False}, 
    {"name": "Meteor Lake Buried Chest", "id": base_id + 94, "inGameId": "(583.9, 102.9, 545.5)", "needsShovel": True, "purchase": False}, 
    {"name": "Meteor Lake Chest", "id": base_id + 95, "inGameId": "(652.9, 103.1, 552.3)", "needsShovel": False, "purchase": False}, 
    {"name": "House North Beach Chest", "id": base_id + 96, "inGameId": "(734.2, 39.0, 445.6)", "needsShovel": False, "purchase": False}, 
    {"name": "East Coast Chest", "id": base_id + 97, "inGameId": "(768.5, 65.8, 571.3)", "needsShovel": False, "purchase": False}, 
    {"name": "Fisherman's Boat Chest 1", "id": base_id + 99, "inGameId": "(755.3, 13.2, 729.6)", "needsShovel": False, "purchase": False}, 
    {"name": "Fisherman's Boat Chest 2", "id": base_id + 100, "inGameId": "(749.7, 13.0, 738.7)", "needsShovel": False, "purchase": False}, 
    {"name": "Airstream Island Chest", "id": base_id + 101, "inGameId": "(832.6, 20.6, 422.2)", "needsShovel": False, "purchase": False}, 
    {"name": "West River Waterfall Head Chest", "id": base_id + 102, "inGameId": "(213.1, 295.4, 687.8)", "needsShovel": False, "purchase": False}, 
    {"name": "Old Building Chest", "id": base_id + 103, "inGameId": "(139.9, 133.9, 715.4)", "needsShovel": False, "purchase": False}, 
    {"name": "Old Building West Chest", "id": base_id + 104, "inGameId": "(25.8, 64.7, 700.8)", "needsShovel": False, "purchase": False}, 
    {"name": "Old Building East Chest", "id": base_id + 105, "inGameId": "(177.4, 184.0, 731.9)", "needsShovel": False, "purchase": False}, 
    {"name": "Hawk Peak West Chest", "id": base_id + 106, "inGameId": "(292.4, 439.9, 834.7)", "needsShovel": False, "purchase": False}, 
    {"name": "Hawk Peak East Buried Chest", "id": base_id + 107, "inGameId": "(512.9, 371.9, 763.2)", "needsShovel": True, "purchase": False}, 
    {"name": "Hawk Peak Northeast Chest", "id": base_id + 108, "inGameId": "(448.8, 354.8, 950.7)", "needsShovel": False, "purchase": False}, 
    {"name": "Northern East Coast Chest", "id": base_id + 109, "inGameId": "(527.5, 93.4, 885.1)", "needsShovel": False, "purchase": False}, 
    {"name": "North Coast Chest", "id": base_id + 110, "inGameId": "(455.9, 49.1, 1012.2)", "needsShovel": False, "purchase": False}, 
    {"name": "North Coast Buried Chest", "id": base_id + 111, "inGameId": "(441.2, 28.3, 1070.3)", "needsShovel": True, "purchase": False}, 
    {"name": "Small South Island Buried Chest", "id": base_id + 112, "inGameId": "(643.7, 20.1, 36.3)", "needsShovel": True, "purchase": False}, 
    {"name": "Secret Island Bottom Chest", "id": base_id + 113, "inGameId": "(816.0, 33.1, 141.3)", "needsShovel": False, "purchase": False}, 
    {"name": "Secret Island Middle Chest", "id": base_id + 114, "inGameId": "(832.1, 95.1, 66.1)", "needsShovel": False, "purchase": False}, 
    {"name": "Sunhat Island Buried Chest", "id": base_id + 115, "inGameId": "(972.8, 27.2, 984.0)", "needsShovel": True, "purchase": False}, 
    {"name": "Orange Islands South Buried Chest", "id": base_id + 116, "inGameId": "(79.2, 19.7, 1150.5)", "needsShovel": True, "purchase": False}, 
    {"name": "Orange Islands West Chest", "id": base_id + 117, "inGameId": "(111.8, 16.6, 1305.4)", "needsShovel": False, "purchase": False}, 
    {"name": "Orange Islands North Buried Chest", "id": base_id + 118, "inGameId": "(88.4, 29.8, 1417.9)", "needsShovel": True, "purchase": False}, 
    {"name": "Orange Islands East Chest", "id": base_id + 119, "inGameId": "(483.7, 16.8, 1424.6)", "needsShovel": False, "purchase": False}, 
    {"name": "Orange Islands South Hidden Chest", "id": base_id + 120, "inGameId": "(441.9, 12.3, 1250.2)", "needsShovel": False, "purchase": False}, 
    {"name": "A Stormy View Buried Treasure Chest", "id": base_id + 121, "inGameId": "(319.5, 8.9, 1314.1)", "needsShovel": True, "purchase": False}, 
    {"name": "Orange Islands Ruins Buried Chest", "id": base_id + 122, "inGameId": "(406.6, 46.3, 1311.0)", "needsShovel": True, "purchase": False}, 

    # Race Rewards
    {"name": "Lighthouse Race Reward", "id": base_id + 123, "inGameId": "RaceOpponent[0]", "needsShovel": False, "purchase": False},
    {"name": "Old Building Race Reward", "id": base_id + 124, "inGameId": "RaceOpponent[1]", "needsShovel": False, "purchase": False},
    {"name": "Hawk Peak Race Reward", "id": base_id + 125, "inGameId": "RaceOpponent[2]", "needsShovel": False, "purchase": False},
    {"name": "Lose Race Gift", "id": base_id + 131, "inGameId": "RaceOpponent[9]", "needsShovel": False, "purchase": False},
]
