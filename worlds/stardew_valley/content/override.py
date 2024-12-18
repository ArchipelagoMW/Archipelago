from typing import Any


def override(content: Any, **kwargs) -> Any:
    attributes = dict(content.__dict__)
    attributes.update(kwargs)
    return type(content)(**attributes)
