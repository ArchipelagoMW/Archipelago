from collections.abc import Hashable

from . import Handler, AbstractHandler
from ...constants import Addresses, Events, EventStatus, Locations, Regions
from ...events import EventHandler, EventData
from ...locations import LocationHandler, Cleared, LocationData
from ...sections import Sections
from .door import Doors


class EventsHandler(AbstractHandler):
    """Handles events management and specific event processes"""

    handlers_by_value: dict[Hashable, Handler]

    _event_states: bytearray = bytearray(0xFF)
    externaly_triggered: list[str] = []

    initialized: bool = False

    async def get_event_states(self) -> bytearray:
        if not self.initialized:
            await self.update_events()

            self.initialized = True

        return self._event_states

    async def start_beginner_dwarf_language(self):
        await self.tomba.events_handler.start(Events.BEGINNERS_DWARF_LANGUAGE)

        # Event giver state to make sure Dwarf Language is correctly started
        await self.tomba.playstation.write_memory(0x09C214, 0x05.to_bytes())

    async def clear_i_cant_swim(self):
        await self.clear(Events.I_CANT_SWIM)

        # Make sure access to river is possible
        await self.tomba.playstation.write_memory(0x09C3E0, 0x04.to_bytes())

    async def clear_save_the_dwarves(self):
        await self.clear(Events.SAVE_THE_DWARVES)

        await self.tomba.playstation.write_memory(0x09C244, 0x01.to_bytes())

    async def handle_value(self, event_name: str, value: int):
        """Handler for specific value of event state"""
        handler = self.handlers_by_value.get(event_name, None)
        if handler:
            await handler.callback(value)

    def init_handlers(self):
        """Keep in mind while writing those rules:
        * Restarting the client means the hanlder can be re-triggered
        So operations like forget/start must be guarded against possible regressions"""
        self.handlers = {
            Events.HIDE_AND_GO_SEEK: Handler(self.on_hide_and_go_seek),
            Events.LOOK_AND_SEE: Handler(self.on_look_and_see),
            Events.WHERED_THE_LIGHTS_GO: Handler(self.on_where_the_lights_go),
            Events.I_WANT_A_SILVER_MEDAL: Handler(self.on_i_want_a_silver_medal),
            Events.THE_HAUNTED_MANSION: Handler(self.on_haunted_mansion),
            Events.LAVA_CAVES: Handler(self.on_lava_caves),
            Events.THE_100_FLOWER_FOREST: Handler(self.on_the_100_flower_forest),
            Events.PHOENIX_MOUNTAIN: Handler(self.on_phoenix_mountain),
            Events.BACCUS_VILLAGE: Handler(self.on_baccus_village),
            Events.THE_DEEP_JUNGLE_PIG: Handler(self.on_deep_jungle_pig),
            Events.TRICK_VILLAGE: Handler(self.on_trick_village),
            Events.BREAK_THE_RUSTY_DOOR: Handler(self.on_break_the_rusty_door),
            Events.WE_NEED_POWER: Handler(self.on_we_need_power),
            Events.A_REAL_EVIL_PIG: Handler(self.on_a_real_evil_pig),
            Events.SOMETHINGS_COOKIN: Handler(self.on_somethings_cookin),
            Events.THE_MERMAIDS_NECKLACE: Handler(self.on_mermaid_necklace),
            Events.CLEAR_THE_FOG: Handler(self.on_clear_the_fog),
        }

        self.handlers_by_value = {
            Events.SAVE_THE_DWARVES: Handler(self.on_save_the_dwarves),
        }

    async def on_save_the_dwarves(self, value: int):
        """Prevents softlock when all dwarves are saved but language is not learned"""
        if value == 0x08:
            await self.tomba.events_handler.clear(Events.BEGINNERS_DWARF_LANGUAGE)

    async def on_clear_the_fog(self):
        """Remove the fog"""
        await self.tomba.playstation.write_memory(0x09BCCE, 0x03.to_bytes())

    async def on_mermaid_necklace(self):
        """Make sure Mighty Fish Food event is not cleared
        Until we actually have picked-it up"""
        if not self.ctx.check_handler.is_checked(Locations.WHATS_UNDERWATER, Regions.HIDING_ROOM):
            await self.tomba.events_handler.forget(Events.MIGHTY_FISH_FOOD)

    async def on_somethings_cookin(self):
        """When this is cleared and the campfire location is not
        We re-start the event in game until the campfire is done"""
        if not self.ctx.check_handler.is_checked(Locations.CAMPFIRE, Regions.FOREST_OF_100_FLOWERS):
            await self.tomba.events_handler.start(Events.SOMETHINGS_COOKIN)

    async def on_a_real_evil_pig(self):
        """Win condition"""
        await self.ctx.on_victory()

    async def on_break_the_rusty_door(self):
        """Uncheck Let's Ride the Raft
        If it's check at this point, the We Need Power event is softlocked"""
        if not await self.get_event_state(Events.WE_NEED_POWER) is EventStatus.CLEARED:
            await self.forget(Events.LETS_RIDE_THE_RAFT)

        await self.clear(Events.I_NEED_A_BOMB)

    async def on_we_need_power(self):
        """Check if the Let's Ride The Raft has been cleared before
        See on_break_the_rusty_door: We reset it there to avoid issue"""
        location = LocationHandler.by_name.get(Cleared(Events.LETS_RIDE_THE_RAFT))
        assert location is not None

        if location.id in self.ctx.sent_checks:
            await self.clear(Events.LETS_RIDE_THE_RAFT)

    async def on_trick_village(self):
        """Clear related events"""
        await self.clear(Events.THE_UNDERWATER_PIG_BAG)

    async def on_deep_jungle_pig(self):
        """Clear related events"""
        await self.clear(Events.THE_JUNGLE_PIG_BAG)

        # The Swimming event is bugged upon clearing the Jungle (Tomba! will learn to swim in the trees...)
        await self.clear(Events.A_REFRESHING_DRINK)
        await self.clear_i_cant_swim()

    async def on_baccus_village(self):
        """Clear related events"""
        await self.clear(Events.THE_MOUSE_PIG_BAG)
        await self.ctx.check_handler.check(Locations.CENTRAL_PARK_CHEST, Regions.CENTRAL_PARK)  # No longer accessible

        # Allow the player to go to Baccus Village
        await self.tomba.doors_handler.open(Doors.BACCUS_DOOR)

    async def on_phoenix_mountain(self):
        """Clear related events"""
        await self.clear(Events.A_STORMY_PIG_BAG)
        await self.clear(Events.TO_PHOENIX_MOUNTAIN)

        # If the player seal the evil pig before going in the mountain for the first time
        if await self.get_event_state(Events.THE_MOUSE_PIG_BAG) is EventStatus.UNDISCOVERED:
            # Prevents softlock if speaking to the Phoenix guy
            await self.start(Events.THE_MOUSE_PIG_BAG)

        # Allow the player to go to Baccus Village
        await self.tomba.doors_handler.open(Doors.BACCUS_DOOR)

    async def on_the_100_flower_forest(self):
        """Clear related events"""
        await self.clear(Events.THE_EVIL_PIG_BAG)

        await self.clear_save_the_dwarves()

        if await self.tomba.events_handler.get_event_state(Events.BEGINNERS_DWARF_LANGUAGE) is EventStatus.UNDISCOVERED:
            await self.start_beginner_dwarf_language()

    async def on_lava_caves(self):
        """Clear related events"""
        await self.clear(Events.THE_FIRE_PIG_BAG)

        await self.ctx.check_handler.check(Locations.CHARLES_PANTS, Regions.LAVA_CAVES)

    async def on_haunted_mansion(self):
        """Clear related events"""
        await self.clear(Events.PAINTING_OF_A_BIG_KEY)
        await self.clear(Events.THE_HAUNTED_PIG_BAG)
        await self.clear(Events.BREAK_THE_MAGIC_EGG)

        await self.ctx.check_handler.check(Locations.PAINTING_OF_A_BIG_KEY, Sections.THIEFS_ROOM_THREE.name)

        await self.tomba.playstation.write_memory(Addresses.MAGIC_EGGS_BROKEN_COUNT, 0xFF.to_bytes())

    async def on_i_want_a_silver_medal(self):
        """Lock the bronze medal out"""
        await self.clear(Events.I_WANT_A_BRONZE_MEDAL)

    async def on_where_the_lights_go(self):
        """This can be cleared without requiring the dwarf to hand the torch, we need to check that manualy"""
        await self.ctx.check_handler.check(Locations.FIRE_STARTER, Regions.DWARF_VILLAGE)

    async def on_hide_and_go_seek(self):
        # Clear Take Out as it becomes softlocked when this one is cleared
        await self.clear(Events.TAKE_OUT)
        await self.ctx.check_handler.check(Locations.FIND_MY_SON, Regions.HIDDEN_VILLAGE)

    async def on_look_and_see(self):
        """When this is cleared prior to grabbing the Telescope, that location becomes unreachable"""
        await self.ctx.check_handler.check(Locations.TELESCOPE, Regions.WATCH_TOWER)

    def get_event(self, event_name: str) -> EventData:
        event = EventHandler.by_name.get(event_name)
        assert event is not None
        return event

    def get_event_location(self, event_name: str) -> LocationData:
        event = LocationHandler.by_name.get(event_name)
        assert event is not None
        return event

    def is_cleared(self, event_name: str) -> bool:
        event = self.get_event_location(Cleared(event_name))
        return event.id in self.ctx.sent_checks

    async def clear(self, event_name: str):
        await self.set_event_state(self.get_event(event_name), EventStatus.CLEARED)

    async def forget(self, event_name: str):
        await self.set_event_state(self.get_event(event_name), EventStatus.UNDISCOVERED)

    async def start(self, event_name: str):
        await self.set_event_state(self.get_event(event_name), EventStatus.STARTED)

    async def get_event_state(self, event_name: str) -> EventStatus:
        event = EventHandler.by_name[event_name]

        try:
            return EventStatus((await self.get_event_states())[event.id])
        except Exception:
            return EventStatus.STARTED

    async def set_event_state(self, event: EventData, status: EventStatus):
        self.externaly_triggered.append(event.name)
        previous_status = await self.get_event_state(event.name)
        await self.tomba.playstation.write_memory(Addresses.EVENT_FLAGS + event.id, status.to_bytes())

        if status != EventStatus.UNDISCOVERED and previous_status != status:
            await self.tomba.show_event(event, status)

    async def update_events(self):
        old_states = self._event_states
        new_states = await self.tomba.playstation.read_memory_block(Addresses.EVENT_FLAGS, 0xFF)

        self._event_states = new_states

        for id in range(len(new_states)):
            if old_states[id] == new_states[id]:
                continue

            event = EventHandler.by_id.get(id, None)
            if event is None:
                continue

            try:
                status = EventStatus(new_states[id])

                if status is not EventStatus.CLEARED:
                    continue

                # Handle Archipelago checks
                await self.ctx.on_event_cleared(event)

                # Trigger rewards
                await self.ctx.check_locations(LocationHandler.by_event.get(event.name, []))

                await self.handle(event.name)
            except ValueError:
                # At least Beginners Dward Language event is expected to have other values as its a multi step event
                pass

            await self.handle_value(event.name, new_states[id])

    def is_externaly_triggered(self, event_name: str):
        return event_name in self.externaly_triggered
