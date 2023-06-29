from worlds.ladx.LADXR.checkMetadata import checkMetadataTable
import json
import logging
import websockets
import asyncio

logger = logging.getLogger("Tracker")


# kbranch you're a hero
# https://github.com/kbranch/Magpie/blob/master/autotracking/checks.py
class Check:
    def __init__(self, id, address, mask, alternateAddress=None):
        self.id = id
        self.address = address
        self.alternateAddress = alternateAddress
        self.mask = mask
        self.value = None
        self.diff = 0

    def set(self, bytes):
        oldValue = self.value

        self.value = 0

        for byte in bytes:
            maskedByte = byte
            if self.mask:
                maskedByte &= self.mask

            self.value |= int(maskedByte > 0)

        if oldValue != self.value:
            self.diff += self.value - (oldValue or 0)
# Todo: unify this with existing item tables?


class LocationTracker:
    all_checks = []

    def __init__(self, gameboy):
        self.gameboy = gameboy
        maskOverrides = {
            '0x106': 0x20,
            '0x12B': 0x20,
            '0x15A': 0x20,
            '0x166': 0x20,
            '0x185': 0x20,
            '0x1E4': 0x20,
            '0x1BC': 0x20,
            '0x1E0': 0x20,
            '0x1E1': 0x20,
            '0x1E2': 0x20,
            '0x223': 0x20,
            '0x234': 0x20,
            '0x2A3': 0x20,
            '0x2FD': 0x20,
            '0x2A7': 0x20,
            '0x1F5': 0x06,
            '0x301-0': 0x10,
            '0x301-1': 0x10,
        }

        addressOverrides = {
            '0x30A-Owl': 0xDDEA,
            '0x30F-Owl': 0xDDEF,
            '0x308-Owl': 0xDDE8,
            '0x302': 0xDDE2,
            '0x306': 0xDDE6,
            '0x307': 0xDDE7,
            '0x308': 0xDDE8,
            '0x30F': 0xDDEF,
            '0x311': 0xDDF1,
            '0x314': 0xDDF4,
            '0x1F5': 0xDB7D,
            '0x301-0': 0xDDE1,
            '0x301-1': 0xDDE1,
            '0x223': 0xDA2E,
            '0x169': 0xD97C,
            '0x2A7': 0xD800 + 0x2A1
        }

        alternateAddresses = {
            '0x0F2': 0xD8B2,
        }

        blacklist = {'None', '0x2A1-2'}

        # in no dungeons boss shuffle, the d3 boss in d7 set 0x20 in fascade's room (0x1BC)
        # after beating evil eagile in D6, 0x1BC is now 0xAC (other things may have happened in between)
        # entered d3, slime eye flag had already been set (0x15A 0x20). after killing angler fish, bits 0x0C were set
        lowest_check = 0xffff
        highest_check = 0

        for check_id in [x for x in checkMetadataTable if x not in blacklist]:
            room = check_id.split('-')[0]
            mask = 0x10
            address = addressOverrides[check_id] if check_id in addressOverrides else 0xD800 + int(
                room, 16)

            if 'Trade' in check_id or 'Owl' in check_id:
                mask = 0x20

            if check_id in maskOverrides:
                mask = maskOverrides[check_id]

            lowest_check = min(lowest_check, address)
            highest_check = max(highest_check, address)
            if check_id in alternateAddresses:
                lowest_check = min(lowest_check, alternateAddresses[check_id])
                highest_check = max(
                    highest_check, alternateAddresses[check_id])

            check = Check(check_id, address, mask,
                          alternateAddresses[check_id] if check_id in alternateAddresses else None)
            if check_id == '0x2A3':
                self.start_check = check
            self.all_checks.append(check)
        self.remaining_checks = [check for check in self.all_checks]
        self.gameboy.set_cache_limits(
            lowest_check, highest_check - lowest_check + 1)

    def has_start_item(self):
        return self.start_check not in self.remaining_checks

    async def readChecks(self, cb):
        new_checks = []
        for check in self.remaining_checks:
            addresses = [check.address]
            if check.alternateAddress:
                addresses.append(check.alternateAddress)
            bytes = await self.gameboy.read_memory_cache(addresses)
            if not bytes:
                return False
            check.set(list(bytes.values()))

            if check.value:
                self.remaining_checks.remove(check)
                new_checks.append(check)
        if new_checks:
            cb(new_checks)
        return True


class MagpieBridge:
    port = 17026
    server = None
    checks = None
    item_tracker = None
    ws = None
    features = []
    async def handler(self, websocket):
        self.ws = websocket
        while True:
            message = json.loads(await websocket.recv())
            if message["type"] == "handshake":
                logger.info(
                    f"Connected, supported features: {message['features']}")
                self.features = message["features"]

            if message["type"] in ("handshake", "sendFull"):
                if "items" in self.features:
                    await self.send_all_inventory()
                if "checks" in self.features:
                    await self.send_all_checks()
    # Translate renamed IDs back to LADXR IDs
    @staticmethod
    def fixup_id(the_id):
        if the_id == "0x2A1":
            return "0x2A1-0"
        if the_id == "0x2A7":
            return "0x2A1-1"
        return the_id

    async def send_all_checks(self):
        while self.checks == None:
            await asyncio.sleep(0.1)
        logger.info("sending all checks to magpie")

        message = {
            "type": "check",
            "refresh":  True,
            "version": "1.0",
            "diff": False,
            "checks": [{"id": self.fixup_id(check.id), "checked": check.value} for check in self.checks]
        }

        await self.ws.send(json.dumps(message))

    async def send_new_checks(self, checks):
        if not self.ws:
            return

        logger.debug("Sending new {checks} to magpie")
        message = {
            "type": "check",
            "refresh": True,
            "version": "1.0",
            "diff": True,
            "checks": [{"id": self.fixup_id(check), "checked": True} for check in checks]
        }

        await self.ws.send(json.dumps(message))

    async def send_all_inventory(self):
        logger.info("Sending inventory to magpie")

        while self.item_tracker == None:
            await asyncio.sleep(0.1)

        await self.item_tracker.sendItems(self.ws)

    async def send_inventory_diffs(self):
        if not self.ws:
            return
        if not self.item_tracker:
            return
        await self.item_tracker.sendItems(self.ws, diff=True)

    async def send_gps(self, gps):
        if not self.ws:
            return
        await gps.send_location(self.ws)

    async def serve(self):
        async with websockets.serve(lambda w: self.handler(w), "", 17026, logger=logger):
            await asyncio.Future()  # run forever

    def set_checks(self, checks):
        self.checks = checks

    async def set_item_tracker(self, item_tracker):
        stale_tracker = self.item_tracker != item_tracker
        self.item_tracker = item_tracker
        if stale_tracker:
            if self.ws:
                await self.send_all_inventory()
        else:
            await self.send_inventory_diffs()

