from ..assembler import ASM


def fixHeartPiece(rom):
    # Patch all locations where the piece of heart is rendered.
    rom.patch(0x03, 0x1b52, ASM("ld de, $5A4D\ncall $3BC0"), ASM("ld a, $04\nrst 8"), fill_nop=True)  # state 0

    # Write custom code in the first state handler, this overwrites all state handlers
    # Till state 5.
    rom.patch(0x03, 0x1A74, 0x1A98, ASM("""
        ; Render sprite
        ld   a, $05
        rst  8
    
        ; Handle item effect
        ld   a, $06 ; giveItemMultiworld
        rst  8
        
        ;Show message
        ld   a, $0A ; showMessageMultiworld
        rst  8
        
        ; Switch to state 5
        ld   hl, $C290; stateTable
        add  hl, bc
        ld   [hl], $05
        ret
    """), fill_nop=True)
    # Insert a state 5 handler
    rom.patch(0x03, 0x1A98, 0x1B17, ASM("""
        ; Render sprite
        ld   a, $05
        rst  8

        ld   a, [$C19F] ; dialog state
        and  a
        ret  nz

        call $512A ; mark room as done
        call $3F8D ; unload entity
        ret
    """), fill_nop=True)
