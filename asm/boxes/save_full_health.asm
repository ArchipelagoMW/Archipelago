.gba

; Add the full health item to the load routine

; Hook into ItemGetFlgSet_LoadSavestateInfo2RAM()
hook 0x8075F10, 0x8075F20, ItemGetFlagFullHealth

.autoregion
.align 2
ItemGetFlagFullHealth:
; Load level state flags into r1
    add r1, r4, r6
    lsl r1, r1, #3
    add r1, r3, r1
    add r1, r12
    ldrb r1, [r1, #1]  ; chest flags are in [r1+1] so treasures can stay in [r1]

; Check full health first so that we can load Keyzer's status to follow the
; original branch when this returns.
; Some other code gets to one of those branches, which is why we can't replace
; it here.
    lsl r2, r1, #25
    lsr r2, r2, #31
    cmp r2, #0
    beq @@NoFullHealth

; Already got the full-health check
    ldr r2, =HasFullHealthItem
    mov r1, #2
    strb r1, [r2]
    b @@CheckKeyzer

@@NoFullhealth:
    ldr r1, =HasFullHealthItem
    strb r2, [r1]

@@CheckKeyzer:
    add r1, r4, r6
    lsl r1, r1, #3
    add r1, r3, r1
    add r1, r12
    ldrb r1, [r1]
    lsl r2, r1, #26
    lsr r2, r2, #31

@@Return:
    cmp r2, #0  ; Next instruction is beq
    mov pc, lr

.pool
.endautoregion


; Add the full health item to the save routine

; Hook into SeisanSave() where it checks Keyzer
hook 0x8081262, 0x8081284, SeisanSaveFullHealthItem

.autoregion
.align 2
SeisanSaveFullHealthItem:
    ldr r3, =LevelStatusTable
    ldrb r1, [r6]
    lsl r1, r1, #2
    ldrb r2, [r5]
    lsl r0, r2, #1
    add r0, r0, r2
    lsl r0, r0, #3
    add r1, r1, r0
    add r1, r1, r3

; Handle Keyzer
    ldr r0, =HasKeyzer
    ldrb r0, [r0]
    cmp r0, #0
    beq @@FullHealthItem
    ldrb r0, [r1]
    mov r2, #0x20
    orr r0, r2
    strb r0, [r1]

@@FullHealthItem:
    ldr r0, =HasFullHealthItem
    ldrb r0, [r0]
    cmp r0, #0
    beq @@Return
    ldrb r0, [r1, #1]
    mov r2, #0x40
    orr r0, r2
    strb r0, [r1, #1]

@@Return:
    mov pc, lr

.pool
.endautoregion
