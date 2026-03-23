.syntax unified
.thumb

.global ap_hook_entry
.type ap_hook_entry, %function
.extern ap_poll_mailbox_c

ap_hook_entry:
    // Save r0-r3 and LR.
    push {r0-r3, lr}

    bl ap_poll_mailbox_c

    // Restore r0-r3 and leave the saved LR on the stack until return.
    // Using r4 as a temporary here corrupts live game state at the hook site.
    pop  {r0-r3}

    // Re-run overwritten instructions from 0x08152696/0x08152698:
    mov r7, r9
    mov r6, r8

    pop  {pc}
