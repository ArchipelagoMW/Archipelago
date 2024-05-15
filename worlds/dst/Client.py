from typing import Dict, List
import urllib.parse
import logging
import asyncio
import json
import time
import socket
import random
from NetUtils import ClientStatus
from CommonClient import CommonContext, get_base_parser
from Utils import async_start
ITEM_ID_OFFSET:int = 264000
LOCATION_RESEARCH_RANGE = {"start": 264501, "end": 264900}
CLIENT_VERSION = "1.1.1"

class DSTTimeoutError(Exception):
    pass

class DSTContext(CommonContext):
    game = "Don't Starve Together"
    items_handling = 0b111
    want_slot_data = True
    logger = logging.getLogger("DSTInterface")
    slotdata = dict()
    resync_items = False
    lockable_items = set()
    dst_handler = None
    connected_to_ap = False
    _eventqueue:List[Dict] = []

    def __init__(self, server_address, password):
        self.dst_handler = DSTHandler(self)
        super().__init__(server_address, password)

    def on_deathlink(self, data:Dict):
        self.dst_handler.enqueue({
            "datatype": "Death",
            "msg": data.get("cause")
        })

    def run_gui(self):
        from kvui import GameManager

        class DSTManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago"),
                ("DSTInterface", "Don't Starve Together"),
            ]
            base_title = "Archipelago Don't Starve Together Client"

        self.ui = DSTManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")
        async_start(self.handle_eventqueue())

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(DSTContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_dst_connect_to_ap(self):
        "When the client connects to both DST and AP"
        self.dst_handler.enqueue({
            "datatype": "State",
            "connected": True,
            "clientversion": CLIENT_VERSION,
            "generatorversion": self.slotdata.get("generator_version"),
            "seed_name": self.seed_name,
            "slot": self.slot,
            "slot_name": self.player_names[self.slot],
            "goal": self.slotdata.get("goal"),
            "days_to_survive": self.slotdata.get("days_to_survive"),
            "required_bosses": self.slotdata.get("required_bosses"), # Legacy
            "goal_locations": self.slotdata.get("goal_locations"),
            "craft_with_locked_items": self.slotdata.get("craft_with_locked_items", True),
            "finished_game": self.finished_game,
        })
        
        self.dst_handler.enqueue({
            "datatype": "Locations",
            "resync": True,
            "missing_locations": list(self.missing_locations),
            "checked_locations": list(self.checked_locations),
        })

        self.resync_items = True # Expecting ReceivedItems package, either following Connect or Sync package
        # Send locked items
        lockable_items = self.slotdata.get("locked_items_local_id")
        if lockable_items:
            self.dst_handler.enqueue({
                "datatype": "Items",
                "locked_items_local_id": lockable_items,
            })
            print(f"DST: Locking {len(lockable_items)} items!")

        # Scout research locations
        async_start(self.send_msgs([{
            "cmd": "LocationScouts",
            "locations": set([id for id in self.missing_locations if (id >= LOCATION_RESEARCH_RANGE["start"] and id <= LOCATION_RESEARCH_RANGE["end"])]),
        }]))

    def send_hints_to_dst(self):
        for hint in self.stored_data.get(f"_read_hints_{self.team}_{self.slot}", []):
            if hint["found"]: 
                continue
            self.dst_handler.enqueue({
                "datatype": "HintInfo",
                "item": hint["item"],
                "locationname": self.location_names[hint["location"]],
                "findingname": self.player_names[hint["finding_player"]],
            }, False)

    def on_dst_handler_connected(self):
        "When the handler connects to DST but is not necessarily connected to AP"
        if self.connected_to_ap:
            print("Connected to DST!")
            self.on_dst_connect_to_ap()
            self.send_hints_to_dst()
            async_start(self.send_msgs([{"cmd": "Sync"}]))
        else:
            self.logger.info("Waiting to connect to Archipelago.")

    def on_package(self, cmd: str, args: Dict):
        # print("on_package", cmd)
        try:
            if cmd == "RoomInfo":
                self.seed_name = args.get("seed_name")

            elif cmd == "Connected":
                self.connected_to_ap = True
                self.slotdata = args.get('slot_data')
                if self.dst_handler.connected:
                    print("Connected to AP!")
                    self.on_dst_connect_to_ap()
                else:
                    async def dst_connect_hint():
                        await asyncio.sleep(1.0)
                        self.logger.info("Waiting for Don't Starve Together server.")
                    async_start(dst_connect_hint())

            elif cmd == "ReceivedItems":
                items = [netitem.item for netitem in args["items"]]
                self.dst_handler.enqueue({
                    "datatype": "Items",
                    "items": items,
                    "resync": True if self.resync_items else None,
                })
                self.resync_items = False

            elif cmd == "RoomUpdate":
                if args.get("checked_locations"):
                    locations = [id for id in args.get("checked_locations")]
                    self.dst_handler.enqueue({"datatype": "Locations", "checked_locations": locations})

            elif cmd == "PrintJSON":
                if (args.get("slot") != self.slot) or args.get("type") == "Goal":
                    text = self.rawjsontotextparser(args["data"])
                    self.dst_handler.enqueue({"datatype": "Chat", "msg": text})

            elif cmd == "LocationInfo":
                locs = args.get("locations")
                for loc in locs:
                    self.dst_handler.enqueue({
                        "datatype": "LocationInfo",
                        "location_info": {
                            "location": loc.location,
                            "item": loc.item,
                            "player": loc.player,
                            "itemname": self.item_names[loc.item],
                            "playername": self.player_names[loc.player],
                            "flags": loc.flags,
                        },
                    }, False)

            elif cmd == "Retrieved":
                print("Got retrieved")
                # Send hints to DST
                if f"_read_hints_{self.team}_{self.slot}" in args.get("keys"):
                    self.send_hints_to_dst()
                    
            elif cmd == "SetReply":
                print("Got setreply")
                # Send hints to DST
                if f"_read_hints_{self.team}_{self.slot}" == args.get("key"):
                    self.send_hints_to_dst()

            elif cmd == "InvalidPacket":
                print(args)

        except Exception as e:
            self.logger.error(f"DST on_package error: {e}")

        return super().on_package(cmd, args)

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.connected_to_ap = False
        await super().disconnect(allow_autoreconnect)

    async def queue_event(self, data):
        if self.connected_to_ap:
            # Since we're connected, manage event immediately
            await self.manage_event(data)
        else:
            # Queue for when we connect to AP again
            self._eventqueue.append(data)

    async def handle_eventqueue(self):
        while True:
            try:
                while self.connected_to_ap and len(self._eventqueue):
                    # print(f"Managed queued event {self._eventqueue[0]}")
                    await self.manage_event(self._eventqueue.pop(0))
            except Exception as e:
                self.logger.error(f"DST event queue error: {e}")
            await asyncio.sleep(3.0)

    async def manage_event(self, event:Dict):
        eventtype = event.get("datatype")
        try:
            # print(f"Got event from DST: {eventtype}" )
            if eventtype == "Chat" or eventtype == "Join" or eventtype == "Leave":
                await self.send_msgs([{"cmd": "Say", "text": event.get("msg")}])

            elif eventtype == "Death":
                if "DeathLink" in self.tags:
                    await self.send_death(event.get("msg"))
                    self.logger.info("...And so does everyone else.")
                else:
                    print("Death Link is disabled. Everyone is safe... except you.")

            elif eventtype == "Item":
                loc_id = event.get("source")
                if loc_id != None:
                    print("  Item:", loc_id)
                    self.locations_checked.add(loc_id)
                locs = event.get("sources")
                if locs != None:
                    self.locations_checked.update(locs)
                await self.send_msgs([{"cmd": "LocationChecks", "locations": self.locations_checked}])

            elif eventtype == "Hint": #I think this should be deterministic enough for races, does not account for manual hints
                if len(self.missing_locations):
                    valid = list(self.missing_locations.difference(self.locations_scouted))
                    if len(valid):
                        hint = random.choice(valid)
                        self.locations_scouted.add(hint)
                        await self.send_msgs([{"cmd": "Set",
                                            "key": self.username + "_locations_scouted",
                                            "operations": [{"operation": "replace", "value": self.locations_scouted}]}])
                        await self.send_msgs([{"cmd": "LocationScouts", "locations": [hint], "create_as_hint": 2}])

            elif eventtype == "Victory":
                await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

            elif eventtype == "Connect": # Connection from within DST

                name = event.get("name") or None
                ip = event.get("ip") or None
                password = event.get("password") or None

                if self.connected_to_ap and name and name != self.username:
                    print("Disconnecting current user")
                    await self.disconnect()

                if not self.server or not self.server.socket:
                    # Not connect to AP server at all
                    print("Not connected to AP server. Connecting.")
                    self.username = name
                    self.server_address = ip if ip else self.server_address
                    self.password = password
                    await self.connect()

                elif not self.connected_to_ap:
                    # Connected to AP server but not logged in
                    if name:
                        self.username = name
                    self.auth = self.username
                    self.password = password
                    if self.auth:
                        print(f"Not logged in. Logging in as {self.auth}.")
                        self.send_connect()

                else:
                    self.logger.info("Already connected.")

            elif eventtype == "Disconnect":
                print("Disconnecting")
                await self.disconnect(False)

        except Exception as e:
            self.logger.error(f"Manage event error ({eventtype}): {e}")

def parse_request(req_bytes:bytes):
    "Parses HTTP request from DST"
    lines = req_bytes.decode("utf-8").splitlines()
    req_info = lines.pop(0)
    assert req_info.startswith("POST")
    headers = {}
    assert len(lines)
    while len(lines):
        line = lines.pop(0)
        if not line:
            break
        entry = line.split(" ", 1)
        headers[entry[0]] = entry[1]
    assert len(lines)
    datastr = "\r\n".join(lines)
    if datastr.endswith("EOF"):
        datastr = datastr[:-3]
    return json.loads(datastr)


def send_response(conn:socket.socket, content:Dict = {}, status=100):
    "Sends a response to the connection "
    header  = f"HTTP/1.1 {status}\r\n".encode()
    header += b"Content-type: application/json\r\n"
    header += b"\r\n"

    body = json.dumps(content).encode()
    try:
        conn.send(header + body)
    except Exception as e:
        print(f"Could not send content: {content}")

class DSTHandler():
    logger = logging.getLogger("DSTInterface")
    ctx = None
    lastping = time.time()
    _sendqueue:List[str] = []
    _sendqueue_lowpriority:List[str] = []

    def __init__(self, ctx:DSTContext):
        self.ctx = ctx
        self._connected = False

    @property
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, value:bool):
        if self._connected != value:
            self._connected = value
            if not value:
                self._sendqueue.clear()
                self._sendqueue_lowpriority.clear()

    def enqueue(self, data, priority = True):
        if self.connected:
            (self._sendqueue if priority else self._sendqueue_lowpriority).append(data)

    async def handle_dst_data(self, conn, data):
        try:
            datatype:str = data.get("datatype")
            if datatype == "Ping":
                if len(self._sendqueue):
                    send_response(conn, self._sendqueue.pop(0), 100)
                elif len(self._sendqueue_lowpriority):
                    send_response(conn, self._sendqueue_lowpriority.pop(0), 100)
                else:
                    # No data to send. Delay next ping
                    await asyncio.sleep(1.0)

            elif datatype in {"Chat", "Join", "Leave", "Death", "Connect", "Disconnect"}:
                 # Instant event
                await self.ctx.manage_event(data)

            elif datatype in {"Item", "Hint", "Victory"}:
                # Queued event
                await self.ctx.queue_event(data)

            else:
                if datatype: self.logger.error(f"Error! Recieved invalid datatype: {datatype}")
                await asyncio.sleep(1.0)
                send_response(conn, {"datatype": "Error"}, 400)
                return

            # Tell DST if we're connected to AP
            send_response(conn, {"datatype": "State", "connected": self.ctx.connected_to_ap}, 100)

        except AssertionError as e:
            print(f"Invalid request! {e}")
            send_response(conn, {"datatype": "Error"}, 400)
            await asyncio.sleep(1.0)

    def on_sock_accept(self, conn, address):
        if not self.connected:
            self.connected = True
            self.logger.info(f"Connected to Don't Starve Together server on: {address[0]}")
            self.ctx.on_dst_handler_connected()

    async def handle_dst_request(self, sock:socket.socket):
        loop = asyncio.get_event_loop()
        while True:
            conn = None
            try:
                conn, address = await asyncio.wait_for(loop.sock_accept(sock), timeout=(10 if self.connected else None))
                request = await loop.sock_recv(conn, 4096)
                self.on_sock_accept(conn, address)
                if not request: break
                self.lastping = time.time()
                await self.handle_dst_data(conn, parse_request(request))
            except asyncio.TimeoutError:
                raise
            except Exception as e:
                self.logger.error(f"DST request error: {e}")
                send_response(conn, {"datatype": "Error"}, 500)
                await asyncio.sleep(5.0)
            finally:
                if conn: conn.close()

    async def run_handler(self):
        while True:
            sock = socket.socket()
            sock.bind(("", 8000))
            sock.listen(2)
            sock.setblocking(False)
            try:
                while True:
                    await self.handle_dst_request(sock)
                    if not self.connected: break
            except asyncio.TimeoutError:
                self.logger.info("Disconnected from Don't Starve Together (timed out).")
            except Exception as e:
                self.logger.error(f"DST handler error: {e}")
            finally:
                sock.close()
                self.connected = False
            print("Restarting connection loop in 5 seconds.")
            await asyncio.sleep(5.0)
            self.logger.info("Waiting for Don't Starve Together server.")

async def main(args):
    ctx = DSTContext(args.connect, args.password)
    ctx.auth = args.name
    ctx.run_gui()

    dst_handler_task = asyncio.create_task(ctx.dst_handler.run_handler(), name="DST Handler")

    await ctx.exit_event.wait()
    dst_handler_task.cancel()
    await ctx.shutdown()


def launch():
    import colorama

    parser = get_base_parser(description="DST Archipelago Client for interfacing with Don't Starve Together.")
    parser.add_argument("--name", default=None, help="Slot Name to connect as.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")
    args = parser.parse_args()

    if args.url:
        url = urllib.parse.urlparse(args.url)
        args.connect = url.netloc
        if url.username:
            args.name = urllib.parse.unquote(url.username)
        if url.password:
            args.password = urllib.parse.unquote(url.password)

    colorama.init()

    asyncio.run(main(args))
    colorama.deinit()