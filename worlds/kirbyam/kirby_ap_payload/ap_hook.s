.syntax unified
.thumb

.global ap_hook_entry
.type ap_hook_entry, %function
.extern ap_poll_mailbox_c

ap_hook_entry:
    // Preserve full low-register context plus LR.
    push {r0-r7, lr}

    // Explicitly preserve high registers used by the overwritten stream.
    // Save r8-r11 via low registers so C call effects cannot leak here.
    mov r0, r8
    mov r1, r9
    mov r2, r10
    mov r3, r11
    push {r0-r3}

    bl ap_poll_mailbox_c

    // Restore preserved high registers first.
    pop  {r0-r3}
    mov r8, r0
    mov r9, r1
    mov r10, r2
    mov r11, r3

    // Restore full low-register context and leave saved LR on stack until return.
    // Using r4 as a temporary here can corrupt live game state at this hook site.
    pop  {r0-r7}

    // Re-run overwritten instructions from 0x08152696/0x08152698:
    mov r7, r9
    mov r6, r8

    pop  {pc}
