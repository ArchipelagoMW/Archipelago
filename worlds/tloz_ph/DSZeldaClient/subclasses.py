from enum import IntEnum
from typing import TYPE_CHECKING
import worlds._bizhawk as bizhawk

if TYPE_CHECKING:
    try:
        from ..Client import PhantomHourglassClient
    except ImportError:
        pass

async def read_multiple(ctx, addresses, signed=False, keys=None) -> dict["Address", int] or dict[str, int]:
    reads = await bizhawk.read(ctx.bizhawk_ctx, [a.get_inner_read_list() for a in addresses])
    reads = [int.from_bytes(r, "little", signed=signed) for r in reads]
    if keys:
        return {k: r for k, r in zip(keys, reads)}
    return {a: r for a, r in zip(addresses, reads)}

async def write_multiple(ctx, addresses, values):
    writes = [a.overwrite(ctx, v) for a, v in zip(addresses, values)]
    await bizhawk.write(ctx.bizhawk_ctx, writes)


# Get address from pointer
async def get_address_from_heap(ctx, pointer, offset=0, size=4) -> "Address":
    """
    Reads a pointer, and follows that pointer with an offset
    :param size: how many bytes
    :param ctx:
    :param pointer:
    :param offset:
    :return:
    """
    m_course = 0
    while m_course == 0:
        m_course = await pointer.read(ctx)
    m_course = AddrFromPointer(m_course - 0x02000000, size=4)
    read = await m_course.read(ctx)
    print(f"Got map address @ {hex(read + offset - 0x02000000)}")
    return AddrFromPointer(read + offset - 0x02000000, size=size)

def storage_key(ctx, key: str):
    return f"{key}_{ctx.slot}_{ctx.team}"

def get_stored_data(ctx, key, default=None):
    store = ctx.stored_data.get(storage_key(ctx, key), default)
    store = store if store is not None else default
    return store

# Split up large values to write into smaller chunks
def split_bits(value, size):
    ret = []
    f = 0xFFFFFFFFFFFFFF00
    for _ in range(size):
        ret.append(value & 0xFF)
        value = (value & f) >> 8
    return ret

all_addresses = []

class Address:
    addr_eu: int
    addr_us: int
    addr: int
    current_region: int
    domain: str
    size: int
    offset: int
    name: str
    all_addresses: list = all_addresses

    def __init__(self, addr_eu, addr_us=None, size=1, domain="Main RAM", name=""):
        if domain == "Main RAM":
            assert addr_eu < 0x400000
        self.addr_eu = addr_eu
        self.addr_us = addr_us if addr_us else None
        self.addr_lookup = [self.addr_eu, self.addr_us]
        self.addr = self.addr_eu

        self.current_region = 0
        self.domain = domain
        self.size = size
        self.name = name

        self.all_addresses.append(self)

    def set_region(self, region: str or int):
        self.current_region = self._region_int(region)
        self.addr = self.addr_lookup[self.current_region]

    @staticmethod
    def _region_int(region: str or int):
        if isinstance(region, str):
            assert region.lower() in ["eu", "us"]
            region = ["eu", "us"].index(region.lower())
        assert region in [0, 1]
        return region

    def get_address(self, region=None):
        if region is not None:
            region = self._region_int(region)
            return self.addr_lookup[region]
        return self.addr

    def get_read_list(self):
        return [self.get_inner_read_list()]

    def get_inner_read_list(self) -> tuple:
        return self.addr, self.size, self.domain

    def get_write_list(self, value:int or list):
        return [self.get_inner_write_list(value)]

    def get_inner_write_list(self, value:int or list):
        if isinstance(value, int):
            value = split_bits(value, self.size)
        return self.addr, value[:self.size], self.domain

    async def read(self, ctx, signed=False, silent=False):
        read_result = await self.read_bytes(ctx)
        res = sum([int.from_bytes(b, "little", signed=signed)<<(8*i) for i, b in enumerate(read_result)])
        if not silent:
            print(f"\tReading address {self}, got value {res}")
        return res

    async def read_bytes(self, ctx):
        return await bizhawk.read(ctx.bizhawk_ctx, [(self.addr, self.size, self.domain)])

    async def overwrite(self, ctx, value, silent=False, offset=0):
        if isinstance(value, int):
            value = split_bits(value, self.size)
        if not silent:
            print(f"\tWriting to address {self} with value {value}")
        return await bizhawk.write(ctx.bizhawk_ctx, [(self.addr+offset, value, self.domain)])

    async def add(self, ctx, value: int, silent=False, offset=0):
        prev = await self.read(ctx, silent=silent)
        return await self.overwrite(ctx, prev + value, silent=silent, offset=offset)

    async def set_bits(self, ctx, value: int or list, silent=False, offset=0):
        if isinstance(value, int):
            value = split_bits(value, self.size)
        prev = split_bits(await self.read(ctx, silent=silent), self.size)
        # print(f"Setting bits {self} {prev} {value} {[p | v for p, v in zip(prev, value)]}")
        return await self.overwrite(ctx, [p | v for p, v in zip(prev, value)], silent=silent, offset=offset)

    async def unset_bits(self, ctx, value: int or list, silent=False, offset=0):
        if isinstance(value, int):
            value = split_bits(value, self.size)
        prev = split_bits(await self.read(ctx, silent=silent), self.size)
        # print(f"Setting bits {self} {prev} {value} {[p | v for p, v in zip(prev, value)]}")
        return await self.overwrite(ctx, [p & (~v) for p, v in zip(prev, value)], silent=silent, offset=offset)


    def __repr__(self, region="eu"):
        return f"Address Object {hex(self.get_address(region))} {self.name}"

    def __str__(self):
        name = f"{self.name}: " if self.name else ""
        return f"{name}{hex(self.get_address())}"

    def __add__(self, other):
        return self.addr + other

    def __sub__(self, other):
        if isinstance(other, Address):
            return self.addr - other.addr
        return self.addr - other

    def __eq__(self, other):
        return self.addr == other

    def __ne__(self, other):
        return self.addr != other

    def __bool__(self):
        return bool(self.addr)

    def __hash__(self):
        return self.addr

    def __gt__(self, other):
        return self.addr > other

    def __lt__(self, other):
        return self.addr < other

    def __ge__(self, other):
        return self.addr >= other

    def __le__(self, other):
        return self.addr <= other

class Pointer(Address):
    """
    Pointer from Data TCM
    """

    def __init__(self, addr, name=""):
        super().__init__(addr, addr, 4, "Data TCM", name)


class AddrFromPointer(Address):
    """
    When addresses are grabbed from pointers, version doesn't matter.
    """

    def __init__(self, addr, size=1, domain="Main RAM", name=""):
        super().__init__(addr, addr, size, domain, name)

class SRAM(Address):
    """
    Saveram also has slot data to care about.
    """

    def __init__(self, addr_eu_1, addr_eu_2=None, addr_us_1=None, addr_us_2=None, name=""):
        super().__init__(addr_eu_1, addr_us_1, size=1, domain="SRAM", name=name)
        self.slot = 0
        self.addr_lookup = [(addr_eu_1, addr_eu_2), (addr_us_1, addr_us_2)]


    async def read(self, ctx, signed=False, silent=False, slot=0):
        addr = self.addr_lookup[self.current_region][self.slot]
        read_result = await bizhawk.read(ctx.bizhawk_ctx, [(addr, self.size, self.domain)])
        res = int.from_bytes(read_result[0], "little", signed=signed)
        if not silent:
            print(f"\tReading address {self}, got value {hex(res)}")
        return res

class DSTransition:
    """
    Datastructures for dealing with Transitions on the client side.
    Not to be confused with PHEntrances, that deals with entrance objects during ER placement.
    """
    entrance_groups: IntEnum | None = None  # set these in game instance or
    opposite_entrance_groups: dict[IntEnum, IntEnum] | None = None

    def __init__(self, name, data):
        self.data = data

        self.name: str = name
        self.id: int = data.get("id", None)
        assert self.id is not None

        self.entrance: tuple = data.get("entrance", None)
        self.exit: tuple = data.get("exit", None)
        self.entrance_region: str = data["entrance_region"]
        self.exit_region: str = data["exit_region"]
        self.two_way: bool = data.get("two_way", True)
        self.category_group = data["type"]
        self.direction = data["direction"]
        self.island = data.get("island", self.entrance_groups.NONE if self.entrance_groups else None)
        self.coords: tuple | None = data.get("coords", None)
        self.extra_data: dict = data.get("extra_data", {})

        self.stage, self.room, _ = self.entrance if self.entrance else (None, None, None)
        self.scene: int = self.get_scene()
        self.exit_scene: int = self.get_exit_scene()
        self.exit_stage = self.exit[0] if self.exit else None
        self.y = self.coords[1] if self.coords else None

        self.vanilla_reciprocal: DSTransition | None = None  # Paired location

        self.copy_number = 0


    def get_scene(self):
        if self.room:
            return self.stage * 0x100 + self.room
        else:
            return self.stage << 8

    def get_exit_scene(self):
        if self.exit:
            return self.exit[0] * 0x100 + self.exit[1]
        else:
            return None

    def is_pairing(self, r1, r2) -> bool:
        return r1 == self.entrance_region and r2 == self.exit_region

    def get_y(self):
        return self.coords[1] if self.coords else None

    def detect_exit_simple(self, stage, room, entrance):
        return self.exit == (stage, room, entrance)

    def detect_exit_scene(self, scene, entrance):
        return self.exit_scene == scene and entrance == self.exit[2]

    def detect_exit(self, scene, entrance, coords, y_offest):
        if self.detect_exit_scene(scene, entrance):
            if entrance < 0xF0:
                return True
            # Continuous entrance check
            x_max = self.extra_data.get("x_max", 0x8FFFFFFF)
            x_min = self.extra_data.get("x_min", -0x8FFFFFFF)
            z_max = self.extra_data.get("z_max", 0x8FFFFFFF)
            z_min = self.extra_data.get("z_min", -0x8FFFFFFF)
            y = self.coords[1] if self.coords else coords["y"] - y_offest
            # print(f"Checking entrance {self.name}: x {x_max} > {coords['x']} > {x_min}")
            # print(f"\ty: {y + 1000} > {y} > {coords['y'] - y_offest}")
            # print(f"\tz: {z_max} > {coords['z']} > {z_min}")
            if y + 2000 > coords["y"] - y_offest >= y and x_max > coords["x"] > x_min and z_max > coords["z"] > z_min:
                return True
        return False

    def set_stage(self, new_stage):
        self.stage = new_stage
        self.scene = self.get_scene()
        self.entrance = tuple([new_stage] + list(self.entrance[1:]))

    def set_exit_stage(self, new_stage):
        self.exit = tuple([new_stage] + list(self.exit[1:]))
        self.exit_scene = self.get_exit_scene()
        self.exit_stage = self.exit[0]

    def set_exit_room(self, new_room):
        self.exit = tuple([self.exit[0], new_room, self.exit[2]])
        self.exit_scene = self.get_exit_scene()

    def copy(self):
        res = DSTransition(f"{self.name}{self.copy_number+1}", self.data)
        res.copy_number = self.copy_number + 1
        return res

    def __str__(self):
        return self.name

    def debug_print(self):
        print(f"Debug print for entrance {self.name}")
        print(f"\tentrance {self.entrance}")
        print(f"\texit {self.exit}")
        print(f"\tcoords {self.coords}")
        print(f"\textra_data {self.extra_data}")

    @classmethod
    def from_data(cls, entrance_data):
        res = dict()
        counter = {}
        ident = 0
        for name, data in entrance_data.items():
            data["id"] = ident
            res[name] = cls(name, data)
            # print(f"{i} {ENTRANCES[name].entrance_region} -> {ENTRANCES[name].exit_region}")
            ident += 1
            point = data["entrance_region"] + "<=>" + data["exit_region"]
            counter.setdefault(point, 0)
            counter[point] += 1
            if "one_way_data" in data:
                res[name].extra_data |= data["one_way_data"]

            if data.get("two_way", True):
                two_way = True
            else:
                two_way = False
            reverse_name = data.get("return_name", f"Unnamed Entrance {ident}")
            reverse_data = {
                "entrance_region": data.get("reverse_exit_region", data["exit_region"]),
                "exit_region": data.get("reverse_entrance_region", data["entrance_region"]),
                "id": ident,
                "entrance": data.get("exit", data.get("entrance", None)),
                "exit": data["entrance"],
                "two_way": two_way,
                "type": data["type"],
                "island": data.get("return_island", data.get("island", cls.entrance_groups.NONE)),
                "direction": cls.opposite_entrance_groups[data["direction"]],
                "coords": data.get("coords", None),

            }
            if "extra_data" in data:
                reverse_data["extra_data"] = data["extra_data"]
            if "reverse_one_way_data" in data:
                reverse_data.setdefault("extra_data", {})
                reverse_data["extra_data"] = data["reverse_one_way_data"]
            if reverse_name in res:
                print(f"DUPLICATE ENTRANCE!!! {reverse_name}")
            res[reverse_name] = cls(reverse_name, reverse_data)

            res[name].vanilla_reciprocal = res[reverse_name]
            res[reverse_name].vanilla_reciprocal = res[name]

            # print(f"{i} {ENTRANCES[reverse_name].entrance_region} -> {ENTRANCES[reverse_name].exit_region}")
            ident += 1
            point: str = reverse_data["entrance_region"] + "<=>" + reverse_data["exit_region"]
            counter.setdefault(point, 0)
            counter[point] += 1
        return res