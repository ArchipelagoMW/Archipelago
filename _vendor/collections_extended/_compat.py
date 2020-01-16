"""Python 2/3 compatibility helpers."""
import sys

is_py2 = sys.version_info[0] == 2

if is_py2:
	def keys_set(d):
		"""Return a set of passed dictionary's keys."""
		return set(d.keys())
else:
	keys_set = dict.keys


if sys.version_info < (3, 6):
	from collections import Sized, Iterable, Container

	def _check_methods(C, *methods):
		mro = C.__mro__
		for method in methods:
			for B in mro:
				if method in B.__dict__:
					if B.__dict__[method] is None:
						return NotImplemented
					break
			else:
				return NotImplemented
		return True

	class Collection(Sized, Iterable, Container):
		"""Backport from Python3.6."""

		__slots__ = tuple()

		@classmethod
		def __subclasshook__(cls, C):
			if cls is Collection:
				return _check_methods(C, "__len__", "__iter__", "__contains__")
			return NotImplemented

else:
	from collections.abc import Collection


def handle_rich_comp_not_implemented():
	"""Correctly handle unimplemented rich comparisons.

	In Python 3, return NotImplemented.
	In Python 2, raise a TypeError.
	"""
	if is_py2:
		raise TypeError()
	else:
		return NotImplemented
