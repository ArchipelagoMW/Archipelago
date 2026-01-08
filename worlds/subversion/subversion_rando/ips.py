# reference: https://zerosoft.zophar.net/ips.php http://justsolve.archiveteam.org/wiki/IPS_(binary_patch_format)


from typing import Union


def patch(original_bytes: Union[bytes, bytearray], patch_bytes: bytes) -> bytearray:
    """ `patch_bytes` is the data in the IPS file """
    if not (patch_bytes[:5] == b"PATCH" and patch_bytes[-3:] == b"EOF"):
        raise ValueError(f"invalid IPS patch: {patch_bytes[:5]!r}, {patch_bytes[-3:]!r}")
    tr = bytearray(original_bytes)
    cursor = 5
    data_limit = len(patch_bytes) - 3  # EOF
    record_begin_limit = data_limit - 5  # offset + size
    while cursor <= record_begin_limit:
        offset = int.from_bytes(patch_bytes[cursor:cursor + 3], "big")
        size = int.from_bytes(patch_bytes[cursor + 3:cursor + 5], "big")
        cursor += 5
        if offset > len(tr):
            print("WARNING: IPS offset is beyond end of data")
            # I don't know whether this should be considered invalid,
            # or whether it should be 0xff or 0 or whatever...
            tr.extend(0 for _ in range(offset - len(tr)))
        if size == 0:
            # RLE encoding
            rle_size = int.from_bytes(patch_bytes[cursor:cursor + 2], "big")
            rle_value = patch_bytes[cursor + 2]
            tr[offset:offset + rle_size] = bytes(rle_value for _ in range(rle_size))
            cursor += 3
        else:
            if cursor + size > data_limit:
                raise ValueError(f"not enough data in IPS file for record at {cursor - 5}: {offset} {size}")
            tr[offset:offset + size] = patch_bytes[cursor:cursor + size]
            cursor += size
    return tr
