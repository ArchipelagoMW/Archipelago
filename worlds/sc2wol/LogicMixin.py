from BaseClasses import MultiWorld
from worlds.AutoWorld import LogicMixin
from .Options import get_option_value


class SC2WoLLogic(LogicMixin):
    def _sc2wol_has_common_unit(self, world: MultiWorld, player: int) -> bool:
        return self.has_any({'Marine', 'Marauder', 'Firebat', 'Hellion', 'Vulture'}, player)

    def _sc2wol_has_manned_bunkers(self, world: MultiWorld, player: int) -> bool:
        return self.has_any({'Marine', 'Marauder'}, player) and self.has('Bunker', player)

    def _sc2wol_has_air(self, world: MultiWorld, player: int) -> bool:
        return self.has_any({'Viking', 'Wraith', 'Banshee'}, player) or \
               self.has_any({'Hercules', 'Medivac'}, player) and self._sc2wol_has_common_unit(world, player)

    def _sc2wol_has_air_anti_air(self, world: MultiWorld, player: int) -> bool:
        return self.has_any({'Viking', 'Wraith'}, player)

    def _sc2wol_has_competent_anti_air(self, world: MultiWorld, player: int) -> bool:
        return self.has_any({'Marine', 'Goliath'}, player) or self._sc2wol_has_air_anti_air(world, player)

    def _sc2wol_has_anti_air(self, world: MultiWorld, player: int) -> bool:
        return self.has_any({'Missile Turret', 'Thor', 'War Pigs', 'Spartan Company', "Hel's Angel", 'Battlecruiser'}, player) or self._sc2wol_has_competent_anti_air(world, player)

    def _sc2wol_has_heavy_defense(self, world: MultiWorld, player: int) -> bool:
        return (self.has_any({'Siege Tank', 'Vulture'}, player) or
                self._sc2wol_has_manned_bunkers(world, player)) and self._sc2wol_has_anti_air(world, player)

    def _sc2wol_has_competent_comp(self, world: MultiWorld, player: int) -> bool:
        return (self.has('Marine', player) or self.has('Marauder', player) and
                self._sc2wol_has_competent_anti_air(world, player)) and self.has_any({'Medivac', 'Medic'}, player) or \
               self.has('Thor', player) or self.has("Banshee", player) and self._sc2wol_has_competent_anti_air(world, player) or \
               self.has('Battlecruiser', player) and self._sc2wol_has_common_unit(world, player) or \
               self.has('Siege Tank', player) and self._sc2wol_has_competent_anti_air(world, player)

    def _sc2wol_has_train_killers(self, world: MultiWorld, player: int) -> bool:
        return (self.has_any({'Siege Tank', 'Diamondback'}, player) or
                self.has_all({'Reaper', "G-4 Clusterbomb"}, player) or self.has_all({'Spectre', 'Psionic Lash'}, player)
                or self.has('Marauders', player))

    def _sc2wol_able_to_rescue(self, world: MultiWorld, player: int) -> bool:
        return self.has_any({'Medivac', 'Hercules', 'Raven', 'Viking'}, player)

    def _sc2wol_has_protoss_common_units(self, world: MultiWorld, player: int) -> bool:
        return self.has_any({'Zealot', 'Immortal', 'Stalker', 'Dark Templar'}, player)

    def _sc2wol_has_protoss_medium_units(self, world: MultiWorld, player: int) -> bool:
        return self._sc2wol_has_protoss_common_units(world, player) and \
               self.has_any({'Stalker', 'Void Ray', 'Phoenix', 'Carrier'}, player)

    def _sc2wol_beats_protoss_deathball(self, world: MultiWorld, player: int) -> bool:
        return self.has_any({'Banshee', 'Battlecruiser'}, player) and self._sc2wol_has_competent_anti_air or \
               self._sc2wol_has_competent_comp(world, player) and self._sc2wol_has_air_anti_air(world, player)

    def _sc2wol_has_mm_upgrade(self, world: MultiWorld, player: int) -> bool:
        return self.has_any({"Combat Shield (Marine)", "Stabilizer Medpacks (Medic)"}, player)

    def _sc2wol_survives_rip_field(self, world: MultiWorld, player: int) -> bool:
        return self.has("Battlecruiser", player) or \
           self._sc2wol_has_air(world, player) and \
           self._sc2wol_has_competent_anti_air(world, player) and \
           self.has("Science Vessel", player)

    def _sc2wol_final_mission_requirements(self, world: MultiWorld, player: int):
        if get_option_value(world, player, 'all_in_map') == 0:
            # Ground
            version_logic = sum(
                self.has(item, player) for item in ['Planetary Fortress', 'Siege Tank', 'Psi Disruptor', 'Banshee', 'Battlecruiser']
            ) + self._sc2wol_has_manned_bunkers(world, player) >= 3
        else:
            # Air
            version_logic = self.has_any({'Viking', 'Battlecruiser'}, player) \
                            and self.has_any({'Hive Mind Emulator', 'Psi Disruptor', 'Missile Turret'}, player)
        return self._sc2wol_has_heavy_defense(world, player) and version_logic

    def _sc2wol_cleared_missions(self, world: MultiWorld, player: int, mission_count: int) -> bool:
        return self.has_group("Missions", player, mission_count)


