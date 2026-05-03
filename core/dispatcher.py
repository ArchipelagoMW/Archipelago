from __future__ import annotations

from typing import Any, Awaitable, Callable, Generic, TypeVar, cast

from .events import EventBus
from .jobs import JobManager
from .requests import BasicError, Request
from .result import Err, Result


TEvent = TypeVar("TEvent")
T = TypeVar("T")
E = TypeVar("E")
Handler = Callable[[Request[Any, Any]], Awaitable[Result[Any, Any]]]


class Dispatcher(Generic[TEvent]):
    """Route typed requests through registered async handlers.

    Example::

        dispatcher = create_dispatcher(create_bus(dict))
        dispatcher.register(MyRequest, handle_my_request)
        result = await dispatcher.handle(MyRequest())
    """

    def __init__(self, bus: EventBus[TEvent], jobs: JobManager[TEvent]) -> None:
        self.bus = bus
        self.jobs = jobs
        self._handlers: dict[type[Request[Any, Any]], Handler] = {}

    def register(self, request_type: type[Request[Any, Any]], handler: Handler) -> None:
        """Register the async handler for `request_type`.

        Example::

            dispatcher.register(GetSupportedGames, handle_supported_games)
        """

        self._handlers[request_type] = handler

    def unregister(self, request_type: type[Request[Any, Any]]) -> None:
        """Remove a handler registration if one exists."""

        self._handlers.pop(request_type, None)

    async def handle(self, request: Request[T, E]) -> Result[T, E]:
        """Dispatch a request to the registered handler for its type."""

        handler = self._resolve_handler(type(request))
        if handler is None:
            return cast(Result[T, E], Err(BasicError(f"Unsupported request type: {type(request).__name__}")))
        return cast(Result[T, E], await handler(request))

    def _resolve_handler(self, request_type: type[Request[Any, Any]]) -> Handler | None:
        """Resolve a handler by exact request type, then by base class."""

        handler = self._handlers.get(request_type)
        if handler is not None:
            return handler
        for base_type in request_type.__mro__[1:]:
            if base_type in self._handlers:
                return self._handlers[base_type]
        return None


def create_dispatcher(bus: EventBus[TEvent], jobs: JobManager[TEvent] | None = None) -> Dispatcher[TEvent]:
    """Create a dispatcher with a provided or fresh in-memory job manager.

    Example::

        dispatcher = create_dispatcher(create_bus(dict))
    """

    return Dispatcher(bus=bus, jobs=jobs or JobManager(bus))
