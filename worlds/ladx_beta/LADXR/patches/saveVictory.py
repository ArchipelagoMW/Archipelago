from ..assembler import ASM

def saveVictory(rom):
    # Replaces end credits debug tools
    # Sets a flag on game completion in the save file
    rom.patch(0x17, 0x0AB7, 0x0AD6, ASM("""
        ld   a, $01
        ld   [$DB59], a ; 3rd unused death count byte
        call $27D0      ; Enable SRAM
        ld   [$A45E], a ; SRAM location corresponding to $DB59
    """), fill_nop=True)
