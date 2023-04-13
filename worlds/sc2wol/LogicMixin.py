from BaseClasses import MultiWorld
from worlds.AutoWorld import LogicMixin
from .Options import get_option_value
from .Items import get_basic_units, defense_ratings, zerg_defense_ratings


class SC2WoLLogic(LogicMixin):
    def _sc2wol_has_common_unit(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has_any(get_basic_units(multiworld, player), player)

    def _sc2wol_has_air(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has_any({'Viking', 'Wraith', 'Banshee'}, player) or get_option_value(multiworld, player, 'required_tactics') > 0 \
                and self.has_any({'Hercules', 'Medivac'}, player) and self._sc2wol_has_common_unit(multiworld, player)

    def _sc2wol_has_air_anti_air(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has('Viking', player) \
               or get_option_value(multiworld, player, 'required_tactics') > 0 and self.has('Wraith', player)

    def _sc2wol_has_competent_anti_air(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has('Goliath', player) \
                or self.has('Marine', player) and self.has_any({'Medic', 'Medivac'}, player) \
                or self._sc2wol_has_air_anti_air(multiworld, player)

    def _sc2wol_has_anti_air(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has_any({'Missile Turret', 'Thor', 'War Pigs', 'Spartan Company', "Hel's Angel", 'Battlecruiser', 'Marine', 'Wraith'}, player) \
                or self._sc2wol_has_competent_anti_air(multiworld, player) \
                or get_option_value(multiworld, player, 'required_tactics') > 0 and self.has_any({'Ghost', 'Spectre'}, player)

    def _sc2wol_defense_rating(self, multiworld: MultiWorld, player: int, zerg_enemy: bool, air_enemy: bool = True) -> bool:
        defense_score = sum((defense_ratings[item] for item in defense_ratings if self.has(item, player)))
        if self.has_any({'Marine', 'Marauder'}, player) and self.has('Bunker', player):
            defense_score += 3
        if self.has_all({'Siege Tank', 'Maelstrom Rounds'}, player):
            defense_score += 2
        if zerg_enemy:
            defense_score += sum((zerg_defense_ratings[item] for item in zerg_defense_ratings if self.has(item, player)))
            if self.has('Firebat', player) and self.has('Bunker', player):
                defense_score += 2
        if not air_enemy and self.has('Missile Turret', player):
            defense_score -= defense_ratings['Missile Turret']
        # Advanced Tactics bumps defense rating requirements down by 2
        if get_option_value(multiworld, player, 'required_tactics') > 0:
            defense_score += 2
        return defense_score

    def _sc2wol_has_competent_comp(self, multiworld: MultiWorld, player: int) -> bool:
        return (self.has('Marine', player) or self.has('Marauder', player) and
                self._sc2wol_has_competent_anti_air(multiworld, player)) and self.has_any({'Medivac', 'Medic'}, player) or \
               self.has('Thor', player) or self.has("Banshee", player) and self._sc2wol_has_competent_anti_air(multiworld, player) or \
               self.has('Battlecruiser', player) and self._sc2wol_has_common_unit(multiworld, player) or \
               self.has('Siege Tank', player) and self._sc2wol_has_competent_anti_air(multiworld, player)

    def _sc2wol_has_train_killers(self, multiworld: MultiWorld, player: int) -> bool:
        return (self.has_any({'Siege Tank', 'Diamondback', 'Marauder'}, player) or get_option_value(multiworld, player, 'required_tactics') > 0
                and self.has_all({'Reaper', "G-4 Clusterbomb"}, player) or self.has_all({'Spectre', 'Psionic Lash'}, player))

    def _sc2wol_able_to_rescue(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has_any({'Medivac', 'Hercules', 'Raven', 'Viking'}, player) or get_option_value(multiworld, player, 'required_tactics') > 0

    def _sc2wol_has_protoss_common_units(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has_any({'Zealot', 'Immortal', 'Stalker', 'Dark Templar'}, player) \
                or get_option_value(multiworld, player, 'required_tactics') > 0 and self.has_any({'High Templar', 'Dark Templar'}, player)

    def _sc2wol_has_protoss_medium_units(self, multiworld: MultiWorld, player: int) -> bool:
        return self._sc2wol_has_protoss_common_units(multiworld, player) and \
               self.has_any({'Stalker', 'Void Ray', 'Phoenix', 'Carrier'}, player) \
               or get_option_value(multiworld, player, 'required_tactics') > 0 and self.has_any({'High Templar', 'Dark Templar'}, player)

    def _sc2wol_beats_protoss_deathball(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has_any({'Banshee', 'Battlecruiser'}, player) and self._sc2wol_has_competent_anti_air(multiworld, player) or \
               self._sc2wol_has_competent_comp(multiworld, player) and self._sc2wol_has_air_anti_air(multiworld, player)

    def _sc2wol_has_mm_upgrade(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has_any({"Combat Shield (Marine)", "Stabilizer Medpacks (Medic)"}, player)

    def _sc2wol_survives_rip_field(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has("Battlecruiser", player) or \
           self._sc2wol_has_air(multiworld, player) and \
           self._sc2wol_has_competent_anti_air(multiworld, player) and \
           self.has("Science Vessel", player)

    def _sc2wol_has_nukes(self, multiworld: MultiWorld, player: int) -> bool:
        return get_option_value(multiworld, player, 'required_tactics') > 0 and self.has_any({'Ghost', 'Spectre'}, player)

    def _sc2wol_final_mission_requirements(self, multiworld: MultiWorld, player: int):
        beats_kerrigan = self.has_any({'Marine', 'Banshee', 'Ghost'}, player) or get_option_value(multiworld, player, 'required_tactics') > 0
        if get_option_value(multiworld, player, 'all_in_map') == 0:
            # Ground
            defense_rating = self._sc2wol_defense_rating(multiworld, player, True, False)
            if self.has_any({'Battlecruiser', 'Banshee'}, player):
                defense_rating += 3
            return defense_rating >= 12 and beats_kerrigan
        else:
            # Air
            defense_rating = self._sc2wol_defense_rating(multiworld, player, True, True)
            return defense_rating >= 8 and beats_kerrigan \
                and self.has_any({'Viking', 'Battlecruiser'}, player) \
                and self.has_any({'Hive Mind Emulator', 'Psi Disruptor', 'Missile Turret'}, player)

    def _sc2wol_cleared_missions(self, multiworld: MultiWorld, player: int, mission_count: int) -> bool:
        return self.has_group("Missions", player, mission_count)
