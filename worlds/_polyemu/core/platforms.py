from typing import ClassVar


__all__ = [
    "PLATFORMS",
]


class PlatformBase:
    _ID: ClassVar[int]
    SYSTEM = 0x00


class GB(PlatformBase):
    _ID = 0x01

    ROM = 0x01
    VRAM = 0x02
    SRAM = 0x03
    WRAM = 0x04
    OAM = 0x05
    IO = 0x06
    HRAM = 0x07


class GBC(PlatformBase):
    _ID = 0x02

    ROM = 0x01
    VRAM = 0x02
    SRAM = 0x03
    WRAM = 0x04
    OAM = 0x05
    IO = 0x06
    HRAM = 0x07


class GBA(PlatformBase):
    _ID = 0x03

    BIOS = 0x01
    EWRAM = 0x02
    IWRAM = 0x03
    IO = 0x04
    PALRAM = 0x05
    VRAM = 0x06
    OAM = 0x07
    ROM = 0x08
    SRAM = 0x09


# I don't know what I'm doing here
class SNES(PlatformBase):
    _ID = 0x04

    ROM = 0x01
    SRAM = 0x02
    WRAM = 0x03
    VRAM = 0x04
    APU = 0x05
    CGRAM = 0x06
    OAM = 0x07
    MISC = 0x08


class PLATFORMS:
    GB = GB
    GBC = GBC
    GBA = GBA
    SNES = SNES

    @staticmethod
    def cast_to_int(value: int | type[PlatformBase]):
        if isinstance(value, int):
            return value
        return value._ID


# Check namespaces for collisions
platform_ids: dict[int, str] = {}
for platforms_attribute_name, platform_class in PLATFORMS.__dict__.items():
    if isinstance(platform_class, type) and issubclass(platform_class, PlatformBase):
        platform_id = platform_class._ID
        if platform_id in platform_ids:
            raise AssertionError(f"Platforms {platforms_attribute_name} and {platform_ids[platform_id]} cannot use the same ID: {platform_id}")

        domain_ids: dict[int, str] = {}
        for platform_attribute_name, domain_id in platform_class.__dict__.items():
            if not platform_attribute_name.startswith("_"):
                if domain_id in domain_ids:
                    raise AssertionError(f"Domains {platform_attribute_name} and {domain_ids[domain_id]} for platform {platforms_attribute_name} cannot use the same ID: {domain_id}")
                domain_ids[domain_id] = platform_attribute_name

        platform_ids[platform_id] = platforms_attribute_name
