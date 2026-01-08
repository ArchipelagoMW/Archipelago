MIN_MATCH_SIZE = 3
MIN_WINDOW_SIZE = 1
MAX_MATCH_SIZE = (1 << 4) - 1 + MIN_MATCH_SIZE
MAX_WINDOW_SIZE = (1 << 12) - 1 + MIN_WINDOW_SIZE


def decomp_rle(input: bytes, idx: int) -> tuple[bytearray, int]:
    """
    Decompresses RLE data and returns it with the size of the compressed data.
    """
    src_start = idx
    passes = bytearray()
    half: int | None = None
    # For each pass
    for p in range(2):
        if p == 1:
            half = len(passes)
        num_bytes = input[idx]
        idx += 1
        while True:
            amount = None
            compare = None
            if num_bytes == 1:
                amount = input[idx]
                compare = 0x80
            else:
                # num_bytes == 2
                amount = (input[idx] << 8) | input[idx + 1]
                compare = 0x8000
            idx += num_bytes

            if amount == 0:
                break

            if (amount & compare) != 0:
                # Compressed
                amount %= compare
                val = input[idx]
                idx += 1
                while amount > 0:
                    passes.append(val)
                    amount -= 1
            else:
                # Uncompressed
                while amount > 0:
                    passes.append(input[idx])
                    idx += 1
                    amount -= 1

    # Each pass must be equal length
    if half is None:
        raise ValueError("half was not assigned")
    if len(passes) != half * 2:
        raise ValueError("Passes are not equal length")

    # Combine passes to get output
    output = bytearray(len(passes))
    for i in range(half):
        output[i * 2] = passes[i]
        output[i * 2 + 1] = passes[half + i]

    # Return bytes and compressed size
    comp_size = idx - src_start
    return output, comp_size


def comp_rle(input: bytes) -> bytearray:
    """
    Compresses data using RLE.
    """

    # Inner helper functions
    def write_len(arr: bytearray, val: int, size: int) -> None:
        if size == 0:
            arr.append(val)
        else:
            arr.append(val >> 8)
            arr.append(val & 0xFF)

    def add_unique(arr: bytearray, unique: bytearray, size: int) -> None:
        write_len(arr, len(unique), size)
        arr += unique
        unique.clear()

    output = bytearray()
    # Do two passes for low and high bytes
    for p in range(2):
        # Get counts of consecutive values
        values = bytearray()
        counts = []

        prev = input[p]
        values.append(prev)
        count = 1

        for i in range(p + 2, len(input), 2):
            val = input[i]
            if val == prev:
                count += 1
            else:
                values.append(val)
                counts.append(count)
                prev = val
                count = 1
        counts.append(count)

        # Try each read length (1 or 2)
        shortest: bytearray | None = None
        for r in range(2):
            temp = bytearray()
            min_run_len = 3 + r
            flag = 0x80 << (8 * r)
            max_run_len = flag - 1
            unique = bytearray()

            # Write number of bytes to read
            temp.append(r + 1)

            # For each value and its count
            for i in range(len(values)):
                count = counts[i]
                # If the value's count is long enough for a run
                if count >= min_run_len:
                    # If the value is preceded by unique values
                    if len(unique) > 0:
                        add_unique(temp, unique, r)
                    # Add run length and value (multiple times if over max run length)
                    while count > 0:
                        curr_len = min(count, max_run_len)
                        len_flag = curr_len + flag
                        write_len(temp, len_flag, r)
                        temp.append(values[i])
                        count -= curr_len
                # If the value's count is too short for a run
                else:
                    # If the total count would be too long for a run
                    if len(unique) + count > max_run_len:
                        add_unique(temp, unique, r)
                    for _ in range(count):
                        unique.append(values[i])
            # Check if there were unique values at the end
            if len(unique) > 0:
                add_unique(temp, unique, r)
            # Write ending zero(s)
            temp.append(0)
            if r == 1:
                temp.append(0)
            if shortest is None or len(temp) < len(shortest):
                shortest = temp
        if shortest is None:
            raise ValueError("shortest was not assigned")
        output += shortest
    return output


def decomp_lz77(input: bytes, idx: int) -> tuple[bytearray, int]:
    """Decompresses LZ77 data and returns it with the size of the compressed data."""
    # Check for 0x10 flag
    if input[idx] != 0x10:
        raise ValueError("Missing 0x10 flag")

    # Get length of decompressed data
    remain = input[idx + 1] | (input[idx + 2] << 8) | (input[idx + 3] << 16)
    output = bytearray([0] * remain)

    # Check for valid data size
    if remain == 0:
        raise ValueError("Invalid data size")

    start = idx
    idx += 4
    dst = 0

    # Decompress
    while True:
        cflag = input[idx]
        idx += 1

        for _ in range(8):
            if (cflag & 0x80) == 0:
                # Uncompressed
                output[dst] = input[idx]
                idx += 1
                dst += 1
                remain -= 1
            else:
                # Compressed
                amount_to_copy = (input[idx] >> 4) + MIN_MATCH_SIZE
                window = ((input[idx] & 0xF) << 8) + input[idx + 1] + MIN_WINDOW_SIZE
                idx += 2
                remain -= amount_to_copy

                for _ in range(amount_to_copy):
                    output[dst] = output[dst - window]
                    dst += 1

            if remain <= 0:
                if remain < 0:
                    raise ValueError("Too many bytes copied at end")
                comp_size = idx - start
                return output, comp_size
            cflag <<= 1


def comp_lz77(input: bytes) -> bytearray:
    """Compresses data using LZ77."""
    length = len(input)
    idx = 0
    longest_matches = _find_longest_matches(input)

    # Write start of data
    output = bytearray()
    output.append(0x10)
    output.append(length & 0xFF)
    output.append((length >> 8) & 0xFF)
    output.append(length >> 16)

    while idx < length:
        # Get index of new compression flag
        flag = len(output)
        output.append(0)

        for i in range(8):
            # Find longest match at current position
            _match = longest_matches.get(idx)
            if _match is not None:
                # Compressed
                match_idx, match_len = _match
                match_offset = idx - match_idx - MIN_WINDOW_SIZE
                output.append(((match_len - MIN_MATCH_SIZE) << 4) | (match_offset >> 8))
                output.append(match_offset & 0xFF)
                output[flag] |= 0x80 >> i
                idx += match_len
            else:
                # Uncompressed
                output.append(input[idx])
                idx += 1

            # Check if at end
            if idx >= length:
                return output

    raise RuntimeError("LZ77 compression error")


def _find_longest_matches(input: bytes) -> dict[int, tuple[int, int]]:
    length = len(input)
    triplets: dict[int, list[int]] = {}
    longest_matches: dict[int, tuple[int, int]] = {}

    for i in range(length - 2):
        # Get triplet at current position
        triplet = input[i] | (input[i + 1] << 8) | (input[i + 2] << 16)

        # Check if triplet has no match
        indexes = triplets.get(triplet)
        if indexes is None:
            triplets[triplet] = [i]
            continue

        window_start = max(i - MAX_WINDOW_SIZE, 0)
        max_size = min(MAX_MATCH_SIZE, length - i)
        longest_len = 0
        longest_idx = -1

        # Skip first index if one byte behind current position
        j = len(indexes) - 1
        if indexes[j] >= i - 1:
            j -= 1

        # Try each index to find the longest match
        while j >= 0:
            idx = indexes[j]
            # Stop if past window
            if idx < window_start:
                break

            # Find length of match
            match_len = MIN_MATCH_SIZE
            while match_len < max_size:
                if input[idx + match_len] != input[i + match_len]:
                    break
                match_len += 1

            # Update longest match
            if match_len > longest_len:
                longest_len = match_len
                longest_idx = idx

                # Stop looking if max size
                if longest_len == max_size:
                    break

            j -= 1

        indexes.append(i)
        if longest_len >= MIN_MATCH_SIZE:
            longest_matches[i] = (longest_idx, longest_len)

    return longest_matches
