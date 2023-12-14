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
from .DSTWebServer import startWebServer, receivequeue, getvariables, setvariables

class DSTContext(CommonContext):
    game = "Don't Starve Together"
    items_handling = 0b111
    want_slot_data = True

    interfacelog = None
    slotdata = dict()
    bosskills = set()
    bosskills_dirty = False
    bosses = set()
    SlotDataDirty = False
    QueueDSTState = False
    waitforconnect = False
    server_location_ids = None # To be filled when first needed
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
        if cmd == "Connected":
            self.slotdata = dict.get(args, 'slot_data')
            # self.slotdata.deathlink = dict.get(dict.get(args, 'slot_data'), 'death_link')
            # self.slotdata.bosses = dict.get(dict.get(args, 'slot_data'), 'bosses')
            self.SlotDataDirty = True
            self.ConnectDataDirty = True

            setvariables({'connected': True})

            sendqueue = getvariables().get('sendqueue')
            items = []
            for netitem in self.items_received:
                items.append(self.item_names.get(netitem.item))
            sendqueue.append(json.dumps({"datatype": "Items", "items": items, "msg": None}))
            # locations = []
            # # for loc in dict.get(args, 'checked_locations'):
            # #     locations.append(self.location_names.get(loc))
            # for locid in self.missing_locations:
            #     locations.append(self.location_names.get(locid))
            # if not "Ancient Fuelweaver" in self.bosses:
            #     locations.append("Ancient Fuelweaver")
            # if not "Celestial Champion" in self.bosses:
            #     locations.append("Celestial Champion")
            # sendqueue.append(json.dumps({"datatype": "Locations", "locations": locations}))
            self.QueueDSTState = True

            setvariables({"sendqueue": sendqueue})

            # This is not standard practice, best to design things in a way to where you ever only need the ids
            # self.location_ids = {y:x for (x,y) in self.location_names.items()} # flip it

        if cmd == "ReceivedItems":
            sendqueue = getvariables().get('sendqueue')
            items = []
            for netitem in dict.get(args, 'items'):
                items.append(self.item_names.get(netitem.item))
            sendqueue.append(json.dumps({"datatype": "Items", "items": items, "msg": None}))
            # locations = []
            # for loc in self.locations_checked:
            #     locations.append(self.location_names.get(loc))
            # for loc in self.bosskills:
            #     locations.append(loc)
            locations = []
            for locid in self.missing_locations:
                locations.append(self.location_names.get(locid))
            if not "Ancient Fuelweaver" in self.bosses:
                locations.append("Ancient Fuelweaver")
            if not "Celestial Champion" in self.bosses:
                locations.append("Celestial Champion")
            sendqueue.append(json.dumps({"datatype": "Locations", "locations": locations}))
            setvariables({"sendqueue": sendqueue})

        if cmd == "ConnectionRefused": #Does not seem to get triggered when connection is refused
            setvariables({'authname': "Nil", 'authip': "Nil"})
            self.waitforconnect = False
            # self.AbortDSTConnect = True


        if cmd == "PrintJSON":
            if (dict.get(args, 'slot') != self.slot) or dict.get(args, 'type') == "Goal":
                sendqueue = getvariables().get('sendqueue')
                text = self.json_text_parser(copy.deepcopy(args["data"]))
                sendqueue.append(json.dumps({"datatype": "Chat", "msg": text}))
                setvariables({"sendqueue": sendqueue})

        if cmd == "Retrieved":
            keys = dict.get(args, 'keys')
            scouted = keys.get(self.username + "_locations_scouted")
            bosskills = keys.get(self.username + "_bosskills")
            print(scouted)
            if scouted is not None:
                self.locations_scouted = set(scouted)
            if bosskills is not None:
                self.bosskills = set(bosskills)
            print(self.locations_scouted)

        if cmd == "InvalidPacket":
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
        self.bosskills = set()
        # if allow_autoreconnect == False:
        #     self.username = None
        #     setvariables({'authname': "Nil", 'authip': "Nil"})
        #     self.QueueDeathLink = None
        #     self.QueueDSTState = False
        #     self.waitforconnect = False
        #     self.scouted_dirty = True
        await super().disconnect(allow_autoreconnect)


def CollectServerLocationNames(ctx) -> dict:
    names = dict()
    for id in ctx.server_locations:
        names[ctx.location_names.get(id)] = id
    return names

def GetTiedLocations(ctx, source = str) -> list:
    if ctx.server_location_ids is None:
        ctx.server_location_ids = CollectServerLocationNames(ctx)
    # print(source)
    # print(ctx.location_names)
    # # print(ctx.server_location_ids)
    # print(ctx.server_location_ids.get(source))
    # print(ctx.server_location_ids.get("Ancient Fuelweaver"))
    if ctx.server_location_ids.get(source) != None:
        print("Found Single")
        return [ctx.server_location_ids.get(source)]
    elif source == "Ancient Fuelweaver" or source == "Celestial Champion":
        print("Boss Kill")
        ctx.bosskills.add(source)
        ctx.bosskills_dirty = True
    else:
        print("Did not find Single")
        collected = []
        num = 1
        while True:
            if ctx.server_location_ids.get(source + " (" + str(num) + ")") != None:
                collected.append(ctx.server_location_ids.get(source + " (" + str(num) + ")"))
                num += 1
            else:
                break
        return collected

async def trytoconnect(ctx, name: str, ip: str, password: str):
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

async def onwaitforconnect(ctx):
    print("onwaitforconnect", ctx.username)
    if not ctx.username:
        await ctx.send_connect()
    else:
        setvariables({'authname': "Nil", 'authip': "Nil", 'connected': True})
        ctx.waitforconnect = False


async def timeoutdisconnect(ctx):
    await ctx.disconnect()

async def manageevent(ctx, event):
    # interfacelog.info("Got event from DST:")
    eventtype = dict.get(event, "datatype")
    if eventtype == "Chat":
        await ctx.send_msgs([{"cmd": "Say", "text": dict.get(event, "msg")}])
    if eventtype == "Join":
        await ctx.send_msgs([{"cmd": "Say", "text": dict.get(event, "msg")}])
    if eventtype == "Leave":
        await ctx.send_msgs([{"cmd": "Say", "text": dict.get(event, "msg")}])
    if eventtype == "Death":
        if "DeathLink" in ctx.tags:
            await ctx.send_death(dict.get(event, "msg"))
            ctx.interfacelog.info("...And so does everyone else.")
        else:
            ctx.interfacelog.info("Death Link is disabled. Everyone is safe... except you.")
    if eventtype == "Item":
        print("  Item:", dict.get(event, "source"))
        locnames = GetTiedLocations(ctx, dict.get(event, "source"))
        if locnames is not None:
            for loc in locnames:
                ctx.locations_checked.add(loc)
        print(ctx.locations_checked)
        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": ctx.locations_checked}])
    if eventtype == "Hint": #I think this should be deterministic enough for races, does not account for manual hints
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

async def onwincondition(ctx):
    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])


async def interface(ctx):
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
                ctx.bosses = ctx.slotdata.get('bosses')
                ctx.SlotDataDirty = False

            elif not ctx.exit_event.is_set() and ctx.QueueDSTState == True:
                sendqueue = getvariables().get('sendqueue')
                sendqueue.append(json.dumps({"datatype": "State", "readyfortraps": True}))

                locations = []
                for locid in ctx.missing_locations:
                    locations.append(ctx.location_names.get(locid))
                if not "Ancient Fuelweaver" in ctx.bosses:
                    locations.append("Ancient Fuelweaver")
                if not "Celestial Champion" in ctx.bosses:
                    locations.append("Celestial Champion")
                sendqueue.append(json.dumps({"datatype": "Locations", "locations": locations}))

                setvariables({"sendqueue": sendqueue})
                ctx.QueueDSTState = False

            elif not ctx.exit_event.is_set() and ctx.ConnectDataDirty == True:
                await ctx.send_msgs([{"cmd": "Get", "keys": [ctx.username + "_locations_scouted"]}])
                await ctx.send_msgs([{"cmd": "Get", "keys": [ctx.username + "_bosskills"]}])
                ctx.ConnectDataDirty = False

            elif not ctx.exit_event.is_set() and ctx.bosskills_dirty == True:
                await ctx.send_msgs([{"cmd": "Set",
                                  "key": ctx.username + "_bosskills",
                                  "operations": [{"operation": "replace", "value": ctx.bosskills}]}])
                
                win = False
                if ctx.bosses == "both":
                    win = ("Ancient Fuelweaver" in ctx.bosskills) and ("Celestial Champion" in ctx.bosskills)
                elif ctx.bosses == "either":
                    win = ("Ancient Fuelweaver" in ctx.bosskills) or ("Celestial Champion" in ctx.bosskills)
                elif ctx.bosses == "ancient_fuelweaver":
                    win = "Ancient Fuelweaver" in ctx.bosskills
                elif ctx.bosses == "celestial_champion":
                    win = "Celestial Champion" in ctx.bosskills

                if win == True:
                    await onwincondition(ctx)
                ctx.bosskills_dirty = False

            elif not ctx.exit_event.is_set() and receivequeue.__len__() > 0: # If Connected and has a event to process
                event = receivequeue.pop(0)
                await manageevent(ctx, event)
                
            if not ctx.exit_event.is_set():
                await asyncio.sleep(0.2)

        ctx.interfacelog.info("Stopping server...")
        setvariables({'serverstopsignel': True})
        Thread.join()
        ctx.interfacelog.info("Server stopped successfully")

    except Exception as e:
        ctx.interfacelog.exception(e)
        ctx.interfacelog.info("Stopping server...")
        setvariables({'serverstopsignel': True})
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

    parser = get_base_parser(description="DST Archipelago Client for interfacing with DST.")
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