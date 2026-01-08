from typing import Optional, Union


Hint = tuple[str, bytes]
""" (location_name, key_of_hint_data) """


def to_jsonable(hint: Optional[Hint]) -> Optional[list[Union[str, list[int]]]]:
    if not hint:
        return None
    return [hint[0], list(hint[1])]


def from_jsonable(hint: Optional[list[Union[str, list[int]]]]) -> Optional[Hint]:
    if not hint:
        return None
    loc_name, key = hint
    assert isinstance(loc_name, str)
    assert isinstance(key, list)
    return (loc_name, bytes(key))
