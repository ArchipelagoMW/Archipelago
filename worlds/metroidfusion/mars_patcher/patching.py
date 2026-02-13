from enum import Enum
from zlib import crc32


class BpsDecodeError(Enum):
    INVALID_BPS = 0
    INVALID_SOURCE = 1
    ALREADY_PATCHED = 2


class BpsDecoder:
    def error(self, err: BpsDecodeError) -> None:
        if err == BpsDecodeError.INVALID_BPS:
            msg = "Invalid BPS file"
        elif err == BpsDecodeError.INVALID_SOURCE:
            msg = "Invalid source file"
        elif err == BpsDecodeError.ALREADY_PATCHED:
            msg = "File already patched"
        raise ValueError(msg)

    def apply_patch(self, patch: bytes, source: bytes, ignore_checksum: bool = False) -> bytearray:
        self.patch = patch
        self.source = source

        # Header
        self.patch_idx = 0
        marker = bytes(self.read_8() for _ in range(4))
        if marker != b"BPS1":
            self.error(BpsDecodeError.INVALID_BPS)
        source_size = self.decode_int()
        target_size = self.decode_int()
        metadata_size = self.decode_int()
        # Ignore metadata
        self.patch_idx += metadata_size

        # Check checksums
        patch_size = len(self.patch)
        if patch_size < self.patch_idx + 12:
            self.error(BpsDecodeError.INVALID_BPS)
        footer_start = patch_size - 12
        if not ignore_checksum:
            source_checksum_expected = self.read_32(footer_start)
            target_checksum_expected = self.read_32(footer_start + 4)
            patch_checksum_expected = self.read_32(footer_start + 8)

            patch_checksum_actual = crc32(self.patch[:-4])
            if patch_checksum_expected != patch_checksum_actual:
                self.error(BpsDecodeError.INVALID_BPS)

            source_checksum_actual = crc32(self.source)
            if source_size != len(source) or source_checksum_expected != source_checksum_actual:
                if (
                    len(source) == target_size
                    and source_checksum_actual == target_checksum_expected
                ):
                    self.error(BpsDecodeError.ALREADY_PATCHED)
                self.error(BpsDecodeError.INVALID_SOURCE)

        # Actions
        output_offset = 0
        source_offset = 0
        target_offset = 0
        target = bytearray()
        while self.patch_idx < footer_start:
            num = self.decode_int()
            length = (num >> 2) + 1
            if output_offset + length > target_size:
                self.error(BpsDecodeError.INVALID_BPS)
            action = num & 3
            if action == 0:
                # Source read
                for _ in range(length):
                    target.append(source[output_offset])
                    output_offset += 1
            elif action == 1:
                # Target read
                for _ in range(length):
                    target.append(self.read_8())
                    output_offset += 1
            elif action == 2:
                # Source copy
                offset = self.decode_int()
                source_offset += (-1 if offset & 1 else 1) * (offset >> 1)
                for _ in range(length):
                    target.append(source[source_offset])
                    output_offset += 1
                    source_offset += 1
            elif action == 3:
                # Target copy
                offset = self.decode_int()
                target_offset += (-1 if offset & 1 else 1) * (offset >> 1)
                for _ in range(length):
                    target.append(target[target_offset])
                    output_offset += 1
                    target_offset += 1
        if self.patch_idx > footer_start:
            self.error(BpsDecodeError.INVALID_BPS)
        if not ignore_checksum:
            target_checksum_actual = crc32(target)
            if target_checksum_expected != target_checksum_actual:
                self.error(BpsDecodeError.INVALID_BPS)
        return target

    def read_8(self) -> int:
        val = self.patch[self.patch_idx]
        self.patch_idx += 1
        return val

    def read_32(self, idx: int) -> int:
        return (
            self.patch[idx]
            | (self.patch[idx + 1] << 8)
            | (self.patch[idx + 2] << 16)
            | (self.patch[idx + 3] << 24)
        )

    def decode_int(self) -> int:
        num = 0
        shift = 1
        while True:
            x = self.read_8()
            num += (x & 0x7F) * shift
            if x & 0x80 != 0:
                return num
            shift <<= 7
            num += shift


class IpsDecodeError(Enum):
    INVALID_IPS = 0
    ABRUPT_IPS_END = 1
    PAST_TARGET_END = 2
    MISSING_EOF = 3


class IpsDecoder:
    def error(self, err: IpsDecodeError, extra: str | None = None) -> None:
        if err == IpsDecodeError.INVALID_IPS:
            msg = "Invalid IPS file"
        elif err == IpsDecodeError.ABRUPT_IPS_END:
            msg = "Abrupt end to IPS file"
        elif err == IpsDecodeError.PAST_TARGET_END:
            msg = "Trying to patch data past end of file"
        elif err == IpsDecodeError.MISSING_EOF:
            msg = "Improperly terminated IPS file"
        if extra is not None:
            msg += ", " + extra
        raise ValueError(msg)

    def apply_patch(self, patch: bytes, target: bytearray) -> None:
        # Check signature
        patch_len = len(patch)
        if patch_len < 8 or patch[:5] != b"PATCH":
            self.error(IpsDecodeError.INVALID_IPS)

        # Records
        idx = 5
        while idx + 2 < patch_len:
            # Check EOF
            if patch[idx : idx + 3] == b"EOF":
                return

            # Get address and size
            addr = (patch[idx] << 16) | (patch[idx + 1] << 8) | patch[idx + 2]
            idx += 3
            if idx + 1 >= patch_len:
                self.error(IpsDecodeError.ABRUPT_IPS_END, "entry cut off before size")
            size = (patch[idx] << 8) | patch[idx + 1]
            idx += 2

            if size == 0:
                # RLE
                if idx + 1 >= patch_len:
                    self.error(IpsDecodeError.ABRUPT_IPS_END, "entry cut off before RLE size")
                rle_size = (patch[idx] << 8) | patch[idx + 1]
                if addr + rle_size > len(target):
                    self.error(IpsDecodeError.PAST_TARGET_END)
                idx += 2
                if idx >= patch_len:
                    self.error(IpsDecodeError.ABRUPT_IPS_END, "entry cut off before RLE byte")
                rle_byte = patch[idx]
                idx += 1
                for i in range(addr, addr + rle_size):
                    target[i] = rle_byte
            else:
                if idx + size > patch_len:
                    self.error(
                        IpsDecodeError.ABRUPT_IPS_END, "entry cut off before end of data block"
                    )
                if addr + size > len(target):
                    self.error(IpsDecodeError.PAST_TARGET_END)
                target[addr : addr + size] = patch[idx : idx + size]
                idx += size

        self.error(IpsDecodeError.MISSING_EOF)
