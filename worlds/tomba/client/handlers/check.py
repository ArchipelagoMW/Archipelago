from collections.abc import Hashable

from . import Handler, AbstractHandler
from ...constants import Locations, Regions, Events
from ...locations import LocationHandler, get_name, LocationData
from ...bitutils import Bitmask


class CheckHandler(AbstractHandler):
    """Handles location checks"""

    ram_update_handlers: dict[Hashable, Handler]

    def is_checked(self, location_name: str, region_name: str):
        """Indicate if the given location has been checked already or not"""
        location = self.get_location(location_name, region_name)
        return location.id in self.ctx.sent_checks

    async def _check(self, location: LocationData):
        await self.ctx.check_locations([location.id])

        if location.at is not None:
            await self.tomba.playstation.set_flag(location.at.address, location.at.mask)

    async def check(self, location_name: str, region_name: str):
        location = self.get_location(location_name, region_name)
        await self._check(location)

    def get_location(self, location_name: str, region_name: str) -> LocationData:
        location = LocationHandler.by_name.get(get_name(location_name, region_name), None)
        assert location is not None
        return location

    async def update_locations(self):
        """Process all locations and reset game objects if needed"""
        if not await self.tomba.has_game_in_progress():
            return

        psx = self.tomba.playstation

        # Cache the states region
        await psx.create_cache(0x09BCEC, 0x700)

        # Check locations that were checked in game
        for location in LocationHandler.with_bitmask:
            assert location.at is not None

            if location.id in self.ctx.missing_locations:
                if await psx.get_flag(location.at.address, location.at.mask):
                    await self._check(location)

        # Check location with triggers
        for location in LocationHandler.with_trigger:
            assert location.trigger is not None

            value = await psx.read_int(location.trigger.address)
            if location.trigger.is_triggered(value):
                await self._check(location)

        # Check direct memory readings
        for bitmask, handler in self.ram_update_handlers.items():
            if not isinstance(bitmask, Bitmask):
                continue

            if await psx.get_flag(bitmask.address, bitmask.mask):
                await handler.callback()

        # Remove all cache left
        psx.destroy_cache()

    def init_handlers(self):
        self.handlers = {
            get_name(Locations.GOLDEN_FRUIT, Regions.BACCUS_VILLAGE): Handler(self.on_golden_fruit),
            get_name(Locations.CAMPFIRE, Regions.FOREST_OF_100_FLOWERS): Handler(self.on_campfire),
            get_name(Locations.CAMPFIRE, Regions.FOREST_OF_100_FLOWERS): Handler(self.on_campfire),
        }

        self.ram_update_handlers = {Bitmask(0x09C1BD, 0xFF): Handler(self.on_campfire_extinguished)}

    async def on_campfire_extinguished(self):
        """This happens when the player use the bucket of water on top of the campfire
        or pickup the cooked Yam after extinguishing the campfire
        In that case, the bucket can no longer be equipped and hence, the bucket of water location
        must be checked to prevent softlocking that location"""
        await self.check(Locations.FILL_THE_BUCKET, Regions.WATCH_TOWER)

    async def on_campfire(self):
        """When this is checked, check if the Something Cookin event should be cleared too
        This can happen when the player clears that event before this campfire location
        We disable the event clear in order to leave the campfire accessible"""
        if self.tomba.events_handler.is_cleared(Events.SOMETHINGS_COOKIN):
            await self.tomba.events_handler.clear(Events.SOMETHINGS_COOKIN)

    async def on_golden_fruit(self):
        """Trigger locations from Some Cheese Please"""
        await self.check(Locations.SOME_CHEESE_PLEASE_1, Regions.BACCUS_VILLAGE)
        await self.check(Locations.SOME_CHEESE_PLEASE_2, Regions.BACCUS_VILLAGE)
