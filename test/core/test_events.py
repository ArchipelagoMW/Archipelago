from __future__ import annotations

import asyncio
import unittest

from core import Event, create_bus


class TestEventBus(unittest.IsolatedAsyncioTestCase):
    async def test_publish_subscribe_fanout(self) -> None:
        bus = create_bus(dict)
        first = bus.subscribe()
        second = bus.subscribe()

        try:
            await bus.publish(Event(name="update", data={"step": 1}))
            event_one = await anext(first)
            event_two = await anext(second)
        finally:
            await first.aclose()
            await second.aclose()

        self.assertEqual("update", event_one.name)
        self.assertEqual({"step": 1}, event_one.data)
        self.assertEqual({"step": 1}, event_two.data)

    async def test_subscriber_cleanup_keeps_bus_usable(self) -> None:
        bus = create_bus(dict)
        subscriber = bus.subscribe()
        await subscriber.aclose()

        survivor = bus.subscribe()
        try:
            await bus.publish(Event(name="update", data={"step": 2}))
            event = await asyncio.wait_for(anext(survivor), timeout=1.0)
        finally:
            await survivor.aclose()

        self.assertEqual({"step": 2}, event.data)

    async def test_type_enforcement(self) -> None:
        bus = create_bus(dict)
        with self.assertRaises(TypeError):
            await bus.publish(Event(name="invalid", data="wrong"))  # type: ignore[arg-type]
