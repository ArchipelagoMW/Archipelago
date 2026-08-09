"""The pickupsanity stub: hand-encoded MIPS, so machine-check it.

This stub is the one piece of the world that cannot be exercised by running
the client - it executes on the PS1, inside a patched disc. Everything about
it that CAN be checked without an emulator is checked here, because the
alternative is finding out from a tester.

v2 (2026-08-09) makes the stub conditional. v1 ended in an unconditional
`j 0x800543C8` (consume, no vanilla effect), and since the collect dispatcher
indexes by ITEM KIND, that ate enemy-dropped health too - reported as "health
pickups from enemies don't work, but they start working once you get all the
pickups in that stage" (the "later" being `_pickup_dispatch_apply` handing the
vanilla handlers back once a stage was fully checked).

The test the stub applies is `obj+0x10 != 0` plus a record content check. It
is sound because the object allocator at 0x8002C938 zeroes 156 bytes of the
pool slot on every allocation and obj+0x10 sits inside that wipe, so only the
placement spawner (`sw s2,0x10(s1)` @ 0x8002B2B8) ever leaves a pointer there
and no stale pointer can survive slot reuse.
"""
import os
import struct
import unittest

from capstone import Cs, CS_ARCH_MIPS, CS_MODE_MIPS32, CS_MODE_LITTLE_ENDIAN

import worlds.mmx5.client as c
from worlds.mmx5 import disc, pickups

BASE = disc.PICKUPSANITY_STUB_ADDR
TABLE = disc.PICKUPSANITY_VANILLA_TABLE_ADDR
CONSUME_TAIL = 0x800543C8
# Capstone renders `beq $x,$zero` as `beqz` and `bne $x,$zero` as `bnez`. An
# audit keyed on ("beq","bne") silently skips exactly the branches this stub
# leans on - which is how the first version of this check passed vacuously.
BRANCHES = {"beq", "bne", "beqz", "bnez"}
LOADS = {"lw", "lbu", "lb", "lhu", "lh"}


def _disasm():
    md = Cs(CS_ARCH_MIPS, CS_MODE_MIPS32 | CS_MODE_LITTLE_ENDIAN)
    code = disc.PICKUPSANITY_STUB[:TABLE - BASE]
    return list(md.disasm(code, BASE))


class TestPickupsanityStubEncoding(unittest.TestCase):
    def test_every_word_decodes(self) -> None:
        insns = _disasm()
        self.assertEqual(len(insns), (TABLE - BASE) // 4,
                         "a word failed to decode - the blob is malformed")

    def test_no_load_delay_slot_violations(self) -> None:
        """R3000 has no load interlock.

        The value a load produces is NOT available to the very next
        instruction. v3..v6 of the sibling stub shipped this bug and recorded
        every field one store late; it took a live session to find.
        """
        insns = _disasm()
        bad = []
        for a, b in zip(insns, insns[1:]):
            if a.mnemonic not in LOADS:
                continue
            dest = a.op_str.split(",")[0].strip()
            ops = [t.strip() for t in
                   b.op_str.replace("(", ",").replace(")", "").split(",")]
            reads = ops if b.mnemonic in BRANCHES else ops[1:]
            if dest in reads:
                bad.append(f"{a.mnemonic} {a.op_str} -> {b.mnemonic} {b.op_str}")
        self.assertEqual(bad, [])

    def test_branches_land_on_instructions_inside_the_stub(self) -> None:
        insns = _disasm()
        found = 0
        for i in insns:
            if i.mnemonic not in BRANCHES:
                continue
            found += 1
            target = int(i.op_str.split(",")[-1].strip(), 16)
            self.assertGreaterEqual(target, BASE, f"{i.mnemonic} escapes the stub")
            self.assertLess(target, TABLE,
                            f"{i.mnemonic} branches into the jump table")
            self.assertEqual((target - BASE) % 4, 0, "branches mid-instruction")
        self.assertEqual(found, 4, "expected 4 conditional branches")

    def test_jump_table_matches_the_vanilla_handlers(self) -> None:
        off = TABLE - BASE
        for n, kind in enumerate(disc.CONSUMABLE_KINDS):
            word = struct.unpack_from("<I", disc.PICKUPSANITY_STUB, off + n * 4)[0]
            self.assertEqual(word, disc.VANILLA_DISPATCH[kind],
                             f"kind {kind:#04x} would enter the wrong handler")

    def test_client_and_disc_agree_on_the_vanilla_handlers(self) -> None:
        """Two copies of the same addresses exist: the client writes them into
        the dispatch table at runtime, the stub jumps through them on the PS1.
        They must not drift."""
        self.assertEqual(c.VANILLA_DISPATCH, disc.VANILLA_DISPATCH)

    def test_stub_fits_the_measured_free_space(self) -> None:
        # 0x800776A0..0x800778F8 is zero in the vanilla EXE: 102 words from
        # this stub's base. Verified against a disc in TestStubAgainstDisc.
        self.assertLessEqual(len(disc.PICKUPSANITY_STUB), 102 * 4)
        self.assertEqual(len(disc.PICKUPSANITY_STUB) % 4, 0)

    def test_tail_still_consumes_without_vanilla_effect(self) -> None:
        # Placed pickups must keep the v1 behaviour exactly: the client owns
        # every grant, and the item respawns until the server confirms.
        self.assertIn(struct.pack("<I", (0x02 << 26) | ((CONSUME_TAIL >> 2) & 0x03FFFFFF)),
                      disc.PICKUPSANITY_STUB)


def _stub_decides(recptr: int, kind: int, record: bytes | None):
    """Model of the stub's routing. Mirrors the encoded logic 1:1.

    Returns 'record' (placed pickup: write a ring record, consume),
    'vanilla' (hand to the real handler - this is what heals enemy drops),
    or 'consume' (kind outside 0x02..0x08).
    """
    if recptr == 0:
        decision = "vanilla"
    elif record[1] != 0x2F:
        decision = "vanilla"
    elif record[2] != ((kind + 0x1E) & 0xFF):
        decision = "vanilla"
    else:
        return "record"
    if decision == "vanilla" and not (0x2 <= kind <= 0x8):
        return "consume"
    return decision


class TestStubRouting(unittest.TestCase):
    """The decision table, stated as behaviour rather than as instructions."""

    def test_enemy_drop_goes_to_the_vanilla_handler(self) -> None:
        # THE BUG. A dropped item is allocated from the wiped pool and never
        # gets a record pointer, so obj+0x10 is 0. It must heal.
        for kind in disc.CONSUMABLE_KINDS:
            self.assertEqual(_stub_decides(0, kind, None), "vanilla",
                             f"kind {kind:#04x} drop would still be eaten")

    def test_placed_pickup_is_recorded(self) -> None:
        for kind in disc.CONSUMABLE_KINDS:
            rec = bytes([0x00, 0x2F, kind + 0x1E, 0x00, 0, 0, 0, 0])
            self.assertEqual(_stub_decides(0x800FBD3C, kind, rec), "record")

    def test_wrong_minor_is_not_treated_as_a_record(self) -> None:
        rec = bytes([0x00, 0x19, 0x20, 0x00, 0, 0, 0, 0])
        self.assertEqual(_stub_decides(0x800FBD3C, 0x2, rec), "vanilla")

    def test_id_kind_mismatch_is_not_treated_as_a_record(self) -> None:
        # A pointer at a real record for a DIFFERENT item type.
        rec = bytes([0x00, 0x2F, 0x26, 0x00, 0, 0, 0, 0])   # 1-UP record
        self.assertEqual(_stub_decides(0x800FBD3C, 0x2, rec), "vanilla")

    def test_out_of_range_kind_still_just_consumes(self) -> None:
        self.assertEqual(_stub_decides(0, 0x0B, None), "consume")

    def test_every_real_pickup_id_maps_into_the_consumable_kinds(self) -> None:
        """The id<->kind half of the content test, checked against all 32 real
        pickups without needing a disc. A record that failed this would make
        its check permanently unsendable - the one failure mode that must be
        impossible rather than unlikely."""
        for stage, area, idx, iid, name in pickups.PICKUPS:
            kind = iid - 0x1E
            self.assertIn(kind, disc.CONSUMABLE_KINDS,
                          f"{name}: id {iid:#04x} is not a consumable kind")
            rec = bytes([0x00, 0x2F, iid, 0x00, 0, 0, 0, 0])
            self.assertEqual(
                _stub_decides(pickups.record_addr(stage, area, idx), kind, rec),
                "record", f"{name} would stop being recorded")


@unittest.skipUnless(os.environ.get("MMX5_DISC"),
                     "set MMX5_DISC to a Megaman X5 .bin to verify against one")
class TestStubAgainstDisc(unittest.TestCase):
    """The two premises that only a real disc can confirm."""

    @classmethod
    def setUpClass(cls) -> None:
        sector, payload, poff = 2352, 2048, 0x18
        with open(os.environ["MMX5_DISC"], "rb") as f:
            f.seek(23432 * sector)
            raw = f.read(261 * sector)
        cls.exe = b"".join(raw[i * sector + poff: i * sector + poff + payload]
                           for i in range(261))
        cls.load = struct.unpack_from("<I", cls.exe, 0x18)[0]
        with open(os.environ["MMX5_DISC"], "rb") as f:
            f.seek(23693 * sector)
            raw = f.read(676 * sector)
        cls.rock = b"".join(raw[i * sector + poff: i * sector + poff + payload]
                            for i in range(676))
        cls.chunks = []
        for i in range(64):
            sec, size = struct.unpack_from("<II", cls.rock, i * 8)
            if sec == 0 and size == 0:
                break
            cls.chunks.append((sec, size))

    def _at(self, addr, n, chunk_id=None):
        if addr < 0x800EE970:
            off = addr - self.load + 0x800
            return self.exe[off:off + n]
        sec, _size = self.chunks[chunk_id]
        off = sec * 2048 + (addr - 0x800EE970)
        return self.rock[off:off + n]

    def test_the_region_it_writes_into_is_actually_free(self) -> None:
        off = BASE - self.load + 0x800
        region = self.exe[off:off + len(disc.PICKUPSANITY_STUB)]
        self.assertEqual(region, bytes(len(region)),
                         "the stub would overwrite real EXE code")

    def test_content_test_accepts_every_real_record_on_the_disc(self) -> None:
        """Read all 32 placement records off the disc and route each one.

        There are only 32, so 'a real pickup is rejected and its check becomes
        unsendable' is eliminated by exhaustion rather than by sampling.
        """
        loader = 0x8006FD50 - self.load + 0x800
        for stage, area, idx, iid, name in pickups.PICKUPS:
            addr = pickups.record_addr(stage, area, idx)
            chunk_id = (self.exe[loader + stage * 2 + area]
                        if addr >= 0x800EE970 else None)
            rec = self._at(addr, 8, chunk_id)
            self.assertEqual(rec[1], 0x2F, f"{name}: minor {rec[1]:#04x} != 0x2F")
            self.assertEqual(rec[2], iid, f"{name}: id on disc disagrees")
            self.assertEqual(_stub_decides(addr, iid - 0x1E, rec), "record",
                             f"{name} would stop being recorded")

    def test_allocator_still_wipes_the_record_pointer(self) -> None:
        """The whole fix rests on obj+0x10 being zero for anything the
        placement spawner did not create. That is true because the allocator
        zeroes 0x9C bytes of the slot; if this ever stops holding, the enemy
        drop test becomes unsound."""
        off = 0x8002C974 - self.load + 0x800
        # addiu $v1, $zero, 0x9b  -  the wipe counter
        self.assertEqual(self.exe[off:off + 4], bytes.fromhex("9b000324"))
        self.assertLess(0x10, 0x9B + 1, "obj+0x10 is outside the wipe")
