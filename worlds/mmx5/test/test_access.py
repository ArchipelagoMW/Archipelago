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
