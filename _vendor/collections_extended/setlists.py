"""Setlist class definitions."""
import random as random_

from collections import (
	Sequence,
	Set,
	MutableSequence,
	MutableSet,
	Hashable,
	)

from . import _util


class _basesetlist(Sequence, Set):
	"""A setlist is an ordered Collection of unique elements.

	_basesetlist is the superclass of setlist and frozensetlist.  It is immutable
	and unhashable.
	"""

	def __init__(self, iterable=None, raise_on_duplicate=False):
		"""Create a setlist.

		Args:
			iterable (Iterable): Values to initialize the setlist with.
		"""
		self._list = list()
		self._dict = dict()
		if iterable:
			if raise_on_duplicate:
				self._extend(iterable)
			else:
				self._update(iterable)

	def __repr__(self):
		if len(self) == 0:
			return '{0}()'.format(self.__class__.__name__)
		else:
			repr_format = '{class_name}({values!r})'
			return repr_format.format(
				class_name=self.__class__.__name__,
				values=tuple(self),
				)

	# Convenience methods
	def _fix_neg_index(self, index):
		if index < 0:
			index += len(self)
		if index < 0:
			raise IndexError('index is out of range')
		return index

	def _fix_end_index(self, index):
		if index is None:
			return len(self)
		else:
			return self._fix_neg_index(index)

	def _append(self, value):
		# Checking value in self will check that value is Hashable
		if value in self:
			raise ValueError('Value "%s" already present' % str(value))
		else:
			self._dict[value] = len(self)
			self._list.append(value)

	def _extend(self, values):
		new_values = set()
		for value in values:
			if value in new_values:
				raise ValueError('New values contain duplicates')
			elif value in self:
				raise ValueError('New values contain elements already present in self')
			else:
				new_values.add(value)
		for value in values:
			self._dict[value] = len(self)
			self._list.append(value)

	def _add(self, item):
		if item not in self:
			self._dict[item] = len(self)
			self._list.append(item)

	def _update(self, values):
		for value in values:
			if value not in self:
				self._dict[value] = len(self)
				self._list.append(value)

	@classmethod
	def _from_iterable(cls, it, **kwargs):
		return cls(it, **kwargs)

	# Implement Container
	def __contains__(self, value):
		return value in self._dict

	# Iterable we get by inheriting from Sequence

	# Implement Sized
	def __len__(self):
		return len(self._list)

	# Implement Sequence
	def __getitem__(self, index):
		if isinstance(index, slice):
			return self._from_iterable(self._list[index])
		return self._list[index]

	def count(self, value):
		"""Return the number of occurences of value in self.

		This runs in O(1)

		Args:
			value: The value to count
		Returns:
			int: 1 if the value is in the setlist, otherwise 0
		"""
		if value in self:
			return 1
		else:
			return 0

	def index(self, value, start=0, end=None):
		"""Return the index of value between start and end.

		By default, the entire setlist is searched.

		This runs in O(1)

		Args:
			value: The value to find the index of
			start (int): The index to start searching at (defaults to 0)
			end (int): The index to stop searching at (defaults to the end of the list)
		Returns:
			int: The index of the value
		Raises:
			ValueError: If the value is not in the list or outside of start - end
			IndexError: If start or end are out of range
		"""
		try:
			index = self._dict[value]
		except KeyError:
			raise ValueError
		else:
			start = self._fix_neg_index(start)
			end = self._fix_end_index(end)
			if start <= index and index < end:
				return index
			else:
				raise ValueError

	@classmethod
	def _check_type(cls, other, operand_name):
		if not isinstance(other, _basesetlist):
			message = (
				"unsupported operand type(s) for {operand_name}: "
				"'{self_type}' and '{other_type}'").format(
					operand_name=operand_name,
					self_type=cls,
					other_type=type(other),
					)
			raise TypeError(message)

	def __add__(self, other):
		self._check_type(other, '+')
		out = self.copy()
		out._extend(other)
		return out

	# Implement Set

	def issubset(self, other):
		return self <= other

	def issuperset(self, other):
		return self >= other

	def union(self, other):
		out = self.copy()
		out.update(other)
		return out

	def intersection(self, other):
		other = set(other)
		return self._from_iterable(item for item in self if item in other)

	def difference(self, other):
		other = set(other)
		return self._from_iterable(item for item in self if item not in other)

	def symmetric_difference(self, other):
		return self.union(other) - self.intersection(other)

	def __sub__(self, other):
		self._check_type(other, '-')
		return self.difference(other)

	def __and__(self, other):
		self._check_type(other, '&')
		return self.intersection(other)

	def __or__(self, other):
		self._check_type(other, '|')
		return self.union(other)

	def __xor__(self, other):
		self._check_type(other, '^')
		return self.symmetric_difference(other)

	# Comparison

	def __eq__(self, other):
		if not isinstance(other, _basesetlist):
			return False
		if not len(self) == len(other):
			return False
		for self_elem, other_elem in zip(self, other):
			if self_elem != other_elem:
				return False
		return True

	def __ne__(self, other):
		return not (self == other)

	# New methods

	def sub_index(self, sub, start=0, end=None):
		"""Return the index of a subsequence.

		This runs in O(len(sub))

		Args:
			sub (Sequence): An Iterable to search for
		Returns:
			int: The index of the first element of sub
		Raises:
			ValueError: If sub isn't a subsequence
			TypeError: If sub isn't iterable
			IndexError: If start or end are out of range
		"""
		start_index = self.index(sub[0], start, end)
		end = self._fix_end_index(end)
		if start_index + len(sub) > end:
			raise ValueError
		for i in range(1, len(sub)):
			if sub[i] != self[start_index + i]:
				raise ValueError
		return start_index

	def copy(self):
		return self.__class__(self)


class setlist(_basesetlist, MutableSequence, MutableSet):
	"""A mutable (unhashable) setlist."""

	def __str__(self):
		return '{[%s}]' % ', '.join(repr(v) for v in self)

	# Helper methods
	def _delete_all(self, elems_to_delete, raise_errors):
		indices_to_delete = set()
		for elem in elems_to_delete:
			try:
				elem_index = self._dict[elem]
			except KeyError:
				if raise_errors:
					raise ValueError('Passed values contain elements not in self')
			else:
				if elem_index in indices_to_delete:
					if raise_errors:
						raise ValueError('Passed vales contain duplicates')
				indices_to_delete.add(elem_index)
		self._delete_values_by_index(indices_to_delete)

	def _delete_values_by_index(self, indices_to_delete):
		deleted_count = 0
		for i, elem in enumerate(self._list):
			if i in indices_to_delete:
				deleted_count += 1
				del self._dict[elem]
			else:
				new_index = i - deleted_count
				self._list[new_index] = elem
				self._dict[elem] = new_index
		# Now remove deleted_count items from the end of the list
		if deleted_count:
			self._list = self._list[:-deleted_count]

	# Set/Sequence agnostic
	def pop(self, index=-1):
		"""Remove and return the item at index."""
		value = self._list.pop(index)
		del self._dict[value]
		return value

	def clear(self):
		"""Remove all elements from self."""
		self._dict = dict()
		self._list = list()

	# Implement MutableSequence
	def __setitem__(self, index, value):
		if isinstance(index, slice):
			old_values = self[index]
			for v in value:
				if v in self and v not in old_values:
					raise ValueError
			self._list[index] = value
			self._dict = {}
			for i, v in enumerate(self._list):
				self._dict[v] = i
		else:
			index = self._fix_neg_index(index)
			old_value = self._list[index]
			if value in self:
				if value == old_value:
					return
				else:
					raise ValueError
			del self._dict[old_value]
			self._list[index] = value
			self._dict[value] = index

	def __delitem__(self, index):
		if isinstance(index, slice):
			indices_to_delete = set(self.index(e) for e in self._list[index])
			self._delete_values_by_index(indices_to_delete)
		else:
			index = self._fix_neg_index(index)
			value = self._list[index]
			del self._dict[value]
			for elem in self._list[index + 1:]:
				self._dict[elem] -= 1
			del self._list[index]

	def insert(self, index, value):
		"""Insert value at index.

		Args:
			index (int): Index to insert value at
			value: Value to insert
		Raises:
			ValueError: If value already in self
			IndexError: If start or end are out of range
		"""
		if value in self:
			raise ValueError
		index = self._fix_neg_index(index)
		self._dict[value] = index
		for elem in self._list[index:]:
			self._dict[elem] += 1
		self._list.insert(index, value)

	def append(self, value):
		"""Append value to the end.

		Args:
			value: Value to append
		Raises:
			ValueError: If value alread in self
			TypeError: If value isn't hashable
		"""
		self._append(value)

	def extend(self, values):
		"""Append all values to the end.

		If any of the values are present, ValueError will
		be raised and none of the values will be appended.

		Args:
			values (Iterable): Values to append
		Raises:
			ValueError: If any values are already present or there are duplicates
				in the passed values.
			TypeError: If any of the values aren't hashable.
		"""
		self._extend(values)

	def __iadd__(self, values):
		"""Add all values to the end of self.

		Args:
			values (Iterable): Values to append
		Raises:
			ValueError: If any values are already present
		"""
		self._check_type(values, '+=')
		self.extend(values)
		return self

	def remove(self, value):
		"""Remove value from self.

		Args:
			value: Element to remove from self
		Raises:
			ValueError: if element is already present
		"""
		try:
			index = self._dict[value]
		except KeyError:
			raise ValueError('Value "%s" is not present.')
		else:
			del self[index]

	def remove_all(self, elems_to_delete):
		"""Remove all elements from elems_to_delete, raises ValueErrors.

		See Also:
			discard_all
		Args:
			elems_to_delete (Iterable): Elements to remove.
		Raises:
			ValueError: If the count of any element is greater in
				elems_to_delete than self.
			TypeError: If any of the values aren't hashable.
		"""
		self._delete_all(elems_to_delete, raise_errors=True)

	# Implement MutableSet

	def add(self, item):
		"""Add an item.

		Note:
			This does not raise a ValueError for an already present value like
			append does. This is to match the behavior of set.add
		Args:
			item: Item to add
		Raises:
			TypeError: If item isn't hashable.
		"""
		self._add(item)

	def update(self, values):
		"""Add all values to the end.

		If any of the values are present, silently ignore
		them (as opposed to extend which raises an Error).

		See also:
			extend
		Args:
			values (Iterable): Values to add
		Raises:
			TypeError: If any of the values are unhashable.
		"""
		self._update(values)

	def discard_all(self, elems_to_delete):
		"""Discard all the elements from elems_to_delete.

		This is much faster than removing them one by one.
		This runs in O(len(self) + len(elems_to_delete))

		Args:
			elems_to_delete (Iterable): Elements to discard.
		Raises:
			TypeError: If any of the values aren't hashable.
		"""
		self._delete_all(elems_to_delete, raise_errors=False)

	def discard(self, value):
		"""Discard an item.

		Note:
			This does not raise a ValueError for a missing value like remove does.
			This is to match the behavior of set.discard
		"""
		try:
			self.remove(value)
		except ValueError:
			pass

	def difference_update(self, other):
		"""Update self to include only the differene with other."""
		other = set(other)
		indices_to_delete = set()
		for i, elem in enumerate(self):
			if elem in other:
				indices_to_delete.add(i)
		if indices_to_delete:
			self._delete_values_by_index(indices_to_delete)

	def intersection_update(self, other):
		"""Update self to include only the intersection with other."""
		other = set(other)
		indices_to_delete = set()
		for i, elem in enumerate(self):
			if elem not in other:
				indices_to_delete.add(i)
		if indices_to_delete:
			self._delete_values_by_index(indices_to_delete)

	def symmetric_difference_update(self, other):
		"""Update self to include only the symmetric difference with other."""
		other = setlist(other)
		indices_to_delete = set()
		for i, item in enumerate(self):
			if item in other:
				indices_to_delete.add(i)
		for item in other:
			self.add(item)
		self._delete_values_by_index(indices_to_delete)

	def __isub__(self, other):
		self._check_type(other, '-=')
		self.difference_update(other)
		return self

	def __iand__(self, other):
		self._check_type(other, '&=')
		self.intersection_update(other)
		return self

	def __ior__(self, other):
		self._check_type(other, '|=')
		self.update(other)
		return self

	def __ixor__(self, other):
		self._check_type(other, '^=')
		self.symmetric_difference_update(other)
		return self

	# New methods
	def shuffle(self, random=None):
		"""Shuffle all of the elements in self randomly."""
		random_.shuffle(self._list, random=random)
		for i, elem in enumerate(self._list):
			self._dict[elem] = i

	def sort(self, *args, **kwargs):
		"""Sort this setlist in place."""
		self._list.sort(*args, **kwargs)
		for index, value in enumerate(self._list):
			self._dict[value] = index


class frozensetlist(_basesetlist, Hashable):
	"""An immutable (hashable) setlist."""

	def __hash__(self):
		if not hasattr(self, '_hash_value'):
			self._hash_value = _util.hash_iterable(self)
		return self._hash_value
