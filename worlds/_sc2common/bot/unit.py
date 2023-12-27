# pylint: disable=W0212
from __future__ import annotations

import math
from dataclasses import dataclass
from functools import cached_property
from typing import TYPE_CHECKING, Any, List, Optional, Set, Tuple, Union

from .cache import CacheDict
from .constants import (
    CAN_BE_ATTACKED,
    IS_ARMORED,
    IS_BIOLOGICAL,
    IS_CLOAKED,
    IS_ENEMY,
    IS_LIGHT,
    IS_MASSIVE,
    IS_MECHANICAL,
    IS_MINE,
    IS_PLACEHOLDER,
    IS_PSIONIC,
    IS_REVEALED,
    IS_SNAPSHOT,
    IS_STRUCTURE,
    IS_VISIBLE,
)
from .data import Alliance, Attribute, CloakState, Race
from .position import Point2, Point3

if TYPE_CHECKING:
    from .bot_ai import BotAI
    from .game_data import AbilityData, UnitTypeData


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
    def _weapons(self):
        """ Returns the weapons of the unit. """
        return self._type_data._proto.weapons

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

    @property
    def detect_range(self) -> float:
        """ Returns the detection distance of the unit. """
        return self._proto.detect_range

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

    def __hash__(self) -> int:
        return self.tag

    def __eq__(self, other: Union[Unit, Any]) -> bool:
        """
        :param other:
        """
        return self.tag == getattr(other, "tag", -1)
