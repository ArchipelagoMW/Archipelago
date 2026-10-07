from ...mods.mod_data import ModNames
from ...options import Booksanity, ExcludeGingerIsland, Mods, Shipsanity
from ...strings.ap_names.mods.mod_items import ModBooks
from ..bases import SVTestBase

ModSkillBooks = [ModBooks.digging_like_worms]
ModPowerBooks = []


class TestModBooksanityNone(SVTestBase):
    options = {  # noqa: RUF012
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Shipsanity: Shipsanity.option_everything,
        Booksanity: Booksanity.option_none,
        Mods.internal_name: frozenset(ModNames.enabled_mods_except_invalid_combinations()),
    }

    def test_no_mod_power_books_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for book in ModPowerBooks:
            with self.subTest(book):
                self.assertNotIn(f"Read {book}", location_names)

    def test_no_mod_skill_books_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for book in ModSkillBooks:
            with self.subTest(book):
                self.assertNotIn(f"Read {book}", location_names)

    def test_no_power_items(self):
        item_names = {location.name for location in self.multiworld.get_items()}
        for book in ModPowerBooks:
            with self.subTest(book):
                self.assertNotIn(f"Power: {book}", item_names)

    def test_can_ship_all_mod_books(self):
        self.collect_everything()
        shipsanity_prefix = "Shipsanity: "
        for location in self.multiworld.get_locations():
            if not location.name.startswith(shipsanity_prefix):
                continue

            item_to_ship = location.name[len(shipsanity_prefix):]
            if item_to_ship not in ModPowerBooks and item_to_ship not in ModSkillBooks:
                continue

            with self.subTest(location.name):
                self.assert_can_reach_location(location)


class TestModBooksanityPowers(SVTestBase):
    options = {  # noqa: RUF012
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Shipsanity: Shipsanity.option_everything,
        Booksanity: Booksanity.option_power,
        Mods.internal_name: frozenset(ModNames.enabled_mods_except_invalid_combinations()),
    }

    def test_all_modp_ower_books_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for book in ModPowerBooks:
            with self.subTest(book):
                self.assertIn(f"Read {book}", location_names)

    def test_no_mod_skill_books_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for book in ModSkillBooks:
            with self.subTest(book):
                self.assertNotIn(f"Read {book}", location_names)

    def test_all_power_items(self):
        item_names = {location.name for location in self.multiworld.get_items()}
        for book in ModPowerBooks:
            with self.subTest(book):
                self.assertIn(f"Power: {book}", item_names)

    def test_can_ship_all_books(self):
        self.collect_everything()
        shipsanity_prefix = "Shipsanity: "
        for location in self.multiworld.get_locations():
            if not location.name.startswith(shipsanity_prefix):
                continue

            item_to_ship = location.name[len(shipsanity_prefix):]
            if item_to_ship not in ModPowerBooks and item_to_ship not in ModSkillBooks:
                continue

            with self.subTest(location.name):
                self.assert_can_reach_location(location)


class TestBooksanityPowersAndSkills(SVTestBase):
    options = {  # noqa: RUF012
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Shipsanity: Shipsanity.option_everything,
        Booksanity: Booksanity.option_power_skill,
        Mods.internal_name: frozenset(ModNames.enabled_mods_except_invalid_combinations()),
    }

    def test_all_mod_power_books_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for book in ModPowerBooks:
            with self.subTest(book):
                self.assertIn(f"Read {book}", location_names)

    def test_all_mod_skill_books_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for book in ModSkillBooks:
            with self.subTest(book):
                self.assertIn(f"Read {book}", location_names)

    def test_all_power_items(self):
        item_names = {location.name for location in self.multiworld.get_items()}
        for book in ModPowerBooks:
            with self.subTest(book):
                self.assertIn(f"Power: {book}", item_names)

    def test_can_ship_all_books(self):
        self.collect_everything()
        shipsanity_prefix = "Shipsanity: "
        for location in self.multiworld.get_locations():
            if not location.name.startswith(shipsanity_prefix):
                continue

            item_to_ship = location.name[len(shipsanity_prefix):]
            if item_to_ship not in ModPowerBooks and item_to_ship not in ModSkillBooks:
                continue

            with self.subTest(location.name):
                self.assert_can_reach_location(location)


class TestBooksanityAll(SVTestBase):
    options = {  # noqa: RUF012
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Shipsanity: Shipsanity.option_everything,
        Booksanity: Booksanity.option_all,
        Mods.internal_name: frozenset(ModNames.enabled_mods_except_invalid_combinations()),
    }

    def test_digging_like_worms_require_2_levels(self):
        read_location = self.world.get_location("Read Digging Like Worms")
        ship_location = self.world.get_location("Shipsanity: Digging Like Worms")
        self.collect("Shipping Bin")
        self.collect("Progressive Hoe")
        self.collect_months(2)

        self.assert_cannot_reach_location(read_location)
        self.assert_cannot_reach_location(ship_location)

        self.collect("Archaeology Level")
        self.collect("Archaeology Level")

        self.assert_can_reach_location(read_location)
        self.assert_can_reach_location(ship_location)

    def test_all_mod_power_books_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for book in ModPowerBooks:
            with self.subTest(book):
                self.assertIn(f"Read {book}", location_names)

    def test_all_mod_skill_books_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for book in ModSkillBooks:
            with self.subTest(book):
                self.assertIn(f"Read {book}", location_names)

    def test_all_power_items(self):
        item_names = {location.name for location in self.multiworld.get_items()}
        for book in ModPowerBooks:
            with self.subTest(book):
                self.assertIn(f"Power: {book}", item_names)

    def test_can_ship_all_books(self):
        self.collect_everything()
        shipsanity_prefix = "Shipsanity: "
        for location in self.multiworld.get_locations():
            if not location.name.startswith(shipsanity_prefix):
                continue

            item_to_ship = location.name[len(shipsanity_prefix):]
            if item_to_ship not in ModPowerBooks and item_to_ship not in ModSkillBooks:
                continue

            with self.subTest(location.name):
                self.assert_can_reach_location(location)
