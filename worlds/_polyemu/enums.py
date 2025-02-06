from enum import IntEnum


class OperationEnum(IntEnum):
    NO_OP = 0x00
    READ = 0x01
    WRITE = 0x02
    GUARD = 0x03
    LOCK = 0x04
    UNLOCK = 0x05
    PLATFORM = 0x06
    DOMAIN_SIZE = 0x07


class PlatformEnum(int):
    # _domains: tuple[str, ...] = ()
    def __new__(cls, platform_id: int, domains: list[str]):
        obj = int.__new__(cls, platform_id)
        for domain_id, domain_name in enumerate(domains):
            setattr(obj, domain_name, domain_id + 1)
        return obj


class Platforms:
    _platforms = [  # Append only
        ("GBA", ["BIOS", "IWRAM", "EWRAM", "PALRAM", "VRAM", "OAM", "ROM", "SRAM"]),
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
    

PLATFORMS = Platforms()
