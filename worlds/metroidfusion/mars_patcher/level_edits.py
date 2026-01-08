from .rom import Rom
from .room_entry import RoomEntry


def apply_level_edits(rom: Rom, edit_dict: dict) -> None:
    # Go through every area
    for area, rooms in edit_dict.items():
        # Go through every room
        for room, layers in rooms.items():
            r = RoomEntry(rom, int(area), int(room))

            # Go through every layer
            for layer, changes in layers.items():
                if layer == "BG1":
                    load = r.load_bg1
                elif layer == "BG2":
                    load = r.load_bg2
                elif layer == "Clipdata":
                    load = r.load_clip
                else:
                    raise ValueError("Unsupported Block Layer")

                # Load layer, do every edit that's provided and write back.
                with load() as layer:
                    for change in changes:
                        layer.set_block_value(change["X"], change["Y"], change["Value"])
