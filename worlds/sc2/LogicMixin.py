from BaseClasses import MultiWorld
from worlds.AutoWorld import LogicMixin
from .Options import get_option_value, RequiredTactics, kerrigan_unit_available, AllInMap, GameDifficulty, \
    GrantStoryTech
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
        return (self.has_any({ItemNames.VIKING, ItemNames.WRAITH, ItemNames.BANSHEE, ItemNames.BATTLECRUISER}, player) or self._sc2_advanced_tactics(multiworld, player)
                and self.has_any({ItemNames.HERCULES, ItemNames.MEDIVAC}, player) and self._sc2wol_has_common_unit(multiworld, player)
        )

    def _sc2wol_has_air_anti_air(self, multiworld: MultiWorld, player: int) -> bool:
        return (
            self.has(ItemNames.VIKING, player)
            or self.has_all({ItemNames.WRAITH, ItemNames.WRAITH_ADVANCED_LASER_TECHNOLOGY}, player)
            or self.has_all({ItemNames.BATTLECRUISER, ItemNames.BATTLECRUISER_ATX_LASER_BATTERY}, player)
            or self._sc2_advanced_tactics(multiworld, player) and self.has_any({ItemNames.WRAITH, ItemNames.VALKYRIE, ItemNames.BATTLECRUISER}, player)
        )

    def _sc2wol_has_competent_ground_to_air(self, multiworld: MultiWorld, player: int) -> bool:
        return (
            self.has(ItemNames.GOLIATH, player)
            or self.has(ItemNames.MARINE, player) and self.has_any({ItemNames.MEDIC, ItemNames.MEDIVAC}, player)
            or self._sc2_advanced_tactics(multiworld, player) and self.has(ItemNames.CYCLONE, player)
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
            and self.has_any({ItemNames.MARINE, ItemNames.VULTURE}, player)
            and self._sc2wol_has_air_anti_air(multiworld, player)
        )

    def _sc2wol_has_anti_air(self, multiworld: MultiWorld, player: int) -> bool:
        return (
            self.has_any({
                ItemNames.MISSILE_TURRET, ItemNames.THOR, ItemNames.WAR_PIGS, ItemNames.SPARTAN_COMPANY,
                ItemNames.HELS_ANGELS, ItemNames.BATTLECRUISER, ItemNames.MARINE, ItemNames.WRAITH,
                ItemNames.VALKYRIE, ItemNames.CYCLONE, ItemNames.WINGED_NIGHTMARES, ItemNames.BRYNHILDS
            }, player)
            or self._sc2wol_has_competent_anti_air(multiworld, player)
            or self._sc2_advanced_tactics(multiworld, player)
            and self.has_any({ItemNames.GHOST, ItemNames.SPECTRE, ItemNames.WIDOW_MINE, ItemNames.LIBERATOR}, player)
        )

    def _sc2wol_defense_rating(self, multiworld: MultiWorld, player: int, zerg_enemy: bool, air_enemy: bool = True) -> int:
        defense_score = sum((defense_ratings[item] for item in defense_ratings if self.has(item, player)))
        if self.has_any({ItemNames.MARINE, ItemNames.MARAUDER}, player) and self.has(ItemNames.BUNKER, player):
            defense_score += 3
        if self.has_all({ItemNames.SIEGE_TANK, ItemNames.SIEGE_TANK_MAELSTROM_ROUNDS}, player):
            defense_score += 2
        if self.has_all({ItemNames.SIEGE_TANK, ItemNames.SIEGE_TANK_GRADUATING_RANGE}, player):
            defense_score += 1
        if self.has_all({ItemNames.WIDOW_MINE, ItemNames.WIDOW_MINE_CONCEALMENT}, player):
            defense_score += 1
        if zerg_enemy:
            defense_score += sum((zerg_defense_ratings[item] for item in zerg_defense_ratings if self.has(item, player)))
            if self.has(ItemNames.FIREBAT, player) and self.has(ItemNames.BUNKER, player):
                defense_score += 2
        if not air_enemy and self.has(ItemNames.MISSILE_TURRET, player):
            defense_score -= defense_ratings[ItemNames.MISSILE_TURRET]
        # Advanced Tactics bumps defense rating requirements down by 2
        if self._sc2_advanced_tactics(multiworld, player):
            defense_score += 2
        return defense_score

    def _sc2wol_has_competent_comp(self, multiworld: MultiWorld, player: int) -> bool:
        return (
            (
                (self.has_any({ItemNames.MARINE, ItemNames.MARAUDER}, player)
                    and self.has_any({ItemNames.MEDIVAC, ItemNames.MEDIC}, player))
                or self.has_any({ItemNames.THOR, ItemNames.BANSHEE, ItemNames.SIEGE_TANK}, player)
                or self.has_all({ItemNames.LIBERATOR, ItemNames.LIBERATOR_RAID_ARTILLERY}, player)
            )
            and self._sc2wol_has_competent_anti_air(multiworld, player)
        ) or (
            self.has(ItemNames.BATTLECRUISER, player) and self._sc2wol_has_common_unit(multiworld, player)
        )

    def _sc2wol_has_train_killers(self, multiworld: MultiWorld, player: int) -> bool:
        return (
            self.has_any({ItemNames.SIEGE_TANK, ItemNames.DIAMONDBACK, ItemNames.MARAUDER, ItemNames.CYCLONE}, player)
            or self._sc2_advanced_tactics(multiworld, player)
            and (
                self.has_all({ItemNames.REAPER, ItemNames.REAPER_G4_CLUSTERBOMB}, player)
                or self.has_all({ItemNames.SPECTRE, ItemNames.SPECTRE_PSIONIC_LASH}, player)
                or self.has_any({ItemNames.VULTURE, ItemNames.LIBERATOR}, player)
            )
        )

    def _sc2wol_able_to_rescue(self, multiworld: MultiWorld, player: int) -> bool:
        return (self.has_any({ItemNames.MEDIVAC, ItemNames.HERCULES, ItemNames.RAVEN, ItemNames.VIKING}, player)
                or self._sc2_advanced_tactics(multiworld, player)
        )

    def _sc2wol_has_protoss_common_units(self, multiworld: MultiWorld, player: int) -> bool:
        return (self.has_any({ItemNames.ZEALOT, ItemNames.IMMORTAL, ItemNames.STALKER, ItemNames.DARK_TEMPLAR}, player)
                or self._sc2_advanced_tactics(multiworld, player) and self.has(ItemNames.HIGH_TEMPLAR, player)
        )

    def _sc2wol_has_protoss_medium_units(self, multiworld: MultiWorld, player: int) -> bool:
        return (
            self._sc2wol_has_protoss_common_units(multiworld, player)
                and self.has_any({ItemNames.STALKER, ItemNames.VOID_RAY, ItemNames.CARRIER}, player)
            or self._sc2_advanced_tactics(multiworld, player)
                and self.has(ItemNames.DARK_TEMPLAR, player)
        )

    def _sc2wol_beats_protoss_deathball(self, multiworld: MultiWorld, player: int) -> bool:
        return (
            (
                self.has_any({ItemNames.BANSHEE, ItemNames.BATTLECRUISER}, player)
                or self.has_all({ItemNames.LIBERATOR, ItemNames.LIBERATOR_RAID_ARTILLERY}, player)
            ) and self._sc2wol_has_competent_anti_air(multiworld, player)
            or self._sc2wol_has_competent_comp(multiworld, player) and self._sc2wol_has_air_anti_air(multiworld, player)
        )

    def _sc2wol_has_mm_upgrade(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has_any({ItemNames.MARINE_COMBAT_SHIELD, ItemNames.MEDIC_STABILIZER_MEDPACKS}, player)

    def _sc2wol_survives_rip_field(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has(ItemNames.BATTLECRUISER, player) or \
           self._sc2wol_has_air(multiworld, player) and \
           self._sc2wol_has_competent_anti_air(multiworld, player) and \
           self.has(ItemNames.SCIENCE_VESSEL, player)

    def _sc2wol_has_nukes(self, multiworld: MultiWorld, player: int) -> bool:
        return (self._sc2_advanced_tactics(multiworld, player)
                and (self.has_any({ItemNames.GHOST, ItemNames.SPECTRE}, player)
                     or self.has_all({ItemNames.THOR, ItemNames.THOR_BUTTON_WITH_A_SKULL_ON_IT}), player))

    def _sc2wol_can_respond_to_colony_infestations(self, multiworld: MultiWorld, player: int) -> bool:
        return (
            self._sc2wol_has_common_unit(multiworld, player)
            and self._sc2wol_has_competent_anti_air(multiworld, player)
            and (
                    self._sc2wol_has_air_anti_air(multiworld, player)
                    or self.has_any({ItemNames.BATTLECRUISER, ItemNames.VALKYRIE}, player)
                )
            and self._sc2wol_defense_rating(multiworld, player, True) >= 3
        )

    def _sc2wol_final_mission_requirements(self, multiworld: MultiWorld, player: int):
        beats_kerrigan = self.has_any({ItemNames.MARINE, ItemNames.BANSHEE, ItemNames.GHOST}, player) or self._sc2_advanced_tactics(multiworld, player)
        if get_option_value(multiworld, player, 'all_in_map') == AllInMap.option_ground:
            # Ground
            defense_rating = self._sc2wol_defense_rating(multiworld, player, True, False)
            if self.has_any({ItemNames.BATTLECRUISER, ItemNames.BANSHEE}, player):
                defense_rating += 3
            return defense_rating >= 12 and beats_kerrigan
        else:
            # Air
            defense_rating = self._sc2wol_defense_rating(multiworld, player, True, True)
            return defense_rating >= 8 and beats_kerrigan \
                and self.has_any({ItemNames.VIKING, ItemNames.BATTLECRUISER, ItemNames.VALKYRIE}, player) \
                and self.has_any({ItemNames.HIVE_MIND_EMULATOR, ItemNames.PSI_DISRUPTER, ItemNames.MISSILE_TURRET}, player)

    def _sc2wol_cleared_missions(self, multiworld: MultiWorld, player: int, mission_count: int) -> bool:
        return self.has_group("WoL Missions", player, mission_count)

    # HotS
    def _sc2hots_has_common_unit(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has_any(get_basic_units(multiworld, player, SC2Race.ZERG), player)

    def _sc2hots_has_good_antiair(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has_any({ItemNames.HYDRALISK, ItemNames.MUTALISK}, player) or \
            self.has_all({ItemNames.SWARM_HOST, ItemNames.SWARM_HOST_PRESSURIZED_GLANDS}, player) or \
            (self._sc2_advanced_tactics(multiworld, player) and self.has(ItemNames.INFESTOR, player))

    def _sc2hots_has_minimal_antiair(self, multiworld: MultiWorld, player: int) -> bool:
        return self._sc2hots_has_good_antiair(multiworld, player) or get_option_value(multiworld, player, 'kerrigan_presence') in kerrigan_unit_available or \
            self.has(ItemNames.SWARM_QUEEN, player) or (self._sc2_advanced_tactics(multiworld, player) and self.has(ItemNames.SPORE_CRAWLER, player))
    
    def _sc2hots_has_brood_lord(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has_all({ItemNames.MUTALISK, ItemNames.MUTALISK_BROOD_LORD_STRAIN}, player)
    
    def _sc2hots_has_viper(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has_all({ItemNames.MUTALISK, ItemNames.MUTALISK_VIPER_STRAIN}, player)

    def _sc2hots_has_impaler_or_lurker(self, multiworld: MultiWorld, player: int) -> bool:
        return self.has(ItemNames.HYDRALISK, player) and self.has_any({ItemNames.HYDRALISK_IMPALER_STRAIN, ItemNames.HYDRALISK_LURKER_STRAIN}, player)

    def _sc2hots_has_competent_comp(self, multiworld: MultiWorld, player: int) -> bool:
        advanced = self._sc2_advanced_tactics(multiworld, player)
        core_unit = self.has_any({ItemNames.ROACH, ItemNames.ABERRATION, ItemNames.ZERGLING}, player)
        support_unit = self.has_any({ItemNames.SWARM_QUEEN, ItemNames.HYDRALISK}, player) \
                       or self._sc2hots_has_brood_lord(multiworld, player) \
                       or advanced and (self.has(ItemNames.INFESTOR, player) or self._sc2hots_has_viper(multiworld, player))
        if core_unit and support_unit:
            return True
        vespene_unit = self.has_any({ItemNames.ULTRALISK, ItemNames.ABERRATION}, player) \
                       or advanced and self._sc2hots_has_viper(multiworld, player)
        return vespene_unit and self.has_any({ItemNames.ZERGLING, ItemNames.SWARM_QUEEN}, player)

    def _sc2hots_has_basic_comp(self, multiworld: MultiWorld, player: int) -> bool:
        if get_option_value(multiworld, player, 'game_difficulty') < GameDifficulty.option_brutal \
           or self._sc2hots_has_basic_kerrigan(multiworld, player) \
           or self._sc2hots_has_two_kerrigan_actives(multiworld, player):
            return self._sc2hots_has_common_unit(multiworld, player)
        else:
            return self._sc2hots_has_competent_comp(multiworld, player)

    def _sc2hots_can_spread_creep(self, multiworld: MultiWorld, player: int) -> bool:
        return self._sc2_advanced_tactics(multiworld, player) or self.has(ItemNames.SWARM_QUEEN, player)
    
    def _sc2hots_has_competent_defense(self, multiworld: MultiWorld, player: int) -> bool:
        return (
            self._sc2hots_has_common_unit(multiworld, player)
            and (
                (
                    self.has(ItemNames.SWARM_HOST, player)
                    or self._sc2hots_has_brood_lord(multiworld, player)
                    or self._sc2hots_has_impaler_or_lurker(multiworld, player)
                ) or (
                    self._sc2_advanced_tactics(multiworld, player)
                    and (self._sc2hots_has_viper(multiworld, player)
                        or self.has(ItemNames.SPINE_CRAWLER, player))
                )
            )
        )

    def _sc2hots_has_basic_kerrigan(self, multiworld: MultiWorld, player: int) -> bool:
        # One active ability that can be used to defeat enemies directly on Standard
        if not self._sc2_advanced_tactics(multiworld, player) and \
            not self.has_any({ItemNames.KERRIGAN_KINETIC_BLAST, ItemNames.KERRIGAN_LEAPING_STRIKE,
                              ItemNames.KERRIGAN_CRUSHING_GRIP, ItemNames.KERRIGAN_PSIONIC_SHIFT,
                              ItemNames.KERRIGAN_SPAWN_BANELINGS}, player):
            return False
        # Two non-ultimate abilities
        count = 0
        for item in (ItemNames.KERRIGAN_KINETIC_BLAST, ItemNames.KERRIGAN_LEAPING_STRIKE, ItemNames.KERRIGAN_HEROIC_FORTITUDE,
                     ItemNames.KERRIGAN_CHAIN_REACTION, ItemNames.KERRIGAN_CRUSHING_GRIP, ItemNames.KERRIGAN_PSIONIC_SHIFT,
                     ItemNames.KERRIGAN_SPAWN_BANELINGS, ItemNames.KERRIGAN_INFEST_BROODLINGS, ItemNames.KERRIGAN_FURY):
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
        return self.has_any({ItemNames.ZERGLING, ItemNames.SWARM_QUEEN, ItemNames.SPINE_CRAWLER}, player) \
               or self._sc2hots_has_common_unit(multiworld, player) and self._sc2hots_has_basic_kerrigan(multiworld, player)

    def _sc2hots_can_pass_vents(self, multiworld: MultiWorld, player: int) -> bool:
        return (get_option_value(multiworld, player, "grant_story_tech") == GrantStoryTech.option_true) \
            or self.has(ItemNames.ZERGLING, player) \
            or (self._sc2_advanced_tactics(multiworld, player) and self.has(ItemNames.INFESTOR, player))

    def _sc2hots_can_pass_supreme(self, multiworld: MultiWorld, player: int) -> bool:
        return (get_option_value(multiworld, player, "grant_story_tech") == GrantStoryTech.option_true) \
            or (get_option_value(multiworld, player, "kerrigan_presence") not in kerrigan_unit_available) \
            or self.has_all({ItemNames.KERRIGAN_LEAPING_STRIKE, ItemNames.KERRIGAN_MEND}, player)
