import worlds.minecraft.Options
from test.TestBase import TestBase
from BaseClasses import MultiWorld
from worlds.minecraft import minecraft_gen_item_pool
from worlds.minecraft.Regions import minecraft_create_regions, link_minecraft_structures
from worlds.minecraft.Rules import set_rules
from worlds.minecraft.Items import MinecraftItem, item_table
import Options

# Converts the name of an item into an item object
def MCItemFactory(items, player: int):
    ret = []
    singleton = False
    if isinstance(items, str):
        items = [items]
        singleton = True
    for item in items:
        if item in item_table:
            ret.append(MinecraftItem(item, item_table[item].progression, item_table[item].code, player))
        else:
            raise Exception(f"Unknown item {item}")

    if singleton:
        return ret[0]
    return ret

class TestMinecraft(TestBase):

    def setUp(self):
        self.world = MultiWorld(1)
        self.world.game[1] = "Minecraft"
        exclusion_pools = ['hard', 'insane', 'postgame']
        for pool in exclusion_pools:
            setattr(self.world, f"include_{pool}_advancements", [False, False])
        setattr(self.world, "advancement_goal", [0, worlds.minecraft.Options.AdvancementGoal(value=0)])
        setattr(self.world, "shuffle_structures", [False, False])
        setattr(self.world, "combat_difficulty", [0, worlds.minecraft.Options.CombatDifficulty(value=1)])
        minecraft_create_regions(self.world, 1)
        link_minecraft_structures(self.world, 1)
        minecraft_gen_item_pool(self.world, 1)
        set_rules(self.world, 1)

    def _get_items(self, item_pool, all_except):
        if all_except and len(all_except) > 0:
            items = self.world.itempool[:]
            items = [item for item in items if
                     item.name not in all_except and not ("Bottle" in item.name and "AnyBottle" in all_except)]
            items.extend(MCItemFactory(item_pool[0], 1))
        else:
            items = MCItemFactory(item_pool[0], 1)
        return self.get_state(items)

    def _get_items_partial(self, item_pool, missing_item):
        new_items = item_pool[0].copy()
        new_items.remove(missing_item)
        items = MCItemFactory(new_items, 1)
        return self.get_state(items)

