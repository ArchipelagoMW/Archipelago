from BaseClasses import MultiWorld
from worlds.AutoWorld import LogicMixin
from .Options import get_option_value, RequiredTactics, kerrigan_unit_available, AllInMap, GameDifficulty
from .Items import get_basic_units, defense_ratings, zerg_defense_ratings, kerrigan_actives
from .MissionTables import SC2Race
from . import ItemNames

class SC2Logic(LogicMixin):
    # Note(phaneros): Uncomment these to make mypy happy; I don't know if it has runtime impact.
    # Note(phaneros): They come from CollectionState in BaseClasses.py
    # def has_group(self, item_name_group: str, player: int, count: int = 1) -> bool: ...
    # def has(self, item: str, player: int, count: int = 1) -> bool: ...
    # def has_all(self, items: set[str], player: int) -> bool: ...
    # def has_any(self, items: set[str], player: int) -> bool: ...

    # General
    def _sc2_cleared_missions(self, multiworld: MultiWorld, player: int, mission_count: int) -> bool:
        return self.has_group("Missions", player, mission_count)
    
    def _sc2_advanced_tactics(self, multiworld: MultiWorld, player: int) -> bool:
        return get_option_value(multiworld, player, 'required_tactics') != RequiredTactics.option_standard
    
    # WoL
    def _sc2wol_has_common_unit(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has_any(get_basic_units(multiworld, player, SC2Race.TERRAN), player)

    def _sc2wol_has_air(self, multiworld: MultiWorld, player: int) -> bool:
        return (self.has_any({ItemNames.Viking, ItemNames.Wraith, ItemNames.Banshee, ItemNames.Battlecruiser}, player) or self._sc2_advanced_tactics(multiworld, player)
                and self.has_any({ItemNames.Hercules, ItemNames.Medivac}, player) and self._sc2wol_has_common_unit(multiworld, player)
        )

    def _sc2wol_has_air_anti_air(self, multiworld: MultiWorld, player: int) -> bool:
        return (
            self.has(ItemNames.Viking, player)
            or self.has_all({ItemNames.Wraith, ItemNames.Wraith_Advanced_Laser_Technology}, player)
            or self.has_all({ItemNames.Battlecruiser, ItemNames.Battlecruiser_ATX_Laser_Battery}, player)
            or self._sc2_advanced_tactics(multiworld, player) and self.has_any({ItemNames.Wraith, ItemNames.Valkyrie, ItemNames.Battlecruiser}, player)
        )

    def _sc2wol_has_competent_ground_to_air(self, multiworld: MultiWorld, player: int) -> bool:
        return (
            self.has(ItemNames.Goliath, player)
            or self.has(ItemNames.Marine, player) and self.has_any({ItemNames.Medic, ItemNames.Medivac}, player)
            or self._sc2_advanced_tactics(multiworld, player) and self.has(ItemNames.Cyclone, player)
        )

    def _sc2wol_has_competent_anti_air(self, multiworld: MultiWorld, player: int) -> bool:
        return (
            self._sc2wol_has_competent_ground_to_air(multiworld, player)
            or self._sc2wol_has_air_anti_air(multiworld, player)
        )

    def _sc2wol_welcome_to_the_jungle_requirement(self, multiworld: MultiWorld, player: int) -> bool:
        return (
            self._sc2wol_has_common_unit(multiworld, player)
            and self._sc2wol_has_competent_ground_to_air(multiworld, player)
        ) or (
            self._sc2_advanced_tactics(multiworld, player)
            and self.has_any({ItemNames.Marine, ItemNames.Vulture}, player)
            and self._sc2wol_has_air_anti_air(multiworld, player)
        )

    def _sc2wol_has_anti_air(self, multiworld: MultiWorld, player: int) -> bool:
        return (
            self.has_any({
                ItemNames.Missile_Turret, ItemNames.Thor, ItemNames.War_Pigs, ItemNames.Spartan_Company,
                ItemNames.Hels_Angel, ItemNames.Battlecruiser, ItemNames.Marine, ItemNames.Wraith,
                ItemNames.Valkyrie, ItemNames.Cyclone,
            }, player)
            or self._sc2wol_has_competent_anti_air(multiworld, player)
            or self._sc2_advanced_tactics(multiworld, player)
            and self.has_any({ItemNames.Ghost, ItemNames.Spectre, ItemNames.Widow_Mine, ItemNames.Liberator}, player)
        )

    def _sc2wol_defense_rating(self, multiworld: MultiWorld, player: int, zerg_enemy: bool, air_enemy: bool = True) -> int:
        defense_score = sum((defense_ratings[item] for item in defense_ratings if self.has(item, player)))
        if self.has_any({ItemNames.Marine, ItemNames.Marauder}, player) and self.has(ItemNames.Bunker, player):
            defense_score += 3
        if self.has_all({ItemNames.Siege_Tank, ItemNames.Siege_Tank_Maelstrom_Rounds}, player):
            defense_score += 2
        if self.has_all({ItemNames.Siege_Tank, ItemNames.Siege_Tank_Graduating_Range}, player):
            defense_score += 1
        if self.has_all({ItemNames.Widow_Mine, ItemNames.Widow_Mine_Concealment}, player):
            defense_score += 1
        if zerg_enemy:
            defense_score += sum((zerg_defense_ratings[item] for item in zerg_defense_ratings if self.has(item, player)))
            if self.has(ItemNames.Firebat, player) and self.has(ItemNames.Bunker, player):
                defense_score += 2
        if not air_enemy and self.has(ItemNames.Missile_Turret, player):
            defense_score -= defense_ratings[ItemNames.Missile_Turret]
        # Advanced Tactics bumps defense rating requirements down by 2
        if self._sc2_advanced_tactics(multiworld, player):
            defense_score += 2
        return defense_score

    def _sc2wol_has_competent_comp(self, multiworld: MultiWorld, player: int) -> bool:
        return (
            (
                (self.has_any({ItemNames.Marine, ItemNames.Marauder}, player)
                    and self.has_any({ItemNames.Medivac, ItemNames.Medic}, player))
                or self.has_any({ItemNames.Thor, ItemNames.Banshee, ItemNames.Siege_Tank}, player)
                or self.has_all({ItemNames.Liberator, ItemNames.Liberator_Raid_Artillery}, player)
            )
            and self._sc2wol_has_competent_anti_air(multiworld, player)
        ) or (
            self.has(ItemNames.Battlecruiser, player) and self._sc2wol_has_common_unit(multiworld, player)
        )

    def _sc2wol_has_train_killers(self, multiworld: MultiWorld, player: int) -> bool:
        return (
            self.has_any({ItemNames.Siege_Tank, ItemNames.Diamondback, ItemNames.Marauder, ItemNames.Cyclone}, player)
            or self._sc2_advanced_tactics(multiworld, player)
            and (
                self.has_all({ItemNames.Reaper, ItemNames.Reaper_G4_Clusterbomb}, player)
                or self.has_all({ItemNames.Spectre, ItemNames.Spectre_Psionic_Lash}, player)
                or self.has_any({ItemNames.Vulture, ItemNames.Liberator}, player)
            )
        )

    def _sc2wol_able_to_rescue(self, multiworld: MultiWorld, player: int) -> bool:
        return (self.has_any({ItemNames.Medivac, ItemNames.Hercules, ItemNames.Raven, ItemNames.Viking}, player)
                or self._sc2_advanced_tactics(multiworld, player)
        )

    def _sc2wol_has_protoss_common_units(self, multiworld: MultiWorld, player: int) -> bool:
        return (self.has_any({ItemNames.Zealot, ItemNames.Immortal, ItemNames.Stalker, ItemNames.Dark_Templar}, player)
                or self._sc2_advanced_tactics(multiworld, player) and self.has(ItemNames.High_Templar, player)
        )

    def _sc2wol_has_protoss_medium_units(self, multiworld: MultiWorld, player: int) -> bool:
        return (
            self._sc2wol_has_protoss_common_units(multiworld, player)
                and self.has_any({ItemNames.Stalker, ItemNames.Void_Ray, ItemNames.Carrier}, player)
            or self._sc2_advanced_tactics(multiworld, player)
                and self.has(ItemNames.Dark_Templar, player)
        )

    def _sc2wol_beats_protoss_deathball(self, multiworld: MultiWorld, player: int) -> bool:
        return (
            (
                self.has_any({ItemNames.Banshee, ItemNames.Battlecruiser}, player)
                or self.has_all({ItemNames.Liberator, ItemNames.Liberator_Raid_Artillery}, player)
            ) and self._sc2wol_has_competent_anti_air(multiworld, player)
            or self._sc2wol_has_competent_comp(multiworld, player) and self._sc2wol_has_air_anti_air(multiworld, player)
        )

    def _sc2wol_has_mm_upgrade(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has_any({ItemNames.Marine_Combat_Shield, ItemNames.Medic_Stabilizer_Medpacks}, player)

    def _sc2wol_survives_rip_field(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has(ItemNames.Battlecruiser, player) or \
           self._sc2wol_has_air(multiworld, player) and \
           self._sc2wol_has_competent_anti_air(multiworld, player) and \
           self.has(ItemNames.Science_Vessel, player)

    def _sc2wol_has_nukes(self, multiworld: MultiWorld, player: int) -> bool:
        return self._sc2_advanced_tactics(multiworld, player) and self.has_any({ItemNames.Ghost, ItemNames.Spectre}, player)

    def _sc2wol_can_respond_to_colony_infestations(self, multiworld: MultiWorld, player: int) -> bool:
        return (
            self._sc2wol_has_common_unit(multiworld, player)
            and self._sc2wol_has_competent_anti_air(multiworld, player)
            and (
                    self._sc2wol_has_air_anti_air(multiworld, player)
                    or self.has_any({ItemNames.Battlecruiser, ItemNames.Valkyrie}, player)
                )
            and self._sc2wol_defense_rating(multiworld, player, True) >= 3
        )

    def _sc2wol_final_mission_requirements(self, multiworld: MultiWorld, player: int):
        beats_kerrigan = self.has_any({ItemNames.Marine, ItemNames.Banshee, ItemNames.Ghost}, player) or self._sc2_advanced_tactics(multiworld, player)
        if get_option_value(multiworld, player, 'all_in_map') == AllInMap.option_ground:
            # Ground
            defense_rating = self._sc2wol_defense_rating(multiworld, player, True, False)
            if self.has_any({ItemNames.Battlecruiser, ItemNames.Banshee}, player):
                defense_rating += 3
            return defense_rating >= 12 and beats_kerrigan
        else:
            # Air
            defense_rating = self._sc2wol_defense_rating(multiworld, player, True, True)
            return defense_rating >= 8 and beats_kerrigan \
                and self.has_any({ItemNames.Viking, ItemNames.Battlecruiser, ItemNames.Valkyrie}, player) \
                and self.has_any({ItemNames.Hive_Mind_Emulator, ItemNames.Psi_Disrupter, ItemNames.Missile_Turret}, player)

    def _sc2wol_cleared_missions(self, multiworld: MultiWorld, player: int, mission_count: int) -> bool:
        return self.has_group("WoL Missions", player, mission_count)

    # HotS
    def _sc2hots_has_common_unit(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has_any(get_basic_units(multiworld, player, SC2Race.ZERG), player)

    def _sc2hots_has_good_antiair(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has_any({ItemNames.Hydralisk, ItemNames.Mutalisk}, player) or \
            self.has_all({ItemNames.Swarm_Host, ItemNames.Swarm_Host_Pressurized_Glands}, player) or \
            (self._sc2_advanced_tactics(multiworld, player) and self.has(ItemNames.Infestor, player))

    def _sc2hots_has_minimal_antiair(self, multiworld: MultiWorld, player: int) -> bool:
        return self._sc2hots_has_good_antiair(multiworld, player) or get_option_value(multiworld, player, 'kerriganless') in kerrigan_unit_available or \
            self.has(ItemNames.Swarm_Queen, player) or (self._sc2_advanced_tactics(multiworld, player) and self.has(ItemNames.Spore_Crawler, player))
    
    def _sc2hots_has_brood_lord(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has_all({ItemNames.Mutalisk, ItemNames.Mutalisk_Brood_Lord_Strain}, player)
    
    def _sc2hots_has_viper(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has_all({ItemNames.Mutalisk, ItemNames.Mutalisk_Viper_Strain}, player)

    def _sc2hots_has_impaler_or_lurker(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has(ItemNames.Hydralisk, player) and self.has_any({ItemNames.Hydralisk_Impaler_Strain, ItemNames.Hydralisk_Lurker_Strain}, player)

    def _sc2hots_has_competent_comp(self, multiworld: MultiWorld, player: int) -> bool:
        advanced = self._sc2_advanced_tactics(multiworld, player)
        core_unit = self.has_any({ItemNames.Roach, ItemNames.Aberration, ItemNames.Zergling}, player)
        support_unit = self.has_any({ItemNames.Swarm_Queen, ItemNames.Hydralisk}, player) \
                       or self._sc2hots_has_brood_lord(multiworld, player) \
                       or advanced and (self.has(ItemNames.Infestor, player) or self._sc2hots_has_viper(multiworld, player))
        if core_unit and support_unit:
            return True
        vespene_unit = self.has_any({ItemNames.Ultralisk, ItemNames.Aberration}, player) \
                       or advanced and self._sc2hots_has_viper(multiworld, player)
        return vespene_unit and self.has_any({ItemNames.Zergling, ItemNames.Swarm_Queen}, player)

    def _sc2hots_has_basic_comp(self, multiworld: MultiWorld, player: int) -> bool:
        if get_option_value(multiworld, player, 'game_difficulty') < GameDifficulty.option_brutal \
           or self._sc2hots_has_basic_kerrigan(multiworld, player) \
           or self._sc2hots_has_two_kerrigan_actives(multiworld, player):
            return self._sc2hots_has_common_unit(multiworld, player)
        else:
            return self._sc2hots_has_competent_comp(multiworld, player)

    def _sc2hots_can_spread_creep(self, multiworld: MultiWorld, player: int) -> bool:
        return self._sc2_advanced_tactics(multiworld, player) or self.has(ItemNames.Swarm_Queen, player)
    
    def _sc2hots_has_competent_defense(self, multiworld: MultiWorld, player: int) -> bool:
        return (
            self._sc2hots_has_common_unit(multiworld, player)
            and (
                (
                    self.has(ItemNames.Swarm_Host, player)
                    or self._sc2hots_has_brood_lord(multiworld, player)
                    or self._sc2hots_has_impaler_or_lurker(multiworld, player)
                ) or (
                    self._sc2_advanced_tactics(multiworld, player)
                    and (self._sc2hots_has_viper(multiworld, player)
                        or self.has(ItemNames.Spine_Crawler, player))
                )
            )
        )

    def _sc2hots_has_basic_kerrigan(self, multiworld: MultiWorld, player: int) -> bool:
        # One active ability that can be used to defeat enemies directly on Standard
        if not self._sc2_advanced_tactics(multiworld, player) and \
            not self.has_any({ItemNames.Kerrigan_Kinetic_Blast, ItemNames.Kerrigan_Leaping_Strike,
                              ItemNames.Kerrigan_Crushing_Grip, ItemNames.Kerrigan_Psionic_Shift,
                              ItemNames.Kerrigan_Spawn_Banelings}, player):
            return False
        # Two non-ultimate abilities
        count = 0
        for item in (ItemNames.Kerrigan_Kinetic_Blast, ItemNames.Kerrigan_Leaping_Strike, ItemNames.Kerrigan_Heroic_Fortitude,
                     ItemNames.Kerrigan_Chain_Reaction, ItemNames.Kerrigan_Crushing_Grip, ItemNames.Kerrigan_Psionic_Shift,
                     ItemNames.Kerrigan_Spawn_Banelings, ItemNames.Kerrigan_Infest_Broodlings, ItemNames.Kerrigan_Fury):
            if self.has(item, player):
                count += 1
            if count >= 2:
                return True
        return False

    def _sc2hots_has_two_kerrigan_actives(self, multiworld: MultiWorld, player: int) -> bool:
        count = 0
        for i in range(7):
            if self.has_any(kerrigan_actives[i], player):
                count += 1
        return count >= 2

    def _sc2hots_has_low_tech(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has_any({ItemNames.Zergling, ItemNames.Swarm_Queen, ItemNames.Spine_Crawler}, player) \
               or self._sc2hots_has_common_unit(multiworld, player) and self._sc2hots_has_basic_kerrigan(multiworld, player)
