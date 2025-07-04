from .bases import SVTestBase
from ..options import ExcludeGingerIsland, Booksanity, Shipsanity
from ..strings.book_names import Book, LostBook

power_books = [Book.animal_catalogue, Book.book_of_mysteries,
               Book.the_alleyway_buffet, Book.the_art_o_crabbing, Book.dwarvish_safety_manual,
               Book.jewels_of_the_sea, Book.raccoon_journal, Book.woodys_secret, Book.jack_be_nimble_jack_be_thick, Book.friendship_101,
               Book.monster_compendium, Book.mapping_cave_systems, Book.treasure_appraisal_guide, Book.way_of_the_wind_pt_1, Book.way_of_the_wind_pt_2,
               Book.horse_the_book, Book.ol_slitherlegs, Book.price_catalogue, Book.the_diamond_hunter, ]

skill_books = [Book.combat_quarterly, Book.woodcutters_weekly, Book.book_of_stars, Book.stardew_valley_almanac, Book.bait_and_bobber, Book.mining_monthly,
               Book.queen_of_sauce_cookbook, ]

lost_books = [
    LostBook.tips_on_farming, LostBook.this_is_a_book_by_marnie, LostBook.on_foraging, LostBook.the_fisherman_act_1,
    LostBook.how_deep_do_the_mines_go, LostBook.an_old_farmers_journal, LostBook.scarecrows, LostBook.the_secret_of_the_stardrop,
    LostBook.journey_of_the_prairie_king_the_smash_hit_video_game, LostBook.a_study_on_diamond_yields, LostBook.brewmasters_guide,
    LostBook.mysteries_of_the_dwarves, LostBook.highlights_from_the_book_of_yoba, LostBook.marriage_guide_for_farmers, LostBook.the_fisherman_act_ii,
    LostBook.technology_report, LostBook.secrets_of_the_legendary_fish, LostBook.gunther_tunnel_notice, LostBook.note_from_gunther,
    LostBook.goblins_by_m_jasper, LostBook.secret_statues_acrostics, ]

lost_book = "Progressive Lost Book"


class TestBooksanityNone(SVTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Shipsanity: Shipsanity.option_everything,
        Booksanity: Booksanity.option_none,
    }

    def test_no_power_books_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for book in power_books:
            with self.subTest(book):
                self.assertNotIn(f"Read {book}", location_names)

    def test_no_skill_books_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for book in skill_books:
            with self.subTest(book):
                self.assertNotIn(f"Read {book}", location_names)

    def test_no_lost_books_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for book in lost_books:
            with self.subTest(book):
                self.assertNotIn(f"Read {book}", location_names)

    def test_no_power_items(self):
        item_names = {location.name for location in self.multiworld.get_items()}
        for book in power_books:
            with self.subTest(book):
                self.assertNotIn(f"Power: {book}", item_names)
        with self.subTest(lost_book):
            self.assertNotIn(lost_book, item_names)

    def test_can_ship_all_books(self):
        self.collect_everything()
        shipsanity_prefix = "Shipsanity: "
        for location in self.multiworld.get_locations():
            if not location.name.startswith(shipsanity_prefix):
                continue

            item_to_ship = location.name[len(shipsanity_prefix):]
            if item_to_ship not in power_books and item_to_ship not in skill_books:
                continue

            with self.subTest(location.name):
                self.assert_can_reach_location(location)


class TestBooksanityPowers(SVTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Shipsanity: Shipsanity.option_everything,
        Booksanity: Booksanity.option_power,
    }

    def test_all_power_books_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for book in power_books:
            with self.subTest(book):
                self.assertIn(f"Read {book}", location_names)

    def test_no_skill_books_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for book in skill_books:
            with self.subTest(book):
                self.assertNotIn(f"Read {book}", location_names)

    def test_no_lost_books_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for book in lost_books:
            with self.subTest(book):
                self.assertNotIn(f"Read {book}", location_names)

    def test_all_power_items(self):
        item_names = {location.name for location in self.multiworld.get_items()}
        for book in power_books:
            with self.subTest(book):
                self.assertIn(f"Power: {book}", item_names)
        with self.subTest(lost_book):
            self.assertNotIn(lost_book, item_names)

    def test_can_ship_all_books(self):
        self.collect_everything()
        shipsanity_prefix = "Shipsanity: "
        for location in self.multiworld.get_locations():
            if not location.name.startswith(shipsanity_prefix):
                continue

            item_to_ship = location.name[len(shipsanity_prefix):]
            if item_to_ship not in power_books and item_to_ship not in skill_books:
                continue

            with self.subTest(location.name):
                self.assert_can_reach_location(location)


class TestBooksanityPowersAndSkills(SVTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Shipsanity: Shipsanity.option_everything,
        Booksanity: Booksanity.option_power_skill,
    }

    def test_all_power_books_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for book in power_books:
            with self.subTest(book):
                self.assertIn(f"Read {book}", location_names)

    def test_all_skill_books_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for book in skill_books:
            with self.subTest(book):
                self.assertIn(f"Read {book}", location_names)

    def test_no_lost_books_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for book in lost_books:
            with self.subTest(book):
                self.assertNotIn(f"Read {book}", location_names)

    def test_all_power_items(self):
        item_names = {location.name for location in self.multiworld.get_items()}
        for book in power_books:
            with self.subTest(book):
                self.assertIn(f"Power: {book}", item_names)
        with self.subTest(lost_book):
            self.assertNotIn(lost_book, item_names)

    def test_can_ship_all_books(self):
        self.collect_everything()
        shipsanity_prefix = "Shipsanity: "
        for location in self.multiworld.get_locations():
            if not location.name.startswith(shipsanity_prefix):
                continue

            item_to_ship = location.name[len(shipsanity_prefix):]
            if item_to_ship not in power_books and item_to_ship not in skill_books:
                continue

            with self.subTest(location.name):
                self.assert_can_reach_location(location)


class TestBooksanityAll(SVTestBase):
    options = {
        ExcludeGingerIsland: ExcludeGingerIsland.option_false,
        Shipsanity: Shipsanity.option_everything,
        Booksanity: Booksanity.option_all,
    }

    def test_all_power_books_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for book in power_books:
            with self.subTest(book):
                self.assertIn(f"Read {book}", location_names)

    def test_all_skill_books_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for book in skill_books:
            with self.subTest(book):
                self.assertIn(f"Read {book}", location_names)

    def test_all_lost_books_locations(self):
        location_names = {location.name for location in self.multiworld.get_locations()}
        for book in lost_books:
            with self.subTest(book):
                self.assertIn(f"Read {book}", location_names)

    def test_all_power_items(self):
        item_names = {location.name for location in self.multiworld.get_items()}
        for book in power_books:
            with self.subTest(book):
                self.assertIn(f"Power: {book}", item_names)
        with self.subTest(lost_book):
            self.assertIn(lost_book, item_names)

    def test_can_ship_all_books(self):
        self.collect_everything()
        shipsanity_prefix = "Shipsanity: "
        for location in self.multiworld.get_locations():
            if not location.name.startswith(shipsanity_prefix):
                continue

            item_to_ship = location.name[len(shipsanity_prefix):]
            if item_to_ship not in power_books and item_to_ship not in skill_books:
                continue

            with self.subTest(location.name):
                self.assert_can_reach_location(location)
