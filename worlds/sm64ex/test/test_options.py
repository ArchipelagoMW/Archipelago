from .bases import SM64TestBase
from .. import Options
from ..Locations import loc100Coin_table, location_table
from ..Regions import sm64_entrances_to_level, sm64_level_to_paintings, sm64_level_to_secrets, valid_move_randomizer_start_courses

valid_move_randomizer_start_entrances = {
    level: entrance
    for (level, entrance) in sm64_entrances_to_level.items()
    if level in valid_move_randomizer_start_courses
}

# Coin Star Logic
class EnableCoinStarsTestBase(SM64TestBase):
    options = {
        "enable_coin_stars": Options.EnableCoinStars.option_on
    }

    # Ensure Coin Star locations are created
    def test_coin_star_locations(self):
        possible_locations = self.world.location_names
        for loc in loc100Coin_table:
            # Use subtest to force all locations to be tested
            with self.subTest("Location created", location=loc):
                assert loc in possible_locations

class DisableCoinStarsTestBase(SM64TestBase):
    options = {
        "enable_coin_stars": Options.EnableCoinStars.option_off
    }

    # Ensure Coin Star locations are not created
    def test_coin_star_locations(self):
        possible_locations = self.world.get_locations()
        for loc in loc100Coin_table:
            # Use subtest to force all locations to be tested
            with self.subTest("Location not created", location=loc):
                assert loc not in possible_locations

class VanillaCoinStarsTestBase(SM64TestBase):
    options = {
        "enable_coin_stars": Options.EnableCoinStars.option_vanilla
    }

    # Ensure Coin Star locations are created
    def test_coin_star_locations(self):
        possible_locations = self.world.location_names
        for loc in loc100Coin_table:
            # Use subtest to force all locations to be tested
            with self.subTest("Location created", location=loc):
                assert loc in possible_locations

    # Vanilla Coin Stars should give the player their own Power Stars
    def test_items_in_coin_star_locations(self):
        for loc in loc100Coin_table:
            # Use subtest to force all locations to be tested
            with self.subTest("Location created", location=loc):
                item_in_loc = self.world.get_location(loc).item
                assert item_in_loc.name == "Power Star"
                # By default, these test bases are single player multiworld.
                # In any other case, we should test that they belong to their respective worlds.


# Exclamation Boxes
class ExclamationBoxesOnTestBase(SM64TestBase):
    options = {
        "exclamation_boxes": Options.ExclamationBoxes.option_true,
    }

class ExclamationBoxesOffTestBase(SM64TestBase):
    options = {
        "exclamation_boxes": Options.ExclamationBoxes.option_false,
    }

    # Should populate the boxes with the players own 1Up Mushrooms
    def test_items_in_exclamation_box_locations(self):
        # Get 1Up Block locations
        loc1ups_table = {name for name in location_table.keys() if "1Up Block" in name}
        for loc in loc1ups_table:
            # Use subtest to force all locations to be tested
            with self.subTest("Location has own 1Up Mushroom.", location=loc):
                item_in_loc = self.world.get_location(loc).item
                assert item_in_loc.name == "1Up Mushroom"
                # By default, these test bases are single player multiworld.
                # In any other case, we should test that they belong to their respective worlds.

# Entrance Randomizer
class EntranceRandoOffTestBase(SM64TestBase):
    options = {
        "area_rando": Options.AreaRandomizer.option_Off
    }
    # Ensure entrance rando disabled
    def test_BoB_entrance(self):
        bob_level_id = sm64_entrances_to_level["Bob-omb Battlefield"]
        assert self.world.area_connections[bob_level_id] == bob_level_id

    def test_BitFS_entrance(self):
        bitfs_level_id = sm64_entrances_to_level["Bowser in the Fire Sea"]
        assert self.world.area_connections[bitfs_level_id] == bitfs_level_id

class EntranceRandoCourseTestBase(SM64TestBase):
    options = {
        "area_rando": Options.AreaRandomizer.option_Courses_Only
    }

    def test_BoB_entrance(self):
        bob_level_id = sm64_entrances_to_level["Bob-omb Battlefield"]
        # BoB goes to a painting, not a secret
        assert self.world.area_connections[bob_level_id] not in sm64_level_to_secrets.keys()
        assert self.world.area_connections[bob_level_id] in sm64_level_to_paintings.keys()

    def test_BitFS_entrance(self):
        bitfs_level_id = sm64_entrances_to_level["Bowser in the Fire Sea"]
        # BitFS is a secret (aka not a course), unaffected by Course Only entrance rando.
        assert self.world.area_connections[bitfs_level_id] == bitfs_level_id

class EntranceRandoSeparateTestBase(SM64TestBase):
    options = {
        "area_rando": Options.AreaRandomizer.option_Courses_and_Secrets_Separate
    }

    def test_BoB_entrance(self):
        bob_level_id = sm64_entrances_to_level["Bob-omb Battlefield"]
        # BoB goes to a painting, not a secret
        assert self.world.area_connections[bob_level_id] not in sm64_level_to_secrets.keys()
        assert self.world.area_connections[bob_level_id] in sm64_level_to_paintings.keys()

    def test_BitFS_entrance(self):
        bitfs_level_id = sm64_entrances_to_level["Bowser in the Fire Sea"]
        # BitFS goes to a secret, not a painting
        assert self.world.area_connections[bitfs_level_id] in sm64_level_to_secrets.keys()
        assert self.world.area_connections[bitfs_level_id] not in sm64_level_to_paintings.keys()
        # BitFS does not go to DDD
        assert self.world.area_connections[bitfs_level_id] != sm64_entrances_to_level["Dire, Dire Docks"]

class EntranceRandoAllTestBase(SM64TestBase):
    options = {
        "area_rando": Options.AreaRandomizer.option_Courses_and_Secrets
    }

    def test_BitFS_entrance(self):
        bitfs_level_id = sm64_entrances_to_level["Bowser in the Fire Sea"]
        # BitFS does not go to DDD
        assert self.world.area_connections[bitfs_level_id] != sm64_entrances_to_level["Dire, Dire Docks"]


# Completion Type
class CompletionLastBowserTestBase(SM64TestBase):
    options = {
        "completion_type": Options.CompletionType.option_Last_Bowser_Stage
    }

class CompletionAllBowserTestBase(SM64TestBase):
    options = {
        "completion_type": Options.CompletionType.option_All_Bowser_Stages
    }



# Option Combos


# Smallest Power Star count possible
class MinimumStarsPossibleTestBase(SM64TestBase):
    options = {
        "amount_of_stars": Options.AmountOfStars.range_start,
        "enable_move_rando": Options.EnableMoveRandomizer.option_true,
        "exclamation_boxes": Options.ExclamationBoxes.option_false,
        "enable_coin_stars": Options.EnableCoinStars.option_off
    }

    # There will be less Power Stars than filler with this low of a star count
    def test_stars_vs_filler(self):
        filler_count = len(self.get_items_by_name("1Up Mushroom"))
        star_count = len(self.get_items_by_name("Power Star"))
        self.assertGreater(filler_count, star_count)


# Entrance + Move Randos
class CourseEntrancesMoveTestBase(SM64TestBase):
    options = {
        "enable_move_rando": Options.EnableMoveRandomizer.option_true,
        "area_rando": Options.AreaRandomizer.option_Courses_Only
    }

    def test_BoB_entrance(self):
        bob_level_id = sm64_entrances_to_level["Bob-omb Battlefield"]
        # BoB goes to a course, not a secret.
        assert self.world.area_connections[bob_level_id] not in sm64_level_to_secrets.keys()
        assert self.world.area_connections[bob_level_id] in sm64_level_to_paintings.keys()
        # BoB goes to level with at least one star without a movement rule.
        assert self.world.area_connections[bob_level_id] in valid_move_randomizer_start_entrances.values()

    def test_BitFS_entrance(self):
        bitfs_level_id = sm64_entrances_to_level["Bowser in the Fire Sea"]
        # BitFS is a secret (aka not a course), unaffected by Course Only entrance rando.
        assert self.world.area_connections[bitfs_level_id] == bitfs_level_id

    def test_WF_entrance(self):
        wf_level_id = sm64_entrances_to_level["Whomp's Fortress"]
        # WF goes to level with at least one star without a movement rule.
        assert self.world.area_connections[wf_level_id] in valid_move_randomizer_start_entrances.values()

class SeparateEntrancesMoveTestBase(SM64TestBase):
    options = {
        "enable_move_rando": Options.EnableMoveRandomizer.option_true,
        "area_rando": Options.AreaRandomizer.option_Courses_and_Secrets_Separate
    }

    def test_BoB_entrance(self):
        bob_level_id = sm64_entrances_to_level["Bob-omb Battlefield"]
        # BoB goes to a course, not a secret.
        assert self.world.area_connections[bob_level_id] not in sm64_level_to_secrets.keys()
        assert self.world.area_connections[bob_level_id] in sm64_level_to_paintings.keys()
        # BoB goes to level with at least one star without a movement rule.
        assert self.world.area_connections[bob_level_id] in valid_move_randomizer_start_entrances.values()

    def test_BitFS_entrance(self):
        bitfs_level_id = sm64_entrances_to_level["Bowser in the Fire Sea"]
        # BitFS does not go to DDD.
        assert self.world.area_connections[bitfs_level_id] != sm64_entrances_to_level["Dire, Dire Docks"]

    def test_WF_entrance(self):
        wf_level_id = sm64_entrances_to_level["Whomp's Fortress"]
        # WF goes to level with at least one star without a movement rule.
        assert self.world.area_connections[wf_level_id] in valid_move_randomizer_start_entrances.values()


class AllEntrancesMoveTestBase(SM64TestBase):
    options = {
        "enable_move_rando": Options.EnableMoveRandomizer.option_true,
        "area_rando": Options.AreaRandomizer.option_Courses_and_Secrets
    }

    def test_BoB_entrance(self):
        bob_level_id = sm64_entrances_to_level["Bob-omb Battlefield"]
        # BoB goes to level with at least one star without a movement rule.
        assert self.world.area_connections[bob_level_id] in valid_move_randomizer_start_entrances.values()

    def test_BitFS_entrance(self):
        bitfs_level_id = sm64_entrances_to_level["Bowser in the Fire Sea"]
        # BitFS does not go to DDD.
        assert self.world.area_connections[bitfs_level_id] != sm64_entrances_to_level["Dire, Dire Docks"]

    def test_WF_entrance(self):
        wf_level_id = sm64_entrances_to_level["Whomp's Fortress"]
        # WF goes to level with at least one star without a movement rule.
        assert self.world.area_connections[wf_level_id] in valid_move_randomizer_start_entrances.values()

    def test_CotMC_entrance(self):
        cotmc_level_id = sm64_entrances_to_level["Cavern of the Metal Cap"]
        # CotMC does not go to HMC.
        assert self.world.area_connections[cotmc_level_id] != sm64_entrances_to_level["Hazy Maze Cave"]
        # If BitFS -> HMC, CotMC does not go to DDD.
        bitfs_level_id = sm64_entrances_to_level["Bowser in the Fire Sea"]
        if self.world.area_connections[bitfs_level_id] == sm64_entrances_to_level["Hazy Maze Cave"]:
            assert self.world.area_connections[cotmc_level_id] != sm64_entrances_to_level["Dire, Dire Docks"]

# No Strict Requirements
class NoStrictRequirementsTestBase(SM64TestBase):
    options = {
        "enable_move_rando": Options.EnableMoveRandomizer.option_true,
        "buddy_checks": Options.BuddyChecks.option_true,
        "strict_move_requirements": Options.StrictMoveRequirements.option_false,
        "strict_cap_requirements": Options.StrictCapRequirements.option_false,
        "strict_cannon_requirements": Options.StrictCannonRequirements.option_false,
    }
