import pkgutil

# Installing packages from requirements.txt is not supported from frozen AP installs for
# dynamically loaded AP Worlds. This can be simplified if/when the world is merged into AP.
try:
    import dataclass_wizard as dw
except ImportError:
    from . import dataclass_wizard as dw
    

def get_data_file_bytes(name: str) -> bytes:
    return pkgutil.get_data(__name__, f"{name}")
