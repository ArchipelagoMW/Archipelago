from __future__ import annotations

import asyncio
from contextlib import suppress
from dataclasses import dataclass
from typing import AsyncIterator, Generic, TypeVar


TEvent = TypeVar("TEvent")


@dataclass(slots=True)
class Event(Generic[TEvent]):
    """Named event payload emitted over the core bus."""

    name: str
    data: TEvent


class EventBus(Generic[TEvent]):
    """In-memory pub/sub bus for adapter-facing core events.

    Example::

        bus = create_bus(dict)
        subscriber = bus.subscribe()
        await bus.publish(Event(name="progress", data={"value": 0.5}))
        event = await anext(subscriber)
    """

    def __init__(self, shape: type[TEvent]) -> None:
        self._shape = shape
        self._subscribers: list[asyncio.Queue[Event[TEvent]]] = []

    async def publish(self, event: Event[TEvent]) -> None:
        """Publish an event to all active subscribers.

        Example::

            await bus.publish(Event(name="status", data={"running": True}))
        """

        if not isinstance(event.data, self._shape):
            raise TypeError(f"Expected event payload of type {self._shape.__name__}, got {type(event.data).__name__}")
        for subscriber in list(self._subscribers):
            await subscriber.put(event)

    def subscribe(self) -> AsyncIterator[Event[TEvent]]:
        """Create an async iterator for future events on this bus.

        Example::

            subscriber = bus.subscribe()
            event = await anext(subscriber)
            await subscriber.aclose()
        """

        queue: asyncio.Queue[Event[TEvent]] = asyncio.Queue()
        self._subscribers.append(queue)

        async def iterator() -> AsyncIterator[Event[TEvent]]:
            try:
                while True:
                    yield await queue.get()
            finally:
                with suppress(ValueError):
                    self._subscribers.remove(queue)

        return iterator()


def create_bus(shape: type[TEvent]) -> EventBus[TEvent]:
    """Create a bus that accepts a single event payload shape.

    Example::

        bus = create_bus(dict)
        await bus.publish(Event(name="ready", data={"ok": True}))
    """

    return EventBus(shape)
