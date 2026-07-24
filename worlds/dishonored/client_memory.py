import pymem
import pymem.process
from typing import List, Optional

class MemoryHandler:
    def __init__(self, process_name: str = "Dishonored.exe"):
        self.process_name = process_name
        self.pm: Optional[pymem.Pymem] = None
        self.module_base: Optional[int] = None

    def connect(self) -> bool:
        """Tente de se connecter au processus et de récupérer la base du module."""
        try:
            self.pm = pymem.Pymem(self.process_name)
            module = pymem.process.module_from_name(self.pm.process_handle, self.process_name)
            self.module_base = module.lpBaseOfDll
            return True
        except Exception:
            self.pm = None
            self.module_base = None
            return False

    def is_connected(self) -> bool:
        """Vérifie si le processus est toujours ouvert."""
        return self.pm is not None and self.pm.process_handle is not None

    def read_pointer_chain(self, static_offset: int, offsets: List[int]) -> int:
        """Navigue dans la chaîne de pointeurs et renvoie la valeur entière lue."""
        if not self.is_connected() or not self.module_base:
            raise ConnectionError("Non connecté à Dishonored.exe")

        base_address = self.module_base + static_offset
        addr = self.pm.read_uint(base_address)
        
        for offset in offsets[:-1]:
            addr = self.pm.read_uint(addr + offset)
            
        final_address = addr + offsets[-1]
        return self.pm.read_int(final_address)