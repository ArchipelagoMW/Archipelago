"""
Slow-running tests that are run infrequently.
Run this file explicitly with `python3 -m unittest worlds.sc2.test.slow_tests`
"""
from .test_base import Sc2SetupTestBase

from Fill import FillError
from .. import mission_tables, options


class LargeTests(Sc2SetupTestBase):
    def test_any_starter_mission_works(self) -> None:
        base_options = {
            options.OPTION_NAME[options.SelectedRaces]: list(options.SelectedRaces.valid_keys),
            options.OPTION_NAME[options.RequiredTactics]: options.RequiredTactics.option_standard,
            options.OPTION_NAME[options.MissionOrder]: options.MissionOrder.option_custom,
            options.OPTION_NAME[options.ExcludeOverpoweredItems]: True,
            # options.OPTION_NAME[options.ExtraLocations]: options.ExtraLocations.option_disabled,
            options.OPTION_NAME[options.VanillaLocations]: options.VanillaLocations.option_disabled,
        }
        missions_to_check = [
            mission for mission in mission_tables.SC2Mission
            if mission.pool == mission_tables.MissionPools.STARTER
        ]
        failed_missions: list[tuple[mission_tables.SC2Mission, int]] = []
        NUM_ATTEMPTS = 3
        for mission in missions_to_check:
            for attempt in range(NUM_ATTEMPTS):
                mission_options = base_options | {
                    options.OPTION_NAME[options.CustomMissionOrder]: {
                        "Test Campaign": {
                            "Test Layout": {
                                "type": "hopscotch",
                                "size": 25,
                                "goal": True,
                                "missions": [
                                    {"index": 0, "mission_pool": [mission.mission_name]}
                                ]
                            }
                        }
                    }
                }
                try:
                    self.generate_world(mission_options)
                    self.fill_after_generation()
                    assert self.multiworld.worlds[1].custom_mission_order.get_starting_missions()[0] == mission
                except FillError as ex:
                    failed_missions.append((mission, self.multiworld.seed))
        if failed_missions:
            for failed_mission in failed_missions:
                print(failed_mission)
            self.assertFalse(failed_missions)
