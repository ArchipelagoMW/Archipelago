.n64
.open "temp_working.z64", 0x80200000 - 0x1000

; ==============================
; N64 Gauntlet Legends - MyCode Loader Hook
; ==============================
; 
; Problem: Dynarec emulators can't execute code from ROM addresses
; Solution: Use PI DMA to copy stub from ROM to RAM, then execute from RAM
;
; Hook location: 0x8020025C (after BSS clear, before final init)
; Available space: 14 instructions before epilogue at 0x80200294
;
; Approach:
; 1. Minimal inline DMA copier at hook point (~14 instructions)
; 2. Copies stub from ROM 0xFFF000 to RAM 0x80201800
; 3. Calls stub in RAM
; 4. Stub loads/decompresses MyCode, returns
; 5. Hook executes overwritten instructions and continues
; ==============================

; Stub size: ~82 instructions = 328 bytes, round up to 0x160 (352) for safety
.definelabel STUB_SIZE, 0x160
.definelabel STUB_RAM_ADDR, 0x803F0000
.definelabel STUB_RAM_PHYS, 0x003F0000

; ==============================
; Hook at 0x8020025C
; Overwrites 14 instructions (0x8020025C - 0x80200293)
; ==============================
.org 0x8020025C

    ; === Inline PI DMA: copy stub from ROM to RAM ===
    lui    $t0, 0xA460             ; 1: PI base register

    ; Set PI_DRAM_ADDR = 0x003F0000 (physical RAM destination)
    lui    $t1, 0x003F             ; 2
    sw     $t1, 0x0000($t0)        ; 3

    ; Set PI_CART_ADDR = 0x10FFF000 (physical ROM source)
    lui    $t1, 0x10FF             ; 5
    ori    $t1, $t1, 0xF000        ; 6
    sw     $t1, 0x0004($t0)        ; 7

    ; Set PI_WR_LEN = STUB_SIZE - 1 (triggers DMA)
    li     $t1, STUB_SIZE - 1      ; 8
    sw     $t1, 0x000C($t0)        ; 9

    ; Wait for DMA complete (check bit 0 of PI_STATUS)
@@WaitDMA:
    lw     $t1, 0x0010($t0)        ; 10: Read PI_STATUS
    andi   $t1, $t1, 0x01          ; 11: Check DMA busy bit only
    bnez   $t1, @@WaitDMA          ; 12
    nop                            ; 13 (delay slot - can't optimize, $t1 used)

    ; Jump to stub in RAM
    j      STUB_RAM_ADDR           ; 13: Jump to stub
    nop                            ; 14: delay slot

    ; The next instruction at 0x80200294 is the original epilogue
    ; (lw $ra, 0x20($sp) etc.)

; ==============================
; Stub at ROM offset 0xFFF000
; Gets DMA'd to RAM 0x80201800 before execution
; ==============================
.orga 0xFFF000

LoadMyCodeStub:
    ; Save registers
    addiu  $sp, $sp, -0x20
    sw     $ra, 0x1C($sp)
    sw     $s0, 0x18($sp)
    sw     $s1, 0x14($sp)

    ; Invalidate I-cache for stub region (critical for dynarec!)
    lui    $t0, 0x803F
    li     $t1, STUB_SIZE
@@FlushICache:
    cache  0x10, 0($t0)            ; Hit Invalidate I-cache
    addiu  $t0, $t0, 0x10          ; Cache line = 16 bytes
    addiu  $t1, $t1, -0x10
    bgtz   $t1, @@FlushICache
    nop

    ; MyCode entry location (hardcoded)
    ; = 0x802002E0 + (6 * 0x30) = 0x80200400
    lui    $s1, 0x8020
    ori    $s1, $s1, 0x0400        ; $s1 = MyCode file table entry

    ; PI base in $s0 for reuse
    lui    $s0, 0xA460

    ; ============================================================
    ; Wait for PI ready
    ; ============================================================
@@WaitPI1:
    lw     $t0, 0x0010($s0)
    andi   $t0, $t0, 0x03
    bnez   $t0, @@WaitPI1
    nop

    ; Clear PI status
    li     $t0, 0x02
    sw     $t0, 0x0010($s0)

    ; ============================================================
    ; DMA MyCode from ROM to temp buffer (0x80300000)
    ; ============================================================

    ; PI_DRAM_ADDR = 0x00300000 (physical)
    lui    $t0, 0x0030
    sw     $t0, 0x0000($s0)

    ; PI_CART_ADDR = entry->rom_offset + 0x10000000
    lw     $t0, 0x10($s1)          ; ROM offset from entry
    lui    $t1, 0x1000
    addu   $t0, $t0, $t1
    sw     $t0, 0x0004($s0)

    ; PI_WR_LEN = entry->comp_size (aligned to 2, minus 1)
    lw     $t0, 0x14($s1)          ; Compressed size
    addiu  $t0, $t0, 1
    li     $t1, -2
    and    $t0, $t0, $t1
    addiu  $t0, $t0, -1
    sw     $t0, 0x000C($s0)        ; Triggers DMA

    ; ============================================================
    ; Wait for DMA complete
    ; ============================================================
@@WaitDMA2:
    lw     $t0, 0x0010($s0)
    andi   $t0, $t0, 0x03
    bnez   $t0, @@WaitDMA2
    nop

    ; Clear PI status
    li     $t0, 0x02
    sw     $t0, 0x0010($s0)

    ; Sync and delay for DMA to settle
    sync
    li     $t0, 0x400
@@Delay:
    addiu  $t0, $t0, -1
    bnez   $t0, @@Delay
    nop

    ; ============================================================
    ; Call decompressor
    ; Signature: void decompress(void* src, void* dst)
    ; ============================================================
    lui    $a0, 0x8030             ; Source = 0x80300000 (temp buffer)
    lw     $a1, 0x18($s1)          ; Dest = entry->load_addr
    
    ; Save $s1 on stack (decompressor might clobber it)
    sw     $s1, 0x10($sp)
    
    lui    $t9, 0x8020
    ori    $t9, $t9, 0x16E4        ; Decompressor at 0x802016E4
    jalr   $t9
    nop
    
    ; Restore $s1
    lw     $s1, 0x10($sp)

    ; ============================================================
    ; Clear BSS section
    ; ============================================================
    lw     $t0, 0x24($s1)          ; BSS size
    beqz   $t0, @@SkipBSS
    nop
    
    ; Sanity check: if BSS size > 0x10000, skip (corrupted value)
    lui    $t2, 0x0001
    sltu   $t2, $t2, $t0
    bnez   $t2, @@SkipBSS
    nop
    
    lw     $t1, 0x20($s1)          ; BSS start address

@@ClearBSS:
    sb     $zero, 0($t1)
    addiu  $t0, $t0, -1
    bnez   $t0, @@ClearBSS
    addiu  $t1, $t1, 1

@@SkipBSS:
    ; ============================================================
    ; Execute overwritten code sequence
    ; Original code at 0x8020025C-0x80200290:
    ;   - Set up copy loop (a0=dest, a1=src, v1=count, a2=-1)
    ;   - Copy 0x1E0 bytes from 0x802002B0 to 0xE01301C0
    ;   - Call 0x80002850 with a0=s3
    ; ============================================================
    
    ; Set up copy: src=0x802002B0, dst=0xE01301C0, count=0x1DF
    lui    $a1, 0x8020
    addiu  $a1, $a1, 0x02B0        ; src = 0x802002B0
    lui    $a0, 0xE013
    addiu  $a0, $a0, 0x01C0        ; dst = 0xE01301C0
    li     $v1, 0x1DF              ; count
    li     $a2, -1                 ; terminator

@@CopyLoop:
    lbu    $v0, 0($a1)
    addiu  $a1, $a1, 1
    addiu  $v1, $v1, -1
    sb     $v0, 0($a0)
    bne    $v1, $a2, @@CopyLoop
    addiu  $a0, $a0, 1

    ; Call 0x80002850 with a0 = s3
    jal    0x80002850
    move   $a0, $s3

    ; ============================================================
    ; Restore and jump to epilogue
    ; ============================================================
    lw     $s1, 0x14($sp)
    lw     $s0, 0x18($sp)
    lw     $ra, 0x1C($sp)
    addiu  $sp, $sp, 0x20

    ; Jump to original function epilogue at 0x80200294
    j      0x80200294
    nop

.close
