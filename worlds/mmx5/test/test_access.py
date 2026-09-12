from .. import names
from . import MMX5TestBase

FALCON = [names.FALCON_HEAD, names.FALCON_BODY, names.FALCON_ARM, names.FALCON_LEG]
GAEA = [names.GAEA_HEAD, names.GAEA_BODY, names.GAEA_ARM, names.GAEA_LEG]


class TestArmorGating(MMX5TestBase):
    def test_gaea_hearts_require_full_gaea_set(self) -> None:
        hearts = [names.heart_location(s) for s in
                  (names.GRIZZLY, names.KRAKEN, names.FIREFLY, names.ROSERED)]
        self.assertAccessDependency(hearts, [GAEA], only_check_listed=True)

    def test_falcon_gated_locations_require_full_falcon_set(self) -> None:
        locations = [
            names.heart_location(names.WHALE),
            names.capsule_location(names.PEGASUS),
            names.capsule_location(names.DINOREX),
            names.capsule_location(names.ROSERED),
            names.tank_location(names.NECROBAT),
        ]
        self.assertAccessDependency(locations, [FALCON], only_check_listed=True)

    def test_weapon_gated_capsules(self) -> None:
        self.assertAccessDependency([names.capsule_location(names.WHALE)],
                                    [[names.GOO_SHAVER]], only_check_listed=True)
        self.assertAccessDependency([names.capsule_location(names.FIREFLY)],
                                    [[names.CSHOT]], only_check_listed=True)
        self.assertAccessDependency([names.capsule_location(names.NECROBAT)],
                                    [[names.F_LASER]], only_check_listed=True)

    def test_sigma_stages_require_all_weapons(self) -> None:
        weapons = [names.BOSS_WEAPON[s] for s in names.STAGES]
        self.assertAccessDependency([names.VICTORY], [weapons], only_check_listed=True)


class TestLaunchGoal(MMX5TestBase):
    options = {"goal": "launch"}

    def test_launcher_parts_are_progression(self) -> None:
        # Completion requires all 4 Enigma + all 4 Shuttle parts.
        self.collect_all_but([names.ENIGMA_PART])
        self.assertBeatable(False)
        self.collect_by_name(names.ENIGMA_PART)
        self.assertBeatable(True)


class TestGoalSlotData(MMX5TestBase):
    """slot_data is the only channel the goal takes to the client, and the
    client's whole all_mavericks behaviour keys off that one int. Generating
    the option correctly is worthless if the value does not arrive."""
    options = {"goal": "all_mavericks"}

    def test_all_mavericks_reaches_the_client_as_goal_2(self) -> None:
        from ..client import GOAL_ALL_MAVERICKS
        slot_data = self.multiworld.worlds[self.player].fill_slot_data()
        self.assertEqual(slot_data["goal"], GOAL_ALL_MAVERICKS,
                         "the client reads slot_data['goal'] and would fall "
                         "back to the permissive sigma behaviour")

    def test_the_goal_needs_the_eight_weapons_in_logic(self) -> None:
        # Logic gates Sigma on the 8 WEAPONS (items, receivable from any
        # world), while the goal's in-game requirement is 8 KILLS (local only,
        # enforced by the client). Different requirements - this pins the
        # logical half so the two do not silently drift into one another.
        from ..items import item_groups
        self.assertBeatable(False)
        self.collect_by_name(sorted(item_groups["Weapons"]))
        self.assertBeatable(True)


class TestSigmaSlotData(MMX5TestBase):
    options = {"goal": "sigma"}

    def test_sigma_still_reaches_the_client_as_goal_0(self) -> None:
        from ..client import GOAL_SIGMA
        slot_data = self.multiworld.worlds[self.player].fill_slot_data()
        self.assertEqual(slot_data["goal"], GOAL_SIGMA)
