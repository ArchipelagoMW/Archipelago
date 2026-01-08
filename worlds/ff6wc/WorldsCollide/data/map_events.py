from ..data.map_event import MapEvent, LongMapEvent
from ..event.event import *

class MapEvents():
    EVENT_COUNT = 1164
    DATA_START_ADDR = 0x040342
    DATA_END_ADDR = 0x041A0F

    def __init__(self, rom):
        self.rom = rom
        self.read()

    def read(self):
        self.events = []

        for event_index in range(self.EVENT_COUNT):
            event_data_start = self.DATA_START_ADDR + event_index * MapEvent.DATA_SIZE
            event_data = self.rom.get_bytes(event_data_start, MapEvent.DATA_SIZE)

            new_event = MapEvent()
            new_event.from_data(event_data)
            self.events.append(new_event)

    def write(self):
        for event_index, event in enumerate(self.events):
            event_data = event.to_data()
            event_data_start = self.DATA_START_ADDR + event_index * MapEvent.DATA_SIZE
            # Assert that the address being written doesn't go beyond the expected end point
            assert(event_data_start < self.DATA_END_ADDR)
            self.rom.set_bytes(event_data_start, event_data)

    def mod(self):
        pass

    def get_event(self, search_start, search_end, x, y):
        for event in self.events[search_start:search_end + 1]:
            if event.x == x and event.y == y:
                return event
        raise IndexError(f"get_event: could not find event at {x} {y}")

    def add_event(self, index, new_event):
        self.events.insert(index, new_event)
        self.EVENT_COUNT += 1

    def delete_event(self, search_start, search_end, x, y):
        for event in self.events[search_start:search_end + 1]:
            if event.x == x and event.y == y:
                self.events.remove(event)
                self.EVENT_COUNT -= 1
                return
        raise IndexError("delete_event: could not find event at {x} {y}")

    def print_range(self, start, count):
        for offset in range(count):
            self.events[start + offset].print()

    def print(self):
        for event in self.events:
            event.print()


class LongMapEvents:
    EVENT_COUNT = 0
    POINTER_START_ADDR_LONG = 0x320000  # Bank $F2.  Set dynamically?
    DATA_START_ADDR_LONG = 0x320342
    verbose = False

    def __init__(self, rom):
        self.rom = rom
        self.read()

        # Modify the ROM to add long events
        self.addLongEvents()

    def read(self):
        # by default, no LongMapEvents in the rom
        self.events = []

        for event_index in range(self.EVENT_COUNT):
            event_data_start = self.DATA_START_ADDR_LONG + event_index * LongMapEvent.DATA_SIZE
            event_data = self.rom.get_bytes(event_data_start, LongMapEvent.DATA_SIZE)

            new_event = LongMapEvent()
            new_event.from_data(event_data)
            self.events.append(new_event)

    def write(self):
        for event_index, event in enumerate(self.events):
            event_data = event.to_data()
            event_data_start = self.DATA_START_ADDR_LONG + event_index * LongMapEvent.DATA_SIZE
            self.rom.set_bytes(event_data_start, event_data)

    def mod(self):
        pass

    def get_event(self, search_start, search_end, x, y):
        for event in self.events[search_start:search_end + 1]:
            if event.x == x and event.y == y:
                return event
        raise IndexError(f"get_event: could not find event at {x} {y}")

    def add_event(self, index, new_event):
        self.events.insert(index, new_event)
        self.EVENT_COUNT += 1

    def delete_event(self, search_start, search_end, x, y):
        for event in self.events[search_start:search_end + 1]:
            if event.x == x and event.y == y:
                self.events.remove(event)
                self.EVENT_COUNT -= 1
                return
        raise IndexError("delete_event: could not find event at {x} {y}")

    def print_range(self, start, count):
        for offset in range(count):
            self.events[start + offset].print()

    def print(self):
        for event in self.events:
            event.print()

    def addLongEvents(self):
        # Modify the ROM to check for long events in the field program & include long event pointers
        # (Following Lenophis' code implementing long events, the event equivalent of long exits)
        ROM_OFFSET = 0xC00000

        # long event triggers
        src = [
            # CHECK IF THERE IS A LONG EVENT ON THIS MAP
            asm.LDA(0x82, asm.DIR), # C08C7B:    LDA $82   [A5 82]
            asm.ASL(),           # C08C7D:    ASL A     [0A]
            asm.TAX(),           # C08C7E:    TAX       [AA]
            asm.LDA(self.POINTER_START_ADDR_LONG + ROM_OFFSET + 2, asm.LNG_X),
                                 # C08C7F:    LDA $F40002, X; load second pointer   [BF XX XX XX]
            asm.STA(0x1e, asm.DIR), # C08C83:    STA $1E   [85 1E]
            asm.LDA(self.POINTER_START_ADDR_LONG + ROM_OFFSET, asm.LNG_X),
                                 # C08C85:    LDA $F40000, X; load first pointer    [BF XX XX XX]
            asm.TAX(),           # C08C89:    TAX;  put first pointer address in X  [AA]
            asm.CMP(0x1e, asm.DIR), # C08C8A:    CMP $1E  [C5 1E]
            asm.BEQ("DO_NORMAL_TRIGGERS"), # C08C8C:    BEQ C08CE8; branch if they do match, we don't have a trigger in this map
                                 # Jump forward 0x5a lines?  Check this.    [F0 5A]

            # FOUND A LONG EVENT TRIGGER ON THE MAP.  CHECK VERTICAL OR HORIZONTAL.
            "ITERATE_LONG_EVENT", # ASM label for checking each long event
            asm.TDC(),           # C08C8E:    TDC           [7B]
            asm.SEP(0x20),       # C08C8F:    SEP  # $20    [E2 20]
            asm.STZ(0x26, asm.DIR), # C08C91:    STZ $26       [64 26]
            asm.LDA(self.POINTER_START_ADDR_LONG + ROM_OFFSET + 5, asm.LNG_X),
                                 # C08C93:    LDA $F40002, X; load trigger's length [BF XX XX XX]
                                 # NOTE: the trigger horiz/vert value is the 5th bit
                                 #       (to maintain similarity to normal events)
            asm.BMI("IS_VERTICAL_EVENT"), # C08C97:    BMI C08CBB; branch if vertical    [30 22]


            # HORIZONTAL TRIGGER CASE
            asm.STA(0x1a, asm.DIR), # C08C99:    STA $1A       [85 1A]
            asm.LDA(self.POINTER_START_ADDR_LONG + ROM_OFFSET + 1, asm.LNG_X),
                                 # C08C9B:    LDA $F40001, X; load trigger's Y coordinate   [BF XX XX XX]
            asm.CMP(0xb0, asm.DIR), # C08C9F:    CMP $B0; compare to current Y position    [C5 B0]
            asm.BNE("SKIP_THIS_EVENT"),       # C08CA1:    BNE C08CDD; if they don't match, check the next trigger  [D0 3A]
            asm.LDA(0xaf, asm.DIR), # C08CA3:    LDA $AF; load current X position  [A5 AF]
            asm.SEC(),           # C08CA5:    SEC (set carry flag)     [38]
            asm.SBC(self.POINTER_START_ADDR_LONG + ROM_OFFSET, asm.LNG_X),
                                 # C08CA6:    SBC $F40000, X; subtract trigger's X coordinate    [FF XX XX XX]
            asm.BCC("SKIP_THIS_EVENT"),       # C08CAA:    BCC C08CDD (branch if carry clear) [90 31]
            asm.STA(0x26, asm.DIR), # C08CAC:    STA $26       [85 26]
            asm.LDA(self.POINTER_START_ADDR_LONG + ROM_OFFSET, asm.LNG_X),
                                 # C08CAE:    LDA $F40000, X; load trigger's X coordinate        [BF XX XX XX]
            asm.CLC(),           # C08CB2:    CLC (clear carry flag)    [18]
            asm.ADC(0x1a, asm.DIR), # C08CB3:    ADC $1A; add in length    [65 1A]
            asm.CMP(0xaf, asm.DIR), # C08CB5:    CMP $AF; compare to current X position    [C5 AF]
            asm.BCS("TRIGGER_LONG_EVENT"),    # C08CB7:    BCS C08CEC; trigger the event (branch if carry set) [B0 33]
            asm.BRA("SKIP_THIS_EVENT"),       # C08CB9:    BRA C08CDD (branch always) [80 22]

            # VERTICAL LONG EVENT TRIGGER CHECK
            "IS_VERTICAL_EVENT",  # ASM label for vertical event
            asm.AND(0x7f, asm.IMM8), # C08CBB:    AND  # $7F  ; remove vertical flag       [29 7F]
            asm.STA(0x1a, asm.DIR), # C08CBD:    STA $1A       [85 1A]
            asm.LDA(self.POINTER_START_ADDR_LONG + ROM_OFFSET, asm.LNG_X),
                                 # C08CBF:    LDA $F40000, X; load trigger's X coordinate       [BF XX XX XX]
            asm.CMP(0xaf, asm.DIR), # C08CC3:    CMP $AF; compare to current X position    [C5 AF]
            asm.BNE("SKIP_THIS_EVENT"),       # C08CC5:    BNE C08CDD  (branch if not equal)         [D0 16]
            asm.LDA(0xb0, asm.DIR), # C08CC7:    LDA $B0       [A5 B0]
            asm.SEC(),           # C08CC9:    SEC           [38]
            asm.SBC(self.POINTER_START_ADDR_LONG + ROM_OFFSET + 1, asm.LNG_X),
                                 # C08CCA:    SBC $F40001, X; subtract trigger's Y coordinate   [FF XX XX XX]
            asm.BCC("SKIP_THIS_EVENT"),       # C08CCE:    BCC C08CDD (branch if carry clear)        [90 0D]
            asm.STA(0x26, asm.DIR), # C08CD0:    STA $26       [85 26]
            asm.LDA(self.POINTER_START_ADDR_LONG + ROM_OFFSET + 1, asm.LNG_X),
                                 # C08CD2:    LDA $F40001, X; load trigger's Y coordinate       [BF XX XX XX]
            asm.CLC(),           # C08CD6:    CLC               [18]
            asm.ADC(0x1a, asm.DIR), # C08CD7:    ADC $1A; add in length    [65 1A]
            asm.CMP(0xb0, asm.DIR), # C08CD9:    CMP $B0; compare to current Y position?   [C5 B0]
            asm.BCS("TRIGGER_LONG_EVENT"),       # C08CDB:    BCS C08CEC; trigger the event (branch if carry set) [B0 0F]

            # ITERATE TO NEXT TRIGGER
            "SKIP_THIS_EVENT",  # ASM label for moving on to the next trigger
            asm.REP(0x21),       # C08CDD:    REP  # $21 (reset status bit)  [C2 21]
            asm.TXA(),           # C08CDF:    TXA  (transfer X to A)         [8A]
            asm.ADC(0x0006, asm.IMM16), # C08CE0:    ADC  # $0006 (add with carry) [69 06 00]
            asm.TAX(),           # C08CE3:    TAX  (transfer A to X)         [AA]
            asm.CPX(0x1e, asm.DIR), # C08CE4:    CPX $1E (compare X)            [E4 1E]
            asm.BNE("ITERATE_LONG_EVENT"),       # C08CE6:    BNE C08C8E   [D0 A6]

            # MOVE ON TO NORMAL TRIGGERS
            "DO_NORMAL_TRIGGERS", # ASM label for moving on to normal triggers
            asm.LDA(0x82, asm.DIR), # C08CE8:    LDA $82; otherwise let's do normal event triggers [A5 82]
            asm.ASL(),           # C08CEA:    ASL A     [0A]
            asm.RTS(),           # C08CEB:    RTS       [60]

            # TRIGGER THE EVENT: see e.g. C0/BCD3 for normal events.
            "TRIGGER_LONG_EVENT", # ASM label for triggering long event
            asm.REP(0x20),       # C08CEC:    REP  # $20  ; (reset status bits)        [C2 20]
                                 # 'we must copy the whole address, not just the first byte :P'
            asm.LDA(self.POINTER_START_ADDR_LONG + ROM_OFFSET + 2, asm.LNG_X),
                                 # C08CEE:    LDA $F40003, X; lower 2 bytes of trigger address  [BF XX XX XX]
                                 # Data structure:  [x, y, trig_lo, trig_mid, trig_hi, d&size]
                                 # (Lenophis used: [x, y, d&size, trigger])
            asm.STA(0xe5, asm.DIR),     # C08CF2:    STA $E5   (store A to memory)     [85 E5]
            asm.STA(0x05f4, asm.ABS),   # C08CF4:    STA $05F4                    [8D F4 05]
            asm.SEP(0x20),           # C08CF7:    SEP  # $20 (set status bit 0x20)  [E2 20]
            asm.TDC(),               # C08CF9:    TDC  (Transfer DP to 16 bit A)    [7B]
            asm.STA(0x0871, asm.ABS_Y), # C08CFA:    STA $0871, Y  (store A to mem, indexed by Y)  [99 71 08]
            asm.STA(0x0873, asm.ABS_Y), # C08CFD:    STA $0873, Y                  [99 73 08]
            asm.SEP(0x20),           # C08D00:    SEP  # $20                    [E2 20]
            asm.STA(0x087E, asm.ABS_Y), # C08D02:    STA $087E, Y                  [99 7E 08]
            asm.LDA(0x01, asm.IMM8),    # C08D05:    LDA  # $01                    [A9 01]
            asm.STA(0x078e, asm.ABS),   # C08D07:    STA $078E                     [8D 8E 07]
            asm.STA(0x05c7, asm.ABS),   # C08D0A:    STA $05C7                     [8D C7 05]
            asm.LDA(self.POINTER_START_ADDR_LONG + ROM_OFFSET + 4, asm.LNG_X),
                                # C08D0D:    LDA $F40005, X; load high byte of trigger address  [BF XX XX XX]
                                # Data structure:  [x, y, trig_lo, trig_mid, trig_hi, d&size]
            asm.CLC(),          # C08D11:    CLC   [18]
            # # C08D12:; JMP C0ED8E   I think we can skip this?
            asm.ADC(0xca, asm.IMM8),    # C0ED8E:    ADC  # $CA                    [69 CA]
            asm.STA(0xe7, asm.DIR),     # C0ED90:    STA $E7                       [85 E7]
            asm.STA(0x05f6, asm.ABS),   # C0ED92:    STA $05F6                     [8D F6 05]
            asm.LDX(0x00, asm.DIR),     # C0ED95:    LDX $00                       [A6 00]
                                # Note: standard event code uses LDX(0x0000, 'IMM16') [A2 00 00]
            asm.STX(0x0594, asm.ABS),   # C0ED97:    STX $0594                     [8E 94 05]
            asm.LDA(0xca, asm.IMM8),    # C0ED9A:    LDA  # $CA                    [A9 CA]
            asm.STA(0x0596, asm.ABS),   # C0ED9C:    STA $0596                     [8D 96 05]
                                # Note: Lenophis skips "LDA #$01, STA $05C7" (see C0/BD06)
                                # This is an efficiency, it's accomplished on line C08D0A.
            asm.LDX(0x0003, asm.IMM16), # C0ED9F:    LDX  # $0003                  [A2 03 00]
            asm.STX(0xe8, asm.DIR),     # C0EDA2:    STX $E8                       [86 E8]
            asm.LDA(0x087c, asm.ABS_Y), # C0EDA4:    LDA $087C, Y                  [B9 7C 08]
            asm.STA(0x087d, asm.ABS_Y), # C0EDA7:    STA $087D, Y                  [99 7D 08]
            asm.LDA(0x04, asm.IMM8),    # C0EDAA:    LDA  # $04                    [A9 04]
            asm.STA(0x087c, asm.ABS_Y), # C0EDAC:    STA $087C, Y                  [99 7C 08]
            asm.JSR(0x7e08, asm.ABS),   # C0EDAF:    JSR $7E08 (jump to subroutine) [20 08 7E]
            asm.JSR(0x2fed, asm.ABS),   # C0EDB2:    JSR $2FED                     [20 ED 2F]

            asm.REP(0x20),              # C0EDB5:    REP  # $20                    [C2 20]
            asm.BRA("DO_NORMAL_TRIGGERS")  # C0EDB7:    BRA C08CE8; do normal event triggers now  [80 AB]
        ]

        space = Write(Bank.C0, src, "Long event program code")

        hook = Reserve(0x0bcaa, 0x0bcac, "Hook for long event program code", field.NOP())
        hook.write(
            asm.JSR(space.start_address, asm.ABS)
        )

        pointspace = Reserve(self.POINTER_START_ADDR_LONG, self.DATA_START_ADDR_LONG, 'Long Event Pointers', 0x0)

        if self.verbose:
            print('Added long event program at: ' + str(hex(space.start_address)) + ' -- ', str(hex(space.end_address)) )

