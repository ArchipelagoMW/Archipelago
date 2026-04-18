import inspect
from abc import ABC
from collections.abc import Mapping
from typing import TYPE_CHECKING, Protocol

from ...data.game_item import Source, Requirement

if TYPE_CHECKING:
    from ... import StardewContent


class DisableSourceHook(Protocol):
    def __call__(self, source: Source, /, *, content: "StardewContent") -> bool:
        """Return True if the source should be disabled by this feature."""
        ...


class DisableRequirementHook(Protocol):
    def __call__(self, requirement: Requirement, /, *, content: "StardewContent") -> bool:
        """Return True if the requirement should be disabled by this feature."""
        ...


def wrap_optional_content_arg(hook):
    """Wraps a hook to ensure it has the correct signature."""
    if "content" in hook.__annotations__:
        return hook

    def wrapper(*args, content: "StardewContent", **kwargs):
        return hook(*args, **kwargs)

    return wrapper


class FeatureBase(ABC):

    @property
    def disable_source_hooks(self) -> Mapping[type[Source], DisableSourceHook]:
        """All hooks to call when a source is created to check if it has to be disabled by this feature."""
        disable_source_hooks = {}
        for attribute_name in dir(self):
            if not attribute_name.startswith("_disable_") or not callable((attribute := getattr(self, attribute_name))):
                continue

            sig = inspect.signature(attribute)

            source_param = sig.parameters.get("source")
            if source_param is not None:
                source_type = source_param.annotation
                disable_source_hooks[source_type] = wrap_optional_content_arg(attribute)
                continue

        return disable_source_hooks

    @property
    def disable_requirement_hooks(self) -> Mapping[type[Requirement], DisableRequirementHook]:
        """All hooks to call when a requirement is created to check if it has to be disabled by this feature."""
        disable_requirement_hooks = {}
        for attribute_name in dir(self):
            if not attribute_name.startswith("_disable_") or not callable((attribute := getattr(self, attribute_name))):
                continue

            sig = inspect.signature(attribute)

            requirement_param = sig.parameters.get("requirement")
            if requirement_param is not None:
                requirement_type = requirement_param.annotation
                disable_requirement_hooks[requirement_type] = wrap_optional_content_arg(attribute)
                continue

        return disable_requirement_hooks
