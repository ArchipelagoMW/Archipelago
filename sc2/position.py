from __future__ import annotations

import itertools
import math
import random
from typing import TYPE_CHECKING, Iterable, List, Set, Tuple, Union

from s2clientprotocol import common_pb2 as common_pb

if TYPE_CHECKING:
    from sc2.unit import Unit
    from sc2.units import Units

EPSILON = 10**-8


def _sign(num):
    return math.copysign(1, num)


class Pointlike(tuple):

    @property
    def position(self) -> Pointlike:
        return self

    def distance_to(self, target: Union[Unit, Point2]) -> float:
        """Calculate a single distance from a point or unit to another point or unit

        :param target:"""
        p = target.position
        return math.hypot(self[0] - p[0], self[1] - p[1])

    def distance_to_point2(self, p: Union[Point2, Tuple[float, float]]) -> float:
        """Same as the function above, but should be a bit faster because of the dropped asserts
        and conversion.

        :param p:"""
        return math.hypot(self[0] - p[0], self[1] - p[1])

    def _distance_squared(self, p2: Point2) -> float:
        """Function used to not take the square root as the distances will stay proportionally the same.
        This is to speed up the sorting process.

        :param p2:"""
        return (self[0] - p2[0])**2 + (self[1] - p2[1])**2

    def sort_by_distance(self, ps: Union[Units, Iterable[Point2]]) -> List[Point2]:
        """This returns the target points sorted as list.
        You should not pass a set or dict since those are not sortable.
        If you want to sort your units towards a point, use 'units.sorted_by_distance_to(point)' instead.

        :param ps:"""
        return sorted(ps, key=lambda p: self.distance_to_point2(p.position))

    def closest(self, ps: Union[Units, Iterable[Point2]]) -> Union[Unit, Point2]:
        """This function assumes the 2d distance is meant

        :param ps:"""
        assert ps, "ps is empty"
        # pylint: disable=W0108
        return min(ps, key=lambda p: self.distance_to(p))

    def distance_to_closest(self, ps: Union[Units, Iterable[Point2]]) -> float:
        """This function assumes the 2d distance is meant
        :param ps:"""
        assert ps, "ps is empty"
        closest_distance = math.inf
        for p2 in ps:
            p2 = p2.position
            distance = self.distance_to(p2)
            if distance <= closest_distance:
                closest_distance = distance
        return closest_distance

    def furthest(self, ps: Union[Units, Iterable[Point2]]) -> Union[Unit, Pointlike]:
        """This function assumes the 2d distance is meant

        :param ps: Units object, or iterable of Unit or Point2"""
        assert ps, "ps is empty"
        # pylint: disable=W0108
        return max(ps, key=lambda p: self.distance_to(p))

    def distance_to_furthest(self, ps: Union[Units, Iterable[Point2]]) -> float:
        """This function assumes the 2d distance is meant

        :param ps:"""
        assert ps, "ps is empty"
        furthest_distance = -math.inf
        for p2 in ps:
            p2 = p2.position
            distance = self.distance_to(p2)
            if distance >= furthest_distance:
                furthest_distance = distance
        return furthest_distance

    def offset(self, p) -> Pointlike:
        """

        :param p:
        """
        return self.__class__(a + b for a, b in itertools.zip_longest(self, p[:len(self)], fillvalue=0))

    def unit_axes_towards(self, p):
        """

        :param p:
        """
        return self.__class__(_sign(b - a) for a, b in itertools.zip_longest(self, p[:len(self)], fillvalue=0))

    def towards(self, p: Union[Unit, Pointlike], distance: Union[int, float] = 1, limit: bool = False) -> Pointlike:
        """

        :param p:
        :param distance:
        :param limit:
        """
        p = p.position
        # assert self != p, f"self is {self}, p is {p}"
        # TODO test and fix this if statement
        if self == p:
            return self
        # end of test
        d = self.distance_to(p)
        if limit:
            distance = min(d, distance)
        return self.__class__(
            a + (b - a) / d * distance for a, b in itertools.zip_longest(self, p[:len(self)], fillvalue=0)
        )

    def __eq__(self, other):
        try:
            return all(abs(a - b) <= EPSILON for a, b in itertools.zip_longest(self, other, fillvalue=0))
        except TypeError:
            return False

    def __hash__(self):
        return hash(tuple(self))


# pylint: disable=R0904
class Point2(Pointlike):

    @classmethod
    def from_proto(cls, data) -> Point2:
        """
        :param data:
        """
        return cls((data.x, data.y))

    @property
    def as_Point2D(self) -> common_pb.Point2D:
        return common_pb.Point2D(x=self.x, y=self.y)

    @property
    def as_PointI(self) -> common_pb.PointI:
        """Represents points on the minimap. Values must be between 0 and 64."""
        return common_pb.PointI(x=self.x, y=self.y)

    @property
    def rounded(self) -> Point2:
        return Point2((math.floor(self[0]), math.floor(self[1])))

    @property
    def length(self) -> float:
        """ This property exists in case Point2 is used as a vector. """
        return math.hypot(self[0], self[1])

    @property
    def normalized(self) -> Point2:
        """ This property exists in case Point2 is used as a vector. """
        length = self.length
        # Cannot normalize if length is zero
        assert length
        return self.__class__((self[0] / length, self[1] / length))

    @property
    def x(self) -> float:
        return self[0]

    @property
    def y(self) -> float:
        return self[1]

    @property
    def to2(self) -> Point2:
        return Point2(self[:2])

    @property
    def to3(self) -> Point3:
        return Point3((*self, 0))

    def round(self, decimals: int) -> Point2:
        """Rounds each number in the tuple to the amount of given decimals."""
        return Point2((round(self[0], decimals), round(self[1], decimals)))

    def offset(self, p: Point2) -> Point2:
        return Point2((self[0] + p[0], self[1] + p[1]))

    def random_on_distance(self, distance) -> Point2:
        if isinstance(distance, (tuple, list)):  # interval
            distance = distance[0] + random.random() * (distance[1] - distance[0])

        assert distance > 0, "Distance is not greater than 0"
        angle = random.random() * 2 * math.pi

        dx, dy = math.cos(angle), math.sin(angle)
        return Point2((self.x + dx * distance, self.y + dy * distance))

    def towards_with_random_angle(
        self,
        p: Union[Point2, Point3],
        distance: Union[int, float] = 1,
        max_difference: Union[int, float] = (math.pi / 4),
    ) -> Point2:
        tx, ty = self.to2.towards(p.to2, 1)
        angle = math.atan2(ty - self.y, tx - self.x)
        angle = (angle - max_difference) + max_difference * 2 * random.random()
        return Point2((self.x + math.cos(angle) * distance, self.y + math.sin(angle) * distance))

    def circle_intersection(self, p: Point2, r: Union[int, float]) -> Set[Point2]:
        """self is point1, p is point2, r is the radius for circles originating in both points
        Used in ramp finding

        :param p:
        :param r:"""
        assert self != p, "self is equal to p"
        distanceBetweenPoints = self.distance_to(p)
        assert r >= distanceBetweenPoints / 2
        # remaining distance from center towards the intersection, using pythagoras
        remainingDistanceFromCenter = (r**2 - (distanceBetweenPoints / 2)**2)**0.5
        # center of both points
        offsetToCenter = Point2(((p.x - self.x) / 2, (p.y - self.y) / 2))
        center = self.offset(offsetToCenter)

        # stretch offset vector in the ratio of remaining distance from center to intersection
        vectorStretchFactor = remainingDistanceFromCenter / (distanceBetweenPoints / 2)
        v = offsetToCenter
        offsetToCenterStretched = Point2((v.x * vectorStretchFactor, v.y * vectorStretchFactor))

        # rotate vector by 90° and -90°
        vectorRotated1 = Point2((offsetToCenterStretched.y, -offsetToCenterStretched.x))
        vectorRotated2 = Point2((-offsetToCenterStretched.y, offsetToCenterStretched.x))
        intersect1 = center.offset(vectorRotated1)
        intersect2 = center.offset(vectorRotated2)
        return {intersect1, intersect2}

    @property
    def neighbors4(self) -> set:
        return {
            Point2((self.x - 1, self.y)),
            Point2((self.x + 1, self.y)),
            Point2((self.x, self.y - 1)),
            Point2((self.x, self.y + 1)),
        }

    @property
    def neighbors8(self) -> set:
        return self.neighbors4 | {
            Point2((self.x - 1, self.y - 1)),
            Point2((self.x - 1, self.y + 1)),
            Point2((self.x + 1, self.y - 1)),
            Point2((self.x + 1, self.y + 1)),
        }

    def negative_offset(self, other: Point2) -> Point2:
        return self.__class__((self[0] - other[0], self[1] - other[1]))

    def __add__(self, other: Point2) -> Point2:
        return self.offset(other)

    def __sub__(self, other: Point2) -> Point2:
        return self.negative_offset(other)

    def __neg__(self) -> Point2:
        return self.__class__(-a for a in self)

    def __abs__(self) -> float:
        return math.hypot(self.x, self.y)

    def __bool__(self) -> bool:
        if self.x != 0 or self.y != 0:
            return True
        return False

    def __mul__(self, other: Union[int, float, Point2]) -> Point2:
        try:
            return self.__class__((self.x * other.x, self.y * other.y))
        except AttributeError:
            return self.__class__((self.x * other, self.y * other))

    def __rmul__(self, other: Union[int, float, Point2]) -> Point2:
        return self.__mul__(other)

    def __truediv__(self, other: Union[int, float, Point2]) -> Point2:
        if isinstance(other, self.__class__):
            return self.__class__((self.x / other.x, self.y / other.y))
        return self.__class__((self.x / other, self.y / other))

    def is_same_as(self, other: Point2, dist=0.001) -> bool:
        return self.distance_to_point2(other) <= dist

    def direction_vector(self, other: Point2) -> Point2:
        """ Converts a vector to a direction that can face vertically, horizontally or diagonal or be zero, e.g. (0, 0), (1, -1), (1, 0) """
        return self.__class__((_sign(other.x - self.x), _sign(other.y - self.y)))

    def manhattan_distance(self, other: Point2) -> float:
        """
        :param other:
        """
        return abs(other.x - self.x) + abs(other.y - self.y)

    @staticmethod
    def center(points: List[Point2]) -> Point2:
        """Returns the central point for points in list

        :param points:"""
        s = Point2((0, 0))
        for p in points:
            s += p
        return s / len(points)


class Point3(Point2):

    @classmethod
    def from_proto(cls, data) -> Point3:
        """
        :param data:
        """
        return cls((data.x, data.y, data.z))

    @property
    def as_Point(self) -> common_pb.Point:
        return common_pb.Point(x=self.x, y=self.y, z=self.z)

    @property
    def rounded(self) -> Point3:
        return Point3((math.floor(self[0]), math.floor(self[1]), math.floor(self[2])))

    @property
    def z(self) -> float:
        return self[2]

    @property
    def to3(self) -> Point3:
        return Point3(self)

    def __add__(self, other: Union[Point2, Point3]) -> Point3:
        if not isinstance(other, Point3) and isinstance(other, Point2):
            return Point3((self.x + other.x, self.y + other.y, self.z))
        return Point3((self.x + other.x, self.y + other.y, self.z + other.z))


class Size(Point2):

    @property
    def width(self) -> float:
        return self[0]

    @property
    def height(self) -> float:
        return self[1]


class Rect(tuple):

    @classmethod
    def from_proto(cls, data):
        """
        :param data:
        """
        assert data.p0.x < data.p1.x and data.p0.y < data.p1.y
        return cls((data.p0.x, data.p0.y, data.p1.x - data.p0.x, data.p1.y - data.p0.y))

    @property
    def x(self) -> float:
        return self[0]

    @property
    def y(self) -> float:
        return self[1]

    @property
    def width(self) -> float:
        return self[2]

    @property
    def height(self) -> float:
        return self[3]

    @property
    def right(self) -> float:
        """ Returns the x-coordinate of the rectangle of its right side. """
        return self.x + self.width

    @property
    def top(self) -> float:
        """ Returns the y-coordinate of the rectangle of its top side. """
        return self.y + self.height

    @property
    def size(self) -> Size:
        return Size((self[2], self[3]))

    @property
    def center(self) -> Point2:
        return Point2((self.x + self.width / 2, self.y + self.height / 2))

    def offset(self, p):
        return self.__class__((self[0] + p[0], self[1] + p[1], self[2], self[3]))
