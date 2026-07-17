.BASE 0x800297b0            # Where this code is located

    # Initialize registers
    lui   $t0, 0x8001       # Load upper 16-bit address for counters
    lbu   $t1, 0xB400($t0)  # $t1 = STACK counter value (from 0x8000B400)

LOOP:
    beq   $s1, $zero, DONE  # If count ($s1) == 0, exit loop
    nop                     # Branch delay slot

    # Calculate current stack write destination
    addi  $t2, $t0, 0xB401  # $t2 = Base STACK address (0x8000B401)
    addu  $t2, $t2, $t1     # $t2 = 0x8000B401 + current stack counter

    # Store Item ID and update tracking
    sb    $s0, 0($t2)       # Store Item ID ($s0) into STACK memory
    addi  $t1, $t1, 1       # Increment STACK counter value
    addi  $s1, $s1, -1      # Decrement loop counter (Count)

    j     LOOP              # Repeat loop
    nop                     # Branch delay slot

DONE:
    # Save the updated STACK counter back to memory
    sb    $t1, 0xB400($t0)  # Update memory at 0x8000B400

    # RETURN
    lw         ra,0x20(sp)
    lw         s1,0x1C(sp)
    lw         s0,0x18(sp)
    addiu      sp,sp,0x28
    jr         ra
    nop
