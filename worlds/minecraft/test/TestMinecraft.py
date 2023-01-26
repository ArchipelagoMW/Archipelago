from test.TestBase import TestBase
from BaseClasses import MultiWorld
from worlds import AutoWorld
from worlds.minecraft import MinecraftWorld
from Options import Toggle
from worlds.minecraft.Options import AdvancementGoal, EggShardsRequired, EggShardsAvailable, BossGoal, BeeTraps, \
    ShuffleStructures, CombatDifficulty


class TestMinecraft(TestBase):

    def setUp(self):
        self.multiworld = MultiWorld(1)
        self.multiworld.game[1] = "Minecraft"
        self.multiworld.worlds[1] = MinecraftWorld(self.multiworld, 1)
        exclusion_pools = ['hard', 'unreasonable', 'postgame']
        for pool in exclusion_pools:
            setattr(self.multiworld, f"include_{pool}_advancements", {1: False})
        setattr(self.multiworld, "advancement_goal", {1: AdvancementGoal(30)})
        setattr(self.multiworld, "egg_shards_required", {1: EggShardsRequired(0)})
        setattr(self.multiworld, "egg_shards_available", {1: EggShardsAvailable(0)})
        setattr(self.multiworld, "required_bosses", {1: BossGoal(1)})  # ender dragon
        setattr(self.multiworld, "shuffle_structures", {1: ShuffleStructures(False)})
        setattr(self.multiworld, "bee_traps", {1: BeeTraps(0)})
        setattr(self.multiworld, "combat_difficulty", {1: CombatDifficulty(1)})  # normal
        setattr(self.multiworld, "structure_compasses", {1: Toggle(False)})
        setattr(self.multiworld, "death_link", {1: Toggle(False)})
        AutoWorld.call_single(self.multiworld, "create_regions", 1)
        AutoWorld.call_single(self.multiworld, "create_items", 1)
        AutoWorld.call_single(self.multiworld, "set_rules", 1)

    def _create_items(self, items, player):
        singleton = False
        if isinstance(items, str):
            items = [items]
            singleton = True
        ret = [self.multiworld.worlds[player].create_item(item) for item in items]
        if singleton:
            return ret[0]
        return ret

    def _get_items(self, item_pool, all_except):
        if all_except and len(all_except) > 0:
            items = self.multiworld.itempool[:]
            items = [item for item in items if item.name not in all_except]
            items.extend(self._create_items(item_pool[0], 1))
        else:
            items = self._create_items(item_pool[0], 1)
        return self.get_state(items)

    def _get_items_partial(self, item_pool, missing_item):
        new_items = item_pool[0].copy()
        new_items.remove(missing_item)
        items = self._create_items(new_items, 1)
        return self.get_state(items)
