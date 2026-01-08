import itertools
from typing import List, Tuple, Union

from . import iterators

ByteString = Union[bytes, bytearray, memoryview]


def decompress(data: ByteString):
    it = iter(data)
    planes = (bytearray(), bytearray())

    for plane in range(2):
        read_length = next(it) - 1
        if read_length not in range(2):
            raise ValueError(f"read length = {read_length + 1}")
        if read_length == 0:
            count = next(it)
        else:
            count = next(it) << 8 | next(it)

        while count > 0:
            flag = 0x80 << (read_length * 8)
            if count & flag:
                copied = next(it)
                planes[plane].extend(copied for _ in range(count & (flag - 1)))
            else:
                planes[plane].extend(next(it) for _ in range(count))

            if read_length == 0:
                count = next(it)
            else:
                count = next(it) << 8 | next(it)

    return bytearray(iterators.interleave(*planes))


def compress(data: ByteString):
    t1, t2 = itertools.tee(iterators.batched(data, 2))
    lo = (t[0] for t in t1)
    hi = (t[1] for t in t2)
    compressed = bytearray()

    for plane in (lo, hi):
        # Count runs of the same value
        run_lengths: List[Tuple[int, int]] = []
        count = 1
        for prev, curr in iterators.pairwise(plane):
            if prev == curr:
                count += 1
            else:
                run_lengths.append((prev, count))
                count = 1
        run_lengths.append((curr, count))

        # Try each read length
        buffers = (bytearray(), bytearray())
        for read_length, buffer in enumerate(buffers):
            min_run_length = 3 + read_length
            flag = 0x80 << (8 * read_length)
            max_run_length = flag - 1
            unique = bytearray()

            buffer.append(read_length + 1)

            def flush_unique():
                buffer.extend(len(unique).to_bytes(read_length + 1, 'big'))
                buffer.extend(unique)
                unique.clear()

            for value, run_length in run_lengths:
                while run_length > 0:
                    if run_length >= min_run_length:
                        if len(unique) > 0:  # Preceded by unique values
                            flush_unique()
                        length = flag | min(run_length, max_run_length)
                        buffer.extend(length.to_bytes(read_length + 1, 'big'))
                        buffer.append(value)
                    else:
                        if len(unique) + run_length > max_run_length:  # Total count would be too long
                            flush_unique()
                        unique.extend([value] * run_length)
                    run_length -= max_run_length
            if len(unique) > 0:
                flush_unique()
            buffer.extend((0).to_bytes(read_length + 1, 'big'))
            # Copy the shorter one
            compressed.extend(min(buffers, key=len))

    return bytes(compressed)
