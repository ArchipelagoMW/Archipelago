; Randomizer seed data
rando_seed_data:
    ; $00
    dw $0000    ; Player Id
    
    ; $02
    dw $0000    ; Seed bitfield

    ; $04-$0f
    dw $0000, $0000, $0000, $0000, $0000, $0000 ; Future use

    ; $10-2f
    db "0233d47a92d14217ac52e932ffc684dd"  ; Seed GUID

    ; $30-4f
    db "adaa377c2adb4ea0b2d7a9741d966c03"  ; Player GUID