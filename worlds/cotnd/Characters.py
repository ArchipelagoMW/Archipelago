
base_chars: list = ['Cadence', 'Melody', 'Aria', 'Dorian', 'Eli', 'Monk', 'Dove', 'Coda', 'Bolt', 'Bard']

amplified_chars: list = ['Nocturna', 'Diamond', 'Mary', 'Tempo']

synchrony_chars: list = ['Klarinetta', 'Chaunter', 'Suzu']

all_chars = base_chars + amplified_chars + synchrony_chars

# Weapons aren't progression
weaponlocked: set = {
    'Melody',
    'Aria',
    'Eli',
    'Dove',
    'Coda',
    'Klarinetta',
    'Suzu',
}

# Only specific armors are progression
ohko: set = {
    'Aria',
    'Coda',
}

ohko_armor: set = {
    'Glass Armor',
    'Heavy Glass Armor',
    'Karate Gi',
}
