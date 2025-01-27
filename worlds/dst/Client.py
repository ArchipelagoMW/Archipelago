from typing import Optional, Any, Dict, List, Set
import urllib.parse
import logging
import asyncio
import json
import time
import socket
import random
from NetUtils import ClientStatus
from CommonClient import CommonContext, get_base_parser
from Utils import async_start, is_windows, is_macos
from pathlib import Path
import os
from .Constants import LOCATION_BOSS_RANGE, LOCATION_RESEARCH_RANGE, VERSION, CLIENT_HOSTNAME, CLIENT_PORT
from math import floor
DST_FILE_START = "KLEI     1 "
TIMEOUT_TIME:int = 60*3

class DSTInvalidRequest(Exception):
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
    locations_hinted = set()
    _eventqueue:List[Dict] = []

    def __init__(self, server_address, password):
        self.dst_handler = DSTHandler(self)
        super().__init__(server_address, password)

    def on_deathlink(self, data:Dict):
        self.dst_handler.enqueue({
            "datatype": "Death",
            "msg": data.get("cause"),
            "timestamp": time.time(),
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
        print("Sending randomizer data to DST.")
        self.dst_handler.enqueue({
            "datatype": "State",
            "connected": True,
            "clientversion": VERSION,
            "generatorversion": self.slotdata.get("generator_version"),
            "seed_name": self.seed_name,
            "slot": self.slot,
            "slot_name": self.player_names[self.slot],
            "goal": self.slotdata.get("goal"),
            "days_to_survive": self.slotdata.get("days_to_survive"),
            "required_bosses": self.slotdata.get("required_bosses"), # Legacy
            "goal_locations": self.slotdata.get("goal_locations"),
            "crafting_mode": self.slotdata.get("crafting_mode"),
            "starting_season": self.slotdata.get("starting_season"),
            "seasons": self.slotdata.get("seasons"),
            "finished_game": self.finished_game,
            "death_link": self.slotdata.get("death_link"), # Game decides whether to use slot data or override
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
            "locations": [id for id in self.missing_locations
                if (id >= LOCATION_RESEARCH_RANGE["start"] and id <= LOCATION_RESEARCH_RANGE["end"])
                or (id >= LOCATION_BOSS_RANGE["start"] and id <= LOCATION_BOSS_RANGE["end"])
            ],
        }]))

    def send_hints_to_dst(self):
        self.locations_hinted = set()
        for hint in self.stored_data.get(f"_read_hints_{self.team}_{self.slot}", []):
            if self.slot == hint["finding_player"]:
                self.locations_hinted.add(hint["location"])
            if hint["found"]:
                continue
            self.dst_handler.enqueue({
                "datatype": "HintInfo",
                "item": hint["item"],
                "itemname": self.item_names.lookup_in_slot(hint["item"], hint["receiving_player"]),
                "location": hint["location"],
                "locationname": self.location_names.lookup_in_slot(hint["location"], hint["finding_player"]),
                "finding_player": hint["finding_player"],
                "findingname": self.player_names[hint["finding_player"]],
                "receiving_player" : hint["receiving_player"],
                "receivingname": self.player_names[hint["receiving_player"]],
            }, False)

    # def on_dst_handler_connected(self):
    #     "When the handler connects to DST but is not necessarily connected to AP"
    #     if self.connected_to_ap:
    #         print("Connected to DST!")
    #         self.on_dst_connect_to_ap()
    #         self.send_hints_to_dst()
    #         async_start(self.send_msgs([{"cmd": "Sync"}]))
    #     else:
    #         self.logger.info("Waiting to connect to Archipelago.")
    
    def on_dst_reader_connected(self):
        "Counterpart of on_dst_handler_connected. When the reader checks that DST data folder exists."
        if self.connected_to_ap:
            print("Located DST data folder!")
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
                self.slotdata = args.get('slot_data', {})
                if self.dst_handler.connected:
                    print("Connected to AP!")
                    self.on_dst_connect_to_ap()
                else:
                    async def dst_connect_hint():
                        await asyncio.sleep(1.0)
                        self.logger.info("Waiting for Don't Starve Together server.")
                    async_start(dst_connect_hint())

                # Remind player of their goal and world settings
                async def goal_hint():
                    await asyncio.sleep(0.5)
                    # Announce generator version
                    self.logger.info(f"World generated on DST version: {self.slotdata.get('generator_version', 'Unknown')}")
                    # Announce goal type
                    _goal = self.slotdata.get("goal")
                    self.logger.info(f"Goal type: {_goal}")
                    if _goal == "survival":
                        # Announce survival day goal
                        _days_to_survive = self.slotdata.get("days_to_survive", "Unknown")
                        self.logger.info(f"Days to survive: {_days_to_survive}")
                    elif _goal == "bosses_all" or _goal == "bosses_any":
                        # List goal bosses
                        _bosses = [self.location_names.lookup_in_game(loc_id) for loc_id in self.slotdata.get("goal_locations", [])]
                        self.logger.info(f"Bosses: {_bosses}")
                    self.logger.info("The client needs to read local files. Create your world as a local save, not cloud save.")
                    self.logger.info("The following settings need to be manually set in your world (if not default)!")
                    # Announce cave settings
                    self.logger.info(f"Caves Required: {'Yes' if self.slotdata.get('is_caves_enabled', True) else 'No'}")
                    # Announce season settings
                    _seasons = self.slotdata.get("seasons", ["Autumn", "Winter", "Spring", "Summer"])
                    _starting_season = str(self.slotdata.get("starting_season", "Autumn")).capitalize()
                    self.logger.info(f"Starting Season: {_starting_season}" + (" (Default)" if _starting_season == "Autumn" else ""))
                    self.logger.info(f"Enabled Seasons: {'All (Default)' if len(_seasons) == 4 else _seasons}")
                    # Announce season flow
                    if self.slotdata.get("unlockable_seasons", False):
                        self.logger.info("Unlockable seasons - Optionally, you may set all season lengths to their longest value.")
                    # Announce day phases
                    _day_phases = self.slotdata.get('day_phases', ["Day", "Dusk", "Night"])
                    self.logger.info(f"Day Phases: {'All (Default)' if len(_day_phases) == 3 else _day_phases}"
                                        + (f" (Lights Out)" if len(_day_phases) == 1 and _day_phases[0] == "Night" else "")
                                    )
                    # Announce intended character
                    self.logger.info(f"Character Selection: {self.slotdata.get('character', 'Any')}")

                async_start(goal_hint())

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
                            "itemname": self.item_names.lookup_in_slot(loc.item, loc.player),
                            "playername": self.player_names[loc.player],
                            "flags": loc.flags,
                        },
                    }, False)

            elif cmd == "Retrieved":
                # Send hints to DST
                if f"_read_hints_{self.team}_{self.slot}" in args.get("keys"):
                    self.send_hints_to_dst()

            elif cmd == "SetReply":
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
                    valid = list(self.missing_locations.difference(self.locations_hinted, set(self.slotdata.get("goal_locations", []))))
                    random.seed(self.seed_name + str(self.slot) + str(len(valid)))
                    valid.sort()
                    if len(valid):
                        hint_id = random.choice(valid)
                        self.locations_hinted.add(hint_id)
                        await self.send_msgs([{"cmd": "LocationScouts", "locations": [hint_id], "create_as_hint": 2}])

            elif eventtype == "ScoutLocation":
                loc_id = event.get("id")
                if loc_id and (loc_id in self.missing_locations or loc_id in self.locations_checked):
                    await self.send_msgs([{
                        "cmd": "LocationScouts",
                        "locations": [loc_id],
                    }])

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

            elif eventtype == "DeathLink":
                await self.update_death_link(event.get("enabled", False))

        except Exception as e:
            self.logger.error(f"Manage event error ({eventtype}): {e}")

# def parse_request(req_bytes:bytes):
#     "Parses HTTP request from DST"
#     try:
#         lines = req_bytes.decode("utf-8").splitlines()
#         req_info = lines.pop(0)
#         assert req_info.startswith("POST")
#         headers = {}
#         assert len(lines)
#         while len(lines):
#             line = lines.pop(0)
#             if not line:
#                 break
#             entry = line.split(" ", 1)
#             headers[entry[0]] = entry[1]
#         assert len(lines)
#         datastr = "\r\n".join(lines)
#         if datastr.endswith("EOF"):
#             datastr = datastr[:-3]
#         return json.loads(datastr)
#     except AssertionError:
#         raise DSTInvalidRequest("Invalid request")
#     except Exception as e:
#         print(f"Bad parse: {e}")
#         print(req_bytes)
#         raise

# class DSTResponse():
#     response:bytes
#     next_ping_time:float = 0.0
#     def __init__(self, content:Dict = {}, status=100, next_ping_time:float=0.0):
#         header  = f"HTTP/1.1 {status}\r\n".encode()
#         header += b"Content-type: application/json\r\n"
#         header += b"\r\n"

#         body = json.dumps(content).encode()
#         self.response = header + body
#         self.next_ping_time = next_ping_time

class DSTHandler():
    logger = logging.getLogger("DSTInterface")
    ctx = None
    lastping = time.time()
    _sendqueue:List[Any] = []
    _sendqueue_lowpriority:List[Any] = []
    filedata_location_scouts:Set[int] = set()
    outgoing_data_dirty = False
    waiting_for_dst = False
    connected_timestamp = time.time()
    session_id:Optional[int] = None # DST's connected timestamp
    _cached_timestamps:Dict[str, Set[int]] = {
        "Death": set(),
        "Hint": set(),
    }
    _debug_cache:Set[str] = set()

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
            self.outgoing_data_dirty = True

    async def handle_incoming_filedata(self, filedata:Dict[str, Any]):
        """
        Filereader workaround for handle_dst_data. May be temporary until game adds a solution to restore HTTP functionality.
        Since the filedata sends everything at once and does not get cleared until the DST reloads, verifying must be done
        to reduce redundant data.
        """
        for datatype, data in filedata.items():
            if datatype == "Victory":
                if not self.ctx.finished_game:
                    await self.handle_dst_filedata_entry({"datatype": datatype})
            elif datatype == "Item":
                _sources:Set[int] = set(data)
                _sources.difference_update(self.ctx.checked_locations)
                if len(_sources):
                    await self.handle_dst_filedata_entry({
                        "datatype": datatype,
                        "sources": list(_sources),
                    })
            elif datatype == "DeathLink":
                if "DeathLink" in self.ctx.tags:
                    await self.handle_dst_filedata_entry({
                        "datatype": datatype,
                        "enabled": data.get("enabled", False),
                    })
            elif datatype == "Death":
                for deathdata in data:
                    timestamp:Optional[int] = deathdata.get("timestamp")
                    # Verify timestamp hasn't been sent yet and is after connection time
                    if timestamp and timestamp > self.connected_timestamp and not timestamp in self._cached_timestamps[datatype]:
                        self._cached_timestamps[datatype].add(timestamp)
                        await self.handle_dst_filedata_entry({
                            "datatype": datatype,
                            "msg": deathdata.get("msg", ""),
                        })
            elif datatype == "ScoutLocation":
                _scouts:Set[int] = set(data)
                _scouts.difference_update(self.filedata_location_scouts)
                self.filedata_location_scouts.update(_scouts)
                if len(_scouts):
                    for id in list(_scouts):
                        await self.handle_dst_filedata_entry({
                            "datatype": datatype,
                            "id": id,
                        })
            elif datatype == "Hint":
                for hintdata in data:
                    timestamp:Optional[int] = hintdata.get("timestamp")
                    # Verify timestamp hasn't been sent yet and is after connection time
                    if timestamp and timestamp > self.connected_timestamp and not timestamp in self._cached_timestamps[datatype]:
                        self._cached_timestamps[datatype].add(timestamp)
                        await self.handle_dst_filedata_entry({"datatype": datatype})

    async def handle_dst_filedata_entry(self, data):
        "Counterpart for handle_dst_data. May be temporary until game adds a solution to restore HTTP functionality."
        try:
            datatype:str = data.get("datatype")
            
            if datatype in {"Chat", "Join", "Leave", "Death", "Connect", "Disconnect", "DeathLink"}:
                 # Instant event
                await self.ctx.manage_event(data)

            elif datatype in {"Item", "Hint", "Victory", "ScoutLocation"}:
                # Queued event
                await self.ctx.queue_event(data)

        except Exception as e:
            print(f"Handle DST filedata entry error! {e}")

    # async def handle_dst_data(self, data) -> DSTResponse:
    #     try:
    #         datatype:str = data.get("datatype")
    #         next_ping_time = 0.0
    #         if datatype == "Ping":
    #             pass
    #             if len(self._sendqueue):
    #                 return DSTResponse(self._sendqueue.pop(0), 100)
    #             elif len(self._sendqueue_lowpriority):
    #                 return DSTResponse(self._sendqueue_lowpriority.pop(0), 100)
    #             else:
    #                 # No data to send. Delay next ping
    #                 next_ping_time = 1.0

    #         elif datatype in {"Chat", "Join", "Leave", "Death", "Connect", "Disconnect", "DeathLink"}:
    #              # Instant event
    #             await self.ctx.manage_event(data)

    #         elif datatype in {"Item", "Hint", "Victory", "ScoutLocation"}:
    #             # Queued event
    #             await self.ctx.queue_event(data)

    #         else:
    #             if datatype: self.logger.error(f"Error! Received invalid datatype: {datatype}")
    #             return DSTResponse({"datatype": "Error"}, 400, 1.0)

    #         # Tell DST if we're connected to AP
    #         return DSTResponse({"datatype": "State", "connected": self.ctx.connected_to_ap}, 100, next_ping_time)

    #     except Exception as e:
    #         print(f"Handle DST data error! {e}")
    #         return DSTResponse({"datatype": "Error"}, 400, 1.0)

    # def on_sock_accept(self, conn, address):
    #     if not self.connected:
    #         self.connected = True
    #         self.logger.info(f"Connected to Don't Starve Together server on: {address[0]}")
    #         self.ctx.on_dst_handler_connected()

    # async def handle_dst_request(self, sock:socket.socket):
    #     loop = asyncio.get_event_loop()
    #     next_ping_time = 0.0
    #     while True:
    #         conn = None
    #         try:
    #             conn, address = await asyncio.wait_for(loop.sock_accept(sock), timeout=(10 if self.connected else None))
    #             request = await loop.sock_recv(conn, 4096)
    #             self.on_sock_accept(conn, address)
    #             if not request: break
    #             self.lastping = time.time()
    #             response:DSTResponse = await self.handle_dst_data(parse_request(request))
    #             next_ping_time = response.next_ping_time
    #             await loop.sock_sendall(conn, response.response)
    #         except asyncio.TimeoutError:
    #             raise
    #         except DSTInvalidRequest as e:
    #             print(f"Invalid request! {e}")
    #             if conn:
    #                 await loop.sock_sendall(conn, DSTResponse({"datatype": "Error"}, 400).response)
    #             next_ping_time = 1.0
    #         except Exception as e:
    #             self.logger.error(f"DST request error: {e}")
    #             if conn:
    #                 await loop.sock_sendall(conn, DSTResponse({"datatype": "Error"}, 500).response)
    #             next_ping_time = 1.0
    #             self.connected = False
    #         finally:
    #             if conn:
    #                 conn.shutdown(socket.SHUT_RDWR)
    #                 conn.close()
    #             if next_ping_time > 0:
    #                 await asyncio.sleep(next_ping_time)

    # async def bind_socket(self, sock:socket.socket):
    #     sock.bind((CLIENT_HOSTNAME, CLIENT_PORT))

    # async def run_handler(self):
    #     self.logger.info(f"Running Don't Starve Together Client Version {VERSION}")
    #     while True:
    #         # Bind the socket and make sure it actually succeeds
    #         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         try:
    #             await asyncio.wait_for(self.bind_socket(sock), timeout=3)
    #             sock.listen(5) 
    #         except Exception as e:
    #             self.logger.error("Could not bind socket. Check that you don't already have another instance of the client running! Attempting again in 10 seconds.")
    #             sock.close()
    #             self.connected = False
    #             await asyncio.sleep(10.0)
    #             continue

    #         # Handle requests
    #         try:
    #             while True:
    #                 await self.handle_dst_request(sock)
    #                 if not self.connected: break
    #         except asyncio.TimeoutError:
    #             self.logger.info("Disconnected from Don't Starve Together (timed out).")
    #         except Exception as e:
    #             self.logger.error(f"DST handler error: {e}")
    #         finally:
    #             sock.close()
    #             self.connected = False
    #         print("Restarting connection loop in 5 seconds.")
    #         await asyncio.sleep(5.0)
    #         self.logger.info("Waiting for Don't Starve Together server.")

    
    def get_game_data_folder(self) -> Path:
        "Gets the path of the savedata folder for DST. May be temporary until game adds a solution to restore HTTP functionality."
        home_path:Path
        data_folder_path:Path
        if is_windows:
            # Copy-paste from SC2
            # The next five lines of utterly inscrutable code are brought to you by copy-paste from Stack Overflow.
            # https://stackoverflow.com/questions/6227590/finding-the-users-my-documents-path/30924555#
            import ctypes.wintypes
            CSIDL_PERSONAL = 5  # My Documents
            SHGFP_TYPE_CURRENT = 0  # Get current, not default value

            buf = ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
            ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
            documentspath:str = buf.value
            home_path = Path(documentspath)
            data_folder_path = Path("Klei/DoNotStarveTogether")
        elif is_macos: # TODO: Verify if works on macos
            home_path = Path.home()
            data_folder_path = Path("Documents/Klei/DoNotStarveTogether")
        else: # TODO: Verify if works on linux
            home_path = Path.home()
            data_folder_path = Path(".klei/DoNotStarveTogether")

        # Check if the file exists.
        full_path = home_path / data_folder_path
        if os.path.isdir(full_path):
            return full_path
        else:
            raise IOError(f"Did not find directory at {str(data_folder_path)}")

    def read_incoming_data(self, base_dir:Path) -> Optional[Dict]:
        "Read AP data coming from DST. May be temporary until game adds a solution to restore HTTP functionality."
        file = base_dir / "archipelagorandomizer_outgoing"
        if os.path.isfile(file):
            raw = ""
            with open(file) as f:
                raw = f.read()

            if not raw.startswith(DST_FILE_START):
                raise IOError(f"Unexpected file format: {str(file)}")
            
            data = json.loads(raw[len(DST_FILE_START):])

            # Check timestamp                
            _timestamp:int = data.get("timestamp", floor(time.time()))
            _time_difference = floor(time.time()) - _timestamp
            if _time_difference > TIMEOUT_TIME:
                print(f"Current data is too old! It's from {_time_difference} seconds ago.")
                return None

            return data
        return None

    def get_incoming_data_timestamp(self, base_dir:Path) -> Optional[int]:
        "Just get the timestamp from data. May be temporary until game adds a solution to restore HTTP functionality."
        file = base_dir / "archipelagorandomizer_outgoing"
        try:
            if os.path.isfile(file):
                raw = ""
                with open(file) as f:
                    raw = f.read()

                if not raw.startswith(DST_FILE_START):
                    raise IOError(f"Unexpected file format: {str(file)}")
                
                data = json.loads(raw[len(DST_FILE_START):])

                # Check timestamp
                return data.get("timestamp")
            return None
        except Exception as e:
            self.logger.error(e)
            return None

    def write_outgoing_data(self, base_dir:Path):
        "Send AP data to DST. May be temporary until game adds a solution to restore HTTP functionality."
        if not self.outgoing_data_dirty:
            return
        self.outgoing_data_dirty = False
        file = base_dir / "archipelagorandomizer_incoming"

        senddata = {
            "seed_name": self.ctx.seed_name,
            "slot": self.ctx.slot,
            "connected_timestamp": floor(self.connected_timestamp),
            "timestamp": floor(time.time()),
        }
        if self.session_id:
            # Include queue
            senddata["session_id"] = self.session_id
            senddata["sendqueue"] = self.optimize_sendqueue_for_filewrite(self._sendqueue)
            senddata["sendqueue_lowpriority"] = self.optimize_sendqueue_for_filewrite(self._sendqueue_lowpriority)
        
        with open(file, "w") as f:
            f.write(DST_FILE_START + json.dumps(senddata))

    def optimize_sendqueue_for_filewrite(self, queue:List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        "Remove duplicates and Chat from sendqueue"
        hint_info_cache:Dict[int, Set[int]] = {}
        ret:List[Dict[str, Any]] = []
        for data in queue:
            datatype:str = data.get("datatype")
            if datatype == "Chat": # Remove Chat
                continue
            elif datatype == "HintInfo":
                # Remove duplicates
                hinted_locs_for_player = hint_info_cache.get(data["finding_player"], set())
                hint_info_cache[data["finding_player"]] = hinted_locs_for_player
                
                if not data["location"] in hinted_locs_for_player:
                    hinted_locs_for_player.add(data["location"])
                    ret.append(data)
            else:
                ret.append(data)
        return ret

    async def handle_io(self, base_dir:Path):
        "Counterpart of handle_dst_request. May be temporary until game adds a solution to restore HTTP functionality."
        # Wait until we have a seed name before proceeding
        while not self.ctx.seed_name or not self.ctx.slot or not self.ctx.connected_to_ap:
            await asyncio.sleep(0.5)

        # Start of session
        self.connected_timestamp = time.time()
        self.outgoing_data_dirty = True
        self.waiting_for_dst = False
        await asyncio.sleep(1.0)
        _session_location = "."

        # Identify all data folders. There could potentially be multiple if there's multiple user profiles(?)
        profile_dirs:List[Path] = []
        if os.path.isdir(base_dir / "client_save"):
            profile_dirs.append(base_dir)
        
        dirs = [str(filename) for filename in os.listdir(base_dir) if os.path.isdir(base_dir / filename)]
        for dirname in dirs:
            if os.path.isdir(base_dir / dirname / "client_save"):
                profile_dirs.append(base_dir / dirname)

        print(f"Found {len(profile_dirs)} profile folder(s).")
        if not len(profile_dirs):
            raise IOError(f"Did not find any save data folders in {str(base_dir)}")
        
        # Locate the folder where the active session is. It'll have a new timestamp
        while True:
            _newest_timestamp = int(self.connected_timestamp) - TIMEOUT_TIME
            _new_base_dir = base_dir
            breakout = False
            total_dirs_num = 0
            for profile_dir in profile_dirs:
                dirs = [str(filename) for filename in os.listdir(profile_dir) if os.path.isdir(profile_dir / filename)]
                total_dirs_num += len(dirs)
                for dirname in dirs:
                    path = dirname / Path("Master/save")
                    if dirname == "client_save":
                        path = Path(dirname)
                    _timestamp = self.get_incoming_data_timestamp(Path(profile_dir / path))
                    if _timestamp and _timestamp > _newest_timestamp:
                        _newest_timestamp = _timestamp
                        _new_base_dir = Path(profile_dir / path)
                        _session_location = str(path)
                        breakout = True
            if not total_dirs_num:
                raise IOError("No world save folders found within DoNotStarveTogether folder")
            if breakout:
                base_dir = _new_base_dir
                break
            # Tell the player to run DST
            if not self.waiting_for_dst:
                self.waiting_for_dst = True
                self.logger.info(f"Looking for active Don't Starve Together session. Load up your world and give it a minute to confirm an active session.")
            await asyncio.sleep(2.0)
                    
        self.waiting_for_dst = False
        self.logger.info(f"Located active session in {_session_location} folder.")

        # Continue the loop while connected to AP
        while self.ctx.connected_to_ap:
            try:
                self.write_outgoing_data(base_dir)
                await asyncio.sleep(1.0)
                incoming_data = self.read_incoming_data(base_dir)
                if incoming_data:
                    dst_session_id = incoming_data.get("connected_timestamp")
                    if not self.session_id:
                        if incoming_data.get("seed") == "None" or (
                            incoming_data.get("seed") == self.ctx.seed_name
                            and incoming_data.get("slotnum") == self.ctx.slot
                        ):
                            self.session_id = dst_session_id
                            self.outgoing_data_dirty = True
                            self.logger.info(f"Connected to Don't Starve Together")
                        else:
                            self.logger.error(f"Error! World doesn't match! Got player {incoming_data.get('slotname', 'Unknown')} with seed {incoming_data.get('seed')}")
                            await asyncio.sleep(5.0) # It will spam but we'll slow it down a bit
                    if self.session_id:
                        if self.session_id != dst_session_id:
                            # Stale session; update session id
                            self.session_id = dst_session_id
                            self.outgoing_data_dirty = True
                            print("Updating session")
                        await self.handle_incoming_filedata(incoming_data)
                else:
                    break
            except Exception as e:
                self.logger.error(f"DST handle io error: {e}")
                raise

    async def run_reader(self):
        "Counterpart of run_handler. May be temporary until game adds a solution to restore HTTP functionality."
        self.logger.info(f"Running Don't Starve Together Client Version {VERSION}")
        while True:
            try:
                base_dir = self.get_game_data_folder()
                while True:
                    if not self.connected:
                        self.connected = True
                        self.ctx.on_dst_reader_connected()

                        await self.handle_io(base_dir)
                        self.connected = False # Reset queues
                        self.logger.info(f"Disconnected from Don't Starve Together (timed out)")
                        await asyncio.sleep(3.0)
            except Exception as e:
                self.logger.error(f"DST file reader error: {e}")
            finally:
                self.connected = False
            print("Restarting connection loop in 5 seconds.")
            await asyncio.sleep(5.0)


async def main(args):
    ctx = DSTContext(args.connect, args.password)
    ctx.auth = args.name
    ctx.run_gui()

    dst_handler_task = asyncio.create_task(ctx.dst_handler.run_reader(), name="DST Handler")

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