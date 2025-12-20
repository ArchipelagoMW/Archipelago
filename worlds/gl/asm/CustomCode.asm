.n64
.create "mycode.bin", 0xE00D0000

; DataArea (0xE00D0800), BIG-ENDIAN:
;   +0x00 word = packed item descriptor (3–4 bytes)
;                potion if FIRST BYTE (MSB) == 0x08
;   +0x04 word = quantity (must be in s1)
;   +0x08 word = player ID (EXTERNAL: 1–4)

.org 0xE00D0000
FrameHook:
    ; --- save ---
    addiu  sp, sp, -0x30
    sw     ra, 0x2C(sp)
    sw     s0, 0x28(sp)
    sw     s1, 0x24(sp)
    sw     s2, 0x20(sp)
    sw     s3, 0x1C(sp)

    ; --- load DataArea ---
    lui    t0, 0xE00D
    lw     s2, 0x0800(t0)     ; packed item descriptor
    lw     s1, 0x0804(t0)     ; quantity
    lw     s3, 0x0808(t0)     ; player ID (1–4 external)

    ; --- gate: require item + qty + valid player ---
    beq    s2, zero, .Skip
    nop
    beq    s1, zero, .Skip
    nop

    ; player ID must be 1–4
    sltiu  t1, s3, 1
    bne    t1, zero, .Skip
    nop
    sltiu  t1, s3, 5
    beq    t1, zero, .Skip
    nop

    ; --- normalize player ID: 1–4 -> 0–3 ---
    addiu  s3, s3, -1

    ; --- engine pickup handling ---
    move   a0, s3             ; player ID (0–3)
    move   a1, s2             ; packed descriptor
    ; s1 already holds quantity as required

    addiu  sp, sp, -0x38      ; REQUIRED caller-allocated frame
    jal    0xE0054FF0
    nop
    ; callee restores sp

    ; --- potion check ---
    ; first byte (MSB) == 0x08
    lui    t0, 0xE00D
    lbu    t2, 0x0803(t0)
    lw    s3, 0x0808(t0)
    addiu  s3, s3, -1
    li     t3, 0x08
    bne    t2, t3, .ClearAndExit
    nop

    ; --- potion logic ---
    move   a0, s3             ; player ID (0–3)
    jal    0xE004DE9C         ; FUN_0004da9c
    nop

.ClearAndExit:
    lui    t0, 0xE00D
    sw     zero, 0x0800(t0)
    sw     zero, 0x0804(t0)
    sw     zero, 0x0808(t0)

.Skip:
    ; --- restore ---
    lw     s3, 0x1C(sp)
    lw     s2, 0x20(sp)
    lw     s1, 0x24(sp)
    lw     s0, 0x28(sp)
    lw     ra, 0x2C(sp)
    addiu  sp, sp, 0x30

    ; --- replay overwritten site ---
    lw     v0, 0(s0)
    beq    v0, zero, .FallThrough
    nop
    j      0xE0006D60
    nop
.FallThrough:
    j      0xE0006C84
    nop


.org 0xE00D0100
Hook_LevelUnlockCheck:
    ; ---- load flags (replay overwritten lw) ----
    lw    t0, 4(v1)

    ; ---- gate: (s0 & 0xFFF) < 0x100 ? ----
    andi  t2, s0, 0x0FFF
    sltiu t2, t2, 0x0100
    beq   t2, zero, .NormalBitCheck
    nop

    ; ---- tier -> single bit remap ----
    li    t2, 1              ; bit = 1 << (tier-1)

    beq   t1, 1, .HaveBit
    nop
    sll   t2, t2, 1          ; 0x2
    beq   t1, 2, .HaveBit
    nop
    sll   t2, t2, 1          ; 0x4
    beq   t1, 3, .HaveBit
    nop
    sll   t2, t2, 1          ; 0x8
    beq   t1, 4, .HaveBit
    nop
    sll   t2, t2, 1          ; 0x10 (boss)

.HaveBit:
    and   t0, t0, t2
    sltu  v0, zero, t0
    b     .Return
    nop

.NormalBitCheck:
    ; ---- original cumulative logic ----
    and   t0, t0, t1
    sltu  v0, zero, t0
    and   v0, v0, v1

.Return:
    j     0xE005545C
    nop


.org 0xE00D0800
DataArea:
    .word 0      ; packed descriptor (3–4 bytes of data)
    .word 0      ; quantity
    .word 0      ; player ID

.close
