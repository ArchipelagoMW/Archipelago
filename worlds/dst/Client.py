import urllib.parse
import threading
import logging
import asyncio
import random
import json
import time
import copy
from NetUtils import RawJSONtoTextParser, ClientStatus, JSONtoTextParser
from CommonClient import CommonContext, get_base_parser, logger
from Utils import async_start
from .DSTWebServer import startWebServer, receivequeue, getvariables, setvariables

class DSTContext(CommonContext):
    game = "Don't Starve Together"
    items_handling = 0b111
    want_slot_data = True

    interfacelog = None
    slotdata = dict()
    defeated_bosses = set()
    defeated_bosses_dirty = False
    required_bosses = set()
    # victories_needed:int = 1
    # days_survived:int = 0
    SlotDataDirty = False
    QueueDSTState = False
    waitforconnect = False
    ConnectDataDirty = True


    

    def __init__(self, server_address, password):
        self.json_text_parser = RawJSONtoTextParser(self)

        super().__init__(server_address, password)

    def on_deathlink(self, data: dict):
        sendqueue = getvariables().get('sendqueue')
        sendqueue.append(json.dumps({'datatype': "Death", 'msg': dict.get(data, 'cause')}))
        setvariables({"sendqueue": sendqueue})

    def run_gui(self):
        from kvui import GameManager

        class DSTManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago"),
                # ("DSTServer", "DST Server Log"),
                ("DSTInterface", "DST Interface"),
            ]
            base_title = "Archipelago Don't Starve Together Client"

        self.ui = DSTManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def on_package(self, cmd: str, args: dict):
        print("on_package", cmd)
        match cmd:
            case "RoomInfo":
                self.seed_name = args.get('seed_name')

            case "Connected":
                self.slotdata = args.get('slot_data')
                self.SlotDataDirty = True
                self.ConnectDataDirty = True
                setvariables({'connected': True})
                sendqueue = getvariables().get('sendqueue')
                sendqueue.append(json.dumps({
                    "datatype": "State",
                    "connected": True,
                    "readyfortraps": True, 
                    "seed_name": self.seed_name,
                    "slot": self.slot,
                    "slot_name": self.player_names[self.slot],
                    "goal": self.slotdata.get("goal"),
                    "days_to_survive": self.slotdata.get("days_to_survive"),
                    "required_bosses": list(self.slotdata.get("required_bosses")),
                    "finished_game": self.finished_game,
                }))
                sendqueue.append(json.dumps({
                    "datatype": "Items", 
                    "items": [netitem.item for netitem in self.items_received],
                    "resync": True,
                }))
                sendqueue.append(json.dumps({
                    "datatype": "Locations", 
                    "missing_locations": list(self.missing_locations),
                }))
                self.QueueDSTState = True
                # setvariables({"sendqueue": sendqueue})

                # Scout missing locations
                async_start(self.send_msgs([{"cmd": "LocationScouts", "locations": self.missing_locations}]))

            case "ReceivedItems":
                sendqueue = getvariables().get('sendqueue')
                items = [netitem.item for netitem in args['items']]
                sendqueue.append(json.dumps({"datatype": "Items", "items": items}))
                # setvariables({"sendqueue": sendqueue})
            
            case "RoomUpdate":
                if args.get("checked_locations"):
                    sendqueue = getvariables().get('sendqueue')
                    locations = [id for id in args.get("checked_locations")]
                    sendqueue.append(json.dumps({"datatype": "Locations", "checked_locations": locations}))
                    # setvariables({"sendqueue": sendqueue})

            case "ConnectionRefused": #Does not seem to get triggered when connection is refused
                setvariables({'authname': "Nil", 'authip': "Nil"})
                self.waitforconnect = False
                # self.AbortDSTConnect = True
                sendqueue = getvariables().get('sendqueue')
                sendqueue.append(json.dumps({"datatype": "State", "connected": False}))

            case "PrintJSON":
                if (args.get('slot') != self.slot) or args.get('type') == "Goal":
                    sendqueue = getvariables().get('sendqueue')
                    text = self.json_text_parser(copy.deepcopy(args["data"]))
                    sendqueue.append(json.dumps({"datatype": "Chat", "msg": text}))
                    # setvariables({"sendqueue": sendqueue})

            # case "Retrieved":
            #     keys = args.get('keys')
            #     scouted = keys.get(self.username + "_locations_scouted")
            #     defeated_bosses = keys.get(self.username + "_defeated_bosses")
            #     print(scouted)
            #     if scouted is not None:
            #         self.locations_scouted = set(scouted)
            #     if defeated_bosses is not None:
            #         self.defeated_bosses = set(defeated_bosses)
            #     print(self.locations_scouted)
            
            case "LocationInfo":
                locs = args.get('locations')
                # relevant_names = {
                #     "item": {},
                #     "player": {},
                # }
                sendqueue = getvariables().get('sendqueue')
                for loc in locs:
                    sendqueue.append(json.dumps({
                        "datatype": "LocationInfo", 
                        "location_info": {
                            "location": loc.location,
                            "item": loc.item,
                            "player": loc.player,
                            "itemname": self.item_names[loc.item],
                            "playername": self.player_names[loc.player],
                            "flags": loc.flags,
                        }, 
                    }))
                # setvariables({"sendqueue": sendqueue})

            case "InvalidPacket":
                print(args)
            
        return super().on_package(cmd, args)
    
    def handle_connection_loss(self, msg: str) -> None:
        super().handle_connection_loss(msg)
        self.waitforconnect = False
        setvariables({'authname': "Nil", 'authip': "Nil", 'connected': False})

    # async def connect(self, address: str | None = None) -> None:

    #     return await super().connect(address)

    async def disconnect(self, allow_autoreconnect: bool = False): # Seems to do nothing
        print("testdisconnect")
        allow_autoreconnect = False
        self.defeated_bosses = set()
        # if allow_autoreconnect == False:
        #     self.username = None
        #     setvariables({'authname': "Nil", 'authip': "Nil"})
        #     self.QueueDeathLink = None
        #     self.QueueDSTState = False
        #     self.waitforconnect = False
        #     self.scouted_dirty = True
        await super().disconnect(allow_autoreconnect)
    

async def trytoconnect(ctx:DSTContext, name: str, ip: str, password: str):
    if name == "Nil":
        name = None
    if ip == "Nil":
        ip = None
    if password == "Nil":
        password = None
    
    if name is not None and ip is not None:
        ctx.username = None
        ctx.auth = name
        ctx.server_address = ip
        ctx.password = password

        ctx.waitforconnect = True
        await ctx.connect()
        # while not ctx.disconnected_intentionally or not ctx.exit_event.is_set() or not ctx.AbortDSTConnect == True:
            
        # ctx.AbortDSTConnect = False

async def onwaitforconnect(ctx:DSTContext):
    print("onwaitforconnect", ctx.username)
    if not ctx.username:
        await ctx.send_connect()
    else:
        setvariables({'authname': "Nil", 'authip': "Nil", 'connected': True})
        ctx.waitforconnect = False


async def timeoutdisconnect(ctx:DSTContext):
    await ctx.disconnect()

async def manageevent(ctx:DSTContext, event):
    # interfacelog.info("Got event from DST:")
    eventtype = dict.get(event, "datatype")
    match eventtype:
        case "Chat" | "Join" | "Leave":
            await ctx.send_msgs([{"cmd": "Say", "text": dict.get(event, "msg")}])
        case "Death":
            if "DeathLink" in ctx.tags:
                await ctx.send_death(dict.get(event, "msg"))
                ctx.interfacelog.info("...And so does everyone else.")
            else:
                ctx.interfacelog.info("Death Link is disabled. Everyone is safe... except you.")
        case "Item":
            loc_id:int = dict.get(event, "source")
            print("  Item:", loc_id)
            ctx.locations_checked.add(loc_id)
            loc_name = ctx.location_names.get(loc_id)
            if loc_name and loc_name in ctx.required_bosses:
                # Boss kill
                ctx.defeated_bosses.add(loc_name)
                ctx.defeated_bosses_dirty = True
            await ctx.send_msgs([{"cmd": "LocationChecks", "locations": ctx.locations_checked}])
        case "Hint": #I think this should be deterministic enough for races, does not account for manual hints
            if ctx.missing_locations.__len__() != 0:
                # print(ctx.locations_scouted)
                valid = ctx.missing_locations.difference(ctx.locations_scouted)
                hints = list()
                for _ in range(3):
                    hint = valid.pop()
                    ctx.locations_scouted.add(hint)
                    hints.append(hint)
                await ctx.send_msgs([{"cmd": "Set",
                                    "key": ctx.username + "_locations_scouted",
                                    #   "default":  ctx.locations_scouted,
                                    "operations": [{"operation": "replace", "value": ctx.locations_scouted}]}])
                await ctx.send_msgs([{"cmd": "LocationScouts", "locations": hints, "create_as_hint": 2}])
        # case "DaysSurvived":
        #     ctx.interfacelog.info("Lived for days:")
        #     ctx.interfacelog.info(ctx.days_survived)
        #     ctx.days_survived = dict.get(event, "num")
        #     ctx.defeated_bosses_dirty = True
        case "Victory":
            await onwincondition(ctx)
        
async def onwincondition(ctx):
    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])


async def interface(ctx:DSTContext):
    ctx.interfacelog = logging.getLogger("DSTInterface")
    # serverinterface = startWebServer()
    Thread = threading.Thread(None, startWebServer, "WebServer") #Add way to restart thread during loop if it shuts down
    Thread.start()

    try:
        while not ctx.exit_event.is_set():
            vars = getvariables()
            authname = vars.get('authname')
            authip = vars.get('authip')
            authpassword = vars.get('password')
            authdirty = vars.get('authdirty')

            setvariables({'frozencheck': time.time()})

            #At a moments notice the loop should be able to stop and abort the Thread

            # print(ctx.username)
            if not ctx.exit_event.is_set() and not Thread.is_alive():
                Thread = threading.Thread(None, startWebServer, "WebServer")
                Thread.start()
                setvariables({'frozencheck': time.time()})

            elif not ctx.exit_event.is_set() and authdirty:
                print("trytoconnect", authname, authip, authpassword, authdirty)
                await trytoconnect(ctx, authname, authip, authpassword)
                setvariables({'authdirty': False})
                
            elif not ctx.exit_event.is_set() and not ctx.username: # If not Connected
                if ctx.waitforconnect:
                    await onwaitforconnect(ctx)

            elif not ctx.exit_event.is_set() and (time.time() - vars.get('lastping') > 10): # If Connected, but has not
                await timeoutdisconnect(ctx)                                           #had a ping from DST for a while

            elif not ctx.exit_event.is_set() and ctx.SlotDataDirty == True: # If Connected and waiting to change DL
                print(ctx.slotdata)
                print(ctx.slotdata.get('death_link'))
                await ctx.update_death_link(ctx.slotdata.get('death_link'))
                # ctx.required_bosses = ctx.slotdata.get('required_bosses',set())
                # match ctx.slotdata.get('goal'):
                #     case "bosses_any": ctx.victories_needed = 1
                #     case "bosses_all": ctx.victories_needed = len(ctx.required_bosses)
                #     case "survival": ctx.victories_needed = 1
                ctx.SlotDataDirty = False

            # elif not ctx.exit_event.is_set() and ctx.QueueDSTState == True:
            #     sendqueue = getvariables().get('sendqueue')
            #     sendqueue.append(json.dumps({"datatype": "State", "readyfortraps": True, "slot": ctx.slot}))
            #     sendqueue.append(json.dumps({"datatype": "Locations", "locations": [id for id in ctx.missing_locations]}))

            #     setvariables({"sendqueue": sendqueue})
            #     ctx.QueueDSTState = False

            elif not ctx.exit_event.is_set() and ctx.ConnectDataDirty == True:
                await ctx.send_msgs([{"cmd": "Get", "keys": [ctx.username + "_locations_scouted"]}])
                await ctx.send_msgs([{"cmd": "Get", "keys": [ctx.username + "_defeated_bosses"]}])
                ctx.ConnectDataDirty = False

            # elif not ctx.exit_event.is_set() and ctx.defeated_bosses_dirty == True:
            #     await ctx.send_msgs([{"cmd": "Set",
            #                       "key": ctx.username + "_defeated_bosses",
            #                       "operations": [{"operation": "replace", "value": ctx.defeated_bosses}]}])
                
            #     victory_count = 0
            #     if ctx.slotdata.get('goal') == "survival":
            #         if ctx.slotdata.get('days_to_survive') <= ctx.days_survived: victory_count += 1
            #     else:
            #         for boss_target in ctx.required_bosses:
            #             if boss_target in ctx.defeated_bosses: victory_count += 1

            #     if victory_count >= ctx.victories_needed:
            #         await onwincondition(ctx)
            #     ctx.defeated_bosses_dirty = False

            elif not ctx.exit_event.is_set() and receivequeue.__len__() > 0: # If Connected and has a event to process
                event = receivequeue.pop(0)
                await manageevent(ctx, event)
                
            if not ctx.exit_event.is_set():
                await asyncio.sleep(0.2)

        ctx.interfacelog.info("Stopping server...")
        setvariables({'serverstopsignal': True})
        Thread.join()
        ctx.interfacelog.info("Server stopped successfully")

    except Exception as e:
        ctx.interfacelog.exception(e)
        ctx.interfacelog.info("Stopping server...")
        setvariables({'serverstopsignal': True})
        Thread.join()
        ctx.interfacelog.info("Server stopped successfully")

async def main(args):
    ctx = DSTContext(args.connect, args.password)
    ctx.auth = args.name
    ctx.run_gui()

    dstinterface = asyncio.create_task(interface(ctx), name="DSTInterface")
    
    await ctx.exit_event.wait()
    await ctx.shutdown()


def launch():
    import colorama

    parser = get_base_parser(description="DST Archipelago Client for interfacing with Don't Starve Together.")
    parser.add_argument('--name', default=None, help="Slot Name to connect as.")
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