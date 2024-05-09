from typing import NamedTuple, List
import struct

entity_struct = struct.Struct("<18H2B2H2B1H2B3H2B4H")


class EntityData(NamedTuple):
    """64-byte Lair Data structure."""

    x: int
    """X position of entity. 2 bytes."""
    y: int
    """Y position of entity. 2 bytes."""
    field_04: int
    """Appears to be related to velocity and changes while entity is moving. 2 bytes."""
    field_06: int
    """Unknown. 2 bytes."""
    field_08: int
    """Unknown. 2 bytes."""
    field_0A: int
    """Might be related to sprite animation states. 2 bytes."""
    field_0C: int
    """Might be related to sub-sprite animation states. 2 bytes."""
    field_0E: int
    """Unknown. 2 bytes."""
    field_10: int
    """Unknown. 2 bytes."""
    field_12: int
    """Unknown. 2 bytes."""
    frame_wait_counter: int
    """Number of frames to wait. Used by COP-1B. 2 bytes."""
    entity_id: int
    """Unsure if this is actually an ID. 2 bytes."""
    script_ret_addr: int
    """Address of return location for entity behavior script. 2 bytes."""
    field_1A: int
    """Unknown. 2 bytes."""
    field_1C: int
    """Unknown. 2 bytes."""
    animation_state: int
    """Current animation state. 2 bytes"""
    animation_state_frame: int
    """The frame that the current animation is in. 2 bytes."""
    # So far I have observed that this always seem to have a long pointer to 0x7E3800 in them, but maybe some entities are different.
    some_addr: int
    """Pointer to some address. 2 bytes."""
    some_bank: int
    """Upper (bank) byte for some_addr. 1 byte."""
    hp: int
    """Current hit points of entity. HP of enemy to spawn for lairs. 1 byte."""
    invincibility_counter: int
    """Used for tracking entity invincibility state. 2 bytes."""
    field_28: int
    """Unknown. Appears to be a pointer of some sort. Changes frequently while entity performs actions. 2 bytes."""
    field_2A: int
    """Unknown. Possibly bank for above pointer. 1 byte."""
    field_2B: int
    """Unknown. 1 byte."""
    field_2C: int
    """Unknown. 2 bytes."""
    loop_counter: int
    """Used in COP-03/04. Also used in lairs to track remaining enemies. 1 byte."""
    loop_counter_mirror: int
    """Same as above, but occasionally delayed. Unsure of its significance. 1 byte."""
    field_30: int
    """Unknown. 2 bytes."""
    parent_entity: int
    """Parent entity pointer. 2 bytes."""
    lair_assotiated_with: int
    """The lair id assotiated with this entity, otherwise 0. 2 bytes."""
    script_ret_addr_bank: int
    """The upper (bank) byte of script_ret_addr. 1 byte."""
    field_37: int
    """Unknown. 1 byte."""
    entity_definition_offset: int
    """Offset added to rom address of entities table to create pointer into entities definition table. 2 bytes."""
    entity_placement_ptr: int
    """Pointer into enemy placement data table. 0x9B39 to 0xA9DD. 2 bytes."""
    field_3C: int
    """Appears to be entity pointer. Possibly linked list previous entity? 2 bytes."""
    field_3E: int
    """Appears to be entity pointer. Possibly linked list next entity? 2 bytes."""


def unpack_entity_data(buffer) -> List[EntityData]:
    return [EntityData._make(data) for data in entity_struct.iter_unpack(buffer)]
