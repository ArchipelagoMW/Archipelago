"""Class definition for bijection."""

from collections import MutableMapping, Mapping


class bijection(MutableMapping):
	"""A one-to-one onto mapping, a dict with unique values."""

	def __init__(self, iterable=None, **kwarg):
		"""Create a bijection from an iterable.

		Matches dict.__init__.
		"""
		self._data = {}
		self.__inverse = self.__new__(bijection)
		self.__inverse._data = {}
		self.__inverse.__inverse = self
		if iterable is not None:
			if isinstance(iterable, Mapping):
				for key, value in iterable.items():
					self[key] = value
			else:
				for pair in iterable:
					self[pair[0]] = pair[1]
		for key, value in kwarg.items():
			self[key] = value

	def __repr__(self):
		if len(self._data) == 0:
			return '{0}()'.format(self.__class__.__name__)
		else:
			repr_format = '{class_name}({values!r})'
			return repr_format.format(
				class_name=self.__class__.__name__,
				values=self._data,
				)

	@property
	def inverse(self):
		"""Return the inverse of this bijection."""
		return self.__inverse

	# Required for MutableMapping
	def __len__(self):
		return len(self._data)

	# Required for MutableMapping
	def __getitem__(self, key):
		return self._data[key]

	# Required for MutableMapping
	def __setitem__(self, key, value):
		if key in self:
			del self.inverse._data[self[key]]
		if value in self.inverse:
			del self._data[self.inverse[value]]
		self._data[key] = value
		self.inverse._data[value] = key

	# Required for MutableMapping
	def __delitem__(self, key):
		value = self._data.pop(key)
		del self.inverse._data[value]

	# Required for MutableMapping
	def __iter__(self):
		return iter(self._data)

	def __contains__(self, key):
		return key in self._data

	def clear(self):
		"""Remove everything from this bijection."""
		self._data.clear()
		self.inverse._data.clear()

	def copy(self):
		"""Return a copy of this bijection."""
		return bijection(self)

	def items(self):
		"""See Mapping.items."""
		return self._data.items()

	def keys(self):
		"""See Mapping.keys."""
		return self._data.keys()

	def values(self):
		"""See Mapping.values."""
		return self.inverse.keys()

	def __eq__(self, other):
		return isinstance(other, bijection) and self._data == other._data
