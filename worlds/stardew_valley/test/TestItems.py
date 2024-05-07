import sys
import random
import sys

from BaseClasses import MultiWorld, get_seed
from . import setup_solo_multiworld, SVTestCase, allsanity_options_without_mods, get_minsanity_options
from .. import StardewValleyWorld
from ..items import Group, item_table
from ..options import Friendsanity, SeasonRandomization, Museumsanity, Shipsanity, Goal
from ..strings.wallet_item_names import Wallet

all_seasons = ["Spring", "Summer", "Fall", "Winter"]
all_farms = ["Standard Farm", "Riverland Farm", "Forest Farm", "Hill-top Farm", "Wilderness Farm", "Four Corners Farm", "Beach Farm"]


class TestItems(SVTestCase):
    def test_can_create_item_of_resource_pack(self):
        item_name = "Resource Pack: 500 Money"

        multi_world = MultiWorld(1)
        multi_world.game[1] = "Stardew Valley"
        multi_world.player_name = {1: "Tester"}
        world = StardewValleyWorld(multi_world, 1)
        item = world.create_item(item_name)

        assert item.name == item_name

    def test_items_table_footprint_is_between_717000_and_737000(self):
        item_with_lowest_id = min((item for item in item_table.values() if item.code is not None), key=lambda x: x.code)
        item_with_highest_id = max((item for item in item_table.values() if item.code is not None),
                                   key=lambda x: x.code)

        assert item_with_lowest_id.code >= 717000
        assert item_with_highest_id.code < 737000

    def test_babies_come_in_all_shapes_and_sizes(self):
        baby_permutations = set()
        options = {Friendsanity.internal_name: Friendsanity.option_bachelors}
        for attempt_number in range(50):
            if len(baby_permutations) >= 4:
                print(f"Already got all 4 baby permutations, breaking early [{attempt_number} generations]")
                break
            seed = get_seed()
            multiworld = setup_solo_multiworld(options, seed=seed, _cache={})
            baby_items = [item for item in multiworld.get_items() if "Baby" in item.name]
            self.assertEqual(len(baby_items), 2)
            baby_permutations.add(f"{baby_items[0]} - {baby_items[1]}")
        self.assertEqual(len(baby_permutations), 4)

    def test_correct_number_of_stardrops(self):
        allsanity_options = allsanity_options_without_mods()
        multiworld = setup_solo_multiworld(allsanity_options)
        stardrop_items = [item for item in multiworld.get_items() if "Stardrop" in item.name]
        self.assertEqual(len(stardrop_items), 7)

    def test_no_duplicate_rings(self):
        allsanity_options = allsanity_options_without_mods()
        multiworld = setup_solo_multiworld(allsanity_options)
        ring_items = [item.name for item in multiworld.get_items() if Group.RING in item_table[item.name].groups]
        self.assertEqual(len(ring_items), len(set(ring_items)))

    def test_can_start_in_any_season(self):
        starting_seasons_rolled = set()
        options = {SeasonRandomization.internal_name: SeasonRandomization.option_randomized}
        for attempt_number in range(50):
            if len(starting_seasons_rolled) >= 4:
                print(f"Already got all 4 starting seasons, breaking early [{attempt_number} generations]")
                break
            seed = get_seed()
            multiworld = setup_solo_multiworld(options, seed=seed, _cache={})
            starting_season_items = [item for item in multiworld.precollected_items[1] if item.name in all_seasons]
            season_items = [item for item in multiworld.get_items() if item.name in all_seasons]
            self.assertEqual(len(starting_season_items), 1)
            self.assertEqual(len(season_items), 3)
            starting_seasons_rolled.add(f"{starting_season_items[0]}")
        self.assertEqual(len(starting_seasons_rolled), 4)

    def test_can_start_on_any_farm(self):
        starting_farms_rolled = set()
        for attempt_number in range(60):
            if len(starting_farms_rolled) >= 7:
                print(f"Already got all 7 farm types, breaking early [{attempt_number} generations]")
                break
            seed = random.randrange(sys.maxsize)
            multiworld = setup_solo_multiworld(seed=seed, _cache={})
            starting_farm = multiworld.worlds[1].fill_slot_data()["farm_type"]
            starting_farms_rolled.add(starting_farm)
        self.assertEqual(len(starting_farms_rolled), 7)


class TestMetalDetectors(SVTestCase):
    def test_minsanity_1_metal_detector(self):
        options = get_minsanity_options()
        multiworld = setup_solo_multiworld(options)
        items = [item.name for item in multiworld.get_items() if item.name == Wallet.metal_detector]
        self.assertEquals(len(items), 1)

    def test_museumsanity_2_metal_detector(self):
        options = get_minsanity_options().copy()
        options[Museumsanity.internal_name] = Museumsanity.option_all
        multiworld = setup_solo_multiworld(options)
        items = [item.name for item in multiworld.get_items() if item.name == Wallet.metal_detector]
        self.assertEquals(len(items), 2)

    def test_shipsanity_full_shipment_1_metal_detector(self):
        options = get_minsanity_options().copy()
        options[Shipsanity.internal_name] = Shipsanity.option_full_shipment
        multiworld = setup_solo_multiworld(options)
        items = [item.name for item in multiworld.get_items() if item.name == Wallet.metal_detector]
        self.assertEquals(len(items), 1)

    def test_shipsanity_everything_2_metal_detector(self):
        options = get_minsanity_options().copy()
        options[Shipsanity.internal_name] = Shipsanity.option_everything
        multiworld = setup_solo_multiworld(options)
        items = [item.name for item in multiworld.get_items() if item.name == Wallet.metal_detector]
        self.assertEquals(len(items), 2)

    def test_complete_collection_2_metal_detector(self):
        options = get_minsanity_options().copy()
        options[Goal.internal_name] = Goal.option_complete_collection
        multiworld = setup_solo_multiworld(options)
        items = [item.name for item in multiworld.get_items() if item.name == Wallet.metal_detector]
        self.assertEquals(len(items), 2)

    def test_perfection_2_metal_detector(self):
        options = get_minsanity_options().copy()
        options[Goal.internal_name] = Goal.option_perfection
        multiworld = setup_solo_multiworld(options)
        items = [item.name for item in multiworld.get_items() if item.name == Wallet.metal_detector]
        self.assertEquals(len(items), 2)

    def test_maxsanity_4_metal_detector(self):
        options = get_minsanity_options().copy()
        options[Museumsanity.internal_name] = Museumsanity.option_all
        options[Shipsanity.internal_name] = Shipsanity.option_everything
        options[Goal.internal_name] = Goal.option_perfection
        multiworld = setup_solo_multiworld(options)
        items = [item.name for item in multiworld.get_items() if item.name == Wallet.metal_detector]
        self.assertEquals(len(items), 4)
