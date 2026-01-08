class Patch:
    process = None
    base_address = 0
    current_address = 0
    name = "Unnamed"
    byte_list = b""
    original_bytes = b""
    patch_applied = False

    def __init__(self, name, base_address, process=None, quiet=False):
        self.name = name
        self.base_address = base_address
        self.process = process
        self.quiet = quiet

    def __str__(self):
        return (f"Patch {self.name} from {hex(self.base_address)} to {hex(self.get_patch_end())} ({len(self)} bytes): "
                f"{self.byte_list.hex(' ')}")

    def __len__(self):
        return len(self.byte_list)

    def get_patch_end(self):
        return self.base_address + len(self)

    def apply(self):
        if self.process is None:
            print(f"Failed to apply patch {self.name}. Process has not been specified!")
            return False

        if self.patch_applied:
            print(f"Failed to apply patch {self.name}. Patch already applied!")
            return False

        self.original_bytes = self.process.read_bytes(self.base_address, len(self.byte_list))
        self.process.write_bytes(self.base_address, self.byte_list, len(self.byte_list))

        if self.process.read_bytes(self.base_address, len(self.byte_list)) != self.byte_list:
            print(f"Failed to apply patch {self.name} ({len(self)} length) at {hex(self.base_address)}!")
            return False

        if not self.quiet:
            print(f"Patch {self.name} ({len(self)} length) applied at {hex(self.base_address)} successfully!")
        self.patch_applied = True
        return True

    def revert(self):
        if self.process is None:
            print(f"Failed to apply patch {self.name}, process has not been specified!")
            return False

        if not self.patch_applied:
            print(f"Failed to revert patch {self.name}, patch has not yet been applied!")
            return False

        if self.original_bytes is None or len(self.original_bytes) == 0:
            print(f"OriginalBytes array is blank. Cannot revert patch {self.name}!")
            return False

        self.process.write_bytes(self.base_address, self.original_bytes, len(self.original_bytes))

        if self.process.read_bytes(self.base_address, len(self.original_bytes)) != self.original_bytes:
            print(f"Failed to revert patch {self.name} ({len(self)} length) at {hex(self.base_address)}!")
            return False
        if not self.quiet:
            print(f"Patch {self.name} ({len(self)} length) at {hex(self.base_address)} reverted successfully!")
        self.patch_applied = False
        self.original_bytes = b''
        return True

    def add_bytes(self, bytes_to_add):
        self.byte_list += bytes_to_add
        return self

    def xor_rax_rax(self):
        """
        Exclusive OR's RAX against RAX (clears RAX)
        3 bytes
        """
        return self.add_bytes(b'\x48\x31\xc0')

    def xor_ecx_ecx(self):
        """
        Exclusive OR's ECX against ECX (clears ECX)
        2 bytes
        """
        return self.add_bytes(b'\x31\xc9')

    def xor_edx_edx(self):
        """
        Exclusive OR's EDX against EDX (clears EDX)
        2 bytes
        """
        return self.add_bytes(b'\x31\xd2')

    def xor_r8d_r8d(self):
        """
        Exclusive OR's R8D against R8D (clears R8D)
        3 bytes
        """
        return self.add_bytes(b'\x45\x31\xc0')

    def xor_r9d_r9d(self):
        """
        Exclusive OR's R9D against R9D (clears R9D)
        3 bytes
        """
        return self.add_bytes(b'\x45\x31\xc9')

    def push_rbx(self):
        """
        Push value of RBX to stack
        1 byte
        """
        return self.add_bytes(b'\x53')

    def push_rcx(self):
        """
        Push value of RCX to stack
        1 byte
        """
        return self.add_bytes(b'\x51')

    def push_rdx(self):
        """
        Push value of RDX to stack
        1 byte
        """
        return self.add_bytes(b'\x52')

    def push_rbp(self):
        """
        Push value of RBP to stack
        1 byte
        """
        return self.add_bytes(b'\x55')

    def push_rdi(self):
        """
        Push value of RDI to stack
        1 byte
        """
        return self.add_bytes(b'\x57')

    def push_rsi(self):
        """
        Push value of RSI to stack
        1 byte
        """
        return self.add_bytes(b'\x56')

    def push_r8(self):
        """
        Push value of R8 to stack
        2 bytes
        """
        return self.add_bytes(b'\x41\x50')

    def push_r9(self):
        """
        Push value of R9 to stack
        2 bytes
        """
        return self.add_bytes(b'\x41\x51')

    def push_r14(self):
        """
        Push value of R14 to stack
        2 bytes
        """
        return self.add_bytes(b'\x41\x56')

    def push_r15(self):
        """
        Push value of R15 to stack
        2 bytes
        """
        return self.add_bytes(b'\x41\x57')

    def call_near(self, address):
        """
        Calls a nearby function, returns when finished
        5 bytes
        """
        diff = address - (self.get_patch_end() + 5)
        print('diff: {} - {} = {}'.format(hex(address), hex(self.get_patch_end() + 5), hex(diff)))
        self.add_bytes(b'\xe8' + diff.to_bytes(4, 'little', signed=True))
        return self

    def call_far(self, address):
        """
        Calls a far-away function using a 64-bit address
        16 bytes
        """
        return self.add_bytes(b'\xff\x15\x02\x00\x00\x00\xeb\x08' + address.to_bytes(8, 'little', signed=True))

    def call_rax(self):
        """
        Calls a function whose address is stored in RAX
        2 bytes
        """
        return self.add_bytes(b'\xff\xd0')

    def nop(self, count=1):
        """
        Does nothing. Specify count to add multiple NOP bytes
        <x> bytes
        """
        return self.add_bytes(b'\x90' * count)

    def mov_rbx(self, value):
        """
        Moves a 64-bit value to RBX
        10 bytes
        """
        return self.add_bytes(b'\x48\xbb' + value.to_bytes(8, 'little'))

    def mov_ecx(self, value):
        """
        Moves a 32-bit value to ECX
        5 bytes
        """
        return self.add_bytes(b'\xb9' + value.to_bytes(4, 'little'))

    def mov_rcx(self, value):
        """
        Moves a 64-bit value to RCX
        10 bytes
        """
        return self.add_bytes(b'\x48\xb9' + value.to_bytes(8, 'little'))

    def mov_edx(self, value):
        """
        Moves a 32-bit value to EDX
        5 bytes
        """
        return self.add_bytes(b'\xba' + value.to_bytes(4, 'little'))

    def mov_rdx(self, value):
        """
        Moves a 64-bit value to RDX
        10 bytes
        """
        return self.add_bytes(b'\x48\xba' + value.to_bytes(8, 'little'))

    def mov_r8(self, value):
        """
        Moves a 64-bit value to R8
        10 bytes
        """
        return self.add_bytes(b'\x49\xb8' + value.to_bytes(8, 'little'))

    def mov_rdi(self, value):
        """
        Moves a 64-bit value to RDI
        10 bytes
        """
        return self.add_bytes(b'\x48\xbf' + value.to_bytes(8, 'little'))

    def mov_from_absolute_address_to_r8(self, address):
        """
        Moves a 64-bit value from the absolute 64-bit address to R8
        13 bytes
        """
        return self.mov_from_absolute_address_to_rax(address).mov_rax_to_r8()

    def mov_from_absolute_address_to_r9(self, address):
        """
        Moves a 64-bit value from the absolute 64-bit address to R9
        13 bytes
        """
        return self.mov_from_absolute_address_to_rax(address).mov_rax_to_r9()

    def mov_r9(self, value):
        """
        Moves a 64-bit value to R9
        10 bytes
        """
        return self.add_bytes(b'\x49\xb9' + value.to_bytes(8, 'little'))

    def mov_cl(self, value):
        """
        Moves an 8-bit value to CL
        2 bytes
        """
        return self.add_bytes(b'\xb1' + value.to_bytes(1, 'little'))

    def mov_edi(self, value):
        """
        Moves a 32-bit value to EDI
        5 bytes
        """
        return self.add_bytes(b'\xbf' + value.to_bytes(4, 'little'))

    def push(self, value):
        """
        Pushes an 8-bit value to the stack
        2 bytes
        """
        return self.add_bytes(b'\x6a' + value.to_bytes(1, 'little'))

    def lea_r8_value(self, value):
        """
        Loads a value from a 32-bit address to R8
        7 bytes
        """
        return self.add_bytes(b'\x4c\x8d\x05' + value.to_bytes(4, 'little'))

    def lea_eax_rdi_minus1(self):
        """
        Loads a 32-bit value from the address at RDI - 0x1 to EAX
        3 bytes
        """
        return self.add_bytes(b'\x8d\x47\xff')

    def lea_rax_addr(self, address):
        """
        Loads absolute address to RAX
        7 bytes
        """
        return self.add_bytes(b'\x48\x8d\x05' + (address - self.base_address - 7).to_bytes(4, 'little'))

    def cmp_al_al(self):
        """
        Compares AL to AL. Sets zero flag if value is 0
        2 bytes
        """
        return self.add_bytes(b'\x38\xc0')

    def cmp_al1_byte(self, value):
        """
        Compares AL1 to an 8-bit value. Sets appropriate flags
        2 bytes
        """
        return self.add_bytes(b'\x3c' + value.to_bytes(1, 'little'))

    def cmp_ebx(self, value):
        """
        Compare a 32-bit value to EBX
        6 bytes
        """
        return self.add_bytes(b'\x81\xfb' + value.to_bytes(4, 'little'))

    def cmp_eax(self, value):
        """
        Compares an 8-bit value to EAX
        3 bytes
        """
        return self.add_bytes(b'\x83\xf8' + value.to_bytes(1, 'little'))

    def cmp_rax(self, value):
        """
        Compare an 8-bit value to RAX
        4 bytes
        """
        return self.add_bytes(b'\x48\x83\xf8' + value.to_bytes(1, 'little'))

    def ja_near(self, address):
        """
        Jump if last comparison first operand was greater than second. Jumps to nearby address
        6 bytes
        """
        start = self.get_patch_end() + 6
        diff = address - start
        # print('diff: {} - {} = {}'.format(hex(address), hex(start), hex(diff)))
        self.add_bytes(b'\x0f\x87' + diff.to_bytes(4, 'little'))
        return self

    def jmp_short_offset(self, offset):
        """
        Jumps a specific number of bytes from the NEXT instruction
        2 bytes
        """
        diff = offset
        self.add_bytes(b'\xeb' + diff.to_bytes(4, 'little', signed=True))
        return self

    def jmp_near_offset(self, offset):
        """
        Jumps a specific number of bytes from the NEXT instruction
        5 bytes
        """
        diff = offset
        self.add_bytes(b'\xe9' + diff.to_bytes(4, 'little', signed=True))
        return self

    def jmp_near_address(self, offset):
        """
        Jumps to a specific nearby address
        5 bytes
        """
        self.add_bytes(b'\xe9' + offset.to_bytes(4, 'little', signed=True))
        return self

    def jmp_far(self, address):
        """
        Jumps to a faraway 64-bit address
        14 bytes
        """
        return self.add_bytes(b'\xff\x25\x00\x00\x00\x00' + address.to_bytes(8, 'little', signed=True))

    def jl_short(self, offset):
        """
        Jumps an 8-bit distance if first operand was less than the second operand in the last CMP
        2 bytes
        """
        return self.add_bytes(b'\x7c' + offset.to_bytes(1, 'little'))

    def jl_near(self, offset):
        """
        Jumps a 32-bit distance if first operand was less than the second operand in the last CMP
        6 bytes
        """
        return self.add_bytes(b'\x0f\x8c' + offset.to_bytes(4, 'little'))

    def jl_far(self, address):
        """
        Jumps to a specific 64-bit address if first operand was less than the second operand in the last CMP
        21 bytes
        """
        return self.jl_short(5).jmp_near_offset(0x0e).jmp_far(address)

    def jnl_short(self, offset):
        """
        Jumps an 8-bit distance if first operand was NOT less than the second operand in the last CMP
        2 bytes
        """
        return self.add_bytes(b'\x7d' + offset.to_bytes(1, 'little'))

    def jnl_near(self, offset):
        """
        Jumps a 32-bit distance if first operand was NOT less than the second operand in the last CMP
        6 bytes
        """
        return self.add_bytes(b'\x0f\x8d' + offset.to_bytes(4, 'little'))

    def jnl_far(self, address):
        """
        Jumps to a specific 64-bit address if first operand was NOT less than the second operand in the last CMP
        21 bytes
        """
        return self.jnl_short(5).jmp_near_offset(0x0e).jmp_far(address)

    def je_near(self, distance):
        """
        Jump an 8-bit or 32-bit distance if the operands of the previous CMP were the same
        2 or 6 bytes
        """
        if distance - 2 > 0x80:
            return self.add_bytes(b'\x0f\x84' + (distance - 6).to_bytes(4, 'little'))
        else:
            return self.add_bytes(b'\x74' + (distance - 2).to_bytes(1, 'little'))

    def je_far(self, address):
        """
        Jump to a 64-bit address if the operands of the previous CMP were the same
        21 bytes
        """
        return self.je_near(7).jmp_near_offset(0x0e).jmp_far(address)

    def mov_to_al(self, value):
        """
        Moves an 8-bit value to AL
        2 bytes
        """
        return self.add_bytes(b'\xb0' + value.to_bytes(1, 'little'))

    def mov_to_ax(self, value):
        """
        Moves a 16-bit value to EAX
        4 bytes
        """
        return self.add_bytes(b'\x66\xb8' + value.to_bytes(2, 'little'))

    def mov_to_eax(self, value):
        """
        Moves a 32-bit value to EAX
        5 bytes
        """
        return self.add_bytes(b'\xb8' + value.to_bytes(4, 'little'))

    def mov_to_rax(self, value):
        """
        Moves a 64-bit value to RAX
        10 bytes
        """
        return self.add_bytes(b'\x48\xb8' + value.to_bytes(8, 'little'))

    def mov_from_absolute_address_to_eax(self, value):
        """
        Moves a 32-bit value from an absolute 64-bit address to EAX
        9 bytes
        """
        return self.add_bytes(b'\xa1' + value.to_bytes(8, 'little'))

    def mov_from_absolute_address_to_rax(self, value):
        """
        Moves a 64-bit value from an absolute 64-bit address to RAX
        10 bytes
        """
        return self.add_bytes(b'\x48\xa1' + value.to_bytes(8, 'little'))

    def mov_eax_pointer_contents_to_ecx(self):
        """
        Moves a 32-bit value from the 32-bit address specified in EAX to ECX
        2 bytes
        """
        return self.add_bytes(b'\x8b\x08')

    def mov_eax_pointer_contents_to_edx(self):
        """
        Moves a 32-bit value from the 32-bit address specified in EAX to EDX
        2 bytes
        """
        return self.add_bytes(b'\x8b\x10')

    def mov_rax_pointer_contents_to_rcx(self):
        """
        Moves a 64-bit value from the 64-bit address specified in RAX to RCX
        3 bytes
        """
        return self.add_bytes(b'\x48\x8b\x08')

    def mov_rax_pointer_contents_to_rdx(self):
        """
        Moves a 64-bit value from the 64-bit address specified in RAX to RDX
        3 bytes
        """
        return self.add_bytes(b'\x48\x8b\x10')

    def mov_al_to_address_in_rbx(self):
        """
        Moves an 8-bit value from AL to the address specified in RBX
        2 bytes
        """
        return self.add_bytes(b'\x88\x03')

    def mov_ax_to_address_in_rbx(self):
        """
        Moves a 16-bit value from AX to the address specified in RBX
        3 bytes
        """
        return self.add_bytes(b'\x66\x89\x03')

    def mov_eax_to_address_in_rbx(self):
        """
        Moves a 32-bit value from EAX to the address specified in RBX
        2 bytes
        """
        return self.add_bytes(b'\x89\x03')

    def mov_rax_to_address_in_rbx(self):
        """
        Moves a 64-bit value from RAX to the address specified in RBX
        3 bytes
        """
        return self.add_bytes(b'\x48\x89\x03')

    def mov_rax_to_rdx(self):
        """
        Moves a 64-bit value from RAX to RDX
        3 bytes
        """
        return self.add_bytes(b'\x48\x8b\xd0')

    def mov_rax_to_r8(self):
        """
        Moves a 64-bit value from RAX to R8
        3 bytes
        """
        return self.add_bytes(b'\x4c\x8b\xc0')

    def mov_rax_to_r9(self):
        """
        Moves a 64-bit value from RAX to R9
        3 bytes
        """
        return self.add_bytes(b'\x4c\x8b\xc8')

    def movq_rax_to_xmm6(self):
        """
        Moves a 64-bit value from RAX to XMM6
        5 bytes
        """
        return self.add_bytes(b'\x66\x48\x0f\x6e\xf0')

    def movq_rax_to_xmm7(self):
        """
        Moves a 64-bit value from RAX to XMM7
        5 bytes
        """
        return self.add_bytes(b'\x66\x48\x0f\x6e\xf8')

    def mov_to_rsp_offset(self, offset, value):
        """
        Moves a 32-bit value to the stack at a location specified with an 8-bit offset from RSP
        7 bytes
        """
        return self.add_bytes(b'\xc7\x44\x24' + offset.to_bytes(1, 'little') + value.to_bytes(4, 'little'))

    def mov_rax_to_rsp_offset(self, offset):
        """
        Moves a 64-bit value from RAX to the stack at a location specified with an 8-bit offset from RSP
        5 bytes
        """
        return self.add_bytes(b'\x48\x89\x44\x24' + offset.to_bytes(1, 'little'))

    def jmp_rax(self):
        """
        Jumps to a 64-bit absolute address stored in RAX
        2 bytes
        """
        return self.add_bytes(b'\xff\xe0')

    def add_rsp(self, value):
        """
        Increases RSP by a 32-bit value, reducing the size of the stack
        7 bytes
        """
        return self.add_bytes(b'\x48\x81\xc4' + value.to_bytes(4, 'little'))

    def dec_rsp(self, value):
        """
        Decreases RSP by a 32-bit value, increasing the size of the stack
        7 bytes
        """
        return self.add_bytes(b'\x48\x81\xec' + value.to_bytes(4, 'little'))

    def pop_rbx(self):
        """
        Pops the top value off the stack to RBX
        1 byte
        """
        return self.add_bytes(b'\x5b')

    def pop_rcx(self):
        """
        Pops the top value off the stack to RCX
        1 byte
        """
        return self.add_bytes(b'\x59')

    def pop_rdx(self):
        """
        Pops the top value off the stack to RDX
        1 byte
        """
        return self.add_bytes(b'\x5a')

    def pop_r8(self):
        """
        Pops the top value off the stack to R8
        2 bytes
        """
        return self.add_bytes(b'\x41\x58')

    def pop_r9(self):
        """
        Pops the top value off the stack to R9
        2 bytes
        """
        return self.add_bytes(b'\x41\x59')

    def pop_rbp(self):
        """
        Pops the top value off the stack to RBP
        1 byte
        """
        return self.add_bytes(b'\x5d')

    def pop_rdi(self):
        """
        Pops the top value off the stack to RDI
        1 byte
        """
        return self.add_bytes(b'\x5f')

    def pop_rsi(self):
        """
        Pops the top value off the stack to RSI
        1 byte
        """
        return self.add_bytes(b'\x5e')

    def pop_r12(self):
        """
        Pops the top value off the stack to R12
        2 bytes
        """
        return self.add_bytes(b'\x41\x5c')

    def pop_r13(self):
        """
        Pops the top value off the stack to R13
        2 bytes
        """
        return self.add_bytes(b'\x41\x5d')

    def pop_r14(self):
        """
        Pops the top value off the stack to R14
        2 bytes
        """
        return self.add_bytes(b'\x41\x5e')

    def pop_r15(self):
        """
        Pops the top value off the stack to R15
        2 bytes
        """
        return self.add_bytes(b'\x41\x5f')

    def sub_rax_from_rsp(self):
        """
        Subtracts the 64-bit value in RAX from RSP, increasing the size of the stack
        3 bytes
        """
        return self.add_bytes(b'\x48\x29\xc4')

    def call_via_rax(self, address):
        """
        Calls an absolute 64-bit address by moving that address to RAX first
        12 bytes
        """
        return self.mov_to_rax(address).call_rax()
