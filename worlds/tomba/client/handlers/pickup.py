from . import Handler, AbstractHandler
from ...constants import Items, Events, Locations, Regions, EventStatus
from ...items import ItemHandler
from .player import XPType


class PickupHandler(AbstractHandler):
    """This class defines additional operations upon receiving a specific item from the multiworld"""

    def init_handlers(self):
        self.handlers = {
            Items.FLOWER_SEEDS: Handler(self.on_flower_seeds),
            Items.SEASHELL_NECKLACE: Handler(self.on_seashell_necklace),
            Items.WEED_KILLER: Handler(self.on_weed_killer),
            Items.YANS_LUNCH_BOX: Handler(self.on_yans_lunch_box),
            Items.GOLD_MEDAL: Handler(self.on_gold_medal),
            Items.SILVER_MEDAL: Handler(self.on_silver_medal),
            Items.BRONZE_MEDAL: Handler(self.on_bronze_medal),
            Items.BANANA_JUICE: Handler(self.on_banana_juice),
            Items.PSYCHIC_FISH: Handler(self.on_psychic_fish),
            Items.RAFT: Handler(self.on_raft),
            Items.BUNK_FLOWER: Handler(self.on_bunk_flower),
            Items.CHICK: Handler(self.on_chick),
            Items.JEWEL_OF_FIRE: Handler(self.on_jewel_of_fire),
            Items.JEWEL_OF_WATER: Handler(self.on_jewel_of_water),
            Items.JEWEL_OF_WIND: Handler(self.on_jewel_of_wind),
            Items.BOMB: Handler(self.on_bomb),
            Items.BUCKET: Handler(self.on_bucket),
        }

    async def on_bucket(self):
        """Make sure it's equipable"""
        if await self.tomba.playstation.read_int(0x09C215) == 0:
            await self.tomba.playstation.write_memory(0x09C215, 0x01.to_bytes())

    async def on_bomb(self):
        """Start break the rusty door if not already started"""
        if await self.tomba.events_handler.get_event_state(Events.BREAK_THE_RUSTY_DOOR) is EventStatus.UNDISCOVERED:
            await self.tomba.events_handler.start(Events.BREAK_THE_RUSTY_DOOR)

    async def on_jewel_of_fire(self):
        """Raise red XP to the max"""
        await self.tomba.player_handler.set_max_xp(XPType.FIRE)

    async def on_jewel_of_water(self):
        """Raise blue XP to the max"""
        await self.tomba.player_handler.set_max_xp(XPType.WATER)

    async def on_jewel_of_wind(self):
        """Raise green XP to the max"""
        await self.tomba.player_handler.set_max_xp(XPType.WIND)

    async def on_chick(self):
        """Player can't have more than 4 Chick at all time to avoid softlock"""
        item = ItemHandler.by_name[Items.CHICK]
        current_amount = await self.tomba.inventory_handler.get_item_amount(item.game_id)
        if current_amount > 4:
            await self.tomba.inventory_handler.set_item_amount(item.game_id, 4)

    async def on_bunk_flower(self):
        """Starts or clear the Phoenix's Favorite"""
        if await self.tomba.events_handler.get_event_state(Events.THE_PHOENIXS_FAVORITE) is EventStatus.UNDISCOVERED:
            await self.tomba.events_handler.start(Events.THE_PHOENIXS_FAVORITE)

        item = ItemHandler.by_name[Items.BUNK_FLOWER]
        if await self.tomba.inventory_handler.get_item_amount(item.game_id) >= 5:
            await self.tomba.events_handler.clear(Events.THE_PHOENIXS_FAVORITE)

    async def on_raft(self):
        """The corresponding location will no longer be accessible"""
        await self.ctx.check_handler.check(Locations.BUILD_A_RAFT, Regions.LUMBERJACK_FACTORY)

    async def on_psychic_fish(self):
        """Clear the 5 Golden Item event which is now softlocked"""
        await self.tomba.events_handler.clear(Events.THE_5_GOLDEN_ITEMS)

    async def on_banana_juice(self):
        """Starts a refreshing drink"""
        if await self.tomba.events_handler.get_event_state(Events.A_REFRESHING_DRINK) is EventStatus.UNDISCOVERED:
            await self.tomba.events_handler.start(Events.A_REFRESHING_DRINK)

        await self.ctx.check_handler.check(Locations.MIXER, Regions.CLOCK_TOWER_ENGINE_ROOM)

    async def on_bronze_medal(self):
        """Clear Bronze Medal event"""
        await self.tomba.events_handler.clear(Events.I_WANT_A_BRONZE_MEDAL)

    async def on_silver_medal(self):
        """Clear Silver Medal event"""
        # This call should naturaly call the handler to provide Bronze Medal location and clear that event too
        # See on_i_want_a_silver_medal in handler/events.py
        await self.tomba.events_handler.clear(Events.I_WANT_A_SILVER_MEDAL)

    async def on_gold_medal(self):
        """Clear Gold Medal event"""
        await self.tomba.events_handler.clear(Events.I_WANT_A_GOLD_MEDAL)

    async def on_yans_lunch_box(self):
        """Start the Take Out event"""
        if await self.tomba.events_handler.get_event_state(Events.TAKE_OUT) is EventStatus.UNDISCOVERED:
            await self.tomba.events_handler.start(Events.TAKE_OUT)

    async def on_flower_seeds(self):
        """The Flower Seeds event must be started to be able to use the seeds"""
        if await self.tomba.events_handler.get_event_state(Events.FLOWER_SEEDS) is EventStatus.UNDISCOVERED:
            await self.tomba.events_handler.start(Events.FLOWER_SEEDS)

    async def on_seashell_necklace(self):
        """Needs the corresponding event to be able to use the necklace"""
        if await self.tomba.events_handler.get_event_state(Events.THE_MERMAIDS_NECKLACE) is EventStatus.UNDISCOVERED:
            await self.tomba.events_handler.start(Events.THE_MERMAIDS_NECKLACE)

    async def on_weed_killer(self):
        """Needs to start the Death Fruit Juice event"""
        if await self.tomba.events_handler.get_event_state(Events.DEATH_FRUIT_JUICE) is EventStatus.UNDISCOVERED:
            await self.tomba.events_handler.start(Events.DEATH_FRUIT_JUICE)

        await self.ctx.check_handler.check(Locations.DEATH_FRUIT_JUICE_STARTED, Regions.BACCUS_VILLAGE)
