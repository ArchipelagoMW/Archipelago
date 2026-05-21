from __future__ import annotations

from collections import Counter, defaultdict
from collections.abc import Generator
from typing import ClassVar

from BaseClasses import CollectionState

from ..charms import charm_name_to_id, charm_names


attribute_list = []
"""list of tuple(term, number of bits used)"""

bit_length_prefix_sums = [0]
"""Lookup for the start bit for any given field by attribute id"""

attribute_ids = {}
"""Lookup for the attribute id for any given term"""

top_bits_mask = 0
"""
Bit Mask for the int state of just the empty bits above the sections reserved for data,
for comparing states to each other while catching overflows
"""

end_mask: int
"""
Bit Mask for the int state of every relevant bit set,
for comparing states to each other while catching overflows
"""

# Calculate the necessary attributes
# TODO: move this initialization into a function and differ so connections could add terms
for charm in charm_names:
    charm_name = "_".join(charm.split(" "))
    attribute_list.append((f"CHARM{charm_name_to_id[charm_name] + 1}", 1))
    attribute_list.append((f"noCHARM{charm_name_to_id[charm_name] + 1}", 1))
attribute_list += [
    ("BROKEHEART", 1),
    ("BROKEGREED", 1),
    ("BROKESTRENGTH", 1),
    ("NOFLOWER", 1),
    ("NOPASSEDCHARMEQUIP", 1),
    ("OVERCHARMED", 1),
    ("CANNOTOVERCHARM", 1),
    ("USEDSHADE", 1),
    ("CANNOTSHADESKIP", 1),
    ("SPENTALLSOUL", 1),
    ("CANNOTREGAINSOUL", 1),
    ("USEDNOTCHES", 5),
    ("MAXNOTCHCOST", 5),
    ("REQUIREDMAXSOUL", 7),
    ("SOULLIMITER", 7),
    ("SPENTSOUL", 7),
    ("SPENTRESERVESOUL", 8),
    ("SPENTHP", 7),
    ("SPENTBLUEHP", 7),
    ("LAZYSPENTHP", 7)
]
for i in range(len(attribute_list)):
    top_bits_mask += 1 << (bit_length_prefix_sums[-1] + attribute_list[i][1])
    bit_length_prefix_sums.append(bit_length_prefix_sums[-1] + attribute_list[i][1] + 1)
    attribute_ids[attribute_list[i][0]] = i

end_mask = (1 << bit_length_prefix_sums[-1]) - 1


def rs_add_value(cur_state: int, attr: str, value: int) -> int:
    """Adds approprate value to the int state by name"""
    attr_id = attribute_ids[attr]
    return cur_state + (value << bit_length_prefix_sums[attr_id])


def rs_get_value(cur_state: int, attr: str) -> int:
    """Gets approprate value from the int state by name"""
    attr_id = attribute_ids[attr]
    attr_len = attribute_list[attr_id][1]
    return (cur_state >> bit_length_prefix_sums[attr_id]) & ((1 << attr_len) - 1)


def rs_set_value(cur_state: int, attr: str, value: int) -> int:
    """Sets approprate value to the int state by name"""
    attr_id = attribute_ids[attr]
    attr_len = attribute_list[attr_id][1]
    start_pos = bit_length_prefix_sums[attr_id]
    cur_value = (cur_state >> start_pos) & ((1 << attr_len) - 1)
    return cur_state + ((value - cur_value) << start_pos)


def rs_increase_if_lower(cur_state: int, attr: str, value: int) -> int:
    """Sets appropriate value to the int state by name only if the existing value is lower than the incoming value"""
    attr_id = attribute_ids[attr]
    attr_len = attribute_list[attr_id][1]
    pos = bit_length_prefix_sums[attr_id]
    cur_value = (cur_state >> pos) & ((1 << attr_len) - 1)
    if cur_value < value:
        return cur_state + ((value - cur_value) << pos)
    else:  # noqa: RET505
        return cur_state


def rs_subtract_at_most(cur_state: int, attr: str, value: int) -> int:
    """Subtracts approprate value from the int state by name only if the result would not go negative"""
    attr_id = attribute_ids[attr]
    attr_len = attribute_list[attr_id][1]
    pos = bit_length_prefix_sums[attr_id]
    cur_value = (cur_state >> pos) & ((1 << attr_len) - 1)
    return cur_state - (min(cur_value, value) << pos)


def rs_leq(state1: int, state2: int) -> bool:
    """Return if state1 is less than or equal to state2"""
    return ((state1 + end_mask - state2) & top_bits_mask) == top_bits_mask


def dict_to_rs(inp: dict[str, int]) -> int:
    """Helper function to convert from a dict of term: value to an int state"""
    res = 0
    for k, v in inp.items():
        res = rs_add_value(res, k, v)
    return res


def rs_to_dict(inp: int) -> dict[str, int]:
    """Helper function to convert from an int state to a dict of term: value"""
    res = {}
    for index in range(len(attribute_list)):
        cur_key = attribute_list[index][0]
        cur_value = rs_get_value(inp, cur_key)
        if cur_value:
            res[cur_key] = cur_value
    return res


# For ease of typing in submodules
cs = CollectionState
rs = int


class ResourceStateHandler(type):
    handlers: ClassVar[list[RCStateVariable]] = []
    _handler_cache: ClassVar[dict[int, dict[str, RCStateVariable]]] = defaultdict(dict)
    # TODO: check if this cache could crash and burn if it is reused for other multiworlds

    def __new__(mcs, name, bases, dct):
        new_class = super().__new__(mcs, name, bases, dct)
        ResourceStateHandler.handlers.append(new_class)
        return new_class

    @staticmethod
    def get_handler(req: str, player: int) -> RCStateVariable:
        ret = None
        if req in ResourceStateHandler._handler_cache[player]:
            return ResourceStateHandler._handler_cache[player][req]

        for handler in ResourceStateHandler.handlers:
            if handler.try_match(req):
                ret = handler(req, player)
                continue
        assert ret, f"searched for a handler for req {req} and did not find one"
        ResourceStateHandler._handler_cache[player][req] = ret
        return ret


class RCStateVariable(metaclass=ResourceStateHandler):
    prefix: str
    player: int
    term_name: str

    def __init__(self, term: str, player: int):
        assert term.startswith(self.prefix)
        self.player = player
        self.term_name = term
        # expecting "prefix" or "prefix[one,two,three]"
        if term != self.prefix:
            params = term[len(self.prefix)+1:-1].split(",")
            self.parse_term(*params)
        else:
            self.parse_term()

    def parse_term(self, *args) -> None:
        """Subclasses should use this to expect parameter counts for init"""
        pass

    @classmethod
    def try_match(cls, term: str) -> bool:
        """Returns True if this class can handle the passed in term"""
        return False

    @property
    def terms(self) -> list[str]:
        raise NotImplementedError

    def modify_state(self, state_blob: rs, item_state: cs) -> Generator[rs]:
        valid, output_state = self._modify_state(state_blob, item_state)
        if valid:
            yield output_state

    def _modify_state(self, state_blob: rs, item_state: cs) -> tuple[bool, rs]:
        raise NotImplementedError

    def can_exclude(self, options) -> bool:
        return True

    def add_simple_item_reqs(self, items: Counter) -> None:
        pass


from .cast_spell import *  # noqa: E402, F403
from .direct_compare import *  # noqa: E402, F403
from .equip_charm import *  # noqa: E402, F403
from .flower_provider import *  # noqa: E402, F403
from .lifeblood_count import *  # noqa: E402, F403
from .regain_soul import *  # noqa: E402, F403
from .resetter import *  # noqa: E402, F403
from .shade_state import *  # noqa: E402, F403
from .spend_soul import *  # noqa: E402, F403
from .stag_state import *  # noqa: E402, F403
from .take_damage import *  # noqa: E402, F403
from .warp_to import *  # noqa: E402, F403
