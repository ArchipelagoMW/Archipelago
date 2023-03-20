.gba

; Change the full health item to check the location instead of filling
; Wario's hearts

; EntityAI_0x8B_Tmain_takara_bainomi()
.org 0x802A39C
.definelabel @@PlaySound, 0x802A3C0
.region @@PlaySound-.
    mov r0, #2
    ldr r1, =HasFullHealthItem
    strb r0, [r1]
    ldr r0, =0x13B  ; a1
    b @@PlaySound
.pool
.endregion


; Change the full health box to work like the jewel boxes and CD case, spawning
; its item if you haven't collected it or simply dropping a coin if you have.

; Hook into EntityAI_0x05_Tmain_takarabako_bainomi(), switch case 18
.org 0x8029EFE
.definelabel @@Case50, 0x8029F2A
.region @@Case50-.
    ldr r0, =@@Case50 | 1
    mov lr, r0
    ldr r0, =FullHealthLocationCheck | 1
    bx r0
.pool
.endregion

.autoregion
.align 2
FullHealthLocationCheck:
    push r4, r5, lr

; Spawn coin?
    ldr r0, =@@SetAnimation | 1
    mov lr, r0
    ldr r0, =EntityAI_Q_K5_Hip_COM_takarabako | 1
    bx r0
@@SetAnimation:
    ldr r0, =zako_takara_box_Anm_11
    str r0, [r4, #4]

; Check full health location
    ldr r0, =HasFullHealthItem
    ldrb r0, [r0]
    cmp r0, #0
    beq @@ContainsFullHealthItem

; Contains nothing
    ldr r1, =EntityLeftOverStateList
    ldr r0, =CurrentRoomId
    ldrb r0, [r0]
    lsl r0, r0, #6
    ldrb r4, [r4, #24]
    add r0, r0, r4
    add r0, r0, r1
    mov r1, #0x21
    strb r1, [r0]
    b @@Return

@@ContainsFullHealthItem:
    ldrb r1, [r4, #24]  ; a2
    ldrh r3, [r4, #8]
    sub r3, #0x80  ; a4
    ldrh r0, [r4, #10]
    str r0, [sp]  ; a5
    mov r0, #0x8B  ; a1
    mov r2, #0  ; a3
    ldr r5, =@@SetChild2 | 1
    mov lr, r5
    ldr r5, =EnemyChildSet | 1
    bx r5
@@SetChild2:
    ldrb r1, [r4, #24]  ; a2
    ldrh r3, [r4, #8]
    sub r3, #0x80  ; a4
    ldrh r0, [r4, #10]
    str r0, [sp]  ; a5
    mov r0, #0x91  ; a1
    mov r2, #0  ; a3
    ldr r5, =@@Return | 1
    mov lr, r5
    ldr r5, =EnemyChildSet | 1
    bx r5

@@Return:
    pop r4, r5, pc

.pool
.endautoregion


; Add the full health item to the load routine

; Hook into ItemGetFlgSet_LoadSavestateInfo2RAM()
.org 0x8075F10
.definelabel @@BranchNoKeyzer, 0x8075F20
.region @@BranchNoKeyzer-.
    ldr r0, =@@BranchNoKeyzer | 1
    mov lr, r0
    ldr r0, =ItemGetFlagFullHealth | 1
    bx r0
.pool
.endregion

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
    ldr r3, =HasFullHealthItem
    lsl r2, r1, #25
    lsr r2, r2, #31
    cmp r2, #0
    beq @@NoFullHealth

; Already got the full-health check
    mov r2, #2
    b @@CheckKeyzer

@@NoFullHealth:
    mov r2, #0

@@CheckKeyzer:
    str r2, [r3]
    lsl r2, r1, #26
    lsr r2, r2, #31

@@Return:
    cmp r2, #0  ; Next instruction is beq
    bx lr

.pool
.endautoregion


; Add the full health item to the save routine

; Hook into SeisanSave() where it checks Keyzer
.org 0x8081262
.definelabel @@HighScore, 0x8081285
.region @@HighScore-.
    ldr r0, =@@HighScore | 1
    mov lr, r0
    ldr r0, =SeisanSaveFullHealthItem | 1
    bx r0
.pool
.endregion

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
    mov r1, lr
    bx r1

.pool
.endautoregion
