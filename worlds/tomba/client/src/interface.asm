.BASE 0x80000B150            # Where this code is located

FUN_PLAY_SFX:0x8001FFE8
FUN_PRINT_INFO_MESSAGE:0x80031124

    # Save context
    addiu   sp,sp,-0x24
    sw      ra,0x20(sp)
    sw      s0,0x1c(sp)
    sw      a1,0x18(sp)
    sw      a0,0x14(sp)
    sw      v0,0x10(sp)

    # Check SFX command
    lui     s0,0x8001
    addiu   s0,s0,-0x4ec0
    lbu     a0,0x0(s0)      # Read DAT_SFX_COMMAND
    beq     a0,zero,LAB_SKIP_PLAY_SFX
    nop

    # Play SFX
    sb      zero,0x0(s0)    # Reset DAT_SFX_COMMAND
    jal     FUN_PLAY_SFX
    nop

LAB_SKIP_PLAY_SFX:
    # Check command
    lui     a0,0x8001
    addiu   a0,a0,-0x4ebf
    lbu     a0,0x0(a0)      # Read DAT_COMMAND
    addiu   a1,zero,0x0
    andi    a1,a0,0x1
    beq     a1,zero,LAB_SKIP_COMMAND
    nop

    # Clear stack of found items
    lui     s0,0x8001
    sb      s0,-0x4c00(s0)  # Reset DAT_STACK_SIZE
    andi    a0,a0,0xfe
    sb      a0,-0x4ebf(s0)  # Reset DAT_COMMAND

LAB_SKIP_COMMAND:
    # Check command
    lui     a0,0x8001
    addiu   a0,a0,-0x4ebf
    lbu     a0,0x0(a0)      # Read DAT_COMMAND
    addiu   a1,zero,0x0
    andi    a1,a0,0x2
    beq     a1,zero,LAB_RETURN
    nop

    # Load info message
    lui     t0,0x8001       # Read DAT_MSG_1
    addiu   t0,t0,-0x4ebe
    lbu     a0,0x0(t0)      
    addiu   t1,t0,0x01      # Read DAT_MSG_1
    lbu     a1,0x0(t1)      

    # Display message
    jal     FUN_PRINT_INFO_MESSAGE
    nop
    lui     s0,0x8001
    addiu   s0,s0,-0x4ebf
    lbu     a0,0x0(s0)      # Read DAT_COMMAND
    nop
    andi    a0,a0,0xfd
    nop
    sb      a0,0x0(s0)  # Reset DAT_COMMAND

LAB_RETURN:
    # Restore context
    lw      v0,0x10(sp)
    lw      a0,0x14(sp)
    lw      a1,0x18(sp)
    lw      s0,0x1c(sp)
    lw      ra,0x20(sp)
    addiu   sp,sp,0x24

    # Return to caller
    jr      ra
    nop
