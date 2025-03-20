import pkgutil


def get_data_file_bytes(name: str) -> bytes:
    return pkgutil.get_data(__name__, f"{name}")
