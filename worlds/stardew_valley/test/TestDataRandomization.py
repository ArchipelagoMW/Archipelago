from .bases import SVTestBase
from ..data.requirement import SkillRequirement, MasteryRequirement
from ..data.shop import ShopSource
from ..options.options import DataRandomization, DataRandomizationBehavior
from ..strings.region_names import Region
from ..strings.skill_names import Skill
from ..strings.tool_names import FishingRod


class TestDataRandomizationRequirements(SVTestBase):
    options = {
        DataRandomization.internal_name: DataRandomization.preset_all,
        DataRandomizationBehavior.internal_name: DataRandomizationBehavior.option_randomized
    }

    def test_training_bamboo_rod_requirements(self):
        content = self.world.content
        tools = content.tool_upgrades
        rods = [FishingRod.training, FishingRod.bamboo]
        for rod_name in rods:
            with self.subTest(rod_name):
                rod = tools[rod_name]
                for source in rod.sources:
                    if isinstance(source, ShopSource):
                        self.assertEqual(source.shop_region, Region.fish_shop)
                        self.assertEqual(len(source.other_requirements), 0)
                        return
                self.fail(f"{rod_name} should have a ShopSource with no other requirements")

    def test_fiberglass_iridium_rod_requirements(self):
        content = self.world.content
        tools = content.tool_upgrades
        rods = [FishingRod.fiberglass, FishingRod.iridium]
        for rod_name in rods:
            with self.subTest(rod_name):
                rod = tools[rod_name]
                for source in rod.sources:
                    if isinstance(source, ShopSource):
                        self.assertEqual(source.shop_region, Region.fish_shop)
                        self.assertEqual(len(source.other_requirements), 1)
                        other_requirement = source.other_requirements[0]
                        if isinstance(other_requirement, SkillRequirement):
                            self.assertTrue(other_requirement.skill == Skill.fishing)
                            level = 2 if rod_name == FishingRod.fiberglass else 6
                            self.assertTrue(other_requirement.level == level)
                            return
                        self.fail(f"{rod_name} should have a SkillRequirement")
                self.fail(f"{rod_name} should have a ShopSource with a SkillRequirement")

    def test_advanced_iridium_rod_requirements(self):
        content = self.world.content
        tools = content.tool_upgrades
        rod_name = FishingRod.advanced_iridium
        rod = tools[rod_name]
        for source in rod.sources:
            if isinstance(source, ShopSource):
                self.assertEqual(source.shop_region, Region.fish_shop)
                self.assertEqual(len(source.other_requirements), 1)
                other_requirement = source.other_requirements[0]
                if isinstance(other_requirement, MasteryRequirement):
                    self.assertTrue(other_requirement.skill == Skill.fishing)
                    return
                self.fail(f"{rod_name} should have a MasteryRequirement")
        self.fail(f"{rod_name} should have a ShopSource with a MasteryRequirement")