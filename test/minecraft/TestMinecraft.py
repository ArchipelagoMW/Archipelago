import worlds.minecraft.Options
from test.TestBase import TestBase
from BaseClasses import MultiWorld, ItemClassification
from worlds import AutoWorld
from worlds.minecraft import MinecraftWorld
from worlds.minecraft.Items import MinecraftItem, item_table
from worlds.minecraft.Options import *
from Options import Toggle, Range

# Converts the name of an item into an item object
def MCItemFactory(items, player: int):
    ret = []
    singleton = False
    if isinstance(items, str):
        items = [items]
        singleton = True
    for item in items:
        if item in item_table:
            ret.append(MinecraftItem(
                item, ItemClassification.progression if item_table[item].progression else ItemClassification.filler,
                item_table[item].code, player
            ))
        else:
            raise Exception(f"Unknown item {item}")

    if singleton:
        return ret[0]
    return ret

class TestMinecraft(TestBase):

    def setUp(self):
        self.world = MultiWorld(1)
        self.world.game[1] = "Minecraft"
        self.world.worlds[1] = MinecraftWorld(self.world, 1)
        exclusion_pools = ['hard', 'unreasonable', 'postgame']
        for pool in exclusion_pools:
            setattr(self.world, f"include_{pool}_advancements", {1: False})
        setattr(self.world, "advancement_goal", {1: AdvancementGoal(30)})
        setattr(self.world, "egg_shards_required", {1: EggShardsRequired(0)})
        setattr(self.world, "egg_shards_available", {1: EggShardsAvailable(0)})
        setattr(self.world, "required_bosses", {1: BossGoal(1)}) # ender dragon
        setattr(self.world, "shuffle_structures", {1: ShuffleStructures(False)})
        setattr(self.world, "bee_traps", {1: BeeTraps(0)})
        setattr(self.world, "combat_difficulty", {1: CombatDifficulty(1)}) # normal
        setattr(self.world, "structure_compasses", {1: Toggle(False)})
        setattr(self.world, "death_link", {1: Toggle(False)})
        AutoWorld.call_single(self.world, "create_regions", 1)
        AutoWorld.call_single(self.world, "generate_basic", 1)
        AutoWorld.call_single(self.world, "set_rules", 1)

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

