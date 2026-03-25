import asyncio
import sys
from argparse import Namespace
from enum import Enum
from typing import TYPE_CHECKING, Any

from CommonClient import logger, server_loop
from NetUtils import ClientStatus

from ..Game.events import LocationClearedEvent, VictoryEvent


if TYPE_CHECKING:
    import kvui

class ConnectionStatus(Enum):
    NOT_CONNECTED = 0
    SCOUTS_NOT_SENT = 1
    SCOUTS_SENT = 2
    GAME_RUNNING = 3

class Nothing_Archipelago_Context():
    game = "nothing_archipelago"
    items_handling = 0b111

    client_loop: asyncio.Task[None]

    last_connected_slot: int | None = None

    slot_data: dict[str, Any]
    goal: int = 1800
    shop_upgrades: bool = True
    shop_colors: bool = True
    shop_music: bool = True
    shop_sounds: bool = True
    gift_coins: bool = True
    milestone_interval: int = 120
    timecap_interval: int = 120
    Starting_coin_count: int = 10
    Death_link: bool = False
    Death_link_mercy: int =100
    Time_dilation: int = 1

    connection_status: ConnectionStatus = ConnectionStatus.NOT_CONNECTED

    highest_processed_item_index: int = 0
    queued_locations: list[int]

    def __init__(self) -> None:
        
        
        self._condition = asyncio.Condition()
        self.queued_locations = []
        self.slot_data = {}
        

    async def server_auth(self, password_requested: bool = False) -> None:
        if password_requested and not self.password:
            
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect(game=self.game)

    def handle_connection_loss(self, msg: str) -> None:
        super().handle_connection_loss(msg)

    async def connect(self, address: str | None = None) -> None:
        #self.ui.switch_to_regular_tab()
        await super().connect(address)

    async def nothing_archipelago_loop(self) -> None:
        while not self.exit_event.is_set():
            
            
            if not self.nothing_archipelago_game:
                await asyncio.sleep(0.1)
                continue


            try:
                while self.queued_locations:
                    location = self.queued_locations.pop(0)
                    self.locations_checked.add(location)
                    await self.check_locations({location})

                new_items = self.items_recieved[self.highest_processed_item_index :]
                if new_items:
                    for _ in new_items:
                        self.highest_processed_item_index += 1
                    self.nothing.update_items(self.items_recieved)

                if self.checked_locations > self.locations_checked:
                    self.nothing.verifylocations(self.checked_locations)

                if self.nothing.data.goalled and not self.finished_game:
                    await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    self.finished_game = True
            except Exception as e:
                logger.exception(e)

            await asyncio.sleep(0.1)

    def on_package(self, cmd: str, args: dict[str, Any]) -> None:
        if cmd == "ConnectionRefused":
            #idk
            test = 1

        if cmd == "Connected":
            if self.connection_status == ConnectionStatus.GAME_RUNNING:
                # In a connection loss -> auto reconnect scenario, we can seamlessly keep going
                return

            self.last_connected_slot = self.slot

            self.connection_status = ConnectionStatus.NOT_CONNECTED  # for safety, it will get set again later

            self.slot_data = args["slot_data"] 
            self.goal = self.slot_data["goal"]
            self.shop_upgrades = self.slot_data["shop_upgrades"]
            self.shop_colors = self.slot_data["shop_colors"]
            self.shop_music = self.slot_data["shop_music"]
            self.shop_sounds = self.slot_data["shop_sounds"]
            self.gift_coins = self.slot_data["gift_coins"]
            self.milestone_interval = self.slot_data["milestone_interval"]
            self.timecap_interval = self.slot_data["timecap_interval"]
            self.Starting_coin_count = self.slot_data["Starting_coin_count"]
            self.Death_link = self.slot_data["Death_link"]
            self.Death_link_mercy = self.slot_data["Death_link_mercy"]
            self.Time_dilation = self.slot_data["Time_dilation"]

            self.nothing_archipelago_game.update_settings(self.goal, self.shop_upgrades, self.shop_colors, self.shop_music, self.shop_sounds,
                                      self.gift_coins, self.milestone_interval, self.timecap_interval, self.Starting_coin_count,
                                      self.Death_link, self.Death_link_mercy, self.Time_dilation)
            self.highest_processed_item_index = 0

    async def disconnect(self, *args: Any, **kwargs: Any) -> None:
        self.finished_game = False
        self.locations_checked = set()
        self.connection_status = ConnectionStatus.NOT_CONNECTED
        await super().disconnect(*args, **kwargs)

    def render(self) -> None:
        if self.nothing is None:
            raise RuntimeError("Tried to render before self.ap_quest_game was initialized.")

        self.nothing.run()
        self.handle_game_events()

    def handle_game_events(self) -> None:
        if self.nothing is None:
            return

        while self.nothing.data.queued_events:
            event = self.nothing.queued_events.pop(0)

            if isinstance(event, LocationClearedEvent):
                self.queued_locations.append(event.location_id)
                continue

            if isinstance(event, VictoryEvent):
                continue

    def trigger_server(server_address, password):
        super().__init__(server_address, password)

class StateManager:
    def __init__(self):
        self._condition = asyncio.Condition()

    async def wait_until_equals(self,ctx, expected_value):
        async with self._condition:
            # wait() releases the lock, pauses the task until notified, 
            # re-acquires the lock upon awakening, and then checks the predicate.
            await self._condition.wait_for(lambda: ctx.nothing.data.archipelagoactive == expected_value)



async def main(data) -> None:
    _condition = asyncio.Condition()
    ctx = Nothing_Archipelago_Context()

    async with _condition:        
        await _condition.wait_for(lambda: data.archipelagoactive == True)
        ctx.trigger_server(data.inputs[0]+":"+data.inputs[1],data.inputs[3])
        ctx.auth = ctx.nothing.data.inputs[2]
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")


        ctx.client_loop = asyncio.create_task(ctx.nothing_archipelago_loop(), name="Client Loop")

    await ctx.exit_event.wait()
    await ctx.shutdown()


def launch() -> None:
    from .launch import launch_nothing_archipelago

    launch_nothing_archipelago()


if __name__ == "__main__":
    launch()