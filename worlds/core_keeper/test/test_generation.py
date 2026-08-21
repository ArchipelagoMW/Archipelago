from BaseClasses import CollectionState

from .bases import CoreKeeperTestBase
from ..items import ITEM_NAME_TO_ID
from ..locations import LOCATION_METADATA
from ..options import LICENSE_OPTIONS


NO_LICENSES = {option_name: False for _, option_name, _ in LICENSE_OPTIONS}
ALL_LICENSES = {option_name: True for _, option_name, _ in LICENSE_OPTIONS}


class TestMainVersionSlice(CoreKeeperTestBase):
    def test_location_and_item_counts_match(self) -> None:
        self.assertEqual(
            len(self.multiworld.get_unfilled_locations(self.player)),
            len([item for item in self.multiworld.itempool if item.player == self.player]),
        )

    def test_default_weighted_caches_fill_every_filler_slot(self) -> None:
        player_items = [
            item for item in self.multiworld.itempool if item.player == self.player
        ]
        self.assertEqual(0, sum(item.name == "Empty Cache" for item in player_items))
        self.assertTrue(any(item.name.endswith("Cache") for item in player_items))

    def test_keys_are_natural_checks_not_archipelago_rewards(self) -> None:
        reward_names = {
            item.name
            for item in self.multiworld.itempool
            if item.player == self.player and item.name.endswith(" Key")
        }
        self.assertEqual(set(), reward_names)
        location_names = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertIn("Collect Copper Key", location_names)
        self.assertIn("Collect Iron Key", location_names)

    def test_slot_data_is_plain_json_data(self) -> None:
        slot_data = self.world.fill_slot_data()
        self.assertEqual(1, slot_data["slot_data_version"])
        self.assertEqual(23543556, slot_data["core_keeper_steam_build_id"])
        self.assertEqual(10, len(slot_data["enabled_licenses"]))
        self.assertEqual(3.0, slot_data["skill_xp_multiplier"])
        self.assertFalse(slot_data["skill_points"])
        for key in (
            "soul_seeker_cache", "titan_breath_cache", "phantom_spark_cache",
            "rune_song_cache", "credence_of_ruin_cache", "stormbringer_cache",
        ):
            self.assertTrue(slot_data[key])
        self.assertEqual(0, slot_data["empty_cache_weight"])
        self.assertFalse(slot_data["reward_tools"])
        self.assertTrue(slot_data["early_repair_and_salvage"])
        self.assertTrue(slot_data["prevent_priority_in_sanity"])
        self.assertTrue(slot_data["prevent_priority_in_optional_checks"])
        self.assertTrue(slot_data["infinite_merchant_stock"])
        self.assertTrue(slot_data["merchant_sells_crown_summon"])
        self.assertFalse(slot_data["randomize_enemies"])
        self.assertEqual(0, slot_data["randomizer_difficulty"])
        enemy_mapping = slot_data["enemy_randomizer_map"]
        self.assertEqual(47, len(enemy_mapping))
        self.assertEqual(set(enemy_mapping), set(enemy_mapping.values()))
        self.assertTrue(all(source != target for source, target in enemy_mapping.items()))
        self.assertFalse(slot_data["bosses"])
        self.assertEqual(
            self.world.location_name_to_id["Defeat Core Commander"],
            slot_data["goal_location_id"],
        )
        self.assertEqual(
            [
                self.world.location_name_to_id["Defeat Glurch the Abominous Mass"],
                self.world.location_name_to_id["Defeat Ghorm the Devourer"],
                self.world.location_name_to_id["Defeat Malugaz the Corrupted"],
                self.world.location_name_to_id["Defeat Azeos the Sky Titan"],
                self.world.location_name_to_id["Defeat Omoroth the Sea Titan"],
                self.world.location_name_to_id["Defeat Ra-Akar the Sand Titan"],
                self.world.location_name_to_id["Defeat Druidra the Wild Titan"],
                self.world.location_name_to_id["Defeat Crydra the Ice Titan"],
                self.world.location_name_to_id["Defeat Pyrdra the Fire Titan"],
                self.world.location_name_to_id["Defeat Core Commander"],
            ],
            slot_data["goal_location_ids"],
        )
        self.assertEqual(
            [5, 6, 5, 4],
            [len(sphere) for sphere in slot_data["progression_spheres"]],
        )
        flattened_spheres = [
            location_id
            for sphere in slot_data["progression_spheres"]
            for location_id in sphere
        ]
        self.assertEqual(len(flattened_spheres), len(set(flattened_spheres)))
        boss_access_spheres = slot_data["boss_access_spheres"]
        self.assertEqual([3, 2, 4, 1, 1, 2, 1, 1, 1, 2, 2], [
            len(sphere) for sphere in boss_access_spheres
        ])
        self.assertEqual(
            set(flattened_spheres),
            {location_id for sphere in boss_access_spheres for location_id in sphere},
        )
        self.assertTrue(slot_data["raw_materials"])
        self.assertTrue(slot_data["refined_materials"])
        self.assertFalse(slot_data["unique_materials"])
        self.assertFalse(slot_data["key_items"])
        self.assertTrue(slot_data["seeds"])
        self.assertTrue(slot_data["food"])
        self.assertFalse(slot_data["critters"])
        self.assertFalse(slot_data["goldensanity"])
        self.assertFalse(slot_data["cardsanity"])
        self.assertFalse(slot_data["blocksanity"])
        self.assertFalse(slot_data["fishsanity"])
        self.assertFalse(slot_data["figurinesanity"])
        self.assertFalse(slot_data["valuablesanity"])
        self.assertFalse(slot_data["toolsanity"])
        self.assertFalse(slot_data["weaponsanity"])
        self.assertFalse(slot_data["accessanity"])
        self.assertFalse(slot_data["jewelrysanity"])
        self.assertFalse(slot_data["armorsanity"])
        self.assertFalse(slot_data["petsanity"])
        self.assertFalse(slot_data["merchantsanity"])
        self.assertTrue(slot_data["enemies"])
        self.assertFalse(slot_data["cattle_mutilation"])
        self.assertNotIn(
            "Slay Crystal Snail",
            {location.name for location in self.multiworld.get_locations(self.player)},
        )
        self.assertTrue(slot_data["locked_chests"])
        self.assertFalse(slot_data["skillsanity"])
        self.assertEqual(
            sorted(
                location.address
                for location in self.multiworld.get_locations(self.player)
                if location.address is not None
            ),
            slot_data["enabled_location_ids"],
        )

class TestAllOptionalChecksDisabled(CoreKeeperTestBase):
    options = {
        "goal": "lower_wall",
        **NO_LICENSES,
        "raw_materials": False,
        "refined_materials": False,
        "unique_materials": False,
        "key_items": False,
        "seeds": False,
        "food": False,
        "goldensanity": False,
        "cardsanity": False,
        "blocksanity": False,
        "fishsanity": False,
        "figurinesanity": False,
        "valuablesanity": False,
        "toolsanity": False,
        "weaponsanity": False,
        "accessanity": False,
        "jewelrysanity": False,
        "armorsanity": False,
        "petsanity": False,
        "merchantsanity": False,
        "critters": False,
        "enemies": False,
        "cattle_mutilation": False,
        "locked_chests": False,
        "skillsanity": False,
        "bosses": False,
        "soul_seeker_cache": False,
        "titan_breath_cache": False,
        "phantom_spark_cache": False,
        "rune_song_cache": False,
        "credence_of_ruin_cache": False,
        "stormbringer_cache": False,
    }

    def test_only_required_boss_check_remains(self) -> None:
        self.assertEqual(
            [
                "Defeat Glurch the Abominous Mass",
                "Defeat Ghorm the Devourer",
                "Defeat Malugaz the Corrupted",
            ],
            [location.name for location in self.multiworld.get_unfilled_locations(self.player)],
        )
        self.assertEqual(3, len([item for item in self.multiworld.itempool if item.player == self.player]))
        self.assertNotIn(
            "Copper Key", [item.name for item in self.multiworld.itempool if item.player == self.player]
        )


class TestOptionalBossesLowerWall(CoreKeeperTestBase):
    options = {"goal": "lower_wall", "bosses": True}

    def test_pre_wall_optional_bosses_are_added(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertIn("Defeat The Hive Mother", names)
        self.assertIn("Defeat King Slime", names)
        self.assertNotIn("Defeat Ivy the Poisonous Mass", names)


class TestOptionalBossesDisabled(CoreKeeperTestBase):
    options = {"goal": "defeat_core_commander", "bosses": False}

    def test_only_goal_chain_bosses_remain(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertNotIn("Defeat The Hive Mother", names)
        self.assertNotIn("Defeat Ivy the Poisonous Mass", names)
        self.assertIn("Defeat Core Commander", names)


class TestOptionalBossesCoreCommander(CoreKeeperTestBase):
    options = {"goal": "defeat_core_commander", "bosses": True}

    def test_post_commander_urschleim_is_not_added(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertIn("Defeat Ivy the Poisonous Mass", names)
        self.assertIn("Defeat Atlantean Worm", names)
        self.assertNotIn("Defeat Urschleim", names)


class TestAllBossesForcesOptionalBosses(CoreKeeperTestBase):
    options = {"goal": "defeat_all_bosses", "bosses": False}

    def test_goal_still_contains_all_optional_bosses(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertIn("Defeat The Hive Mother", names)
        self.assertIn("Defeat Oblidra the Void Titan", names)
        self.assertTrue(self.world.fill_slot_data()["bosses"])


class TestCoreCommanderBossChain(CoreKeeperTestBase):
    def test_enemy_goal_scope_stops_before_passage(self) -> None:
        self.assertEqual(37, sum(
            8406352 <= location.address <= 8406401
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))
    def test_required_boss_checks_are_present(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertTrue({
            "Defeat Glurch the Abominous Mass", "Defeat Ghorm the Devourer",
            "Defeat Malugaz the Corrupted", "Defeat Azeos the Sky Titan",
            "Defeat Omoroth the Sea Titan", "Defeat Ra-Akar the Sand Titan",
            "Defeat Druidra the Wild Titan", "Defeat Crydra the Ice Titan",
            "Defeat Pyrdra the Fire Titan", "Defeat Core Commander",
        }.issubset(names))

    def test_raw_material_goal_scope_stops_before_passage(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertIn("Collect Scarlet Ore", names)
        self.assertIn("Collect Solarite Ore", names)
        self.assertNotIn("Collect Pandorium Ore", names)
        self.assertEqual(29, sum(
            location.name == "Collect Wood" or 8406100 <= location.address <= 8406132
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))

    def test_refined_material_goal_scope_stops_before_passage(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertIn("Collect Copper Bar", names)
        self.assertIn("Collect Solarite Bar", names)
        self.assertNotIn("Collect Pandorium Bar", names)
        self.assertEqual(12, sum(
            8406133 <= location.address <= 8406146
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))

    def test_food_stops_before_passage_foods(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertIn("Collect Atlantean Worm Heart", names)
        self.assertNotIn("Collect Glowing Mushroom", names)
        self.assertNotIn("Collect Oblidra's Heart", names)
        self.assertIn("Collect Paradise Fruit Basket", names)
        self.assertIn("Collect Splendid Amalgam", names)
        self.assertEqual(20, sum(
            LOCATION_METADATA.get(location.name, (None,))[0] == "food"
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestSahabarBossChain(CoreKeeperTestBase):
    options = {"goal": "defeat_sahabar", "unique_materials": True}

    def test_required_boss_checks_and_terminal_are_present(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertIn("Defeat Core Commander", names)
        self.assertIn("Defeat Nimruza, Queen of the Burrowed Sands", names)
        self.assertIn("Defeat S.A.H.A.B.A.R", names)
        slot_data = self.world.fill_slot_data()
        self.assertEqual(12, len(slot_data["goal_location_ids"]))
        self.assertEqual(
            self.world.location_name_to_id["Defeat S.A.H.A.B.A.R"],
            slot_data["goal_location_id"],
        )
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertIn("Collect Pandorium Ore", names)
        self.assertIn("Collect Relucite Ore", names)
        self.assertIn("Collect Oblivion Fragment", names)
        self.assertNotIn("Collect S.A.H.A.B.A.R's Mortar Housing", names)
        self.assertEqual(18, sum(
            8406147 <= location.address <= 8406165
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))
        self.assertEqual(22, sum(
            LOCATION_METADATA.get(location.name, (None,))[0] == "food"
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))
        self.assertEqual(49, sum(
            8406352 <= location.address <= 8406401
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))

class TestAllBossesChain(CoreKeeperTestBase):
    options = {"goal": "defeat_all_bosses", "unique_materials": True}

    def test_all_twenty_boss_checks_and_terminal_are_present(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        optional = {
            "Defeat The Hive Mother", "Defeat King Slime",
            "Defeat Ivy the Poisonous Mass", "Defeat Morpha the Aquatic Mass",
            "Defeat Igneous the Molten Mass", "Defeat Atlantean Worm",
            "Defeat Urschleim", "Defeat Oblidra the Void Titan",
        }
        self.assertTrue(optional.issubset(names))
        slot_data = self.world.fill_slot_data()
        self.assertEqual(20, len(slot_data["goal_location_ids"]))
        self.assertEqual(
            self.world.location_name_to_id["Defeat Oblidra the Void Titan"],
            slot_data["goal_location_id"],
        )
        self.assertIsNotNone(
            self.multiworld.get_location("Collect S.A.H.A.B.A.R's Mortar Housing", self.player)
        )


class TestLowerWallGoal(CoreKeeperTestBase):
    options = {"goal": "lower_wall", "unique_materials": True, "key_items": True}

    def test_post_wall_checks_are_removed(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertNotIn("Defeat Azeos the Sky Titan", names)
        self.assertNotIn("Defeat Core Commander", names)
        self.assertNotIn("Collect Scarlet Ore", names)
        self.assertNotIn("Collect Pandorium Ore", names)
        self.assertIn("Collect Crystal Skull Shard", names)
        self.assertNotIn("Collect Chipped Blade", names)
        self.assertEqual(3, len(self.world.fill_slot_data()["goal_location_ids"]))

    def test_key_items_stop_at_the_three_prewall_boss_items(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertEqual(
            {"Collect Ghorm's Horn", "Collect Glurch Eye", "Collect Stolen Crystal Heart"},
            {name for name in names if name.startswith("Collect ") and name in {
                "Collect Ghorm's Horn", "Collect Glurch Eye", "Collect Stolen Crystal Heart",
                "Collect Admin Key", "Collect Azeos Feather Fan", "Collect Omoroth Compass",
                "Collect Ra-Akar Automaton", "Collect Brood Void Neuron", "Collect Herald Void Neuron",
            }},
        )

    def test_seeds_stop_at_the_six_prewall_varieties(self) -> None:
        self.assertEqual(6, sum(
            8406254 <= location.address <= 8406267
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))

    def test_food_stops_at_the_ten_prewall_varieties(self) -> None:
        self.assertEqual(10, sum(
            LOCATION_METADATA.get(location.name, (None,))[0] == "food"
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))

    def test_enemies_stop_at_the_eighteen_prewall_types(self) -> None:
        self.assertEqual(18, sum(
            8406352 <= location.address <= 8406401
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestCattleMutilationEnabled(CoreKeeperTestBase):
    options = {"cattle_mutilation": True}

    def test_all_livestock_and_crystal_snail_checks_are_present(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertTrue({
            "Slay Moolin", "Slay Bambuck", "Slay Strolly Poly",
            "Slay Kelple", "Slay Dodo", "Slay Drohmble", "Slay Crystal Snail",
        }.issubset(names))

    def test_crystal_snail_is_enabled_by_cattle_mutilation(self) -> None:
        self.assertIn(
            "Slay Crystal Snail",
            {location.name for location in self.multiworld.get_locations(self.player)},
        )


class TestLowerWallCattleMutilation(CoreKeeperTestBase):
    options = {"goal": "lower_wall", "cattle_mutilation": True}

    def test_only_three_prewall_livestock_checks_are_present(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertTrue({"Slay Moolin", "Slay Bambuck", "Slay Strolly Poly"}.issubset(names))
        self.assertTrue({
            "Slay Kelple", "Slay Dodo", "Slay Drohmble", "Slay Crystal Snail",
        }.isdisjoint(names))


class TestCrittersEnabled(CoreKeeperTestBase):
    options = {"goal": "defeat_all_bosses", "critters": True}

    def test_all_twenty_five_critter_checks_are_present(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertEqual(25, len({name for name in names if name.startswith("Collect ") and name in {
            "Collect Yellow Glowbug", "Collect Blue Glowbug", "Collect Green Glowbug",
            "Collect Red Glowbug", "Collect Purple Glowbug", "Collect Blackbug",
            "Collect Larvlet", "Collect Moon Pincher", "Collect Dusk Fairy",
            "Collect Dream Messenger", "Collect Citrus Pinion", "Collect Ice Wind",
            "Collect Crimson Wing", "Collect Little Death", "Collect Leaf Hopper",
            "Collect Earthworm", "Collect Manyleg", "Collect Pest Bug", "Collect Sun Pincher",
            "Collect Gem Snail", "Collect Snoot Fly", "Collect Shadow Newt",
            "Collect Drape Ray", "Collect Sniffling", "Collect Void Larvlet",
        }}))


class TestLowerWallCritters(CoreKeeperTestBase):
    options = {"goal": "lower_wall", "critters": True}

    def test_only_prewall_critter_checks_are_present(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertTrue({
            "Collect Yellow Glowbug", "Collect Blue Glowbug", "Collect Blackbug",
            "Collect Larvlet", "Collect Earthworm", "Collect Pest Bug",
        }.issubset(names))
        self.assertNotIn("Collect Drape Ray", names)
        self.assertNotIn("Collect Void Larvlet", names)


class TestGoldensanityEnabled(CoreKeeperTestBase):
    options = {"goldensanity": True}

    def test_all_eleven_golden_food_checks_are_present(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertEqual(11, sum(
            8406297 <= location.address <= 8406307
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))
        self.assertIn("Collect Shiny Larva Meat", names)


class TestLowerWallGoldensanity(CoreKeeperTestBase):
    options = {"goal": "lower_wall", "goldensanity": True}

    def test_only_five_prewall_golden_food_checks_are_present(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertTrue({
            "Collect Golden Heart Berry", "Collect Golden Bomb Pepper", "Collect Golden Carrock",
            "Collect Golden Glow Tulip", "Collect Shiny Larva Meat",
        }.issubset(names))
        self.assertEqual(5, sum(
            8406297 <= location.address <= 8406307
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestCardsanityEnabled(CoreKeeperTestBase):
    options = {"cardsanity": True}

    def test_nine_cards_and_deck_are_present(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertEqual(9, sum(name.startswith("Collect Oracle Card") for name in names))
        self.assertIn("Collect Oracle Deck", names)


class TestLowerWallCardsanity(CoreKeeperTestBase):
    options = {"goal": "lower_wall", "cardsanity": True}

    def test_only_three_early_cards_are_present(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertEqual({
            'Collect Oracle Card "Aura"', 'Collect Oracle Card "Entity"',
            'Collect Oracle Card "Brilliance"',
        }, {name for name in names if name.startswith("Collect Oracle Card")})
        self.assertNotIn("Collect Oracle Deck", names)


class TestBlocksanityEnabled(CoreKeeperTestBase):
    options = {"blocksanity": True}

    def test_core_commander_scope_has_eighteen_blocks(self) -> None:
        self.assertEqual(18, sum(
            8406660 <= location.address <= 8406685
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestLowerWallBlocksanity(CoreKeeperTestBase):
    options = {"goal": "lower_wall", "blocksanity": True}

    def test_only_seven_early_blocks_are_present(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertEqual({
            "Collect Dirt Block", "Collect Turf Block", "Collect Sand Block", "Collect Meadow Block",
            "Collect Clay Block", "Collect Larva Hive Block", "Collect Stone Block",
        }, {name for name in names if name.endswith(" Block")})


class TestPassageBlocksanity(CoreKeeperTestBase):
    options = {"goal": "defeat_sahabar", "blocksanity": True}

    def test_all_twenty_three_blocks_are_present(self) -> None:
        self.assertEqual(23, sum(
            8406660 <= location.address <= 8406685
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestFishsanityEnabled(CoreKeeperTestBase):
    options = {"fishsanity": True}

    def test_core_commander_scope_has_thirty_nine_fish(self) -> None:
        self.assertEqual(39, sum(
            8406308 <= location.address <= 8406351
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestLowerWallFishsanity(CoreKeeperTestBase):
    options = {"goal": "lower_wall", "fishsanity": True}

    def test_only_twelve_early_fish_are_present(self) -> None:
        self.assertEqual(12, sum(
            8406308 <= location.address <= 8406351
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestPassageFishsanity(CoreKeeperTestBase):
    options = {"goal": "defeat_sahabar", "fishsanity": True}

    def test_all_forty_four_fish_are_present(self) -> None:
        self.assertEqual(44, sum(
            8406308 <= location.address <= 8406351
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestFigurinesanityEnabled(CoreKeeperTestBase):
    options = {"figurinesanity": True}

    def test_core_commander_scope_has_fifty_five_figurines(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        self.assertEqual(55, sum(
            name.endswith(" Figurine") or name == "Collect S.A.H.A.B.A.R. Trophy"
            for name in names
        ))


class TestLowerWallFigurinesanity(CoreKeeperTestBase):
    options = {"goal": "lower_wall", "figurinesanity": True}

    def test_only_twenty_two_early_figurines_are_present(self) -> None:
        self.assertEqual(22, sum(
            8406166 <= location.address <= 8406236
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestPassageFigurinesanity(CoreKeeperTestBase):
    options = {"goal": "defeat_sahabar", "figurinesanity": True}

    def test_all_seventy_one_figurines_are_present(self) -> None:
        self.assertEqual(71, sum(
            8406166 <= location.address <= 8406236
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestValuablesanityEnabled(CoreKeeperTestBase):
    options = {"valuablesanity": True}

    def test_core_commander_scope_has_one_hundred_fifteen_valuables(self) -> None:
        self.assertEqual(113, sum(
            8406542 <= location.address <= 8406659
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestLowerWallValuablesanity(CoreKeeperTestBase):
    options = {"goal": "lower_wall", "valuablesanity": True}

    def test_only_forty_one_early_valuables_are_present(self) -> None:
        self.assertEqual(40, sum(
            8406542 <= location.address <= 8406659
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestPassageValuablesanity(CoreKeeperTestBase):
    options = {"goal": "defeat_sahabar", "valuablesanity": True}

    def test_all_one_hundred_eighteen_valuables_are_present(self) -> None:
        self.assertEqual(116, sum(
            8406542 <= location.address <= 8406659
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestToolsanityEnabled(CoreKeeperTestBase):
    options = {"toolsanity": True}

    def test_core_commander_scope_has_all_forty_one_tools(self) -> None:
        self.assertEqual(41, sum(
            8406726 <= location.address <= 8407194
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestLowerWallToolsanity(CoreKeeperTestBase):
    options = {"goal": "lower_wall", "toolsanity": True}

    def test_only_twenty_three_early_tools_are_present(self) -> None:
        self.assertEqual(23, sum(
            8406726 <= location.address <= 8407194
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestWeaponsanityEnabled(CoreKeeperTestBase):
    options = {"weaponsanity": True}

    def test_core_commander_scope_has_sixty_nine_weapons(self) -> None:
        self.assertEqual(69, sum(
            8406765 <= location.address <= 8406839
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestLowerWallWeaponsanity(CoreKeeperTestBase):
    options = {"goal": "lower_wall", "weaponsanity": True}

    def test_only_thirty_two_early_weapons_are_present(self) -> None:
        self.assertEqual(32, sum(
            8406765 <= location.address <= 8406839
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestPassageWeaponsanity(CoreKeeperTestBase):
    options = {"goal": "defeat_sahabar", "weaponsanity": True}

    def test_all_seventy_five_weapons_are_present(self) -> None:
        self.assertEqual(75, sum(
            8406765 <= location.address <= 8406839
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestAccessanityEnabled(CoreKeeperTestBase):
    options = {"accessanity": True}

    def test_core_commander_scope_has_fifty_nine_accessories(self) -> None:
        self.assertEqual(58, sum(
            8406944 <= location.address <= 8407004
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestLowerWallAccessanity(CoreKeeperTestBase):
    options = {"goal": "lower_wall", "accessanity": True}

    def test_only_twenty_five_early_accessories_are_present(self) -> None:
        self.assertEqual(25, sum(
            8406944 <= location.address <= 8407004
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestPassageAccessanity(CoreKeeperTestBase):
    options = {"goal": "defeat_sahabar", "accessanity": True}

    def test_all_sixty_accessories_are_present(self) -> None:
        self.assertEqual(59, sum(
            8406944 <= location.address <= 8407004
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestJewelrysanityEnabled(CoreKeeperTestBase):
    options = {"jewelrysanity": True}

    def test_core_commander_scope_has_one_hundred_one_jewels(self) -> None:
        self.assertEqual(94, sum(
            8406840 <= location.address <= 8406943
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestLowerWallJewelrysanity(CoreKeeperTestBase):
    options = {"goal": "lower_wall", "jewelrysanity": True}

    def test_only_forty_two_early_jewels_are_present(self) -> None:
        self.assertEqual(40, sum(
            8406840 <= location.address <= 8406943
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestPassageJewelrysanity(CoreKeeperTestBase):
    options = {"goal": "defeat_sahabar", "jewelrysanity": True}

    def test_all_one_hundred_four_jewels_are_present(self) -> None:
        self.assertEqual(97, sum(
            8406840 <= location.address <= 8406943
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestArmorsanityEnabled(CoreKeeperTestBase):
    options = {"armorsanity": True}

    def test_core_commander_scope_has_one_hundred_seventy_armor_pieces(self) -> None:
        self.assertEqual(170, sum(
            8407005 <= location.address <= 8407192
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestLowerWallArmorsanity(CoreKeeperTestBase):
    options = {"goal": "lower_wall", "armorsanity": True}

    def test_only_sixty_early_armor_pieces_are_present(self) -> None:
        self.assertEqual(60, sum(
            8407005 <= location.address <= 8407192
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestPassageArmorsanity(CoreKeeperTestBase):
    options = {"goal": "defeat_sahabar", "armorsanity": True}

    def test_all_one_hundred_eighty_eight_armor_pieces_are_present(self) -> None:
        self.assertEqual(188, sum(
            8407005 <= location.address <= 8407192
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestPetsanityEnabled(CoreKeeperTestBase):
    options = {"petsanity": True}

    def test_core_commander_scope_has_twenty_six_pet_checks(self) -> None:
        self.assertEqual(26, sum(
            8406698 <= location.address <= 8406725
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestLowerWallPetsanity(CoreKeeperTestBase):
    options = {"goal": "lower_wall", "petsanity": True}

    def test_only_fourteen_early_pet_checks_are_present(self) -> None:
        self.assertEqual(14, sum(
            8406698 <= location.address <= 8406725
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestPassagePetsanity(CoreKeeperTestBase):
    options = {"goal": "defeat_sahabar", "petsanity": True}

    def test_all_twenty_eight_pet_checks_are_present(self) -> None:
        self.assertEqual(28, sum(
            8406698 <= location.address <= 8406725
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestMerchantsanityEnabled(CoreKeeperTestBase):
    options = {"merchantsanity": True}

    def test_core_commander_scope_has_four_merchants(self) -> None:
        self.assertEqual(4, sum(
            8406693 <= location.address <= 8406697
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestLowerWallMerchantsanity(CoreKeeperTestBase):
    options = {"goal": "lower_wall", "merchantsanity": True}

    def test_only_two_early_merchants_are_present(self) -> None:
        self.assertEqual(2, sum(
            8406693 <= location.address <= 8406697
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestAllBossesMerchantsanity(CoreKeeperTestBase):
    options = {"goal": "defeat_all_bosses", "merchantsanity": True}

    def test_all_five_merchants_are_present(self) -> None:
        self.assertEqual(5, sum(
            8406693 <= location.address <= 8406697
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None
        ))


class TestSkillsanityEnabled(CoreKeeperTestBase):
    options = {"skillsanity": True}

    def test_all_twelve_skills_match_goal_cap(self) -> None:
        self.assertIsNotNone(self.multiworld.get_location("Level 10 Mining", self.player))
        self.assertIsNotNone(self.multiworld.get_location("Level 60 Mining", self.player))
        self.assertIsNotNone(self.multiworld.get_location("Level 10 Running", self.player))
        self.assertIsNotNone(self.multiworld.get_location("Level 60 Running", self.player))
        self.assertIsNotNone(self.multiworld.get_location("Level 10 Explosives", self.player))
        self.assertIsNotNone(self.multiworld.get_location("Level 60 Fishing", self.player))
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        skill_names = {name for name in names if name.startswith("Level ")}
        self.assertEqual(72, len(skill_names))
        self.assertNotIn("Level 70 Mining", names)
        self.assertNotIn("Level 100 Running", names)

    def test_skillsanity_does_not_add_skill_point_rewards(self) -> None:
        names = [item.name for item in self.multiworld.itempool if item.player == self.player]
        self.assertFalse(any(name.startswith("+5 ") for name in names))
        self.assertFalse(self.world.fill_slot_data()["skill_points"])


class TestSkillPointsEnabledWithoutSkillsanity(CoreKeeperTestBase):
    options = {"goal": "defeat_all_bosses", "skill_points": True, "skillsanity": False}

    def test_skill_points_are_an_independent_sixty_item_reward_pool(self) -> None:
        names = [item.name for item in self.multiworld.itempool if item.player == self.player]
        skill_rewards = [name for name in names if name.startswith("+5 ")]
        self.assertEqual(60, len(skill_rewards))
        self.assertEqual(12, len(set(skill_rewards)))
        self.assertFalse(
            any(location.name.startswith("Level ") for location in self.multiworld.get_locations(self.player))
        )
        self.assertTrue(self.world.fill_slot_data()["skill_points"])


class TestAllBossesSkillsanity(CoreKeeperTestBase):
    options = {"goal": "defeat_all_bosses", "skillsanity": True}

    def test_level_one_hundred_is_all_bosses_only(self) -> None:
        names = {location.name for location in self.multiworld.get_locations(self.player)}
        skill_names = {name for name in names if name.startswith("Level ")}
        self.assertEqual(120, len(skill_names))
        self.assertIn("Level 100 Mining", skill_names)
        self.assertIn("Level 100 Running", skill_names)
        self.assertIn("Level 100 Explosives", skill_names)


class TestLicensesDisabled(CoreKeeperTestBase):
    options = NO_LICENSES

    def test_license_rewards_are_absent_and_slot_data_disables_enforcement(self) -> None:
        names = [item.name for item in self.multiworld.itempool if item.player == self.player]
        self.assertNotIn("Progressive Workbench License", names)
        self.assertNotIn("Progressive Anvil License", names)
        self.assertEqual([], self.world.fill_slot_data()["enabled_licenses"])


class TestImportantCraftingLicenses(CoreKeeperTestBase):
    options = {
        "goal": "defeat_sahabar",
        "skillsanity": True,
    }

    def test_exact_verified_license_stages_fill_the_pool(self) -> None:
        names = [item.name for item in self.multiworld.itempool if item.player == self.player]
        expected = {
            "Progressive Workbench License": 7,
            "Progressive Anvil License": 7,
            "Progressive Furnace License": 3,
            "Fishing Workbench License": 1,
            "Egg Incubator License": 1,
            "Key Casting Table License": 1,
            "Salvage and Repair Station License": 1,
            "Ancient Hologram Pod License": 1,
            "Table Saw License": 1,
            "Cooking Pot License": 1,
        }
        for name, count in expected.items():
            with self.subTest(item=name):
                self.assertEqual(count, names.count(name))
        self.assertEqual(24, sum("License" in name for name in names))
        self.assertEqual(set(expected), set(self.world.fill_slot_data()["enabled_licenses"]))
        self.assertEqual(0, sum(name.endswith(" Key") for name in names))


class TestAllLicenses(CoreKeeperTestBase):
    options = {
        "goal": "defeat_all_bosses",
        **ALL_LICENSES,
        "skillsanity": True,
    }

    def test_all_optional_station_licenses_use_exact_stage_counts(self) -> None:
        names = [item.name for item in self.multiworld.itempool if item.player == self.player]
        singles = {
            "Table Saw License", "Carpenter's Table License", "Distillery Table License",
            "Electronics Table License", "Railway Forge License", "Go-Kart Workbench License",
            "Loom License", "Music Workbench License", "Livestock Workbench License",
            "Glass Workbench License", "Painter's Table License", "Glass Smelter License",
            "Rift Statue License", "Upgrade Station License",
        }
        for name in singles:
            with self.subTest(item=name):
                self.assertEqual(1, names.count(name))
        self.assertEqual(2, names.count("Progressive Smithing Table License"))
        self.assertEqual(29, len(self.world.fill_slot_data()["enabled_licenses"]))
        self.assertEqual(47, sum("License" in name for name in names))
        self.assertEqual(0, sum(name.endswith(" Key") for name in names))


class TestAllCacheWeightsZero(CoreKeeperTestBase):
    options = {
        "raw_material_cache_weight": 0,
        "refined_material_cache_weight": 0,
        "potions_cache_weight": 0,
        "pet_cache_weight": 0,
        "money_cache_weight": 0,
        "automation_cache_weight": 0,
    }

    def test_empty_cache_fills_every_non_progression_slot(self) -> None:
        names = [item.name for item in self.multiworld.itempool if item.player == self.player]
        cache_names = {
            "Raw Material Cache", "Refined Material Cache", "Potions Cache",
            "Pet Cache", "Money Cache", "Automation Cache",
        }
        self.assertFalse(cache_names.intersection(names))
        self.assertGreater(names.count("Empty Cache"), 0)


class TestAllCacheWeightsOneHundred(CoreKeeperTestBase):
    options = {
        "goal": "defeat_sahabar",
        "raw_material_cache_weight": 100,
        "refined_material_cache_weight": 100,
        "potions_cache_weight": 100,
        "pet_cache_weight": 100,
        "money_cache_weight": 100,
        "automation_cache_weight": 100,
    }

    def test_weights_are_relative_and_generation_remains_valid(self) -> None:
        names = [item.name for item in self.multiworld.itempool if item.player == self.player]
        self.assertEqual(
            len(self.multiworld.get_unfilled_locations(self.player)),
            len(names),
        )
        self.assertNotIn("Empty Cache", names)


class TestIndividualLegendaryCaches(CoreKeeperTestBase):
    options = {"goal": "defeat_all_bosses"}

    def test_every_enabled_legendary_cache_appears_once_regardless_of_goal(self) -> None:
        names = [item.name for item in self.multiworld.itempool if item.player == self.player]
        expected = {
            "Soul Seeker Cache", "Titan Breath Cache", "Phantom Spark Cache",
            "Rune Song Cache", "Credence of Ruin Cache", "Stormbringer Cache",
        }
        for name in expected:
            self.assertEqual(1, names.count(name), name)
        self.assertNotIn("Legendary Cache", names)


class TestDisabledIndividualLegendaryCache(CoreKeeperTestBase):
    options = {"soul_seeker_cache": False}

    def test_disabled_legendary_cache_is_absent_without_affecting_others(self) -> None:
        names = [item.name for item in self.multiworld.itempool if item.player == self.player]
        self.assertNotIn("Soul Seeker Cache", names)
        self.assertEqual(1, names.count("Titan Breath Cache"))


class TestEarlyRepairAndSalvage(CoreKeeperTestBase):
    options = {
        "early_repair_and_salvage": True,
    }

    def test_salvage_license_is_early(self) -> None:
        from Fill import distribute_items_restrictive

        distribute_items_restrictive(self.multiworld)
        self.world.post_fill()
        placement = next(
            location for location in self.multiworld.get_locations(self.player)
            if location.item is not None
            and location.item.name == "Salvage and Repair Station License"
        )
        starting_state = CollectionState(self.multiworld)
        starting_state.sweep_for_advancements(locations=(
            location for location in self.multiworld.get_filled_locations()
            if location.address is None
        ))
        self.assertTrue(placement.can_reach(starting_state), placement.name)
        furnace = next(
            location for location in self.multiworld.get_locations(self.player)
            if location.item is not None
            and location.item.name == "Progressive Furnace License"
        )
        self.assertTrue(furnace.can_reach(starting_state), furnace.name)

    def test_salvage_and_first_furnace_are_both_requested_early(self) -> None:
        early = self.multiworld.local_early_items[self.player]
        self.assertEqual(1, early["Salvage and Repair Station License"])
        self.assertEqual(1, early["Progressive Furnace License"])


class TestEarlyRepairWithoutLicensePool(CoreKeeperTestBase):
    options = {
        "early_repair_and_salvage": True,
        **NO_LICENSES,
    }

    def test_absent_salvage_license_is_not_requested_early(self) -> None:
        self.assertNotIn(
            "Salvage and Repair Station License",
            self.multiworld.local_early_items[self.player],
        )


class TestPreventPriorityInSanity(CoreKeeperTestBase):
    options = {
        "prevent_priority_in_sanity": True,
        "prevent_priority_in_optional_checks": False,
        "goldensanity": True,
        "skillsanity": True,
        "figurinesanity": True,
        "cardsanity": True,
        "fishsanity": True,
        "valuablesanity": True,
        "blocksanity": True,
        "merchantsanity": True,
        "petsanity": True,
    }

    def test_progression_is_rejected_by_sanity_locations(self) -> None:
        progression = self.world.create_item("Progressive Workbench License")
        for location_name in (
            "Level 10 Mining",
            "Collect Orange Cave Guppy",
            "Collect Shrooman Figurine",
            'Collect Oracle Card "Aura"',
            "Collect Rusty Spoon",
        ):
            self.assertFalse(
                self.multiworld.get_location(location_name, self.player).item_rule(
                    progression
                ),
                location_name,
            )

    def test_optional_checks_allow_progression_when_their_guard_is_off(self) -> None:
        progression = self.world.create_item("Progressive Workbench License")
        for location_name in (
            "Collect Dirt Block",
            "Talk to Bearded Merchant",
            "Collect Loyal Egg",
            "Collect Golden Heart Berry",
        ):
            self.assertTrue(
                self.multiworld.get_location(location_name, self.player).item_rule(
                    progression
                ),
                location_name,
            )

    def test_normal_checks_still_allow_progression(self) -> None:
        progression = self.world.create_item("Progressive Workbench License")
        self.assertTrue(
            self.multiworld.get_location(
                "Collect Copper Ore", self.player
            ).item_rule(progression)
        )

    def test_non_progression_is_allowed_in_sanity(self) -> None:
        cache = self.world.create_item("Raw Material Cache")
        self.assertTrue(
            self.multiworld.get_location(
                "Collect Loyal Egg", self.player
            ).item_rule(cache)
        )


class TestPreventPriorityInOptionalChecks(CoreKeeperTestBase):
    options = {
        "goal": "defeat_all_bosses",
        "prevent_priority_in_optional_checks": True,
        "prevent_priority_in_sanity": False,
        "unique_materials": True,
        "key_items": True,
        "bosses": True,
        "blocksanity": True,
        "merchantsanity": True,
        "petsanity": True,
        "goldensanity": True,
        "critters": True,
        "cattle_mutilation": True,
        "skillsanity": True,
    }

    def test_progression_is_rejected_by_optional_locations(self) -> None:
        progression = self.world.create_item("Progressive Workbench License")
        for location_name in (
            "Collect Crystal Skull Shard",
            "Collect Ghorm's Horn",
            "Defeat King Slime",
            "Collect Dirt Block",
            "Talk to Bearded Merchant",
            "Collect Loyal Egg",
            "Collect Golden Heart Berry",
            "Collect Yellow Glowbug",
            "Slay Moolin",
        ):
            self.assertFalse(
                self.multiworld.get_location(location_name, self.player).item_rule(progression),
                location_name,
            )

    def test_sanity_checks_allow_progression_when_their_guard_is_off(self) -> None:
        progression = self.world.create_item("Progressive Workbench License")
        self.assertTrue(
            self.multiworld.get_location("Level 10 Mining", self.player).item_rule(progression)
        )


class TestPreventPriorityOverflow(CoreKeeperTestBase):
    options = {
        "goal": "lower_wall",
        "prevent_priority_in_sanity": True,
        "raw_materials": False,
        "refined_materials": False,
        "unique_materials": False,
        "key_items": False,
        "locked_chests": False,
        "seeds": False,
        "food": False,
        "enemies": False,
        "bosses": False,
        "petsanity": True,
        "skillsanity": True,
    }

    def test_only_required_overflow_is_reopened(self) -> None:
        progression = self.world.create_item("Progressive Workbench License")
        skill_locations = [
            location
            for location in self.multiworld.get_locations(self.player)
            if (LOCATION_METADATA.get(location.name) or (None,))[0] == "skillsanity"
        ]
        self.assertTrue(any(location.item_rule(progression) for location in skill_locations))
        self.assertTrue(any(not location.item_rule(progression) for location in skill_locations))


class TestToolRewardPool(CoreKeeperTestBase):
    options = {
        "reward_tools": True,
        "raw_material_cache_weight": 0,
        "refined_material_cache_weight": 0,
        "potions_cache_weight": 0,
        "pet_cache_weight": 0,
        "money_cache_weight": 0,
        "automation_cache_weight": 0,
    }

    def test_all_41_validated_tools_enter_the_filler_candidates(self) -> None:
        names = [item.name for item in self.multiworld.itempool if item.player == self.player]
        tool_names = {
            name for name, item_id in ITEM_NAME_TO_ID.items()
            if 8410000 <= item_id < 8411000
        }
        self.assertEqual(41, len(tool_names))
        self.assertTrue(tool_names.issubset(names))


class TestConstrainedEquipmentRewardPool(CoreKeeperTestBase):
    options = TestAllOptionalChecksDisabled.options | {
        "reward_tools": True,
    }

    def test_later_equipment_is_cut_before_earlier_equipment(self) -> None:
        names = {
            item.name
            for item in self.multiworld.itempool
            if item.player == self.player and 8410000 <= ITEM_NAME_TO_ID[item.name] < 8411000
        }
        self.assertEqual({"Wood Pickaxe", "Copper Pickaxe", "Tin Pickaxe"}, names)


class TestExactProgressiveLicenseCounts(CoreKeeperTestBase):
    options = ALL_LICENSES | {"goal": "defeat_all_bosses"}

    def test_progressives_stop_exactly_at_their_maximum_stage(self) -> None:
        names = [item.name for item in self.multiworld.itempool if item.player == self.player]
        self.assertEqual(7, names.count("Progressive Workbench License"))
        self.assertEqual(7, names.count("Progressive Anvil License"))
        self.assertEqual(3, names.count("Progressive Furnace License"))
        self.assertEqual(2, names.count("Progressive Automation Table License"))
        self.assertEqual(2, names.count("Progressive Alchemy Table License"))
        self.assertEqual(2, names.count("Progressive Jewelry Workbench License"))
        self.assertEqual(2, names.count("Progressive Smithing Table License"))


class TestBossLicenseRequirements(CoreKeeperTestBase):
    options = ALL_LICENSES | {"goal": "defeat_all_bosses"}

    def _state(self, *items: str) -> CollectionState:
        state = CollectionState(self.multiworld)
        for name in items:
            if name.startswith("Defeated ") or name == "Wall Lowered":
                item = self.multiworld.get_location(name, self.player).item
            else:
                item = self.world.create_item(name)
            state.collect(item, True)
        return state

    def _rule(self, entrance_name: str, *items: str) -> bool:
        return self.multiworld.get_entrance(
            entrance_name, self.player
        ).access_rule(self._state(*items))

    def test_azeos_requires_hologram_and_two_furnaces(self) -> None:
        self.assertFalse(self._rule(
            "Reach Azeos",
            "Ancient Hologram Pod License",
            "Progressive Furnace License",
        ))
        self.assertTrue(self._rule(
            "Reach Azeos",
            "Ancient Hologram Pod License",
            "Progressive Furnace License",
            "Progressive Furnace License",
        ))

    def test_omoroth_requires_complete_rod_and_bait_license_chain(self) -> None:
        required = [
            "Defeated Azeos",
            "Ancient Hologram Pod License",
            "Fishing Workbench License",
            *(["Progressive Workbench License"] * 5),
            *(["Progressive Furnace License"] * 2),
        ]
        self.assertTrue(self._rule("Reach Omoroth", *required))
        for missing in {
            "Ancient Hologram Pod License",
            "Fishing Workbench License",
            "Progressive Workbench License",
            "Progressive Furnace License",
        }:
            reduced = list(required)
            reduced.remove(missing)
            with self.subTest(missing=missing):
                self.assertFalse(self._rule("Reach Omoroth", *reduced))

    def test_ra_akar_requires_three_furnaces_hologram_and_table_saw(self) -> None:
        required = [
            "Defeated Omoroth",
            "Ancient Hologram Pod License",
            "Table Saw License",
            *(["Progressive Furnace License"] * 3),
        ]
        self.assertTrue(self._rule("Reach Ra-Akar", *required))
        for missing in {
            "Ancient Hologram Pod License",
            "Table Saw License",
            "Progressive Furnace License",
        }:
            reduced = list(required)
            reduced.remove(missing)
            with self.subTest(missing=missing):
                self.assertFalse(self._rule("Reach Ra-Akar", *reduced))

    def test_each_second_titan_requires_three_furnaces_and_table_saw(self) -> None:
        cases = {
            "Reach Druidra": ["Defeated Azeos", "Defeated Omoroth", "Defeated Ra-Akar"],
            "Reach Crydra": ["Defeated Druidra"],
            "Reach Pyrdra": ["Defeated Crydra"],
        }
        for entrance, events in cases.items():
            required = events + [
                "Table Saw License",
                *(["Progressive Furnace License"] * 3),
            ]
            with self.subTest(entrance=entrance):
                self.assertTrue(self._rule(entrance, *required))
                without_saw = list(required)
                without_saw.remove("Table Saw License")
                self.assertFalse(self._rule(entrance, *without_saw))
                without_furnace = list(required)
                without_furnace.remove("Progressive Furnace License")
                self.assertFalse(self._rule(entrance, *without_furnace))

    def test_nimruza_requires_three_furnaces(self) -> None:
        required = ["Defeated Core Commander", *(["Progressive Furnace License"] * 3)]
        self.assertTrue(self._rule("Reach Nimruza", *required))
        required.pop()
        self.assertFalse(self._rule("Reach Nimruza", *required))

    def test_sahabar_does_not_require_rift_statue(self) -> None:
        self.assertTrue(self._rule("Reach S.A.H.A.B.A.R", "Defeated Nimruza"))

class TestBossLicenseRequirementsDisabled(CoreKeeperTestBase):
    options = NO_LICENSES | {"goal": "defeat_all_bosses"}

    def test_boss_license_gates_are_bypassed(self) -> None:
        state = CollectionState(self.multiworld)
        for event in (
            "Defeated Azeos", "Defeated Omoroth", "Defeated Ra-Akar",
            "Defeated Druidra", "Defeated Crydra", "Defeated Core Commander",
        ):
            state.collect(self.multiworld.get_location(event, self.player).item, True)
        for entrance in (
            "Reach Azeos", "Reach Omoroth", "Reach Ra-Akar", "Reach Druidra",
            "Reach Crydra", "Reach Pyrdra", "Reach Nimruza",
        ):
            with self.subTest(entrance=entrance):
                self.assertTrue(
                    self.multiworld.get_entrance(entrance, self.player).access_rule(state)
                )


class TestCorrectedCatalogRules(CoreKeeperTestBase):
    options = {"goldensanity": True, "goal": "lower_wall"}

    def test_golden_glow_tulip_is_available_from_start(self) -> None:
        location = self.multiworld.get_location("Collect Golden Glow Tulip", self.player)
        self.assertTrue(location.access_rule(CollectionState(self.multiworld)))


class TestDeathLinkKeepInventory(CoreKeeperTestBase):
    options = {"death_link": "death_link_keep_inventory"}

    def test_slot_data_enables_keep_inventory_mode(self) -> None:
        self.assertEqual(2, self.world.fill_slot_data()["death_link"])
