
def fixTrendy(rom):
    rom.patch(0x04, 0x2F29, "04", "02")  # Patch the trendy game shield to be a ruppee
