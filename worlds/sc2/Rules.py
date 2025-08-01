from typing import Set

from BaseClasses import  CollectionState
from .Options import get_option_value, RequiredTactics, kerrigan_unit_available, AllInMap, \
    GrantStoryTech, GrantStoryLevels, TakeOverAIAllies, SpearOfAdunAutonomouslyCastAbilityPresence, \
    get_enabled_campaigns, MissionOrder
from .Items import get_basic_units, defense_ratings, zerg_defense_ratings, kerrigan_actives, air_defense_ratings, \
    kerrigan_levels, get_full_item_list
from .MissionTables import SC2Race, SC2Campaign
from . import ItemNames
from worlds.AutoWorld import World


class SC2Logic:

    def lock_any_item(self, state: CollectionState, items: Set[str]) -> bool:
        """
        Guarantees that at least one of these items will remain in the world. Doesn't affect placement.
        Needed for cases when the dynamic pool filtering could remove all the item prerequisites
        :param state:
        :param items:
        :return:
        """
        return self.is_item_placement(state) \
            or state.has_any(items, self.player)

    def is_item_placement(self, state):
        """
        Tells if it's item placement or item pool filter
        :param state:
        :return: True for item placement, False for pool filter
        """
        # has_group with count = 0 is always true for item placement and always false for SC2 item filtering
        return state.has_group("Missions", self.player, 0)

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

        # General enemy-based rules
        if zerg_enemy:
            defense_score += sum((zerg_defense_ratings[item] for item in zerg_defense_ratings if state.has(item, self.player)))
        if air_enemy:
            defense_score += sum((air_defense_ratings[item] for item in air_defense_ratings if state.has(item, self.player)))
        if air_enemy and zerg_enemy and state.has(ItemNames.VALKYRIE, self.player):
            # Valkyries shred mass Mutas, most common air enemy that's massed in these cases
            defense_score += 2
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

    def great_train_robbery_train_stopper(self, state: CollectionState) -> bool:
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
            or (self.advanced_tactics
                and ((state.has_all({ItemNames.RAVEN, ItemNames.RAVEN_HUNTER_SEEKER_WEAPON}, self.player)
                      or self.can_nuke(state))
                     and (
                             state.has_all({ItemNames.VIKING, ItemNames.VIKING_SHREDDER_ROUNDS}, self.player)
                             or state.has_all({ItemNames.BANSHEE, ItemNames.BANSHEE_SHOCKWAVE_MISSILE_BATTERY}, self.player))
                     )
                )

    def terran_mobile_detector(self, state: CollectionState) -> bool:
        return state.has_any({ItemNames.RAVEN, ItemNames.SCIENCE_VESSEL, ItemNames.PROGRESSIVE_ORBITAL_COMMAND}, self.player)

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

    def engine_of_destruction_requirement(self, state: CollectionState):
        return self.marine_medic_upgrade(state) \
        and (
                self.terran_competent_anti_air(state)
                and self.terran_common_unit(state) or state.has(ItemNames.WRAITH, self.player)
        )

    def all_in_requirement(self, state: CollectionState):
        """
        All-in
        :param state:
        :return:
        """
        beats_kerrigan = state.has_any({ItemNames.MARINE, ItemNames.BANSHEE, ItemNames.GHOST}, self.player) or self.advanced_tactics
        if get_option_value(self.world, 'all_in_map') == AllInMap.option_ground:
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
        return state.has_any({ItemNames.HYDRALISK, ItemNames.MUTALISK, ItemNames.CORRUPTOR, ItemNames.BROOD_QUEEN}, self.player) \
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
                       or advanced and (state.has_any({ItemNames.INFESTOR, ItemNames.DEFILER}, self.player) or self.morph_viper(state))
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
            or state.has_any({ItemNames.ZERGLING, ItemNames.HYDRALISK, ItemNames.ROACH}, self.player) \
            or (self.advanced_tactics and state.has(ItemNames.INFESTOR, self.player))

    def supreme_requirement(self, state: CollectionState) -> bool:
        return self.story_tech_granted \
            or not self.kerrigan_unit_available \
            or (
                state.has_all({ItemNames.KERRIGAN_LEAPING_STRIKE, ItemNames.KERRIGAN_MEND}, self.player)
                and self.kerrigan_levels(state, 35)
            )

    def kerrigan_levels(self, state: CollectionState, target: int) -> bool:
        if self.story_levels_granted or not self.kerrigan_unit_available:
            return True  # Levels are granted
        if self.kerrigan_levels_per_mission_completed > 0 \
           and self.kerrigan_levels_per_mission_completed_cap > 0 \
           and not self.is_item_placement(state):
            # Levels can be granted from mission completion.
            # Item pool filtering isn't aware of missions beaten. Assume that missions beaten will fulfill this rule.
            return True
        # Levels from missions beaten
        levels = self.kerrigan_levels_per_mission_completed * state.count_group("Missions", self.player)
        if self.kerrigan_levels_per_mission_completed_cap != -1:
            levels = min(levels, self.kerrigan_levels_per_mission_completed_cap)
        # Levels from items
        for kerrigan_level_item in kerrigan_levels:
            level_amount = get_full_item_list()[kerrigan_level_item].number
            item_count = state.count(kerrigan_level_item, self.player)
            levels += item_count * level_amount
        # Total level cap
        if self.kerrigan_total_level_cap != -1:
            levels = min(levels, self.kerrigan_total_level_cap)

        return levels >= target


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
                and self.kerrigan_levels(state, 70)
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

    def protoss_stalker_upgrade(self, state: CollectionState) -> bool:
        return (
                state.has_any(
                    {
                        ItemNames.STALKER_INSTIGATOR_SLAYER_DISINTEGRATING_PARTICLES,
                        ItemNames.STALKER_INSTIGATOR_SLAYER_PARTICLE_REFLECTION
                    }, self.player)
                and self.lock_any_item(state, {ItemNames.STALKER, ItemNames.INSTIGATOR, ItemNames.SLAYER})
        )

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
                            or (
                                    state.has(ItemNames.ULTRALISK, self.player)
                                    and self.protoss_competent_anti_air(state)
                            )
                    )
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

    def nova_any_weapon(self, state: CollectionState) -> bool:
        return state.has_any(
            {ItemNames.NOVA_C20A_CANISTER_RIFLE, ItemNames.NOVA_HELLFIRE_SHOTGUN, ItemNames.NOVA_PLASMA_RIFLE,
             ItemNames.NOVA_MONOMOLECULAR_BLADE, ItemNames.NOVA_BLAZEFIRE_GUNBLADE}, self.player)

    def nova_ranged_weapon(self, state: CollectionState) -> bool:
        return state.has_any(
            {ItemNames.NOVA_C20A_CANISTER_RIFLE, ItemNames.NOVA_HELLFIRE_SHOTGUN, ItemNames.NOVA_PLASMA_RIFLE},
            self.player)

    def nova_splash(self, state: CollectionState) -> bool:
        return state.has_any({
            ItemNames.NOVA_HELLFIRE_SHOTGUN, ItemNames.NOVA_BLAZEFIRE_GUNBLADE, ItemNames.NOVA_PULSE_GRENADES
        }, self.player) \
            or self.advanced_tactics and state.has_any(
                {ItemNames.NOVA_PLASMA_RIFLE, ItemNames.NOVA_MONOMOLECULAR_BLADE}, self.player)

    def nova_dash(self, state: CollectionState) -> bool:
        return state.has_any({ItemNames.NOVA_MONOMOLECULAR_BLADE, ItemNames.NOVA_BLINK}, self.player)

    def nova_full_stealth(self, state: CollectionState) -> bool:
        return state.count(ItemNames.NOVA_PROGRESSIVE_STEALTH_SUIT_MODULE, self.player) >= 2

    def nova_heal(self, state: CollectionState) -> bool:
        return state.has_any({ItemNames.NOVA_ARMORED_SUIT_MODULE, ItemNames.NOVA_STIM_INFUSION}, self.player)

    def nova_escape_assist(self, state: CollectionState) -> bool:
        return state.has_any({ItemNames.NOVA_BLINK, ItemNames.NOVA_HOLO_DECOY, ItemNames.NOVA_IONIC_FORCE_FIELD}, self.player)

    def the_escape_stuff_granted(self) -> bool:
        """
        The NCO first mission requires having too much stuff first before actually able to do anything
        :return:
        """
        return self.story_tech_granted \
            or (self.mission_order == MissionOrder.option_vanilla and self.enabled_campaigns == {SC2Campaign.NCO})

    def the_escape_first_stage_requirement(self, state: CollectionState) -> bool:
        return self.the_escape_stuff_granted() \
            or (self.nova_ranged_weapon(state) and (self.nova_full_stealth(state) or self.nova_heal(state)))

    def the_escape_requirement(self, state: CollectionState) -> bool:
        return self.the_escape_first_stage_requirement(state) \
            and (self.the_escape_stuff_granted() or self.nova_splash(state))

    def terran_cliffjumper(self, state: CollectionState) -> bool:
        return state.has(ItemNames.REAPER, self.player) \
                or state.has_all({ItemNames.GOLIATH, ItemNames.GOLIATH_JUMP_JETS}, self.player) \
                or state.has_all({ItemNames.SIEGE_TANK, ItemNames.SIEGE_TANK_JUMP_JETS}, self.player)

    def terran_able_to_snipe_defiler(self, state: CollectionState) -> bool:
        return state.has_all({ItemNames.NOVA_JUMP_SUIT_MODULE, ItemNames.NOVA_C20A_CANISTER_RIFLE}, self.player) \
                or state.has_all({ItemNames.SIEGE_TANK, ItemNames.SIEGE_TANK_MAELSTROM_ROUNDS, ItemNames.SIEGE_TANK_JUMP_JETS}, self.player)

    def sudden_strike_requirement(self, state: CollectionState) -> bool:
        return self.sudden_strike_can_reach_objectives(state) \
            and self.terran_able_to_snipe_defiler(state) \
            and state.has_any({ItemNames.SIEGE_TANK, ItemNames.VULTURE}, self.player) \
            and self.nova_splash(state) \
            and (self.terran_defense_rating(state, True, False) >= 2
                 or state.has(ItemNames.NOVA_JUMP_SUIT_MODULE, self.player))

    def sudden_strike_can_reach_objectives(self, state: CollectionState) -> bool:
        return self.terran_cliffjumper(state) \
            or state.has_any({ItemNames.BANSHEE, ItemNames.VIKING}, self.player) \
            or (
                    self.advanced_tactics
                    and state.has(ItemNames.MEDIVAC, self.player)
                    and state.has_any({ItemNames.MARINE, ItemNames.MARAUDER, ItemNames.VULTURE, ItemNames.HELLION,
                                       ItemNames.GOLIATH}, self.player)
            )

    def enemy_intelligence_garrisonable_unit(self, state: CollectionState) -> bool:
        """
        Has unit usable as a Garrison in Enemy Intelligence
        :param state:
        :return:
        """
        return state.has_any(
            {ItemNames.MARINE, ItemNames.REAPER, ItemNames.MARAUDER, ItemNames.GHOST, ItemNames.SPECTRE,
             ItemNames.HELLION, ItemNames.GOLIATH, ItemNames.WARHOUND, ItemNames.DIAMONDBACK, ItemNames.VIKING},
            self.player)

    def enemy_intelligence_cliff_garrison(self, state: CollectionState) -> bool:
        return state.has_any({ItemNames.REAPER, ItemNames.VIKING, ItemNames.MEDIVAC, ItemNames.HERCULES}, self.player) \
            or state.has_all({ItemNames.GOLIATH, ItemNames.GOLIATH_JUMP_JETS}, self.player) \
            or self.advanced_tactics and state.has_any({ItemNames.HELS_ANGELS, ItemNames.BRYNHILDS}, self.player)

    def enemy_intelligence_first_stage_requirement(self, state: CollectionState) -> bool:
        return self.enemy_intelligence_garrisonable_unit(state) \
            and (self.terran_competent_comp(state)
                 or (
                         self.terran_common_unit(state)
                         and self.terran_competent_anti_air(state)
                         and state.has(ItemNames.NOVA_NUKE, self.player)
                 )
                 ) \
            and self.terran_defense_rating(state, True, True) >= 5

    def enemy_intelligence_second_stage_requirement(self, state: CollectionState) -> bool:
        return self.enemy_intelligence_first_stage_requirement(state) \
            and self.enemy_intelligence_cliff_garrison(state) \
            and (
                    self.story_tech_granted
                    or (
                            self.nova_any_weapon(state)
                            and (
                                    self.nova_full_stealth(state)
                                    or (self.nova_heal(state)
                                        and self.nova_splash(state)
                                        and self.nova_ranged_weapon(state))
                            )
                    )
            )

    def enemy_intelligence_third_stage_requirement(self, state: CollectionState) -> bool:
        return self.enemy_intelligence_second_stage_requirement(state) \
            and (
                    self.story_tech_granted
                    or (
                            state.has(ItemNames.NOVA_PROGRESSIVE_STEALTH_SUIT_MODULE, self.player)
                            and self.nova_dash(state)
                    )
            )

    def trouble_in_paradise_requirement(self, state: CollectionState) -> bool:
        return self.nova_any_weapon(state) \
            and self.nova_splash(state) \
            and self.terran_beats_protoss_deathball(state) \
            and self.terran_defense_rating(state, True, True) >= 7

    def night_terrors_requirement(self, state: CollectionState) -> bool:
        return self.terran_common_unit(state) \
            and self.terran_competent_anti_air(state) \
            and (
                # These can handle the waves of infested, even volatile ones
                    state.has(ItemNames.SIEGE_TANK, self.player)
                    or state.has_all({ItemNames.VIKING, ItemNames.VIKING_SHREDDER_ROUNDS}, self.player)
                    or (
                            (
                                # Regular infesteds
                                    state.has(ItemNames.FIREBAT, self.player)
                                    or state.has_all({ItemNames.HELLION, ItemNames.HELLION_HELLBAT_ASPECT}, self.player)
                                    or (
                                            self.advanced_tactics
                                            and state.has_any({ItemNames.PERDITION_TURRET, ItemNames.PLANETARY_FORTRESS}, self.player)
                                    )
                            )
                            and self.terran_bio_heal(state)
                            and (
                                # Volatile infesteds
                                    state.has(ItemNames.LIBERATOR, self.player)
                                    or (
                                            self.advanced_tactics
                                            and state.has_any({ItemNames.HERC, ItemNames.VULTURE}, self.player)
                                    )
                            )
                    )
            )

    def flashpoint_far_requirement(self, state: CollectionState) -> bool:
        return self.terran_competent_comp(state) \
            and self.terran_mobile_detector(state) \
            and self.terran_defense_rating(state, True, False) >= 6

    def enemy_shadow_tripwires_tool(self, state: CollectionState) -> bool:
        return state.has_any({ItemNames.NOVA_FLASHBANG_GRENADES, ItemNames.NOVA_BLINK, ItemNames.NOVA_DOMINATION},
                             self.player)

    def enemy_shadow_door_unlocks_tool(self, state: CollectionState) -> bool:
        return state.has_any({ItemNames.NOVA_DOMINATION, ItemNames.NOVA_BLINK, ItemNames.NOVA_JUMP_SUIT_MODULE},
                             self.player)

    def enemy_shadow_domination(self, state: CollectionState) -> bool:
        return self.story_tech_granted \
            or (self.nova_ranged_weapon(state)
                and (self.nova_full_stealth(state)
                     or state.has(ItemNames.NOVA_JUMP_SUIT_MODULE, self.player)
                     or (self.nova_heal(state) and self.nova_splash(state))
                     )
                )

    def enemy_shadow_first_stage(self, state: CollectionState) -> bool:
        return self.enemy_shadow_domination(state) \
            and (self.story_tech_granted
                 or ((self.nova_full_stealth(state) and self.enemy_shadow_tripwires_tool(state))
                     or (self.nova_heal(state) and self.nova_splash(state))
                     )
                 )

    def enemy_shadow_second_stage(self, state: CollectionState) -> bool:
        return self.enemy_shadow_first_stage(state) \
            and (self.story_tech_granted
                 or self.nova_splash(state)
                 or self.nova_heal(state)
                 or self.nova_escape_assist(state)
                 )

    def enemy_shadow_door_controls(self, state: CollectionState) -> bool:
        return self.enemy_shadow_second_stage(state) \
            and (self.story_tech_granted or self.enemy_shadow_door_unlocks_tool(state))

    def enemy_shadow_victory(self, state: CollectionState) -> bool:
        return self.enemy_shadow_door_controls(state) \
            and (self.story_tech_granted or self.nova_heal(state))

    def dark_skies_requirement(self, state: CollectionState) -> bool:
        return self.terran_common_unit(state) \
            and self.terran_beats_protoss_deathball(state) \
            and self.terran_defense_rating(state, False, True) >= 8

    def end_game_requirement(self, state: CollectionState) -> bool:
        return self.terran_competent_comp(state) \
            and self.terran_mobile_detector(state) \
            and (
                    state.has_any({ItemNames.BATTLECRUISER, ItemNames.LIBERATOR, ItemNames.BANSHEE}, self.player)
                    or state.has_all({ItemNames.WRAITH, ItemNames.WRAITH_ADVANCED_LASER_TECHNOLOGY}, self.player)
            ) \
            and (state.has_any({ItemNames.BATTLECRUISER, ItemNames.VIKING, ItemNames.LIBERATOR}, self.player)
                 or (self.advanced_tactics
                     and state.has_all({ItemNames.RAVEN, ItemNames.RAVEN_HUNTER_SEEKER_WEAPON}, self.player)
                     )
                 )

    def __init__(self, world: World):
        self.world: World = world
        self.player = None if world is None else world.player
        self.logic_level = get_option_value(world, 'required_tactics')
        self.advanced_tactics = self.logic_level != RequiredTactics.option_standard
        self.take_over_ai_allies = get_option_value(world, "take_over_ai_allies") == TakeOverAIAllies.option_true
        self.kerrigan_unit_available = get_option_value(world, 'kerrigan_presence') in kerrigan_unit_available \
            and SC2Campaign.HOTS in get_enabled_campaigns(world)
        self.kerrigan_levels_per_mission_completed = get_option_value(world, "kerrigan_levels_per_mission_completed")
        self.kerrigan_levels_per_mission_completed_cap = get_option_value(world, "kerrigan_levels_per_mission_completed_cap")
        self.kerrigan_total_level_cap = get_option_value(world, "kerrigan_total_level_cap")
        self.story_tech_granted = get_option_value(world, "grant_story_tech") == GrantStoryTech.option_true
        self.story_levels_granted = get_option_value(world, "grant_story_levels") != GrantStoryLevels.option_disabled
        self.basic_terran_units = get_basic_units(world, SC2Race.TERRAN)
        self.basic_zerg_units = get_basic_units(world, SC2Race.ZERG)
        self.basic_protoss_units = get_basic_units(world, SC2Race.PROTOSS)
        self.spear_of_adun_autonomously_cast_presence = get_option_value(world, "spear_of_adun_autonomously_cast_ability_presence")
        self.enabled_campaigns = get_enabled_campaigns(world)
        self.mission_order = get_option_value(world, "mission_order")
