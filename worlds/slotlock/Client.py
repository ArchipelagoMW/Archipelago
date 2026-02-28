import re
from . import SlotLockWorld
from CommonClient import ClientCommandProcessor, CommonContext, logger, server_loop, gui_enabled, get_base_parser
from MultiServer import mark_raw
from NetUtils import ClientStatus
from settings import get_settings
try:
    from NetUtils import HintStatus
except ImportError:
    pass
import asyncio
class SlotLockCommandProcessor(ClientCommandProcessor):
    ctx: "SlotLockContext"
    def _cmd_clear_autohint(self):
        """Clear the autohint queue."""
        self.ctx.auto_hint_queue = []
        logger.info("Cleared autohint queue.")
    @mark_raw
    def _cmd_queue_autohint(self, item=None):
        """Queue something to the autohint queue."""
        if item:
            self.ctx.auto_hint_queue.append(item)
        logger.info(f"Autohint queue: {self.ctx.auto_hint_queue}")
        self.ctx.checking_hints = False
    def _cmd_toggle_autohint(self):
        """Toggle the autohint."""
        logger.info(f"Toggling Locked Autohint to {not self.ctx.auto_hint_locked_items}")
        self.ctx.auto_hint_locked_items = not self.ctx.auto_hint_locked_items
        self.ctx.checking_hints =  False
    @mark_raw
    def _cmd_admin(self, password=None):
        """Use admin rights for autohint. This automatically logs into the server. Password defaults to the one in host.yaml."""
        if not password:
            settings = get_settings()
            password = settings.server_options.server_password
        self.ctx.use_server_password = password
        asyncio.create_task(self.ctx.send_msgs([{"cmd": "Say", "text": f"!admin login {password}"}]))
    def _cmd_unlocked_slots(self):
        """List all unlocked slots."""
        for slot in self.ctx.unlocked_slots:
            logger.info(f"{slot}")
    def _cmd_create_tree(self, start=None):
        """Make a tree of all the unlocked slots. Or from the slot that is put in the start, can be None."""
        self.ctx.display_dependencies(start)

class SlotLockContext(CommonContext):

    # Text Mode to use !hint and such with games that have no text entry
    tags = CommonContext.tags
    game = "SlotLock"  # empty matches any game since 0.3.2
    items_handling = 0b111  # receive all items for /received
    want_slot_data = True
    checking_hints = False
    command_processor = SlotLockCommandProcessor
    auto_hint_queue = []
    locked_slots = []
    unlocked_slots = []
    players = {}
    slot_dependency = {} #stores a list of all connections: {2:[1,3], 1:[3]} means 2 unlocks 1 and 3. And 1 also unlocks 3.
    use_server_password = False
    connected = False
    has_hinted = []
    def __init__(self, server_address=None, password=None):
        CommonContext.__init__(self, server_address, password)

    async def server_auth(self, password_requested: bool = False):
        await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()
    async def run_checking_hints(self):
        while True:
            if not self.connected:
                return
            await self.check_hints()
            await asyncio.sleep(1)
    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = "Slotlock Client"
        return ui
    

#    TODO Make a seperate tab for the tree to reside inside of.
#    This code already makes the tab, now the thing needs to fill in.
#    def run_gui(self):
#        from kvui import GameManager
#
#        class SlotlockManager(GameManager):
#            logging_pairs = [
#                ("Client", "Archipelago"),
#                ("SlotlockTree", "Slot Lock Tree"),
#            ]
#            base_title = "Archipelago Slotlock Client"
#
#        self.ui = SlotlockManager(self)
#        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")
    
    async def check_hints(self):
        #print("Checking Hints.")
        if f"_read_hints_{self.team}_{self.slot}" in self.stored_data: #if hints are in the game
            hintdata = self.stored_data[f"_read_hints_{self.team}_{self.slot}"].copy() #make a copy
            for slot in self.player_names:
                player_name = self.player_names[slot]
                if player_name in self.locked_slots and f"_read_hints_{self.team}_{slot}" in self.stored_data:
                    hintdata.extend(self.stored_data[f"_read_hints_{self.team}_{slot}"])
                    #print(f"{player_name}: {self.stored_data[f"_read_hints_{self.team}_{slot}"]}")
                    #if a player is locked. Add the hints of that player to the hint data.
            hinted_count = {}
            loc_count = {}
            for location in self.server_locations:
                if location // 10 in loc_count:
                    loc_count[location // 10] += 1
                else:
                    loc_count[location // 10] = 1
            for hint in hintdata:
                if self.slot_concerns_self(hint["receiving_player"]): #if a hint is for slotlock
                    if hint["item"] not in hinted_count:
                        hinted_count[hint["item"]] = 1
                    else:
                        hinted_count[hint["item"]] += 1 #count how often the item is hinted for.
                    if any(item.item == hint["item"] for item in self.items_received):
                        if hasattr(self, "update_hint") and hint["status"] == HintStatus.HINT_PRIORITY:
                            self.update_hint(hint["location"],hint["finding_player"], HintStatus.HINT_NO_PRIORITY)
                            # remove prio if an item has alreay found.
            if len(self.auto_hint_queue) > 0:
                await self.send_hint(self.auto_hint_queue.pop(0)) #send a hint that is in the hint queue.
                await asyncio.sleep(1)
                self.checking_hints = False
                return
            if self.auto_hint_locked_items:
                for hint in hintdata:
                    if self.slot_concerns_self(hint["finding_player"]):
                        if hint["location"]//10 not in hinted_count:
                            hinted_count[hint["location"]// 10] = 0
                        if (not "status" in hint) or hint["status"] == HintStatus.HINT_PRIORITY:
                            if not hint["found"] and hinted_count[hint["location"]//10] < 1:
                                await self.send_hint(self.item_names.lookup_in_game(hint["location"]//10, "SlotLock"))
                                self.checking_hints = False
                                await asyncio.sleep(2)
                                return
                    elif hint["finding_player"] in self.locked_slots_nums:
                        if (not "status" in hint) or hint["status"] == HintStatus.HINT_PRIORITY:
                            if (not hint["found"]):
                                hinted = False
                                for ahint in hintdata:
                                    if self.slot_concerns_self(ahint["receiving_player"]) and ahint["item"] == hint["finding_player"]+1001:
                                        hinted = True
                                print(f"Already hinted for {hint}: {hinted}")
                                if not hinted:
                                    await self.send_hint(f"Unlock {self.player_names[hint['finding_player']]}")
                                    await asyncio.sleep(2)
                                    return
                            else:
                                pass
                                #print(f"Skipping hint: {hint} because not enough hint points or hint already found. ")
                        else:
                            pass
                            #print(f"Skipping hint: {hint} because not priority.")
        await asyncio.sleep(1)
    async def send_hint(self, item_name):
        if item_name in self.has_hinted:
            return
        self.has_hinted.append(item_name)
        for loc in self.item_locations[item_name]:
            print(f"{item_name}, {loc}")
            await self.send_msgs([{"cmd": "CreateHints", "player": loc[0], "locations": [loc[1]]}])
    def update_auto_locations(self):
        self.unlocked_slots = []
        received_items = [*map(lambda item: self.item_names.lookup_in_game(item.item, "SlotLock"), self.items_received)]
        print(received_items)
        for slot in self.player_names.values():
            if f"Unlock {slot}" in received_items:
                self.unlocked_slots.append(slot)
        self.locations_checked = set()
        for location in self.missing_locations:
            if any(item.item == location // 10 for item in self.items_received) or (location >= 10000 and self.free_starting_items):
                self.locations_checked.add(location)
            else:
                logger.debug(f"Don't yet have {self.location_names.lookup_in_game(location,"SlotLock")}, required item {self.item_names.lookup_in_game(location // 10)}")
                pass

    # TODO: add some logic to find if the item comes from a SlotLock. And then route the dependency from Slotlock to the game Slotlock gets the check from.
    # update the slot_dependency list with the information from the hints.
    def update_dependency_hint(self):
        if f"_read_hints_{self.team}_{self.slot}" in self.stored_data:
            for hint in self.stored_data[f"_read_hints_{self.team}_{self.slot}"]: #loop though all hints
                item_name = self.item_names.lookup_in_game(hint["item"])
                if re.match(r"Unlock ", item_name):
                    player_name = re.sub(r"Unlock ", "", item_name)
                    for player in self.players:
                        #players: 0 = team, 1 = slot, 2 = alias, 3 = name
                        if player_name == player[3]:
                            if hint["finding_player"] in self.slot_dependency:
                                if not player[1] in self.slot_dependency[hint["finding_player"]]:
                                    self.slot_dependency[hint["finding_player"]].append(player[1])
                            else:
                                self.slot_dependency[hint["finding_player"]] = [player[1]]
                            break
        
    
    # update the slot_dependency list with the information from the recieved items.
    def update_dependency_items(self):
        if self.slot_dependency == {}: #This if statement will ensure that this slot will be the fist on the list. Ensuring that it will be the first to be displayed.
            for slot in self.players:
                #players: 0 = team, 1 = slot, 2 = alias, 3 = name
                if slot[1] == self.slot: #if it is this slot.
                    for item in self.items_received:
                        item_name = self.item_names.lookup_in_game(item.item, "SlotLock")
                        if f"Unlock {slot[3]}" == item_name: #find where this slot was found, likely from slot 0; archipelago.
                            if item.player in self.slot_dependency:
                                if not slot[1] in self.slot_dependency[item.player]:
                                    self.slot_dependency[item.player].append(slot[1])
                            else:
                                self.slot_dependency[item.player] = [slot[1]]
                            break
                    break
        for item in self.items_received:
            item_name = self.item_names.lookup_in_game(item.item, "SlotLock")
            for slot in self.players:
                #players: 0 = team, 1 = slot, 2 = alias, 3 = name
                if f"Unlock {slot[3]}" == item_name:
                    if item.player in self.slot_dependency:
                        if not slot[1] in self.slot_dependency[item.player]:
                            self.slot_dependency[item.player].append(slot[1])
                    else:
                        self.slot_dependency[item.player] = [slot[1]]
                    break

    #start the display sequence. 
    def display_dependencies(self, named):
        
        temp_slot_dependency =  {k: v.copy() for k, v in self.slot_dependency.items()}
        temp_slot_dependency[0] = temp_slot_dependency[0] or []
        temp_slot_dependency[-1] = []
        for key_holder in self.slot_dependency:
            cages = self.slot_dependency[key_holder]
            nothing = True
            for key_holder_2 in self.slot_dependency:
                if (key_holder in self.slot_dependency[key_holder_2]):
                    nothing = False
                    break
            if nothing and key_holder > 1:
                temp_slot_dependency[-1].append(key_holder) #add temp exta things for unhinted games. So they show up as mystery.

        named_num = -1
        named_is_mystery = True
        if not named == None:
            for player in self.players: 
                if named == player[3]: # find the info on this slot.
                    named_num = player[1]
                    break
            if named_num == -1:
                for player in self.players: 
                    if named == player[2]: # find the info on this slot.
                        named_num = player[1]
                        break
            if named_num == -1:
                logger.info(f"The slot {named} was not found in both the names and the aliases. The search is case sensitive.")
                return
            
            for key_holder in self.slot_dependency:
                if (named_num in self.slot_dependency[key_holder]):
                    named_is_mystery = False
                    break

            if not named_num in temp_slot_dependency[0]:
                temp_slot_dependency[-1] = [named_num]


        for key_holder in [0,-1]:
            cages = temp_slot_dependency[key_holder]
            for cage in cages:
                if named == None or named_num == cage: #if this slot does not yet have a known game that unlocks it.
                    cage_name = ""
                    for player in self.players: 
                        if cage == player[1]: # find the info on this slot.
                            cage_name = player[2]
                            break
                    if cage_name in self.unlocked_slots or self.slot == cage: #Display the correct game name with current state
                        logger.info(f"{cage_name}     (Unlocked)")
                    elif key_holder == -1 and named == None or named_is_mystery:
                        logger.info(f"{cage_name}     (Mystery)")
                    else:
                        logger.info(f"{cage_name}     (Hinted)")
                    temp_2_slot_dependency = {k: v.copy() for k, v in temp_slot_dependency.items()}
                    temp_2_slot_dependency[key_holder].remove(cage)
                    if cage in temp_2_slot_dependency:
                        self.recusion_display(temp_2_slot_dependency, cage, "  |  ") #Start the recusion with a sinlge bar.

    def recusion_display(self, temp_slot_dependency: dict, this_layer, depth):
        cages = temp_slot_dependency[this_layer]
        for cage in cages:
            cage_name = ""
            for player in self.players: 
                if cage == player[1]: # find the info on this slot.
                    cage_name = player[2]
                    break
            if cage_name in self.unlocked_slots: #Display the correct game name with current state and extra depth
                logger.info(f"{depth}{cage_name}     (Unlocked)")
            else:
                logger.info(f"{depth}{cage_name}     (Hinted)")
            temp_2_slot_dependency = {k: v.copy() for k, v in temp_slot_dependency.items()}
            temp_2_slot_dependency[this_layer].remove(cage)
            if cage in temp_2_slot_dependency:
                self.recusion_display(temp_2_slot_dependency, cage, depth + "  |  ") #do more recursion with an extra line.

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            self.game = self.slot_info[self.slot].game
            self.free_starting_items = args["slot_data"]["free_starting_items"]
            self.locked_slots = args["slot_data"]["locked_slots"]
            self.unlock_item_copies = args["slot_data"]["unlock_item_copies"]
            self.unlock_item_filler = args["slot_data"]["unlock_item_filler"]
            self.bonus_item_slots = args["slot_data"]["bonus_item_slots"]
            self.bonus_item_copies = args["slot_data"]["bonus_item_copies"]
            self.bonus_item_filler = args["slot_data"]["bonus_item_filler"]
            self.item_locations = args["slot_data"]["item_locations"]
            self.connected = True
            self.slot_dependency = {}
            asyncio.create_task(self.run_checking_hints())
            try:
                self.auto_hint_locked_items = args["slot_data"]["auto_hint_locked_items"]
                if self.auto_hint_locked_items == 2:
                    self.auto_hint_locked_items = True
                    self.use_server_password = True
                    self.command_processor(self)._cmd_admin()
            except KeyError:
                self.auto_hint_locked_items = False
            self.locked_slots_nums = []
            for slot in self.player_names:
                player_name = self.player_names[slot]
                if player_name in self.locked_slots:
                    self.locked_slots_nums.append(slot)
            slots = [*map(lambda slot: f"_read_hints_{self.team}_{slot}",self.locked_slots_nums)]
            for slot in slots:
                self.set_notify(slot)
        if cmd == "ReceivedItems" or cmd == "Connected" or cmd == "RoomUpdate":
            self.update_auto_locations()
            self.update_dependency_items()
            asyncio.create_task(self.send_msgs([{"cmd": "LocationChecks",
                         "locations": list(self.locations_checked)}]))
            victory = True
            if len(self.missing_locations) > 0:
                victory = False
            else:
                for i, name in self.player_names.items():
                    success = False
                    for item in self.items_received:
                        print(item)
                        if i == 0 or item.item == i + 1001:
                            success = True
                    if not success:
                        print(f"No victory yet, {name} unlock required. Item ID {i + 1001}")
                        victory = False
            if victory:
                print("Victory!")
                self.finished_game = True
                asyncio.create_task(self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}]))
                
            if "players" in args:
                self.players = args["players"]
                
        elif cmd == "Retrieved":
            if f"_read_hints_{self.team}_{self.slot}" in args["keys"]:
                self.update_dependency_hint()

        elif cmd == "SetReply":
            if f"_read_hints_{self.team}_{self.slot}" == args["key"]:
                self.update_dependency_hint()


    async def disconnect(self, allow_autoreconnect: bool = False):
        await super().disconnect(allow_autoreconnect)
        self.finished_game = False
        self.free_starting_items = False
        self.auto_hint_locked_items = False
        self.checked_locations = set()
        self.locations_checked = set()
        self.items_received = []
        self.update_auto_locations()

def launch(*args):

    async def main(args):
        ctx = SlotLockContext(args.connect, args.password)
        ctx.auth = args.name
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    import colorama

    parser = get_base_parser(description="SlotLock Archipelago Client, for text interfacing.")
    parser.add_argument('--name', default=None, help="Slot Name to connect as.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")
    args = parser.parse_args(args)

    # handle if text client is launched using the "archipelago://name:pass@host:port" url from webhost
    if args.url:
        import urllib
        url = urllib.parse.urlparse(args.url)
        if url.scheme == "archipelago":
            args.connect = url.netloc
            if url.username:
                args.name = urllib.parse.unquote(url.username)
            if url.password:
                args.password = urllib.parse.unquote(url.password)
        else:
            parser.error(f"bad url, found {args.url}, expected url in form of archipelago://archipelago.gg:38281")

    # use colorama to display colored text highlighting on windows
    colorama.init()

    asyncio.run(main(args))
    colorama.deinit()
