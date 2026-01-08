import struct

from .romWriter import RomWriter

"""
rooms.SelectMany(
room => statelist.Where(condition.testcode.GetShortAddressSNES() == 0xE612 && condition.args[0].Data == 0x0E)
.Select(String.Format("\"{0}\": ({1:X}, {2:X}, {3:X}, {4:X}),",
room.ToString(),
condition.address,
state.address,
room.statelist.Last().state.layer1_2,
room.statelist.Last().state.FX2
)))
"""

escape_rooms = {
    # (condition address, state address, default setup asm, default main asm, skip state value)
    # "IMPACT CRATER":                 (0x8FBB66, 0x8FBBA6, 0x91C9, 0xC116, 0xE625),  # This caused unplayable lag.
    "VULNAR CAVES ACCESS":           (0x8FEAC6, 0x8FEAE7, 0x91D3, 0x0000, 0xE625),
    "WEST TERMINAL ACCESS":          (0x8F81D2, 0x8F81F3, 0x91D3, 0x0000, 0xE625),
    "EAST TERMINAL":                 (0x8FDDA8, 0x8FDDC9, 0x91D3, 0x0000, 0xE625),
    "TRANSIT CONCOURSE":             (0x8FD7D3, 0x8FD7F4, 0x91D3, 0x0000, 0xE625),
    "WEST TERMINAL":                 (0x8FD858, 0x8FD879, 0x91D3, 0x0000, 0xE625),
    "TRANSIT CONCOURSE (power off)": (0x8FD7C8, 0x8FD828, 0x91D3, 0x0000, 0xE5FA),
    "WEST TERMINAL (power off)":     (0x8FD84D, 0x8FD8AD, 0x91D3, 0x0000, 0xE5FA),
    "GRAND CHASM":                   (0x8FBC30, 0x8FBC70, 0x91D3, 0x0000, 0xE625),
    "NORAK PERIMETER":               (0x8F897A, 0x8F899B, 0x91D3, 0x0000, 0xE625),
    "ROCKY RIDGE TRAIL":             (0x8F88EE, 0x8F890F, 0x91D3, 0x0000, 0xE625),
    "ROCKY RIDGE":                   (0x8FBA9C, 0x8FBADC, 0x91C9, 0xC116, 0xE625),
    "WRECKED AIR LOCK":              (0x8F82A4, 0x8F82C5, 0x91D3, 0x0000, 0xE625),
    "WRECKED CREW QUARTERS ACCESS":  (0x8F85A6, 0x8F85C7, 0x91D3, 0x0000, 0xE625),
    "WRECKED CREW QUARTERS":         (0x8F8A4C, 0x8F8A6D, 0x91D3, 0x0000, 0xE625),
    "WRECKED MAP STATION":           (0x8FE0AA, 0x8FE0CB, 0x91D3, 0x0000, 0xE625),
    "WRECKED MAIN ENGINEERING":      (0x8FE0F0, 0x8FE111, 0x91D3, 0x0000, 0xE625),
    "VULNAR CANYON":                 (0x8F8B64, 0x8F8B85, 0x91C9, 0xC116, 0xE625),
    "CANYON PASSAGE":                (0x8F8BAA, 0x8F8BCB, 0x91D3, 0x0000, 0xE625),
    "NORAK BROOK":                   (0x8F8BF0, 0x8F8C11, 0x91D3, 0x0000, 0xE625),
    "CRACKED CLIFFSIDE CAVE":        (0x8F89C0, 0x8F89E1, 0x91D3, 0x0000, 0xE625),
    "CLIFFTOP CRANNY":               (0x8FE4CE, 0x8FE4EF, 0x91D3, 0x0000, 0xE625),
    "AURORA UNIT WRECKAGE":          (0x8F800B, 0x8F804B, 0xC91E, 0x0000, 0xE625),
    "WRECKED MAINTENANCE DECK":      (0x8FE064, 0x8FE085, 0x91D3, 0x0000, 0xE625),
    "WRECKED OBSERVATION DECK":      (0x8FE01E, 0x8FE03F, 0x91D3, 0x0000, 0xE625),
    "WRECKED MACHINE ROOM":          (0x8FECB0, 0x8FECD1, 0xC91E, 0x0000, 0xE625),
}

# these escape rooms keep their alternate states to ensure that some escape mechanics work
escape_rooms_omit = (
    "AURORA UNIT WRECKAGE",      # Keeping the alternate state so that the fight works correctly
    "WRECKED MAINTENANCE DECK",  # Keeping the alternate state so that the timer cannot be restarted
    "WRECKED MAIN ENGINEERING",  # Keeping the alternate state so that MB cannot be re-entered
    "VULNAR CAVES ACCESS",       # Keeping the ability to save animals - terrain patched to open passage to right
    # "IMPACT CRATER",             # Make sure the ship is there if space port hasn't been crashed
)
# TODO: change IMPACT CRATER grey doors to blue


def patch_open_escape(romWriter: RomWriter) -> None:
    for room, addresses in escape_rooms.items():
        if room in escape_rooms_omit:
            # if using the alternate states then use the normal room asm instead
            # main = state + 18
            romWriter.writeBytes(RomWriter.snes_to_index_addr(addresses[1]) + 18, struct.pack("<H", addresses[2]))
            # init = state + 24
            romWriter.writeBytes(RomWriter.snes_to_index_addr(addresses[1]) + 24, struct.pack("<H", addresses[3]))
        else:
            # never load alternate escape state
            romWriter.writeBytes(RomWriter.snes_to_index_addr(addresses[0]), struct.pack("<H", addresses[4]))
