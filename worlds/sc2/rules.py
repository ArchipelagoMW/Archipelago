from math import floor
from typing import TYPE_CHECKING, Set, Optional, Callable

from BaseClasses import CollectionState, Location
from .options import (
    get_option_value, RequiredTactics, kerrigan_unit_available, AllInMap,
    GrantStoryTech, GrantStoryLevels, SpearOfAdunAutonomouslyCastAbilityPresence,
    get_enabled_campaigns, MissionOrder, EnableMorphling, get_enabled_races
)
from .item.item_tables import (
    tvx_defense_ratings, tvz_defense_ratings, kerrigan_actives, tvx_air_defense_ratings,
    kerrigan_levels, get_full_item_list, zvx_air_defense_ratings, zvx_defense_ratings, pvx_defense_ratings,
    pvz_defense_ratings, no_logic_basic_units, advanced_basic_units, basic_units, upgrade_bundle_inverted_lookup, WEAPON_ARMOR_UPGRADE_MAX_LEVEL
)
from .mission_tables import SC2Race, SC2Campaign
from .item import item_groups, item_names

if TYPE_CHECKING:
    from . import SC2World


class SC2Logic:

    def is_item_placement(self, state: CollectionState):
        """
        Tells if it's item placement or item pool filter
        :return: True for item placement, False for pool filter
        """
        # has_group with count = 0 is always true for item placement and always false for SC2 item filtering
        return state.has_group("Missions", self.player, 0)

    # Needs to react on how many missions actually got generated
    def total_mission_count(self):
        return (
            1 if (self.world is None or not hasattr(self.world, 'custom_mission_order'))
            else self.world.custom_mission_order.get_mission_count()
        )

    # Unit classes in world, these are set properly into the world after the item culling is done
    # Therefore need to get from the world
    def world_has_barracks_unit(self):
        return self.world is not None and self.world.has_barracks_unit

    def world_has_factory_unit(self):
        return self.world is not None and self.world.has_factory_unit

    def world_has_starport_unit(self):
        return self.world is not None and self.world.has_starport_unit

    def world_has_zerg_melee_unit(self):
        return self.world is not None and self.world.has_zerg_melee_unit

    def world_has_zerg_ranged_unit(self):
        return self.world is not None and self.world.has_zerg_ranged_unit

    def world_has_zerg_air_unit(self):
        return self.world is not None and self.world.has_zerg_air_unit

    def world_has_protoss_ground_unit(self):
        return self.world is not None and self.world.has_protoss_ground_unit

    def world_has_protoss_air_unit(self):
        return self.world is not None and self.world.has_protoss_air_unit

    def get_very_hard_required_upgrade_level(self):
        return 2 if self.advanced_tactics else 3

    def weapon_armor_upgrade_count(self, upgrade_item: str, state: CollectionState) -> int:
        assert upgrade_item in upgrade_bundle_inverted_lookup.keys()
        count: int = 0
        if self.generic_upgrade_missions > 0:
            if (not self.is_item_placement(state)) or self.logic_level == RequiredTactics.option_no_logic:
                # Item pool filtering, W/A upgrades aren't items
                # No Logic: Don't care about W/A in this case
                return WEAPON_ARMOR_UPGRADE_MAX_LEVEL
            else:
                count += floor(
                    (100 / self.generic_upgrade_missions)
                    * (state.count_group("Missions", self.player) / self.total_mission_count())
                )
        count += state.count(upgrade_item, self.player)
        count += state.count_from_list(upgrade_bundle_inverted_lookup[upgrade_item], self.player)
        if upgrade_item == item_names.PROGRESSIVE_PROTOSS_SHIELDS:
            count += max(
                state.count(item_names.PROGRESSIVE_PROTOSS_GROUND_UPGRADE, self.player),
                state.count(item_names.PROGRESSIVE_PROTOSS_AIR_UPGRADE, self.player)
            )
        if (
                upgrade_item in item_groups.protoss_generic_upgrades
                and state.has(item_names.QUATRO, self.player)
        ):
            count += 1
        return count

    def terran_army_weapon_armor_upgrade_min_level(self, state: CollectionState) -> int:
        """
        Minimum W/A upgrade level for unit classes present in the world
        """
        count: int = WEAPON_ARMOR_UPGRADE_MAX_LEVEL
        if self.world_has_barracks_unit():
            count = min(
                count,
                self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_TERRAN_INFANTRY_WEAPON, state),
                self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_TERRAN_INFANTRY_ARMOR, state)
            )
        if self.world_has_factory_unit():
            count = min(
                count,
                self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_TERRAN_VEHICLE_WEAPON, state),
                self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_TERRAN_VEHICLE_ARMOR, state)
            )
        if self.world_has_starport_unit():
            count = min(
                count,
                self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_TERRAN_SHIP_WEAPON, state),
                self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_TERRAN_SHIP_ARMOR, state)
            )
        return count

    def terran_very_hard_mission_weapon_armor_level(self, state: CollectionState) -> bool:
        return self.terran_army_weapon_armor_upgrade_min_level(state) >= self.get_very_hard_required_upgrade_level()

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
                state.has_any({
                    item_names.MARINE, item_names.DOMINION_TROOPER, item_names.FIREBAT, item_names.MARAUDER,
                    item_names.REAPER, item_names.HELLION
                }, self.player)
                or (self.advanced_tactics and state.has_any({item_names.GOLIATH, item_names.DIAMONDBACK, item_names.VIKING, item_names.BANSHEE}, self.player))
        )

    def terran_air(self, state: CollectionState) -> bool:
        """
        Air units or drops on advanced tactics
        """
        return (
                state.has_any({
                    item_names.VIKING, item_names.WRAITH, item_names.BANSHEE, item_names.BATTLECRUISER
                }, self.player)
                or (
                        self.advanced_tactics
                        and state.has_any({item_names.HERCULES, item_names.MEDIVAC}, self.player)
                        and self.terran_common_unit(state)
                )
        )

    def terran_air_anti_air(self, state: CollectionState) -> bool:
        """
        Air-to-air
        """
        return (
            state.has(item_names.VIKING, self.player)
            or state.has_all({item_names.WRAITH, item_names.WRAITH_ADVANCED_LASER_TECHNOLOGY}, self.player)
            or state.has_all({item_names.BATTLECRUISER, item_names.BATTLECRUISER_ATX_LASER_BATTERY}, self.player)
            or (
                    self.advanced_tactics
                    and state.has_any({item_names.WRAITH, item_names.VALKYRIE, item_names.BATTLECRUISER}, self.player)
                    and self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_TERRAN_SHIP_WEAPON, state) >= 2
            )
        )

    def terran_any_air_unit(self, state: CollectionState) -> bool:
        return state.has_any({
            item_names.VIKING, item_names.MEDIVAC, item_names.RAVEN, item_names.BANSHEE, item_names.SCIENCE_VESSEL,
            item_names.BATTLECRUISER, item_names.WRAITH, item_names.HERCULES, item_names.LIBERATOR, item_names.VALKYRIE,
            item_names.SKY_FURY, item_names.NIGHT_HAWK, item_names.EMPERORS_GUARDIAN, item_names.NIGHT_WOLF,
            item_names.PRIDE_OF_AUGUSTRGRAD
        }, self.player)

    def terran_competent_ground_to_air(self, state: CollectionState) -> bool:
        """
        Ground-to-air
        """
        return (
            state.has(item_names.GOLIATH, self.player)
            or (
                    state.has_any({item_names.MARINE, item_names.DOMINION_TROOPER}, self.player)
                    and self.terran_bio_heal(state)
                    and self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_TERRAN_INFANTRY_WEAPON, state) >= 2
            )
            or self.advanced_tactics and state.has(item_names.CYCLONE, self.player)
        )

    def terran_competent_anti_air(self, state: CollectionState) -> bool:
        """
        Good AA unit
        """
        return (
            self.terran_competent_ground_to_air(state)
            or self.terran_air_anti_air(state)
        )
    
    def terran_outbreak_requirement(self, state: CollectionState) -> bool:
        """Outbreak mission requirement"""
        return (
            self.terran_defense_rating(state, True, False) >= 4
            and (self.terran_common_unit(state) or state.has(item_names.REAPER, self.player))
        )

    def terran_safe_haven_requirement(self, state: CollectionState) -> bool:
        """Safe Haven mission requirement"""
        return (
            self.terran_common_unit(state)
            and self.terran_competent_anti_air(state)
        )

    def terran_gates_of_hell_requirement(self, state: CollectionState) -> bool:
        """Gates of Hell mission requirement"""
        return (
            self.terran_competent_comp(state)
            and (self.terran_defense_rating(state, True) > 6)
        )

    def zerg_gates_of_hell_requirement(self, state: CollectionState) -> bool:
        """Gates of Hell mission requirement"""
        return (
            self.zerg_competent_comp_competent_aa(state)
            and (self.zerg_defense_rating(state, True) > 8)
        )

    def protoss_gates_of_hell_requirement(self, state: CollectionState) -> bool:
        """Gates of Hell mission requirement"""
        return (
            self.protoss_competent_comp(state)
            and (self.protoss_defense_rating(state, True) > 6)
            and (self.advanced_tactics or state.has(item_names.PROGRESSIVE_WARP_RELOCATE, self.player))
        )

    def welcome_to_the_jungle_requirement(self, state: CollectionState) -> bool:
        """
        Welcome to the Jungle requirements - able to deal with Scouts, Void Rays, Zealots and Stalkers
        """
        return (
            self.terran_common_unit(state)
            and self.terran_competent_ground_to_air(state)
        ) or (
            self.advanced_tactics
            and state.has_any({item_names.MARINE, item_names.DOMINION_TROOPER, item_names.VULTURE}, self.player)
            and self.terran_air_anti_air(state)
        )

    def welcome_to_the_jungle_z_requirement(self, state: CollectionState) -> bool:
        """
        Welcome to the Jungle requirements - able to deal with Scouts, Void Rays, Zealots and Stalkers
        """
        return (
                self.zerg_competent_comp(state) and state.has_any({item_names.HYDRALISK, item_names.MUTALISK}, self.player)
        ) or (
                self.advanced_tactics
                and self.zerg_common_unit(state)
                and (state.has_any({item_names.MUTALISK, item_names.INFESTOR}, self.player)
                 or (self.morph_devourer(state) and state.has_any({item_names.HYDRALISK, item_names.SWARM_QUEEN}, self.player))
                 or (self.morph_viper(state) and state.has(item_names.VIPER_PARASITIC_BOMB, self.player))
                 )
                and self.zerg_army_weapon_armor_upgrade_min_level(state) >= 1
        )

    def welcome_to_the_jungle_p_requirement(self, state: CollectionState) -> bool:
        """
        Welcome to the Jungle requirements - able to deal with Scouts, Void Rays, Zealots and Stalkers
        """
        return (
            self.protoss_common_unit(state) and self.protoss_competent_anti_air(state)
            or (
                self.advanced_tactics
                and self.protoss_common_unit_anti_light_air(state)
                and (self.protoss_anti_armor_anti_air(state)
                    or state.has_any((item_names.HIGH_TEMPLAR, item_names.SIGNIFIER, item_names.ASCENDANT), self.player)
                    or state.has_all((item_names.DISRUPTOR, item_names.DISRUPTOR_PERFECTED_POWER), self.player)
                )
            )
        )

    def terran_basic_anti_air(self, state: CollectionState) -> bool:
        """
        Basic AA to deal with few air units
        """
        return (
            state.has_any((
                item_names.MISSILE_TURRET, item_names.THOR, item_names.WAR_PIGS, item_names.SPARTAN_COMPANY,
                item_names.HELS_ANGELS, item_names.BATTLECRUISER, item_names.MARINE, item_names.WRAITH,
                item_names.VALKYRIE, item_names.CYCLONE, item_names.WINGED_NIGHTMARES, item_names.BRYNHILDS,
                item_names.SKY_FURY, item_names.DOMINION_TROOPER, item_names.SON_OF_KORHAL, item_names.BULWARK_COMPANY
            ), self.player)
            or self.terran_competent_anti_air(state)
            or self.advanced_tactics and (
                state.has_any((
                    item_names.GHOST, item_names.SPECTRE, item_names.WIDOW_MINE, item_names.LIBERATOR,
                    item_names.PRIDE_OF_AUGUSTRGRAD, item_names.BLACKHAMMER, item_names.EMPERORS_SHADOW,
                    item_names.EMPERORS_GUARDIAN, item_names.NIGHT_HAWK,
                ), self.player)
                or (
                        state.has(item_names.MEDIVAC, self.player)
                        and state.has_any((item_names.SIEGE_TANK, item_names.SHOCK_DIVISION), self.player)
                        and state.count(item_names.SIEGE_TANK_PROGRESSIVE_TRANSPORT_HOOK, self.player) >= 2
                )
            )
        )

    def terran_defense_rating(self, state: CollectionState, zerg_enemy: bool, air_enemy: bool = True) -> int:
        """
        Ability to handle defensive missions
        :param state:
        :param zerg_enemy: Whether the enemy is zerg
        :param air_enemy: Whether the enemy attacks with air
        :return:
        """
        defense_score = sum((tvx_defense_ratings[item] for item in tvx_defense_ratings if state.has(item, self.player)))
        # Manned Bunker
        if state.has_any({item_names.MARINE, item_names.DOMINION_TROOPER, item_names.MARAUDER}, self.player) and state.has(
                item_names.BUNKER, self.player):
            defense_score += 3
        elif zerg_enemy and state.has(item_names.FIREBAT, self.player) and state.has(item_names.BUNKER, self.player):
            defense_score += 2
        # Siege Tank upgrades
        if state.has_all({item_names.SIEGE_TANK, item_names.SIEGE_TANK_MAELSTROM_ROUNDS}, self.player):
            defense_score += 2
        if state.has_all({item_names.SIEGE_TANK, item_names.SIEGE_TANK_GRADUATING_RANGE}, self.player):
            defense_score += 1
        # Widow Mine upgrade
        if state.has_all({item_names.WIDOW_MINE, item_names.WIDOW_MINE_CONCEALMENT}, self.player):
            defense_score += 1
        # Viking with splash
        if state.has_all({item_names.VIKING, item_names.VIKING_SHREDDER_ROUNDS}, self.player):
            defense_score += 2

        # General enemy-based rules
        if zerg_enemy:
            defense_score += sum((tvz_defense_ratings[item] for item in tvz_defense_ratings if state.has(item, self.player)))
        if air_enemy:
            defense_score += sum((tvx_air_defense_ratings[item] for item in tvx_air_defense_ratings if state.has(item, self.player)))
        if air_enemy and zerg_enemy and state.has(item_names.VALKYRIE, self.player):
            # Valkyries shred mass Mutas, most common air enemy that's massed in these cases
            defense_score += 2
        # Advanced Tactics bumps defense rating requirements down by 2
        if self.advanced_tactics:
            defense_score += 2
        return defense_score

    def terran_competent_comp(self, state: CollectionState) -> bool:
        """
        Ability to deal with most of hard missions
        """
        return (
            (
                (
                        state.has_any({item_names.MARINE, item_names.DOMINION_TROOPER, item_names.MARAUDER}, self.player)
                        and self.terran_bio_heal(state)
                        and self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_TERRAN_INFANTRY_WEAPON, state) >= 2
                )
                or state.has_any({item_names.THOR, item_names.BANSHEE, item_names.SIEGE_TANK}, self.player)
                or state.has_all({item_names.LIBERATOR, item_names.LIBERATOR_RAID_ARTILLERY}, self.player)
            )
            and self.terran_competent_anti_air(state)
        ) or (
            state.has(item_names.BATTLECRUISER, self.player)
            and self.terran_common_unit(state)
            and (
                    self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_TERRAN_SHIP_WEAPON, state) >= 2
                    or state.has(item_names.BATTLECRUISER_ATX_LASER_BATTERY, self.player)
            )
        )

    def terran_mineral_dump(self, state: CollectionState) -> bool:
        """
        Can build something using only minerals
        """
        return (
                state.has_any({item_names.MARINE, item_names.VULTURE, item_names.HELLION, item_names.SON_OF_KORHAL},
                              self.player)
                or state.has_all({item_names.REAPER, item_names.REAPER_RESOURCE_EFFICIENCY}, self.player)
                or (
                        self.advanced_tactics
                        and state.has_any({item_names.PERDITION_TURRET, item_names.DEVASTATOR_TURRET}, self.player)
                )
        )

    def terran_can_grab_ghosts_in_the_fog_east_rock_formation(self, state: CollectionState) -> bool:
        """
        Able to shoot by a long range or from air to claim the rock formation separated by a chasm
        """
        return (
                state.has_any({
                    item_names.MEDIVAC, item_names.HERCULES, item_names.VIKING, item_names.BANSHEE,
                    item_names.WRAITH, item_names.SIEGE_TANK, item_names.BATTLECRUISER, item_names.NIGHT_HAWK,
                    item_names.NIGHT_WOLF, item_names.SHOCK_DIVISION, item_names.SKY_FURY
                }, self.player)
                or state.has_all({item_names.VALKYRIE, item_names.VALKYRIE_FLECHETTE_MISSILES}, self.player)
                or state.has_all({item_names.RAVEN, item_names.RAVEN_HUNTER_SEEKER_WEAPON}, self.player)
                or (
                        state.has_any({item_names.LIBERATOR, item_names.EMPERORS_GUARDIAN}, self.player)
                        and state.has(item_names.LIBERATOR_RAID_ARTILLERY, self.player)
                ) or (
                        self.advanced_tactics
                        and (
                            state.has_any({
                                item_names.HELS_ANGELS, item_names.DUSK_WINGS, item_names.WINGED_NIGHTMARES,
                                item_names.SIEGE_BREAKERS, item_names.BRYNHILDS, item_names.JACKSONS_REVENGE
                            }, self.player)
                        )
                        or state.has_all({item_names.MIDNIGHT_RIDERS, item_names.LIBERATOR_RAID_ARTILLERY}, self.player)
                )
        )

    def terran_great_train_robbery_train_stopper(self, state: CollectionState) -> bool:
        """
        Ability to deal with trains (moving target with a lot of HP)
        """
        return (
            state.has_any({item_names.SIEGE_TANK, item_names.DIAMONDBACK, item_names.MARAUDER, item_names.CYCLONE, item_names.BANSHEE}, self.player)
            or (self.advanced_tactics
                and (
                    state.has_all({item_names.REAPER, item_names.REAPER_G4_CLUSTERBOMB}, self.player)
                    or state.has_all({item_names.SPECTRE, item_names.SPECTRE_PSIONIC_LASH}, self.player)
                    or state.has_any({item_names.VULTURE, item_names.LIBERATOR}, self.player)
                )
            )
        )
    
    def zerg_great_train_robbery_train_stopper(self, state: CollectionState) -> bool:
        """
        Ability to deal with trains (moving target with a lot of HP)
        """
        return (
            self.morph_impaler_or_lurker(state)
            or state.has_all({item_names.MUTALISK_SEVERING_GLAIVE, item_names.MUTALISK}, self.player)
            or state.has(item_names.ABERRATION, self.player)
            or (self.advanced_tactics
                and (
                    state.has_all({item_names.ZERGLING_BANELING_ASPECT, item_names.BANELING_CORROSIVE_ACID}, self.player)
                    or state.has_all({item_names.ROACH, item_names.ROACH_GLIAL_RECONSTITUTION}, self.player)
                )
            )
        )

    def protoss_great_train_robbery_train_stopper(self, state: CollectionState) -> bool:
        """
        Ability to deal with trains (moving target with a lot of HP)
        """
        return (
            state.has_any({item_names.ANNIHILATOR, item_names.INSTIGATOR, item_names.STALKER}, self.player)
            or state.has_all({item_names.SLAYER, item_names.SLAYER_PHASE_BLINK}, self.player)
            or (self.advanced_tactics
                and  (
                    state.has_all({item_names.WRATHWALKER, item_names.WRATHWALKER_RAPID_POWER_CYCLING}, self.player)
                    or state.has_all({item_names.VANGUARD, item_names.VANGUARD_RAPIDFIRE_CANNON}, self.player)
                    or (
                        state.has_any({item_names.VOID_RAY, item_names.DAWNBRINGER}, self.player)
                        and state.has_all({item_names.DESTROYER, item_names.DESTROYER_REFORGED_BLOODSHARD_CORE}, self.player)
                    )
                ) 
            )
        )

    def terran_can_rescue(self, state) -> bool:
        """
        Rescuing in The Moebius Factor
        """
        return state.has_any({item_names.MEDIVAC, item_names.HERCULES, item_names.RAVEN, item_names.VIKING}, self.player) or self.advanced_tactics

    def terran_beats_protoss_deathball(self, state: CollectionState) -> bool:
        """
        Ability to deal with Immortals, Colossi with some air support
        """
        return (
            (
                state.has_any({item_names.BANSHEE, item_names.BATTLECRUISER}, self.player)
                or state.has_all({item_names.LIBERATOR, item_names.LIBERATOR_RAID_ARTILLERY}, self.player)
            ) and self.terran_competent_anti_air(state)
            or self.terran_competent_comp(state) and self.terran_air_anti_air(state)
        ) and self.terran_army_weapon_armor_upgrade_min_level(state) >= 2

    def marine_medic_upgrade(self, state: CollectionState) -> bool:
        """
        Infantry upgrade to infantry-only no-build segments
        """
        return (
            state.has_any({
                item_names.MARINE_COMBAT_SHIELD, item_names.MARINE_MAGRAIL_MUNITIONS, item_names.MEDIC_STABILIZER_MEDPACKS
            }, self.player)
            or (state.count(item_names.MARINE_PROGRESSIVE_STIMPACK, self.player) >= 2
                and state.has_group("Missions", self.player, 1)
                )
        )

    def terran_survives_rip_field(self, state: CollectionState) -> bool:
        """
        Ability to deal with large areas with environment damage
        """
        return (
                (
                        state.has(item_names.BATTLECRUISER, self.player)
                        and (self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_TERRAN_SHIP_WEAPON, state) >= 2
                             or state.has(item_names.BATTLECRUISER_ATX_LASER_BATTERY, self.player)
                             )
                )
                or (
                        self.terran_air(state)
                        and self.terran_competent_anti_air(state)
                        and self.terran_sustainable_mech_heal(state))
        )

    def zerg_maw_requirement(self, state: CollectionState) -> bool:
        """
        Ability to cross defended gaps, deal with skytoss, and avoid costly losses.
        """
        return (
                state.has(item_names.SWARM_QUEEN, self.player)
                # Cross the gap
                and (state.has_any((item_names.NYDUS_WORM, item_names.OVERLORD_VENTRAL_SACS), self.player)
                     or (self.advanced_tactics and state.has(item_names.YGGDRASIL, self.player)))
                # Air to ground
                and (self.morph_brood_lord(state) or self.morph_guardian(state))
                # Ground to air
                and (
                    state.has(item_names.INFESTOR, self.player)
                    or self.morph_tyrannozor(state)
                    or state.has_all({item_names.SWARM_HOST, item_names.SWARM_HOST_RESOURCE_EFFICIENCY, item_names.SWARM_HOST_PRESSURIZED_GLANDS}, self.player)
                    or state.has_all({item_names.HYDRALISK, item_names.HYDRALISK_RESOURCE_EFFICIENCY}, self.player)
                    or state.has_all({item_names.INFESTED_DIAMONDBACK, item_names.INFESTED_DIAMONDBACK_PROGRESSIVE_FUNGAL_SNARE}, self.player)
                )
                # Survives rip-field
                and (state.has_any({item_names.ABERRATION, item_names.ROACH, item_names.ULTRALISK}, self.player)
                     or self.morph_tyrannozor(state))
                # Air-to-air
                and (state.has_any({item_names.MUTALISK, item_names.CORRUPTOR, item_names.INFESTED_LIBERATOR, item_names.BROOD_QUEEN}, self.player))
                # Upgrades / general
                and self.zerg_competent_comp(state)
        )

    def protoss_maw_requirement(self, state: CollectionState) -> bool:
        """
        Ability to cross defended gaps and deal with skytoss.
        """
        return (
            (
                state.has(item_names.WARP_PRISM, self.player)
                or (self.advanced_tactics and state.has(item_names.ARBITER, self.player))
            )
            and self.protoss_common_unit_anti_armor_air(state)
            and self.protoss_fleet(state)
        )

    def terran_sustainable_mech_heal(self, state: CollectionState) -> bool:
        """
        Can heal mech units without spending resources
        """
        return (
            state.has(item_names.SCIENCE_VESSEL, self.player)
            or (
                state.has_any({item_names.MEDIC, item_names.FIELD_RESPONSE_THETA}, self.player)
                and state.has(item_names.MEDIC_ADAPTIVE_MEDPACKS, self.player)
            )
            or state.count(item_names.PROGRESSIVE_REGENERATIVE_BIO_STEEL, self.player) >= 3
            or (self.advanced_tactics
                and (
                    state.has_all({item_names.RAVEN, item_names.RAVEN_BIO_MECHANICAL_REPAIR_DRONE}, self.player)
                    or state.count(item_names.PROGRESSIVE_REGENERATIVE_BIO_STEEL, self.player) >= 2
                )
            )
        )

    def terran_bio_heal(self, state: CollectionState) -> bool:
        """
        Ability to heal bio units
        """
        return (
            state.has_any({item_names.MEDIC, item_names.MEDIVAC, item_names.FIELD_RESPONSE_THETA}, self.player)
            or (self.advanced_tactics
                and state.has_all({item_names.RAVEN, item_names.RAVEN_BIO_MECHANICAL_REPAIR_DRONE}, self.player)
            )
        )

    def terran_base_trasher(self, state: CollectionState) -> bool:
        """
        Can attack heavily defended bases
        """
        return (
            state.has(item_names.SIEGE_TANK, self.player)
            or state.has_all({item_names.BATTLECRUISER, item_names.BATTLECRUISER_ATX_LASER_BATTERY}, self.player)
            or state.has_all({item_names.LIBERATOR, item_names.LIBERATOR_RAID_ARTILLERY}, self.player)
            or (self.advanced_tactics
                and (
                    state.has_all({item_names.RAVEN, item_names.RAVEN_HUNTER_SEEKER_WEAPON}, self.player)
                    or self.can_nuke(state)
                )
                and (
                    state.has_all({item_names.VIKING, item_names.VIKING_SHREDDER_ROUNDS}, self.player)
                    or state.has_all({item_names.BANSHEE, item_names.BANSHEE_SHOCKWAVE_MISSILE_BATTERY}, self.player)
                )
            )
        ) and self.terran_very_hard_mission_weapon_armor_level(state)

    def terran_mobile_detector(self, state: CollectionState) -> bool:
        return state.has_any({item_names.RAVEN, item_names.SCIENCE_VESSEL, item_names.COMMAND_CENTER_SCANNER_SWEEP}, self.player)

    def can_nuke(self, state: CollectionState) -> bool:
        """
        Ability to launch nukes
        """
        return (self.advanced_tactics
                and (state.has_any({item_names.GHOST, item_names.SPECTRE}, self.player)
                     or state.has_all({item_names.THOR, item_names.THOR_BUTTON_WITH_A_SKULL_ON_IT}, self.player)))

    def terran_respond_to_colony_infestations(self, state: CollectionState) -> bool:
        """
        Can deal quickly with Brood Lords and Mutas in Haven's Fall and being able to progress the mission
        """
        return (
            self.terran_common_unit(state)
            and self.terran_competent_anti_air(state)
            and (
                    self.terran_air_anti_air(state)
                    or (
                            state.has_any({item_names.BATTLECRUISER, item_names.VALKYRIE}, self.player)
                            and self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_TERRAN_SHIP_WEAPON, state) >= 2
                    )
                )
            and self.terran_defense_rating(state, True) >= 3
        )

    def terran_engine_of_destruction_requirement(self, state: CollectionState):
        return (
            self.marine_medic_upgrade(state)
            and (state.has(item_names.WRAITH, self.player)
                or (
                    self.terran_competent_anti_air(state)
                    and self.terran_common_unit(state)
                )
            )
        )

    def zerg_engine_of_destruction_requirement(self, state: CollectionState):
        return (
            self.zergling_hydra_roach_start(state)
            and self.zerg_repair_odin(state)
            and (
                    self.zerg_competent_anti_air(state)
                    and self.zerg_common_unit(state)
                )

        )


    def protoss_engine_of_destruction_requirement(self, state: CollectionState):
        return (
            self.zealot_sentry_slayer_start(state)
            and self.protoss_repair_odin(state)
            and (
                    self.protoss_competent_anti_air(state)
                    and self.protoss_common_unit(state)
                )
        )

    def zerg_repair_odin(self, state: CollectionState):
        return (
            state.has_all({item_names.SWARM_QUEEN_BIO_MECHANICAL_TRANSFUSION, item_names.SWARM_QUEEN}, self.player)
            or (self.advanced_tactics
                and state.has(item_names.SWARM_QUEEN, self.player)
            )   
        )

    def protoss_repair_odin(self, state: CollectionState):
        return (
            state.has(item_names.SENTRY, self.player)
            or (self.advanced_tactics
                and state.has(item_names.SHIELD_BATTERY, self.player)
            )   
        )

    def zergling_hydra_roach_start(self, state: CollectionState):
        """
        Created mainly for engine of destruction start, but works for other missions with no-build starts.
        """
        return (
            state.has_any({item_names.ZERGLING_ADRENAL_OVERLOAD, item_names.HYDRALISK_FRENZY, item_names.ROACH_HYDRIODIC_BILE}, self.player)
        )

    def zealot_sentry_slayer_start(self, state: CollectionState):
        """
        Created mainly for engine of destruction start, but works for other missions with no-build starts.
        """
        return (
            state.has_any({item_names.ZEALOT_WHIRLWIND, item_names.SENTRY_DOUBLE_SHIELD_RECHARGE, item_names.SLAYER_PHASE_BLINK}, self.player)
        )

    def all_in_requirement(self, state: CollectionState):
        """
        All-in
        """
        if not self.terran_very_hard_mission_weapon_armor_level(state):
            return False
        beats_kerrigan = (
            state.has_any({item_names.MARINE, item_names.DOMINION_TROOPER, item_names.BANSHEE, item_names.GHOST}, self.player)
            or state.has_all({item_names.REAPER, item_names.REAPER_RESOURCE_EFFICIENCY}, self.player)
            or self.advanced_tactics
        )
        if get_option_value(self.world, 'all_in_map') == AllInMap.option_ground:
            # Ground
            defense_rating = self.terran_defense_rating(state, True, False)
            if state.has_any({item_names.BATTLECRUISER, item_names.BANSHEE}, self.player):
                defense_rating += 2
            return defense_rating >= 13 and beats_kerrigan
        else:
            # Air
            defense_rating = self.terran_defense_rating(state, True, True)
            return (
                defense_rating >= 9 and beats_kerrigan
                and state.has_any({item_names.VIKING, item_names.BATTLECRUISER, item_names.VALKYRIE}, self.player)
                and state.has_any({item_names.HIVE_MIND_EMULATOR, item_names.PSI_DISRUPTER, item_names.MISSILE_TURRET}, self.player)
            )

    def all_in_z_requirement(self, state: CollectionState):
        """
        All-in (Zerg)
        """
        if not self.zerg_very_hard_mission_weapon_armor_level(state):
            return False
        beats_kerrigan = (
                state.has_any({item_names.ZERGLING, item_names.MUTALISK, item_names.INFESTED_MARINE}, self.player)
                or state.has_all({item_names.SWARM_HOST, item_names.SWARM_HOST_RESOURCE_EFFICIENCY}, self.player)
                or self.morph_brood_lord(state)
                or self.advanced_tactics
        )
        if get_option_value(self.world, 'all_in_map') == AllInMap.option_ground:
            # Ground
            defense_rating = self.zerg_defense_rating(state, True, False)
            if state.has_any({item_names.MUTALISK, item_names.INFESTED_BANSHEE, item_names.INFESTED_DUSK_WINGS}, self.player) or self.morph_brood_lord(state):
                defense_rating += 2
            return defense_rating >= 13 and beats_kerrigan
        else:
            # Air
            defense_rating = self.zerg_defense_rating(state, True, True)
            return (
                    defense_rating >= 9 and beats_kerrigan
                    and state.has_any({item_names.MUTALISK, item_names.CORRUPTOR}, self.player)
                    and state.has_any({item_names.SPORE_CRAWLER, item_names.INFESTED_MISSILE_TURRET}, self.player)
            )

    def all_in_p_requirement(self, state: CollectionState):
        """
        All-in (Protoss)
        """
        if not self.protoss_very_hard_mission_weapon_armor_level(state):
            return False
        beats_kerrigan = (
                # cheap units with multiple small attacks, or anything with Feedback
                state.has_any({item_names.CENTURION, item_names.SENTINEL, item_names.SKIRMISHER,
                               item_names.HIGH_TEMPLAR}, self.player)
                or state.has_all({item_names.SIGNIFIER, item_names.SIGNIFIER_FEEDBACK}, self.player)
                or (self.protoss_can_merge_archon(state) and state.has(item_names.ARCHON_HIGH_ARCHON, self.player))
                or (self.protoss_can_merge_dark_archon(state) and state.has(item_names.DARK_ARCHON_FEEDBACK, self.player))
                or self.advanced_tactics
        )
        if get_option_value(self.world, 'all_in_map') == AllInMap.option_ground:
            # Ground
            defense_rating = self.protoss_defense_rating(state, True)
            if state.has_any({item_names.SKIRMISHER, item_names.DARK_TEMPLAR, item_names.TEMPEST, item_names.TRIREME}, self.player):
                defense_rating += 2
            return defense_rating >= 13 and beats_kerrigan
        else:
            # Air
            defense_rating = self.protoss_defense_rating(state, True)
            if state.has(item_names.KHAYDARIN_MONOLITH, self.player):
                defense_rating += 2
            return (
                    defense_rating >= 9 and beats_kerrigan
                    and self.protoss_anti_light_anti_air(state)
                    and state.has_any(
                {item_names.TEMPEST, item_names.SKYLORD, item_names.VOID_RAY},
                self.player)
            )

    # HotS

    def zerg_defense_rating(self, state: CollectionState, zerg_enemy: bool, air_enemy: bool = True) -> int:
        """
        Ability to handle defensive missions
        :param state:
        :param zerg_enemy: Whether the enemy is zerg
        :param air_enemy: Whether the enemy attacks with air
        """
        defense_score = sum((zvx_defense_ratings[item] for item in zvx_defense_ratings if state.has(item, self.player)))
        # Twin Drones
        if state.has(item_names.TWIN_DRONES, self.player):
            if state.has(item_names.SPINE_CRAWLER, self.player):
                defense_score += 1
            if state.has(item_names.SPORE_CRAWLER, self.player) and air_enemy:
                defense_score += 1
        # Impaler
        if self.morph_impaler(state):
            defense_score += 3
            if state.has(item_names.IMPALER_HARDENED_TENTACLE_SPINES, self.player):
                defense_score += 1
            if zerg_enemy:
                defense_score += -1
        # Lurker
        if self.morph_lurker(state):
            defense_score += 1
            if state.has(item_names.LURKER_SEISMIC_SPINES, self.player):
                defense_score += 2
            if state.has(item_names.LURKER_ADAPTED_SPINES, self.player) and not zerg_enemy:
                defense_score += 1
            if zerg_enemy:
                defense_score += 1
        # Brood Lord
        if self.morph_brood_lord(state):
            defense_score += 2
        # Corpser Roach
        if state.has_all({item_names.ROACH, item_names.ROACH_CORPSER_STRAIN}, self.player):
            defense_score += 1
            if zerg_enemy:
                defense_score += 1
        # Igniter
        if self.morph_igniter(state) and zerg_enemy:
            defense_score += 2
        # Creep Tumors
        if state.has_any({item_names.SWARM_QUEEN, item_names.OVERLORD_OVERSEER_ASPECT}, self.player):
            if not zerg_enemy:
                defense_score += 1
            if state.has(item_names.MALIGNANT_CREEP, self.player):
                defense_score += 1
        # Infested Siege Breakers
        if state.has_all({item_names.INFESTED_SIEGE_BREAKERS, item_names.SIEGE_TANK_GRADUATING_RANGE}, self.player):
            defense_score += 1

        # General enemy-based rules
        if air_enemy:
            defense_score += sum((zvx_air_defense_ratings[item] for item in zvx_air_defense_ratings if state.has(item, self.player)))
            # spore and missile turret should not stack for defense rating
            if state.has_all({item_names.SPORE_CRAWLER, item_names.INFESTED_MISSILE_TURRET}, self.player):
                defense_score -= 2
        # Advanced Tactics bumps defense rating requirements down by 2
        if self.advanced_tactics:
            defense_score += 2
        return defense_score

    def zerg_army_weapon_armor_upgrade_min_level(self, state: CollectionState) -> int:
        count: int = WEAPON_ARMOR_UPGRADE_MAX_LEVEL
        if self.world_has_zerg_melee_unit():
            count = min(count, self.zerg_melee_weapon_armor_upgrade_min_level(state))
        if self.world_has_zerg_ranged_unit():
            count = min(count, self.zerg_ranged_weapon_armor_upgrade_min_level(state))
        if self.world_has_zerg_air_unit():
            count = min(count, self.zerg_flyer_weapon_armor_upgrade_min_level(state))
        return count
    
    def zerg_melee_weapon_armor_upgrade_min_level(self, state: CollectionState) -> int:
        return min(
            self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_ZERG_MELEE_ATTACK, state),
            self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_ZERG_GROUND_CARAPACE, state),
        )

    def zerg_ranged_weapon_armor_upgrade_min_level(self, state: CollectionState) -> int:
        return min(
            self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_ZERG_MISSILE_ATTACK, state),
            self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_ZERG_GROUND_CARAPACE, state),
        )

    def zerg_flyer_weapon_armor_upgrade_min_level(self, state: CollectionState) -> int:
        return min(
            self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_ZERG_FLYER_ATTACK, state),
            self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_ZERG_FLYER_CARAPACE, state),
        )

    def zerg_very_hard_mission_weapon_armor_level(self, state: CollectionState) -> bool:
        return self.zerg_army_weapon_armor_upgrade_min_level(state) >= self.get_very_hard_required_upgrade_level()

    def zerg_common_unit(self, state: CollectionState) -> bool:
        return state.has_any(self.basic_zerg_units, self.player)

    def zerg_competent_anti_air(self, state: CollectionState) -> bool:
        return (
            state.has_any({item_names.HYDRALISK, item_names.MUTALISK, item_names.CORRUPTOR, item_names.BROOD_QUEEN}, self.player)
            or state.has_all({item_names.SWARM_HOST, item_names.SWARM_HOST_PRESSURIZED_GLANDS}, self.player)
            or state.has_all({item_names.SCOURGE, item_names.SCOURGE_RESOURCE_EFFICIENCY}, self.player)
            or (self.advanced_tactics and state.has(item_names.INFESTOR, self.player))
        )

    def zerg_basic_anti_air(self, state: CollectionState) -> bool:
        return self.zerg_basic_kerriganless_anti_air(state) or self.kerrigan_unit_available

    def zerg_basic_kerriganless_anti_air(self, state: CollectionState) -> bool:
        return (
            self.zerg_competent_anti_air(state) or state.has_any({item_names.SWARM_QUEEN, item_names.SCOURGE}, self.player)
            or (self.advanced_tactics and state.has_any({item_names.SPORE_CRAWLER, item_names.INFESTED_MISSILE_TURRET}, self.player))
        )

    def zerg_basic_air_to_air(self, state: CollectionState) -> bool:
        return (
            state.has_any({
                item_names.MUTALISK, item_names.CORRUPTOR, item_names.BROOD_QUEEN, item_names.SCOURGE,
                item_names.INFESTED_LIBERATOR
            }, self.player)
            or self.morph_devourer(state)
            or self.morph_viper(state)
            or (
                self.morph_guardian(state) and state.has(item_names.GUARDIAN_PRIMAL_ADAPTATION, self.player)
            )
        )

    def zerg_basic_air_to_ground(self, state: CollectionState) -> bool:
        return (
            state.has_any({
                item_names.MUTALISK, item_names.INFESTED_BANSHEE
            }, self.player)
            or self.morph_guardian(state)
            or self.morph_brood_lord(state)
            or (
                self.morph_devourer(state) and state.has(item_names.DEVOURER_PRESCIENT_SPORES, self.player)
            )
        )

    def zerg_versatile_air(self, state: CollectionState) -> bool:
        return self.zerg_basic_air_to_air(state) and self.zerg_basic_air_to_ground(state)

    def zerg_infested_tank_with_ammo(self, state: CollectionState) -> bool:
        return (
                state.has(item_names.INFESTED_SIEGE_TANK, self.player)
                and (
                        state.has_all({item_names.INFESTOR, item_names.INFESTOR_INFESTED_TERRAN}, self.player)
                        or state.has(item_names.INFESTED_BUNKER, self.player)
                        or state.count(item_names.INFESTED_SIEGE_TANK_PROGRESSIVE_AUTOMATED_MITOSIS, self.player) >= (1 if self.advanced_tactics else 2)
                )
        )

    def morph_brood_lord(self, state: CollectionState) -> bool:
        return (
            (state.has_any({item_names.MUTALISK, item_names.CORRUPTOR}, self.player) or self.morphling_enabled)
            and state.has(item_names.MUTALISK_CORRUPTOR_BROOD_LORD_ASPECT, self.player)
        )

    def morph_guardian(self, state: CollectionState) -> bool:
        return (
            (state.has_any({item_names.MUTALISK, item_names.CORRUPTOR}, self.player) or self.morphling_enabled)
            and state.has(item_names.MUTALISK_CORRUPTOR_GUARDIAN_ASPECT, self.player)
        )
    
    def morph_viper(self, state: CollectionState) -> bool:
        return (
            (state.has_any({item_names.MUTALISK, item_names.CORRUPTOR}, self.player) or self.morphling_enabled)
            and state.has(item_names.MUTALISK_CORRUPTOR_VIPER_ASPECT, self.player)
        )

    def morph_devourer(self, state: CollectionState) -> bool:
        return (
            (state.has_any({item_names.MUTALISK, item_names.CORRUPTOR}, self.player) or self.morphling_enabled)
            and state.has(item_names.MUTALISK_CORRUPTOR_DEVOURER_ASPECT, self.player)
        )
    
    def morph_impaler(self, state: CollectionState) -> bool:
        return (
            (state.has(item_names.HYDRALISK, self.player) or self.morphling_enabled)
            and state.has(item_names.HYDRALISK_IMPALER_ASPECT, self.player)
        )

    def morph_lurker(self, state: CollectionState) -> bool:
        return (
            (state.has(item_names.HYDRALISK, self.player) or self.morphling_enabled)
            and state.has(item_names.HYDRALISK_LURKER_ASPECT, self.player)
        )

    def morph_impaler_or_lurker(self, state: CollectionState) -> bool:
        return self.morph_impaler(state) or self.morph_lurker(state)

    def morph_igniter(self, state: CollectionState) -> bool:
        return (
            (state.has(item_names.ROACH, self.player) or self.morphling_enabled)
            and state.has(item_names.ROACH_PRIMAL_IGNITER_ASPECT, self.player)
        )

    def morph_tyrannozor(self, state: CollectionState) -> bool:
        return (
            state.has(item_names.ULTRALISK_TYRANNOZOR_ASPECT, self.player)
            and (state.has(item_names.ULTRALISK, self.player) or self.morphling_enabled)
        )
    
    def zerg_infested_siege_tanks_with_ammo(self, state: CollectionState) -> bool:
        return (
            state.has(item_names.INFESTED_SIEGE_TANK, self.player)
            and state.has_any((
                item_names.INFESTED_SIEGE_TANK_PROGRESSIVE_AUTOMATED_MITOSIS,
                item_names.INFESTED_MARINE,
                item_names.INFESTED_BUNKER,
            ), self.player)
        )

    def zerg_competent_comp(self, state: CollectionState) -> bool:
        if self.zerg_army_weapon_armor_upgrade_min_level(state) < 2:
            return False
        advanced = self.advanced_tactics
        core_unit = state.has_any({item_names.ROACH, item_names.ABERRATION, item_names.ZERGLING}, self.player)
        support_unit = (
            state.has_any({item_names.SWARM_QUEEN, item_names.HYDRALISK}, self.player)
            or self.morph_brood_lord(state)
            or advanced and (
                state.has_any({item_names.INFESTOR, item_names.DEFILER}, self.player)
                or self.morph_viper(state)
            )
        )
        if core_unit and support_unit:
            return True
        vespene_unit = (
            state.has_any({item_names.ULTRALISK, item_names.ABERRATION}, self.player)
            or advanced and self.morph_viper(state)
        )
        return vespene_unit and state.has_any({item_names.ZERGLING, item_names.SWARM_QUEEN}, self.player)
    
    def zerg_common_unit_basic_aa(self, state: CollectionState) -> bool:
        return self.zerg_common_unit(state) and self.zerg_basic_anti_air(state)

    def zerg_common_unit_competent_aa(self, state: CollectionState) -> bool:
        return self.zerg_common_unit(state) and self.zerg_competent_anti_air(state)
    
    def zerg_competent_comp_basic_aa(self, state: CollectionState) -> bool:
        return self.zerg_competent_comp(state) and self.zerg_basic_anti_air(state)
    
    def zerg_competent_comp_competent_aa(self, state: CollectionState) -> bool:
        return self.zerg_competent_comp(state) and self.zerg_competent_anti_air(state)

    def spread_creep(self, state: CollectionState) -> bool:
        return self.advanced_tactics or state.has_any({item_names.SWARM_QUEEN, item_names.OVERLORD_OVERSEER_ASPECT}, self.player)

    def zerg_mineral_dump(self, state: CollectionState) -> bool:
        return (
                state.has_any({item_names.ZERGLING, item_names.PYGALISK, item_names.INFESTED_BUNKER}, self.player)
                or state.has_all({item_names.SWARM_QUEEN, item_names.SWARM_QUEEN_RESOURCE_EFFICIENCY}, self.player)
                or (
                        self.advanced_tactics
                        and self.spread_creep(state)
                        and state.has(item_names.SPINE_CRAWLER, self.player)
                )
        )

    def zerg_big_monsters(self, state: CollectionState) -> bool:
        """
        Durable units with some capacity for damage
        """
        return (
            self.morph_tyrannozor(state)
            or state.has_any((item_names.ABERRATION, item_names.ULTRALISK), self.player)
            or (self.spread_creep(state) and state.has(item_names.INFESTED_BUNKER, self.player))
        )
    
    def zerg_base_buster(self, state: CollectionState) -> bool:
        """Powerful and sustainable zerg anti-ground for busting big bases; anti-air not included"""
        return (
            (
                self.zerg_melee_weapon_armor_upgrade_min_level(state) >= self.get_very_hard_required_upgrade_level()
                and (
                    self.morph_tyrannozor(state)
                    or (
                        state.has(item_names.ULTRALISK, self.player)
                        and state.has_any((item_names.ULTRALISK_TORRASQUE_STRAIN, item_names.ULTRALISK_CHITINOUS_PLATING), self.player)
                    )
                )
                and state.has(item_names.SWARM_QUEEN, self.player)  # Healing to sustain the frontline
            ) or (
                self.zerg_ranged_weapon_armor_upgrade_min_level(state) >= self.get_very_hard_required_upgrade_level()
                and (
                    self.morph_impaler(state)
                    or self.morph_lurker(state) and state.has_any((item_names.LURKER_SEISMIC_SPINES, item_names.LURKER_ADAPTED_SPINES), self.player)
                    or state.has_all((
                        item_names.ROACH, item_names.ROACH_CORPSER_STRAIN, item_names.ROACH_ADAPTIVE_PLATING, item_names.ROACH_GLIAL_RECONSTITUTION,
                    ), self.player)
                    or self.morph_igniter(state) and state.has(item_names.PRIMAL_IGNITER_PRIMAL_TENACITY, self.player)
                    or state.has_all((item_names.INFESTOR, item_names.INFESTOR_INFESTED_TERRAN), self.player)
                    or state.has_any((
                        item_names.INFESTED_BANSHEE, item_names.INFESTED_DIAMONDBACK, item_names.INFESTED_MARINE,
                    ), self.player)
                    or self.spread_creep(state) and state.has(item_names.INFESTED_BUNKER, self.player)
                    or self.zerg_infested_siege_tanks_with_ammo(state)
                    # Highly-upgraded swarm hosts may also work, but that would require promoting many upgrades to progression
                )
            ) or (
                self.zerg_flyer_weapon_armor_upgrade_min_level(state) >= self.get_very_hard_required_upgrade_level()
                and (
                    self.morph_brood_lord(state)
                    or self.morph_guardian(state) and state.has_all((item_names.GUARDIAN_PROPELLANT_SACS, item_names.GUARDIAN_SORONAN_ACID), self.player)
                    # Highly-upgraded anti-ground devourers would also be good
                )
            )
        )
    
    def zerg_competent_defense(self, state: CollectionState) -> bool:
        return (
            self.zerg_common_unit(state)
            and (
                (
                    state.has(item_names.SWARM_HOST, self.player)
                    or self.morph_brood_lord(state)
                    or self.morph_impaler_or_lurker(state)
                    or state.has_all({item_names.INFESTED_LIBERATOR, item_names.INFESTED_LIBERATOR_DEFENDER_MODE}, self.player)
                ) or (
                    self.advanced_tactics
                    and (self.morph_viper(state)
                         or state.has(item_names.SPINE_CRAWLER, self.player))
                )
            )
        )

    def zerg_can_grab_ghosts_in_the_fog_east_rock_formation(self, state: CollectionState) -> bool:
        return (
                state.has_any({
                    item_names.MUTALISK, item_names.INFESTED_BANSHEE, item_names.OVERLORD_VENTRAL_SACS,
                    item_names.INFESTOR
                }, self.player)
                or (
                        self.morph_devourer(state) and state.has(item_names.DEVOURER_PRESCIENT_SPORES, self.player)
                ) or (
                        self.morph_guardian(state) and state.has(item_names.GUARDIAN_PRIMAL_ADAPTATION, self.player)
                ) or (
                        (self.morph_guardian(state) or self.morph_brood_lord(state))
                        and self.zerg_basic_air_to_air(state)
                ) or (
                        self.advanced_tactics
                        and (
                            state.has_any({
                                item_names.INFESTED_SIEGE_BREAKERS, item_names.INFESTED_DUSK_WINGS
                            }, self.player)
                            or (
                                state.has(item_names.HUNTERLING, self.player)
                                and self.zerg_basic_air_to_air(state)
                            )
                        )
                )
        )
    
    def zerg_respond_to_colony_infestations(self, state: CollectionState) -> bool:
        """
        Can deal quickly with Brood Lords and Mutas in Haven's Fall and being able to progress the mission
        """
        return (
            self.zerg_common_unit(state)
            and self.zerg_competent_anti_air(state)
            and (
                    self.morph_devourer(state)
                    or self.advanced_tactics and self.morph_viper(state)
                    or state.has_any({item_names.MUTALISK, item_names.CORRUPTOR}, self.player)
                    or self.advanced_tactics and state.has_any({item_names.BROOD_QUEEN, item_names.SCOURGE}, self.player)
                )
            and self.zerg_defense_rating(state, True) >= 3
        )

    def zerg_temple_of_unification_requirement(self, state: CollectionState) -> bool:
        # Don't be locked to roach/hydra
        return (
                self.zerg_competent_comp(state)
                and self.zerg_competent_anti_air(state)
                and (
                        state.has_any({item_names.INFESTED_BANSHEE, item_names.INFESTED_LIBERATOR}, self.player)
                        or state.has_all({item_names.MUTALISK, item_names.MUTALISK_SUNDERING_GLAIVE}, self.player)
                        or self.zerg_big_monsters(state)
                        or (
                                self.advanced_tactics
                                and (
                                        state.has_any({item_names.INFESTOR, item_names.DEFILER, item_names.BROOD_QUEEN}, self.player)
                                        or self.morph_viper(state)
                                )
                        )
                )
        )

    def basic_kerrigan(self, state: CollectionState) -> bool:
        # One active ability that can be used to defeat enemies directly on Standard
        if (not self.advanced_tactics
            and not state.has_any({
                item_names.KERRIGAN_KINETIC_BLAST, item_names.KERRIGAN_LEAPING_STRIKE,
                item_names.KERRIGAN_CRUSHING_GRIP, item_names.KERRIGAN_PSIONIC_SHIFT,
                item_names.KERRIGAN_SPAWN_BANELINGS
            }, self.player)
        ):
            return False
        # Two non-ultimate abilities
        count = 0
        for item in (
                item_names.KERRIGAN_KINETIC_BLAST, item_names.KERRIGAN_LEAPING_STRIKE, item_names.KERRIGAN_HEROIC_FORTITUDE,
                item_names.KERRIGAN_CHAIN_REACTION, item_names.KERRIGAN_CRUSHING_GRIP, item_names.KERRIGAN_PSIONIC_SHIFT,
                item_names.KERRIGAN_SPAWN_BANELINGS, item_names.KERRIGAN_INFEST_BROODLINGS, item_names.KERRIGAN_FURY
        ):
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
        return (
            self.story_tech_granted
            or state.has_any({item_names.ZERGLING, item_names.HYDRALISK, item_names.ROACH}, self.player)
            or (self.advanced_tactics and state.has(item_names.INFESTOR, self.player))
        )

    def supreme_requirement(self, state: CollectionState) -> bool:
        return (
            self.story_tech_granted
            or not self.kerrigan_unit_available
            or (
                state.has_all({item_names.KERRIGAN_LEAPING_STRIKE, item_names.KERRIGAN_MEND}, self.player)
                and self.kerrigan_levels(state, 35)
            )
        )

    def kerrigan_levels(self, state: CollectionState, target: int) -> bool:
        if self.story_levels_granted or not self.kerrigan_unit_available:
            return True  # Levels are granted
        if (self.kerrigan_levels_per_mission_completed > 0
            and self.kerrigan_levels_per_mission_completed_cap > 0
            and not self.is_item_placement(state)
        ):
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

    def terran_infested_garrison_claimer(self, state: CollectionState) -> bool:
        return state.has_any((item_names.GHOST, item_names.SPECTRE, item_names.EMPERORS_SHADOW), self.player)

    def protoss_infested_garrison_claimer(self, state: CollectionState) -> bool:
        return (
            state.has_any((item_names.HIGH_TEMPLAR, item_names.SIGNIFIER, item_names.ASCENDANT), self.player)
            or self.protoss_can_merge_dark_archon(state)
        )

    def zerg_the_reckoning_requirement(self, state: CollectionState) -> bool:
        if self.take_over_ai_allies:
            return (
                self.terran_competent_comp(state)
                and self.zerg_competent_comp(state)
                and (self.zerg_competent_anti_air(state)
                    or self.terran_competent_anti_air(state)
                )
                and self.terran_very_hard_mission_weapon_armor_level(state)
                and self.zerg_very_hard_mission_weapon_armor_level(state)
            )
        else:
            return (
                    self.zerg_competent_comp(state)
                    and self.zerg_competent_anti_air(state)
                    and self.zerg_very_hard_mission_weapon_armor_level(state)
            )

    def terran_the_reckoning_requirement(self, state: CollectionState) -> bool:
        return (
                self.terran_very_hard_mission_weapon_armor_level(state)
                and self.terran_beats_protoss_deathball(state)
        )

    def protoss_the_reckoning_requirement(self, state: CollectionState) -> bool:
        return (
                self.protoss_very_hard_mission_weapon_armor_level(state)
                and self.protoss_competent_comp(state)
                and (
                        not self.take_over_ai_allies
                        or (
                            self.terran_competent_comp(state)
                            and self.terran_very_hard_mission_weapon_armor_level(state)
                        )
                )
        )

    # LotV
    def protoss_army_weapon_armor_upgrade_min_level(self, state: CollectionState) -> int:
        count: int = WEAPON_ARMOR_UPGRADE_MAX_LEVEL + 1 # +1 for Quatro
        if self.world_has_protoss_ground_unit():
            count = min(
                count,
                self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_PROTOSS_GROUND_WEAPON, state),
                self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_PROTOSS_GROUND_ARMOR, state)
            )
        if self.world_has_protoss_air_unit():
            count = min(
                count,
                self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_PROTOSS_AIR_WEAPON, state),
                self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_PROTOSS_AIR_ARMOR, state)
            )
        if self.world_has_protoss_ground_unit() or self.world_has_protoss_air_unit():
            count = min(
                count,
                self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_PROTOSS_SHIELDS, state),
            )
        return count

    def protoss_very_hard_mission_weapon_armor_level(self, state: CollectionState) -> bool:
        return self.protoss_army_weapon_armor_upgrade_min_level(state) >= self.get_very_hard_required_upgrade_level()

    def protoss_defense_rating(self, state: CollectionState, zerg_enemy: bool) -> int:
        """
        Ability to handle defensive missions
        :param state:
        :param zerg_enemy: Whether the enemy is zerg
        """
        defense_score = sum((pvx_defense_ratings[item] for item in pvx_defense_ratings if state.has(item, self.player)))

        # No anti-air defense dict here, use an existing logic rule instead
        if zerg_enemy:
            defense_score += sum((pvz_defense_ratings[item] for item in pvz_defense_ratings if state.has(item, self.player)))
        # Advanced Tactics bumps defense rating requirements down by 2
        if self.advanced_tactics:
            defense_score += 2
        return defense_score

    def protoss_common_unit(self, state: CollectionState) -> bool:
        return state.has_any(self.basic_protoss_units, self.player)

    def protoss_basic_anti_air(self, state: CollectionState) -> bool:
        return (
            self.protoss_competent_anti_air(state)
            or state.has_any({
                item_names.PHOENIX, item_names.MIRAGE, item_names.CORSAIR, item_names.CARRIER, item_names.SKYLORD,
                item_names.SCOUT, item_names.DARK_ARCHON, item_names.MOTHERSHIP
            }, self.player)
            or state.has_all({item_names.TRIREME, item_names.TRIREME_SOLAR_BEAM}, self.player)
            or state.has_all({item_names.WRATHWALKER, item_names.WRATHWALKER_AERIAL_TRACKING}, self.player)
            or state.has_all({item_names.WARP_PRISM, item_names.WARP_PRISM_PHASE_BLASTER}, self.player)
            or self.advanced_tactics and state.has_any(
                {item_names.HIGH_TEMPLAR, item_names.SIGNIFIER, item_names.ASCENDANT, item_names.DARK_TEMPLAR,
                 item_names.SENTRY, item_names.ENERGIZER}, self.player)
        )

    def protoss_anti_armor_anti_air(self, state: CollectionState) -> bool:
        return (
            self.protoss_competent_anti_air(state)
            or state.has_any({item_names.SCOUT, item_names.WARP_RAY}, self.player)
            or (state.has_any({item_names.IMMORTAL, item_names.ANNIHILATOR}, self.player)
                and state.has(item_names.IMMORTAL_ANNIHILATOR_ADVANCED_TARGETING_MECHANICS, self.player))
            or state.has_all({item_names.WRATHWALKER, item_names.WRATHWALKER_AERIAL_TRACKING}, self.player)
        )

    def protoss_anti_light_anti_air(self, state: CollectionState) -> bool:
        return (
            self.protoss_competent_anti_air(state)
            or state.has_any({
                item_names.PHOENIX, item_names.MIRAGE, item_names.CORSAIR, item_names.CARRIER,
            }, self.player)
            or state.has_all((item_names.SKIRMISHER, item_names.SKIRMISHER_PEER_CONTEMPT), self.player)
        )
    
    def protoss_common_unit_basic_aa(self, state: CollectionState) -> bool:
        return self.protoss_common_unit(state) and self.protoss_basic_anti_air(state)
    
    def protoss_common_unit_anti_light_air(self, state: CollectionState) -> bool:
        return self.protoss_common_unit(state) and self.protoss_anti_light_anti_air(state)

    def protoss_common_unit_anti_armor_air(self, state: CollectionState) -> bool:
        return self.protoss_common_unit(state) and self.protoss_anti_armor_anti_air(state)

    def protoss_competent_anti_air(self, state: CollectionState) -> bool:
        return (
            state.has_any({
                item_names.STALKER, item_names.SLAYER, item_names.INSTIGATOR, item_names.DRAGOON, item_names.ADEPT,
                item_names.VOID_RAY, item_names.DESTROYER, item_names.TEMPEST, item_names.SKYLORD,
            }, self.player)
            or ((
                    state.has_any({
                        item_names.PHOENIX, item_names.MIRAGE, item_names.CORSAIR, item_names.CARRIER,
                    }, self.player)
                    or state.has_all((item_names.SKIRMISHER, item_names.SKIRMISHER_PEER_CONTEMPT), self.player)
                )
                and (
                    state.has_any({item_names.SCOUT, item_names.WARP_RAY}, self.player)
                    or state.has_all({item_names.WRATHWALKER, item_names.WRATHWALKER_AERIAL_TRACKING}, self.player)
                )
            )
            or (self.advanced_tactics
                and state.has_any({item_names.IMMORTAL, item_names.ANNIHILATOR}, self.player)
                and state.has(item_names.IMMORTAL_ANNIHILATOR_ADVANCED_TARGETING_MECHANICS, self.player)
            )
        )

    def protoss_has_blink(self, state: CollectionState) -> bool:
        return (
            state.has_any({item_names.STALKER, item_names.INSTIGATOR}, self.player)
            or state.has_all({item_names.SLAYER, item_names.SLAYER_PHASE_BLINK}, self.player)
            or (
                state.has(item_names.DARK_TEMPLAR_AVENGER_BLOOD_HUNTER_BLINK, self.player)
                and state.has_any({item_names.DARK_TEMPLAR, item_names.BLOOD_HUNTER, item_names.AVENGER}, self.player)
            )
        )

    def protoss_can_attack_behind_chasm(self, state: CollectionState) -> bool:
        return (
            state.has_any({
                item_names.SCOUT, item_names.TEMPEST,
                item_names.CARRIER, item_names.SKYLORD, item_names.TRIREME,
                item_names.VOID_RAY, item_names.DESTROYER, item_names.WARP_RAY, item_names.DAWNBRINGER,
                item_names.MOTHERSHIP,
            }, self.player)
            or self.protoss_has_blink(state)
            or (state.has(item_names.WARP_PRISM, self.player)
                and (self.protoss_common_unit(state) or state.has(item_names.WARP_PRISM_PHASE_BLASTER, self.player)))
            or (self.advanced_tactics
                and state.has_any({item_names.ORACLE, item_names.ARBITER}, self.player))
        )

    def protoss_respond_to_colony_infestations(self, state: CollectionState) -> bool:
        """
        Can deal quickly with Brood Lords and Mutas in Haven's Fall and being able to progress the mission
        """
        return (
            self.protoss_common_unit(state)
            and self.protoss_competent_anti_air(state)
            and (
                state.has_any({
                    item_names.CARRIER, item_names.SKYLORD,
                }, self.player)
                # handle mutas
                or (state.has_any({
                        item_names.PHOENIX, item_names.MIRAGE, item_names.CORSAIR,
                    }, self.player)
                    or state.has_all((item_names.SKIRMISHER, item_names.SKIRMISHER_PEER_CONTEMPT), self.player)
                )
                # handle brood lords and virophages
                and (state.has_any({
                        item_names.VOID_RAY, item_names.DESTROYER, item_names.WARP_RAY,
                        item_names.TEMPEST
                    }, self.player)
                    or self.advanced_tactics and state.has_all({item_names.SCOUT, item_names.WARP_PRISM}, self.player)
                )
            )
            and self.protoss_defense_rating(state, True) >= 3
        )

    def protoss_fleet(self, state: CollectionState) -> bool:
        return state.has_any({
            item_names.CARRIER, item_names.SKYLORD, item_names.TRIREME, item_names.TEMPEST, item_names.VOID_RAY,
            item_names.DESTROYER, item_names.WARP_RAY, item_names.DAWNBRINGER
        }, self.player)

    def templars_return_phase_2_requirement(self, state: CollectionState) -> bool:
        return (
            self.story_tech_granted
            or (state.has_any({
                    item_names.IMMORTAL, item_names.ANNIHILATOR, item_names.VANGUARD,
                    item_names.COLOSSUS, item_names.WRATHWALKER, item_names.REAVER,
                    item_names.DARK_TEMPLAR, item_names.HIGH_TEMPLAR,
                    item_names.ENERGIZER, item_names.SENTRY,
                }, self.player)
            )
        )

    def templars_return_phase_3_reach_colossus_requirement(self, state: CollectionState) -> bool:
        return (
            self.templars_return_phase_2_requirement(state)
            and (self.story_tech_granted
                or (state.has_any({item_names.ZEALOT_WHIRLWIND, item_names.VANGUARD_RAPIDFIRE_CANNON}, self.player))
            )
        )

    def templars_return_phase_3_reach_dts_requirement(self, state: CollectionState) -> bool:
        return (
            self.templars_return_phase_3_reach_colossus_requirement(state)
            and (self.story_tech_granted
                or state.has(item_names.COLOSSUS_FIRE_LANCE, self.player)
                or state.has_all({
                    item_names.COLOSSUS_PACIFICATION_PROTOCOL,
                    item_names.ENERGIZER_MOBILE_CHRONO_BEAM,
                }, self.player)
            )
        )

    def terran_spear_of_adun_requirement(self, state: CollectionState) -> bool:
        return (
                self.terran_common_unit(state)
                and self.terran_competent_anti_air(state)
                and self.terran_defense_rating(state, False, False) >= 5
                and self.terran_defense_rating(state, True, False) >= 5
        )

    def protoss_brothers_in_arms_requirement(self, state: CollectionState) -> bool:
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
                or state.has_any({item_names.BATTLECRUISER, item_names.LIBERATOR, item_names.SIEGE_TANK}, self.player)
                or (
                        self.advanced_tactics
                        and state.has_all({item_names.SPECTRE, item_names.SPECTRE_PSIONIC_LASH}, self.player)
                )
                or (state.has(item_names.IMMORTAL, self.player)
                    and state.has_any({item_names.MARINE, item_names.DOMINION_TROOPER, item_names.MARAUDER}, self.player)
                    and self.terran_bio_heal(state)
                )
            )
        )

    def zerg_brothers_in_arms_requirement(self, state: CollectionState) -> bool:
        return (
                self.zerg_common_unit(state)
                and self.zerg_competent_comp(state)
                and self.zerg_competent_anti_air(state)
                and self.zerg_big_monsters(state)
        ) or (
                self.take_over_ai_allies
                and (
                        self.zerg_common_unit(state)
                        or self.protoss_common_unit(state)
                )
                and (
                        self.terran_competent_anti_air(state)
                        or self.zerg_competent_anti_air(state)
                )
                and (
                        self.zerg_big_monsters(state)
                        or state.has_any({item_names.BATTLECRUISER, item_names.LIBERATOR, item_names.SIEGE_TANK}, self.player)
                        or (
                                self.advanced_tactics
                                and state.has_all({item_names.SPECTRE, item_names.SPECTRE_PSIONIC_LASH}, self.player)
                        )
                        or (state.has(item_names.ABERRATION, self.player)
                            and state.has_any({item_names.MARINE, item_names.DOMINION_TROOPER, item_names.MARAUDER}, self.player)
                            and self.terran_bio_heal(state)
                            )
                )
        )

    def protoss_hybrid_counter(self, state: CollectionState) -> bool:
        """
        Ground Hybrids
        """
        return (
            state.has_any({
                item_names.ANNIHILATOR, item_names.ASCENDANT, item_names.TEMPEST, item_names.CARRIER,
                item_names.SKYLORD, item_names.TRIREME, item_names.VOID_RAY, item_names.WARP_RAY,
                item_names.WRATHWALKER, item_names.VANGUARD
            }, self.player)
            or (state.has(item_names.IMMORTAL, self.player)
                or self.advanced_tactics
            ) and state.has_any({
                item_names.STALKER, item_names.DRAGOON, item_names.ADEPT, item_names.INSTIGATOR, item_names.SLAYER
            }, self.player)
        )

    def the_infinite_cycle_requirement(self, state: CollectionState) -> bool:
        return (
            self.story_tech_granted
            or not self.kerrigan_unit_available
            or (
                self.two_kerrigan_actives(state)
                and self.basic_kerrigan(state)
                and self.kerrigan_levels(state, 70)
            )
        )

    def protoss_basic_splash(self, state: CollectionState) -> bool:
        return state.has_any({
            item_names.ZEALOT, item_names.COLOSSUS, item_names.VANGUARD, item_names.HIGH_TEMPLAR, item_names.SIGNIFIER,
            item_names.DARK_TEMPLAR, item_names.REAVER, item_names.ASCENDANT, item_names.DAWNBRINGER
        }, self.player)

    def protoss_static_defense(self, state: CollectionState) -> bool:
        return state.has_any({item_names.PHOTON_CANNON, item_names.KHAYDARIN_MONOLITH}, self.player)

    def protoss_can_merge_archon(self, state: CollectionState) -> bool:
        return state.has_any({item_names.HIGH_TEMPLAR, item_names.DARK_TEMPLAR, item_names.SIGNIFIER, item_names.ASCENDANT}, self.player)

    def protoss_can_merge_dark_archon(self, state: CollectionState) -> bool:
        return state.has(item_names.DARK_ARCHON, self.player) or state.has_all({item_names.DARK_TEMPLAR, item_names.DARK_TEMPLAR_DARK_ARCHON_MELD}, self.player)

    def protoss_competent_comp(self, state: CollectionState) -> bool:
        return (
                self.protoss_common_unit(state)
                and self.protoss_competent_anti_air(state)
                and self.protoss_hybrid_counter(state)
                and self.protoss_basic_splash(state)
                and self.protoss_army_weapon_armor_upgrade_min_level(state) >= 2
        )

    def protoss_heal(self, state: CollectionState) -> bool:
        return (
                state.has_any((item_names.SENTRY, item_names.SHIELD_BATTERY, item_names.RECONSTRUCTION_BEAM), self.player)
                or state.has_all((item_names.CARRIER, item_names.CARRIER_REPAIR_DRONES), self.player)
        )

    def protoss_last_stand_requirement(self, state: CollectionState) -> bool:
        return (
            self.protoss_common_unit(state)
            and self.protoss_competent_anti_air(state)
            and self.protoss_static_defense(state)
            and (
                self.advanced_tactics
                or self.protoss_basic_splash(state)
            )
        )

    def terran_last_stand_requirement(self, state: CollectionState) -> bool:
        return (
            self.terran_common_unit(state)
            and state.has_any({item_names.SIEGE_TANK, item_names.LIBERATOR}, self.player)
            and state.has_any({item_names.PERDITION_TURRET, item_names.DEVASTATOR_TURRET, item_names.PLANETARY_FORTRESS}, self.player)
            and self.terran_air_anti_air(state)
            and state.has_any({item_names.VIKING, item_names.BATTLECRUISER}, self.player)
            and self.terran_defense_rating(state, True, False) >= 10
            and self.terran_army_weapon_armor_upgrade_min_level(state) >= 2
        )

    def zerg_last_stand_requirement(self, state: CollectionState) -> bool:
        return (
            self.zerg_common_unit(state)
            and self.zerg_competent_anti_air(state)
            and state.has(item_names.SPINE_CRAWLER, self.player)
            and (
                self.morph_lurker(state)
                or state.has_all({item_names.ULTRALISK, item_names.ULTRALISK_CHITINOUS_PLATING, item_names.ULTRALISK_MONARCH_BLADES}, self.player)
                or state.has_all({item_names.MUTALISK, item_names.MUTALISK_SEVERING_GLAIVE, item_names.MUTALISK_VICIOUS_GLAIVE}, self.player)
                or self.zerg_infested_tank_with_ammo(state)
            )
            and (
                self.morph_impaler(state)
                or state.has_all({item_names.INFESTED_LIBERATOR, item_names.INFESTED_LIBERATOR_DEFENDER_MODE}, self.player)
                or self.zerg_infested_tank_with_ammo(state)
            )
            and (
                self.morph_devourer(state)
                or state.has(item_names.BROOD_QUEEN, self.player)
                or state.has_all({item_names.MUTALISK, item_names.MUTALISK_SUNDERING_GLAIVE}, self.player)
            )
            and self.zerg_mineral_dump(state)
            and self.zerg_army_weapon_armor_upgrade_min_level(state) >= 2
        )

    def protoss_harbinger_of_oblivion_requirement(self, state: CollectionState) -> bool:
        return (
            self.protoss_anti_armor_anti_air(state)
            and (self.take_over_ai_allies
                or (
                    self.protoss_common_unit(state)
                    and self.protoss_hybrid_counter(state)
                )
            )
        )

    def terran_harbinger_of_oblivion_requirement(self, state: CollectionState) -> bool:
        return (
                self.terran_competent_anti_air(state)
                and (
                        self.take_over_ai_allies
                        or (
                                self.terran_beats_protoss_deathball(state)
                                and state.has_any({item_names.BATTLECRUISER, item_names.LIBERATOR, item_names.SIEGE_TANK, item_names.THOR}, self.player)
                        )
                )
        )

    def zerg_harbinger_of_oblivion_requirement(self, state: CollectionState) -> bool:
        return (
                self.zerg_competent_anti_air(state)
                and self.zerg_common_unit(state)
                and (
                        self.take_over_ai_allies
                        or (
                                self.zerg_competent_comp(state)
                                and self.zerg_big_monsters(state)
                        )
                )
        )

    def terran_unsealing_the_past_requirement(self, state: CollectionState) -> bool:
        return (
                self.terran_competent_anti_air(state)
                and self.terran_competent_comp(state)
                and (
                        state.has_all({item_names.SIEGE_TANK, item_names.SIEGE_TANK_JUMP_JETS}, self.player)
                        or state.has_all({item_names.BATTLECRUISER, item_names.BATTLECRUISER_ATX_LASER_BATTERY,
                                          item_names.BATTLECRUISER_COVERT_OPS_ENGINES}, self.player)
                        or (
                                self.advanced_tactics
                                and (
                                        state.has_all({item_names.SIEGE_TANK, item_names.SIEGE_TANK_SMART_SERVOS},
                                                      self.player)
                                        or (
                                                state.has_all({item_names.LIBERATOR, item_names.LIBERATOR_SMART_SERVOS},
                                                              self.player)
                                                and (
                                                        (
                                                                state.has_all(
                                                                    {item_names.HELLION,
                                                                     item_names.HELLION_HELLBAT_ASPECT},
                                                                    self.player)
                                                                or state.has(item_names.FIREBAT, self.player)
                                                        )
                                                        and self.terran_bio_heal(state)
                                                        or state.has_all({item_names.VIKING, item_names.VIKING_SHREDDER_ROUNDS},
                                                                         self.player)
                                                        or state.has(item_names.BANSHEE, self.player)
                                                )
                                        )
                                )
                        )
                )
        )

    def zerg_unsealing_the_past_requirement(self, state: CollectionState) -> bool:
        return (
            self.zerg_competent_comp(state)
            and self.zerg_competent_anti_air(state)
            and (
                self.morph_brood_lord(state)
                or self.zerg_big_monsters(state)
                or state.has_all({item_names.MUTALISK, item_names.MUTALISK_SEVERING_GLAIVE, item_names.MUTALISK_VICIOUS_GLAIVE}, self.player)
                or (
                    self.advanced_tactics
                    and (
                        self.morph_igniter(state)
                        or (
                            self.morph_lurker(state)
                            and state.has(item_names.LURKER_SEISMIC_SPINES, self.player)
                        )
                    )
                )
            )
        )

    def terran_purification_requirement(self, state: CollectionState) -> bool:
        return (
            self.terran_competent_comp(state)
            and self.terran_competent_anti_air(state)
            and self.terran_very_hard_mission_weapon_armor_level(state)
            and self.terran_defense_rating(state, True, False) >= 10
            and (
                state.has_any({item_names.LIBERATOR, item_names.THOR}, self.player)
                or (
                    state.has(item_names.SIEGE_TANK, self.player)
                    and (self.advanced_tactics or state.has(item_names.SIEGE_TANK_MAELSTROM_ROUNDS, self.player))
                )
            )
            and (
                state.has_all({item_names.VIKING, item_names.VIKING_SHREDDER_ROUNDS}, self.player)
                or (
                    state.has(item_names.BANSHEE, self.player)
                    and (
                        state.has(item_names.BANSHEE_SHOCKWAVE_MISSILE_BATTERY, self.player)
                        or (
                            self.advanced_tactics
                            and state.has(item_names.BANSHEE_ROCKET_BARRAGE, self.player)
                        )
                    )
                )
            )
        )

    def zerg_purification_requirement(self, state: CollectionState) -> bool:
        return (
            self.zerg_competent_comp(state)
            and self.zerg_competent_anti_air(state)
            and self.zerg_competent_defense(state)
            and self.zerg_big_monsters(state)
            and (
                state.has(item_names.ULTRALISK, self.player)
                or self.morph_igniter(state)
                or self.morph_lurker(state)
            )
        )

    def protoss_steps_of_the_rite_requirement(self, state: CollectionState) -> bool:
        return (
            self.protoss_competent_comp(state)
            or (
                self.protoss_common_unit(state)
                and self.protoss_competent_anti_air(state)
                and self.protoss_static_defense(state)
            )
        )

    def terran_steps_of_the_rite_requirement(self, state: CollectionState) -> bool:
        return (
            self.terran_beats_protoss_deathball(state)
            and (
                state.has_any({item_names.SIEGE_TANK, item_names.LIBERATOR}, self.player)
                or state.has_all({item_names.BATTLECRUISER, item_names.BATTLECRUISER_ATX_LASER_BATTERY}, self.player)
            )
            and (
                state.has_all({item_names.BATTLECRUISER, item_names.BATTLECRUISER_ATX_LASER_BATTERY}, self.player)
                or state.has(item_names.VALKYRIE, self.player)
            )
            and self.terran_very_hard_mission_weapon_armor_level(state)
        )

    def zerg_steps_of_the_rite_requirement(self, state: CollectionState) -> bool:
        return (
            self.zerg_competent_comp(state)
            and self.zerg_competent_anti_air(state)
            and (
                self.morph_lurker(state)
                or self.zerg_infested_siege_tanks_with_ammo(state)
                or state.has_all({item_names.INFESTED_LIBERATOR, item_names.INFESTED_LIBERATOR_DEFENDER_MODE}, self.player)
                or (
                    state.has(item_names.SWARM_QUEEN, self.player)
                    and self.zerg_big_monsters(state)
                )
            )
            and (
                state.has(item_names.INFESTED_LIBERATOR, self.player)
                or state.has_all({item_names.MUTALISK, item_names.MUTALISK_SEVERING_GLAIVE, item_names.MUTALISK_VICIOUS_GLAIVE}, self.player)
                or (
                    state.has(item_names.MUTALISK, self.player)
                    and self.morph_devourer(state)
                )
            )
        )

    def terran_rak_shir_requirement(self, state: CollectionState) -> bool:
        return (
            self.terran_beats_protoss_deathball(state)
            and self.terran_very_hard_mission_weapon_armor_level(state)
            and (
                state.has_any({item_names.SIEGE_TANK, item_names.LIBERATOR}, self.player)
                or state.has_all({item_names.BATTLECRUISER, item_names.BATTLECRUISER_ATX_LASER_BATTERY}, self.player)
            )
            and (
                self.terran_air_anti_air(state)
                or state.has(item_names.SKY_FURY, self.player)
            )
        )

    def zerg_rak_shir_requirement(self, state: CollectionState) -> bool:
        return (
            self.zerg_competent_comp(state)
            and self.zerg_competent_anti_air(state)
            and (
                self.zerg_big_monsters(state)
                or state.has_all({item_names.INFESTED_LIBERATOR, item_names.INFESTED_LIBERATOR_DEFENDER_MODE}, self.player)
                or self.morph_impaler_or_lurker(state)
            )
            and (
                state.has_all({item_names.INFESTED_LIBERATOR, item_names.INFESTED_LIBERATOR_CLOUD_DISPERSAL}, self.player)
                or (
                    state.has(item_names.MUTALISK, self.player)
                    and (
                        state.has(item_names.MUTALISK_SUNDERING_GLAIVE, self.player)
                        or self.morph_devourer(state)
                    )
                )
                or (
                    self.advanced_tactics and state.has(item_names.INFESTOR, self.player)
                )
            )
        )

    def protoss_templars_charge_requirement(self, state: CollectionState) -> bool:
        return (
            self.protoss_heal(state)
            and self.protoss_anti_armor_anti_air(state)
            and (
                self.protoss_fleet(state)
                or (self.advanced_tactics
                    and self.protoss_competent_comp(state)
                )
            )
        )

    def terran_templars_charge_requirement(self, state: CollectionState) -> bool:
        return (
                self.terran_very_hard_mission_weapon_armor_level(state)
                and (
                        (
                                state.has_all({item_names.BATTLECRUISER, item_names.BATTLECRUISER_ATX_LASER_BATTERY},
                                              self.player)
                                and state.count(item_names.BATTLECRUISER_PROGRESSIVE_DEFENSIVE_MATRIX, self.player) >= 2
                        ) or (
                                self.terran_air_anti_air(state)
                                and self.terran_sustainable_mech_heal(state)
                                and (
                                        state.has_any({item_names.BANSHEE, item_names.BATTLECRUISER}, self.player)
                                        or state.has_all({item_names.LIBERATOR, item_names.LIBERATOR_RAID_ARTILLERY},
                                                         self.player)
                                        or (
                                                self.advanced_tactics
                                                and (
                                                        state.has_all({
                                                            item_names.WRAITH,
                                                            item_names.WRAITH_ADVANCED_LASER_TECHNOLOGY
                                                        },
                                                            self.player)
                                                        or state.has_all({item_names.SIEGE_TANK, item_names.SIEGE_TANK_JUMP_JETS},
                                                    self.player)
                                                )
                                        )
                                )
                        )
                )
        )

    def zerg_templars_charge_requirement(self, state: CollectionState) -> bool:
        return (
                self.zerg_competent_comp(state)
                and self.zerg_competent_anti_air(state)
                and state.has(item_names.SWARM_QUEEN, self.player)
                and (
                        self.morph_guardian(state)
                        or self.morph_brood_lord(state)
                        or state.has(item_names.INFESTED_BANSHEE, self.player)
                        or (
                                self.advanced_tactics
                                and state.has_all({item_names.MUTALISK, item_names.MUTALISK_SEVERING_GLAIVE, item_names.MUTALISK_VICIOUS_GLAIVE, item_names.MUTALISK_AERODYNAMIC_GLAIVE_SHAPE}, self.player)
                        )
                ) and (
                        state.has_all({item_names.INFESTED_LIBERATOR, item_names.INFESTED_LIBERATOR_CLOUD_DISPERSAL}, self.player)
                        or (
                                self.morph_devourer(state)
                                and state.has(item_names.MUTALISK, self.player)
                        )
                        or state.has_all({item_names.MUTALISK, item_names.MUTALISK_SUNDERING_GLAIVE}, self.player)
                )
        )

    def protoss_the_host_requirement(self, state: CollectionState) -> bool:
        return (
            (
                    self.protoss_fleet(state)
                    and self.protoss_static_defense(state)
                    and self.protoss_army_weapon_armor_upgrade_min_level(state) >= 2
            )
            or (
                self.protoss_competent_comp(state)
                and state.has(item_names.SOA_TIME_STOP, self.player)
            )
        )

    def terran_the_host_requirement(self, state: CollectionState) -> bool:
        return (
            self.terran_beats_protoss_deathball(state)
            and self.terran_very_hard_mission_weapon_armor_level(state)
            and self.terran_air_anti_air(state)
            and state.has_any({item_names.THOR, item_names.SIEGE_TANK, item_names.BATTLECRUISER, item_names.BANSHEE, item_names.LIBERATOR}, self.player)
            and (self.advanced_tactics or self.terran_sustainable_mech_heal(state))
        )

    def zerg_the_host_requirement(self, state: CollectionState) -> bool:
        return (
            self.zerg_competent_comp(state)
            and self.zerg_competent_anti_air(state)
            and self.zerg_very_hard_mission_weapon_armor_level(state)
            and self.zerg_base_buster(state)
            and self.zerg_big_monsters(state)
            and (
                self.advanced_tactics or self.zerg_versatile_air(state)
            )
        )

    def protoss_salvation_requirement(self, state: CollectionState) -> bool:
        return (
                [
                    self.protoss_competent_comp(state),
                    self.protoss_fleet(state),
                    self.protoss_static_defense(state)
                ].count(True) >= 2
        ) and self.protoss_very_hard_mission_weapon_armor_level(state)

    def terran_salvation_requirement(self, state: CollectionState) -> bool:
        return (
            self.terran_beats_protoss_deathball(state)
            and self.terran_very_hard_mission_weapon_armor_level(state)
            and self.terran_air_anti_air(state)
            and state.has_any({item_names.SIEGE_TANK, item_names.LIBERATOR}, self.player)
            and state.has_any({item_names.PERDITION_TURRET, item_names.DEVASTATOR_TURRET, item_names.PLANETARY_FORTRESS}, self.player)
        )

    def zerg_salvation_requirement(self, state: CollectionState) -> bool:
        return (
            self.zerg_competent_comp(state)
            and self.zerg_competent_anti_air(state)
            and self.zerg_very_hard_mission_weapon_armor_level(state)
            and (
                self.morph_impaler_or_lurker(state)
                or state.has_all({item_names.INFESTED_LIBERATOR, item_names.INFESTED_LIBERATOR_DEFENDER_MODE}, self.player)
                or state.has_all({item_names.MUTALISK, item_names.MUTALISK_SEVERING_GLAIVE, item_names.MUTALISK_VICIOUS_GLAIVE}, self.player)
            )
            and (
                state.has_all({item_names.INFESTED_LIBERATOR, item_names.INFESTED_LIBERATOR_CLOUD_DISPERSAL}, self.player)
                or (
                    self.morph_devourer(state)
                    and state.has(item_names.MUTALISK, self.player)
                )
                or state.has_all({item_names.MUTALISK, item_names.MUTALISK_SUNDERING_GLAIVE}, self.player)
            )
        )

    def into_the_void_requirement(self, state: CollectionState) -> bool:
        if not self.protoss_very_hard_mission_weapon_armor_level(state):
            return False
        if self.take_over_ai_allies and not (
            self.terran_very_hard_mission_weapon_armor_level(state)
            and self.zerg_very_hard_mission_weapon_armor_level(state)
        ):
            return False
        return (self.protoss_competent_comp(state)
            or (
                self.take_over_ai_allies
                and (
                    state.has(item_names.BATTLECRUISER, self.player)
                    or (state.has(item_names.ULTRALISK, self.player)
                        and self.protoss_competent_anti_air(state)
                    )
                )
            )
        )

    def essence_of_eternity_requirement(self, state: CollectionState) -> bool:
        if not self.terran_very_hard_mission_weapon_armor_level(state):
            return False
        if self.take_over_ai_allies and not (
                self.protoss_very_hard_mission_weapon_armor_level(state)
                and self.zerg_very_hard_mission_weapon_armor_level(state)
        ):
            return False
        defense_score = self.terran_defense_rating(state, False, True)
        if self.take_over_ai_allies and self.protoss_static_defense(state):
            defense_score += 2
        return (
            defense_score >= 10
            and (
                self.terran_competent_anti_air(state)
                or self.take_over_ai_allies and self.protoss_competent_anti_air(state)
            )
            and (
                state.has(item_names.BATTLECRUISER, self.player)
                or (state.has(item_names.BANSHEE, self.player)
                    and state.has_any({item_names.VIKING, item_names.VALKYRIE}, self.player)
                )
                or self.take_over_ai_allies and self.protoss_fleet(state)
            )
            and state.has_any({item_names.SIEGE_TANK, item_names.LIBERATOR}, self.player)
        )

    def amons_fall_requirement(self, state: CollectionState) -> bool:
        if not self.zerg_very_hard_mission_weapon_armor_level(state):
            return False
        if self.take_over_ai_allies and not (
                self.terran_very_hard_mission_weapon_armor_level(state)
                and self.protoss_very_hard_mission_weapon_armor_level(state)
        ):
            return False
        if self.take_over_ai_allies:
            return (
                (
                    state.has_any({item_names.BATTLECRUISER, item_names.CARRIER, item_names.SKYLORD, item_names.TRIREME}, self.player)
                    or (state.has(item_names.ULTRALISK, self.player)
                        and self.protoss_competent_anti_air(state)
                        and (
                            state.has_any({item_names.LIBERATOR, item_names.BANSHEE, item_names.VALKYRIE, item_names.VIKING}, self.player)
                            or state.has_all({item_names.WRAITH, item_names.WRAITH_ADVANCED_LASER_TECHNOLOGY}, self.player)
                            or self.protoss_fleet(state)
                        )
                        and (self.terran_sustainable_mech_heal(state)
                            or (self.spear_of_adun_autonomously_cast_presence == SpearOfAdunAutonomouslyCastAbilityPresence.option_everywhere
                                 and state.has(item_names.RECONSTRUCTION_BEAM, self.player)
                            )
                        )
                    )
                )
                and self.terran_competent_anti_air(state)
                and self.protoss_competent_comp(state)
                and self.zerg_competent_comp(state)
            )
        else:
            return state.has(item_names.MUTALISK, self.player) and self.zerg_competent_comp(state)

    def nova_any_weapon(self, state: CollectionState) -> bool:
        return state.has_any({
            item_names.NOVA_C20A_CANISTER_RIFLE, item_names.NOVA_HELLFIRE_SHOTGUN, item_names.NOVA_PLASMA_RIFLE,
            item_names.NOVA_MONOMOLECULAR_BLADE, item_names.NOVA_BLAZEFIRE_GUNBLADE
        }, self.player)

    def nova_ranged_weapon(self, state: CollectionState) -> bool:
        return state.has_any({
            item_names.NOVA_C20A_CANISTER_RIFLE, item_names.NOVA_HELLFIRE_SHOTGUN, item_names.NOVA_PLASMA_RIFLE
        }, self.player)

    def nova_splash(self, state: CollectionState) -> bool:
        return (
            state.has_any({
                item_names.NOVA_HELLFIRE_SHOTGUN, item_names.NOVA_BLAZEFIRE_GUNBLADE, item_names.NOVA_PULSE_GRENADES
            }, self.player)
            or (self.advanced_tactics
                and state.has_any({item_names.NOVA_PLASMA_RIFLE, item_names.NOVA_MONOMOLECULAR_BLADE}, self.player)
            )
        )

    def nova_dash(self, state: CollectionState) -> bool:
        return state.has_any({item_names.NOVA_MONOMOLECULAR_BLADE, item_names.NOVA_BLINK}, self.player)

    def nova_full_stealth(self, state: CollectionState) -> bool:
        return state.count(item_names.NOVA_PROGRESSIVE_STEALTH_SUIT_MODULE, self.player) >= 2

    def nova_heal(self, state: CollectionState) -> bool:
        return state.has_any({item_names.NOVA_ARMORED_SUIT_MODULE, item_names.NOVA_STIM_INFUSION}, self.player)

    def nova_escape_assist(self, state: CollectionState) -> bool:
        return state.has_any({item_names.NOVA_BLINK, item_names.NOVA_HOLO_DECOY, item_names.NOVA_IONIC_FORCE_FIELD}, self.player)

    def the_escape_stuff_granted(self) -> bool:
        """
        The NCO first mission requires having too much stuff first before actually able to do anything
        :return:
        """
        return (
            self.story_tech_granted
            or (self.mission_order == MissionOrder.option_vanilla and self.enabled_campaigns == {SC2Campaign.NCO})
        )

    def the_escape_first_stage_requirement(self, state: CollectionState) -> bool:
        return (
            self.the_escape_stuff_granted()
            or (self.nova_ranged_weapon(state) and (self.nova_full_stealth(state) or self.nova_heal(state)))
        )

    def the_escape_requirement(self, state: CollectionState) -> bool:
        return (
            self.the_escape_first_stage_requirement(state)
            and (self.the_escape_stuff_granted() or self.nova_splash(state))
        )

    def terran_cliffjumper(self, state: CollectionState) -> bool:
        return (
            state.has(item_names.REAPER, self.player)
            or state.has_all({item_names.GOLIATH, item_names.GOLIATH_JUMP_JETS}, self.player)
            or state.has_all({item_names.SIEGE_TANK, item_names.SIEGE_TANK_JUMP_JETS}, self.player)
        )

    def terran_able_to_snipe_defiler(self, state: CollectionState) -> bool:
        return (
            state.has_all({item_names.NOVA_JUMP_SUIT_MODULE, item_names.NOVA_C20A_CANISTER_RIFLE}, self.player)
            or state.has_all({item_names.SIEGE_TANK, item_names.SIEGE_TANK_MAELSTROM_ROUNDS, item_names.SIEGE_TANK_JUMP_JETS}, self.player)
        )

    def sudden_strike_requirement(self, state: CollectionState) -> bool:
        return (
            self.sudden_strike_can_reach_objectives(state)
            and self.terran_able_to_snipe_defiler(state)
            and state.has_any({item_names.SIEGE_TANK, item_names.VULTURE}, self.player)
            and self.nova_splash(state)
            and (self.terran_defense_rating(state, True, False) >= 2
                 or state.has(item_names.NOVA_JUMP_SUIT_MODULE, self.player)
            )
        )

    def sudden_strike_can_reach_objectives(self, state: CollectionState) -> bool:
        return (
            self.terran_cliffjumper(state)
            or state.has_any({item_names.BANSHEE, item_names.VIKING}, self.player)
            or (
                self.advanced_tactics
                and state.has(item_names.MEDIVAC, self.player)
                and state.has_any({
                    item_names.MARINE, item_names.DOMINION_TROOPER, item_names.MARAUDER, item_names.VULTURE, item_names.HELLION, item_names.GOLIATH
                }, self.player)
            )
        )

    def enemy_intelligence_garrisonable_unit(self, state: CollectionState) -> bool:
        """
        Has unit usable as a Garrison in Enemy Intelligence
        """
        return state.has_any({
            item_names.MARINE, item_names.REAPER, item_names.MARAUDER, item_names.GHOST, item_names.SPECTRE,
            item_names.HELLION, item_names.GOLIATH, item_names.WARHOUND, item_names.DIAMONDBACK, item_names.VIKING
        }, self.player)

    def enemy_intelligence_cliff_garrison(self, state: CollectionState) -> bool:
        return (
            state.has_any({item_names.REAPER, item_names.VIKING, item_names.MEDIVAC, item_names.HERCULES}, self.player)
            or state.has_all({item_names.GOLIATH, item_names.GOLIATH_JUMP_JETS}, self.player)
            or (self.advanced_tactics
                and state.has_any({item_names.HELS_ANGELS, item_names.BRYNHILDS}, self.player)
            )
        )

    def enemy_intelligence_first_stage_requirement(self, state: CollectionState) -> bool:
        return (
            self.enemy_intelligence_garrisonable_unit(state)
            and (self.terran_competent_comp(state)
                or (self.terran_common_unit(state)
                    and self.terran_competent_anti_air(state)
                    and state.has(item_names.NOVA_NUKE, self.player)
                )
            )
            and self.terran_defense_rating(state, True, True) >= 5
        )

    def enemy_intelligence_second_stage_requirement(self, state: CollectionState) -> bool:
        return (
            self.enemy_intelligence_first_stage_requirement(state)
            and self.enemy_intelligence_cliff_garrison(state)
            and (
                self.story_tech_granted
                or (
                    self.nova_any_weapon(state)
                    and (
                        self.nova_full_stealth(state)
                        or (self.nova_heal(state)
                            and self.nova_splash(state)
                            and self.nova_ranged_weapon(state)
                        )
                    )
                )
            )
        )

    def enemy_intelligence_third_stage_requirement(self, state: CollectionState) -> bool:
        return (
            self.enemy_intelligence_second_stage_requirement(state)
            and (
                self.story_tech_granted
                or (
                    state.has(item_names.NOVA_PROGRESSIVE_STEALTH_SUIT_MODULE, self.player)
                    and self.nova_dash(state)
                )
            )
        )

    def trouble_in_paradise_requirement(self, state: CollectionState) -> bool:
        return (
            self.nova_any_weapon(state)
            and self.nova_splash(state)
            and self.terran_beats_protoss_deathball(state)
            and self.terran_defense_rating(state, True, True) >= 7
        )

    def night_terrors_requirement(self, state: CollectionState) -> bool:
        return (
                self.terran_common_unit(state)
                and self.terran_competent_anti_air(state)
                and (
                # These can handle the waves of infested, even volatile ones
                state.has(item_names.SIEGE_TANK, self.player)
                or state.has_all({item_names.VIKING, item_names.VIKING_SHREDDER_ROUNDS}, self.player)
                or (
                    (
                        # Regular infesteds
                        state.has(item_names.FIREBAT, self.player)
                        or state.has_all({item_names.HELLION, item_names.HELLION_HELLBAT_ASPECT}, self.player)
                        or (
                            self.advanced_tactics
                            and state.has_any({item_names.PERDITION_TURRET, item_names.PLANETARY_FORTRESS}, self.player)
                        )
                    )
                    and self.terran_bio_heal(state)
                    and (
                        # Volatile infesteds
                        state.has(item_names.LIBERATOR, self.player)
                        or (
                            self.advanced_tactics
                            and state.has_any({item_names.HERC, item_names.VULTURE}, self.player)
                        )
                    )
                )
            )
                and self.terran_army_weapon_armor_upgrade_min_level(state) >= 2
        )

    def flashpoint_far_requirement(self, state: CollectionState) -> bool:
        return (
                self.terran_competent_comp(state)
                and self.terran_mobile_detector(state)
                and self.terran_defense_rating(state, True, False) >= 6
                and self.terran_army_weapon_armor_upgrade_min_level(state) >= 2
        )

    def enemy_shadow_tripwires_tool(self, state: CollectionState) -> bool:
        return state.has_any({
            item_names.NOVA_FLASHBANG_GRENADES, item_names.NOVA_BLINK, item_names.NOVA_DOMINATION
        }, self.player)

    def enemy_shadow_door_unlocks_tool(self, state: CollectionState) -> bool:
        return state.has_any({
            item_names.NOVA_DOMINATION, item_names.NOVA_BLINK, item_names.NOVA_JUMP_SUIT_MODULE
        }, self.player)

    def enemy_shadow_domination(self, state: CollectionState) -> bool:
        return (
            self.story_tech_granted
            or (self.nova_ranged_weapon(state)
                and (self.nova_full_stealth(state)
                    or state.has(item_names.NOVA_JUMP_SUIT_MODULE, self.player)
                    or (self.nova_heal(state) and self.nova_splash(state))
                )
            )
        )

    def enemy_shadow_first_stage(self, state: CollectionState) -> bool:
        return (
            self.enemy_shadow_domination(state)
            and (self.story_tech_granted
                 or ((self.nova_full_stealth(state) and self.enemy_shadow_tripwires_tool(state))
                    or (self.nova_heal(state) and self.nova_splash(state))
                )
            )
        )

    def enemy_shadow_second_stage(self, state: CollectionState) -> bool:
        return (
            self.enemy_shadow_first_stage(state)
            and (self.story_tech_granted
                 or self.nova_splash(state)
                 or self.nova_heal(state)
                 or self.nova_escape_assist(state)
            )
        )

    def enemy_shadow_door_controls(self, state: CollectionState) -> bool:
        return (
            self.enemy_shadow_second_stage(state)
            and (self.story_tech_granted or self.enemy_shadow_door_unlocks_tool(state))
        )

    def enemy_shadow_victory(self, state: CollectionState) -> bool:
        return (
            self.enemy_shadow_door_controls(state)
            and (self.story_tech_granted or self.nova_heal(state))
        )

    def dark_skies_requirement(self, state: CollectionState) -> bool:
        return (
            self.terran_common_unit(state)
            and self.terran_beats_protoss_deathball(state)
            and self.terran_defense_rating(state, False, True) >= 8
        )

    def end_game_requirement(self, state: CollectionState) -> bool:
        return (
            self.terran_competent_comp(state)
            and self.terran_mobile_detector(state)
            and (
                state.has_any({item_names.BATTLECRUISER, item_names.LIBERATOR, item_names.BANSHEE}, self.player)
                or state.has_all({item_names.WRAITH, item_names.WRAITH_ADVANCED_LASER_TECHNOLOGY}, self.player)
            )
            and (state.has_any({item_names.BATTLECRUISER, item_names.VIKING, item_names.LIBERATOR}, self.player)
                or (self.advanced_tactics
                    and state.has_all({item_names.RAVEN, item_names.RAVEN_HUNTER_SEEKER_WEAPON}, self.player)
                )
            )
            and self.terran_very_hard_mission_weapon_armor_level(state)
        )

    def __init__(self, world: Optional['SC2World']):
        self.world = world
        self.player = -1 if world is None else world.player
        self.logic_level: int = world.options.required_tactics.value if world else RequiredTactics.default
        self.advanced_tactics = self.logic_level != RequiredTactics.option_standard
        self.take_over_ai_allies = bool(world and world.options.take_over_ai_allies)
        self.kerrigan_unit_available = (
            get_option_value(world, 'kerrigan_presence') in kerrigan_unit_available
            and SC2Campaign.HOTS in get_enabled_campaigns(world)
            and SC2Race.ZERG in get_enabled_races(world)
        )
        self.kerrigan_levels_per_mission_completed = get_option_value(world, "kerrigan_levels_per_mission_completed")
        self.kerrigan_levels_per_mission_completed_cap = get_option_value(world, "kerrigan_levels_per_mission_completed_cap")
        self.kerrigan_total_level_cap = get_option_value(world, "kerrigan_total_level_cap")
        self.morphling_enabled = get_option_value(world, "enable_morphling") == EnableMorphling.option_true
        self.story_tech_granted = get_option_value(world, "grant_story_tech") == GrantStoryTech.option_true
        self.story_levels_granted = get_option_value(world, "grant_story_levels") != GrantStoryLevels.option_disabled
        self.basic_terran_units = get_basic_units(self.logic_level, SC2Race.TERRAN)
        self.basic_zerg_units = get_basic_units(self.logic_level, SC2Race.ZERG)
        self.basic_protoss_units = get_basic_units(self.logic_level, SC2Race.PROTOSS)
        self.spear_of_adun_autonomously_cast_presence = get_option_value(world, "spear_of_adun_autonomously_cast_ability_presence")
        self.enabled_campaigns = get_enabled_campaigns(world)
        self.mission_order = get_option_value(world, "mission_order")
        self.generic_upgrade_missions = get_option_value(world, "generic_upgrade_missions")


def get_basic_units(logic_level: int, race: SC2Race) -> Set[str]:
    if logic_level == RequiredTactics.option_no_logic:
        return no_logic_basic_units[race]
    elif logic_level == RequiredTactics.option_advanced:
        return advanced_basic_units[race]
    else:
        return basic_units[race]


def has_terran_units(player: int, target: int) -> Callable[['CollectionState'], bool]:
    def _has_terran_units(state: CollectionState) -> bool:
        return (
            state.count_from_list_unique(item_groups.terran_units + item_groups.terran_buildings, player) >= target
        )
    return _has_terran_units


def has_zerg_units(player: int, target: int) -> Callable[['CollectionState'], bool]:
    def _has_zerg_units(state: CollectionState) -> bool:
        return (
            state.count_from_list_unique(item_groups.zerg_units + item_groups.zerg_buildings, player) >= target
        )
    return _has_zerg_units


def has_protoss_units(player: int, target: int) -> Callable[['CollectionState'], bool]:
    def _has_protoss_units(state: CollectionState) -> bool:
        return (
            state.count_from_list_unique(item_groups.protoss_units + item_groups.protoss_buildings, player) >= target
        )
    return _has_protoss_units


def has_race_units(player: int, target: int, race: SC2Race) -> Callable[['CollectionState'], bool]:
    if race == SC2Race.TERRAN:
        return has_terran_units(player, target)
    if race == SC2Race.ZERG:
        return has_zerg_units(player, target)
    if race == SC2Race.PROTOSS:
        return has_protoss_units(player, target)
    return Location.access_rule
