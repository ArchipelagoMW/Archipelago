WORLD_PATHS_JSON = [
    {
        "fromId": "massan",
        "toId": "massan_cave",
        "twoWay": True,
        "requiredItems": [
            "Axe Magic"
        ]
    },
    {
        "fromId": "massan",
        "toId": "massan_after_swamp_shrine",
        "requiredNodes": [
            "swamp_shrine"
        ]
    },
    {
        "fromId": "massan",
        "toId": "route_massan_gumi",
        "twoWay": True
    },
    {
        "fromId": "route_massan_gumi",
        "toId": "waterfall_shrine",
        "twoWay": True
    },
    {
        "fromId": "route_massan_gumi",
        "toId": "swamp_shrine",
        "twoWay": True,
        "weight": 2,
        "requiredItems": [
            "Idol Stone"
        ]
    },
    {
        "fromId": "route_massan_gumi",
        "toId": "gumi",
        "twoWay": True
    },
    {
        "fromId": "gumi",
        "toId": "gumi_after_swamp_shrine",
        "requiredNodes": [
            "swamp_shrine"
        ]
    },
    {
        "fromId": "gumi",
        "toId": "route_gumi_ryuma"
    },
    {
        "fromId": "route_gumi_ryuma",
        "toId": "ryuma",
        "twoWay": True
    },
    {
        "fromId": "route_gumi_ryuma",
        "toId": "tibor_tree",
        "twoWay": True
    },
    {
        "fromId": "route_gumi_ryuma",
        "toId": "mercator_gate_tree",
        "twoWay": True
    },
    {
        "fromId": "ryuma",
        "toId": "ryuma_after_thieves_hideout",
        "requiredNodes": [
            "thieves_hideout_post_key"
        ]
    },
    {
        "fromId": "ryuma",
        "toId": "ryuma_lighthouse_repaired",
        "twoWay": True,
        "requiredItems": [
            "Sun Stone"
        ]
    },
    {
        "fromId": "ryuma",
        "toId": "thieves_hideout_pre_key",
        "twoWay": True
    },
    {
        "fromId": "thieves_hideout_pre_key",
        "toId": "thieves_hideout_post_key",
        "requiredItems": [
            "Key"
        ]
    },
    {
        "fromId": "thieves_hideout_post_key",
        "toId": "thieves_hideout_pre_key"
    },
    {
        "fromId": "route_gumi_ryuma",
        "toId": "tibor",
        "twoWay": True
    },
    {
        "fromId": "route_gumi_ryuma",
        "toId": "helga_hut",
        "twoWay": True,
        "requiredItems": [
            "Einstein Whistle"
        ],
        "requiredNodes": [
            "massan"
        ]
    },
    {
        "fromId": "route_gumi_ryuma",
        "toId": "mercator",
        "twoWay": True,
        "weight": 2,
        "requiredItems": [
            "Safety Pass"
        ]
    },
    {
        "fromId": "mercator",
        "toId": "mercator_dungeon",
        "twoWay": True
    },
    {
        "fromId": "mercator",
        "toId": "crypt",
        "twoWay": True
    },
    {
        "fromId": "mercator",
        "toId": "mercator_special_shop",
        "twoWay": True,
        "requiredItems": [
            "Buyer Card"
        ]
    },
    {
        "fromId": "mercator",
        "toId": "mercator_casino",
        "twoWay": True,
        "requiredItems": [
            "Casino Ticket"
        ]
    },
    {
        "fromId": "mercator",
        "toId": "mir_tower_sector",
        "twoWay": True
    },
    {
        "fromId": "mir_tower_sector",
        "toId": "twinkle_village",
        "twoWay": True
    },
    {
        "fromId": "mir_tower_sector",
        "toId": "mir_tower_sector_tree_ledge",
        "twoWay": True,
        "requiredItems": [
            "Axe Magic"
        ]
    },
    {
        "fromId": "mir_tower_sector",
        "toId": "mir_tower_sector_tree_coast",
        "twoWay": True,
        "requiredItems": [
            "Axe Magic"
        ]
    },
    {
        "fromId": "mir_tower_sector",
        "toId": "mir_tower_pre_garlic",
        "requiredItems": [
            "Armlet"
        ]
    },
    {
        "fromId": "mir_tower_pre_garlic",
        "toId": "mir_tower_sector"
    },
    {
        "fromId": "mir_tower_pre_garlic",
        "toId": "mir_tower_post_garlic",
        "requiredItems": [
            "Garlic"
        ]
    },
    {
        "fromId": "mir_tower_post_garlic",
        "toId": "mir_tower_pre_garlic"
    },
    {
        "fromId": "mir_tower_post_garlic",
        "toId": "mir_tower_sector"
    },
    {
        "fromId": "mercator",
        "toId": "greenmaze_pre_whistle",
        "weight": 2,
        "requiredItems": [
            "Key"
        ]
    },
    {
        "fromId": "greenmaze_pre_whistle",
        "toId": "greenmaze_post_whistle",
        "requiredItems": [
            "Einstein Whistle"
        ]
    },
    {
        "fromId": "greenmaze_pre_whistle",
        "toId": "greenmaze_cutter",
        "requiredItems": [
            "EkeEke"
        ],
        "twoWay": True
    },
    {
        "fromId": "greenmaze_post_whistle",
        "toId": "greenmaze_post_whistle_tree",
        "twoWay": True
    },
    {
        "fromId": "greenmaze_post_whistle",
        "toId": "route_massan_gumi"
    },
    {
        "fromId": "mercator",
        "toId": "mercator_repaired_docks",
        "requiredNodes": [
            "ryuma_lighthouse_repaired"
        ]
    },
    {
        "fromId": "mercator_repaired_docks",
        "toId": "verla_shore"
    },
    {
        "fromId": "verla_shore",
        "toId": "verla",
        "twoWay": True
    },
    {
        "fromId": "verla",
        "toId": "verla_after_mines",
        "requiredNodes": [
            "verla_mines"
        ],
        "twoWay": True
    },
    {
        "fromId": "verla_shore",
        "toId": "verla_mines",
        "twoWay": True
    },
    {
        "fromId": "verla_mines",
        "toId": "verla_shore_cliff",
        "twoWay": True
    },
    {
        "fromId": "verla_shore_cliff",
        "toId": "verla_shore"
    },
    {
        "fromId": "verla_shore",
        "toId": "verla_shore_tree",
        "twoWay": True
    },
    {
        "fromId": "verla_shore",
        "toId": "mir_tower_sector",
        "requiredNodes": [
            "verla_mines"
        ],
        "twoWay": True
    },
    {
        "fromId": "verla_mines",
        "toId": "route_verla_destel"
    },
    {
        "fromId": "verla_mines",
        "toId": "verla_mines_behind_lava",
        "twoWay": True,
        "requiredItems": [
            "Fireproof"
        ]
    },
    {
        "fromId": "route_verla_destel",
        "toId": "destel",
        "twoWay": True
    },
    {
        "fromId": "destel",
        "toId": "route_after_destel",
        "twoWay": True
    },
    {
        "fromId": "destel",
        "toId": "destel_well",
        "twoWay": True
    },
    {
        "fromId": "destel_well",
        "toId": "route_lake_shrine",
        "twoWay": True
    },
    {
        "fromId": "route_lake_shrine",
        "toId": "lake_shrine",
        "itemsPlacedWhenCrossing": [
            "Sword of Gaia"
        ]
    },
    {
        "fromId": "lake_shrine",
        "toId": "route_lake_shrine"
    },
    {
        "fromId": "lake_shrine",
        "toId": "mir_tower_sector"
    },
    {
        "fromId": "greenmaze_pre_whistle",
        "toId": "mountainous_area",
        "twoWay": True,
        "requiredItems": [
            "Axe Magic"
        ]
    },
    {
        "fromId": "mountainous_area",
        "toId": "mountainous_area_tree",
        "twoWay": True
    },
    {
        "fromId": "mountainous_area",
        "toId": "route_lake_shrine_cliff",
        "twoWay": True,
        "requiredItems": [
            "Axe Magic"
        ]
    },
    {
        "fromId": "route_lake_shrine_cliff",
        "toId": "route_lake_shrine"
    },
    {
        "fromId": "mountainous_area",
        "toId": "king_nole_cave",
        "twoWay": True,
        "weight": 2,
        "requiredItems": [
            "Gola's Eye"
        ]
    },
    {
        "fromId": "king_nole_cave",
        "toId": "mercator"
    },
    {
        "fromId": "king_nole_cave",
        "toId": "kazalt",
        "itemsPlacedWhenCrossing": [
            "Lithograph"
        ]
    },
    {
        "fromId": "kazalt",
        "toId": "king_nole_cave"
    },
    {
        "fromId": "kazalt",
        "toId": "king_nole_labyrinth_pre_door",
        "twoWay": True
    },
    {
        "fromId": "king_nole_labyrinth_pre_door",
        "toId": "king_nole_labyrinth_post_door",
        "requiredItems": [
            "Key"
        ]
    },
    {
        "fromId": "king_nole_labyrinth_post_door",
        "toId": "king_nole_labyrinth_pre_door"
    },
    {
        "fromId": "king_nole_labyrinth_pre_door",
        "toId": "king_nole_labyrinth_exterior",
        "requiredItems": [
            "Iron Boots"
        ]
    },
    {
        "fromId": "king_nole_labyrinth_exterior",
        "toId": "king_nole_labyrinth_fall_from_exterior",
        "requiredItems": [
            "Axe Magic"
        ]
    },
    {
        "fromId": "king_nole_labyrinth_fall_from_exterior",
        "toId": "king_nole_labyrinth_pre_door"
    },
    {
        "fromId": "king_nole_labyrinth_post_door",
        "toId": "king_nole_labyrinth_raft_entrance",
        "requiredItems": [
            "Snow Spikes"
        ]
    },
    {
        "fromId": "king_nole_labyrinth_raft_entrance",
        "toId": "king_nole_labyrinth_post_door"
    },
    {
        "fromId": "king_nole_labyrinth_raft_entrance",
        "toId": "king_nole_labyrinth_raft",
        "requiredItems": [
            "Logs"
        ]
    },
    {
        "fromId": "king_nole_labyrinth_raft",
        "toId": "king_nole_labyrinth_raft_entrance"
    },
    {
        "fromId": "king_nole_labyrinth_post_door",
        "toId": "king_nole_labyrinth_path_to_palace",
        "requiredItems": [
            "Snow Spikes"
        ]
    },
    {
        "fromId": "king_nole_labyrinth_path_to_palace",
        "toId": "king_nole_labyrinth_post_door"
    },
    {
        "fromId": "king_nole_labyrinth_post_door",
        "toId": "king_nole_labyrinth_sacred_tree",
        "requiredItems": [
            "Axe Magic"
        ],
        "requiredNodes": [
            "king_nole_labyrinth_raft_entrance"
        ]
    },
    {
        "fromId": "king_nole_labyrinth_path_to_palace",
        "toId": "king_nole_palace",
        "twoWay": True
    },
    {
        "fromId": "king_nole_palace",
        "toId": "end",
        "requiredItems": [
            "Gola's Fang",
            "Gola's Horn",
            "Gola's Nail"
        ]
    }
]