; --- swap DMA order ---

; Upper tilemaps were loaded before lower, but rendered after. The order is
; swapped to avoid larger DMAs overwriting later ones. Swap the commands in
; $80:9382-93CA with $80:93CB-9413, but most are identical so just change these:

org $809382+1 : db $1E
org $809389+1 : db $21
org $80938E+1 : db $80
org $8093B6+1 : db $80
org $8093CB+1 : db $1D
org $8093D2+1 : db $1F
org $8093D7+1 : db $00
org $8093FF+1 : db $00


; --- disable upper bypass ---

; Since a DMA of zero usually results in a game crash by DMA-ing an entire bank,
; Deerforce made separate subroutines that skipped upper tilemaps in certain cases.
; This is fixed by the DMA order swap, but the subroutines now break a few
; animations in their new form. However, there is not a simple way to avoid DMA,
; you have to use a bypass routine, so the null routine is reused for all cases.

org $90864E
    rep 28 : dw $8686


; --- hide suit light tile ---

; This tile hid the green light on the right side of Samus suit. It is now
; superfluous so we solve that by making it transparent.

org $9AD620
    rep $20 : db $00


; --- death DMA asm ---

; During the death sequence data is prefetched while Samus is pausing (for
; dramatic effect), so we just prefetch more. The very last one is not
; prefetched because it overwrites the bonk pose
;$9B:B44A    CMP #$0004

org $9BB44A
    CMP #$000F


; The final fetch overwrites Samus bonk pose, so it is indexed at the last moment
;$9B:B5AE    LDY #$0008

org $9BB5AE
    LDY #$001E


; Use the correct bank
;$9B:B6EE    LDA #$9B    ;use bank 9B

org $9BB6EE
    LDA #$FF


org $9BFDA0

death_left_table:
    dw $8000+(1*$400)
    dw $8000+(2*$400)
    dw $8000+(3*$400)
    dw $8000+(4*$400)
    dw $8000+(5*$400)
    dw $8000+(6*$400)
    dw $8000+(7*$400)
    dw $8000+(8*$400)
    dw $8000+(9*$400)
    dw $8000+(10*$400)
    dw $8000+(11*$400)
    dw $8000+(12*$400)
    dw $8000+(13*$400)
    dw $8000+(14*$400)
    dw $8000+(15*$400)
    dw $8000

death_right_table:
    dw $C000+(1*$400)
    dw $C000+(2*$400)
    dw $C000+(3*$400)
    dw $C000+(4*$400)
    dw $C000+(5*$400)
    dw $C000+(6*$400)
    dw $C000+(7*$400)
    dw $C000+(8*$400)
    dw $C000+(9*$400)
    dw $C000+(10*$400)
    dw $C000+(11*$400)
    dw $C000+(12*$400)
    dw $C000+(13*$400)
    dw $C000+(14*$400)
    dw $C000+(15*$400)
    dw $C000

dest_table:
    dw $6000+(1*$200)
    dw $6000+(2*$200)
    dw $6000+(3*$200)
    dw $6000+(4*$200)
    dw $6000+(5*$200)
    dw $6000+(6*$200)
    dw $6000+(7*$200)
    dw $6000+(8*$200)
    dw $6000+(9*$200)
    dw $6000+(10*$200)
    dw $6000+(11*$200)
    dw $6000+(12*$200)
    dw $6000+(13*$200)
    dw $6000+(14*$200)
    dw $6000+(15*$200)
    dw $6000

death_routine:       ; New code to load different data based upon left or right facing
    LDA $0A1E        ; load the direction that Samus is facing
    BIT #$0008       ; right facing?
    BNE .right
    LDA death_left_table,y
    RTS

.right
    LDA death_right_table,y
    RTS


; Hook the new pointers
;$9B:B6F5    LDA $B7C9,y    ;destination of DMA data transfer during the death sequence

org $9BB6F5
    LDA dest_table,y


; Hook the new subroutine
;$9B:B6E5    LDA $B7BF,y    ;get the DMA relative pointers

org $9BB6E5
    JSR death_routine
