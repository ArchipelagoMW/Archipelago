import pkgutil


def get_patch_bytes(name: str) -> bytes:
    return pkgutil.get_data(__name__, f"{name}.bsdiff4")
