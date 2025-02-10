from enum import IntEnum


BROKER_DEVICE_ID = b"\x00\x00\x00\x00\x00\x00\x00\x00"


class PolyEmuRequestType(IntEnum):
    NO_OP = 0x00
    SUPPORTED_OPERATIONS = 0x01
    PLATFORM = 0x02
    MEMORY_SIZE = 0x03
    LIST_DEVICES = 0x04
    READ = 0x10
    WRITE = 0x11
    GUARD = 0x12
    LOCK = 0x20
    UNLOCK = 0x21
    DISPLAY_MESSAGE = 0x22


class PolyEmuResponseType(IntEnum):
    NO_OP = 0x80
    SUPPORTED_OPERATIONS = 0x81
    PLATFORM = 0x82
    MEMORY_SIZE = 0x83
    LIST_DEVICES = 0x84
    READ = 0x90
    WRITE = 0x91
    GUARD = 0x92
    LOCK = 0xA0
    UNLOCK = 0xA1
    DISPLAY_MESSAGE = 0xA2
    ERROR = 0xFF


class PolyEmuErrorType(IntEnum):
    UNKNOWN = 0x00
    UNSUPPORTED_OPERATION = 0x01
    MISMATCHED_DEVICE = 0x02
    NO_SUCH_DEVICE = 0x80
    DEVICE_CLOSED_CONNECTION = 0x81


class PlatformEnum(int):
    def __new__(cls, platform_id: int, domains: list[str]):
        obj = int.__new__(cls, platform_id)
        setattr(obj, "SYSTEM", 0)
        for domain_id, domain_name in enumerate(domains):
            setattr(obj, domain_name, domain_id + 1)
        return obj


class Platforms:
    _platforms = [  # Append only
        ("GB", ["ROM", "VRAM", "SRAM", "WRAM", "OAM", "IO", "HRAM"]),
        ("GBC", ["ROM", "VRAM", "SRAM", "WRAM", "OAM", "IO", "HRAM"]),
        ("GBA", ["BIOS", "EWRAM", "IWRAM", "IO", "PALRAM", "VRAM", "OAM", "ROM", "SRAM"]),
    ]
    _platforms_dict: dict[str, PlatformEnum] = {}

    def __init__(self):
        self._platforms_dict = {
            name: PlatformEnum(i + 1, domains)
            for i, (name, domains)
            in enumerate(self._platforms)
        }

    def __getattr__(self, name):
        if name in self._platforms_dict:
            return self._platforms_dict[name]
        raise AttributeError(f"Unknown platform: {name}")

    def get_by_id(self, platform_id: int):
        return next(platform for platform in self._platforms_dict.values() if platform_id == platform)
    

PLATFORMS = Platforms()
