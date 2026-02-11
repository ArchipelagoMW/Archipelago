
from typing import TYPE_CHECKING
from .subclasses import split_bits
from ..data.Constants import DUNGEON_KEY_DATA

if TYPE_CHECKING:
    from BaseClasses import ItemClassification
    from worlds._bizhawk.context import BizHawkClientContext
    from .DSZeldaClient import DSZeldaClient
    from .subclasses import Address


# Handle Small Keys
async def receive_small_key(client: "DSZeldaClient", ctx: "BizHawkClientContext", item: "DSItem", num_received_items):
    res = []
    async def write_keys_to_storage(dungeon) -> tuple[int, list, str]:
        key_data = DUNGEON_KEY_DATA[dungeon]  # TODO: Add dungeon key data to item_data
        prev = await key_data["address"].read(ctx)
        bit_filter = key_data["filter"]
        new_v = prev | bit_filter if (prev & bit_filter) + key_data[
            "value"] > bit_filter else prev + key_data["value"]
        print(f"Writing {key_data['name']} key to storage: {hex(prev)} -> {hex(new_v)}")
        return key_data["address"].get_inner_write_list(new_v)

    # Get key in own dungeon
    if client.current_stage == item.dungeon:
        print("In dungeon! Getting Key")
        # Don't remove vanilla keys
        if client.last_vanilla_item and client.last_vanilla_item[-1] == item.name:
            client.last_vanilla_item.pop()
        else:
            key_value = await client.key_address.read(ctx)
            key_value = 7 if key_value > 7 else key_value
            res += client.key_address.get_write_list(key_value + 1)
            res += await client.receive_key_in_own_dungeon(ctx, item.name, write_keys_to_storage)  # TODO: Move special operation here too

    # Get key elsewhere
    else:
        res.append(await write_keys_to_storage(item.dungeon))

    # Extra key operations, in ph writing totok midway keys
    res += await client.received_special_small_keys(ctx, item.name, write_keys_to_storage)
    return res

async def receive_refill(client: "DSZeldaClient", ctx: "BizHawkClientContext", item: "DSItem", num_received_items):
    res = []
    prog_received = min(client.item_count(ctx, item.refill, num_received_items),
                        len(item.give_ammo)) - 1
    if prog_received >= 0:
        res += item.address.get_write_list(item.give_ammo[prog_received])
    return res

# Handle progressive and incremental items.
# TODO Split progressive and incremental?
async def receive_normal(client: "DSZeldaClient", ctx: "BizHawkClientContext", item: "DSItem", num_received_items):
    prog_received = 0
    item_value = 0
    res = []
    if hasattr(item, "progressive"):
        prog_received = min(client.item_count(ctx, item.name, num_received_items),
                            len(item.progressive) - 1)
        item_address, item_value = item.progressive[prog_received]
    else:
        item_address = item.address

    # Read address item is to be written to
    prev_value = await item_address.read(ctx)

    # Handle different writing operations
    if "incremental" in item.tags:
        value = item.value
        if type(value) is str:
            value = await client.received_special_incremental(ctx, item)  # TODO: hook into this somehow?

        item_value = prev_value + value
        item_value = 0 if item_value <= 0 else item_value
        if "Rupee" in item.name:
            item_value = min(item_value, 9999)
        if item.address.size > 1:
            item_value = split_bits(item_value, item.address.size)
        if hasattr(item, "max") and item_value > item.max:
            item_value = min(item.max, prev_value)
    elif hasattr(item, "progressive"):
        if "progressive_overwrite" in item.tags and prog_received >= 1:
            item_value = item_value  # Bomb upgrades need to overwrite of everything breaks
        else:
            item_value = prev_value | item_value
    elif "monotone_incremental" in item.tags:  # For incremental items you want to recalculate their count for each time.
        item_value = item.value
        if type(item_value) is str:
            item_value = await client.received_special_incremental(ctx, item)  # TODO: hook into this somehow?
        else:
            item_value = item.value * client.item_count(ctx, item.name) + getattr(item, "base_count", 0)
        # Heal on heart container
        if item.name == "Heart Container":
            await client.full_heal(ctx, 4)
    else:
        item_value = prev_value | item.value

    # item_values = item_value if isinstance(item_value, list) else split_bits(item_value, item_address.size)
    # item_values = [min(255, i) for i in item_values]
    res += item_address.get_write_list(item_value)

    # Handle special item conditions
    if hasattr(item, "give_ammo"):
        res += item.ammo_address.get_write_list(item.give_ammo[prog_received])
    if hasattr(item, "set_bit"):
        for adr, bit in item.set_bit:
            bit_prev = await adr.read(ctx)
            res += adr.get_write_list(bit | bit_prev)

    return res

async def remove_vanilla_small_key(client: "DSZeldaClient", ctx: "BizHawkClientContext", item: "DSItem", num_received_items):
    address = client.key_address = await client.get_small_key_address(ctx)
    prev_value = await address.read(ctx)
    return address.get_write_list(prev_value-1)

async def remove_vanilla_progressive(client: "DSZeldaClient", ctx: "BizHawkClientContext", item: "DSItem", num_received_items):
    res = []
    index = client.item_count(ctx, item.name, num_received_items)
    if index >= len(item.progressive):
        return res
    address, value = item.progressive[index]
    if hasattr(item, "give_ammo"):
        ammo_v = item.give_ammo[min(max(index - 1, 0), len(item.give_ammo) - 1)]
        res += item.ammo_address.get_write_list(ammo_v)
    # Progressive overwrite fix
    if "progressive_overwrite" in item.tags and index > 1:
        res += address.get_write_list(value)
    return res

async def remove_vanilla_normal(client: "DSZeldaClient", ctx: "BizHawkClientContext", item: "DSItem", num_received_items):
    address, value = item.address, item.value

    prev_value = await address.read(ctx)
    # Catch vanilla rupees going over 9999
    if "Rupee" in item.name:
        value = 9999 - prev_value if prev_value + value > 9999 else value
        value = prev_value if prev_value-value < 0 else value
    if "incremental" or "monotone_incremental" in item.tags:
        if prev_value - value < 0: print(f"TRIED TO UNDERFLOW {item.name}")
        value = prev_value if prev_value - value < 0 else prev_value - value

    else:
        value = prev_value & (~value)

    return address.get_write_list(value)

class DSItem:
    """
    Datastructure for item data
    """
    id: int
    classification: "ItemClassification"

    # Basics
    address: "Address"
    value: int
    size: int or str
    progressive: list[tuple["Address", int]]
    domain: str
    base_count: int  # If monotone_incremental, base amount of an item, ex. 12 for hearts

    # Ammo
    ammo_address: "Address"
    give_ammo: list[int]  # Ammo amount for each upgrade stage
    refill: str  # item reference for refill data

    # Extra bits
    set_bit: list[tuple["Address", int]]
    set_bit_in_room: dict[int, list]

    dungeon: int or bool  # dungeon stage
    ship: int  # index in constants.ships

    # Tags and flags
    dummy: bool
    tags: list[str]

    overflow_item: str
    max: int  # only used for salvage, and is weird there.
    inventory_id: int  # used for creating item menu on first item

    disconnect_entrances: list[str]  # list of entrances to attempt to disconnect on receive
    hint_on_receive: list[str]  # list of items to hint for on receive

    def __init__(self, name, data, all_items):
        self.data = data
        self.name: str = name
        self.all_items = all_items

        self.value = 1
        self.size = 1
        self.domain = "Main RAM"
        self.tags = []

        for attribute, value in data.items():
            self.__setattr__(attribute, value)

        self.receive_item_func = self.get_receive_function()
        self.remove_vanilla_func = self.get_remove_vanilla_function()

    def get_receive_function(self):
        if "Small Key" in self.name:
            return receive_small_key
        if hasattr(self, "refill"):
            return receive_refill
        if hasattr(self, "address") or hasattr(self, "progressive"):
            return receive_normal

        return None

    def get_remove_vanilla_function(self):
        if hasattr(self, "dummy"):
            return lambda *args: []
        if "Small Key" in self.name:
            return remove_vanilla_small_key
        if hasattr(self, "progressive"):
            return remove_vanilla_progressive
        return remove_vanilla_normal

    def receive_item(self, client: "DSZeldaClient", ctx: "BizHawkClientContext", num_received_items: int):
        return self.receive_item_func(client, ctx, self, num_received_items)

    def remove_vanilla(self, client: "DSZeldaClient", ctx: "BizHawkClientContext", num_received_items):
        return self.remove_vanilla_func(client, ctx, self, num_received_items)

    def get_count(self, ctx, items_received=-1) -> int:
        items_received = len(ctx.items_received) if items_received == -1 else items_received
        return sum([1 for i in ctx.items_received[:items_received] if i.item == self.id])

    def post_process(self, client: "DSZeldaClient", ctx: "BizHawkClientContext"):
        return

    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"{type(self)} object {self.name}"
