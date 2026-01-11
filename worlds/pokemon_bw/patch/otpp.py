
def create(source: str | bytes, destination: str | bytes) -> bytes:
    if type(source) is str:
        with open(source, "rb") as source_file:
            source = source_file.read()
    if type(destination) is str:
        with open(destination, "rb") as destination_file:
            destination = destination_file.read()

    patch_list: list[int] = [
        (destination[i] - source[i] + 256) % 256
        for i in range(min(len(source), len(destination)))
    ]
    if len(destination) > len(source):
        patch_list += [b for b in destination[len(source):]]

    return bytes(patch_list)


def patch(source: str | bytes, otp_patch: str | bytes) -> bytes:
    if type(source) is str:
        with open(source, "rb") as source_file:
            source = source_file.read()
    if type(otp_patch) is str:
        with open(otp_patch, "rb") as otp_patch_file:
            otp_patch = otp_patch_file.read()

    destination_list: list[int] = [
        (source[i] + otp_patch[i]) % 256
        for i in range(min(len(source), len(otp_patch)))
    ]
    if len(otp_patch) > len(source):
        destination_list += [b for b in otp_patch[len(source):]]

    return bytes(destination_list)

