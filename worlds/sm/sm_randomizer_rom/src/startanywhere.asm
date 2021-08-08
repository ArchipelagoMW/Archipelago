;
; Patches to support starting at any given location in the game
; by injecting a save station at X/Y coordinates in the specified room.
; 
; Requires adding a new save station with ID: 7 for the correct region in the save station table as well.
;

!savestation_id = $07

org $82e8d5
    jsl inject_savestation
org $82eb8b
    jsl inject_savestation
org $82804e
    jsr start_anywhere

org $8ffd00
startroom_region:
    dw $0000
startroom_id:
    dw $92fd
startroom_save_plm:
    dw $b76f : db $05, $0a : dw $0007

org $82fd00
start_anywhere:
    lda startroom_id
    beq .ret

    ; Make sure game mode is 1f
    lda $7e0998
    cmp.w #$001f
    bne .ret
    
    ; Check if samus saved energy is 00, if it is, run startup code
    lda $7ed7e2
    bne .ret

    lda startroom_region
    sta $079F
    lda #$0007
    sta $078B

.ret
    jsr $819B
    rts

inject_savestation:
    lda $079b    ; Load room id
    cmp startroom_id
    bne .end
                 
    ldx.w #startroom_save_plm
    lda.w $0000, x
    jsl $84846a  ; create PLM

.end
    jsl $8FE8A3  ; Execute door ASM
    rtl