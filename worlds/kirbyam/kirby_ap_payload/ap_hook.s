.syntax unified
.thumb

.global ap_hook_entry
.type ap_hook_entry, %function
.extern ap_poll_mailbox_c

ap_hook_entry:
    // Legacy hook site behavior: run mailbox poll, then replay overwritten
    // instructions from 0x08152696/0x08152698.
    push {r0-r3, lr}

    bl ap_poll_mailbox_c

    pop  {r0-r3}
    pop  {r4}
    mov  lr, r4

    mov  r7, r9
    mov  r6, r8
    bx   lr
