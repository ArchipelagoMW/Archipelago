from typing import NamedTuple, List
import struct


lair_struct = struct.Struct("<16B1H8B1H2B1H")


class LairData(NamedTuple):
    """32-byte Lair Data structure."""

    release_map: int
    """Map ID for the released NPC. Byte."""
    release_layer: int
    """Which layer from the map arrangement data to pull new map data from. Byte."""
    release_x: int
    """Top-left corner X of release zone. Byte."""
    release_y: int
    """Top-left corner Y of release zone. Byte."""
    release_arrangement_x: int
    """Top-left corner X of map arrangement data. Byte."""
    release_arrangement_y: int
    """Top-left corner Y of map arrangement data. Byte."""
    release_width: int
    """Width of NPC release zone. Byte."""
    release_height: int
    """Height of NPC release zone. Byte."""
    flags: int
    """
    Flags used if map contains alternate layers. Byte.
    Not entirely sure on usage.
    """
    npc_name_index: int
    """Index into NPC name pointer table. Byte."""
    act_id: int
    """
    Which Act the zone is for. Byte.
    Used to determine which monsters to spawn.
    00: Act 1 - Grass Valley
    01: Act 2 - Greenwood
    02: Act 3 - St Elles
    03: Act 4 - Mountain of Souls
    04: Act 5 - Leo's Lab
    05: Act 6 - Magridd Castle
    06: Act 7 - World of Evil
    """
    lair_map: int
    """Map ID that the lair is on. Byte."""
    lair_x: int
    """Lair X coordinate. Byte."""
    lair_y: int
    """Lair Y coordinate. Byte."""
    field_0E: int
    """
    Non-zero value for lairs without release cutscenes. Byte.
    Value is multiplied by 16 (0x10) and stored to memory address 0x16.
    Used during map transformation, but not sure how exactly.
    """
    field_0F: int
    """
    Non-zero value for lairs without release cutscenes. Byte.
    Value is multiplied by 16 (0x10) and stored to memory address 0x18.
    Used during map transformation, but not sure how exactly.
    """
    # Actually 3 bytes but python structs dont support packing/unpacking ints of that size.
    # I could use '3s' to get a bytes of size 3, but this is slightly more convienent.
    lair_behavior_pointer: int
    """
    Lair Behavior Pointer. 2 bytes.
    0x000000: Pre-cleared.
    0x00A6F3: One by one.
    0x00A71B: Multispawn.
    0x00A752: Aleady there.
    0x00A7D2: Two up, two down.
    0x00A813: One by one (proximity).
    """
    lair_behavior_pointer_bank: int
    """
    The upper byte (bank) of the lair behavior address. Byte.
    Happens to always be zero since all the lair behavior functions are in bank 0.
    """
    enemy_count: int
    """Number of enemies to spawn. Byte."""
    spawn_rate: int
    """How quickly to spawn enemies. Byte."""
    entity_id: int
    """Used with act_id to index into the entities table to determine which enemy to spawn. Byte."""
    field_16: int
    """Unknown, always zero. Might be second byte of entity_id."""
    orientation: int
    """Enemy orientation. Byte."""
    # Fields 0x18, 0x19, and 0x1A have been repurposed for decoupled lair rewards.
    lair_reward_id: int
    """The reward ID for the lair. Byte."""
    lair_reward_operand: int
    """The reward operand for the lair. 2 bytes."""
    field_1B: int
    """Unknown, always zero. Probably unused."""
    field_1C: int
    """Unknown, always zero. Probably unused."""
    field_1D: int
    """Unknownm, usually zero, but ocasionally 1,2 or 3."""
    lair_dependency: int
    """Lair ID of NPC this lair is dependent on. 2 bytes."""


def unpack_lair_data(buffer) -> List[LairData]:
    return [LairData._make(data) for data in lair_struct.iter_unpack(buffer)]


# TODO: unsure if this is the correct syntax. Verify.
def pack_lair_data(buffer, offset: int, *lair_data: LairData) -> None:
    lair_struct.pack_into(buffer, offset, lair_data)
    return
