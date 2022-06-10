from BaseClasses import MultiWorld
from ..AutoWorld import LogicMixin


class SC2WoLLogic(LogicMixin):
    def _sc2wol_has_common_unit(self, world: MultiWorld, player: int) -> bool:
        return self.has_any({'Marine', 'Marauder', 'Firebat', 'Hellion', 'Vulture'}, player)

    def _sc2wol_has_bunker_unit(self, world: MultiWorld, player: int) -> bool:
        return self.has_any({'Marine', 'Marauder'}, player)

    def _sc2wol_has_air(self, world: MultiWorld, player: int) -> bool:
        return self.has_any({'Viking', 'Wraith', 'Medivac', 'Banshee', 'Hercules'}, player)

    def _sc2wol_has_air_anti_air(self, world: MultiWorld, player: int) -> bool:
        return self.has_any({'Viking', 'Wraith'}, player)

    def _sc2wol_has_mobile_anti_air(self, world: MultiWorld, player: int) -> bool:
        return self.has_any({'Marine', 'Goliath'}, player) or self._sc2wol_has_air_anti_air(world, player)

    def _sc2wol_has_anti_air(self, world: MultiWorld, player: int) -> bool:
        return self.has('Missile Turret', player) or self._sc2wol_has_mobile_anti_air(world, player)

    def _sc2wol_has_heavy_defense(self, world: MultiWorld, player: int) -> bool:
        return (self.has_any({'Siege Tank', 'Vulture'}, player) or
                self.has('Bunker', player) and self._sc2wol_has_bunker_unit(world, player)) and \
               self._sc2wol_has_anti_air(world, player)

    def _sc2wol_has_competent_comp(self, world: MultiWorld, player: int) -> bool:
        return (self.has('Marine', player) or self.has('Marauder', player) and
                self._sc2wol_has_mobile_anti_air(world, player)) and self.has_any({'Medivac', 'Medic'}, player) or \
               self.has('Thor', player) or self.has("Banshee", player) and self._sc2wol_has_mobile_anti_air(world, player) or \
               self.has('Battlecruiser', player) and self._sc2wol_has_common_unit(world, player)

    def _sc2wol_has_train_killers(self, world: MultiWorld, player: int) -> bool:
        return (self.has_any({'Siege Tank', 'Diamondback'}, player) or
                self.has_all({'Reaper', "G-4 Clusterbomb"}, player) or self.has_all({'Spectre', 'Psionic Lash'}, player))

    def _sc2wol_able_to_rescue(self, world: MultiWorld, player: int) -> bool:
        return self.has_any({'Medivac', 'Hercules', 'Raven', 'Orbital Strike'}, player)

    def _sc2wol_has_protoss_common_units(self, world: MultiWorld, player: int) -> bool:
        return self.has_any({'Zealot', 'Immortal', 'Stalker', 'Dark Templar'}, player)

    def _sc2wol_has_protoss_medium_units(self, world: MultiWorld, player: int) -> bool:
        return self._sc2wol_has_protoss_common_units(world, player) and \
               self.has_any({'Stalker', 'Void Ray', 'Phoenix', 'Carrier'}, player)

    def _sc2wol_cleared_missions(self, world: MultiWorld, player: int, mission_count: int) -> bool:
        return self.has_group("Missions", player, mission_count)


