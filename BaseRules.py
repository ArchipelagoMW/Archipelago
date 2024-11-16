import functools

from typing import Callable, List, Optional, Tuple, Union

from BaseClasses import CollectionState, Req


TRUE = lambda state: True
FALSE = lambda state: False

class AnyReq(Tuple):
    """A collection of Reqs, AnyReqs, and AllReqs, which evaluates as True if any of them evaluates True.
    
    Also evaluates to True if any entry is None.
    """
    def __repr__(self):
        return f"AnyReq{super().__repr__()}"
    __str__ = __repr__


class AllReq(Tuple):
    """A collection of Reqs, AnyReqs, and AllReqs, which evaluate as True if all of them evaluate True.
    
    Any entries that are None are implicitly evaluated as True.
    """
    def __repr__(self):
        return f"AllReq{super().__repr__()}"
    __str__ = __repr__


def meets_req(state: CollectionState, player: int, req: Optional[Req]) -> bool:
    """Returns whether the player meets the requirements in the given state.
    
    If req is empty (`None`), the requirement is considered met (i.e. True).
    """
    if not req:
        return True
    return state.has(req.item, player, count=req.count)


def meets_all_reqs(state: CollectionState, player: int, *reqs: Optional[Req]) -> bool:
    """Returns whether the player meets all the requirements in the given state.
    
    If a req is empty (`None`), that requirement is considered met (i.e. True).
    If no reqs are provided, the overall requirement **has** been met.
    """
    for req in reqs:
        if req and not state.has(req.item, player, count=req.count):
            return False
    return True


def meets_any_req(state: CollectionState, player: int, *reqs: Optional[Req]) -> bool:
    """Returns whether the player meets all the requirements in the given state.
    
    If a req is empty (`None`), that requirement is considered met, which makes
    this function return True.
    If no reqs are provided, the overall requirement **has not** been met.
    """
    for req in reqs:
        if not req or state.has(req.item, player, count=req.count):
            return True
    return False


@functools.lru_cache(maxsize=None)
def req_to_rule(player: int, req: Optional[Req]) -> Callable[[CollectionState], bool]:
    if not req:
        return TRUE
    return lambda state: state.has(req.item, player, count=req.count)


@functools.lru_cache(maxsize=None)
def all_reqs_to_rule(player: int, *reqs: Optional[Req]) -> Callable[[CollectionState], bool]:
    rreqs: List[Req] = []
    for req in reqs:
        if req:
            rreqs.append(req)
    if not rreqs:
        return TRUE
    rreqs = tuple(rreqs)
    return lambda state: state.has_all_reqs(rreqs, player)


@functools.lru_cache(maxsize=None)
def any_req_to_rule(player: int, *reqs: Optional[Req]) -> Callable[[CollectionState], bool]:
    if not reqs:
        return FALSE
    for req in reqs:
        if not req:
            return TRUE
    return lambda state: state.has_any_req(reqs, player)


@functools.lru_cache(maxsize=None)
def complex_reqs_to_rule(player: int, req: Union[AnyReq, AllReq]) -> Callable[[CollectionState], bool]:
    bare_reqs = []
    nested_reqs = []
    is_any = isinstance(req, AnyReq)
    for inner in req:
        if inner is None:
            if is_any:
                return TRUE
            continue
        if isinstance(inner, Req):
            bare_reqs.append(inner)
        else:
            nested_reqs.append(inner)

    rules = [complex_reqs_to_rule(player, nested) for nested in nested_reqs]
    if is_any:
        if bare_reqs:
            rules.append(any_req_to_rule(player, *bare_reqs))

        def full_rule(state: CollectionState) -> bool:
            for rule in rules:
                if rule(state):
                    return True
            return False
        return full_rule
    else:
        if bare_reqs:
            rules.append(all_reqs_to_rule(player, *bare_reqs))
        
        rules = [r for r in rules if r != TRUE]
        if not rules:
            return TRUE

        def full_rule(state: CollectionState) -> bool:
            for rule in rules:
                if not rule(state):
                    return False
            return True
        return full_rule
