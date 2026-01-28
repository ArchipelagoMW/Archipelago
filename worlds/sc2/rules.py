from math import floor
from typing import TYPE_CHECKING, Set, Optional, Callable, Dict, Tuple, Iterable

from BaseClasses import CollectionState, Location
from .item.item_groups import kerrigan_non_ulimates, kerrigan_logic_active_abilities
from .item.item_names import PROGRESSIVE_PROTOSS_AIR_WEAPON, PROGRESSIVE_PROTOSS_AIR_ARMOR, PROGRESSIVE_PROTOSS_SHIELDS
from .options import (
    RequiredTactics,
    kerrigan_unit_available,
    AllInMap,
    GrantStoryTech,
    GrantStoryLevels,
    SpearOfAdunPassiveAbilityPresence,
    SpearOfAdunPresence,
    MissionOrder,
    EnableMorphling,
    NovaGhostOfAChanceVariant,
    get_enabled_campaigns,
    get_enabled_races,
)
from .item.item_tables import (
    kerrigan_levels,
    get_full_item_list,
    no_logic_basic_units,
    advanced_basic_units,
    basic_units,
    upgrade_bundle_inverted_lookup,
    WEAPON_ARMOR_UPGRADE_MAX_LEVEL,
)
from .mission_tables import SC2Race, SC2Campaign
from .item import item_groups, item_names

if TYPE_CHECKING:
    from . import SC2World


def min2(a: int, b: int) -> int:
    """`min()` that only takes two values; faster than baseline int by about 2x"""
    if a <= b:
        return a
    return b


class SC2Logic:
    def __init__(self, world: Optional["SC2World"]) -> None:
        # Note: Don't store a reference to the world so we can cache this object on the world object
        self.player = -1 if world is None else world.player
        self.logic_level: int = world.options.required_tactics.value if world else RequiredTactics.default
        self.advanced_tactics = self.logic_level != RequiredTactics.option_standard
        self.take_over_ai_allies = bool(world and world.options.take_over_ai_allies)
        self.kerrigan_unit_available = (
            (True if world is None else (world.options.kerrigan_presence.value in kerrigan_unit_available))
            and SC2Campaign.HOTS in get_enabled_campaigns(world)
            and SC2Race.ZERG in get_enabled_races(world)
        )
        self.kerrigan_levels_per_mission_completed = 0 if world is None else world.options.kerrigan_levels_per_mission_completed.value
        self.kerrigan_levels_per_mission_completed_cap = -1 if world is None else world.options.kerrigan_levels_per_mission_completed_cap.value
        self.kerrigan_total_level_cap = -1 if world is None else world.options.kerrigan_total_level_cap.value
        self.morphling_enabled = False if world is None else (world.options.enable_morphling.value == EnableMorphling.option_true)
        self.grant_story_tech = GrantStoryTech.option_no_grant if world is None else (world.options.grant_story_tech.value)
        self.story_levels_granted = False if world is None else (world.options.grant_story_levels.value != GrantStoryLevels.option_disabled)
        self.basic_terran_units = get_basic_units(self.logic_level, SC2Race.TERRAN)
        self.basic_zerg_units = get_basic_units(self.logic_level, SC2Race.ZERG)
        self.basic_protoss_units = get_basic_units(self.logic_level, SC2Race.PROTOSS)
        self.spear_of_adun_presence = SpearOfAdunPresence.default if world is None else world.options.spear_of_adun_presence.value
        self.spear_of_adun_passive_presence = (
            SpearOfAdunPassiveAbilityPresence.default if world is None else world.options.spear_of_adun_passive_ability_presence.value
        )
        self.enabled_campaigns = get_enabled_campaigns(world)
        self.mission_order = MissionOrder.default if world is None else world.options.mission_order.value
        self.generic_upgrade_missions = 0 if world is None else world.options.generic_upgrade_missions.value
        self.all_in_map = AllInMap.option_ground if world is None else world.options.all_in_map.value
        self.nova_ghost_of_a_chance_variant = NovaGhostOfAChanceVariant.option_wol if world is None else world.options.nova_ghost_of_a_chance_variant.value
        self.war_council_upgrades = True if world is None else not world.options.war_council_nerfs.value
        self.base_power_rating = 2 if self.advanced_tactics else 0

        # Must be set externally for accurate logic checking of upgrade level when generic_upgrade_missions is checked
        self.total_mission_count = 1

        # Must be set externally
        self.nova_used = True

        # Conditionally set to False by the world after culling items
        self.has_barracks_unit: bool = True
        self.has_factory_unit: bool = True
        self.has_starport_unit: bool = True
        self.has_zerg_melee_unit: bool = True
        self.has_zerg_ranged_unit: bool = True
        self.has_zerg_air_unit: bool = True
        self.has_protoss_ground_unit: bool = True
        self.has_protoss_air_unit: bool = True

        self.unit_count_functions: Dict[Tuple[SC2Race, int], Callable[[CollectionState], bool]] = {}
        """Cache of logic functions used by any_units logic level"""

    # Super Globals

    def is_item_placement(self, state: CollectionState) -> bool:
        """
        Tells if it's item placement or item pool filter
        :return: True for item placement, False for pool filter
        """
        # has_group with count = 0 is always true for item placement and always false for SC2 item filtering
        return state.has_group("Missions", self.player, 0)

    def get_very_hard_required_upgrade_level(self) -> int:
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
                count += floor((100 / self.generic_upgrade_missions) * (state.count_group("Missions", self.player) / self.total_mission_count))
        count += state.count(upgrade_item, self.player)
        count += state.count_from_list(upgrade_bundle_inverted_lookup[upgrade_item], self.player)
        if upgrade_item == item_names.PROGRESSIVE_PROTOSS_SHIELDS:
            count += max(
                state.count(item_names.PROGRESSIVE_PROTOSS_GROUND_UPGRADE, self.player),
                state.count(item_names.PROGRESSIVE_PROTOSS_AIR_UPGRADE, self.player),
            )
        if upgrade_item in item_groups.protoss_generic_upgrades and state.has(item_names.QUATRO, self.player):
            count += 1
        return count

    def soa_power_rating(self, state: CollectionState) -> int:
        power_rating = 0
        # Spear of Adun Ultimates (Strongest)
        for item, rating in soa_ultimate_ratings.items():
            if state.has(item, self.player):
                power_rating += rating
                break
        # Spear of Adun ability that consumes energy (Strongest, then second strongest)
        found_main_weapon = False
        for item, rating in soa_energy_ratings.items():
            count = 1
            if item == item_names.SOA_PROGRESSIVE_PROXY_PYLON:
                count = 2
            if state.has(item, self.player, count):
                if not found_main_weapon:
                    power_rating += rating
                    found_main_weapon = True
                else:
                    power_rating += rating // 2
                    break
        # Mass Recall (Negligible energy cost)
        if state.has(item_names.SOA_MASS_RECALL, self.player):
            power_rating += 2
        return power_rating

    # Global Terran

    def terran_power_rating(self, state: CollectionState) -> int:
        power_score = self.base_power_rating
        # Passive Score (Economic upgrades and global army upgrades)
        power_score += sum((rating for item, rating in terran_passive_ratings.items() if state.has(item, self.player)))
        # Spear of Adun
        if self.spear_of_adun_presence == SpearOfAdunPresence.option_everywhere:
            power_score += self.soa_power_rating(state)
        if self.spear_of_adun_passive_presence == SpearOfAdunPassiveAbilityPresence.option_everywhere:
            power_score += sum((rating for item, rating in soa_passive_ratings.items() if state.has(item, self.player)))
        return power_score

    def terran_army_weapon_armor_upgrade_min_level(self, state: CollectionState) -> int:
        """
        Minimum W/A upgrade level for unit classes present in the world
        """
        count: int = WEAPON_ARMOR_UPGRADE_MAX_LEVEL
        if self.has_barracks_unit:
            count = min(
                count,
                self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_TERRAN_INFANTRY_WEAPON, state),
                self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_TERRAN_INFANTRY_ARMOR, state),
            )
        if self.has_factory_unit:
            count = min(
                count,
                self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_TERRAN_VEHICLE_WEAPON, state),
                self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_TERRAN_VEHICLE_ARMOR, state),
            )
        if self.has_starport_unit:
            count = min(
                count,
                self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_TERRAN_SHIP_WEAPON, state),
                self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_TERRAN_SHIP_ARMOR, state),
            )
        return count

    def terran_very_hard_mission_weapon_armor_level(self, state: CollectionState) -> bool:
        return self.terran_army_weapon_armor_upgrade_min_level(state) >= self.get_very_hard_required_upgrade_level()

    # WoL
    def terran_common_unit(self, state: CollectionState) -> bool:
        return state.has_any(self.basic_terran_units, self.player)

    def terran_early_tech(self, state: CollectionState) -> bool:
        """
        Basic combat unit that can be deployed quickly from mission start
        :param state
        :return:
        """
        return state.has_any(
            {item_names.MARINE, item_names.DOMINION_TROOPER, item_names.FIREBAT, item_names.MARAUDER, item_names.REAPER, item_names.HELLION},
            self.player,
        ) or (
            self.advanced_tactics and state.has_any({item_names.GOLIATH, item_names.DIAMONDBACK, item_names.VIKING, item_names.BANSHEE}, self.player)
        )

    def terran_air(self, state: CollectionState) -> bool:
        """
        Air units or drops on advanced tactics
        """
        return (
            state.has_any({item_names.VIKING, item_names.WRAITH, item_names.BANSHEE, item_names.BATTLECRUISER}, self.player)
            or state.has_all((item_names.VALKYRIE, item_names.VALKYRIE_FLECHETTE_MISSILES), self.player)
            or state.has_all((item_names.LIBERATOR, item_names.LIBERATOR_RAID_ARTILLERY), self.player)
            or (
                self.advanced_tactics
                and (
                    (state.has_any({item_names.HERCULES, item_names.MEDIVAC}, self.player) and self.terran_common_unit(state))
                    or (state.has_all((item_names.RAVEN, item_names.RAVEN_HUNTER_SEEKER_WEAPON), self.player))
                )
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
        return state.has_any((
            item_names.VIKING,
            item_names.MEDIVAC,
            item_names.RAVEN,
            item_names.BANSHEE,
            item_names.SCIENCE_VESSEL,
            item_names.BATTLECRUISER,
            item_names.WRAITH,
            item_names.HERCULES,
            item_names.LIBERATOR,
            item_names.VALKYRIE,
            item_names.SKY_FURY,
            item_names.NIGHT_HAWK,
            item_names.EMPERORS_GUARDIAN,
            item_names.NIGHT_WOLF,
            item_names.PRIDE_OF_AUGUSTRGRAD,
        ), self.player)

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
            or (
                self.advanced_tactics
                and (
                    state.has(item_names.CYCLONE, self.player)
                    or state.has_all((item_names.THOR, item_names.THOR_PROGRESSIVE_HIGH_IMPACT_PAYLOAD), self.player)
                )
            )
        )

    def terran_competent_anti_air(self, state: CollectionState) -> bool:
        """
        Good AA unit
        """
        return self.terran_competent_ground_to_air(state) or self.terran_air_anti_air(state)

    def terran_any_anti_air(self, state: CollectionState) -> bool:
        return (
            state.has_any(
                (
                    # Barracks
                    item_names.MARINE,
                    item_names.WAR_PIGS,
                    item_names.SON_OF_KORHAL,
                    item_names.DOMINION_TROOPER,
                    item_names.GHOST,
                    item_names.SPECTRE,
                    item_names.EMPERORS_SHADOW,
                    # Factory
                    item_names.GOLIATH,
                    item_names.SPARTAN_COMPANY,
                    item_names.BULWARK_COMPANY,
                    item_names.CYCLONE,
                    item_names.WIDOW_MINE,
                    item_names.THOR,
                    item_names.JOTUN,
                    item_names.BLACKHAMMER,
                    # Ships
                    item_names.WRAITH,
                    item_names.WINGED_NIGHTMARES,
                    item_names.NIGHT_HAWK,
                    item_names.VIKING,
                    item_names.HELS_ANGELS,
                    item_names.SKY_FURY,
                    item_names.LIBERATOR,
                    item_names.MIDNIGHT_RIDERS,
                    item_names.EMPERORS_GUARDIAN,
                    item_names.VALKYRIE,
                    item_names.BRYNHILDS,
                    item_names.BATTLECRUISER,
                    item_names.JACKSONS_REVENGE,
                    item_names.PRIDE_OF_AUGUSTRGRAD,
                    item_names.RAVEN,
                    # Buildings
                    item_names.MISSILE_TURRET,
                ),
                self.player,
            )
            or state.has_all((item_names.REAPER, item_names.REAPER_JET_PACK_OVERDRIVE), self.player)
            or state.has_all((item_names.PLANETARY_FORTRESS, item_names.PLANETARY_FORTRESS_IBIKS_TRACKING_SCANNERS), self.player)
            or (
                state.has(item_names.MEDIVAC, self.player)
                and state.has_any((item_names.SIEGE_TANK, item_names.SIEGE_BREAKERS, item_names.SHOCK_DIVISION), self.player)
                and state.count(item_names.SIEGE_TANK_PROGRESSIVE_TRANSPORT_HOOK, self.player) >= 2
            )
        )

    def terran_any_anti_air_or_science_vessels(self, state: CollectionState) -> bool:
        return self.terran_any_anti_air(state) or state.has(item_names.SCIENCE_VESSEL, self.player)

    def terran_moderate_anti_air(self, state: CollectionState) -> bool:
        return self.terran_competent_anti_air(state) or (
            state.has_any(
                (
                    item_names.MARINE,
                    item_names.DOMINION_TROOPER,
                    item_names.THOR,
                    item_names.CYCLONE,
                    item_names.BATTLECRUISER,
                    item_names.WRAITH,
                    item_names.VALKYRIE,
                ),
                self.player,
            )
            or (
                state.has_all((item_names.MEDIVAC, item_names.SIEGE_TANK), self.player)
                and state.count(item_names.SIEGE_TANK_PROGRESSIVE_TRANSPORT_HOOK, self.player) >= 2
            )
            or (self.advanced_tactics and state.has_any((item_names.GHOST, item_names.SPECTRE, item_names.LIBERATOR), self.player))
        )

    def terran_basic_anti_air(self, state: CollectionState) -> bool:
        """
        Basic AA to deal with few air units
        """
        return (
            state.has_any((
                item_names.MISSILE_TURRET,
                item_names.WAR_PIGS,
                item_names.SPARTAN_COMPANY,
                item_names.HELS_ANGELS,
                item_names.WINGED_NIGHTMARES,
                item_names.BRYNHILDS,
                item_names.SKY_FURY,
                item_names.SON_OF_KORHAL,
                item_names.BULWARK_COMPANY,
            ), self.player)
            or self.terran_moderate_anti_air(state)
            or (self.advanced_tactics
                and (
                    state.has_any((
                        item_names.WIDOW_MINE,
                        item_names.PRIDE_OF_AUGUSTRGRAD,
                        item_names.BLACKHAMMER,
                        item_names.EMPERORS_SHADOW,
                        item_names.EMPERORS_GUARDIAN,
                        item_names.NIGHT_HAWK,
                    ), self.player)
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
        if (state.has_any((item_names.MARINE, item_names.DOMINION_TROOPER, item_names.MARAUDER), self.player)
            and state.has(item_names.BUNKER, self.player)
        ):
            defense_score += 3
        elif zerg_enemy and state.has(item_names.FIREBAT, self.player) and state.has(item_names.BUNKER, self.player):
            defense_score += 2
        # Siege Tank upgrades
        if state.has_all((item_names.SIEGE_TANK, item_names.SIEGE_TANK_MAELSTROM_ROUNDS), self.player):
            defense_score += 2
        if state.has_all((item_names.SIEGE_TANK, item_names.SIEGE_TANK_GRADUATING_RANGE), self.player):
            defense_score += 1
        # Widow Mine upgrade
        if state.has_all((item_names.WIDOW_MINE, item_names.WIDOW_MINE_CONCEALMENT), self.player):
            defense_score += 1
        # Viking with splash
        if state.has_all((item_names.VIKING, item_names.VIKING_SHREDDER_ROUNDS), self.player):
            defense_score += 2

        # General enemy-based rules
        if zerg_enemy:
            defense_score += sum((
                tvz_defense_ratings[item]
                for item in tvz_defense_ratings
                if state.has(item, self.player)
            ))
        if air_enemy:
            # Capped at 2
            defense_score += min2(
                2,
                sum((tvx_air_defense_ratings[item] for item in tvx_air_defense_ratings if state.has(item, self.player))),
            )
        if air_enemy and zerg_enemy and state.has(item_names.VALKYRIE, self.player):
            # Valkyries shred mass Mutas, the most common air enemy that's massed in these cases
            defense_score += 2
        # Advanced Tactics bumps defense rating requirements down by 2
        if self.advanced_tactics:
            defense_score += 2
        return defense_score

    def terran_competent_comp(self, state: CollectionState, upgrade_level: int = 1) -> bool:
        # All competent comps require anti-air
        if not self.terran_competent_anti_air(state):
            return False
        # Infantry with Healing
        infantry_weapons = self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_TERRAN_INFANTRY_WEAPON, state)
        infantry_armor = self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_TERRAN_INFANTRY_ARMOR, state)
        infantry = state.has_any((item_names.MARINE, item_names.DOMINION_TROOPER, item_names.MARAUDER), self.player)
        if (infantry_weapons >= upgrade_level + 1
            and infantry_armor >= upgrade_level
            and infantry
            and self.terran_bio_heal(state)
        ):
            return True
        # Mass Air-To-Ground
        ship_weapons = self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_TERRAN_SHIP_WEAPON, state)
        ship_armor = self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_TERRAN_SHIP_ARMOR, state)
        if ship_weapons >= upgrade_level and ship_armor >= upgrade_level:
            air = (
                state.has_any((item_names.BANSHEE, item_names.BATTLECRUISER), self.player)
                or state.has_all((item_names.LIBERATOR, item_names.LIBERATOR_RAID_ARTILLERY), self.player)
                or state.has_all((item_names.WRAITH, item_names.WRAITH_ADVANCED_LASER_TECHNOLOGY), self.player)
                or (state.has_all((item_names.VALKYRIE, item_names.VALKYRIE_FLECHETTE_MISSILES), self.player)
                    and ship_weapons >= 2
                )
            )
            if air and self.terran_mineral_dump(state):
                return True
        # Strong Mech
        vehicle_weapons = self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_TERRAN_VEHICLE_WEAPON, state)
        vehicle_armor = self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_TERRAN_VEHICLE_ARMOR, state)
        if vehicle_weapons >= upgrade_level and vehicle_armor >= upgrade_level:
            strong_vehicle = state.has_any({item_names.THOR, item_names.SIEGE_TANK}, self.player)
            light_frontline = state.has_any(
                {item_names.MARINE, item_names.DOMINION_TROOPER, item_names.HELLION, item_names.VULTURE}, self.player
            ) or state.has_all({item_names.REAPER, item_names.REAPER_RESOURCE_EFFICIENCY}, self.player)
            if strong_vehicle and light_frontline:
                return True
            # Mech with Healing
            vehicle = state.has_any({item_names.GOLIATH, item_names.WARHOUND}, self.player)
            micro_gas_vehicle = self.advanced_tactics and state.has_any({item_names.DIAMONDBACK, item_names.CYCLONE}, self.player)
            if self.terran_sustainable_mech_heal(state) and (vehicle or (micro_gas_vehicle and light_frontline)):
                return True
        return False

    def terran_mineral_dump(self, state: CollectionState) -> bool:
        """
        Can build something using only minerals
        """
        return (
            state.has_any((item_names.MARINE, item_names.VULTURE, item_names.HELLION, item_names.SON_OF_KORHAL), self.player)
            or state.has_all((item_names.REAPER, item_names.REAPER_RESOURCE_EFFICIENCY), self.player)
            or (self.advanced_tactics
                and state.has_any((item_names.PERDITION_TURRET, item_names.DEVASTATOR_TURRET), self.player)
            )
        )

    def terran_beats_protoss_deathball(self, state: CollectionState) -> bool:
        """
        Ability to deal with Immortals, Colossi with some air support
        """
        return (
            (
                (
                    state.has_any((item_names.BANSHEE, item_names.BATTLECRUISER), self.player)
                    or state.has_all((item_names.LIBERATOR, item_names.LIBERATOR_RAID_ARTILLERY), self.player)
                )
                and self.terran_competent_anti_air(state)
            )
            or (self.terran_competent_comp(state)
                and self.terran_air_anti_air(state)
            )
        ) and self.terran_army_weapon_armor_upgrade_min_level(state) >= 2

    def marine_medic_upgrade(self, state: CollectionState) -> bool:
        """
        Infantry upgrade to infantry-only no-build segments
        """
        return (
            state.has_any((
                item_names.MARINE_COMBAT_SHIELD,
                item_names.MARINE_MAGRAIL_MUNITIONS,
                item_names.MEDIC_STABILIZER_MEDPACKS,
            ), self.player)
            or (state.count(item_names.MARINE_PROGRESSIVE_STIMPACK, self.player) >= 2
                and state.has_group("Missions", self.player, 1)
            )
            or (self.advanced_tactics
                and state.has(item_names.MARINE_LASER_TARGETING_SYSTEM, self.player)
            )
        )

    def marine_medic_firebat_upgrade(self, state: CollectionState) -> bool:
        return (
            self.marine_medic_upgrade(state)
            or state.count(item_names.FIREBAT_PROGRESSIVE_STIMPACK, self.player) >= 2
            or state.has_any((item_names.FIREBAT_NANO_PROJECTORS, item_names.FIREBAT_JUGGERNAUT_PLATING), self.player)
        )

    def terran_bio_heal(self, state: CollectionState) -> bool:
        """
        Ability to heal bio units
        """
        return state.has_any({item_names.MEDIC, item_names.MEDIVAC, item_names.FIELD_RESPONSE_THETA}, self.player) or (
            self.advanced_tactics and state.has_all({item_names.RAVEN, item_names.RAVEN_BIO_MECHANICAL_REPAIR_DRONE}, self.player)
        )

    def terran_base_trasher(self, state: CollectionState) -> bool:
        """
        Can attack heavily defended bases
        """
        if not self.terran_competent_comp(state):
            return False
        if not self.terran_very_hard_mission_weapon_armor_level(state):
            return False
        return (
            state.has_all((item_names.SIEGE_TANK, item_names.SIEGE_TANK_JUMP_JETS), self.player)
            or state.has_all({item_names.BATTLECRUISER, item_names.BATTLECRUISER_ATX_LASER_BATTERY}, self.player)
            or state.has_all({item_names.LIBERATOR, item_names.LIBERATOR_RAID_ARTILLERY}, self.player)
            or (
                self.advanced_tactics
                and (state.has_all({item_names.RAVEN, item_names.RAVEN_HUNTER_SEEKER_WEAPON}, self.player))
                and (
                    state.has_all({item_names.VIKING, item_names.VIKING_SHREDDER_ROUNDS}, self.player)
                    or state.has_all({item_names.BANSHEE, item_names.BANSHEE_SHOCKWAVE_MISSILE_BATTERY}, self.player)
                )
            )
        )

    def terran_mobile_detector(self, state: CollectionState) -> bool:
        return state.has_any({item_names.RAVEN, item_names.SCIENCE_VESSEL, item_names.COMMAND_CENTER_SCANNER_SWEEP}, self.player)

    def can_nuke(self, state: CollectionState) -> bool:
        """
        Ability to launch nukes
        """
        return self.advanced_tactics and (
            state.has_any({item_names.GHOST, item_names.SPECTRE}, self.player)
            or state.has_all({item_names.THOR, item_names.THOR_BUTTON_WITH_A_SKULL_ON_IT}, self.player)
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
            or (
                self.advanced_tactics
                and (
                    state.has_all({item_names.RAVEN, item_names.RAVEN_BIO_MECHANICAL_REPAIR_DRONE}, self.player)
                    or state.count(item_names.PROGRESSIVE_REGENERATIVE_BIO_STEEL, self.player) >= 2
                )
            )
        )

    def terran_cliffjumper(self, state: CollectionState) -> bool:
        return (
            state.has(item_names.REAPER, self.player)
            or state.has_all({item_names.GOLIATH, item_names.GOLIATH_JUMP_JETS}, self.player)
            or state.has_all({item_names.SIEGE_TANK, item_names.SIEGE_TANK_JUMP_JETS}, self.player)
        )

    def nova_any_nobuild_damage(self, state: CollectionState) -> bool:
        return state.has_any(
            (
                item_names.NOVA_C20A_CANISTER_RIFLE,
                item_names.NOVA_HELLFIRE_SHOTGUN,
                item_names.NOVA_PLASMA_RIFLE,
                item_names.NOVA_MONOMOLECULAR_BLADE,
                item_names.NOVA_BLAZEFIRE_GUNBLADE,
                item_names.NOVA_PULSE_GRENADES,
                item_names.NOVA_DOMINATION,
            ),
            self.player,
        )

    def nova_any_weapon(self, state: CollectionState) -> bool:
        return state.has_any(
            {
                item_names.NOVA_C20A_CANISTER_RIFLE,
                item_names.NOVA_HELLFIRE_SHOTGUN,
                item_names.NOVA_PLASMA_RIFLE,
                item_names.NOVA_MONOMOLECULAR_BLADE,
                item_names.NOVA_BLAZEFIRE_GUNBLADE,
            },
            self.player,
        )

    def nova_ranged_weapon(self, state: CollectionState) -> bool:
        return state.has_any({item_names.NOVA_C20A_CANISTER_RIFLE, item_names.NOVA_HELLFIRE_SHOTGUN, item_names.NOVA_PLASMA_RIFLE}, self.player)

    def nova_anti_air_weapon(self, state: CollectionState) -> bool:
        return state.has_any({item_names.NOVA_C20A_CANISTER_RIFLE, item_names.NOVA_PLASMA_RIFLE, item_names.NOVA_BLAZEFIRE_GUNBLADE}, self.player)

    def nova_splash(self, state: CollectionState) -> bool:
        return state.has_any({item_names.NOVA_HELLFIRE_SHOTGUN, item_names.NOVA_PULSE_GRENADES}, self.player) or (
            self.advanced_tactics and state.has_any({item_names.NOVA_PLASMA_RIFLE, item_names.NOVA_MONOMOLECULAR_BLADE}, self.player)
        )

    def nova_dash(self, state: CollectionState) -> bool:
        return state.has_any({item_names.NOVA_MONOMOLECULAR_BLADE, item_names.NOVA_BLINK}, self.player)

    def nova_full_stealth(self, state: CollectionState) -> bool:
        return state.count(item_names.NOVA_PROGRESSIVE_STEALTH_SUIT_MODULE, self.player) >= 2

    def nova_heal(self, state: CollectionState) -> bool:
        return state.has_any({item_names.NOVA_ARMORED_SUIT_MODULE, item_names.NOVA_STIM_INFUSION}, self.player)

    def nova_escape_assist(self, state: CollectionState) -> bool:
        return state.has_any({item_names.NOVA_BLINK, item_names.NOVA_HOLO_DECOY, item_names.NOVA_IONIC_FORCE_FIELD}, self.player)
    
    def nova_beat_stone(self, state: CollectionState) -> bool:
        """
        Used for any units logic for beating Stone. Shotgun may not be possible; may need feedback.
        """
        return (
            state.has_any((
                item_names.NOVA_DOMINATION,
                item_names.NOVA_BLAZEFIRE_GUNBLADE,
                item_names.NOVA_C20A_CANISTER_RIFLE,
            ), self.player)
            or ((
                    state.has_any((
                        item_names.NOVA_PLASMA_RIFLE,
                        item_names.NOVA_MONOMOLECULAR_BLADE,
                    ), self.player)
                    or state.has_all((
                        item_names.NOVA_HELLFIRE_SHOTGUN,
                        item_names.NOVA_STIM_INFUSION
                    ), self.player)
                )
                and state.has_any((
                    item_names.NOVA_JUMP_SUIT_MODULE,
                    item_names.NOVA_ARMORED_SUIT_MODULE,
                    item_names.NOVA_ENERGY_SUIT_MODULE,
                ), self.player)
                and state.has_any((
                    item_names.NOVA_FLASHBANG_GRENADES,
                    item_names.NOVA_STIM_INFUSION,
                    item_names.NOVA_BLINK,
                    item_names.NOVA_IONIC_FORCE_FIELD,
                ), self.player)
            )
        )

    # Global Zerg
    def zerg_power_rating(self, state: CollectionState) -> int:
        power_score = self.base_power_rating
        # Passive Score (Economic upgrades and global army upgrades)
        power_score += sum((rating for item, rating in zerg_passive_ratings.items() if state.has(item, self.player)))
        # Spear of Adun
        if self.spear_of_adun_presence == SpearOfAdunPresence.option_everywhere:
            power_score += self.soa_power_rating(state)
        if self.spear_of_adun_passive_presence == SpearOfAdunPassiveAbilityPresence.option_everywhere:
            power_score += sum((rating for item, rating in soa_passive_ratings.items() if state.has(item, self.player)))
        return power_score

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
            if state.has(item_names.IMPALER_SUNKEN_SPINES, self.player):
                defense_score += 1
            if zerg_enemy:
                defense_score += -1
        # Lurker
        if self.morph_lurker(state):
            defense_score += 2
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
        if self.spread_creep(state, False):
            if not zerg_enemy:
                defense_score += 1
            if state.has(item_names.MALIGNANT_CREEP, self.player):
                defense_score += 1
        # Infested Siege Tanks
        if self.zerg_infested_tank_with_ammo(state):
            defense_score += 5
        # Infested Liberators
        if state.has_all((item_names.INFESTED_LIBERATOR, item_names.INFESTED_LIBERATOR_DEFENDER_MODE), self.player):
            defense_score += 3
        # Bile Launcher upgrades
        if state.has_all((item_names.BILE_LAUNCHER, item_names.BILE_LAUNCHER_RAPID_BOMBARMENT), self.player):
            defense_score += 2

        # General enemy-based rules
        if air_enemy:
            # Capped at 2
            defense_score += min(sum((zvx_air_defense_ratings[item] for item in zvx_air_defense_ratings if state.has(item, self.player))), 2)
        # Advanced Tactics bumps defense rating requirements down by 2
        if self.advanced_tactics:
            defense_score += 2
        return defense_score

    def zerg_army_weapon_armor_upgrade_min_level(self, state: CollectionState) -> int:
        count: int = WEAPON_ARMOR_UPGRADE_MAX_LEVEL
        if self.has_zerg_melee_unit:
            count = min2(count, self.zerg_melee_weapon_armor_upgrade_min_level(state))
        if self.has_zerg_ranged_unit:
            count = min2(count, self.zerg_ranged_weapon_armor_upgrade_min_level(state))
        if self.has_zerg_air_unit:
            count = min2(count, self.zerg_flyer_weapon_armor_upgrade_min_level(state))
        return count

    def zerg_melee_weapon_armor_upgrade_min_level(self, state: CollectionState) -> int:
        return min2(
            self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_ZERG_MELEE_ATTACK, state),
            self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_ZERG_GROUND_CARAPACE, state),
        )

    def zerg_ranged_weapon_armor_upgrade_min_level(self, state: CollectionState) -> int:
        return min2(
            self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_ZERG_MISSILE_ATTACK, state),
            self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_ZERG_GROUND_CARAPACE, state),
        )

    def zerg_flyer_weapon_armor_upgrade_min_level(self, state: CollectionState) -> int:
        return min2(
            self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_ZERG_FLYER_ATTACK, state),
            self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_ZERG_FLYER_CARAPACE, state),
        )

    def zerg_can_collect_pickup_across_gap(self, state: CollectionState) -> bool:
        """Any way for zerg to get any ground unit across gaps longer than viper yoink range to collect a pickup."""
        return (
            state.has_any(
                (
                    item_names.NYDUS_WORM,
                    item_names.ECHIDNA_WORM,
                    item_names.OVERLORD_VENTRAL_SACS,
                    item_names.YGGDRASIL,
                    item_names.INFESTED_BANSHEE,
                ),
                self.player,
            )
            or (self.morph_ravager(state) and state.has(item_names.RAVAGER_DEEP_TUNNEL, self.player))
            or state.has_all(
                (
                    item_names.INFESTED_SIEGE_TANK,
                    item_names.INFESTED_SIEGE_TANK_DEEP_TUNNEL,
                    item_names.OVERLORD_GENERATE_CREEP,
                ),
                self.player,
            )
            or state.has_all((item_names.SWARM_QUEEN_DEEP_TUNNEL, item_names.OVERLORD_OVERSEER_ASPECT), self.player)  # Deep tunnel to a creep tumor
        )

    def zerg_has_infested_scv(self, state: CollectionState) -> bool:
        return (
            state.has_any((
                item_names.INFESTED_MARINE,
                item_names.INFESTED_BUNKER,
                item_names.INFESTED_DIAMONDBACK,
                item_names.INFESTED_SIEGE_TANK,
                item_names.INFESTED_BANSHEE,
                item_names.BULLFROG,
                item_names.INFESTED_LIBERATOR,
                item_names.INFESTED_MISSILE_TURRET,
            ), self.player)
        )

    def zerg_very_hard_mission_weapon_armor_level(self, state: CollectionState) -> bool:
        return self.zerg_army_weapon_armor_upgrade_min_level(state) >= self.get_very_hard_required_upgrade_level()

    def zerg_common_unit(self, state: CollectionState) -> bool:
        return state.has_any(self.basic_zerg_units, self.player)

    def zerg_competent_anti_air(self, state: CollectionState) -> bool:
        return state.has_any({item_names.HYDRALISK, item_names.MUTALISK, item_names.CORRUPTOR, item_names.BROOD_QUEEN}, self.player) or (
            self.advanced_tactics and state.has(item_names.INFESTOR, self.player)
        )

    def zerg_moderate_anti_air(self, state: CollectionState) -> bool:
        return (
            self.zerg_competent_anti_air(state)
            or self.zerg_basic_air_to_air(state)
            or (
                state.has(item_names.SWARM_QUEEN, self.player)
                or state.has_all({item_names.SWARM_HOST, item_names.SWARM_HOST_PRESSURIZED_GLANDS}, self.player)
                or (self.spread_creep(state, True) and state.has(item_names.INFESTED_BUNKER, self.player))
            )
            or (self.advanced_tactics and state.has(item_names.INFESTED_MARINE, self.player))
        )

    def zerg_kerrigan_or_any_anti_air(self, state: CollectionState) -> bool:
        return self.kerrigan_unit_available or self.zerg_any_anti_air(state)

    def zerg_any_anti_air(self, state: CollectionState) -> bool:
        return (
            state.has_any(
                (
                    item_names.HYDRALISK,
                    item_names.SWARM_QUEEN,
                    item_names.BROOD_QUEEN,
                    item_names.MUTALISK,
                    item_names.CORRUPTOR,
                    item_names.SCOURGE,
                    item_names.INFESTOR,
                    item_names.INFESTED_MARINE,
                    item_names.INFESTED_LIBERATOR,
                    item_names.SPORE_CRAWLER,
                    item_names.INFESTED_MISSILE_TURRET,
                    item_names.INFESTED_BUNKER,
                    item_names.HUNTER_KILLERS,
                    item_names.CAUSTIC_HORRORS,
                ),
                self.player,
            )
            or state.has_all((item_names.SWARM_HOST, item_names.SWARM_HOST_PRESSURIZED_GLANDS), self.player)
            or state.has_all((item_names.ABERRATION, item_names.ABERRATION_PROGRESSIVE_BANELING_LAUNCH), self.player)
            or state.has_all((item_names.INFESTED_DIAMONDBACK, item_names.INFESTED_DIAMONDBACK_PROGRESSIVE_FUNGAL_SNARE), self.player)
            or self.morph_ravager(state)
            or self.morph_viper(state)
            or self.morph_devourer(state)
            or (self.morph_guardian(state) and state.has(item_names.GUARDIAN_PRIMAL_ADAPTATION, self.player))
        )

    def zerg_basic_anti_air(self, state: CollectionState) -> bool:
        return self.zerg_basic_kerriganless_anti_air(state) or self.kerrigan_unit_available

    def zerg_basic_kerriganless_anti_air(self, state: CollectionState) -> bool:
        return (
            self.zerg_moderate_anti_air(state)
            or state.has_any((item_names.HUNTER_KILLERS, item_names.CAUSTIC_HORRORS), self.player)
            or (self.advanced_tactics and state.has_any({item_names.SPORE_CRAWLER, item_names.INFESTED_MISSILE_TURRET}, self.player))
        )

    def zerg_basic_air_to_air(self, state: CollectionState) -> bool:
        return (
            state.has_any(
                {item_names.MUTALISK, item_names.CORRUPTOR, item_names.BROOD_QUEEN, item_names.SCOURGE, item_names.INFESTED_LIBERATOR}, self.player
            )
            or self.morph_devourer(state)
            or self.morph_viper(state)
            or (self.morph_guardian(state) and state.has(item_names.GUARDIAN_PRIMAL_ADAPTATION, self.player))
        )

    def zerg_basic_air_to_ground(self, state: CollectionState) -> bool:
        return (
            state.has_any({item_names.MUTALISK, item_names.INFESTED_BANSHEE}, self.player)
            or self.morph_guardian(state)
            or self.morph_brood_lord(state)
            or (self.morph_devourer(state) and state.has(item_names.DEVOURER_PRESCIENT_SPORES, self.player))
        )

    def zerg_versatile_air(self, state: CollectionState) -> bool:
        return self.zerg_basic_air_to_air(state) and self.zerg_basic_air_to_ground(state)

    def zerg_infested_tank_with_ammo(self, state: CollectionState) -> bool:
        return state.has(item_names.INFESTED_SIEGE_TANK, self.player) and (
            state.has_all({item_names.INFESTOR, item_names.INFESTOR_INFESTED_TERRAN}, self.player)
            or state.has(item_names.INFESTED_BUNKER, self.player)
            or (self.advanced_tactics and state.has(item_names.INFESTED_MARINE, self.player))
            or state.count(item_names.INFESTED_SIEGE_TANK_PROGRESSIVE_AUTOMATED_MITOSIS, self.player) >= (1 if self.advanced_tactics else 2)
        )

    def morph_baneling(self, state: CollectionState) -> bool:
        return (state.has(item_names.ZERGLING, self.player) or self.morphling_enabled) and state.has(item_names.ZERGLING_BANELING_ASPECT, self.player)

    def morph_ravager(self, state: CollectionState) -> bool:
        return (state.has(item_names.ROACH, self.player) or self.morphling_enabled) and state.has(item_names.ROACH_RAVAGER_ASPECT, self.player)

    def morph_brood_lord(self, state: CollectionState) -> bool:
        return (state.has_any({item_names.MUTALISK, item_names.CORRUPTOR}, self.player) or self.morphling_enabled) and state.has(
            item_names.MUTALISK_CORRUPTOR_BROOD_LORD_ASPECT, self.player
        )

    def morph_guardian(self, state: CollectionState) -> bool:
        return (state.has_any({item_names.MUTALISK, item_names.CORRUPTOR}, self.player) or self.morphling_enabled) and state.has(
            item_names.MUTALISK_CORRUPTOR_GUARDIAN_ASPECT, self.player
        )

    def morph_viper(self, state: CollectionState) -> bool:
        return (state.has_any({item_names.MUTALISK, item_names.CORRUPTOR}, self.player) or self.morphling_enabled) and state.has(
            item_names.MUTALISK_CORRUPTOR_VIPER_ASPECT, self.player
        )

    def morph_devourer(self, state: CollectionState) -> bool:
        return (state.has_any({item_names.MUTALISK, item_names.CORRUPTOR}, self.player) or self.morphling_enabled) and state.has(
            item_names.MUTALISK_CORRUPTOR_DEVOURER_ASPECT, self.player
        )

    def morph_impaler(self, state: CollectionState) -> bool:
        return (state.has(item_names.HYDRALISK, self.player) or self.morphling_enabled) and state.has(
            item_names.HYDRALISK_IMPALER_ASPECT, self.player
        )

    def morph_lurker(self, state: CollectionState) -> bool:
        return (state.has(item_names.HYDRALISK, self.player) or self.morphling_enabled) and state.has(item_names.HYDRALISK_LURKER_ASPECT, self.player)

    def morph_impaler_or_lurker(self, state: CollectionState) -> bool:
        return self.morph_impaler(state) or self.morph_lurker(state)

    def morph_igniter(self, state: CollectionState) -> bool:
        return (state.has(item_names.ROACH, self.player) or self.morphling_enabled) and state.has(item_names.ROACH_PRIMAL_IGNITER_ASPECT, self.player)

    def morph_tyrannozor(self, state: CollectionState) -> bool:
        return state.has(item_names.ULTRALISK_TYRANNOZOR_ASPECT, self.player) and (
            state.has(item_names.ULTRALISK, self.player) or self.morphling_enabled
        )

    def zerg_competent_comp(self, state: CollectionState) -> bool:
        if self.zerg_army_weapon_armor_upgrade_min_level(state) < 2:
            return False
        advanced = self.advanced_tactics
        core_unit = (
            state.has_any((
                item_names.ROACH,
                item_names.ABERRATION,
                item_names.ZERGLING,
                item_names.INFESTED_DIAMONDBACK,
            ), self.player)
            or self.morph_igniter(state)
        )
        support_unit = (
            state.has_any({item_names.SWARM_QUEEN, item_names.HYDRALISK, item_names.INFESTED_BANSHEE}, self.player)
            or self.morph_brood_lord(state)
            or state.has_all((item_names.MUTALISK, item_names.MUTALISK_SEVERING_GLAIVE, item_names.MUTALISK_VICIOUS_GLAIVE), self.player)
            or (advanced
                and (state.has_any((item_names.INFESTOR, item_names.DEFILER), self.player) or self.morph_viper(state))
            )
        )
        if core_unit and support_unit:
            return True
        vespene_unit = (
            state.has_any({item_names.ULTRALISK, item_names.ABERRATION}, self.player)
            or (
                self.morph_guardian(state)
                and state.has_any(
                    (item_names.GUARDIAN_SORONAN_ACID, item_names.GUARDIAN_EXPLOSIVE_SPORES, item_names.GUARDIAN_PRIMORDIAL_FURY), self.player
                )
            )
            or (advanced
                and self.morph_viper(state)
            )
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

    def spread_creep(self, state: CollectionState, free_creep_tumor=True) -> bool:
        return (self.advanced_tactics and free_creep_tumor) or state.has_any(
            {item_names.SWARM_QUEEN, item_names.OVERLORD_OVERSEER_ASPECT}, self.player
        )

    def zerg_mineral_dump(self, state: CollectionState) -> bool:
        return (
            state.has_any({item_names.ZERGLING, item_names.PYGALISK, item_names.INFESTED_BUNKER}, self.player)
            or state.has_all({item_names.SWARM_QUEEN, item_names.SWARM_QUEEN_RESOURCE_EFFICIENCY}, self.player)
            or (self.advanced_tactics and self.spread_creep(state) and state.has(item_names.SPINE_CRAWLER, self.player))
        )

    def zerg_big_monsters(self, state: CollectionState) -> bool:
        """
        Durable units with some capacity for damage
        """
        return (
            self.morph_tyrannozor(state)
            or state.has_any((item_names.ABERRATION, item_names.ULTRALISK), self.player)
            or (self.spread_creep(state, False) and state.has(item_names.INFESTED_BUNKER, self.player))
        )

    def zerg_base_buster(self, state: CollectionState) -> bool:
        """Powerful and sustainable zerg anti-ground for busting big bases; anti-air not included"""
        if not self.zerg_competent_comp(state):
            return False
        return (
            (
                self.zerg_melee_weapon_armor_upgrade_min_level(state) >= self.get_very_hard_required_upgrade_level()
                and (
                    self.morph_tyrannozor(state)
                    or (
                        state.has(item_names.ULTRALISK, self.player)
                        and state.has_any((item_names.ULTRALISK_TORRASQUE_STRAIN, item_names.ULTRALISK_CHITINOUS_PLATING), self.player)
                    )
                    or (self.morph_baneling(state) and state.has(item_names.BANELING_SPLITTER_STRAIN, self.player))
                )
                and state.has(item_names.SWARM_QUEEN, self.player)  # Healing to sustain the frontline
            )
            or (
                self.zerg_ranged_weapon_armor_upgrade_min_level(state) >= self.get_very_hard_required_upgrade_level()
                and (
                    self.morph_impaler(state)
                    or (self.morph_lurker(state)
                        and state.has_all((item_names.LURKER_SEISMIC_SPINES, item_names.LURKER_ADAPTED_SPINES), self.player)
                    )
                    or state.has_all((
                        item_names.ROACH,
                        item_names.ROACH_CORPSER_STRAIN,
                        item_names.ROACH_ADAPTIVE_PLATING,
                        item_names.ROACH_GLIAL_RECONSTITUTION,
                    ), self.player)
                    or (self.morph_igniter(state)
                        and state.has(item_names.PRIMAL_IGNITER_PRIMAL_TENACITY, self.player)
                    )
                    or state.has_all((item_names.INFESTOR, item_names.INFESTOR_INFESTED_TERRAN), self.player)
                    or (self.spread_creep(state, False)
                        and state.has(item_names.INFESTED_BUNKER, self.player)
                    )
                    or self.zerg_infested_tank_with_ammo(state)
                    # Highly-upgraded swarm hosts may also work, but that would require promoting many upgrades to progression
                )
            )
            or (
                self.zerg_flyer_weapon_armor_upgrade_min_level(state) >= self.get_very_hard_required_upgrade_level()
                and (
                    self.morph_brood_lord(state)
                    or (self.morph_guardian(state)
                        and state.has_all((item_names.GUARDIAN_PROPELLANT_SACS, item_names.GUARDIAN_SORONAN_ACID), self.player)
                    )
                    or state.has_all((item_names.INFESTED_BANSHEE, item_names.INFESTED_BANSHEE_FLESHFUSED_TARGETING_OPTICS), self.player)
                    # Highly-upgraded anti-ground devourers would also be good
                )
            )
        )

    def zergling_hydra_roach_start(self, state: CollectionState) -> bool:
        """
        Created mainly for engine of destruction start, but works for other missions with no-build starts.
        """
        return state.has_any((
                item_names.ZERGLING_ADRENAL_OVERLOAD,
                item_names.HYDRALISK_FRENZY,
                item_names.ROACH_HYDRIODIC_BILE,
                item_names.ZERGLING_RAPTOR_STRAIN,
                item_names.ROACH_CORPSER_STRAIN,
        ), self.player)

    def kerrigan_levels(self, state: CollectionState, target: int, story_levels_available=True) -> bool:
        if (story_levels_available and self.story_levels_granted) or not self.kerrigan_unit_available:
            return True  # Levels are granted
        if (
            self.kerrigan_levels_per_mission_completed > 0
            and self.kerrigan_levels_per_mission_completed_cap != 0
            and not self.is_item_placement(state)
        ):
            # Levels can be granted from mission completion.
            # Item pool filtering isn't aware of missions beaten. Assume that missions beaten will fulfill this rule.
            return True
        # Levels from missions beaten
        levels = self.kerrigan_levels_per_mission_completed * state.count_group("Missions", self.player)
        if self.kerrigan_levels_per_mission_completed_cap != -1:
            levels = min2(levels, self.kerrigan_levels_per_mission_completed_cap)
        # Levels from items
        for kerrigan_level_item in kerrigan_levels:
            level_amount = get_full_item_list()[kerrigan_level_item].number
            item_count = state.count(kerrigan_level_item, self.player)
            levels += item_count * level_amount
        # Total level cap
        if self.kerrigan_total_level_cap != -1:
            levels = min2(levels, self.kerrigan_total_level_cap)

        return levels >= target

    def basic_kerrigan(self, state: CollectionState, story_tech_available=True) -> bool:
        if story_tech_available and (
            self.grant_story_tech == GrantStoryTech.option_grant
            or not self.kerrigan_unit_available
        ):
            return True
        # One active ability that can be used to defeat enemies directly
        if not state.has_any(
            (
                item_names.KERRIGAN_LEAPING_STRIKE,
                item_names.KERRIGAN_KINETIC_BLAST,
                item_names.KERRIGAN_SPAWN_BANELINGS,
                item_names.KERRIGAN_PSIONIC_SHIFT,
                item_names.KERRIGAN_CRUSHING_GRIP,
            ),
            self.player,
        ):
            return False
        # Two non-ultimate abilities
        count = 0
        for item in kerrigan_non_ulimates:
            if state.has(item, self.player):
                count += 1
            if count >= 2:
                return True
        return False

    def two_kerrigan_actives(self, state: CollectionState, story_tech_available=True) -> bool:
        if story_tech_available and (
            self.grant_story_tech == GrantStoryTech.option_grant
            or not self.kerrigan_unit_available
        ):
            return True
        return state.count_from_list(item_groups.kerrigan_logic_active_abilities, self.player) >= 2

    # Global Protoss
    def protoss_power_rating(self, state: CollectionState) -> int:
        power_score = self.base_power_rating
        # War Council Upgrades (all units are improved)
        if self.war_council_upgrades:
            power_score += 3
        # Passive Score (Economic upgrades and global army upgrades)
        power_score += sum((rating for item, rating in protoss_passive_ratings.items() if state.has(item, self.player)))
        # Spear of Adun
        if self.spear_of_adun_presence in (SpearOfAdunPresence.option_everywhere, SpearOfAdunPresence.option_protoss):
            power_score += self.soa_power_rating(state)
        if self.spear_of_adun_passive_presence in (SpearOfAdunPassiveAbilityPresence.option_everywhere, SpearOfAdunPresence.option_protoss):
            power_score += sum((rating for item, rating in soa_passive_ratings.items() if state.has(item, self.player)))
        return power_score

    def protoss_army_weapon_armor_upgrade_min_level(self, state: CollectionState) -> int:
        count: int = WEAPON_ARMOR_UPGRADE_MAX_LEVEL + 1  # +1 for Quatro
        if self.has_protoss_ground_unit:
            count = min(
                count,
                self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_PROTOSS_GROUND_WEAPON, state),
                self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_PROTOSS_GROUND_ARMOR, state),
            )
        if self.has_protoss_air_unit:
            count = min(
                count,
                self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_PROTOSS_AIR_WEAPON, state),
                self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_PROTOSS_AIR_ARMOR, state),
            )
        if self.has_protoss_ground_unit or self.has_protoss_air_unit:
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
        # Vanguard + rapid fire
        if state.has_all((item_names.VANGUARD, item_names.VANGUARD_RAPIDFIRE_CANNON), self.player):
            defense_score += 1
        # Fire Colossus
        if state.has_all((item_names.COLOSSUS, item_names.COLOSSUS_FIRE_LANCE), self.player):
            defense_score += 2
            if zerg_enemy:
                defense_score += 2
        if (
            state.has_any((item_names.PHOTON_CANNON, item_names.KHAYDARIN_MONOLITH, item_names.NEXUS_OVERCHARGE), self.player)
            and state.has(item_names.SHIELD_BATTERY, self.player)
        ):
            defense_score += 2

        # No anti-air defense dict here, use an existing logic rule instead
        if zerg_enemy:
            defense_score += sum((pvz_defense_ratings[item] for item in pvz_defense_ratings if state.has(item, self.player)))
        # Advanced Tactics bumps defense rating requirements down by 2
        if self.advanced_tactics:
            defense_score += 2
        return defense_score

    def protoss_common_unit(self, state: CollectionState) -> bool:
        return state.has_any(self.basic_protoss_units, self.player)

    def protoss_any_gap_transport(self, state: CollectionState) -> bool:
        """Can get ground units across large gaps, larger than blink range"""
        return (
            state.has_any(
                (
                    item_names.WARP_PRISM,
                    item_names.ARBITER,
                ),
                self.player,
            )
            or state.has(item_names.SOA_PROGRESSIVE_PROXY_PYLON, self.player, count=2)
            or state.has_all((item_names.MISTWING, item_names.MISTWING_PILOT), self.player)
            or (
                state.has(item_names.SOA_PROGRESSIVE_PROXY_PYLON, self.player)
                and (
                    state.has_any(item_groups.gateway_units + [item_names.ELDER_PROBES, item_names.PROBE_WARPIN], self.player)
                    or (state.has(item_names.WARP_HARMONIZATION, self.player) and state.has_any(item_groups.protoss_ground_wa, self.player))
                )
            )
        )

    def protoss_any_anti_air_unit_or_soa_any_protoss(self, state: CollectionState) -> bool:
        return self.protoss_any_anti_air_unit(state) or (
            self.spear_of_adun_presence in (SpearOfAdunPresence.option_everywhere, SpearOfAdunPresence.option_protoss)
            and self.protoss_any_anti_air_soa(state)
        )

    def protoss_any_anti_air_unit_or_soa(self, state: CollectionState) -> bool:
        return self.protoss_any_anti_air_unit(state) or self.protoss_any_anti_air_soa(state)

    def protoss_any_anti_air_soa(self, state: CollectionState) -> bool:
        return (
            state.has_any(
                (
                    item_names.SOA_ORBITAL_STRIKE,
                    item_names.SOA_SOLAR_LANCE,
                    item_names.SOA_SOLAR_BOMBARDMENT,
                    item_names.SOA_PURIFIER_BEAM,
                    item_names.SOA_PYLON_OVERCHARGE,
                ),
                self.player,
            )
            or state.has(item_names.SOA_PROGRESSIVE_PROXY_PYLON, self.player, 2)  # Warp-In Reinforcements
        )

    def protoss_any_anti_air_unit(self, state: CollectionState) -> bool:
        return (
            state.has_any(
                (
                    # Gateway
                    item_names.STALKER,
                    item_names.SLAYER,
                    item_names.INSTIGATOR,
                    item_names.DRAGOON,
                    item_names.ADEPT,
                    item_names.SENTRY,
                    item_names.ENERGIZER,
                    item_names.HIGH_TEMPLAR,
                    item_names.SIGNIFIER,
                    item_names.ASCENDANT,
                    item_names.DARK_ARCHON,
                    # Robo
                    item_names.ANNIHILATOR,
                    # Stargate
                    item_names.PHOENIX,
                    item_names.MIRAGE,
                    item_names.CORSAIR,
                    item_names.SCOUT,
                    item_names.MISTWING,
                    item_names.CALADRIUS,
                    item_names.OPPRESSOR,
                    item_names.ARBITER,
                    item_names.VOID_RAY,
                    item_names.DESTROYER,
                    item_names.PULSAR,
                    item_names.CARRIER,
                    item_names.SKYLORD,
                    item_names.TEMPEST,
                    item_names.MOTHERSHIP,
                    # Buildings
                    item_names.NEXUS_OVERCHARGE,
                    item_names.PHOTON_CANNON,
                    item_names.KHAYDARIN_MONOLITH,
                ),
                self.player,
            )
            or state.has_all((item_names.SUPPLICANT, item_names.SUPPLICANT_ZENITH_PITCH), self.player)
            or state.has_all((item_names.WARP_PRISM, item_names.WARP_PRISM_PHASE_BLASTER), self.player)
            or state.has_all((item_names.WRATHWALKER, item_names.WRATHWALKER_AERIAL_TRACKING), self.player)
            or state.has_all((item_names.DISRUPTOR, item_names.DISRUPTOR_PERFECTED_POWER), self.player)
            or state.has_all((item_names.IMMORTAL, item_names.IMMORTAL_ANNIHILATOR_ADVANCED_TARGETING), self.player)
            or state.has_all((item_names.SKIRMISHER, item_names.SKIRMISHER_PEER_CONTEMPT), self.player)
            or state.has_all((item_names.TRIREME, item_names.TRIREME_SOLAR_BEAM), self.player)
            or (
                state.has(item_names.DARK_TEMPLAR, self.player)
                and state.has_any((item_names.DARK_TEMPLAR_DARK_ARCHON_MELD, item_names.DARK_TEMPLAR_ARCHON_MERGE), self.player)
            )
        )

    def protoss_basic_anti_air(self, state: CollectionState) -> bool:
        return (
            self.protoss_competent_anti_air(state)
            or state.has_any(
                {
                    item_names.PHOENIX,
                    item_names.MIRAGE,
                    item_names.CORSAIR,
                    item_names.CARRIER,
                    item_names.SKYLORD,
                    item_names.SCOUT,
                    item_names.DARK_ARCHON,
                    item_names.MOTHERSHIP,
                    item_names.MISTWING,
                    item_names.CALADRIUS,
                    item_names.OPPRESSOR,
                    item_names.DRAGOON,
                },
                self.player,
            )
            or state.has_all({item_names.TRIREME, item_names.TRIREME_SOLAR_BEAM}, self.player)
            or state.has_all({item_names.WRATHWALKER, item_names.WRATHWALKER_AERIAL_TRACKING}, self.player)
            or state.has_all({item_names.WARP_PRISM, item_names.WARP_PRISM_PHASE_BLASTER}, self.player)
            or (self.advanced_tactics
                and state.has_any((
                    item_names.HIGH_TEMPLAR,
                    item_names.SIGNIFIER,
                    item_names.SENTRY,
                    item_names.ENERGIZER,
                ), self.player)
            )
            or self.protoss_can_merge_archon(state)
            or self.protoss_can_merge_dark_archon(state)
        )

    def protoss_anti_armor_anti_air(self, state: CollectionState) -> bool:
        return (
            self.protoss_competent_anti_air(state)
            or state.has_any((item_names.SCOUT, item_names.MISTWING, item_names.DRAGOON), self.player)
            or (
                state.has_any({item_names.IMMORTAL, item_names.ANNIHILATOR}, self.player)
                and state.has(item_names.IMMORTAL_ANNIHILATOR_ADVANCED_TARGETING, self.player)
            )
            or state.has_all({item_names.WRATHWALKER, item_names.WRATHWALKER_AERIAL_TRACKING}, self.player)
        )

    def protoss_anti_light_anti_air(self, state: CollectionState) -> bool:
        return (
            self.protoss_competent_anti_air(state)
            or state.has_any(
                {
                    item_names.PHOENIX,
                    item_names.MIRAGE,
                    item_names.CORSAIR,
                    item_names.CARRIER,
                },
                self.player,
            )
            or state.has_all((item_names.SKIRMISHER, item_names.SKIRMISHER_PEER_CONTEMPT), self.player)
        )

    def protoss_moderate_anti_air(self, state: CollectionState) -> bool:
        return (
            self.protoss_competent_anti_air(state)
            or self.protoss_anti_light_anti_air(state)
            or self.protoss_anti_armor_anti_air(state)
            or state.has(item_names.SKYLORD, self.player)
        )

    def protoss_common_unit_basic_aa(self, state: CollectionState) -> bool:
        return self.protoss_common_unit(state) and self.protoss_basic_anti_air(state)

    def protoss_common_unit_anti_light_air(self, state: CollectionState) -> bool:
        return self.protoss_common_unit(state) and self.protoss_anti_light_anti_air(state)

    def protoss_common_unit_anti_armor_air(self, state: CollectionState) -> bool:
        return self.protoss_common_unit(state) and self.protoss_anti_armor_anti_air(state)

    def protoss_competent_anti_air(self, state: CollectionState) -> bool:
        return (
            state.has_any(
                {
                    item_names.STALKER,
                    item_names.SLAYER,
                    item_names.INSTIGATOR,
                    item_names.ADEPT,
                    item_names.VOID_RAY,
                    item_names.DESTROYER,
                    item_names.TEMPEST,
                    item_names.CALADRIUS,
                },
                self.player,
            )
            or (
                (
                    state.has_any(
                        {
                            item_names.PHOENIX,
                            item_names.MIRAGE,
                            item_names.CORSAIR,
                            item_names.CARRIER,
                        },
                        self.player,
                    )
                    or state.has_all((item_names.SKIRMISHER, item_names.SKIRMISHER_PEER_CONTEMPT), self.player)
                )
                and (
                    state.has_any((item_names.SCOUT, item_names.MISTWING, item_names.DRAGOON), self.player)
                    or state.has_all({item_names.WRATHWALKER, item_names.WRATHWALKER_AERIAL_TRACKING}, self.player)
                    or (
                        state.has_any({item_names.IMMORTAL, item_names.ANNIHILATOR}, self.player)
                        and state.has(item_names.IMMORTAL_ANNIHILATOR_ADVANCED_TARGETING, self.player)
                    )
                )
            )
            or (
                self.advanced_tactics
                and state.has_any({item_names.IMMORTAL, item_names.ANNIHILATOR}, self.player)
                and state.has(item_names.IMMORTAL_ANNIHILATOR_ADVANCED_TARGETING, self.player)
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

    def protoss_fleet(self, state: CollectionState) -> bool:
        return (
            (
                state.has_any(
                    {
                        item_names.CARRIER,
                        item_names.SKYLORD,
                        item_names.TEMPEST,
                        item_names.VOID_RAY,
                        item_names.DESTROYER,
                    },
                    self.player,
                )
            )
            or (
                state.has_all((item_names.TRIREME, item_names.TRIREME_SOLAR_BEAM), self.player)
                and (
                    state.has_any((item_names.PHOENIX, item_names.MIRAGE, item_names.CORSAIR), self.player)
                    or state.has_all((item_names.SKIRMISHER, item_names.SKIRMISHER_PEER_CONTEMPT), self.player)
                )
            )
            and self.weapon_armor_upgrade_count(PROGRESSIVE_PROTOSS_AIR_WEAPON, state) >= 2
            and self.weapon_armor_upgrade_count(PROGRESSIVE_PROTOSS_AIR_ARMOR, state) >= 2
            and self.weapon_armor_upgrade_count(PROGRESSIVE_PROTOSS_SHIELDS, state) >= 2
        )

    def protoss_hybrid_counter(self, state: CollectionState) -> bool:
        """
        Ground Hybrids
        """
        return (
            state.has_any(
                {
                    item_names.ANNIHILATOR,
                    item_names.ASCENDANT,
                    item_names.TEMPEST,
                    item_names.CARRIER,
                    item_names.TRIREME,
                    item_names.VOID_RAY,
                    item_names.WRATHWALKER,
                },
                self.player,
            )
            or state.has_all((item_names.VANGUARD, item_names.VANGUARD_FUSION_MORTARS), self.player)
            or (
                (state.has(item_names.IMMORTAL, self.player) or self.advanced_tactics)
                and (state.has_any({item_names.STALKER, item_names.DRAGOON, item_names.ADEPT, item_names.INSTIGATOR, item_names.SLAYER}, self.player))
            )
            or (self.advanced_tactics and state.has_all((item_names.OPPRESSOR, item_names.OPPRESSOR_VULCAN_BLASTER), self.player))
        )

    def protoss_basic_splash(self, state: CollectionState) -> bool:
        return (
            state.has_any((
                item_names.COLOSSUS,
                item_names.VANGUARD,
                item_names.HIGH_TEMPLAR,
                item_names.SIGNIFIER,
                item_names.REAVER,
                item_names.ASCENDANT,
                item_names.DAWNBRINGER,
            ), self.player)
            or state.has_all((item_names.ZEALOT, item_names.ZEALOT_WHIRLWIND), self.player)
            or (
                state.has_all(
                    (item_names.DARK_TEMPLAR, item_names.DARK_TEMPLAR_LESSER_SHADOW_FURY, item_names.DARK_TEMPLAR_GREATER_SHADOW_FURY), self.player
                )
            )
            or (
                state.has(item_names.DESTROYER, self.player)
                and (
                    state.has_any((
                        item_names.DESTROYER_REFORGED_BLOODSHARD_CORE,
                        item_names.DESTROYER_RESOURCE_EFFICIENCY,
                    ), self.player)
                )
            )
        )

    def protoss_static_defense(self, state: CollectionState) -> bool:
        return state.has_any({item_names.PHOTON_CANNON, item_names.KHAYDARIN_MONOLITH}, self.player)

    def protoss_can_merge_archon(self, state: CollectionState) -> bool:
        return (
            state.has_any({item_names.HIGH_TEMPLAR, item_names.SIGNIFIER}, self.player)
            or state.has_all({item_names.ASCENDANT, item_names.ASCENDANT_ARCHON_MERGE}, self.player)
            or state.has_all({item_names.DARK_TEMPLAR, item_names.DARK_TEMPLAR_ARCHON_MERGE}, self.player)
        )

    def protoss_can_merge_dark_archon(self, state: CollectionState) -> bool:
        return state.has(item_names.DARK_ARCHON, self.player) or state.has_all(
            {item_names.DARK_TEMPLAR, item_names.DARK_TEMPLAR_DARK_ARCHON_MELD}, self.player
        )

    def protoss_competent_comp(self, state: CollectionState) -> bool:
        if not self.protoss_competent_anti_air(state):
            return False
        if self.protoss_fleet(state) and self.protoss_mineral_dump(state):
            return True
        if self.protoss_deathball(state):
            return True
        core_unit: bool = state.has_any(
            (
                item_names.ZEALOT,
                item_names.CENTURION,
                item_names.SENTINEL,
                item_names.STALKER,
                item_names.INSTIGATOR,
                item_names.SLAYER,
                item_names.ADEPT,
            ),
            self.player,
        )
        support_unit: bool = (
            state.has_any(
                (
                    item_names.SENTRY,
                    item_names.ENERGIZER,
                    item_names.IMMORTAL,
                    item_names.VANGUARD,
                    item_names.COLOSSUS,
                    item_names.REAVER,
                    item_names.VOID_RAY,
                    item_names.PHOENIX,
                    item_names.CORSAIR,
                ),
                self.player,
            )
            or state.has_all((item_names.MIRAGE, item_names.MIRAGE_GRAVITON_BEAM), self.player)
            or state.has_all(
                (item_names.DARK_TEMPLAR, item_names.DARK_TEMPLAR_LESSER_SHADOW_FURY, item_names.DARK_TEMPLAR_GREATER_SHADOW_FURY), self.player
            )
            or (
                self.advanced_tactics
                and (
                    state.has_any(
                        (
                            item_names.HIGH_TEMPLAR,
                            item_names.SIGNIFIER,
                            item_names.ASCENDANT,
                            item_names.ANNIHILATOR,
                            item_names.WRATHWALKER,
                            item_names.SKIRMISHER,
                            item_names.ARBITER,
                        ),
                        self.player,
                    )
                )
            )
        )
        if core_unit and support_unit:
            return True
        return False

    def protoss_deathball(self, state: CollectionState) -> bool:
        return (
            self.protoss_common_unit(state)
            and self.protoss_competent_anti_air(state)
            and self.protoss_hybrid_counter(state)
            and self.protoss_basic_splash(state)
            and self.protoss_army_weapon_armor_upgrade_min_level(state) >= 2
        )

    def protoss_heal(self, state: CollectionState) -> bool:
        return state.has_any((item_names.SENTRY, item_names.SHIELD_BATTERY, item_names.RECONSTRUCTION_BEAM), self.player) or state.has_all(
            (item_names.CARRIER, item_names.CARRIER_REPAIR_DRONES), self.player
        )

    def protoss_mineral_dump(self, state: CollectionState) -> bool:
        return (
            state.has_any((item_names.ZEALOT, item_names.SENTINEL, item_names.PHOTON_CANNON), self.player)
            or state.has_all((item_names.CENTURION, item_names.CENTURION_RESOURCE_EFFICIENCY), self.player)
            or (self.advanced_tactics
                and state.has_any((item_names.SUPPLICANT, item_names.SHIELD_BATTERY), self.player)
            )
        )

    def zealot_sentry_slayer_start(self, state: CollectionState) -> bool:
        """
        Created mainly for engine of destruction start, but works for other missions with no-build starts.
        """
        return state.has_any((
                item_names.ZEALOT_WHIRLWIND,
                item_names.SENTRY_DOUBLE_SHIELD_RECHARGE,
                item_names.SLAYER_PHASE_BLINK,
                item_names.STALKER_INSTIGATOR_SLAYER_DISINTEGRATING_PARTICLES,
                item_names.STALKER_INSTIGATOR_SLAYER_PARTICLE_REFLECTION,
        ), self.player)

    # Mission-specific rules
    def ghost_of_a_chance_requirement(self, state: CollectionState) -> bool:
        return (
            self.grant_story_tech == GrantStoryTech.option_grant
            or self.nova_ghost_of_a_chance_variant == NovaGhostOfAChanceVariant.option_wol
            or not self.nova_used
            or (
                self.nova_ranged_weapon(state)
                and state.has_any({item_names.NOVA_DOMINATION, item_names.NOVA_C20A_CANISTER_RIFLE}, self.player)
                and (self.nova_full_stealth(state) or self.nova_heal(state))
                and self.nova_anti_air_weapon(state)
            )
        )

    def terran_outbreak_requirement(self, state: CollectionState) -> bool:
        """Outbreak mission requirement"""
        return self.terran_defense_rating(state, True, False) >= 4 and (self.terran_common_unit(state) or state.has(item_names.REAPER, self.player))

    def zerg_outbreak_requirement(self, state: CollectionState) -> bool:
        """
        Outbreak mission requirement.
        Need to boot out Aberration-based comp
        """
        return (
            self.zerg_defense_rating(state, True, False) >= 4
            and self.zerg_common_unit(state)
            and (
                state.has_any(
                    (
                        item_names.SWARM_QUEEN,
                        item_names.HYDRALISK,
                        item_names.ROACH,
                        item_names.MUTALISK,
                        item_names.INFESTED_BANSHEE,
                    ),
                    self.player,
                )
                or self.morph_lurker(state)
                or self.morph_brood_lord(state)
                or (
                    self.advanced_tactics
                    and (
                        self.morph_impaler(state)
                        or self.morph_igniter(state)
                        or state.has_any((item_names.INFESTED_DIAMONDBACK, item_names.INFESTED_SIEGE_TANK), self.player)
                    )
                )
            )
        )

    def protoss_outbreak_requirement(self, state: CollectionState) -> bool:
        """
        Outbreak mission requirement
        Something other than Zealot-based comp is required.
        """
        return (
            self.protoss_defense_rating(state, True) >= 4
            and self.protoss_common_unit(state)
            and self.protoss_basic_splash(state)
            and (
                state.has_any(
                    (
                        item_names.STALKER,
                        item_names.SLAYER,
                        item_names.INSTIGATOR,
                        item_names.ADEPT,
                        item_names.COLOSSUS,
                        item_names.VANGUARD,
                        item_names.SKIRMISHER,
                        item_names.OPPRESSOR,
                        item_names.CARRIER,
                        item_names.SKYLORD,
                        item_names.TRIREME,
                        item_names.DAWNBRINGER,
                    ),
                    self.player,
                )
                or (self.advanced_tactics and (state.has_any((item_names.VOID_RAY, item_names.DESTROYER), self.player)))
            )
        )

    def terran_safe_haven_requirement(self, state: CollectionState) -> bool:
        """Safe Haven mission requirement"""
        return self.terran_common_unit(state) and self.terran_competent_anti_air(state)

    def terran_havens_fall_requirement(self, state: CollectionState) -> bool:
        """Haven's Fall mission requirement"""
        return self.terran_common_unit(state) and (
            self.terran_competent_comp(state)
            or (
                self.terran_competent_anti_air(state)
                and (
                    state.has_any((item_names.VIKING, item_names.BATTLECRUISER), self.player)
                    or state.has_all((item_names.WRAITH, item_names.WRAITH_ADVANCED_LASER_TECHNOLOGY), self.player)
                    or state.has_all((item_names.LIBERATOR, item_names.LIBERATOR_RAID_ARTILLERY), self.player)
                )
            )
        )

    def terran_respond_to_colony_infestations(self, state: CollectionState) -> bool:
        """
        Can deal quickly with Brood Lords and Mutas in Haven's Fall and being able to progress the mission
        """
        return self.terran_havens_fall_requirement(state) and (
            self.terran_air_anti_air(state)
            or (
                state.has_any({item_names.BATTLECRUISER, item_names.VALKYRIE}, self.player)
                and self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_TERRAN_SHIP_WEAPON, state) >= 2
            )
        )

    def zerg_havens_fall_requirement(self, state: CollectionState) -> bool:
        return (
            self.zerg_common_unit(state)
            and self.zerg_competent_anti_air(state)
            and (state.has(item_names.MUTALISK, self.player) or self.zerg_competent_comp(state))
        )

    def zerg_respond_to_colony_infestations(self, state: CollectionState) -> bool:
        """
        Can deal quickly with Brood Lords and Mutas in Haven's Fall and being able to progress the mission
        """
        return self.zerg_havens_fall_requirement(state) and (
            self.morph_devourer(state)
            or state.has_any({item_names.MUTALISK, item_names.CORRUPTOR}, self.player)
            or (self.advanced_tactics
                and (
                    self.morph_viper(state)
                    or state.has_any((item_names.BROOD_QUEEN, item_names.SCOURGE), self.player)
                )
            )
        )

    def protoss_havens_fall_requirement(self, state: CollectionState) -> bool:
        return (
            self.protoss_common_unit(state)
            and self.protoss_competent_anti_air(state)
            and (
                self.protoss_competent_comp(state)
                or state.has_any((item_names.TEMPEST, item_names.SKYLORD, item_names.DESTROYER), self.player)
                or (
                    self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_PROTOSS_AIR_WEAPON, state) >= 2
                    and (
                        state.has_all((item_names.SKIRMISHER, item_names.SKIRMISHER_PEER_CONTEMPT), self.player)
                        or (state.has(item_names.CARRIER, self.player))
                    )
                )
            )
        )

    def protoss_respond_to_colony_infestations(self, state: CollectionState) -> bool:
        """
        Can deal quickly with Brood Lords and Mutas in Haven's Fall and being able to progress the mission
        """
        return (
            self.protoss_havens_fall_requirement(state)
            and (
                # One-unit solutions
                state.has_any((
                    item_names.CARRIER,
                    item_names.SKYLORD,
                    item_names.DESTROYER,
                    item_names.TEMPEST,
                    item_names.VOID_RAY,
                    item_names.SCOUT,
                ), self.player)
                or (
                    (
                        # handle mutas
                        state.has_any((
                            item_names.PHOENIX,
                            item_names.MIRAGE,
                            item_names.CORSAIR,
                        ), self.player)
                        or state.has_all((item_names.SKIRMISHER, item_names.SKIRMISHER_PEER_CONTEMPT), self.player)
                    )
                    and (
                        # handle brood lords and virophages
                        state.has(item_names.MISTWING, self.player)
                    )
                )
            )
        )

    def terran_gates_of_hell_requirement(self, state: CollectionState) -> bool:
        """Gates of Hell mission requirement"""
        return self.terran_competent_comp(state) and (self.terran_defense_rating(state, True) > 6)

    def zerg_gates_of_hell_requirement(self, state: CollectionState) -> bool:
        """Gates of Hell mission requirement"""
        return self.zerg_competent_comp_competent_aa(state) and (self.zerg_defense_rating(state, True) > 8)

    def protoss_gates_of_hell_requirement(self, state: CollectionState) -> bool:
        """Gates of Hell mission requirement"""
        return self.protoss_competent_comp(state) and (self.protoss_defense_rating(state, True) > 6)

    def terran_welcome_to_the_jungle_requirement(self, state: CollectionState) -> bool:
        """
        Welcome to the Jungle requirements - able to deal with Scouts, Void Rays, Zealots and Stalkers
        """
        if self.terran_power_rating(state) < 5:
            return False
        return (self.terran_common_unit(state) and self.terran_competent_ground_to_air(state)) or (
            self.advanced_tactics
            and state.has_any({item_names.MARINE, item_names.DOMINION_TROOPER, item_names.VULTURE}, self.player)
            and self.terran_air_anti_air(state)
        )

    def zerg_welcome_to_the_jungle_requirement(self, state: CollectionState) -> bool:
        """
        Welcome to the Jungle requirements - able to deal with Scouts, Void Rays, Zealots and Stalkers
        """
        if self.zerg_power_rating(state) < 5:
            return False
        return (self.zerg_competent_comp(state) and state.has_any({item_names.HYDRALISK, item_names.MUTALISK}, self.player)) or (
            self.advanced_tactics
            and self.zerg_common_unit(state)
            and (
                state.has_any({item_names.MUTALISK, item_names.INFESTOR}, self.player)
                or (self.morph_devourer(state) and state.has_any({item_names.HYDRALISK, item_names.SWARM_QUEEN}, self.player))
                or (self.morph_viper(state) and state.has(item_names.VIPER_PARASITIC_BOMB, self.player))
            )
            and self.zerg_army_weapon_armor_upgrade_min_level(state) >= 1
        )

    def protoss_welcome_to_the_jungle_requirement(self, state: CollectionState) -> bool:
        """
        Welcome to the Jungle requirements - able to deal with Scouts, Void Rays, Zealots and Stalkers
        """
        if self.protoss_power_rating(state) < 5:
            return False
        return self.protoss_common_unit(state) and self.protoss_anti_armor_anti_air(state)

    def terran_can_grab_ghosts_in_the_fog_east_rock_formation(self, state: CollectionState) -> bool:
        """
        Able to shoot by a long range or from air to claim the rock formation separated by a chasm
        """
        return (
            state.has_any((
                item_names.MEDIVAC,
                item_names.HERCULES,
                item_names.VIKING,
                item_names.BANSHEE,
                item_names.WRAITH,
                item_names.SIEGE_TANK,
                item_names.BATTLECRUISER,
                item_names.NIGHT_HAWK,
                item_names.NIGHT_WOLF,
                item_names.SHOCK_DIVISION,
                item_names.SKY_FURY,
            ), self.player)
            or state.has_all({item_names.VALKYRIE, item_names.VALKYRIE_FLECHETTE_MISSILES}, self.player)
            or state.has_all({item_names.RAVEN, item_names.RAVEN_HUNTER_SEEKER_WEAPON}, self.player)
            or (
                state.has_any({item_names.LIBERATOR, item_names.EMPERORS_GUARDIAN}, self.player)
                and state.has(item_names.LIBERATOR_RAID_ARTILLERY, self.player)
            )
            or (
                self.advanced_tactics
                and (
                    state.has_any((
                        item_names.HELS_ANGELS,
                        item_names.DUSK_WINGS,
                        item_names.WINGED_NIGHTMARES,
                        item_names.SIEGE_BREAKERS,
                        item_names.BRYNHILDS,
                        item_names.JACKSONS_REVENGE,
                    ), self.player)
                    or state.has_all((
                        item_names.MIDNIGHT_RIDERS, item_names.LIBERATOR_RAID_ARTILLERY,
                    ), self.player)
                )
            )
        )

    def terran_great_train_robbery_train_stopper(self, state: CollectionState) -> bool:
        """
        Ability to deal with trains (moving target with a lot of HP)
        """
        return state.has_any(
            {item_names.SIEGE_TANK, item_names.DIAMONDBACK, item_names.MARAUDER, item_names.CYCLONE, item_names.BANSHEE}, self.player
        ) or (
            self.advanced_tactics
            and (
                state.has_all({item_names.REAPER, item_names.REAPER_G4_CLUSTERBOMB}, self.player)
                or state.has_all({item_names.SPECTRE, item_names.SPECTRE_PSIONIC_LASH}, self.player)
                or state.has_any({item_names.VULTURE, item_names.LIBERATOR}, self.player)
            )
        )

    def zerg_great_train_robbery_train_stopper(self, state: CollectionState) -> bool:
        """
        Ability to deal with trains (moving target with a lot of HP)
        """
        return (
            state.has_any(
                (
                    item_names.ABERRATION,
                    item_names.INFESTED_DIAMONDBACK,
                    item_names.INFESTED_BANSHEE,
                ),
                self.player,
            )
            or state.has_all({item_names.MUTALISK, item_names.MUTALISK_SUNDERING_GLAIVE}, self.player)
            or state.has_all((item_names.HYDRALISK, item_names.HYDRALISK_MUSCULAR_AUGMENTS), self.player)
            # Note: Zerglings were tested by Snarky, and it was found they'd need >= 3 upgrades to be viable,
            # so they are not included in this logic.
            # Raptor + 2 of (Shredding, Adrenal, +2 attack upgrade)
            or self.zerg_infested_tank_with_ammo(state)
            or (self.advanced_tactics and (self.morph_tyrannozor(state)))
        )

    def protoss_great_train_robbery_train_stopper(self, state: CollectionState) -> bool:
        """
        Ability to deal with trains (moving target with a lot of HP)
        """
        return (
            state.has_any((
                item_names.ANNIHILATOR,
                item_names.IMMORTAL,
                item_names.STALKER,
                item_names.ADEPT,  # Tested by Snarky, "An easy 1-item solve"
                item_names.WRATHWALKER,
                item_names.VOID_RAY,
                item_names.DESTROYER,
            ), self.player)
            or state.has_all((item_names.SLAYER, item_names.SLAYER_PHASE_BLINK), self.player)
            or state.has_all((item_names.REAVER, item_names.REAVER_KHALAI_REPLICATORS), self.player)
            or state.has_all((item_names.VANGUARD, item_names.VANGUARD_FUSION_MORTARS), self.player)
            or (
                state.has(item_names.INSTIGATOR, self.player)
                and state.has_any((item_names.INSTIGATOR_BLINK_OVERDRIVE, item_names.INSTIGATOR_MODERNIZED_SERVOS), self.player)
            )
            or (state.has_all((item_names.OPPRESSOR, item_names.SCOUT_GRAVITIC_THRUSTERS, item_names.SCOUT_ADVANCED_PHOTON_BLASTERS), self.player))
            or state.has_all((item_names.ORACLE, item_names.ORACLE_TEMPORAL_ACCELERATION_BEAM), self.player)
            or (
                self.advanced_tactics
                and (
                    state.has(item_names.TEMPEST, self.player)
                    or state.has_all((item_names.VANGUARD, item_names.VANGUARD_RAPIDFIRE_CANNON), self.player)
                    or state.has_all((item_names.OPPRESSOR, item_names.SCOUT_GRAVITIC_THRUSTERS, item_names.OPPRESSOR_VULCAN_BLASTER), self.player)
                    or state.has_all((item_names.ASCENDANT, item_names.ASCENDANT_POWER_OVERWHELMING, item_names.SUPPLICANT), self.player)
                    or state.has_all(
                        (item_names.DARK_TEMPLAR, item_names.DARK_TEMPLAR_LESSER_SHADOW_FURY, item_names.DARK_TEMPLAR_GREATER_SHADOW_FURY),
                        self.player,
                    )
                    or (
                        state.has(item_names.DARK_TEMPLAR_AVENGER_BLOOD_HUNTER_BLINK, self.player)
                        and (
                            state.has_any((item_names.DARK_TEMPLAR, item_names.AVENGER), self.player)
                            or state.has_all((item_names.BLOOD_HUNTER, item_names.BLOOD_HUNTER_BRUTAL_EFFICIENCY), self.player)
                        )
                    )
                )
            )
        )

    def terran_can_rescue(self, state) -> bool:
        """
        Rescuing in The Moebius Factor
        """
        return (
            state.has_any((
                item_names.MEDIVAC, item_names.HERCULES, item_names.RAVEN, item_names.VIKING
            ), self.player)
            or self.advanced_tactics
        )

    def terran_supernova_requirement(self, state) -> bool:
        return self.terran_beats_protoss_deathball(state) and self.terran_power_rating(state) >= 6

    def zerg_supernova_requirement(self, state) -> bool:
        return (
            self.zerg_common_unit(state)
            and self.zerg_power_rating(state) >= 6
            and (self.advanced_tactics or state.has(item_names.YGGDRASIL, self.player))
        )

    def protoss_supernova_requirement(self, state: CollectionState) -> bool:
        return (
            (
                state.count(item_names.PROGRESSIVE_WARP_RELOCATE, self.player) >= 2
                or (self.advanced_tactics and state.has(item_names.PROGRESSIVE_WARP_RELOCATE, self.player))
            )
            and self.protoss_competent_anti_air(state)
            and (
                self.protoss_fleet(state)
                or (self.protoss_competent_comp(state) and self.protoss_power_rating(state) >= 6)
            )
        )

    def terran_maw_requirement(self, state: CollectionState) -> bool:
        """
        Ability to deal with large areas with environment damage
        """
        return (
            state.has(item_names.BATTLECRUISER, self.player)
            and (
                self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_TERRAN_SHIP_WEAPON, state) >= 2
                or state.has(item_names.BATTLECRUISER_ATX_LASER_BATTERY, self.player)
            )
        ) or (
            self.terran_air(state)
            and (
                # Avoid dropping Troopers or units that do barely damage
                state.has_any(
                    (
                        item_names.GOLIATH,
                        item_names.THOR,
                        item_names.WARHOUND,
                        item_names.VIKING,
                        item_names.BANSHEE,
                        item_names.WRAITH,
                        item_names.BATTLECRUISER,
                    ),
                    self.player,
                )
                or state.has_all((item_names.LIBERATOR, item_names.LIBERATOR_RAID_ARTILLERY), self.player)
                or state.has_all((item_names.VALKYRIE, item_names.VALKYRIE_FLECHETTE_MISSILES), self.player)
                or (state.has(item_names.MARAUDER, self.player) and self.terran_bio_heal(state))
            )
            and (
                # Can deal damage to air units inside rip fields
                state.has_any((item_names.GOLIATH, item_names.CYCLONE, item_names.VIKING), self.player)
                or (
                    state.has_any((item_names.WRAITH, item_names.VALKYRIE, item_names.BATTLECRUISER), self.player)
                    and self.weapon_armor_upgrade_count(item_names.PROGRESSIVE_TERRAN_SHIP_WEAPON, state) >= 2
                )
                or state.has_all((item_names.THOR, item_names.THOR_PROGRESSIVE_HIGH_IMPACT_PAYLOAD), self.player)
            )
            and self.terran_competent_comp(state)
            and self.terran_competent_anti_air(state)
            and self.terran_sustainable_mech_heal(state)
        )

    def zerg_maw_requirement(self, state: CollectionState) -> bool:
        """
        Ability to cross defended gaps, deal with skytoss, and avoid costly losses.
        """
        if self.advanced_tactics and state.has(item_names.INFESTOR, self.player):
            return True
        usable_muta = (
            state.has_all((item_names.MUTALISK, item_names.MUTALISK_RAPID_REGENERATION), self.player)
            and state.count_from_list_unique((
                item_names.MUTALISK_SEVERING_GLAIVE,
                item_names.MUTALISK_SUNDERING_GLAIVE,
                item_names.MUTALISK_VICIOUS_GLAIVE,
            ), self.player) >= 2
        )
        return (
            # Heal
            (
                state.has(item_names.SWARM_QUEEN, self.player)
                or (self.advanced_tactics
                    and (
                        (
                            self.morph_tyrannozor(state)
                            and state.has(item_names.TYRANNOZOR_HEALING_ADAPTATION, self.player)
                        )
                        or usable_muta
                    )
                )
            )
            # Cross the gap
            and (
                state.has_any((item_names.NYDUS_WORM, item_names.OVERLORD_VENTRAL_SACS), self.player)
                or (self.advanced_tactics and state.has(item_names.YGGDRASIL, self.player))
            )
            # Air to ground
            and (self.morph_brood_lord(state) or self.morph_guardian(state) or usable_muta)
            # Ground to air
            and (
                state.has(item_names.INFESTOR, self.player)
                or self.morph_tyrannozor(state)
                or state.has_all(
                    {item_names.SWARM_HOST, item_names.SWARM_HOST_RESOURCE_EFFICIENCY, item_names.SWARM_HOST_PRESSURIZED_GLANDS}, self.player
                )
                or state.has_all({item_names.HYDRALISK, item_names.HYDRALISK_RESOURCE_EFFICIENCY}, self.player)
                or state.has_all({item_names.INFESTED_DIAMONDBACK, item_names.INFESTED_DIAMONDBACK_PROGRESSIVE_FUNGAL_SNARE}, self.player)
            )
            # Survives rip-field
            and (
                state.has_any({item_names.ABERRATION, item_names.ROACH, item_names.ULTRALISK}, self.player)
                or self.morph_tyrannozor(state)
                or (self.advanced_tactics and usable_muta)
            )
            # Air-to-air
            and (state.has_any({item_names.MUTALISK, item_names.CORRUPTOR, item_names.INFESTED_LIBERATOR, item_names.BROOD_QUEEN}, self.player))
            # Upgrades / general
            and self.zerg_competent_anti_air(state)
            and self.zerg_competent_comp(state)
        )

    def protoss_maw_requirement(self, state: CollectionState) -> bool:
        """
        Ability to cross defended gaps and deal with skytoss.
        """
        return (
            (
                state.has(item_names.WARP_PRISM, self.player)
                or (
                    self.advanced_tactics
                    and (state.has(item_names.ARBITER, self.player) or state.has_all((item_names.MISTWING, item_names.MISTWING_PILOT), self.player))
                )
            )
            and self.protoss_common_unit_anti_armor_air(state)
            and self.protoss_fleet(state)
        )

    def terran_engine_of_destruction_requirement(self, state: CollectionState) -> bool:
        power_rating = self.terran_power_rating(state)
        if power_rating < 3 or not self.marine_medic_upgrade(state) or not self.terran_common_unit(state):
            return False
        if power_rating >= 7 and self.terran_competent_comp(state):
            return True
        else:
            return (
                state.has_any((item_names.WRAITH, item_names.BATTLECRUISER), self.player)
                or (self.terran_air_anti_air(state)
                    and state.has_any((item_names.BANSHEE, item_names.LIBERATOR), self.player)
                )
            )

    def zerg_engine_of_destruction_requirement(self, state: CollectionState) -> bool:
        power_rating = self.zerg_power_rating(state)
        if (
            power_rating < 3
            or not self.zergling_hydra_roach_start(state)
            or not self.zerg_common_unit(state)
            or not self.zerg_competent_anti_air(state)
            or not self.zerg_repair_odin(state)
        ):
            return False
        if power_rating >= 7 and self.zerg_competent_comp(state):
            return True
        else:
            return self.zerg_base_buster(state)

    def protoss_engine_of_destruction_requirement(self, state: CollectionState) -> bool:
        return (
            self.zealot_sentry_slayer_start(state)
            and self.protoss_repair_odin(state)
            and (self.protoss_deathball(state) or self.protoss_fleet(state))
        )

    def zerg_repair_odin(self, state: CollectionState) -> bool:
        return (
            self.zerg_has_infested_scv(state)
            or state.has_all({item_names.SWARM_QUEEN_BIO_MECHANICAL_TRANSFUSION, item_names.SWARM_QUEEN}, self.player)
            or (self.advanced_tactics and state.has(item_names.SWARM_QUEEN, self.player))
        )

    def protoss_repair_odin(self, state: CollectionState) -> bool:
        return (
            state.has(item_names.SENTRY, self.player)
            or state.has_all((item_names.CARRIER, item_names.CARRIER_REPAIR_DRONES), self.player)
            or (
                self.spear_of_adun_passive_presence
                in [SpearOfAdunPassiveAbilityPresence.option_protoss, SpearOfAdunPassiveAbilityPresence.option_everywhere]
                and state.has(item_names.RECONSTRUCTION_BEAM, self.player)
            )
            or (self.advanced_tactics and state.has_all({item_names.SHIELD_BATTERY, item_names.KHALAI_INGENUITY}, self.player))
        )

    def terran_in_utter_darkness_requirement(self, state: CollectionState) -> bool:
        return self.terran_competent_comp(state) and self.terran_defense_rating(state, True, True) >= 8

    def zerg_in_utter_darkness_requirement(self, state: CollectionState) -> bool:
        return self.zerg_competent_comp(state) and self.zerg_competent_anti_air(state) and self.zerg_defense_rating(state, True, True) >= 8

    def protoss_in_utter_darkness_requirement(self, state: CollectionState) -> bool:
        return self.protoss_competent_comp(state) and self.protoss_defense_rating(state, True) >= 4

    def terran_all_in_requirement(self, state: CollectionState) -> bool:
        """
        All-in
        """
        if not self.terran_very_hard_mission_weapon_armor_level(state):
            return False
        beats_kerrigan = (
            state.has_any({item_names.MARINE, item_names.DOMINION_TROOPER, item_names.BANSHEE}, self.player)
            or state.has_all({item_names.REAPER, item_names.REAPER_RESOURCE_EFFICIENCY}, self.player)
            or (self.all_in_map == AllInMap.option_air and state.has_all((item_names.VALKYRIE, item_names.VALKYRIE_FLECHETTE_MISSILES), self.player))
            or (self.advanced_tactics and state.has_all((item_names.GHOST, item_names.GHOST_EMP_ROUNDS), self.player))
        )
        if not beats_kerrigan:
            return False
        if not self.terran_competent_comp(state):
            return False
        if self.all_in_map == AllInMap.option_ground:
            # Ground
            defense_rating = self.terran_defense_rating(state, True, False)
            if state.has_any({item_names.BATTLECRUISER, item_names.BANSHEE}, self.player):
                defense_rating += 2
            return defense_rating >= 13
        else:
            # Air
            defense_rating = self.terran_defense_rating(state, True, True)
            return (
                defense_rating >= 9
                and self.terran_competent_anti_air(state)
                and state.has_any({item_names.VIKING, item_names.BATTLECRUISER, item_names.VALKYRIE}, self.player)
                and state.has_any({item_names.HIVE_MIND_EMULATOR, item_names.PSI_DISRUPTER, item_names.MISSILE_TURRET}, self.player)
            )

    def zerg_all_in_requirement(self, state: CollectionState) -> bool:
        """
        All-in (Zerg)
        """
        if not self.zerg_very_hard_mission_weapon_armor_level(state):
            return False
        beats_kerrigan = (
            state.has_any({item_names.INFESTED_MARINE, item_names.INFESTED_BANSHEE, item_names.INFESTED_BUNKER}, self.player)
            or state.has_all({item_names.SWARM_HOST, item_names.SWARM_HOST_RESOURCE_EFFICIENCY}, self.player)
            or self.morph_brood_lord(state)
        )
        if not beats_kerrigan:
            return False
        if not self.zerg_competent_comp(state):
            return False
        if self.all_in_map == AllInMap.option_ground:
            # Ground
            defense_rating = self.zerg_defense_rating(state, True, False)
            if (
                state.has_any({item_names.MUTALISK, item_names.INFESTED_BANSHEE}, self.player)
                or self.morph_brood_lord(state)
                or self.morph_guardian(state)
            ):
                defense_rating += 3
            if state.has(item_names.SPINE_CRAWLER, self.player):
                defense_rating += 2
            return defense_rating >= 13
        else:
            # Air
            defense_rating = self.zerg_defense_rating(state, True, True)
            return (
                defense_rating >= 9
                and state.has_any({item_names.MUTALISK, item_names.CORRUPTOR}, self.player)
                and state.has_any({item_names.SPORE_CRAWLER, item_names.INFESTED_MISSILE_TURRET}, self.player)
            )

    def protoss_all_in_requirement(self, state: CollectionState) -> bool:
        """
        All-in (Protoss)
        """
        if not self.protoss_very_hard_mission_weapon_armor_level(state):
            return False
        beats_kerrigan = (
            # cheap units with multiple small attacks, or anything with Feedback
            state.has_any({item_names.ZEALOT, item_names.SENTINEL, item_names.SKIRMISHER, item_names.HIGH_TEMPLAR}, self.player)
            or state.has_all((item_names.CENTURION, item_names.CENTURION_RESOURCE_EFFICIENCY), self.player)
            or state.has_all({item_names.SIGNIFIER, item_names.SIGNIFIER_FEEDBACK}, self.player)
            or (self.protoss_can_merge_archon(state) and state.has(item_names.ARCHON_HIGH_ARCHON, self.player))
            or (self.protoss_can_merge_dark_archon(state) and state.has(item_names.DARK_ARCHON_FEEDBACK, self.player))
        )
        if not beats_kerrigan:
            return False
        if not self.protoss_competent_comp(state):
            return False
        if self.all_in_map == AllInMap.option_ground:
            # Ground
            defense_rating = self.protoss_defense_rating(state, True)
            if (
                state.has_any({item_names.SKIRMISHER, item_names.DARK_TEMPLAR, item_names.TEMPEST, item_names.TRIREME}, self.player)
                or state.has_all((item_names.BLOOD_HUNTER, item_names.BLOOD_HUNTER_BRUTAL_EFFICIENCY), self.player)
                or state.has_all((item_names.AVENGER, item_names.AVENGER_KRYHAS_CLOAK), self.player)
            ):
                defense_rating += 2
            if state.has(item_names.PHOTON_CANNON, self.player):
                defense_rating += 2
            return defense_rating >= 13
        else:
            # Air
            defense_rating = self.protoss_defense_rating(state, True)
            if state.has(item_names.KHAYDARIN_MONOLITH, self.player):
                defense_rating += 2
            if state.has(item_names.PHOTON_CANNON, self.player):
                defense_rating += 2
            return defense_rating >= 9 and (state.has_any({item_names.TEMPEST, item_names.SKYLORD, item_names.VOID_RAY}, self.player))

    def zerg_can_grab_ghosts_in_the_fog_east_rock_formation(self, state: CollectionState) -> bool:
        return (
            state.has_any({item_names.MUTALISK, item_names.INFESTED_BANSHEE, item_names.OVERLORD_VENTRAL_SACS, item_names.INFESTOR}, self.player)
            or (self.morph_devourer(state) and state.has(item_names.DEVOURER_PRESCIENT_SPORES, self.player))
            or (self.morph_guardian(state) and state.has(item_names.GUARDIAN_PRIMAL_ADAPTATION, self.player))
            or ((self.morph_guardian(state) or self.morph_brood_lord(state)) and self.zerg_basic_air_to_air(state))
            or (
                self.advanced_tactics
                and (
                    state.has_any({item_names.INFESTED_SIEGE_BREAKERS, item_names.INFESTED_DUSK_WINGS}, self.player)
                    or (state.has(item_names.HUNTERLING, self.player) and self.zerg_basic_air_to_air(state))
                )
            )
        )
    def zerg_any_units_back_in_the_saddle_requirement(self, state: CollectionState) -> bool:
        return (
            self.grant_story_tech == GrantStoryTech.option_grant
            # Note(mm): This check isn't necessary as self.kerrigan_levels cover it,
            # and it's not fully desirable in future when we support non-grant story tech + kerriganless.
            # or not self.kerrigan_presence
            or not self.kerrigan_unit_available
            or state.has_any((
                # Cases tested by Snarky
                item_names.KERRIGAN_KINETIC_BLAST,
                item_names.KERRIGAN_LEAPING_STRIKE,
                item_names.KERRIGAN_CRUSHING_GRIP,
                item_names.KERRIGAN_PSIONIC_SHIFT,
                item_names.KERRIGAN_SPAWN_BANELINGS,
                item_names.KERRIGAN_FURY,
                item_names.KERRIGAN_APOCALYPSE,
                item_names.KERRIGAN_DROP_PODS,
                item_names.KERRIGAN_SPAWN_LEVIATHAN,
                item_names.KERRIGAN_IMMOBILIZATION_WAVE,  # Involves a 1-minute cooldown wait before the ultra
                item_names.KERRIGAN_MEND,  # See note from THE EV below
            ), self.player)
            or self.kerrigan_levels(state, 20)
            or (self.kerrigan_levels(state, 10) and state.has(item_names.KERRIGAN_CHAIN_REACTION, self.player))
            # Tested by THE EV, "facetank with Kerrigan and stutter step to the end with >10s left"
            # > have to lure the first group of Zerg in the 2nd timed section into the first room of the second area
            # > (with the heal box) so you can kill them before the timer starts.
            # 
            # phaneros: Technically possible without the levels, but adding them in for safety margin and to hopefully
            # make generation force this branch less often
            or (state.has_any((item_names.KERRIGAN_HEROIC_FORTITUDE, item_names.KERRIGAN_INFEST_BROODLINGS), self.player)
                and self.kerrigan_levels(state, 5)
            )
            # Insufficient: Wild Mutation, Assimilation Aura
        )

    def zerg_pass_vents(self, state: CollectionState) -> bool:
        return (
            self.grant_story_tech == GrantStoryTech.option_grant
            or state.has_any({item_names.ZERGLING, item_names.HYDRALISK, item_names.ROACH}, self.player)
            or (self.advanced_tactics and state.has(item_names.INFESTOR, self.player))
        )

    def supreme_requirement(self, state: CollectionState) -> bool:
        return (
            self.grant_story_tech == GrantStoryTech.option_grant
            or not self.kerrigan_unit_available
            or (self.grant_story_tech == GrantStoryTech.option_allow_substitutes
                and state.has_any((
                    item_names.KERRIGAN_LEAPING_STRIKE,
                    item_names.OVERLORD_VENTRAL_SACS,
                    item_names.YGGDRASIL,
                    item_names.MUTALISK_CORRUPTOR_VIPER_ASPECT,
                    item_names.NYDUS_WORM,
                    item_names.BULLFROG,
                ), self.player)
                and state.has_any((
                    item_names.KERRIGAN_MEND,
                    item_names.SWARM_QUEEN,
                    item_names.INFESTED_MEDICS,
                ), self.player)
                and self.kerrigan_levels(state, 35)
            )
            or (state.has_all((item_names.KERRIGAN_LEAPING_STRIKE, item_names.KERRIGAN_MEND), self.player) and self.kerrigan_levels(state, 35))
        )

    def terran_infested_garrison_claimer(self, state: CollectionState) -> bool:
        return state.has_any((item_names.GHOST, item_names.SPECTRE, item_names.EMPERORS_SHADOW), self.player)

    def protoss_infested_garrison_claimer(self, state: CollectionState) -> bool:
        return state.has_any(
            (item_names.HIGH_TEMPLAR, item_names.SIGNIFIER, item_names.ASCENDANT), self.player
        ) or self.protoss_can_merge_dark_archon(state)

    def terran_hand_of_darkness_requirement(self, state: CollectionState) -> bool:
        return self.terran_competent_comp(state) and self.terran_power_rating(state) >= 6

    def zerg_hand_of_darkness_requirement(self, state: CollectionState) -> bool:
        return (
            self.zerg_competent_comp(state)
            and (self.zerg_competent_anti_air(state) or self.advanced_tactics and self.zerg_moderate_anti_air(state))
            and (self.basic_kerrigan(state, False) or self.zerg_power_rating(state) >= 4)
        )

    def protoss_hand_of_darkness_requirement(self, state: CollectionState) -> bool:
        return self.protoss_competent_comp(state) and self.protoss_power_rating(state) >= 6

    def terran_planetfall_requirement(self, state: CollectionState) -> bool:
        return self.terran_beats_protoss_deathball(state) and self.terran_power_rating(state) >= 8

    def zerg_planetfall_requirement(self, state: CollectionState) -> bool:
        return self.zerg_competent_comp(state) and self.zerg_competent_anti_air(state) and self.zerg_power_rating(state) >= 8

    def protoss_planetfall_requirement(self, state: CollectionState) -> bool:
        return self.protoss_deathball(state) and self.protoss_power_rating(state) >= 8

    def zerg_the_reckoning_requirement(self, state: CollectionState) -> bool:
        if not (self.zerg_power_rating(state) >= 6 or self.basic_kerrigan(state, False)):
            return False
        if self.take_over_ai_allies:
            return (
                self.terran_competent_comp(state)
                and self.zerg_competent_comp(state)
                and (self.zerg_competent_anti_air(state) or self.terran_competent_anti_air(state))
                and self.terran_very_hard_mission_weapon_armor_level(state)
                and self.zerg_very_hard_mission_weapon_armor_level(state)
            )
        else:
            return self.zerg_competent_comp(state) and self.zerg_competent_anti_air(state) and self.zerg_very_hard_mission_weapon_armor_level(state)

    def terran_the_reckoning_requirement(self, state: CollectionState) -> bool:
        return self.terran_very_hard_mission_weapon_armor_level(state) and self.terran_base_trasher(state)

    def protoss_the_reckoning_requirement(self, state: CollectionState) -> bool:
        return (
            self.protoss_very_hard_mission_weapon_armor_level(state)
            and self.protoss_deathball(state)
            and (not self.take_over_ai_allies or (self.terran_competent_comp(state) and self.terran_very_hard_mission_weapon_armor_level(state)))
        )

    def protoss_can_attack_behind_chasm(self, state: CollectionState) -> bool:
        return (
            state.has_any((
                item_names.SCOUT,
                item_names.SKIRMISHER,
                item_names.TEMPEST,
                item_names.CARRIER,
                item_names.SKYLORD,
                item_names.TRIREME,
                item_names.VOID_RAY,
                item_names.DESTROYER,
                item_names.PULSAR,
                item_names.DAWNBRINGER,
                item_names.MOTHERSHIP,
            ), self.player)
            or self.protoss_has_blink(state)
            or (
                state.has(item_names.WARP_PRISM, self.player)
                and (self.protoss_common_unit(state) or state.has(item_names.WARP_PRISM_PHASE_BLASTER, self.player))
            )
            or (self.advanced_tactics and state.has_any({item_names.ORACLE, item_names.ARBITER}, self.player))
        )

    def the_infinite_cycle_requirement(self, state: CollectionState) -> bool:
        return (
            self.kerrigan_levels(state, 70)
            and (
                self.grant_story_tech == GrantStoryTech.option_grant
                or not self.kerrigan_unit_available
                or (
                    state.has_any((
                        item_names.KERRIGAN_KINETIC_BLAST,
                        item_names.KERRIGAN_SPAWN_BANELINGS,
                        item_names.KERRIGAN_LEAPING_STRIKE,
                        item_names.KERRIGAN_SPAWN_LEVIATHAN,
                    ), self.player)
                    and self.basic_kerrigan(state)
                )
            )
        )

    def templars_return_phase_2_requirement(self, state: CollectionState) -> bool:
        return (
            self.grant_story_tech == GrantStoryTech.option_grant
            or self.advanced_tactics
            or (
                state.has_any((
                    item_names.IMMORTAL,
                    item_names.ANNIHILATOR,
                    item_names.VANGUARD,
                    item_names.COLOSSUS,
                    item_names.WRATHWALKER,
                    item_names.REAVER,
                    item_names.DARK_TEMPLAR,
                    item_names.HIGH_TEMPLAR,
                    item_names.ENERGIZER,
                    item_names.SENTRY,
                ), self.player)
            )
        )

    def templars_return_phase_3_reach_colossus_requirement(self, state: CollectionState) -> bool:
        return self.templars_return_phase_2_requirement(state) and (
            self.grant_story_tech == GrantStoryTech.option_grant
            or (self.advanced_tactics
                and state.has_any((
                    item_names.ZEALOT_WHIRLWIND, item_names.VANGUARD_RAPIDFIRE_CANNON,
                ), self.player)
            )
            or state.has_all((
                item_names.ZEALOT_WHIRLWIND, item_names.VANGUARD_RAPIDFIRE_CANNON
            ), self.player)
        )

    def templars_return_phase_3_reach_dts_requirement(self, state: CollectionState) -> bool:
        return self.templars_return_phase_3_reach_colossus_requirement(state) and (
            self.grant_story_tech == GrantStoryTech.option_grant
            or state.has_all((
                item_names.COLOSSUS_PACIFICATION_PROTOCOL,
                item_names.ENERGIZER_MOBILE_CHRONO_BEAM,
            ), self.player)
            or (
                state.has(item_names.COLOSSUS_FIRE_LANCE, self.player)
                and (self.advanced_tactics
                    or state.has(item_names.ENERGIZER_MOBILE_CHRONO_BEAM, self.player)
                )
            )
        )

    def terran_spear_of_adun_requirement(self, state: CollectionState) -> bool:
        return self.terran_common_unit(state) and self.terran_competent_anti_air(state) and self.terran_defense_rating(state, False, False) >= 5

    def zerg_spear_of_adun_requirement(self, state: CollectionState) -> bool:
        return self.zerg_common_unit(state) and self.zerg_competent_anti_air(state) and self.zerg_defense_rating(state, False, False) >= 5

    def protoss_spear_of_adun_requirement(self, state: CollectionState) -> bool:
        return (
            self.protoss_common_unit(state)
            and self.protoss_anti_light_anti_air(state)
            and (
                state.has_any((item_names.ZEALOT, item_names.CENTURION, item_names.SENTINEL, item_names.ADEPT), self.player)
                or self.protoss_basic_splash(state)
            )
            and self.protoss_defense_rating(state, False) >= 5
        )

    def terran_sky_shield_requirement(self, state: CollectionState) -> bool:
        return self.terran_common_unit(state) and self.terran_competent_anti_air(state) and self.terran_power_rating(state) >= 7

    def zerg_sky_shield_requirement(self, state: CollectionState) -> bool:
        return self.zerg_common_unit(state) and self.zerg_competent_anti_air(state) and self.zerg_power_rating(state) >= 7

    def protoss_sky_shield_requirement(self, state: CollectionState) -> bool:
        return self.protoss_common_unit(state) and self.protoss_competent_anti_air(state) and self.protoss_power_rating(state) >= 7

    def protoss_brothers_in_arms_requirement(self, state: CollectionState) -> bool:
        return (self.protoss_common_unit(state) and self.protoss_anti_armor_anti_air(state) and self.protoss_hybrid_counter(state)) or (
            self.take_over_ai_allies
            and (self.terran_common_unit(state) or self.protoss_common_unit(state))
            and (self.terran_competent_anti_air(state) or self.protoss_anti_armor_anti_air(state))
            and (
                self.protoss_hybrid_counter(state)
                or state.has_any({item_names.BATTLECRUISER, item_names.LIBERATOR, item_names.SIEGE_TANK}, self.player)
                or (self.advanced_tactics and state.has_all({item_names.SPECTRE, item_names.SPECTRE_PSIONIC_LASH}, self.player))
                or (
                    state.has(item_names.IMMORTAL, self.player)
                    and state.has_any({item_names.MARINE, item_names.DOMINION_TROOPER, item_names.MARAUDER}, self.player)
                    and self.terran_bio_heal(state)
                )
            )
        )

    def zerg_brothers_in_arms_requirement(self, state: CollectionState) -> bool:
        return (
            self.zerg_common_unit(state) and self.zerg_competent_comp(state) and self.zerg_competent_anti_air(state) and self.zerg_big_monsters(state)
        ) or (
            self.take_over_ai_allies
            and (self.zerg_common_unit(state) or self.terran_common_unit(state))
            and (self.terran_competent_anti_air(state) or self.zerg_competent_anti_air(state))
            and (
                self.zerg_big_monsters(state)
                or state.has_any({item_names.BATTLECRUISER, item_names.LIBERATOR, item_names.SIEGE_TANK}, self.player)
                or (self.advanced_tactics and state.has_all({item_names.SPECTRE, item_names.SPECTRE_PSIONIC_LASH}, self.player))
                or (
                    state.has(item_names.ABERRATION, self.player)
                    and state.has_any({item_names.MARINE, item_names.DOMINION_TROOPER, item_names.MARAUDER}, self.player)
                    and self.terran_bio_heal(state)
                )
            )
        )

    def protoss_amons_reach_requirement(self, state: CollectionState) -> bool:
        return self.protoss_common_unit_anti_light_air(state) and self.protoss_basic_splash(state) and self.protoss_power_rating(state) >= 7

    def protoss_last_stand_requirement(self, state: CollectionState) -> bool:
        return (
            self.protoss_common_unit(state)
            and self.protoss_competent_anti_air(state)
            and self.protoss_static_defense(state)
            and self.protoss_defense_rating(state, False) >= 8
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
                or state.has_all({item_names.MUTALISK, item_names.MUTALISK_SEVERING_GLAIVE, item_names.MUTALISK_VICIOUS_GLAIVE}, self.player)
                or self.zerg_infested_tank_with_ammo(state)
                or (self.advanced_tactics
                    and state.has_all((item_names.ULTRALISK, item_names.ULTRALISK_CHITINOUS_PLATING, item_names.ULTRALISK_MONARCH_BLADES), self.player)
                )
            )
            and (
                self.morph_impaler(state)
                or state.has_all({item_names.INFESTED_LIBERATOR, item_names.INFESTED_LIBERATOR_DEFENDER_MODE}, self.player)
                or self.zerg_infested_tank_with_ammo(state)
                or state.has(item_names.BILE_LAUNCHER, self.player)
            )
            and (
                self.morph_devourer(state)
                or state.has_all({item_names.MUTALISK, item_names.MUTALISK_SUNDERING_GLAIVE}, self.player)
                or (self.advanced_tactics
                    and state.has(item_names.BROOD_QUEEN, self.player)
                )
            )
            and self.zerg_mineral_dump(state)
            and self.zerg_army_weapon_armor_upgrade_min_level(state) >= 2
        )

    def terran_temple_of_unification_requirement(self, state: CollectionState) -> bool:
        return self.terran_beats_protoss_deathball(state) and self.terran_power_rating(state) >= 10

    def zerg_temple_of_unification_requirement(self, state: CollectionState) -> bool:
        # Don't be locked to roach/hydra
        return (
            self.zerg_competent_comp(state)
            and self.zerg_competent_anti_air(state)
            and (
                state.has(item_names.INFESTED_BANSHEE, self.player)
                or state.has_all((item_names.INFESTED_LIBERATOR, item_names.INFESTED_LIBERATOR_DEFENDER_MODE), self.player)
                or state.has_all({item_names.MUTALISK, item_names.MUTALISK_SUNDERING_GLAIVE}, self.player)
                or self.zerg_big_monsters(state)
                or (
                    self.advanced_tactics
                    and (state.has_any({item_names.INFESTOR, item_names.DEFILER, item_names.BROOD_QUEEN}, self.player) or self.morph_viper(state))
                )
            )
            and self.zerg_power_rating(state) >= 10
        )

    def protoss_temple_of_unification_requirement(self, state: CollectionState) -> bool:
        return self.protoss_competent_comp(state) and self.protoss_power_rating(state) >= 10

    def protoss_harbinger_of_oblivion_requirement(self, state: CollectionState) -> bool:
        return (
            self.protoss_anti_armor_anti_air(state)
            and (
                (self.protoss_competent_comp(state) and self.protoss_hybrid_counter(state))
                or (self.take_over_ai_allies
                    and (self.protoss_common_unit(state) or self.zerg_common_unit(state))
                )
            )
            and self.protoss_power_rating(state) >= 6
        )

    def terran_harbinger_of_oblivion_requirement(self, state: CollectionState) -> bool:
        return (
            self.terran_competent_anti_air(state)
            and (
                (
                    self.terran_beats_protoss_deathball(state)
                    and state.has_any((
                        item_names.BATTLECRUISER,
                        item_names.LIBERATOR,
                        item_names.SIEGE_TANK,
                        item_names.THOR,
                    ), self.player)
                )
                or (
                    self.take_over_ai_allies
                    and (self.terran_common_unit(state) or self.zerg_common_unit(state))
                )
            )
            and self.terran_power_rating(state) >= 6
        )

    def zerg_harbinger_of_oblivion_requirement(self, state: CollectionState) -> bool:
        return (
            self.zerg_competent_anti_air(state)
            and self.zerg_common_unit(state)
            and (self.take_over_ai_allies or (self.zerg_competent_comp(state) and self.zerg_big_monsters(state)))
            and self.zerg_power_rating(state) >= 6
        )
    
    def protoss_unsealing_the_past_ledge_requirement(self, state: CollectionState) -> bool:
        return (
            state.has_any((item_names.COLOSSUS, item_names.WRATHWALKER), self.player)
            or self.protoss_can_attack_behind_chasm(state)
        )

    def terran_unsealing_the_past_requirement(self, state: CollectionState) -> bool:
        return (
            self.terran_competent_anti_air(state)
            and self.terran_competent_comp(state)
            and self.terran_power_rating(state) >= 6
            and (
                state.has_all((item_names.SIEGE_TANK, item_names.SIEGE_TANK_JUMP_JETS), self.player)
                or state.has_all(
                    {item_names.BATTLECRUISER, item_names.BATTLECRUISER_ATX_LASER_BATTERY, item_names.BATTLECRUISER_MOIRAI_IMPULSE_DRIVE}, self.player
                )
                or (
                    self.advanced_tactics
                    and (
                        state.has_all({item_names.SIEGE_TANK, item_names.SIEGE_TANK_SMART_SERVOS}, self.player)
                        or (
                            state.has_all({item_names.LIBERATOR, item_names.LIBERATOR_SMART_SERVOS}, self.player)
                            and (
                                (
                                    (
                                        state.has_all((item_names.HELLION, item_names.HELLION_HELLBAT), self.player)
                                        or state.has(item_names.FIREBAT, self.player)
                                    )
                                    and self.terran_bio_heal(state)
                                )
                                or state.has_all({item_names.VIKING, item_names.VIKING_SHREDDER_ROUNDS}, self.player)
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
            and self.zerg_power_rating(state) >= 6
            and (
                self.morph_brood_lord(state)
                or self.zerg_big_monsters(state)
                or state.has_all({item_names.MUTALISK, item_names.MUTALISK_SEVERING_GLAIVE, item_names.MUTALISK_VICIOUS_GLAIVE}, self.player)
                or (
                    self.advanced_tactics
                    and (self.morph_igniter(state) or (self.morph_lurker(state) and state.has(item_names.LURKER_SEISMIC_SPINES, self.player)))
                )
            )
        )

    def terran_purification_requirement(self, state: CollectionState) -> bool:
        return (
            self.terran_competent_comp(state)
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
                        or (self.advanced_tactics and state.has(item_names.BANSHEE_ROCKET_BARRAGE, self.player))
                    )
                )
            )
        )

    def zerg_purification_requirement(self, state: CollectionState) -> bool:
        return (
            self.zerg_competent_comp(state)
            and self.zerg_competent_anti_air(state)
            and self.zerg_defense_rating(state, True, True) >= 5
            and self.zerg_big_monsters(state)
            and (state.has(item_names.ULTRALISK, self.player) or self.morph_igniter(state) or self.morph_lurker(state))
        )

    def protoss_steps_of_the_rite_requirement(self, state: CollectionState) -> bool:
        return self.protoss_deathball(state) or self.protoss_fleet(state)

    def terran_steps_of_the_rite_requirement(self, state: CollectionState) -> bool:
        return (
            self.terran_beats_protoss_deathball(state)
            and (
                state.has_any({item_names.SIEGE_TANK, item_names.LIBERATOR}, self.player)
                or state.has_all({item_names.BATTLECRUISER, item_names.BATTLECRUISER_ATX_LASER_BATTERY}, self.player)
                or state.has_all((item_names.BANSHEE, item_names.BANSHEE_SHOCKWAVE_MISSILE_BATTERY), self.player)
            )
            and (
                state.has_all({item_names.BATTLECRUISER, item_names.BATTLECRUISER_ATX_LASER_BATTERY}, self.player)
                or state.has(item_names.VALKYRIE, self.player)
                or state.has_all((item_names.VIKING, item_names.VIKING_RIPWAVE_MISSILES), self.player)
            )
            and self.terran_very_hard_mission_weapon_armor_level(state)
        )

    def zerg_steps_of_the_rite_requirement(self, state: CollectionState) -> bool:
        return (
            self.zerg_competent_comp(state)
            and self.zerg_competent_anti_air(state)
            and self.zerg_base_buster(state)
            and (
                self.morph_lurker(state)
                or self.zerg_infested_tank_with_ammo(state)
                or state.has_all({item_names.INFESTED_LIBERATOR, item_names.INFESTED_LIBERATOR_DEFENDER_MODE}, self.player)
                or (state.has(item_names.SWARM_QUEEN, self.player) and self.zerg_big_monsters(state))
            )
            and (
                state.has(item_names.INFESTED_LIBERATOR, self.player)
                or state.has_all({item_names.MUTALISK, item_names.MUTALISK_SEVERING_GLAIVE, item_names.MUTALISK_VICIOUS_GLAIVE}, self.player)
                or (state.has(item_names.MUTALISK, self.player) and self.morph_devourer(state))
            )
        )

    def terran_rak_shir_requirement(self, state: CollectionState) -> bool:
        return self.terran_beats_protoss_deathball(state) and self.terran_power_rating(state) >= 10

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
                    and (state.has(item_names.MUTALISK_SUNDERING_GLAIVE, self.player) or self.morph_devourer(state))
                )
                or state.has(item_names.CORRUPTOR, self.player)
                or (self.advanced_tactics and state.has(item_names.INFESTOR, self.player))
            )
            and self.zerg_power_rating(state) >= 10
        )

    def protoss_rak_shir_requirement(self, state: CollectionState) -> bool:
        return (self.protoss_deathball(state) or self.protoss_fleet(state)) and self.protoss_power_rating(state) >= 10

    def protoss_templars_charge_requirement(self, state: CollectionState) -> bool:
        return (
            self.protoss_heal(state)
            and self.protoss_anti_armor_anti_air(state)
            and (
                self.protoss_fleet(state)
                or (
                    self.advanced_tactics
                    and self.protoss_competent_comp(state)
                    and (
                        state.has_any((item_names.ARBITER, item_names.CORSAIR, item_names.PHOENIX), self.player)
                        or state.has_all((item_names.MIRAGE, item_names.MIRAGE_GRAVITON_BEAM), self.player)
                    )
                )
            )
        )

    def terran_templars_charge_requirement(self, state: CollectionState) -> bool:
        return self.terran_very_hard_mission_weapon_armor_level(state) and (
            (
                state.has_all({item_names.BATTLECRUISER, item_names.BATTLECRUISER_ATX_LASER_BATTERY}, self.player)
                and state.count(item_names.BATTLECRUISER_PROGRESSIVE_DEFENSIVE_MATRIX, self.player) >= 2
            )
            or (
                self.terran_air_anti_air(state)
                and self.terran_sustainable_mech_heal(state)
                and (
                    state.has_any({item_names.BANSHEE, item_names.BATTLECRUISER}, self.player)
                    or state.has_all({item_names.LIBERATOR, item_names.LIBERATOR_RAID_ARTILLERY}, self.player)
                    or (self.advanced_tactics and (state.has_all({item_names.WRAITH, item_names.WRAITH_ADVANCED_LASER_TECHNOLOGY}, self.player)))
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
                    and (
                        state.has_all(
                            {
                                item_names.MUTALISK,
                                item_names.MUTALISK_SEVERING_GLAIVE,
                                item_names.MUTALISK_VICIOUS_GLAIVE,
                                item_names.MUTALISK_AERODYNAMIC_GLAIVE_SHAPE,
                            },
                            self.player,
                        )
                        or self.morph_viper(state)
                    )
                )
            )
            and (
                state.has_all({item_names.INFESTED_LIBERATOR, item_names.INFESTED_LIBERATOR_CLOUD_DISPERSAL}, self.player)
                or (self.morph_devourer(state) and state.has(item_names.MUTALISK, self.player))
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
                self.protoss_deathball(state)
                and (
                    state.has(item_names.SOA_TIME_STOP, self.player)
                    or (self.advanced_tactics
                        and (state.has_any((item_names.SOA_SHIELD_OVERCHARGE, item_names.SOA_SOLAR_BOMBARDMENT), self.player))
                    )
                )
            )
        )

    def terran_the_host_requirement(self, state: CollectionState) -> bool:
        return (
            self.terran_beats_protoss_deathball(state)
            and self.terran_very_hard_mission_weapon_armor_level(state)
            and (
                (
                    state.has_all({item_names.BATTLECRUISER, item_names.BATTLECRUISER_ATX_LASER_BATTERY}, self.player)
                    and state.count(item_names.BATTLECRUISER_PROGRESSIVE_DEFENSIVE_MATRIX, self.player) >= 2
                )
                or (
                    self.terran_air_anti_air(state)
                    and self.terran_sustainable_mech_heal(state)
                    and (
                        state.has_any({item_names.BANSHEE, item_names.BATTLECRUISER}, self.player)
                        or state.has_all({item_names.LIBERATOR, item_names.LIBERATOR_RAID_ARTILLERY}, self.player)
                    )
                )
                or (
                    (
                        self.spear_of_adun_presence == SpearOfAdunPresence.option_everywhere
                        or self.spear_of_adun_presence == SpearOfAdunPresence.option_any_race_lotv
                    )
                    and (
                        state.has(item_names.SOA_TIME_STOP, self.player)
                        or (self.advanced_tactics
                            and (
                                state.has_any((
                                    item_names.SOA_SHIELD_OVERCHARGE,
                                    item_names.SOA_SOLAR_BOMBARDMENT,
                                ), self.player)
                            )
                        )
                    )
                )
            )
        )

    def zerg_the_host_requirement(self, state: CollectionState) -> bool:
        return (
            self.zerg_competent_comp(state)
            and self.zerg_competent_anti_air(state)
            and self.zerg_very_hard_mission_weapon_armor_level(state)
            and self.zerg_base_buster(state)
            and self.zerg_big_monsters(state)
            and (
                (
                    (
                        (self.morph_brood_lord(state) or self.morph_guardian(state))
                        and (
                                self.morph_devourer(state) and state.has(item_names.MUTALISK, self.player)
                                or state.has_all(
                                (
                                    item_names.INFESTED_LIBERATOR,
                                    item_names.INFESTED_LIBERATOR_CLOUD_DISPERSAL
                                ),
                                self.player
                            )
                        )
                    )
                    or (
                        state.has_all(
                            (
                                item_names.MUTALISK,
                                item_names.MUTALISK_SEVERING_GLAIVE,
                                item_names.MUTALISK_VICIOUS_GLAIVE,
                                item_names.MUTALISK_SUNDERING_GLAIVE,
                                item_names.MUTALISK_RAPID_REGENERATION,
                            ),
                            self.player,
                        )
                    )
                )
                or (
                    (
                        self.spear_of_adun_presence == SpearOfAdunPresence.option_everywhere
                        or self.spear_of_adun_presence == SpearOfAdunPresence.option_any_race_lotv
                    )
                    and (
                        state.has(item_names.SOA_TIME_STOP, self.player)
                        or (self.advanced_tactics
                            and (
                                state.has_any((
                                    item_names.SOA_SHIELD_OVERCHARGE,
                                    item_names.SOA_SOLAR_BOMBARDMENT
                                ), self.player)
                            )
                        )
                    )
                )
            )
        )

    def protoss_salvation_requirement(self, state: CollectionState) -> bool:
        return (
            ([self.protoss_competent_comp(state), self.protoss_fleet(state), self.protoss_static_defense(state)].count(True) >= 2)
            and self.protoss_very_hard_mission_weapon_armor_level(state)
            and self.protoss_power_rating(state) >= 6
        )

    def terran_salvation_requirement(self, state: CollectionState) -> bool:
        return (
            self.terran_beats_protoss_deathball(state)
            and self.terran_very_hard_mission_weapon_armor_level(state)
            and self.terran_air_anti_air(state)
            and state.has_any({item_names.SIEGE_TANK, item_names.LIBERATOR}, self.player)
            and state.has_any({item_names.PERDITION_TURRET, item_names.DEVASTATOR_TURRET, item_names.PLANETARY_FORTRESS}, self.player)
            and self.terran_power_rating(state) >= 6
        )

    def zerg_salvation_requirement(self, state: CollectionState) -> bool:
        return (
            self.zerg_competent_comp(state)
            and self.zerg_competent_anti_air(state)
            and state.has(item_names.SPINE_CRAWLER, self.player)
            and self.zerg_very_hard_mission_weapon_armor_level(state)
            and (
                self.morph_impaler_or_lurker(state)
                or state.has_all({item_names.INFESTED_LIBERATOR, item_names.INFESTED_LIBERATOR_DEFENDER_MODE}, self.player)
                or state.has_all({item_names.MUTALISK, item_names.MUTALISK_SEVERING_GLAIVE, item_names.MUTALISK_VICIOUS_GLAIVE}, self.player)
            )
            and (
                state.has_all({item_names.INFESTED_LIBERATOR, item_names.INFESTED_LIBERATOR_CLOUD_DISPERSAL}, self.player)
                or (self.morph_devourer(state) and state.has(item_names.MUTALISK, self.player))
                or state.has_all({item_names.MUTALISK, item_names.MUTALISK_SUNDERING_GLAIVE}, self.player)
            )
            and self.zerg_power_rating(state) >= 6
        )

    def into_the_void_requirement(self, state: CollectionState) -> bool:
        if not self.protoss_very_hard_mission_weapon_armor_level(state):
            return False
        if self.take_over_ai_allies and not (
            self.terran_very_hard_mission_weapon_armor_level(state) and self.zerg_very_hard_mission_weapon_armor_level(state)
        ):
            return False
        return self.protoss_competent_comp(state) or (
            self.take_over_ai_allies
            and (
                state.has(item_names.BATTLECRUISER, self.player)
                or (state.has(item_names.ULTRALISK, self.player) and self.protoss_competent_anti_air(state))
            )
        )

    def essence_of_eternity_requirement(self, state: CollectionState) -> bool:
        if not self.terran_very_hard_mission_weapon_armor_level(state):
            return False
        if self.take_over_ai_allies and not (
            self.protoss_very_hard_mission_weapon_armor_level(state) and self.zerg_very_hard_mission_weapon_armor_level(state)
        ):
            return False
        defense_score = self.terran_defense_rating(state, False, True)
        if self.take_over_ai_allies and self.protoss_static_defense(state):
            defense_score += 2
        return (
            defense_score >= 12
            and (self.terran_competent_anti_air(state) or self.take_over_ai_allies and self.protoss_competent_anti_air(state))
            and (
                state.has(item_names.BATTLECRUISER, self.player)
                or (
                    state.has_any((item_names.BANSHEE, item_names.LIBERATOR), self.player)
                    and state.has_any({item_names.VIKING, item_names.VALKYRIE}, self.player)
                )
                or self.take_over_ai_allies
                and self.protoss_fleet(state)
            )
            and self.terran_power_rating(state) >= 6
        )

    def amons_fall_requirement(self, state: CollectionState) -> bool:
        if not self.zerg_very_hard_mission_weapon_armor_level(state):
            return False
        if not self.zerg_competent_anti_air(state):
            return False
        if self.zerg_power_rating(state) < 6:
            return False
        if self.take_over_ai_allies and not (
            self.terran_very_hard_mission_weapon_armor_level(state) and self.protoss_very_hard_mission_weapon_armor_level(state)
        ):
            return False
        if self.take_over_ai_allies:
            return (
                (
                    state.has_any({item_names.BATTLECRUISER, item_names.CARRIER, item_names.SKYLORD, item_names.TRIREME}, self.player)
                    or (
                        state.has(item_names.ULTRALISK, self.player)
                        and self.protoss_competent_anti_air(state)
                        and (
                            state.has_any({item_names.LIBERATOR, item_names.BANSHEE, item_names.VALKYRIE, item_names.VIKING}, self.player)
                            or state.has_all({item_names.WRAITH, item_names.WRAITH_ADVANCED_LASER_TECHNOLOGY}, self.player)
                            or self.protoss_fleet(state)
                        )
                        and (
                            self.terran_sustainable_mech_heal(state)
                            or (
                                self.spear_of_adun_passive_presence == SpearOfAdunPassiveAbilityPresence.option_everywhere
                                and state.has(item_names.RECONSTRUCTION_BEAM, self.player)
                            )
                        )
                    )
                )
                and self.terran_competent_anti_air(state)
                and self.protoss_deathball(state)
                and self.zerg_competent_comp(state)
            )
        else:
            return (
                (
                    state.has_any((item_names.MUTALISK, item_names.CORRUPTOR, item_names.BROOD_QUEEN, item_names.INFESTED_BANSHEE), self.player)
                    or state.has_all((item_names.INFESTED_LIBERATOR, item_names.INFESTED_LIBERATOR_CLOUD_DISPERSAL), self.player)
                    or state.has_all((item_names.SCOURGE, item_names.SCOURGE_RESOURCE_EFFICIENCY), self.player)
                    or self.morph_brood_lord(state)
                    or self.morph_guardian(state)
                    or self.morph_devourer(state)
                )
                or (self.advanced_tactics and self.spread_creep(state, False) and self.zerg_big_monsters(state))
            ) and self.zerg_competent_comp(state)

    def the_escape_stuff_granted(self) -> bool:
        """
        The NCO first mission requires having too much stuff first before actually able to do anything
        :return:
        """
        return self.grant_story_tech == GrantStoryTech.option_grant or (self.mission_order == MissionOrder.option_vanilla and self.enabled_campaigns == {SC2Campaign.NCO})

    def the_escape_first_stage_requirement(self, state: CollectionState) -> bool:
        return self.the_escape_stuff_granted() or (self.nova_ranged_weapon(state) and (self.nova_full_stealth(state) or self.nova_heal(state)))

    def the_escape_requirement(self, state: CollectionState) -> bool:
        return self.the_escape_first_stage_requirement(state) and (self.the_escape_stuff_granted() or self.nova_splash(state))

    def terran_able_to_snipe_defiler(self, state: CollectionState) -> bool:
        return (
            state.has(item_names.BANSHEE, self.player)
            or (
                state.has(item_names.NOVA_JUMP_SUIT_MODULE, self.player)
                and (state.has_any({item_names.NOVA_DOMINATION, item_names.NOVA_C20A_CANISTER_RIFLE, item_names.NOVA_PULSE_GRENADES}, self.player))
            )
            or (state.has_all({item_names.SIEGE_TANK, item_names.SIEGE_TANK_MAELSTROM_ROUNDS, item_names.SIEGE_TANK_JUMP_JETS}, self.player))
        )

    def sudden_strike_requirement(self, state: CollectionState) -> bool:
        return (
            self.terran_able_to_snipe_defiler(state)
            and (self.terran_cliffjumper(state) or state.has(item_names.BANSHEE, self.player))
            and self.nova_splash(state)
            and self.terran_defense_rating(state, True, False) >= 3
            and (self.advanced_tactics
                or state.has(item_names.NOVA_JUMP_SUIT_MODULE, self.player)
            )
        )

    def enemy_intelligence_garrisonable_unit(self, state: CollectionState) -> bool:
        """
        Has unit usable as a Garrison in Enemy Intelligence
        """
        return (
            state.has_any((
                item_names.MARINE,
                item_names.SON_OF_KORHAL,
                item_names.REAPER,
                item_names.MARAUDER,
                item_names.GHOST,
                item_names.SPECTRE,
                item_names.HELLION,
                item_names.GOLIATH,
                item_names.WARHOUND,
                item_names.DIAMONDBACK,
                item_names.VIKING,
                item_names.DOMINION_TROOPER,
            ), self.player)
            or (self.advanced_tactics
                and state.has(item_names.ROGUE_FORCES, self.player)
                and state.count_from_list((
                    item_names.WAR_PIGS,
                    item_names.HAMMER_SECURITIES,
                    item_names.DEATH_HEADS,
                    item_names.SPARTAN_COMPANY,
                    item_names.HELS_ANGELS,
                    item_names.BRYNHILDS,
                ), self.player) >= 3
            )
        )

    def enemy_intelligence_cliff_garrison(self, state: CollectionState) -> bool:
        return (
            state.has_any((item_names.REAPER, item_names.VIKING), self.player)
            or (state.has_any((item_names.MEDIVAC, item_names.HERCULES), self.player)
                and self.enemy_intelligence_garrisonable_unit(state)
            )
            or state.has_all({item_names.GOLIATH, item_names.GOLIATH_JUMP_JETS}, self.player)
            or (self.advanced_tactics and state.has_any({item_names.HELS_ANGELS, item_names.BRYNHILDS}, self.player))
        )

    def enemy_intelligence_first_stage_requirement(self, state: CollectionState) -> bool:
        return (
            self.enemy_intelligence_garrisonable_unit(state)
            and (
                self.terran_competent_comp(state)
                or (self.terran_common_unit(state) and self.terran_competent_anti_air(state) and state.has(item_names.NOVA_NUKE, self.player))
            )
            and self.terran_defense_rating(state, True, True) >= 5
        )

    def enemy_intelligence_second_stage_requirement(self, state: CollectionState) -> bool:
        return (
            self.enemy_intelligence_first_stage_requirement(state)
            and self.enemy_intelligence_cliff_garrison(state)
            and (
                self.grant_story_tech == GrantStoryTech.option_grant
                or (
                    self.nova_any_weapon(state)
                    and (self.nova_full_stealth(state) or (self.nova_heal(state) and self.nova_splash(state) and self.nova_ranged_weapon(state)))
                )
            )
        )

    def enemy_intelligence_third_stage_requirement(self, state: CollectionState) -> bool:
        return self.enemy_intelligence_second_stage_requirement(state) and (
            self.grant_story_tech == GrantStoryTech.option_grant or (state.has(item_names.NOVA_PROGRESSIVE_STEALTH_SUIT_MODULE, self.player) and self.nova_dash(state))
        )

    def enemy_intelligence_cliff_garrison_and_nova_mobility(self, state: CollectionState) -> bool:
        return self.enemy_intelligence_cliff_garrison(state) and (
            self.nova_any_nobuild_damage(state)
            or (
                state.has(item_names.NOVA_PROGRESSIVE_STEALTH_SUIT_MODULE, self.player, 2)
                and state.has_any((item_names.NOVA_FLASHBANG_GRENADES, item_names.NOVA_BLINK), self.player)
            )
        )

    def trouble_in_paradise_requirement(self, state: CollectionState) -> bool:
        return (
            self.nova_any_weapon(state)
            and self.nova_splash(state)
            and self.terran_beats_protoss_deathball(state)
            and self.terran_defense_rating(state, True, True) >= 7
            and self.terran_power_rating(state) >= 5
        )

    def night_terrors_requirement(self, state: CollectionState) -> bool:
        return (
            self.terran_common_unit(state)
            and self.terran_competent_anti_air(state)
            and (
                # These can handle the waves of infested, even volatile ones
                state.has(item_names.SIEGE_TANK, self.player)
                or state.has_all({item_names.VIKING, item_names.VIKING_SHREDDER_ROUNDS}, self.player)
                or state.has_all((item_names.BANSHEE, item_names.BANSHEE_SHOCKWAVE_MISSILE_BATTERY), self.player)
                or (
                    (
                        # Regular infesteds
                        (
                            self.terran_bio_heal(state)
                            and (
                                state.has_any((item_names.FIREBAT, item_names.REAPER), self.player)
                                or state.has_all((item_names.HELLION, item_names.HELLION_HELLBAT), self.player)
                            )
                        )
                        or (self.advanced_tactics and state.has_any((item_names.PERDITION_TURRET, item_names.PLANETARY_FORTRESS), self.player))
                    )
                    and (
                        # Volatile infesteds
                        state.has(item_names.LIBERATOR, self.player)
                        or (
                            self.advanced_tactics
                            and (state.has(item_names.VULTURE, self.player)
                                or (state.has(item_names.HERC, self.player) and self.terran_bio_heal(state))
                            )
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
            and self.nova_splash(state)
            and (self.advanced_tactics or self.terran_competent_ground_to_air(state))
        )

    def enemy_shadow_tripwires_tool(self, state: CollectionState) -> bool:
        return state.has_any({item_names.NOVA_FLASHBANG_GRENADES, item_names.NOVA_BLINK, item_names.NOVA_DOMINATION}, self.player)

    def enemy_shadow_door_unlocks_tool(self, state: CollectionState) -> bool:
        return state.has_any({item_names.NOVA_DOMINATION, item_names.NOVA_BLINK, item_names.NOVA_JUMP_SUIT_MODULE}, self.player)

    def enemy_shadow_nova_damage_and_blazefire_unlock(self, state: CollectionState) -> bool:
        return self.nova_any_nobuild_damage(state) and (
            state.has(item_names.NOVA_BLINK, self.player) or state.has_all((item_names.NOVA_HOLO_DECOY, item_names.NOVA_DOMINATION), self.player)
        )

    def enemy_shadow_domination(self, state: CollectionState) -> bool:
        return self.grant_story_tech == GrantStoryTech.option_grant or (
            self.nova_ranged_weapon(state)
            and (
                self.nova_full_stealth(state)
                or state.has(item_names.NOVA_JUMP_SUIT_MODULE, self.player)
                or (self.nova_heal(state) and self.nova_splash(state))
            )
        )

    def enemy_shadow_first_stage(self, state: CollectionState) -> bool:
        return self.enemy_shadow_domination(state) and (
            self.grant_story_tech == GrantStoryTech.option_grant
            or (self.nova_full_stealth(state)
                and self.enemy_shadow_tripwires_tool(state)
            )
            or (self.nova_heal(state)
                and self.nova_splash(state)
            )
        )

    def enemy_shadow_second_stage(self, state: CollectionState) -> bool:
        return self.enemy_shadow_first_stage(state) and (
            self.grant_story_tech == GrantStoryTech.option_grant
            or (
                (self.advanced_tactics or state.has(item_names.NOVA_GHOST_VISOR, self.player))
                and (
                    self.nova_splash(state)
                    or self.nova_heal(state)
                    or self.nova_escape_assist(state)
                )
            )
        )

    def enemy_shadow_door_controls(self, state: CollectionState) -> bool:
        return self.enemy_shadow_second_stage(state) and (self.grant_story_tech == GrantStoryTech.option_grant or self.enemy_shadow_door_unlocks_tool(state))

    def enemy_shadow_victory(self, state: CollectionState) -> bool:
        return self.enemy_shadow_door_controls(state) and (self.grant_story_tech == GrantStoryTech.option_grant or (self.nova_heal(state) and self.nova_beat_stone(state)))

    def dark_skies_requirement(self, state: CollectionState) -> bool:
        return self.terran_common_unit(state) and self.terran_beats_protoss_deathball(state) and self.terran_defense_rating(state, False, True) >= 8

    def end_game_requirement(self, state: CollectionState) -> bool:
        return (
            self.terran_competent_comp(state)
            and self.terran_mobile_detector(state)
            and self.nova_any_weapon(state)
            and self.nova_splash(state)
            and (
                # Xanthos
                state.has_any((item_names.BATTLECRUISER, item_names.VIKING, item_names.WARHOUND), self.player)
                or state.has_all((item_names.LIBERATOR, item_names.LIBERATOR_SMART_SERVOS), self.player)
                or state.has_all((item_names.THOR, item_names.THOR_PROGRESSIVE_HIGH_IMPACT_PAYLOAD), self.player)
                or (
                    state.has(item_names.VALKYRIE, self.player)
                    and state.has_any((item_names.VALKYRIE_AFTERBURNERS, item_names.VALKYRIE_SHAPED_HULL), self.player)
                    and state.has_any((item_names.VALKYRIE_FLECHETTE_MISSILES, item_names.VALKYRIE_ENHANCED_CLUSTER_LAUNCHERS), self.player)
                )
                or (state.has(item_names.BANSHEE, self.player) and (self.advanced_tactics or state.has(item_names.BANSHEE_SHAPED_HULL, self.player)))
                or (
                    self.advanced_tactics
                    and (
                        (
                            state.has_all((item_names.MARINE, item_names.MARINE_PROGRESSIVE_STIMPACK), self.player)
                            and (self.terran_bio_heal(state) or state.count(item_names.MARINE_PROGRESSIVE_STIMPACK, self.player) >= 2)
                        )
                        or (state.has(item_names.DOMINION_TROOPER, self.player) and self.terran_bio_heal(state))
                        or state.has_all(
                            (item_names.PREDATOR, item_names.PREDATOR_RESOURCE_EFFICIENCY, item_names.PREDATOR_ADAPTIVE_DEFENSES), self.player
                        )
                        or state.has_all((item_names.CYCLONE, item_names.CYCLONE_TARGETING_OPTICS), self.player)
                    )
                )
            )
            and (  # The enemy has 3/3 BCs
                state.has_any(
                    (item_names.GOLIATH, item_names.VIKING, item_names.NOVA_C20A_CANISTER_RIFLE, item_names.NOVA_BLAZEFIRE_GUNBLADE), self.player
                )
                or state.has_all((item_names.THOR, item_names.THOR_PROGRESSIVE_HIGH_IMPACT_PAYLOAD), self.player)
                or state.has_all((item_names.GHOST, item_names.GHOST_LOCKDOWN), self.player)
                or state.has_all((item_names.BATTLECRUISER, item_names.BATTLECRUISER_ATX_LASER_BATTERY), self.player)
            )
            and self.terran_army_weapon_armor_upgrade_min_level(state) >= 3
        )

    def has_terran_units(self, target: int) -> Callable[["CollectionState"], bool]:
        def _has_terran_units(state: CollectionState) -> bool:
            return (
                state.count_from_list_unique(
                    item_groups.terran_units + item_groups.terran_buildings, self.player
                ) >= target
                and (
                    target < 5
                    or self.terran_any_anti_air(state)
                )
                and (
                    # Anything that can hit buildings
                    state.has_any((
                        # Infantry
                        item_names.MARINE,
                        item_names.FIREBAT,
                        item_names.MARAUDER,
                        item_names.REAPER,
                        item_names.HERC,
                        item_names.DOMINION_TROOPER,
                        item_names.GHOST,
                        item_names.SPECTRE,
                        # Vehicles
                        item_names.HELLION,
                        item_names.VULTURE,
                        item_names.SIEGE_TANK,
                        item_names.WARHOUND,
                        item_names.GOLIATH,
                        item_names.DIAMONDBACK,
                        item_names.THOR,
                        item_names.PREDATOR,
                        item_names.CYCLONE,
                        # Ships
                        item_names.WRAITH,
                        item_names.VIKING,
                        item_names.BANSHEE,
                        item_names.RAVEN,
                        item_names.BATTLECRUISER,
                        # RG
                        item_names.SON_OF_KORHAL,
                        item_names.AEGIS_GUARD,
                        item_names.EMPERORS_SHADOW,
                        item_names.BULWARK_COMPANY,
                        item_names.SHOCK_DIVISION,
                        item_names.BLACKHAMMER,
                        item_names.SKY_FURY,
                        item_names.NIGHT_WOLF,
                        item_names.NIGHT_HAWK,
                        item_names.PRIDE_OF_AUGUSTRGRAD,
                    ), self.player)
                    or state.has_all((item_names.LIBERATOR, item_names.LIBERATOR_RAID_ARTILLERY), self.player)
                    or state.has_all((item_names.EMPERORS_GUARDIAN, item_names.LIBERATOR_RAID_ARTILLERY), self.player)
                    or state.has_all((item_names.VALKYRIE, item_names.VALKYRIE_FLECHETTE_MISSILES), self.player)
                    or state.has_all((item_names.WIDOW_MINE, item_names.WIDOW_MINE_DEMOLITION_PAYLOAD), self.player)
                    or (
                        state.has_any((
                            # Mercs with shortest initial cooldown (300s)
                            item_names.WAR_PIGS,
                            item_names.DEATH_HEADS,
                            item_names.HELS_ANGELS,
                            item_names.WINGED_NIGHTMARES,
                        ), self.player)
                        # + 2 upgrades that allow getting faster/earlier mercs
                        and state.count_from_list((
                            item_names.RAPID_REINFORCEMENT,
                            item_names.PROGRESSIVE_FAST_DELIVERY,
                            item_names.ROGUE_FORCES,
                            # item_names.SIGNAL_BEACON,  # Probably doesn't help too much on the first unit
                        ), self.player) >= 2
                    )
                )
            )

        return _has_terran_units

    def has_zerg_units(self, target: int) -> Callable[["CollectionState"], bool]:
        def _has_zerg_units(state: CollectionState) -> bool:
            num_units = (
                state.count_from_list_unique(
                    item_groups.zerg_nonmorph_units + item_groups.zerg_buildings + [item_names.OVERLORD_OVERSEER_ASPECT],
                    self.player
                )
                + self.morph_baneling(state)
                + self.morph_ravager(state)
                + self.morph_igniter(state)
                + self.morph_lurker(state)
                + self.morph_impaler(state)
                + self.morph_viper(state)
                + self.morph_devourer(state)
                + self.morph_brood_lord(state)
                + self.morph_guardian(state)
                + self.morph_tyrannozor(state)
            )
            return (
                num_units >= target
                and (
                    target < 5
                    or self.zerg_any_anti_air(state)
                )
                and (
                    # Anything that can hit buildings
                    state.has_any((
                        item_names.ZERGLING,
                        item_names.SWARM_QUEEN,
                        item_names.ROACH,
                        item_names.HYDRALISK,
                        item_names.ABERRATION,
                        item_names.SWARM_HOST,
                        item_names.MUTALISK,
                        item_names.ULTRALISK,
                        item_names.PYGALISK,
                        item_names.INFESTED_MARINE,
                        item_names.INFESTED_BUNKER,
                        item_names.INFESTED_DIAMONDBACK,
                        item_names.INFESTED_SIEGE_TANK,
                        item_names.INFESTED_BANSHEE,
                    ), self.player)
                    or state.has_all((item_names.INFESTOR, item_names.INFESTOR_INFESTED_TERRAN), self.player)
                    or self.morph_baneling(state)
                    or self.morph_lurker(state)
                    or self.morph_impaler(state)
                    or self.morph_brood_lord(state)
                    or self.morph_guardian(state)
                    or self.morph_ravager(state)
                    or self.morph_igniter(state)
                    or self.morph_tyrannozor(state)
                    or (self.morph_devourer(state)
                        and state.has(item_names.DEVOURER_PRESCIENT_SPORES, self.player)
                    )
                    or (
                        state.has_any((
                            # Mercs with <= 300s first drop time
                            item_names.DEVOURING_ONES,
                            item_names.HUNTER_KILLERS,
                            item_names.CAUSTIC_HORRORS,
                            item_names.HUNTERLING,
                        ), self.player)
                        # + 2 upgrades that allow getting faster/earlier mercs
                        and state.count_from_list((
                            item_names.UNRESTRICTED_MUTATION,
                            item_names.EVOLUTIONARY_LEAP,
                            item_names.CELL_DIVISION,
                            item_names.SELF_SUFFICIENT,
                        ), self.player) >= 2
                    )
                )
            )

        return _has_zerg_units

    def has_protoss_units(self, target: int) -> Callable[["CollectionState"], bool]:
        def _has_protoss_units(state: CollectionState) -> bool:
            return (
                state.count_from_list_unique(item_groups.protoss_units + item_groups.protoss_buildings + [item_names.NEXUS_OVERCHARGE], self.player)
                >= target
            ) and (
                target < 5
                or self.protoss_any_anti_air_unit(state)
            ) and (
                # Anything that can hit buildings
                state.has_any((
                    # Gateway
                    item_names.ZEALOT,
                    item_names.CENTURION,
                    item_names.SENTINEL,
                    item_names.SUPPLICANT,
                    item_names.STALKER,
                    item_names.INSTIGATOR,
                    item_names.SLAYER,
                    item_names.DRAGOON,
                    item_names.ADEPT,
                    item_names.SENTRY,
                    item_names.ENERGIZER,
                    item_names.AVENGER,
                    item_names.DARK_TEMPLAR,
                    item_names.BLOOD_HUNTER,
                    item_names.HIGH_TEMPLAR,
                    item_names.SIGNIFIER,
                    item_names.ASCENDANT,
                    item_names.DARK_ARCHON,
                    # Robo
                    item_names.IMMORTAL,
                    item_names.ANNIHILATOR,
                    item_names.VANGUARD,
                    item_names.STALWART,
                    item_names.COLOSSUS,
                    item_names.WRATHWALKER,
                    item_names.REAVER,
                    item_names.DISRUPTOR,
                    # Stargate
                    item_names.SKIRMISHER,
                    item_names.SCOUT,
                    item_names.MISTWING,
                    item_names.OPPRESSOR,
                    item_names.PULSAR,
                    item_names.VOID_RAY,
                    item_names.DESTROYER,
                    item_names.DAWNBRINGER,
                    item_names.ARBITER,
                    item_names.ORACLE,
                    item_names.CARRIER,
                    item_names.TRIREME,
                    item_names.SKYLORD,
                    item_names.TEMPEST,
                    item_names.MOTHERSHIP,
                ), self.player)
                or state.has_all((item_names.WARP_PRISM, item_names.WARP_PRISM_PHASE_BLASTER), self.player)
                or state.has_all((item_names.CALADRIUS, item_names.CALADRIUS_CORONA_BEAM), self.player)
                or state.has_all((item_names.PHOTON_CANNON, item_names.KHALAI_INGENUITY), self.player)
                or state.has_all((item_names.KHAYDARIN_MONOLITH, item_names.KHALAI_INGENUITY), self.player)
            )

        return _has_protoss_units

    def has_race_units(self, target: int, race: SC2Race) -> Callable[["CollectionState"], bool]:
        if target == 0 or race == SC2Race.ANY:
            return Location.access_rule
        result = self.unit_count_functions.get((race, target))
        if result is not None:
            return result
        if race == SC2Race.TERRAN:
            result = self.has_terran_units(target)
        if race == SC2Race.ZERG:
            result = self.has_zerg_units(target)
        if race == SC2Race.PROTOSS:
            result = self.has_protoss_units(target)
        assert result
        self.unit_count_functions[(race, target)] = result
        return result


def get_basic_units(logic_level: int, race: SC2Race) -> Set[str]:
    if logic_level > RequiredTactics.option_advanced:
        return no_logic_basic_units[race]
    elif logic_level == RequiredTactics.option_advanced:
        return advanced_basic_units[race]
    else:
        return basic_units[race]


# Defense rating table
# Commented defense ratings are handled in the defense_rating function
tvx_defense_ratings = {
    item_names.SIEGE_TANK: 5,
    # "Graduating Range": 1,
    item_names.PLANETARY_FORTRESS: 3,
    # Bunker w/ Marine/Marauder: 3,
    item_names.PERDITION_TURRET: 2,
    item_names.DEVASTATOR_TURRET: 2,
    item_names.VULTURE: 1,
    item_names.BANSHEE: 1,
    item_names.BATTLECRUISER: 1,
    item_names.LIBERATOR: 4,
    item_names.WIDOW_MINE: 1,
    # "Concealment (Widow Mine)": 1
}
tvz_defense_ratings = {
    item_names.PERDITION_TURRET: 2,
    # Bunker w/ Firebat: 2,
    item_names.LIBERATOR: -2,
    item_names.HIVE_MIND_EMULATOR: 3,
    item_names.PSI_DISRUPTER: 3,
}
tvx_air_defense_ratings = {
    item_names.MISSILE_TURRET: 2,
}
zvx_defense_ratings = {
    # Note that this doesn't include Kerrigan because this is just for race swaps, which doesn't involve her (for now)
    item_names.SPINE_CRAWLER: 3,
    # w/ Twin Drones: 1
    item_names.SWARM_QUEEN: 1,
    item_names.SWARM_HOST: 1,
    # impaler: 3
    #  "Hardened Tentacle Spines (Impaler)": 2
    # lurker: 1
    #  "Seismic Spines (Lurker)": 2
    #  "Adapted Spines (Lurker)": 1
    # brood lord : 2
    # corpser roach: 1
    # creep tumors (swarm queen or overseer): 1
    # w/ malignant creep: 1
    # tanks with ammo: 5
    item_names.INFESTED_BUNKER: 3,
    item_names.BILE_LAUNCHER: 2,
}
# zvz_defense_ratings = {
    # corpser roach: 1
    # primal igniter: 2
    # lurker: 1
    # w/ adapted spines: -1
    # impaler: -1
# }
zvx_air_defense_ratings = {
    item_names.SPORE_CRAWLER: 2,
    # w/ Twin Drones: 1
    item_names.INFESTED_MISSILE_TURRET: 2,
}
pvx_defense_ratings = {
    item_names.PHOTON_CANNON: 2,
    item_names.KHAYDARIN_MONOLITH: 3,
    item_names.SHIELD_BATTERY: 1,
    item_names.NEXUS_OVERCHARGE: 2,
    item_names.SKYLORD: 1,
    item_names.MATRIX_OVERLOAD: 1,
    item_names.COLOSSUS: 1,
    item_names.VANGUARD: 1,
    item_names.REAVER: 1,
}
pvz_defense_ratings = {
    item_names.KHAYDARIN_MONOLITH: -2,
    item_names.COLOSSUS: 1,
}

terran_passive_ratings = {
    item_names.AUTOMATED_REFINERY: 4,
    item_names.COMMAND_CENTER_MULE: 4,
    item_names.ORBITAL_DEPOTS: 2,
    item_names.COMMAND_CENTER_COMMAND_CENTER_REACTOR: 2,
    item_names.COMMAND_CENTER_EXTRA_SUPPLIES: 2,
    item_names.MICRO_FILTERING: 2,
    item_names.TECH_REACTOR: 2
}

zerg_passive_ratings = {
    item_names.TWIN_DRONES: 7,
    item_names.AUTOMATED_EXTRACTORS: 4,
    item_names.VESPENE_EFFICIENCY: 3,
    item_names.OVERLORD_IMPROVED_OVERLORDS: 4,
    item_names.MALIGNANT_CREEP: 2
}

protoss_passive_ratings = {
    item_names.QUATRO: 4,
    item_names.ORBITAL_ASSIMILATORS: 4,
    item_names.AMPLIFIED_ASSIMILATORS: 3,
    item_names.PROBE_WARPIN: 2,
    item_names.ELDER_PROBES: 2,
    item_names.MATRIX_OVERLOAD: 2
}

soa_energy_ratings = {
    item_names.SOA_SOLAR_LANCE: 8,
    item_names.SOA_DEPLOY_FENIX: 7,
    item_names.SOA_TEMPORAL_FIELD: 6,
    item_names.SOA_PROGRESSIVE_PROXY_PYLON: 5,  # Requires Lvl 2 (Warp in Reinforcements)
    item_names.SOA_SHIELD_OVERCHARGE: 5,
    item_names.SOA_ORBITAL_STRIKE: 4
}

soa_passive_ratings = {
    item_names.GUARDIAN_SHELL: 4,
    item_names.OVERWATCH: 2
}

soa_ultimate_ratings = {
    item_names.SOA_TIME_STOP: 4,
    item_names.SOA_PURIFIER_BEAM: 3,
    item_names.SOA_SOLAR_BOMBARDMENT: 3
}
