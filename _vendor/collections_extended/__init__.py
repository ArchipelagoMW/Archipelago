"""collections_extended contains a few extra basic data structures."""
from ._compat import Collection
from .bags import bag, frozenbag
from .setlists import setlist, frozensetlist
from .bijection import bijection
from .range_map import RangeMap, MappedRange

__version__ = '1.0.2'

__all__ = (
	'collection',
	'setlist',
	'frozensetlist',
	'bag',
	'frozenbag',
	'bijection',
	'RangeMap',
	'MappedRange',
	'Collection',
	)


def collection(iterable=None, mutable=True, ordered=False, unique=False):
	"""Return a Collection with the specified properties.

	Args:
		iterable (Iterable): collection to instantiate new collection from.
		mutable (bool): Whether or not the new collection is mutable.
		ordered (bool): Whether or not the new collection is ordered.
		unique (bool): Whether or not the new collection contains only unique values.
	"""
	if iterable is None:
		iterable = tuple()
	if unique:
		if ordered:
			if mutable:
				return setlist(iterable)
			else:
				return frozensetlist(iterable)
		else:
			if mutable:
				return set(iterable)
			else:
				return frozenset(iterable)
	else:
		if ordered:
			if mutable:
				return list(iterable)
			else:
				return tuple(iterable)
		else:
			if mutable:
				return bag(iterable)
			else:
				return frozenbag(iterable)
