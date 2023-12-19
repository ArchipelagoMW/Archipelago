from BaseClasses import MultiWorld, CollectionState
from worlds.AutoWorld import LogicMixin
from .Options import get_option_value, RequiredTactics, kerrigan_unit_available, AllInMap, GameDifficulty, \
    GrantStoryTech, TakeOverAIAllies, SpearOfAdunAutonomouslyCastAbilityPresence
from .Items import get_basic_units, defense_ratings, zerg_defense_ratings, kerrigan_actives, air_defense_ratings
from .MissionTables import SC2Race
from . import ItemNames


class SC2Logic:

    # WoL
    def terran_common_unit(self, state: CollectionState) -> bool:
        return state.has_any(self.basic_terran_units, self.player)

    def terran_early_tech(self, state: CollectionState):
        """
        Basic combat unit that can be deployed quickly from mission start
        :param state
        :return:
        """
        return (
                state.has_any({ItemNames.MARINE, ItemNames.FIREBAT, ItemNames.MARAUDER, ItemNames.REAPER, ItemNames.HELLION}, self.player)
                or (self.advanced_tactics and state.has_any({ItemNames.GOLIATH, ItemNames.DIAMONDBACK, ItemNames.VIKING, ItemNames.BANSHEE}, self.player))
        )

    def terran_air(self, state: CollectionState) -> bool:
        """
        Air units or drops on advanced tactics
        :param state:
        :return:
        """
        return (state.has_any({ItemNames.VIKING, ItemNames.WRAITH, ItemNames.BANSHEE, ItemNames.BATTLECRUISER}, self.player) or self.advanced_tactics
                and state.has_any({ItemNames.HERCULES, ItemNames.MEDIVAC}, self.player) and self.terran_common_unit(state)
        )

    def terran_air_anti_air(self, state: CollectionState) -> bool:
        """
        Air-to-air
        :param state:
        :return:
        """
        return (
            state.has(ItemNames.VIKING, self.player)
            or state.has_all({ItemNames.WRAITH, ItemNames.WRAITH_ADVANCED_LASER_TECHNOLOGY}, self.player)
            or state.has_all({ItemNames.BATTLECRUISER, ItemNames.BATTLECRUISER_ATX_LASER_BATTERY}, self.player)
            or self.advanced_tactics and state.has_any({ItemNames.WRAITH, ItemNames.VALKYRIE, ItemNames.BATTLECRUISER}, self.player)
        )

    def terran_competent_ground_to_air(self, state: CollectionState) -> bool:
        """
        Ground-to-air
        :param state:
        :return:
        """
        return (
            state.has(ItemNames.GOLIATH, self.player)
            or state.has(ItemNames.MARINE, self.player) and self.terran_bio_heal(state)
            or self.advanced_tactics and state.has(ItemNames.CYCLONE, self.player)
        )

    def terran_competent_anti_air(self, state: CollectionState) -> bool:
        """
        Good AA unit
        :param state:
        :return:
        """
        return (
            self.terran_competent_ground_to_air(state)
            or self.terran_air_anti_air(state)
        )

    def welcome_to_the_jungle_requirement(self, state: CollectionState) -> bool:
        """
        Welcome to the Jungle requirements - able to deal with Scouts, Void Rays, Zealots and Stalkers
        :param state:
        :return:
        """
        return (
            self.terran_common_unit(state)
            and self.terran_competent_ground_to_air(state)
        ) or (
            self.advanced_tactics
            and state.has_any({ItemNames.MARINE, ItemNames.VULTURE}, self.player)
            and self.terran_air_anti_air(state)
        )

    def terran_basic_anti_air(self, state: CollectionState) -> bool:
        """
        Basic AA to deal with few air units
        :param state:
        :return:
        """
        return (
            state.has_any({
                ItemNames.MISSILE_TURRET, ItemNames.THOR, ItemNames.WAR_PIGS, ItemNames.SPARTAN_COMPANY,
                ItemNames.HELS_ANGELS, ItemNames.BATTLECRUISER, ItemNames.MARINE, ItemNames.WRAITH,
                ItemNames.VALKYRIE, ItemNames.CYCLONE, ItemNames.WINGED_NIGHTMARES, ItemNames.BRYNHILDS
            }, self.player)
            or self.terran_competent_anti_air(state)
            or self.advanced_tactics and state.has_any({ItemNames.GHOST, ItemNames.SPECTRE, ItemNames.WIDOW_MINE, ItemNames.LIBERATOR}, self.player)
        )

    def terran_defense_rating(self, state: CollectionState, zerg_enemy: bool, air_enemy: bool = True) -> int:
        """
        Ability to handle defensive missions
        :param state:
        :param zerg_enemy:
        :param air_enemy:
        :return:
        """
        defense_score = sum((defense_ratings[item] for item in defense_ratings if state.has(item, self.player)))
        # Manned Bunker
        if state.has_any({ItemNames.MARINE, ItemNames.MARAUDER}, self.player) and state.has(ItemNames.BUNKER, self.player):
            defense_score += 3
        elif zerg_enemy and state.has(ItemNames.FIREBAT, self.player) and state.has(ItemNames.BUNKER, self.player):
            defense_score += 2
        # Siege Tank upgrades
        if state.has_all({ItemNames.SIEGE_TANK, ItemNames.SIEGE_TANK_MAELSTROM_ROUNDS}, self.player):
            defense_score += 2
        if state.has_all({ItemNames.SIEGE_TANK, ItemNames.SIEGE_TANK_GRADUATING_RANGE}, self.player):
            defense_score += 1
        # Widow Mine upgrade
        if state.has_all({ItemNames.WIDOW_MINE, ItemNames.WIDOW_MINE_CONCEALMENT}, self.player):
            defense_score += 1
        # Viking with splash
        if state.has_all({ItemNames.VIKING, ItemNames.VIKING_SHREDDER_ROUNDS}, self.player):
            defense_score += 2
        # Banshee upgrade
        if state.has_all({ItemNames.BANSHEE, ItemNames.BANSHEE_ROCKET_BARRAGE}, self.player):
            defense_score += 3

        # General enemy-based rules
        if zerg_enemy:
            defense_score += sum((zerg_defense_ratings[item] for item in zerg_defense_ratings if state.has(item, self.player)))
        if air_enemy:
            defense_score += sum((air_defense_ratings[item] for item in air_defense_ratings if state.has(item, self.player)))
        # Advanced Tactics bumps defense rating requirements down by 2
        if self.advanced_tactics:
            defense_score += 2
        return defense_score

    def terran_competent_comp(self, state: CollectionState) -> bool:
        """
        Ability to deal with most of hard missions
        :param state:
        :return:
        """
        return (
            (
                (state.has_any({ItemNames.MARINE, ItemNames.MARAUDER}, self.player) and self.terran_bio_heal(state))
                or state.has_any({ItemNames.THOR, ItemNames.BANSHEE, ItemNames.SIEGE_TANK}, self.player)
                or state.has_all({ItemNames.LIBERATOR, ItemNames.LIBERATOR_RAID_ARTILLERY}, self.player)
            )
            and self.terran_competent_anti_air(state)
        ) or (
            state.has(ItemNames.BATTLECRUISER, self.player) and self.terran_common_unit(state)
        )

    def great_train_robbery_requirement(self, state: CollectionState) -> bool:
        """
        Ability to deal with trains (moving target with a lot of HP)
        :param state:
        :return:
        """
        return (
            state.has_any({ItemNames.SIEGE_TANK, ItemNames.DIAMONDBACK, ItemNames.MARAUDER, ItemNames.CYCLONE, ItemNames.BANSHEE}, self.player)
            or self.advanced_tactics
            and (
                state.has_all({ItemNames.REAPER, ItemNames.REAPER_G4_CLUSTERBOMB}, self.player)
                or state.has_all({ItemNames.SPECTRE, ItemNames.SPECTRE_PSIONIC_LASH}, self.player)
                or state.has_any({ItemNames.VULTURE, ItemNames.LIBERATOR}, self.player)
            )
        )

    def terran_can_rescue(self, state) -> bool:
        """
        Rescuing in The Moebius Factor
        :param state:
        :return:
        """
        return state.has_any({ItemNames.MEDIVAC, ItemNames.HERCULES, ItemNames.RAVEN, ItemNames.VIKING}, self.player) or self.advanced_tactics

    def terran_beats_protoss_deathball(self, state: CollectionState) -> bool:
        """
        Ability to deal with Immortals, Colossi with some air support
        :param state:
        :return:
        """
        return (
            (
                state.has_any({ItemNames.BANSHEE, ItemNames.BATTLECRUISER}, self.player)
                or state.has_all({ItemNames.LIBERATOR, ItemNames.LIBERATOR_RAID_ARTILLERY}, self.player)
            ) and self.terran_competent_anti_air(state)
            or self.terran_competent_comp(state) and self.terran_air_anti_air(state)
        )

    def marine_medic_upgrade(self, state: CollectionState) -> bool:
        """
        Infantry upgrade to infantry-only no-build segments
        :param state:
        :return:
        """
        return state.has_any({
            ItemNames.MARINE_COMBAT_SHIELD, ItemNames.MARINE_MAGRAIL_MUNITIONS, ItemNames.MEDIC_STABILIZER_MEDPACKS
        }, self.player) \
            or (state.count(ItemNames.MARINE_PROGRESSIVE_STIMPACK, self.player) >= 2
                and state.has_group("Missions", self.player, 1))

    def terran_survives_rip_field(self, state: CollectionState) -> bool:
        """
        Ability to deal with large areas with environment damage
        :param state:
        :return:
        """
        return (state.has(ItemNames.BATTLECRUISER, self.player)
                or self.terran_air(state) and self.terran_competent_anti_air(state) and self.terran_sustainable_mech_heal(state))

    def terran_sustainable_mech_heal(self, state: CollectionState) -> bool:
        """
        Can heal mech units without spending resources
        :param state:
        :return:
        """
        return state.has(ItemNames.SCIENCE_VESSEL, self.player) \
            or state.has_all({ItemNames.MEDIC, ItemNames.MEDIC_ADAPTIVE_MEDPACKS}, self.player) \
            or state.count(ItemNames.PROGRESSIVE_REGENERATIVE_BIO_STEEL, self.player) >= 3 \
            or (self.advanced_tactics
                and (
                        state.has_all({ItemNames.RAVEN, ItemNames.RAVEN_BIO_MECHANICAL_REPAIR_DRONE}, self.player)
                        or state.count(ItemNames.PROGRESSIVE_REGENERATIVE_BIO_STEEL, self.player) >= 2)
                )

    def terran_bio_heal(self, state: CollectionState) -> bool:
        """
        Ability to heal bio units
        :param state:
        :return:
        """
        return state.has_any({ItemNames.MEDIC, ItemNames.MEDIVAC}, self.player) \
            or self.advanced_tactics and state.has_all({ItemNames.RAVEN, ItemNames.RAVEN_BIO_MECHANICAL_REPAIR_DRONE}, self.player)

    def terran_base_trasher(self, state: CollectionState) -> bool:
        """
        Can attack heavily defended bases
        :param state:
        :return:
        """
        return state.has(ItemNames.SIEGE_TANK, self.player) \
            or state.has_all({ItemNames.BATTLECRUISER, ItemNames.BATTLECRUISER_ATX_LASER_BATTERY}, self.player) \
            or state.has_all({ItemNames.LIBERATOR, ItemNames.LIBERATOR_RAID_ARTILLERY}, self.player) \
            or (
                    state.has_all({ItemNames.BANSHEE, ItemNames.BANSHEE_ROCKET_BARRAGE}, self.player)
                    and (
                            self.advanced_tactics
                            or state.has(ItemNames.BANSHEE_ADVANCED_TARGETING_OPTICS, self.player)
                    )
            ) \
            or (self.advanced_tactics
                and ((state.has_all({ItemNames.RAVEN, ItemNames.RAVEN_HUNTER_SEEKER_WEAPON}, self.player)
                      or self.can_nuke(state))
                     and (
                             state.has_all({ItemNames.VIKING, ItemNames.VIKING_SHREDDER_ROUNDS}, self.player)
                             or state.has_all({ItemNames.BANSHEE, ItemNames.BANSHEE_SHOCKWAVE_MISSILE_BATTERY}, self.player))
                     )
                )

    def can_nuke(self, state: CollectionState) -> bool:
        """
        Ability to launch nukes
        :param state:
        :return:
        """
        return (self.advanced_tactics
                and (state.has_any({ItemNames.GHOST, ItemNames.SPECTRE}, self.player)
                     or state.has_all({ItemNames.THOR, ItemNames.THOR_BUTTON_WITH_A_SKULL_ON_IT}, self.player)))

    def terran_respond_to_colony_infestations(self, state: CollectionState) -> bool:
        """
        Can deal quickly with Brood Lords and Mutas in Haven's Fall and being able to progress the mission
        :param state:
        :return:
        """
        return (
            self.terran_common_unit(state)
            and self.terran_competent_anti_air(state)
            and (
                    self.terran_air_anti_air(state)
                    or state.has_any({ItemNames.BATTLECRUISER, ItemNames.VALKYRIE}, self.player)
                )
            and self.terran_defense_rating(state, True) >= 3
        )

    def all_in_requirement(self, state: CollectionState):
        """
        All-in
        :param state:
        :return:
        """
        beats_kerrigan = state.has_any({ItemNames.MARINE, ItemNames.BANSHEE, ItemNames.GHOST}, self.player) or self.advanced_tactics
        if get_option_value(self.multiworld, self.player, 'all_in_map') == AllInMap.option_ground:
            # Ground
            defense_rating = self.terran_defense_rating(state, True, False)
            if state.has_any({ItemNames.BATTLECRUISER, ItemNames.BANSHEE}, self.player):
                defense_rating += 2
            return defense_rating >= 13 and beats_kerrigan
        else:
            # Air
            defense_rating = self.terran_defense_rating(state, True, True)
            return defense_rating >= 9 and beats_kerrigan \
                and state.has_any({ItemNames.VIKING, ItemNames.BATTLECRUISER, ItemNames.VALKYRIE}, self.player) \
                and state.has_any({ItemNames.HIVE_MIND_EMULATOR, ItemNames.PSI_DISRUPTER, ItemNames.MISSILE_TURRET}, self.player)

    # HotS
    def zerg_common_unit(self, state: CollectionState) -> bool:
        return state.has_any(self.basic_zerg_units, self.player)

    def zerg_competent_anti_air(self, state: CollectionState) -> bool:
        return state.has_any({ItemNames.HYDRALISK, ItemNames.MUTALISK, ItemNames.CORRUPTOR}, self.player) \
            or state.has_all({ItemNames.SWARM_HOST, ItemNames.SWARM_HOST_PRESSURIZED_GLANDS}, self.player) \
            or state.has_all({ItemNames.SCOURGE, ItemNames.SCOURGE_RESOURCE_EFFICIENCY}, self.player) \
            or (self.advanced_tactics and state.has(ItemNames.INFESTOR, self.player))

    def zerg_basic_anti_air(self, state: CollectionState) -> bool:
        return self.zerg_competent_anti_air(state) or self.kerrigan_unit_available in kerrigan_unit_available or \
               state.has_any({ItemNames.SWARM_QUEEN, ItemNames.SCOURGE}, self.player) or (self.advanced_tactics and state.has(ItemNames.SPORE_CRAWLER, self.player))
    
    def morph_brood_lord(self, state: CollectionState) -> bool:
        return state.has_any({ItemNames.MUTALISK, ItemNames.CORRUPTOR}, self.player) \
            and state.has(ItemNames.MUTALISK_CORRUPTOR_BROOD_LORD_ASPECT, self.player)
    
    def morph_viper(self, state: CollectionState) -> bool:
        return state.has_any({ItemNames.MUTALISK, ItemNames.CORRUPTOR}, self.player) \
            and state.has(ItemNames.MUTALISK_CORRUPTOR_VIPER_ASPECT, self.player)

    def morph_impaler_or_lurker(self, state: CollectionState) -> bool:
        return state.has(ItemNames.HYDRALISK, self.player) and state.has_any({ItemNames.HYDRALISK_IMPALER_ASPECT, ItemNames.HYDRALISK_LURKER_ASPECT}, self.player)

    def zerg_competent_comp(self, state: CollectionState) -> bool:
        advanced = self.advanced_tactics
        core_unit = state.has_any({ItemNames.ROACH, ItemNames.ABERRATION, ItemNames.ZERGLING}, self.player)
        support_unit = state.has_any({ItemNames.SWARM_QUEEN, ItemNames.HYDRALISK}, self.player) \
                       or self.morph_brood_lord(state) \
                       or advanced and (state.has(ItemNames.INFESTOR, self.player) or self.morph_viper(state))
        if core_unit and support_unit:
            return True
        vespene_unit = state.has_any({ItemNames.ULTRALISK, ItemNames.ABERRATION}, self.player) \
                       or advanced and self.morph_viper(state)
        return vespene_unit and state.has_any({ItemNames.ZERGLING, ItemNames.SWARM_QUEEN}, self.player)

    def spread_creep(self, state: CollectionState) -> bool:
        return self.advanced_tactics or state.has(ItemNames.SWARM_QUEEN, self.player)
    
    def zerg_competent_defense(self, state: CollectionState) -> bool:
        return (
            self.zerg_common_unit(state)
            and (
                (
                    state.has(ItemNames.SWARM_HOST, self.player)
                    or self.morph_brood_lord(state)
                    or self.morph_impaler_or_lurker(state)
                ) or (
                    self.advanced_tactics
                    and (self.morph_viper(state)
                        or state.has(ItemNames.SPINE_CRAWLER, self.player))
                )
            )
        )

    def basic_kerrigan(self, state: CollectionState) -> bool:
        # One active ability that can be used to defeat enemies directly on Standard
        if not self.advanced_tactics and \
            not state.has_any({ItemNames.KERRIGAN_KINETIC_BLAST, ItemNames.KERRIGAN_LEAPING_STRIKE,
                              ItemNames.KERRIGAN_CRUSHING_GRIP, ItemNames.KERRIGAN_PSIONIC_SHIFT,
                              ItemNames.KERRIGAN_SPAWN_BANELINGS}, self.player):
            return False
        # Two non-ultimate abilities
        count = 0
        for item in (ItemNames.KERRIGAN_KINETIC_BLAST, ItemNames.KERRIGAN_LEAPING_STRIKE, ItemNames.KERRIGAN_HEROIC_FORTITUDE,
                     ItemNames.KERRIGAN_CHAIN_REACTION, ItemNames.KERRIGAN_CRUSHING_GRIP, ItemNames.KERRIGAN_PSIONIC_SHIFT,
                     ItemNames.KERRIGAN_SPAWN_BANELINGS, ItemNames.KERRIGAN_INFEST_BROODLINGS, ItemNames.KERRIGAN_FURY):
            if state.has(item, self.player):
                count += 1
            if count >= 2:
                return True
        return False

    def two_kerrigan_actives(self, state: CollectionState) -> bool:
        count = 0
        for i in range(7):
            if state.has_any(kerrigan_actives[i], self.player):
                count += 1
        return count >= 2

    def zerg_pass_vents(self, state: CollectionState) -> bool:
        return self.story_tech_granted \
            or state.has(ItemNames.ZERGLING, self.player) \
            or (self.advanced_tactics and state.has(ItemNames.INFESTOR, self.player))

    def supreme_requirement(self, state: CollectionState) -> bool:
        return self.story_tech_granted \
            or not self.kerrigan_unit_available \
            or state.has_all({ItemNames.KERRIGAN_LEAPING_STRIKE, ItemNames.KERRIGAN_MEND}, self.player)

    def the_reckoning_requirement(self, state: CollectionState) -> bool:
        if self.take_over_ai_allies:
            return self.terran_competent_comp(state) \
                and self.zerg_competent_comp(state) \
                and (self.zerg_competent_anti_air(state)
                     or self.terran_competent_anti_air(state))
        else:
            return self.zerg_competent_comp(state) \
                and self.zerg_competent_anti_air(state)

    # LotV

    def protoss_common_unit(self, state: CollectionState) -> bool:
        return state.has_any(self.basic_protoss_units, self.player)

    def protoss_basic_anti_air(self, state: CollectionState) -> bool:
        return self.protoss_competent_anti_air(state) \
            or state.has_any({ItemNames.PHOENIX, ItemNames.MIRAGE, ItemNames.CORSAIR, ItemNames.CARRIER, ItemNames.SCOUT,
                             ItemNames.DARK_ARCHON, ItemNames.WRATHWALKER, ItemNames.MOTHERSHIP}, self.player) \
            or state.has_all({ItemNames.WARP_PRISM, ItemNames.WARP_PRISM_PHASE_BLASTER}, self.player) \
            or self.advanced_tactics and state.has_any(
                {ItemNames.HIGH_TEMPLAR, ItemNames.SIGNIFIER, ItemNames.ASCENDANT, ItemNames.DARK_TEMPLAR,
                 ItemNames.SENTRY, ItemNames.ENERGIZER}, self.player)

    def protoss_anti_armor_anti_air(self, state: CollectionState) -> bool:
        return self.protoss_competent_anti_air(state) \
            or state.has_any({ItemNames.SCOUT, ItemNames.WRATHWALKER}, self.player) \
            or (state.has_any({ItemNames.IMMORTAL, ItemNames.ANNIHILATOR}, self.player)
                and state.has(ItemNames.IMMORTAL_ANNIHILATOR_ADVANCED_TARGETING_MECHANICS, self.player))

    def protoss_anti_light_anti_air(self, state: CollectionState) -> bool:
        return self.protoss_competent_anti_air(state) \
            or state.has_any({ItemNames.PHOENIX, ItemNames.MIRAGE, ItemNames.CORSAIR, ItemNames.CARRIER}, self.player)

    def protoss_competent_anti_air(self, state: CollectionState) -> bool:
        return state.has_any(
            {ItemNames.STALKER, ItemNames.SLAYER, ItemNames.INSTIGATOR, ItemNames.DRAGOON, ItemNames.ADEPT,
             ItemNames.VOID_RAY, ItemNames.DESTROYER, ItemNames.TEMPEST}, self.player) \
            or (state.has_any({ItemNames.PHOENIX, ItemNames.MIRAGE, ItemNames.CORSAIR, ItemNames.CARRIER}, self.player)
                and state.has_any({ItemNames.SCOUT, ItemNames.WRATHWALKER}, self.player)) \
            or (self.advanced_tactics
                and state.has_any({ItemNames.IMMORTAL, ItemNames.ANNIHILATOR}, self.player)
                and state.has(ItemNames.IMMORTAL_ANNIHILATOR_ADVANCED_TARGETING_MECHANICS, self.player))

    def protoss_has_blink(self, state: CollectionState) -> bool:
        return state.has_any({ItemNames.STALKER, ItemNames.INSTIGATOR, ItemNames.SLAYER}, self.player) \
            or (
                    state.has(ItemNames.DARK_TEMPLAR_AVENGER_BLOOD_HUNTER_BLINK, self.player)
                    and state.has_any({ItemNames.DARK_TEMPLAR, ItemNames.BLOOD_HUNTER, ItemNames.AVENGER}, self.player)
            )

    def protoss_can_attack_behind_chasm(self, state: CollectionState) -> bool:
        return state.has_any(
            {ItemNames.SCOUT, ItemNames.TEMPEST,
             ItemNames.CARRIER, ItemNames.VOID_RAY, ItemNames.DESTROYER, ItemNames.MOTHERSHIP}, self.player) \
            or self.protoss_has_blink(state) \
            or (state.has(ItemNames.WARP_PRISM, self.player)
                and (self.protoss_common_unit(state) or state.has(ItemNames.WARP_PRISM_PHASE_BLASTER, self.player))) \
            or (self.advanced_tactics
                and state.has_any({ItemNames.ORACLE, ItemNames.ARBITER}, self.player))

    def protoss_fleet(self, state: CollectionState) -> bool:
        return state.has_any({ItemNames.CARRIER, ItemNames.TEMPEST, ItemNames.VOID_RAY, ItemNames.DESTROYER}, self.player)

    def templars_return_requirement(self, state: CollectionState) -> bool:
        return self.story_tech_granted \
            or (
                state.has_any({ItemNames.IMMORTAL, ItemNames.ANNIHILATOR}, self.player)
                and state.has_any({ItemNames.COLOSSUS, ItemNames.VANGUARD, ItemNames.REAVER, ItemNames.DARK_TEMPLAR}, self.player)
                and state.has_any({ItemNames.SENTRY, ItemNames.HIGH_TEMPLAR}, self.player)
            )

    def brothers_in_arms_requirement(self, state: CollectionState) -> bool:
        return (
                self.protoss_common_unit(state)
                and self.protoss_anti_armor_anti_air(state)
                and self.protoss_hybrid_counter(state)
        ) or (
                self.take_over_ai_allies
                and (
                        self.terran_common_unit(state)
                        or self.protoss_common_unit(state)
                )
                and (
                        self.terran_competent_anti_air(state)
                        or self.protoss_anti_armor_anti_air(state)
                )
                and (
                        self.protoss_hybrid_counter(state)
                        or state.has_any({ItemNames.BATTLECRUISER, ItemNames.LIBERATOR, ItemNames.SIEGE_TANK}, self.player)
                        or state.has_all({ItemNames.SPECTRE, ItemNames.SPECTRE_PSIONIC_LASH}, self.player)
                        or (state.has(ItemNames.IMMORTAL, self.player)
                            and state.has_any({ItemNames.MARINE, ItemNames.MARAUDER}, self.player)
                            and self.terran_bio_heal(state))
                )
        )

    def protoss_hybrid_counter(self, state: CollectionState) -> bool:
        """
        Ground Hybrids
        """
        return state.has_any(
            {ItemNames.ANNIHILATOR, ItemNames.ASCENDANT, ItemNames.TEMPEST, ItemNames.CARRIER, ItemNames.VOID_RAY,
             ItemNames.WRATHWALKER, ItemNames.VANGUARD}, self.player) \
            or (state.has(ItemNames.IMMORTAL, self.player) or self.advanced_tactics) and state.has_any(
                {ItemNames.STALKER, ItemNames.DRAGOON, ItemNames.ADEPT, ItemNames.INSTIGATOR, ItemNames.SLAYER}, self.player)

    def the_infinite_cycle_requirement(self, state: CollectionState) -> bool:
        return self.story_tech_granted \
            or not self.kerrigan_unit_available \
            or (
                self.two_kerrigan_actives(state)
                and self.basic_kerrigan(state)
            )

    def protoss_basic_splash(self, state: CollectionState) -> bool:
        return state.has_any(
            {ItemNames.ZEALOT, ItemNames.COLOSSUS, ItemNames.VANGUARD, ItemNames.HIGH_TEMPLAR, ItemNames.SIGNIFIER,
             ItemNames.DARK_TEMPLAR, ItemNames.REAVER, ItemNames.ASCENDANT}, self.player)

    def protoss_static_defense(self, state: CollectionState) -> bool:
        return state.has_any({ItemNames.PHOTON_CANNON, ItemNames.KHAYDARIN_MONOLITH}, self.player)

    def last_stand_requirement(self, state: CollectionState) -> bool:
        return self.protoss_common_unit(state) \
            and self.protoss_competent_anti_air(state) \
            and self.protoss_static_defense(state) \
            and (
                self.advanced_tactics
                or self.protoss_basic_splash(state)
            )

    def harbinger_of_oblivion_requirement(self, state: CollectionState) -> bool:
        return self.protoss_anti_armor_anti_air(state) and (
                self.take_over_ai_allies
                or (
                        self.protoss_common_unit(state)
                        and self.protoss_hybrid_counter(state)
                )
        )

    def protoss_competent_comp(self, state: CollectionState) -> bool:
        return self.protoss_common_unit(state) \
            and self.protoss_competent_anti_air(state) \
            and self.protoss_hybrid_counter(state) \
            and self.protoss_basic_splash(state)

    def steps_of_the_rite_requirement(self, state: CollectionState) -> bool:
        return self.protoss_competent_comp(state) \
            or (
                    self.protoss_common_unit(state)
                    and self.protoss_competent_anti_air(state)
                    and self.protoss_static_defense(state)
            )

    def protoss_heal(self, state: CollectionState) -> bool:
        return state.has_any({ItemNames.CARRIER, ItemNames.SENTRY, ItemNames.SHIELD_BATTERY, ItemNames.RECONSTRUCTION_BEAM}, self.player)

    def templars_charge_requirement(self, state: CollectionState) -> bool:
        return self.protoss_heal(state) \
            and self.protoss_anti_armor_anti_air(state) \
            and (
                    self.protoss_fleet(state)
                    or (self.advanced_tactics
                        and self.protoss_competent_comp(state)
                        )
            )

    def the_host_requirement(self, state: CollectionState) -> bool:
        return (self.protoss_fleet(state)
                and self.protoss_static_defense(state)
                ) or (
                self.protoss_competent_comp(state)
                and state.has(ItemNames.SOA_TIME_STOP, self.player)
        )

    def salvation_requirement(self, state: CollectionState) -> bool:
        return [
            self.protoss_competent_comp(state),
            self.protoss_fleet(state),
            self.protoss_static_defense(state)
        ].count(True) >= 2

    def into_the_void_requirement(self, state: CollectionState) -> bool:
        return self.protoss_competent_comp(state) \
            or (
                    self.take_over_ai_allies
                    and (
                        state.has(ItemNames.BATTLECRUISER, self.player)
                    )
                    or (state.has(ItemNames.ULTRALISK, self.player)
                        and self.protoss_competent_anti_air(state))
            )

    def essence_of_eternity_requirement(self, state: CollectionState) -> bool:
        defense_score = self.terran_defense_rating(state, False, True)
        if self.take_over_ai_allies and self.protoss_static_defense(state):
            defense_score += 2
        return defense_score >= 10 \
            and (
                    self.terran_competent_anti_air(state)
                    or self.take_over_ai_allies
                    and self.protoss_competent_anti_air(state)
            ) \
            and (
                    state.has(ItemNames.BATTLECRUISER, self.player)
                    or (state.has(ItemNames.BANSHEE, self.player) and state.has_any({ItemNames.VIKING, ItemNames.VALKYRIE},
                                                                                    self.player))
                    or self.take_over_ai_allies and self.protoss_fleet(state)
            ) \
            and state.has_any({ItemNames.SIEGE_TANK, ItemNames.LIBERATOR}, self.player)

    def amons_fall_requirement(self, state: CollectionState) -> bool:
        if self.take_over_ai_allies:
            return (
                    (
                        state.has_any({ItemNames.BATTLECRUISER, ItemNames.CARRIER}, self.player)
                    )
                    or (state.has(ItemNames.ULTRALISK, self.player)
                        and self.protoss_competent_anti_air(state)
                        and (
                                state.has_any({ItemNames.LIBERATOR, ItemNames.BANSHEE, ItemNames.VALKYRIE, ItemNames.VIKING}, self.player)
                                or state.has_all({ItemNames.WRAITH, ItemNames.WRAITH_ADVANCED_LASER_TECHNOLOGY}, self.player)
                                or self.protoss_fleet(state)
                        )
                        and (self.terran_sustainable_mech_heal(state)
                             or (self.spear_of_adun_autonomously_cast_presence == SpearOfAdunAutonomouslyCastAbilityPresence.option_everywhere
                                 and state.has(ItemNames.RECONSTRUCTION_BEAM, self.player))
                             )
                        )
            ) \
                and self.terran_competent_anti_air(state) \
                and self.protoss_competent_comp(state) \
                and self.zerg_competent_comp(state)
        else:
            return state.has(ItemNames.MUTALISK, self.player) and self.zerg_competent_comp(state)

    def __init__(self, multiworld: MultiWorld, player: int):
        self.multiworld = multiworld
        self.player = player
        self.logic_level = get_option_value(multiworld, self.player, 'required_tactics')
        self.advanced_tactics = self.logic_level != RequiredTactics.option_standard
        self.take_over_ai_allies = get_option_value(multiworld, self.player, "take_over_ai_allies") == TakeOverAIAllies.option_true
        self.kerrigan_unit_available = get_option_value(multiworld, self.player, 'kerrigan_presence') in kerrigan_unit_available
        self.story_tech_granted = get_option_value(multiworld, self.player, "grant_story_tech") == GrantStoryTech.option_true
        self.basic_terran_units = get_basic_units(self.multiworld, self.player, SC2Race.TERRAN)
        self.basic_zerg_units = get_basic_units(self.multiworld, self.player, SC2Race.ZERG)
        self.basic_protoss_units = get_basic_units(self.multiworld, self.player, SC2Race.PROTOSS)
        self.spear_of_adun_autonomously_cast_presence = get_option_value(multiworld, player, "spear_of_adun_autonomously_cast_ability_presence")
