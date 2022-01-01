from BaseClasses import MultiWorld
from .Names import LocationName, ItemName
from ..AutoWorld import LogicMixin
from ..generic.Rules import set_rule


class LegacyLogic(LogicMixin):
    def _legacy_has_any_vendors(self, player: int) -> bool:
        return self.has_any({ItemName.blacksmith, ItemName.enchantress}, player)

    def _legacy_has_all_vendors(self, player: int) -> bool:
        return self.has_all({ItemName.blacksmith, ItemName.enchantress}, player)

    def _legacy_has_stat_upgrades(self, player: int, amount: int) -> bool:
        count: int = self.item_count(ItemName.health, player) + self.item_count(ItemName.mana, player) + \
                     self.item_count(ItemName.attack, player) + self.item_count(ItemName.magic_damage, player) + \
                     self.item_count(ItemName.armor, player) + self.item_count(ItemName.equip, player)
        return count >= amount


def set_rules(world: MultiWorld, player: int):
    # Chests
    for i in range(0, world.chests_per_zone[player]):
        set_rule(world.get_location(f"{LocationName.garden} - Chest {i + 1}", player),
                 lambda state: state.has(ItemName.boss_khindr, player))
        set_rule(world.get_location(f"{LocationName.tower} - Chest {i + 1}", player),
                 lambda state: state.has(ItemName.boss_alexander, player))
        set_rule(world.get_location(f"{LocationName.dungeon} - Chest {i + 1}", player),
                 lambda state: state.has(ItemName.boss_leon, player))

    # Fairy Chests
    for i in range(0, world.fairy_chests_per_zone[player]):
        set_rule(world.get_location(f"{LocationName.garden} - Fairy Chest {i + 1}", player),
                 lambda state: state.has(ItemName.boss_khindr, player))
        set_rule(world.get_location(f"{LocationName.tower} - Fairy Chest {i + 1}", player),
                 lambda state: state.has(ItemName.boss_alexander, player))
        set_rule(world.get_location(f"{LocationName.dungeon} - Fairy Chest {i + 1}", player),
                 lambda state: state.has(ItemName.boss_leon, player))

    # Vendors
    if world.vendors[player] == "early":
        set_rule(world.get_location(LocationName.castle, player),
                 lambda state: state._legacy_has_all_vendors(player))
    elif world.vendors[player] == "normal":
        set_rule(world.get_location(LocationName.garden, player),
                 lambda state: state._legacy_has_any_vendors(player))
    elif world.vendors[player] == "anywhere":
        pass  # it can be anywhere, so no rule for this!

    # Diaries
    for i in range(0, 5):
        set_rule(world.get_location(f"Diary {i + 6}", player),
                 lambda state: state.has(ItemName.boss_khindr, player))
        set_rule(world.get_location(f"Diary {i + 11}", player),
                 lambda state: state.has(ItemName.boss_alexander, player))
        set_rule(world.get_location(f"Diary {i + 16}", player),
                 lambda state: state.has(ItemName.boss_leon, player))
        set_rule(world.get_location(f"Diary {i + 21}", player),
                 lambda state: state.has(ItemName.boss_herodotus, player))

    # Scale each manor location.
    set_rule(world.get_location(LocationName.manor_left_wing_window, player),
             lambda state: state.has(ItemName.boss_khindr, player))
    set_rule(world.get_location(LocationName.manor_left_wing_roof, player),
             lambda state: state.has(ItemName.boss_khindr, player))
    set_rule(world.get_location(LocationName.manor_right_wing_window, player),
             lambda state: state.has(ItemName.boss_khindr, player))
    set_rule(world.get_location(LocationName.manor_right_wing_roof, player),
             lambda state: state.has(ItemName.boss_khindr, player))
    set_rule(world.get_location(LocationName.manor_left_big_base, player),
             lambda state: state.has(ItemName.boss_khindr, player))
    set_rule(world.get_location(LocationName.manor_right_big_base, player),
             lambda state: state.has(ItemName.boss_khindr, player))
    set_rule(world.get_location(LocationName.manor_left_tree1, player),
             lambda state: state.has(ItemName.boss_khindr, player))
    set_rule(world.get_location(LocationName.manor_left_tree2, player),
             lambda state: state.has(ItemName.boss_khindr, player))
    set_rule(world.get_location(LocationName.manor_right_tree, player),
             lambda state: state.has(ItemName.boss_khindr, player))
    set_rule(world.get_location(LocationName.manor_left_big_upper1, player),
             lambda state: state.has(ItemName.boss_alexander, player))
    set_rule(world.get_location(LocationName.manor_left_big_upper2, player),
             lambda state: state.has(ItemName.boss_alexander, player))
    set_rule(world.get_location(LocationName.manor_left_big_windows, player),
             lambda state: state.has(ItemName.boss_alexander, player))
    set_rule(world.get_location(LocationName.manor_left_big_roof, player),
             lambda state: state.has(ItemName.boss_alexander, player))
    set_rule(world.get_location(LocationName.manor_left_far_base, player),
             lambda state: state.has(ItemName.boss_alexander, player))
    set_rule(world.get_location(LocationName.manor_left_far_roof, player),
             lambda state: state.has(ItemName.boss_alexander, player))
    set_rule(world.get_location(LocationName.manor_left_extension, player),
             lambda state: state.has(ItemName.boss_alexander, player))
    set_rule(world.get_location(LocationName.manor_right_big_upper, player),
             lambda state: state.has(ItemName.boss_alexander, player))
    set_rule(world.get_location(LocationName.manor_right_big_roof, player),
             lambda state: state.has(ItemName.boss_alexander, player))
    set_rule(world.get_location(LocationName.manor_right_extension, player),
             lambda state: state.has(ItemName.boss_alexander, player))
    set_rule(world.get_location(LocationName.manor_right_high_base, player),
             lambda state: state.has(ItemName.boss_leon, player))
    set_rule(world.get_location(LocationName.manor_right_high_upper, player),
             lambda state: state.has(ItemName.boss_leon, player))
    set_rule(world.get_location(LocationName.manor_right_high_tower, player),
             lambda state: state.has(ItemName.boss_leon, player))
    set_rule(world.get_location(LocationName.manor_observatory_base, player),
             lambda state: state.has(ItemName.boss_leon, player))
    set_rule(world.get_location(LocationName.manor_observatory_scope, player),
             lambda state: state.has(ItemName.boss_leon, player))

    # Standard Zone Progression
    set_rule(world.get_location(LocationName.garden, player),
             lambda state: state._legacy_has_stat_upgrades(player, 10) and state.has(ItemName.boss_khindr, player))
    set_rule(world.get_location(LocationName.tower, player),
             lambda state: state._legacy_has_stat_upgrades(player, 25) and state.has(ItemName.boss_alexander, player))
    set_rule(world.get_location(LocationName.dungeon, player),
             lambda state: state._legacy_has_stat_upgrades(player, 40) and state.has(ItemName.boss_leon, player))

    # Bosses
    set_rule(world.get_location(LocationName.boss_khindr, player),
             lambda state: state.has(ItemName.boss_khindr, player))
    set_rule(world.get_location(LocationName.boss_alexander, player),
             lambda state: state.has(ItemName.boss_alexander, player))
    set_rule(world.get_location(LocationName.boss_leon, player),
             lambda state: state.has(ItemName.boss_leon, player))
    set_rule(world.get_location(LocationName.boss_herodotus, player),
             lambda state: state.has(ItemName.boss_herodotus, player))
    set_rule(world.get_location(LocationName.fountain, player),
             lambda state: state._legacy_has_stat_upgrades(player, 50) and state.has(ItemName.boss_herodotus, player))

    world.completion_condition[player] = lambda state: state.has(ItemName.boss_fountain, player)
