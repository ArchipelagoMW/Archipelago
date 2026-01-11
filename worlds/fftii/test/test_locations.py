from Fill import distribute_items_restrictive
from .bases import FFTIITestBase

from ..data.items import zodiac_stone_names, world_map_pass_names, earned_job_names
from ..data.locations import (location_sort_list, job_unlock_locations, monster_location_names, world_map_regions,
                              gallione_regions, fovoham_regions, lesalia_regions, lionel_regions, zeltennia_regions,
                              limberry_regions, murond_regions)
from ..data.logic.FFTLocation import LocationNames
from ..data.logic.Monsters import monster_locations_lookup, monster_family_lookup, MonsterNames, monster_families

zodiac_stone_locations = [
    LocationNames.LIONEL_2_STORY.value,
    LocationNames.GOUG_STORY.value,
    LocationNames.RIOVANES_2_STORY.value,
    LocationNames.RIOVANES_3_STORY.value,
    LocationNames.BETHLA_SLUICE_STORY.value,
    LocationNames.LIMBERRY_2_STORY.value,
    LocationNames.LIMBERRY_3_STORY.value,
    LocationNames.IGROS_STORY.value,
]

zodiac_stone_locations_with_sidequests = [
    LocationNames.LIONEL_2_STORY.value,
    LocationNames.GOUG_STORY.value,
    LocationNames.RIOVANES_2_STORY.value,
    LocationNames.RIOVANES_3_STORY.value,
    LocationNames.BETHLA_SLUICE_STORY.value,
    LocationNames.LIMBERRY_2_STORY.value,
    LocationNames.LIMBERRY_3_STORY.value,
    LocationNames.IGROS_STORY.value,
    LocationNames.GOLAND_4_SIDEQUEST.value,
    LocationNames.NELVESKA_SIDEQUEST.value,
    LocationNames.END_SIDEQUEST.value
]

sidequest_names = [
    LocationNames.GOLAND_1_SIDEQUEST.value,
    LocationNames.GOLAND_2_SIDEQUEST.value,
    LocationNames.GOLAND_3_SIDEQUEST.value,
    LocationNames.GOLAND_4_SIDEQUEST.value,
    LocationNames.NELVESKA_SIDEQUEST.value,
    LocationNames.ZARGHIDAS_SIDEQUEST.value,
    LocationNames.NOGIAS_SIDEQUEST.value,
    LocationNames.TERMINATE_SIDEQUEST.value,
    LocationNames.DELTA_SIDEQUEST.value,
    LocationNames.VALKYRIES_SIDEQUEST.value,
    LocationNames.MLAPAN_SIDEQUEST.value,
    LocationNames.TIGER_SIDEQUEST.value,
    LocationNames.BRIDGE_SIDEQUEST.value,
    LocationNames.VOYAGE_SIDEQUEST.value,
    LocationNames.HORROR_SIDEQUEST.value,
    LocationNames.END_SIDEQUEST.value,
    LocationNames.BEOWULF_RECRUIT.value,
    LocationNames.WORKER_8_RECRUIT.value,
    LocationNames.REIS_DRAGON_RECRUIT.value,
    LocationNames.REIS_HUMAN_RECRUIT.value,
    LocationNames.CLOUD_RECRUIT.value,
    LocationNames.BYBLOS_RECRUIT.value
]

rare_battle_names = [
    LocationNames.MANDALIA_RARE.value,
    LocationNames.SWEEGY_RARE.value,
    LocationNames.LENALIA_RARE.value,
    LocationNames.FOVOHAM_RARE.value,
    LocationNames.YUGUO_RARE.value,
    LocationNames.GROG_RARE.value,
    LocationNames.BERVENIA_VOLCANO_RARE.value,
    LocationNames.ZEKLAUS_RARE.value,
    LocationNames.ARAGUAY_RARE.value,
    LocationNames.ZIREKILE_RARE.value,
    LocationNames.BARIAUS_HILL_RARE.value,
    LocationNames.BARIAUS_VALLEY_RARE.value,
    LocationNames.ZIGOLIS_RARE.value,
    LocationNames.DOGUOLA_RARE.value,
    LocationNames.FINATH_RARE.value,
    LocationNames.GERMINAS_RARE.value,
    LocationNames.BED_RARE.value,
    LocationNames.DOLBODAR_RARE.value,
    LocationNames.POESKAS_RARE.value
]

class TestAllRegionsReachable(FFTIITestBase):
    def test_regions_from_gallione(self):
        with self.subTest("Test all"):
            self.collect_by_name(world_map_pass_names)
            self.collect_by_name("Progressive Shop Level")
            self.collect_by_name(zodiac_stone_names)
            self.collect_by_name(earned_job_names)
            for region in world_map_regions:
                self.assertTrue(self.can_reach_region(region.name), region.name)
        with self.subTest("Test Fovoham regions"):
            self.remove_by_name(world_map_pass_names)
            self.collect_by_name("Fovoham Pass")
            for region in fovoham_regions:
                self.assertTrue(self.can_reach_region(region.name), region.name)
        with self.subTest("Test Lesalia regions"):
            self.remove_by_name(world_map_pass_names)
            self.collect_by_name("Lesalia Pass")
            for region in lesalia_regions:
                self.assertTrue(self.can_reach_region(region.name), region.name)
        with self.subTest("Test Lionel regions from Lesalia"):
            self.remove_by_name(world_map_pass_names)
            self.collect_by_name("Lesalia Pass")
            self.collect_by_name("Lionel Pass")
            for region in lionel_regions:
                self.assertTrue(self.can_reach_region(region.name), region.name)
        with self.subTest("Test Lionel regions from Murond"):
            self.remove_by_name(world_map_pass_names)
            self.collect_by_name("Murond Pass")
            self.collect_by_name("Lionel Pass")
            for region in lionel_regions:
                self.assertTrue(self.can_reach_region(region.name), region.name)
        with self.subTest("Test Zeltennia regions"):
            self.remove_by_name(world_map_pass_names)
            self.collect_by_name("Fovoham Pass")
            self.collect_by_name("Zeltennia Pass")
            for region in zeltennia_regions:
                self.assertTrue(self.can_reach_region(region.name), region.name)
        with self.subTest("Test Limberry regions"):
            self.remove_by_name(world_map_pass_names)
            self.collect_by_name("Lesalia Pass")
            self.collect_by_name("Limberry Pass")
            for region in limberry_regions:
                self.assertTrue(self.can_reach_region(region.name), region.name)
        with self.subTest("Test Murond regions"):
            self.remove_by_name(world_map_pass_names)
            self.collect_by_name("Murond Pass")
            self.collect_by_name("Lionel Pass")
            self.collect_by_name(zodiac_stone_names)
            for region in murond_regions:
                self.assertTrue(self.can_reach_region(region.name), region.name)

class TestZodiacStonesOnVanillaStones(FFTIITestBase):
    options = {
        "zodiac_stone_locations": 0,
        "zodiac_stones_in_pool": 13,
        "sidequest_battles": "false"
    }

    def test_stones_on_correct_locations(self) -> None:
        with self.subTest("Test stones are only on story locations"):
            self.world_setup()
            distribute_items_restrictive(self.multiworld)

            all_stones = []
            all_locations = self.multiworld.get_locations(self.player)
            for location in all_locations:
                if location.item.name in zodiac_stone_names:
                    all_stones.append(location.item)
            for stone in all_stones:
                if stone.location is not None:
                    self.assertTrue(stone.location.name in zodiac_stone_locations)

class TestZodiacStonesOnVanillaStonesWithSidequests(FFTIITestBase):
    options = {
        "zodiac_stone_locations": 0,
        "zodiac_stones_in_pool": 13,
        "sidequest_battles": "true"
    }

    def test_stones_on_correct_locations(self) -> None:
        with self.subTest("Test stones are only on story and sidequest locations"):
            self.world_setup()
            distribute_items_restrictive(self.multiworld)

            all_stones = []
            all_locations = self.multiworld.get_locations(self.player)
            for location in all_locations:
                if location.item.name in zodiac_stone_names:
                    all_stones.append(location.item)
            for stone in all_stones:
                if stone.location is not None:
                    self.assertTrue(stone.location.name in zodiac_stone_locations_with_sidequests)

class TestSidequestsNotInPoolWithOptionDisabled(FFTIITestBase):
    options = {
        "zodiac_stone_locations": 0,
        "zodiac_stones_in_pool": 13,
        "sidequest_battles": "false"
    }

    def test_sidequests_not_in_pool(self) -> None:
        with self.subTest("Test sidequests are not locations with option disabled."):
            all_locations = self.multiworld.get_locations(self.player)
            for location in all_locations:
                self.assertTrue(location.name not in sidequest_names)

class TestSidequestsInPoolWithOptionEnabled(FFTIITestBase):
    options = {
        "zodiac_stone_locations": 0,
        "zodiac_stones_in_pool": 13,
        "sidequest_battles": "true"
    }

    def test_sidequests_in_pool(self) -> None:
        with self.subTest("Test sidequests are locations with option enabled."):
            all_locations = self.multiworld.get_locations(self.player)
            all_location_names = [location.name for location in all_locations]
            for location_name in sidequest_names:
                self.assertTrue(location_name in all_location_names)


class TestRareBattlesNotInPoolWithOptionDisabled(FFTIITestBase):
    options = {
        "zodiac_stone_locations": 0,
        "zodiac_stones_in_pool": 13,
        "rare_battles": "false"
    }

    def test_rare_battles_not_in_pool(self) -> None:
        with self.subTest("Test rare battles are not locations with option disabled."):
            all_locations = self.multiworld.get_locations(self.player)
            for location in all_locations:
                self.assertTrue(location.name not in rare_battle_names)

class TestRareBattlesInPoolWithOptionEnabled(FFTIITestBase):
    options = {
        "zodiac_stone_locations": 0,
        "zodiac_stones_in_pool": 13,
        "rare_battles": "true"
    }

    def test_rare_battles_in_pool(self) -> None:
        with self.subTest("Test rare battles are locations with option enabled."):
            all_locations = self.multiworld.get_locations(self.player)
            all_location_names = [location.name for location in all_locations]
            for location_name in rare_battle_names:
                self.assertTrue(location_name in all_location_names)

class TestRegionLogicGallioneStart(FFTIITestBase):
    options = {
        #"starting_region": 0 # Gallione
        "sidequest_battles": "true",
        "rare_battles": "true",
        "final_battles": 0
    }

    run_default_tests = False

    def test_region_access(self) -> None:
        tested_locations = set()
        with self.subTest("Test Gallione Access"):
            test_locations = [
                LocationNames.GARILAND_STORY,
                LocationNames.MANDALIA_STORY,
                LocationNames.IGROS_STORY,
                LocationNames.THIEVES_FORT_STORY,
                LocationNames.SWEEGY_STORY,
                LocationNames.DORTER_1_STORY,
                LocationNames.DORTER_2_STORY,
                LocationNames.LENALIA_STORY,
                LocationNames.ZEAKDEN_STORY,
                LocationNames.MANDALIA_SHOP,
                LocationNames.LENALIA_SHOP,
                LocationNames.ZEAKDEN_SHOP,
                LocationNames.RAMZA_CHAPTER_2_UNLOCK,
                LocationNames.RAD_RECRUIT,
                LocationNames.ALICIA_RECRUIT,
                LocationNames.LAVIAN_RECRUIT,
                LocationNames.MANDALIA_RARE,
                LocationNames.SWEEGY_RARE,
                LocationNames.LENALIA_RARE
            ]
            tested_locations.update(set(test_locations))
            self.collect_by_name("Progressive Shop Level")
            self.collect_by_name(earned_job_names)
            location_names = [str(location.value) for location in test_locations]
            for location in location_names:
                self.assertTrue(self.world.get_location(location).can_reach(self.multiworld.state), location)

        with self.subTest("Test Fovoham Access"):
            test_locations = [
                LocationNames.FOVOHAM_STORY,
                LocationNames.RIOVANES_1_STORY,
                LocationNames.RIOVANES_2_STORY,
                LocationNames.RIOVANES_3_STORY,
                LocationNames.YUGUO_STORY,
                LocationNames.YARDOW_STORY,
                LocationNames.GROG_STORY,
                LocationNames.RIOVANES_SHOP,
                LocationNames.YARDOW_SHOP,
                LocationNames.RAMZA_CHAPTER_4_UNLOCK,
                LocationNames.RAFA_RECRUIT,
                LocationNames.MALAK_RECRUIT,
                LocationNames.FOVOHAM_RARE,
                LocationNames.YUGUO_RARE,
                LocationNames.GROG_RARE
            ]
            tested_locations.update(set(test_locations))
            location_names = [str(location.value) for location in test_locations]

            for location in location_names:
                self.assertFalse(self.world.get_location(location).can_reach(self.multiworld.state), location)
            self.collect_by_name("Fovoham Pass")
            for location in location_names:
                self.assertTrue(self.world.get_location(location).can_reach(self.multiworld.state), location)

        with self.subTest("Test Lesalia Access"):
            test_locations = [
                LocationNames.ZEKLAUS_STORY,
                LocationNames.ARAGUAY_STORY,
                LocationNames.ZIREKILE_STORY,
                LocationNames.GOLAND_STORY,
                LocationNames.LESALIA_STORY,
                LocationNames.ZEKLAUS_SHOP,
                LocationNames.ZIREKILE_SHOP,
                LocationNames.LESALIA_SHOP,
                LocationNames.BOCO_RECRUIT,
                LocationNames.GOLAND_1_SIDEQUEST,
                LocationNames.GOLAND_2_SIDEQUEST,
                LocationNames.GOLAND_3_SIDEQUEST,
                LocationNames.GOLAND_4_SIDEQUEST,
                LocationNames.BEOWULF_RECRUIT,
                LocationNames.REIS_DRAGON_RECRUIT,
                LocationNames.WORKER_8_RECRUIT,
                LocationNames.BERVENIA_VOLCANO_RARE,
                LocationNames.ZEKLAUS_RARE,
                LocationNames.ARAGUAY_RARE,
                LocationNames.ZIREKILE_RARE
            ]
            tested_locations.update(set(test_locations))
            location_names = [str(location.value) for location in test_locations]

            for location in location_names:
                self.assertFalse(self.world.get_location(location).can_reach(self.multiworld.state), location)
            self.remove_by_name(world_map_pass_names)
            self.collect_by_name("Lesalia Pass")
            for location in location_names:
                self.assertTrue(self.world.get_location(location).can_reach(self.multiworld.state), location)

        with self.subTest("Test Lionel Access From Lesalia"):
            test_locations = [
                LocationNames.ZALAND_STORY,
                LocationNames.BARIAUS_HILL_STORY,
                LocationNames.LIONEL_1_STORY,
                LocationNames.LIONEL_2_STORY,
                LocationNames.BARIAUS_VALLEY_STORY,
                LocationNames.GOLGORAND_STORY,
                LocationNames.ZIGOLIS_STORY,
                LocationNames.BARIAUS_HILL_SHOP,
                LocationNames.LIONEL_SHOP,
                LocationNames.BARIAUS_VALLEY_SHOP,
                LocationNames.AGRIAS_RECRUIT,
                LocationNames.BARIAUS_HILL_RARE,
                LocationNames.BARIAUS_VALLEY_RARE,
                LocationNames.ZIGOLIS_RARE
            ]
            tested_locations.update(set(test_locations))
            location_names = [str(location.value) for location in test_locations]

            self.remove_by_name(world_map_pass_names)
            for location in location_names:
                self.assertFalse(self.world.get_location(location).can_reach(self.multiworld.state), location)
            self.collect_by_name("Lionel Pass")
            for location in location_names:
                self.assertFalse(self.world.get_location(location).can_reach(self.multiworld.state), location)
            self.collect_by_name("Lesalia Pass")
            for location in location_names:
                self.assertTrue(self.world.get_location(location).can_reach(self.multiworld.state), location)

        with self.subTest("Test Lionel Access From Murond"):
            test_locations = [
                LocationNames.ZALAND_STORY,
                LocationNames.BARIAUS_HILL_STORY,
                LocationNames.LIONEL_1_STORY,
                LocationNames.LIONEL_2_STORY,
                LocationNames.BARIAUS_VALLEY_STORY,
                LocationNames.GOLGORAND_STORY,
                LocationNames.ZIGOLIS_STORY,
                LocationNames.BARIAUS_HILL_SHOP,
                LocationNames.LIONEL_SHOP,
                LocationNames.BARIAUS_VALLEY_SHOP,
                LocationNames.AGRIAS_RECRUIT,
                LocationNames.BARIAUS_HILL_RARE,
                LocationNames.BARIAUS_VALLEY_RARE,
                LocationNames.ZIGOLIS_RARE
            ]
            tested_locations.update(set(test_locations))
            location_names = [str(location.value) for location in test_locations]

            self.remove_by_name(world_map_pass_names)
            for location in location_names:
                self.assertFalse(self.world.get_location(location).can_reach(self.multiworld.state), location)
            self.collect_by_name("Lionel Pass")
            for location in location_names:
                self.assertFalse(self.world.get_location(location).can_reach(self.multiworld.state), location)
            self.collect_by_name("Murond Pass")
            for location in location_names:
                self.assertTrue(self.world.get_location(location).can_reach(self.multiworld.state), location)

        with self.subTest("Test Zeltennia Access"):
            test_locations = [
                LocationNames.DOGUOLA_STORY,
                LocationNames.BERVENIA_CITY_STORY,
                LocationNames.FINATH_STORY,
                LocationNames.ZELTENNIA_STORY,
                LocationNames.GERMINAS_STORY,
                LocationNames.NELVESKA_SIDEQUEST,
                LocationNames.ZARGHIDAS_SIDEQUEST,
                LocationNames.REIS_HUMAN_RECRUIT,
                LocationNames.CLOUD_RECRUIT,
                LocationNames.DOGUOLA_RARE,
                LocationNames.FINATH_RARE,
                LocationNames.GERMINAS_RARE
            ]
            tested_locations.update(set(test_locations))
            location_names = [str(location.value) for location in test_locations]

            self.remove_by_name(world_map_pass_names)
            for location in location_names:
                self.assertFalse(self.world.get_location(location).can_reach(self.multiworld.state), location)
            self.collect_by_name("Zeltennia Pass")
            for location in location_names:
                self.assertFalse(self.world.get_location(location).can_reach(self.multiworld.state), location)
            self.collect_by_name("Fovoham Pass")
            for location in location_names:
                self.assertTrue(self.world.get_location(location).can_reach(self.multiworld.state), location)

        with self.subTest("Test Limberry Access"):
            test_locations = [
                LocationNames.BED_STORY,
                LocationNames.BETHLA_NORTH_STORY,
                LocationNames.BETHLA_SOUTH_STORY,
                LocationNames.BETHLA_SLUICE_STORY,
                LocationNames.POESKAS_STORY,
                LocationNames.LIMBERRY_1_STORY,
                LocationNames.LIMBERRY_2_STORY,
                LocationNames.LIMBERRY_3_STORY,
                LocationNames.BETHLA_SHOP,
                LocationNames.LIMBERRY_SHOP,
                LocationNames.ORLANDU_RECRUIT,
                LocationNames.MELIADOUL_RECRUIT,
                LocationNames.BED_RARE,
                LocationNames.POESKAS_RARE,
                LocationNames.DOLBODAR_RARE
            ]
            tested_locations.update(set(test_locations))
            location_names = [str(location.value) for location in test_locations]

            self.remove_by_name(world_map_pass_names)
            for location in location_names:
                self.assertFalse(self.world.get_location(location).can_reach(self.multiworld.state), location)
            self.collect_by_name("Limberry Pass")
            for location in location_names:
                self.assertFalse(self.world.get_location(location).can_reach(self.multiworld.state), location)
            self.collect_by_name("Lesalia Pass")
            for location in location_names:
                self.assertTrue(self.world.get_location(location).can_reach(self.multiworld.state), location)

        with self.subTest("Test Murond Access"):
            test_locations_west = [
                LocationNames.MUROND_TEMPLE_1_STORY,
                LocationNames.MUROND_TEMPLE_2_STORY,
                LocationNames.MUROND_TEMPLE_3_STORY,
                LocationNames.GOUG_STORY,
                LocationNames.UBS_1_STORY,
                LocationNames.UBS_2_STORY,
                LocationNames.UBS_3_STORY,
                LocationNames.ORBONNE_SHOP,
                LocationNames.MUSTADIO_RECRUIT
            ]
            tested_locations.update(set(test_locations_west))
            test_locations_east = [
                LocationNames.UBS_4_STORY,
                LocationNames.UBS_5_STORY,
                LocationNames.MUROND_DEATH_CITY_STORY,
                LocationNames.PRECINCTS_STORY,
                LocationNames.AIRSHIPS_1_STORY,
                LocationNames.AIRSHIPS_2_STORY,
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
                LocationNames.BYBLOS_RECRUIT
            ]
            tested_locations.update(set(test_locations_east))
            location_names_west = [str(location.value) for location in test_locations_west]
            location_names_east = [str(location.value) for location in test_locations_east]

            self.remove_by_name(world_map_pass_names)
            for location in [*location_names_west, *location_names_east]:
                self.assertFalse(self.world.get_location(location).can_reach(self.multiworld.state), location)
            self.collect_by_name("Murond Pass")
            for location in location_names_east:
                self.assertFalse(self.world.get_location(location).can_reach(self.multiworld.state), location)
            for location in location_names_west:
                self.assertTrue(self.world.get_location(location).can_reach(self.multiworld.state), location)
            self.collect_by_name("Lionel Pass")
            for location in [*location_names_west, *location_names_east]:
                self.assertTrue(self.world.get_location(location).can_reach(self.multiworld.state), location)

        with self.subTest("Test All Locations Were Tested"):
            for location in location_sort_list:
                if location not in job_unlock_locations:
                    self.assertTrue(location in tested_locations, location)

class TestRegionLogicGallioneStartAltimaOnly(FFTIITestBase):
    options = {
        #"starting_region": 0 # Gallione
        "sidequest_battles": "true",
        "rare_battles": "true",
        "final_battles": 1
    }

    run_default_tests = False

    def test_region_access(self) -> None:
        with self.subTest("Test Murond Access"):
            test_locations_west = [
                LocationNames.MUROND_TEMPLE_1_STORY,
                LocationNames.MUROND_TEMPLE_2_STORY,
                LocationNames.MUROND_TEMPLE_3_STORY,
                LocationNames.GOUG_STORY,
                LocationNames.UBS_1_STORY,
                LocationNames.UBS_2_STORY,
                LocationNames.UBS_3_STORY,
                LocationNames.UBS_4_STORY,
                LocationNames.UBS_5_STORY,
                LocationNames.MUROND_DEATH_CITY_STORY,
                LocationNames.PRECINCTS_STORY,
                LocationNames.AIRSHIPS_1_STORY,
                LocationNames.ORBONNE_SHOP,
                LocationNames.MUSTADIO_RECRUIT
            ]
            test_locations_east = [
                LocationNames.AIRSHIPS_2_STORY,
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
                LocationNames.BYBLOS_RECRUIT
            ]
            location_names_west = [str(location.value) for location in test_locations_west]
            location_names_east = [str(location.value) for location in test_locations_east]

            self.collect_all_but(["Murond Pass", "Lionel Pass"])
            for location in [*location_names_west, *location_names_east]:
                self.assertFalse(self.world.get_location(location).can_reach(self.multiworld.state), location)
            self.collect_by_name("Murond Pass")
            for location in location_names_east:
                self.assertFalse(self.world.get_location(location).can_reach(self.multiworld.state), location)
            for location in location_names_west:
                self.assertTrue(self.world.get_location(location).can_reach(self.multiworld.state), location)
            self.collect_by_name("Lionel Pass")
            for location in [*location_names_west, *location_names_east]:
                self.assertTrue(self.world.get_location(location).can_reach(self.multiworld.state), location)

class TestPoachLogicWithGallioneStart(FFTIITestBase):
    options = {
        "poach_locations": "true",
        "job_unlocks": "true",
        "sidequest_battles": "true"
    }

    run_default_tests = False

    def test_jobs_required(self):
        with self.subTest("Test Thief required"):
            self.assertAccessDependency(
                monster_location_names,
                [["Thief"]],
                only_check_listed=True,
            )
        with self.subTest("Test Mediator and Thief required for Wildbow"):
            self.assertAccessDependency(
                ["Poach Wildbow"],
                [["Thief", "Mediator"]],
                only_check_listed=True
            )
        with self.subTest("Test passes required"):
            self.assertAccessDependency(
                ["Poach Porky"],
                [
                    ["Lesalia Pass", "Limberry Pass", "Thief"],
                    ["Fovoham Pass", "Zeltennia Pass", "Limberry Pass", "Thief"],
                    ["Fovoham Pass", "Zeltennia Pass", "Thief", "Mediator"],
                    ["Lesalia Pass", "Lionel Pass", "Thief", "Mediator"]
                ],
                only_check_listed=True
            )

    def test_gallione_monsters(self):
        self.collect_by_name("Progressive Shop Level")
        self.collect_by_name(earned_job_names)
        with self.subTest("Test Thief logic"):
            self.collect_by_name("Thief")
            for monster_location in monster_location_names:
                monster_data = monster_locations_lookup[monster_location[6:]]
                if len(monster_data.gallione_locations) > 0:
                    self.assertTrue(self.can_reach_location(monster_location), monster_location)
                self.collect_by_name("Fovoham Pass")
                if len(monster_data.fovoham_locations) > 0:
                    self.assertTrue(self.can_reach_location(monster_location), monster_location)
                #self.remove_by_name("Fovoham Pass")
                self.collect_by_name("Lesalia Pass")
                if len(monster_data.lesalia_locations) > 0:
                    self.assertTrue(self.can_reach_location(monster_location), monster_location)
                self.remove_by_name("Fovoham Pass")
                self.collect_by_name("Lionel Pass")
                if len(monster_data.lionel_locations) > 0:
                    self.assertTrue(self.can_reach_location(monster_location), monster_location)
                self.remove_by_name("Lionel Pass")
                self.collect_by_name("Fovoham Pass")
                self.collect_by_name("Zeltennia Pass")
                if len(monster_data.zeltennia_locations) > 0:
                    self.assertTrue(self.can_reach_location(monster_location), monster_location)
                self.remove_by_name("Zeltennia Pass")
                self.collect_by_name("Limberry Pass")
                if len(monster_data.limberry_locations) > 0:
                    self.assertTrue(self.can_reach_location(monster_location), monster_location)
        with self.subTest("Test Mediator logic"):
            self.remove_by_name(world_map_pass_names)
            self.collect_by_name("Mediator")
            for monster_location in monster_location_names:
                monster_name = monster_location[6:]
                monster_family_name = monster_family_lookup[MonsterNames(monster_name)]
                monster_family_values = monster_families[monster_family_name]
                monster_datas = []
                for monster in monster_family_values:
                    monster_datas.append(monster_locations_lookup[monster.value])
                if any([
                    len(monster_datas[0].gallione_locations) > 0,
                    len(monster_datas[1].gallione_locations) > 0,
                    len(monster_datas[2].gallione_locations) > 0,
                ]):
                    self.assertTrue(self.can_reach_location(monster_location), monster_location)
                self.collect_by_name("Fovoham Pass")
                if any([
                    len(monster_datas[0].fovoham_locations) > 0,
                    len(monster_datas[1].fovoham_locations) > 0,
                    len(monster_datas[2].fovoham_locations) > 0,
                ]):
                    self.assertTrue(self.can_reach_location(monster_location), monster_location)
                self.remove_by_name("Fovoham Pass")
                # self.remove_by_name("Fovoham Pass")
                self.collect_by_name("Lesalia Pass")
                if any([
                    len(monster_datas[0].lesalia_locations) > 0,
                    len(monster_datas[1].lesalia_locations) > 0,
                    len(monster_datas[2].lesalia_locations) > 0,
                ]):
                    self.assertTrue(self.can_reach_location(monster_location), monster_location)
                self.collect_by_name("Lionel Pass")
                if any([
                    len(monster_datas[0].lionel_locations) > 0,
                    len(monster_datas[1].lionel_locations) > 0,
                    len(monster_datas[2].lionel_locations) > 0,
                ]):
                    self.assertTrue(self.can_reach_location(monster_location), monster_location)
                self.remove_by_name("Lionel Pass")
                self.collect_by_name("Fovoham Pass")
                self.collect_by_name("Zeltennia Pass")
                if any([
                    len(monster_datas[0].zeltennia_locations) > 0,
                    len(monster_datas[1].zeltennia_locations) > 0,
                    len(monster_datas[2].zeltennia_locations) > 0,
                ]):
                    self.assertTrue(self.can_reach_location(monster_location), monster_location)
                self.remove_by_name("Zeltennia Pass")
                self.collect_by_name("Limberry Pass")
                if any([
                    len(monster_datas[0].limberry_locations) > 0,
                    len(monster_datas[1].limberry_locations) > 0,
                    len(monster_datas[2].limberry_locations) > 0,
                ]):
                    self.assertTrue(self.can_reach_location(monster_location), monster_location)