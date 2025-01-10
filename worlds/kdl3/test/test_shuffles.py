from typing import List, Tuple, Optional
from . import KDL3TestBase
from ..room import KDL3Room
from ..names import animal_friend_spawns


class TestCopyAbilityShuffle(KDL3TestBase):
    options = {
        "open_world": False,
        "goal_speed": "normal",
        "max_heart_stars": 30,
        "heart_stars_required": 50,
        "filler_percentage": 0,
        "copy_ability_randomization": "enabled",
    }

    def test_goal(self) -> None:
        try:
            self.assertBeatable(False)
            heart_stars = self.get_items_by_name("Heart Star")
            self.collect(heart_stars[0:14])
            self.assertEqual(self.count("Heart Star"), 14, str(self.multiworld.seed))
            self.assertBeatable(False)
            self.collect(heart_stars[14:15])
            self.assertEqual(self.count("Heart Star"), 15, str(self.multiworld.seed))
            self.assertBeatable(False)
            self.collect_by_name(["Burning", "Cutter", "Kine"])
            self.assertBeatable(True)
            self.remove([self.get_item_by_name("Love-Love Rod")])
            self.collect(heart_stars)
            self.assertEqual(self.count("Heart Star"), 30, str(self.multiworld.seed))
            self.assertBeatable(True)
        except AssertionError as ex:
            # if assert beatable fails, this will catch and print the seed
            raise AssertionError(f"Test failed, Seed:{self.multiworld.seed}") from ex

    def test_kine(self) -> None:
        try:
            self.collect_by_name(["Cutter", "Burning", "Heart Star"])
            self.assertBeatable(False)
        except AssertionError as ex:
            raise AssertionError(f"Test failed, Seed:{self.multiworld.seed}") from ex

    def test_cutter(self) -> None:
        try:
            self.collect_by_name(["Kine", "Burning", "Heart Star"])
            self.assertBeatable(False)
        except AssertionError as ex:
            raise AssertionError(f"Test failed, Seed:{self.multiworld.seed}") from ex

    def test_burning(self) -> None:
        try:
            self.collect_by_name(["Cutter", "Kine", "Heart Star"])
            self.assertBeatable(False)
        except AssertionError as ex:
            raise AssertionError(f"Test failed, Seed:{self.multiworld.seed}") from ex

    def test_cutter_and_burning_reachable(self) -> None:
        rooms = self.multiworld.worlds[1].rooms
        copy_abilities = self.multiworld.worlds[1].copy_abilities
        sand_canyon_5 = self.multiworld.get_region("Sand Canyon 5 - 9", 1)
        assert isinstance(sand_canyon_5, KDL3Room)
        valid_rooms = [room for room in rooms if (room.level < sand_canyon_5.level)
                       or (room.level == sand_canyon_5.level and room.stage < sand_canyon_5.stage)]
        for room in valid_rooms:
            if any(copy_abilities[enemy] == "Cutter Ability" for enemy in room.enemies):
                break
        else:
            self.fail("Could not reach Cutter Ability before Sand Canyon 5!")
        iceberg_4 = self.multiworld.get_region("Iceberg 4 - 7", 1)
        assert isinstance(iceberg_4, KDL3Room)
        valid_rooms = [room for room in rooms if (room.level < iceberg_4.level)
                       or (room.level == iceberg_4.level and room.stage < iceberg_4.stage)]
        for room in valid_rooms:
            if any(copy_abilities[enemy] == "Burning Ability" for enemy in room.enemies):
                break
        else:
            self.fail("Could not reach Burning Ability before Iceberg 4!")

    def test_valid_abilities_for_ROB(self) -> None:
        # there exists a subset of 4-7 abilities that will allow us access to ROB heart star on default settings
        self.collect_by_name(["Heart Star", "Kine", "Coo"])  # we will guaranteed need Coo, Kine, and Heart Stars to reach
        # first we need to identify our bukiset requirements
        groups = [
            ({"Parasol Ability", "Cutter Ability"}, {'Bukiset (Parasol)', 'Bukiset (Cutter)'}),
            ({"Spark Ability", "Clean Ability"}, {'Bukiset (Spark)', 'Bukiset (Clean)'}),
            ({"Ice Ability", "Needle Ability"}, {'Bukiset (Ice)', 'Bukiset (Needle)'}),
            ({"Stone Ability", "Burning Ability"}, {'Bukiset (Stone)', 'Bukiset (Burning)'}),
        ]
        copy_abilities = self.multiworld.worlds[1].copy_abilities
        required_abilities: List[List[str]] = []
        for abilities, bukisets in groups:
            potential_abilities: List[str] = list()
            for bukiset in bukisets:
                if copy_abilities[bukiset] in abilities:
                    potential_abilities.append(copy_abilities[bukiset])
            required_abilities.append(potential_abilities)
        collected_abilities = list()
        for group in required_abilities:
            self.assertFalse(len(group) == 0, str(self.multiworld.seed))
            collected_abilities.append(group[0])
        self.collect_by_name([ability.replace(" Ability", "") for ability in collected_abilities])
        if "Parasol Ability" not in collected_abilities or "Stone Ability" not in collected_abilities:
            # required for non-Bukiset related portions
            self.collect_by_name(["Parasol", "Stone"])

        if "Cutter Ability" not in collected_abilities:
            # we can't actually reach 3-6 without Cutter
            self.assertFalse(self.can_reach_location("Sand Canyon 6 - Professor Hector & R.O.B"), str(self.multiworld.seed))
            self.collect_by_name(["Cutter"])

        self.assertTrue(self.can_reach_location("Sand Canyon 6 - Professor Hector & R.O.B"),
                        ''.join(str(self.multiworld.seed)).join(collected_abilities))


class TestAnimalShuffle(KDL3TestBase):
    options = {
        "open_world": False,
        "goal_speed": "normal",
        "max_heart_stars": 30,
        "heart_stars_required": 50,
        "filler_percentage": 0,
        "animal_randomization": "full",
    }

    def test_goal(self) -> None:
        try:
            self.assertBeatable(False)
            heart_stars = self.get_items_by_name("Heart Star")
            self.collect(heart_stars[0:14])
            self.assertEqual(self.count("Heart Star"), 14, str(self.multiworld.seed))
            self.assertBeatable(False)
            self.collect(heart_stars[14:15])
            self.assertEqual(self.count("Heart Star"), 15, str(self.multiworld.seed))
            self.assertBeatable(False)
            self.collect_by_name(["Burning", "Cutter", "Kine"])
            self.assertBeatable(True)
            self.remove([self.get_item_by_name("Love-Love Rod")])
            self.collect(heart_stars)
            self.assertEqual(self.count("Heart Star"), 30, str(self.multiworld.seed))
            self.assertBeatable(True)
        except AssertionError as ex:
            # if assert beatable fails, this will catch and print the seed
            raise AssertionError(f"Test failed, Seed:{self.multiworld.seed}") from ex

    def test_kine(self) -> None:
        try:
            self.collect_by_name(["Cutter", "Burning", "Heart Star"])
            self.assertBeatable(False)
        except AssertionError as ex:
            raise AssertionError(f"Test failed, Seed:{self.multiworld.seed}") from ex

    def test_cutter(self) -> None:
        try:
            self.collect_by_name(["Kine", "Burning", "Heart Star"])
            self.assertBeatable(False)
        except AssertionError as ex:
            raise AssertionError(f"Test failed, Seed:{self.multiworld.seed}") from ex

    def test_burning(self) -> None:
        try:
            self.collect_by_name(["Cutter", "Kine", "Heart Star"])
            self.assertBeatable(False)
        except AssertionError as ex:
            raise AssertionError(f"Test failed, Seed:{self.multiworld.seed}") from ex

    def test_locked_animals(self) -> None:
        ripple_field_5 = self.multiworld.get_location("Ripple Field 5 - Animal 2", 1)
        self.assertTrue(ripple_field_5.item is not None and ripple_field_5.item.name == "Pitch Spawn",
                        f"Multiworld did not place Pitch, Seed: {self.multiworld.seed}")
        iceberg_4 = self.multiworld.get_location("Iceberg 4 - Animal 1", 1)
        self.assertTrue(iceberg_4.item is not None and iceberg_4.item.name == "ChuChu Spawn",
                        f"Multiworld did not place ChuChu, Seed: {self.multiworld.seed}")
        sand_canyon_6 = self.multiworld.get_location("Sand Canyon 6 - Animal 1", 1)
        self.assertTrue(sand_canyon_6.item is not None and sand_canyon_6.item.name in
                        {"Kine Spawn", "Coo Spawn"}, f"Multiworld did not place Coo/Kine, Seed: {self.multiworld.seed}")

    def test_problematic(self) -> None:
        for spawns in animal_friend_spawns.problematic_sets:
            placed = [self.multiworld.get_location(spawn, 1).item for spawn in spawns]
            placed_names = set([item.name for item in placed])
            self.assertEqual(len(placed), len(placed_names),
                             f"Duplicate animal placed in problematic locations:"
                             f" {[spawn.location for spawn in placed]}, "
                             f"Seed: {self.multiworld.seed}")


class TestAllShuffle(KDL3TestBase):
    options = {
        "open_world": False,
        "goal_speed": "normal",
        "max_heart_stars": 30,
        "heart_stars_required": 50,
        "filler_percentage": 0,
        "animal_randomization": "full",
        "copy_ability_randomization": "enabled",
    }

    def test_goal(self) -> None:
        try:
            self.assertBeatable(False)
            heart_stars = self.get_items_by_name("Heart Star")
            self.collect(heart_stars[0:14])
            self.assertEqual(self.count("Heart Star"), 14, str(self.multiworld.seed))
            self.assertBeatable(False)
            self.collect(heart_stars[14:15])
            self.assertEqual(self.count("Heart Star"), 15, str(self.multiworld.seed))
            self.assertBeatable(False)
            self.collect_by_name(["Burning", "Cutter", "Kine"])
            self.assertBeatable(True)
            self.remove([self.get_item_by_name("Love-Love Rod")])
            self.collect(heart_stars)
            self.assertEqual(self.count("Heart Star"), 30, str(self.multiworld.seed))
            self.assertBeatable(True)
        except AssertionError as ex:
            # if assert beatable fails, this will catch and print the seed
            raise AssertionError(f"Test failed, Seed:{self.multiworld.seed}") from ex

    def test_kine(self) -> None:
        try:
            self.collect_by_name(["Cutter", "Burning", "Heart Star"])
            self.assertBeatable(False)
        except AssertionError as ex:
            raise AssertionError(f"Test failed, Seed:{self.multiworld.seed}") from ex

    def test_cutter(self) -> None:
        try:
            self.collect_by_name(["Kine", "Burning", "Heart Star"])
            self.assertBeatable(False)
        except AssertionError as ex:
            raise AssertionError(f"Test failed, Seed:{self.multiworld.seed}") from ex

    def test_burning(self) -> None:
        try:
            self.collect_by_name(["Cutter", "Kine", "Heart Star"])
            self.assertBeatable(False)
        except AssertionError as ex:
            raise AssertionError(f"Test failed, Seed:{self.multiworld.seed}") from ex

    def test_locked_animals(self) -> None:
        ripple_field_5 = self.multiworld.get_location("Ripple Field 5 - Animal 2", 1)
        self.assertTrue(ripple_field_5.item is not None and ripple_field_5.item.name == "Pitch Spawn",
                        f"Multiworld did not place Pitch, Seed: {self.multiworld.seed}")
        iceberg_4 = self.multiworld.get_location("Iceberg 4 - Animal 1", 1)
        self.assertTrue(iceberg_4.item is not None and iceberg_4.item.name == "ChuChu Spawn",
                        f"Multiworld did not place ChuChu, Seed: {self.multiworld.seed}")
        sand_canyon_6 = self.multiworld.get_location("Sand Canyon 6 - Animal 1", 1)
        self.assertTrue(sand_canyon_6.item is not None and sand_canyon_6.item.name in
                        {"Kine Spawn", "Coo Spawn"}, f"Multiworld did not place Coo/Kine, Seed: {self.multiworld.seed}")

    def test_problematic(self) -> None:
        for spawns in animal_friend_spawns.problematic_sets:
            placed = [self.multiworld.get_location(spawn, 1).item for spawn in spawns]
            placed_names = set([item.name for item in placed])
            self.assertEqual(len(placed), len(placed_names),
                             f"Duplicate animal placed in problematic locations:"
                             f" {[spawn.location for spawn in placed]}, "
                             f"Seed: {self.multiworld.seed}")

    def test_cutter_and_burning_reachable(self) -> None:
        rooms = self.multiworld.worlds[1].rooms
        copy_abilities = self.multiworld.worlds[1].copy_abilities
        sand_canyon_5 = self.multiworld.get_region("Sand Canyon 5 - 9", 1)
        assert isinstance(sand_canyon_5, KDL3Room)
        valid_rooms = [room for room in rooms if (room.level < sand_canyon_5.level)
                       or (room.level == sand_canyon_5.level and room.stage < sand_canyon_5.stage)]
        for room in valid_rooms:
            if any(copy_abilities[enemy] == "Cutter Ability" for enemy in room.enemies):
                break
        else:
            self.fail("Could not reach Cutter Ability before Sand Canyon 5!")
        iceberg_4 = self.multiworld.get_region("Iceberg 4 - 7", 1)
        assert isinstance(iceberg_4, KDL3Room)
        valid_rooms = [room for room in rooms if (room.level < iceberg_4.level)
                       or (room.level == iceberg_4.level and room.stage < iceberg_4.stage)]
        for room in valid_rooms:
            if any(copy_abilities[enemy] == "Burning Ability" for enemy in room.enemies):
                break
        else:
            self.fail("Could not reach Burning Ability before Iceberg 4!")

    def test_valid_abilities_for_ROB(self) -> None:
        # there exists a subset of 4-7 abilities that will allow us access to ROB heart star on default settings
        self.collect_by_name(["Heart Star", "Kine", "Coo"])  # we will guaranteed need Coo, Kine, and Heart Stars to reach
        # first we need to identify our bukiset requirements
        groups = [
            ({"Parasol Ability", "Cutter Ability"}, {'Bukiset (Parasol)', 'Bukiset (Cutter)'}),
            ({"Spark Ability", "Clean Ability"}, {'Bukiset (Spark)', 'Bukiset (Clean)'}),
            ({"Ice Ability", "Needle Ability"}, {'Bukiset (Ice)', 'Bukiset (Needle)'}),
            ({"Stone Ability", "Burning Ability"}, {'Bukiset (Stone)', 'Bukiset (Burning)'}),
        ]
        copy_abilities = self.multiworld.worlds[1].copy_abilities
        required_abilities: List[List[str]] = []
        for abilities, bukisets in groups:
            potential_abilities: List[str] = list()
            for bukiset in bukisets:
                if copy_abilities[bukiset] in abilities:
                    potential_abilities.append(copy_abilities[bukiset])
            required_abilities.append(potential_abilities)
        collected_abilities = list()
        for group in required_abilities:
            self.assertFalse(len(group) == 0, str(self.multiworld.seed))
            collected_abilities.append(group[0])
        self.collect_by_name([ability.replace(" Ability", "") for ability in collected_abilities])
        if "Parasol Ability" not in collected_abilities or "Stone Ability" not in collected_abilities:
            # required for non-Bukiset related portions
            self.collect_by_name(["Parasol", "Stone"])

        if "Cutter Ability" not in collected_abilities:
            # we can't actually reach 3-6 without Cutter
            self.assertFalse(self.can_reach_location("Sand Canyon 6 - Professor Hector & R.O.B"), str(self.multiworld.seed))
            self.collect_by_name(["Cutter"])

        self.assertTrue(self.can_reach_location("Sand Canyon 6 - Professor Hector & R.O.B"),
                        f"Seed: {self.multiworld.seed}, Collected: {collected_abilities}")
