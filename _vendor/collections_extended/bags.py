"""Bag class definitions."""
import heapq
from operator import itemgetter
from collections import Set, MutableSet, Hashable

from . import _compat


class _basebag(Set):
	"""Base class for bag classes.

	Base class for bag and frozenbag.	Is not mutable and not hashable, so there's
	no reason to use this instead of either bag or frozenbag.
	"""

	# Basic object methods

	def __init__(self, iterable=None):
		"""Create a new basebag.

		If iterable isn't given, is None or is empty then the bag starts empty.
		Otherwise each element from iterable will be added to the bag
		however many times it appears.

		This runs in O(len(iterable))
		"""
		self._dict = dict()
		self._size = 0
		if iterable:
			if isinstance(iterable, _basebag):
				for elem, count in iterable._dict.items():
					self._dict[elem] = count
					self._size += count
			else:
				for value in iterable:
					self._dict[value] = self._dict.get(value, 0) + 1
					self._size += 1

	def __repr__(self):
		if self._size == 0:
			return '{0}()'.format(self.__class__.__name__)
		else:
			repr_format = '{class_name}({values!r})'
			return repr_format.format(
				class_name=self.__class__.__name__,
				values=tuple(self),
				)

	def __str__(self):
		if self._size == 0:
			return '{class_name}()'.format(class_name=self.__class__.__name__)
		else:
			format_single = '{elem!r}'
			format_mult = '{elem!r}^{mult}'
			strings = []
			for elem, mult in self._dict.items():
				if mult > 1:
					strings.append(format_mult.format(elem=elem, mult=mult))
				else:
					strings.append(format_single.format(elem=elem))
			return '{%s}' % ', '.join(strings)

	# New public methods (not overriding/implementing anything)

	def num_unique_elements(self):
		"""Return the number of unique elements.

		This runs in O(1) time
		"""
		return len(self._dict)

	def unique_elements(self):
		"""Return a view of unique elements in this bag.

		In Python 3:
			This runs in O(1) time and returns a view of the unique elements
		In Python 2:
			This runs in O(n) and returns set of the current elements.
		"""
		return _compat.keys_set(self._dict)

	def count(self, value):
		"""Return the number of value present in this bag.

		If value is not in the bag no Error is raised, instead 0 is returned.

		This runs in O(1) time

		Args:
			value: The element of self to get the count of
		Returns:
			int: The count of value in self
		"""
		return self._dict.get(value, 0)

	def nlargest(self, n=None):
		"""List the n most common elements and their counts.

		List is from the most
		common to the least.  If n is None, the list all element counts.

		Run time should be O(m log m) where m is len(self)
		Args:
			n (int): The number of elements to return
		"""
		if n is None:
			return sorted(self._dict.items(), key=itemgetter(1), reverse=True)
		else:
			return heapq.nlargest(n, self._dict.items(), key=itemgetter(1))

	@classmethod
	def _from_iterable(cls, it):
		return cls(it)

	@classmethod
	def from_mapping(cls, mapping):
		"""Create a bag from a dict of elem->count.

		Each key in the dict is added if the value is > 0.
		"""
		out = cls()
		for elem, count in mapping.items():
			if count > 0:
				out._dict[elem] = count
				out._size += count
		return out

	def copy(self):
		"""Create a shallow copy of self.

		This runs in O(len(self.num_unique_elements()))
		"""
		return self.from_mapping(self._dict)

	# implementing Sized methods

	def __len__(self):
		"""Return the cardinality of the bag.

		This runs in O(1)
		"""
		return self._size

	# implementing Container methods

	def __contains__(self, value):
		"""Return the multiplicity of the element.

		This runs in O(1)
		"""
		return self._dict.get(value, 0)

	# implementing Iterable methods

	def __iter__(self):
		"""Iterate through all elements.

		Multiple copies will be returned if they exist.
		"""
		for value, count in self._dict.items():
			for i in range(count):
				yield(value)

	# Comparison methods

	def _is_subset(self, other):
		"""Check that every element in self has a count <= in other.

		Args:
			other (Set)
		"""
		if isinstance(other, _basebag):
			for elem, count in self._dict.items():
				if not count <= other._dict.get(elem, 0):
					return False
		else:
			for elem in self:
				if self._dict.get(elem, 0) > 1 or elem not in other:
					return False
		return True

	def _is_superset(self, other):
		"""Check that every element in self has a count >= in other.

		Args:
			other (Set)
		"""
		if isinstance(other, _basebag):
			for elem, count in other._dict.items():
				if not self._dict.get(elem, 0) >= count:
					return False
		else:
			for elem in other:
				if elem not in self:
					return False
		return True

	def __le__(self, other):
		if not isinstance(other, Set):
			return _compat.handle_rich_comp_not_implemented()
		return len(self) <= len(other) and self._is_subset(other)

	def __lt__(self, other):
		if not isinstance(other, Set):
			return _compat.handle_rich_comp_not_implemented()
		return len(self) < len(other) and self._is_subset(other)

	def __gt__(self, other):
		if not isinstance(other, Set):
			return _compat.handle_rich_comp_not_implemented()
		return len(self) > len(other) and self._is_superset(other)

	def __ge__(self, other):
		if not isinstance(other, Set):
			return _compat.handle_rich_comp_not_implemented()
		return len(self) >= len(other) and self._is_superset(other)

	def __eq__(self, other):
		if not isinstance(other, Set):
			return False
		if isinstance(other, _basebag):
			return self._dict == other._dict
		if not len(self) == len(other):
			return False
		for elem in other:
			if self._dict.get(elem, 0) != 1:
				return False
		return True

	def __ne__(self, other):
		return not (self == other)

	# Operations - &, |, +, -, ^, * and isdisjoint

	def __and__(self, other):
		"""Intersection is the minimum of corresponding counts.

		This runs in O(l + n) where:
			n is self.num_unique_elements()
			if other is a bag:
				l = 1
			else:
				l = len(other)
		"""
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		values = dict()
		for elem in self._dict:
			values[elem] = min(other._dict.get(elem, 0), self._dict.get(elem, 0))
		return self.from_mapping(values)

	def isdisjoint(self, other):
		"""Return if this bag is disjoint with the passed collection.

		This runs in O(len(other))

		TODO move isdisjoint somewhere more appropriate
		"""
		for value in other:
			if value in self:
				return False
		return True

	def __or__(self, other):
		"""Union is the maximum of all elements.

		This runs in O(m + n) where:
			n is self.num_unique_elements()
			if other is a bag:
				m = other.num_unique_elements()
			else:
				m = len(other)
		"""
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		values = dict()
		for elem in self.unique_elements() | other.unique_elements():
			values[elem] = max(self._dict.get(elem, 0), other._dict.get(elem, 0))
		return self.from_mapping(values)

	def __add__(self, other):
		"""Return a new bag also containing all the elements of other.

		self + other = self & other + self | other

		This runs in O(m + n) where:
			n is self.num_unique_elements()
			m is len(other)
		Args:
			other (Iterable): elements to add to self
		"""
		out = self.copy()
		for value in other:
			out._dict[value] = out._dict.get(value, 0) + 1
			out._size += 1
		return out

	def __sub__(self, other):
		"""Difference between the sets.

		For normal sets this is all x s.t. x in self and x not in other.
		For bags this is count(x) = max(0, self.count(x)-other.count(x))

		This runs in O(m + n) where:
			n is self.num_unique_elements()
			m is len(other)
		Args:
			other (Iterable): elements to remove
		"""
		out = self.copy()
		for value in other:
			old_count = out._dict.get(value, 0)
			if old_count == 1:
				del out._dict[value]
				out._size -= 1
			elif old_count > 1:
				out._dict[value] = old_count - 1
				out._size -= 1
		return out

	def __mul__(self, other):
		"""Cartesian product of the two sets.

		other can be any iterable.
		Both self and other must contain elements that can be added together.

		This should run in O(m*n+l) where:
			m is the number of unique elements in self
			n is the number of unique elements in other
			if other is a bag:
				l is 0
			else:
				l is the len(other)
		The +l will only really matter when other is an iterable with MANY
		repeated elements.
		For example: {'a'^2} * 'bbbbbbbbbbbbbbbbbbbbbbbbbb'
		The algorithm will be dominated by counting the 'b's
		"""
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		values = dict()
		for elem, count in self._dict.items():
			for other_elem, other_count in other._dict.items():
				new_elem = elem + other_elem
				new_count = count * other_count
				values[new_elem] = new_count
		return self.from_mapping(values)

	def __xor__(self, other):
		"""Symmetric difference between the sets.

		other can be any iterable.

		This runs in O(m + n) where:
			m = len(self)
			n = len(other)
		"""
		return (self - other) | (other - self)


class bag(_basebag, MutableSet):
	"""bag is a mutable unhashable bag."""

	def pop(self):
		"""Remove and return an element of self."""
		# TODO can this be done more efficiently (no need to create an iterator)?
		it = iter(self)
		try:
			value = next(it)
		except StopIteration:
			raise KeyError
		self.discard(value)
		return value

	def add(self, elem):
		"""Add elem to self."""
		self._dict[elem] = self._dict.get(elem, 0) + 1
		self._size += 1

	def discard(self, elem):
		"""Remove elem from this bag, silent if it isn't present."""
		try:
			self.remove(elem)
		except ValueError:
			pass

	def remove(self, elem):
		"""Remove elem from this bag, raising a ValueError if it isn't present.

		Args:
			elem: object to remove from self
		Raises:
			ValueError: if the elem isn't present
		"""
		old_count = self._dict.get(elem, 0)
		if old_count == 0:
			raise ValueError
		elif old_count == 1:
			del self._dict[elem]
		else:
			self._dict[elem] -= 1
		self._size -= 1

	def discard_all(self, other):
		"""Discard all of the elems from other."""
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		for elem, other_count in other._dict.items():
			old_count = self._dict.get(elem, 0)
			new_count = old_count - other_count
			if new_count >= 0:
				if new_count == 0:
					if elem in self:
						del self._dict[elem]
				else:
					self._dict[elem] = new_count
				self._size += new_count - old_count

	def remove_all(self, other):
		"""Remove all of the elems from other.

		Raises a ValueError if the multiplicity of any elem in other is greater
		than in self.
		"""
		if not self._is_superset(other):
			raise ValueError
		self.discard_all(other)

	def clear(self):
		"""Remove all elements from this bag."""
		self._dict = dict()
		self._size = 0

	# In-place operations

	def __ior__(self, other):
		"""Set multiplicity of each element to the maximum of the two collections.

		if isinstance(other, _basebag):
			This runs in O(other.num_unique_elements())
		else:
			This runs in O(len(other))
		"""
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		for elem, other_count in other._dict.items():
			old_count = self._dict.get(elem, 0)
			new_count = max(other_count, old_count)
			self._dict[elem] = new_count
			self._size += new_count - old_count
		return self

	def __iand__(self, other):
		"""Set multiplicity of each element to the minimum of the two collections.

		if isinstance(other, _basebag):
			This runs in O(other.num_unique_elements())
		else:
			This runs in O(len(other))
		"""
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		for elem, old_count in set(self._dict.items()):
			other_count = other._dict.get(elem, 0)
			new_count = min(other_count, old_count)
			if new_count == 0:
				del self._dict[elem]
			else:
				self._dict[elem] = new_count
			self._size += new_count - old_count
		return self

	def __ixor__(self, other):
		"""Set self to the symmetric difference between the sets.

		if isinstance(other, _basebag):
			This runs in O(other.num_unique_elements())
		else:
			This runs in O(len(other))
		"""
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		other_minus_self = other - self
		self -= other
		self |= other_minus_self
		return self

	def __isub__(self, other):
		"""Discard the elements of other from self.

		if isinstance(it, _basebag):
			This runs in O(it.num_unique_elements())
		else:
			This runs in O(len(it))
		"""
		self.discard_all(other)
		return self

	def __iadd__(self, other):
		"""Add all of the elements of other to self.

		if isinstance(it, _basebag):
			This runs in O(it.num_unique_elements())
		else:
			This runs in O(len(it))
		"""
		if not isinstance(other, _basebag):
			other = self._from_iterable(other)
		for elem, other_count in other._dict.items():
			self._dict[elem] = self._dict.get(elem, 0) + other_count
			self._size += other_count
		return self


class frozenbag(_basebag, Hashable):
	"""frozenbag is an immutable, hashable bab."""

	def __hash__(self):
		"""Compute the hash value of a frozenbag.

		This was copied directly from _collections_abc.Set._hash in Python3 which
		is identical to _abcoll.Set._hash
		We can't call it directly because Python2 raises a TypeError.
		"""
		if not hasattr(self, '_hash_value'):
			self._hash_value = self._hash()
		return self._hash_value
