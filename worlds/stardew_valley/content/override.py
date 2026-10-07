from typing import TypeVar

T = TypeVar("T")

def override(content: T, **kwargs) -> T:
    attributes = dict(content.__dict__)

    # Annotations contain only the fields, not the cached properties
    # So we just pop any field that isn't an annotation, assuming it's something illegal like a cached property
    # We also have to grab the parent types from their annotations, if applicable, so things like `other_requirements` get brought along
    # We do this through __mro__ because it gives the whole tree, instead of just the immediate parents
    content_type = type(content)
    type_hierarchy = content_type.__mro__
    annotations_on_class = set()
    for base_type in type_hierarchy:
        base_annotations = getattr(base_type, "__annotations__", {})
        annotations_on_class.update(base_annotations)
    for field in list(attributes.keys()):
        if field not in annotations_on_class:
            attributes.pop(field)

    attributes.update(kwargs)

    return type(content)(**attributes)
