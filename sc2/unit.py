# pylint: disable=W0212
from __future__ import annotations

import math
import warnings
from dataclasses import dataclass
from functools import cached_property
from typing import TYPE_CHECKING, Any, FrozenSet, List, Optional, Set, Tuple, Union

from sc2.cache import CacheDict
from sc2.constants import (
    CAN_BE_ATTACKED,
    DAMAGE_BONUS_PER_UPGRADE,
    IS_ARMORED,
    IS_ATTACKING,
    IS_BIOLOGICAL,
    IS_CARRYING_MINERALS,
    IS_CARRYING_RESOURCES,
    IS_CARRYING_VESPENE,
    IS_CLOAKED,
    IS_COLLECTING,
    IS_CONSTRUCTING_SCV,
    IS_DETECTOR,
    IS_ENEMY,
    IS_GATHERING,
    IS_LIGHT,
    IS_MASSIVE,
    IS_MECHANICAL,
    IS_MINE,
    IS_PATROLLING,
    IS_PLACEHOLDER,
    IS_PSIONIC,
    IS_REPAIRING,
    IS_RETURNING,
    IS_REVEALED,
    IS_SNAPSHOT,
    IS_STRUCTURE,
    IS_VISIBLE,
    OFF_CREEP_SPEED_INCREASE_DICT,
    OFF_CREEP_SPEED_UPGRADE_DICT,
    SPEED_ALTERING_BUFFS,
    SPEED_INCREASE_DICT,
    SPEED_INCREASE_ON_CREEP_DICT,
    SPEED_UPGRADE_DICT,
    TARGET_AIR,
    TARGET_BOTH,
    TARGET_GROUND,
    TARGET_HELPER,
    UNIT_BATTLECRUISER,
    UNIT_COLOSSUS,
    UNIT_ORACLE,
    UNIT_PHOTONCANNON,
    transforming,
)
from sc2.data import Alliance, Attribute, CloakState, Race, Target, race_gas, warpgate_abilities
from sc2.ids.ability_id import AbilityId
from sc2.ids.buff_id import BuffId
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.upgrade_id import UpgradeId
from sc2.position import Point2, Point3
from sc2.unit_command import UnitCommand

if TYPE_CHECKING:
    from sc2.bot_ai import BotAI
    from sc2.game_data import AbilityData, UnitTypeData


@dataclass
class RallyTarget:
    point: Point2
    tag: Optional[int] = None

    @classmethod
    def from_proto(cls, proto: Any) -> RallyTarget:
        return cls(
            Point2.from_proto(proto.point),
            proto.tag if proto.HasField("tag") else None,
        )


@dataclass
class UnitOrder:
    ability: AbilityData  # TODO: Should this be AbilityId instead?
    target: Optional[Union[int, Point2]] = None
    progress: float = 0

    @classmethod
    def from_proto(cls, proto: Any, bot_object: BotAI) -> UnitOrder:
        target: Optional[Union[int, Point2]] = proto.target_unit_tag
        if proto.HasField("target_world_space_pos"):
            target = Point2.from_proto(proto.target_world_space_pos)
        elif proto.HasField("target_unit_tag"):
            target = proto.target_unit_tag
        return cls(
            ability=bot_object.game_data.abilities[proto.ability_id],
            target=target,
            progress=proto.progress,
        )

    def __repr__(self) -> str:
        return f"UnitOrder({self.ability}, {self.target}, {self.progress})"


# pylint: disable=R0904
class Unit:
    class_cache = CacheDict()

    def __init__(
        self,
        proto_data,
        bot_object: BotAI,
        distance_calculation_index: int = -1,
        base_build: int = -1,
    ):
        """
        :param proto_data:
        :param bot_object:
        :param distance_calculation_index:
        :param base_build:
        """
        self._proto = proto_data
        self._bot_object: BotAI = bot_object
        self.game_loop: int = bot_object.state.game_loop
        self.base_build = base_build
        # Index used in the 2D numpy array to access the 2D distance between two units
        self.distance_calculation_index: int = distance_calculation_index

    def __repr__(self) -> str:
        """ Returns string of this form: Unit(name='SCV', tag=4396941328). """
        return f"Unit(name={self.name !r}, tag={self.tag})"

    @property
    def type_id(self) -> UnitTypeId:
        """ UnitTypeId found in sc2/ids/unit_typeid. """
        unit_type: int = self._proto.unit_type
        return self.class_cache.retrieve_and_set(unit_type, lambda: UnitTypeId(unit_type))

    @cached_property
    def _type_data(self) -> UnitTypeData:
        """ Provides the unit type data. """
        return self._bot_object.game_data.units[self._proto.unit_type]

    @cached_property
    def _creation_ability(self) -> AbilityData:
        """ Provides the AbilityData of the creation ability of this unit. """
        return self._type_data.creation_ability

    @property
    def name(self) -> str:
        """ Returns the name of the unit. """
        return self._type_data.name

    @cached_property
    def race(self) -> Race:
        """ Returns the race of the unit """
        return Race(self._type_data._proto.race)

    @property
    def tag(self) -> int:
        """ Returns the unique tag of the unit. """
        return self._proto.tag

    @property
    def is_structure(self) -> bool:
        """ Checks if the unit is a structure. """
        return IS_STRUCTURE in self._type_data.attributes

    @property
    def is_light(self) -> bool:
        """ Checks if the unit has the 'light' attribute. """
        return IS_LIGHT in self._type_data.attributes

    @property
    def is_armored(self) -> bool:
        """ Checks if the unit has the 'armored' attribute. """
        return IS_ARMORED in self._type_data.attributes

    @property
    def is_biological(self) -> bool:
        """ Checks if the unit has the 'biological' attribute. """
        return IS_BIOLOGICAL in self._type_data.attributes

    @property
    def is_mechanical(self) -> bool:
        """ Checks if the unit has the 'mechanical' attribute. """
        return IS_MECHANICAL in self._type_data.attributes

    @property
    def is_massive(self) -> bool:
        """ Checks if the unit has the 'massive' attribute. """
        return IS_MASSIVE in self._type_data.attributes

    @property
    def is_psionic(self) -> bool:
        """ Checks if the unit has the 'psionic' attribute. """
        return IS_PSIONIC in self._type_data.attributes

    @cached_property
    def tech_alias(self) -> Optional[List[UnitTypeId]]:
        """Building tech equality, e.g. OrbitalCommand is the same as CommandCenter
        For Hive, this returns [UnitTypeId.Hatchery, UnitTypeId.Lair]
        For SCV, this returns None"""
        return self._type_data.tech_alias

    @cached_property
    def unit_alias(self) -> Optional[UnitTypeId]:
        """Building type equality, e.g. FlyingOrbitalCommand is the same as OrbitalCommand
        For flying OrbitalCommand, this returns UnitTypeId.OrbitalCommand
        For SCV, this returns None"""
        return self._type_data.unit_alias

    @cached_property
    def _weapons(self):
        """ Returns the weapons of the unit. """
        return self._type_data._proto.weapons

    @cached_property
    def can_attack(self) -> bool:
        """ Checks if the unit can attack at all. """
        # TODO BATTLECRUISER doesnt have weapons in proto?!
        return bool(self._weapons) or self.type_id in {UNIT_BATTLECRUISER, UNIT_ORACLE}

    @property
    def can_attack_both(self) -> bool:
        """ Checks if the unit can attack both ground and air units. """
        return self.can_attack_ground and self.can_attack_air

    @cached_property
    def can_attack_ground(self) -> bool:
        """ Checks if the unit can attack ground units. """
        if self.type_id in {UNIT_BATTLECRUISER, UNIT_ORACLE}:
            return True
        if self._weapons:
            return any(weapon.type in TARGET_GROUND for weapon in self._weapons)
        return False

    @cached_property
    def ground_dps(self) -> float:
        """ Returns the dps against ground units. Does not include upgrades. """
        if self.can_attack_ground:
            weapon = next((weapon for weapon in self._weapons if weapon.type in TARGET_GROUND), None)
            if weapon:
                return (weapon.damage * weapon.attacks) / weapon.speed
        return 0

    @cached_property
    def ground_range(self) -> float:
        """ Returns the range against ground units. Does not include upgrades. """
        if self.type_id == UNIT_ORACLE:
            return 4
        if self.type_id == UNIT_BATTLECRUISER:
            return 6
        if self.can_attack_ground:
            weapon = next((weapon for weapon in self._weapons if weapon.type in TARGET_GROUND), None)
            if weapon:
                return weapon.range
        return 0

    @cached_property
    def can_attack_air(self) -> bool:
        """ Checks if the unit can air attack at all. Does not include upgrades. """
        if self.type_id == UNIT_BATTLECRUISER:
            return True
        if self._weapons:
            return any(weapon.type in TARGET_AIR for weapon in self._weapons)
        return False

    @cached_property
    def air_dps(self) -> float:
        """ Returns the dps against air units. Does not include upgrades. """
        if self.can_attack_air:
            weapon = next((weapon for weapon in self._weapons if weapon.type in TARGET_AIR), None)
            if weapon:
                return (weapon.damage * weapon.attacks) / weapon.speed
        return 0

    @cached_property
    def air_range(self) -> float:
        """ Returns the range against air units. Does not include upgrades. """
        if self.type_id == UNIT_BATTLECRUISER:
            return 6
        if self.can_attack_air:
            weapon = next((weapon for weapon in self._weapons if weapon.type in TARGET_AIR), None)
            if weapon:
                return weapon.range
        return 0

    @cached_property
    def bonus_damage(self) -> Optional[Tuple[int, str]]:
        """Returns a tuple of form '(bonus damage, armor type)' if unit does 'bonus damage' against 'armor type'.
        Possible armor typs are: 'Light', 'Armored', 'Biological', 'Mechanical', 'Psionic', 'Massive', 'Structure'."""
        # TODO: Consider units with ability attacks (Oracle, Baneling) or multiple attacks (Thor).
        if self._weapons:
            for weapon in self._weapons:
                if weapon.damage_bonus:
                    b = weapon.damage_bonus[0]
                    return b.bonus, Attribute(b.attribute).name
        return None

    @property
    def armor(self) -> float:
        """ Returns the armor of the unit. Does not include upgrades """
        return self._type_data._proto.armor

    @property
    def sight_range(self) -> float:
        """ Returns the sight range of the unit. """
        return self._type_data._proto.sight_range

    @property
    def movement_speed(self) -> float:
        """Returns the movement speed of the unit.
        This is the unit movement speed on game speed 'normal'. To convert it to 'faster' movement speed, multiply it by a factor of '1.4'. E.g. reaper movement speed is listed here as 3.75, but should actually be 5.25.
        Does not include upgrades or buffs."""
        return self._type_data._proto.movement_speed

    @cached_property
    def real_speed(self) -> float:
        """ See 'calculate_speed'. """
        return self.calculate_speed()

    def calculate_speed(self, upgrades: Set[UpgradeId] = None) -> float:
        """Calculates the movement speed of the unit including buffs and upgrades.
        Note: Upgrades only work with own units. Use "upgrades" param to set expected enemy upgrades.

        :param upgrades:
        """
        speed: float = self.movement_speed
        unit_type: UnitTypeId = self.type_id

        # ---- Upgrades ----
        if upgrades is None and self.is_mine:
            upgrades = self._bot_object.state.upgrades

        if upgrades and unit_type in SPEED_UPGRADE_DICT:
            upgrade_id: Optional[UpgradeId] = SPEED_UPGRADE_DICT.get(unit_type, None)
            if upgrade_id and upgrade_id in upgrades:
                speed *= SPEED_INCREASE_DICT.get(unit_type, 1)

        # ---- Creep ----
        if unit_type in SPEED_INCREASE_ON_CREEP_DICT or unit_type in OFF_CREEP_SPEED_UPGRADE_DICT:
            # On creep
            x, y = self.position_tuple
            if self._bot_object.state.creep[(int(x), int(y))]:
                speed *= SPEED_INCREASE_ON_CREEP_DICT.get(unit_type, 1)

            # Off creep upgrades
            elif upgrades:
                upgrade_id2: Optional[UpgradeId] = OFF_CREEP_SPEED_UPGRADE_DICT.get(unit_type, None)
                if upgrade_id2:
                    speed *= OFF_CREEP_SPEED_INCREASE_DICT[unit_type]

            # Ultralisk has passive ability "Frenzied" which makes it immune to speed altering buffs
            if unit_type == UnitTypeId.ULTRALISK:
                return speed

        # ---- Buffs ----
        # Hard reset movement speed: medivac boost, void ray charge
        if self.buffs and unit_type in {UnitTypeId.MEDIVAC, UnitTypeId.VOIDRAY}:
            if BuffId.MEDIVACSPEEDBOOST in self.buffs:
                speed = self.movement_speed * 1.7
            elif BuffId.VOIDRAYSWARMDAMAGEBOOST in self.buffs:
                speed = self.movement_speed * 0.75

        # Speed altering buffs, e.g. stimpack, zealot charge, concussive shell, time warp, fungal growth, inhibitor zone
        for buff in self.buffs:
            speed *= SPEED_ALTERING_BUFFS.get(buff, 1)
        return speed

    @property
    def distance_per_step(self) -> float:
        """The distance a unit can move in one step. This does not take acceleration into account.
        Useful for micro-retreat/pathfinding"""
        return (self.real_speed / 22.4) * self._bot_object.client.game_step

    @property
    def distance_to_weapon_ready(self) -> float:
        """ Distance a unit can travel before it's weapon is ready to be fired again."""
        return (self.real_speed / 22.4) * self.weapon_cooldown

    @property
    def is_mineral_field(self) -> bool:
        """ Checks if the unit is a mineral field. """
        return self._type_data.has_minerals

    @property
    def is_vespene_geyser(self) -> bool:
        """ Checks if the unit is a non-empty vespene geyser or gas extraction building. """
        return self._type_data.has_vespene

    @property
    def health(self) -> float:
        """ Returns the health of the unit. Does not include shields. """
        return self._proto.health

    @property
    def health_max(self) -> float:
        """ Returns the maximum health of the unit. Does not include shields. """
        return self._proto.health_max

    @cached_property
    def health_percentage(self) -> float:
        """ Returns the percentage of health the unit has. Does not include shields. """
        if not self._proto.health_max:
            return 0
        return self._proto.health / self._proto.health_max

    @property
    def shield(self) -> float:
        """ Returns the shield points the unit has. Returns 0 for non-protoss units. """
        return self._proto.shield

    @property
    def shield_max(self) -> float:
        """ Returns the maximum shield points the unit can have. Returns 0 for non-protoss units. """
        return self._proto.shield_max

    @cached_property
    def shield_percentage(self) -> float:
        """ Returns the percentage of shield points the unit has. Returns 0 for non-protoss units. """
        if not self._proto.shield_max:
            return 0
        return self._proto.shield / self._proto.shield_max

    @cached_property
    def shield_health_percentage(self) -> float:
        """Returns the percentage of combined shield + hp points the unit has.
        Also takes build progress into account."""
        max_ = (self._proto.shield_max + self._proto.health_max) * self.build_progress
        if max_ == 0:
            return 0
        return (self._proto.shield + self._proto.health) / max_

    @property
    def energy(self) -> float:
        """ Returns the amount of energy the unit has. Returns 0 for units without energy. """
        return self._proto.energy

    @property
    def energy_max(self) -> float:
        """ Returns the maximum amount of energy the unit can have. Returns 0 for units without energy. """
        return self._proto.energy_max

    @cached_property
    def energy_percentage(self) -> float:
        """ Returns the percentage of amount of energy the unit has. Returns 0 for units without energy. """
        if not self._proto.energy_max:
            return 0
        return self._proto.energy / self._proto.energy_max

    @property
    def age_in_frames(self) -> int:
        """ Returns how old the unit object data is (in game frames). This age does not reflect the unit was created / trained / morphed! """
        return self._bot_object.state.game_loop - self.game_loop

    @property
    def age(self) -> float:
        """ Returns how old the unit object data is (in game seconds). This age does not reflect when the unit was created / trained / morphed! """
        return (self._bot_object.state.game_loop - self.game_loop) / 22.4

    @property
    def is_memory(self) -> bool:
        """ Returns True if this Unit object is referenced from the future and is outdated. """
        return self.game_loop != self._bot_object.state.game_loop

    @cached_property
    def is_snapshot(self) -> bool:
        """Checks if the unit is only available as a snapshot for the bot.
        Enemy buildings that have been scouted and are in the fog of war or
        attacking enemy units on higher, not visible ground appear this way."""
        if self.base_build >= 82457:
            return self._proto.display_type == IS_SNAPSHOT
        # TODO: Fixed in version 5.0.4, remove if a new linux binary is released: https://github.com/Blizzard/s2client-proto/issues/167
        position = self.position.rounded
        return self._bot_object.state.visibility.data_numpy[position[1], position[0]] != 2

    @cached_property
    def is_visible(self) -> bool:
        """Checks if the unit is visible for the bot.
        NOTE: This means the bot has vision of the position of the unit!
        It does not give any information about the cloak status of the unit."""
        if self.base_build >= 82457:
            return self._proto.display_type == IS_VISIBLE
        # TODO: Remove when a new linux binary (5.0.4 or newer) is released
        return self._proto.display_type == IS_VISIBLE and not self.is_snapshot

    @property
    def is_placeholder(self) -> bool:
        """Checks if the unit is a placerholder for the bot.
        Raw information about placeholders:
            display_type: Placeholder
            alliance: Self
            unit_type: 86
            owner: 1
            pos {
              x: 29.5
              y: 53.5
              z: 7.98828125
            }
            radius: 2.75
            is_on_screen: false
        """
        return self._proto.display_type == IS_PLACEHOLDER

    @property
    def alliance(self) -> Alliance:
        """ Returns the team the unit belongs to. """
        return self._proto.alliance

    @property
    def is_mine(self) -> bool:
        """ Checks if the unit is controlled by the bot. """
        return self._proto.alliance == IS_MINE

    @property
    def is_enemy(self) -> bool:
        """ Checks if the unit is hostile. """
        return self._proto.alliance == IS_ENEMY

    @property
    def owner_id(self) -> int:
        """ Returns the owner of the unit. This is a value of 1 or 2 in a two player game. """
        return self._proto.owner

    @property
    def position_tuple(self) -> Tuple[float, float]:
        """ Returns the 2d position of the unit as tuple without conversion to Point2. """
        return self._proto.pos.x, self._proto.pos.y

    @cached_property
    def position(self) -> Point2:
        """ Returns the 2d position of the unit. """
        return Point2.from_proto(self._proto.pos)

    @cached_property
    def position3d(self) -> Point3:
        """ Returns the 3d position of the unit. """
        return Point3.from_proto(self._proto.pos)

    def distance_to(self, p: Union[Unit, Point2]) -> float:
        """Using the 2d distance between self and p.
        To calculate the 3d distance, use unit.position3d.distance_to(p)

        :param p:
        """
        if isinstance(p, Unit):
            return self._bot_object._distance_squared_unit_to_unit(self, p)**0.5
        return self._bot_object.distance_math_hypot(self.position_tuple, p)

    def distance_to_squared(self, p: Union[Unit, Point2]) -> float:
        """Using the 2d distance squared between self and p. Slightly faster than distance_to, so when filtering a lot of units, this function is recommended to be used.
        To calculate the 3d distance, use unit.position3d.distance_to(p)

        :param p:
        """
        if isinstance(p, Unit):
            return self._bot_object._distance_squared_unit_to_unit(self, p)
        return self._bot_object.distance_math_hypot_squared(self.position_tuple, p)

    def target_in_range(self, target: Unit, bonus_distance: float = 0) -> bool:
        """Checks if the target is in range.
        Includes the target's radius when calculating distance to target.

        :param target:
        :param bonus_distance:
        """
        # TODO: Fix this because immovable units (sieged tank, planetary fortress etc.) have a little lower range than this formula
        if self.can_attack_ground and not target.is_flying:
            unit_attack_range = self.ground_range
        elif self.can_attack_air and (target.is_flying or target.type_id == UNIT_COLOSSUS):
            unit_attack_range = self.air_range
        else:
            return False
        return (
            self._bot_object._distance_squared_unit_to_unit(self, target) <=
            (self.radius + target.radius + unit_attack_range + bonus_distance)**2
        )

    def in_ability_cast_range(
        self, ability_id: AbilityId, target: Union[Unit, Point2], bonus_distance: float = 0
    ) -> bool:
        """Test if a unit is able to cast an ability on the target without checking ability cooldown (like stalker blink) or if ability is made available through research (like HT storm).

        :param ability_id:
        :param target:
        :param bonus_distance:
        """
        cast_range = self._bot_object.game_data.abilities[ability_id.value]._proto.cast_range
        assert cast_range > 0, f"Checking for an ability ({ability_id}) that has no cast range"
        ability_target_type = self._bot_object.game_data.abilities[ability_id.value]._proto.target
        # For casting abilities that target other units, like transfuse, feedback, snipe, yamato
        if (
            ability_target_type in {Target.Unit.value, Target.PointOrUnit.value}  # type: ignore
            and isinstance(target, Unit)
        ):
            return (
                self._bot_object._distance_squared_unit_to_unit(self, target) <=
                (cast_range + self.radius + target.radius + bonus_distance)**2
            )
        # For casting abilities on the ground, like queen creep tumor, ravager bile, HT storm
        if (
            ability_target_type in {Target.Point.value, Target.PointOrUnit.value}  # type: ignore
            and isinstance(target, (Point2, tuple))
        ):
            return (
                self._bot_object._distance_pos_to_pos(self.position_tuple, target) <=
                cast_range + self.radius + bonus_distance
            )
        return False

    # pylint: disable=R0912,R0911
    def calculate_damage_vs_target(
        self,
        target: Unit,
        ignore_armor: bool = False,
        include_overkill_damage: bool = True,
    ) -> Tuple[float, float, float]:
        """Returns a tuple of: [potential damage against target, attack speed, attack range]
        Returns the properly calculated damage per full-attack against the target unit.
        Returns (0, 0, 0) if this unit can't attack the target unit.

        If 'include_overkill_damage=True' and the unit deals 10 damage, the target unit has 5 hp and 0 armor,
        the target unit would result in -5hp, so the returning damage would be 10.
        For 'include_overkill_damage=False' this function would return 5.

        If 'ignore_armor=False' and the unit deals 10 damage, the target unit has 20 hp and 5 armor,
        the target unit would result in 15hp, so the returning damage would be 5.
        For 'ignore_armor=True' this function would return 10.

        :param target:
        :param ignore_armor:
        :param include_overkill_damage:
        """
        if self.type_id not in {UnitTypeId.BATTLECRUISER, UnitTypeId.BUNKER}:
            if not self.can_attack:
                return 0, 0, 0
            if target.type_id != UnitTypeId.COLOSSUS:
                if not self.can_attack_ground and not target.is_flying:
                    return 0, 0, 0
                if not self.can_attack_air and target.is_flying:
                    return 0, 0, 0
        # Structures that are not completed can't attack
        if not self.is_ready:
            return 0, 0, 0
        target_has_guardian_shield: bool = False
        if ignore_armor:
            enemy_armor: float = 0
            enemy_shield_armor: float = 0
        else:
            # TODO: enemy is under influence of anti armor missile -> reduce armor and shield armor
            enemy_armor = target.armor + target.armor_upgrade_level
            enemy_shield_armor = target.shield_upgrade_level
            # Ultralisk armor upgrade, only works if target belongs to the bot calling this function
            if (
                target.type_id in {UnitTypeId.ULTRALISK, UnitTypeId.ULTRALISKBURROWED} and target.is_mine
                and UpgradeId.CHITINOUSPLATING in target._bot_object.state.upgrades
            ):
                enemy_armor += 2
            # Guardian shield adds 2 armor
            if BuffId.GUARDIANSHIELD in target.buffs:
                target_has_guardian_shield = True
            # Anti armor missile of raven
            if BuffId.RAVENSHREDDERMISSILETINT in target.buffs:
                enemy_armor -= 2
                enemy_shield_armor -= 2

        # Hard coded return for battlecruiser because they have no weapon in the API
        if self.type_id == UnitTypeId.BATTLECRUISER:
            if target_has_guardian_shield:
                enemy_armor += 2
                enemy_shield_armor += 2
            weapon_damage: float = (5 if target.is_flying else 8) + self.attack_upgrade_level
            weapon_damage = weapon_damage - enemy_shield_armor if target.shield else weapon_damage - enemy_armor
            return weapon_damage, 0.224, 6

        # Fast return for bunkers, since they don't have a weapon similar to BCs
        if self.type_id == UnitTypeId.BUNKER:
            if self.is_enemy:
                if self.is_active:
                    # Expect fully loaded bunker with marines
                    return (24, 0.854, 6)
                return (0, 0, 0)
            # TODO if bunker belongs to us, use passengers and upgrade level to calculate damage

        required_target_type: Set[int] = (
            TARGET_BOTH
            if target.type_id == UnitTypeId.COLOSSUS else TARGET_GROUND if not target.is_flying else TARGET_AIR
        )
        # Contains total damage, attack speed and attack range
        damages: List[Tuple[float, float, float]] = []
        for weapon in self._weapons:
            if weapon.type not in required_target_type:
                continue
            enemy_health: float = target.health
            enemy_shield: float = target.shield
            total_attacks: int = weapon.attacks
            weapon_speed: float = weapon.speed
            weapon_range: float = weapon.range
            bonus_damage_per_upgrade = (
                0 if not self.attack_upgrade_level else
                DAMAGE_BONUS_PER_UPGRADE.get(self.type_id, {}).get(weapon.type, {}).get(None, 1)
            )
            damage_per_attack: float = weapon.damage + self.attack_upgrade_level * bonus_damage_per_upgrade
            # Remaining damage after all damage is dealt to shield
            remaining_damage: float = 0

            # Calculate bonus damage against target
            boni: List[float] = []
            # TODO: hardcode hellbats when they have blueflame or attack upgrades
            for bonus in weapon.damage_bonus:
                # More about damage bonus https://github.com/Blizzard/s2client-proto/blob/b73eb59ac7f2c52b2ca585db4399f2d3202e102a/s2clientprotocol/data.proto#L55
                if bonus.attribute in target._type_data.attributes:
                    bonus_damage_per_upgrade = (
                        0 if not self.attack_upgrade_level else
                        DAMAGE_BONUS_PER_UPGRADE.get(self.type_id, {}).get(weapon.type, {}).get(bonus.attribute, 0)
                    )
                    # Hardcode blueflame damage bonus from hellions
                    if (
                        bonus.attribute == IS_LIGHT and self.type_id == UnitTypeId.HELLION
                        and UpgradeId.HIGHCAPACITYBARRELS in self._bot_object.state.upgrades
                    ):
                        bonus_damage_per_upgrade += 5
                    # TODO buffs e.g. void ray charge beam vs armored
                    boni.append(bonus.bonus + self.attack_upgrade_level * bonus_damage_per_upgrade)
            if boni:
                damage_per_attack += max(boni)

            # Subtract enemy unit's shield
            if target.shield > 0:
                # Fix for ranged units + guardian shield
                enemy_shield_armor_temp = (
                    enemy_shield_armor + 2 if target_has_guardian_shield and weapon_range >= 2 else enemy_shield_armor
                )
                # Shield-armor has to be applied
                while total_attacks > 0 and enemy_shield > 0:
                    # Guardian shield correction
                    enemy_shield -= max(0.5, damage_per_attack - enemy_shield_armor_temp)
                    total_attacks -= 1
                if enemy_shield < 0:
                    remaining_damage = -enemy_shield
                    enemy_shield = 0

            # TODO roach and hydra in melee range are not affected by guardian shield
            # Fix for ranged units if enemy has guardian shield buff
            enemy_armor_temp = enemy_armor + 2 if target_has_guardian_shield and weapon_range >= 2 else enemy_armor
            # Subtract enemy unit's HP
            if remaining_damage > 0:
                enemy_health -= max(0.5, remaining_damage - enemy_armor_temp)
            while total_attacks > 0 and (include_overkill_damage or enemy_health > 0):
                # Guardian shield correction
                enemy_health -= max(0.5, damage_per_attack - enemy_armor_temp)
                total_attacks -= 1

            # Calculate the final damage
            if not include_overkill_damage:
                enemy_health = max(0, enemy_health)
                enemy_shield = max(0, enemy_shield)
            total_damage_dealt = target.health + target.shield - enemy_health - enemy_shield
            # Unit modifiers: buffs and upgrades that affect weapon speed and weapon range
            if self.type_id in {
                UnitTypeId.ZERGLING,
                UnitTypeId.MARINE,
                UnitTypeId.MARAUDER,
                UnitTypeId.ADEPT,
                UnitTypeId.HYDRALISK,
                UnitTypeId.PHOENIX,
                UnitTypeId.PLANETARYFORTRESS,
                UnitTypeId.MISSILETURRET,
                UnitTypeId.AUTOTURRET,
            }:
                upgrades: Set[UpgradeId] = self._bot_object.state.upgrades
                if (
                    self.type_id == UnitTypeId.ZERGLING
                    # Attack speed calculation only works for our unit
                    and self.is_mine and UpgradeId.ZERGLINGATTACKSPEED in upgrades
                ):
                    # 0.696044921875 for zerglings divided through 1.4 equals (+40% attack speed bonus from the upgrade):
                    weapon_speed /= 1.4
                elif (
                    # Adept ereceive 45% attack speed bonus from glaives
                    self.type_id == UnitTypeId.ADEPT and self.is_mine and UpgradeId.ADEPTPIERCINGATTACK in upgrades
                ):
                    # TODO next patch: if self.type_id is adept: check if attack speed buff is active, instead of upgrade
                    weapon_speed /= 1.45
                elif self.type_id == UnitTypeId.MARINE and BuffId.STIMPACK in self.buffs:
                    # Marine and marauder receive 50% attack speed bonus from stim
                    weapon_speed /= 1.5
                elif self.type_id == UnitTypeId.MARAUDER and BuffId.STIMPACKMARAUDER in self.buffs:
                    weapon_speed /= 1.5
                elif (
                    # TODO always assume that the enemy has the range upgrade researched
                    self.type_id == UnitTypeId.HYDRALISK and self.is_mine and UpgradeId.EVOLVEGROOVEDSPINES in upgrades
                ):
                    weapon_range += 1
                elif self.type_id == UnitTypeId.PHOENIX and self.is_mine and UpgradeId.PHOENIXRANGEUPGRADE in upgrades:
                    weapon_range += 2
                elif (
                    self.type_id in {UnitTypeId.PLANETARYFORTRESS, UnitTypeId.MISSILETURRET, UnitTypeId.AUTOTURRET}
                    and self.is_mine and UpgradeId.HISECAUTOTRACKING in upgrades
                ):
                    weapon_range += 1

            # Append it to the list of damages, e.g. both thor and queen attacks work on colossus
            damages.append((total_damage_dealt, weapon_speed, weapon_range))

        # If no attack was found, return (0, 0, 0)
        if not damages:
            return 0, 0, 0
        # Returns: total potential damage, attack speed, attack range
        return max(damages, key=lambda damage_tuple: damage_tuple[0])

    def calculate_dps_vs_target(
        self,
        target: Unit,
        ignore_armor: bool = False,
        include_overkill_damage: bool = True,
    ) -> float:
        """Returns the DPS against the given target.

        :param target:
        :param ignore_armor:
        :param include_overkill_damage:
        """
        calc_tuple: Tuple[float, float,
                          float] = self.calculate_damage_vs_target(target, ignore_armor, include_overkill_damage)
        # TODO fix for real time? The result may have to be multiplied by 1.4 because of game_speed=normal
        if calc_tuple[1] == 0:
            return 0
        return calc_tuple[0] / calc_tuple[1]

    @property
    def facing(self) -> float:
        """Returns direction the unit is facing as a float in range [0,2π). 0 is in direction of x axis."""
        return self._proto.facing

    def is_facing(self, other_unit: Unit, angle_error: float = 0.05) -> bool:
        """Check if this unit is facing the target unit. If you make angle_error too small, there might be rounding errors. If you make angle_error too big, this function might return false positives.

        :param other_unit:
        :param angle_error:
        """
        # TODO perhaps return default True for units that cannot 'face' another unit? e.g. structures (planetary fortress, bunker, missile turret, photon cannon, spine, spore) or sieged tanks
        angle = math.atan2(
            other_unit.position_tuple[1] - self.position_tuple[1], other_unit.position_tuple[0] - self.position_tuple[0]
        )
        if angle < 0:
            angle += math.pi * 2
        angle_difference = math.fabs(angle - self.facing)
        return angle_difference < angle_error

    @property
    def footprint_radius(self) -> Optional[float]:
        """For structures only.
        For townhalls this returns 2.5
        For barracks, spawning pool, gateway, this returns 1.5
        For supply depot, this returns 1
        For sensor tower, creep tumor, this return 0.5

        NOTE: This can be None if a building doesn't have a creation ability.
        For rich vespene buildings, flying terran buildings, this returns None"""
        return self._type_data.footprint_radius

    @property
    def radius(self) -> float:
        """ Half of unit size. See https://liquipedia.net/starcraft2/Unit_Statistics_(Legacy_of_the_Void) """
        return self._proto.radius

    @property
    def build_progress(self) -> float:
        """ Returns completion in range [0,1]."""
        return self._proto.build_progress

    @property
    def is_ready(self) -> bool:
        """ Checks if the unit is completed. """
        return self.build_progress == 1

    @property
    def cloak(self) -> CloakState:
        """Returns cloak state.
        See https://github.com/Blizzard/s2client-api/blob/d9ba0a33d6ce9d233c2a4ee988360c188fbe9dbf/include/sc2api/sc2_unit.h#L95
        """
        return CloakState(self._proto.cloak)

    @property
    def is_cloaked(self) -> bool:
        """ Checks if the unit is cloaked. """
        return self._proto.cloak in IS_CLOAKED

    @property
    def is_revealed(self) -> bool:
        """ Checks if the unit is revealed. """
        return self._proto.cloak == IS_REVEALED

    @property
    def can_be_attacked(self) -> bool:
        """ Checks if the unit is revealed or not cloaked and therefore can be attacked. """
        return self._proto.cloak in CAN_BE_ATTACKED

    @cached_property
    def buffs(self) -> FrozenSet[BuffId]:
        """ Returns the set of current buffs the unit has. """
        return frozenset(BuffId(buff_id) for buff_id in self._proto.buff_ids)

    @cached_property
    def is_carrying_minerals(self) -> bool:
        """ Checks if a worker or MULE is carrying (gold-)minerals. """
        return not IS_CARRYING_MINERALS.isdisjoint(self.buffs)

    @cached_property
    def is_carrying_vespene(self) -> bool:
        """ Checks if a worker is carrying vespene gas. """
        return not IS_CARRYING_VESPENE.isdisjoint(self.buffs)

    @cached_property
    def is_carrying_resource(self) -> bool:
        """ Checks if a worker is carrying a resource. """
        return not IS_CARRYING_RESOURCES.isdisjoint(self.buffs)

    @property
    def detect_range(self) -> float:
        """ Returns the detection distance of the unit. """
        return self._proto.detect_range

    @cached_property
    def is_detector(self) -> bool:
        """Checks if the unit is a detector. Has to be completed
        in order to detect and Photoncannons also need to be powered."""
        return self.is_ready and (self.type_id in IS_DETECTOR or self.type_id == UNIT_PHOTONCANNON and self.is_powered)

    @property
    def radar_range(self) -> float:
        return self._proto.radar_range

    @property
    def is_selected(self) -> bool:
        """ Checks if the unit is currently selected. """
        return self._proto.is_selected

    @property
    def is_on_screen(self) -> bool:
        """ Checks if the unit is on the screen. """
        return self._proto.is_on_screen

    @property
    def is_blip(self) -> bool:
        """ Checks if the unit is detected by a sensor tower. """
        return self._proto.is_blip

    @property
    def is_powered(self) -> bool:
        """ Checks if the unit is powered by a pylon or warppism. """
        return self._proto.is_powered

    @property
    def is_active(self) -> bool:
        """ Checks if the unit has an order (e.g. unit is currently moving or attacking, structure is currently training or researching). """
        return self._proto.is_active

    # PROPERTIES BELOW THIS COMMENT ARE NOT POPULATED FOR SNAPSHOTS

    @property
    def mineral_contents(self) -> int:
        """ Returns the amount of minerals remaining in a mineral field. """
        return self._proto.mineral_contents

    @property
    def vespene_contents(self) -> int:
        """ Returns the amount of gas remaining in a geyser. """
        return self._proto.vespene_contents

    @property
    def has_vespene(self) -> bool:
        """Checks if a geyser has any gas remaining.
        You can't build extractors on empty geysers."""
        return bool(self._proto.vespene_contents)

    @property
    def is_flying(self) -> bool:
        """ Checks if the unit is flying. """
        return self._proto.is_flying or self.has_buff(BuffId.GRAVITONBEAM)

    @property
    def is_burrowed(self) -> bool:
        """ Checks if the unit is burrowed. """
        return self._proto.is_burrowed

    @property
    def is_hallucination(self) -> bool:
        """ Returns True if the unit is your own hallucination or detected. """
        return self._proto.is_hallucination

    @property
    def attack_upgrade_level(self) -> int:
        """Returns the upgrade level of the units attack.
        # NOTE: Returns 0 for units without a weapon."""
        return self._proto.attack_upgrade_level

    @property
    def armor_upgrade_level(self) -> int:
        """ Returns the upgrade level of the units armor. """
        return self._proto.armor_upgrade_level

    @property
    def shield_upgrade_level(self) -> int:
        """Returns the upgrade level of the units shield.
        # NOTE: Returns 0 for units without a shield."""
        return self._proto.shield_upgrade_level

    @property
    def buff_duration_remain(self) -> int:
        """Returns the amount of remaining frames of the visible timer bar.
        # NOTE: Returns 0 for units without a timer bar."""
        return self._proto.buff_duration_remain

    @property
    def buff_duration_max(self) -> int:
        """Returns the maximum amount of frames of the visible timer bar.
        # NOTE: Returns 0 for units without a timer bar."""
        return self._proto.buff_duration_max

    # PROPERTIES BELOW THIS COMMENT ARE NOT POPULATED FOR ENEMIES

    @cached_property
    def orders(self) -> List[UnitOrder]:
        """ Returns the a list of the current orders. """
        # TODO: add examples on how to use unit orders
        return [UnitOrder.from_proto(order, self._bot_object) for order in self._proto.orders]

    @cached_property
    def order_target(self) -> Optional[Union[int, Point2]]:
        """Returns the target tag (if it is a Unit) or Point2 (if it is a Position)
        from the first order, returns None if the unit is idle"""
        if self.orders:
            target = self.orders[0].target
            if isinstance(target, int):
                return target
            return Point2.from_proto(target)
        return None

    @property
    def is_idle(self) -> bool:
        """ Checks if unit is idle. """
        return not self._proto.orders

    def is_using_ability(self, abilities: Union[AbilityId, Set[AbilityId]]) -> bool:
        """Check if the unit is using one of the given abilities.
        Only works for own units."""
        if not self.orders:
            return False
        if isinstance(abilities, AbilityId):
            abilities = {abilities}
        return self.orders[0].ability.id in abilities

    @cached_property
    def is_moving(self) -> bool:
        """Checks if the unit is moving.
        Only works for own units."""
        return self.is_using_ability(AbilityId.MOVE)

    @cached_property
    def is_attacking(self) -> bool:
        """Checks if the unit is attacking.
        Only works for own units."""
        return self.is_using_ability(IS_ATTACKING)

    @cached_property
    def is_patrolling(self) -> bool:
        """Checks if a unit is patrolling.
        Only works for own units."""
        return self.is_using_ability(IS_PATROLLING)

    @cached_property
    def is_gathering(self) -> bool:
        """Checks if a unit is on its way to a mineral field or vespene geyser to mine.
        Only works for own units."""
        return self.is_using_ability(IS_GATHERING)

    @cached_property
    def is_returning(self) -> bool:
        """Checks if a unit is returning from mineral field or vespene geyser to deliver resources to townhall.
        Only works for own units."""
        return self.is_using_ability(IS_RETURNING)

    @cached_property
    def is_collecting(self) -> bool:
        """Checks if a unit is gathering or returning.
        Only works for own units."""
        return self.is_using_ability(IS_COLLECTING)

    @cached_property
    def is_constructing_scv(self) -> bool:
        """Checks if the unit is an SCV that is currently building.
        Only works for own units."""
        return self.is_using_ability(IS_CONSTRUCTING_SCV)

    @cached_property
    def is_transforming(self) -> bool:
        """Checks if the unit transforming.
        Only works for own units."""
        return self.type_id in transforming and self.is_using_ability(transforming[self.type_id])

    @cached_property
    def is_repairing(self) -> bool:
        """Checks if the unit is an SCV or MULE that is currently repairing.
        Only works for own units."""
        return self.is_using_ability(IS_REPAIRING)

    @property
    def add_on_tag(self) -> int:
        """Returns the tag of the addon of unit. If the unit has no addon, returns 0."""
        return self._proto.add_on_tag

    @property
    def has_add_on(self) -> bool:
        """ Checks if unit has an addon attached. """
        return bool(self._proto.add_on_tag)

    @cached_property
    def has_techlab(self) -> bool:
        """Check if a structure is connected to a techlab addon. This should only ever return True for BARRACKS, FACTORY, STARPORT. """
        return self.add_on_tag in self._bot_object.techlab_tags

    @cached_property
    def has_reactor(self) -> bool:
        """Check if a structure is connected to a reactor addon. This should only ever return True for BARRACKS, FACTORY, STARPORT. """
        return self.add_on_tag in self._bot_object.reactor_tags

    @cached_property
    def add_on_land_position(self) -> Point2:
        """If this unit is an addon (techlab, reactor), returns the position
        where a terran building (BARRACKS, FACTORY, STARPORT) has to land to connect to this addon.

        Why offset (-2.5, 0.5)? See description in 'add_on_position'
        """
        return self.position.offset(Point2((-2.5, 0.5)))

    @cached_property
    def add_on_position(self) -> Point2:
        """If this unit is a terran production building (BARRACKS, FACTORY, STARPORT),
        this property returns the position of where the addon should be, if it should build one or has one attached.

        Why offset (2.5, -0.5)?
        A barracks is of size 3x3. The distance from the center to the edge is 1.5.
        An addon is 2x2 and the distance from the edge to center is 1.
        The total distance from center to center on the x-axis is 2.5.
        The distance from center to center on the y-axis is -0.5.
        """
        return self.position.offset(Point2((2.5, -0.5)))

    @cached_property
    def passengers(self) -> Set[Unit]:
        """ Returns the units inside a Bunker, CommandCenter, PlanetaryFortress, Medivac, Nydus, Overlord or WarpPrism. """
        return {Unit(unit, self._bot_object) for unit in self._proto.passengers}

    @cached_property
    def passengers_tags(self) -> Set[int]:
        """ Returns the tags of the units inside a Bunker, CommandCenter, PlanetaryFortress, Medivac, Nydus, Overlord or WarpPrism. """
        return {unit.tag for unit in self._proto.passengers}

    @property
    def cargo_used(self) -> int:
        """Returns how much cargo space is currently used in the unit.
        Note that some units take up more than one space."""
        return self._proto.cargo_space_taken

    @property
    def has_cargo(self) -> bool:
        """ Checks if this unit has any units loaded. """
        return bool(self._proto.cargo_space_taken)

    @property
    def cargo_size(self) -> int:
        """ Returns the amount of cargo space the unit needs. """
        return self._type_data.cargo_size

    @property
    def cargo_max(self) -> int:
        """ How much cargo space is available at maximum. """
        return self._proto.cargo_space_max

    @property
    def cargo_left(self) -> int:
        """ Returns how much cargo space is currently left in the unit. """
        return self._proto.cargo_space_max - self._proto.cargo_space_taken

    @property
    def assigned_harvesters(self) -> int:
        """ Returns the number of workers currently gathering resources at a geyser or mining base."""
        return self._proto.assigned_harvesters

    @property
    def ideal_harvesters(self) -> int:
        """Returns the ideal harverster count for unit.
        3 for gas buildings, 2*n for n mineral patches on that base."""
        return self._proto.ideal_harvesters

    @property
    def surplus_harvesters(self) -> int:
        """Returns a positive int if unit has too many harvesters mining,
        a negative int if it has too few mining.
        Will only works on townhalls, and gas buildings.
        """
        return self._proto.assigned_harvesters - self._proto.ideal_harvesters

    @property
    def weapon_cooldown(self) -> float:
        """Returns the time until the unit can fire again,
        returns -1 for units that can't attack.
        Usage:
        if unit.weapon_cooldown == 0:
            unit.attack(target)
        elif unit.weapon_cooldown < 0:
            unit.move(closest_allied_unit_because_cant_attack)
        else:
            unit.move(retreatPosition)"""
        if self.can_attack:
            return self._proto.weapon_cooldown
        return -1

    @property
    def weapon_ready(self) -> bool:
        """Checks if the weapon is ready to be fired."""
        return self.weapon_cooldown == 0

    @property
    def engaged_target_tag(self) -> int:
        # TODO What does this do?
        return self._proto.engaged_target_tag

    @cached_property
    def rally_targets(self) -> List[RallyTarget]:
        """ Returns the queue of rallytargets of the structure. """
        return [RallyTarget.from_proto(rally_target) for rally_target in self._proto.rally_targets]

    # Unit functions

    def has_buff(self, buff: BuffId) -> bool:
        """Checks if unit has buff 'buff'.

        :param buff:
        """
        assert isinstance(buff, BuffId), f"{buff} is no BuffId"
        return buff in self.buffs

    def train(
        self,
        unit: UnitTypeId,
        queue: bool = False,
        can_afford_check: bool = False,
    ) -> Union[UnitCommand, bool]:
        """Orders unit to train another 'unit'.
        Usage: COMMANDCENTER.train(SCV)

        :param unit:
        :param queue:
        :param can_afford_check:
        """
        return self(
            self._bot_object.game_data.units[unit.value].creation_ability.id,
            queue=queue,
            subtract_cost=True,
            can_afford_check=can_afford_check,
        )

    def build(
        self,
        unit: UnitTypeId,
        position: Point2 = None,
        queue: bool = False,
        can_afford_check: bool = False,
    ) -> Union[UnitCommand, bool]:
        """Orders unit to build another 'unit' at 'position'.
        Usage::

            SCV.build(COMMANDCENTER, position)
            # Target for refinery, assimilator and extractor needs to be the vespene geysir unit, not its position
            SCV.build(REFINERY, target_vespene_geysir)

        :param unit:
        :param position:
        :param queue:
        :param can_afford_check:
        """
        if unit in {UnitTypeId.EXTRACTOR, UnitTypeId.ASSIMILATOR, UnitTypeId.REFINERY}:
            assert isinstance(
                position, Unit
            ), "When building the gas structure, the target needs to be a unit (the vespene geysir) not the position of the vespene geysir."
        return self(
            self._bot_object.game_data.units[unit.value].creation_ability.id,
            target=position,
            queue=queue,
            subtract_cost=True,
            can_afford_check=can_afford_check,
        )

    def build_gas(
        self,
        target_geysir: Unit,
        queue: bool = False,
        can_afford_check: bool = False,
    ) -> Union[UnitCommand, bool]:
        """Orders unit to build another 'unit' at 'position'.
        Usage::

            # Target for refinery, assimilator and extractor needs to be the vespene geysir unit, not its position
            SCV.build_gas(target_vespene_geysir)

        :param target_geysir:
        :param queue:
        :param can_afford_check:
        """
        gas_structure_type_id: UnitTypeId = race_gas[self._bot_object.race]
        assert isinstance(
            target_geysir, Unit
        ), "When building the gas structure, the target needs to be a unit (the vespene geysir) not the position of the vespene geysir."
        return self(
            self._bot_object.game_data.units[gas_structure_type_id.value].creation_ability.id,
            target=target_geysir,
            queue=queue,
            subtract_cost=True,
            can_afford_check=can_afford_check,
        )

    def research(
        self,
        upgrade: UpgradeId,
        queue: bool = False,
        can_afford_check: bool = False,
    ) -> Union[UnitCommand, bool]:
        """Orders unit to research 'upgrade'.
        Requires UpgradeId to be passed instead of AbilityId.

        :param upgrade:
        :param queue:
        :param can_afford_check:
        """
        return self(
            self._bot_object.game_data.upgrades[upgrade.value].research_ability.exact_id,
            queue=queue,
            subtract_cost=True,
            can_afford_check=can_afford_check,
        )

    def warp_in(
        self,
        unit: UnitTypeId,
        position: Point2,
        can_afford_check: bool = False,
    ) -> Union[UnitCommand, bool]:
        """Orders Warpgate to warp in 'unit' at 'position'.

        :param unit:
        :param queue:
        :param can_afford_check:
        """
        normal_creation_ability = self._bot_object.game_data.units[unit.value].creation_ability.id
        return self(
            warpgate_abilities[normal_creation_ability],
            target=position,
            subtract_cost=True,
            subtract_supply=True,
            can_afford_check=can_afford_check,
        )

    def attack(self, target: Union[Unit, Point2], queue: bool = False) -> Union[UnitCommand, bool]:
        """Orders unit to attack. Target can be a Unit or Point2.
        Attacking a position will make the unit move there and attack everything on its way.

        :param target:
        :param queue:
        """
        return self(AbilityId.ATTACK, target=target, queue=queue)

    def smart(self, target: Union[Unit, Point2], queue: bool = False) -> Union[UnitCommand, bool]:
        """Orders the smart command. Equivalent to a right-click order.

        :param target:
        :param queue:
        """
        return self(AbilityId.SMART, target=target, queue=queue)

    def gather(self, target: Unit, queue: bool = False) -> Union[UnitCommand, bool]:
        """Orders a unit to gather minerals or gas.
        'Target' must be a mineral patch or a gas extraction building.

        :param target:
        :param queue:
        """
        return self(AbilityId.HARVEST_GATHER, target=target, queue=queue)

    def return_resource(self, target: Unit = None, queue: bool = False) -> Union[UnitCommand, bool]:
        """Orders the unit to return resource. Does not need a 'target'.

        :param target:
        :param queue:
        """
        return self(AbilityId.HARVEST_RETURN, target=target, queue=queue)

    def move(self, position: Union[Unit, Point2], queue: bool = False) -> Union[UnitCommand, bool]:
        """Orders the unit to move to 'position'.
        Target can be a Unit (to follow that unit) or Point2.

        :param position:
        :param queue:
        """
        return self(AbilityId.MOVE_MOVE, target=position, queue=queue)

    def hold_position(self, queue: bool = False) -> Union[UnitCommand, bool]:
        """Orders a unit to stop moving. It will not move until it gets new orders.

        :param queue:
        """
        return self(AbilityId.HOLDPOSITION, queue=queue)

    def stop(self, queue: bool = False) -> Union[UnitCommand, bool]:
        """Orders a unit to stop, but can start to move on its own
        if it is attacked, enemy unit is in range or other friendly
        units need the space.

        :param queue:
        """
        return self(AbilityId.STOP, queue=queue)

    def patrol(self, position: Point2, queue: bool = False) -> Union[UnitCommand, bool]:
        """Orders a unit to patrol between position it has when the command starts and the target position.
        Can be queued up to seven patrol points. If the last point is the same as the starting
        point, the unit will patrol in a circle.

        :param position:
        :param queue:
        """
        return self(AbilityId.PATROL, target=position, queue=queue)

    def repair(self, repair_target: Unit, queue: bool = False) -> Union[UnitCommand, bool]:
        """Order an SCV or MULE to repair.

        :param repair_target:
        :param queue:
        """
        return self(AbilityId.EFFECT_REPAIR, target=repair_target, queue=queue)

    def __hash__(self) -> int:
        return self.tag

    def __eq__(self, other: Union[Unit, Any]) -> bool:
        """
        :param other:
        """
        return self.tag == getattr(other, "tag", -1)

    def __call__(
        self,
        ability: AbilityId,
        target: Optional[Union[Point2, Unit]] = None,
        queue: bool = False,
        subtract_cost: bool = False,
        subtract_supply: bool = False,
        can_afford_check: bool = False,
    ) -> Union[UnitCommand, bool]:
        """ Deprecated: Stop using self.do() - This may be removed in the future.

        :param ability:
        :param target:
        :param queue:
        :param subtract_cost:
        :param subtract_supply:
        :param can_afford_check:
        """
        if self._bot_object.unit_command_uses_self_do:
            return UnitCommand(ability, self, target=target, queue=queue)
        expected_target: int = self._bot_object.game_data.abilities[ability.value]._proto.target
        # 1: None, 2: Point, 3: Unit, 4: PointOrUnit, 5: PointOrNone
        if target is None and expected_target not in {1, 5}:
            warnings.warn(
                f"{self} got {ability} with no target but expected {TARGET_HELPER[expected_target]}",
                RuntimeWarning,
                stacklevel=2,
            )
        elif isinstance(target, Point2) and expected_target not in {2, 4, 5}:
            warnings.warn(
                f"{self} got {ability} with Point2 as target but expected {TARGET_HELPER[expected_target]}",
                RuntimeWarning,
                stacklevel=2,
            )
        elif isinstance(target, Unit) and expected_target not in {3, 4}:
            warnings.warn(
                f"{self} got {ability} with Unit as target but expected {TARGET_HELPER[expected_target]}",
                RuntimeWarning,
                stacklevel=2,
            )
        return self._bot_object.do(
            UnitCommand(ability, self, target=target, queue=queue),
            subtract_cost=subtract_cost,
            subtract_supply=subtract_supply,
            can_afford_check=can_afford_check,
        )
