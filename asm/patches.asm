.gba

; Single-line patches.


; Save data
; ---------
; Use the second byte of each level state word to store the boxes that have been
; opened and looted, keeping the actual world status in the least significant byte.

; ItemGetFlgSet_LoadSavestateInfo2RAM()
.org 0x8075E4E  ; Jewel piece 1
    ldrb r1, [r1, #1]
.org 0x8075E78  ; Jewel piece 2
    ldrb r1, [r1, #1]
.org 0x8075EA0  ; Jewel piece 3
    ldrb r1, [r1, #1]
.org 0x8075EC8  ; Jewel piece 4
    ldrb r1, [r1, #1]
.org 0x8075EF0  ; CD
    ldrb r1, [r1, #1]

; SeisanSave()
.org 0x80811D0  ; Jewel piece 1
    ldrb r0, [r1, #1]
    .skip 4
    strb r0, [r1, #1]
.org 0x80811F4  ; Jewel piece 2
    ldrb r0, [r1, #1]
    .skip 4
    strb r0, [r1, #1]
.org 0x8081216  ; Jewel piece 3
    ldrb r0, [r1, #1]
    .skip 4
    strb r0, [r1, #1]
.org 0x8081238  ; Jewel piece 4
    ldrb r0, [r1, #1]
    .skip 4
    strb r0, [r1, #1]
.org 0x808125A  ; CD
    ldrb r0, [r1, #1]
    .skip 4
    strb r0, [r1, #1]


; Skip cutscenes
; --------------

; Intro cutscene
.org 0x8000312  ; MainGameLoop(): Prevent cutscene starting
    mov r0, #1
.org 0x8091944  ; GameReady(): Stop title music
    nop
.org 0x8091DA8  ; ReadySet_SelectKey(): Don't play car engine sound
    .word 0x8091DD8

; Jewel cutscene and jewel door opening
.org 0x8080FA8  ; DoraGetItemHantei()
    nop

; Post-boss cutscenes
.org 0x8079FDC  ; MainGameLoop(): Pyramid appears
    mov r0, #1
.org 0x807A030  ; MainGameLoop(): Pyramid opens
