# -*- coding: utf-8 -*-

from enum import Enum


class PtraceCommandsEnum(Enum):
    """
    Enum with commands for ptrace() system call.

    Read more about ptrace commands here:
    https://man7.org/linux/man-pages/man2/ptrace.2.html
    """
    # Turns the calling thread into a tracee. The thread continues to
    # run (doesn't enter ptrace-stop). A common practice is to follow
    # the PTRACE_TRACEME with "raise(SIGSTOP);" and allow the parent,
    # which is our tracer now, to observe our signal-delivery-stop.
    PTRACE_TRACEME = 0

    # PEEKTEXT and PEEKDATE read a word at the address addr in the
    # tracee's memory, returning the word as the result of the ptrace()
    # call. Linux does not have separate text and data address spaces,
    # so these two requests are currently equivalent.
    PTRACE_PEEKTEXT = 1
    PTRACE_PEEKDATA = 2

    # Read a word at offset addr in the tracee's USER area, which holds
    # the registers and other information about the process. The word is
    # returned as the result of the ptrace() call. Typically, the offset
    # must be word-aligned, though this might vary by architecture.
    PTRACE_PEEKUSER = 3

    # POKETEXT and POKEDATA copy the word data to the address addr in the
    # tracee's memory. These two requests are currently equivalent.
    PTRACE_POKETEXT = 4
    PTRACE_POKEDATA = 5

    # Copy the word data to offset addr in the tracee's USER area. As
    # for PTRACE_PEEKUSER, the offset must typically be word-aligned. In
    # order to maintain the integrity of the kernel, some modifications
    # to the USER area are disallowed.
    PTRACE_POKEUSER = 6

    # Restart the stopped tracee process. If data is nonzero, it is
    # interpreted as the number of a signal to be delivered to the tracee;
    # otherwise, no signal is delivered. Thus, for example, the tracer can
    # control whether a signal sent to the tracee is delivered or not.
    PTRACE_CONT = 7

    # Send the tracee a SIGKILL to terminate it. This operation is deprecated;
    # do not use it! Instead, send a SIGKILL directly using kill(2) or tgkill(2).
    # The problem with PTRACE_KILL is that it requires the tracee to be in
    # signal-delivery-stop, otherwise it may not work (i.e., may complete
    # successfully but won't kill the tracee). By contrast, sending a SIGKILL
    # directly has no such limitation.
    PTRACE_KILL = 8

    # GETREGS and GETFPREGS copy the tracee's general-purpose or floating-point
    # registers, respectively, to the address data in the tracer. Note that SPARC
    # systems have the meaning of data and addr reversed; that is, data is ignored
    # and the registers are copied to the address addr. PTRACE_GETREGS and
    # PTRACE_GETFPREGS are not present on all architectures.
    PTRACE_GETREGS = 12
    PTRACE_GETFPREGS = 14

    # SETREGS and SETFPREGS modify the tracee's general-purpose or floating-point
    # registers, respectively, from the address data in the tracer. As for
    # PTRACE_POKEUSER, some general-purpose register modifications may be
    # disallowed. Note that SPARC systems have the meaning of data and addr
    # reversed; that is, data is ignored and the registers are copied from the
    # address addr. PTRACE_SETREGS and PTRACE_SETFPREGS are not present on all
    # architectures.
    PTRACE_SETREGS = 13
    PTRACE_SETFPREGS = 15

    # Attach to the process specified in pid, making it a tracee of the calling
    # process. The tracee is sent a SIGSTOP, but will not necessarily have
    # stopped by the completion of this call; use waitpid(2) to wait for the
    # tracee to stop. See the "Attaching and detaching" subsection for additional
    # information. Permission to perform a PTRACE_ATTACH is governed by a ptrace
    # access mode PTRACE_MODE_ATTACH_REALCREDS check.
    PTRACE_ATTACH = 16

    # Restart the stopped tracee as for PTRACE_CONT, but first detach from it.
    # Under Linux, a tracee can be detached in this way regardless of which
    # method was used to initiate tracing.
    PTRACE_DETACH = 17

    # SINGLESTEP and SYSCALL restart the stopped tracee as for PTRACE_CONT,
    # but arrange for the tracee to be stopped at the next entry to or exit
    # from a system call, or after execution of a single instruction,
    # respectively. The tracee will also, as usual, be stopped upon receipt
    # of a signal. From the tracer's perspective, the tracee will appear to
    # have been stopped by receipt of a SIGTRAP. So, for PTRACE_SYSCALL, for
    # example, the idea is to inspect the arguments to the system call at the
    # first stop, then do another PTRACE_SYSCALL and inspect the return value
    # of the system call at the second stop. The data argument is treated as
    # for PTRACE_CONT.
    PTRACE_SINGLESTEP = 9
    PTRACE_SYSCALL = 24

    # Set ptrace options from data. Data is interpreted as a bit mask of options,
    # which are specified by the following flags:
    # - PTRACE_O_EXITKILL
    # - PTRACE_O_TRACECLONE
    # - PTRACE_O_TRACEFORK
    # - PTRACE_O_TRACESYSGOOD
    # - PTRACE_O_TRACEVFORK
    # - PTRACE_O_TRACEVFORKDONE
    # - PTRACE_O_TRACESECCOMP
    # - PTRACE_O_SUSPEND_SECCOMP
    PTRACE_SETOPTIONS = 0x4200
