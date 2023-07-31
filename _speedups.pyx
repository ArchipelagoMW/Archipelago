#cython: language_level=3
#distutils: language = c++

"""
Provides faster implementation of some core parts.
This is deliberately .pyx because using a non-compiled "pure python" may be slower.
"""

# pip install cython cymem
import cython
import warnings
from cpython cimport PyObject
from typing import Any, Dict, Iterable, Iterator, Generator, Sequence, Tuple, TypeVar, Union, Set, List, TYPE_CHECKING
from cymem.cymem cimport Pool
from libc.stdint cimport int64_t, uint32_t
from libcpp.set cimport set as std_set
from collections import defaultdict

cdef extern from *:
    """
    // avoid warning from cython-generated code with MSVC + pyximport
    #ifdef _MSC_VER
    #pragma warning( disable: 4551 )
    #endif
    """

ctypedef uint32_t ap_player_t  # on AMD64 this is faster (and smaller) than 64bit ints
ctypedef uint32_t ap_flags_t
ctypedef int64_t ap_id_t

cdef ap_player_t MAX_PLAYER_ID = 1000000  # limit the size of indexing array
cdef size_t INVALID_SIZE = <size_t>(-1)  # this is all 0xff... adding 1 results in 0, but it's not negative


cdef struct LocationEntry:
    # layout is so that
    # 64bit player: location+sender and item+receiver 128bit comparisons, if supported
    # 32bit player: aligned to 32/64bit with no unused space
    ap_id_t location
    ap_player_t sender
    ap_player_t receiver
    ap_id_t item
    ap_flags_t flags


cdef struct IndexEntry:
    size_t start
    size_t count


cdef class LocationStore:
    """Compact store for locations and their items in a MultiServer"""
    # The original implementation uses Dict[int, Dict[int, Tuple(int, int, int]]
    # with sender, location, (item, receiver, flags).
    # This implementation is a flat list of (sender, location, item, receiver, flags) using native integers
    # as well as some mapping arrays used to speed up stuff, saving a lot of memory while speeding up hints.
    # Using std::map might be worth investigating, but memory overhead would be ~100% compared to arrays.

    cdef Pool _mem
    cdef object _len
    cdef LocationEntry* entries  # 3.2MB/100k items
    cdef size_t entry_count
    cdef IndexEntry* sender_index  # 16KB/1000 players
    cdef size_t sender_index_size
    cdef list _keys  # ~36KB/1000 players, speed up iter (28 per int + 8 per list entry)
    cdef list _items  # ~64KB/1000 players, speed up items (56 per tuple + 8 per list entry)
    cdef list _proxies  # ~92KB/1000 players, speed up self[player] (56 per struct + 28 per len + 8 per list entry)
    cdef PyObject** _raw_proxies  # 8K/1000 players, faster access to _proxies, but does not keep a ref

    def get_size(self):
        from sys import getsizeof
        size = getsizeof(self) + getsizeof(self._mem) + getsizeof(self._len) \
                + sizeof(LocationEntry) * self.entry_count + sizeof(IndexEntry) * self.sender_index_size
        size += getsizeof(self._keys) + getsizeof(self._items) + getsizeof(self._proxies)
        size += sum(sizeof(key) for key in self._keys)
        size += sum(sizeof(item) for item in self._items)
        size += sum(sizeof(proxy) for proxy in self._proxies)
        size += sizeof(self._raw_proxies[0]) * self.sender_index_size
        return size

    def __cinit__(self, locations_dict: Dict[int, Dict[int, Sequence[int]]]) -> None:
        self._mem = None
        self._keys = None
        self._items = None
        self._proxies = None
        self._len = 0
        self.entries = NULL
        self.entry_count = 0
        self.sender_index = NULL
        self.sender_index_size = 0
        self._raw_proxies = NULL

    def __init__(self, locations_dict: Dict[int, Dict[int, Sequence[int]]]) -> None:
        self._mem = Pool()
        cdef object key
        self._keys = []
        self._items = []
        self._proxies = []

        # iterate over everything to get all maxima and validate everything
        cdef size_t max_sender = INVALID_SIZE  # keep track of highest used player id for indexing
        cdef size_t sender_count = 0
        cdef size_t count = 0
        for sender, locations in locations_dict.items():
            # we don't require the dict to be sorted here
            if not isinstance(sender, int) or sender < 1 or sender > MAX_PLAYER_ID:
                raise ValueError(f"Invalid player id {sender} for location")
            if max_sender == INVALID_SIZE:
                max_sender = sender
            else:
                max_sender = max(max_sender, sender)
            for location, data in locations.items():
                receiver = data[1]
                if receiver < 1 or receiver > MAX_PLAYER_ID:
                    raise ValueError(f"Invalid player id {receiver} for item")
                count += 1
            sender_count += 1

        if not sender_count:
            raise ValueError(f"Rejecting game with 0 players")

        if sender_count != max_sender:
            # we assume player 0 will never have locations
            raise ValueError("Player IDs not continuous")

        if not count:
            warnings.warn("Game has no locations")

        # allocate the arrays and invalidate index (0xff...)
        self.entries = <LocationEntry*>self._mem.alloc(count, sizeof(LocationEntry))
        self.sender_index = <IndexEntry*>self._mem.alloc(max_sender + 1, sizeof(IndexEntry))
        self._raw_proxies = <PyObject**>self._mem.alloc(max_sender + 1, sizeof(PyObject*))

        # build entries and index
        cdef size_t i = 0
        for sender, locations in sorted(locations_dict.items()):
            self.sender_index[sender].start = i
            self.sender_index[sender].count = 0
            # Sorting locations here makes it possible to write a faster lookup without an additional index.
            for location, data in sorted(locations.items()):
                self.entries[i].sender = sender
                self.entries[i].location = location
                self.entries[i].item = data[0]
                self.entries[i].receiver = data[1]
                if len(data) > 2:
                    self.entries[i].flags = data[2]  # initialized to 0 during alloc
                # Ignoring extra data. warn?
                self.sender_index[sender].count += 1
                i += 1

        # build pyobject caches
        self._proxies.append(None)  # player 0
        assert self.sender_index[0].count == 0
        for i in range(1, max_sender + 1):
            assert self.sender_index[i].count == 0 or (
                    self.sender_index[i].start < count and
                    self.sender_index[i].start + self.sender_index[i].count <= count)
            key = i  # allocate python integer
            proxy = PlayerLocationProxy(self, i)
            self._keys.append(key)
            self._items.append((key, proxy))
            self._proxies.append(proxy)
            self._raw_proxies[i] = <PyObject*>proxy

        self.sender_index_size = max_sender + 1
        self.entry_count = count
        self._len = sender_count

    # fake dict access
    def __len__(self) -> int:
        return self._len

    def __iter__(self) -> Iterator[int]:
        return self._keys.__iter__()

    def __getitem__(self, key: int) -> Any:
        # figure out if player actually exists in the multidata and return a proxy
        cdef size_t i = key  # NOTE: this may raise TypeError
        if i < 1 or i >= self.sender_index_size:
            raise KeyError(key)
        return <object>self._raw_proxies[key]

    T = TypeVar('T')

    def get(self, key: int, default: T) -> Union[PlayerLocationProxy, T]:
        # calling into self.__getitem__ here is slow, but this is not used in MultiServer
        try:
            return self[key]
        except KeyError:
            return default

    def items(self) -> Iterable[Tuple[int, PlayerLocationProxy]]:
        return self._items

    # specialized accessors
    def find_item(self, slots: Set[int], seeked_item_id: int) -> Generator[Tuple[int, int, int, int, int], None, None]:
        cdef ap_id_t item = seeked_item_id
        cdef ap_player_t receiver
        cdef std_set[ap_player_t] receivers
        cdef size_t slot_count = len(slots)
        if slot_count == 1:
            # specialized implementation for single slot
            receiver = list(slots)[0]
            with nogil:
                for entry in self.entries[:self.entry_count]:
                    if entry.item == item and entry.receiver == receiver:
                        with gil:
                            yield entry.sender, entry.location, entry.item, entry.receiver, entry.flags
        elif slot_count:
            # generic implementation with lookup in set
            for receiver in slots:
                receivers.insert(receiver)
            with nogil:
                for entry in self.entries[:self.entry_count]:
                    if entry.item == item and receivers.count(entry.receiver):
                        with gil:
                            yield entry.sender, entry.location, entry.item, entry.receiver, entry.flags

    def get_for_player(self, slot: int) -> Dict[int, Set[int]]:
        cdef ap_player_t receiver = slot
        all_locations: Dict[int, Set[int]] = {}
        with nogil:
            for entry in self.entries[:self.entry_count]:
                if entry.receiver == receiver:
                    with gil:
                        sender: int = entry.sender
                        if sender not in all_locations:
                            all_locations[sender] = set()
                        all_locations[sender].add(entry.location)
        return all_locations

    if TYPE_CHECKING:
        State = Dict[Tuple[int, int], Set[int]]
    else:
        State = Union[Tuple[int, int], Set[int], defaultdict]

    def get_checked(self, state: State, team: int, slot: int) -> List[int]:
        # This used to validate checks actually exist. A remnant from the past.
        # If the order of locations becomes relevant at some point, we could not do sorted(set), so leaving it.
        cdef set checked = state[team, slot]

        if not len(checked):
            # Skips loop if none have been checked.
            # This optimizes the case where everyone connects to a fresh game at the same time.
            return []

        # Unless the set is close to empty, it's cheaper to use the python set directly, so we do that.
        cdef LocationEntry* entry
        cdef ap_player_t sender = slot
        cdef size_t start = self.sender_index[sender].start
        cdef size_t count = self.sender_index[sender].count
        return [entry.location for
                entry in self.entries[start:start+count] if
                entry.location in checked]

    def get_missing(self, state: State, team: int, slot: int) -> List[int]:
        cdef LocationEntry* entry
        cdef ap_player_t sender = slot
        cdef size_t start = self.sender_index[sender].start
        cdef size_t count = self.sender_index[sender].count
        cdef set checked = state[team, slot]
        if not len(checked):
            # Skip `in` if none have been checked.
            # This optimizes the case where everyone connects to a fresh game at the same time.
            return [entry.location for
                    entry in self.entries[start:start + count]]
        else:
            # Unless the set is close to empty, it's cheaper to use the python set directly, so we do that.
            return [entry.location for
                    entry in self.entries[start:start + count] if
                    entry.location not in checked]

    def get_remaining(self, state: State, team: int, slot: int) -> List[int]:
        cdef LocationEntry* entry
        cdef ap_player_t sender = slot
        cdef size_t start = self.sender_index[sender].start
        cdef size_t count = self.sender_index[sender].count
        cdef set checked = state[team, slot]
        return sorted([entry.item for
                       entry in self.entries[start:start+count] if
                       entry.location not in checked])


@cython.internal  # unsafe. disable direct import
cdef class PlayerLocationProxy:
    cdef LocationStore _store
    cdef size_t _player
    cdef object _len

    def __init__(self, store: LocationStore, player: int) -> None:
        self._store = store
        self._player = player
        self._len = self._store.sender_index[self._player].count

    def __len__(self) -> int:
        return self._store.sender_index[self._player].count

    def __iter__(self) -> Generator[int, None, None]:
        cdef LocationEntry* entry
        cdef size_t i
        cdef size_t off = self._store.sender_index[self._player].start
        for i in range(self._store.sender_index[self._player].count):
            entry = self._store.entries + off + i
            yield entry.location

    cdef LocationEntry* _get(self, ap_id_t loc):
        # This requires locations to be sorted.
        # This is always going to be slower than a pure python dict, because constructing the result tuple takes as long
        # as the search in a python dict, which stores a pointer to an existing tuple.
        cdef LocationEntry* entry = NULL
        # binary search
        cdef size_t l = self._store.sender_index[self._player].start
        cdef size_t r = l + self._store.sender_index[self._player].count
        cdef size_t m
        while l < r:
            m = (l + r) // 2
            entry = self._store.entries + m
            if entry.location < loc:
                l = m + 1
            else:
                r = m
        if entry:  # count != 0
            entry = self._store.entries + l
            if entry.location == loc:
                return entry
        return NULL

    def __getitem__(self, key: int) -> Tuple[int, int, int]:
        cdef LocationEntry* entry = self._get(key)
        if entry:
            return entry.item, entry.receiver, entry.flags
        raise KeyError(f"No location {key} for player {self._player}")

    T = TypeVar('T')

    def get(self, key: int, default: T) -> Union[Tuple[int, int, int], T]:
        cdef LocationEntry* entry = self._get(key)
        if entry:
            return entry.item, entry.receiver, entry.flags
        return default

    def items(self) -> Generator[Tuple[int, Tuple[int, int, int]], None, None]:
        cdef LocationEntry* entry
        start = self._store.sender_index[self._player].start
        count = self._store.sender_index[self._player].count
        for entry in self._store.entries[start:start+count]:
            yield entry.location, (entry.item, entry.receiver, entry.flags)
