from .logic.FFTLocation import LocationNames
from .logic.FFTRegion import FFTRegion
from .logic.Monsters import monster_locations
from .logic.regions.Fovoham import fovoham_regions
from .logic.regions.Gallione import gallione_regions
from .logic.regions.Jobs import jobs_regions
from .logic.regions.Lesalia import lesalia_regions
from .logic.regions.Limberry import limberry_regions
from .logic.regions.Lionel import lionel_regions
from .logic.regions.Murond import murond_regions
from .logic.regions.Zeltennia import zeltennia_regions

world_map_regions: list[FFTRegion] = [
    *gallione_regions,
    *fovoham_regions,
    *lesalia_regions,
    *lionel_regions,
    *zeltennia_regions,
    *limberry_regions,
    *murond_regions
]

menu_regions: list[FFTRegion] = [
    *jobs_regions
]

all_regions: list[FFTRegion] = [
    *world_map_regions, *menu_regions
]

story_battle_locations: list[LocationNames] = [
    LocationNames.GARILAND_STORY,
    LocationNames.MANDALIA_STORY,
    LocationNames.IGROS_STORY,
    LocationNames.SWEEGY_STORY,
    LocationNames.DORTER_1_STORY,
    LocationNames.DORTER_2_STORY,
    LocationNames.THIEVES_FORT_STORY,
    LocationNames.LENALIA_STORY,
    LocationNames.ZEAKDEN_STORY,
    LocationNames.GROG_STORY,
    LocationNames.YARDOW_STORY,
    LocationNames.YUGUO_STORY,
    LocationNames.RIOVANES_1_STORY,
    LocationNames.RIOVANES_2_STORY,
    LocationNames.RIOVANES_3_STORY,
    LocationNames.FOVOHAM_STORY,
    LocationNames.ARAGUAY_STORY,
    LocationNames.ZIREKILE_STORY,
    LocationNames.ZEKLAUS_STORY,
    LocationNames.LESALIA_STORY,
    LocationNames.GOLAND_STORY,
    LocationNames.ZALAND_STORY,
    LocationNames.BARIAUS_HILL_STORY,
    LocationNames.LIONEL_1_STORY,
    LocationNames.LIONEL_2_STORY,
    LocationNames.ZIGOLIS_STORY,
    LocationNames.GOLGORAND_STORY,
    LocationNames.BARIAUS_VALLEY_STORY,
    LocationNames.DOGUOLA_STORY,
    LocationNames.BERVENIA_CITY_STORY,
    LocationNames.FINATH_STORY,
    LocationNames.ZELTENNIA_STORY,
    LocationNames.GERMINAS_STORY,
    LocationNames.BETHLA_NORTH_STORY,
    LocationNames.BETHLA_SOUTH_STORY,
    LocationNames.BETHLA_SLUICE_STORY,
    LocationNames.BED_STORY,
    LocationNames.LIMBERRY_1_STORY,
    LocationNames.LIMBERRY_2_STORY,
    LocationNames.LIMBERRY_3_STORY,
    LocationNames.POESKAS_STORY,
    LocationNames.MUROND_TEMPLE_1_STORY,
    LocationNames.MUROND_TEMPLE_2_STORY,
    LocationNames.MUROND_TEMPLE_3_STORY,
    LocationNames.UBS_1_STORY,
    LocationNames.UBS_2_STORY,
    LocationNames.UBS_3_STORY,
    LocationNames.UBS_4_STORY,
    LocationNames.UBS_5_STORY,
    LocationNames.GOUG_STORY,
    LocationNames.MUROND_DEATH_CITY_STORY,
    LocationNames.PRECINCTS_STORY,
    LocationNames.AIRSHIPS_1_STORY,
    LocationNames.AIRSHIPS_2_STORY
]

story_character_recruit_locations: list[LocationNames] = [
    LocationNames.RAD_RECRUIT,
    LocationNames.ALICIA_RECRUIT,
    LocationNames.LAVIAN_RECRUIT,
    LocationNames.BOCO_RECRUIT,
    LocationNames.MUSTADIO_RECRUIT,
    LocationNames.AGRIAS_RECRUIT,
    LocationNames.RAFA_RECRUIT,
    LocationNames.MALAK_RECRUIT,
    LocationNames.ORLANDU_RECRUIT,
    LocationNames.MELIADOUL_RECRUIT
]

character_recruit_locations: list[LocationNames] = [
    LocationNames.RAD_RECRUIT,
    LocationNames.ALICIA_RECRUIT,
    LocationNames.LAVIAN_RECRUIT,
    LocationNames.RAFA_RECRUIT,
    LocationNames.MALAK_RECRUIT,
    LocationNames.BOCO_RECRUIT,
    LocationNames.BEOWULF_RECRUIT,
    LocationNames.WORKER_8_RECRUIT,
    LocationNames.AGRIAS_RECRUIT,
    LocationNames.REIS_DRAGON_RECRUIT,
    LocationNames.REIS_HUMAN_RECRUIT,
    LocationNames.CLOUD_RECRUIT,
    LocationNames.ORLANDU_RECRUIT,
    LocationNames.MELIADOUL_RECRUIT,
    LocationNames.MUSTADIO_RECRUIT,
    LocationNames.BYBLOS_RECRUIT
]

sidequest_battles: list[LocationNames] = [
    LocationNames.GOLAND_1_SIDEQUEST,
    LocationNames.GOLAND_2_SIDEQUEST,
    LocationNames.GOLAND_3_SIDEQUEST,
    LocationNames.GOLAND_4_SIDEQUEST,
    LocationNames.NELVESKA_SIDEQUEST,
    LocationNames.ZARGHIDAS_SIDEQUEST,
    LocationNames.NOGIAS_SIDEQUEST,
    LocationNames.TERMINATE_SIDEQUEST,
    LocationNames.DELTA_SIDEQUEST,
    LocationNames.VALKYRIES_SIDEQUEST,
    LocationNames.MLAPAN_SIDEQUEST,
    LocationNames.TIGER_SIDEQUEST,
    LocationNames.BRIDGE_SIDEQUEST,
    LocationNames.VOYAGE_SIDEQUEST,
    LocationNames.HORROR_SIDEQUEST,
    LocationNames.END_SIDEQUEST,
]

dd_locations: list[LocationNames] = [
    LocationNames.NOGIAS_SIDEQUEST,
    LocationNames.TERMINATE_SIDEQUEST,
    LocationNames.DELTA_SIDEQUEST,
    LocationNames.VALKYRIES_SIDEQUEST,
    LocationNames.MLAPAN_SIDEQUEST,
    LocationNames.TIGER_SIDEQUEST,
    LocationNames.BRIDGE_SIDEQUEST,
    LocationNames.VOYAGE_SIDEQUEST,
    LocationNames.HORROR_SIDEQUEST,
    LocationNames.END_SIDEQUEST,
]

dd_location_names: list[str] = [location.value for location in dd_locations]

sidequest_battle_locations: list[LocationNames] = [
    *sidequest_battles,
    LocationNames.BEOWULF_RECRUIT,
    LocationNames.WORKER_8_RECRUIT,
    LocationNames.REIS_DRAGON_RECRUIT,
    LocationNames.REIS_HUMAN_RECRUIT,
    LocationNames.CLOUD_RECRUIT,
    LocationNames.BYBLOS_RECRUIT
]

rare_battle_locations: list[LocationNames] = [
    LocationNames.MANDALIA_RARE,
    LocationNames.SWEEGY_RARE,
    LocationNames.LENALIA_RARE,
    LocationNames.GROG_RARE,
    LocationNames.YUGUO_RARE,
    LocationNames.FOVOHAM_RARE,
    LocationNames.ARAGUAY_RARE,
    LocationNames.ZIREKILE_RARE,
    LocationNames.ZEKLAUS_RARE,
    LocationNames.BERVENIA_VOLCANO_RARE,
    LocationNames.DOGUOLA_RARE,
    LocationNames.BARIAUS_HILL_RARE,
    LocationNames.ZIGOLIS_RARE,
    LocationNames.BARIAUS_VALLEY_RARE,
    LocationNames.FINATH_RARE,
    LocationNames.GERMINAS_RARE,
    LocationNames.BED_RARE,
    LocationNames.DOLBODAR_RARE,
    LocationNames.POESKAS_RARE
]

rare_battle_location_names: list[str] = [location.value for location in rare_battle_locations]

job_unlock_locations: list[LocationNames] = [
    LocationNames.SQUIRE_UNLOCK,
    LocationNames.CHEMIST_UNLOCK,
    LocationNames.KNIGHT_UNLOCK,
    LocationNames.ARCHER_UNLOCK,
    LocationNames.THIEF_UNLOCK,
    LocationNames.MONK_UNLOCK,
    LocationNames.PRIEST_UNLOCK,
    LocationNames.WIZARD_UNLOCK,
    LocationNames.TIME_MAGE_UNLOCK,
    LocationNames.SUMMONER_UNLOCK,
    LocationNames.ORACLE_UNLOCK,
    LocationNames.MEDIATOR_UNLOCK,
    LocationNames.GEOMANCER_UNLOCK,
    LocationNames.LANCER_UNLOCK,
    LocationNames.SAMURAI_UNLOCK,
    LocationNames.NINJA_UNLOCK,
    LocationNames.CALCULATOR_UNLOCK,
    LocationNames.BARD_UNLOCK,
    LocationNames.DANCER_UNLOCK,
    LocationNames.MIME_UNLOCK
]

shop_unlock_locations: list[LocationNames] = [
    LocationNames.MANDALIA_SHOP,
    LocationNames.LENALIA_SHOP,
    LocationNames.ZEAKDEN_SHOP,
    LocationNames.YARDOW_SHOP,
    LocationNames.RIOVANES_SHOP,
    LocationNames.ZIREKILE_SHOP,
    LocationNames.ZEKLAUS_SHOP,
    LocationNames.LESALIA_SHOP,
    LocationNames.BARIAUS_HILL_SHOP,
    LocationNames.LIONEL_SHOP,
    LocationNames.BARIAUS_VALLEY_SHOP,
    LocationNames.BETHLA_SHOP,
    LocationNames.LIMBERRY_SHOP,
    LocationNames.ORBONNE_SHOP
]

ramza_job_unlock_locations: list[LocationNames] = [
    LocationNames.RAMZA_CHAPTER_2_UNLOCK,
    LocationNames.RAMZA_CHAPTER_4_UNLOCK
]

default_murond_fights: list[LocationNames] = [
    LocationNames.UBS_4_STORY,
    LocationNames.UBS_5_STORY,
    LocationNames.MUROND_DEATH_CITY_STORY,
    LocationNames.PRECINCTS_STORY,
    LocationNames.AIRSHIPS_1_STORY
]

story_zodiac_stone_locations: list[LocationNames] = [
    LocationNames.IGROS_STORY, # Capricorn
    LocationNames.RIOVANES_3_STORY, # Pisces
    LocationNames.RIOVANES_2_STORY, # Aries
    LocationNames.GOUG_STORY, # Taurus
    LocationNames.LIMBERRY_2_STORY, # Gemini
    # "Graveyard of Airships 1 Story Battle", # Leo
    # "Graveyard of Airships 2 Story Battle", # Virgo
    LocationNames.BETHLA_SLUICE_STORY, # Libra
    LocationNames.LIONEL_2_STORY, # Scorpio
    LocationNames.LIMBERRY_3_STORY, # Sagittarius
]

altima_only_story_zodiac_stone_locations: list[LocationNames] = [
    LocationNames.AIRSHIPS_1_STORY
]

sidequest_zodiac_stone_locations: list[LocationNames] = [
    LocationNames.GOLAND_4_SIDEQUEST,
    LocationNames.NELVESKA_SIDEQUEST,
    LocationNames.END_SIDEQUEST,
]

linked_rewards: dict[LocationNames, list[LocationNames]] = {
    LocationNames.MANDALIA_STORY: [
        LocationNames.MANDALIA_SHOP
    ],
    LocationNames.LENALIA_STORY: [
        LocationNames.LENALIA_SHOP,
    ],
    LocationNames.ZEAKDEN_STORY: [
        LocationNames.ZEAKDEN_SHOP,
        LocationNames.RAMZA_CHAPTER_2_UNLOCK,
        LocationNames.RAD_RECRUIT,
        LocationNames.ALICIA_RECRUIT,
        LocationNames.LAVIAN_RECRUIT
    ],
    LocationNames.YARDOW_STORY: [
        LocationNames.YARDOW_SHOP
    ],
    LocationNames.RIOVANES_3_STORY: [
        LocationNames.RIOVANES_SHOP,
        LocationNames.RAFA_RECRUIT,
        LocationNames.MALAK_RECRUIT,
        LocationNames.RAMZA_CHAPTER_4_UNLOCK
    ],
    LocationNames.ZIREKILE_STORY: [
        LocationNames.ZIREKILE_SHOP
    ],
    LocationNames.ZEKLAUS_STORY: [
        LocationNames.ZEKLAUS_SHOP
    ],
    LocationNames.ARAGUAY_STORY: [
        LocationNames.BOCO_RECRUIT
    ],
    LocationNames.GOLAND_4_SIDEQUEST: [
        LocationNames.BEOWULF_RECRUIT,
        LocationNames.REIS_DRAGON_RECRUIT,
        LocationNames.WORKER_8_RECRUIT
    ],
    LocationNames.LESALIA_STORY: [
        LocationNames.LESALIA_SHOP
    ],
    LocationNames.BARIAUS_HILL_STORY: [
        LocationNames.BARIAUS_HILL_SHOP
    ],
    LocationNames.LIONEL_2_STORY: [
        LocationNames.LIONEL_SHOP
    ],
    LocationNames.BARIAUS_VALLEY_STORY: [
        LocationNames.BARIAUS_VALLEY_SHOP,
        LocationNames.AGRIAS_RECRUIT
    ],
    LocationNames.NELVESKA_SIDEQUEST: [
        LocationNames.REIS_HUMAN_RECRUIT
    ],
    LocationNames.ZARGHIDAS_SIDEQUEST: [
        LocationNames.CLOUD_RECRUIT
    ],
    LocationNames.BETHLA_SLUICE_STORY: [
        LocationNames.BETHLA_SHOP,
        LocationNames.ORLANDU_RECRUIT
    ],
    LocationNames.LIMBERRY_3_STORY: [
        LocationNames.LIMBERRY_SHOP,
        LocationNames.MELIADOUL_RECRUIT
    ],
    LocationNames.UBS_1_STORY: [
        LocationNames.ORBONNE_SHOP
    ],
    LocationNames.GOUG_STORY: [
        LocationNames.MUSTADIO_RECRUIT
    ],
    LocationNames.END_SIDEQUEST: [
        LocationNames.BYBLOS_RECRUIT
    ]
}

linked_reward_names: dict[str, list[str]] = {}
for location, value in linked_rewards.items():
    new_list = []
    for linked_location in value:
        new_list.append(linked_location.value)
    linked_reward_names[location.value] = new_list


locations_with_text: list[str] = []

for location in story_battle_locations:
    locations_with_text.append(location.value)

for location in sidequest_battles:
    locations_with_text.append(location.value)

for location in rare_battle_locations:
    locations_with_text.append(location.value)

monster_location_names: list[str] = [f"Poach {monster.monster_name.value}" for monster in monster_locations]

location_sort_list: list[LocationNames] = [
    *story_battle_locations,
    *shop_unlock_locations,
    *ramza_job_unlock_locations,
    *character_recruit_locations,
    *sidequest_battles,
    *rare_battle_locations,
    *job_unlock_locations
]

location_sort_list_names: list[str] = [
    location.value for location in location_sort_list
]

location_groups = {
    "Story Battles": [
        location.value for location in [
            *story_battle_locations,
            *shop_unlock_locations,
            *ramza_job_unlock_locations,
            *story_character_recruit_locations
        ]
    ],
    "Sidequest Battles": [location.value for location in sidequest_battles],
    "Rare Battles": rare_battle_location_names,
    "Poaches": monster_location_names,
    "Job Unlocks": [location.value for location in job_unlock_locations]
}