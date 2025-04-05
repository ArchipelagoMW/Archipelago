import pkgutil
from typing import Any, Callable, Optional, TypeVar

T = TypeVar('T')

def str_from_yaml(yaml: Any) -> str:
    assert isinstance(yaml, str);
    return yaml

def int_from_yaml(yaml: Any) -> int:
    assert isinstance(yaml, int);
    return yaml

def list_from_yaml(yaml: Any, f: Callable[[Any], T]) -> list[T]:
    assert isinstance(yaml, list)
    return list(map(f, yaml))

def from_yaml_or(yaml: Any, f: Callable[[Any], T], default: T) -> T:
    if yaml is None:
        return default

    return f(yaml)

def get_data_file_bytes(name: str) -> bytes:
    return pkgutil.get_data(__name__, f"{name}")
