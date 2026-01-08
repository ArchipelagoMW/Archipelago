from .droppedKey import DroppedKey


class GoldLeaf(DroppedKey):
    pass  # Golden leaves are patched to work exactly like dropped keys


class SlimeKey(DroppedKey):
    # The slime key is secretly a golden leaf and just normally uses logic depended on the room number.
    # As we patched it to act like a dropped key, we can just be a dropped key in the right room
    def __init__(self):
        super().__init__(0x0C6)
