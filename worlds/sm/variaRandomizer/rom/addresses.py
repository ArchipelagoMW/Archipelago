from .addressTypes import ValueList, ValueSingle, ValueRange, Byte, Word, Long
from .objectivesAddresses import objectivesAddr

# TODO::add patches


class Addresses(object):
    @staticmethod
    def getOne(key):
        value = Addresses.addresses[key]
        return value.getOne()

    @staticmethod
    def getAll(key):
        value = Addresses.addresses[key]
        return value.getAll()

    @staticmethod
    def getWeb(key):
        value = Addresses.addresses[key]
        return value.getWeb()

    @staticmethod
    def getRange(key):
        value = Addresses.addresses[key]
        return value.getWeb()

    addresses = {
        'totalItems': ValueList([0x8BE656, 0x8BE6B3], storage=Byte),
        'majorsSplit': ValueSingle(0x82fb6c, storage=Byte),
        # scavenger hunt items list (17 prog items (including ridley) + hunt over + terminator, each is a word)
        'scavengerOrder': ValueRange(0xA1F5D8, length=(17+1+1)*2),
        'plandoAddresses': ValueRange(0xdee000, length=128),
        'plandoTransitions': ValueSingle(0xdee100),
        'escapeTimer': ValueSingle(0x809e21),
        'escapeTimerTable': ValueSingle(0xA1F0AA),
        'startAP': ValueSingle(0xa1f200),
        'customDoorsAsm': ValueSingle(0x8ff800),
        'locIdsByArea': ValueRange(0xA1F568, end=0xA1F5D7),
        'plmSpawnTable': ValueSingle(0x8fe9a0),
        'plmSpawnRoomTable': ValueSingle(0x8ff000),
        'moonwalk': ValueSingle(0x81b35d),
        'additionalETanks': ValueSingle(0xA1F470, storage=Byte),
        'hellrunRate': ValueSingle(0x8DE387),
        'BTtweaksHack1': ValueSingle(0x84ba6f+3),
        'BTtweaksHack2': ValueSingle(0x84d33b+3),
        # in intro_text.ips
        'introText': ValueSingle(0x8cc389)
    }

Addresses.addresses.update(objectivesAddr)
