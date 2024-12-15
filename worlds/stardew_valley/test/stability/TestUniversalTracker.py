import unittest
from unittest.mock import Mock

from .. import SVTestBase, create_args, allsanity_mods_6_x_x
from ... import STARDEW_VALLEY, FarmType, BundleRandomization, EntranceRandomization


class TestUniversalTrackerGenerationIsStable(SVTestBase):
    options = allsanity_mods_6_x_x()
    options.update({
        EntranceRandomization.internal_name: EntranceRandomization.option_buildings,
        BundleRandomization.internal_name: BundleRandomization.option_shuffled,
        FarmType.internal_name: FarmType.option_standard,  # Need to choose one  otherwise it's random
    })

    def test_all_locations_and_items_are_the_same_between_two_generations(self):
        # This might open a kivy window temporarily, but it's the only way to test this...
        if self.skip_long_tests:
            raise unittest.SkipTest("Long tests disabled")

        try:
            # This test only run if UT is present, so no risk of running in the CI.
            from worlds.tracker.TrackerClient import TrackerGameContext  # noqa
        except ImportError:
            raise unittest.SkipTest("UT not loaded, skipping test")

        slot_data = self.world.fill_slot_data()
        ut_data = self.world.interpret_slot_data(slot_data)

        fake_context = Mock()
        fake_context.re_gen_passthrough = {STARDEW_VALLEY: ut_data}
        args = create_args({0: self.options})
        args.outputpath = None
        args.outputname = None
        args.multi = 1
        args.race = None
        args.plando_options = self.multiworld.plando_options
        args.plando_items = self.multiworld.plando_items
        args.plando_texts = self.multiworld.plando_texts
        args.plando_connections = self.multiworld.plando_connections
        args.game = self.multiworld.game
        args.name = self.multiworld.player_name
        args.sprite = {}
        args.sprite_pool = {}
        args.skip_output = True

        generated_multi_world = TrackerGameContext.TMain(fake_context, args, self.multiworld.seed)
        generated_slot_data = generated_multi_world.worlds[1].fill_slot_data()

        # Just checking slot data should prove that UT generates the same result as AP generation.
        self.maxDiff = None
        self.assertEqual(slot_data, generated_slot_data)
