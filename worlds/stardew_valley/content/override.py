from typing import Any


def override(content: Any, **kwargs) -> Any:
    attributes = dict(content.__dict__)

    # Annotations contain only the fields, not the cached properties
    # So we just pop any field that isn't an annotation, assuming it's something illegal like a cached property
    field_on_class = type(content).__annotations__
    for field in list(attributes.keys()):
        if field not in field_on_class:
            attributes.pop(field)

    attributes.update(kwargs)

    return type(content)(**attributes)
