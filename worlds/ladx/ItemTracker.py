import json

inventorySlotCount = 16
inventoryStartAddress = 0xDB00
inventoryEndAddress = inventoryStartAddress + inventorySlotCount

rupeesHigh = 0xDB5D
rupeesLow = 0xDB5E
addRupeesHigh = 0xDB8F
addRupeesLow = 0xDB90
removeRupeesHigh = 0xDB91
removeRupeesLow = 0xDB92

inventoryItemIds = {
    0x02: 'BOMB',
    0x05: 'BOW',
    0x06: 'HOOKSHOT',
    0x07: 'MAGIC_ROD',
    0x08: 'PEGASUS_BOOTS',
    0x09: 'OCARINA',
    0x0A: 'FEATHER',
    0x0B: 'SHOVEL',
    0x0C: 'MAGIC_POWDER',
    0x0D: 'BOOMERANG',
    0x0E: 'TOADSTOOL',
    0x0F: 'ROOSTER',
}

dungeonKeyDoors = [
    { # D1
        0xD907: [0x04],
        0xD909: [0x40],
        0xD90F: [0x01],
    },
    { # D2
        0xD921: [0x02],
        0xD925: [0x02],
        0xD931: [0x02],
        0xD932: [0x08],
        0xD935: [0x04],
    },
    { # D3
        0xD945: [0x40],
        0xD946: [0x40],
        0xD949: [0x40],
        0xD94A: [0x40],
        0xD956: [0x01, 0x02, 0x04, 0x08],
    },
    { # D4
        0xD969: [0x04],
        0xD96A: [0x40],
        0xD96E: [0x40],
        0xD978: [0x01],
        0xD979: [0x04],
    },
    { # D5
        0xD98C: [0x40],
        0xD994: [0x40],
        0xD99F: [0x04],
    },
    { # D6
        0xD9C3: [0x40],
        0xD9C6: [0x40],
        0xD9D0: [0x04],
    },
    { # D7
        0xDA10: [0x04],
        0xDA1E: [0x40],
        0xDA21: [0x40],
    },
    { # D8
        0xDA39: [0x02],
        0xDA3B: [0x01],
        0xDA42: [0x40],
        0xDA43: [0x40],
        0xDA44: [0x40],
        0xDA49: [0x40],
        0xDA4A: [0x01],
    },
    { # D0(9)
        0xDDE5: [0x02],
        0xDDE9: [0x04],
        0xDDF0: [0x04],
    },
]

dungeonItemAddresses = [
    0xDB16, # D1
    0xDB1B, # D2
    0xDB20, # D3
    0xDB25, # D4
    0xDB2A, # D5
    0xDB2F, # D6
    0xDB34, # D7
    0xDB39, # D8
    0xDDDA, # Color Dungeon
]

dungeonItemOffsets = {
    'MAP{}': 0,
    'COMPASS{}': 1,
    'STONE_BEAK{}': 2,
    'NIGHTMARE_KEY{}': 3,
    'KEY{}': 4,
    'UNUSED_KEY{}': 4,
}

class Item:
    def __init__(self, id, address, threshold=0, mask=None, increaseOnly=False, count=False, max=None, encodedCount=True):
        self.id = id
        self.address = address
        self.threshold = threshold
        self.mask = mask
        self.increaseOnly = increaseOnly
        self.count = count
        self.value = 0 if increaseOnly else None
        self.rawValue = 0
        self.diff = 0
        self.max = max
        self.encodedCount = encodedCount

    def set(self, byte, extra):
        oldValue = self.value

        if self.mask:
            byte = byte & self.mask
        
        if not self.count:
            byte = int(byte > self.threshold)
        elif self.encodedCount:
            # LADX seems to store one decimal digit per nibble
            byte = byte - (byte // 16 * 6)
        
        byte += extra
        
        if self.max and byte > self.max:
            byte = self.max

        if self.increaseOnly:
            if byte > self.rawValue:
                self.value += byte - self.rawValue
        else:
            self.value = byte
        
        self.rawValue = byte

        if oldValue != self.value:
            self.diff += self.value - (oldValue or 0)

class ItemTracker:
    def __init__(self, gameboy) -> None:
        self.gameboy = gameboy
        self.loadItems()
        pass
    extraItems = {}

    async def readRamByte(self, byte):
        return (await self.gameboy.read_memory_cache([byte]))[byte]

    def loadItems(self):
        self.items = [
            Item('BOMB', None),
            Item('BOW', None),
            Item('HOOKSHOT', None),
            Item('MAGIC_ROD', None),
            Item('PEGASUS_BOOTS', None),
            Item('OCARINA', None),
            Item('FEATHER', None),
            Item('SHOVEL', None),
            Item('MAGIC_POWDER', None),
            Item('BOOMERANG', None),
            Item('TOADSTOOL', None),
            Item('ROOSTER', None),
            Item('RUPEE_COUNT', None, count=True, encodedCount=False),
            Item('SWORD', 0xDB4E, count=True),
            Item('POWER_BRACELET', 0xDB43, count=True),
            Item('SHIELD', 0xDB44, count=True),
            Item('BOWWOW', 0xDB56),
            Item('MAX_POWDER_UPGRADE', 0xDB76, threshold=0x20),
            Item('MAX_BOMBS_UPGRADE', 0xDB77, threshold=0x30),
            Item('MAX_ARROWS_UPGRADE', 0xDB78, threshold=0x30),
            Item('TAIL_KEY', 0xDB11),
            Item('SLIME_KEY', 0xDB15),
            Item('ANGLER_KEY', 0xDB12),
            Item('FACE_KEY', 0xDB13),
            Item('BIRD_KEY', 0xDB14),
            Item('FLIPPERS', 0xDB3E),
            Item('SEASHELL', 0xDB41, count=True),
            Item('GOLD_LEAF', 0xDB42, count=True, max=5),
            Item('INSTRUMENT1', 0xDB65, mask=1 << 1),
            Item('INSTRUMENT2', 0xDB66, mask=1 << 1),
            Item('INSTRUMENT3', 0xDB67, mask=1 << 1),
            Item('INSTRUMENT4', 0xDB68, mask=1 << 1),
            Item('INSTRUMENT5', 0xDB69, mask=1 << 1),
            Item('INSTRUMENT6', 0xDB6A, mask=1 << 1),
            Item('INSTRUMENT7', 0xDB6B, mask=1 << 1),
            Item('INSTRUMENT8', 0xDB6C, mask=1 << 1),
            Item('TRADING_ITEM_YOSHI_DOLL', 0xDB40, mask=1 << 0),
            Item('TRADING_ITEM_RIBBON', 0xDB40, mask=1 << 1),
            Item('TRADING_ITEM_DOG_FOOD', 0xDB40, mask=1 << 2),
            Item('TRADING_ITEM_BANANAS', 0xDB40, mask=1 << 3),
            Item('TRADING_ITEM_STICK', 0xDB40, mask=1 << 4),
            Item('TRADING_ITEM_HONEYCOMB', 0xDB40, mask=1 << 5),
            Item('TRADING_ITEM_PINEAPPLE', 0xDB40, mask=1 << 6),
            Item('TRADING_ITEM_HIBISCUS', 0xDB40, mask=1 << 7),
            Item('TRADING_ITEM_LETTER', 0xDB7F, mask=1 << 0),
            Item('TRADING_ITEM_BROOM', 0xDB7F, mask=1 << 1),
            Item('TRADING_ITEM_FISHING_HOOK', 0xDB7F, mask=1 << 2),
            Item('TRADING_ITEM_NECKLACE', 0xDB7F, mask=1 << 3),
            Item('TRADING_ITEM_SCALE', 0xDB7F, mask=1 << 4),
            Item('TRADING_ITEM_MAGNIFYING_GLASS', 0xDB7F, mask=1 << 5),
            Item('SONG1', 0xDB49, mask=1 << 2),
            Item('SONG2', 0xDB49, mask=1 << 1),
            Item('SONG3', 0xDB49, mask=1 << 0),
            Item('RED_TUNIC', 0xDB6D, mask=1 << 0),
            Item('BLUE_TUNIC', 0xDB6D, mask=1 << 1),
            Item('GREAT_FAIRY', 0xDDE1, mask=1 << 4),
        ]

        for i in range(len(dungeonItemAddresses)):
            for item, offset in dungeonItemOffsets.items():
                if item.startswith('KEY'):
                    self.items.append(Item(item.format(i + 1), dungeonItemAddresses[i] + offset, count=True))
                else:
                    self.items.append(Item(item.format(i + 1), dungeonItemAddresses[i] + offset))

        self.itemDict = {item.id: item for item in self.items}

    async def readItems(self):
        extraItems = self.extraItems
        missingItems = {x for x in self.items if x.address == None and x.id != 'RUPEE_COUNT'}
        
        # Add keys for opened key doors
        for i in range(len(dungeonKeyDoors)):
            item = f'KEY{i + 1}'
            extraItems[item] = 0

            for address, masks in dungeonKeyDoors[i].items():
                for mask in masks:
                    value = await self.readRamByte(address) & mask
                    if value > 0:
                        extraItems[item] += 1

        # Main inventory items
        for i in range(inventoryStartAddress, inventoryEndAddress):
            value = await self.readRamByte(i)

            if value in inventoryItemIds:
                item = self.itemDict[inventoryItemIds[value]]
                extra = extraItems[item.id] if item.id in extraItems else 0
                item.set(1, extra)
                missingItems.remove(item)
        
        for item in missingItems:
            extra = extraItems[item.id] if item.id in extraItems else 0
            item.set(0, extra)
        
        # All other items
        for item in [x for x in self.items if x.address]:
            extra = extraItems[item.id] if item.id in extraItems else 0
            item.set(await self.readRamByte(item.address), extra)
        
        # The current rupee count is BCD, but the add/remove values are not
        currentRupees = self.calculateRupeeCount(await self.readRamByte(rupeesHigh), await self.readRamByte(rupeesLow))
        addingRupees = (await self.readRamByte(addRupeesHigh) << 8) +  await self.readRamByte(addRupeesLow)
        removingRupees = (await self.readRamByte(removeRupeesHigh) << 8) + await self.readRamByte(removeRupeesLow)
        self.itemDict['RUPEE_COUNT'].set(currentRupees + addingRupees - removingRupees, 0)
    
    def calculateRupeeCount(self, high: int, low: int) -> int:
        return (high - (high // 16 * 6)) * 100 + (low - (low // 16 * 6))
    
    def setExtraItem(self, item: str, qty: int) -> None:
        self.extraItems[item] = qty

    async def sendItems(self, socket, diff=False):
        if not self.items: 
            return
        message = {
            "type":"item",
            "refresh": True,
            "diff": diff,
            "items": [],
        }
        items = self.items
        if diff:
            items = [item for item in items if item.diff != 0]
        if not items:
            return
        for item in items:
            value = item.diff if diff else item.value

            message["items"].append(
                {
                    'id': item.id,
                    'qty': value,
                }
            )

            item.diff = 0
        
        await socket.send(json.dumps(message))