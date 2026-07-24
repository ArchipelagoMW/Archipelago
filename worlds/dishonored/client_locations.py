from dataclasses import dataclass
from typing import List, Callable

@dataclass
class MemoryCheck:
    id: int                          # ID Archipelago
    name: str                        # Nom lisible pour les logs
    static_offset: int               # Offset de base du module
    offsets: List[int]               # Chaîne d'offsets
    condition: Callable[[int], bool] # Règle de validation (lambda)
    
# --- DICTIONNAIRE / LISTE DES CHECKS DU JEU ---
GAME_CHECKS: List[MemoryCheck] = [
    # 1. Check sur les pièces
    MemoryCheck(
        id=990001,
        name="150 Pièces accumulées",
        static_offset=0x105F628,
        offsets=[0x59C, 0xC8, 0x10],
        condition=lambda val: val >= 150
    ),
    
    # 2. Check sur les Runes (exemple avec d'autres offsets)
    MemoryCheck(
        id=990002,
        name="Première Rune ramassée",
        static_offset=0x105F628,
        offsets=[0x59C, 0xC8, 0x10],
        condition=lambda val: val >= 1
    ),
    
    # 3. Check sur un drapeau d'état / Bitflag (ex: Porte déverrouillée = 1)
    MemoryCheck(
        id=990003,
        name="Clé du bagne utilisée",
        static_offset=0x105F628,
        offsets=[0x59C, 0xC8, 0x10],
        condition=lambda val: val == 1
    ),
]