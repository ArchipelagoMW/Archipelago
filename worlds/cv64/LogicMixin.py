from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin
from .Options import get_option_value


class CV64Logic(LogicMixin):
    def _cv64_has_archives_key(self, world: MultiWorld, player: int) -> bool:
        return self.has('Archives key', player)

    def _cv64_has_left_tower_key(self, world: MultiWorld, player: int) -> bool:
        return self.has('Left Tower Key', player)

    def _cv64_has_storeroom_key(self, world: MultiWorld, player: int) -> bool:
        return self.has('Storeroom Key', player)

    def _cv64_has_garden_key(self, world: MultiWorld, player: int) -> bool:
        return self.has('Garden Key', player)

    def _cv64_has_copper_key(self, world: MultiWorld, player: int) -> bool:
        return self.has('Copper Key', player)

    def _cv64_has_chamber_key(self, world: MultiWorld, player: int) -> bool:
        return self.has('Chamber Key', player)

    def _cv64_has_execution_key(self, world: MultiWorld, player: int) -> bool:
        return self.has('Execution Key', player)

    def _cv64_has_science_key1(self, world: MultiWorld, player: int) -> bool:
        return self.has('Science Key1', player)

    def _cv64_has_science_key2(self, world: MultiWorld, player: int) -> bool:
        return self.has('Science Key2', player)

    def _cv64_has_science_key3(self, world: MultiWorld, player: int) -> bool:
        return self.has('Science Key3', player)

    def _cv64_has_clocktower_key1(self, world: MultiWorld, player: int) -> bool:
        return self.has('Clocktower Key1', player)

    def _cv64_has_clocktower_key2(self, world: MultiWorld, player: int) -> bool:
        return self.has('Clocktower Key2', player)

    def _cv64_has_clocktower_key3(self, world: MultiWorld, player: int) -> bool:
        return self.has('Clocktower Key3', player)

    def _cv64_has_explosives(self, world: MultiWorld, player: int) -> bool:
        return (self.has("Magical Nitro", player, 2) and
                self.has("Mandragora", player, 2))

    def _cv64_has_special2s(self, world: MultiWorld, player: int, special2_count: int) -> bool:
        return self.has_group("Special2", player, special2_count)

    def _cv64_can_face_drac(self, world: MultiWorld, player: int,
                            boss_kills: int, special1_count: int) -> bool:
        if get_option_value(world, player, "DraculasCondition") == 0:
            return self.has_group("Boss Kills", player, boss_kills)
        elif get_option_value(world, player, "DraculasCondition") == 1:
            return self.has_group("Special1", player, special1_count)
        else:
            return self.has("Crystal On", player)
