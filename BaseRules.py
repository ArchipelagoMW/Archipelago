import functools

from typing import Callable, List, Optional

from BaseClasses import CollectionState, Req


TRUE = lambda state: True
FALSE = lambda state: False


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


@functools.cache
def req_to_rule(player: int, req: Optional[Req]) -> Callable[[CollectionState], bool]:
    if not req:
        return TRUE
    return lambda state: state.has(req.item, player, count=req.count)


@functools.cache
def all_reqs_to_rule(player: int, *reqs: Optional[Req]) -> Callable[[CollectionState], bool]:
    rreqs: List[Req] = []
    for req in reqs:
        if req:
            rreqs.append(req)
    if not rreqs:
        return TRUE
    rreqs = tuple(rreqs)
    return lambda state: state.has_all_reqs(rreqs, player)


@functools.cache
def any_req_to_rule(player: int, *reqs: Optional[Req]) -> Callable[[CollectionState], bool]:
    if not reqs:
        return FALSE
    for req in reqs:
        if not req:
            return TRUE
    return lambda state: state.has_any_req(reqs, player)
