from BaseClasses import MultiWorld
from worlds.minecraft import minecraft_create_regions, minecraft_gen_item_pool
from worlds.minecraft.Rules import set_rules
from test.TestBase import TestBase


class TestMinecraft(TestBase):
    def setUp(self):
        self.world = MultiWorld(1)
        self.world.game[1] = "Minecraft"
        exclusion_pools = ['hard', 'insane', 'postgame']
        for pool in exclusion_pools:
            setattr(self.world, f"exclude_{pool}_advancements", False)
        minecraft_create_regions(self.world, 1)
        minecraft_gen_item_pool(self.world, 1)
        set_rules(self.world, 1)
